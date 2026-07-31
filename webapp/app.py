from __future__ import annotations

import asyncio
import json
import logging
import os
import secrets
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from webapp.generator import (
    GenerationError,
    export_gif,
    generate_svg,
    render_review_image,
    review_and_maybe_fix,
)
from webapp.storage import Store


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = Path(os.getenv("DATA_DIR", ROOT / "webapp-data")).resolve()
MAX_STORAGE_BYTES = int(os.getenv("MAX_STORAGE_BYTES", str(5 * 1024**3)))
MAX_QUEUE = int(os.getenv("MAX_QUEUE", "100"))
CONCURRENCY = int(os.getenv("GENERATION_CONCURRENCY", "10"))
EXPORT_CONCURRENCY = int(os.getenv("EXPORT_CONCURRENCY", "2"))
ENABLE_VISUAL_REVIEW = os.getenv("ENABLE_VISUAL_REVIEW", "false").lower() in {"1", "true", "yes"}
TRUSTED_PROXIES = {item.strip() for item in os.getenv("TRUSTED_PROXIES", "127.0.0.1,::1").split(",")}

store = Store(DATA_ROOT, MAX_STORAGE_BYTES)
queue: asyncio.Queue["Task"] = asyncio.Queue(maxsize=MAX_QUEUE)
admission_lock = asyncio.Lock()
active_work_ids: set[str] = set()
inflight_work_ids: set[str] = set()
export_slots: asyncio.Semaphore | None = None
log = logging.getLogger("clawd-workshop")


@dataclass
class Task:
    work_id: str
    prompt: str
    client_ip: str
    previous_svg: str | None = None


class CreateRequest(BaseModel):
    prompt: str = Field(max_length=500)

    @field_validator("prompt")
    @classmethod
    def clean_prompt(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("请至少输入 2 个字")
        return value


class ReviseRequest(CreateRequest):
    edit_token: str = Field(min_length=32, max_length=128)


class DeleteRequest(BaseModel):
    edit_token: str = Field(min_length=32, max_length=128)


def client_ip(request: Request) -> str:
    direct = request.client.host if request.client else "unknown"
    if direct in TRUSTED_PROXIES:
        forwarded = request.headers.get("x-real-ip", "").strip()
        if forwarded and len(forwarded) <= 64:
            return forwarded
    return direct


async def process(task: Task) -> None:
    try:
        row = store.get(task.work_id)
        if not row:
            return
        store.set_status(task.work_id, "processing")
        svg_path, gif_path = store.paths(task.work_id)
        prompts = store.prompts(task.work_id)
        svg = await generate_svg(task.prompt, task.previous_svg, prompts)
        loop = asyncio.get_running_loop()
        if ENABLE_VISUAL_REVIEW:
            preview = await loop.run_in_executor(None, render_review_image, svg)
            svg = await review_and_maybe_fix(svg, task.prompt, preview)
        svg_path.write_text(svg, encoding="utf-8")
        store.set_status(task.work_id, "export_queued")
        if export_slots is None:
            raise RuntimeError("GIF exporter is not initialized")
        async with export_slots:
            store.set_status(task.work_id, "exporting")
            await loop.run_in_executor(None, export_gif, svg_path, gif_path)
        store.complete(task.work_id, svg_path, gif_path)
    except GenerationError as exc:
        try:
            store.set_status(task.work_id, "failed", str(exc)[:800])
        except Exception:
            log.exception("could not mark work %s failed", task.work_id)
    except Exception as exc:
        log.exception("work %s failed", task.work_id)
        try:
            store.set_status(task.work_id, "failed", "生成失败，请稍后重试")
        except Exception:
            log.exception("could not mark work %s failed", task.work_id)


async def worker(worker_id: int) -> None:
    while True:
        task = await queue.get()
        active_work_ids.add(task.work_id)
        try:
            await process(task)
        except asyncio.CancelledError:
            raise
        except Exception:
            log.exception("worker %s recovered after task %s failed", worker_id, task.work_id)
        finally:
            active_work_ids.discard(task.work_id)
            inflight_work_ids.discard(task.work_id)
            queue.task_done()


@asynccontextmanager
async def lifespan(_: FastAPI):
    global export_slots
    store.fail_incomplete()
    export_slots = asyncio.Semaphore(EXPORT_CONCURRENCY)
    workers = [asyncio.create_task(worker(index)) for index in range(CONCURRENCY)]
    yield
    for item in workers:
        item.cancel()
    await asyncio.gather(*workers, return_exceptions=True)


app = FastAPI(title="Clawd 表情工坊", docs_url=None, redoc_url=None, lifespan=lifespan)


@app.middleware("http")
async def harden(request: Request, call_next):
    length = request.headers.get("content-length")
    if length and (not length.isdigit() or int(length) > 16_384):
        return JSONResponse({"detail": "请求内容过大"}, status_code=413)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
    )
    return response


@app.get("/health")
def health():
    return {"ok": True, "queue": queue.qsize(), "active": len(active_work_ids), "model": os.getenv("GENERATION_MODEL", "deepseek-v4-flash")}


@app.post("/api/works")
async def create_work(body: CreateRequest, request: Request):
    ip = client_ip(request)
    work_id = uuid.uuid4().hex
    edit_token = secrets.token_urlsafe(32)
    prompt = body.prompt
    async with admission_lock:
        if queue.full():
            raise HTTPException(503, "当前排队人数过多，请稍后再试")
        store.create(work_id, edit_token, ip, prompt)
        queue.put_nowait(Task(work_id, prompt, ip))
        inflight_work_ids.add(work_id)
    return {"id": work_id, "edit_token": edit_token, "status": "queued"}


@app.post("/api/works/{work_id}/revise")
async def revise_work(work_id: str, body: ReviseRequest, request: Request):
    ip = client_ip(request)
    prompt = body.prompt
    row = store.get(work_id)
    svg_path = store.files / work_id / "clawd.svg"
    if not row or row["edit_hash"] != store.token_hash(body.edit_token) or not svg_path.exists():
        raise HTTPException(403, "修改凭证无效")
    previous_svg = svg_path.read_text(encoding="utf-8")
    async with admission_lock:
        if work_id in inflight_work_ids:
            raise HTTPException(409, "这个作品正在修改，请等待完成")
        if queue.full():
            raise HTTPException(503, "当前排队人数过多，请稍后再试")
        if not store.queue_revision(work_id, body.edit_token, prompt, ip):
            raise HTTPException(403, "修改凭证无效")
        queue.put_nowait(Task(work_id, prompt, ip, previous_svg))
        inflight_work_ids.add(work_id)
    return {"id": work_id, "status": "queued"}


@app.post("/api/works/{source_id}/remix")
async def remix_work(source_id: str, body: CreateRequest, request: Request):
    source = store.get(source_id)
    source_svg_path = store.files / source_id / "clawd.svg"
    if not source or source["status"] != "ready" or not source_svg_path.exists():
        raise HTTPException(404, "原作品不存在或已被自动清理")
    previous_svg = source_svg_path.read_text(encoding="utf-8")
    ip = client_ip(request)
    work_id = uuid.uuid4().hex
    edit_token = secrets.token_urlsafe(32)
    prompt = body.prompt
    async with admission_lock:
        if queue.full():
            raise HTTPException(503, "当前排队人数过多，请稍后再试")
        store.create(work_id, edit_token, ip, prompt)
        queue.put_nowait(Task(work_id, prompt, ip, previous_svg))
        inflight_work_ids.add(work_id)
    return {"id": work_id, "edit_token": edit_token, "status": "queued"}


@app.get("/api/works/{work_id}")
def work_status(work_id: str):
    row = store.get(work_id)
    if not row:
        raise HTTPException(404, "作品不存在或已被自动清理")
    result = {"id": work_id, "status": row["status"], "updated_at": row["updated_at"]}
    if row["status"] == "queued":
        result["position"] = store.queue_position(work_id)
    if row["status"] == "failed":
        result["error"] = row["error"] or "生成失败"
    if row["status"] in {"export_queued", "exporting"}:
        result["svg_url"] = f"/files/{work_id}/clawd.svg"
    if row["status"] == "ready":
        result.update({
            "svg_url": f"/files/{work_id}/clawd.svg",
            "gif_url": f"/files/{work_id}/clawd.gif?v={row['updated_at']}",
        })
    return result


@app.delete("/api/works/{work_id}", status_code=204)
async def delete_work(work_id: str, body: DeleteRequest):
    async with admission_lock:
        if work_id in inflight_work_ids:
            raise HTTPException(409, "作品正在生成或修改，请稍后再删除")
        result = store.delete_owned(work_id, body.edit_token)
    if result == "not_found":
        raise HTTPException(404, "作品不存在或已被自动清理")
    if result == "forbidden":
        raise HTTPException(403, "删除凭证无效")
    if result == "busy":
        raise HTTPException(409, "作品正在生成或修改，请稍后再删除")
    return Response(status_code=204)


@app.get("/api/gallery")
def gallery(offset: int = 0, limit: int = 48):
    limit = max(1, min(limit, 60))
    offset = max(0, offset)
    items = store.list_ready(limit, offset)
    return [{
        "id": item["id"],
        "created_at": item["created_at"],
        "updated_at": item["updated_at"],
        "gif_url": f"/files/{item['id']}/clawd.gif?v={item['updated_at']}",
    } for item in items]


@app.get("/api/gallery-page")
def gallery_page_api(
    limit: int = 48,
    before_updated_at: str | None = None,
    before_id: str | None = None,
):
    limit = max(1, min(limit, 60))
    if (before_updated_at is None) != (before_id is None):
        raise HTTPException(400, "分页游标不完整")
    rows = store.list_ready_page(limit + 1, before_updated_at, before_id)
    has_more = len(rows) > limit
    items = rows[:limit]
    next_cursor = None
    if has_more and items:
        last = items[-1]
        next_cursor = {"updated_at": last["updated_at"], "id": last["id"]}
    return {
        "items": [{
            "id": item["id"],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
            "gif_url": f"/files/{item['id']}/clawd.gif?v={item['updated_at']}",
        } for item in items],
        "next_cursor": next_cursor,
    }


@app.get("/files/{work_id}/{filename}")
def files(work_id: str, filename: str, download: bool = False):
    if filename not in {"clawd.svg", "clawd.gif"}:
        raise HTTPException(404)
    row = store.get(work_id)
    if not row or row["status"] not in {"export_queued", "exporting", "ready"}:
        raise HTTPException(404)
    path = (store.files / work_id / filename).resolve()
    if store.files not in path.parents or not path.exists():
        raise HTTPException(404)
    media = "image/svg+xml" if filename.endswith(".svg") else "image/gif"
    disposition = "attachment" if download else "inline"
    headers = {"Content-Disposition": f'{disposition}; filename="clawd-{work_id[:8]}.{filename.rsplit(".", 1)[-1]}"'}
    return FileResponse(path, media_type=media, headers=headers)


STATIC = ROOT / "webapp" / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")
app.mount("/examples", StaticFiles(directory=ROOT / "wechat_stickers"), name="examples")


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/gallery")
def gallery_page():
    return FileResponse(STATIC / "gallery.html")

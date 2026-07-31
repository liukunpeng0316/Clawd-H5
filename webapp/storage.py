from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class Store:
    def __init__(self, root: Path, max_bytes: int):
        self.root = root
        self.files = root / "works"
        self.db_path = root / "clawd.db"
        self.max_bytes = max_bytes
        self.files.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def _db(self):
        conn = self._connect()
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._db() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS works (
                    id TEXT PRIMARY KEY,
                    edit_hash TEXT NOT NULL,
                    client_ip TEXT NOT NULL,
                    prompts TEXT NOT NULL,
                    status TEXT NOT NULL,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    svg_path TEXT,
                    gif_path TEXT
                )
                """
            )
            conn.execute(
                "UPDATE works SET status='failed', error='服务重启，请重新提交' "
                "WHERE status IN ('queued','processing','export_queued','exporting')"
            )

    @staticmethod
    def token_hash(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create(self, work_id: str, token: str, client_ip: str, prompt: str) -> None:
        now = utcnow()
        with self._lock, self._db() as conn:
            conn.execute(
                "INSERT INTO works VALUES (?,?,?,?,?,?,?,?,?,?)",
                (work_id, self.token_hash(token), client_ip, json.dumps([prompt], ensure_ascii=False),
                 "queued", None, now, now, None, None),
            )

    def queue_revision(self, work_id: str, token: str, prompt: str, client_ip: str) -> bool:
        with self._lock, self._db() as conn:
            row = conn.execute("SELECT * FROM works WHERE id=?", (work_id,)).fetchone()
            if not row or row["edit_hash"] != self.token_hash(token):
                return False
            prompts = json.loads(row["prompts"])
            prompts.append(prompt)
            conn.execute(
                "UPDATE works SET prompts=?, client_ip=?, status='queued', error=NULL, updated_at=? WHERE id=?",
                (json.dumps(prompts, ensure_ascii=False), client_ip, utcnow(), work_id),
            )
            return True

    def set_status(self, work_id: str, status: str, error: str | None = None) -> None:
        with self._lock, self._db() as conn:
            conn.execute(
                "UPDATE works SET status=?, error=?, updated_at=? WHERE id=?",
                (status, error, utcnow(), work_id),
            )

    def complete(self, work_id: str, svg_path: Path, gif_path: Path) -> None:
        with self._lock, self._db() as conn:
            conn.execute(
                "UPDATE works SET status='ready', error=NULL, updated_at=?, svg_path=?, gif_path=? WHERE id=?",
                (utcnow(), str(svg_path), str(gif_path), work_id),
            )
        self.enforce_limit()

    def get(self, work_id: str) -> dict | None:
        with self._db() as conn:
            row = conn.execute("SELECT * FROM works WHERE id=?", (work_id,)).fetchone()
        return dict(row) if row else None

    def queue_position(self, work_id: str) -> int | None:
        row = self.get(work_id)
        if not row or row["status"] != "queued":
            return None
        with self._db() as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM works WHERE status='queued' AND updated_at<=?",
                (row["updated_at"],),
            ).fetchone()[0]
        return int(count)

    def list_ready(self, limit: int = 60, offset: int = 0) -> list[dict]:
        with self._db() as conn:
            rows = conn.execute(
                "SELECT id, created_at, updated_at FROM works WHERE status='ready' ORDER BY updated_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
        return [dict(row) for row in rows]

    def prompts(self, work_id: str) -> list[str]:
        row = self.get(work_id)
        return json.loads(row["prompts"]) if row else []

    def paths(self, work_id: str) -> tuple[Path, Path]:
        folder = self.files / work_id
        folder.mkdir(parents=True, exist_ok=True)
        return folder / "clawd.svg", folder / "clawd.gif"

    def enforce_limit(self) -> None:
        with self._lock:
            while self._disk_usage() > self.max_bytes:
                with self._db() as conn:
                    row = conn.execute(
                        "SELECT id, svg_path, gif_path FROM works WHERE status IN ('ready','failed') ORDER BY created_at ASC LIMIT 1"
                    ).fetchone()
                    if not row:
                        return
                    work_id = row["id"]
                    for value in (row["svg_path"], row["gif_path"]):
                        if value:
                            Path(value).unlink(missing_ok=True)
                    folder = self.files / work_id
                    try:
                        folder.rmdir()
                    except OSError:
                        pass
                    conn.execute("DELETE FROM works WHERE id=?", (work_id,))

    def _disk_usage(self) -> int:
        total = self.db_path.stat().st_size if self.db_path.exists() else 0
        for path in self.files.rglob("*"):
            if path.is_file():
                try:
                    total += path.stat().st_size
                except FileNotFoundError:
                    pass
        return total

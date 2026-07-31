from __future__ import annotations

import asyncio
import tempfile
import threading
import time
import unittest
from unittest.mock import AsyncMock, patch
from pathlib import Path
from PIL import Image

from starlette.requests import Request

from webapp.security import UnsafeSVG, extract_svg, sanitize_svg
from webapp.storage import Store
from webapp import app as app_module, generator

ExportOptions = generator.svg_to_gif.ExportOptions
render_frames = generator.svg_to_gif.render_frames


SAFE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-15 -25 45 45">
<style>.body{animation:bob 2s infinite}@keyframes bob{50%{transform:translateY(-1px)}}</style>
<rect class="body" x="2" y="6" width="11" height="7" fill="#DE886D"/>
</svg>"""


class SvgSecurityTests(unittest.TestCase):
    def test_accepts_safe_animated_svg(self):
        output = sanitize_svg(SAFE)
        self.assertIn("viewBox", output)
        self.assertIn("@keyframes", output)

    def test_extracts_svg_from_fence(self):
        self.assertEqual(extract_svg(f"```svg\n{SAFE}\n```"), SAFE)

    def test_rejects_script(self):
        with self.assertRaises(UnsafeSVG):
            sanitize_svg("<svg><script>alert(1)</script></svg>")

    def test_rejects_event_handler(self):
        with self.assertRaises(UnsafeSVG):
            sanitize_svg("<svg><rect onload='alert(1)'/></svg>")

    def test_rejects_external_css(self):
        with self.assertRaises(UnsafeSVG):
            sanitize_svg("<svg><style>@import url(https://bad.example/x)</style></svg>")

    def test_all_reference_svgs_pass_sanitizer(self):
        root = Path(__file__).resolve().parents[1]
        for path in root.glob("assets/*/svg/*.svg"):
            with self.subTest(path=path.name):
                sanitize_svg(path.read_text(encoding="utf-8"))


class StoreTests(unittest.TestCase):
    def test_token_required_for_revision_and_prompt_not_in_gallery(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp), 1024 * 1024)
            store.create("a", "secret", "127.0.0.1", "private prompt")
            self.assertFalse(store.queue_revision("a", "wrong", "change", "127.0.0.1"))
            self.assertTrue(store.queue_revision("a", "secret", "change", "127.0.0.1"))
            svg, gif = store.paths("a")
            svg.write_text(SAFE, encoding="utf-8")
            gif.write_bytes(b"GIF89a")
            store.complete("a", svg, gif)
            self.assertNotIn("prompts", store.list_ready()[0])

    def test_storage_limit_deletes_oldest(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp), 100)
            for work_id in ("old", "new"):
                store.create(work_id, "secret", "127.0.0.1", work_id)
                svg, gif = store.paths(work_id)
                svg.write_bytes(b"x" * 80)
                gif.write_bytes(b"y" * 80)
                store.complete(work_id, svg, gif)
            self.assertIsNone(store.get("old"))

    def test_store_construction_does_not_fail_active_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = Store(root, 1024 * 1024)
            for work_id, status in (("waiting", "export_queued"), ("running", "exporting")):
                store.create(work_id, "secret", "127.0.0.1", work_id)
                store.set_status(work_id, status)
            restarted = Store(root, 1024 * 1024)
            self.assertEqual(restarted.get("waiting")["status"], "export_queued")
            self.assertEqual(restarted.get("running")["status"], "exporting")
            self.assertEqual(restarted.fail_incomplete(), 2)
            self.assertEqual(restarted.get("waiting")["status"], "failed")
            self.assertEqual(restarted.get("running")["status"], "failed")

    def test_cursor_pagination_stays_stable_when_new_work_arrives(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp), 1024 * 1024)
            for index in range(6):
                work_id = f"work-{index}"
                store.create(work_id, "secret", "127.0.0.1", work_id)
                svg, gif = store.paths(work_id)
                svg.write_text(SAFE, encoding="utf-8")
                gif.write_bytes(b"GIF89a")
                store.complete(work_id, svg, gif)
            first = store.list_ready_page(4)
            cursor = first[-1]
            store.create("new-work", "secret", "127.0.0.1", "new")
            svg, gif = store.paths("new-work")
            svg.write_text(SAFE, encoding="utf-8")
            gif.write_bytes(b"GIF89a")
            store.complete("new-work", svg, gif)
            second = store.list_ready_page(10, cursor["updated_at"], cursor["id"])
            combined = [row["id"] for row in first + second]
            self.assertEqual(len(combined), 6)
            self.assertEqual(len(set(combined)), 6)
            self.assertNotIn("new-work", combined)


class RequestValidationTests(unittest.TestCase):
    def test_prompt_is_stripped_before_minimum_length_check(self):
        with self.assertRaises(ValueError):
            app_module.CreateRequest(prompt="   ")
        self.assertEqual(app_module.CreateRequest(prompt="  挥手  ").prompt, "挥手")

    def test_same_ip_can_enqueue_multiple_tasks(self):
        async def scenario(root: Path):
            store = Store(root, 1024 * 1024)
            work_queue = asyncio.Queue(maxsize=100)
            request = Request({"type": "http", "client": ("198.51.100.8", 1234), "headers": []})
            with (
                patch.object(app_module, "store", store),
                patch.object(app_module, "queue", work_queue),
                patch.object(app_module, "admission_lock", asyncio.Lock()),
                patch.object(app_module, "inflight_work_ids", set()),
            ):
                first = await app_module.create_work(app_module.CreateRequest(prompt="挥手"), request)
                second = await app_module.create_work(app_module.CreateRequest(prompt="点头"), request)
            return first, second, work_queue.qsize()

        with tempfile.TemporaryDirectory() as tmp:
            first, second, queued = asyncio.run(scenario(Path(tmp)))
        self.assertNotEqual(first["id"], second["id"])
        self.assertEqual(queued, 2)

    def test_same_work_cannot_be_revised_concurrently(self):
        async def scenario(root: Path):
            store = Store(root, 1024 * 1024)
            store.create("source", "secret-token-that-is-long-enough", "ip", "original")
            svg, gif = store.paths("source")
            svg.write_text(SAFE, encoding="utf-8")
            gif.write_bytes(b"GIF89a")
            store.complete("source", svg, gif)
            work_queue = asyncio.Queue(maxsize=100)
            request = Request({"type": "http", "client": ("198.51.100.8", 1234), "headers": []})
            with (
                patch.object(app_module, "store", store),
                patch.object(app_module, "queue", work_queue),
                patch.object(app_module, "admission_lock", asyncio.Lock()),
                patch.object(app_module, "inflight_work_ids", {"source"}),
            ):
                with self.assertRaises(app_module.HTTPException) as raised:
                    await app_module.revise_work(
                        "source",
                        app_module.ReviseRequest(
                            prompt="换成蓝色", edit_token="secret-token-that-is-long-enough"
                        ),
                        request,
                    )
            return raised.exception.status_code, work_queue.qsize(), store.get("source")["status"]

        with tempfile.TemporaryDirectory() as tmp:
            status_code, queued, status = asyncio.run(scenario(Path(tmp)))
        self.assertEqual(status_code, 409)
        self.assertEqual(queued, 0)
        self.assertEqual(status, "ready")


class RemixTests(unittest.TestCase):
    @staticmethod
    def request() -> Request:
        return Request({"type": "http", "client": ("198.51.100.8", 1234), "headers": []})

    def test_remix_creates_independent_work_from_public_svg(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp), 1024 * 1024)
            store.create("source", "source-secret", "127.0.0.1", "original")
            svg, gif = store.paths("source")
            svg.write_text(SAFE, encoding="utf-8")
            gif.write_bytes(b"GIF89a")
            store.complete("source", svg, gif)
            remix_queue = asyncio.Queue()
            with (
                patch.object(app_module, "store", store),
                patch.object(app_module, "queue", remix_queue),
                patch.object(app_module, "admission_lock", asyncio.Lock()),
                patch.object(app_module, "inflight_work_ids", set()),
            ):
                result = asyncio.run(app_module.remix_work(
                    "source", app_module.CreateRequest(prompt="换成蓝色"), self.request()
                ))
                task = remix_queue.get_nowait()
            self.assertNotEqual(result["id"], "source")
            self.assertEqual(task.previous_svg, SAFE)
            self.assertEqual(store.prompts(result["id"]), ["换成蓝色"])
            self.assertEqual(store.prompts("source"), ["original"])

    def test_download_response_forces_attachment(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp), 1024 * 1024)
            store.create("source", "secret", "127.0.0.1", "original")
            svg, gif = store.paths("source")
            svg.write_text(SAFE, encoding="utf-8")
            gif.write_bytes(b"GIF89a")
            store.complete("source", svg, gif)
            with patch.object(app_module, "store", store):
                response = app_module.files("source", "clawd.gif", download=True)
            self.assertTrue(response.headers["content-disposition"].startswith("attachment;"))


class ExportConcurrencyTests(unittest.TestCase):
    def test_only_two_gif_exports_run_at_once(self):
        async def scenario(root: Path):
            store = Store(root, 1024 * 1024)
            tasks = []
            for index in range(6):
                work_id = f"work-{index}"
                ip = f"198.51.100.{index}"
                store.create(work_id, "secret", ip, "test")
                tasks.append(app_module.Task(work_id, "test", ip))
            counts = {"active": 0, "peak": 0}
            lock = threading.Lock()

            def fake_export(_svg_path, gif_path):
                with lock:
                    counts["active"] += 1
                    counts["peak"] = max(counts["peak"], counts["active"])
                time.sleep(0.04)
                gif_path.write_bytes(b"GIF89a")
                with lock:
                    counts["active"] -= 1

            with (
                patch.object(app_module, "store", store),
                patch.object(app_module, "export_slots", asyncio.Semaphore(2)),
                patch.object(app_module, "generate_svg", AsyncMock(return_value=SAFE)),
                patch.object(app_module, "export_gif", fake_export),
            ):
                await asyncio.gather(*(app_module.process(task) for task in tasks))
            return counts["peak"]

        with tempfile.TemporaryDirectory() as tmp:
            peak = asyncio.run(scenario(Path(tmp)))
        self.assertEqual(peak, 2)


class WorkerRecoveryTests(unittest.TestCase):
    def test_worker_continues_after_unexpected_task_error(self):
        async def scenario():
            work_queue = asyncio.Queue()
            await work_queue.put(app_module.Task("broken", "test", "ip"))
            await work_queue.put(app_module.Task("next", "test", "ip"))
            fake_process = AsyncMock(side_effect=[RuntimeError("broken"), None])
            with (
                patch.object(app_module, "queue", work_queue),
                patch.object(app_module, "active_work_ids", set()),
                patch.object(app_module, "inflight_work_ids", set()),
                patch.object(app_module, "process", fake_process),
                patch.object(app_module.log, "exception"),
            ):
                runner = asyncio.create_task(app_module.worker(0))
                await asyncio.wait_for(work_queue.join(), timeout=1)
                runner.cancel()
                await asyncio.gather(runner, return_exceptions=True)
            return fake_process.await_count

        self.assertEqual(asyncio.run(scenario()), 2)


class ApiFallbackTests(unittest.TestCase):
    def test_chat_falls_back_after_primary_http_error(self):
        import asyncio
        from webapp import generator

        class Response:
            def __init__(self, status, content=None):
                self.status_code = status
                self.text = "failed" if status >= 400 else ""
                self._content = content

            def json(self):
                return {"choices": [{"message": {"content": self._content}}]}

        class Client:
            def __init__(self):
                self.urls = []

            async def __aenter__(self):
                return self

            async def __aexit__(self, *_):
                return None

            async def post(self, url, **_):
                self.urls.append(url)
                return Response(503) if len(self.urls) == 1 else Response(200, "OK")

        client = Client()
        with (
            patch.dict("os.environ", {"DEEPSEEK_API_KEY": "primary-key", "STEPFUN_API_KEY": "test-key"}),
            patch.object(generator, "PRIMARY_BASE_URL", "https://primary.example/v1"),
            patch.object(generator, "FALLBACK_BASE_URL", "https://fallback.example/v1"),
            patch.object(generator.httpx, "AsyncClient", return_value=client),
        ):
            result = asyncio.run(generator._chat([{"role": "user", "content": "test"}], 8))
        self.assertEqual(result, "OK")
        self.assertEqual(client.urls, [
            "https://primary.example/v1/chat/completions",
            "https://fallback.example/v1/chat/completions",
        ])


class PromptOptimizationTests(unittest.TestCase):
    def test_action_keyword_beats_emotion_keyword(self):
        chosen = generator.select_references("一只开心挥手的小龙虾")
        self.assertEqual(chosen[0][1].stem, "clawd-salute")

    def test_unknown_action_uses_only_static_reference(self):
        chosen = generator.select_references("量子纠缠")
        self.assertEqual([svg.stem for _, svg in chosen], ["clawd-static-base"])

    def test_every_reference_hint_resolves(self):
        for _, stem, _ in generator.REFERENCE_HINTS:
            with self.subTest(stem=stem):
                self.assertIsNotNone(generator._reference_files(stem))

    def test_initial_prompt_stays_compact(self):
        for prompt in ("挥手", "喝咖啡", "发呆", "写代码"):
            with self.subTest(prompt=prompt):
                messages = generator.build_messages(prompt, None, [prompt])
                self.assertLess(sum(len(str(item["content"])) for item in messages), 12_000)

    def test_revision_uses_recent_history_without_reference(self):
        prompts = ["初始要求"] + [f"修改{i}" for i in range(1, 11)]
        messages = generator.build_messages(prompts[-1], SAFE, prompts)
        content = messages[1]["content"]
        self.assertNotIn("REFERENCE SVG", content)
        self.assertNotIn("修改1\"", content)
        self.assertIn("修改9", content)
        self.assertEqual(content.count("修改10"), 1)


class GifSpeedTests(unittest.TestCase):
    def test_fixed_33_unit_crop_enlarges_without_per_frame_zoom(self):
        frame = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        frame.paste((222, 136, 109, 255), (45, 45, 55, 55))
        bounds = generator.svg_to_gif.crop_bounds(
            [frame], padding=0, alpha_threshold=128,
            px_per_unit=100 / 45, min_units=33, max_units=45,
        )
        self.assertEqual(bounds[2] - bounds[0], round(33 * 100 / 45))

    def test_export_caps_frame_count_but_samples_full_cycle(self):
        options = ExportOptions(
            size=240, fps=15, padding=6, alpha_threshold=128,
            background="transparent", hide_ground_shadow=True,
            workers=1, timeout=25, min_units=20, max_units=33,
            max_duration_ms=2000,
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "long.svg"
            path.write_text(
                SAFE.replace("animation:bob 2s infinite", "animation-duration:4s;"),
                encoding="utf-8",
            )
            with patch.object(generator.svg_to_gif.chrome_render, "render_frames", return_value=[object()] * 30) as mocked:
                frames = render_frames(path, options, None)
        self.assertEqual(len(frames), 30)
        times = mocked.call_args.args[1]
        self.assertGreater(times[-1], 3800)


if __name__ == "__main__":
    unittest.main()

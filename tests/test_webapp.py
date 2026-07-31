from __future__ import annotations

import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from webapp.security import UnsafeSVG, extract_svg, sanitize_svg
from webapp.storage import Store
from webapp import generator

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


class GifSpeedTests(unittest.TestCase):
    def test_export_caps_frame_count_but_samples_full_cycle(self):
        options = ExportOptions(
            size=240, fps=12, padding=6, alpha_threshold=128,
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
            with patch.object(generator.svg_to_gif.chrome_render, "render_frames", return_value=[object()] * 24) as mocked:
                frames = render_frames(path, options, None)
        self.assertEqual(len(frames), 24)
        times = mocked.call_args.args[1]
        self.assertGreater(times[-1], 3800)


if __name__ == "__main__":
    unittest.main()

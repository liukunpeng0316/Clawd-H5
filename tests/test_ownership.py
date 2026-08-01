from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from webapp import app as app_module
from webapp.storage import Store


TOKEN = "owner-token-that-is-at-least-32-characters"
SAFE = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>'


def ready_work(store: Store, work_id: str = "owned") -> tuple[Path, Path]:
    store.create(work_id, TOKEN, "127.0.0.1", "test")
    svg, gif = store.paths(work_id)
    svg.write_text(SAFE, encoding="utf-8")
    gif.write_bytes(b"GIF89a")
    store.complete(work_id, svg, gif)
    return svg, gif


class OwnershipDeletionTests(unittest.TestCase):
    def test_correct_token_deletes_database_and_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp), 1024 * 1024)
            svg, gif = ready_work(store)
            self.assertEqual(store.delete_owned("owned", TOKEN), "deleted")
            self.assertIsNone(store.get("owned"))
            self.assertFalse(svg.exists())
            self.assertFalse(gif.exists())

    def test_wrong_token_cannot_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp), 1024 * 1024)
            svg, gif = ready_work(store)
            self.assertEqual(store.delete_owned("owned", "wrong-token"), "forbidden")
            self.assertIsNotNone(store.get("owned"))
            self.assertTrue(svg.exists())
            self.assertTrue(gif.exists())

    def test_busy_work_cannot_be_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp), 1024 * 1024)
            ready_work(store)
            store.set_status("owned", "processing")
            self.assertEqual(store.delete_owned("owned", TOKEN), "busy")
            self.assertIsNotNone(store.get("owned"))

    def test_delete_endpoint_rejects_inflight_work(self):
        async def scenario(root: Path):
            store = Store(root, 1024 * 1024)
            ready_work(store)
            with (
                patch.object(app_module, "store", store),
                patch.object(app_module, "admission_lock", asyncio.Lock()),
                patch.object(app_module, "inflight_work_ids", {"owned"}),
            ):
                with self.assertRaises(app_module.HTTPException) as raised:
                    await app_module.delete_work("owned", app_module.DeleteRequest(edit_token=TOKEN))
            return raised.exception.status_code

        with tempfile.TemporaryDirectory() as tmp:
            status_code = asyncio.run(scenario(Path(tmp)))
        self.assertEqual(status_code, 409)

    def test_delete_endpoint_accepts_owner_token(self):
        async def scenario(root: Path):
            store = Store(root, 1024 * 1024)
            ready_work(store)
            with (
                patch.object(app_module, "store", store),
                patch.object(app_module, "admission_lock", asyncio.Lock()),
                patch.object(app_module, "inflight_work_ids", set()),
            ):
                response = await app_module.delete_work(
                    "owned", app_module.DeleteRequest(edit_token=TOKEN)
                )
            return response.status_code, store.get("owned")

        with tempfile.TemporaryDirectory() as tmp:
            status_code, row = asyncio.run(scenario(Path(tmp)))
        self.assertEqual(status_code, 204)
        self.assertIsNone(row)


if __name__ == "__main__":
    unittest.main()

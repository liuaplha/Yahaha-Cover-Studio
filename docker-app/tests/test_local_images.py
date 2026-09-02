from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from app.services import CoverService


class LocalImageSelectionTests(unittest.TestCase):
    def test_random_sort_samples_local_folder_images(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("01.jpg", "02.jpg", "03.jpg", "04.jpg"):
                (root / name).write_bytes(b"image")

            service = CoverService()
            service.config["sort_by"] = "Random"
            with patch.object(service, "input_directory", return_value=root), patch(
                "app.services.random.sample", side_effect=lambda values, k: values[-k:]
            ) as sample:
                images = service.local_images(limit=2)

            sample.assert_called_once()
            self.assertEqual([path.name for path in images], ["03.jpg", "04.jpg"])

    def test_manual_sort_keeps_filename_order(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("03.jpg", "01.jpg", "02.jpg"):
                (root / name).write_bytes(b"image")

            service = CoverService()
            service.config["sort_by"] = "Manual"
            with patch.object(service, "input_directory", return_value=root):
                images = service.local_images(limit=2)

            self.assertEqual([path.name for path in images], ["01.jpg", "02.jpg"])

    def test_latest_rendered_local_images_are_available_for_preview(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            images = []
            for name in ("03.jpg", "01.jpg", "02.jpg"):
                path = root / name
                path.write_bytes(b"image")
                images.append(path)

            service = CoverService()
            service.remember_local_images("动漫", images)

            self.assertEqual(
                [path.name for path in service.last_local_images("动漫", 2)],
                ["03.jpg", "01.jpg"],
            )


if __name__ == "__main__":
    unittest.main()

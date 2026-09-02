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

    def test_non_random_sort_keeps_filename_order(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("03.jpg", "01.jpg", "02.jpg"):
                (root / name).write_bytes(b"image")

            service = CoverService()
            service.config["sort_by"] = "DateCreated"
            with patch.object(service, "input_directory", return_value=root):
                images = service.local_images(limit=2)

            self.assertEqual([path.name for path in images], ["01.jpg", "02.jpg"])


if __name__ == "__main__":
    unittest.main()

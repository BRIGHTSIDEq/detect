from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from urllib.request import urlretrieve

import yaml

COCO8_URL = "https://github.com/ultralytics/assets/releases/download/v0.0.0/coco8.zip"
OPEN_IMAGES_SPLITS = ("train", "validation", "test")


def load_project_classes(path: Path) -> list[dict]:
    """Загружает классы проекта."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return list(data.get("classes", []))


def write_yolo_data_yaml(dataset_dir: Path, classes: list[dict]) -> Path:
    """Создаёт data.yaml для подготовленного YOLO-набора."""
    names = {int(item["id"]): item["name"] for item in classes}
    output = dataset_dir / "data.yaml"
    payload = {
        "path": str(dataset_dir.resolve()).replace("\\", "/"),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": names,
    }
    output.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return output


def download_coco8(raw_dir: Path, processed_dir: Path) -> Path:
    """Скачивает маленький проверочный датасет COCO8 по прямой ссылке."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    archive = raw_dir / "coco8.zip"
    if not archive.exists():
        urlretrieve(COCO8_URL, archive)
    unpack_dir = raw_dir / "coco8_unpacked"
    if unpack_dir.exists():
        shutil.rmtree(unpack_dir)
    shutil.unpack_archive(str(archive), str(unpack_dir))
    source = next(unpack_dir.glob("**/coco8"), unpack_dir / "coco8")
    target = processed_dir / "coco8"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    return target / "coco8.yaml"


def export_open_images_yolo(classes: list[dict], raw_dir: Path, processed_dir: Path, max_samples: int) -> Path:
    """Скачивает Open Images через FiftyOne и экспортирует YOLO-разметку."""
    try:
        import fiftyone as fo
        import fiftyone.zoo as foz
    except ImportError as exc:
        raise SystemExit(
            "Для автоматической загрузки Open Images установите зависимость: "
            "pip install fiftyone. Она не ставится по умолчанию, потому что пакет большой."
        ) from exc

    class_names = [item["display_en"] for item in classes]
    dataset_name = "object_lens_open_images_v7"
    if fo.dataset_exists(dataset_name):
        fo.delete_dataset(dataset_name)
    merged = fo.Dataset(dataset_name)
    raw_dir.mkdir(parents=True, exist_ok=True)
    for split in OPEN_IMAGES_SPLITS:
        split_dataset = foz.load_zoo_dataset(
            "open-images-v7",
            split=split,
            label_types=["detections"],
            classes=class_names,
            max_samples=max_samples,
            dataset_dir=str(raw_dir / "open-images-v7"),
        )
        merged.add_samples(split_dataset)
    target = processed_dir / "open_images_yolo"
    if target.exists():
        shutil.rmtree(target)
    merged.export(
        export_dir=str(target),
        dataset_type=fo.types.YOLOv5Dataset,
        label_field="detections",
        classes=class_names,
        split="train",
    )
    metadata = {
        "source": "open-images-v7",
        "classes": class_names,
        "max_samples_per_split": max_samples,
        "note": "Проверьте статистику классов перед долгим обучением.",
    }
    (target / "object_lens_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return target / "dataset.yaml"


def main() -> None:
    """Запускает автоматическую загрузку датасета."""
    parser = argparse.ArgumentParser(description="Автоматическая загрузка датасетов Object Lens")
    parser.add_argument("--preset", choices=["coco8", "open-images"], default="coco8")
    parser.add_argument("--classes", type=Path, default=Path("configs/classes.yaml"))
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--max-samples-per-split", type=int, default=400)
    args = parser.parse_args()

    classes = load_project_classes(args.classes)
    if args.preset == "coco8":
        data_yaml = download_coco8(args.raw_dir, args.processed_dir)
        print(f"Проверочный датасет скачан: {data_yaml}")
        print("Для реального обучения запустите --preset open-images на машине с достаточным диском.")
        return
    data_yaml = export_open_images_yolo(
        classes, args.raw_dir, args.processed_dir, args.max_samples_per_split
    )
    print(f"Open Images подготовлен: {data_yaml}")


if __name__ == "__main__":
    main()

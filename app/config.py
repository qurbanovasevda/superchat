from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    data_dir: Path = Path(__file__).resolve().parents[1] / "data"
    database_path: Path = Path(__file__).resolve().parents[1] / "var" / "superchat.sqlite3"
    reference_date: date = date(2026, 11, 2)
    application_name: str = "SuperChat"

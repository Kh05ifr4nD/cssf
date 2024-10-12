from dataclasses import dataclass
from PySide6.QtCore import QSize
from typing import List, Dict


@dataclass(frozen=True)
class Cfg:
    menu_page_items: List[Dict[str, str]]
    icon_dir: str = "./icons"
    th_xml: str = "dark_teal.xml"

    btn_size: QSize = QSize(48, 48)
    icon_size: QSize = QSize(32, 32)
    lbl_size: QSize = QSize(144, 48)
    srch_le_min_size: QSize = QSize(200, 48)
    win_min_size: QSize = QSize(480, 300)

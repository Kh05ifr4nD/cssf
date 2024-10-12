import sys
from PySide6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    QTimer,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from ui import MainWinIniter
from qt_material import apply_stylesheet
from cfg import Cfg


class MainWin(QMainWindow):
    def __init__(self, cfg: Cfg):
        super().__init__()
        self.cfg = cfg
        self.ui = MainWinIniter()
        self.ui.setup_ui(self)
        self.setup_anime()
        self.cnct_sgl()
        self.pnl_ex = False

    def setup_anime(self):
        self.sidebar_anime_grp = QParallelAnimationGroup()
        self.w_anime = QPropertyAnimation(self.ui.sidebar_frm, b"minimumWidth")
        self.w_anime.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.w_anime.setDuration(300)

        self.opa_anime = QPropertyAnimation(self.ui.sidebar_frm, b"windowOpacity")
        self.opa_anime.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.opa_anime.setDuration(300)

        self.sidebar_anime_grp.addAnimation(self.w_anime)
        self.sidebar_anime_grp.addAnimation(self.opa_anime)

    def cnct_sgl(self):
        self.ui.pnl_btn.clicked.connect(self.tgl_pnl)
        self._cnct_page_btn()

    def _cnct_page_btn(self):
        btn_list = [
            (self.ui.home_btn, 0),
            (self.ui.usr_btn, 1),
            (self.ui.stg_btn, 2),
            (self.ui.about_btn, 3),
        ]
        for btn, idx in btn_list:
            btn.clicked.connect(
                lambda _, idx=idx: self.ui.page_stk.setCurrentIndex(idx)
            )

    def tgl_pnl(self):
        self.pnl_ex = not self.pnl_ex
        self.ui.pnl_btn.setChecked(self.pnl_ex)
        self._anime_sidebar()
        self._tgl_pnl_btn_icon()

    def _anime_sidebar(self):
        start_w = self.ui.sidebar_frm.width()
        end_w = 192 if self.pnl_ex else 52
        self.w_anime.setStartValue(start_w)
        self.w_anime.setEndValue(end_w)

        self.opa_anime.setStartValue(1 if self.pnl_ex else 0)
        self.opa_anime.setEndValue(0 if self.pnl_ex else 1)

        self.sidebar_anime_grp.start()

        QTimer.singleShot(150, lambda: self._tgl_lbl_vis())

    def _tgl_pnl_btn_icon(self):
        icon_name = "收起面板.png" if self.pnl_ex else "展开面板.png"
        self.ui.pnl_btn.setIcon(QIcon(f"{self.cfg.icon_dir}/{icon_name}"))

    def _tgl_lbl_vis(self):
        for r in range(self.ui.sidebar_glo.rowCount()):
            i = self.ui.sidebar_glo.itemAtPosition(r, 1)
            if isinstance(i.widget(), QLabel):
                i.widget().show() if self.pnl_ex else i.widget().hide()


if __name__ == "__main__":
    cfg = Cfg([{"name": "主页", "icon": "主页.png"}])
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme=cfg.th_xml)
    win = MainWin(cfg)
    win.show()
    sys.exit(app.exec())

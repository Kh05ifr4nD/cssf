from PySide6.QtCore import QCoreApplication, QMetaObject
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QWidget,
)
from cfg import Cfg


class MainWinIniter:
    def setup_ui(self, main_win: QMainWindow):
        self._setupMainWin(main_win)
        self._setupCent(main_win)
        self._setupSidebarFrm(main_win.cfg)
        self._setupSrchHlo(main_win.cfg)
        self._setupPageStk()
        self._finalizeLo(main_win)

    def _setupMainWin(self, main_win: QMainWindow):
        if not main_win.objectName():
            main_win.setObjectName("main_win")
        main_win.setMinimumSize(main_win.cfg.win_min_size)
        main_win.setWindowIcon(QIcon(f"{main_win.cfg.icon_dir}/徽标.png"))

    def _setupCent(self, main_win: QMainWindow):
        self.cent = QWidget(main_win)
        self.cent.setObjectName("cent")
        self.cent.setMinimumSize(main_win.cfg.win_min_size)

        self.cent_glo = QGridLayout(self.cent)
        self.cent_glo.setObjectName("cent_glo")
        self.cent_glo.setSpacing(0)
        self.cent_glo.setContentsMargins(0, 0, 0, 0)

    def _setupSidebarFrm(self, cfg: Cfg):
        self.sidebar_frm = QFrame()
        self.sidebar_frm.setObjectName("sidebar_frm")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebar_frm.sizePolicy().hasHeightForWidth())
        self.sidebar_frm.setSizePolicy(sizePolicy)

        self.sidebar_glo = QGridLayout(self.sidebar_frm)
        self.sidebar_glo.setSpacing(0)
        self.sidebar_glo.setObjectName("sidebar_glo")
        self.sidebar_glo.setContentsMargins(0, 0, 0, 0)

        self._setupSidebarIcons(cfg)
        self._setupSidebarLbls(cfg)
        self._setupSidebarSpcs()

        self.cent_glo.addWidget(self.sidebar_frm, 0, 0, 2, 1)

    def _setupSidebarIcons(self, cfg: Cfg):
        buttons = [
            ("icon_lbl", f"{cfg.icon_dir}/徽标.png", 0, 0),
            ("pnl_btn", f"{cfg.icon_dir}/展开面板.png", 1, 0),
            ("home_btn", f"{cfg.icon_dir}/主页.png", 2, 0),
            ("usr_btn", f"{cfg.icon_dir}/用户.png", 4, 0),
            ("stg_btn", f"{cfg.icon_dir}/设置.png", 5, 0),
            ("about_btn", f"{cfg.icon_dir}/关于.png", 6, 0),
        ]

        for name, icon_path, row, col in buttons:
            if name == "icon_lbl":
                setattr(self, name, QLabel(self.cent))
                getattr(self, name).setPixmap(
                    QPixmap(icon_path).scaled(
                        cfg.icon_size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
                )
                getattr(self, name).setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                setattr(self, name, QPushButton(self.cent))
                getattr(self, name).setIcon(QIcon(icon_path))
                getattr(self, name).setIconSize(cfg.icon_size)
                getattr(self, name).setFlat(True)

            getattr(self, name).setObjectName(name)
            getattr(self, name).setFixedSize(cfg.btn_size)
            self.sidebar_glo.addWidget(getattr(self, name), row, col, 1, 1)

        self.pnl_btn.setCheckable(True)

    def _setupSidebarLbls(self, cfg: Cfg):
        labels = [
            ("tit_lbl", 0, 1),
            ("home_lbl", 2, 1),
            ("usr_lbl", 4, 1),
            ("stg_lbl", 5, 1),
            ("about_lbl", 6, 1),
        ]

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        for name, row, col in labels:
            setattr(self, name, QLabel(self.cent))
            label = getattr(self, name)
            label.setObjectName(name)
            sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
            label.setSizePolicy(sizePolicy)
            label.setFixedSize(cfg.lbl_size)
            self.sidebar_glo.addWidget(label, row, col, 1, 1)

    def _setupSidebarSpcs(self):
        spacers = [
            (
                "icon_vspc",
                3,
                0,
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum,
            ),
            (
                "ext_vspc",
                3,
                1,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            ),
            (
                "pnl_btn_vspc",
                1,
                1,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Maximum,
                48,
            ),
        ]

        for name, row, col, h_policy, v_policy, *args in spacers:
            setattr(
                self, name, QSpacerItem(0, args[0] if args else 0, h_policy, v_policy)
            )
            self.sidebar_glo.addItem(getattr(self, name), row, col, 1, 1)

        for row in range(self.sidebar_glo.rowCount()):
            item = self.sidebar_glo.itemAtPosition(row, 1)
            if w := item.widget():
                w.hide()

    def _setupSrchHlo(self, cfg: Cfg):
        self.srch_hlo = QHBoxLayout()
        self.srch_hlo.setSpacing(0)
        self.srch_hlo.setContentsMargins(0, 0, 0, 0)
        self.srch_hlo.setObjectName("srch_hlo")

        self.srch_hspc = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.srch_hlo.addItem(self.srch_hspc)

        self.srch_le = QLineEdit(self.cent)
        self.srch_le.setObjectName("srch_le")
        self.srch_le.setMinimumSize(cfg.srch_le_min_size)
        self.srch_le.setProperty("color", "cyan")
        self.srch_hlo.addWidget(self.srch_le)

        self.srch_btn = QPushButton(self.cent)
        self.srch_btn.setObjectName("srch_btn")
        self.srch_btn.setFixedSize(cfg.btn_size)
        self.srch_btn.setIconSize(cfg.icon_size)
        self.srch_btn.setFlat(False)
        self.srch_btn.setIcon(QIcon(f"{cfg.icon_dir}/搜索.png"))
        self.srch_hlo.addWidget(self.srch_btn)

        self.cent_glo.addLayout(self.srch_hlo, 0, 1, 1, 1)

    def _setupPageStk(self):
        self.page_stk = QStackedWidget(self.cent)
        self.page_stk.setObjectName("page_stk")

        pages = ["home_page", "usr_page", "stg_page", "about_page"]
        for page in pages:
            setattr(self, page, QWidget())
            getattr(self, page).setObjectName(page)
            self.page_stk.addWidget(getattr(self, page))

        self.cent_glo.addWidget(self.page_stk, 1, 1, 1, 1)

    def _finalizeLo(self, main_win: QMainWindow):
        main_win.setCentralWidget(self.cent)
        self.retranslateUi(main_win)
        QMetaObject.connectSlotsByName(main_win)

    def retranslateUi(self, main_win: QMainWindow):
        main_win.setWindowTitle(
            QCoreApplication.translate("Genshin Impact", "原神", None)
        )
        self.usr_lbl.setText(QCoreApplication.translate("main_win", "用户", None))
        self.tit_lbl.setText(QCoreApplication.translate("main_win", "原神", None))
        self.stg_lbl.setText(QCoreApplication.translate("main_win", "设置", None))
        self.home_lbl.setText(QCoreApplication.translate("main_win", "主页", None))
        self.about_lbl.setText(QCoreApplication.translate("main_win", "关于", None))
        self.srch_le.setPlaceholderText(
            QCoreApplication.translate("Search…", "搜索……", None)
        )
        self.usr_btn.setText("")
        self.stg_btn.setText("")
        self.about_btn.setText("")
        self.home_btn.setText("")
        self.pnl_btn.setText("")
        self.srch_btn.setText("")

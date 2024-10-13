from PySide6.QtCore import QCoreApplication, QMetaObject
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from cfg import Cfg


class MainWinIniter:
    def setup_ui(self, main_win: QMainWindow):
        self._setup_main_win(main_win)
        self._setup_cent(main_win)
        self._setup_sidebar_frm(main_win.cfg)
        self._setup_srch_hlo(main_win.cfg)
        self._setup_page_stk(main_win.cfg)
        self._finalize_lo(main_win)

    def _setup_main_win(self, main_win: QMainWindow):
        if not main_win.objectName():
            main_win.setObjectName("main_win")
        main_win.setMinimumSize(main_win.cfg.win_min_size)
        main_win.setWindowIcon(QIcon(f"{main_win.cfg.icon_dir}/徽标.png"))

    def _setup_cent(self, main_win: QMainWindow):
        self.cent = QWidget(main_win)
        self.cent.setObjectName("cent")
        self.cent.setMinimumSize(main_win.cfg.win_min_size)

        self.cent_glo = QGridLayout(self.cent)
        self.cent_glo.setObjectName("cent_glo")
        self.cent_glo.setSpacing(4)
        self.cent_glo.setContentsMargins(0, 0, 0, 0)

    def _setup_sidebar_frm(self, cfg: Cfg):
        self.sidebar_frm = QFrame()
        self.sidebar_frm.setObjectName("sidebar_frm")
        self.sidebar_frm.setStyleSheet(
            "QFrame#sidebar_frm {border: 2px solid #34495E;}"
        )

        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.sidebar_frm.setSizePolicy(sizePolicy)

        self.sidebar_glo = QGridLayout(self.sidebar_frm)
        self.sidebar_glo.setSpacing(0)
        self.sidebar_glo.setObjectName("sidebar_glo")
        self.sidebar_glo.setContentsMargins(0, 0, 0, 0)

        self._setup_sidebar_icon(cfg)
        self._setup_sidebar_lbl(cfg)
        self._setup_sidebar_spcs()

        self.cent_glo.addWidget(self.sidebar_frm, 0, 0, 2, 1)

    def _setup_sidebar_icon(self, cfg: Cfg):
        buttons = [
            ("icon_lbl", f"{cfg.icon_dir}/徽标.png", 0, 0),
            ("pnl_btn", f"{cfg.icon_dir}/展开面板.png", 1, 0),
            ("home_btn", f"{cfg.icon_dir}/主页.png", 2, 0),
            ("usr_btn", f"{cfg.icon_dir}/用户.png", 4, 0),
            ("stg_btn", f"{cfg.icon_dir}/设置.png", 5, 0),
            ("about_btn", f"{cfg.icon_dir}/关于.png", 6, 0),
        ]

        for name, icon_path, row, col in buttons:
            widget = self._create_icon_btn(name, icon_path, cfg)
            widget.setFixedSize(cfg.btn_size)
            self.sidebar_glo.addWidget(widget, row, col, 1, 1)

        self.pnl_btn.setCheckable(True)

    def _create_icon_btn(self, name, icon, cfg):
        if name == "icon_lbl":
            widget = QLabel(self.cent)
            widget.setPixmap(
                QPixmap(icon).scaled(
                    cfg.icon_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            widget = QPushButton(self.cent)
            widget.setIcon(QIcon(icon))
            widget.setIconSize(cfg.icon_size)
            widget.setFlat(True)
        widget.setObjectName(name)
        setattr(self, name, widget)
        return widget

    def _setup_sidebar_lbl(self, cfg: Cfg):
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
            label = QLabel(self.cent)
            label.setObjectName(name)
            sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
            label.setSizePolicy(sizePolicy)
            label.setFixedSize(cfg.lbl_size)
            label.setStyleSheet("QLabel {font-size: 14pt;}")

            self.sidebar_glo.addWidget(label, row, col, 1, 1)
            setattr(self, name, label)

    def _setup_sidebar_spcs(self):
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
            spacer = QSpacerItem(0, args[0] if args else 0, h_policy, v_policy)
            self.sidebar_glo.addItem(spacer, row, col, 1, 1)
            setattr(self, name, spacer)

        for row in range(self.sidebar_glo.rowCount()):
            item = self.sidebar_glo.itemAtPosition(row, 1)
            if w := item.widget():
                w.hide()

    def _setup_srch_hlo(self, cfg: Cfg):
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
        self.srch_hlo.addWidget(self.srch_le)

        self.srch_btn = QPushButton(self.cent)
        self.srch_btn.setObjectName("srch_btn")
        self.srch_btn.setFixedSize(cfg.btn_size)
        self.srch_btn.setIconSize(cfg.icon_size)
        self.srch_btn.setFlat(False)
        self.srch_btn.setIcon(QIcon(f"{cfg.icon_dir}/搜索.png"))
        self.srch_hlo.addWidget(self.srch_btn)

        self.cent_glo.addLayout(self.srch_hlo, 0, 1, 1, 1)

    def _setup_page_stk(self, cfg: Cfg):
        self.page_stk = QStackedWidget(self.cent)
        self.page_stk.setObjectName("page_stk")

        pages = ["home_page", "usr_page", "stg_page", "about_page"]

        for page in pages:
            widget = QWidget()
            widget.setObjectName(page)
            self.page_stk.addWidget(widget)
            setattr(self, page, widget)

        self._setup_stg_page(cfg)

        self.cent_glo.addWidget(self.page_stk, 1, 1, 1, 1)

    def _setup_stg_page(self, cfg: Cfg):
        self.stg_scroll_area = QScrollArea(self.stg_page)
        self.stg_scroll_area.setWidgetResizable(True)
        self.stg_scroll_cont = QWidget()
        self.stg_vlo = QVBoxLayout(self.stg_scroll_cont)
        self.stg_vlo.setSpacing(12)
        self.stg_vlo.setContentsMargins(12, 12, 12, 12)
        self.opt_hspc = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        for grp_name, opt_list in cfg.stg_grp_list.items():
            gb = self._create_gb(grp_name)
            grp_vlo = QVBoxLayout(gb)
            grp_vlo.setSpacing(12)
            grp_vlo.setContentsMargins(0, 12, 0, 12)

            for opt_name, opt_icon, opt in opt_list:
                opt_frm = self._create_opt_frm(opt_name, opt_icon, opt, cfg)
                grp_vlo.addWidget(opt_frm)

            self.stg_vlo.addWidget(gb)

        self.stg_vlo.addStretch(1)
        self.stg_scroll_area.setWidget(self.stg_scroll_cont)

        stg_page_layout = QVBoxLayout(self.stg_page)
        stg_page_layout.setContentsMargins(0, 0, 0, 0)
        stg_page_layout.addWidget(self.stg_scroll_area)

    def _create_gb(self, grp_name):
        gb = QGroupBox(grp_name)
        gb.setObjectName(f"{grp_name}_gb")
        gb.setStyleSheet("QGroupBox{border:0px;}")
        return gb

    def _create_opt_frm(self, opt_name, opt_icon, opt, cfg):
        opt_frm = QFrame()
        opt_frm.setObjectName(f"{opt_name}_frm")
        opt_hlo = QHBoxLayout(opt_frm)
        opt_hlo.setSpacing(12)
        opt_hlo.setContentsMargins(12, 12, 12, 12)

        icon_opt_lbl = self._create_icon_opt_lbl(opt_name, opt_icon, cfg)
        opt_hlo.addWidget(icon_opt_lbl)

        opt_lbl = QLabel()
        opt_lbl.setObjectName(f"{opt_name}_lbl")
        opt_lbl.setText(opt_name)
        setattr(self, f"{opt_name}_lbl", opt_lbl)
        opt_hlo.addWidget(opt_lbl)

        if isinstance(opt, list):
            opt_cb = QComboBox()
            opt_cb.addItems(opt)
            setattr(self, f"{opt_name}_cb", opt_cb)
            opt_hlo.addItem(self.opt_hspc)
            opt_hlo.addWidget(opt_cb)

        return opt_frm

    def _create_icon_opt_lbl(self, opt_name, opt_icon, cfg):
        icon_opt_lbl = QLabel()
        icon_opt_lbl.setObjectName(f"icon_{opt_name}_lbl")
        icon_opt_lbl.setPixmap(
            QPixmap(f"{cfg.icon_dir}/{opt_icon}").scaled(
                cfg.opt_icon_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )
        icon_opt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        setattr(self, f"icon_{opt_name}_lbl", icon_opt_lbl)
        return icon_opt_lbl

    def _finalize_lo(self, main_win: QMainWindow):
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

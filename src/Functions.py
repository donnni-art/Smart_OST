######################################################
# GUI function
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomTipOverlay import QCustomTipOverlay
from Custom_Widgets.QCustomLoadingIndicators import QCustom3CirclesLoader

from PySide6.QtCore import QSettings, QTimer
from PySide6.QtGui import QColor, QFont, QFontDatabase
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from src.config_manager import config_manager
from src.config_dialog import ConfigDialog
from PySide6.QtWidgets import QDialog, QMessageBox
from src.app_logger import get_logger

log = get_logger("functions")

class GuiFunctions():
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.ui = MainWindow.ui
        self.ui_config = config_manager.get_ui_config()

        self.initializeAppTheme()
        self.LoadProductSansFont()

        # Clear hard-coded inline styles from .ui so SCSS/QSS can take over
        self._clear_inline_styles()

        self.connectMenuButtons()
        self.setup_configuration_menu()

    # ─── Style helpers ───────────────────────────────────────────────────────────

    def _clear_inline_styles(self):
        """
        ลบ inline styleSheet ที่ hard-code ไว้ใน .ui เพื่อให้ SCSS/QSS ควบคุมได้
        ต้องเรียกหลัง setupUi() และ loadJsonStyle() เพื่อให้แน่ใจว่า theme โหลดแล้ว
        """
        ui = self.ui

        # Info card frames — remove white-background inline style
        for name in ('frame_3', 'frame_4', 'frame_5', 'frame_6', 'frame_7'):
            w = getattr(ui, name, None)
            if w:
                w.setStyleSheet("")

        # Info labels — remove hard-coded black color
        for name in ('label', 'label_9', 'label_10', 'label_11', 'label_12',
                     'product_name', 'lot_number', 'tooling_code', 'operator_name'):
            w = getattr(ui, name, None)
            if w:
                w.setStyleSheet("")

        # KPI card title labels
        for name in ('label_sheet_per_ht', 'label_pcs_per_hr', 'shot_per_hr_2'):
            w = getattr(ui, name, None)
            if w:
                w.setStyleSheet("")

        # Manual PM button — let SCSS handle it
        btn = getattr(ui, 'pushButton_2', None)
        if btn:
            btn.setStyleSheet("")

        # KPI cards — replace old colors with modern flat palette
        kpi_palette = (
            ('widget_9',  '#e67e22'),   # Sheets/hr — orange
            ('widget_10', '#2980b9'),   # PCS/hr    — blue
            ('widget_11', '#1abc9c'),   # Shots/hr  — teal
        )
        for name, color in kpi_palette:
            w = getattr(ui, name, None)
            if w:
                w.setStyleSheet(
                    f"QWidget#{name} {{ background-color: {color}; border-radius: 8px; }}"
                    f"QWidget#{name} QLabel {{ color: white; background-color: transparent; font-weight: bold; }}"
                )

    ##################################################################################################
    # setup config
    ##################################################################################################
    def setup_configuration_menu(self):
        """Add configuration menu to the application"""
        # ใช้ปุ่ม communicationBtn ที่มีอยู่ใน UI แทน settingsBtn
        if hasattr(self.ui, 'communication'):
            self.ui.communication.clicked.connect(self.show_config_dialog)
        else:
            log.warning("communicationBtn not found in UI")

    def show_config_dialog(self):
        """Show configuration dialog"""
        try:
            config_dialog = ConfigDialog(self.main)
            result = config_dialog.exec()
            
            if result == QDialog.Accepted:
                # อัพเดตการตั้งค่า UI ถ้าจำเป็น
                self.apply_ui_config()
                
        except Exception as e:
            QMessageBox.critical(self.main, "Error", f"Cannot open configuration dialog:\n{str(e)}")

    def apply_ui_config(self):
        """Apply UI configuration changes"""
        try:
            ui_config = self.config_manager.get_ui_config()
            
            # อัพเดตธีม
            current_theme = ui_config.get('theme', 'LightBlue')
            settings = QSettings()
            if settings.value("THEME") != current_theme:
                settings.setValue("THEME", current_theme)
                self.main.theme_changed.emit()
            
            # อัพเดตขนาดฟอนต์
            font_size = ui_config.get('font_size', 12)
            current_font = self.main.font()
            current_font.setPointSize(font_size)
            self.main.setFont(current_font)
            
        except Exception as e:
            log.error("Error applying UI config: %s", e)

    #######################################################################################################

    def connectMenuButtons(self):
        self.ui.repairBtn.clicked.connect(lambda: self.ui.centerMenu.expandMenu())
        self.ui.informationBtn.clicked.connect(lambda: self.ui.centerMenu.expandMenu())
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.centerMenu.expandMenu())
        self.ui.closeCenterMenuBtn.clicked.connect(lambda: self.ui.centerMenu.collapseMenu())

    def createSearchTipOverlay(self):
        """Create a shearch tip overlay under the search input"""
        self.searchTooltip = QCustomTipOverlay(
            title="Search result",
            description="Searching...",
            icon= self.main.theme.PATH_RESOURCES + "feather/search.png",
            isClosable=True,
            target=self.ui.search,
            parent= self.main,
            deleteOnClose=True,
            duration=-1,
            tailPosition="top-center",
            closeIcon=self.main.theme.PATH_RESOURCES + "material_design/close.png", # Add a close icon
            toolFlag =True
        )

        #สร้าง loader
        loader = QCustom3CirclesLoader(
            parent =self.searchTooltip,
            color =QColor(self.main.theme.COLOR_ACCENT_1),
            penWidth = 20,
            animationDuration = 400
        )

        #add load to tipoverlay
        self.searchTooltip.addWidget(loader)

    def showSearchResults(self):
        # แสดงเฉพาะการค้นหาที่ไม่ว่างเปล่า
        seachPhrase = self.ui.searchEdit.text()
        if not seachPhrase:
            return
        try:
            self.searchTooltip.show()
        except:
            self.createSearchTipOverlay()
            self.searchTooltip.show()

        self.searchTooltip.setDescription("Showing search result for:" + searchPhrase)

    def initializeAppTheme(self):
        """initialize the application theme from settings"""
        settings = QSettings()
        current_theme = settings.value("THEME")
        #print("current_theme is :", current_theme )
        self.populateThemeList(current_theme)

        # connect theme signal to change app theme
        self.ui.themeList.currentTextChanged.connect(self.changeAppTheme)

    def populateThemeList(self, current_theme):
        """Popup the list from available app themes"""
        theme_count = -1
        for theme in self.ui.themes:
            self.ui.themeList.addItem(theme.name, theme.name)
            #ตรวจสอบค่าเริ่มต้ม theme / current theme
            if theme.defaultTheme or theme.name == current_theme:
                self.ui.themeList.setCurrentIndex(theme_count) # เลือก Theme

    def changeAppTheme(self):
        """Change app theme and restore window size"""
        settings = QSettings()
        selected_theme = self.ui.themeList.currentData()
        current_theme = settings.value("THEME")

        if current_theme != selected_theme:
            settings.setValue("THEME", selected_theme)
            QAppSettings.updateAppSettings(self.main, reloadJson=True)

            if hasattr(self.main, 'update_theme_settings'):
                self.main.update_theme_settings()

            # ✅ ส่วนนี้คือหัวใจสำคัญที่ส่งสัญญาณออกไป
            if hasattr(self.main, "theme_changed"):
                self.main.theme_changed.emit()
                log.info("Theme changed signal emitted to all dialogs")

    def LoadProductSansFont(self):
        """Load and apply product sans font"""
        font_id = QFontDatabase.addApplicationFont("./fonts/google-sans-cufonfonts/ProductSans-Regular.ttf")

        if font_id == -1:
            log.warning("Failed to load product font")
            return

        font_family = QFontDatabase.applicationFontFamilies(font_id)
        if font_family :
            product_sans = QFont(font_family[0])
        else:
            product_sans = QFont("Sans Serif")

        #เพิ่มใน main
        self.main.setFont(product_sans)

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

class GuiFunctions():
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.ui = MainWindow.ui
        self.ui_config = config_manager.get_ui_config()

        #initializeAppTheme
        self.initializeAppTheme()

        #load font
        self.LoadProductSansFont()

        # add click evemt to search button
        #self.ui.searchBtn.clicked.connect(self.showSearchResults)

        #connect menu btns
        self.connectMenuButtons()
         # ✅ เพิ่ม: ตั้งค่า configuration menu
        self.setup_configuration_menu()

    ##################################################################################################
    # setup config
    ##################################################################################################
    def setup_configuration_menu(self):
        """Add configuration menu to the application"""
        # ใช้ปุ่ม communicationBtn ที่มีอยู่ใน UI แทน settingsBtn
        if hasattr(self.ui, 'communication'):
            self.ui.communication.clicked.connect(self.show_config_dialog)
        else:
            print("Warning: communicationBtn not found in UI")

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
            print(f"Error applying UI config: {e}")

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
                print("✅ Theme changed signal emitted to all dialogs")

    def LoadProductSansFont(self):
        """Load and apply product sans font"""
        font_id = QFontDatabase.addApplicationFont("./fonts/google-sans-cufonfonts/ProductSans-Regular.ttf")

        if font_id == -1:
            print("Failed to load product font")
            return

        font_family = QFontDatabase.applicationFontFamilies(font_id)
        if font_family :
            product_sans = QFont(font_family[0])
        else:
            product_sans = QFont("Sans Serif")

        #เพิ่มใน main
        self.main.setFont(product_sans)

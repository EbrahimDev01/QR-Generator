import sys
import qrcode
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from GUIs.qr_generator_ui import Ui_MainWindow
from show_qr_generated_by_your_text import ShowQRGeneratedByYourTextWindow


class QRGeneratorWindow(QMainWindow):
    def __init__(self):
        super(QRGeneratorWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.child_window = ShowQRGeneratedByYourTextWindow(self)
        self.ui.setupUi(self)
        self.setup_events()

    def setup_events(self):
        self.ui.btn_qr_generate.clicked.connect(lambda: asyncio.run(self.qr_generate()))

    async def qr_generate(self):
        text = self.ui.plain_text_edit_convert_to_qr.toPlainText().strip()
        if len(text.strip()) > 0:
            img = qrcode.make(text)
            await asyncio.create_task(self.child_window.load_image_qr_generated(img))
            if self.child_window.isHidden():
                self.child_window.show()
        else:
            QMessageBox(QMessageBox.Warning, 'Warning', 'Enter Text', parent=self).exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QRGeneratorWindow()
    window.show()
    sys.exit(app.exec_())

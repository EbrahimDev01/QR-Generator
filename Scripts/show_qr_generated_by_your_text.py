from GUIs.show_qr_generated_by_your_text_ui import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap
import io
import asyncio


class ShowQRGeneratedByYourTextWindow(QMainWindow):
    def __init__(self, got_parent=None):
        super(ShowQRGeneratedByYourTextWindow, self).__init__(got_parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.image_qr = None
        self.setup_events()

    def setup_events(self):
        # setup events btn clicked
        self.ui.btn_show_file_dialog_save_file_url.clicked.connect(self.save_image_qr)

    async def load_image_qr_generated(self, got_image_qr):
        self.image_qr = got_image_qr
        pixmap = await convert_pil_image_to_q_pixmap(got_image_qr)
        self.ui.label_show_image_qr.setPixmap(pixmap)

    def save_image_qr(self):
        if self.image_qr is not None:
            default_name = 'QrCode'
            file_path_location = QFileDialog.getSaveFileName(self, 'Select Path Location for Save Image Qr',
                                                             default_name, 'Image Files (*.png *.jpg)')
            file_path_location = file_path_location[0].strip()
            if len(file_path_location) <= 0:
                file_path_location = default_name

            file_extension = file_path_location.lower()[-4:]
            if '.png' != file_extension and \
                    '.jpg' != file_extension:
                file_path_location += '.png'

            self.image_qr.save(file_path_location)


async def convert_pil_image_to_q_pixmap(got_pil_image):
    img_byte_arr = io.BytesIO()
    got_pil_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    pixmap = QPixmap()
    pixmap.loadFromData(img_byte_arr)
    return pixmap


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShowQRGeneratedByYourTextWindow()
    import qrcode

    img = qrcode.make("It's Not Enough, I Want Infinity")
    window.show()
    asyncio.run(window.load_image_qr_generated(img))
    sys.exit(app.exec_())

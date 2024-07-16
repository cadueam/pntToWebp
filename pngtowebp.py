import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit
)
from PIL import Image

class ImageConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Selecionar pasta para transformar imagens para webP", self)
        layout.addWidget(self.label)

        self.input_label = QLabel("Pasta selecionada:", self)
        layout.addWidget(self.input_label)
        self.input_field = QLineEdit(self)
        self.input_field.setReadOnly(True)
        layout.addWidget(self.input_field)

        self.input_button = QPushButton('Escolha pasta', self)
        self.input_button.clicked.connect(self.showInputDialog)
        layout.addWidget(self.input_button)

        self.convert_button = QPushButton('Converter', self)
        self.convert_button.clicked.connect(self.convert_images)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)
        self.setWindowTitle('STDQ')
        self.setGeometry(300, 300, 400, 200)
        self.show()

        self.input_folder = ""

    def showInputDialog(self):
        self.input_folder = str(QFileDialog.getExistingDirectory(self, "Selecionar Diretório"))
        if self.input_folder:
            self.input_field.setText(self.input_folder)

    def convert_images(self):
        if not self.input_folder:
            self.label.setText("Escolha uma pasta, por favor!")
            return

        self.label.setText("Convertendo imagens!")
        QApplication.processEvents()

        output_folder = self.input_folder + "_webp"
        shutil.copytree(self.input_folder, output_folder)

        max_size_kb = 150
        files_converted = 0

        for root, dirs, files in os.walk(output_folder):
            for filename in files:
                if filename.endswith(".png"):
                    img_path = os.path.join(root, filename)
                    img = Image.open(img_path)
                    new_filename = os.path.splitext(filename)[0] + ".webp"
                    webp_path = os.path.join(root, new_filename)

                    quality = 100
                    img.save(webp_path, "WEBP", quality=quality)
                    while os.path.getsize(webp_path) > max_size_kb * 1024 and quality > 0:
                        quality -= 5
                        img.save(webp_path, "WEBP", quality=quality)

                    os.remove(img_path)  #Remove os arquivos PNG
                    files_converted += 1

        self.label.setText(f"Conversão completa! {files_converted} arquivos convertidos. Pasta de saída: {output_folder}")

if __name__ == "__main__":
    app = QApplication([])
    ex = ImageConverterApp()
    app.exec_()

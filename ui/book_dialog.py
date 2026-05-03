from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QComboBox, QSpinBox, QPushButton, QMessageBox
)

class BookDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Form Buku")

        self.judul = QLineEdit()
        self.penulis = QLineEdit()

        self.genre = QComboBox()
        self.genre.addItems(["Novel", "Edukasi", "Komik"])

        self.status = QComboBox()
        self.status.addItems(["Belum Dibaca", "Sedang Dibaca", "Selesai"])

        self.rating = QSpinBox()
        self.rating.setRange(1, 5)

        if data:
            self.judul.setText(data[0])
            self.penulis.setText(data[1])
            self.genre.setCurrentText(data[2])
            self.status.setCurrentText(data[3])
            self.rating.setValue(int(data[4]))

        layout = QFormLayout()
        layout.addRow("Judul", self.judul)
        layout.addRow("Penulis", self.penulis)
        layout.addRow("Genre", self.genre)
        layout.addRow("Status", self.status)
        layout.addRow("Rating", self.rating)

        btn = QPushButton("Simpan")
        btn.clicked.connect(self.validate)
        layout.addWidget(btn)

        self.setLayout(layout)

    def validate(self):
        if len(self.judul.text()) < 2:
            QMessageBox.warning(self, "Error", "Judul minimal 2 karakter")
            return
        if len(self.penulis.text()) < 2:
            QMessageBox.warning(self, "Error", "Penulis minimal 2 karakter")
            return
        self.accept()

    def get_data(self):
        return (
            self.judul.text(),
            self.penulis.text(),
            self.genre.currentText(),
            self.status.currentText(),
            self.rating.value()
        )
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QAbstractItemView, QHeaderView

from controllers.controller import Controller
from ui.book_dialog import BookDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Smart Book Dashboard")
        self.resize(1100, 650)

        self.controller = Controller()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main = QVBoxLayout()

        menubar = self.menuBar()
        menu_help = menubar.addMenu("Tentang")

        about_action = QAction("Tentang Aplikasi", self)
        about_action.triggered.connect(self.show_about)
        menu_help.addAction(about_action)

        title = QLabel("📊 Smart Book Dashboard")
        title.setObjectName("title")

        info = QLabel("Nama: SYAZWANI | NIM: F1D02310140")
        info.setObjectName("info")

        self.stat_total = QLabel("0")
        self.stat_done = QLabel("0")
        self.stat_reading = QLabel("0")

        stat_layout = QGridLayout()
        stat_layout.setSpacing(12)

        stat_layout.addWidget(self.create_stat("Total Buku", self.stat_total, "#38bdf8"), 0, 0)
        stat_layout.addWidget(self.create_stat("Selesai", self.stat_done, "#22c55e"), 0, 1)
        stat_layout.addWidget(self.create_stat("Sedang Dibaca", self.stat_reading, "#facc15"), 0, 2)

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Cari judul atau penulis...")
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self.load_data)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Judul", "Penulis", "Genre", "Status", "Rating", "Aksi"]
        )
        self.table.setColumnHidden(0, True)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setColumnWidth(6, 200)

        btn_add = QPushButton("➕ Tambah Buku")
        btn_add.setObjectName("primary")
        btn_add.clicked.connect(self.add_book)

        main.addWidget(title)
        main.addWidget(info)
        main.addSpacing(10)
        main.addLayout(stat_layout)
        main.addWidget(self.search)
        main.addSpacing(10)
        main.addWidget(self.table)
        main.addWidget(btn_add)

        container = QWidget()
        container.setLayout(main)
        self.setCentralWidget(container)

    def create_stat(self, label, value, color):
        container = QFrame()
        container.setObjectName("statCard")

        label_widget = QLabel(label)
        label_widget.setObjectName("statLabel")

        value.setObjectName("statValue")

        accent = QFrame()
        accent.setFixedWidth(5)
        accent.setStyleSheet(f"background:{color}; border-radius:3px;")

        content = QVBoxLayout()
        content.addWidget(label_widget)
        content.addWidget(value)

        row = QHBoxLayout()
        row.addWidget(accent)
        row.addSpacing(10)
        row.addLayout(content)

        container.setLayout(row)
        return container

    def load_data(self):
        # RESET TOTAL TABLE (INI KUNCI FIX BUG)
        self.table.clearContents()
        self.table.setRowCount(0)

        all_data = self.controller.get_books()

        keyword = self.search.text().strip().lower()

        if keyword == "":
            data = all_data
        else:
            data = []
            for d in all_data:
                if keyword in d[1].lower() or keyword in d[2].lower():
                    data.append(d)

        total = len(data)
        done = len([d for d in data if d[4] == "Selesai"])
        reading = len([d for d in data if d[4] == "Sedang Dibaca"])

        self.stat_total.setText(str(total))
        self.stat_done.setText(str(done))
        self.stat_reading.setText(str(reading))

        if not data:
            self.table.setRowCount(1)

            empty = QTableWidgetItem("📚 Belum ada data buku.")
            empty.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(0, 0, empty)
            self.table.setSpan(0, 0, 1, self.table.columnCount())
            return

        self.table.setRowCount(len(data))

        for r, row in enumerate(data):
            self.table.setRowHeight(r, 50)

            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))

                if c == 5:
                    rating = int(val)
                    if rating >= 4:
                        item.setBackground(QColor("#166534"))
                    elif rating == 3:
                        item.setBackground(QColor("#92400e"))
                    else:
                        item.setBackground(QColor("#7f1d1d"))

                self.table.setItem(r, c, item)

            btn_widget = QWidget()

            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(6, 6, 6, 6)
            btn_layout.setSpacing(8)
            btn_layout.setAlignment(Qt.AlignCenter)

            btn_edit = QPushButton("Edit")
            btn_delete = QPushButton("Hapus")

            btn_edit.setObjectName("btnEdit")
            btn_delete.setObjectName("btnDelete")

            btn_edit.setFixedSize(70, 30)
            btn_delete.setFixedSize(70, 30)

            btn_edit.clicked.connect(lambda _, b=row: self.edit_book(b))
            btn_delete.clicked.connect(lambda _, i=row[0]: self.delete_book(i))

            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_delete)

            btn_widget.setLayout(btn_layout)
            self.table.setCellWidget(r, 6, btn_widget)

    def add_book(self):
        d = BookDialog()
        if d.exec():
            self.controller.add_book(d.get_data())
            self.load_data()

    def edit_book(self, book):
        d = BookDialog(book[1:])
        if d.exec():
            self.controller.update_book(book[0], d.get_data())
            self.load_data()

    def delete_book(self, book_id):
        if QMessageBox.question(self, "Konfirmasi", "Hapus buku?") == QMessageBox.Yes:
            self.controller.delete_book(book_id)
            self.load_data()

    def show_about(self):
        QMessageBox.information(
            self,
            "Tentang Aplikasi",
            "Smart Book Dashboard\n\n"
            "Aplikasi manajemen buku.\n\n"
            "Nama: SYAZWANI\n"
            "NIM: F1D02310140"
        )
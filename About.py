
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("About")
        self.resize(450, 300)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Ice Cream Profits")
        title.setObjectName("mainTitle")
        layout.addWidget(title)

        name = QLabel("Created by: Hof Moscow")
        layout.addWidget(name)

        email = QLabel("Email: hmoscow1234@gmail.com")
        layout.addWidget(email)

        github = QLabel(
            '<a href="https://github.com/hof-moscow/Ice-Cream-Profits">'
            'GitHub Repository</a>'
        )
        github.setOpenExternalLinks(True)
        layout.addWidget(github)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

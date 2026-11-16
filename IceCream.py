from About import AboutWindow
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class IceCreamWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = ""
        self.temperatures = []
        self.revenues = []
        self.about_window = AboutWindow()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ice Cream Profits")
        self.resize(850, 650)

        layout = QVBoxLayout()

        title = QLabel("Ice Cream Sales Analysis")
        title.setObjectName("mainTitle")
        layout.addWidget(title)

        self.file_button = QPushButton("Select CSV File")
        self.file_button.clicked.connect(self.choose_file)
        layout.addWidget(self.file_button)

        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)

        # Matplotlib graph
        self.figure = Figure(figsize=(7, 5))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.about_window.show)
        layout.addWidget(self.about_button)

        self.setLayout(layout)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.draw_plot()

    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Ice Cream Data", "", "CSV Files (*.csv)"
        )

        if file_name:
            self.selected_file = file_name
            self.file_label.setText(file_name)

    def draw_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Temporary graph
        ax.plot([1, 2, 3, 4], [2, 4, 3, 6])

        ax.set_title("Example Graph")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IceCreamWindow()
    window.show()
    app.exec()

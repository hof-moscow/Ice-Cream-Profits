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
            self.temperatures = []
            self.revenues = []

            with open(file_name, "r") as f:
                next(f)  # Skip the header

                for line in f:
                    temperature, revenue = line.strip().split(",")

                    self.temperatures.append(float(temperature))
                    self.revenues.append(float(revenue))

            self.file_label.setText(
                f"Loaded {len(self.temperatures)} records"
            )

            self.draw_plot()


    
    def draw_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if self.temperatures:
            ax.scatter(self.temperatures, self.revenues, s=1)
        else:
            # Temporary graph before loading a file
            ax.plot([1, 2, 3, 4], [2, 4, 3, 6])

        ax.set_title("Ice Cream Revenue vs Temperature")
        ax.set_xlabel("Temperature")
        ax.set_ylabel("Revenue")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        self.canvas.draw()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IceCreamWindow()
    window.show()
    app.exec()

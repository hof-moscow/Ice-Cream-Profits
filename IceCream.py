from About import AboutWindow
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog,QCheckBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np


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

        self.trend_checkbox = QCheckBox("Show Trend Line")
        self.trend_checkbox.setChecked(True)
        self.trend_checkbox.clicked.connect(self.draw_plot)
        layout.addWidget(self.trend_checkbox)



        self.figure = Figure(figsize=(7, 5))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.stats_label = QLabel("Statistics will appear after loading a file")
        self.stats_label.setObjectName("statsLabel")
        layout.addWidget(self.stats_label)

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

            count = len(self.temperatures)
            min_temp = min(self.temperatures)
            max_temp = max(self.temperatures)
            avg_revenue = sum(self.revenues) / len(self.revenues)

            self.stats_label.setText(
                f"Records: {count}  |  "
                f"Temperature: {min_temp:.1f} - {max_temp:.1f}  |  "
                f"Average Revenue: {avg_revenue:.2f}"
            )

            self.draw_plot()


    
    def draw_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)


   
        if self.temperatures:
            ax.scatter(self.temperatures, self.revenues, s=1, label="Data")

            if self.trend_checkbox.isChecked():
                coefficients = np.polyfit(self.temperatures, self.revenues, 1)
                line_function = np.poly1d(coefficients)

                line_x = np.linspace(min(self.temperatures), max(self.temperatures), 100)
                line_y = line_function(line_x)

                ax.plot(line_x, line_y, color="red", label="Trend Line")

                ax.text(
                    0.05, 0.95,
                    f"y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}",
                    transform=ax.transAxes,
                    color="red",
                    verticalalignment="top"
                )

            ax.legend()


        else:
            # גרף זמני לפני טעינת נתונים
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

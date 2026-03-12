import sys
from PySide6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ISR Sensor Coverage Planner")
        self.resize(1200, 800)


def main():
    print("Starting app...")
    app = QApplication(sys.argv)
    print("QApplication created")
    window = MainWindow()
    print("MainWindow created")
    window.show()
    print("Window shown")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
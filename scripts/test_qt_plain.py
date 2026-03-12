import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Plain Qt Test")
    window.resize(800, 600)

    label = QLabel("Plain Qt window works", parent=window)
    label.move(50, 50)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
import sys
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtInteractor Test")
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        self.plotter = QtInteractor(self)
        layout.addWidget(self.plotter.interactor)

        self.plotter.add_mesh(pv.Sphere(), color="lightblue")
        self.plotter.reset_camera()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
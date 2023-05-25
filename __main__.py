import sys

import PyQt5.QtWidgets as pq

from demodulation import DemodulationWindow
from modulation import ModulationWindow


class MainWindow(pq.QMainWindow):
    def __init__(self):
        super().__init__()

        modulation_window = ModulationWindow()
        modulation_window.exec()

        demodulation_window = DemodulationWindow()
        demodulation_window.exec()


def main() -> None:
    app = pq.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.close()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

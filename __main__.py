import sys

import PyQt5.QtWidgets as pq

from modulation import ModulationWindow


def main() -> None:
    app = pq.QApplication(sys.argv)
    modulation_window = ModulationWindow()
    modulation_window.show()
    app.exec()

    sys.exit()


if __name__ == '__main__':
    main()

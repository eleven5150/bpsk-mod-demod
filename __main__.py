import sys
from dataclasses import dataclass

import PyQt5.QtWidgets as pq


@dataclass
class Signal:
    sampling_freq: int
    carrier_freq: int
    noise_level: int
    data_period: int
    data_size: int
    data: bytes

    @classmethod
    def raw_to_signal(
            cls,
            sampling_freq: str,
            carrier_freq: str,
            noise_level: str,
            data_period: str,
            data_size: str,
            data: bytes
    ) -> "Signal":
        return cls(
            sampling_freq=int(sampling_freq),
            carrier_freq=int(carrier_freq),
            noise_level=int(noise_level),
            data_period=int(data_period),
            data_size=int(data_size),
            data=data
        )


class ModulationWindow(pq.QDialog):
    def __init__(self):
        super(ModulationWindow, self).__init__()
        self.setWindowTitle("BPSK Modulator")

        self.setGeometry(500, 500, 500, 500)

        self.modulation_group: pq.QGroupBox = pq.QGroupBox()

        self.sampling_freq: pq.QLineEdit = pq.QLineEdit()
        self.carrier_freq: pq.QLineEdit = pq.QLineEdit()
        self.noise_level: pq.QLineEdit = pq.QLineEdit()
        self.data_period: pq.QLineEdit = pq.QLineEdit()
        self.data_size: pq.QLineEdit = pq.QLineEdit()

        self.upload_mod_data_button: pq.QPushButton = pq.QPushButton("Upload")
        self.upload_mod_data_button.clicked.connect(self.get_modulated_data)

        self.modulate_button: pq.QPushButton = pq.QPushButton("Modulate", self)
        self.modulate_button.clicked.connect(self.modulate)

        self.create_form()

        main_layout: pq.QVBoxLayout = pq.QVBoxLayout()
        main_layout.addWidget(self.modulation_group)

        self.setLayout(main_layout)

        self.input_data: bytes = bytes()

    def create_form(self) -> None:
        layout = pq.QFormLayout()

        layout.addRow(pq.QLabel("Sampling frequency"), self.sampling_freq)
        layout.addRow(pq.QLabel("Carrier frequency"), self.carrier_freq)
        layout.addRow(pq.QLabel("Noise level"), self.noise_level)
        layout.addRow(pq.QLabel("Data period"), self.data_period)
        layout.addRow(pq.QLabel("Data size"), self.data_size)
        layout.addRow(pq.QLabel("Upload data"), self.upload_mod_data_button)
        layout.addRow(self.modulate_button)

        self.modulation_group.setLayout(layout)

    def get_modulated_data(self) -> None:
        filename: str = pq.QFileDialog.getOpenFileName(self, caption='Choose File')[0]
        with open(filename, "rb") as input_data_file:
            self.input_data = input_data_file.read()

    def modulate(self) -> None:
        signal: Signal = Signal.raw_to_signal(
            self.sampling_freq,
            self.carrier_freq,
            self.noise_level,
            self.data_period,
            self.data_size,
            self.input_data
        )



def main() -> None:
    app = pq.QApplication(sys.argv)
    window = ModulationWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

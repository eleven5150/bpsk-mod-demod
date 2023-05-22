import sys
import PyQt5.QtWidgets as pq


class ModulationWindow(pq.QDialog):
    def __init__(self):
        super(ModulationWindow, self).__init__()
        self.setWindowTitle("BPSK Modulator")

        self.setGeometry(500, 500, 500, 500)

        self.modulation_group = pq.QGroupBox()

        self.sampling_freq = pq.QLineEdit()
        self.carrier_freq = pq.QLineEdit()
        self.noise_level = pq.QLineEdit()
        self.data_period = pq.QLineEdit()
        self.data_size = pq.QLineEdit()

        self.upload_mod_data_button = pq.QPushButton("Upload", self)
        self.upload_mod_data_button.clicked.connect(self.get_modulated_data)

        self.modulate_button = pq.QPushButton("Modulate", self)
        self.modulate_button.clicked.connect(self.modulate)

        self.create_form()

        main_layout = pq.QVBoxLayout()
        main_layout.addWidget(self.modulation_group)

        self.setLayout(main_layout)

    def get_info(self):
        print(f"Sampling freq : {self.sampling_freq.text()}")
        print(f"Carrier frequency : {self.carrier_freq.text()}")
        print(f"Noise level : {self.noise_level.text()}")
        print(f"Data period : {self.data_period.text()}")
        print(f"Data size : {self.data_size.text()}")

        self.close()

    def create_form(self):
        layout = pq.QFormLayout()

        layout.addRow(pq.QLabel("Sampling frequency"), self.sampling_freq)
        layout.addRow(pq.QLabel("Carrier frequency"), self.carrier_freq)
        layout.addRow(pq.QLabel("Noise level"), self.noise_level)
        layout.addRow(pq.QLabel("Data period"), self.data_period)
        layout.addRow(pq.QLabel("Data size"), self.data_size)
        layout.addRow(pq.QLabel("Upload data"), self.upload_mod_data_button)
        layout.addRow(self.modulate_button)

        self.modulation_group.setLayout(layout)

    def get_modulated_data(self):
        pass

    def modulate(self):
        pass


def main():
    app = pq.QApplication(sys.argv)
    window = ModulationWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

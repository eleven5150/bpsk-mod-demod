import PyQt5.QtWidgets as pq


class DemodulationWindow(pq.QDialog):
    def __init__(self):
        super(DemodulationWindow, self).__init__()
        self.setWindowTitle("BPSK Demodulator")

        self.setGeometry(0, 0, 500, 200)

        self.demodulation_group: pq.QGroupBox = pq.QGroupBox()

        self.upload_mod_data_button: pq.QPushButton = pq.QPushButton("Upload")
        self.upload_mod_data_button.clicked.connect(self.get_modulated_signal_data)

        self.demodulate_button: pq.QPushButton = pq.QPushButton("Demodulate", self)
        self.demodulate_button.clicked.connect(self.demodulate)

        self.create_form()

        main_layout: pq.QVBoxLayout = pq.QVBoxLayout()
        main_layout.addWidget(self.demodulation_group)

        self.setLayout(main_layout)

        self.input_data: str = str()

    def create_form(self) -> None:
        layout = pq.QFormLayout()

        layout.addRow(pq.QLabel("Upload modulated data"), self.upload_mod_data_button)
        layout.addRow(self.demodulate_button)

        self.demodulation_group.setLayout(layout)

    def get_modulated_signal_data(self) -> None:
        filename: str = pq.QFileDialog.getOpenFileName(self, caption='Choose File')[0]
        with open(filename, "rt") as modulated_data_file:
            self.input_data = modulated_data_file.read()

    def demodulate(self):
        pass

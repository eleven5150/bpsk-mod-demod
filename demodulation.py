import json
import math
from dataclasses import dataclass

import PyQt5.QtWidgets as pq
import numpy as np
from matplotlib import pyplot as plt

from extensions import low_pass_filter, BITS_IN_BYTE


@dataclass
class ModulatedSignal:
    sampling_freq: int
    carrier_freq: int
    data_period: int
    data: np.ndarray

    @classmethod
    def data_to_modulated_signal(cls, file_data: str) -> "ModulatedSignal":
        parsed_modulated_signal: dict[str, any] = json.loads(file_data)
        return cls(
            sampling_freq=parsed_modulated_signal["sampling_freq"],
            carrier_freq=parsed_modulated_signal["carrier_freq"],
            data_period=parsed_modulated_signal["data_period"],
            data=np.asarray(parsed_modulated_signal["modulated_signal"])
        )


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
        modulated_signal: ModulatedSignal = ModulatedSignal.data_to_modulated_signal(self.input_data)

        signal_length: float = modulated_signal.data.size / modulated_signal.sampling_freq
        time_points: np.ndarray = np.arange(0, signal_length, 1 / modulated_signal.sampling_freq)

        cos_points: list[float] = [2 * math.pi * x * modulated_signal.carrier_freq for x in time_points]
        carrier_signal: np.ndarray = np.cos(cos_points)

        tmp_signal: np.ndarray = np.multiply(modulated_signal.data, carrier_signal)
        demodulated_signal: np.ndarray = low_pass_filter(
            tmp_signal,
            modulated_signal.carrier_freq,
            modulated_signal.sampling_freq
        )
        digital_signal: np.ndarray = demodulated_signal > 0.1

        plt.plot(time_points, modulated_signal.data)
        plt.plot(time_points, digital_signal)
        plt.xlabel("Time, s")
        plt.ylabel("Signal level")
        plt.grid()
        plt.ion()
        plt.show()

        data_bits_raw: list[int] = list()
        for offset in range(modulated_signal.data_period//2, digital_signal.size, modulated_signal.data_period):
            data_bits_raw.append(digital_signal[offset])

        data_bits: np.ndarray = np.asarray(data_bits_raw)

        data_bytes = np.split(data_bits, data_bits.size / BITS_IN_BYTE)
        result_bytes = bytes()
        for byte in data_bytes:
            result_bytes += int("".join(str(int(x)) for x in byte), 2).to_bytes(1, "little")

        with open("demodulated_data.bin", "wb") as demodulated_data_file:
            demodulated_data_file.write(result_bytes)

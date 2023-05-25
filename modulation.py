import math
import json

import numpy as np
import PyQt5.QtWidgets as pq

from dataclasses import dataclass
from matplotlib import pyplot as plt

from demodulation import DemodulationWindow
from extensions import byte_to_bin, bin_to_bpsk, BITS_IN_BYTE

plt.rcParams['figure.dpi'] = 300


@dataclass
class SourceSignal:
    sampling_freq: int
    carrier_freq: int
    noise_level: int
    data_period: int
    signal_length: float
    time_points: np.ndarray
    data_size: int
    data: bytes

    @classmethod
    def raw_to_source_signal(
            cls,
            sampling_freq_i: str,
            carrier_freq_i: str,
            noise_level_i: str,
            data_period_i: str,
            data_size_i: str,
            data: bytes
    ) -> "SourceSignal":
        sampling_freq: int = int(sampling_freq_i)
        carrier_freq: int = int(carrier_freq_i)
        noise_level: int = int(noise_level_i)
        data_period: int = int(data_period_i)
        data_size: int = int(data_size_i)
        signal_length: float = data_period * data_size * BITS_IN_BYTE / sampling_freq
        time_points: np.ndarray = np.arange(0, signal_length, 1 / sampling_freq)
        return cls(
            sampling_freq=sampling_freq,
            carrier_freq=carrier_freq,
            noise_level=noise_level,
            data_period=data_period,
            signal_length=signal_length,
            time_points=time_points,
            data_size=data_size,
            data=data[:data_size]
        )

    def save_modulated_signal_to_file(self, modulated_signal: np.ndarray) -> None:
        output_file: dict[str, any] = {
            "sampling_freq": self.sampling_freq,
            "carrier_freq": self.carrier_freq,
            "data_period": self.data_period,
            "modulated_signal": modulated_signal.tolist()
        }

        json_output_file: str = json.dumps(output_file, indent=4)
        with open("modulated_signal.json", "wt") as modulated_signal_file:
            modulated_signal_file.write(json_output_file)

    def add_noise(self, modulated_signal: np.ndarray) -> np.ndarray:
        modulated_signal_power: np.ndarray = modulated_signal ** 2
        modulated_signal_avg_power: np.ndarray = np.mean(modulated_signal_power)
        modulated_signal_avg_power_db: int = 10 * np.log10(modulated_signal_avg_power)
        noise_level_db: int = modulated_signal_avg_power_db - self.noise_level
        noise_level_avr_power: float = 10 ** (noise_level_db / 10)
        noise_level_power: np.foat64 = np.sqrt(noise_level_avr_power)
        print(type(noise_level_power))

        noise_signal: np.ndarray = np.random.normal(0, noise_level_power, modulated_signal.size)

        return modulated_signal + noise_signal


class ModulationWindow(pq.QDialog):
    def __init__(self):
        super(ModulationWindow, self).__init__()
        self.setWindowTitle("BPSK Modulator")

        self.setGeometry(0, 0, 500, 400)

        self.modulation_group: pq.QGroupBox = pq.QGroupBox()

        self.sampling_freq: pq.QLineEdit = pq.QLineEdit()
        self.carrier_freq: pq.QLineEdit = pq.QLineEdit()
        self.noise_level: pq.QLineEdit = pq.QLineEdit()
        self.data_period: pq.QLineEdit = pq.QLineEdit()
        self.data_size: pq.QLineEdit = pq.QLineEdit()

        self.upload_source_data_button: pq.QPushButton = pq.QPushButton("Upload")
        self.upload_source_data_button.clicked.connect(self.get_source_signal_raw_data)

        self.modulate_button: pq.QPushButton = pq.QPushButton("Modulate", self)
        self.modulate_button.clicked.connect(self.modulate)

        self.create_form()

        main_layout: pq.QVBoxLayout = pq.QVBoxLayout()
        main_layout.addWidget(self.modulation_group)

        self.setLayout(main_layout)

        self.input_data: bytes = bytes()
        self.demodulation_window = None

    def create_form(self) -> None:
        layout = pq.QFormLayout()

        layout.addRow(pq.QLabel("Sampling frequency"), self.sampling_freq)
        layout.addRow(pq.QLabel("Carrier frequency"), self.carrier_freq)
        layout.addRow(pq.QLabel("Noise level"), self.noise_level)
        layout.addRow(pq.QLabel("Data period"), self.data_period)
        layout.addRow(pq.QLabel("Data size"), self.data_size)
        layout.addRow(pq.QLabel("Upload data"), self.upload_source_data_button)
        layout.addRow(self.modulate_button)

        self.modulation_group.setLayout(layout)

    def get_source_signal_raw_data(self) -> None:
        filename: str = pq.QFileDialog.getOpenFileName(self, caption='Choose File')[0]
        with open(filename, "rb") as input_data_file:
            self.input_data = input_data_file.read()

    def modulate(self) -> None:
        source_signal: SourceSignal = SourceSignal.raw_to_source_signal(
            self.sampling_freq.text(),
            self.carrier_freq.text(),
            self.noise_level.text(),
            self.data_period.text(),
            self.data_size.text(),
            self.input_data
        )

        cos_points: list[float] = [2 * math.pi * x * source_signal.carrier_freq for x in source_signal.time_points]
        carrier_signal: np.ndarray = np.cos(cos_points)

        bpsk_data_values: list[int] = list()
        for byte in source_signal.data:
            binary: list[int] = byte_to_bin(byte)
            bpsk_binary: list[int] = bin_to_bpsk(binary)
            bpsk_data_values.extend(bpsk_binary)

        bpsk_data_signal: np.ndarray = np.repeat(bpsk_data_values, source_signal.data_period)

        modulated_signal: np.ndarray = np.multiply(carrier_signal, bpsk_data_signal)

        modulated_signal = source_signal.add_noise(modulated_signal)

        plt.plot(source_signal.time_points, modulated_signal)
        plt.xlabel("Time, s")
        plt.ylabel("Signal level")
        plt.grid()
        plt.ion()
        plt.show()

        source_signal.save_modulated_signal_to_file(modulated_signal)
        self.close()

BITS_IN_BYTE: int = 8


def byte_to_bin(number: int) -> list[int]:
    bin_number: str = bin(number)[2:]
    binary: list[int] = [int(x) for x in bin_number]
    zero_bits_len: int = BITS_IN_BYTE - len(bin_number)
    for bit in range(zero_bits_len):
        binary.insert(0, 0)

    return binary


def bin_to_bpsk(data: list[int]) -> list[int]:
    return [-1 if bit == 0 else bit for bit in data]

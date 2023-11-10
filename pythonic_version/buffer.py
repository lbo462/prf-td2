from typing import List

from models import Packet


class BufferEmpty(Exception):
    """Raised when trying to remove a packet from an empty buffer"""


class BufferFull(Exception):
    """Raised when trying to add a packet to a full buffer"""


class Buffer:
    """Holds a list of packets"""

    def __init__(self, size: int):
        # Init with an empty list of packets
        self.max_size = size
        self.packets: List[Packet] = []

    @property
    def amount_of_packets_in(self) -> int:
        return len(self.packets)

    def add_packet(self, p: Packet):
        if self.amount_of_packets_in == self.max_size:
            raise BufferFull()

        self.packets.append(p)

    def remove_first_packet(self) -> Packet:
        """Removes and return the first packet in the buffer"""

        # Treat empty buffer
        if not self.packets:
            raise BufferEmpty()

        return self.packets.pop(0)  # removes at first index

    def __str__(self) -> str:
        out = ""
        for _ in range(self.max_size - self.amount_of_packets_in):
            out += "[]"
        for _ in range(self.amount_of_packets_in):
            out += "[x]"
        return out

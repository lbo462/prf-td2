from dataclasses import dataclass

"""Entities
Defines the simulation entities that interact with each other
"""


@dataclass
class Packet:
    """
    Single piece of information contained in a buffer
    No attributes seems to be useful here, hence the class is empty
    """


"""System state
The system is defined by its state
This state should be sufficient to compute the metrics
"""


@dataclass
class SystemState:
    """
    Defines the system state
    Keep count on the packets states
    """

    # Total count of the packets that went though the buffer
    packets_went_though_buffer: int

    # Amount of lost packets
    packets_lost: int

    def get_error_rate(self) -> float:
        return self.packets_lost / self.packets_went_though_buffer

    def get_mean(self, lambda_: float) -> float:
        return (1 - self.get_error_rate()) * lambda_

    def __str__(self) -> str:
        return (
            f"| Packets went though buffer : {self.packets_went_though_buffer} | "
            f"Packets lost : {self.packets_lost} |"
        )

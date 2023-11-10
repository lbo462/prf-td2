import numpy as np

from models import Packet, SystemState
from buffer import Buffer, BufferFull
from event import EventTypesEnum, EventScheduler, NoMoreEvents


def main():
    # Set parameters
    MAX_EVENTS = 10
    lambda_ = 1
    mu = 1
    k = 10

    # Create the system
    system = SystemState(
        packets_went_though_buffer=0, packets_in_the_buffer=0, packets_lost=0
    )

    # Create a new buffer instance of size k
    buffer = Buffer(size=k)

    # Create a event scheduler ...
    evt_scheduler = EventScheduler()

    # ... and add a first arrival event
    evt_scheduler.add(type_=EventTypesEnum.ARRIVAL, delay=0)

    evt_count = 0
    while evt_count < MAX_EVENTS:
        # Get the event
        try:
            evt = evt_scheduler.get_next()
        except NoMoreEvents:
            # If the scheduler has no events, break the loop
            break

        if not evt:
            # If no event is currently happening, just wait for the next one
            continue

        evt_count += 1

        if evt.type_ is EventTypesEnum.ARRIVAL:
            # Treat an arriving packet

            # Create a new packet
            packet = Packet()

            # Add the packet to the buffer
            try:
                buffer.add_packet(packet)

                # Increment the system counters
                system.packets_in_the_buffer += 1
                system.packets_went_though_buffer += 1

                # Create a new DEPARTURE event
                evt_scheduler.add(
                    type_=EventTypesEnum.DEPARTURE, delay=np.random.exponential(1 / mu)
                )
            except BufferFull:
                # If the buffer is full, update the system and create a new event
                system.packets_lost += 1

                evt_scheduler.add(
                    type_=EventTypesEnum.ARRIVAL,
                    delay=np.random.exponential(1 / lambda_),
                )

        elif evt.type_ is EventTypesEnum.DEPARTURE:
            # Treat a departing packet

            # Removes the first packet in the buffer
            packet = buffer.remove_first_packet()

            # Decrement the system counter
            system.packets_in_the_buffer -= 1

            # Create a new ARRIVAL event and add it to scheduler
            evt_scheduler.add(
                type_=EventTypesEnum.ARRIVAL, delay=np.random.exponential(1 / lambda_)
            )

        print(system)


if __name__ == "__main__":
    main()

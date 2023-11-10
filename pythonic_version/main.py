import numpy as np

from models import Packet, SystemState
from buffer import Buffer, BufferFull
from event import EventTypesEnum, EventScheduler, NoMoreEvents
from grapher import Grapher


def run_iters(max_evt: int, lambda_: int, mu: int, k: int) -> SystemState:
    # Create the system
    system = SystemState(incomming_packets=0, packets_lost=0)

    # Create a new buffer instance of size k
    buffer = Buffer(size=k)

    # Create a event scheduler ...
    evt_scheduler = EventScheduler()

    # ... and add a first arrival event
    evt_scheduler.add(type_=EventTypesEnum.ARRIVAL, delay=0)

    evt_count = 0
    while evt_count < max_evt:
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

        print(evt)
        print(f"Buffer : {buffer}")

        if evt.type_ is EventTypesEnum.ARRIVAL:
            # Treat an arriving packet

            # Add a new event in the list
            evt_scheduler.add(
                type_=EventTypesEnum.ARRIVAL,
                delay=np.random.exponential(1 / lambda_),
            )

            # Increment the system counter
            system.incomming_packets += 1

            # Create a new packet
            packet = Packet()

            # Add the packet to the buffer
            try:
                buffer.add_packet(packet)

                # Create a new DEPARTURE event
                evt_scheduler.add(
                    type_=EventTypesEnum.DEPARTURE, delay=np.random.exponential(1 / mu)
                )
            except BufferFull:
                # If the buffer is full, update the system and create a new event
                system.packets_lost += 1

        elif evt.type_ is EventTypesEnum.DEPARTURE:
            # Treat a departing packet

            # Removes the first packet in the buffer
            packet = buffer.remove_first_packet()

    print(system)
    print(
        f"| Mean : {system.get_mean(lambda_)} | "
        f"Error rate : {system.get_error_rate()}"
    )
    return system


def graph():
    grapher = Grapher()

    for k in [1, 5, 10, 15, 20, 25, 30, 40, 50, 70, 100]:
        for lambda_ in [500, 700, 900, 1000, 1100, 1300]:
            # Compute the mean error rate for the given parameters
            error_rates = []
            for _ in range(100):
                system = run_iters(
                    lambda_=lambda_,
                    mu=1000,
                    k=k,
                    max_evt=200,
                )
                error_rates.append(system.get_error_rate())

            mean_error = sum(error_rates) / len(error_rates)
            grapher.add(lambda_, k, mean_error)

    # Plot the graph
    # grapher.plot_set_arrival_rate(lambda_=...)
    # grapher.plot_set_buffer_size(k=...)


def main():
    system = run_iters(
        lambda_=10,
        mu=0.5,
        k=10,
        max_evt=1000,
    )
    print(f"Error rate : {system.get_error_rate()}")


if __name__ == "__main__":
    main()
    # graph()

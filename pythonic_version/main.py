import numpy as np

from models import Packet, SystemState
from buffer import Buffer, BufferFull
from event import EventTypesEnum, EventScheduler, NoMoreEvents
from grapher import Grapher


def run_iters(max_evt: int, lambda_: int, mu: int, k: int) -> SystemState:
    # Create the system
    system = SystemState(incoming_packets=0, packets_lost=0)

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

        # print the event and the buffer state
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
            system.incoming_packets += 1

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
            buffer.remove_first_packet()

    print(system)
    print(
        f"| Mean : {system.get_mean(lambda_)} | "
        f"Error rate : {system.get_error_rate()}"
    )
    return system


def main():
    system = run_iters(
        lambda_=5,
        mu=1,
        k=10,
        max_evt=1000,
    )
    print(f"Error rate : {system.get_error_rate()}")


def graph():
    grapher = Grapher()

    """
    When trying to plot a curve for a static value of k or lambda,
    it is highly recommanded to set the corresponding list to a single-value array
    in order to same your precious time
    """
    k_list = [1, 5, 10, 15, 20, 25, 30, 40, 50, 70, 100]
    lambda_list = [500, 700, 900, 1000, 1100, 1300]

    amount_of_runs = 100

    for k in k_list:
        for lambda_ in lambda_list:
            # Compute the mean error rate for the given parameters
            error_rates = []
            for _ in range(amount_of_runs):
                system = run_iters(
                    lambda_=lambda_,
                    mu=50,
                    k=k,
                    max_evt=200,
                )
                error_rates.append(system.get_error_rate())

            mean_error = sum(error_rates) / len(error_rates)
            grapher.add(lambda_, k, mean_error)

    # Plot the graph
    """
    Uncomment one of the following lines to display the graphs
    and set a value to lambda or k (that was used in k_list of lambda_list)
    
    Multiple graphs can be plotted
    """
    # grapher.plot_set_arrival_rate(lambda_=...)
    # grapher.plot_set_buffer_size(k=...)


if __name__ == "__main__":
    """
    The main() func runs a single iteration
    The graph() runs multiple times to create a graph

    Please check theses functions to have more details.
    """

    main()
    # graph()

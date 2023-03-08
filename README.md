# cs262assignment2
The goal of this exercise was to demonstrate synchronization behavior between three machines with different clock rates. Below is a manual with setup instructions, functionality, and engineering decisions for our simulation. 

## Running the simulation
On one terminal, run `python server.py`. The server is now up and will wait until all three clients to connect. 

On three other terminals, run `python client.py 1 [run_number]`, `python client.py 2 [run_number]`, and `python client.py 3 [run_number]`. 

`[run_number]` is an optional argument for logging purposes. You will see it as a prefix for log files, which will generate as `[run_number]_[machine_number].txt`.

## Engineering decisions
Most decisions were well-outlined by the assignment spec. Although it was possible to have 3 clients connect directly to each other, we chose to have a server intermediary handle the delivery of the messages.

In order to simulate different clock speeds, we create a clock_cycle function for each client that sleeps for 1/rate time at the beginning, where rate ranges from 1-6 (we experimented with smaller ranges, results noted in report.md). 

Each client keeps a message queue. If there are any messages, it will handle it by updating its own logical clock through the `update_logical_clock` method. This method takes the client's current logical clock value and the received one, and decides what the updated logical clock value should be (max of the 2 values, + 1). For internal events and sends, we simply set the received value to 0. 

Then we generate a random number from 1-10 (we experimented with smaller probability of running internal event, results noted in report.md). For 1, a message is sent to one client, for 2, a message is sent to the other client, for 3, a message is sent to both other clients, and for other events an "internal event" occurs.

A message consists of the random number generated (used by the server to determine message recipients) and the logical clock time.

## Experimental observations
View [report.md](https://github.com/karlyh66/cs262assignment2/blob/main/report.md).

## Lab Notebook
View notebook.md.
This is a lab notebook tracking our day-by-day progress. For a report of logical clock observations, see [report.md](https://github.com/karlyh66/cs262assignment2/blob/main/report.md).

March 1, 2023
=========================
Progress:
- Started basic client/machine code
- Implemented basic server code to connect client comms
- Client can send message any of the two (or both) other clients

Questions:
- Are the clients supposed to connect to each other? Or should we have a central 
  server "brokering" the communication?
    - For now we are implementing with a server but will see Ed feedback


March 5, 2023 
=========================
Progress:
Most logical clock functionality is implemented
- We now take random number generation into account to determine each machine's clock rate, and the action taken at each clock clock_cycle
- The code "responds" to the random number telling the client which other machine(s) to send the message to (if any), as encoded in the random number from 1-10
    - In particular, the server parses the message sent by the client, in the form `'<recipient code> <logical clock value>'`
    - Recipient code "1" means send to the first other machine, recipient code "2" means send to the second other machine, and recipient code "3" means send to both other machines
    - To each client, the "first other machine" remains the same machine throughout (as does the "second other machine")
- Implemented writing to logs
- Implemented actually simulating the clock rates by having client do a `time.sleep(2 / self.rate)` (will change to `1 / self.rate` later, but we wanted to observe things more slowly)
- Implemented properly updating the client clock value

Issues:
- We spent a long time trying to change our model to being a peer-to-peer based one, where each machine has a client and server thread that together send and receive to and from the two other machines
- However, the 3 machine + 1 server model still makes the most sense to us, and by the time we had thought of the peer-to-peer model, we had already fully implemented (the socket and send/receive parts of the) client/server framework

TODOs:
- Analyze log files in more detail
- Find a nicer way to run the three programs that do not involve manually specifying the machine ID (1, 2, or 3), since that is less than ideal design

March 6, 2023 
=========================
Progress:
- found some bugs with not closing sockets properly when the client disconnects
    - the specific bug we hit was a "broken pipe"
    - because of us having spawned two threads per client, we need a signal handler the whole process responds to
    - and we implemented this SIGINT signal handler in the client
    - also implemented the functionality of when one client shuts down, the other two also shut down (while server stays up)
- added unit tests
- started working on analysis report
- saved data not just in log.txt form but also in .csv form for easier and more versatile analysis
- started pandas code for analysis of csv, goal to create metrics/charts

March 7, 2023 
=========================
Progress:
- we found a bug caused by the clients already starting their clock cycles (so, sending messages) before all three clients are connected
    - this leads to the message parsing code (in the server) throwing an exception
    - for context, all of the messeges that each client sends to the server are of format `'<sender type> <logical clock value>'` (a concatenation of two ints, with a whitespace between them)
        - sender type = 1 if send is to the first other machine, 2 if send is to the second other machine, 3 if the send is to both machines
    - we fixed this bug by having the clients not go into the clock_cycle() infinite loop until sender sends them a message indicating that the all three clients have connected
- collected more data (we have 5 runs' worth of data now, in .txt and .csv format)
Next steps:
- data analysis
- consider starting to track system time from the moment all 3 clients connect to server
    - treat system time as "nanoseconds elapsed since the beginning of this system"
    - we currently only record nanoseconds since the UNIX epoch

March 8, 2023
=========================
Progress:
- updated logical clock unit test to test more cases
- added unit test for listen
- experimented with less variation in machine speed and less often internal events as suggested
  to observe results, noted in report.md
- completed data analysis for different machines and added observations to report


March 8, 2023 (evening)
=========================
Progress:
- did data analysis and visualization of the following aspects:
    - logical clock value over time
    - extent to which logical clock is overwritten by incoming message
    - length of message queue over time
    - frequency of send message vs. receive message vs. internal event
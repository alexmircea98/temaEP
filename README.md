# temaEP
Tema EP 2022-2023

TODO:
* Make a documentation in LaTeX?
* Use the file beforeHomeworkPyModules.txt to see what modules I installed for my hw? It is a
"before" snapshot.
* Do mention how the .pyc file works for python 3.8 and not 3.10? Lol

Installed deps:
* If running outside the virtual machine:
  * Python 3.8!
  * mininet
* On the mininet machine:
  * To be seen...

Documentation ideas?:
* 1st I started up the topology and used the help command to get a list of available tools.

Available tools from mininet machine:
* iperf and iperfudp:

  Measure network bandwidth between computers.
* dpctl: The  ovs-ofctl program is a command line tool for monitoring and admin‐
       istering OpenFlow switches.
* link: 
Bring link(s) between two nodes up or down.
           Usage: link node1 node2 [up/down]

How to answer II Eval:
*   How many requests can be handled by a single machine?
Use iperf commands, probably...
That gets me a list with two bandwidths in Kbits/sec
This probably explains that the 1st number is Upload speed and second number is Download speed:
https://github.com/esnet/iperf/issues/480#issuecomment-307205313
This question is a bit complex so answer it last?

*   What is the latency of each region?
Use pings and parse output?
Did multiple pings, 1st of which is done without being recorded to remove outlier case where
1st time routing is longer!

*   What is the server path with the smallest response time? But the slowest?
pings again?

*   What is the path that has the greatest loss percentage?
pings again?

*   What is the latency introduced by the first router in our path?
pings from c1 to hn stations and compare to pings from rx to hn?
n = station num & x = zone num

*   Is there any bottleneck in the topology? How would you solve this issue?
There may be, based on the previous data. Solve issue with better hw or a better topology (
connections and whatnot) or perhaps better routing software?

*   What is your estimation regarding the latency introduced?
...introduced? By what?

*   What downsides do you see in the current architecture design?
Probably more evident after gathering data.

BUG?
* UnicodeEncodeError: 'latin-1' codec can't encode character '\u03bc' in position 22: ordinal not
in range(256)
This was likely caused by the usage of miu instead of u in the python script...

# Illumio Coding Challenge!

As a preface, I wanted to say that I thoroughly enjoyed the coding challenge, as it had a large breadth of possible solutions and optimizations! While I was not able to implement my initial optimal solution, I felt like I had decent optimization and structured code.


## Design and Optimizations
In essence, this problem boiled down to a linked double range search. Testing direction and protocol matching was trivial with a hash table, but searching in a range and then again in another range would be more of a challenge. 

My first solution was to use a sorted array of port intervals, sorted by the starting index and containing a pointer to another structure that held a sorted array of ip intervals. A query would perform binary search on the first layer and then binary search again on the second layer. The problem was that for many intervals with the same starting index, I would still have to check every single one of them, making this O(p + i) time (p = # of port ranges, i = # of ip ranges).

My second approach came after a bit of googling. I had come across an [Interval Tree](https://en.wikipedia.org/wiki/Interval_tree). The idea was to have a 2d interval tree - the upper layer would contain the port intervals and each node contained an interval tree of the ip addresses. Querying would take O(logp + logi) time. However, I quickly realized that Python didn't come with any interval tree standard libraries and that this may be too ambitious for a challenge where I only had an hour.

My third approach was simpler and relied moreso on edge case optimization. I would have a dictionary of the four possible direction/protocol arrangements, each pointing to a data structure that contained a dictionary for insertions with one port and a list of ranges for insertions with more than one port.

Insertion was O(1) as it was either hashing or appending to the list.
Searching was O(p + i) worst case (every line in the .csv had a port range) as it would involve iterating through the entire array, but the separate dictionary for single port insertions meant that it would query in O(1) time for a portion of the cases on real world data. If pS and iS were the number of ports (and their ips) in the singles hash table, the total runtime would be O(1) + O(p - pS + i - iS).

I had also considered an approach that involved merging intervals but ran into some trouble thinking about all the edge cases that involved two layers of intervals. I would probably explore that path further if I had more time!

## Testing

I created my own data.csv file for testing and tested in the file for all the direction/protocol pairs, port ranges and one-off errors, ip ranges and one-off errors, queries that involved a port/ip between a range, queries for entries that don't exist, and queries for direction/protocol pairs that don't exist.

## Overall

This was an interesting and fun challenge! I ran into some time trouble near the end that I could've used to optimize further but I'm happy with how it turned out in just over an hour. 

## Teams

I am most interested in the Platform team as I would really love to sharpen my skills on systems at scale. I have prior experience designing and building out APIs, as well as application development. It would be an amazing opportunity to learn about systems at scale and work with tens of thousands of managed servers.

I am also interested in the Data team; I integrated data collection to an enterprise web app during my last internship and it was incredible the insights one can receive from data. I'm especially interested in Illumination and prototyping infrastructure / data visualization with the latest techniques.
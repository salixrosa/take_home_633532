# Take Home

### Broad Notes

I've had to learn Dijkstra's in interview prep previously, but when it comes to actual work, I've used the NetworkX library to implement path-finding logic algorithms. This means that I've also already seen one potential implementation of a path-finding API; previously, I've populated a networkX Graph with nodes and weighted edge data, then used the networkX `shortest_path` function (implementing Dijkstra's) to find the shortest path between the two relevant networkX Nodes.

Here, I've decided to re-implement Dijkstra's in Python, since it seemed safe to assume that simply using NetworkX would not provide enough material for this take home.

I selected Python for entirely circumstantial, personal reasons (my personal machine is not currently set up to develop in Kotlin). I would much refer to have Kotlin's typing though.

### Function
The main function here is `dijkstra_shortest_path` located in `shortest_path.py`. It can be used like so:
```python
facility_1 = Node("A")
facility_2 = Node("B")
route_1 = DirectedEdge(facility_1, facility_2, weight = 10)
route_map = Graph([route_1])
shortest_paths, total_cost = dijkstra_shortest_path(route_map, facility_1, facility_2)
shortest_paths # [[facility_1, facility_2]]
total_cost  # 10
```
shortest_paths will be a list of lists, where each list contains the facilities to be traversed, in order, and the total_cost is the sum of the entire path(s).  

### Testing
I did not clearly distinguish separate test functions or use a testing framework. Tests are contained within the `sample_tests.py` file, and are meant to be checked by running that file.

If you have the docker compose plugin in your machine, the tests can be run using the `docker compose run test` command from this directory. Otherwise, they can be run using python 3 locally. Running the `sample_tests.py` file will give logging on the tests being run and whether they passed or failed. Currently, one test is failing, to illustrate a point; I made no decision on how the graph should handle the same edge being input multiple times with different weights.

If this were an actual library or service, functionality broken out into methods or functions would be unit tested, but it isn't. 

#### SOME EDGE CASES NOT HANDLED / BEHAVIOR TO CONSIDER
* Empty graph; should it be possible to initialize an empty Graph? should the algo handle an empty graph differently from looking for a node that doesn't exist in the graph?
* Duplicate (parallel) edges; if someone tries to create a graph with edge ["A", "B", 5] and edge ["A", "B", 10], we should probably throw immediately. This algorithm just ends up using whichever edge it sees first.
* Nonsensical (loop) edges; should we allow edges that have the same start and end?
* Negative values; we should throw if the weight of an edge is a negative value... a negative weight in the wrong place in a graph WILL cause an infinite loop
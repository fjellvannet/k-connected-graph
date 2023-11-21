# K-connected graph / network

This repo shows the implementation of an algorithm that can generate graphs of `n` nodes where each node is connected to exactly `k` others. If that isn't possible, as few as possible edges are added to such that each node is connected to at least `k` others. Below you see an example for `n=6` and `k=3`.

![n-6-k-3-graph.png](res%2Fn-6-k-3-graph.png)

Nodes are connected randomly. To keep it predictable, the `random.seed` can be set in the beginning to ensure that the same input of `n` and `k` always produces the same output.

The goal is to always connect exactly `k` other nodes to each node. If it doesn't manage to do so, it will try 10 times with different seeds to see if it can work. The image below shows a graph for `n=5` and `k=3`, which at least to my knowledge isn't possible, therefore an additional edge is added (note that 4 edges come from node 0).

![n-5-k-3-graph-additional-edge.png](res%2Fn-5-k-3-graph-additional-edge.png)

The algorithm itself is implemented in `generate_connections(n, k)` and has no external dependencies. `matplotlib` and `networkx` are only used for visualisation / debugging. Thank you to ChatGPT for the code visualising these networks, which really helped to debug this code.

Feel free to comment here on GitHub if you have ideas for further improvement, otherwise feel free to copy / extend / fork as stated in the ISC license.

## Explanation of the algorithm
### Finding connections
The algorithm in `generate_connections(n, k)` first loops through all the nodes. 

1. **Find nodes available for connection**: Every node which currently is connected to less than `k` other nodes is available. This can only be the case for nodes coming after the current one. The available nodes are first randomized, and then sorted by the number of their connections. Thereby, nodes which are connected to no or few other nodes come before nodes that already are connected to more other nodes. As the sorting algorithm is stable, the random order of nodes is kept as long as the number of connections is the same.
2. **There are enough nodes available**: The current node needs to connect to `x` others. If there are `x` or more nodes available for connection, connect to the first `x` nodes from the list of available nodes from step 1. This is what mostly happens.
3. **Fewer nodes available than necessary**: This can happen towards the end or if the graph can't be connected perfectly as shown in the 2nd picture. First, connect to all the remaining available nodes. For the remaining necessary connections, connect to other random nodes which already are fully connected. Sort the randomized list by the number of their connections like in step 1 to add the fewest possible additional connections. 
4. **Add the new connections**: References to the new nodes from step 2 or 3 are added to the connections the node already has. Then, all the new nodes the current node connects to also get a reference to the current node.
5. **Best-effort cleanup of additional edges**: For instance for `k=3`, the two nodes `a` and `f` have gotten additional edges. This should not happen, but it can happen. Check if `a` and `f` are connected directly, and if so remove that connection. To find these additional edges, consider all pairs of nodes having more than `k` edges. Step 5 actually is a remainder from previous iterations where the algorithm wasn't fully optimized yet, so it is possible that this step isn't needed anymore. However, as the loop basically is skipped when all the nodes are exactly `k`-connected, it was kept.

### Trying to find the optimal graph
The function `get_optimal_connections(n, k)` runs `generate_connections(n, k)` up to 10 times to see if another random seed allows to connect each node to exactly `k` others. Yet, it has only been observed that the algorithm either finds an optimal solution in the first run (see first image). Otherwise, it runs 10 times producing the same number of additional edges in each run (second image). 

This indicates that the algorithm probably finds an optimal solution in the first run already given that it is possible to find, and that it finds the solution with the least number of additional edges if there are is no optimal solution.

This was a quick project needed for a Distributed Algorithms class at the university, and I haven't conducted a lot of research around this. For this reason, I just state my observations. If you have additional ideas or more input, feel free to share.

### Deterministic vs random
Both occurrences of `random.sample()` in `generate_connections(n, k)` can be removed  to get a deterministic and ordered output, just keep the `tuple()`-expression without the surrounding `random`. This however eliminates the possibility to try different node orders and see if additional edges can be avoided. However, as the argumentation in [Tryging to find the optimal graph](#trying-to-find-the-optimal-graph) indicates, this probably isn't even necessary.
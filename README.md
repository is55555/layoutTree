# Buchheim-tree

## structure for tree layout generation using Buchheim algorithm 

(beta) - tested under Python 2.7

See tests for usage details and the sample_output folder for the graphical output of the tests.

See the paper by Buchheim et al. for a full explanation of the algorithm and proof of its O(N) performance.

(PDF of the paper provided in the repository)

# Example tree layout

![large tree](https://raw.githubusercontent.com/is55555/layoutTree/master/sample_output/saved_new_sample_tree_composite-five.png)

This tree is generated programmatically in test.py (see "composite-five"). The dotted lines show the "threads" from the 
Buchheim algorithm (see explanation in the paper). These dotted lines are optional in the graph.py drawing library. I
set it to default to true:

```python
    draw(context, algorithm, tree, 
        node_radius=default_node_radius, proportions=default_proportions, 
        p_draw_connections=True, p_draw_threads=True)
```


# Requirements

Packages pycairo and Future.


# Pending

- Width of node mostly ignored
- more documentation

# Ideas for improvement (TODO)

- Migrate away from Cairo / add other output options
- visual interface


# Licence
 
 MIT
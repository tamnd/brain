---
title: "CF 280C - Game on Tree"
description: "We are given a tree with root at vertex 1. A game is played on this rooted tree until every node disappears. At each move, one of the currently remaining vertices is chosen uniformly at random."
date: "2026-06-05T08:57:35+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "probabilities", "trees"]
categories: ["algorithms"]
codeforces_contest: 280
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 172 (Div. 1)"
rating: 2200
weight: 280
solve_time_s: 121
verified: true
draft: false
---

[CF 280C - Game on Tree](https://codeforces.com/problemset/problem/280/C)

**Rating:** 2200  
**Tags:** implementation, math, probabilities, trees  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with root at vertex `1`. A game is played on this rooted tree until every node disappears.

At each move, one of the currently remaining vertices is chosen uniformly at random. When a vertex `v` is chosen, the entire subtree rooted at `v` is deleted immediately, including `v` itself. The game ends when the root is eventually removed, because deleting the root removes the whole remaining tree.

The task is to compute the expected number of moves before the tree becomes empty.

The input describes an undirected tree with up to `10^5` vertices. Since the tree is rooted at vertex `1`, we can interpret every edge in terms of parent-child relationships after a DFS or BFS from the root.

The constraint `n ≤ 100000` immediately rules out any approach that explicitly simulates the random process. Even an `O(n^2)` algorithm would require around `10^10` operations in the worst case, which is far beyond the time limit. We need a solution that is linear or nearly linear.

A subtle aspect of the problem is that the state of the game changes after every deletion. The probability that a vertex is selected depends on which vertices survived previous moves. Trying to write transitions between all possible remaining trees quickly becomes impossible.

Consider a chain:

```
1
|
2
|
3
```

A common mistake is to think that each vertex contributes independently. It does not. If vertex `2` is chosen, vertex `3` disappears without ever being selected. Any approach that assigns a fixed probability to each vertex being chosen exactly once will produce the wrong expectation.

Another easy pitfall is forgetting that the root is always selected eventually. For a single-node tree:

```
1
```

the game always lasts exactly one move, so the answer is `1`. Any formula that gives `0` here is missing the contribution of the root.

A star-shaped tree also exposes incorrect reasoning:

```
1
/|\
2 3 4
```

The leaves can disappear only by being selected themselves, while the root destroys everything at once. The expected answer is not equal to the tree height, the number of leaves, or any other obvious structural quantity.

The key is finding a quantity whose expectation can be computed directly without modeling the entire process.

## Approaches

A brute-force solution would treat every possible remaining tree as a state. From a state containing `k` vertices, each vertex is chosen with probability `1/k`, leading to another state obtained by deleting a subtree.

This state-space view is correct because it exactly matches the game rules. Unfortunately, even small trees generate exponentially many possible remaining configurations. A tree with `10^5` vertices makes this completely infeasible.

The breakthrough comes from changing what we measure.

Instead of asking for the expected number of moves directly, consider whether a particular vertex contributes one move to the game.

Imagine assigning every vertex a random priority. Choosing a uniformly random remaining vertex at each step is equivalent to generating a random permutation of all vertices and revealing them in that order. A vertex actually causes a move if and only if it appears before every ancestor of that vertex in the permutation.

Why? If an ancestor appears first, that ancestor's subtree deletion removes the vertex before it ever gets selected. If the vertex is the earliest among all vertices on the path from the root to itself, then it survives until its turn and contributes one move.

For a vertex at depth `d` (root depth `1`), the path from the root to that vertex contains exactly `d` vertices. Among these `d` vertices, every one is equally likely to be the earliest in a random permutation. Hence

$$P(\text{vertex } v \text{ contributes a move}) = \frac{1}{d}.$$

Let `I(v)` be the indicator that vertex `v` contributes a move. The total number of moves is

$$X = \sum_v I(v).$$

Using linearity of expectation,

$$E[X] = \sum_v E[I(v)] = \sum_v \frac{1}{\text{depth}(v)}.$$

The problem has become extremely simple. We only need the depth of every vertex in the rooted tree.

A single DFS computes all depths, and the answer is the sum of their reciprocals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force state enumeration | Exponential | Exponential | Too slow |
| DFS depth summation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the tree.
2. Root the tree at vertex `1`.
3. Perform a DFS from the root and compute the depth of every vertex, using depth `1` for the root.
4. For each visited vertex, add `1 / depth` to the answer.
5. Continue until all vertices have been visited.
6. Print the accumulated sum with sufficient precision.

The non-obvious part is step 4. A vertex contributes one move exactly when it is the earliest vertex on its root-to-vertex path in the random permutation interpretation. Since every vertex on that path is equally likely to be earliest, the contribution probability is simply `1 / depth`.

### Why it works

For any vertex `v`, define an indicator random variable:

$$I(v)= \begin{cases} 1,&\text{if }v\text{ is ever selected},\\ 0,&\text{otherwise}. \end{cases}$$

Vertex `v` is selected if and only if no ancestor of `v` is selected before it. In a random permutation of all vertices, this happens exactly when `v` is the first vertex on the root-to-`v` path.

If the path contains `depth(v)` vertices, symmetry gives

$$P(I(v)=1)=\frac{1}{depth(v)}.$$

The total number of game moves equals

$$X=\sum_v I(v).$$

Applying linearity of expectation,

$$E[X] = \sum_v E[I(v)] = \sum_v P(I(v)=1) = \sum_v \frac{1}{depth(v)}.$$

The DFS computes every depth exactly once, so the algorithm evaluates precisely this formula. Since the formula equals the expected number of moves, the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    ans = 0.0

    stack = [(1, 0, 1)]  # node, parent, depth

    while stack:
        u, parent, depth = stack.pop()

        ans += 1.0 / depth

        for v in g[u]:
            if v != parent:
                stack.append((v, u, depth + 1))

    print("{:.15f}".format(ans))

if __name__ == "__main__":
    solve()
```

The adjacency list stores the tree in `O(n)` memory.

The DFS is implemented iteratively rather than recursively. A recursive DFS on a path of length `100000` would exceed Python's recursion limit. Using an explicit stack avoids that issue completely.

Each stack entry stores the current vertex, its parent, and its depth. When a vertex is popped, we immediately add `1/depth` to the answer. This directly implements the proven formula

$$\sum_v \frac{1}{depth(v)}.$$

The root starts at depth `1`, not `0`. This is crucial because the probability associated with the root is `1`, and dividing by zero would obviously be invalid.

The answer is accumulated in a floating-point variable. Double precision is more than sufficient for the required `10^{-6}` accuracy.

## Worked Examples

### Example 1

Input:

```
2
1 2
```

The rooted tree is:

```
1
|
2
```

| Vertex | Depth | Contribution |
| --- | --- | --- |
| 1 | 1 | 1.0 |
| 2 | 2 | 0.5 |

Total:

$$1+\frac12=1.5$$

| Step | Node Visited | Depth | Running Answer |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1.0 |
| 2 | 2 | 2 | 1.5 |

Output:

```
1.500000000000000
```

This example shows that the root always contributes exactly one move, while the child survives long enough to be selected only half the time.

### Example 2

Input:

```
3
1 2
1 3
```

The rooted tree is:

```
  1
 / \
2   3
```

| Vertex | Depth | Contribution |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 0.5 |
| 3 | 2 | 0.5 |

Total:

$$1+\frac12+\frac12=2$$

| Step | Node Visited | Depth | Running Answer |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1.0 |
| 2 | 2 | 2 | 1.5 |
| 3 | 2 | 2 | 2.0 |

Output:

```
2.000000000000000
```

This demonstrates the linearity-of-expectation viewpoint. We never need to enumerate the different deletion orders.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each vertex and edge is processed once during DFS |
| Space | O(n) | Adjacency list and DFS stack store at most O(n) data |

A linear traversal is easily fast enough for `n = 100000`. The memory usage is also comfortably within the limit because the graph representation contains only `2(n - 1)` adjacency entries.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    ans = 0.0
    stack = [(1, 0, 1)]

    while stack:
        u, p, d = stack.pop()
        ans += 1.0 / d

        for v in g[u]:
            if v != p:
                stack.append((v, u, d + 1))

    return f"{ans:.15f}"

# provided sample
assert run("2\n1 2\n") == "1.500000000000000"

# single node
assert run("1\n") == "1.000000000000000"

# star with three leaves
assert run("4\n1 2\n1 3\n1 4\n") == "2.500000000000000"

# chain of length 3
assert run("3\n1 2\n2 3\n") == "1.833333333333333"

# chain of length 4
assert run("4\n1 2\n2 3\n3 4\n") == "2.083333333333333"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1.0` | Smallest possible tree |
| Star with 3 leaves | `2.5` | Multiple children at same depth |
| Chain of length 3 | `1.833333333333333` | Increasing depths |
| Chain of length 4 | `2.083333333333333` | Deep tree, depth handling |
| Sample input | `1.5` | Matches official example |

## Edge Cases

### Single vertex tree

Input:

```
1
```

The DFS visits only the root.

| Vertex | Depth | Contribution |
| --- | --- | --- |
| 1 | 1 | 1 |

Answer:

$$1$$

This confirms that the root always contributes one move and that depth must start from `1`.

### Long chain

Input:

```
4
1 2
2 3
3 4
```

Depths are `1, 2, 3, 4`.

The answer becomes

$$1+\frac12+\frac13+\frac14 = 2.083333333333333.$$

A recursive DFS could overflow on a chain of length `100000`, but the iterative stack handles it safely.

### Star centered at the root

Input:

```
4
1 2
1 3
1 4
```

Depths are `1, 2, 2, 2`.

The answer is

$$1+\frac12+\frac12+\frac12 = 2.5.$$

This case verifies that each leaf contributes independently through its probability `1/2`, even though selecting the root instantly removes all leaves.

### Unbalanced tree

Input:

```
5
1 2
2 3
1 4
4 5
```

Depths are:

| Vertex | Depth |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 2 |
| 5 | 3 |

Answer:

$$1+\frac12+\frac13+\frac12+\frac13 = \frac{8}{3} = 2.666666666666667.$$

The algorithm depends only on root-to-vertex depths, regardless of how balanced or unbalanced the tree is. This confirms that the probability argument works for arbitrary tree shapes.

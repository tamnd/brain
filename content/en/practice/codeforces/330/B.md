---
title: "CF 330B - Road Construction"
description: "We have a graph with n cities and no roads initially. Some pairs of cities are forbidden, meaning we are not allowed to build a road directly between them. We must add the smallest possible number of roads so that two conditions hold."
date: "2026-06-06T09:26:14+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs"]
categories: ["algorithms"]
codeforces_contest: 330
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 192 (Div. 2)"
rating: 1300
weight: 330
solve_time_s: 116
verified: false
draft: false
---

[CF 330B - Road Construction](https://codeforces.com/problemset/problem/330/B)

**Rating:** 1300  
**Tags:** constructive algorithms, graphs  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We have a graph with `n` cities and no roads initially. Some pairs of cities are forbidden, meaning we are not allowed to build a road directly between them.

We must add the smallest possible number of roads so that two conditions hold.

First, every city must be reachable from every other city.

Second, the distance between any two cities must be at most 2, meaning we can travel from one city to another using either one road or two roads.

The input describes the forbidden pairs. Every pair not listed is available for construction. The problem guarantees that at least one valid solution exists.

The key observation about the requirements is that they are extremely strong. A connected graph on `n` vertices needs at least `n - 1` edges, because every connected graph contains a spanning tree. Since we are asked for the minimum number of roads, any valid answer must use exactly `n - 1` roads.

A graph with `n - 1` edges is a tree. Among trees, the only ones whose diameter is at most 2 are stars. Any other tree contains a path of length at least 3.

This immediately suggests that the answer must be a star centered at some city.

A subtle point is choosing the center. If we pick a city that has a forbidden pair with another city, we cannot connect the star edge to that city. The problem guarantee implies that there exists at least one city that is not involved in any forbidden pair. Finding that city is the whole problem.

Consider the input

```
4 1
1 3
```

City 2 never appears in a forbidden pair. A star centered at city 2 uses edges `(2,1)`, `(2,3)`, `(2,4)`. Every pair of cities is either directly connected to 2 or can meet through 2 in exactly two steps.

A careless approach might try to connect cities greedily while avoiding forbidden edges. For example,

```
4 2
1 2
3 4
```

Building arbitrary legal roads may produce a connected graph, but it could use more than `n - 1` edges and would no longer be minimal.

Another easy mistake is to search for a city that is not forbidden with every other city individually. The problem is simpler. We only need a city that never appears in any forbidden pair at all. Such a city can connect to everyone because every forbidden edge would have to involve it, which never happens.

For example,

```
5 3
1 2
1 3
1 4
```

City 5 appears nowhere in the forbidden list. Every edge `(5,x)` is legal, so a star centered at 5 is valid.

## Approaches

A brute-force viewpoint is to try every possible graph satisfying the forbidden-edge constraints and check whether all pairwise distances are at most 2. Even if we restrict ourselves to connected graphs, the number of possible edge subsets is exponential in the number of available edges. This is completely infeasible.

A more reasonable brute-force idea is to test every city as a possible center. For each city, check whether it can connect to every other city, then build the corresponding star. This already hints at the real structure of the solution.

The crucial observation comes from combining two facts.

Any connected graph on `n` vertices needs at least `n - 1` edges.

A graph with exactly `n - 1` edges is a tree.

Among all trees, the only way to keep every pair of vertices within distance 2 is to use a star.

So instead of constructing an arbitrary graph, we only need to construct a star. The remaining question is whether a valid center exists.

Let us mark every city that appears in at least one forbidden pair. Since each forbidden edge marks both endpoints, any city that remains unmarked never participates in a forbidden pair. Every edge from that city to another city is legal.

The problem guarantee ensures at least one such city exists. Once found, we connect it to all other cities. The result is a star with exactly `n - 1` edges, which is the minimum possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Graph Construction | Exponential | Exponential | Too slow |
| Optimal Star Construction | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a boolean array indicating whether each city appears in any forbidden pair.
2. Read every forbidden pair `(u, v)`.
3. Mark both `u` and `v` as appearing in a forbidden pair.
4. After processing all pairs, find a city `center` that was never marked.

Such a city does not belong to any forbidden pair, so every road from `center` to another city is allowed.
5. Output `n - 1`, because a star on `n` vertices contains exactly `n - 1` roads.
6. For every city different from `center`, output the road `(center, city)`.

### Why it works

Let `center` be a city that never appears in any forbidden pair.

Since `center` is absent from all forbidden pairs, every edge `(center, v)` is legal. Thus all roads of the constructed star can be built.

The resulting graph is connected because every city is directly connected to `center`.

Any two non-center cities can reach each other through `center` in exactly two roads. Any city and the center are connected by one road. Hence every pair of cities is at distance at most 2.

The graph contains exactly `n - 1` edges. No connected graph can use fewer edges, so the construction is minimal.

Since the problem guarantees a solution exists, there is always at least one city that never appears in a forbidden pair, and the algorithm always finds one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    used = [False] * (n + 1)

    for _ in range(m):
        u, v = map(int, input().split())
        used[u] = True
        used[v] = True

    center = 1
    for i in range(1, n + 1):
        if not used[i]:
            center = i
            break

    print(n - 1)
    for i in range(1, n + 1):
        if i != center:
            print(center, i)

solve()
```

The first part records which cities participate in at least one forbidden pair. We do not need to store the forbidden edges themselves. The only information that matters is whether a city appears in any of them.

The search for `center` scans the cities once. Because the problem guarantees a valid solution, at least one unmarked city exists.

After finding the center, the construction is straightforward. We connect the center to every other city, producing exactly `n - 1` roads.

A common implementation mistake is to store forbidden edges and then repeatedly check whether `(center, i)` is forbidden. That work is unnecessary. By construction, an unmarked center never appears in any forbidden pair, so every such edge is automatically legal.

## Worked Examples

### Example 1

Input:

```
4 1
1 3
```

Processing the forbidden pairs:

| Step | Pair | Marked Cities |
| --- | --- | --- |
| Initial | - | {} |
| 1 | (1,3) | {1,3} |

Finding the center:

| City | Marked? |
| --- | --- |
| 1 | Yes |
| 2 | No |

So `center = 2`.

Output edges:

| Edge |
| --- |
| (2,1) |
| (2,3) |
| (2,4) |

The graph is a star. Every pair of leaves communicates through city 2 in two steps.

### Example 2

Input:

```
5 3
1 2
1 3
1 4
```

Processing:

| Step | Pair | Marked Cities |
| --- | --- | --- |
| 1 | (1,2) | {1,2} |
| 2 | (1,3) | {1,2,3} |
| 3 | (1,4) | {1,2,3,4} |

Finding the center:

| City | Marked? |
| --- | --- |
| 1 | Yes |
| 2 | Yes |
| 3 | Yes |
| 4 | Yes |
| 5 | No |

So `center = 5`.

Constructed edges:

| Edge |
| --- |
| (5,1) |
| (5,2) |
| (5,3) |
| (5,4) |

This example demonstrates that the center does not have to be related to the forbidden structure at all. It only needs to avoid appearing in it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One pass over the forbidden pairs and one pass over the cities |
| Space | O(n) | The marked array stores one boolean per city |

The algorithm performs only linear work in the input size. Even for the largest allowed values of `n` and `m`, this easily fits within the time limit. Memory usage is also minimal, requiring only a single array of size `n`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())

    used = [False] * (n + 1)

    for _ in range(m):
        u, v = map(int, input().split())
        used[u] = True
        used[v] = True

    center = next(i for i in range(1, n + 1) if not used[i])

    out = [str(n - 1)]
    for i in range(1, n + 1):
        if i != center:
            out.append(f"{center} {i}")

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""4 1
1 3
"""
) == (
"""3
2 1
2 3
2 4
"""
)

# minimum size
assert run(
"""2 0
"""
) == (
"""1
1 2
"""
)

# one city involved in all forbidden pairs
assert run(
"""5 3
1 2
1 3
1 4
"""
) == (
"""4
5 1
5 2
5 3
5 4
"""
)

# no forbidden pairs
assert run(
"""4 0
"""
) == (
"""3
1 2
1 3
1 4
"""
)

# smallest nontrivial center at the end
assert run(
"""4 2
1 2
2 3
"""
) == (
"""3
4 1
4 2
4 3
"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0` | Single edge | Minimum graph size |
| Forbidden pairs all touch city 1 | Star centered elsewhere | Correct center selection |
| No forbidden pairs | Star centered at first city | Empty constraint set |
| Center appears at highest index | Uses last possible center | Scan correctness |
| Sample case | Valid minimal construction | Basic functionality |

## Edge Cases

Consider:

```
4 0
```

No city appears in a forbidden pair. The algorithm chooses city 1 as the center and outputs:

```
3
1 2
1 3
1 4
```

Every pair of non-center cities has distance 2 through city 1.

Now consider:

```
5 4
1 2
1 3
1 4
1 5
```

Every city except 1 appears in a forbidden pair, and city 1 appears in all of them. This input would not satisfy the problem guarantee because every city is marked. The guarantee excludes such cases, which is why the algorithm can safely assume an unmarked city exists.

Finally, consider:

```
6 3
1 2
2 3
3 4
```

Cities 5 and 6 never appear in any forbidden pair. The algorithm may choose city 5. It outputs:

```
5 1
5 2
5 3
5 4
5 6
```

All roads are legal because city 5 never participates in a forbidden pair. Every city is at distance at most 2 from every other city through the center. This confirms the key invariant used by the solution.

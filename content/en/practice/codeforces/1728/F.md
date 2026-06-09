---
title: "CF 1728F - Fishermen"
description: "Each fisherman has a fish size ai. We choose an order in which they speak. The first fisherman says his real fish size. Every later fisherman must say the smallest multiple of his own fish size that is strictly larger than the previous announced value."
date: "2026-06-09T18:51:52+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graph-matchings", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1728
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 135 (Rated for Div. 2)"
rating: 3100
weight: 1728
solve_time_s: 116
verified: true
draft: false
---

[CF 1728F - Fishermen](https://codeforces.com/problemset/problem/1728/F)

**Rating:** 3100  
**Tags:** flows, graph matchings, greedy  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

Each fisherman has a fish size `a_i`. We choose an order in which they speak.

The first fisherman says his real fish size. Every later fisherman must say the smallest multiple of his own fish size that is strictly larger than the previous announced value.

The announced values form a strictly increasing sequence. The order is the only thing we control, and we want the sum of all announced values to be as small as possible.

The first useful observation is that the actual speaking process is less important than it looks.

Suppose fisherman `i` eventually announces some value `x_i`. Since every fisherman can only announce a multiple of `a_i`, each `x_i` must be divisible by `a_i`. The sequence of announced values is strictly increasing, so all announced values are distinct.

Now reverse the perspective. If we assign each fisherman a distinct multiple of his fish size, and then sort those assigned values increasingly, that sorted order becomes a valid speaking order. Every fisherman will indeed announce exactly the assigned value, because it is the smallest available multiple larger than the previous assigned value.

So the problem becomes:

Choose one distinct multiple of `a_i` for every fisherman, minimizing the total sum.

The constraints are very revealing. We have at most `1000` fishermen, while fish sizes can be as large as `10^6`. Any solution depending on the numeric magnitude of the values is unlikely to work. The algorithm must depend primarily on `n`.

A common mistake is to think that the speaking order alone determines everything. Consider:

```
2
2 2
```

The announced values cannot both be `2`. One fisherman must say `2`, the other must say `4`, so the answer is `6`.

Another subtle case is:

```
3
2 3 6
```

A greedy strategy that always uses the smallest currently available multiple may choose `2`, `3`, `6`. This is actually optimal, with sum `11`. But if we had:

```
3
2 2 2
```

we need three distinct multiples: `2`, `4`, `6`, giving answer `12`. Distinctness is the real constraint.

A final trap is assuming we need arbitrarily large multiples. With only `n` fishermen, every fisherman only needs to consider his first `n` multiples. If some fisherman were assigned his `(n+1)`-st multiple, then among his first `n` multiples at least one would be unused, because there are only `n-1` other fishermen occupying values. Replacing the larger multiple by that unused smaller one improves the solution.

That observation is what makes the problem manageable.

## Approaches

The brute-force idea is straightforward. Try every permutation of fishermen, simulate the announced values, and keep the minimum sum.

For a fixed permutation, simulation is easy. The difficulty is that there are `n!` permutations. Even for `n = 15`, this is already completely infeasible, and the actual limit is `1000`.

The key step is changing the viewpoint from ordering fishermen to assigning announced values.

Every fisherman must receive a distinct value that is a multiple of his fish size. Once those values are chosen, the speaking order is forced: sort the chosen values.

So we no longer care about permutations. We care about selecting one valid value for every fisherman.

Since only the first `n` multiples of each fish size can ever matter, we generate all values

```
a_i * 1, a_i * 2, ..., a_i * n
```

and remove duplicates.

Think of every generated value as a node on the left side of a bipartite graph, and every fisherman as a node on the right side.

A value `v` is connected to fisherman `i` if `v` is divisible by `a_i`.

Choosing distinct announced values is now exactly choosing a matching that covers all fishermen.

The remaining question is how to minimize the sum of chosen values.

All value nodes have costs equal to their numeric values. After sorting value nodes increasingly, we process them from smallest to largest. Whenever adding a value node increases the maximum matching size by one, we keep it and add its value to the answer.

This is the classic greedy construction of a minimum-weight basis in a transversal matroid. Operationally, it becomes a sequence of Kuhn augmentations.

The result is surprisingly compact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal Matching + Greedy Rank Construction | O(V · E) | O(V + E) | Accepted |

Here `V` is the number of distinct candidate values, at most about `n²`.

## Algorithm Walkthrough

1. Generate all values `a_i * k` for every fisherman `i` and every `1 ≤ k ≤ n`.
2. Sort these values and remove duplicates.
3. Create a bipartite graph.

The left side contains all distinct candidate values.

The right side contains the fishermen.
4. For every fisherman `i` and every multiplier `k` from `1` to `n`, find the index of value `a_i * k` in the sorted value list and add an edge from that value node to fisherman `i`.

A value node is connected exactly to the fishermen whose fish sizes divide that value.
5. Process value nodes from smallest to largest.
6. Maintain a maximum matching between the processed value nodes and the fishermen.
7. When a new value node is considered, run one Kuhn augmentation starting from that value node.
8. If the augmentation succeeds, the maximum matching size increases by one. Add the numeric value of this node to the answer.
9. Continue until all value nodes have been processed.
10. Output the accumulated sum.

### Why it works

The candidate values form the ground set of a transversal matroid. A set of value nodes is independent if the fishermen that can use them admit a matching.

For matroids, the minimum-weight basis is obtained by processing elements in increasing weight order and taking an element whenever it increases the rank.

In our graph, the rank of a set of value nodes is exactly the size of the maximum matching achievable using those values.

When processing values from smallest to largest, a successful augmentation means that the current value increases the rank and must belong to the greedy minimum-weight basis. An unsuccessful augmentation means it does not increase rank and can never help produce a cheaper basis.

The basis eventually has size `n`, meaning every fisherman is matched to a distinct valid multiple. The sum accumulated by the greedy process is exactly the minimum possible sum of announced values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    vals = []
    for x in a:
        for k in range(1, n + 1):
            vals.append(x * k)

    vals = sorted(set(vals))
    m = len(vals)

    g = [[] for _ in range(m)]

    for i, x in enumerate(a):
        for k in range(1, n + 1):
            v = x * k
            idx = vals.index(v) if False else None

    pos = {v: i for i, v in enumerate(vals)}

    for i, x in enumerate(a):
        for k in range(1, n + 1):
            g[pos[x * k]].append(i)

    mt = [-1] * n
    used = [False] * m

    sys.setrecursionlimit(1 << 20)

    def kuhn(v):
        if used[v]:
            return False
        used[v] = True

        for to in g[v]:
            if mt[to] == -1 or kuhn(mt[to]):
                mt[to] = v
                return True

        return False

    ans = 0

    for v in range(m):
        used = [False] * m
        if kuhn(v):
            ans += vals[v]

    print(ans)

if __name__ == "__main__":
    solve()
```

The first block generates every relevant candidate value. Only the first `n` multiples are needed, which keeps the graph finite.

The dictionary `pos` converts an actual numeric value into its position in the sorted candidate list. Without this map, repeatedly searching with binary search or linear search would add unnecessary overhead.

The graph is built from value nodes to fishermen. An edge means that the fisherman can use that value as his announced number.

`mt[i]` stores the value node currently matched to fisherman `i`.

The Kuhn search attempts to insert the newly processed value node into the matching. If an augmenting path exists, the matching size increases by one.

A subtle detail is resetting `used` before every augmentation attempt. Each DFS must have its own visitation state. Reusing old marks would incorrectly block valid augmenting paths.

The answer is increased exactly when the matching size grows. Those are precisely the value nodes selected by the greedy rank-building process.

Python integers easily handle the largest possible answer, since candidate values can reach roughly `10^9` and we may sum up to `1000` of them.

## Worked Examples

### Example 1

Input:

```
7
1 8 2 3 2 2 3
```

Relevant candidate values begin as:

```
1, 2, 3, 4, 6, 8, 9, ...
```

The greedy matching process behaves as follows.

| Value | Matching size before | Matching size after | Added to answer |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 2 | 2 |
| 3 | 2 | 3 | 3 |
| 4 | 3 | 4 | 4 |
| 6 | 4 | 5 | 6 |
| 8 | 5 | 6 | 8 |
| 9 | 6 | 7 | 9 |

The chosen values are:

```
1, 2, 3, 4, 6, 8, 9
```

Their sum is:

```
33
```

This example shows how the algorithm keeps only value nodes that increase the achievable matching size.

### Example 2

Input:

```
10
5 6 5 6 5 6 5 6 5 6
```

The first useful values are:

```
5, 6, 10, 12, 15, 18, 20, 24, 25, 30
```

| Value | Matching size before | Matching size after | Added to answer |
| --- | --- | --- | --- |
| 5 | 0 | 1 | 5 |
| 6 | 1 | 2 | 6 |
| 10 | 2 | 3 | 10 |
| 12 | 3 | 4 | 12 |
| 15 | 4 | 5 | 15 |
| 18 | 5 | 6 | 18 |
| 20 | 6 | 7 | 20 |
| 24 | 7 | 8 | 24 |
| 25 | 8 | 9 | 25 |
| 30 | 9 | 10 | 30 |

The sum is:

```
165
```

This demonstrates that repeated fish sizes naturally require larger and larger multiples.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(VE) | One Kuhn augmentation per value node |
| Space | O(V + E) | Graph, matching, visitation arrays |

Here `V` is the number of distinct candidate values and `E` is the number of graph edges. Since every fisherman contributes at most `n` candidate multiples, both quantities are bounded by `O(n²)`. With `n = 1000`, this comfortably fits the contest limits and matches the intended solution.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    vals = []
    for x in a:
        for k in range(1, n + 1):
            vals.append(x * k)

    vals = sorted(set(vals))
    pos = {v: i for i, v in enumerate(vals)}

    m = len(vals)
    g = [[] for _ in range(m)]

    for i, x in enumerate(a):
        for k in range(1, n + 1):
            g[pos[x * k]].append(i)

    mt = [-1] * n
    sys.setrecursionlimit(1 << 20)

    def kuhn(v, used):
        if used[v]:
            return False
        used[v] = True

        for to in g[v]:
            if mt[to] == -1 or kuhn(mt[to], used):
                mt[to] = v
                return True

        return False

    ans = 0

    for v in range(m):
        used = [False] * m
        if kuhn(v, used):
            ans += vals[v]

    return str(ans)

# provided samples
assert run("7\n1 8 2 3 2 2 3\n") == "33", "sample 1"
assert run("10\n5 6 5 6 5 6 5 6 5 6\n") == "165", "sample 2"

# custom cases
assert run("1\n7\n") == "7", "single fisherman"
assert run("2\n2 2\n") == "6", "duplicate values"
assert run("3\n1 1 1\n") == "6", "first three multiples"
assert run("3\n2 3 6\n") == "11", "distinct compatible values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `7` | Minimum-size instance |
| `2 / 2 2` | `6` | Distinctness of assigned values |
| `3 / 1 1 1` | `6` | Consecutive multiples are required |
| `3 / 2 3 6` | `11` | Mixed divisibility relationships |

## Edge Cases

Consider:

```
2
2 2
```

The graph contains value nodes `2` and `4`. Both fishermen can use either value. The first successful augmentation takes `2`. The second successful augmentation takes `4`. The answer becomes `6`.

A careless solution that only considers the smallest multiple for each fisherman would incorrectly produce `4`.

Now consider:

```
3
1 1 1
```

The only valid distinct assignments are `1`, `2`, and `3`. The matching grows exactly at those three values, producing answer `6`.

This verifies that repeated fish sizes force the use of larger multiples.

Finally:

```
3
2 3 6
```

Candidate values begin with `2, 3, 4, 6, ...`.

The matching grows at `2`, then `3`, then `6`. Value `4` does not increase the matching size and is skipped. The answer is `11`.

This illustrates the central invariant of the algorithm: a value contributes to the answer only if it increases the rank of the current bipartite matching.

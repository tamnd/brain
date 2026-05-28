---
title: "CF 28B - pSort"
description: "We start with an array where position i initially contains value i. Each position also has a fixed jump distance d[i]. A"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 28
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 28 (Codeforces format)"
rating: 1600
weight: 28
solve_time_s: 93
verified: true
draft: false
---

[CF 28B - pSort](https://codeforces.com/problemset/problem/28/B)

**Rating:** 1600  
**Tags:** dfs and similar, dsu, graphs  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array where position `i` initially contains value `i`. Each position also has a fixed jump distance `d[i]`. A swap is allowed between positions `i` and `j` only if `|i - j| = d[i]`.

The target array is a permutation. We must decide whether the allowed swaps are enough to transform the initial ordered array into that permutation.

The first detail that matters is that the swap rule is asymmetric in the statement. Position `i` may swap with any `j` satisfying the distance condition. But once such a pair exists, the swap itself is completely normal, both values exchange places. If position `i` can reach `j`, then positions `i` and `j` belong to the same movement structure.

The constraints are very small, `n ≤ 100`. Even cubic solutions fit comfortably inside the time limit. That means we do not need advanced optimizations, but we still need the correct graph interpretation. A brute-force state search over all permutations is impossible because there are `n!` states. Even for `n = 10`, this already becomes too large.

The key observation is that swaps only move values inside connected regions of positions. If position `1` can eventually reach positions `3` and `5` through a chain of swaps, then values can be rearranged arbitrarily among those positions. If two positions belong to different connected components, no sequence of swaps can move a value across that boundary.

A common mistake is to check only direct swaps instead of chains of swaps.

Consider:

```
3
2 3 1
1 1 1
```

The correct answer is `YES`.

Position `1` can swap with `2`, and `2` can swap with `3`. Even though `1` cannot directly swap with `3`, the value `1` can still travel there through intermediate swaps.

Another easy mistake is forgetting that the graph is undirected in practice.

Example:

```
2
2 1
1 2
```

The answer is `NO`.

Position `1` can swap with `2` because `|1 - 2| = 1`, but position `2` cannot swap with `1` because `|2 - 1| ≠ 2`. Since the statement says the `i`-th cell may exchange with `j`, only edges generated from valid `i` matter. Here only one direction exists, but the swap itself still connects the positions. We treat this as an undirected edge because after one legal swap, the values at both positions exchange.

Another subtle case is isolated nodes.

```
4
1 3 2 4
4 1 1 4
```

The answer is `YES`.

Positions `2` and `3` can swap, while positions `1` and `4` are isolated. The target permutation only swaps values inside the connected pair `{2,3}`, so it is reachable.

## Approaches

A brute-force approach would simulate all reachable permutations using BFS or DFS over states. Each state is a permutation, and each legal swap generates another state. This is correct because eventually every reachable configuration would be explored.

The problem is the state count. There are `n!` permutations. Even at `n = 10`, that is already more than 3 million states, and each state can generate many swaps. The actual limit is `100`, so exhaustive search is hopeless.

The structure of the swaps gives a much simpler interpretation.

Think of positions as graph vertices. For every position `i`, we connect it with every valid position `j` satisfying:

```
|i - j| = d[i]
```

If two positions lie in the same connected component, then values can move between them through sequences of swaps. Inside a connected component, arbitrary rearrangement becomes possible because swaps along paths allow us to permute the contained values freely.

That changes the problem completely. Instead of tracking permutations, we only need to verify that every value ends up inside the same connected component as its original position.

Value `x` starts at position `x`. In the target permutation, it appears at some position `pos`. The arrangement is reachable if and only if `x` and `pos` belong to the same connected component.

We can build the graph and compute connected components using DFS or DSU.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n²) | O(n!) | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the permutation `p` and the favorite distances `d`.
2. Build a graph on positions `1 ... n`.

For every position `i`, check positions:

```
i - d[i]
i + d[i]
```

If they are inside bounds, connect them with `i`.

These edges represent legal swaps.
3. Compute connected components using DFS or DSU.

Positions inside the same component can exchange values through sequences of swaps.
4. For every position `i`, look at value `p[i]`.

Value `p[i]` originally started at position `p[i]`. To place it at position `i`, both positions must belong to the same connected component.
5. If any position fails this check, print `NO`.
6. Otherwise print `YES`.

### Why it works

A legal swap never moves a value outside its connected component because every swap edge stays inside that component. So if value `x` must end at position `i`, then `x` and `i` must belong to the same component.

The reverse direction also holds. Inside a connected component, repeated swaps along graph edges allow values to move anywhere in that component. Since connected components are independent, we can rearrange each component separately into the desired order.

That makes the connected-component condition both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a != b:
            self.parent[b] = a

def solve():
    n = int(input())

    p = list(map(int, input().split()))
    d = list(map(int, input().split()))

    dsu = DSU(n)

    for i in range(n):
        left = i - d[i]
        right = i + d[i]

        if left >= 0:
            dsu.union(i, left)

        if right < n:
            dsu.union(i, right)

    for i in range(n):
        target_value = p[i] - 1

        if dsu.find(i) != dsu.find(target_value):
            print("NO")
            return

    print("YES")

solve()
```

The DSU stores connected components of positions. Every valid swap creates an edge between two indices, so union operations build the movement graph incrementally.

The implementation uses zero-based indexing internally. That is why the value at position `i` becomes `p[i] - 1` before comparing components. Forgetting this conversion is one of the most common off-by-one bugs in this problem.

For each index, we try both possible destinations, `i - d[i]` and `i + d[i]`. Bounds checking matters because some jumps leave the array.

The final verification step encodes the core invariant directly. Value `p[i]` started at position `p[i] - 1`. If its original position and current destination belong to different components, no sequence of legal swaps can place it there.

## Worked Examples

### Example 1

Input:

```
5
5 4 3 2 1
1 1 1 1 1
```

Graph construction:

| Position | d[i] | Reachable positions |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 1 | 1, 3 |
| 3 | 1 | 2, 4 |
| 4 | 1 | 3, 5 |
| 5 | 1 | 4 |

All positions become connected.

Component table:

| Position | Component |
| --- | --- |
| 1 | A |
| 2 | A |
| 3 | A |
| 4 | A |
| 5 | A |

Verification:

| Target position | Needed value | Original position of value | Same component? |
| --- | --- | --- | --- |
| 1 | 5 | 5 | Yes |
| 2 | 4 | 4 | Yes |
| 3 | 3 | 3 | Yes |
| 4 | 2 | 2 | Yes |
| 5 | 1 | 1 | Yes |

Output:

```
YES
```

This trace shows that once the graph is fully connected, any permutation becomes reachable.

### Example 2

Input:

```
4
2 1 4 3
2 2 1 1
```

Graph construction:

| Position | d[i] | Reachable positions |
| --- | --- | --- |
| 1 | 2 | 3 |
| 2 | 2 | 4 |
| 3 | 1 | 2, 4 |
| 4 | 1 | 3 |

Connected components:

| Position | Component |
| --- | --- |
| 1 | A |
| 2 | B |
| 3 | B |
| 4 | B |

Verification:

| Target position | Needed value | Original position of value | Same component? |
| --- | --- | --- | --- |
| 1 | 2 | 2 | No |

Output:

```
NO
```

Value `2` starts in component `B`, but position `1` belongs to component `A`. No legal sequence can cross that boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | DSU operations are nearly constant, and we process at most two edges per node |
| Space | O(n) | DSU parent array stores one entry per position |

With `n ≤ 100`, this solution is far below the limits. Even a dense graph traversal would pass comfortably.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))

        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)

            if a != b:
                self.parent[b] = a

    n = int(input())

    p = list(map(int, input().split()))
    d = list(map(int, input().split()))

    dsu = DSU(n)

    for i in range(n):
        left = i - d[i]
        right = i + d[i]

        if left >= 0:
            dsu.union(i, left)

        if right < n:
            dsu.union(i, right)

    for i in range(n):
        if dsu.find(i) != dsu.find(p[i] - 1):
            return "NO"

    return "YES"

# provided sample
assert run(
"""5
5 4 3 2 1
1 1 1 1 1
"""
) == "YES", "sample 1"

# minimum size
assert run(
"""1
1
1
"""
) == "YES", "single element"

# isolated positions
assert run(
"""4
2 1 3 4
4 4 4 4
"""
) == "NO", "no swaps possible"

# connected through chains
assert run(
"""3
2 3 1
1 1 1
"""
) == "YES", "indirect reachability"

# partial components
assert run(
"""4
1 3 2 4
4 1 1 4
"""
) == "YES", "swap only inside one component"

# off-by-one boundary test
assert run(
"""2
2 1
2 2
"""
) == "NO", "out-of-range jumps create no edges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | YES | Trivial component handling |
| No valid swaps anywhere | NO | Isolated nodes remain fixed |
| Chain-connected graph | YES | Indirect movement through paths |
| One small connected component | YES | Independent component rearrangement |
| Out-of-range jumps | NO | Boundary checks and indexing correctness |

## Edge Cases

Consider the indirect connectivity case:

```
3
2 3 1
1 1 1
```

The graph edges are:

```
1 <-> 2
2 <-> 3
```

All positions belong to one connected component. Even though position `1` cannot directly swap with `3`, value `1` can move using:

```
[1 2 3]
-> swap 1 and 2
[2 1 3]
-> swap 2 and 3
[2 3 1]
```

The DSU correctly merges all three positions, so the algorithm outputs `YES`.

Now consider isolated nodes:

```
4
2 1 3 4
4 4 4 4
```

Every jump goes outside the array, so no edges are created. Each position forms its own component.

The target permutation tries to place value `2` at position `1`. Their components differ, so the algorithm immediately returns `NO`.

Finally, consider a partially connected graph:

```
4
1 3 2 4
4 1 1 4
```

Only positions `2` and `3` are connected. The target permutation swaps exactly those two values.

Component structure:

```
{1}, {2,3}, {4}
```

Each value remains inside its original component, so the algorithm correctly outputs `YES`.

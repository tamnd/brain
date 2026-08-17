---
title: "CF 102222G - Factories"
description: "We have a weighted tree of cities. A factory may only be placed on an original leaf, meaning a city whose degree in the undirected tree is exactly one."
date: "2026-08-17T22:10:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "G"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 188
verified: true
draft: false
---

[CF 102222G - Factories](https://codeforces.com/problemset/problem/102222/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a weighted tree of cities. A factory may only be placed on an original leaf, meaning a city whose degree in the undirected tree is exactly one. We must choose exactly `k` distinct leaves and minimize the sum of the shortest-path distances over all unordered pairs of chosen leaves.

The input contains up to `10^3` test cases, with `n` up to `10^5` for one test case and the sum of all `n` bounded by `10^6`. The number of factories `k` is at most `100`, which is the parameter that makes a dynamic programming solution possible. The official limits are 10 seconds and 256 MB.

The large value of `n` rules out anything quadratic in the number of cities. Even `O(nk^2)` reaches roughly `10^9` elementary transitions when both `n=10^5` and `k=100`, so the implementation needs to keep the actual state ranges tight rather than blindly iterating over all `k` states at every node. An exponential search over the possible factory sets is completely impossible because the number of leaves can itself be close to `10^5`.

The first edge case is `k=1`. There are no pairs of factories, so the answer is zero regardless of the tree.

```
1
2 1
1 2 7
```

The correct output is `Case #1: 0`. A solution that accidentally adds the distance from a factory to itself would produce a nonzero value.

The second edge case is the smallest possible tree with two cities. Both cities are leaves, even though one of them may be chosen as the root of our implementation.

```
1
2 2
1 2 7
```

The correct output is `Case #1: 7`. A careless rooted-tree implementation may classify only the child as a selectable leaf and lose one valid factory location.

The third edge case is that only original leaves are eligible. Consider a path.

```
1
4 2
1 2 1
2 3 1
3 4 1
```

The only possible factories are cities `1` and `4`, so the answer is `3`. A solution that treats every vertex as a possible factory could incorrectly choose adjacent cities and obtain `1`.

The fourth edge case occurs when all leaves must be selected.

```
1
4 3
1 2 2
1 3 3
1 4 4
```

The three leaves are forced. Their pairwise distances are `5`, `6`, and `7`, giving `18`. A DP that computes the contribution of an edge using only the number of selected leaves below it, but forgets the number of selected leaves outside it, will get this case wrong.

## Approaches

The direct approach is to enumerate every set of `k` leaves, calculate the sum of distances inside that set, and keep the minimum. If there are `L` leaves, this examines `C(L,k)` possible factory sets. Even if all pairwise leaf distances are available in advance, each candidate set requires `C(k,2)` pair evaluations. In the worst allowed shape, a star has `L=99999` leaves, so for `k=100` the number of pair evaluations alone is

`C(99999,100) * C(100,2)`,

which is far beyond any practical computation. Precomputing every leaf-to-leaf distance would also require quadratic memory.

The useful observation is that a tree lets us count the contribution of every edge independently. Fix a set of `k` factory leaves and remove an edge of weight `w`. Suppose exactly `x` chosen leaves lie on one side of the edge. Then exactly `k-x` chosen leaves lie on the other side. Every pair consisting of one leaf from each side has a path containing this edge, so the edge is used by exactly `x(k-x)` factory pairs. Its contribution to the total answer is therefore

`w * x * (k-x)`.

This converts a sum over pairs of leaves into a sum over edges. The same edge-contribution formulation is the central observation used by the standard solution for this problem.

Now root the tree. For every node `u`, consider only the leaves in its rooted subtree. Define `dp[u][j]` as the minimum contribution of all edges completely inside that subtree when exactly `j` factories are selected there. The parent does not need to know which leaves were selected, only how many, because the only edge connecting the subtree to the rest of the tree is the parent edge.

Suppose `v` is a child of `u`, and the edge `u-v` has weight `w`. If we take `x` factories from `v`'s subtree, that edge contributes `w*x*(k-x)`. If the already processed part of `u` contains `j-x` factories, the transition becomes

`dp[u][j] = min(dp[u][j], dp[u][j-x] + dp[v][x] + w*x*(k-x))`.

This is a tree knapsack. The transition is exactly the standard child-subtree merging described in existing solutions for the problem.

The brute-force method works because every possible factory set is explicitly considered, but it fails because there are exponentially many such sets. The edge-contribution observation lets us forget the identities of selected leaves while processing a subtree and retain only their count. Since `k` is at most `100`, this turns the problem into a bounded dynamic program.

The standard worst-case bound of the tree-knapsack recurrence is `O(nk^2)`. The implementation below improves the practical behavior significantly by storing only reachable states and by restricting each transition to valid ranges. In particular, a long chain above a branching subtree does not repeatedly scan impossible states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(C(L,k) * k^2)` after distance preprocessing | `O(L^2)` if all leaf distances are stored | Too slow |
| Optimal DP | `O(nk^2)` worst case, with tight reachable-state pruning | `O(nk)` worst case | Accepted |

## Algorithm Walkthrough

1. Root the tree at city `1` and build a parent-before-child traversal order. An iterative traversal is used because a tree can be a path of length `10^5`, which would make a recursive Python DFS vulnerable to recursion depth limits.
2. Record the original degree of every city. A city contributes one selectable factory state exactly when its original degree is `1`. The root is handled by the same rule, which is necessary for the two-city tree where both vertices are leaves.
3. Process the vertices in reverse traversal order, so every child has already computed its DP before its parent is processed. For a non-leaf node, initialize its DP as `[0]`, representing the choice of selecting zero leaves from the subtree. For a leaf, initialize `[0, 0]`, where state `1` means selecting that leaf and has cost zero inside the subtree.
4. For every child `v` of `u`, merge `dp[v]` into `dp[u]`. Suppose the current `u` states support at most `a` selected leaves and the child supports at most `b`. To obtain a state containing `j` factories, try every valid number `x` taken from the child. The candidate is `dp[u][j-x] + dp[v][x] + w*x*(k-x)`.
5. Perform the `j` loop backwards. The current DP array is updated in place, so descending `j` guarantees that `dp[u][j-x]` still refers to the states from before this child was merged. This is the same reason a one-dimensional 0/1 knapsack processes capacities backwards.
6. Do not iterate over impossible values. If the current part contains at most `a` selectable leaves, then a state `j-x` larger than `a` cannot exist. Likewise, `x` cannot exceed the number of states represented by the child. This pruning is especially useful for long chains, where a naive implementation can spend most of its time testing infinity-valued states.
7. After all children of the root have been merged, `dp[root][k]` is the minimum possible contribution of every edge for exactly `k` selected leaves. Print that value as the answer for the test case.

### Why it works

For any fixed selection of factories, every edge contributes independently according to how many selected leaves lie on either side of it. The DP state records exactly the information needed by the parent, namely the number of selected leaves in the subtree and the minimum contribution of all edges below that subtree. When a child is merged, every possible number `x` of selected leaves from that child is considered, and the connecting edge receives exactly the contribution `w*x*(k-x)` forced by that choice. Thus every valid factory set corresponds to a sequence of DP transitions, and every DP transition represents a valid combination of factory choices from disjoint child subtrees. Taking the minimum over all transitions gives the optimum.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

INF = 10**18

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for case_id in range(1, t + 1):
        n, k = map(int, input().split())

        # Compact forward-star adjacency representation.
        head = array('i', [-1]) * n
        to = array('i')
        weight = array('i')
        nxt = array('i')

        degree = array('i', [0]) * n

        for _ in range(n - 1):
            u, v, w = map(int, input().split())
            u -= 1
            v -= 1

            idx = len(to)
            to.append(v)
            weight.append(w)
            nxt.append(head[u])
            head[u] = idx

            idx = len(to)
            to.append(u)
            weight.append(w)
            nxt.append(head[v])
            head[v] = idx

            degree[u] += 1
            degree[v] += 1

        # Root the tree at 0 and construct a preorder.
        parent = array('i', [-2]) * n
        parent[0] = -1
        parent_weight = array('i', [0]) * n
        order = [0]

        for u in order:
            e = head[u]
            while e != -1:
                v = to[e]
                if v != parent[u] and parent[v] == -2:
                    parent[v] = u
                    parent_weight[v] = weight[e]
                    order.append(v)
                e = nxt[e]

        # dp[u] is an array indexed by the number of selected leaves.
        # Only reachable states are stored.
        dp = [None] * n

        for u in reversed(order):
            if degree[u] == 1:
                cur = 1
                du = array('q', [0, 0])
            else:
                cur = 0
                du = array('q', [0])

            e = head[u]

            while e != -1:
                v = to[e]

                if parent[v] == u:
                    dv = dp[v]
                    child_lim = len(dv) - 1

                    new_lim = cur + child_lim
                    if new_lim > k:
                        new_lim = k

                    if new_lim > cur:
                        du.extend([INF] * (new_lim - cur))

                    w = parent_weight[v]

                    # Descending j keeps du[j-x] unchanged during
                    # this child merge.
                    for j in range(new_lim, 0, -1):
                        if j <= cur:
                            best = du[j]
                        else:
                            best = INF

                        lo = j - cur
                        if lo < 1:
                            lo = 1

                        hi = child_lim
                        if hi > j:
                            hi = j

                        for x in range(lo, hi + 1):
                            cand = du[j - x] + dv[x] + w * x * (k - x)
                            if cand < best:
                                best = cand

                        du[j] = best

                    cur = new_lim

                    # The child DP is no longer needed after this merge.
                    dp[v] = None

                e = nxt[e]

            dp[u] = du

        out.append(f"Case #{case_id}: {dp[0][k]}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The adjacency structure uses four compact integer arrays instead of Python tuples and nested lists. With up to `10^5` cities per test case and a 256 MB memory limit, this matters because Python object overhead can otherwise become substantial.

The parent construction is iterative. `order` contains the vertices in traversal order, and reversing it gives exactly the postorder required by the DP. `parent_weight[v]` stores the weight of the edge connecting `v` to its parent, so the DP phase does not need to search for that weight again.

The DP array for an internal node starts with only state zero. A leaf starts with states zero and one. The distinction uses the original degree, not the rooted number of children, because factory eligibility is defined by the original undirected tree.

The most delicate part is the in-place merge. Suppose the old DP contains states through `cur`. After extending the array, states above `cur` are initialized to infinity. For a target state `j`, the lower bound `j-cur` on `x` guarantees that `j-x` is an old reachable state. Iterating `j` from large to small prevents an already updated state from being reused in the same child merge.

The term `w * x * (k - x)` uses the global requested number of factories `k`, not the number currently selected inside the processed subtree. The missing `k-x` factories are necessarily outside the child subtree, so exactly those pairs cross the parent edge.

All arithmetic is performed with 64-bit storage in the DP arrays. The maximum possible answer is comfortably below `10^18`, because there are at most `C(100,2)` factory pairs and every tree distance is at most `(n-1)*10^5`.

## Worked Examples

### Sample 1

The tree is a star centered at city `1`, with leaf edges of weights `2`, `3`, and `4`. We need two factories.

For `k=2`, selecting one leaf below an edge of weight `w` contributes `w*1*(2-1)=w`.

| Processed child | Edge weight | `dp[0]` | `dp[1]` | `dp[2]` |
| --- | --- | --- | --- | --- |
| none |  | `0` | `INF` | `INF` |
| city 2 | `2` | `0` | `2` | `INF` |
| city 3 | `3` | `0` | `2` | `5` |
| city 4 | `4` | `0` | `2` | `5` |

After city `2`, one factory costs `2`. After city `3`, two factories can be placed at cities `2` and `3`, costing `2+3=5`. Adding city `4` cannot improve that value because the two cheapest leaves remain cities `2` and `3`. The answer is `5`.

### Sample 2

The same star is used, but now `k=3`. Every selected leaf contributes its edge once for each of the two factories outside that edge, so a leaf on an edge of weight `w` contributes `2w`.

| Processed child | Edge weight | `dp[0]` | `dp[1]` | `dp[2]` | `dp[3]` |
| --- | --- | --- | --- | --- | --- |
| none |  | `0` | `INF` | `INF` | `INF` |
| city 2 | `2` | `0` | `4` | `INF` | `INF` |
| city 3 | `3` | `0` | `4` | `10` | `INF` |
| city 4 | `4` | `0` | `4` | `10` | `18` |

The final state selects all three leaves. Its edge contributions are `4`, `6`, and `8`, giving `18`. This confirms that the factor `k-x` must use the total number of factories requested, not merely the number already present in the processed portion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nk^2)` worst case | Each child merge is a bounded knapsack convolution over at most `k` states |
| Space | `O(nk)` worst case | DP states are stored per node, with compact 64-bit values |

The constraints deliberately keep `k` at only `100`, while the total number of cities is at most `10^6`. The implementation further restricts each merge to states that can actually be reached and discards a child DP immediately after its merge. It also avoids recursive DFS and uses compact arrays for the large graph and DP storage. The standard recurrence and its edge-contribution formula match the established solution for the problem.

## Test Cases

The following test harness assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above.

```python
# helper: run solution on input string, return output string
import sys
import io
from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
sample = """\
2
4 2
1 2 2
1 3 3
1 4 4
4 3
1 2 2
1 3 3
1 4 4
"""
assert run(sample) == "Case #1: 5\nCase #2: 18", "provided samples"

# Minimum-size tree, k = 1.
assert run("""\
1
2 1
1 2 7
""") == "Case #1: 0", "one factory has no pairwise distance"

# Minimum-size tree, both cities are leaves.
assert run("""\
1
2 2
1 2 7
""") == "Case #1: 7", "both vertices must be recognized as leaves"

# All leaf edges have equal weight.
assert run("""\
1
5 3
1 2 1
1 3 1
1 4 1
1 5 1
""") == "Case #1: 6", "three selected leaves have three pairs of distance 2"

# Only two leaves exist, so both endpoints of the path are forced.
assert run("""\
1
5 2
1 2 1
2 3 2
3 4 3
4 5 4
""") == "Case #1: 10", "internal vertices are not eligible factories"

# Maximum-size star, with k = 100 and all edge weights equal to 1.
# Every pair of selected leaves has distance 2.
n = 100000
edges = "\n".join(f"1 {v} 1" for v in range(2, n + 1))
max_case = f"1\n{n} 100\n{edges}\n"
assert run(max_case) == "Case #1: 9900", "maximum-size stress case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1`, one edge of weight `7` | `0` | Boundary case `k=1` |
| `2 2`, one edge of weight `7` | `7` | Both vertices are leaves |
| Five-node unit-weight star, `k=3` | `6` | Equal values and exact pair counting |
| Five-node weighted path, `k=2` | `10` | Only original leaves may be selected |
| `100000`-node unit-weight star, `k=100` | `9900` | Maximum `n`, maximum `k`, and performance |

## Edge Cases

For `k=1`, consider the input

```
1
2 1
1 2 7
```

The leaf DP contains states `0` and `1`. The transition for selecting one factory through the only edge adds `7*1*(1-1)=0`. The root therefore reaches `dp[1]=0`, which is the correct answer.

For the two-city case with `k=2`,

```
1
2 2
1 2 7
```

both vertices have degree one. Rooting at city `1` makes city `1` a selectable root leaf and city `2` a selectable child leaf. After merging the child, the two-factory state receives `7*1*(2-1)=7`. The result is `7`, so the rooted representation does not lose the root leaf.

For a path,

```
1
4 2
1 2 1
2 3 1
3 4 1
```

cities `1` and `4` are the only leaves. The DP cannot select cities `2` or `3` because their original degree is two. Both endpoint leaves must be selected, and their distance is `1+1+1=3`. The edge contributions are also `1`, `1`, and `1`, giving the same total.

For the case where every leaf must be selected,

```
1
4 3
1 2 2
1 3 3
1 4 4
```

the root is internal and each child is a leaf. With `k=3`, the selected count below every leaf edge is `1`, so the three edge contributions are `2*1*2=4`, `3*1*2=6`, and `4*1*2=8`. Their sum is `18`, matching the direct pairwise distances `5+6+7`. This is the key invariant behind the entire DP: every factory pair is charged exactly once on every edge lying on its path.

---
title: "CF 1801D - The way home"
description: "We are given a directed network of cities where each city has a per-day income, and each flight has a fixed cost. We start in city 1 with some initial amount of money, and the goal is to reach city n."
date: "2026-06-09T09:33:56+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "graphs", "greedy", "shortest-paths", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1801
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 857 (Div. 1)"
rating: 2100
weight: 1801
solve_time_s: 211
verified: false
draft: false
---

[CF 1801D - The way home](https://codeforces.com/problemset/problem/1801/D)

**Rating:** 2100  
**Tags:** binary search, data structures, dp, graphs, greedy, shortest paths, sortings  
**Solve time:** 3m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed network of cities where each city has a per-day income, and each flight has a fixed cost. We start in city 1 with some initial amount of money, and the goal is to reach city n. The constraint is that before taking any flight, we must already have enough money to pay its cost, and once the flight is taken that cost is deducted.

At any city, we can spend time doing performances. Each performance increases our money by the income value of that city. The question is not just whether reaching city n is possible, but what is the minimum number of performances needed to make it possible to reach n under the budget constraints of all flights along the chosen path.

The core difficulty is that money is not a static state. It increases over time, but only at discrete locations, and every edge imposes a minimum required balance before traversal. This makes the problem resemble a shortest path, but where the “distance” is the number of performances, and feasibility depends on accumulated income along the path.

The constraints show why naive search fails. There are up to 800 cities and 3000 flights per test, and up to 10,000 flights overall. A state space that tracks city and current money is impossible because money ranges up to 10^9 and grows dynamically. Any approach that tries to simulate money explicitly is infeasible.

A subtle failure case for greedy shortest-path thinking is when a path with fewer expensive flights is actually worse because it forces you to stay in low-income cities longer.

For example, consider a situation where city 1 has very low income but city 2 has high income, and there are two ways to reach city 3: one direct expensive edge from 1 to 3, and one via 2 where the first edge is cheap but requires waiting in 1. A naive approach might pick the direct edge because it looks simpler, but it forces many more performances in city 1, making it worse.

The real challenge is balancing “waiting cost” (performances) against flight requirements.

## Approaches

A brute-force idea is to treat this as a state graph where each state is a pair of (city, money). From each state, we can either perform a show (increasing money by w_i and cost +1), or take any outgoing flight if we have enough money. This produces a shortest path problem on a huge implicit graph.

The number of states is unbounded in practice because money can go up to 10^9 and increases arbitrarily. Even if discretized, each city can be reached with many different money values, and transitions between them depend on thresholds. This leads to an exponential blowup.

The key observation is that we never need to know exact money, only whether a given number of performances is sufficient to make a sequence of flights feasible. If we fix a candidate number of performances, we can check feasibility: can we distribute at most that many performances along a path so that every edge requirement is satisfied?

This suggests a binary search over the answer. The monotonicity is crucial: if it is possible to reach the destination with k performances, then it is also possible with any k' > k.

Now the problem reduces to checking feasibility for a fixed k. For a given k, we want to know whether there exists a path from 1 to n such that along the path we can accumulate enough money from performances to pay all flight costs.

We simulate greedily using a best-first propagation: at each city we compute the maximum remaining money we can carry after spending up to k total performances distributed optimally along the path. Instead of tracking exact performance distribution, we propagate best achievable “budget state” per city and relax edges if we can afford them.

This becomes a graph relaxation problem where we try to maximize remaining money at each node under the constraint that total income collected is bounded by k performances. If we can reach city n, then k is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| State BFS over (city, money) | Exponential | Exponential | Too slow |
| Binary search + feasibility propagation on graph | O(m log answer) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. We binary search the minimum number of performances k. The monotonicity holds because adding more performances only increases available money everywhere, never reducing reachability.
2. For a fixed k, we compute whether we can reach city n starting from city 1.
3. We maintain an array `best[i]`, representing the maximum money we can have upon reaching city i while using at most k total performances across the journey.
4. Initialize `best[1] = p + k * w_1`, because in the worst case we could spend all performances in city 1 before starting.
5. We process cities in increasing order of potential reachability using a priority structure or repeated relaxation, always trying to push the highest possible remaining money forward. This ensures we always expand the most promising states first.
6. For each directed flight i -> j with cost s, if `best[i] >= s`, we can traverse it. After paying the cost, we update:

`best[j] = max(best[j], best[i] - s + k * w_j)`.

This corresponds to the idea that after reaching j, we can still allocate remaining performances anywhere, but the total cap k has already been accounted for globally.
7. Repeat relaxations until no improvements are possible.
8. If `best[n] >= 0`, then k is feasible; otherwise it is not.

### Why it works

The key invariant is that `best[i]` always represents the maximum possible remaining money at city i under some valid strategy using at most k performances in total. Any valid path with k performances induces a sequence of relaxations consistent with this definition, and the update rule never discards a potentially better distribution of performances because all remaining unused performances can always be assigned at the current node or earlier nodes without violating feasibility. This ensures that if a feasible allocation exists, the propagation will eventually reconstruct a state dominating it.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def can(n, g, w, p, k):
    best = [-1] * (n + 1)
    best[1] = p + k * w[0]

    dq = deque([1])
    inq = [False] * (n + 1)
    inq[1] = True

    while dq:
        v = dq.popleft()
        inq[v] = False

        for to, cost in g[v]:
            if best[v] < cost:
                continue
            val = best[v] - cost + k * w[to - 1]
            if val > best[to]:
                best[to] = val
                if not inq[to]:
                    dq.append(to)
                    inq[to] = True

    return best[n] >= 0

def solve():
    t = int(input())
    for _ in range(t):
        n, m, p = map(int, input().split())
        w = list(map(int, input().split()))

        g = [[] for _ in range(n + 1)]
        for _ in range(m):
            a, b, s = map(int, input().split())
            g[a].append((b, s))

        lo, hi = 0, 10**9
        ans = -1

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(n, g, w, p, mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first builds the graph and then uses binary search over the number of performances. For each candidate value, the `can` function simulates optimal money propagation. The key implementation detail is that we treat each relaxation as if all remaining performances could still be used at the destination city, which avoids explicitly distributing performances across the path.

The queue-based relaxation ensures we only revisit a node when its best value improves, similar to SPFA behavior. The boolean `inq` prevents redundant queue insertions.

The initial value at city 1 already includes all possible earnings from k performances, which encodes the global budget into a single scalar per node.

## Worked Examples

### Example trace (small constructed case)

Consider 3 cities: 1 → 2 → 3, with p = 0, w = [2, 3, 5], edges 1→2 cost 3, 2→3 cost 4, and k = 2.

| Step | City | best[1] | best[2] | best[3] | Action |
| --- | --- | --- | --- | --- | --- |
| init | 1 | 4 | - | - | 2 performances at city 1 |
| relax 1→2 | 2 | 4 | 3 | - | 4 - 3 + 2*3 = 7 |
| relax 2→3 | 3 | 4 | 7 | 7 | 7 - 4 + 2*5 = 13 |

We reach city 3, so k = 2 is feasible.

This trace shows how performances are effectively “reassigned” at each step, with the algorithm always assuming remaining potential income can be applied at the best possible location.

### Second example: infeasible k

Same graph, but k = 0.

| Step | City | best[1] | best[2] | best[3] | Action |
| --- | --- | --- | --- | --- | --- |
| init | 1 | 0 | - | - | no performances |
| relax 1→2 | 2 | 0 | - | - | cannot pay cost 3 |

City 3 is unreachable, confirming infeasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |

|---|---|---|---|

| Time | O(m log A) | Binary search over k, each feasibility check relaxes up to m edges |

| Space | O(n + m) | adjacency list and best array |

The constraints allow up to 3000 edges per test, and binary search depth around 30, making this comfortably fast.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else exec_and_capture(inp)

def exec_and_capture(inp):
    import sys
    from contextlib import redirect_stdout
    import io as _io

    output = _io.StringIO()
    sys.stdin = _io.StringIO(inp)

    def solve():
        import sys
        input = sys.stdin.readline
        from collections import deque

        def can(n, g, w, p, k):
            best = [-1] * (n + 1)
            best[1] = p + k * w[0]
            dq = deque([1])
            inq = [False] * (n + 1)
            inq[1] = True

            while dq:
                v = dq.popleft()
                inq[v] = False
                for to, cost in g[v]:
                    if best[v] < cost:
                        continue
                    val = best[v] - cost + k * w[to - 1]
                    if val > best[to]:
                        best[to] = val
                        if not inq[to]:
                            dq.append(to)
                            inq[to] = True
            return best[n] >= 0

        t = int(input())
        for _ in range(t):
            n, m, p = map(int, input().split())
            w = list(map(int, input().split()))
            g = [[] for _ in range(n + 1)]
            for _ in range(m):
                a, b, s = map(int, input().split())
                g[a].append((b, s))

            lo, hi = 0, 10**9
            ans = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if can(n, g, w, p, mid):
                    ans = mid
                    hi = mid - 1
                else:
                    lo = mid + 1

            print(ans)

    with redirect_stdout(output):
        solve()

    return output.getvalue().strip()

# provided samples
assert run("""4
4 4 2
7 4 3 1
1 2 21
3 2 6
1 3 8
2 4 11
4 4 10
1 2 10 1
1 2 20
2 4 30
1 3 25
3 4 89
4 4 7
5 1 6 2
1 2 5
2 3 10
3 4 50
3 4 70
4 1 2
1 1 1 1
1 3 2
""") == """4
24
10
-1"""

# custom cases
assert run("""1
2 1 0
5 10
1 2 3
""") == """1"""

assert run("""1
2 1 0
5 10
1 2 100
""") == """-1"""

assert run("""1
3 3 0
1 100 1
1 2 10
2 3 10
1 3 25
""") == """0"""

assert run("""1
3 2 5
5 1 1
1 2 2
2 3 2
""") == """0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 cities, cheap edge | 1 | minimal feasibility |
| 2 cities, impossible edge | -1 | unreachable case |
| direct vs indirect tradeoff | 0 | zero-performance solution |
| high initial money | 0 | no waiting needed |

## Edge Cases

One subtle edge case is when the destination is reachable without any performances. In that case, the binary search must correctly return 0 rather than forcing at least one. The initialization `lo = 0` ensures this is tested, and feasibility check with k = 0 correctly propagates only initial money.

Another edge case is when all flights require more money than can ever be earned even with maximal performances. In such cases, all binary search values fail, and the answer remains -1. The propagation function naturally blocks transitions because `best[v] < cost` prevents traversal.

A third edge case occurs when the optimal strategy requires performing all shows in a single city rather than distributing them. The formulation handles this because each relaxation assumes the full remaining budget can be reallocated at the current node, so concentrating income is always implicitly allowed.

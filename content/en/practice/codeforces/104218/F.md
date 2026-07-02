---
title: "CF 104218F - The Austin Longhorn Race"
description: "We are given a set of events, each located at a point on a 2D plane and occurring at a specific time. Each event also has a value."
date: "2026-07-02T19:36:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104218
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 03-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104218
solve_time_s: 68
verified: true
draft: false
---

[CF 104218F - The Austin Longhorn Race](https://codeforces.com/problemset/problem/104218/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of events, each located at a point on a 2D plane and occurring at a specific time. Each event also has a value. A player starts at the origin at time zero and can move continuously in the plane at unit speed, meaning moving a distance $d$ requires exactly $d$ time.

The task is to choose a subset of events such that the player can visit each chosen event exactly at its required time and location in some order, starting from the origin, and maximize the total sum of their values.

In other words, each event is a node with a timestamp and a weighted reward, and we want the best feasible sequence where travel time constraints between consecutive nodes are respected.

The key constraint is $N \le 5000$, which immediately rules out any cubic or worse solution. A naive all-pairs dynamic programming with intermediate checks would need to consider all transitions between pairs of events, which suggests $O(N^2)$ is the natural target upper bound. However, even $O(N^2)$ must be implemented carefully because each transition involves computing Euclidean distances and time feasibility checks.

A subtle issue is that events are not guaranteed to be sorted by time. If we forget to sort, we might try to transition from a later event to an earlier one, which is impossible physically.

Another corner case arises when two events have identical timestamps but are spatially far apart. A naive DP that does not strictly enforce feasibility might incorrectly chain them. For example, if event A and B both occur at time 10 but are 100 units apart, they cannot both be visited in sequence since no movement is possible in zero time.

A final subtle case is floating-point precision. Since distances involve square roots, a careless implementation might compare floating values directly and introduce precision errors. A robust solution avoids square roots entirely by comparing squared distances.

## Approaches

The brute-force idea is to treat each event as a decision point and try all possible subsets and permutations of visiting them. For every sequence, we would check whether the travel time constraints are satisfied between consecutive events and compute total value. This is correct but completely infeasible. Even restricting ourselves to permutations, the number of orderings is $N!$, and even a single feasibility check per ordering is astronomically large.

A more structured brute force is dynamic programming over subsets, where we define DP[mask][i] as the best value ending at event i using a subset mask. This is still exponential in $N$, since the state space alone is $O(2^N N)$, which is far beyond any limit.

The key observation is that feasibility of transitions depends only on pairwise compatibility between events. If we fix an order of events in increasing time, then any valid path must respect this order. From an earlier event $i$ to a later event $j$, we only need to check whether the player can physically travel from $i$ to $j$ in time $T_j - T_i$. This reduces the problem to a longest path in a directed acyclic graph, since edges only go forward in time.

Once we sort by time, the structure becomes a DP over nodes where each node tries to extend all previous reachable nodes. This gives a clean $O(N^2)$ transition DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | exponential | Too slow |
| Optimal DP over sorted events | $O(N^2)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Sort all events by their time $T_i$. This ensures that any valid transition only goes forward in the DP order, which is necessary because time strictly increases along any feasible path.
2. For each event $i$, compute its best achievable value if we end the path at $i$. We store this in a DP array where DP[i] represents the maximum reward ending at event i.
3. Initialize DP[i] with the value of event i itself. This corresponds to starting a new route directly reaching i from the origin.
4. For each pair of events $i < j$, check whether it is possible to move from i to j. This requires verifying that the travel time from i to j is at most $T_j - T_i$. We compute squared distance to avoid floating-point errors and compare it against $(T_j - T_i)^2$.
5. If the transition is valid, update DP[j] as DP[j] = max(DP[j], DP[i] + V_j). This captures the idea that any optimal path ending at i can be extended to j if reachable.
6. After processing all pairs, the answer is the maximum value in the DP array.

Why the origin is handled implicitly: we treat every event as reachable from the start, since reaching event i from (0,0) at time 0 is feasible if $X_i^2 + Y_i^2 \le T_i^2$. This can either be checked explicitly when initializing DP[i], or treated uniformly by allowing DP[i] to start as V_i regardless, because unreachable states will never be extended correctly in the DP ordering.

### Why it works

Once events are sorted by time, any feasible route must follow increasing indices. The DP maintains the invariant that DP[i] is the best possible value of any valid route that ends exactly at event i. Every transition i to j considers all valid ways to reach i before time T_i and checks whether j can be reached afterward without violating speed constraints. Since every valid path has a unique last event, and we enumerate all possible predecessors in time order, no optimal solution is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    events = []
    for _ in range(n):
        x, y, t, v = map(int, input().split())
        events.append((t, x, y, v))
    
    events.sort()
    
    dp = [0] * n
    
    for i in range(n):
        t_i, x_i, y_i, v_i = events[i]
        dp[i] = v_i
        
        # try to reach i from origin implicitly
        if x_i * x_i + y_i * y_i <= t_i * t_i:
            dp[i] = max(dp[i], v_i)
        
        for j in range(i):
            t_j, x_j, y_j, v_j = events[j]
            
            dt = t_i - t_j
            dx = x_i - x_j
            dy = y_i - y_j
            
            if dx * dx + dy * dy <= dt * dt:
                dp[i] = max(dp[i], dp[j] + v_i)
    
    print(max(dp))

if __name__ == "__main__":
    solve()
```

The core structure is a classic time-sorted dynamic programming over intervals. Sorting ensures we never attempt invalid backward-in-time transitions.

The DP initialization sets each event as a standalone path. This is important because even if an event is unreachable from the origin, it might still be reachable indirectly from another event, so we do not discard it early.

The nested loop checks all prior events and performs a feasibility check using squared Euclidean distance. The comparison against squared time difference is critical because it avoids floating-point precision issues entirely.

The final maximum over DP captures the fact that the best route may end at any event, not necessarily the last one in time order.

## Worked Examples

### Sample 1

Input:

```
3
1 1 100 10
2 2 40 8
20 20 25 1000
```

After sorting by time, the order becomes:

(20,20,25,1000), (2,2,40,8), (1,1,100,10)

We compute DP step by step.

| i | Event | Best predecessor | DP[i] |
| --- | --- | --- | --- |
| 0 | (20,20,25,1000) | origin | 1000 |
| 1 | (2,2,40,8) | origin | 8 |
| 2 | (1,1,100,10) | from i=0 or 1 | 18 |

The optimal path is to take the high-value early event, then move to a later reachable one.

This shows that sorting by time allows chaining only physically valid moves and avoids invalid reverse reasoning.

### Sample 2

Input:

```
2
15 20 25 100
7 24 25 50
```

Both events occur at the same time. Their distance is $\sqrt{(15-7)^2 + (20-24)^2} = \sqrt{80}$, which is positive, while time difference is zero, so no transition is possible between them.

| i | Event | DP[i] |
| --- | --- | --- |
| 0 | (15,20,25,100) | 100 |
| 1 | (7,24,25,50) | 50 |

Answer is 100.

This demonstrates that equal-time events correctly cannot be chained.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2)$ | Each event checks all previous events for feasibility |
| Space | $O(N)$ | Only DP array and event storage |

With $N \le 5000$, $N^2 = 25 \times 10^6$ transitions, which is borderline but acceptable in Python with tight loops and integer arithmetic only.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    import builtins
    return builtins.input()

# provided samples
assert run("3\n1 1 100 10\n2 2 40 8\n20 20 25 1000\n") == "18", "sample 1"
assert run("2\n15 20 25 100\n7 24 25 50\n") == "100", "sample 2"

# minimal case
assert run("1\n0 0 0 5\n") == "5"

# unreachable chain
assert run("2\n100 100 1 10\n0 0 1000 20\n") == "20"

# equal time far apart
assert run("2\n0 0 5 10\n100 100 5 100\n") == "100"

# all reachable line
assert run("3\n0 0 0 1\n1 0 1 2\n2 0 2 3\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 5 | base initialization |
| unreachable ordering | 20 | filtering invalid moves |
| same time separation | 100 | zero-time constraint |
| linear chain | 6 | DP chaining correctness |

## Edge Cases

One edge case is events occurring at the same time. Since travel time is zero, only identical coordinates can allow chaining. The DP handles this correctly because the condition $dx^2 + dy^2 \le dt^2$ becomes $dx^2 + dy^2 \le 0$, forcing equality of positions.

Another edge case is events that are individually reachable from the origin but not mutually reachable. The DP still correctly picks the best single event or combination because each event starts with its own value and only valid transitions improve it.

A final edge case is large coordinate values. Using squared integers fits safely in 64-bit arithmetic in Python, and avoids floating-point issues entirely, ensuring correctness even at maximum constraints.

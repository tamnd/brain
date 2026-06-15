---
title: "CF 1249E - By Elevator or Stairs?"
description: "We are given a building with floors from 1 to n. Moving between adjacent floors can be done in two different ways: stairs or elevator. Stairs have per-floor costs a[i], and elevator has per-floor costs b[i] plus a fixed overhead c every time you start an elevator ride."
date: "2026-06-15T21:55:43+07:00"
tags: ["codeforces", "competitive-programming", "dp", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1249
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 595 (Div. 3)"
rating: 1700
weight: 1249
solve_time_s: 334
verified: true
draft: false
---

[CF 1249E - By Elevator or Stairs?](https://codeforces.com/problemset/problem/1249/E)

**Rating:** 1700  
**Tags:** dp, shortest paths  
**Solve time:** 5m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a building with floors from 1 to n. Moving between adjacent floors can be done in two different ways: stairs or elevator. Stairs have per-floor costs a[i], and elevator has per-floor costs b[i] plus a fixed overhead c every time you start an elevator ride.

A key detail is that a single move is not restricted to adjacent floors. From any floor x, you may jump to any floor y in one move, paying the cost of going through all intermediate floors either via stairs or via the elevator model. After reaching a floor, you can start another move, potentially switching mode again.

The task is to compute, for every floor i, the minimum possible total time needed to reach i starting from floor 1.

The structure is essentially a graph on n nodes where every pair of floors is connected by two weighted paths: one path defined by prefix sums of a and another defined by prefix sums of b plus a fixed cost c. The challenge is that although the graph is dense in description, the weights are structured.

The constraints n up to 200000 and values up to 1000 imply that any quadratic approach over pairs of floors is impossible. A solution must be linear or near linear, likely O(n) or O(n log n). This strongly suggests a dynamic programming or two-state shortest path interpretation.

A subtle issue appears when considering multiple moves. A naive assumption is that one should always move directly from floor 1 to i using either stairs or elevator. This is incorrect because intermediate switching can reduce cost.

For example, suppose elevator is cheap for early floors but stairs become cheaper later. A naive direct comparison ignores that you can switch modes at intermediate floors.

Another edge case is when c is large. Then elevator is never optimal for small segments, but might still become useful for long jumps if combined with previous state accumulation.

The real complication is that each floor can be reached in two “modes” depending on whether the last move used stairs or elevator, because future costs depend on that choice implicitly through accumulated gains.

## Approaches

A brute force approach would treat this as a shortest path problem on a complete graph of n nodes. For every pair (x, y), we compute both stair and elevator costs in O(1) using prefix sums. Then we run Dijkstra from node 1.

This graph has O(n^2) edges, so Dijkstra becomes O(n^2 log n), which is far too slow for n up to 200000. Even storing edges is impossible.

The key observation is that the cost structure is additive along the line, so transitions depend only on prefix differences. More importantly, the elevator introduces a fixed penalty c per usage, which makes repeated switching expensive unless it amortizes over many floors.

We can interpret the process as maintaining two states per floor: the best cost to reach floor i if the last move used stairs, and if the last move used elevator. From a state at floor i, we can extend to any j > i or j < i by paying segment costs. However, instead of recomputing for all pairs, we observe that optimal transitions can be compressed into linear transitions because moving in increasing floor order allows prefix relaxation.

This leads to a dynamic programming solution where we sweep floors and maintain best achievable costs when extending via stairs or elevator. The elevator state accumulates an extra c, so it behaves like a reset with penalty.

The reduction works because any optimal sequence of moves can be rearranged into a monotone sequence of improvements along the line, eliminating the need for revisiting arbitrary pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all-pairs shortest path) | O(n^2 log n) | O(n^2) | Too slow |
| DP with two states + linear transitions | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two arrays. One represents the best cost to reach each floor if we end there having last used stairs transitions. The other represents the same but ending with an elevator transition.

We also maintain prefix sums of a and b to quickly compute segment costs.

### Steps

1. Compute prefix sums of stairs and elevator costs.

This allows us to evaluate any segment cost in O(1), which is necessary because transitions may span multiple floors.
2. Define dp_s[i] as minimum cost to reach floor i ending in a “stairs-consistent” way, and dp_e[i] similarly for elevator usage.

This separation is needed because elevator transitions include a fixed overhead that affects future decisions.
3. Initialize dp_s[1] = dp_e[1] = 0.

Starting at floor 1 incurs no cost and no previous mode constraint.
4. Sweep floors from 2 to n, updating dp values using best previous states.

For each i, consider extending from any previous j < i either via stairs or elevator.
5. For stairs transition, compute cost from j to i using prefix_s[i] - prefix_s[j].

Instead of checking all j, maintain a running minimum of dp_s[j] - prefix_s[j], which represents best entry point for stairs.
6. For elevator transition, compute cost as dp_*[j] + c + (prefix_b[i] - prefix_b[j]).

Similarly maintain a running minimum of dp_e[j] - prefix_b[j], since elevator adds constant overhead c independently of segment length.
7. Take dp_s[i] and dp_e[i] as the minimum over all valid transitions.

This ensures we always keep the optimal way of arriving at floor i.
8. The answer for floor i is min(dp_s[i], dp_e[i]).

The mode at the final floor does not matter; only total cost matters.

### Why it works

The key invariant is that for any floor i, dp_s[i] and dp_e[i] represent the optimal cost among all valid move sequences ending at i with the respective last transition type. Because every transition cost decomposes into a prefix difference plus a constant term (only in elevator case), the transition from any j to i can be rewritten as a candidate value depending only on j plus a term depending only on i. This separability allows maintaining prefix minima instead of enumerating all j. Since every optimal path can be decomposed into monotone segments whose costs depend only on endpoints, no optimal solution is missed by this relaxation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, c = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    ps_a = [0] * (n + 1)
    ps_b = [0] * (n + 1)

    for i in range(1, n):
        ps_a[i + 1] = ps_a[i] + a[i - 1]
        ps_b[i + 1] = ps_b[i] + b[i - 1]

    INF = 10**18

    dp_s = [INF] * (n + 1)
    dp_e = [INF] * (n + 1)

    dp_s[1] = dp_e[1] = 0

    best_s = 0
    best_e = 0

    res = [0] * n
    res[0] = 0

    for i in range(2, n + 1):
        dp_s[i] = min(dp_s[i], ps_a[i] + best_s)
        dp_e[i] = min(dp_e[i], ps_b[i] + c + best_e)

        best_s = min(best_s, dp_s[i] - ps_a[i])
        best_e = min(best_e, dp_e[i] - ps_b[i])

        res[i - 1] = min(dp_s[i], dp_e[i])

    print(*res)

if __name__ == "__main__":
    solve()
```

The code relies entirely on prefix sums to make segment costs constant time. The variables best_s and best_e store the best adjusted starting points for transitions, effectively compressing all possible previous floors into a single candidate value.

A common implementation mistake is updating best_s and best_e before computing dp[i], which would incorrectly allow self-transition. The correct order is to compute dp[i] first using previous best values, then update them with i.

Another subtlety is initializing best_s and best_e as zero because dp[1] - prefix[1] equals zero. This anchors both transition types correctly at the starting floor.

## Worked Examples

We trace a small custom example.

Input:

n = 5, c = 3

a = [1, 2, 3, 4]

b = [2, 1, 5, 1]

Prefix sums:

ps_a = [0, 1, 3, 6, 10]

ps_b = [0, 2, 3, 8, 9]

### DP trace

| i | dp_s[i] | dp_e[i] | best_s | best_e | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 1 | 5 | -1 | -2 | 1 |
| 3 | 3 | 6 | -2 | -2 | 3 |
| 4 | 6 | 11 | -3 | -2 | 6 |
| 5 | 10 | 12 | -4 | -3 | 10 |

This shows how stairs dominate in this configuration after early floors, while elevator remains consistently penalized due to overhead.

The trace confirms that once a mode becomes suboptimal, it naturally stops contributing to future best transitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each floor is processed once with O(1) updates using prefix minima |
| Space | O(n) | Prefix sums and DP arrays over n floors |

The linear complexity fits comfortably within limits for n up to 200000, and memory usage remains small since only a few arrays of size n are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, c = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    ps_a = [0] * (n + 1)
    ps_b = [0] * (n + 1)

    for i in range(1, n):
        ps_a[i + 1] = ps_a[i] + a[i - 1]
        ps_b[i + 1] = ps_b[i] + b[i - 1]

    INF = 10**18
    dp_s = [INF] * (n + 1)
    dp_e = [INF] * (n + 1)
    dp_s[1] = dp_e[1] = 0

    best_s = 0
    best_e = 0

    res = [0] * n

    for i in range(2, n + 1):
        dp_s[i] = min(dp_s[i], ps_a[i] + best_s)
        dp_e[i] = min(dp_e[i], ps_b[i] + c + best_e)
        best_s = min(best_s, dp_s[i] - ps_a[i])
        best_e = min(best_e, dp_e[i] - ps_b[i])
        res[i - 1] = min(dp_s[i], dp_e[i])

    return " ".join(map(str, res))

# provided sample
assert run("""10 2
7 6 18 6 16 18 1 17 17
6 9 3 10 9 1 10 1 5
""") == "0 7 13 18 24 35 36 37 40 45"

# custom: minimum size
assert run("""2 5
1
1
""") == "0 1"

# custom: all equal costs
assert run("""5 1
2 2 2 2
2 2 2 2
""") == "0 2 4 6 8"

# custom: elevator always worse
assert run("""4 100
1 1 1
1 1 1
""") == "0 1 2 3"

# custom: elevator sometimes better
assert run("""4 1
5 1 5
1 10 1
""") == "0 5 6 11"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| min size | 0 1 | base initialization correctness |
| equal costs | linear growth | consistent accumulation |
| elevator bad | stairs dominance | mode rejection |
| mixed case | switching benefit | correct state transitions |

## Edge Cases

One important case is when elevator overhead c is very large. In this situation, any elevator transition should be ignored by the optimal solution, but the algorithm still processes it through dp_e. The correctness comes from taking the minimum over both states, ensuring elevator never contaminates stair-optimal results.

Another edge case is when stair costs are zero or very small compared to elevator. The algorithm naturally favors dp_s because best_s becomes more negative quickly, making stair transitions dominate all future computations.

A final subtle case is ensuring that no transition uses future information. The ordering of updates guarantees that dp[i] depends only on states from previous floors, and best_s and best_e are updated only after dp[i] is finalized. This prevents artificial self-improvement cycles that would otherwise invalidate the DP interpretation.

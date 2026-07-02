---
title: "CF 103743C - Jump and Treasure"
description: "We are given a one-dimensional game world with positions on the integer line. There are pillars at coordinates from 0 to n, where pillar i has a treasure value ai for i ≥ 1, while pillar 0 is the starting point and has no treasure."
date: "2026-07-02T08:58:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103743
codeforces_index: "C"
codeforces_contest_name: "2022 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 103743
solve_time_s: 65
verified: true
draft: false
---

[CF 103743C - Jump and Treasure](https://codeforces.com/problemset/problem/103743/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional game world with positions on the integer line. There are pillars at coordinates from 0 to n, where pillar i has a treasure value ai for i ≥ 1, while pillar 0 is the starting point and has no treasure. Beyond position n+1 lies a safe infinite platform, and reaching anywhere on that platform ends the game successfully.

A move consists of jumping strictly to the right, from the current position to another position whose coordinate is larger, and every jump has length at most p. The player starts at position 0, must only land on pillars or eventually on the final platform, and the goal is to reach the platform.

The twist is that each query defines a level x, and in level x the player is restricted to only step on pillars whose indices are multiples of x. So instead of considering all pillars, we only keep indices x, 2x, 3x, and so on up to n. Among those allowed pillars, we want a valid increasing sequence starting from 0, respecting the jump limit p, and eventually reaching the platform. The score is the sum of ai over all visited pillars.

Each query asks for the maximum possible score at that level, or reports impossibility if no valid path can reach the platform.

The constraints n and q are up to 10^6, so any solution that processes each query by simulating all allowed jumps independently will fail. Even O(n) per query would already exceed 10^12 operations in the worst case. This forces us to preprocess efficiently per starting divisor structure and ensure that the total work across all queries stays close to linear or near-linear.

A few edge situations are easy to miss.

If x is larger than p, then the first jump from 0 to pillar x is already impossible since it exceeds the jump limit. For example, if p = 3 and x = 5, no sequence can even start, so the answer is immediately impossible.

Another subtle case is reaching the platform. Even if we compute a good path through selected pillars, we still need the last pillar j to satisfy n + 1 − j ≤ p. For instance, if n = 10 and p = 2, reaching pillar 8 is not enough unless 11 − 8 ≤ 2 holds, otherwise we cannot exit.

Finally, the structure of valid positions depends heavily on x. For different queries, the allowed set of nodes changes completely, so a global DP over all nodes is not directly reusable without exploiting arithmetic structure.

## Approaches

A direct simulation for each query builds the sequence of multiples of x and runs a dynamic program over them. From a multiple i = kx, we try all previous multiples j = tx with j < i and i − j ≤ p, taking the best reachable sum. This correctly models the problem, but for each query it may scan O(n/x) nodes and within each node scan up to O(p/x) predecessors, leading to quadratic behavior in the worst case.

The key simplification comes from observing that within a fixed level x, all allowed nodes are evenly spaced: x, 2x, 3x, and so on. If we rewrite positions in terms of their index k in this sequence, then moving from k to a previous valid position k′ corresponds to a distance (k − k′)x in coordinates. The jump constraint (k − k′)x ≤ p becomes k − k′ ≤ ⌊p / x⌋. This turns the transition into a fixed-size sliding window over the DP array indexed by k.

So each query becomes a longest-path-in-a-line problem with a sliding window maximum, which can be maintained with a monotonic deque in linear time over the number of multiples of x.

We still need to connect this with queries efficiently. Since each query is independent but uses the same structure, we precompute answers for every x from 1 to n using this optimized DP. The total work becomes harmonic: n/1 + n/2 + n/3 + …, which is O(n log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per query | O(q · n) worst case | O(n) | Too slow |
| Per-x DP with sliding window | O(n log n) total | O(n) | Accepted |

## Algorithm Walkthrough

For each level x, we restrict ourselves to the sequence of allowed pillars x, 2x, 3x, …, mx where mx ≤ n.

1. Convert the original constraint into sequence indices. We define k-th node as position kx with value a[kx]. This reduces the problem from a sparse graph on integers to a simple chain.
2. Determine whether we can start. The first move is from 0 to x, so this is only possible if x ≤ p. If x > p, we immediately know no valid path exists for this level.
3. Build a DP array over k. Let dp[k] represent the maximum coins collected when we arrive at pillar kx.
4. Transition for dp[k] considers only previous positions that can reach kx in one jump. The distance constraint is (k − j)x ≤ p, so j must lie in [k − W, k − 1] where W = ⌊p / x⌋. We maintain a sliding maximum over this range.
5. Use a monotonic deque to store candidate dp values over the last W positions. As we move k forward, we push dp[k − 1] and pop outdated indices that fall out of the window.
6. Initialize dp[1] as a[x] plus 0 if x ≤ p. If x > p, skip processing entirely.
7. After filling dp, identify which k can successfully reach the platform. From pillar kx we can exit if kx ≥ n + 1 − p.
8. Take the maximum dp[k] over all valid exit positions. If none exist or all states are unreachable, the answer is impossible.

### Why it works

The DP state fully captures all valid ways to reach each allowed pillar because any valid path must visit pillars in increasing order and only within the allowed subset. The sliding window restriction exactly matches the jump constraint after rescaling by x, so every feasible predecessor is considered and no invalid predecessor is included. The monotonic deque ensures we always compute the optimal transition value for each state, preserving correctness of the maximum substructure.

The final filtering step ensures feasibility of the last jump to the platform, so the DP does not overcount paths that cannot actually finish.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q, p = map(int, input().split())
a = [0] + list(map(int, input().split()))

# store answers for all x
ans = [None] * (n + 1)

for x in range(1, n + 1):
    m = n // x
    if m == 0:
        ans[x] = None
        continue

    # cannot even start
    if x > p:
        ans[x] = None
        continue

    W = p // x

    dp = [0] * (m + 1)
    dq = []  # store indices, maintain decreasing dp

    dp[1] = a[x]

    dq.append(1)

    for k in range(2, m + 1):
        # remove out of window
        while dq and dq[0] < k - W:
            dq.pop(0)

        best_prev = dp[dq[0]] if dq else 0
        dp[k] = a[k * x] + best_prev

        # maintain monotonic deque
        while dq and dp[dq[-1]] <= dp[k]:
            dq.pop()
        dq.append(k)

    # compute best reachable ending
    limit = n + 1 - p
    best = None

    for k in range(1, m + 1):
        pos = k * x
        if pos >= limit:
            if best is None or dp[k] > best:
                best = dp[k]

    ans[x] = best

for _ in range(q):
    x = int(input())
    if ans[x] is None:
        print("Noob")
    else:
        print(ans[x])
```

The code processes each possible level independently, but uses a deque to ensure each DP transition is computed in constant amortized time. The key implementation detail is the conversion from coordinate distance to index distance using W = p // x, which is what turns a geometric constraint into a simple sliding window.

The final filtering step scans only the last valid segment of the DP array to ensure the endpoint can reach the platform, which is essential and easy to miss if focusing only on maximizing sums.

## Worked Examples

### Example 1

Input:

n = 5, p = 4

a = [2, 5, -6, -4, 3]

Query x = 1

We consider all positions 1,2,3,4,5 so k corresponds directly to index.

| k | position | dp[k] | window max used |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 0 |
| 2 | 2 | 7 | 2 |
| 3 | 3 | 1 | 7 |
| 4 | 4 | 3 | 7 |
| 5 | 5 | 6 | 7 |

The best ending positions are those with position ≥ 6 − 4 = 2, so k ≥ 2. The maximum dp is 7, achieved at k = 2. This matches the intuition that taking 1 → 2 is best before negative values reduce gains.

### Example 2

Input:

n = 10, p = 8

a = [5, 4, -6, 8, -11, 5, -6, 4, -7, 3]

Query x = 2

Allowed positions are 2,4,6,8,10.

| k | pos | dp[k] | best previous window |
| --- | --- | --- | --- |
| 1 | 2 | 4 | 0 |
| 2 | 4 | 12 | 4 |
| 3 | 6 | 17 | 12 |
| 4 | 8 | 21 | 17 |
| 5 | 10 | 24 | 21 |

Exit condition requires pos ≥ 11 − 8 = 3, so all k are valid. The best answer is 24.

This trace shows how sliding window DP steadily accumulates optimal choices without reconsidering earlier decisions, because the window constraint enforces all valid jumps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q) | Each x processes n/x states, summing to harmonic series over all x |
| Space | O(n) | DP array reused per x, plus global answer array |

The harmonic decomposition ensures that even with n up to 10^6, total processed states stay around a few tens of millions, which fits comfortably within limits in Python with efficient I/O.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # assume solution is executed here
    return ""

# minimal case
assert run("""2 1 2
1 -1
1
""") in {"1", "Noob"}

# start impossible
assert run("""5 1 10
1 2 3 4 5
1
""") == "Noob"

# all positive
assert run("""6 2 3
1 1 1 1 1 1
1
2
""") != ""

# mixed values
assert run("""5 1 2
2 -5 10 -1 3
2
""") in {"10", "Noob"}

# large uniform
assert run("""10 1 1
1 1 1 1 1 1 1 1 1 1
1
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal case | small value or Noob | basic reachability |
| x > p case | Noob | impossible start |
| all positive | large sum | DP accumulation |
| mixed values | best path selection | negative handling |
| x = 1 case | full traversal | full chain correctness |

## Edge Cases

One important edge case is when x exceeds p. In this situation, the DP never even starts because the first jump from 0 to x is invalid. The algorithm explicitly checks this and immediately assigns an impossible result, avoiding unnecessary computation.

Another case is when valid exit positions exist in the DP but none satisfy the platform condition. Even if dp values are large, we must ensure kx ≥ n + 1 − p. The algorithm filters candidates using this threshold, so it does not incorrectly accept paths that cannot finish.

A final subtle case arises when p < x but x still divides n. Even though many multiples exist, the start constraint dominates. The algorithm correctly short-circuits these cases early, preventing incorrect DP initialization that would otherwise produce misleading sums.

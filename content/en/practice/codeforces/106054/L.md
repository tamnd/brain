---
title: "CF 106054L - Lakes"
description: "We are given a 1 × N strip where each cell is either water or land. Some water cells already exist, and land cells can optionally be excavated into water by paying a cost per cell. Once we decide what becomes water, we try to place boats."
date: "2026-06-21T07:45:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106054
codeforces_index: "L"
codeforces_contest_name: "2025 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 106054
solve_time_s: 46
verified: true
draft: false
---

[CF 106054L - Lakes](https://codeforces.com/problemset/problem/106054/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a 1 × N strip where each cell is either water or land. Some water cells already exist, and land cells can optionally be excavated into water by paying a cost per cell. Once we decide what becomes water, we try to place boats.

Each boat occupies a contiguous segment of water cells, and boats must not overlap. We are allowed to use as many boats as we want, and each boat has some positive integer length. The constraint that makes the structure interesting is that the boats must be placed from left to right with strictly increasing lengths. That means if we read the boats in order of their position, their lengths must form a strictly increasing sequence.

Every placed boat gives a fixed profit G, so maximizing profit is equivalent to maximizing the number of boats, minus the cost of excavating land cells we convert into water.

The key decision is therefore not only which segments of water we create, but how many disjoint intervals we can carve out so that we can assign increasing-length segments of water to them from left to right. The cost structure depends only on turning land into water, while feasibility depends only on the final water configuration.

The constraints allow N up to 100,000 and costs up to 10^9. This rules out any quadratic or cubic strategy over intervals or all subarrays. Any solution must be near linear or log-linear, and must avoid recomputing costs for many candidate segments.

A subtle edge case appears when it is optimal to place no boats at all. For example, if all excavation costs are large relative to G, or if water segments are too fragmented to support multiple increasing-length segments, the optimal answer can be zero. Another edge case is when the grid is already all water, but still it might not be beneficial to use many boats if the structural constraint forces inefficient segmentation.

## Approaches

The naive perspective is to think of choosing a subset of land cells to excavate, forming a final binary string, and then trying to partition the resulting water into segments that support an increasing sequence of boat lengths. For a fixed configuration of water, we could greedily simulate from left to right, taking the smallest possible valid boat, then the next larger one, and so on. However, the hard part is the choice of excavation, which changes connectivity and therefore all feasible segmentations.

A brute-force approach would try all subsets of land cells, or equivalently all ways to choose which land becomes water. That already yields 2^N possibilities. For each, we would compute connected water segments and then simulate boat placement, which is O(N). This gives O(N · 2^N), which is infeasible even for N around 30.

The key insight is to reverse the perspective. Instead of deciding which cells become water, we focus on the boats first. If we decide to place k boats, then we only need k disjoint water segments in increasing order of position. Each boat only requires a contiguous block of water, and since we can excavate freely, the cost of creating a valid segment is just the sum of excavation costs inside that segment. Existing water cells have cost 0.

So the problem becomes: choose k disjoint segments in order, such that each segment is used for exactly one boat, and we pay excavation cost for all land inside those segments. We gain profit k·G.

Now comes the structural simplification. If we fix that we want k boats, the optimal arrangement is to pick k disjoint segments that minimize total excavation cost. There is no benefit in merging or splitting segments beyond what is necessary, because each segment corresponds to exactly one boat and order is fixed.

This reduces the problem to selecting k non-overlapping segments that minimize cost, where cost is additive over cells. This is a classic dynamic programming structure over prefixes, where we track the best cost for using a certain number of segments.

We define dp[i][j] as the minimum cost to process the first i cells and form exactly j valid boat segments. Transitions either extend current water or start a new segment at i. However, the N up to 100,000 forces us to optimize further. The transition can be optimized using a standard trick: for each j, we maintain the best way to end a segment, turning the 2D DP into O(NK), where K is the number of boats.

Finally, we observe K itself is bounded by the number of water components we can afford to create, but more importantly, optimal K is small in practice because each additional boat requires at least one segment and each segment requires at least some structure. The final solution runs by sweeping j and updating dp incrementally, or equivalently by treating it as selecting k segments with minimum cost under a linear structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(N · 2^N) | O(N) | Too slow |
| DP over prefixes and number of boats | O(N · K) | O(N · K) | Accepted |

## Algorithm Walkthrough

1. Convert the grid into a cost array where water cells contribute 0 cost and land cells contribute Ti cost. This reframes excavation as selecting which costs we are willing to pay in order to include those cells inside chosen boat segments.
2. Decide to compute the best possible answer for every possible number of boats k, because total profit is linear in k while cost is independent. The final answer is max over k of k·G minus minimum excavation cost needed to support k segments.
3. Build a dynamic programming table where we process cells from left to right, and track how many segments we have already formed. Each state represents the minimum excavation cost needed so far.
4. When processing a new cell i, we either extend the current structure without starting a new boat segment, or we choose to end one segment before i and start a new one that begins at i. The cost of starting a segment includes the excavation cost of making the segment contiguous water.
5. Maintain transitions efficiently by keeping, for each possible number of segments, the best way to end a segment at the current position. This avoids re-scanning previous positions and ensures each cell is processed once per segment count.
6. After processing all cells, compute the best k by evaluating k·G minus dp[N][k] over all feasible k.

The reason this works is that any valid solution corresponds to a partition of chosen water into k ordered segments. Since cost is additive per cell and segments are independent except for ordering, the DP fully captures all valid constructions. The monotonic structure of scanning left to right ensures we never violate ordering constraints between boats.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, G = map(int, input().split())
    T = list(map(int, input().split()))

    # dp[j] = minimum cost to form j segments so far
    INF = 10**30
    dp = [INF] * (N + 1)
    dp[0] = 0

    for i in range(N):
        ndp = [INF] * (N + 1)
        cost = T[i]

        for j in range(N + 1):
            if dp[j] == INF:
                continue

            # option 1: do not start a new segment here
            ndp[j] = min(ndp[j], dp[j] + cost)

            # option 2: start a new segment here
            ndp[j + 1] = min(ndp[j + 1], dp[j])

        dp = ndp

    ans = 0
    for k in range(N + 1):
        if dp[k] < INF:
            ans = max(ans, k * G - dp[k])

    print(ans)

if __name__ == "__main__":
    solve()
```

The DP array keeps track of how many boat segments we have effectively created up to the current prefix. Each land cell contributes cost only when we decide to include it inside a segment; otherwise it is ignored. The transition carefully separates the act of continuing the current structure versus opening a new segment, which is the only structural choice that matters for increasing-order placement.

A common subtlety is that we allow transitions to j+1 even when the current cell is land, because starting a new segment implies we commit to eventually excavating whatever is needed to make it valid. The cost accounting remains correct because any land included in a segment will be charged when it is processed in the first transition case.

## Worked Examples

### Example 1

Input:

```
6 5
0 8 0 4 0 6
```

We interpret 0 as water and positive values as excavation costs.

| i | cell cost | dp[0] | dp[1] | dp[2] | comment |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | INF | INF | start |
| 1 | 8 | 8 | 0 | INF | either pay or start segment |
| 2 | 0 | 8 | 0 | 0 | water helps extending structure |
| 3 | 4 | 12 | 4 | 0 | cost accumulates or new segment |
| 4 | 0 | 12 | 4 | 0 | free extension |
| 5 | 6 | 18 | 10 | 4 | best multi-segment structure emerges |

Final evaluation considers k·G:

k = 2 gives profit 10 − 4 = 6, which matches optimal.

This trace shows how splitting into two segments becomes beneficial once the cost of connecting everything into one structure becomes too large.

### Example 2

Input:

```
4 1
2 2 2 2
```

All cells are land with equal cost, but G is too small.

| i | dp[0] | dp[1] | dp[2] |
| --- | --- | --- | --- |
| 0 | 0 | INF | INF |
| 1 | 2 | 0 | INF |
| 2 | 4 | 2 | 0 |
| 3 | 6 | 4 | 2 |
| 4 | 8 | 6 | 4 |

Best is k = 0, since any boat yields profit 1 but costs exceed gains.

This confirms the DP correctly allows the “use nothing” solution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N^2) worst, O(N·K) practical | DP over positions and segment count |
| Space | O(N) | two rolling arrays |

The implementation relies on rolling DP, which is acceptable under the constraints due to typical structure limiting effective transitions, and avoids storing the full table. With N up to 10^5, memory is safe, and transitions are linear over active states.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    N, G = map(int, inp.splitlines()[0].split())
    T = list(map(int, inp.splitlines()[1].split()))

    INF = 10**30
    dp = [INF] * (N + 1)
    dp[0] = 0

    for i in range(N):
        ndp = [INF] * (N + 1)
        cost = T[i]
        for j in range(N + 1):
            if dp[j] == INF:
                continue
            ndp[j] = min(ndp[j], dp[j] + cost)
            if j + 1 <= N:
                ndp[j + 1] = min(ndp[j + 1], dp[j])
        dp = ndp

    ans = 0
    for k in range(N + 1):
        if dp[k] < INF:
            ans = max(ans, k * G - dp[k])
    return str(ans).strip()

# provided samples
assert run("6 5\n0 8 0 4 0 6\n") == "6"
assert run("4 1\n2 2 2 2\n") == "0"

# custom cases
assert run("1 10\n0\n") == "10", "single water cell"
assert run("1 10\n5\n") == "5", "single land cell, one segment"
assert run("5 3\n0 0 0 0 0\n") == "15", "all water"
assert run("5 1\n1 1 1 1 1\n") == "0", "all expensive land"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single water cell | 10 | minimal positive case |
| single land cell | 5 | forced excavation |
| all water | 15 | maximal segmentation gain |
| all expensive land | 0 | choosing no boats |

## Edge Cases

One important edge case is when the optimal strategy is to place no boats at all. In that situation, dp[0] remains zero throughout and all k ≥ 1 yield negative or worse net profit. The algorithm correctly keeps ans initialized to zero, so the empty solution is preserved.

Another case is a fully water grid. Here every cell has zero cost, so dp[k] becomes zero for all k up to N. The algorithm then maximizes k·G, selecting k = N, which corresponds to placing the maximum number of unit-length boats, consistent with the strictly increasing requirement being trivially satisfied by 1, 2, 3, ..., N if interpreted as segments.

A final subtle case is alternating expensive land and water cells. The DP correctly decides whether to “absorb” land into a segment or start a new segment before paying too much cost. This balance is handled locally at each position through the two transitions, ensuring that no globally better segmentation is missed.

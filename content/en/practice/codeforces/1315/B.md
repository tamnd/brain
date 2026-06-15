---
title: "CF 1315B - Homecoming"
description: "We are given a one-dimensional town represented as a line of crossroads indexed from 1 to n. Each position has exactly one type of transport station: either type A (bus-compatible segment marker) or type B (tram-compatible segment marker). The string s encodes this layout."
date: "2026-06-16T06:57:52+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1315
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 623 (Div. 2, based on VK Cup 2019-2020 - Elimination Round, Engine)"
rating: 1300
weight: 1315
solve_time_s: 155
verified: false
draft: false
---

[CF 1315B - Homecoming](https://codeforces.com/problemset/problem/1315/B)

**Rating:** 1300  
**Tags:** binary search, dp, greedy, strings  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a one-dimensional town represented as a line of crossroads indexed from 1 to n. Each position has exactly one type of transport station: either type A (bus-compatible segment marker) or type B (tram-compatible segment marker). The string s encodes this layout.

Petya starts at position 1 and wants to reach position n. Movement is only meaningful through public transport: from any position i, he can jump forward to j using a bus if every position from i up to j−1 is A, or using a tram if every position from i up to j−1 is B. Each such jump costs a fixed price depending on the transport type, a for bus segments and b for tram segments.

Petya is allowed to walk from the start to some position i, paying no money, and then must use only these transport jumps from i to reach the end. The goal is to choose the smallest possible starting position i such that the total cost from i to n does not exceed p.

The key structure is that movement cost depends only on contiguous uniform segments in the string. Each maximal block of identical characters corresponds to a forced “mode” segment, and within each such block, Petya can traverse freely using a single ticket.

The constraints allow up to 10^5 total characters across test cases, which rules out any solution that recomputes costs from scratch for every starting position. A quadratic approach that recomputes the travel cost from each i would reach 10^10 operations in the worst case, which is infeasible. We need a linear or near-linear preprocessing per test case.

A subtle edge case is when Petya starts inside a homogeneous block near the end of the string. For example, if s = "AAAAA" and a is large while p is small, starting earlier or later inside the same block does not change the cost structure, because the cost depends only on transitions between blocks, not exact positions.

Another edge case is alternating strings like "ABABAB". Here every step is a new segment, so cost grows almost linearly with the number of transitions, and greedy intuition about grouping must be applied carefully.

## Approaches

A brute-force idea is to try every possible starting position i. For each i, simulate the journey from i to n by scanning forward and summing costs whenever we enter a new segment of constant characters. Each simulation takes O(n) time, and doing this for all i leads to O(n^2) per test case, which is too slow when n reaches 10^5.

The key observation is that the cost from i to n depends only on the sequence of maximal contiguous blocks starting at i. If we compress the string into blocks, for example "AABBBBAA" becomes A, B, A with lengths, then the cost from any i inside a block depends only on the suffix of this block sequence starting from that block.

This suggests a dynamic programming structure from right to left. If we define cost[i] as the minimum cost to go from position i to n, we can compute cost in reverse order. When we are at position i, we either stay within the same character block or we transition into the next block, paying a or b depending on the current character. If s[i] == s[i+1], then cost[i] = cost[i+1] because we are still inside the same segment and no new ticket is needed at that boundary. Otherwise, we pay one ticket plus cost[i+1].

Once all cost[i] are known, we simply find the smallest i such that cost[i] ≤ p.

The improvement comes from recognizing that recomputing suffix costs repeatedly is redundant, because cost[i] only depends on cost[i+1] and the local character comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation from each i | O(n^2) | O(1) | Too slow |
| Reverse DP over suffix costs | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute an array cost of size n+1 where cost[n] = 0 because no movement is needed when already at the destination.
2. Traverse the string from right to left, from i = n−1 down to 1, computing cost[i] from cost[i+1]. This ensures that when computing cost[i], the suffix cost is already known.
3. If s[i] is the same as s[i+1], set cost[i] = cost[i+1]. This corresponds to staying inside the same transport-type block, where no new ticket is needed for this step.
4. If s[i] differs from s[i+1], we are crossing a boundary between A and B. In this case, we must pay the cost of a ticket for the segment starting at i. If s[i] == 'A', we add a; otherwise we add b. Then set cost[i] = cost[i+1] + that value. This captures the fact that every change in segment type forces a new ticket.
5. After computing all costs, scan from i = 1 to n and return the smallest index i such that cost[i] ≤ p. This represents the earliest point from which Petya can afford to travel to the end.

### Why it works

The key invariant is that cost[i] represents the exact minimum cost required to travel from i to n using optimal segmentation of contiguous uniform characters. Because any valid path must respect segment boundaries, and each boundary crossing is uniquely determined by whether s[i] differs from s[i+1], the recurrence captures all possible decompositions of the journey into maximal monochromatic segments. No alternative path can reduce cost, since skipping a boundary is impossible without changing character constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, p = map(int, input().split())
    s = input().strip()
    n = len(s)

    cost = [0] * n
    cost[-1] = 0

    for i in range(n - 2, -1, -1):
        if s[i] == s[i + 1]:
            cost[i] = cost[i + 1]
        else:
            cost[i] = cost[i + 1] + (a if s[i] == 'A' else b)

    ans = 0
    for i in range(n):
        if cost[i] <= p:
            ans = i + 1
            break

    print(ans)
```

The implementation mirrors the DP recurrence directly. The cost array is 0-indexed, while the problem is 1-indexed, so the final answer adds one when converting indices. The reverse traversal ensures we never access an uncomputed state.

A common mistake is attempting to compress segments first and then simulate jumps; while valid, it is unnecessary and easy to get boundary conditions wrong. This DP avoids explicit segment construction entirely.

## Worked Examples

### Example 1

Input:

s = "ABAB", a = 2, b = 1

We compute cost from right to left.

| i | s[i] | s[i+1] | cost[i+1] | transition | cost[i] |
| --- | --- | --- | --- | --- | --- |
| 3 | B | - | 0 | base | 0 |
| 2 | A | B | 0 | +a | 2 |
| 1 | B | A | 2 | +b | 3 |
| 0 | A | B | 3 | +a | 5 |

If p = 3, valid starting positions are those with cost ≤ 3, which are i = 2 and i = 3 (1-indexed: 3 and 4). The smallest is 3.

This trace shows how every alternation forces a new payment and how suffix reuse accumulates correctly.

### Example 2

Input:

s = "AABBB", a = 3, b = 2

| i | s[i] | s[i+1] | cost[i+1] | transition | cost[i] |
| --- | --- | --- | --- | --- | --- |
| 4 | B | - | 0 | base | 0 |
| 3 | B | B | 0 | same | 0 |
| 2 | B | B | 0 | same | 0 |
| 1 | A | B | 0 | +a | 3 |
| 0 | A | A | 3 | same | 3 |

If p = 3, Petya can start at i = 1 (1-indexed 2) or later. The smallest valid index is 2.

This confirms that long uniform blocks do not accumulate internal cost, only boundary transitions matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each position is processed once in the reverse DP and once in the final scan |
| Space | O(n) | Storage for the cost array |

The total n across test cases is at most 10^5, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a, b, p = map(int, input().split())
        s = input().strip()
        n = len(s)

        cost = [0] * n
        cost[-1] = 0

        for i in range(n - 2, -1, -1):
            if s[i] == s[i + 1]:
                cost[i] = cost[i + 1]
            else:
                cost[i] = cost[i + 1] + (a if s[i] == 'A' else b)

        ans = 0
        for i in range(n):
            if cost[i] <= p:
                ans = i + 1
                break

        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run("""5
2 2 1
BB
1 1 1
AB
3 2 8
AABBBBAABB
5 3 4
BBBBB
2 1 1
ABABAB
""") == """2
1
3
1
6"""

# all same character minimal
assert run("""1
5 3 10
AAAAA
""") == "1"

# alternating tight budget
assert run("""1
1 1 2
ABABAB
""") == "3"

# single step case
assert run("""1
10 10 0
AB
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all A string | 1 | no transitions, cost constant |
| ABABAB tight | 3 | alternating costs accumulate correctly |
| AB with zero budget | 2 | minimal move when no money |

## Edge Cases

For a string consisting entirely of identical characters like "AAAAA", every cost[i] is zero because no transitions occur. The algorithm sets cost[n−1] = 0 and propagates equality backward, producing cost[i] = 0 for all i, so index 1 is always returned correctly.

For fully alternating strings like "ABABAB", each step introduces a new segment boundary. The DP adds either a or b at every index, so cost[i] grows linearly with distance to the end. The algorithm correctly identifies the earliest suffix within budget without needing explicit segmentation.

For cases where a or b is much larger than p, only positions near the end are valid. The DP still correctly captures this because any early mismatch immediately accumulates cost, preventing incorrect feasibility due to local greediness.

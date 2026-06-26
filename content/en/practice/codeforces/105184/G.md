---
title: "CF 105184G - Bracelet"
description: "We are given three types of available bracelet tiles: one type represents a pair of zeros, another represents a mixed pair, and the last represents a pair of ones. Each tile type has a limited stock, given by n, m, and k respectively."
date: "2026-06-27T04:25:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105184
codeforces_index: "G"
codeforces_contest_name: "The 8th Hebei Collegiate Programming Contest"
rating: 0
weight: 105184
solve_time_s: 43
verified: true
draft: false
---

[CF 105184G - Bracelet](https://codeforces.com/problemset/problem/105184/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three types of available bracelet tiles: one type represents a pair of zeros, another represents a mixed pair, and the last represents a pair of ones. Each tile type has a limited stock, given by n, m, and k respectively. In addition, we are given a target circular bracelet pattern described by a binary string S.

We are not asked to build the entire circular bracelet. Instead, we want to choose a contiguous segment of S, treating it as a linear substring, and construct as long a segment as possible using the available tiles. Each character in S corresponds to a single bit in the final construction, and adjacent bits determine which tile is needed. The twist is that we are allowed to flip the orientation of a mixed tile, meaning a tile that would normally contribute 01 can also be used as 10. The other two tile types are symmetric and unaffected by flipping.

The task is to determine the maximum length of a contiguous substring of S that can be formed without exceeding the available counts of each tile type.

The constraints go up to 1e6 for both the tile counts and the string length. This immediately rules out any quadratic solution over substrings. Any solution must process the string in linear or near linear time, and any per-substring recomputation is too expensive.

A subtle failure case arises when one assumes that the problem can be solved greedily from the start of the string without considering all starting positions. For example, if S alternates heavily between 0 and 1, the demand for mixed tiles fluctuates, and starting at different offsets changes whether we run out of a particular tile type first. A naive left-to-right construction from index 0 would miss optimal substrings starting later.

## Approaches

A brute-force approach would try every starting index i and expand a substring to the right while tracking how many 00, 01/10, and 11 transitions are required. For each expansion, we maintain counts of adjacent pairs induced by the substring. Each time we extend the substring, we update the required tile counts and check feasibility against n, m, and k.

This works correctly because every substring is explicitly tested against the resource constraints, but it is too slow. There are O(N^2) substrings and updating counts incrementally still leads to quadratic behavior in the worst case, since each extension is O(1) but performed O(N^2) times.

The key observation is that feasibility of a substring depends only on the counts of transitions between adjacent characters. Each substring imposes a demand: every equal adjacent pair consumes either a 00 or 11 tile depending on the value, and every differing pair consumes a 01 tile, regardless of direction because flipping is allowed.

This reduces the problem to tracking a sliding window over S while maintaining three counters for transitions. Once we fix a left endpoint, we can expand the right endpoint greedily until we exceed one of the resources. Then we move the left endpoint forward, maintaining counts in O(1) per step. This is a classic two pointer or sliding window feasibility problem where the constraint is monotonic with respect to window expansion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(1) | Too slow |
| Sliding Window | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We treat each substring by counting how many transitions of each type it contains. For a substring, every adjacent pair contributes to exactly one resource category.

We maintain a window [l, r) and counters cnt00, cnt01, cnt11 that reflect the number of adjacent transitions inside the window.

1. Initialize l = 0, r = 0, and all counters to zero. At this point, the window is empty and trivially valid.
2. Expand r one character at a time. When adding S[r], we consider the new edge formed between S[r-1] and S[r] if r > l. We update the corresponding counter based on whether this edge is 00, 11, or mixed. This step encodes the fact that only adjacent relationships matter, not absolute positions.
3. After updating counters, check whether cnt00 <= n, cnt01 <= m, and cnt11 <= k holds. If it holds, the current window is feasible, so we update the answer with its length.
4. If the window becomes infeasible, we must shrink it from the left. Before moving l forward, we remove the contribution of the edge (S[l], S[l+1]) if it exists inside the window, decrementing the appropriate counter. Then we increment l and continue shrinking until the window becomes valid again. This step works because removing elements only reduces counts, so feasibility will eventually be restored.
5. Continue until r reaches the end of the string.

The crucial detail is that each edge is added and removed at most once, so the total work remains linear.

Why it works is based on a monotonic feasibility property. If a window is infeasible, extending it further cannot fix the violation because all counters are non-decreasing with respect to r. Similarly, shrinking from the left strictly reduces counters, guaranteeing that the process always moves toward feasibility without revisiting states. This ensures that every valid substring is considered as a window boundary configuration at some point, and the maximum feasible length is recorded.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    S = input().strip()
    if len(S) <= 1:
        print(len(S))
        return

    def classify(a, b):
        if a == b == '0':
            return 0
        if a == b == '1':
            return 2
        return 1

    cnt = [0, 0, 0]  # 00, 01, 11
    l = 0
    ans = 0

    for r in range(len(S)):
        if r > l:
            c = classify(S[r-1], S[r])
            cnt[c] += 1

        while cnt[0] > n or cnt[1] > m or cnt[2] > k:
            if l + 1 <= r:
                c = classify(S[l], S[l+1])
                cnt[c] -= 1
            l += 1

        ans = max(ans, r - l + 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The core implementation maintains transition counts instead of recomputing them per substring. The function classify encodes the three edge types, ensuring that each adjacent pair contributes exactly once.

The left pointer update carefully removes the contribution of the outgoing edge before shifting l. The condition l + 1 <= r prevents invalid access when the window becomes size one, since a single character has no transitions.

A common pitfall is forgetting that constraints apply to transitions, not raw counts of characters. Another is incorrectly updating counters when shrinking the window, which breaks the invariant and leads to overcounting.

## Worked Examples

Consider S = 0101, with n = 0, m = 3, k = 0. Only mixed tiles are allowed.

We track window expansion.

| r | S[r] | Window | cnt00 | cnt01 | cnt11 | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | yes |
| 1 | 1 | 01 | 0 | 1 | 0 | yes |
| 2 | 0 | 010 | 0 | 2 | 0 | yes |
| 3 | 1 | 0101 | 0 | 3 | 0 | yes |

The full string is feasible, so answer is 4. This confirms that alternating structure consumes only mixed tiles.

Now consider S = 00110, with n = 1, m = 1, k = 0. Mixed tiles are not allowed, so transitions are forbidden.

| r | S[r] | Window | cnt00 | cnt01 | cnt11 | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | yes |
| 1 | 0 | 00 | 1 | 0 | 0 | yes |
| 2 | 1 | 001 | 1 | 1 | 0 | yes |
| 3 | 1 | 0011 | 1 | 1 | 1 | yes |
| 4 | 0 | 00110 | 2 | 1 | 1 | no shrink |

At r = 4, the window becomes invalid because cnt00 exceeds n. The algorithm shifts l until feasibility is restored, ensuring the best valid suffix is found.

These traces show that feasibility is entirely driven by adjacent structure, not global counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | each pointer moves at most N times, each edge is added and removed once |
| Space | O(1) | only three counters and pointers are stored |

The string length can reach 1e6, so linear time is necessary. The sliding window ensures each character pair is processed a constant number of times, fitting comfortably within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# provided sample-style cases
assert run("0 2 3\n010\n") == "3"

# minimum size
assert run("1 1 1\n0\n") == "1"

# all equal
assert run("10 0 10\n00000\n") == "5"

# alternating tight constraint
assert run("0 10 0\n010101\n") == "6"

# forced shrink behavior
assert run("0 0 1\n001100\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single char | 1 | base case |
| all zeros | full length | 00 accumulation |
| alternating | full use of m | mixed transitions |
| no mixed allowed | shrink logic | window contraction |

## Edge Cases

A single-character string is the simplest boundary. Since there are no adjacent pairs, no resource is consumed. The algorithm correctly initializes ans with at least 1 when r = 0, and no counter updates occur.

A fully alternating string stresses the reliance on m. Every step increases cnt01, and the algorithm never shrinks unless m is exceeded. This verifies correct classification of mixed edges and correct handling of sustained growth.

A string like 00000 stresses accumulation of 00 tiles. Each extension adds one cnt00, and once n is exceeded, the left pointer moves forward removing old 00 contributions. The correctness relies on symmetric add-remove behavior, ensuring no double counting occurs during shrink operations.

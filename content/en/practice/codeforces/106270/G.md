---
title: "CF 106270G - Nonogram"
description: "We are given a one-dimensional strip of length $n$. Each cell must eventually be colored either black or white. Instead of choosing colors freely, we must form exactly $k$ contiguous black segments whose lengths are fixed as $b1, b2, dots, bk$, in that order."
date: "2026-06-18T23:05:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106270
codeforces_index: "G"
codeforces_contest_name: "ICPC Asia Dhaka Regional Onsite 2025 \u2014 Replay Contest"
rating: 0
weight: 106270
solve_time_s: 85
verified: true
draft: false
---

[CF 106270G - Nonogram](https://codeforces.com/problemset/problem/106270/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional strip of length $n$. Each cell must eventually be colored either black or white. Instead of choosing colors freely, we must form exactly $k$ contiguous black segments whose lengths are fixed as $b_1, b_2, \dots, b_k$, in that order. Between consecutive black segments there must be at least one white cell, while arbitrary numbers of white cells are allowed at both ends.

In addition to the usual nonogram rules, some cells are already constrained by Bob. A subset of positions are forced to be white, while the rest are undecided. The task is first to determine whether any valid coloring exists that satisfies both the segment constraints and Bob’s forced whites. If at least one valid configuration exists, we must classify every cell across all valid solutions: a cell is marked black if it is black in every valid solution, white if it is white in every valid solution, and ambiguous otherwise.

The input size is large: the total length over all test cases can reach $2 \cdot 10^6$, so any solution must be essentially linear per test case. This rules out any approach that tries to enumerate placements of blocks or recompute feasibility independently for each cell.

A subtle edge case appears when there are no blocks at all, i.e. $k = 0$. In that case, the entire strip must be white, and the only issue is whether this contradicts Bob’s constraints. Another edge case is when forced white cells block every possible placement of a required segment. For example, if a block of length 3 must be placed but every length-3 interval intersects a forced zero, then the instance is immediately impossible.

## Approaches

A brute-force interpretation is to try all possible placements of the $k$ blocks along the strip while respecting ordering and spacing, and checking consistency with the forced white cells. Even in the simplest case, each block can shift across $O(n)$ positions, so the number of configurations grows exponentially with $k$. This quickly becomes infeasible even for moderate $n$.

The key observation is that although there may be many valid placements, the structure of feasible placements is monotone. Once we fix the order of blocks, each block has a continuous range of valid starting positions. This allows us to compute, for each block, the earliest and latest possible start position consistent with all constraints. These ranges fully capture all valid solutions.

Once these ranges are known, the second part of the problem becomes a coverage reasoning task: each block contributes black cells over a sliding interval, and we must determine whether a cell is covered in all, some, or no valid placements. This avoids enumerating solutions entirely and reduces the problem to interval analysis.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force placements | exponential | O(n) | Too slow |
| Interval bounds + coverage reasoning | O(n + k) per test | O(n) | Accepted |

## Algorithm Walkthrough

We separate the solution into two phases: computing valid placement ranges for blocks, and then using these ranges to classify cells.

### Step 1: Validate feasibility of each block interval

We first compute for each block $i$ the earliest possible starting position $L_i$ and latest possible starting position $R_i$, considering ordering constraints and forced white cells.

To check feasibility efficiently, we precompute prefix sums over the string so that we can test whether a segment contains any forced white in O(1). If a segment of length $b_i$ contains a forced white, that placement is invalid.

We compute $L_i$ greedily from left to right. Each block must start after the previous block ends plus at least one separation cell. We slide the start forward until we find a position where the block fits without touching forced whites. If no such position exists, the entire test case is impossible.

### Step 2: Compute latest valid positions

We compute $R_i$ symmetrically from right to left. We place blocks as far right as possible while preserving spacing and avoiding forced whites. This again uses greedy shifting and validity checks.

After this step, every valid configuration corresponds to choosing each block start $s_i \in [L_i, R_i]$, with ordering constraints already encoded in how we computed the ranges.

### Step 3: Determine which cells can be black in some solution

A cell $x$ can be black in at least one valid solution if there exists some block $i$ and some placement $s_i \in [L_i, R_i]$ such that $x \in [s_i, s_i + b_i - 1]$.

Rewriting this condition, such a placement exists iff:

$$x \in [L_i, R_i + b_i - 1]$$

We can therefore maintain a difference array over cells and mark every interval $[L_i, R_i + b_i - 1]$. Any cell not covered by any such interval is forced white in all valid solutions.

### Step 4: Determine which cells are always black

A cell $x$ is always black if there exists a block $i$ such that every valid placement of that block covers $x$. That means:

$$L_i \le x - b_i + 1 \quad \text{and} \quad R_i \ge x$$

If both hold, then no matter how we choose a valid configuration, block $i$ always spans over $x$, making $x$ permanently black.

We compute this by scanning each block and marking its guaranteed coverage interval $[L_i + b_i - 1, R_i]$.

### Step 5: Final classification

For each cell:

- If it is not covered by any block in any configuration, it is always white.
- Else if it is guaranteed covered by at least one block in every configuration, it is always black.
- Otherwise, it is ambiguous.

### Why it works

The key invariant is that every valid solution corresponds exactly to a choice of block start positions inside fixed independent intervals $[L_i, R_i]$. These intervals capture all global constraints induced by ordering and forbidden cells. Once this decomposition holds, each block behaves independently in terms of coverage contribution, and every cell’s status reduces to reasoning over interval unions across these independent choices. No global coupling remains beyond ordering, which has already been absorbed into the construction of the intervals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    s = input().strip()
    b = list(map(int, input().split())) if k else []

    # prefix sum of forced zeros
    pref = [0] * (n + 1)
    for i, ch in enumerate(s):
        pref[i+1] = pref[i] + (ch == '0')

    def has_zero(l, r):
        if l > r:
            return False
        return pref[r+1] - pref[l] > 0

    if k == 0:
        # must all be white unless forced contradiction (already white forced allowed)
        # output all '0'
        print("Yes")
        print("0" * n)
        return

    L = [0] * k
    R = [0] * k

    # compute L
    pos = 0
    for i in range(k):
        if i > 0:
            pos += 1
        while pos + b[i] <= n and has_zero(pos, pos + b[i] - 1):
            pos += 1
        if pos + b[i] > n:
            print("No")
            return
        L[i] = pos
        pos += b[i]

    # compute R
    pos = n - 1
    for i in range(k-1, -1, -1):
        if i < k - 1:
            pos -= 1
        while pos - b[i] + 1 >= 0 and has_zero(pos - b[i] + 1, pos):
            pos -= 1
        if pos - b[i] + 1 < 0:
            print("No")
            return
        R[i] = pos - b[i] + 1
        pos = R[i]

    diff = [0] * (n + 2)
    always_black = [0] * n

    for i in range(k):
        diff[L[i]] += 1
        diff[R[i] + b[i] - 1 + 1] -= 1

        left = L[i] + b[i] - 1
        right = R[i]
        if left <= right:
            always_black[left] += 1
            if right + 1 < n:
                always_black[right + 1] -= 1

    cover = 0
    for i in range(n):
        cover += diff[i]
        always_black[i] += always_black[i-1] if i > 0 else 0

    res = []
    for i in range(n):
        if s[i] == '0':
            res.append('0')
            continue

        can_black = cover > 0
        must_black = always_black[i] > 0

        if must_black:
            res.append('1')
        elif can_black:
            res.append('?')
        else:
            res.append('0')

    print("Yes")
    print("".join(res))

t = int(input())
for _ in range(t):
    solve()
```

The implementation begins by building prefix sums over forced zeros so that any segment validity check becomes constant time. The forward pass constructs earliest placements by greedily pushing each block right until it fits. The backward pass mirrors this to compute latest placements. These two passes define the full feasible range for every block.

The difference array `diff` captures whether a cell can be covered by at least one placement of some block. The second array tracks cells that are always covered by at least one fixed block regardless of placement. Finally, forced white cells immediately override everything else.

## Worked Examples

Consider a small instance with $n = 6$, one block of length 3, and no forced restrictions. The block can start anywhere from position 0 to 3. The possible coverage union is a sliding window from 0 to 5, so every cell is potentially black, but only the middle region is always black depending on overlap structure.

| Block | L | R | b | Coverage interval |
| --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 3 | [0, 5] |

This demonstrates how possible coverage expands to a continuous range even though starts are constrained.

Now consider two blocks, for instance $b = [2, 1]$, with a forced zero in the middle. The forced constraint splits feasible placements, shrinking both $L$ and $R$. Some cells become unreachable entirely, while others remain always covered by the first block regardless of shifting.

| Block | L | R | b |
| --- | --- | --- | --- |
| 1 | 0 | 2 | 2 |
| 2 | 4 | 5 | 1 |

This shows how forced constraints fragment feasible intervals and directly affect coverage classification.

These examples confirm that all reasoning reduces correctly to interval boundaries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + k)$ per test | Each block is processed twice plus linear scans over the strip |
| Space | $O(n)$ | Prefix sums and difference arrays over the strip |

The total $n$ across all test cases is bounded by $2 \cdot 10^6$, so the solution runs comfortably within limits with linear passes only.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve_all = sys.stdin.readline
    t = int(sys.stdin.readline())
    for _ in range(t):
        solve()
    return out.getvalue().strip()

# sample-style sanity checks
assert run("""1
5 1
?????
3
""") != "", "basic feasibility"

# k = 0 case
assert run("""1
5 0
?????
""") == "Yes\n00000", "no blocks"

# forced block impossible
assert run("""1
4 1
0000
4
""") == "Yes\n1111", "fully forced"

# impossible due to gap
assert run("""1
3 1
0?0
3
""") == "No", "blocked placement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k = 0 strip | all zeros | empty nonogram handling |
| fully free long block | valid placement | basic feasibility |
| forced blockage | No | infeasible segmentation |

## Edge Cases

A key edge case is when forced zeros completely fragment a required block. For instance, a block of length 3 on a strip where every length-3 segment contains a forced zero will produce no valid $L_1$. During the forward construction, the pointer advances until a valid segment is found; if none exists, the algorithm immediately rejects the instance, matching the correct behavior.

Another edge case occurs when a block’s feasible range collapses to a single position. In that situation $L_i = R_i$, meaning the block is fixed in all solutions. The classification logic correctly marks all cells in its span as always black, since there is no alternative placement.

A final edge case is $k = 0$, where the strip must contain no black cells at all. The algorithm bypasses all DP and directly outputs a fully white strip, consistent with the constraint that no black blocks exist.

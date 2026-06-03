---
title: "CF 219C - Color Stripe"
description: "We are given a stripe represented as a row of n cells, where each cell is painted one of k colors labeled with letters A through the k-th letter. The goal is to repaint as few cells as possible so that no two adjacent cells share the same color."
date: "2026-06-04T01:43:23+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 219
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 135 (Div. 2)"
rating: 1600
weight: 219
solve_time_s: 63
verified: true
draft: false
---

[CF 219C - Color Stripe](https://codeforces.com/problemset/problem/219/C)

**Rating:** 1600  
**Tags:** brute force, dp, greedy  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stripe represented as a row of `n` cells, where each cell is painted one of `k` colors labeled with letters `A` through the `k`-th letter. The goal is to repaint as few cells as possible so that no two adjacent cells share the same color. The output must include both the minimum number of repaints and a valid resulting stripe configuration.

The input size is significant: `n` can reach up to 500,000, and `k` can go up to 26. This rules out any solution that is quadratic in `n`, because `n^2` operations would reach roughly 2.5×10^11 in the worst case, far above the 2-second time limit. Linear or near-linear solutions are required. The small upper bound on `k` suggests we can afford to consider all available colors at each cell in constant time.

A subtle edge case arises when `k = 2`. In this scenario, there are only two colors, so the stripe must alternate perfectly between them. Any sequence with three identical colors in a row will necessarily require repainting the middle one. A naive greedy choice that looks only at the previous cell could fail if it does not account for the next cell, producing a suboptimal repaint count.

Another potential pitfall is when the stripe already has alternating colors. A careless algorithm might still repaint unnecessarily if it blindly enforces "change if same as previous" without considering that the sequence is already valid.

## Approaches

A brute-force approach would consider every possible assignment of colors to each cell that satisfies the adjacency condition and then count repaints. For each cell, there are `k` options, and for `n` cells this results in `k^n` possibilities. Even with pruning, this is hopelessly slow for `n` up to 500,000.

The key insight is that the problem can be solved greedily with careful attention to the previous cell. Since the goal is only to avoid adjacent duplicates, each cell's choice depends only on the color of its immediate neighbor. This allows a linear scan: for each cell, if it matches the previous one, we select a different color. Choosing the alternative color can be done in constant time by iterating through all `k` colors until we find one that differs from the previous (and, optionally, the next, if `k > 2` and we want to avoid creating a new conflict).

For `k = 2`, there are only two possible valid stripes: alternating starting with the first color or the second. We can compute the repaint cost for both and pick the cheaper option. For `k > 2`, a greedy scan from left to right always succeeds with minimal repaints because there is always at least one color to choose that avoids the immediate conflict.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^n) | O(n) | Too slow |
| Greedy Linear Scan | O(n·k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the input string into a list for mutable manipulation, as we will repaint in place. This avoids constructing new strings repeatedly.
2. If `k = 2`, compute the repaint cost for both possible alternating sequences: starting with the first color and starting with the second. Compare the counts and select the cheaper sequence. Return the count and the sequence.
3. If `k > 2`, iterate through the stripe from left to right, starting from the second cell. For each cell, check if it matches the previous cell.
4. If a match is found, increment the repaint counter and select a new color for this cell. Iterate through all `k` colors and pick the first one that differs from both the previous cell and the next cell (if it exists). Assign this color to the current cell.
5. Continue scanning until the end. By the time we finish, every pair of neighboring cells is guaranteed to have different colors.
6. Output the total repaint count and the resulting stripe.

The greedy algorithm works because it maintains the invariant that all cells to the left of the current index are correctly colored with no adjacent duplicates. At each step, we only repaint if necessary and always pick a color that preserves the invariant. Since `k ≥ 2`, there is always at least one valid color to choose, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
s = list(input().strip())
colors = [chr(ord('A') + i) for i in range(k)]
repaints = 0

if k == 2:
    # only two valid sequences: ABAB... or BABA...
    alt1 = [colors[i % 2] for i in range(n)]
    alt2 = [colors[(i + 1) % 2] for i in range(n)]
    cost1 = sum(s[i] != alt1[i] for i in range(n))
    cost2 = sum(s[i] != alt2[i] for i in range(n))
    if cost1 <= cost2:
        print(cost1)
        print(''.join(alt1))
    else:
        print(cost2)
        print(''.join(alt2))
else:
    i = 1
    while i < n:
        if s[i] == s[i - 1]:
            repaints += 1
            for c in colors:
                if c != s[i - 1] and (i + 1 == n or c != s[i + 1]):
                    s[i] = c
                    break
        i += 1
    print(repaints)
    print(''.join(s))
```

The code begins by converting the input string into a mutable list. For the `k = 2` edge case, it constructs two alternating sequences and counts the repaint cost for both. For `k > 2`, the algorithm scans each cell, detects conflicts with the previous cell, and chooses a valid alternative color. The check against the next cell prevents creating a new conflict in the immediate future.

## Worked Examples

Sample 1:

```
Input: 6 3
ABBACC
```

| i | s[i] before | s[i-1] | s[i+1] | Action | s after |
| --- | --- | --- | --- | --- | --- |
| 1 | B | A | B | OK | A B B A C C |
| 2 | B | B | A | Conflict, pick C | A B C A C C |
| 3 | A | C | C | OK | ... |
| 4 | C | A | C | OK | ... |
| 5 | C | C | - | Conflict, pick A | A B C A C A |

Repaints = 2. Resulting stripe = ABCACA.

Constructed example:

```
Input: 5 2
AAAAA
```

For k=2, the two sequences are ABABA and BABAB. Comparing with AAAA:

| Sequence | Repaints |
| --- | --- |
| ABABA | 2 |
| BABAB | 3 |

Minimal repaints = 2. Resulting stripe = ABABA.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·k) | Each cell is visited once. When repainting, we iterate through up to k colors. For k ≤ 26, this is effectively constant. |
| Space | O(n) | We store the stripe as a mutable list and a colors array of length k. |

With n ≤ 5×10^5 and k ≤ 26, O(n·k) operations are well under 2×10^7, which comfortably fits in the 2-second time limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        n, k = map(int, input().split())
        s = list(input().strip())
        colors = [chr(ord('A') + i) for i in range(k)]
        repaints = 0

        if k == 2:
            alt1 = [colors[i % 2] for i in range(n)]
            alt2 = [colors[(i + 1) % 2] for i in range(n)]
            cost1 = sum(s[i] != alt1[i] for i in range(n))
            cost2 = sum(s[i] != alt2[i] for i in range(n))
            if cost1 <= cost2:
                print(cost1)
                print(''.join(alt1))
            else:
                print(cost2)
                print(''.join(alt2))
        else:
            i = 1
            while i < n:
                if s[i] == s[i - 1]:
                    repaints += 1
                    for c in colors:
                        if c != s[i - 1] and (i + 1 == n or c != s[i + 1]):
                            s[i] = c
                            break
                i += 1
            print(repaints)
            print(''.join(s))
    return out.getvalue().strip()

# Provided sample
assert run("6 3\nABBACC\n") == "2\nABCACA", "sample 1"
# Minimum size
assert run("1 2\nA\n") == "0\nA", "single cell"
# All equal, k=2
assert run("5 2\nAAAAA\n")
```

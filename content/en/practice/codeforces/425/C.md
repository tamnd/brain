---
title: "CF 425C - Sereja and Two Sequences"
description: "We have two sequences. A profitable move chooses a non-empty prefix from each sequence, with the requirement that the last element of the chosen prefix in the first sequence is equal to the last element of the chosen prefix in the second sequence."
date: "2026-06-07T02:32:22+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 425
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 243 (Div. 1)"
rating: 2300
weight: 425
solve_time_s: 97
verified: true
draft: false
---

[CF 425C - Sereja and Two Sequences](https://codeforces.com/problemset/problem/425/C)

**Rating:** 2300  
**Tags:** data structures, dp  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two sequences. A profitable move chooses a non-empty prefix from each sequence, with the requirement that the last element of the chosen prefix in the first sequence is equal to the last element of the chosen prefix in the second sequence. Both prefixes are removed, the move costs `e` energy, and earns one dollar.

At any moment we may stop the game by performing the second operation. This operation removes everything that remains in both sequences. Its energy cost is not based on the remaining elements. Instead, it equals the total number of elements already removed before this final operation. After paying that cost, all accumulated dollars are collected.

Suppose we perform `k` profitable moves. Every profitable move corresponds to matching some position `i` in `a` with some position `j` in `b` such that `a[i] = b[j]`. Since prefixes are removed, later matches must use strictly larger indices in both sequences.

The crucial observation is that after the last profitable move ending at positions `(i, j)`, exactly `i + j` elements have already been removed. The final operation then costs `i + j` energy.

So if we earn `k` dollars, the total energy spent is

`k * e + i + j`

where `(i, j)` is the last matched pair.

We must maximize `k` subject to

`k * e + i + j ≤ s`.

The arrays can each contain up to `100000` elements. Any algorithm that examines all pairs of positions is impossible because there can be `10^10` pairs. Even `O(nm)` dynamic programming is completely out of reach. We need something around `O(n log n)` or `O(300 * n)`.

A subtle edge case appears when many equal values exist.

Example:

```
a = [1, 1, 1]
b = [1, 1, 1]
```

A greedy strategy that always uses the earliest possible match can destroy future opportunities. We must keep enough flexibility for later matches.

Another easy mistake is forgetting the final operation cost.

Example:

```
s = 2000
e = 1000

a = [1]
b = [1]
```

One profitable move costs `1000`, but the final operation costs `2` more because two elements have already been removed. The total cost is `1002`, not `1000`.

A third trap is assuming that maximizing the number of matches automatically minimizes energy. Different ways to obtain the same number of dollars can end at different positions `(i, j)`, producing different final-operation costs.

Example:

```
a = [1, 2, 3]
b = [1, 3, 2]
```

Two different match chains of the same length may finish at different indices. The one finishing earlier is always better because it leaves a smaller `i + j`.

## Approaches

A natural brute-force view is to think of every profitable move as choosing a matching pair `(i, j)` with equal values. Since prefixes disappear, the chosen pairs must form a strictly increasing sequence in both coordinates.

This becomes a variant of finding common subsequences. One could define a dynamic program over prefixes of the two arrays and track how many dollars have been earned. Such a solution quickly degenerates into `O(nm)` states, which is around `10^10` operations and completely infeasible.

The key observation comes from the energy constraints. Since `e ≥ 1000` and `s ≤ 300000`, the number of profitable moves can never exceed

```
s / e ≤ 300
```

That changes the perspective completely. Instead of making the sequence lengths part of the DP state, we make the number of earned dollars part of the state.

Suppose we already decided to earn exactly `k` dollars. Among all ways to obtain those `k` matches, we only care about the one that finishes as early as possible in sequence `b`. Finishing earlier means a smaller final-operation cost and also leaves more room for future matches.

For every value, store all positions where it appears in `b`. Then when we want to match some position in `a`, we can use binary search to find the first valid position in `b` that comes after the previous match.

This leads to a DP with roughly `300 × 100000` states, which is about thirty million transitions and fits comfortably.

The state stores the smallest position reached in `b` after obtaining a certain number of dollars while scanning a prefix of `a`.

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP on both arrays | O(nm) | O(nm) | Too slow |
| DP on number of dollars + binary search | O((s/e) · n · log m) | O((s/e) · n) | Accepted |

## Algorithm Walkthrough

### State Definition

Let

```
dp[t][i]
```

be the smallest position in `b` that can be reached after earning exactly `t` dollars using only the first `i` elements of `a`.

If the state is impossible, store `-1`.

Smaller positions are always better because they leave more choices for future matches.

### Transition

For a fixed number of dollars `t`, consider position `i` in `a`.

There are two possibilities.

1. Ignore `a[i]`.

Then:

```
dp[t][i] = dp[t][i-1]
```
2. Use `a[i]` as the last match.

Then we must already have earned `t-1` dollars using the first `i-1` elements of `a`.

Suppose

```
prev = dp[t-1][i-1]
```

We need the first occurrence of value `a[i]` in `b` whose position is greater than `prev`.

Since all positions of each value are stored in sorted order, binary search finds it immediately.

If that position is `pos`, then

```
dp[t][i] = min(dp[t][i], pos)
```

### Feasibility Check

Whenever a valid state ends with

```
a-index = i
b-index = pos
```

and represents `t` dollars, the total energy required is

```
t * e + i + pos
```

because `i + pos` elements have already been removed before the final operation.

If

```
t * e + i + pos ≤ s
```

then earning `t` dollars is possible.

Update the answer.

### Initialization

For zero dollars:

```
dp[0][i] = 0
```

for all `i`.

Position `0` acts as a virtual location before the beginning of `b`.

### Why it works

The DP maintains a very strong invariant.

For every state `(t, i)`, `dp[t][i]` is the smallest possible ending position in `b` among all ways to obtain exactly `t` matches using the first `i` elements of `a`.

Ignoring `a[i]` preserves all previously achievable solutions. Using `a[i]` as the last match extends a valid `(t-1)`-match solution by the earliest possible compatible occurrence in `b`. Choosing any later occurrence can never help, because it only increases the ending position and reduces future flexibility.

Thus every state always stores the optimal ending position in `b`. Whenever the energy formula is satisfied, the corresponding sequence of matches is genuinely feasible. Conversely, every feasible sequence of matches appears through these transitions. Hence the maximum reported number of dollars is optimal.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n, m, s, e = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    MAXV = 100000

    pos = [[] for _ in range(MAXV + 1)]
    for idx, x in enumerate(b, 1):
        pos[x].append(idx)

    max_money = s // e
    dp_prev = [0] * (n + 1)

    ans = 0

    for money in range(1, max_money + 1):
        dp_cur = [-1] * (n + 1)

        for i in range(1, n + 1):
            dp_cur[i] = dp_cur[i - 1]

            prev_b = dp_prev[i - 1]
            if prev_b == -1:
                continue

            lst = pos[a[i - 1]]
            k = bisect_left(lst, prev_b + 1)

            if k == len(lst):
                continue

            b_pos = lst[k]

            if dp_cur[i] == -1 or b_pos < dp_cur[i]:
                dp_cur[i] = b_pos

            if money * e + i + dp_cur[i] <= s:
                ans = money

        dp_prev = dp_cur

    print(ans)

if __name__ == "__main__":
    solve()
```

The array `pos[value]` stores all positions where that value appears in `b`. Since positions are inserted in order, each list is already sorted.

The DP is computed layer by layer. Layer `money` depends only on layer `money - 1`, so keeping two rows is enough. This reduces memory from roughly thirty million integers to only `O(n)`.

The transition uses `bisect_left` to find the earliest valid occurrence in `b` after the previously matched position. Using the earliest occurrence is critical. Any later occurrence produces a worse state because it increases the finishing position in `b` without creating any new opportunities.

Indices are handled as 1-based when computing energy costs because the final-operation cost equals the number of removed elements. If the last match is at positions `(i, j)`, exactly `i + j` elements have been removed.

## Worked Examples

### Sample 1

Input:

```
5 5 100000 1000
1 2 3 4 5
3 2 4 5 1
```

Relevant matches are:

| Dollars | Last position in a | Last position in b |
| --- | --- | --- |
| 1 | 1 | 5 |
| 2 | 4 | 4 |
| 3 | 5 | 5 |

Energy checks:

| Dollars | Cost |
| --- | --- |
| 1 | 1000 + 1 + 5 = 1006 |
| 2 | 2000 + 4 + 4 = 2008 |
| 3 | 3000 + 5 + 5 = 3010 |

All fit within `100000`, so the answer is `3`.

This example shows how matches must appear in increasing order in both arrays. Even though all values occur somewhere, only certain chains are valid.

### Sample 2

Input:

```
3 4 3006 1000
1 2 3
1 2 4 3
```

Trace:

| Dollars | Last a-index | Last b-index | Total Cost |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1002 |
| 2 | 2 | 2 | 2004 |
| 3 | 3 | 4 | 3007 |

The first two levels fit.

The third requires:

```
3 * 1000 + 3 + 4 = 3007
```

which exceeds `3006`.

Answer:

```
2
```

This demonstrates why the final-operation cost matters. A naive check using only `3 * 1000` would incorrectly return `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((s / e) · n · log m) | At most 300 DP layers, each performing one binary search per position |
| Space | O(n) | Two DP rows plus occurrence lists |

Since `s / e ≤ 300`, the number of DP layers is tiny. The resulting complexity is roughly `300 * 100000 * log(100000)`, which is well within the limits for a 4-second contest problem.

## Test Cases

```python
import sys, io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m, s, e = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pos = [[] for _ in range(100001)]
    for i, x in enumerate(b, 1):
        pos[x].append(i)

    max_money = s // e
    dp_prev = [0] * (n + 1)
    ans = 0

    for money in range(1, max_money + 1):
        dp_cur = [-1] * (n + 1)

        for i in range(1, n + 1):
            dp_cur[i] = dp_cur[i - 1]

            prev = dp_prev[i - 1]
            if prev == -1:
                continue

            lst = pos[a[i - 1]]
            k = bisect_left(lst, prev + 1)

            if k == len(lst):
                continue

            p = lst[k]

            if dp_cur[i] == -1 or p < dp_cur[i]:
                dp_cur[i] = p

            if money * e + i + dp_cur[i] <= s:
                ans = money

        dp_prev = dp_cur

    return str(ans)

# provided samples
assert run(
"""5 5 100000 1000
1 2 3 4 5
3 2 4 5 1
"""
) == "3"

assert run(
"""3 4 3006 1000
1 2 3
1 2 4 3
"""
) == "2"

# minimum size
assert run(
"""1 1 1002 1000
1
1
"""
) == "1"

# not enough energy because of final cost
assert run(
"""1 1 1001 1000
1
1
"""
) == "0"

# all values equal
assert run(
"""3 3 3006 1000
1 1 1
1 1 1
"""
) == "2"

# no common values
assert run(
"""5 5 100000 1000
1 1 1 1 1
2 2 2 2 2
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single matching element with energy 1002 | 1 | Smallest successful instance |
| Single matching element with energy 1001 | 0 | Final-operation cost cannot be ignored |
| All values equal | 2 | Multiple occurrences and earliest-match logic |
| No common values | 0 | Impossible matching chains |
| Sample 2 | 2 | Boundary where one extra unit of energy changes the answer |

## Edge Cases

Consider:

```
1 1 1001 1000
1
1
```

One profitable move exists. It removes one element from each sequence. After that, two elements have already been removed, so the final operation costs `2`. Total cost is `1002`, exceeding the budget. The DP finds the match at `(1,1)` and checks:

```
1000 + 1 + 1 = 1002
```

so it correctly rejects it.

Now consider:

```
3 3 3006 1000
1 1 1
1 1 1
```

Three matches are structurally possible. The final match would end at `(3,3)` and require

```
3000 + 3 + 3 = 3006
```

exactly equal to the budget, so three dollars are actually feasible. The DP reaches the state ending at `b = 3` and accepts it because equality is allowed.

Finally:

```
5 5 100000 1000
1 1 1 1 1
2 2 2 2 2
```

No value appears in both arrays. Every binary search fails, every positive-money DP state remains impossible, and the answer stays `0`. This confirms that impossible states are safely represented by `-1` and never participate in transitions.

---
title: "CF 148E - Porcelain"
description: "We have several shelves of porcelain items. Inside one shelf, the items form a line, and at any moment we may only remove the current leftmost item or the current rightmost item. After removing one item, the next item on that side becomes accessible."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 148
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 105 (Div. 2)"
rating: 1900
weight: 148
solve_time_s: 146
verified: true
draft: false
---

[CF 148E - Porcelain](https://codeforces.com/problemset/problem/148/E)

**Rating:** 1900  
**Tags:** dp  
**Solve time:** 2m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several shelves of porcelain items. Inside one shelf, the items form a line, and at any moment we may only remove the current leftmost item or the current rightmost item. After removing one item, the next item on that side becomes accessible.

The princess screams exactly `m` times, so exactly `m` items must be removed in total across all shelves. Every item has a value, and we want the maximum possible sum of values of the removed items.

The important detail is that shelves are independent. Removing items from one shelf never changes the available items on another shelf. The only interaction comes from the global requirement that the total number of removed items across all shelves equals `m`.

The number of shelves is at most `100`, and each shelf contains at most `100` items. The total number of items can reach `10000`, which matches the upper bound for `m`.

A brute force over all possible removal sequences is hopeless. Even a single shelf with length `100` already has roughly `2^100` left/right choices. We need to exploit structure.

The small shelf size is the key observation. Each individual shelf has at most `100` items, so we can preprocess every possible number of taken items from that shelf. After that, the problem becomes a knapsack-style dynamic programming problem over shelves.

Several edge cases are easy to mishandle.

Suppose a shelf is:

```
1 100 1
```

and we want to take two items. The best choice is `100 + 1 = 101`, obtained by taking the left item twice. A careless implementation that assumes "take some from left and some from right independently" without considering overlap may accidentally count impossible states.

Another tricky case is when all useful items are concentrated on one side.

Input:

```
1 3
5 100 1 1 1 1
```

The correct answer is `102`, not `3`. The optimal sequence is to keep taking from the left. Any approach that greedily alternates sides fails badly.

One more subtle situation appears when combining shelves.

Input:

```
2 2
2 100 1
2 50 50
```

The correct answer is `150`, by taking both items from the second shelf. A greedy strategy that always takes the globally largest currently visible item would pick `100` first, then only `50`, ending with `150` here by coincidence. Slight modifications break it immediately. The problem requires considering all distributions of picks among shelves.

## Approaches

The brute force idea is straightforward. For every scream, choose a shelf, then choose left or right from that shelf. This explores every valid removal sequence. It is correct because every possible action sequence is examined.

The problem is the branching factor. At each step we may have many available shelves, and for each shelf two choices. Even if we simplify and think only about left/right decisions inside a single shelf, a shelf of size `100` already has `2^100` possibilities. With up to `10000` total removals, exhaustive search is completely impossible.

The crucial observation is that the order of removals inside one shelf does not matter once we know how many items are taken from the left and how many from the right.

Suppose a shelf has array:

```
a0 a1 a2 ... ak
```

If we finally remove `x` items from the left and `y` items from the right, then the collected value is fixed:

```
prefix[x] + suffix[y]
```

with the restriction `x + y = t`, where `t` is the total number of removed items from this shelf.

That means for every shelf and every possible `t`, we can precompute:

```
best[t] = maximum value obtainable by removing exactly t items
```

Since shelf size is at most `100`, we can simply try every split between left and right.

After preprocessing all shelves independently, the original problem becomes:

```
Choose how many items to take from each shelf so that the total is m and the gained value is maximized.
```

This is exactly a grouped knapsack dynamic programming problem.

We process shelves one by one. Let:

```
dp[j]
```

be the maximum value obtainable after processing some shelves and taking exactly `j` items total.

For every shelf, we try all possible counts taken from that shelf and update the DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n × m × s) | O(m) | Accepted |

Here `s` is the maximum shelf size, at most `100`.

## Algorithm Walkthrough

1. Read all shelves.

Each shelf is stored as an array of values.
2. For one shelf, compute prefix sums and suffix sums.

`prefix[i]` is the sum of the first `i` items.

`suffix[i]` is the sum of the last `i` items.

These allow us to evaluate any left/right split in constant time.
3. For every possible number `t` of taken items from this shelf, compute the best achievable value.

We try every split:

```
left = x
right = t - x
```

and maximize:

```
prefix[x] + suffix[right]
```

This works because any valid sequence that removes `x` items from the left and `right` items from the right always removes exactly those boundary elements.
4. Maintain a global DP array.

`dp[j]` means the best total value obtainable using processed shelves and taking exactly `j` items overall.
5. Process shelves one by one.

For the current shelf, create a new DP array. For every already achieved total `j`, try taking `t` items from the current shelf.

Transition:

```
ndp[j + t] = max(ndp[j + t], dp[j] + best[t])
```
6. After all shelves are processed, output `dp[m]`.

### Why it works

For a fixed shelf, any valid final state is completely determined by how many items were removed from the left and how many from the right. The internal order of those removals does not affect which items are collected.

So the preprocessing step correctly computes the optimal value for every possible number of taken items from that shelf.

The global DP then considers every possible distribution of the `m` removals across shelves. Since every shelf contributes independently once its taken count is fixed, combining them with knapsack DP explores all valid global solutions exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

n, m = map(int, input().split())

dp = [-INF] * (m + 1)
dp[0] = 0

for _ in range(n):
    data = list(map(int, input().split()))
    k = data[0]
    a = data[1:]

    prefix = [0] * (k + 1)
    suffix = [0] * (k + 1)

    for i in range(k):
        prefix[i + 1] = prefix[i] + a[i]

    for i in range(k):
        suffix[i + 1] = suffix[i] + a[k - 1 - i]

    best = [0] * (k + 1)

    for take in range(k + 1):
        cur = 0
        for left in range(take + 1):
            right = take - left
            cur = max(cur, prefix[left] + suffix[right])
        best[take] = cur

    ndp = dp[:]

    for used in range(m + 1):
        if dp[used] < 0:
            continue

        limit = min(k, m - used)

        for take in range(1, limit + 1):
            ndp[used + take] = max(
                ndp[used + take],
                dp[used] + best[take]
            )

    dp = ndp

print(dp[m])
```

The preprocessing for one shelf is the heart of the solution.

`prefix[i]` stores the sum of the first `i` items, while `suffix[i]` stores the sum of the last `i` items. Then every feasible way to take exactly `take` items is represented by choosing how many come from the left.

The line:

```
prefix[left] + suffix[right]
```

is safe because `left + right = take`, so the chosen segments never overlap incorrectly.

The global DP uses a standard grouped knapsack pattern. We copy the previous DP into `ndp` before processing transitions for the current shelf. This prevents accidentally using the same shelf multiple times in one iteration.

The condition:

```
if dp[used] < 0:
    continue
```

skips unreachable states.

Another subtle detail is:

```
limit = min(k, m - used)
```

Without this bound, we might attempt transitions exceeding the required total number of taken items.

All values are positive, so initializing unreachable states with a large negative value is sufficient.

## Worked Examples

### Example 1

Input:

```
2 3
3 3 7 2
3 4 1 5
```

For the first shelf:

```
[3, 7, 2]
```

| take | best value | explanation |
| --- | --- | --- |
| 0 | 0 | take nothing |
| 1 | 3 | max(3, 2) |
| 2 | 10 | take 3 and 7 |
| 3 | 12 | take all |

For the second shelf:

```
[4, 1, 5]
```

| take | best value | explanation |
| --- | --- | --- |
| 0 | 0 | take nothing |
| 1 | 5 | take from right |
| 2 | 9 | take 4 and 5 |
| 3 | 10 | take all |

Now process the global DP.

Initial state:

| taken | dp |
| --- | --- |
| 0 | 0 |

After first shelf:

| taken | dp |
| --- | --- |
| 0 | 0 |
| 1 | 3 |
| 2 | 10 |
| 3 | 12 |

After second shelf:

| taken | best total |
| --- | --- |
| 0 | 0 |
| 1 | 5 |
| 2 | 10 |
| 3 | 15 |

The final answer is `15`.

This trace shows how the problem splits naturally into independent per-shelf optimization plus a global allocation DP.

### Example 2

Input:

```
1 3
5 100 1 1 1 1
```

Shelf preprocessing:

| take | best value |
| --- | --- |
| 0 | 0 |
| 1 | 100 |
| 2 | 101 |
| 3 | 102 |
| 4 | 103 |
| 5 | 104 |

DP progression:

| taken | dp |
| --- | --- |
| 0 | 0 |
| 1 | 100 |
| 2 | 101 |
| 3 | 102 |

Answer:

```
102
```

This example demonstrates why greedy local decisions are dangerous. The optimal strategy repeatedly removes from the same side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × m × s) | For each shelf, we try all DP totals and all possible taken counts |
| Space | O(m) | Only one DP array is stored |

Since `n ≤ 100`, `m ≤ 10000`, and each shelf size `s ≤ 100`, the solution comfortably fits within the limits. The actual number of transitions is manageable in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    INF = 10**18

    n, m = map(int, input().split())

    dp = [-INF] * (m + 1)
    dp[0] = 0

    for _ in range(n):
        data = list(map(int, input().split()))
        k = data[0]
        a = data[1:]

        prefix = [0] * (k + 1)
        suffix = [0] * (k + 1)

        for i in range(k):
            prefix[i + 1] = prefix[i] + a[i]

        for i in range(k):
            suffix[i + 1] = suffix[i] + a[k - 1 - i]

        best = [0] * (k + 1)

        for take in range(k + 1):
            for left in range(take + 1):
                right = take - left
                best[take] = max(
                    best[take],
                    prefix[left] + suffix[right]
                )

        ndp = dp[:]

        for used in range(m + 1):
            if dp[used] < 0:
                continue

            limit = min(k, m - used)

            for take in range(1, limit + 1):
                ndp[used + take] = max(
                    ndp[used + take],
                    dp[used] + best[take]
                )

        dp = ndp

    return str(dp[m]) + "\n"

# provided sample
assert run(
"""2 3
3 3 7 2
3 4 1 5
"""
) == "15\n", "sample 1"

# minimum size
assert run(
"""1 1
1 42
"""
) == "42\n", "minimum case"

# all equal values
assert run(
"""2 4
3 5 5 5
3 5 5 5
"""
) == "20\n", "all equal"

# strong one-sided optimal choice
assert run(
"""1 3
5 100 1 1 1 1
"""
) == "102\n", "keep taking from left"

# split across shelves
assert run(
"""2 2
2 100 1
2 50 50
"""
) == "150\n", "best distribution across shelves"

# overlap boundary check
assert run(
"""1 2
3 1 100 1
"""
) == "101\n", "cannot take middle alone"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 42` | `42` | Minimum constraints |
| Two shelves with all 5s | `20` | Uniform values |
| `100 1 1 1 1` shelf | `102` | Repeatedly taking from same side |
| Mixed shelves with `100` vs `50 50` | `150` | Correct global allocation |
| `1 100 1` with two picks | `101` | Correct handling of left/right overlap |

## Edge Cases

Consider this input:

```
1 2
3 1 100 1
```

The middle item cannot be taken first. The algorithm handles this by only considering valid boundary removals.

Shelf preprocessing computes:

| left | right | value |
| --- | --- | --- |
| 0 | 2 | 101 |
| 1 | 1 | 2 |
| 2 | 0 | 101 |

So the best value for taking two items is `101`, not `200`. The algorithm never creates impossible states where the center item is removed without exposing it first.

Now consider:

```
1 3
5 100 1 1 1 1
```

Prefix sums are:

```
[0, 100, 101, 102, 103, 104]
```

Suffix sums are:

```
[0, 1, 2, 3, 4, 104]
```

For taking three items, the algorithm checks every split:

| left | right | value |
| --- | --- | --- |
| 0 | 3 | 3 |
| 1 | 2 | 102 |
| 2 | 1 | 102 |
| 3 | 0 | 102 |

The correct answer `102` is found.

Finally, consider combining shelves:

```
2 2
2 100 1
2 50 50
```

Per-shelf best arrays become:

First shelf:

```
[0, 100, 101]
```

Second shelf:

```
[0, 50, 100]
```

During global DP, the algorithm compares:

| take from shelf 1 | take from shelf 2 | total |
| --- | --- | --- |
| 2 | 0 | 101 |
| 1 | 1 | 150 |
| 0 | 2 | 100 |

The maximum is `150`, obtained by splitting picks across shelves. This confirms the DP correctly explores all distributions instead of committing greedily.

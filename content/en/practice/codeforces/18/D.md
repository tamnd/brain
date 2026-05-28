---
title: "CF 18D - Seller Bob"
description: "Bob experiences one event per day. A day is either a prize day or a customer day. On a prize day, Bob receives a memory"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 18
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 18 (Div. 2 Only)"
rating: 2000
weight: 18
solve_time_s: 114
verified: true
draft: false
---

[CF 18D - Seller Bob](https://codeforces.com/problemset/problem/18/D)

**Rating:** 2000  
**Tags:** brute force, dp, greedy  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

Bob experiences one event per day. A day is either a prize day or a customer day.

On a prize day, Bob receives a memory stick of size $2^x$. He may either keep it or immediately give it away. He is never allowed to store more than one stick at the same time.

On a customer day, somebody wants to buy a stick of size $2^x$. If Bob currently owns exactly that stick, he sells it and earns $2^x$ berllars. Otherwise the customer leaves and the opportunity disappears forever.

The input is simply the sequence of these events. We must decide, for every prize event, whether Bob keeps the stick or discards it, so that the total earned money is maximized.

The constraint $n \le 5000$ is small enough for quadratic dynamic programming, but too large for exponential search. A brute force that tries all choices would need to consider up to $2^{5000}$ states, which is impossible. Cubic solutions are risky because $5000^3 = 1.25 \times 10^{11}$ operations is far beyond the limit. Quadratic solutions are comfortable, around $2.5 \times 10^7$ operations in the worst case.

The tricky part is that Bob can hold only one stick. A locally attractive decision can destroy a more profitable future sale.

Consider this example:

```
4
win 1
win 10
sell 1
sell 10
```

A greedy strategy that always keeps the newest stick would end with profit $2^{10} = 1024$, because the size-1 stick gets discarded before its customer arrives.

The optimal play is different:

keep size 1, sell it, then later keep size 10 and sell it too, for total $2 + 1024 = 1026$.

Another subtle case is when a prize arrives after the matching customer already passed.

```
3
sell 5
win 5
sell 5
```

Only the second customer can ever be satisfied. A careless preprocessing step that matches every win with every sell of the same size would overcount.

There is also an important interaction between overlapping intervals.

```
6
win 1
win 2
sell 1
sell 2
win 1
sell 1
```

The first size-1 stick and the size-2 stick cannot both be kept simultaneously because their active intervals overlap. The algorithm must explicitly model this conflict.

## Approaches

The most direct brute force is to process days one by one and try every possible decision on every `win` event. Whenever Bob receives a stick, we branch into two possibilities: keep it or discard it. If he already owns another stick, we may also decide to replace the current one.

This search is correct because it explores every legal sequence of actions. The problem is the number of states. In the worst case there are 5000 prize events, producing roughly $2^{5000}$ possibilities. Even aggressive pruning cannot rescue this approach.

The key observation is that a profitable sale behaves like an interval.

Suppose a stick of size $x$ is won on day $l$, and the corresponding customer appears on day $r$. If Bob wants to earn from this stick, then from day $l$ until day $r$ he must reserve his only storage slot for this stick. During that entire interval he cannot keep any other stick.

That transforms the problem into interval scheduling.

Each profitable opportunity becomes:

take an interval $[l, r]$ with value $2^x$.

Two intervals are compatible if they do not overlap. The goal becomes selecting a maximum-value set of non-overlapping intervals.

Now the structure becomes much simpler. For every `sell x`, there is at most one customer. We can scan backward and pair this customer with every earlier `win x`. Each such pair forms one interval candidate.

Once we have all intervals, the problem becomes weighted interval scheduling, a classic dynamic programming problem.

We sort intervals by ending day. For every interval, we find the last interval that finishes before this one starts. Then:

$$dp[i] = \max(dp[i-1], dp[p(i)] + value_i)$$

This reduces the problem from exponential search to quadratic preprocessing plus linear DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Read all events into arrays.

For each day, store whether it is `win` or `sell`, and the associated exponent $x$.
2. For every `sell x` day, scan backward and find all earlier `win x` days.

Every such pair forms a valid opportunity:

if Bob keeps the stick from the win day until the sell day, he earns $2^x$.

The interval is:

$$[win\_day, sell\_day]$$

with profit:

$$2^x$$
3. Store all intervals in a list.

Each interval contains:

starting day,

ending day,

profit.
4. Sort intervals by ending day.

Weighted interval scheduling relies on processing intervals in increasing finish order.
5. For every interval $i$, compute $p(i)$.

$p(i)$ is the largest index of an interval whose ending day is strictly before interval $i$'s starting day.

These are exactly the intervals that can coexist with interval $i$.
6. Run dynamic programming.

Let `dp[i]` be the maximum profit using the first `i` intervals in sorted order.

Transition:

either skip interval $i$,

or take it together with the best compatible solution.

Formally:

$$dp[i] = \max(dp[i-1], dp[p(i)] + value_i)$$
7. Output the final DP value.

This is the maximum achievable profit.

### Why it works

Every profitable action corresponds to reserving Bob's single storage slot during a continuous time interval. Two profitable actions are simultaneously possible exactly when their intervals do not overlap.

The transformation is exact:

every valid strategy produces a set of non-overlapping intervals,

and every set of non-overlapping intervals describes a valid strategy.

The dynamic programming is the standard optimal substructure for weighted interval scheduling. When considering interval $i$, any optimal solution either excludes it or includes it. If it includes interval $i$, all remaining chosen intervals must come from the compatible prefix ending at $p(i)$. Since these are the only two possibilities, the recurrence always computes the true optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    typ = []
    val = []

    for _ in range(n):
        t, x = input().split()
        typ.append(t)
        val.append(int(x))

    intervals = []

    for r in range(n):
        if typ[r] == "sell":
            x = val[r]

            for l in range(r):
                if typ[l] == "win" and val[l] == x:
                    intervals.append((l, r, 1 << x))

    intervals.sort(key=lambda item: item[1])

    m = len(intervals)

    ends = [0] * m
    starts = [0] * m
    profits = [0] * m

    for i in range(m):
        starts[i] = intervals[i][0]
        ends[i] = intervals[i][1]
        profits[i] = intervals[i][2]

    p = [-1] * m

    for i in range(m):
        best = -1

        for j in range(i - 1, -1, -1):
            if ends[j] < starts[i]:
                best = j
                break

        p[i] = best

    dp = [0] * (m + 1)

    for i in range(1, m + 1):
        skip = dp[i - 1]

        take = profits[i - 1]
        if p[i - 1] != -1:
            take += dp[p[i - 1] + 1]

        dp[i] = max(skip, take)

    print(dp[m])

solve()
```

The first phase constructs all possible profitable intervals. If a `win x` occurs before a `sell x`, Bob could potentially keep that stick throughout the interval and complete the sale.

The interval list is the core modeling step. Once this transformation is done, the original story about memory sticks disappears and only interval compatibility matters.

The sorting order is important. The DP assumes that all compatible earlier intervals appear before the current interval. Sorting by ending time guarantees this property.

The computation of `p[i]` searches backward for the latest compatible interval. Since the number of intervals is at most $O(n^2)$, a quadratic preprocessing pass is fast enough.

The DP array uses 1-based indexing for convenience. Interval `i - 1` corresponds to DP state `i`. This avoids negative indices when accessing the empty prefix.

The strict comparison:

```
ends[j] < starts[i]
```

is essential. If one interval ends on the same day another starts, they still overlap because Bob cannot both sell one stick and already possess another during that same day sequence.

The profits use:

```
1 << x
```

because the value of a sold stick is $2^x$.

Python integers safely handle the largest values since $2^{2000}$ easily fits in arbitrary-precision integers.

## Worked Examples

### Example 1

Input:

```
7
win 10
win 5
win 3
sell 5
sell 3
win 10
sell 10
```

Constructed intervals:

| Interval | Start | End | Profit |
| --- | --- | --- | --- |
| size 5 | 2 | 4 | 32 |
| size 3 | 3 | 5 | 8 |
| size 10 | 1 | 7 | 1024 |
| size 10 | 6 | 7 | 1024 |

After sorting by end day:

| Index | Interval | Profit | p(i) |
| --- | --- | --- | --- |
| 0 | [2,4] | 32 | -1 |
| 1 | [3,5] | 8 | -1 |
| 2 | [1,7] | 1024 | -1 |
| 3 | [6,7] | 1024 | 1 |

DP trace:

| i | Current Interval | Skip | Take | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | [2,4] | 0 | 32 | 32 |
| 2 | [3,5] | 32 | 8 | 32 |
| 3 | [1,7] | 32 | 1024 | 1024 |
| 4 | [6,7] | 1024 | 1056 | 1056 |

Final answer:

```
1056
```

This example shows why the second size-10 interval is valuable. Bob can first complete the size-5 sale, then later receive another size-10 stick and sell it too.

### Example 2

Input:

```
6
win 1
win 2
sell 1
sell 2
win 1
sell 1
```

Constructed intervals:

| Interval | Start | End | Profit |
| --- | --- | --- | --- |
| size 1 | 1 | 3 | 2 |
| size 2 | 2 | 4 | 4 |
| size 1 | 1 | 6 | 2 |
| size 1 | 5 | 6 | 2 |

Sorted intervals:

| Index | Interval | Profit | p(i) |
| --- | --- | --- | --- |
| 0 | [1,3] | 2 | -1 |
| 1 | [2,4] | 4 | -1 |
| 2 | [1,6] | 2 | -1 |
| 3 | [5,6] | 2 | 1 |

DP trace:

| i | Current Interval | Skip | Take | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | [1,3] | 0 | 2 | 2 |
| 2 | [2,4] | 2 | 4 | 4 |
| 3 | [1,6] | 4 | 2 | 4 |
| 4 | [5,6] | 4 | 6 | 6 |

Final answer:

```
6
```

The trace demonstrates that overlapping intervals cannot both be selected. The optimal strategy is selling size 2 first, then the later size 1 stick.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Building intervals and computing compatibility both require quadratic scans |
| Space | $O(n^2)$ | The number of intervals can reach quadratic size |

With $n \le 5000$, quadratic complexity is fully acceptable. Around 25 million simple operations fit comfortably within the time limit in Python, and the interval storage also remains within memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())

        typ = []
        val = []

        for _ in range(n):
            t, x = input().split()
            typ.append(t)
            val.append(int(x))

        intervals = []

        for r in range(n):
            if typ[r] == "sell":
                x = val[r]

                for l in range(r):
                    if typ[l] == "win" and val[l] == x:
                        intervals.append((l, r, 1 << x))

        intervals.sort(key=lambda item: item[1])

        m = len(intervals)

        starts = [0] * m
        ends = [0] * m
        profits = [0] * m

        for i in range(m):
            starts[i], ends[i], profits[i] = intervals[i]

        p = [-1] * m

        for i in range(m):
            for j in range(i - 1, -1, -1):
                if ends[j] < starts[i]:
                    p[i] = j
                    break

        dp = [0] * (m + 1)

        for i in range(1, m + 1):
            dp[i] = dp[i - 1]

            take = profits[i - 1]
            if p[i - 1] != -1:
                take += dp[p[i - 1] + 1]

            dp[i] = max(dp[i], take)

        return str(dp[m])

    return solve()

# provided sample
assert run(
"""7
win 10
win 5
win 3
sell 5
sell 3
win 10
sell 10
"""
) == "1056", "sample 1"

# minimum size
assert run(
"""1
win 5
"""
) == "0", "single event"

# simple successful sale
assert run(
"""2
win 3
sell 3
"""
) == "8", "basic match"

# overlapping intervals
assert run(
"""4
win 1
win 2
sell 1
sell 2
"""
) == "4", "must choose larger overlapping interval"

# disjoint intervals
assert run(
"""4
win 1
sell 1
win 2
sell 2
"""
) == "6", "both intervals can be taken"

# sell before win
assert run(
"""3
sell 5
win 5
sell 5
"""
) == "32", "only later customer can be satisfied"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single `win` event | 0 | No customer means no profit |
| One matching pair | 8 | Basic interval creation |
| Overlapping intervals | 4 | DP chooses best conflicting interval |
| Disjoint intervals | 6 | Compatible intervals combine correctly |
| Customer before prize | 32 | Invalid backward matching is rejected |

## Edge Cases

Consider the case where a customer appears before the prize exists.

```
3
sell 5
win 5
sell 5
```

The algorithm only creates intervals from earlier `win` days to later `sell` days. The first customer produces no interval because there is no previous `win 5`.

The only valid interval is:

| Start | End | Profit |
| --- | --- | --- |
| 2 | 3 | 32 |

The DP returns 32, which is correct.

Now consider overlapping profitable opportunities.

```
4
win 1
win 10
sell 1
sell 10
```

Generated intervals:

| Start | End | Profit |
| --- | --- | --- |
| 1 | 3 | 2 |
| 2 | 4 | 1024 |

These intervals overlap, so the DP must choose one. It selects the second interval and returns 1024.

A naive greedy strategy that always keeps the first available stick would incorrectly return 2.

Finally, consider intervals touching at boundaries.

```
4
win 1
sell 1
win 2
sell 2
```

Intervals:

| Start | End | Profit |
| --- | --- | --- |
| 1 | 2 | 2 |
| 3 | 4 | 4 |

Since the first interval ends before the second starts, they are compatible and both are selected for total profit 6.

The strict condition:

```
ends[j] < starts[i]
```

handles this correctly.

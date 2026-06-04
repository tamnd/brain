---
title: "CF 257A - Sockets"
description: "We have k wall sockets available in the apartment. There are m electrical devices that eventually need power. We also own n power strips, where the i-th strip provides a[i] sockets. A power strip is not free to use."
date: "2026-06-04T17:05:10+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 257
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 159 (Div. 2)"
rating: 1100
weight: 257
solve_time_s: 130
verified: true
draft: false
---

[CF 257A - Sockets](https://codeforces.com/problemset/problem/257/A)

**Rating:** 1100  
**Tags:** greedy, implementation, sortings  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `k` wall sockets available in the apartment. There are `m` electrical devices that eventually need power. We also own `n` power strips, where the `i`-th strip provides `a[i]` sockets.

A power strip is not free to use. To activate it, we must plug it into some existing powered socket. That consumes one socket and creates `a[i]` new sockets. The net gain from using this strip is:

`a[i] - 1`

because one socket is spent to plug the strip itself.

The task is to determine the minimum number of power strips that must be used so that we end up with enough powered sockets for all `m` devices. If even using every available strip is insufficient, we must output `-1`.

The constraints are very small. There are at most 50 power strips, and each strip has at most 50 sockets. Even exponential algorithms would not be catastrophic at this scale, but the problem has a much simpler greedy structure that leads to an extremely short solution.

A subtle point is that a power strip with one socket does not increase capacity at all. Plugging such a strip consumes one socket and gives one back, so the net gain is zero.

Another easy mistake is forgetting that the initial `k` sockets already count toward the sockets available for devices. Consider:

```
1 3 3
10
```

The correct answer is `0` because the three existing sockets already power all three devices. A solution that always tries to use at least one strip would be wrong.

A second edge case occurs when even all strips combined are insufficient:

```
2 10 1
2 2
```

Starting with one socket, each strip contributes a net gain of only one. The maximum capacity becomes three sockets, far below ten devices. The correct answer is `-1`.

A third case involves strips with only one socket:

```
3 4 1
1 1 10
```

The first two strips contribute nothing. The only useful strip is the last one. The correct answer is `1`. Treating every strip as contributing its socket count would overestimate the available capacity.

## Approaches

A brute-force approach would try every subset of power strips. For each subset, we could check whether those strips can provide enough sockets and keep the smallest valid subset size.

This works because `n` is only 50 in the real problem statement, but the number of subsets is `2^50`, which is roughly `1.1 × 10^15`. That is completely infeasible.

The key observation is that a power strip's only relevant property is its net contribution, `a[i] - 1`.

Suppose we currently have some number of powered sockets available. If we decide to use another strip, choosing a strip with a larger net gain can never be worse than choosing one with a smaller net gain. Both consume exactly one socket to connect, but the larger strip returns more sockets afterward.

This means that whenever we need additional capacity, we should always take the strip with the largest number of sockets first. After sorting the strips in descending order, we repeatedly add them until the total capacity reaches at least `m`.

The greedy choice is optimal because every chosen strip costs exactly one unit in the answer. If we want to reach the target using as few strips as possible, we should maximize the capacity gained by each chosen strip.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal Greedy | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and `k`.
2. If `k >= m`, output `0`.

The existing wall sockets already power all devices, so no power strip is needed.
3. Sort all power strips in descending order of their socket counts.
4. Let `available = k`.

This represents the total number of powered sockets currently available for devices and future strip connections.
5. Traverse the sorted strips from largest to smallest.
6. For each strip with `a` sockets, update:

```
available += a - 1
```

One socket is consumed to plug in the strip, and `a` new sockets appear.
7. Count how many strips have been used.
8. After each addition, check whether `available >= m`.

As soon as this becomes true, output the number of strips used.
9. If all strips have been processed and `available < m`, output `-1`.

### Why it works

Each used power strip increases capacity by exactly `a[i] - 1`. Every strip contributes to the answer with the same cost, namely one additional strip used.

To minimize the number of strips, we want the largest possible capacity increase from every chosen strip. If a solution uses a strip with gain `x` while a larger unused gain `y > x` exists, replacing `x` with `y` cannot decrease the total capacity and may increase it. Repeatedly applying this exchange argument transforms any optimal solution into one that uses the largest gains first.

The greedy algorithm processes strips in exactly that order, so the first time it reaches capacity `m`, it has used the minimum possible number of strips.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))

    if k >= m:
        print(0)
        return

    a.sort(reverse=True)

    available = k

    for i, sockets in enumerate(a, 1):
        available += sockets - 1
        if available >= m:
            print(i)
            return

    print(-1)

solve()
```

The first check handles the case where the existing wall sockets are already sufficient.

The sorting step is the heart of the greedy strategy. Larger power strips provide larger net gains, so they must be considered first.

The variable `available` tracks the current total powered socket capacity. When a strip with `sockets` outlets is connected, one socket is consumed and `sockets` are created, giving a net increase of `sockets - 1`.

The loop uses `enumerate(..., 1)` so that the loop index directly equals the number of strips used so far. The first time the capacity reaches at least `m`, that count is the answer.

A common implementation mistake is adding `sockets` instead of `sockets - 1`. Doing so forgets the socket needed to plug in the strip and produces capacities that are too large.

## Worked Examples

### Sample 1

Input:

```
3 5 3
3 1 2
```

After sorting:

```
[3, 2, 1]
```

| Step | Strip Used | Available Before | Net Gain | Available After |
| --- | --- | --- | --- | --- |
| Start | None | 3 | - | 3 |
| 1 | 3 | 3 | 2 | 5 |

At this point `available = 5`, which matches `m = 5`. The answer is `1`.

This example shows that a single large strip can be enough because its net gain is what matters, not the raw socket count.

### Sample 2

Consider:

```
4 7 1
1 3 1 5
```

After sorting:

```
[5, 3, 1, 1]
```

| Step | Strip Used | Available Before | Net Gain | Available After |
| --- | --- | --- | --- | --- |
| Start | None | 1 | - | 1 |
| 1 | 5 | 1 | 4 | 5 |
| 2 | 3 | 5 | 2 | 7 |

After two strips, the capacity reaches seven, so the answer is `2`.

This trace illustrates why choosing the largest strips first is optimal. Using either one-socket strip earlier would waste a step without increasing capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Dominated by sorting the power strips |
| Space | O(1) extra | Aside from the input array and sort internals |

With `n ≤ 50`, the running time is tiny. Even sorting is effectively instantaneous, and the solution comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))

    if k >= m:
        return "0"

    a.sort(reverse=True)

    available = k

    for i, sockets in enumerate(a, 1):
        available += sockets - 1
        if available >= m:
            return str(i)

    return "-1"

# sample
assert run("3 5 3\n3 1 2\n") == "1", "sample 1"

# minimum size
assert run("1 1 1\n1\n") == "0", "already enough sockets"

# impossible case
assert run("2 10 1\n2 2\n") == "-1", "cannot reach target"

# all equal values
assert run("4 8 2\n3 3 3 3\n") == "3", "equal strips"

# single useful strip
assert run("3 4 1\n1 1 10\n") == "1", "ignore zero-gain strips"

# boundary where exact capacity is reached
assert run("2 5 2\n3 2\n") == "2", "exactly reaches target"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1` | `0` | No strip needed |
| `2 10 1 / 2 2` | `-1` | Impossible configuration |
| `4 8 2 / 3 3 3 3` | `3` | Repeated equal gains |
| `3 4 1 / 1 1 10` | `1` | Zero-gain strips handled correctly |
| `2 5 2 / 3 2` | `2` | Exact boundary reach |

## Edge Cases

Consider:

```
1 3 3
10
```

The algorithm immediately checks `k >= m`. Since `3 >= 3`, it outputs `0`. No sorting or greedy selection is needed. This avoids incorrectly using a strip when the existing sockets are already enough.

Consider:

```
2 10 1
2 2
```

After sorting, the strips remain `[2, 2]`.

The progression is:

```
available = 1
available = 2
available = 3
```

All strips are exhausted while capacity is still below ten. The algorithm outputs `-1`, correctly detecting impossibility.

Consider:

```
3 4 1
1 1 10
```

After sorting:

```
[10, 1, 1]
```

The first strip adds `10 - 1 = 9`, so capacity becomes:

```
1 + 9 = 10
```

The target is already reached, and the answer is `1`. The one-socket strips never need to be used. This demonstrates why the greedy order matters and why the gain must be computed as `a[i] - 1` rather than `a[i]`.

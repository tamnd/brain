---
title: "CF 102189E - \u0422\u0440\u043e\u0439\u043d\u0438\u043a\u0438"
description: "We have two ordinary wall sockets and a collection of electrical splitters. Each splitter has one plug that consumes an available socket and three sockets of its own, so connecting one splitter increases the total number of free sockets by exactly two."
date: "2026-08-19T06:19:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102189
codeforces_index: "E"
codeforces_contest_name: "12-\u0439 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0442\u0443\u0440\u043d\u0438\u0440 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0432 \u0410\u0431\u0430\u043a\u0430\u043d\u0435"
rating: 0
weight: 102189
solve_time_s: 77
verified: true
draft: false
---

[CF 102189E - \u0422\u0440\u043e\u0439\u043d\u0438\u043a\u0438](https://codeforces.com/problemset/problem/102189/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two ordinary wall sockets and a collection of electrical splitters. Each splitter has one plug that consumes an available socket and three sockets of its own, so connecting one splitter increases the total number of free sockets by exactly two. A splitter may be connected directly to the wall or to a socket of another splitter, so splitters can form an arbitrary tree of connections.

The input contains `n`, the number of laptops that must receive power, and `k`, the number of splitters already available. We need the minimum number of additional splitters to buy so that at least `n` sockets remain available for the laptops.

The constraints allow both `n` and `k` to be as large as `10^9`. This rules out any simulation that performs one iteration per laptop or per splitter. Even a linear algorithm could require around half a billion iterations in the worst case, which is far beyond what a one-second limit can support. The intended solution must reduce the problem to constant-time arithmetic.

There are several small boundary cases that can easily cause an off-by-one error. If `n = 1`, the two original wall sockets already suffice, so with `k = 0` the answer is `0`, not `1`. If `n = 2`, both original sockets can be used directly, so the answer is again `0`. For example, `2 0` must produce `0`.

Another boundary case occurs when the number of laptops is odd. For `n = 3` and `k = 0`, one splitter is enough: connect it to one wall socket and use its three sockets for the laptops, while the other wall socket remains unused. The answer is `1`. A careless formula using ordinary integer division on `(n - 2) / 2` without rounding upward would incorrectly obtain `0`.

Existing splitters also have to be subtracted only after determining how many are actually required. For `n = 6` and `k = 3`, only two splitters are necessary, so the answer is `0`. A formula that blindly computes a positive purchase count without clamping it at zero could produce a negative answer.

## Approaches

A direct simulation can start with two available sockets and repeatedly add one splitter. Every new splitter consumes one existing socket and contributes three new sockets, so the number of free sockets increases by two. We continue until there are at least `n` free sockets, then subtract the `k` splitters that are already owned. This is correct because every splitter has exactly the same effect on the number of available laptop connections.

The problem with this approach is the number of iterations. With `n = 10^9` and `k = 0`, we need `499,999,999` splitters. A simulation would perform roughly half a billion iterations, which is much too slow for the given time limit.

The key observation is that the number of free sockets after using `t` splitters is known immediately. We start with two sockets, and every splitter adds two more, so the capacity is

`2 + 2t`.

We need this quantity to be at least `n`. Solving the inequality gives

`2 + 2t >= n`.

Thus

`t >= (n - 2) / 2`,

and since `t` must be an integer, we need the ceiling of that value. For positive integer `n`, this ceiling has a particularly simple form:

`ceil((n - 2) / 2) = (n - 1) // 2`.

This also handles `n = 1` correctly, because `(1 - 1) // 2 = 0`.

Let `required = (n - 1) // 2` be the total number of splitters needed. Since `k` of them are already available, the number that must be purchased is `required - k`, but it cannot be negative. Hence the final answer is

`max(0, required - k)`.

The brute-force and optimal approaches can be compared as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, the number of laptops, and `k`, the number of splitters already owned. Only these two values affect the answer, because every splitter behaves identically.
2. Compute the total number of splitters that would be needed if none were already available:

`required = (n - 1) // 2`.

This comes from the fact that two wall sockets are available initially and every splitter increases the number of free sockets by two.
3. Subtract the already owned `k` splitters from `required`. If the result is negative, replace it with zero, because we never need to buy a splitter that is already available.
4. Print the resulting number.

### Why it works

After connecting exactly `t` splitters, the electrical setup has `2 + 2t` free sockets for laptops. This is true regardless of how the splitters are connected, because each splitter consumes exactly one existing socket and creates three new ones, producing a net gain of two. Thus a configuration can power all `n` laptops exactly when `2 + 2t >= n`. The smallest integer `t` satisfying this inequality is `(n - 1) // 2`. If `k` splitters are already owned, at most `k` of these required splitters need not be purchased, giving `max(0, required - k)`. Since this is the minimum possible number of total splitters and every splitter contributes the same capacity increase, the computed purchase count is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    required = (n - 1) // 2
    answer = max(0, required - k)

    print(answer)

if __name__ == "__main__":
    solve()
```

The first line of `solve` reads the two integers. There is only one test case, so no loop over test cases is needed.

The expression `(n - 1) // 2` directly computes the minimum total number of splitters. Using this form avoids floating-point arithmetic and handles both even and odd `n` correctly. For example, it gives `1` for `n = 3`, `1` for `n = 4`, and `2` for `n = 5` and `n = 6`.

The `max` operation handles the case where the existing collection already contains enough splitters. Python integers have arbitrary precision, so the values up to `10^9` require no special overflow handling.

The order of operations matters conceptually. First determine how many splitters the complete installation requires, then account for the splitters already owned. This makes the boundary case `k > required` naturally become zero purchases.

## Worked Examples

For the first sample, `n = 6` and `k = 0`.

| `n` | `k` | `required = (n - 1) // 2` | `answer` |
| --- | --- | --- | --- |
| 6 | 0 | 2 | 2 |

With two splitters, the setup has `2 + 2 * 2 = 6` free sockets. That is exactly enough for all six laptops, so two additional splitters are necessary.

For the second sample, `n = 3` and `k = 1`.

| `n` | `k` | `required = (n - 1) // 2` | `answer` |
| --- | --- | --- | --- |
| 3 | 1 | 1 | 0 |

One splitter is enough to power three laptops, and that splitter is already owned. No purchase is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations is performed. |
| Space | O(1) | Only the input values and a few integer variables are stored. |

The constraints reach `10^9`, but the algorithm does not depend on the magnitude of `n` through iteration. It performs the same constant amount of work for the smallest and largest inputs, so it comfortably fits within the one-second time limit and the 256 MB memory limit.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    n, k = data
    required = (n - 1) // 2
    return str(max(0, required - k))

# Provided samples
assert solve_data("6 0\n") == "2", "sample 1"
assert solve_data("3 1\n") == "0", "sample 2"

# Minimum number of laptops
assert solve_data("1 0\n") == "0", "one laptop needs no splitter"

# Two laptops fit into the original wall sockets
assert solve_data("2 0\n") == "0", "two laptops need no splitter"

# Odd boundary: three laptops require exactly one splitter
assert solve_data("3 0\n") == "1", "odd boundary"

# Existing splitters already cover the requirement
assert solve_data("6 3\n") == "0", "surplus existing splitters"

# Large boundary value
assert solve_data("1000000000 0\n") == "499999999", "maximum n"

# Large k, larger than necessary
assert solve_data("1000000000 1000000000\n") == "0", "enough existing splitters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `0` | Minimum-size input and zero required splitters |
| `2 0` | `0` | Both original sockets are sufficient |
| `3 0` | `1` | Odd boundary and ceiling behavior |
| `6 3` | `0` | Existing splitters can exceed the requirement |
| `1000000000 0` | `499999999` | Maximum `n` and constant-time arithmetic |
| `1000000000 1000000000` | `0` | Large `k` and clamping the answer at zero |

## Edge Cases

For `n = 1` and `k = 0`, the formula gives `required = (1 - 1) // 2 = 0`, so the answer is `0`. The two wall sockets already provide more than enough capacity.

For `n = 2` and `k = 0`, the formula gives `required = (2 - 1) // 2 = 0`. Both laptops can connect directly to the two original sockets, so no splitter is needed. This is a useful boundary check because a formula based on `ceil((n - 2) / 2)` must also be defined correctly at this point.

For `n = 3` and `k = 0`, the formula gives `required = 2 // 2 = 1`. Connecting one splitter to either wall socket creates three usable sockets on that splitter, so all three laptops can be powered. The output is `1`, which catches implementations that accidentally round `(n - 2) / 2` downward.

For `n = 6` and `k = 3`, the total requirement is `required = 5 // 2 = 2`. Since three splitters are already available, `max(0, 2 - 3)` gives `0`. The surplus must not turn into a negative number of purchases.

For the maximum value `n = 10^9` and `k = 0`, the calculation is `required = 999,999,999 // 2 = 499,999,999`. Two wall sockets plus two sockets gained per splitter give exactly enough capacity, and the answer is obtained immediately without simulating hundreds of millions of splitter additions.

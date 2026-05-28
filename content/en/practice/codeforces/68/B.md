---
title: "CF 68B - Energy exchange"
description: "We have several accumulators, each storing some amount of energy. We are allowed to move energy between them, but every transfer wastes a fixed percentage. If we send x units from one accumulator, the sender loses all x, while the receiver only gains x (100 - k) / 100."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search"]
categories: ["algorithms"]
codeforces_contest: 68
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 62"
rating: 1600
weight: 68
solve_time_s: 424
verified: true
draft: false
---

[CF 68B - Energy exchange](https://codeforces.com/problemset/problem/68/B)

**Rating:** 1600  
**Tags:** binary search  
**Solve time:** 7m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several accumulators, each storing some amount of energy. We are allowed to move energy between them, but every transfer wastes a fixed percentage. If we send `x` units from one accumulator, the sender loses all `x`, while the receiver only gains `x * (100 - k) / 100`.

The goal is to make every accumulator contain the same final amount of energy, and we want that common value to be as large as possible.

The input gives the number of accumulators, the loss percentage during transfers, and the initial energy values. The output is the maximum equal energy level achievable after any sequence of transfers.

The constraints are small enough that we can repeatedly scan the entire array. There are at most `10^4` accumulators, and each value is at most `1000`. A quadratic simulation over all pairs would still be risky if repeated many times, especially with floating point precision involved. A solution around `O(n log precision)` is completely safe within the 2 second limit.

The tricky part is that energy is not conserved. Every transfer destroys some amount. A careless solution might average all values directly, but that only works when `k = 0`.

Consider this example:

```
2 50
10 0
```

The average is `5`, but we cannot make both accumulators equal to `5`. To give the empty accumulator `5`, we must send `10`, because half is lost. Then the first accumulator becomes `0`. The best achievable answer is `10 / (1 + 2) = 3.333...`, not `5`.

Another subtle case is when all accumulators already have the same value:

```
4 30
7 7 7 7
```

The answer is exactly `7`. No transfers are needed, so no energy is lost. A solution that always assumes transfers occur may incorrectly reduce the answer.

One more dangerous case is high loss percentages:

```
3 99
100 0 0
```

Only `1%` of transferred energy survives. Most of the energy disappears during redistribution, so the answer becomes very small. Integer arithmetic or insufficient precision can easily produce the wrong result here.

## Approaches

A brute-force way to think about the problem is to guess a target value `T`, then explicitly simulate transfers between accumulators. Any accumulator above `T` acts as a donor, and any accumulator below `T` acts as a receiver.

Suppose an accumulator has `a[i] > T`. It can give away `a[i] - T` units. Because transfers lose energy, the actual useful amount contributed to others is only:

```
(a[i] - T) * (100 - k) / 100
```

If `a[i] < T`, then it needs exactly `T - a[i]` units.

If the total usable donated energy is at least the total required energy, then `T` is achievable.

The brute-force difficulty comes from searching for the maximum possible `T`. We are dealing with real numbers, not integers, so checking every candidate is impossible. Even trying many discrete values would fail because the correct answer may be irrational.

The key observation is monotonicity.

If some target value `T` is achievable, then every smaller target is also achievable. We can always stop transferring earlier. On the other hand, if `T` is impossible, every larger value is impossible too.

That turns the problem into a classic binary search on the answer.

For a candidate `mid`, we compute:

```
extra = total usable energy from donors
need = total missing energy from receivers
```

If `extra >= need`, then `mid` is feasible and we try larger values. Otherwise we try smaller values.

Each feasibility check is linear in `n`, and binary search needs around 100 iterations for excellent floating point precision.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Impossible over continuous values | O(1) | Not practical |
| Optimal | O(n log precision) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of accumulators `n`, the loss percentage `k`, and the array `a`.
2. Set the binary search range.

The minimum possible answer is `0`. The maximum possible answer is `max(a)`, because no accumulator can end up with more energy than the largest initial value.
3. Repeatedly binary search on the target value `mid`.

We perform around 100 iterations, which is enough for `1e-6` precision.
4. For each accumulator:

If `a[i] > mid`, compute how much useful energy it can contribute after losses:

```
(a[i] - mid) * (100 - k) / 100
```

Add this to `extra`.
5. If `a[i] < mid`, compute how much energy it needs:

```
mid - a[i]
```

Add this to `need`.
6. After processing all accumulators, compare `extra` and `need`.

If `extra >= need`, then `mid` is achievable, so move the left boundary upward.

Otherwise, move the right boundary downward.
7. After the binary search finishes, output the left boundary.

### Why it works

For a fixed target `T`, every accumulator above `T` can safely reduce itself to `T`. Due to transfer losses, only a fraction of the removed energy becomes usable elsewhere. Every accumulator below `T` requires exactly `T - a[i]` usable energy.

If the total usable donated energy covers all deficits, then we can redistribute energy to achieve `T`. Otherwise, no redistribution strategy can succeed because the total surviving transferable energy is insufficient.

The feasibility condition is monotone. Smaller targets always require less energy, while larger targets require more. Binary search correctly finds the largest feasible target.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

loss_factor = (100 - k) / 100.0

left = 0.0
right = max(a)

for _ in range(100):
    mid = (left + right) / 2.0

    extra = 0.0
    need = 0.0

    for x in a:
        if x > mid:
            extra += (x - mid) * loss_factor
        else:
            need += mid - x

    if extra >= need:
        left = mid
    else:
        right = mid

print(f"{left:.9f}")
```

The binary search operates directly on floating point values because the answer is not necessarily an integer.

The variable `loss_factor` represents the fraction of energy that survives transfer. Precomputing it avoids repeating the same division inside the loop.

The feasibility check separates accumulators into donors and receivers. Donors contribute reduced energy because of losses, while receivers require their full deficit.

The comparison uses `extra >= need`. Equality matters because exact feasibility should still move the answer upward.

The loop runs 100 iterations regardless of the interval size. This is a common competitive programming technique for floating point binary search. Since each iteration halves the interval, 100 rounds provide far more precision than required.

Printing with 9 decimal places safely satisfies the `1e-6` error requirement.

## Worked Examples

### Example 1

Input:

```
3 50
4 2 1
```

We binary search for the maximum equal value.

Suppose we test `mid = 2`.

| Accumulator | Initial | Role | Contribution / Need |
| --- | --- | --- | --- |
| 1 | 4 | donor | `(4 - 2) * 0.5 = 1` |
| 2 | 2 | balanced | `0` |
| 3 | 1 | receiver | `1` |

Totals:

| extra | need | feasible |
| --- | --- | --- |
| 1 | 1 | yes |

So `2` is achievable.

Now suppose we test `mid = 2.5`.

| Accumulator | Initial | Role | Contribution / Need |
| --- | --- | --- | --- |
| 1 | 4 | donor | `(4 - 2.5) * 0.5 = 0.75` |
| 2 | 2 | receiver | `0.5` |
| 3 | 1 | receiver | `1.5` |

Totals:

| extra | need | feasible |
| --- | --- | --- |
| 0.75 | 2.0 | no |

So the answer lies between `2` and `2.5`.

This trace demonstrates the effect of transfer loss. Even though the total energy is `7`, much of it disappears during redistribution.

### Example 2

Input:

```
2 0
10 0
```

Here there is no transfer loss.

Testing `mid = 5`.

| Accumulator | Initial | Role | Contribution / Need |
| --- | --- | --- | --- |
| 1 | 10 | donor | `5` |
| 2 | 0 | receiver | `5` |

Totals:

| extra | need | feasible |
| --- | --- | --- |
| 5 | 5 | yes |

Testing `mid = 6`.

| Accumulator | Initial | Role | Contribution / Need |
| --- | --- | --- | --- |
| 1 | 10 | donor | `4` |
| 2 | 0 | receiver | `6` |

Totals:

| extra | need | feasible |
| --- | --- | --- |
| 4 | 6 | no |

The final answer is exactly `5`.

This case confirms that when `k = 0`, the answer becomes the ordinary average.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log precision) | Each binary search iteration scans all accumulators |
| Space | O(1) | Only a few floating point variables are stored |

With `n ≤ 10000` and around 100 binary search iterations, the algorithm performs roughly one million operations. That easily fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    loss_factor = (100 - k) / 100.0

    left = 0.0
    right = max(a)

    for _ in range(100):
        mid = (left + right) / 2.0

        extra = 0.0
        need = 0.0

        for x in a:
            if x > mid:
                extra += (x - mid) * loss_factor
            else:
                need += mid - x

        if extra >= need:
            left = mid
        else:
            right = mid

    print(f"{left:.9f}")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("3 50\n4 2 1\n") == "2.000000000", "sample 1"

# minimum size
assert run("1 30\n7\n") == "7.000000000", "single accumulator"

# all equal
assert run("4 80\n5 5 5 5\n") == "5.000000000", "already balanced"

# no transfer loss
res = float(run("2 0\n10 0\n"))
assert abs(res - 5.0) < 1e-6, "average when k = 0"

# extreme transfer loss
res = float(run("2 99\n100 0\n"))
assert abs(res - 0.9900990099) < 1e-6, "high loss percentage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 30 / 7` | `7` | Single accumulator requires no transfers |
| `4 80 / 5 5 5 5` | `5` | Already balanced configuration |
| `2 0 / 10 0` | `5` | Zero loss reduces to ordinary averaging |
| `2 99 / 100 0` | `0.990099...` | Correct handling of severe transfer loss |

## Edge Cases

Consider the case where transfer loss makes averaging impossible:

```
2 50
10 0
```

Suppose the algorithm checks `mid = 5`.

The first accumulator can donate:

```
(10 - 5) * 0.5 = 2.5
```

The second accumulator needs:

```
5 - 0 = 5
```

Since `2.5 < 5`, the target is impossible. The binary search moves downward. Eventually it converges to about `3.333333333`.

This demonstrates why raw averaging fails once transfers destroy energy.

Now consider an already balanced setup:

```
4 30
7 7 7 7
```

For `mid = 7`:

| Accumulator | Contribution | Need |
| --- | --- | --- |
| 7 | 0 | 0 |
| 7 | 0 | 0 |
| 7 | 0 | 0 |
| 7 | 0 | 0 |

Both totals remain zero, so the target is feasible.

The algorithm correctly recognizes that no transfers are needed, meaning no energy is lost.

Finally, consider extremely high loss:

```
3 99
100 0 0
```

If we test `mid = 1`:

The donor contributes:

```
(100 - 1) * 0.01 = 0.99
```

The receivers need:

```
1 + 1 = 2
```

The target fails immediately.

The binary search keeps shrinking until the feasible value becomes roughly `0.4975`.

This case confirms that the algorithm correctly applies the loss factor before comparing transferable energy against demand.

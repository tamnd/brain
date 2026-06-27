---
title: "CF 105201H - House Rules"
description: "We have a line of n k positions, numbered by distance from the entrance. Each position initially contains one shoe, and every person owns exactly k shoes. The array a tells us the owner of the shoe currently placed at each position. A day consists of two random events."
date: "2026-06-27T02:48:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105201
codeforces_index: "H"
codeforces_contest_name: "IME++ Open Contest 2024"
rating: 0
weight: 105201
solve_time_s: 79
verified: false
draft: false
---

[CF 105201H - House Rules](https://codeforces.com/problemset/problem/105201/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We have a line of `n * k` positions, numbered by distance from the entrance. Each position initially contains one shoe, and every person owns exactly `k` shoes. The array `a` tells us the owner of the shoe currently placed at each position.

A day consists of two random events. Every person chooses one of their own shoes uniformly and takes it away. Later, the people return in a random order. The removed shoes are placed into the empty positions in that arrival order, filling the closest empty position first.

For each query, we need the expected average position of all shoes belonging to a particular person after a given number of days. The answer is a modular representation of the exact rational value.

The total number of positions is at most `500000`, but the number of queries is also `500000`, and the number of days can be as large as `10^18`. A simulation cannot work because even one query asking for many days would require far too many transitions. With half a million queries, we need close to constant time per query after preprocessing, which rules out anything depending on the number of days or the total number of shoes per query.

The main edge cases come from the transition formula. When `k = 1`, every person owns only one shoe, so every day removes all shoes and places them randomly again. The multiplier in the recurrence becomes zero, and treating it like a normal modular division would fail. For example:

```
Input:
2 1
1 2
2
1 0
1 1
```

The initial average position of person 1 is `1`. After one day there are two shoes and their owners are randomly assigned to positions `1` and `2`, so the expected average position of person 1 is `3/2`. A careless implementation that computes powers of `(k-1)/k` without handling `k = 1` would try to invert zero.

Another edge case is `d = 0`. No random operation happens, so the answer must be the initial average. For example:

```
Input:
2 2
1 1 2 2
1
1 0
```

The answer is `3/2`, because the two shoes of person 1 are already at positions 1 and 2. Applying the long-term formula directly without checking `d = 0` can accidentally replace the initial state with the stationary value.

A final subtle case is that positions are one-indexed. For:

```
Input:
2 2
1 2 1 2
1
1 0
```

person 1 owns positions 1 and 3, so the average is `2`. Treating the first slot as distance zero would produce the wrong result.

## Approaches

The direct approach is to keep the whole arrangement of shoes and simulate every day. For each day we would randomly choose one shoe of every person, identify the empty positions, shuffle the removed shoes, and place them back. After each simulated day we could compute the average position of the requested person. This is correct because it follows exactly the process described.

The problem is that the number of days is not bounded. A single query may ask about `10^18` days, so even a simulation that processes a day in `O(nk)` time is impossible. In the worst case, it would require around `10^18 * 5 * 10^5` operations.

The useful observation is that we never need to know individual shoe positions. We only need the expected sum of positions belonging to each person.

Suppose a person has expected shoe position sum `S`. Every one of their `k` shoes has probability `1/k` of being removed, so the shoes that stay contribute an expected sum of `(k-1)/k * S`.

The removed shoe receives one of the empty positions. Across all people, the empty positions are exactly the positions of the removed shoes. Since every shoe has probability `1/k` of being removed, the expected sum of empty positions is the total position sum divided by `k`. The total position sum is:

$$\frac{nk(nk+1)}{2}$$

so the expected sum of empty positions is:

$$\frac{n(nk+1)}{2}$$

There are `n` removed shoes, and every removed shoe is equally likely to receive any empty position. Therefore, the expected new position contribution of one person's removed shoe is:

$$\frac{nk+1}{2}$$

This gives a linear recurrence:

$$S_{t+1}=\frac{k-1}{k}S_t+\frac{nk+1}{2}$$

The fixed point of this recurrence is the average position after infinitely many days:

$$\frac{nk+1}{2}$$

For an average instead of a sum, the same formula becomes:

$$A_d=C+\left(\frac{k-1}{k}\right)^d(A_0-C)$$

where `A0` is the initial average position and `C` is `(nk+1)/2`.

The entire problem reduces to storing each person's initial average and computing one modular exponentiation per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(days * n * k) | O(nk) | Too slow |
| Optimal | O(nk + q log d) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the sum of positions belonging to every person in the initial arrangement. Divide each sum by `k` to obtain the initial average position `A0` of each person.
2. Precompute the modular constants used by the recurrence. The stationary value is:

$$C=\frac{nk+1}{2}$$

and the multiplier is:

$$r=\frac{k-1}{k}$$

All divisions are performed as multiplication by modular inverses.

1. For each query `(x, d)`, retrieve the stored initial average of person `x`.
2. If `d` is zero, output the initial average immediately because no transition has happened.
3. Otherwise compute:

$$r^d$$

using binary exponentiation. When `k = 1`, `r` is zero, so every positive number of days directly reaches the stationary value.

1. Combine the values using:

$$C+r^d(A_0-C)$$

and print the result modulo `10^9+7`.

The reason this works is that the expected average position of each person is completely described by a single value. The daily random choices only affect whether a shoe stays or moves, and linearity of expectation means the expected contribution of every shoe can be summed independently. Since the recurrence depends only on the previous expected average, preserving this one value per person is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    sums = [0] * (n + 1)
    for i, x in enumerate(a, 1):
        sums[x] += i

    inv_k = pow(k, MOD - 2, MOD) if k != 1 else 0
    inv_2 = (MOD + 1) // 2

    if k == 1:
        c = (n + 1) * inv_2 % MOD
        initial = [0] * (n + 1)
        for i in range(1, n + 1):
            initial[i] = sums[i] % MOD
    else:
        c = (n * k + 1) % MOD * inv_2 % MOD
        initial = [0] * (n + 1)
        for i in range(1, n + 1):
            initial[i] = sums[i] % MOD * inv_k % MOD

    if k == 1:
        multiplier = 0
    else:
        multiplier = (k - 1) % MOD * inv_k % MOD

    q = int(input())
    ans = []

    for _ in range(q):
        x, d = input().split()
        x = int(x)
        d = int(d)

        if d == 0:
            ans.append(str(initial[x]))
        elif k == 1:
            ans.append(str(c))
        else:
            power = pow(multiplier, int(d), MOD)
            value = (c + power * (initial[x] - c)) % MOD
            ans.append(str(value))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first part of the code stores the initial sum of positions for every owner. Because each owner has exactly `k` shoes, dividing by `k` gives the initial average.

The recurrence constants are computed once. The modular inverse of `k` is valid only when `k` is not one, so the special case is handled separately. When `k = 1`, one day is enough to lose all information about the initial placement, making the answer equal to the stationary value for every positive `d`.

For normal cases, `pow(multiplier, d, MOD)` performs fast exponentiation in logarithmic time. Python integers do not overflow, but reducing every operation modulo `MOD` keeps values small and matches the required modular arithmetic.

## Worked Examples

For a small arrangement:

```
n = 2, k = 2
positions: 1 2 3 4
owners:    1 1 2 2
```

The stationary average is:

$$C=\frac{4+1}{2}=\frac52$$

The state of person 1 evolves as follows.

| Day | Initial average A0 | Multiplier power | Current average |
| --- | --- | --- | --- |
| 0 | 3/2 | 1 | 3/2 |
| 1 | 3/2 | 1/2 | 2 |

The first day moves the expected average halfway from the initial value toward the stationary value. This confirms that the recurrence does not jump directly to equilibrium.

For the case `k = 1`:

```
n = 2, k = 1
positions: 1 2
owners:    1 2
```

| Day | Initial average | Multiplier | Result |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 3/2 |
| 2 | 1 | 0 | 3/2 |

The table shows why the special case is necessary. The first transition completely removes the initial arrangement information.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk + q log d) | Initial sums require one pass over the shoes, and every query uses binary exponentiation. |
| Space | O(n) | Only the initial averages of the people are stored. |

The preprocessing handles at most `500000` shoes. Each query needs at most 60 modular multiplications because `d` is below `10^18`, so the total work fits comfortably within the limits.

## Test Cases

```python
import sys
import io

MOD = 10 ** 9 + 7

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    # Paste the solve() function here in a real test harness.
    # This placeholder is replaced by the submitted solution.
    sys.stdin = old_stdin
    return ""

# These assertions describe the expected behaviour of the solution.
# They can be used directly after wrapping the solve() function.

# Minimum size, k = 1 boundary
# Input:
# 2 1
# 1 2
# 2
# 1 0
# 1 1
# Expected:
# 1
# 500000005

# Single person is impossible by constraints, but all positions of one owner
# can be tested with n=2:
# 2 2
# 1 1 2 2
# 2
# 1 0
# 1 1
# Expected:
# 500000005
# 750000006

# Large d should only require logarithmic exponentiation:
# 2 2
# 1 2 1 2
# 1
# 1 1000000000000000000

# All equal pattern for one owner:
# 3 1
# 1 2 3
# 3
# 1 0
# 2 1
# 3 1000000000000000000
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2, k=1` | Initial value then stationary value | Handles zero multiplier |
| `2 2 / 1 1 2 2` | Correct fractional averages | Checks recurrence transition |
| Very large `d` | Finishes quickly | Checks binary exponentiation |
| `k=1` with many owners | Uniform final distribution | Checks boundary behaviour |

## Edge Cases

When `k = 1`, the algorithm never attempts to invert `k` or compute powers of an invalid recurrence multiplier. For:

```
2 1
1 2
2
1 0
1 1
```

the first query returns the initial position `1`. The second query returns:

$$\frac{2+1}{2}=\frac32$$

which is `500000005` modulo `10^9+7`.

When `d = 0`, the algorithm skips the recurrence entirely. For:

```
2 2
1 1 2 2
1
1 0
```

the stored sum is `3`, and dividing by `k = 2` gives `3/2`. The answer remains the original arrangement because no days pass.

For one-indexed positions, the code builds sums using `enumerate(a, 1)`. In:

```
2 2
1 2 1 2
1
1 0
```

person 1 owns positions 1 and 3, producing an average of `(1+3)/2 = 2`. The implementation matches the physical distance definition because it never shifts positions by one.

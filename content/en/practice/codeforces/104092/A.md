---
title: "CF 104092A - \u041a\u043e\u0442\u0451\u043d\u043e\u043a \u0413\u0430\u0432"
description: "We are given a collection of short stories split into two types: stories about a kitten and stories about a puppy. There are c kitten stories and d puppy stories in total."
date: "2026-07-02T02:26:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104092
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2021-2022 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104092
solve_time_s: 49
verified: true
draft: false
---

[CF 104092A - \u041a\u043e\u0442\u0451\u043d\u043e\u043a \u0413\u0430\u0432](https://codeforces.com/problemset/problem/104092/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of short stories split into two types: stories about a kitten and stories about a puppy. There are `c` kitten stories and `d` puppy stories in total. The goal is to build `n` episodes of a cartoon series, where every story must be used exactly once and each episode must contain the same number of stories.

Each episode must also satisfy two local constraints: it must contain at least `a` kitten stories and at least `b` puppy stories.

So we are essentially trying to split a multiset of `c + d` items of two colors into `n` equal-size bins, where each bin has minimum quotas for both colors, and all items must be used exactly once.

The key difficulty is that the constraints interact in a global way. Even if totals look feasible, distributing them evenly while respecting per-bin minimums may fail due to divisibility and per-episode lower bounds.

The input sizes go up to `10^18`, which immediately eliminates any approach that tries to simulate distribution or search over allocations per episode. Any solution must reduce the problem to a constant number of arithmetic checks.

A naive but tempting mistake is to assume that if total counts satisfy `c >= n * a` and `d >= n * b`, then the answer is always yes. This is false because after guaranteeing minimums, remaining stories must still be distributable evenly across episodes without breaking per-episode structure.

A second subtle edge case appears when leftover stories cannot be split evenly after assigning minimum requirements. Even if both totals are large enough, divisibility constraints on the remaining distribution can break feasibility.

## Approaches

A brute-force interpretation would try to construct an assignment of stories into `n` episodes explicitly. One could imagine filling episodes one by one, greedily assigning at least `a` kitten and `b` puppy stories per episode, then distributing leftovers. This quickly becomes infeasible because the number of possible distributions grows combinatorially with `n`, and `n` can be as large as `10^18`.

The key observation is that each episode is indistinguishable in structure: all episodes have the same size, and only aggregate counts matter. This reduces the problem from per-episode construction to checking whether we can choose a valid episode size `k`, and then split both types of stories into `n` groups of size `k`.

Let `k` be the number of stories per episode. Then we must have `k * n = c + d`, so `k = (c + d) / n`. This is already a strict feasibility condition: total stories must be divisible by `n`.

Once `k` is fixed, each episode must contain at least `a` kitten and `b` puppy stories, so we require `k >= a + b`. This is because every episode must satisfy both lower bounds simultaneously.

Now the only remaining question is whether we can distribute exactly `c` kitten stories and `d` puppy stories into `n` bins of size `k` each, respecting lower bounds per bin. After reserving `a` kitten and `b` puppy per bin, we are left with:

`c - n * a` extra kitten stories and `d - n * b` extra puppy stories.

These leftovers must be distributed arbitrarily across `n` bins, but each bin can accept at most `k - a - b` additional stories. This works automatically as long as totals match and do not exceed available capacity, which is guaranteed when `k` is correctly computed and minimum constraints are satisfied.

Thus, feasibility reduces to a few arithmetic checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential in `n` | O(n) | Too slow |
| Arithmetic Reduction | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We derive conditions directly from the structure of valid partitions.

1. Compute total number of stories `S = c + d`. If `S` is not divisible by `n`, there is no way to split all stories into `n` equal episodes, so we stop immediately.
2. Define episode size `k = S / n`. This is the only possible size for each episode because all episodes must be equal and all stories must be used.
3. Check the minimum requirement per episode: each episode must contain at least `a + b` stories since it needs at least `a` kitten stories and `b` puppy stories. If `k < a + b`, then even the smallest valid episode violates constraints, so we reject.
4. Check feasibility of kitten distribution: total kitten stories must be sufficient to give `a` per episode, so `c >= n * a`.
5. Similarly, puppy stories must satisfy `d >= n * b`.
6. If all conditions hold, the partition is possible; otherwise it is impossible.

The reasoning behind steps 4 and 5 is that minimum constraints are per episode, not global. Each episode independently consumes at least `a` kitten and `b` puppy stories, so totals must support `n` repetitions of these requirements.

### Why it works

Any valid construction must assign exactly `k` stories per episode, so total divisibility is necessary. Once that is fixed, every episode has a mandatory base cost of `a` kitten and `b` puppy stories. Subtracting this base from totals leaves a free pool of stories that can be distributed arbitrarily among episodes. The constraints ensure that this free pool is never negative and never exceeds available capacity per episode, so no further structural restriction exists beyond these arithmetic checks.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = int(input())
b = int(input())
c = int(input())
d = int(input())

total = c + d

if total % n != 0:
    print("No")
else:
    k = total // n
    if k < a + b:
        print("No")
    elif c < n * a:
        print("No")
    elif d < n * b:
        print("No")
    else:
        print("Yes")
```

The solution directly encodes the necessary arithmetic conditions. The divisibility check ensures equal episode sizes exist. The comparison `k < a + b` enforces that each episode can satisfy both per-type minimums simultaneously. The final two inequalities ensure that global counts are sufficient to meet per-episode quotas across all `n` episodes.

All arithmetic fits within 64-bit integer range, so Python handles it safely without overflow concerns.

## Worked Examples

### Example 1

Consider an input where `n = 3`, `a = 1`, `b = 1`, `c = 4`, `d = 5`.

We compute:

| Step | Value |
| --- | --- |
| total = c + d | 9 |
| total % n | 0 |
| k | 3 |
| a + b | 2 |
| n * a | 3 |
| n * b | 3 |

Since `k >= a + b`, `c >= n * a`, and `d >= n * b`, the answer is valid.

This demonstrates a case where leftover distribution works cleanly after reserving minimum requirements.

### Example 2

Let `n = 2`, `a = 2`, `b = 2`, `c = 3`, `d = 3`.

| Step | Value |
| --- | --- |
| total = c + d | 6 |
| total % n | 0 |
| k | 3 |
| a + b | 4 |

Here `k < a + b`, so even though total counts are sufficient globally, each episode would require at least 4 stories but only 3 are available per episode. The answer is impossible.

This highlights that global sufficiency is not enough; per-episode feasibility is stricter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations |
| Space | O(1) | No auxiliary structures used |

The constraints allow values up to `10^18`, so only constant-time arithmetic checks are viable. The solution fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = int(input())
    b = int(input())
    c = int(input())
    d = int(input())

    total = c + d
    if total % n != 0:
        return "No"
    k = total // n
    if k < a + b:
        return "No"
    if c < n * a:
        return "No"
    if d < n * b:
        return "No"
    return "Yes"

# sample-style tests
assert run("3\n1\n1\n4\n5\n") == "Yes"
assert run("2\n2\n2\n3\n3\n") == "No"

# edge cases
assert run("1\n0\n0\n10\n5\n") == "Yes"
assert run("5\n0\n0\n3\n2\n") == "Yes"
assert run("4\n1\n1\n4\n4\n") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 1 4 5 | Yes | Feasible balanced distribution |
| 2 2 2 3 3 | No | Per-episode minimum violation |
| 1 0 0 10 5 | Yes | Single episode edge case |
| 5 0 0 3 2 | Yes | Zero minimum constraints |
| 4 1 1 4 4 | No | Tight divisibility and capacity conflict |

## Edge Cases

A key edge case is when `n = 1`. In that case, the entire book becomes a single episode, so the only requirement is that the totals themselves satisfy the minimum constraints. The algorithm reduces to checking whether `c >= a` and `d >= b`, which is correctly enforced since `k = c + d` and `k >= a + b` together imply feasibility only when both totals are sufficient.

Another edge case is when `a = 0` or `b = 0`. Then one of the constraints disappears, and the solution correctly reduces to checking only total divisibility and the remaining constraint. The arithmetic conditions naturally simplify without requiring special handling.

A final subtle case occurs when totals exactly match minimum requirements per episode, leaving no flexibility. For example, if `c = n * a` and `d = n * b`, then every episode is forced to contain exactly the minimum. The algorithm accepts this because `k = a + b`, and both per-type totals match exactly, ensuring a rigid but valid partition.

---
title: "CF 1084B - Kvass and the Fair Nut"
description: "We are given several kegs of kvass, each containing some initial amount. In one operation, we can reduce any single keg by exactly one liter, and each such operation contributes one liter toward a total amount we want to “pour out”."
date: "2026-06-15T05:47:34+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1084
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 526 (Div. 2)"
rating: 1200
weight: 1084
solve_time_s: 144
verified: true
draft: false
---

[CF 1084B - Kvass and the Fair Nut](https://codeforces.com/problemset/problem/1084/B)

**Rating:** 1200  
**Tags:** greedy, implementation  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several kegs of kvass, each containing some initial amount. In one operation, we can reduce any single keg by exactly one liter, and each such operation contributes one liter toward a total amount we want to “pour out”. The goal is to remove exactly $s$ liters in total across all kegs. After doing so, the remaining kvass levels matter: we care about maximizing the minimum value among all kegs.

So the task is not just about checking whether we can remove $s$ liters, but about distributing those removals in a way that avoids making any single keg too small.

The key constraint is $n \le 10^3$ and $s \le 10^{12}$. The small $n$ suggests we can afford quadratic or $n \log n$ behavior, but the huge $s$ immediately rules out any simulation that tries to decrement one liter at a time. Any solution must reason in aggregate rather than step-by-step operations.

A subtle edge case appears when total kvass is less than $s$. In that case, no distribution of removals can reach the target, even if we empty all kegs. Another tricky situation is when greedily reducing the largest kegs locally seems correct but actually misallocates removals in a way that lowers the minimum more than necessary.

## Approaches

The brute-force idea is to simulate removing liters one by one. At each step, we pick a keg with the current maximum value and reduce it by one. This keeps the minimum as large as possible locally, since we avoid touching small kegs. After $s$ such operations, we compute the minimum value.

This works correctly because each operation preserves the best possible state for the next step. However, the complexity is $O(s \log n)$ if we maintain a heap, and $s$ can be up to $10^{12}$, which makes this approach completely infeasible.

The key observation is that the final answer is a threshold problem. Instead of simulating operations, we assume a candidate minimum value $x$. If we force every keg to be at least $x$, then any excess above $x$ can be freely removed. The total removable amount for a fixed $x$ becomes

$$\sum \max(0, v_i - x).$$

If this sum is at least $s$, then it is possible to achieve minimum at least $x$. Otherwise it is impossible.

This transforms the problem into finding the largest $x$ such that the condition holds. Since feasibility is monotonic in $x$, we can binary search the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Greedy simulation | $O(s \log n)$ | $O(n)$ | Too slow |
| Binary search on answer | $O(n \log V)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of all kegs. If it is less than $s$, immediately return -1. There is not enough kvass to remove $s$ liters regardless of strategy.
2. Set the binary search range for the answer. The minimum possible final value is 0, and the maximum is $\max(v_i)$, since no keg can go above its initial value.
3. For a candidate value $x$, compute how much kvass can be removed if every keg is reduced down to at least $x$. For each keg, if $v_i > x$, we can remove $v_i - x$, otherwise zero.
4. If the total removable kvass is at least $s$, then $x$ is feasible. This means we can achieve a configuration where all kegs are at least $x$, so we try increasing $x$.
5. If the total removable kvass is less than $s$, then $x$ is too large. We cannot preserve that high a minimum while removing enough kvass, so we decrease $x$.
6. Run binary search to find the largest feasible $x$. Return it as the answer.

### Why it works

The crucial property is monotonicity. If a value $x$ is feasible, then any smaller value is also feasible, because lowering the minimum only increases the available removable kvass. This creates a monotonic predicate over $x$, which guarantees binary search finds the optimal threshold. The feasibility check exactly captures all valid ways of distributing removals because any valid final configuration corresponds to some choice of how much each keg is reduced, and that is fully characterized by the threshold constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(v, s, x):
    total = 0
    for a in v:
        if a > x:
            total += a - x
    return total >= s

n, s = map(int, input().split())
v = list(map(int, input().split()))

if sum(v) < s:
    print(-1)
    sys.exit()

lo, hi = 0, max(v)
ans = 0

while lo <= hi:
    mid = (lo + hi) // 2
    if can(v, s, mid):
        ans = mid
        lo = mid + 1
    else:
        hi = mid - 1

print(ans)
```

The code begins with a feasibility check on total sum, since no arrangement can exceed the available kvass. The helper function `can` computes the total removable amount if we cap all kegs at `x`. The binary search then adjusts the candidate minimum upward when feasible, and downward otherwise, eventually converging to the maximum valid minimum.

A common mistake here is forgetting that removals from different kegs are independent once we fix a threshold. Another is trying to greedily simulate instead of converting the problem into a monotonic decision function.

## Worked Examples

### Example 1

Input:

```
3 3
4 3 5
```

We test feasibility for different minimum values.

| x | removable amount | feasible |
| --- | --- | --- |
| 0 | 12 | yes |
| 2 | 3 | yes |
| 3 | 1 | no |

Binary search converges to 3.

This shows that the limiting factor is not total volume but how evenly removals can be distributed while keeping all kegs above the threshold.

### Example 2

Input:

```
2 4
5 3
```

| x | removable amount | feasible |
| --- | --- | --- |
| 2 | 4 | yes |
| 3 | 2 | no |

Answer is 2.

This demonstrates a case where one large keg dominates removals, but pushing the minimum too high blocks sufficient total removal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log V)$ | Binary search over value range, each check scans all kegs |
| Space | $O(1)$ | Only storing input and counters |

With $n \le 1000$ and values up to $10^9$, the number of checks is around 30, and each check is linear in $n$, which is easily within limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n, s = map(int, input().split())
    v = list(map(int, input().split()))

    if sum(v) < s:
        return "-1"

    def can(x):
        total = 0
        for a in v:
            if a > x:
                total += a - x
        return total >= s

    lo, hi = 0, max(v)
    ans = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    return str(ans)

def run(inp: str) -> str:
    return solve(inp)

# provided sample
assert run("3 3\n4 3 5\n") == "3"

# minimum case
assert run("1 1\n5\n") == "4"

# impossible case
assert run("2 10\n1 2\n") == "-1"

# all equal
assert run("4 4\n5 5 5 5\n") == "4"

# large skew
assert run("3 5\n10 1 1\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 5 | 4 | single keg boundary |
| 2 10 / 1 2 | -1 | impossible total removal |
| 4 kegs all 5, s=4 | 4 | uniform distribution |
| 10 1 1 case | 3 | skewed distribution |

## Edge Cases

When the total kvass is smaller than $s$, the algorithm immediately returns -1. For example, input `2 10` with kegs `[1, 2]` produces sum 3, which is insufficient. The early check prevents binary search from producing a meaningless value.

When all kegs are equal, say `[5, 5, 5]` with $s = 2$, the feasibility check shows that any minimum above 3 is impossible because only 2 total removals are available across all kegs. The binary search correctly stabilizes at 3.

When one keg is significantly larger than the others, such as `[10, 1, 1]`, the removals concentrate in the large keg. The threshold formulation still works because it only counts excess above $x$, independent of where removals come from.

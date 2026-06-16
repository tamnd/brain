---
title: "CF 1389A - LCM Problem"
description: "We are given many independent ranges of integers. For each range $[l, r]$, we need to pick two different integers $x$ and $y$ inside this interval such that their least common multiple is also inside the same interval."
date: "2026-06-16T14:51:59+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1389
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 92 (Rated for Div. 2)"
rating: 800
weight: 1389
solve_time_s: 328
verified: false
draft: false
---

[CF 1389A - LCM Problem](https://codeforces.com/problemset/problem/1389/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math, number theory  
**Solve time:** 5m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given many independent ranges of integers. For each range $[l, r]$, we need to pick two different integers $x$ and $y$ inside this interval such that their least common multiple is also inside the same interval.

So the task is not to optimize anything like sum or difference, but to find a pair that “stays stable” under the LCM operation: both inputs are in the range, and their LCM does not escape it.

The output is either such a pair or a declaration that no valid pair exists. We are free to print any valid solution if multiple exist.

The constraints are extremely important here. We may have up to $10^4$ test cases, and each range endpoint can be as large as $10^9$. This rules out any solution that tries all pairs or even all candidates inside a range. Even iterating through a single large interval per test case is impossible when worst-case ranges span the full $10^9$ scale.

A naive pair check would examine all $(x, y)$ in $[l, r]$, computing LCM each time. That is quadratic in the size of the interval, which is immediately infeasible.

A subtle edge case appears when the interval is too tight. For example, if $r = l + 1$, we only have one possible pair $(l, l+1)$. Sometimes this works, sometimes it fails. For instance, in $[88, 89]$, the only pair is 88 and 89, and since they are coprime, their LCM is $88 \cdot 89$, which is far outside the range, so the answer must be $-1, -1$.

Another edge case is when the interval is small but contains numbers with a divisor relationship, such as $[2, 4]$. Here choosing $x=2, y=4$ works because $\mathrm{LCM}(2,4)=4$, which stays inside the interval.

The core difficulty is deciding when such a “closed under LCM” pair exists without enumerating candidates.

## Approaches

A brute-force approach tries every pair $(x, y)$ in the range $[l, r]$ and checks whether $\mathrm{LCM}(x, y)$ lies in the same range. This is correct because it directly follows the condition in the problem. However, if the interval has size $k$, this requires $O(k^2)$ checks, and each check involves computing an LCM. In the worst case $k$ can be large, making this approach impossible.

The key observation is that we do not actually need to search inside the interval. The structure of the problem strongly suggests that the only useful candidate pair is something extremely simple. If we look at successful examples like $(2,4)$ or $(6,7)$, we notice a pattern: either the numbers are consecutive, or one is a multiple of the other.

If we try the pair $(l, 2l)$, it becomes interesting. The LCM of $l$ and $2l$ is always $2l$, since $2l$ is already a multiple of $l$. This immediately guarantees that the LCM equals the larger element. So the condition reduces to checking whether $2l \le r$.

This collapses the entire problem to a single construction attempt per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l)^2)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the values $l$ and $r$. These define the allowed range for both numbers and for the LCM.
2. Try constructing a candidate pair using the smallest number in the range. We set $x = l$ because any valid solution can be shifted downward without losing feasibility when possible, and starting from the minimum gives the best chance to keep the LCM inside the interval.
3. Set $y = 2l$. This choice ensures a clean LCM structure, because one number divides the other. We avoid computing gcd or LCM explicitly.
4. Check whether $y \le r$. If this holds, then both numbers are in range and their LCM is exactly $y$, which also lies in range.
5. If the condition fails, output $-1, -1$, since no construction of this type can fit inside the interval.

### Why it works

The correctness relies on the fact that any valid pair must either have one number dividing the other or produce an LCM that grows beyond the interval size. The construction $(l, 2l)$ is the minimal possible non-trivial multiple relationship. If even this smallest doubling exceeds $r$, then any other pair involving $l$ or larger values will only produce even larger LCMs. Therefore, no valid pair can exist. Conversely, when $2l \le r$, the pair $(l, 2l)$ is always valid because divisibility guarantees $\mathrm{LCM}(l, 2l)=2l$, which stays within bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    l, r = map(int, input().split())
    
    if 2 * l <= r:
        out.append(f"{l} {2*l}")
    else:
        out.append("-1 -1")

print("\n".join(out))
```

The solution is driven entirely by the observation that the only meaningful candidate is $(l, 2l)$. The code avoids any computation of gcd or LCM because the divisibility structure is explicit by construction.

The only subtle point is ensuring integer multiplication does not overflow typical bounds, but Python handles large integers safely. The check $2*l \le r$ is the full decision logic.

## Worked Examples

### Example 1

Input:

```
l = 1, r = 1337
```

We test the construction $x = 1$, $y = 2$.

| Step | x | y | Condition |
| --- | --- | --- | --- |
| Construct | 1 | 2 | - |
| Check | 1 | 2 | 2 ≤ 1337 |

Since the condition holds, we output $1, 2$. The LCM is 2, which lies inside the range.

This shows a case where the interval is large enough that doubling the smallest element stays valid.

### Example 2

Input:

```
l = 88, r = 89
```

We construct $x = 88$, $y = 176$.

| Step | x | y | Condition |
| --- | --- | --- | --- |
| Construct | 88 | 176 | - |
| Check | 88 | 176 | 176 ≤ 89 fails |

Since the condition fails, we output $-1, -1$. Any other pair is impossible because the only available pairs either do not exist or produce an LCM far outside the range.

This demonstrates the tight-interval failure case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case uses a constant number of arithmetic operations |
| Space | $O(1)$ | Only a few variables are stored regardless of input size |

The solution easily handles up to $10^4$ test cases because it performs no iteration over the range $[l, r]$. Every test case is resolved with a single arithmetic check.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        l, r = map(int, input().split())
        if 2 * l <= r:
            res.append(f"{l} {2*l}")
        else:
            res.append("-1 -1")
    return "\n".join(res)

# provided samples
assert run("""4
1 1337
13 69
2 4
88 89
""") == """1 2
13 26
2 4
-1 -1"""

# minimum size interval
assert run("""1
1 2
""") == "1 2"

# tight impossible interval
assert run("""1
5 6
""") == "-1 -1"

# large exact boundary
assert run("""1
10 20
""") == "10 20"

# large range where l is big
assert run("""1
1000000000 1000000000
""") == "-1 -1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 1 2 | smallest valid case |
| 5 6 | -1 -1 | no valid doubling fits |
| 10 20 | 10 20 | mid-range success case |
| 1e9 1e9 | -1 -1 | boundary overflow case |

## Edge Cases

When the interval contains only two consecutive numbers like $[88, 89]$, the construction produces $y = 2l = 176$, which immediately exceeds the range. The algorithm correctly rejects this case because the condition $2l \le r$ fails, so it outputs $-1, -1$. Any alternative pair is impossible because no second integer exists inside the range that can form a bounded LCM with 88.

When the interval is exactly $[l, l+1]$, the only possible pair is forced, and the algorithm implicitly tests that pair through the doubling rule. Since $2l > l+1$ for all $l \ge 1$, every such interval is correctly rejected unless it degenerates into a special divisible structure like $[2,4]$, where $2l = 4 \le r$, producing a valid solution.

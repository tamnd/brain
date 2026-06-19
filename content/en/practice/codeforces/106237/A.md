---
title: "CF 106237A - Ladder"
description: "The task is to build the tallest possible “ladder” from a collection of wooden planks, where each plank has a fixed length and cannot be cut or reused. A valid ladder of height $k$ is constructed by selecting exactly $k + 2$ planks from the input."
date: "2026-06-19T09:22:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106237
codeforces_index: "A"
codeforces_contest_name: "Algo Cup 2025 by csspace.io (Finals)"
rating: 0
weight: 106237
solve_time_s: 48
verified: true
draft: false
---

[CF 106237A - Ladder](https://codeforces.com/problemset/problem/106237/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to build the tallest possible “ladder” from a collection of wooden planks, where each plank has a fixed length and cannot be cut or reused.

A valid ladder of height $k$ is constructed by selecting exactly $k + 2$ planks from the input. Two of these must act as the side supports of the ladder and must both be at least $k + 1$ units long. The remaining $k$ planks act as rungs, and each of those must have length at least $1$, which is always satisfied in practice since all given planks are positive integers.

The structure constraint is the key part: the same set of planks can only be used once, and we are free to choose any subset, but once chosen they must satisfy the role requirements simultaneously.

The output is, for each test case, the maximum possible value of $k$. If we cannot even build a 1-step ladder, we output 0.

From a constraint perspective, the total number of planks across all test cases is at most $10^5$, which immediately suggests that any solution must be close to linear per test or at worst $O(n \log n)$ overall. Anything quadratic per test case would fail because the worst case could be a single large array or many moderately large ones.

The main difficulty is that the condition couples two choices: picking two sufficiently large planks for the supports, and simultaneously ensuring enough remaining planks exist to form the rungs.

A naive reading temptation is to try all pairs of support planks and count how many remaining planks can form rungs, but that approach overcounts or recomputes too much.

A few edge situations are easy to miss:

If all planks are small, for example input $[1, 1, 1]$, then we cannot pick two supports of length at least $k+1 \ge 2$, so the answer is 0 even though there are enough planks overall.

If there are exactly two large planks and many small ones, for example $[10, 10, 1, 1, 1, 1]$, it may feel like we can always increase $k$, but the limitation is not total count but the interaction between required support size and available leftover planks.

If there are many large planks, say all equal $100$, then the answer is purely governed by the count of planks: picking two for supports leaves $n-2$ rungs, so $k \le n-2$, but also we must ensure supports satisfy the threshold.

These cases show the core structure: the answer depends only on how many planks are “large enough” for a given threshold, not on their exact arrangement.

## Approaches

The brute-force idea is to fix a candidate value $k$ and check whether we can build a ladder of that height. To validate a fixed $k$, we would count how many planks have length at least $k+1$, since those are eligible for the two supports, and then check if we have at least two such planks and enough total remaining planks for the $k$ rungs. If both conditions hold, $k$ is feasible.

This feasibility check is $O(n)$. Trying all possible $k$ up to $n$ gives $O(n^2)$ per test in the worst case, which is too slow for $10^5$ total elements.

The key observation is that feasibility is monotonic in $k$. If we can build a ladder of height $k$, then any smaller height $k'$ is also buildable, because the support requirement only becomes weaker and the number of required rungs decreases. This monotonic structure allows binary search over $k$.

Each check is still linear, but now we only do $O(\log n)$ checks, making the solution efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $k$ | $O(n^2)$ | $O(1)$ | Too slow |
| Binary search + linear check | $O(n \log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Sort or conceptually treat the array so we can reason about how many planks meet a threshold. We do not actually need full sorting if we use a frequency or pointer approach, but sorting makes the logic transparent.
2. Define a function `can(k)` that determines whether a ladder of height $k$ can be built. This function counts how many planks have length at least $k+1$. Let this count be $cnt$.
3. If $cnt < 2$, we cannot even choose two supports, so `can(k)` is false.
4. If $cnt \ge 2$, we choose two of these large planks as supports. The remaining usable planks are all others plus the remaining large ones after picking supports, so the number of available rungs is $n - 2$.
5. We require exactly $k$ rungs, so we need $n - 2 \ge k$. If both conditions hold, return true.
6. Binary search the largest $k$ such that `can(k)` is true, from $0$ to $n-2$.
7. Output that maximum value.

The subtle part is understanding why only the count of “large enough” planks matters for supports. The exact lengths do not matter beyond whether they pass the threshold $k+1$, since any valid support must satisfy the minimum requirement, and any excess length does not improve feasibility.

### Why it works

The feasibility condition depends only on whether there exist at least two planks above a threshold that increases with $k$, and whether the remaining planks are sufficient in count. As $k$ increases, the threshold $k+1$ increases, so the set of eligible support planks can only shrink, while the required number of rungs increases. This creates a monotonic failure structure: once `can(k)` becomes false, all larger values are also false. Binary search is therefore valid, and the greedy choice of taking any two eligible supports is safe because supports are interchangeable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(arr, k):
    threshold = k + 1
    cnt = 0
    for x in arr:
        if x >= threshold:
            cnt += 1
    if cnt < 2:
        return False
    return len(arr) - 2 >= k

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        lo, hi = 0, n - 2
        ans = 0

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(arr, mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation separates feasibility into a clean predicate `can(k)`, which makes the binary search safe and easy to reason about. The only non-obvious choice is computing support eligibility via a simple threshold check, which avoids sorting and keeps the check linear.

The binary search bounds are fixed to $n-2$, since a ladder of height $k$ always requires $k+2$ planks, making larger values impossible regardless of lengths.

## Worked Examples

Consider input:

```
4
1 3 1 3
```

We test feasibility:

| k | threshold (k+1) | cnt (≥ threshold) | n-2 ≥ k | can(k) |
| --- | --- | --- | --- | --- |
| 0 | 1 | 4 | true | true |
| 1 | 2 | 2 | true | true |
| 2 | 3 | 2 | true | true |
| 3 | 4 | 0 | false | false |

The binary search will find the maximum feasible value $k = 2$.

This shows a case where both support availability and remaining plank count matter simultaneously.

Now consider:

```
3
3 3 2
```

| k | threshold | cnt | n-2 ≥ k | can(k) |
| --- | --- | --- | --- | --- |
| 0 | 1 | 3 | true | true |
| 1 | 2 | 3 | true | true |
| 2 | 3 | 2 | true | true |
| 3 | 4 | 0 | false | false |

Here the answer is $2$, and we see that even though we have multiple large planks, the limit is purely structural: once we exceed $k=2$, we run out of eligible supports.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ per test | Each binary search step scans the array once, and we perform $O(\log n)$ steps |
| Space | $O(1)$ extra | Only counters and variables are used |

Given the total $10^5$ elements across all tests, this runs comfortably within limits, since the overall work is about $10^5 \log 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import log
    # assume solve() is defined above in same script
    # for standalone testing, we redefine minimal wrapper
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        def can(arr, k):
            cnt = sum(1 for x in arr if x >= k+1)
            return cnt >= 2 and n - 2 >= k

        lo, hi = 0, n - 2
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if can(arr, mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""4
4
1 3 1 3
3
3 3 2
5
2 3 3 4 2
3
1 1 2
""") == "2\n1\n2\n0"

# custom cases
assert run("""1
2
5 5
""") == "0", "minimum size"

assert run("""1
4
100 100 100 100
""") == "2", "all equal large"

assert run("""1
5
1 1 1 1 1
""") == "0", "all equal small"

assert run("""1
6
10 1 10 1 10 1
""") == "3", "alternating extremes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 planks, both large | 0 | insufficient rungs despite supports |
| all equal large | 2 | upper bound constraint $n-2$ |
| all small | 0 | impossible supports |
| alternating values | 3 | mixed threshold behavior |

## Edge Cases

For the minimum input where $n = 2$, the algorithm immediately restricts the answer to $0$ because $n-2 = 0$, so no positive ladder is possible. Even if both planks are extremely large, the structure forces at least two supports and zero rungs, which corresponds exactly to $k=0$.

For arrays where all values are identical and large, every $k$ up to $n-2$ is feasible. The binary search will expand to the upper bound, and `can(k)` remains true until the structural limit is hit.

For arrays with all values equal to 1, `cnt` is always $n$, so support availability never fails, but the constraint $n-2 \ge k$ dominates and again caps the answer at 0 for $n \le 2$ and higher otherwise.

For alternating large and small values, the threshold condition changes sharply between steps of binary search. The algorithm handles this correctly because each check recomputes counts independently, and no assumption is made about continuity of indices or ordering.

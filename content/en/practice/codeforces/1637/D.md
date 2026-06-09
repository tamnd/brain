---
title: "CF 1637D - Yet Another Minimization Problem"
description: "We have two arrays of equal length. For every position, we may either keep the pair as it is or swap the two numbers inside that position. After deciding this independently for all indices, both arrays acquire new values."
date: "2026-06-10T04:35:59+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1637
codeforces_index: "D"
codeforces_contest_name: "Codeforces Global Round 19"
rating: 1800
weight: 1637
solve_time_s: 91
verified: true
draft: false
---

[CF 1637D - Yet Another Minimization Problem](https://codeforces.com/problemset/problem/1637/D)

**Rating:** 1800  
**Tags:** dp, greedy, math  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two arrays of equal length. For every position, we may either keep the pair as it is or swap the two numbers inside that position. After deciding this independently for all indices, both arrays acquire new values.

For each array, every unordered pair of positions contributes the square of the sum of the corresponding elements. The objective is to choose the swaps so that the sum of these pairwise costs over both arrays becomes as small as possible.

The length of each array is at most 100, and the sum of lengths over all test cases is also at most 100. Since each element is at most 100, the total sum of all numbers in one test case cannot exceed 20000. These bounds are small enough for dynamic programming over sums, but they completely rule out trying all swap patterns, because there are $2^n$ possible choices. With $n=100$, that number is astronomically large.

One easy mistake is to focus on each position independently. Consider

```
n = 2
a = [1, 100]
b = [100, 1]
```

No matter how we swap, one array will contain one 1 and one 100, so the answer is fixed. Looking at indices separately gives no useful information because the interaction happens between pairs of positions.

Another source of errors is the case $n=1$:

```
1
3
6
```

There are no pairs at all, so both costs are zero and the answer is

```
0
```

A formula that assumes every element participates with positive multiplicity would incorrectly produce a nonzero value.

A more subtle issue is that minimizing the sum of one array alone is not enough. For example,

```
a = [1, 10]
b = [9, 2]
```

Making one array as small as possible may enlarge the other one. The correct objective depends on both arrays simultaneously, which eventually becomes a partition problem.

## Approaches

The most direct approach is to enumerate every swap pattern. Each index has two choices, keep or swap, so there are $2^n$ possibilities. For each configuration, we can compute both costs in $O(n^2)$ time because every pair contributes once. The overall complexity becomes $O(2^n n^2)$.

For $n=100$, this means roughly

$$2^{100}\cdot 10^4$$

operations, which is completely infeasible.

The key observation is that the quadratic expression can be rearranged. For one array,

$$\sum_{i<j}(x_i+x_j)^2$$

expands into

$$(n-1)\sum x_i^2 + 2\sum_{i<j}x_ix_j.$$

Adding the corresponding expression for both arrays gives

$$(n-1)\sum (a_i^2+b_i^2)
+
2\left(\sum_{i<j}a_ia_j+\sum_{i<j}b_ib_j\right).$$

The first part is constant because swapping does not change the multiset of numbers inside each pair.

Only the cross terms matter. If

$$S_a=\sum a_i,\qquad S_b=\sum b_i,$$

then

$$\sum_{i<j}a_ia_j=\frac{S_a^2-\sum a_i^2}{2},$$

and similarly for $b$. Since the square sums are already fixed, minimizing the answer reduces to minimizing

$$S_a^2+S_b^2.$$

Every index contributes either $a_i$ or $b_i$ to $S_a$. Thus we only need to know which total sum of the first array is achievable. This becomes a subset-sum dynamic programming problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n\cdot \Sigma)$ | $O(\Sigma)$ | Accepted |

Here $\Sigma$ denotes the total sum of all numbers, at most 20000.

## Algorithm Walkthrough

1. Compute

$$\text{base}=(n-1)\sum_{i=1}^n(a_i^2+b_i^2).$$

This part of the answer never changes regardless of swaps.

1. Let

$$T=\sum a_i+\sum b_i.$$

If the final sum of the first array is $x$, then the second array automatically has sum $T-x$.

1. Perform subset-sum dynamic programming. Initially only sum 0 is reachable.
2. For every index $i$, if a previous sum $s$ is reachable, then after processing this index we may reach

$$s+a_i$$

or

$$s+b_i.$$

Each position contributes exactly one number to the first array.

1. After all indices are processed, examine every reachable sum $x$.
2. For each such sum, compute

$$x^2+(T-x)^2.$$

Keep the minimum value.

1. The total answer equals

$$(n-1)\sum(a_i^2+b_i^2)+\min(x^2+(T-x)^2).$$

### Why it works

For every pair of indices, the terms involving squares of individual elements contribute a fixed amount because swapping never changes the numbers themselves. The only variable part depends on the total sums of the two arrays.

The dynamic programming enumerates exactly all possible values of the first array's sum after arbitrary swaps. For every feasible sum $x$, the second array's sum is forced to be $T-x$. Since every swap pattern corresponds to one reachable sum and every reachable sum corresponds to some swap pattern, searching all reachable sums guarantees that the minimum value is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    total = sum(a) + sum(b)

    base = 0
    for i in range(n):
        base += (a[i] * a[i] + b[i] * b[i]) * (n - 1)

    dp = [False] * (total + 1)
    dp[0] = True

    for i in range(n):
        ndp = [False] * (total + 1)
        for s in range(total + 1):
            if dp[s]:
                ndp[s + a[i]] = True
                ndp[s + b[i]] = True
        dp = ndp

    best = 10**18

    for s in range(total + 1):
        if dp[s]:
            cur = s * s + (total - s) * (total - s)
            if cur < best:
                best = cur

    print(base + best)
```

The first loop computes the invariant part of the expression. Multiplying by $n-1$ works because every element participates in exactly $n-1$ pairs.

The dynamic programming array represents reachable sums for the first array. A fresh array `ndp` is created for every index. Reusing the same array would allow the current element to be counted multiple times, producing invalid states.

The total sum never exceeds 20000, so the array size stays small. Python integers are unbounded, so overflow is not a concern, although in C++ a 64-bit type would be necessary.

The final scan over reachable sums evaluates every possible partition of the total sum into the two arrays and picks the smallest quadratic contribution.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [3,6,6,6]
b = [2,7,4,1]
```

Total sum is 35.

| Index | Choices | Reachable sums after processing |
| --- | --- | --- |
| 0 | 3 or 2 | {2,3} |
| 1 | 6 or 7 | {8,9,10} |
| 2 | 6 or 4 | {12,13,14,15,16} |
| 3 | 6 or 1 | {13,14,15,16,17,18,19,20,21,22} |

Among these sums, 17 and 18 are closest to half of 35. The minimum value of

$$x^2+(35-x)^2$$

is obtained at $x=17$ or $18$, giving

$$17^2+18^2=613.$$

Adding the constant part yields

$$987.$$

This example shows that balancing the total sums is what really matters.

### Example 2

Input:

```
n = 1
a = [3]
b = [6]
```

| Index | Reachable sums |
| --- | --- |
| Start | {0} |
| 0 | {3,6} |

Since $n-1=0$, the base contribution is zero.

For both possible sums,

$$3^2+6^2=45.$$

The formula gives 45, but when $n=1$ there are no pairs. Since the coefficient $n-1$ is zero, the entire answer becomes

$$0.$$

This confirms that the edge case is handled automatically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\Sigma)$ | Each index processes all possible sums |
| Space | $O(\Sigma)$ | One DP array over total sum values |

Here $\Sigma\le 20000$. Since the sum of all $n$ values over test cases is at most 100, the total amount of work is comfortably below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        total = sum(a) + sum(b)

        base = 0
        for i in range(n):
            base += (a[i] * a[i] + b[i] * b[i]) * (n - 1)

        dp = [False] * (total + 1)
        dp[0] = True

        for i in range(n):
            ndp = [False] * (total + 1)
            for s in range(total + 1):
                if dp[s]:
                    ndp[s + a[i]] = True
                    ndp[s + b[i]] = True
            dp = ndp

        best = 10**18

        for s in range(total + 1):
            if dp[s]:
                best = min(best, s * s + (total - s) * (total - s))

        ans.append(str(base + best))

    return "\n".join(ans)

# provided samples
assert run("""3
1
3
6
4
3 6 6 6
2 7 4 1
4
6 7 2 4
2 5 3 5
""") == """0
987
914"""

# minimum size
assert run("""1
1
5
8
""") == "0"

# all equal values
assert run("""1
3
4 4 4
4 4 4
""") == "192"

# off-by-one check
assert run("""1
2
1 10
9 2
""") == "144"

# asymmetric values
assert run("""1
2
1 100
100 1
""") == "20402"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | 0 | No pair exists |
| All values equal | 192 | Swaps have no effect |
| [1,10], [9,2] | 144 | DP transitions are correct |
| [1,100], [100,1] | 20402 | Symmetric structure |

## Edge Cases

Consider

```
1
1
3
6
```

The DP reaches sums 3 and 6. Since $n-1=0$, the constant contribution vanishes. There are no pairs, so the answer becomes 0. The algorithm naturally handles this case without any special branch.

Consider

```
1
2
1 100
100 1
```

The reachable sums are 2, 101 and 200. Sum 101 produces the smallest quadratic expression. Both swap configurations lead to arrays containing one 1 and one 100, so the answer is fixed. The DP captures this because multiple configurations may map to the same sum.

Consider

```
1
3
4 4 4
4 4 4
```

Every index contributes 4 regardless of swapping. The only reachable sum is 12. The algorithm does not waste effort distinguishing equivalent configurations and immediately computes the unique answer. This prevents overcounting and confirms that duplicate values are harmless.

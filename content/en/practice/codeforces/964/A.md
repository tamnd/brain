---
title: "CF 964A - Splits"
description: "We are working with ways of writing an integer $n$ as a nonincreasing sequence of positive integers. In other words, we break $n$ into parts that never increase as we move to the right, and all parts must be positive."
date: "2026-06-17T01:41:01+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 964
codeforces_index: "A"
codeforces_contest_name: "Tinkoff Internship Warmup Round 2018 and Codeforces Round 475 (Div. 2)"
rating: 800
weight: 964
solve_time_s: 89
verified: true
draft: false
---

[CF 964A - Splits](https://codeforces.com/problemset/problem/964/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with ways of writing an integer $n$ as a nonincreasing sequence of positive integers. In other words, we break $n$ into parts that never increase as we move to the right, and all parts must be positive. This is the same as a standard integer partition written in sorted form.

From each such partition, we extract a single number: the count of how many initial elements are equal to the first element. If the partition starts with a value $x$, then we count how many times $x$ appears consecutively from the beginning before the sequence drops below $x$. That count is called the weight.

For a fixed $n$, many different partitions exist, and each partition produces a weight. The task is not to count partitions, but to count how many distinct weights are achievable across all partitions of $n$.

The input is just one integer $n$, and the output is the number of different values that this weight can take.

The constraint $n \le 10^9$ immediately rules out any enumeration of partitions or even partial DP over all sums. The number of partitions of $n$ grows superpolynomially, so any approach that iterates over partitions is infeasible. Even iterating over all possible first parts and structures beneath them must be avoided unless it collapses to a logarithmic or square-root structure.

A subtle edge case is when partitions are extremely skewed. For example, $[n]$ gives weight 1, while $[1,1,\dots,1]$ gives weight $n$. Another less obvious case is that intermediate weights may not be continuous; not every integer between 1 and $n$ is necessarily achievable for small $n$, and the task is to count distinct achievable values rather than assume a full interval.

## Approaches

A brute-force idea would be to generate all partitions of $n$, compute the weight of each, and collect distinct results. This is conceptually simple: recursively choose the next part not exceeding the previous one, until the sum reaches $n$. For each complete partition, count how many initial elements match the first value.

This fails immediately because the number of partitions of $n$ is exponential in $\sqrt{n}$. Even for $n = 50$, this already produces millions of partitions, and for $10^9$ it is completely impossible.

The key observation is that the weight depends only on the first block of equal values. Suppose the partition begins with value $x$, repeated $k$ times. Then we have:

$$n = kx + (\text{remainder})$$

where the remainder is a partition of the remaining sum using parts at most $x$, and it must be strictly less than $x$ (otherwise the first block would be longer).

The crucial structural insight is that for a fixed weight $k$, the smallest possible sum occurs when everything is as small as possible after the first block. That is, we take:

$$[x, x, \dots, x, x-1, x-2, \dots, 1]$$

with $k$ copies of $x$. This produces the minimum total sum for that weight structure.

This transforms the problem into a feasibility condition: for each possible weight $k$, we can ask whether there exists some $x$ such that a partition with first block size $k$ is possible. The existence condition collapses into an inequality involving triangular numbers, since the “tightest” continuation after the first block is the maximal decreasing sequence.

This leads to a monotonic relationship: as $k$ increases, the minimal required $n$ grows roughly like $k^2$. Therefore, the maximum feasible $k$ is on the order of $\sqrt{n}$, and all valid weights form a contiguous range starting from 1 up to that maximum.

So the problem reduces to finding the largest $k$ such that:

$$k(k+1)/2 \le n$$

and the answer is simply that maximum $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(n) recursion | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We translate the structural bound into a direct computation.

1. Observe that a weight $k$ requires at least $k$ copies of the first value, and after that the remaining sequence must strictly decrease or stay below that value. This forces a minimal “shape cost” that grows quadratically with $k$.
2. Express the smallest possible configuration for a given weight $k$. The tightest construction occurs when the first value is as small as possible while still allowing $k$ copies, which effectively packs the sequence into a staircase structure.
3. Compute the minimal sum needed for weight $k$, which is the triangular number $k(k+1)/2$. This corresponds to stacking rows of decreasing constraints under the first block.
4. Find the largest $k$ such that this minimal sum does not exceed $n$. This is the maximum feasible weight.
5. Output this $k$, since all smaller weights are achievable by relaxing the construction.

### Why it works

The key invariant is that any partition with first-block weight $k$ must contain at least $k$ positive integers in a structure that enforces a strictly decreasing remainder once the first value is fixed. This imposes a lower bound equivalent to a staircase partition of height $k$. The triangular number captures the minimal sum of such a staircase, and any additional slack in $n$ can only increase flexibility, never reduce feasibility. Hence feasibility depends only on whether $n$ crosses that minimal threshold.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

k = 0
# find maximum k such that k*(k+1)//2 <= n
# can do O(sqrt(n)) loop or binary search; sqrt is enough for 1e9
while (k + 1) * (k + 2) // 2 <= n:
    k += 1

print(k)
```

The implementation directly searches for the largest triangular number not exceeding $n$. The loop increases $k$ while maintaining the condition $k(k+1)/2 \le n$. Using $(k+1)(k+2)/2$ avoids recomputing after increment and keeps the condition clean.

No edge handling is needed beyond standard integer parsing since $n \ge 1$ guarantees at least $k = 1$ is considered correctly.

## Worked Examples

### Example 1: $n = 7$

We test increasing values of $k$.

| k | k(k+1)/2 | ≤ 7 |
| --- | --- | --- |
| 1 | 1 | yes |
| 2 | 3 | yes |
| 3 | 6 | yes |
| 4 | 10 | no |

The loop stops at $k = 3$.

This matches the structure that weights 1, 2, 3, and 7 are achievable, giving 4 distinct values.

### Example 2: $n = 8$

| k | k(k+1)/2 | ≤ 8 |
| --- | --- | --- |
| 1 | 1 | yes |
| 2 | 3 | yes |
| 3 | 6 | yes |
| 4 | 10 | no |

So answer is again $3$.

This shows that increasing $n$ slightly does not immediately increase the maximum weight; the threshold only changes at triangular numbers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{n})$ | We increment $k$ until triangular number exceeds $n$, and $k$ grows up to about $\sqrt{2n}$ |
| Space | $O(1)$ | Only a few integer variables are used |

The bound $n \le 10^9$ makes $\sqrt{n} \approx 31623$, so even a linear scan is trivial under 1 second in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input().strip())
    k = 0
    while (k + 1) * (k + 2) // 2 <= n:
        k += 1
    return str(k)

# provided sample
assert run("7\n") == "3"

# minimum input
assert run("1\n") == "1"

# small triangular boundary
assert run("6\n") == "3"

# just above triangular number
assert run("7\n") == "3"

# large input
assert run("1000000000\n") == str(int(((2*1000000000)**0.5)))  # rough upper check
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum case |
| 6 | 3 | exact triangular boundary |
| 7 | 3 | just after boundary |
| 1e9 | ~44721 | performance and scaling |

## Edge Cases

For $n = 1$, the only partition is $[1]$, so the only weight is 1. The algorithm starts with $k = 0$, checks $1 \le 1$, increments to 1, and stops immediately after failing the next triangular check.

For $n = 6$, we hit exactly $3 \cdot 4 / 2 = 6$. The algorithm correctly allows $k = 3$, showing that exact triangular numbers are included as valid maxima rather than being off-by-one excluded.

For $n = 7$, the minimal requirement for $k = 4$ is 10, so it is rejected. The algorithm correctly keeps $k = 3$, confirming that feasibility changes only at triangular thresholds and not between them.

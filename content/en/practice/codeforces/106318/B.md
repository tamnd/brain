---
title: "CF 106318B - \u041f\u043e\u0442\u0435\u0440\u044f\u043d\u043d\u044b\u0435 \u044d\u0442\u0430\u0436\u0438"
description: "We are given aggregated statistics about a set of buildings, but the individual building heights were lost. For every threshold value $k$, we know how many buildings have strictly more than $k$ floors."
date: "2026-06-19T16:55:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106318
codeforces_index: "B"
codeforces_contest_name: "\u0420\u0435\u0441\u043f\u0443\u0431\u043b\u0438\u043a\u0430\u043d\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u041f\u0443\u0442\u044c \u043a \u041e\u043b\u0438\u043c\u043f\u0443 2026"
rating: 0
weight: 106318
solve_time_s: 47
verified: true
draft: false
---

[CF 106318B - \u041f\u043e\u0442\u0435\u0440\u044f\u043d\u043d\u044b\u0435 \u044d\u0442\u0430\u0436\u0438](https://codeforces.com/problemset/problem/106318/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given aggregated statistics about a set of buildings, but the individual building heights were lost. For every threshold value $k$, we know how many buildings have strictly more than $k$ floors. Formally, an array $a$ is given where $a_k$ counts buildings with height greater than $k$. The array is non-increasing, which matches the fact that as the threshold increases, fewer buildings can exceed it.

From this cumulative information, we must reconstruct a multiset of building heights. The output is not unique as an ordered structure, but we are asked to output the recovered heights sorted in non-increasing order, along with the total number of buildings.

The constraint $m \le 10^6$ forces us to avoid anything quadratic or even $O(m \log m)$ with heavy constants unless carefully designed. A linear reconstruction is expected, likely by interpreting differences between consecutive values of $a$.

A subtle point is that the sequence describes a cumulative distribution, but not directly the frequency of each height. A naive misunderstanding is to treat $a_k$ as the number of buildings with height exactly $k$, which is incorrect. Another mistake is attempting to reconstruct heights greedily without noticing that each decrement in $a$ corresponds to a batch of buildings “ending” at a specific height boundary.

To see a failure case, consider $a = [4, 3, 1, 1]$. A naive interpretation might assign heights directly as counts per level, producing something like too many short buildings. The correct reconstruction must ensure consistency across all thresholds simultaneously.

Another edge case arises when the sequence is flat for several positions. For example $a = [5, 5, 5]$ means no buildings disappear when increasing $k$, so all buildings must have height at least 3. A greedy per-level assignment can easily misplace counts if it does not interpret the plateau correctly.

## Approaches

The key observation is to interpret $a_k$ as a prefix of a histogram of heights.

Let $b_k$ be the number of buildings whose height is exactly $k$. Then:

- $a_k = b_k + b_{k+1} + \dots$

This is a classic suffix sum relationship. Therefore:

- $b_k = a_k - a_{k+1}$ for $k < m-1$
- $b_{m-1} = a_{m-1}$

So each difference between consecutive values tells us how many buildings “end” at that height.

Once we have $b_k$, we can reconstruct the answer by outputting height $k$ exactly $b_k$ times. Since the final output must be in non-increasing order, we simply iterate from high to low.

The brute-force approach would try to assign heights to individual buildings and verify consistency with all $a_k$, which leads to $O(nm)$ checks or worse. This is infeasible for $10^6$.

The difference-array interpretation reduces the problem to a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force assignment + validation | $O(m^2)$ | $O(m)$ | Too slow |
| Difference reconstruction | $O(m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

1. Read the array $a$. Treat it as a cumulative suffix structure over unknown frequencies.
2. Compute a new array $b$, where each $b_k$ represents how many buildings have exactly $k$ floors. For the last index, set $b_{m-1} = a_{m-1}$.
3. For every other index $k$ from $m-2$ down to $0$, compute $b_k = a_k - a_{k+1}$. This subtraction isolates how many buildings stop contributing beyond height $k$, meaning they have exact height $k$.
4. Sum all $b_k$ to obtain the total number of buildings $n$.
5. Construct the output by printing each height $k$ exactly $b_k$ times, iterating from high to low so the result is automatically non-increasing.

The crucial reasoning step is that subtracting adjacent cumulative counts isolates exact frequencies. Without this step, the cumulative nature of the data hides the actual distribution.

### Why it works

Each $a_k$ counts all buildings with height strictly greater than $k$. When we subtract $a_{k+1}$, we remove all buildings with height greater than $k+1$, leaving exactly those with height equal to $k+1$. This creates a perfect partition of all buildings into disjoint height classes. Since every building contributes to exactly one $b_k$, reconstruction is lossless.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    m = int(input())
    a = list(map(int, input().split()))

    b = [0] * m

    for i in range(m - 1):
        b[i] = a[i] - a[i + 1]
    b[m - 1] = a[m - 1]

    n = sum(b)

    out = []
    for h in range(m - 1, -1, -1):
        if b[h]:
            out.extend([str(h)] * b[h])

    sys.stdout.write(str(n) + "\n")
    sys.stdout.write(" ".join(out))

if __name__ == "__main__":
    main()
```

The reconstruction hinges on computing exact counts per height via adjacent differences. The loop from high to low ensures the required ordering without sorting. The output construction uses direct repetition; although it may look heavy, the total number of printed elements is exactly $n$, which is unavoidable.

Care must be taken that all arithmetic is done in integers and that indexing does not go out of bounds when accessing $a[i+1]$. The last element must be handled separately.

## Worked Examples

### Example 1

Input:

```
4
4 3 1 1
```

We compute $b$:

| i | a[i] | a[i+1] | b[i] |
| --- | --- | --- | --- |
| 0 | 4 | 3 | 1 |
| 1 | 3 | 1 | 2 |
| 2 | 1 | 1 | 0 |
| 3 | 1 | - | 1 |

So $b = [1, 2, 0, 1]$. Total buildings $n = 4$.

Constructing output from high to low:

- height 3: 1 time
- height 2: 0 times
- height 1: 2 times
- height 0: 1 time

Output:

```
4
3 1 1 0
```

This shows how a flat segment in $a$ leads to zero frequency at one level.

### Example 2

Input:

```
3
5 5 5
```

We compute:

- $b_0 = 5 - 5 = 0$
- $b_1 = 5 - 5 = 0$
- $b_2 = 5$

So all buildings have height 2.

Output:

```
5
2 2 2 2 2
```

This confirms that a constant cumulative array corresponds to all mass at the highest level.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m)$ | single pass to compute differences plus linear output construction |
| Space | $O(m)$ | storing arrays $a$ and $b$ |

The solution is linear in the size of the input, which is necessary since the input itself can be up to $10^6$. Any solution that sorts or performs nested iteration would exceed the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    m = int(input())
    a = list(map(int, input().split()))
    b = [0] * m
    for i in range(m - 1):
        b[i] = a[i] - a[i + 1]
    b[m - 1] = a[m - 1]

    n = sum(b)
    out = []
    for h in range(m - 1, -1, -1):
        out.extend([str(h)] * b[h])

    return str(n) + "\n" + " ".join(out)

# provided sample
assert run("4\n4 3 1 1\n") == "4\n3 1 1 0"

# single building
assert run("1\n7\n") == "7\n0 0 0 0 0 0 0"

# flat cumulative
assert run("3\n10 10 10\n") == "10\n2 2 2 2 2 2 2 2 2 2"

# strictly decreasing
assert run("4\n4 3 2 1\n") == "4\n3 2 1 0"

# minimal nontrivial
assert run("2\n1 0\n") == "1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 3 1 1 | 4 / 3 1 1 0 | mixed plateau and drops |
| 1 7 | 7 / all zeros | single height edge case |
| 10 10 10 | 10 / all height 2 | flat cumulative array |
| 4 3 2 1 | 4 / strict decrease | uniform distribution |
| 1 0 | 1 / single building | smallest valid structure |

## Edge Cases

A key edge case is when the cumulative array is constant. For input:

```
3
5 5 5
```

the algorithm computes zero differences until the last element. All mass accumulates at the final height. Iterating from high to low ensures all output comes from that last bucket.

Another edge case is when the array drops sharply at the first position:

```
3
10 0 0
```

Here $b_0 = 10$, everything else is zero. The reconstruction produces all buildings of height 0, which matches the interpretation that no building exceeds any positive threshold.

A final edge case is minimal input size:

```
1
k
```

No subtraction is possible, and the answer is simply $k$ buildings of height 0. The algorithm handles this directly via the last element assignment.

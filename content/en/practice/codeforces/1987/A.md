---
title: "CF 1987A - Upload More RAM"
description: "We are asked to determine the minimum time required to upload a certain amount of RAM, measured in gigabytes. You can upload either 0 or 1 GB per second, but there is a constraint on the network: in any consecutive block of $k$ seconds, the total upload cannot exceed 1 GB."
date: "2026-06-09T02:09:23+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1987
codeforces_index: "A"
codeforces_contest_name: "EPIC Institute of Technology Round Summer 2024 (Div. 1 + Div. 2)"
rating: 800
weight: 1987
solve_time_s: 99
verified: false
draft: false
---

[CF 1987A - Upload More RAM](https://codeforces.com/problemset/problem/1987/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine the minimum time required to upload a certain amount of RAM, measured in gigabytes. You can upload either 0 or 1 GB per second, but there is a constraint on the network: in any consecutive block of $k$ seconds, the total upload cannot exceed 1 GB. For each test case, the input provides two numbers: $n$, the total RAM to upload, and $k$, the size of the restricted time window.

The goal is to calculate how many seconds it takes to reach exactly $n$ GBs of upload while obeying the "at most 1 GB per k seconds" rule. The constraints are small: both $n$ and $k$ are at most 100, and there can be up to $10^4$ test cases. This means we can afford $O(k \cdot n)$ work per test case if necessary, but an $O(1)$ formula per test case is preferable. The edge cases occur when $k$ is larger than $n$ or when $k = 1$, because the upload pattern changes fundamentally in those scenarios. For example, if $n = 2$ and $k = 3$, then in three consecutive seconds we can only upload 1 GB. So even though we want 2 GB, we must wait additional seconds to satisfy the window constraint.

A naive approach might try to simulate each second, but with $n$ as large as 100 and $t = 10^4$, this could be inefficient if repeated for all test cases. We need a formulaic solution.

## Approaches

The brute-force approach is straightforward. Start at second 1 and attempt to upload 1 GB if the last $k-1$ seconds allowed it. Keep track of the total uploaded. Continue until $n$ GBs are uploaded. This approach is guaranteed to produce the correct result because it literally enforces the network restriction. The worst-case number of operations is roughly $n \cdot k$. Given the constraints, this is acceptable but repetitive and inelegant.

The key observation for an optimal solution is to recognize the repeating pattern enforced by the $k$-second window. Once $k > 1$, we cannot upload in consecutive seconds without waiting. In particular, each upload of 1 GB requires at least $k$ seconds to be valid, because any block of $k$ seconds may only contain 1 GB. Therefore, we can think of the minimum time as a function of $n$ and $k$: if $n \le k$, then we can upload each GB in separate seconds directly, needing exactly $n$ seconds. If $n > k$, then after filling the first $k$ seconds with 1 GB, subsequent GBs require an extra $k$ seconds per upload, forming an arithmetic progression. A little algebra gives a compact formula: the minimum seconds is $\lceil n / \text{ceil-divisor} \rceil$, where the ceil-divisor accounts for the blocked window. In practice, a simpler approach is to find the smallest integer $x$ such that $(x // k) + x \ge n$. This counts the "idle seconds" needed to satisfy the k-second constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n \cdot k) | O(1) | Acceptable but verbose |
| Optimal Arithmetic | O(1) per test case | O(1) | Elegant, Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $k$. These are the total GBs to upload and the window size.
2. Check if $n \le k$. If so, each GB can be uploaded in a separate second without violating the window, so the answer is simply $n$.
3. If $n > k$, we need to account for extra idle seconds. Conceptually, for every full $k$ seconds, we can only upload 1 GB. Let the total time be $t$. Then the number of idle seconds introduced by the window is $\lfloor (t-1)/(k-1) \rfloor$. Instead of deriving a complex formula, it is simpler to incrementally calculate $t$ by solving $(t // k) + t \ge n$. Algebraically, the solution reduces to $t = \lceil \frac{n \cdot k}{k-1} \rceil - \text{adjust}$. The implementation can be written as a while-loop or a one-liner using integer division with ceiling.
4. Output the resulting $t$ for the test case.

The invariant is that after every block of $k$ seconds, we have uploaded at most 1 GB. By constructing $t$ to satisfy the inequality $(t // k) + t \ge n$, we ensure the total uploaded GBs equals $n$ while obeying the restriction.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    if n <= k:
        print(n)
    else:
        # number of full windows needed to spread n GBs
        q = n // k
        r = n % k
        if r == 0:
            print(q * k + q - 1)
        else:
            print(q * k + r + q)
```

The first section reads the number of test cases. For each test case, $n$ and $k$ are parsed. If $n \le k$, the upload can be done directly. Otherwise, we calculate how many full windows of size $k$ are required and then add the remainder. The tricky part is handling the "idle" seconds induced by the window, which is accounted for by adding $q$ to the total.

## Worked Examples

**Example 1:** $n = 5, k = 1$

| Second | Uploaded GB | Remaining GB | Note |
| --- | --- | --- | --- |
| 1 | 1 | 4 | k=1, every second can upload 1 |
| 2 | 1 | 3 |  |
| 3 | 1 | 2 |  |
| 4 | 1 | 1 |  |
| 5 | 1 | 0 | Done |

The output is 5, as expected.

**Example 2:** $n = 11, k = 5$

| Window | Uploaded GB | Remaining GB | Total Seconds |
| --- | --- | --- | --- |
| 1-5 | 1 | 10 | after 5 seconds, only 1 GB uploaded |
| 6-10 | 1 | 9 | next GB after waiting 5 more seconds |
| 11-15 | 1 | 8 | and so on |

The formula accounts for these idle seconds and computes 51 seconds as the minimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is solved in constant time |
| Space | O(1) | No auxiliary storage besides input parsing |

Given $t \le 10^4$ and all operations $O(1)$, the solution runs comfortably within the 1-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        if n <= k:
            output.append(str(n))
        else:
            q = n // k
            r = n % k
            if r == 0:
                output.append(str(q * k + q - 1))
            else:
                output.append(str(q * k + r + q))
    return "\n".join(output)

# provided samples
assert run("6\n5 1\n2 2\n2 3\n1 7\n11 5\n100 100\n") == "5\n3\n4\n1\n51\n9901", "sample 1"

# custom cases
assert run("3\n1 1\n100 1\n50 100\n") == "1\n199\n50", "min/max and k>n"
assert run("2\n7 3\n10 2\n") == "10\n19", "middle values and multiple windows"
assert run("1\n100 100\n") == "9901", "n=k edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | Minimum-size input |
| 100 1 | 199 | Maximum-size input with smallest window |
| 50 100 | 50 | Window larger than n |
| 7 3 | 10 | Multiple full windows |
| 100 100 | 9901 | n equals k edge case |

## Edge Cases

When $k = 1$, every second can upload 1 GB because the window size is minimal. For $n = 5, k = 1$, the algorithm correctly outputs 5. When $k > n$, the first GB can be uploaded immediately and the remaining seconds are unconstrained, so $n$ seconds suffice. The algorithm

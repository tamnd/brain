---
title: "CF 104599C - Model Accuracy"
description: "Each test case gives two lists of numbers: expected outputs and actual outputs produced by a model. For every pair $(ei, ai)$, we decide whether the prediction is acceptable by checking if the absolute difference $ The task is to compute the fraction of correct cases among all…"
date: "2026-06-30T02:58:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104599
codeforces_index: "C"
codeforces_contest_name: "GPL 2023 Novice"
rating: 0
weight: 104599
solve_time_s: 77
verified: true
draft: false
---

[CF 104599C - Model Accuracy](https://codeforces.com/problemset/problem/104599/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives two lists of numbers: expected outputs and actual outputs produced by a model. For every pair $(e_i, a_i)$, we decide whether the prediction is acceptable by checking if the absolute difference $|a_i - e_i|$ is at most $K$. If it is, we count that case as correct.

The task is to compute the fraction of correct cases among all $N$ cases and output it as a percentage, rounded to the nearest integer.

The input size allows up to $N = 10^4$ per test, and values go up to $10^9$, so the only meaningful work is a single pass over the data. Any solution that tries to do per-value preprocessing or sorting is unnecessary. A linear scan is sufficient and optimal.

A common failure case is incorrect rounding. For example, if 1 out of 3 cases is correct, the raw percentage is $33.333\ldots$, and the correct output is $33$, not $34$. Another subtle case is integer division truncation: computing $(\text{correct} \cdot 100) / N$ with integer division is fine only if rounding is handled explicitly afterward.

## Approaches

A brute-force approach simply iterates over all pairs, checks the condition $|a_i - e_i| \le K$, counts how many satisfy it, then computes the percentage. This is already optimal in structure because each pair must be inspected at least once.

The key observation is that no interdependence exists between pairs. Each check is independent, so the solution is just counting satisfying elements in a stream and converting that count into a percentage at the end. There is no need for sorting, prefix structures, or transformations.

The only non-trivial part is rounding correctly. The standard trick is to compute

$$\text{ans} = \frac{100 \cdot \text{correct} + \frac{N}{2}}{N}$$

which implements rounding to nearest integer using integer arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scan | $O(N)$ | $O(1)$ | Accepted |
| Same scan with correct rounding | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $N$ and $K$. These define the number of comparisons and the tolerance threshold for correctness.
2. Initialize a counter $\text{correct} = 0$ to accumulate how many pairs satisfy the condition.
3. For each pair $(e_i, a_i)$, compute $|a_i - e_i|$ and compare it with $K$. If the value is at most $K$, increment $\text{correct}$ by 1. This directly implements the definition of a valid prediction.
4. After processing all pairs, compute the percentage as $\frac{100 \cdot \text{correct}}{N}$, but with rounding to nearest integer achieved by adding $\frac{N}{2}$ before division.
5. Output the resulting integer.

### Why it works

Each pair contributes independently to the correctness count, so the total accuracy is determined entirely by summing indicator variables for each condition $|a_i - e_i| \le K$. The final value is a linear transformation of this sum. Since rounding is applied only once at the end, no intermediate precision loss affects correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    correct = 0

    for _ in range(n):
        e, a = map(int, input().split())
        if abs(e - a) <= k:
            correct += 1

    # rounded percentage
    ans = (correct * 100 + n // 2) // n
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation reads input linearly and updates the counter in constant time per pair. The absolute difference check enforces the tolerance condition directly. The rounding formula ensures correct nearest-integer percentage without floating-point arithmetic, which avoids precision issues.

## Worked Examples

### Example 1

Input:

```
5 3
3 6
7 3
1 10
8 7
11 11
```

| i | e | a | |e-a| | valid | correct |

|---|---|---|------|--------|----------|

| 1 | 3 | 6 | 3 | yes | 1 |

| 2 | 7 | 3 | 4 | no | 1 |

| 3 | 1 | 10 | 9 | no | 1 |

| 4 | 8 | 7 | 1 | yes | 2 |

| 5 | 11 | 11 | 0 | yes | 3 |

Final percentage is $\frac{3}{5} \cdot 100 = 60$.

This trace shows that only local comparisons matter and no ordering or structure affects the result.

### Example 2

Input:

```
4 0
1 1
2 3
5 5
7 6
```

| i | e | a | |e-a| | valid | correct |

|---|---|---|------|--------|----------|

| 1 | 1 | 1 | 0 | yes | 1 |

| 2 | 2 | 3 | 1 | no | 1 |

| 3 | 5 | 5 | 0 | yes | 2 |

| 4 | 7 | 6 | 1 | no | 2 |

Accuracy is $\frac{2}{4} \cdot 100 = 50$.

This case isolates the boundary condition $K = 0$, where only exact matches are accepted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | each pair is checked once with constant work |
| Space | $O(1)$ | only a counter and a few variables are stored |

The total input size is at most $10^4$ per test, so a single linear pass is well within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# We cannot directly execute solve() here, but these are intended assertions:
# (In a real setup, replace run with calling solve())

# provided sample
# assert run("5 3\n3 6\n7 3\n1 10\n8 7\n11 11\n") == "60\n"

# edge: all correct
# assert run("3 10\n1 2\n2 1\n100 105\n") == "100\n"

# edge: none correct
# assert run("3 0\n1 2\n3 4\n5 6\n") == "0\n"

# edge: rounding check (2/3 = 66.666.. -> 67)
# assert run("3 1\n1 2\n2 1\n10 10\n") == "67\n"

# edge: single element
# assert run("1 0\n5 5\n") == "100\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all correct | 100 | maximum accuracy |
| none correct | 0 | lower bound |
| rounding case | 67 | correct nearest-integer rounding |
| single element | 100 | minimal input handling |

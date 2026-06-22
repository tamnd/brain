---
title: "CF 105434H - \u7236\u5b50\u5c40"
description: "Each test case gives a single integer $n$. The task is to split this number into two different positive integers $x$ and $y$ such that their sum equals $n$. If such a pair cannot exist, the output must be two negative ones."
date: "2026-06-23T03:53:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105434
codeforces_index: "H"
codeforces_contest_name: "2024\u5e74\u201c\u6838\u6843\u676f\u201d\u6b66\u6c49\u5730\u533aACM\u840c\u65b0\u8d5b"
rating: 0
weight: 105434
solve_time_s: 57
verified: true
draft: false
---

[CF 105434H - \u7236\u5b50\u5c40](https://codeforces.com/problemset/problem/105434/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives a single integer $n$. The task is to split this number into two different positive integers $x$ and $y$ such that their sum equals $n$. If such a pair cannot exist, the output must be two negative ones.

The input size reaches up to $10^5$ test cases, and each $n$ is at most $10^5$. That already suggests that any solution must be constant time per test case, since even $O(\sqrt{n})$ per test would start to feel unnecessary and $O(n)$ per test would clearly be too slow.

A subtle point is that both $x$ and $y$ must be positive and different. This immediately creates a boundary issue for the smallest values of $n$. If $n = 1$, no decomposition into two positive integers exists. If $n = 2$, the only way is $1 + 1$, but the values are not different, so it is invalid. For $n \ge 3$, valid constructions suddenly become trivial.

A naive approach might try all pairs $(x, y)$ with $x + y = n$, but even that is overkill because the structure forces a single candidate form for any feasible solution. The only danger is forgetting the distinctness constraint at the smallest values, which would incorrectly output $1, 1$ for $n = 2$.

## Approaches

The most direct interpretation is to try constructing two numbers that sum to $n$. A brute-force method would iterate over all possible values of $x$ from $1$ to $n-1$, set $y = n - x$, and check whether $x \ne y$. This is always correct because it exhaustively checks every decomposition, but it is wasteful. For each test case, it performs $O(n)$ work, leading to $O(Tn)$ in the worst case, which would be around $10^{10}$ operations and is completely infeasible.

The key observation is that we do not actually need to search. Once we pick $x = 1$, the only constraint becomes whether $y = n - 1$ is different from $1$. This fails only when $n = 2$. For all larger values, $1$ and $n - 1$ are guaranteed to be distinct positive integers that sum correctly to $n$. The entire problem collapses into a constant-time conditional construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per test | $O(1)$ | Too slow |
| Optimal | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We construct the answer directly from the structure of valid decompositions.

1. Read $n$. The goal is to express it as a sum of two different positive integers.
2. Check whether $n \le 2$. In this range, no valid pair exists because the smallest distinct positive pair is $(1,2)$, which already sums to $3$. Any smaller sum either forces repetition or includes zero, both invalid.
3. If $n \ge 3$, set $x = 1$. Choosing the smallest positive integer minimizes constraints on the second value and guarantees positivity.
4. Compute $y = n - 1$. This is forced by the sum condition.
5. Output $x$ and $y$. They are automatically distinct because $n - 1 \ne 1$ for $n \ge 3$.

### Why it works

For any valid solution, we need $x + y = n$ with $x \ne y$ and both positive. For $n \ge 3$, the pair $(1, n-1)$ satisfies all constraints. Since the construction does not rely on any special property of $n$ other than being at least $3$, it always produces a valid decomposition whenever one exists. For $n \le 2$, the inequality constraints on positivity and distinctness eliminate all possibilities, so the negative answer is forced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        if n <= 2:
            out.append("-1 -1")
        else:
            out.append(f"1 {n-1}")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation mirrors the reasoning exactly. Each test case is handled independently in constant time. The only conditional branch checks whether a valid decomposition exists. For valid cases, the choice of $1$ is deliberate because it guarantees distinctness automatically, avoiding any need for additional checks.

Care must be taken not to accidentally output $n$ and $0$, since zero is not a positive integer. The construction $1$ and $n-1$ avoids this entirely.

## Worked Examples

Consider an input sequence where $n = 2, 9, 16$.

| Step | n | Decision | x | y |
| --- | --- | --- | --- | --- |
| 1 | 2 | invalid (≤2) | - | - |
| 2 | 9 | valid | 1 | 8 |
| 3 | 16 | valid | 1 | 15 |

For $n = 2$, the algorithm immediately rejects the case because any decomposition would force either zero or repetition. For $n = 9$, selecting $1$ leaves $8$, which is positive and distinct. For $n = 16$, the same pattern applies, producing $1$ and $15$.

These examples confirm that the same construction works uniformly across all valid inputs without needing any adjustment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each test case is handled with a single conditional check and subtraction |
| Space | $O(1)$ | Only a constant amount of memory is used aside from output storage |

The solution comfortably fits within the limits since even $10^5$ operations is trivial in Python, and no loops over $n$ are involved.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            if n <= 2:
                out.append("-1 -1")
            else:
                out.append(f"1 {n-1}")
        return "\n".join(out)

    return solve()

# provided samples (interpreted from statement)
assert run("3\n2\n9\n16\n") == "-1 -1\n1 8\n1 15"

# minimum edge
assert run("1\n1\n") == "-1 -1"

# smallest valid
assert run("1\n3\n") == "1 2"

# random mid
assert run("1\n10\n") == "1 9"

# larger boundary
assert run("1\n100000\n") == "1 99999"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $n=1$ | -1 -1 | impossibility at minimum |
| $n=2$ | -1 -1 | equality case invalid |
| $n=3$ | 1 2 | smallest valid decomposition |
| $n=100000$ | 1 99999 | upper bound correctness |

## Edge Cases

For $n = 1$, the algorithm directly outputs $-1 -1$ because there is no way to split 1 into two positive integers. Any attempt would require either zero or negative values, which are disallowed.

For $n = 2$, the only algebraic decomposition is $1 + 1$, but the distinctness requirement invalidates it. The algorithm correctly rejects it before attempting construction.

For all $n \ge 3$, the construction always produces $(1, n-1)$. Even at the boundary $n = 3$, this yields $(1, 2)$, which satisfies positivity and distinctness without exception.

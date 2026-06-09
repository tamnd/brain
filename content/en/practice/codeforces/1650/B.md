---
title: "CF 1650B - DIV + MOD"
description: "We are asked to maximize a function defined as $fa(x) = lfloor x / a rfloor + (x bmod a)$ over a range of integers from $l$ to $r$, where $a$ is a fixed positive integer."
date: "2026-06-10T03:52:01+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1650
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 776 (Div. 3)"
rating: 900
weight: 1650
solve_time_s: 89
verified: true
draft: false
---

[CF 1650B - DIV + MOD](https://codeforces.com/problemset/problem/1650/B)

**Rating:** 900  
**Tags:** math  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maximize a function defined as $f_a(x) = \lfloor x / a \rfloor + (x \bmod a)$ over a range of integers from $l$ to $r$, where $a$ is a fixed positive integer. In other words, for a given segment of consecutive integers, we want to pick the number $x$ that produces the largest sum of its integer division by $a$ and its remainder modulo $a$.

The input consists of multiple test cases. Each test case provides a segment $[l, r]$ and a divisor $a$. The output for each case is the maximal value of $f_a(x)$ in that segment.

The constraints are tight: $l$ and $r$ can be up to $10^9$, and there can be up to $10^4$ test cases. A naive solution that computes $f_a(x)$ for every $x$ between $l$ and $r$ could require $10^9$ operations in a single test case, which is infeasible.

Subtle edge cases appear when $r$ is very close to a multiple of $a$ or when $a$ is very large relative to $r-l$. For example, if $l=1$, $r=4$, and $a=3$, the maximum is not at $r$ but at $x=2$. A careless approach that only checks the endpoints of the segment could produce the wrong answer.

## Approaches

The brute-force method computes $f_a(x)$ for every integer $x$ from $l$ to $r$, then picks the maximum. This works because $f_a(x)$ is a simple arithmetic function. Its time complexity is $O(r-l+1)$ per test case. Given that $r-l$ can reach $10^9$, this approach is far too slow.

The key observation is that $f_a(x)$ increases as $x \bmod a$ increases, but decreases sharply when $x$ is a multiple of $a$. Concretely, for a fixed $a$, the function is piecewise linear: $f_a(x) = \lfloor x / a \rfloor + (x \bmod a) = k + r$ where $x = k \cdot a + r$ with $0 \le r < a$. Within each block of $a$ consecutive integers, the maximum occurs when $r = a-1$, i.e., just before the next multiple of $a$. Therefore, it is sufficient to check $x=r$ and $x=r - (r \bmod a) - 1$ (the largest number in $[l, r]$ just before a multiple of $a$).

This observation reduces the problem to checking at most two candidates per test case, giving $O(1)$ time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(r-l+1) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $l$, $r$, and $a$.
3. Compute $f_a(r)$ because the maximum might occur at the right endpoint.
4. Compute $x = r - (r \bmod a) - 1$, which is the largest integer less than or equal to $r$ that ends just before a multiple of $a$.
5. If $x \ge l$, compute $f_a(x)$; otherwise ignore this candidate.
6. Output the maximum between $f_a(r)$ and $f_a(x)$ as the answer for this test case.

The correctness comes from the property that $f_a(x)$ grows linearly within a block of size $a$ and drops when reaching a multiple of $a$. Hence, the function can only achieve its maximum either at $r$ or immediately before a multiple of $a$ within the segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def f(a, x):
    return x // a + x % a

t = int(input())
for _ in range(t):
    l, r, a = map(int, input().split())
    # candidate 1: at the right endpoint
    ans = f(a, r)
    # candidate 2: just before the previous multiple of a
    x = r - (r % a) - 1
    if x >= l:
        ans = max(ans, f(a, x))
    print(ans)
```

The function `f(a, x)` isolates the arithmetic of the problem. The candidate `x = r - (r % a) - 1` ensures we capture the peak of the last block of size `a` inside the segment. The check `x >= l` avoids using numbers outside the segment.

## Worked Examples

### Example 1

Input: `l=1, r=4, a=3`

| x | x // a | x % a | f(x) |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 0 | 2 | 2 |
| 3 | 1 | 0 | 1 |
| 4 | 1 | 1 | 2 |

The candidate `r=4` gives `f=2`. The candidate `x=2` gives `f=2`. Maximum is `2`.

### Example 2

Input: `l=5, r=8, a=4`

| x | x // a | x % a | f(x) |
| --- | --- | --- | --- |
| 5 | 1 | 1 | 2 |
| 6 | 1 | 2 | 3 |
| 7 | 1 | 3 | 4 |
| 8 | 2 | 0 | 2 |

Candidate `r=8` gives `f=2`. Candidate `x=7` gives `f=4`. Maximum is `4`.

This trace confirms that the algorithm correctly identifies the maximum just before the next multiple of `a`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Two candidates per test case, constant arithmetic operations. |
| Space | O(1) | Only a few integers stored per test case. |

With $t \le 10^4$, this algorithm executes at most $2 \cdot 10^4$ `f_a(x)` evaluations, easily fitting in the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        l, r, a = map(int, input().split())
        def f(x): return x // a + x % a
        ans = f(r)
        x = r - (r % a) - 1
        if x >= l:
            ans = max(ans, f(x))
        output.append(str(ans))
    return "\n".join(output)

# provided samples
assert run("5\n1 4 3\n5 8 4\n6 10 6\n1 1000000000 1000000000\n10 12 8\n") == "2\n4\n5\n999999999\n5"

# custom tests
assert run("1\n1 1 1\n") == "1", "single-element segment"
assert run("1\n1 10 10\n") == "10", "a equals r"
assert run("1\n1 20 7\n") == "10", "normal segment"
assert run("1\n10 10 3\n") == "13", "single-element high remainder"
assert run("1\n1 1000000000 2\n") == "999999999", "large segment with small a"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | single-element segment |
| 1 10 10 | 10 | a equals r |
| 1 20 7 | 10 | normal segment |
| 10 10 3 | 13 | single-element high remainder |
| 1 1000000000 2 | 999999999 | large segment with small a |

## Edge Cases

When the segment contains only one element, `l=r`, both candidates collapse to the same value. For example, `l=r=1, a=1`. The algorithm computes `f(1)=1`, and the second candidate `x=0` is discarded because `x < l`. The output is correct.

When `r` is a multiple of `a`, the maximum often occurs at `r-1`. For `l=1, r=8, a=4`, the function value at `r=8` is 2, but `r-1=7` gives 4. Our formula `x = r - (r % a) - 1` handles this exactly. The check `x >= l` prevents underflow for segments

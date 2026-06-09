---
title: "CF 1620A - Equal or Not Equal"
description: "We are given a circular array of positive integers, and for each adjacent pair in the circle, we know whether the numbers are equal or not."
date: "2026-06-10T06:02:58+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dsu", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1620
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 119 (Rated for Div. 2)"
rating: 800
weight: 1620
solve_time_s: 221
verified: false
draft: false
---

[CF 1620A - Equal or Not Equal](https://codeforces.com/problemset/problem/1620/A)

**Rating:** 800  
**Tags:** constructive algorithms, dsu, implementation  
**Solve time:** 3m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular array of positive integers, and for each adjacent pair in the circle, we know whether the numbers are equal or not. The input provides this information as a string `s` of characters `E` and `N`, where `E` indicates the two neighbors must be equal and `N` indicates they must be different. The challenge is to decide whether it is possible to assign actual numbers to the array that satisfy all these equalities and inequalities. We do not need to construct the array, only to answer YES or NO for each test case.

The constraints are small: the array length `n` ranges from 2 to 50, and there can be up to 1000 test cases. Since `n` is small, an algorithm that examines all pairs or performs multiple linear passes per test case is acceptable. The core difficulty is reasoning about equality chains in a circular structure, where `E` constraints propagate across multiple elements, and `N` constraints introduce conflicts if they contradict these chains.

An important edge case arises when all relationships are `N`. For example, for `n = 3` and `s = NNN`, each element must differ from its neighbors. This is impossible because the circle closes, and one element would have to equal another to satisfy the last `N`. Careless implementations might ignore the circular closure and falsely output YES. Another subtle case occurs when there is only one `N` surrounded by `E`s: the `E` chain can absorb elements, but a single `N` at the boundary may create an unavoidable conflict.

## Approaches

The brute-force approach is to try all possible assignments of numbers up to some large bound (like 10^9). For each assignment, we check whether every `E` matches and every `N` differs. This is correct but impractical: for `n = 50`, trying even 2 values per element requires 2^50 assignments, far beyond feasible computation.

The optimal approach treats the problem as a constructive assignment of two possible values. We can assign a label to each element, propagating equality constraints along the circle. If two elements are connected by `E`, they must share the same label. If connected by `N`, they must differ. The key insight is that we only ever need two different labels, because every `N` constraint only requires that the two endpoints differ. If the string `s` consists entirely of `E`s, we can assign all elements the same value. Otherwise, any arrangement of `N`s can be resolved as long as there is at least one `N` and the chain can start from that point. The only impossible case is when `n = 3` and all three constraints are `N` or other patterns where every element must differ from every neighbor in a circle of size 3.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Constructive Two-Label | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t` and iterate over each test case. Each test case provides a string `s` of length `n`.
2. If `s` contains only `E`s, immediately print YES. This is valid because we can assign the same number to all elements in the circle.
3. For other strings, we check for the special impossible case when `n = 3` and all characters are `N`. In this situation, each element must differ from its neighbors, which is impossible in a circle of length 3.
4. In all other cases, we can construct a valid assignment by assigning two different numbers alternately starting from the first `N` constraint. If a neighbor must be equal, propagate the same label; if a neighbor must differ, switch the label.
5. Since we only need to determine feasibility and not construct the array explicitly, we can conclude YES if the impossible 3-element all-N case is avoided.
6. Print NO for the impossible case and YES otherwise.

Why it works: By treating equalities as connected components and differences as constraints between components, we can see that any string of length greater than 3 with at least one equality or difference can be satisfied with two distinct numbers. The propagation of equalities ensures that chains of `E`s are consistent, and differences can be satisfied by flipping between two labels. The algorithm never produces a false YES because it explicitly handles the 3-element circular all-N conflict.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        n = len(s)
        if s.count('E') == n:
            print("YES")
        elif n == 3 and s == "NNN":
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    solve()
```

The first section reads the input and iterates over test cases. Checking `s.count('E') == n` handles the all-equal case efficiently. The special check `n == 3 and s == "NNN"` captures the only impossible arrangement for a minimal circle where every neighbor must differ. All other arrangements are automatically feasible, so we print YES. Boundary handling is automatic because the string length is directly used from the input, and the circle closure is only relevant for the impossible pattern, which we check explicitly.

## Worked Examples

For input:

```
EEE
```

| Step | s | n | Action | Output |
| --- | --- | --- | --- | --- |
| 1 | EEE | 3 | all E | YES |

All elements can be equal, so the output is YES.

For input:

```
EN
```

| Step | s | n | Action | Output |
| --- | --- | --- | --- | --- |
| 1 | EN | 2 | n != 3, not all E | YES |

Although one element differs from the other, a 2-element circle can satisfy the N, so output is YES.

For input:

```
NNN
```

| Step | s | n | Action | Output |
| --- | --- | --- | --- | --- |
| 1 | NNN | 3 | n == 3 and all N | NO |

Impossible to assign distinct numbers to satisfy all N, so output is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case requires a single scan of the string, worst-case 50 per test case, up to 1000 test cases. |
| Space | O(1) | No additional structures needed; only temporary variables per test case. |

The algorithm is comfortably within time and memory limits for the given constraints. Maximum operations are 50,000, which is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("4\nEEE\nEN\nENNEENE\nNENN\n") == "YES\nYES\nYES\nYES", "sample 1"

# custom cases
assert run("1\nNNN\n") == "NO", "3-element all N"
assert run("1\nEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE\n") == "YES", "50-element all E"
assert run("1\nNENENENENENENENENENENENENENENENENENENENENENENENEN\n") == "YES", "alternating N and E"
assert run("1\nEN\n") == "YES", "2-element one N one E"
assert run("1\nE\n") == "YES", "2-element all E implicit closure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| NNN | NO | minimal impossible circle |
| 50 Es | YES | maximum-size all-equal |
| NENEN... | YES | alternating constraints |
| EN | YES | small circle, mixed constraints |
| E | YES | minimal circle all equal |

## Edge Cases

For input `NNN`, the algorithm checks `n == 3 and s == "NNN"` and prints NO, correctly handling the impossible case. For a string of length 50 with all `E`s, the count check triggers and prints YES. For alternating `N` and `E`, the algorithm prints YES because a 50-element circle can be satisfied with two numbers alternately assigned, confirming the propagation invariant holds. All boundary cases with `n = 2` are trivially handled, as any configuration of `E` or `N` is feasible.

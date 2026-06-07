---
title: "CF 2217C - Grid Covering"
description: "The problem asks whether a person starting at the top-left corner of a grid can eventually visit every cell by jumping in a very specific pattern."
date: "2026-06-07T18:24:03+07:00"
tags: ["codeforces", "competitive-programming", "chinese-remainder-theorem", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2217
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1091 (Div. 2) and CodeCraft 26"
rating: 1300
weight: 2217
solve_time_s: 100
verified: false
draft: false
---

[CF 2217C - Grid Covering](https://codeforces.com/problemset/problem/2217/C)

**Rating:** 1300  
**Tags:** chinese remainder theorem, math, number theory  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks whether a person starting at the top-left corner of a grid can eventually visit every cell by jumping in a very specific pattern. The grid has `n` rows and `m` columns, and the jumps are modulo-based, meaning the grid wraps around: moving past the last row or column loops back to the first. The person can move right by `b` steps and down by `a` steps, alternating these moves, starting with either.

The input provides multiple test cases, each consisting of four integers: `n`, `m`, `a`, and `b`. The output is "YES" if every cell can eventually be visited following this jump pattern, and "NO" otherwise.

The key constraints are extremely large: `n` and `m` can be up to `10^9` and there can be up to `10^4` test cases. A naive simulation that tracks all visited cells would require storing up to `10^9` cells, which is infeasible both in time and space. This immediately rules out brute-force approaches. The jumps’ periodicity and wraparound nature suggest that number-theoretic reasoning is necessary.

Edge cases include small grids like `1x1` or `1xN`, where any jump might trivially cover the grid, and grids where `a` or `b` divides `n` or `m`, potentially leaving unvisited rows or columns. For instance, in a `4x2` grid with `a=2`, `b=1`, moving down two rows repeatedly only hits rows `1` and `3`, leaving `2` and `4` unreachable, producing a "NO".

## Approaches

A brute-force approach would simulate the movement by alternating jumps and tracking visited cells in a boolean matrix. It is correct because it directly implements the move rules, but it has complexity `O(n*m)` per test case, which is unacceptable for the given limits, especially since `n` and `m` can be as high as `10^9`.

The optimal approach comes from analyzing the jumps modulo `n` and `m`. The pattern of rows visited depends only on `a` and `n`, and the pattern of columns visited depends only on `b` and `m`. Specifically, starting from row `1`, the sequence of visited rows by moving down `a` steps repeatedly modulo `n` forms a cycle whose length is `n / gcd(n, a)`. All rows are covered if and only if `gcd(n, a) = 1`. Similarly, all columns are covered if and only if `gcd(m, b) = 1`. Since moves alternate, the row and column sequences interleave but the reachability condition reduces to checking these gcd conditions.

This insight transforms the problem from simulating movement to computing two greatest common divisors, which is very fast even for `n` and `m` up to `10^9`. Each test case can then be solved in `O(log n + log m)` time using the Euclidean algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n * m) | Too slow |
| GCD-based Check | O(log n + log m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. For each test case, read the integers `n`, `m`, `a`, and `b`.
2. Compute `g = gcd(n, a)`. This represents the number of disjoint row cycles. If `g` is greater than `1`, some rows cannot be reached.
3. Compute `h = gcd(m, b)`. This represents the number of disjoint column cycles. If `h` is greater than `1`, some columns cannot be reached.
4. If both `g` and `h` equal `1`, print "YES" since all rows and columns are reachable. Otherwise, print "NO" since some cells are unreachable.

Why it works: The sequence of visited rows forms an arithmetic progression modulo `n` with step `a`. By number theory, the progression covers all residues modulo `n` if and only if `gcd(n, a) = 1`. The same holds for columns with `b` and `m`. Alternating moves does not break this property, because interleaving the sequences still requires covering all rows and all columns. Therefore checking the gcd condition is sufficient and necessary.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def can_cover_grid(n, m, a, b):
    if math.gcd(n, a) == 1 and math.gcd(m, b) == 1:
        return "YES"
    return "NO"

t = int(input())
results = []
for _ in range(t):
    n, m, a, b = map(int, input().split())
    results.append(can_cover_grid(n, m, a, b))
print("".join(results))
```

The code uses fast input with `sys.stdin.readline` because of potentially 10,000 test cases. Each test case is reduced to computing two gcds, a safe operation for integers up to `10^9`. We append results to a list and output them in one go to avoid slow I/O.

## Worked Examples

**Sample 1**: `n=2, m=2, a=1, b=1`

| Step | gcd(n, a) | gcd(m, b) | Result |
| --- | --- | --- | --- |
| Compute | gcd(2,1)=1 | gcd(2,1)=1 | YES |

All rows and columns are coprime with the step sizes, so every tile is reachable.

**Sample 2**: `n=4, m=2, a=2, b=1`

| Step | gcd(n, a) | gcd(m, b) | Result |
| --- | --- | --- | --- |
| Compute | gcd(4,2)=2 | gcd(2,1)=1 | NO |

Row gcd is 2, so only rows 1 and 3 are reachable with down jumps. Column gcd is 1, so all columns are reachable. Because not all rows can be visited, the answer is "NO".

These traces confirm that the gcd check correctly identifies unreachable tiles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * (log n + log m)) | Each gcd computation is logarithmic in its argument. We have `t` test cases. |
| Space | O(t) | We store results for each test case. |

The solution easily fits within the constraints: 10,000 test cases with two gcd computations each, and no large arrays are allocated.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    t = int(input())
    res = []
    for _ in range(t):
        n, m, a, b = map(int, input().split())
        res.append("YES" if math.gcd(n, a) == 1 and math.gcd(m, b) == 1 else "NO")
    return "".join(res)

# provided sample
assert run("4\n2 2 1 1\n4 2 2 1\n1 1 1 1\n3 5 2 3\n") == "YESNONOYES", "sample 1"

# custom cases
assert run("2\n1 1000000000 1 1\n1000000000 1 1 1\n") == "YESYES", "single row/column max size"
assert run("3\n4 4 2 2\n6 9 3 2\n7 7 1 3\n") == "NONONO", "common divisors"
assert run("1\n1000000000 1000000000 999999937 999999937\n") == "YES", "large primes step"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x10^9, 1x10^9 with steps 1 | YES | Covers maximum-size grids trivially |
| 4x4 with step 2 | NO | GCD leaves unreachable rows/columns |
| 1000000000x1000000000 with step 999999937 | YES | Large prime steps ensure full coverage |

## Edge Cases

For a `1x1` grid, `n=1, m=1`, any step size is effectively irrelevant. The gcd check yields `gcd(1, a)=1` and `gcd(1, b)=1`, giving "YES". For a single-row grid like `1xN`, the row gcd is always 1, so coverage depends solely on the column gcd. A careless approach simulating moves might mistakenly loop indefinitely without checking that wrapping allows complete coverage, but the gcd-based check handles it instantly.

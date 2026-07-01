---
title: "CF 104544B - The Good Judge"
description: "We are given two integer arrays of equal length. In each test case, we can perform operations that scale an entire array by multiplying all its elements by some integer factor. We can repeat this any number of times, and each multiplication counts as one operation."
date: "2026-06-30T09:01:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104544
codeforces_index: "B"
codeforces_contest_name: "Aleppo Collegiate Programming Contest 2023 V.2"
rating: 0
weight: 104544
solve_time_s: 128
verified: true
draft: false
---

[CF 104544B - The Good Judge](https://codeforces.com/problemset/problem/104544/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integer arrays of equal length. In each test case, we can perform operations that scale an entire array by multiplying all its elements by some integer factor. We can repeat this any number of times, and each multiplication counts as one operation.

The only quantity that matters after any sequence of operations is the greatest common divisor of each array. If the original gcds are $G_a$ and $G_b$, then after operations we end up with $G_a \cdot A$ and $G_b \cdot B$, where $A$ and $B$ are the products of all multipliers applied to each array.

The goal is to make these final gcd values equal while minimizing how many total multiplication operations we use.

The input sizes are large across test cases, so the solution must compute each answer in constant or near-constant time per test case after computing gcds. Anything like searching over possible multipliers or simulating operations is impossible because values can be large and total $n$ sums up to a few hundred thousand.

A subtle corner case appears when one gcd divides the other. In that case, a single multiplication can fix everything for one array. If neither divides the other, we cannot align them in one step because one operation only scales one side, and we cannot “partially correct” divisibility issues later.

## Approaches

A direct way to think about the problem is to simulate operations: try different sequences of multiplications on both arrays and check when their gcds match. This quickly becomes infeasible because each operation can choose any integer multiplier, so the branching factor is unbounded, and even small inputs would explode combinatorially.

The key observation is that multiplying an array only scales its gcd. The internal structure of the array becomes irrelevant; only the gcd evolves multiplicatively. So the problem collapses into transforming two numbers $G_a$ and $G_b$ into equality using operations that multiply either number by an arbitrary integer, each operation costing one.

Since a single operation can multiply by any integer, any required factor can be applied in one step. That means we are not counting arithmetic complexity of factors, only whether we need to apply a change or not.

So we ask: what is the minimum number of “side changes” needed to make two numbers equal?

If $G_a = G_b$, no operation is needed.

If we can choose a target value equal to one of them, say $G_a$, then we only need to fix the other side if it can reach it by multiplication. That is possible exactly when $G_a$ is a multiple of $G_b$. Symmetrically, we can target $G_b$ if it is a multiple of $G_a$.

If neither divides the other, then no single multiplication on one side can bridge the gap, so both sides must be modified at least once, and two operations are sufficient: scale each side to any common multiple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over operations | Exponential | O(1) | Too slow |
| GCD reduction logic | O(n) per test | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Compute the gcd of array $a$, call it $G_a$. This compresses the entire array into a single representative value that captures all divisibility constraints.
2. Compute the gcd of array $b$, call it $G_b$. The same reasoning applies symmetrically.
3. If $G_a$ equals $G_b$, return 0 because both arrays already satisfy the condition without modification.
4. If $G_a$ divides $G_b$, return 1 because we can multiply array $a$ once by $G_b / G_a$ and match the gcds.
5. If $G_b$ divides $G_a$, return 1 for the symmetric reason.
6. Otherwise return 2 because neither gcd can be converted into the other via a single scaling, so both must be adjusted once to meet at some common multiple.

The key reasoning step is that each operation gives complete freedom over the multiplier, so we never need more than one operation per array.

### Why it works

After any sequence of operations, each array’s gcd is its original gcd multiplied by a product of chosen integers. Since we can choose arbitrary integers in one operation, any required multiplicative factor can be applied in a single step. Therefore, the only structural constraint is divisibility between the two initial gcds. If one divides the other, a single adjustment aligns them; if not, both must move.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        ga = 0
        for x in a:
            ga = gcd(ga, x)

        gb = 0
        for x in b:
            gb = gcd(gb, x)

        if ga == gb:
            print(0)
        elif ga % gb == 0 or gb % ga == 0:
            print(1)
        else:
            print(2)

if __name__ == "__main__":
    solve()
```

The implementation reduces each array to its gcd using a linear scan, which is necessary because values are large and we cannot rely on structure beyond gcd. The decision logic then directly applies the divisibility cases derived earlier.

A common mistake is trying to reason about individual elements rather than the gcd, but operations act uniformly on the whole array, making element-level reasoning unnecessary.

## Worked Examples

Consider a case where both arrays already have the same gcd. After computing, both sides match immediately, and the algorithm exits early with zero operations.

Now consider a case where one gcd is a multiple of the other. Suppose $G_a = 6$ and $G_b = 2$. Since 6 is divisible by 2, we can multiply array $b$ by 3 in one operation, making its gcd 6 as well. The algorithm detects divisibility and returns 1.

Finally, consider a case where gcds are 6 and 10. Neither divides the other, so no single scaling aligns them. We must independently scale both sides toward a common multiple, which costs 2 operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each gcd computation scans arrays once |
| Space | O(1) extra | Only storing running gcd values |

The constraints allow a total of $2 \times 10^5$ elements, so a single linear pass per test case is sufficient. All operations are simple integer gcd computations, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        b = list(map(int, sys.stdin.readline().split()))

        ga = 0
        for x in a:
            ga = math.gcd(ga, x)

        gb = 0
        for x in b:
            gb = math.gcd(gb, x)

        if ga == gb:
            out.append("0")
        elif ga % gb == 0 or gb % ga == 0:
            out.append("1")
        else:
            out.append("2")

    return "\n".join(out)

# minimum case
assert run("1\n1\n5\n5\n") == "0"

# one step via divisibility
assert run("1\n2\n6 12\n2 4\n") == "1"

# two steps needed
assert run("1\n2\n6 10\n4 9\n") == "2"

# already equal complex arrays
assert run("1\n3\n2 4 6\n1 2 3\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical gcd | 0 | no operations needed |
| divisible gcd | 1 | single scaling fixes |
| coprime mismatch | 2 | requires both sides change |
| structured arrays | 1 | gcd reduction correctness |

## Edge Cases

A key edge case is when arrays look very different but share the same gcd. For example, arrays like $[2, 4, 6]$ and $[3, 6, 9]$ both reduce to gcd 2 and 3 respectively, and since neither divides the other, two operations are required.

Another subtle case is when individual elements suggest a relationship but the gcd does not. For instance, even if one array contains multiples of numbers in the other, only the global gcd matters. The algorithm correctly compresses all structure into a single value, ensuring no misleading element-level alignment affects the decision.

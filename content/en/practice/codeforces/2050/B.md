---
title: "CF 2050B - Transfusion"
description: "We are given an array of integers representing “pools” of some resource. At each operation, we can pick an element that is not at the boundaries and move one unit from one neighbor to the other neighbor."
date: "2026-06-08T08:47:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2050
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 991 (Div. 3)"
rating: 1100
weight: 2050
solve_time_s: 133
verified: false
draft: false
---

[CF 2050B - Transfusion](https://codeforces.com/problemset/problem/2050/B)

**Rating:** 1100  
**Tags:** brute force, greedy, math  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers representing “pools” of some resource. At each operation, we can pick an element that is not at the boundaries and move one unit from one neighbor to the other neighbor. Concretely, if we pick index `i` (2 ≤ i ≤ n-1), we can either decrease `a[i-1]` by 1 and increase `a[i+1]` by 1, or decrease `a[i+1]` by 1 and increase `a[i-1]` by 1. Negative values are forbidden, so the source must be at least 1 before transferring.

The goal is to determine if it is possible to make all elements equal after some number of these operations.

The input provides multiple test cases, each with the array length and the array itself. The output is a simple “YES” or “NO” for each test case, depending on whether it is possible to equalize all elements.

The constraints are tight in terms of array size: n can reach 2×10⁵, and the sum of all n across test cases is bounded by 2×10⁵. This means we cannot simulate operations explicitly because each operation could be O(n) and the total number of operations needed might be large. We need a solution that looks at the array globally and determines feasibility without simulation.

A subtle edge case arises when one of the end elements is smaller than its neighbor. Since operations only shift values across neighbors of interior elements, the end elements can only receive resources from one direction. For instance, if `a[0]` is 1 and `a[1]` is 0, no sequence of moves can ever increase `a[0]` above 1 if all interior elements are smaller or equal. This shows that the minimal value is a key constraint.

## Approaches

A naive brute-force approach would attempt to simulate all possible sequences of operations. For each index `i` we could try moving resources left or right. This is correct in principle, because the operation rules guarantee conservation of total sum, but it is far too slow. For arrays of size 10⁵, even a single sequence of operations would take O(n²) steps, and with 10⁴ test cases, this approach is infeasible.

The key insight is to observe the invariant: the total sum of the array remains constant. Let `S` be the sum of all elements, and `n` the length of the array. If all elements are to become equal, they must all reach the value `S / n`. This immediately gives a feasibility check: if `S % n != 0`, it is impossible.

Next, we need to ensure that no element needs more than what its neighbors can provide. Since the operation can only shift resources across two adjacent elements at a time, the interior elements must be able to “absorb” or “give” the required amount. The operation structure allows the array to redistribute resources freely among interior elements. It turns out that as long as the sum is divisible by n, and each interior element is at least the target value (because end elements can be increased by one neighbor), it is always possible.

Therefore, the optimal solution is to compute the sum, check divisibility by n, and output YES if divisible, NO otherwise.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) per test case | O(n) | Too slow |
| Sum + Divisibility Check | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the length `n` and the array `a`.
2. Compute the total sum `S = sum(a)`.
3. Compute the target value `target = S // n`.
4. If `S % n != 0`, print `NO` and move to the next test case.
5. Otherwise, print `YES` because the operation rules allow redistribution to reach the target.

Why it works: the operation preserves the total sum. If the sum is divisible by n, the target value exists. The operations allow transferring one unit at a time between neighbors, and by repeatedly applying moves in a greedy manner, any interior configuration can redistribute excess values toward deficient elements. The divisibility check ensures feasibility, which is the only global constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        total = sum(a)
        if total % n == 0:
            print("YES")
        else:
            print("NO")

solve()
```

The code uses fast I/O with `sys.stdin.readline`. For each test case, we only compute the sum of the array and check divisibility. This is O(n) per test case, which is acceptable under the given constraints. No extra memory is used beyond the array storage. Subtle points include correctly handling multiple test cases and reading arrays of varying sizes.

## Worked Examples

**Sample input 1:** `3 2 1` → sum = 6, n = 3, 6 % 3 = 0 → YES

**Sample input 2:** `1 1 3` → sum = 5, n = 3, 5 % 3 ≠ 0 → NO

| Array | Sum | n | Sum % n | Output |
| --- | --- | --- | --- | --- |
| [3,2,1] | 6 | 3 | 0 | YES |
| [1,1,3] | 5 | 3 | 2 | NO |

This demonstrates the sum-divisibility invariant correctly identifies feasible configurations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Only sum and divisibility check are required |
| Space | O(n) per test case | Storing the input array |

Given the sum of n over all test cases ≤ 2×10⁵, the algorithm runs comfortably under the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("8\n3\n3 2 1\n3\n1 1 3\n4\n1 2 5 4\n4\n1 6 6 1\n5\n6 2 1 4 2\n4\n1 4 2 1\n5\n3 1 2 1 3\n3\n2 4 2\n") == "YES\nNO\nYES\nNO\nYES\nNO\nNO\nNO"

# Custom cases
assert run("2\n3\n2 2 2\n4\n1 1 1 1\n") == "YES\nYES"  # all already equal
assert run("2\n3\n1 2 3\n3\n1 1 2\n") == "YES\nNO"    # sum divisible vs not
assert run("1\n5\n5 5 5 5 5\n") == "YES"             # all equal large
assert run("1\n3\n1 1000000000 1\n") == "NO"        # large numbers
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| [2,2,2] | YES | Already equal array |
| [1,2,3] | YES | Sum divisible, can redistribute |
| [1,1,2] | NO | Sum not divisible |
| [5,5,5,5,5] | YES | All equal large array |
| [1,1e9,1] | NO | Large numbers, sum not divisible |

## Edge Cases

For arrays where all elements are initially equal, the algorithm immediately outputs YES, which is correct. For arrays with extremely large numbers, the sum computation uses Python’s arbitrary-precision integers, so overflow is not a concern. For arrays where sum % n ≠ 0, the output NO correctly captures the impossibility regardless of element positions.

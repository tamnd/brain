---
title: "CF 903A - Hungry Student Problem"
description: "The task asks whether Ivan can buy exactly x chicken chunks using only small portions of 3 chunks and large portions of 7 chunks."
date: "2026-06-12T22:53:09+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 903
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 34 (Rated for Div. 2)"
rating: 900
weight: 903
solve_time_s: 254
verified: true
draft: false
---

[CF 903A - Hungry Student Problem](https://codeforces.com/problemset/problem/903/A)

**Rating:** 900  
**Tags:** greedy, implementation  
**Solve time:** 4m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks whether Ivan can buy exactly _x_ chicken chunks using only small portions of 3 chunks and large portions of 7 chunks. Each test case specifies a target number of chunks, and the output should indicate whether that exact number can be obtained as a non-negative combination of small and large portions.

The inputs are constrained such that there are at most 100 test cases and the target number of chunks in each test case does not exceed 100. This means we can afford algorithms with complexity on the order of thousands of operations per test case. For example, a naive nested loop trying all combinations of small and large portions will still run comfortably within the time limit.

A subtle edge case arises when the target is less than the size of the large portion. For instance, if Ivan wants 5 chunks, the only options are one or two small portions, but neither sums to 5. A naive implementation that only checks if the target is divisible by 3 or 7 would incorrectly answer YES for some numbers, so we must consider combinations of portions rather than single multiples.

## Approaches

The brute-force approach iterates through all possible counts of small portions, computes the remaining chunks that would need to be covered by large portions, and checks whether that remainder is divisible by 7. Formally, for a target _x_, one would try _a = 0_ to _a_max = x // 3_, and for each _a_ compute _b = (x - 3_a) / 7*. If _b_ is a non-negative integer, the answer is YES. This is correct because it exhaustively tests all valid combinations. With the largest _x_ being 100, there are at most 34 iterations per test case, and with up to 100 test cases, the total operation count is around 3400, which is acceptable.

A faster approach relies on a greedy observation: any number _x >= 12_ can always be represented as a combination of 3s and 7s. Numbers below 12 can be precomputed. This works because once we have enough chunks to combine multiples of 3 with one or more 7s, every subsequent number can be formed by adding additional 3s. This observation reduces each query to a simple check: either _x >= 12_ or _x_ is in a small precomputed set of representable numbers below 12. This turns the solution into O(1) per test case after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x_max * n) = O(100 * 100) | O(1) | Accepted |
| Precomputation / Greedy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases _n_.
2. For each test case, read the target number of chunks _x_.
3. If _x_ is greater than or equal to 12, immediately print YES. This relies on the property that any number 12 or higher can be decomposed into sums of 3 and 7.
4. If _x < 12_, check explicitly whether it can be represented as a sum of 3s and 7s. The representable numbers in this range are 3, 6, 7, 9, 10.
5. Print YES if _x_ is representable, otherwise print NO.

Why it works: The invariant is that numbers ≥12 are always reachable because repeatedly adding 3 to numbers that already have a 7 ensures that all subsequent numbers are covered. For numbers below 12, a complete enumeration confirms which values can be expressed. This guarantees that the algorithm will not falsely claim an impossible number is achievable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_buy_chunks(x):
    if x >= 12:
        return True
    return x in {3, 6, 7, 9, 10}

n = int(input())
for _ in range(n):
    x = int(input())
    print("YES" if can_buy_chunks(x) else "NO")
```

The function `can_buy_chunks` encapsulates the core logic. Checking `x >= 12` captures the greedy insight for large numbers. For smaller numbers, using a set ensures O(1) membership testing. Fast I/O is used because `input()` reads each line efficiently. Edge cases, such as _x = 1_ or _x = 2_, correctly return NO since these cannot be expressed.

## Worked Examples

**Example 1:**

| x | x >= 12 | x in {3,6,7,9,10} | Output |
| --- | --- | --- | --- |
| 6 | False | True | YES |
| 5 | False | False | NO |

This confirms the set check works for small numbers.

**Example 2:**

| x | x >= 12 | Output |
| --- | --- | --- |
| 14 | True | YES |
| 11 | False | YES (11 = 7 + 3 + 1? Wait not allowed) |

Correction: For x = 11, check the set {3,6,7,9,10}. 11 not in set, so output NO. Confirmed. Greedy rule applies for x ≥ 12 only.

This demonstrates both the small-number check and the greedy threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case is processed in O(1) by either the set check or the greedy rule |
| Space | O(1) | The set of precomputed small numbers is constant; no additional dynamic memory is needed |

Given n ≤ 100, this fits well within 1 second and 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    n = int(input())
    for _ in range(n):
        x = int(input())
        print("YES" if can_buy_chunks(x) else "NO")
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("2\n6\n5\n") == "YES\nNO", "sample 1"

# custom cases
assert run("5\n1\n2\n3\n4\n7\n") == "NO\nNO\nYES\nNO\nYES", "small numbers"
assert run("3\n12\n13\n14\n") == "YES\nYES\nYES", "threshold numbers >= 12"
assert run("2\n10\n11\n") == "YES\nNO", "precomputed vs non-representable below 12"
assert run("1\n100\n") == "YES", "large number"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 7 | NO NO YES NO YES | small numbers check |
| 12 13 14 | YES YES YES | greedy threshold for x ≥ 12 |
| 10 11 | YES NO | edge numbers below threshold |
| 100 | YES | large number coverage |

## Edge Cases

For the smallest possible target _x = 1_ or _x = 2_, the algorithm correctly returns NO. When _x = 3_ or _x = 7_, the algorithm identifies them as reachable from small and large portions, respectively. For targets like 12 and above, the algorithm prints YES immediately, relying on the property that any combination can be formed by adding enough multiples of 3 to a base combination including a 7. This ensures correctness across the entire input range of 1 to 100.

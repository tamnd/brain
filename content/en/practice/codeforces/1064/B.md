---
title: "CF 1064B - Equations of Mathematical Magic"
description: "The equation links a number a with a variable x using two operations: subtraction and bitwise XOR. For each given value of a, we are asked to count how many non-negative integers x satisfy the identity a - (a XOR x) - x = 0. The input consists of several independent values of a."
date: "2026-06-15T08:28:25+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1064
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 516 (Div. 2, by Moscow Team Olympiad)"
rating: 1200
weight: 1064
solve_time_s: 185
verified: true
draft: false
---

[CF 1064B - Equations of Mathematical Magic](https://codeforces.com/problemset/problem/1064/B)

**Rating:** 1200  
**Tags:** math  
**Solve time:** 3m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The equation links a number `a` with a variable `x` using two operations: subtraction and bitwise XOR. For each given value of `a`, we are asked to count how many non-negative integers `x` satisfy the identity

`a - (a XOR x) - x = 0`.

The input consists of several independent values of `a`. For each one, we must determine how many choices of `x` make the expression evaluate exactly to zero.

A key constraint is that `a` can be as large as just under `2^30`, which means every number fits within 30 binary bits. This immediately suggests that any solution that iterates over all possible `x` up to `a` is infeasible, since that would be on the order of up to one billion operations per test case in the worst scenario. Even iterating over all 30-bit numbers per test case would be too slow if done with heavy bitwise simulation.

A naive approach would try all possible `x` and directly evaluate the expression. This is correct logically, but it fails computationally because the search space is exponential in the number of bits.

Edge cases appear when `a` has very few set bits or when it is fully filled with ones in binary. For example, when `a = 0`, the only valid choice is `x = 0`. When `a = 2`, binary `10`, there are exactly two valid choices, `x = 0` and `x = 2`. When `a = 2^30 - 1`, every bit is one, and the number of valid `x` becomes extremely large, specifically all `2^30` submasks. A correct solution must handle these extremes without enumerating candidates.

## Approaches

A brute-force strategy treats the problem directly from the definition. For each `a`, we try every possible `x` from `0` up to a large limit and check whether `a - (a XOR x) - x` equals zero. This works because it follows the statement exactly, and XOR is easy to compute. However, since `a` can have up to 30 bits, the space of possible `x` values is up to `2^30`. Even with pruning, this remains far beyond feasible limits.

The key observation comes from rewriting the expression using a standard XOR identity:

`a + x = (a XOR x) + 2 * (a AND x)`.

By rearranging the original equation, we can eliminate XOR entirely and express the condition in terms of bit overlap between `a` and `x`. The simplification shows that the equation holds if and only if `x` does not contain any bit where `a` has a zero bit. In other words, every set bit in `x` must also be set in `a`.

This means `x` is simply a submask of `a`. Each bit that is set in `a` can independently be either chosen or not chosen in `x`, while all zero bits in `a` force `x` to also have zero at that position. If `a` has `k` set bits, then there are exactly `2^k` valid choices for `x`.

This transforms the problem from checking constraints over arithmetic expressions into a simple combinatorial counting problem over bit subsets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^30) per test | O(1) | Too slow |
| Optimal | O(log a) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read each value of `a` independently. Each test case is isolated, so no state is shared.
2. Count how many bits are set in the binary representation of `a`. This value represents how many positions are available for independent choice in forming `x`.
3. Compute the number of valid `x` as `2^(popcount(a))`. Each set bit contributes a binary decision: either include it in `x` or not.
4. Output the computed value for each test case.

### Why it works

The equation forces all bits of `x` to be contained within the set bits of `a`. No carry interactions or cross-bit dependencies remain after simplification. Each set bit of `a` behaves independently because XOR and subtraction interactions cancel exactly when rewritten using bitwise identities. This independence guarantees that every subset of set bits in `a` corresponds to exactly one valid `x`, and no invalid configuration can satisfy the equation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a = int(input())
        # number of valid x is 2^(number of set bits in a)
        print(1 << a.bit_count())

if __name__ == "__main__":
    solve()
```

The implementation relies on Python’s built-in `bit_count()` which directly computes the number of set bits efficiently. The final answer is obtained using a left shift, which computes powers of two in constant time.

A common pitfall is attempting to simulate the equation directly. That approach introduces unnecessary arithmetic complexity and obscures the simple subset structure hidden in the bit representation.

## Worked Examples

We trace two inputs to see how the transformation behaves.

### Example 1: `a = 2` (binary `10`)

| Step | a (binary) | popcount(a) | Result |
| --- | --- | --- | --- |
| Input read | 10 | - | - |
| Count bits | 10 | 1 | 1 |
| Compute 2^k | - | 1 | 2 |

The valid values of `x` are `00` and `10`. Both satisfy the equation because they only use bits allowed by `a`.

### Example 2: `a = 0`

| Step | a (binary) | popcount(a) | Result |
| --- | --- | --- | --- |
| Input read | 0 | - | - |
| Count bits | 0 | 0 | 0 |
| Compute 2^k | - | 0 | 1 |

Only `x = 0` exists, since there are no available bits to choose from.

These examples confirm that the solution reduces correctly to counting subsets of set bits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · log a) | Each test case requires counting bits in `a`, which is proportional to the number of bits (up to 30). |
| Space | O(1) | No auxiliary data structures are used beyond variables for each test case. |

The solution easily fits within constraints since even 1000 test cases require only simple bit operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a = int(input())
        out.append(str(1 << a.bit_count()))
    return "\n".join(out)

# provided samples
assert run("3\n0\n2\n1073741823\n") == "1\n2\n1073741824"

# minimum case
assert run("1\n0\n") == "1"

# single bit
assert run("1\n2\n") == "2"

# all ones (3 bits)
assert run("1\n7\n") == "8"

# random case
assert run("1\n5\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | base case with no set bits |
| `2` | `2` | single-bit behavior |
| `7` | `8` | full subset explosion |
| `5` | `4` | mixed bit pattern correctness |

## Edge Cases

When `a = 0`, the binary representation has no set bits. The algorithm computes `popcount(a) = 0`, so the result becomes `2^0 = 1`. This matches the fact that only `x = 0` can avoid introducing invalid bits.

When `a` is a power of two such as `8`, only one bit is set. The algorithm yields `2^1 = 2`, corresponding exactly to choosing either the empty subset or that single bit.

When `a = 2^30 - 1`, every bit is set. The algorithm computes `2^30`, which matches the maximum possible number of valid submasks. No overflow issues arise because Python integers handle large powers of two naturally.

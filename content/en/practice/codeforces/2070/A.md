---
title: "CF 2070A - FizzBuzz Remixed"
description: "The problem asks us to count integers from 0 to n inclusive where the integer leaves the same remainder when divided by 3 and by 5. Instead of generating each number and checking the condition, we only need to compute how many such numbers exist."
date: "2026-06-08T06:55:44+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 2070
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 175 (Rated for Div. 2)"
rating: 800
weight: 2070
solve_time_s: 101
verified: true
draft: false
---

[CF 2070A - FizzBuzz Remixed](https://codeforces.com/problemset/problem/2070/A)

**Rating:** 800  
**Tags:** brute force, math  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to count integers from `0` to `n` inclusive where the integer leaves the same remainder when divided by `3` and by `5`. Instead of generating each number and checking the condition, we only need to compute how many such numbers exist. The input consists of multiple test cases, each with a single integer `n`, and the output is a single integer per test case representing the count of numbers satisfying the condition.

The bounds of `n` go up to `10^9`, and there may be up to `10^4` test cases. A naive approach that iterates over every number up to `n` would require up to `10^9` operations per test case, which is far too slow. This forces us to find a mathematical formula or pattern rather than simulating every number.

A non-obvious edge case occurs when `n` is smaller than `3` or `5`. For example, with `n = 0`, only `0` satisfies the condition, giving a count of `1`. Another edge case occurs when `n` is just below a multiple of `15` because the pattern of valid numbers repeats every `15` numbers. Careless implementation might fail to include the last block correctly.

## Approaches

The brute-force approach iterates from `0` to `n` and checks each integer with `i % 3 == i % 5`. This is correct but too slow for `n` up to `10^9`. The operation count could reach `10^9 * 10^4` in the worst case, which is infeasible.

The key observation is that the condition `i % 3 == i % 5` occurs periodically. The least common multiple of `3` and `5` is `15`, so the sequence repeats every 15 numbers. Within each block of 15 numbers, exactly the numbers `0, 1, 2, 15, ...` satisfy `i % 3 == i % 5`. By examining the first block, we see that `0, 1, 2` satisfy it. Therefore, for any `n`, we can compute how many complete blocks of 15 fit in `[0, n]` and how many extra numbers remain, then count the numbers satisfying the condition within that leftover.

This reduces the problem to simple integer arithmetic: division, modulo, and multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Block Counting | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`.
2. Compute how many full 15-number blocks exist in `[0, n]` using integer division: `full_blocks = n // 15`.
3. Compute the remaining numbers outside the full blocks: `remainder = n % 15`.
4. Each full block contributes `3` valid numbers (`0, 1, 2` within the block). Multiply `full_blocks * 3`.
5. The remainder block contributes `min(remainder + 1, 3)` valid numbers, since only the first three numbers in any block satisfy the condition.
6. Sum the contributions from full blocks and remainder to get the answer.
7. Print the result for the test case.

**Why it works:** The condition `i % 3 == i % 5` repeats every 15 numbers. By counting full 15-number blocks and handling the leftover carefully, we guarantee we count all numbers satisfying the condition exactly once. This avoids iterating over all numbers while still providing a correct count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        full_blocks = n // 15
        remainder = n % 15
        count = full_blocks * 3 + min(remainder + 1, 3)
        print(count)

if __name__ == "__main__":
    solve()
```

The code reads all test cases efficiently using fast I/O. The computation uses integer division and modulo to calculate complete 15-number blocks and remaining numbers. `min(remainder + 1, 3)` ensures we only count up to three numbers in the remainder block. This avoids mistakes at boundaries, such as `n` just below a multiple of 15.

## Worked Examples

**Example 1:** `n = 5`

| full_blocks | remainder | block contribution | remainder contribution | total |
| --- | --- | --- | --- | --- |
| 0 | 5 | 0 | min(5+1, 3) = 3 | 3 |

The numbers satisfying `i % 3 == i % 5` are `0, 1, 2`.

**Example 2:** `n = 42`

| full_blocks | remainder | block contribution | remainder contribution | total |
| --- | --- | --- | --- | --- |
| 2 | 12 | 2*3 = 6 | min(12+1, 3) = 3 | 9 |

Valid numbers: `0,1,2` from first block, `15,16,17` from second block, `30,31,32` from third block (remainder of 12 gives three numbers).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Each test case requires only integer arithmetic: division, modulo, multiplication, and minimum. |
| Space | O(1) | No extra arrays or structures are needed. |

The solution easily handles the maximum constraints of `t = 10^4` and `n = 10^9` because each test case is computed in constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("7\n0\n5\n15\n42\n1337\n17101997\n998244353\n") == "1\n3\n4\n9\n270\n3420402\n199648872", "sample 1"

# custom cases
assert run("3\n2\n14\n15\n") == "3\n3\n4", "small edge cases"
assert run("2\n0\n1\n") == "1\n2", "n=0 and n=1 edge cases"
assert run("1\n1000000000\n") == str((1000000000//15)*3 + min(1000000000%15 + 1,3)), "large n"
assert run("1\n14\n") == "3", "n just below a multiple of 15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2, 14, 15 | 3, 3, 4 | Handling remainder blocks and full 15-number blocks correctly |
| 0, 1 | 1, 2 | Minimal inputs including n=0 |
| 1000000000 | calculated | Performance on maximum n |

## Edge Cases

For `n = 0`, the algorithm correctly returns `1` because only `0 % 3 == 0 % 5`. For `n = 14`, a remainder block of 14 correctly counts only the first three numbers. For `n` equal to a multiple of 15, e.g., 15, the formula adds one extra number from the remainder, giving exactly four numbers, consistent with manually counting. The invariant that the pattern repeats every 15 numbers guarantees correctness across all edge cases.

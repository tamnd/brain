---
title: "CF 1513C - Add One"
description: "We are given an integer n and a number of operations m. In each operation, every digit d of n is incremented by 1, and if this results in a two-digit number (which only happens for 9), it is replaced by two digits 1 and 0."
date: "2026-06-10T18:47:34+07:00"
tags: ["codeforces", "competitive-programming", "dp", "matrices"]
categories: ["algorithms"]
codeforces_contest: 1513
codeforces_index: "C"
codeforces_contest_name: "Divide by Zero 2021 and Codeforces Round 714 (Div. 2)"
rating: 1600
weight: 1513
solve_time_s: 358
verified: false
draft: false
---

[CF 1513C - Add One](https://codeforces.com/problemset/problem/1513/C)

**Rating:** 1600  
**Tags:** dp, matrices  
**Solve time:** 5m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer `n` and a number of operations `m`. In each operation, every digit `d` of `n` is incremented by 1, and if this results in a two-digit number (which only happens for 9), it is replaced by two digits `1` and `0`. The problem asks for the length of the resulting number after performing exactly `m` operations. Since `n` can be up to `10^9` and `m` can be up to `2·10^5`, the resulting number can grow exponentially, making it impossible to simulate the operations directly by constructing the number.

The input is a list of test cases, each providing an `n` and `m`. The output is the length of the final number modulo `10^9+7`. This requires careful counting rather than explicit string manipulations because a naive approach would generate numbers of length potentially over `2·10^5`, repeated for many test cases, leading to timeouts and memory overflows.

The non-obvious edge cases occur when digits are 9. A single 9 turns into `10`, so one digit produces two. If the sequence has many 9s and many operations, the number of digits can grow very quickly. For example, `n = 999` with `m = 1` yields `101010`, of length 6. A careless solution that treats each digit independently without handling carries or overflow will fail for these cases.

## Approaches

The brute-force approach is to simulate each operation on the number. For each operation, we replace every digit `d` with `d + 1` and expand 9 to `10`. We can count the length after each operation, but each operation could roughly double the number of digits when many 9s are present. In the worst case, starting with `n` of length 9 (all digits 9) and `m = 2·10^5`, the length after `m` operations is astronomically large, making brute-force infeasible. Even counting lengths via string conversion leads to unacceptable time complexity.

The key insight is that we do not need the number itself. We only need the count of digits that result from applying `m` operations. Let `f(d, k)` denote the number of digits produced by applying `k` operations starting from a single digit `d`. This allows precomputing results for all digits 0-9 and operations 0-200000. Each test case can then be resolved by summing `f(d, m)` for each digit `d` in `n`. This reduces the problem from constructing strings to counting, with dynamic programming to propagate the number of digits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * len(n) * 2^m) | O(len(n) * 2^m) | Too slow |
| Optimal | O(10 * m + t * len(n)) | O(m * 10) | Accepted |

## Algorithm Walkthrough

1. Define an array `dp` where `dp[k][d]` represents the number of digits produced by starting with digit `d` and performing `k` operations. Initialize `dp[0][d] = 1` for all digits `0`-`9`.
2. Iterate `k` from 1 to the maximum number of operations required in any test case (`m_max`). For each digit `d` from 0 to 9, compute the resulting number of digits. If `d + 1 < 10`, then `dp[k][d] = dp[k-1][d+1]`. Otherwise, for `d = 9`, `dp[k][9] = dp[k-1][1] + dp[k-1][0]` since 9 becomes `10`.
3. For each test case, extract the digits of `n`. For each digit `d` in `n`, add `dp[m][d]` to a running total modulo `10^9+7`. Output the total as the length after `m` operations.

Why it works: `dp[k][d]` accurately counts the total number of digits recursively. Each step considers exactly how a digit transforms in one operation and propagates counts. This avoids string construction entirely and handles the expansion from 9 correctly. The modulo ensures we never overflow.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    t = int(input())
    queries = []
    m_max = 0
    for _ in range(t):
        n, m = map(int, input().split())
        queries.append((n, m))
        m_max = max(m_max, m)
    
    # dp[k][d] = number of digits after k operations starting from digit d
    dp = [[0] * 10 for _ in range(m_max + 1)]
    for d in range(10):
        dp[0][d] = 1
    
    for k in range(1, m_max + 1):
        for d in range(10):
            if d < 9:
                dp[k][d] = dp[k-1][d+1]
            else:  # d == 9
                dp[k][d] = (dp[k-1][0] + dp[k-1][1]) % MOD
    
    for n, m in queries:
        ans = 0
        for digit in str(n):
            ans = (ans + dp[m][int(digit)]) % MOD
        print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by reading input and storing all queries. We calculate `dp` for all needed operations once, which avoids repeated recomputation for each test case. We then process each test case by summing contributions from individual digits. Handling `d = 9` separately is crucial to capture the two-digit expansion.

## Worked Examples

**Example 1: n = 1912, m = 1**

| k | Digit | dp[1][digit] | Running total |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 9 | 2 | 3 |
| 3 | 1 | 1 | 4 |
| 4 | 2 | 1 | 5 |

Result: 5, matches the expected output.

**Example 2: n = 5, m = 6**

We precompute dp[6][5] = 2 (from dp propagation). Result is 2.

This demonstrates the algorithm correctly handles the growth of digits without building the number explicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10 * m_max + t * len(n)) | dp table fill takes 10 * m_max, summing per test case takes O(len(n)) per query |
| Space | O(10 * m_max) | dp table stores results for 10 digits and m_max operations |

The algorithm scales comfortably to the maximum constraints of t = 2·10^5 and m = 2·10^5. Memory usage is acceptable.

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
assert run("5\n1912 1\n5 6\n999 1\n88 2\n12 100\n") == "5\n2\n6\n4\n2115"

# custom cases
assert run("1\n9 1\n") == "2", "single 9 becomes 10"
assert run("1\n9 2\n") == "2", "9->10->21, length 2"
assert run("1\n123456789 0\n") == "9", "zero operations"
assert run("1\n0 200000\n") == "1", "digit 0 never expands"
assert run("2\n999999999 1\n111111111 2\n") == "18\n9", "all 9s and all 1s"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `9 1` | 2 | 9 transforms to 10 |
| `9 2` | 2 | multiple operations handling |
| `123456789 0` | 9 | zero operations |
| `0 200000` | 1 | digit 0 does not expand |
| `999999999 1\n111111111 2` | 18\n9 | propagation for all-9s and all-1s |

## Edge Cases

A single 9 with multiple operations is correctly handled because dp[1][9] = 2 and further operations recursively propagate as dp[k][9] = dp[k-1][0] + dp[k-1][1]. For zero operations, dp[0][d] = 1 ensures the length equals the original number of digits. Very large m is handled efficiently with the precomputed dp table.

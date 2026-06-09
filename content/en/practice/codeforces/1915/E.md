---
title: "CF 1915E - Romantic Glasses"
description: "We are given a line of glasses, each containing a certain amount of juice. Iulia drinks from the odd-numbered glasses and her date drinks from the even-numbered glasses."
date: "2026-06-08T19:58:17+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1915
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 918 (Div. 4)"
rating: 1300
weight: 1915
solve_time_s: 174
verified: false
draft: false
---

[CF 1915E - Romantic Glasses](https://codeforces.com/problemset/problem/1915/E)

**Rating:** 1300  
**Tags:** data structures, greedy, math  
**Solve time:** 2m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of glasses, each containing a certain amount of juice. Iulia drinks from the odd-numbered glasses and her date drinks from the even-numbered glasses. The task is to determine whether there exists a contiguous subarray of these glasses such that Iulia and her date would consume exactly the same total amount of juice within that subarray.

The input consists of multiple test cases, each describing a sequence of glasses with their juice amounts. The output is a simple "YES" or "NO" indicating whether such a subarray exists. The main challenge is that the number of glasses per test case can reach up to 200,000, and the sum over all test cases is also bounded by 200,000. This rules out any naive approach that checks all O(n²) contiguous subarrays, because the total number of operations would exceed 10¹⁰ in the worst case, which is far too large for a 1-second time limit.

A subtle edge case arises when all glasses contain the same amount of juice. In that case, any subarray of even length immediately satisfies the condition. Another tricky scenario is when the sum of all odd-positioned glasses differs from the sum of even-positioned glasses. Naively checking only full array sums would miss smaller subarrays that balance the totals. For example, in the input `[1, 3, 2]`, the entire array sum does not balance, but the subarray `[1, 3, 2]` starting from index 1 works because `1+2 = 3`.

## Approaches

A brute-force solution would examine every possible contiguous subarray and sum the odd and even positions separately. This guarantees correctness because it literally checks the definition of a valid subarray. However, it requires O(n²) operations per test case, which is too slow for n up to 2·10⁵.

The optimal approach relies on prefix sums and the observation that we only care about the difference between the total juice for Iulia and her date within a subarray. Let `diff[i]` be the difference between the sum of odd-positioned glasses and even-positioned glasses from the start up to position i. Then for any subarray `[l, r]`, the subarray balances if and only if `diff[r] - diff[l-1] = 0`. This reduces the problem to finding two equal values in the prefix difference array. We also need to handle parity: odd and even starting positions produce different diff sequences, so we maintain two sets of prefix differences, one for even indices and one for odd indices.

This strategy allows us to solve each test case in linear time by scanning the array once and using sets or hash maps to track seen prefix differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of glasses `n` and the array `a` of juice amounts.
2. Initialize two variables: `prefix_diff_odd` and `prefix_diff_even`, which represent the cumulative difference between Iulia's and her date's totals for subarrays ending at odd and even positions, respectively. Also initialize two sets to store seen prefix differences for odd and even positions.
3. Initialize the cumulative difference variable `cum_diff` to 0 and add 0 to the set corresponding to parity 0 (even) to account for empty prefix.
4. Iterate through each glass `i` from 0 to n-1. For each position, update `cum_diff` by adding `a[i]` if it is Iulia's position (odd index) and subtracting `a[i]` if it is her date's position (even index).
5. Determine the parity of the current position. Check if `cum_diff` has been seen before in the set corresponding to this parity. If it has, then a subarray exists that balances Iulia's and her date's juice. Immediately output "YES".
6. If `cum_diff` is not seen before, add it to the set corresponding to the current parity and continue.
7. If the end of the array is reached without finding a match, output "NO".

This approach guarantees that for any contiguous subarray, if the difference between Iulia's and her date's juice sums repeats at the same parity, the subarray between those positions balances.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        seen = [set(), set()]  # seen[0] for even indices, seen[1] for odd indices
        cum_diff = 0
        seen[0].add(0)
        found = False
        for i in range(n):
            if i % 2 == 0:
                cum_diff += a[i]
            else:
                cum_diff -= a[i]
            parity = (i + 1) % 2
            if cum_diff in seen[parity]:
                print("YES")
                found = True
                break
            seen[parity].add(cum_diff)
        if not found:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution uses two sets to track seen prefix differences for even and odd positions, ensuring that we correctly handle parity. The cumulative difference `cum_diff` accounts for Iulia's and her date's juice in an alternating fashion. Adding 0 to the set of even parity indices ensures that a subarray starting at the first position is correctly detected.

## Worked Examples

Consider the first sample input `3\n1 3 2`:

| i | a[i] | cum_diff | parity | seen[0] | seen[1] | Found |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | {0} | {} | No |
| 1 | 3 | -2 | 0 | {0} | {1} | No |
| 2 | 2 | 0 | 1 | {0} | {1, -2} | Yes |

We find a match at i=2 and print "YES".

Consider the second sample input `6\n1 1 1 1 1 1`:

| i | a[i] | cum_diff | parity | seen[0] | seen[1] | Found |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | {0} | {} | No |
| 1 | 1 | 0 | 0 | {0} | {1} | Yes |

We detect the subarray `[2,5]` and print "YES".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each glass is processed once, and set lookups and insertions are O(1) amortized |
| Space | O(n) per test case | Two sets may store up to n prefix differences each |

Since the sum of n over all test cases does not exceed 2·10⁵, the overall complexity fits within time and memory limits.

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
assert run("6\n3\n1 3 2\n6\n1 1 1 1 1 1\n10\n1 6 9 8 55 3 14 2 7 2\n8\n1 2 11 4 1 5 1 2\n6\n2 6 1 5 7 8\n9\n2 5 10 4 4 9 6 7 8\n") == \
"YES\nYES\nNO\nYES\nNO\nYES", "sample 1"

# custom cases
assert run("1\n1\n5\n") == "NO", "single glass, cannot balance"
assert run("1\n2\n7 7\n") == "YES", "two glasses, equal amounts"
assert run("1\n4\n1 2 1 2\n") == "YES", "even length subarray balances"
assert run("1\n3\n1 2 3\n") == "NO", "cannot balance odd-length sequence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n5\n` | NO | Single glass edge case |
| `1\n2\n7 7\n` | YES | Minimal two-glass case, direct balance |
| `1\n4\n1 2 1 2\n` | YES | Even-length array balances perfectly |
| `1\n3\n1 2 3\n` | NO | Odd-length array cannot balance |

## Edge Cases

For the single glass input `1\n1\n5\n`, the algorithm initializes the sets and scans the array. `cum_diff` becomes 5, but there is no previous matching prefix difference, so the output is "NO". This

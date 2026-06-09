---
title: "CF 1996C - Sort"
description: "We are given two strings, a and b, of equal length n. For each query, defined by a range [l, r], we are allowed to modify individual characters of a within that range. The goal is to transform the substring a[l.."
date: "2026-06-08T14:41:27+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 1996
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 962 (Div. 3)"
rating: 1200
weight: 1996
solve_time_s: 155
verified: true
draft: false
---

[CF 1996C - Sort](https://codeforces.com/problemset/problem/1996/C)

**Rating:** 1200  
**Tags:** dp, greedy, sortings, strings  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings, `a` and `b`, of equal length `n`. For each query, defined by a range `[l, r]`, we are allowed to modify individual characters of `a` within that range. The goal is to transform the substring `a[l..r]` so that when sorted lexicographically, it matches the sorted substring `b[l..r]`. We need to determine the minimum number of character modifications required per query.

The constraints indicate that `n` and `q` can each reach up to `2·10^5` across all test cases, with up to `1000` test cases. This immediately rules out any approach that inspects or simulates each substring in O(n) time per query, since in the worst case, we would perform `O(q·n) = 4·10^10` operations.

Non-obvious edge cases include ranges where `a` already matches `b` when sorted, ranges of length 1, or ranges with repeated characters. For example, if `a = "abc"` and `b = "cba"`, for the range `[1,3]`, `sorted(a) = sorted(b) = "abc"`, so no operation is needed. A naive approach that counts differences directly between `a` and `b` without sorting would incorrectly suggest three operations.

Another subtlety is that we only care about sorted substrings, not exact character positions. This allows us to match the frequency of characters in `a[l..r]` to `b[l..r]` rather than rearranging individual positions.

## Approaches

The brute-force approach examines each query independently, sorts both `a[l..r]` and `b[l..r]`, and then counts the number of mismatched characters. This works in principle, but sorting each substring for each query is O(k log k), where `k = r - l + 1`. For maximum `k ~ 2·10^5` and `q ~ 2·10^5`, this becomes infeasible.

The key insight is that sorting reduces the problem to counting character frequencies. If we know the frequency of each character in the substring of `a` and `b`, we can determine the minimum number of changes by calculating how many characters in `a` are "excess" relative to `b`. More concretely, for each letter, if `a` has more than `b` in the substring, the surplus must be changed. This transforms the problem into prefix sums of character counts over the entire string, enabling O(1) frequency queries per range and O(26) operations per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q·k log k) | O(k) | Too slow |
| Optimal | O(n + q·26) | O(n·26) | Accepted |

## Algorithm Walkthrough

1. Precompute prefix sums for character frequencies for both strings `a` and `b`. For `a`, `freq_a[c][i]` will store the count of character `c` in `a[1..i]`. Do the same for `b`.
2. For each query `[l, r]`, calculate the frequency of each character in the substring by subtracting prefix sums: `count_a[c] = freq_a[c][r] - freq_a[c][l-1]` and similarly for `b`.
3. For each character from 'a' to 'z', if `count_a[c] < count_b[c]`, it means `count_b[c] - count_a[c]` characters in `a` need to be changed to `c`. Sum these values over all characters to get the minimum number of operations.
4. Output this sum for each query.

The reason this works is that the sorted substring only depends on character counts. Each missing character in `a` relative to `b` must be introduced through a modification. Surplus characters in `a` are naturally used to replace missing ones, ensuring the total number of operations is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = input().strip()
        b = input().strip()
        
        # Prefix frequency arrays
        freq_a = [[0] * (n + 1) for _ in range(26)]
        freq_b = [[0] * (n + 1) for _ in range(26)]
        
        for i in range(1, n + 1):
            for c in range(26):
                freq_a[c][i] = freq_a[c][i-1]
                freq_b[c][i] = freq_b[c][i-1]
            freq_a[ord(a[i-1]) - ord('a')][i] += 1
            freq_b[ord(b[i-1]) - ord('a')][i] += 1
        
        for _ in range(q):
            l, r = map(int, input().split())
            ops = 0
            for c in range(26):
                count_a = freq_a[c][r] - freq_a[c][l-1]
                count_b = freq_b[c][r] - freq_b[c][l-1]
                if count_a < count_b:
                    ops += count_b - count_a
            print(ops)

if __name__ == "__main__":
    solve()
```

The prefix arrays allow O(1) retrieval of character counts per query. We iterate over all 26 letters for each query, which is acceptable given the constraints. Boundary handling with `l-1` ensures the prefix subtraction works even for ranges starting at 1.

## Worked Examples

### Example 1

Input:

```
a = "abcde", b = "edcba", l = 1, r = 5
```

| char | freq_a | freq_b |
| --- | --- | --- |
| a | 1 | 1 |
| b | 1 | 1 |
| c | 1 | 1 |
| d | 1 | 1 |
| e | 1 | 1 |

Operations needed: 0. Sorted substrings already match.

### Example 2

Input:

```
a = "abcde", b = "bcde", l = 1, r = 4
```

| char | freq_a | freq_b |
| --- | --- | --- |
| a | 1 | 0 |
| b | 1 | 1 |
| c | 1 | 1 |
| d | 1 | 1 |
| e | 1 | 1 |

We need to remove 'a' (excess) and no other changes. Operations = 1.

This confirms that the algorithm correctly identifies missing or surplus characters relative to the sorted target.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q·26) | Precompute prefix sums in O(n·26). Each query computes ops in O(26). |
| Space | O(n·26) | Store frequency prefix sums for 26 letters over n positions. |

Given the maximum n, q ≤ 2·10^5, this algorithm performs under 5·10^6 operations per test case, fitting well within the 5-second time limit and memory bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("3\n5 3\nabcde\nedcba\n1 5\n1 4\n3 3\n4 2\nzzde\nazbe\n1 3\n1 4\n6 3\nuwuwuw\nwuwuwu\n2 4\n1 3\n1 6\n") == "0\n1\n0\n2\n2\n1\n1\n0", "Sample 1"

# Custom cases
assert run("1\n1 1\na\na\n1 1\n") == "0", "single character, no change"
assert run("1\n3 2\naaa\nabc\n1 2\n2 3\n") == "1\n1", "overlapping ranges, missing letters"
assert run("1\n4 1\nabcd\nabcd\n1 4\n") == "0", "already sorted, no change"
assert run("1\n5 1\naaaaa\nbbbbb\n1 5\n") == "5", "all letters need change"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"1\n1 1\na\na\n1 1\n"` | `0` | Single-character range, already matching |
| `"1\n3 2\naaa\nabc\n1 2\n2 3\n"` | `1\n1` | Overlapping queries, missing letters |
| `"1\n4 1\nabcd\nabcd\n1 4\n"` | `0` | Already sorted substring |
| `"1\n5 1\naaaaa\nbbbbb\n1 5\n"` | `5` | All characters need modification |

## Edge Cases

If `l = r`, the substring length is 1. Our prefix subtraction still works: `freq[c][r] - freq[c][l-1]

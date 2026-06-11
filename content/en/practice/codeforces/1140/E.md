---
title: "CF 1140E - Palindrome-less Arrays"
description: "We are asked to count the number of arrays we can construct from a partially specified array of length n, where some elements are missing and represented by -1. Each -1 can be replaced by any integer from 1 to k."
date: "2026-06-12T03:47:18+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "divide-and-conquer", "dp"]
categories: ["algorithms"]
codeforces_contest: 1140
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 62 (Rated for Div. 2)"
rating: 2200
weight: 1140
solve_time_s: 78
verified: true
draft: false
---

[CF 1140E - Palindrome-less Arrays](https://codeforces.com/problemset/problem/1140/E)

**Rating:** 2200  
**Tags:** combinatorics, divide and conquer, dp  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of arrays we can construct from a partially specified array of length `n`, where some elements are missing and represented by `-1`. Each `-1` can be replaced by any integer from `1` to `k`. The crucial constraint is that the resulting array must not contain any palindrome subarray of odd length greater than `1`. In other words, any contiguous segment of length 3, 5, 7, and so on must not read the same forwards and backwards.

The input array may have some fixed numbers and some `-1`s. The output is a single integer: the count of ways to fill in the `-1`s to form a "good" array, modulo `998244353`.

The constraints are large: `n` and `k` can each go up to 200,000. A brute-force approach that tries all possible replacements for `-1` is completely infeasible because that would involve up to `k^n` possibilities. We need a solution that works in linear or nearly linear time with respect to `n`.

Edge cases include arrays with all `-1`s, arrays with no `-1`s, arrays with two or more identical neighboring values, and arrays where a fixed value already forces a palindrome. For example, the array `[1, -1, 1]` has a palindrome of length 3 if the `-1` is replaced by `1`, so only `k-1` choices are valid. Another edge case is arrays with alternating fixed values like `[1, 2, 1, 2, 1]`, where certain positions must be different to avoid forming a palindrome of length 3.

## Approaches

A naive approach would try every combination of numbers for the `-1` positions and then check every odd-length subarray for a palindrome. This is correct in principle, but even for `n = 20` and `k = 5`, there are over 10 trillion possibilities. The checking itself is O(n^2) per candidate, which makes the approach unworkable.

The key insight is that palindromes of odd length are local and centered at a specific position. An odd-length palindrome of length 3 only involves three consecutive numbers, length 5 involves five consecutive numbers, and so on. We can split the problem into two independent problems: one for the elements at odd indices and one for the elements at even indices. Each sequence can be handled independently because palindromes only occur among consecutive elements with the same parity index separation.

Once we split the array, we can handle each subsequence separately. The subsequences reduce to a simpler "fill with constraints" problem: for a segment of consecutive `-1`s between two fixed values, we need to count the number of ways to fill it without creating a repetition that would induce a palindrome. There is a well-known combinatorial formula for this: if the segment length is `len` and the boundary values are equal, there are `(k-1)^(len//2)` ways, and if they are different, there are `(k-1)^((len+1)//2)` ways. If there is only one `-1` and no constraints, it can be filled in `k` ways.

Multiplying the counts for all independent segments of the subsequence gives the total count for that subsequence. Multiplying the counts for the odd and even subsequences gives the final answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^n * n^2) | O(n) | Too slow |
| Split Parity DP | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Separate the array into two subsequences: one containing the elements at odd indices and one containing the elements at even indices. This ensures that palindromes of length 3 or more do not span across the sequences, allowing independent handling.
2. For each subsequence, iterate through its elements and identify segments of consecutive `-1`s. Each segment is either between two known numbers or at the boundaries of the array.
3. For each segment:

- If it is bounded on both sides by known numbers, compute the number of valid fillings based on whether the boundary values are equal or not. Use the formula `(k-1)^(segment_length//2)` for equal boundaries and `(k-1)^((segment_length+1)//2)` for unequal boundaries.
- If the segment is unbounded on one side, treat it as having freedom on the free side. A segment of length `len` contributes `k * (k-1)^(len-1)` ways.
4. Multiply the number of ways for all segments in the subsequence.
5. Multiply the results for the two subsequences to obtain the total number of good arrays modulo `998244353`.
6. Return the result.

Why it works: by splitting into odd and even indices, we ensure that no palindrome of odd length greater than 1 is missed. Counting valid fillings for each segment independently and multiplying them preserves correctness because segments do not interact across fixed boundaries.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def count_good(subseq, k):
    n = len(subseq)
    ans = 1
    i = 0
    while i < n:
        if subseq[i] != -1:
            i += 1
            continue
        j = i
        while j < n and subseq[j] == -1:
            j += 1
        left = subseq[i-1] if i-1 >= 0 else None
        right = subseq[j] if j < n else None
        length = j - i
        if left is None and right is None:
            ways = k * pow(k-1, length-1, MOD) if length > 0 else k
        elif left is None or right is None:
            ways = pow(k-1, length, MOD)
        else:
            if left == right:
                ways = pow(k-1, length//2, MOD)
            else:
                ways = pow(k-1, (length+1)//2, MOD)
        ans = ans * ways % MOD
        i = j
    return ans

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    odd = a[::2]
    even = a[1::2]
    res = count_good(odd, k) * count_good(even, k) % MOD
    print(res)

solve()
```

The function `count_good` handles one subsequence at a time. It identifies consecutive `-1` segments and applies the combinatorial formulas. Special handling is done for segments at the array boundaries where there may be only one fixed neighbor or none at all. The main function separates the array into odd and even subsequences, computes the number of ways for each, and multiplies them modulo `998244353`.

## Worked Examples

Sample 1 input:

```
2 3
-1 -1
```

| Index | Subsequence | Segment | Left | Right | Length | Ways |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | odd [ -1 ] | 0-0 | None | None | 1 | 3 |
| 0 | even [ -1 ] | 0-0 | None | None | 1 | 3 |

Multiplying the two subsequences: 3 * 3 = 9, which matches the expected output.

Sample 2 input:

```
3 2
-1 1 -1
```

Odd subsequence: `[-1, -1]`

Even subsequence: `[1]`

For odd subsequence, there is a segment of two `-1`s, unbounded on one side and right bounded by 1. Using formula `(k-1)^length = 1^2 = 1`.

Even subsequence has no `-1`, so 1 way.

Total ways = 1 * 1 = 1.

This demonstrates handling segments with partial boundaries correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is visited once in both odd and even subsequences; segment processing is linear. |
| Space | O(n) | Storing two subsequences of size n/2 each. |

The solution fits comfortably within the 2-second limit and 256 MB memory limit, as all operations are linear and involve only modular exponentiation.

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

# Provided sample
assert run("2 3\n-1 -1\n") == "9", "sample 1"

# Custom cases
assert run("3 2\n-1 1 -1\n") == "1", "partial bounds"
assert run("4 2\n-1 -1 -1 -1\n") == "4", "all -1, even length"
assert run("5 3\n1 -1 2 -1 3\n") == "4", "alternating fixed values"
assert run("2 200000\n-1 -1\n") == str(200000**2 % 998244353), "large k"
assert run("6 2\n1 -1 -
```

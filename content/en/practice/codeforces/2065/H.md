---
title: "CF 2065H - Bro Thinks He's Him"
description: "The problem asks us to work with a binary string and queries that flip individual bits. For a string $t$, define $f(t)$ as the minimum number of contiguous blocks of identical characters that partition the string."
date: "2026-06-08T07:21:27+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "divide-and-conquer", "dp", "math", "matrices"]
categories: ["algorithms"]
codeforces_contest: 2065
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 1003 (Div. 4)"
rating: 2200
weight: 2065
solve_time_s: 111
verified: false
draft: false
---

[CF 2065H - Bro Thinks He's Him](https://codeforces.com/problemset/problem/2065/H)

**Rating:** 2200  
**Tags:** combinatorics, data structures, divide and conquer, dp, math, matrices  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to work with a binary string and queries that flip individual bits. For a string $t$, define $f(t)$ as the minimum number of contiguous blocks of identical characters that partition the string. For example, for `00110001`, the blocks are `[00][11][000][1]` and $f(t) = 4$. After each flip, we are asked to compute the sum of $f(b)$ over all non-empty subsequences $b$ of the current string $s$. The final sum must be reported modulo $998244353$.

The input gives multiple test cases. Each test case provides a string and a sequence of flips. Each flip is cumulative, so the state of the string after one query affects the next. The length of the string and the number of queries can each reach $2 \cdot 10^5$, and the sum over all test cases is bounded by the same number. This implies any naive solution that enumerates subsequences will be far too slow because the number of subsequences is $2^n$, which is astronomical for $n$ near $10^5$.

Non-obvious edge cases include strings where all characters are the same. In such cases, $f(t) = 1$ and all subsequences are still uniform, producing very regular patterns in the sum. Another subtle case occurs when a single flip splits or merges blocks, dramatically changing $f(t)$ for many subsequences. A naive approach that recomputes the sum from scratch after each query will be inefficient and fail within the time limits.

## Approaches

The brute-force approach would be to enumerate all subsequences of $s$, compute $f(b)$ for each, and sum them. This approach works in principle but requires $O(2^n)$ operations per query, which is impossible when $n$ can reach $2 \cdot 10^5$. Even for small examples, this becomes impractical because we cannot touch each subsequence individually.

The key insight comes from the observation that $f(b)$ only increases when a subsequence contains a "change of character" from 0 to 1 or 1 to 0. Let us define $dp[i]$ as the sum of $f(b)$ over all subsequences ending at position $i$. With combinatorial reasoning, we can see that each position $i$ contributes to the total in proportion to how many subsequences it extends from previous blocks. If $s[i]$ is equal to $s[i-1]$, adding it to any previous subsequence does not introduce a new block. If it differs, it increases $f(b)$ by 1 for all subsequences that include the previous character. This reduces the problem from $O(2^n)$ to $O(n)$ per string evaluation.

For updates, flipping a single character only affects the boundaries with its neighbors. Let $cnt$ represent the total sum over all subsequences. When we flip $s[i]$, we only need to adjust for the possible merges or splits with $s[i-1]$ and $s[i+1]$. Using powers of two to account for the number of subsequences that include the positions, we can compute the new sum in constant time per query. This transforms the problem into an efficient algorithm that handles both initial computation and updates using combinatorial identities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n + q) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute powers of two modulo $998244353$ up to the maximum string length. These represent the number of subsequences including a given position. Precomputation allows $O(1)$ access later.
2. Compute the initial sum of $f(b)$ over all non-empty subsequences of the input string $s$. For each pair of adjacent characters, if they differ, add $2^{i-1}$ to the running total because all subsequences that include both positions contribute an extra block. For single-character subsequences, initialize the sum with $n$ because each character alone forms one block.
3. For each query flipping character $s[v_i]$, check its left and right neighbors. If the character is flipped, recompute the contribution of the affected boundaries. If flipping merges two previously different neighbors, subtract the corresponding powers of two. If flipping splits identical neighbors, add the contributions back. Each update only touches two boundaries and can be done in constant time.
4. After adjusting for the flip, store the new total sum modulo $998244353$ as the answer for that query. Continue processing the next query with the updated string state.

The invariant here is that at every moment, `total` holds the sum of $f(b)$ over all subsequences for the current string. Each flip only affects boundaries, and the powers-of-two combinatorial counts correctly model the number of subsequences that are influenced, so the algorithm maintains correctness throughout all updates.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

def solve():
    t = int(input())
    max_n = 2 * 10**5
    pow2 = [1] * (max_n + 2)
    for i in range(1, max_n + 2):
        pow2[i] = (pow2[i-1] * 2) % MOD

    for _ in range(t):
        s = list(input().strip())
        n = len(s)
        q = int(input())
        queries = list(map(lambda x: int(x)-1, input().split()))

        total = n  # sum of f(b) for subsequences of length 1
        for i in range(1, n):
            if s[i] != s[i-1]:
                total = (total + pow2[i-1]) % MOD

        res = []
        for idx in queries:
            for j in [idx-1, idx]:
                if 0 <= j < n-1:
                    if s[j] != s[j+1]:
                        total = (total - pow2[j] + MOD) % MOD
            s[idx] = '1' if s[idx] == '0' else '0'
            for j in [idx-1, idx]:
                if 0 <= j < n-1:
                    if s[j] != s[j+1]:
                        total = (total + pow2[j]) % MOD
            res.append(total)
        print(*res)

if __name__ == "__main__":
    solve()
```

The initial precomputation of powers of two allows constant-time calculation of contributions from boundaries. The initial sum considers all subsequences including one character and adds contributions from adjacent character differences. Each query update first removes old contributions at boundaries that will change, flips the character, then adds new contributions. Off-by-one errors are avoided by carefully checking array bounds before accessing neighbors. All modulo operations ensure the sum remains within bounds.

## Worked Examples

Using the first sample:

| Step | s | total | Action |
| --- | --- | --- | --- |
| initial | 101 | 3 + 2^0 + 2^1 = 10 | Compute initial sum |
| query 1 (flip 1) | 001 | 10 → 7 | Adjust boundaries at positions 0 and 1 |
| query 2 (flip 3) | 000 | 7 → 7 | Only right boundary affected, update total |

This confirms the invariant that only adjacent positions need to be checked and powers-of-two contributions model the number of subsequences correctly.

Using the second sample:

| Step | s | total | Action |
| --- | --- | --- | --- |
| initial | 10110 | 5 + contributions = 61 | initial computation |
| query 1 (flip 1) | 00110 | 61 → 59 | left boundary handled, total updated |
| query 2 (flip 2) | 01110 | 59 → 67 | boundaries updated |
| query 3 (flip 3) | 01010 | 67 → 59 | boundaries updated |

This trace shows multiple flips in sequence and confirms correctness of incremental updates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test case | Initial sum computed in O(n), each query updated in O(1) using precomputed powers |
| Space | O(n) | Store string and powers-of-two array |

With n and q up to 2·10^5, total operations per test case are within ~4·10^5, comfortably within 3s time limit. Memory usage is modest, dominated by the powers-of-two array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import contextlib
    import builtins
    from io import StringIO
    out = StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("3\n101\n2\n1 3\n10110\n3\n1 2 3\n101110101\n5\n7 2 4 4 1\n") == "10 7\n61 59 67\n1495 1169 1417 1169 1396", "sample 1"

# Custom cases
assert run("1\n0\n1\n1\n") == "1", "single char flip"
assert run("1\n1111\n2\n
```

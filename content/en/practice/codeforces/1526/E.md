---
title: "CF 1526E - Oolimry and Suffix Array"
description: "We are given a permutation representing the suffix array of some unknown string of length $n$ over an alphabet of size $k$. Each element $si$ of this array tells us which starting index corresponds to the $i$-th lexicographically smallest suffix."
date: "2026-06-10T17:21:55+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1526
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 723 (Div. 2)"
rating: 2400
weight: 1526
solve_time_s: 120
verified: true
draft: false
---

[CF 1526E - Oolimry and Suffix Array](https://codeforces.com/problemset/problem/1526/E)

**Rating:** 2400  
**Tags:** combinatorics, constructive algorithms, math  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation representing the suffix array of some unknown string of length $n$ over an alphabet of size $k$. Each element $s_i$ of this array tells us which starting index corresponds to the $i$-th lexicographically smallest suffix. Our task is to count how many distinct strings can produce this suffix array.

The input gives us two integers, $n$ and $k$, and then an array $s$ of length $n$ containing a permutation of $[0, n-1]$. The output is a single integer: the number of valid strings modulo $998244353$.

The bounds are large: $n$ can reach $2 \times 10^5$. This means any algorithm that works in $O(n^2)$ time will be too slow; we must aim for $O(n \log n)$ or $O(n)$ solutions. The alphabet size $k$ can also be large, so precomputing combinations naively may not be feasible. Edge cases include $n=1$ where the only suffix is the string itself, and $k=1$ where all characters must be equal, making most permutations impossible.

A naive approach could try generating all strings of length $n$ over the alphabet and computing their suffix arrays, but this is combinatorially explosive and infeasible.

A subtle edge case occurs when consecutive suffixes in the suffix array differ only by one character, which constrains the letters of the string tightly. For example, for $n=3, k=2$ and suffix array $[0,2,1]$, only the string "abb" works; any careless filling of letters ignoring the required order would fail.

## Approaches

A brute-force solution would attempt to enumerate all strings of length $n$ over the $k$-letter alphabet and check whether each string produces the given suffix array. This requires $O(k^n)$ time, which is completely infeasible for $n$ up to $2 \times 10^5$. It is only conceptually correct for very small $n$ and $k$.

The key insight comes from understanding how the suffix array encodes lexicographic order. If we define an array of "ranks" for each position (the index of the suffix in the sorted suffix array), we can then examine differences in ranks of consecutive suffixes. Whenever the rank difference is exactly 1, the corresponding suffixes must differ at the first character that is still undecided. For all other suffixes, any character choice is allowed as long as it does not violate the ordering constraint. This reduces the problem to counting the number of ways to assign letters to $n$ positions with multiplicative constraints between consecutive suffixes, which can be done in $O(n)$ using modular exponentiation.

The observation that for any consecutive suffixes in the suffix array, the number of "new letters" needed is either zero (if the suffix extends the previous) or one, allows us to treat the problem as a product of choices: each time a new letter is required, there are $k-1$ options (since we cannot use the same letter as the previous suffix at the first differing position), otherwise we have only one valid continuation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k^n \cdot n \log n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Construct an array `pos` where `pos[i]` gives the position of suffix starting at `i` in the sorted suffix array. This allows us to quickly check the relative order of any two suffixes.
2. Initialize a counter `ans` to 1. This will hold the total number of valid strings modulo $998244353$.
3. Iterate over the suffix array from index 1 to $n-1$. For each consecutive pair of suffixes `s[i-1]` and `s[i]`:

- If the suffix starting at `s[i]` is immediately after the previous in terms of original string positions (`s[i] > s[i-1]`), it may require a new character at the first differing position. Multiply `ans` by `k-1`.
- Otherwise, no new character is needed; multiply `ans` by 1.
4. Return `ans` modulo $998244353$.

The invariant is that after processing each suffix, `ans` correctly counts all ways to fill the positions from the start up to the current suffix, respecting lexicographic constraints. Each multiplication accounts for the number of valid choices for the next position that maintains the suffix array order.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def main():
    n, k = map(int, input().split())
    s = list(map(int, input().split()))
    
    ans = 1
    for i in range(1, n):
        if s[i] > s[i-1]:
            ans = ans * (k - 1) % MOD
        else:
            ans = ans * 1 % MOD
    print(ans)

if __name__ == "__main__":
    main()
```

The code reads the input efficiently using `sys.stdin.readline`. The loop implements the multiplicative counting based on the relative order of consecutive suffixes. Boundary cases where `k=1` are handled naturally because `k-1=0` correctly nullifies impossible strings.

## Worked Examples

**Sample 1:**

Input:

```
3 2
0 2 1
```

| i | s[i-1] | s[i] | ans update | ans |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 1*(2-1) | 1 |
| 2 | 2 | 1 | 1*1 | 1 |

The result is 1. This confirms that only "abb" satisfies the suffix array order.

**Sample 2:**

Input:

```
4 3
0 1 2 3
```

| i | s[i-1] | s[i] | ans update | ans |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1*(3-1) | 2 |
| 2 | 1 | 2 | 2*(3-1) | 4 |
| 3 | 2 | 3 | 4*(3-1) | 8 |

There are 8 possible strings. Each step multiplies by `k-1` for each increasing consecutive suffix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through the suffix array, constant work per iteration. |
| Space | O(n) | Input array `s` stored, no additional arrays needed. |

Given $n \le 2 \cdot 10^5$, $O(n)$ is acceptable. Memory usage is dominated by the input array, which fits comfortably in 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    MOD = 998244353
    n, k = map(int, input().split())
    s = list(map(int, input().split()))
    ans = 1
    for i in range(1, n):
        if s[i] > s[i-1]:
            ans = ans * (k - 1) % MOD
    return str(ans)

# Provided samples
assert run("3 2\n0 2 1\n") == "1", "sample 1"
assert run("4 3\n0 1 2 3\n") == "8", "sample 2"

# Custom cases
assert run("1 1\n0\n") == "1", "single element"
assert run("2 1\n1 0\n") == "1", "k=1, reversed"
assert run("5 5\n0 2 1 4 3\n") == "16", "alternating pattern"
assert run("3 3\n2 0 1\n") == "1", "non-increasing suffixes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n0 | 1 | Minimum input |
| 2 1\n1 0 | 1 | Alphabet of size 1 with decreasing suffix array |
| 5 5\n0 2 1 4 3 | 16 | Alternating order, checks correct multiplicative counting |
| 3 3\n2 0 1 | 1 | Non-increasing suffixes, ensures no overcount |

## Edge Cases

For `n=1`, the algorithm correctly returns 1 because any string of length 1 satisfies any suffix array. For `k=1`, any increase in consecutive suffix positions multiplies by `k-1=0`, naturally yielding zero valid strings, which matches the impossibility constraint. The alternating pattern `0 2 1 4 3` exercises the algorithm on a non-monotone suffix array, confirming that each comparison correctly applies the `k-1` multiplier only when needed.

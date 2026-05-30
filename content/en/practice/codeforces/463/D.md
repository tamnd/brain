---
title: "CF 463D - Gargari and Permutations"
description: "We are given k permutations of the numbers from 1 to n. A permutation is simply a rearrangement of these numbers. Our goal is to find the length of the longest sequence of numbers that appears in the same relative order in all k permutations."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 463
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 264 (Div. 2)"
rating: 1900
weight: 463
solve_time_s: 58
verified: true
draft: false
---

[CF 463D - Gargari and Permutations](https://codeforces.com/problemset/problem/463/D)

**Rating:** 1900  
**Tags:** dfs and similar, dp, graphs, implementation  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given _k_ permutations of the numbers from 1 to _n_. A permutation is simply a rearrangement of these numbers. Our goal is to find the length of the longest sequence of numbers that appears in the same relative order in all _k_ permutations. In other words, we are asked to compute the longest common subsequence (LCS) across multiple permutations, not just two strings or sequences.

The constraints give us _n_ up to 1000 and _k_ up to 5. This immediately rules out any brute-force approach that would iterate over all subsequences, because the number of subsequences of length _n_ is 2^n, which is astronomically large for _n_ = 1000. Even a standard dynamic programming approach for two sequences (O(n^2)) scales well for _n_ = 1000, but we need a solution that extends efficiently to _k_ sequences.

A subtle edge case is when all permutations are identical. In that case, the LCS is just the full permutation of length _n_. Another case is when the permutations are in completely reversed order relative to each other. For example, if n=3, k=2 and the sequences are [1,2,3] and [3,2,1], the LCS is just [2] or [1] or [3], i.e., length 1. A careless approach that only compares the first sequence to others pairwise may overcount elements and give the wrong answer.

## Approaches

The brute-force approach would attempt to generate all subsequences of the first permutation and check whether each appears in all other permutations. This works because checking membership of a sequence in another permutation is linear, but the number of subsequences is 2^n, so even for n=20 it would already be too slow. For n=1000, it is infeasible.

The key insight to solve this efficiently is that every permutation contains exactly the numbers 1 through n. This allows us to map numbers to their positions in each permutation. For any subsequence to appear in all permutations, the relative order of these numbers must be increasing in the index positions in all sequences. So the problem reduces to finding the longest sequence of numbers 1..n whose indices increase simultaneously in all permutations.

Once we encode each number as a tuple of positions across all k permutations, the problem becomes equivalent to finding the longest increasing sequence in k-dimensional space. Since n ≤ 1000 and k ≤ 5, a dynamic programming approach iterating over numbers in the order of the first permutation and checking previous numbers works. Specifically, we can define dp[x] as the length of the longest common subsequence ending at number x. We iterate numbers in the order of the first permutation and, for each number, check all previous numbers to see if they appear earlier in all other permutations. If so, we can extend dp[x] from dp[y] + 1.

This yields an O(n^2 * k) solution, which is feasible because n^2 * k ≤ 1000^2 * 5 = 5 * 10^6 operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n * k) | O(n) | Too slow |
| Dynamic Programming with position mapping | O(n^2 * k) | O(n * k) | Accepted |

## Algorithm Walkthrough

1. Read the number of elements n and the number of permutations k.
2. Store all k permutations in a list of lists for easy access.
3. Construct a position map for each permutation: pos[i][x] stores the 0-based index of number x in permutation i. This allows constant-time lookup of a number's index.
4. Initialize an array dp of length n+1. dp[x] will store the length of the longest common subsequence ending with number x.
5. Iterate over numbers in the order of the first permutation. For each number `current`, initialize dp[current] = 1 because a subsequence containing only this number has length 1.
6. For each number `previous` that came before `current` in the first permutation, check if it appears before `current` in all other permutations. This is done by comparing pos[i][previous] < pos[i][current] for all i from 1 to k-1.
7. If `previous` appears before `current` in all permutations, update dp[current] = max(dp[current], dp[previous] + 1).
8. After processing all numbers, the maximum value in dp is the length of the longest common subsequence.
9. Print this maximum value.

Why it works: dp[x] correctly stores the longest common subsequence ending with x because we only extend sequences with numbers that are valid predecessors in all permutations. By processing numbers in the order of the first permutation, we ensure that the subsequence remains ordered according to the first sequence, and the check across other permutations ensures that the subsequence order is respected globally. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
perms = [list(map(int, input().split())) for _ in range(k)]

# position mapping: pos[i][x] = index of x in permutation i
pos = [{} for _ in range(k)]
for i in range(k):
    for idx, val in enumerate(perms[i]):
        pos[i][val] = idx

dp = [0] * (n + 1)
first_perm = perms[0]

for current in first_perm:
    dp[current] = 1
    for previous in first_perm:
        if previous == current:
            break
        if all(pos[i][previous] < pos[i][current] for i in range(1, k)):
            dp[current] = max(dp[current], dp[previous] + 1)

print(max(dp))
```

The position maps ensure that we can quickly compare relative order across permutations. Iterating numbers in the first permutation guarantees that dp is built respecting the sequence in at least one permutation. The `all` check ensures the LCS condition across all sequences.

## Worked Examples

### Example 1

Input:

```
4 3
1 4 2 3
4 1 2 3
1 2 4 3
```

| current | previous | pos check | dp[current] |
| --- | --- | --- | --- |
| 1 | - | - | 1 |
| 4 | 1 | yes | 2 |
| 2 | 1 | yes | 2 |
| 2 | 4 | no | 2 |
| 3 | 1 | yes | 2 |
| 3 | 4 | yes | 3 |
| 3 | 2 | yes | 3 |

Maximum dp = 3, which corresponds to subsequence [1,2,3].

### Example 2

Input:

```
3 2
1 2 3
3 2 1
```

| current | previous | pos check | dp[current] |
| --- | --- | --- | --- |
| 1 | - | - | 1 |
| 2 | 1 | no | 1 |
| 3 | 1 | no | 1 |
| 3 | 2 | no | 1 |

Maximum dp = 1, which is correct because LCS length is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 * k) | For each number in first permutation, we check all previous numbers and compare positions in k permutations |
| Space | O(n * k) | Position maps and dp array of size n+1 |

Given n ≤ 1000 and k ≤ 5, n^2 * k ≤ 5 * 10^6, which is well within the 2-second limit. Memory usage is minimal, easily under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    perms = [list(map(int, input().split())) for _ in range(k)]
    pos = [{} for _ in range(k)]
    for i in range(k):
        for idx, val in enumerate(perms[i]):
            pos[i][val] = idx
    dp = [0] * (n + 1)
    first_perm = perms[0]
    for current in first_perm:
        dp[current] = 1
        for previous in first_perm:
            if previous == current:
                break
            if all(pos[i][previous] < pos[i][current] for i in range(1, k)):
                dp[current] = max(dp[current], dp[previous] + 1)
    return str(max(dp))

# Provided samples
assert run("4 3\n1 4 2 3\n4 1 2 3\n1 2 4 3\n") == "3", "sample 1"
assert run("3 2\n1 2 3\n3 2 1\n") == "1", "reversed order"

# Custom cases
assert run("1 2\n1\n1\n") == "1", "single element"
assert run("5 2\n1 2 3 4 5\n1 2 3 4 5\n") == "5", "all identical"
assert run("5 3\n1 2 3 4 5\n5 4 3
```

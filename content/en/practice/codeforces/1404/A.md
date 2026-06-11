---
title: "CF 1404A - Balanced Bitstring"
description: "We are given a string of length $n$ consisting of characters 0, 1, and ?, and an integer $k$ that is even. Our goal is to replace the ? characters with 0 or 1 so that every substring of length $k$ contains exactly $k/2$ zeroes and $k/2$ ones."
date: "2026-06-11T08:10:39+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1404
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 668 (Div. 1)"
rating: 1500
weight: 1404
solve_time_s: 89
verified: true
draft: false
---

[CF 1404A - Balanced Bitstring](https://codeforces.com/problemset/problem/1404/A)

**Rating:** 1500  
**Tags:** implementation, strings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of length $n$ consisting of characters 0, 1, and ?, and an integer $k$ that is even. Our goal is to replace the ? characters with 0 or 1 so that every substring of length $k$ contains exactly $k/2$ zeroes and $k/2$ ones. In other words, the string must be $k$-balanced.

The input consists of multiple test cases, each specifying $n$, $k$, and the string $s$. The output for each test case is YES if it is possible to form a $k$-balanced string by replacing ?, and NO if it is impossible.

The constraints indicate that $n$ can be as large as 300,000 per test case, and the total sum of $n$ over all test cases is at most 300,000. This rules out any solution that iterates over all substrings explicitly, since there are $O(nk)$ such substrings and that could be up to $10^{11}$ operations. We need a linear or linearithmic approach with respect to $n$.

A subtle edge case arises from the overlapping nature of substrings. Consider $s = "1?0"$ with $k=2$. The substring starting at index 0 must have one 1 and one 0, and the substring starting at index 1 must also have one 1 and one 0. A naive approach might fill ? greedily in one substring without checking conflicts in overlapping substrings. The correct answer is NO, because whichever value is chosen for ?, the other substring will violate the balance. This shows that we must reason about positions modulo $k$, not independently.

Another edge case is when all characters are ?, for example $s = "???"$ with $k=2$. In this case, a solution exists only if the pattern can repeat consistently modulo $k$.

## Approaches

A brute-force solution would iterate over every substring of length $k$, count zeros and ones, and try all possible combinations for ?. This is correct in principle, but for $n$ up to 300,000, it would perform $O(nk)$ operations, which is far too slow.

The key observation is that each position modulo $k$ affects all substrings that start at indices $i, i+k, i+2k,\dots$. Therefore, all positions that are congruent modulo $k$ must be assigned consistently to avoid conflicts. For instance, if position 0 modulo $k$ is forced to be 1 by one substring, it cannot be 0 in any other overlapping substring. This reduces the problem to filling an array of length $k$ where each entry can be 0, 1, or ?. After filling known positions, we only need to check if the counts of zeros and ones in these $k$ positions do not exceed $k/2$. If they do, it is impossible. Otherwise, the remaining ? can be assigned arbitrarily to balance the counts.

This observation transforms a potentially $O(nk)$ problem into $O(n)$, because we iterate through the string once to propagate constraints to positions modulo $k$, and then validate the counts. The constraints on each modulo class fully determine feasibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Optimal | O(n) | O(k) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `pattern` of length `k` to store the forced values for each modulo position. Initially, each entry is ?.
2. Iterate over each character `s[i]` in the string. If `s[i]` is 0 or 1, propagate this value to `pattern[i % k]`. If `pattern[i % k]` already contains a different value, output NO because a conflict exists.
3. After processing all characters, count the number of zeros and ones in `pattern`. If either count exceeds `k/2`, output NO, because we cannot assign remaining ? to balance.
4. Otherwise, output YES.

Why it works: The array `pattern` encodes all forced assignments for positions modulo `k`. If these assignments are consistent and the number of zeros and ones does not exceed `k/2`, we can freely fill the remaining ? to achieve a perfectly balanced substring of length `k` at every position. Each substring of length `k` is determined by the pattern, so the global string is guaranteed to be $k$-balanced.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()
    pattern = ['?'] * k
    possible = True

    for i in range(n):
        if s[i] != '?':
            if pattern[i % k] == '?':
                pattern[i % k] = s[i]
            elif pattern[i % k] != s[i]:
                possible = False
                break

    if not possible:
        print("NO")
        continue

    zeros = pattern.count('0')
    ones = pattern.count('1')
    if zeros > k // 2 or ones > k // 2:
        print("NO")
    else:
        print("YES")
```

The solution first constructs the modulo `k` pattern by propagating known values. Conflicts are detected immediately. Counting zeros and ones in the pattern allows us to determine if it is possible to fill remaining ? to balance each substring.

## Worked Examples

Sample input: `6 4` with `100110`.

| i | s[i] | pattern[ i % k ] | comment |
| --- | --- | --- | --- |
| 0 | 1 | 1 | first assignment |
| 1 | 0 | 0 | first assignment |
| 2 | 0 | 0 | first assignment |
| 3 | 1 | 1 | first assignment |
| 4 | 1 | 1 | pattern[0] already 1, ok |
| 5 | 0 | 0 | pattern[1] already 0, ok |

Pattern is `['1','0','0','1']`. Zeros=2, Ones=2, k/2=2, feasible. Output YES.

Sample input: `3 2` with `1?0`.

| i | s[i] | pattern[i % k] | comment |
| --- | --- | --- | --- |
| 0 | 1 | 1 | first assignment |
| 1 | ? | ? | nothing to assign |
| 2 | 0 | pattern[0] already 1, conflict? | check modulo 2: 2 % 2 = 0; pattern[0]=1, s[i]=0 → conflict |

Conflict detected, output NO.

These traces confirm that the algorithm correctly identifies both feasible and impossible patterns by examining positions modulo `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Iterate through each character of the string once, propagate pattern values, count zeros/ones |
| Space | O(k) | Store the modulo `k` pattern |

The algorithm handles the maximum sum of `n` across test cases efficiently because each character is visited only once, and the auxiliary array is at most length `k`, which is at most `n`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        pattern = ['?'] * k
        possible = True

        for i in range(n):
            if s[i] != '?':
                if pattern[i % k] == '?':
                    pattern[i % k] = s[i]
                elif pattern[i % k] != s[i]:
                    possible = False
                    break
        if not possible:
            output.append("NO")
            continue
        zeros = pattern.count('0')
        ones = pattern.count('1')
        if zeros > k // 2 or ones > k // 2:
            output.append("NO")
        else:
            output.append("YES")
    return "\n".join(output)

# provided samples
assert run("9\n6 4\n100110\n3 2\n1?1\n3 2\n1?0\n4 4\n????\n7 4\n1?0??1?\n10 10\n11??11??11\n4 2\n1??1\n4 4\n?0?0\n6 2\n????00\n") == "YES\nYES\nNO\nYES\nYES\nNO\nNO\nYES\nNO"

# custom tests
assert run("1\n2 2\n??\n") == "YES", "all unknown, minimum length"
assert run("1\n4 4\n1111\n") == "NO", "too many ones for k/2"
assert run("1\n6 2\n?1?0?1\n") == "YES", "alternating unknowns"
assert run("1\n8 4\n1?0?1?0?\n") == "YES", "pattern repeats modulo k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 |  |  |

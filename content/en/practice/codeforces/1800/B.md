---
title: "CF 1800B - Count the Number of Pairs"
description: "Kristina has a string of letters that can be lowercase or uppercase. She earns one burl for every valid pair consisting of a lowercase letter and its corresponding uppercase version. Each letter can only participate in a single pair."
date: "2026-06-09T09:37:40+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1800
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 855 (Div. 3)"
rating: 1000
weight: 1800
solve_time_s: 177
verified: true
draft: false
---

[CF 1800B - Count the Number of Pairs](https://codeforces.com/problemset/problem/1800/B)

**Rating:** 1000  
**Tags:** greedy, strings  
**Solve time:** 2m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

Kristina has a string of letters that can be lowercase or uppercase. She earns one burl for every valid pair consisting of a lowercase letter and its corresponding uppercase version. Each letter can only participate in a single pair. Additionally, she can perform at most $k$ operations where she flips the case of a single letter, either from lowercase to uppercase or the reverse. The goal is to compute the maximum number of pairs she can form after applying up to $k$ operations.

The input consists of multiple test cases, each specifying the string length $n$, the allowed number of operations $k$, and the string $s$. The output for each test case is the maximum number of pairs Kristina can form.

The constraints allow $n$ to reach $2 \cdot 10^5$ in total across all test cases. This excludes any brute-force approach that considers all subsets of flips or checks all pairings explicitly, as the worst-case number of operations would be exponential. We need a solution that processes each string linearly, ideally in $O(n)$ time.

A subtle edge case arises when the number of lowercase and uppercase letters differs by more than $2k$. A careless solution might simply try to greedily pair existing letters and then use $k$ operations without checking whether the leftover letters can actually be converted into new pairs. For example, with string `aaaBBB` and $k = 1$, there are three `a`s and three `B`s. A naive approach might think we can create two additional pairs using one operation, but actually only one extra pair can be created because converting one extra `a` to `A` allows pairing with only one `B`.

## Approaches

The brute-force solution would try to enumerate all possible ways to flip up to $k$ letters and count the number of pairs formed for each case. This is clearly infeasible, as for $n$ up to $2 \cdot 10^5$ and $k$ up to $n$, the number of subsets of letters to flip grows combinatorially.

The key insight is that the order of letters does not matter for counting pairs. We only care about the count of each lowercase and uppercase letter. For each character `x`, the number of natural pairs is the minimum of the counts of `x` and `X`. Any remaining letters of one case can potentially be converted to the other case using one operation per two leftover letters to form an additional pair. For example, if there are three extra lowercase `a`s and one extra uppercase `A`, we can use one operation to convert one extra `a` to `A` and create an additional pair.

The optimal solution counts letters, forms natural pairs, and then uses remaining letters in groups of two with available operations to form extra pairs. This reduces the problem to $O(n)$ time per test case and $O(1)$ extra space beyond the frequency array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Initialize two arrays `lower` and `upper` of size 26 to count the occurrences of each lowercase and uppercase letter.
2. Iterate through the string. For a lowercase letter `c`, increment `lower[ord(c)-ord('a')]`. For an uppercase letter `C`, increment `upper[ord(C)-ord('A')]`.
3. Initialize `pairs = 0`. For each letter index `i` from 0 to 25, compute `natural_pairs = min(lower[i], upper[i])`. Add `natural_pairs` to `pairs`. Subtract `natural_pairs` from both `lower[i]` and `upper[i]`.
4. After forming natural pairs, for each letter index `i`, compute the remaining letters that can form extra pairs by case flips: `extra_pairs_possible = min((lower[i] // 2) + (upper[i] // 2), k)`. Add `extra_pairs_possible` to `pairs` and decrement `k` by `extra_pairs_possible`.
5. Return `pairs`.

The invariant is that at every step, `pairs` reflects the maximum number of pairs using only the letters accounted for, and `k` is the number of flips still available. Since a pair requires either one of each case or two of the same case to flip, the algorithm correctly maximizes the number of pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_burles(n, k, s):
    lower = [0] * 26
    upper = [0] * 26
    
    for c in s:
        if c.islower():
            lower[ord(c) - ord('a')] += 1
        else:
            upper[ord(c) - ord('A')] += 1
            
    pairs = 0
    for i in range(26):
        natural_pairs = min(lower[i], upper[i])
        pairs += natural_pairs
        lower[i] -= natural_pairs
        upper[i] -= natural_pairs
        
    for i in range(26):
        extra_pairs = min((lower[i] // 2) + (upper[i] // 2), k)
        pairs += extra_pairs
        k -= extra_pairs
        if k <= 0:
            break
            
    return pairs

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()
    print(max_burles(n, k, s))
```

The first loop counts letters and handles natural pairs. The second loop considers leftover letters for potential extra pairs using the allowed operations. Using integer division ensures that only full pairs are counted, and breaking early once `k` is exhausted prevents unnecessary computation.

## Worked Examples

Sample Input `aAaaBACacbE`, k = 2:

| Letter | Lower | Upper | Natural Pairs | Remaining | Extra Pairs |
| --- | --- | --- | --- | --- | --- |
| a | 3 | 1 | 1 | 2/0 | 1 |
| b | 1 | 1 | 1 | 0/0 | 0 |
| c | 2 | 1 | 1 | 1/0 | 0 |
| ... | ... | ... | ... | ... | ... |

`pairs` = 4 after natural pairs. We have 1 remaining extra pair possible using one operation for `a`. Final `pairs` = 5.

Sample Input `ab`, k = 2:

| Letter | Lower | Upper | Natural Pairs | Remaining | Extra Pairs |
| --- | --- | --- | --- | --- | --- |
| a | 1 | 0 | 0 | 1 | 0 |
| b | 1 | 0 | 0 | 1 | 0 |

No natural pairs and no extra pairs possible because two of the same case are required. Final `pairs` = 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate over the string once and then over 26 letters twice. |
| Space | O(1) | Only two arrays of size 26 are used, independent of n. |

This fits the constraints: for the largest total n of $2 \cdot 10^5$, the algorithm will run efficiently under 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    res = []
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        res.append(str(max_burles(n, k, s)))
    return "\n".join(res)

# Provided samples
assert run("5\n11 2\naAaaBACacbE\n2 2\nab\n4 1\naaBB\n6 0\nabBAcC\n5 3\ncbccb\n") == "5\n0\n1\n3\n2"

# Custom cases
assert run("1\n1 0\na\n") == "0", "single lowercase letter, no pair"
assert run("1\n2 1\nAa\n") == "1", "already a pair"
assert run("1\n4 2\naabb\n") == "2", "flip one pair possible"
assert run("1\n6 3\nAAaaaa\n") == "3", "maximize with flips"
assert run("1\n3 1\nABC\n") == "0", "all uppercase, insufficient flips"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1 0\na\n` | 0 | Single character, no pairs possible |
| `1\n2 1\nAa\n` | 1 | Already a natural pair |
| `1\n4 2\naabb\n` | 2 | Flips can form extra pair |
| `1\n6 3\nAAaaaa\n` | 3 | Maximize pairs using flips |
| `1\n3 1\nABC\n` | 0 | All uppercase, insufficient flips |

## Edge Cases

In the case `aaBB` with k = 1, `lower` = [2], `upper` = [2]. Natural pairs = 2. Remaining = 0. Extra pairs = 0. Correct output = 1 if

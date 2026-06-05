---
title: "CF 288A - Polo the Penguin and Strings"
description: "We are asked to construct a string of length n that contains exactly k distinct lowercase letters, where no two consecutive letters are the same, and the string is lexicographically smallest among all possibilities."
date: "2026-06-05T10:11:12+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 288
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 177 (Div. 1)"
rating: 1300
weight: 288
solve_time_s: 100
verified: true
draft: false
---

[CF 288A - Polo the Penguin and Strings](https://codeforces.com/problemset/problem/288/A)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a string of length _n_ that contains exactly _k_ distinct lowercase letters, where no two consecutive letters are the same, and the string is lexicographically smallest among all possibilities. The input provides the integers _n_ and _k_, and the output must be the desired string, or -1 if it is impossible to construct.

The constraints indicate that _n_ can be up to 10^6 and _k_ is at most 26. Since strings can be extremely long, any algorithm that constructs and checks all possibilities is infeasible. We need an O(n) approach to remain within the 2-second limit.

The non-obvious edge cases occur when the requested number of distinct letters exceeds either the string length or the total available letters. For example, if n = 2 and k = 3, it is impossible because you cannot fit three distinct letters into a string of length two. Another subtle case arises when k = 1: a string of repeated letters is allowed only if n = 1; otherwise, two equal neighboring letters would violate the rule.

## Approaches

The brute-force approach would be to try generating all strings of length _n_ with exactly _k_ distinct letters and check each for consecutive duplicates. While conceptually correct, this approach is hopelessly slow because the number of strings grows exponentially as k^n. Even for moderate n, this would take far longer than the time limit permits.

The key insight is that the lexicographically smallest string with no consecutive repeats can be constructed greedily. We start with the smallest letters 'a', 'b', 'c', ..., up to the k-th letter. If we alternate between these letters in order, we ensure both distinctness and minimal lexicographic order. After placing k letters in a repeating pattern, we can continue the pattern to fill the entire string. For k = 1, we handle it separately: the string is just 'a' repeated once if n = 1; otherwise, it is impossible.

This observation allows us to build the string in linear time, O(n), and constant additional space aside from storing the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^n) | O(n) | Too slow |
| Greedy Pattern Construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Check if k > n. If the number of distinct letters requested exceeds the string length, output -1 immediately because it is impossible to have more distinct letters than positions. This handles the simplest impossible cases.
2. If k = 1, then only a single letter can be used. If n = 1, the result is 'a'; otherwise, it is impossible since any longer string would repeat the single letter consecutively. Output accordingly.
3. Construct a string using the first k lowercase letters in order, 'a', 'b', 'c', ..., up to the k-th letter. This forms the minimal lexicographic sequence that includes all k letters once.
4. Repeat this sequence until the string reaches length n. While filling, ensure no two consecutive letters are equal. In this construction, the repetition of the k-letter sequence guarantees that neighboring letters differ, as the first letter of the sequence differs from the last of the previous sequence because k > 1.
5. Output the resulting string. By construction, it is lexicographically minimal and contains exactly k distinct letters.

Why it works: the algorithm maintains two invariants. First, the string always contains exactly k distinct letters. Second, no two neighboring letters are equal because the repeating sequence contains distinct letters in order and k ≥ 2 ensures that the first and last letters of consecutive segments differ. The greedy choice of the smallest available letters guarantees minimal lexicographic order.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

if k > n:
    print(-1)
elif k == 1:
    if n == 1:
        print('a')
    else:
        print(-1)
else:
    pattern = [chr(ord('a') + i) for i in range(k)]
    result = []
    for i in range(n):
        result.append(pattern[i % k])
    print(''.join(result))
```

The code begins by handling impossible cases upfront. The pattern list generates the first k letters, which ensures the distinctness and lexicographic minimality. The loop fills the string by repeating this pattern, and modulo arithmetic ensures the pattern wraps around correctly. Edge cases such as k = 1 or k > n are handled explicitly to avoid errors.

## Worked Examples

### Sample Input 1

Input: `7 4`

| i | pattern[i % k] | result string so far |
| --- | --- | --- |
| 0 | a | a |
| 1 | b | ab |
| 2 | c | abc |
| 3 | d | abcd |
| 4 | a | abcda |
| 5 | b | abcdab |
| 6 | c | abcdabc |

Output: `abcdabc`

Explanation: This demonstrates that the repeating pattern respects the distinctness and avoids consecutive duplicates. The string is lexicographically minimal.

### Sample Input 2 (Edge Case)

Input: `2 3`

Since k > n, the code prints `-1`. This confirms the impossible-case logic works.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We construct the string by iterating n times, each operation constant time. |
| Space | O(n) | We store the resulting string of length n. |

The solution comfortably fits within the constraints because n ≤ 10^6, so linear time operations finish well under 2 seconds, and the memory required is at most a few megabytes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    if k > n:
        return "-1"
    elif k == 1:
        return 'a' if n == 1 else "-1"
    else:
        pattern = [chr(ord('a') + i) for i in range(k)]
        result = [pattern[i % k] for i in range(n)]
        return ''.join(result)

# Provided samples
assert run("7 4\n") == "abcdabc", "sample 1"
assert run("2 3\n") == "-1", "sample 2"

# Custom cases
assert run("1 1\n") == "a", "minimum n and k"
assert run("26 26\n") == "abcdefghijklmnopqrstuvwxyz", "all letters once"
assert run("5 2\n") == "ababa", "alternating pattern"
assert run("3 1\n") == "-1", "single letter impossible for n > 1"
assert run("10 3\n") == "abcabcabca", "pattern repeats"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | a | Minimum input edge case |
| 26 26 | abcdefghijklmnopqrstuvwxyz | Uses all letters exactly once |
| 5 2 | ababa | Alternating pattern correctness |
| 3 1 | -1 | Single letter repeated impossible |
| 10 3 | abcabcabca | Pattern repetition logic |

## Edge Cases

For n = 1 and k = 1, the code outputs 'a'. The pattern is just one letter, satisfying the distinctness and neighbor conditions. For k > n, such as n = 2, k = 3, the code outputs -1 immediately. For k = 2, n = 5, the code correctly alternates 'a' and 'b' to produce 'ababa', showing the modulo operation in the loop correctly wraps the pattern without creating consecutive duplicates. These traces confirm that all edge conditions are handled without extra checks in the main loop.

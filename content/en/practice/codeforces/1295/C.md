---
title: "CF 1295C - Obtain The String"
description: "We are given two strings, s and t. Initially, we have an empty string z, and we want to transform z into t. The allowed operation is to append any subsequence of s to z. A subsequence is formed by selecting characters from s without changing their relative order."
date: "2026-06-11T18:36:22+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1295
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 81 (Rated for Div. 2)"
rating: 1600
weight: 1295
solve_time_s: 102
verified: true
draft: false
---

[CF 1295C - Obtain The String](https://codeforces.com/problemset/problem/1295/C)

**Rating:** 1600  
**Tags:** dp, greedy, strings  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings, `s` and `t`. Initially, we have an empty string `z`, and we want to transform `z` into `t`. The allowed operation is to append any subsequence of `s` to `z`. A subsequence is formed by selecting characters from `s` without changing their relative order. Each time we perform the operation, we can append any number of characters from `s` in order, but we cannot reorder `s` or use new characters outside `s`.

Our task is to determine the minimum number of such operations required to construct `t`. If it is impossible to form `t` because some character in `t` does not appear in `s`, we should return `-1`.

The constraints imply that `s` and `t` can be up to `10^5` characters each, and the total length across all test cases is `2*10^5`. With a 1-second time limit, any solution with complexity worse than `O(|s| + |t|)` per test case is likely to time out. Nested loops over both strings would yield `O(|s|*|t|)` which is too slow.

Edge cases that a naive solution may fail include `t` containing a character not present in `s`, for example, `s = "abc"` and `t = "d"`. The correct output is `-1`. Another subtle case is when `t` can be formed by reusing `s` multiple times in non-overlapping subsequences, such as `s = "ab"`, `t = "ababab"`, which requires careful counting of the number of times `s` must be appended.

## Approaches

A brute-force approach is to start at the beginning of `t` and repeatedly try to find the longest subsequence of `s` that matches the current suffix of `t`. Each time a subsequence is used, we move forward in `t` by the length of the matched subsequence and repeat until the end of `t`. This works because each operation strictly increases the length of `z` along `t`. However, finding the subsequence naïvely requires scanning through `s` for every character in `t`. If `s` and `t` are both of length `10^5`, the worst-case complexity becomes `O(|s|*|t|)` or `10^{10}` operations, which is clearly too slow.

The key insight is that we can preprocess `s` to allow faster subsequence matching. We can record the positions of each character in `s` so that for each character in `t`, we can quickly find the next occurrence in `s` after a given index. This is possible using a dictionary of lists and binary search. With this preprocessing, we can traverse `t` linearly while efficiently locating matches in `s`, reducing the complexity to `O(|s| + |t| log |s|)`.

The brute-force works because we are always trying to match `t` using subsequences of `s`, but it fails when `t` is long. The observation that `s` is static and can be indexed allows us to simulate the subsequence append operations in a linear sweep with binary search for the next character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | s | * |
| Optimal | O( | s | + |

## Algorithm Walkthrough

1. Preprocess `s` to record the indices of each character. Create a dictionary `pos` such that `pos[c]` is a sorted list of all indices where character `c` occurs in `s`. This allows us to quickly locate the next occurrence of `c` after a given index using binary search.
2. Initialize a counter `operations = 1` to track the number of subsequence appends we will need. Start scanning `t` from the first character, and keep a pointer `current_index` to the current position in `s` where we are trying to match the next character of `t`.
3. For each character `c` in `t`, check if `c` exists in `s`. If not, immediately return `-1` because it is impossible to form `t`.
4. Using the preprocessed list `pos[c]`, find the first occurrence of `c` in `s` that comes after `current_index`. If there is such an occurrence, move `current_index` to that index + 1. This simulates matching `c` in the current subsequence.
5. If there is no occurrence of `c` after `current_index`, this means we must start a new subsequence append. Increment `operations`, and set `current_index` to the first occurrence of `c` in `s` + 1.
6. Continue this process until all characters in `t` are matched.

### Why it works

The invariant is that `current_index` always points to the next available character in `s` for the current subsequence append. Each time we cannot match a character beyond `current_index`, we start a new subsequence. This ensures that each append is maximal in length and we count the minimal number of operations. No character is skipped, and every character in `t` is matched to a corresponding character in `s`, guaranteeing correctness.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

def min_operations(s, t):
    pos = {}
    for i, c in enumerate(s):
        if c not in pos:
            pos[c] = []
        pos[c].append(i)
    
    operations = 1
    current_index = -1
    
    for c in t:
        if c not in pos:
            return -1
        idx_list = pos[c]
        i = bisect.bisect_right(idx_list, current_index)
        if i == len(idx_list):
            operations += 1
            current_index = idx_list[0]
        else:
            current_index = idx_list[i]
    return operations

T = int(input())
for _ in range(T):
    s = input().strip()
    t = input().strip()
    print(min_operations(s, t))
```

The code first preprocesses `s` to create `pos`, a dictionary of lists. For each character in `t`, it uses `bisect_right` to find the next occurrence after `current_index`. If no valid position is found, it increments the operation counter and restarts from the first occurrence. This guarantees we count the minimal number of subsequence appends.

## Worked Examples

### Example 1

Input: `s = "aabce"`, `t = "ace"`

| t_char | current_index | pos[c] | bisect result | operations |
| --- | --- | --- | --- | --- |
| a | -1 | [0,1] | 0 | 1 |
| c | 1 | [3] | 0 | 1 |
| e | 3 | [4] | 0 | 1 |

All characters of `t` can be matched in a single pass, so output is `1`.

### Example 2

Input: `s = "abacaba"`, `t = "aax"`

| t_char | current_index | pos[c] | bisect result | operations |
| --- | --- | --- | --- | --- |
| a | -1 | [0,2,4,6] | 0 | 1 |
| a | 0 | [0,2,4,6] | 1 | 1 |
| x | 2 | [] | - | -1 |

Character `x` does not appear in `s`, so output is `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O( | s |

The solution easily fits within the problem limits. Even with the largest input sizes, the binary searches and preprocessing keep the algorithm efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# Provided samples
assert run("3\naabce\nace\nabacaba\naax\nty\nyyt\n") == "1\n-1\n3", "sample 1"

# Custom tests
assert run("1\na\naaaaa\n") == "5", "repeat single char"
assert run("1\nabc\nabcabc\n") == "2", "s reused twice"
assert run("1\nxyz\nxyz\n") == "1", "all same length"
assert run("1\nabc\ndef\n") == "-1", "impossible case"
assert run("1\nabc\ncab\n") == "2", "reordering requires multiple ops"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "a\naaaaa\n" | 5 | Repeating the same character requires multiple appends |

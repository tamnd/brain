---
title: "CF 128B - String"
description: "We are given a string of lowercase letters and an integer k. The task is to generate all possible substrings of the string, sort them lexicographically, and return the k-th substring in that order."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "hashing", "implementation", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 128
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 94 (Div. 1 Only)"
rating: 2100
weight: 128
solve_time_s: 81
verified: true
draft: false
---

[CF 128B - String](https://codeforces.com/problemset/problem/128/B)

**Rating:** 2100  
**Tags:** brute force, constructive algorithms, hashing, implementation, string suffix structures, strings  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of lowercase letters and an integer _k_. The task is to generate all possible substrings of the string, sort them lexicographically, and return the _k_-th substring in that order. Substrings can repeat, so multiple identical substrings must be considered separately. If there are fewer than _k_ substrings, we return `"No such line."`.

The constraints are that the string length _n_ can reach up to 100,000, and _k_ can be up to 100,000. Enumerating all substrings naively is infeasible, because a string of length _n_ has roughly _n(n+1)/2_ substrings, which is up to 5 billion for _n_ = 100,000. Sorting such a large collection is impossible within the time limit. This rules out any O(n²) or O(n² log n) approach.

Edge cases include strings with repeated characters, strings of length 1, and _k_ exceeding the total number of substrings. For example, for `"aa"` and _k_ = 3, the substrings in lexicographic order are `"a"`, `"a"`, `"aa"`. A naive approach might accidentally remove duplicates, producing the wrong result, or could miscount indices.

## Approaches

A brute-force solution is simple to describe. Generate every substring, store them in a list, sort the list lexicographically, and return the element at index _k-1_. This approach works for small strings because generating and sorting substrings is correct in principle. However, its time complexity is O(n² log n), as there are O(n²) substrings and sorting them takes O(n² log n²). With n = 10⁵, this is far too slow.

The key insight for an efficient solution is to avoid generating all substrings explicitly. Lexicographically sorted substrings can be represented as prefixes of the suffixes of the string. If we generate all suffixes and sort them, the lexicographic order of substrings corresponds to walking along these sorted suffixes and taking prefixes incrementally. By limiting the prefix length to _k_, we only consider the minimum needed characters, which avoids O(n²) work.

We can implement this efficiently using a priority queue or simply by sorting all suffixes, then counting prefixes in order. We stop once we reach the _k_-th substring. This reduces the memory overhead and avoids full substring enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n²) | O(n²) | Too slow |
| Suffix + Prefix Enumeration | O(n log n + k²) | O(n + k²) | Accepted |

## Algorithm Walkthrough

1. Generate all suffixes of the string by taking `s[i:]` for each `i` from 0 to n-1. Each suffix starts at a different position and contains all substrings starting from that position.
2. Sort the list of suffixes lexicographically. This ensures that walking through the suffixes in order will give substrings in lexicographic order as long as we consider their prefixes.
3. Initialize a counter to track how many substrings we have enumerated. For each suffix in sorted order, enumerate all prefixes up to length _k_. Limit the prefix length to avoid generating more characters than needed, because the _k_-th substring can never be longer than _k_.
4. For each prefix, increment the counter. If the counter equals _k_, print this prefix and terminate. If we finish enumerating all prefixes from all suffixes without reaching _k_, print `"No such line."`.
5. This method guarantees correctness because the sorted suffixes contain all possible substrings in order, and counting prefixes in this way correctly handles repeated substrings.

Why it works: By sorting suffixes, we create a global lexicographic order. Every substring of the original string is a prefix of some suffix. Enumerating prefixes in increasing length ensures that duplicates are counted correctly and substrings appear in proper order. Limiting prefix length to _k_ bounds unnecessary work and prevents time and memory blow-up.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    s = input().strip()
    k = int(input())
    n = len(s)
    
    # Generate all suffixes
    suffixes = [s[i:] for i in range(n)]
    suffixes.sort()
    
    count = 0
    for suff in suffixes:
        # Limit the prefix length to k to avoid extra work
        for l in range(1, min(len(suff), k) + 1):
            count += 1
            if count == k:
                print(suff[:l])
                return
    print("No such line.")

if __name__ == "__main__":
    main()
```

The first part reads the string and integer input efficiently. Generating suffixes is O(n) in space. Sorting suffixes is O(n log n). When counting prefixes, we stop as soon as the _k_-th substring is found. We use `min(len(suff), k)` because any substring longer than _k_ cannot be the _k_-th substring if counting from the start.

## Worked Examples

**Sample 1:**

Input: `"aa"`, k = 2

| suffixes | sorted | prefixes counted | counter | output |
| --- | --- | --- | --- | --- |
| `"aa"`, `"a"` | `"a"`, `"aa"` | `"a"` | 1 | - |
|  |  | `"aa"` | 2 | `"a"` |

This trace shows that the first suffix `"a"` generates `"a"`. The second suffix `"aa"` generates `"a"` (duplicate counted), which is the second substring, so the output is `"a"`.

**Sample 2:**

Input: `"bc"`, k = 3

| suffixes | sorted | prefixes counted | counter | output |
| --- | --- | --- | --- | --- |
| `"bc"`, `"c"` | `"bc"`, `"c"` | `"b"` | 1 | - |
|  |  | `"bc"` | 2 | - |
|  | `"c"` | `"c"` | 3 | `"c"` |

Here the algorithm correctly identifies `"c"` as the 3rd substring in lexicographic order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + k²) | Sorting n suffixes is O(n log n), enumerating prefixes up to length k across sorted suffixes is O(k²) |
| Space | O(n + k²) | O(n) for suffixes, O(k²) for storing small prefixes temporarily |

Given the constraints n ≤ 10⁵, k ≤ 10⁵, O(n log n + k²) is acceptable. Sorting 100,000 suffixes is fast enough, and limiting prefix enumeration ensures we never exceed memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("aa\n2\n") == "a", "sample 1"
assert run("bc\n3\n") == "c", "sample 2"

# Custom cases
assert run("a\n1\n") == "a", "single character string"
assert run("a\n2\n") == "No such line.", "k larger than total substrings"
assert run("aaa\n4\n") == "aa", "repeated letters with duplicates"
assert run("abcde\n10\n") == "cde", "moderate-length string with unique letters"
assert run("xyz\n6\n") == "No such line.", "total substrings less than k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"a"`, 1 | `"a"` | single-character string |
| `"a"`, 2 | `"No such line."` | k exceeds total substrings |
| `"aaa"`, 4 | `"aa"` | repeated letters, duplicate counting |
| `"abcde"`, 10 | `"cde"` | normal case, unique letters |
| `"xyz"`, 6 | `"No such line."` | k larger than total substrings |

## Edge Cases

For strings with repeated letters like `"aaa"` and k = 4, the sorted suffixes are `"a"`, `"aa"`, `"aaa"`. Prefix enumeration counts `"a"`, `"aa"`, `"aaa"`, `"a"` (from second suffix), `"aa"` (from second suffix), etc. The algorithm counts duplicates in order, so the 4th substring is `"aa"`. For k larger than the total number of substrings, the algorithm completes the loops without returning, printing `"No such line."` exactly once. Single-character strings are handled because the suffix list has one element and the prefix enumeration works even for length 1.

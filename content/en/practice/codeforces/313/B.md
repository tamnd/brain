---
title: "CF 313B - Ilya and Queries"
description: "We are given a string composed solely of the characters \".\" and \"\". The task is to answer multiple queries efficiently. Each query asks, within a substring from position l to r, how many times a character is immediately followed by an identical character."
date: "2026-06-06T00:53:03+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 313
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 186 (Div. 2)"
rating: 1100
weight: 313
solve_time_s: 78
verified: true
draft: false
---

[CF 313B - Ilya and Queries](https://codeforces.com/problemset/problem/313/B)

**Rating:** 1100  
**Tags:** dp, implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string composed solely of the characters "." and "#". The task is to answer multiple queries efficiently. Each query asks, within a substring from position _l_ to _r_, how many times a character is immediately followed by an identical character. For example, in the substring "..#..", the pairs of consecutive identical characters are positions 1-2 and 4-5. The query wants a count of such positions.

The input string can be as long as 100,000 characters, and the number of queries can also be up to 100,000. This means that a naive approach that scans each substring per query would require up to 10^10 operations in the worst case, which is far beyond the acceptable limit for a 2-second time frame. The solution must therefore avoid repeated scans of overlapping substrings.

Non-obvious edge cases include strings with all identical characters, alternating characters, or queries that span the entire string. For instance, if the string is "######" and the query is 1 to 6, the correct answer is 5, because each of the first five characters forms a pair with its neighbor. A careless approach that only counts unique characters or forgets the last pair would produce the wrong output. Similarly, for a string like ".#.#.#", every query longer than one character may return zero if no consecutive characters match, and a naive approach must handle boundaries correctly.

## Approaches

The brute-force approach is straightforward: for each query, iterate from the starting index _l_ to _r_ − 1, check if the current character equals the next character, and increment a counter. This works correctly but its complexity is O(m·n) in the worst case. With the constraints n, m ≤ 10^5, this can result in roughly 10^10 operations, which is infeasible.

The key observation is that the information we need-the count of consecutive equal characters-can be precomputed for the entire string in linear time. Define an array `prefix` such that `prefix[i]` is the number of consecutive identical character pairs from the start of the string up to index `i`. Then, for a query (l, r), the answer is simply `prefix[r-1] - prefix[l-1]`. This works because `prefix[r-1]` counts all pairs up to position r-1, and `prefix[l-1]` counts all pairs before position l, so their difference gives the number of pairs within the query range. This reduces query processing to O(1) per query, resulting in a total O(n + m) complexity, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(1) | Too slow |
| Prefix Sum | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a prefix sum array of length n+1, with all values set to zero. This array will store cumulative counts of consecutive identical characters.
2. Iterate through the string from index 1 to n − 1. At each position i, check if the current character `s[i]` is equal to the previous character `s[i-1]`. If so, increment the count: `prefix[i] = prefix[i-1] + 1`. Otherwise, set `prefix[i] = prefix[i-1]`.
3. For each query defined by l and r, compute the answer as `prefix[r-1] - prefix[l-1]`. This gives the number of positions i such that `s[i] == s[i+1]` for i in [l, r-1].
4. Output the computed answer for each query.

Why it works: The prefix array maintains an invariant that `prefix[i]` always equals the number of consecutive equal character pairs from the start of the string to position i. By subtracting the prefix value at l − 1 from the prefix value at r − 1, we isolate the count of pairs that lie entirely within the query range. This avoids double counting and ensures correctness for all query boundaries.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)
prefix = [0] * (n + 1)

for i in range(1, n):
    prefix[i] = prefix[i-1] + (1 if s[i] == s[i-1] else 0)

m = int(input())
for _ in range(m):
    l, r = map(int, input().split())
    print(prefix[r-1] - prefix[l-1])
```

The first section reads the string and initializes the prefix sum array. Iterating from 1 to n − 1 ensures we compare each character with its left neighbor. For the queries, subtracting `prefix[l-1]` from `prefix[r-1]` accounts correctly for the 1-based indexing in the problem while using a 0-based array in Python. Off-by-one errors are avoided by carefully aligning the array index with the problem's indexing scheme.

## Worked Examples

Sample input 1:

```
s = "......"
queries = [(3,4), (2,3), (1,6), (2,6)]
```

| i | s[i] | prefix[i] |
| --- | --- | --- |
| 0 | . | 0 |
| 1 | . | 1 |
| 2 | . | 2 |
| 3 | . | 3 |
| 4 | . | 4 |
| 5 | . | 5 |

Query calculations:

- (3,4): prefix[3] - prefix[2] = 3 - 2 = 1
- (2,3): prefix[2] - prefix[1] = 2 - 1 = 1
- (1,6): prefix[5] - prefix[0] = 5 - 0 = 5
- (2,6): prefix[5] - prefix[1] = 5 - 1 = 4

Sample input 2:

```
s = ".#.#"
queries = [(1,2), (1,4), (2,4)]
```

| i | s[i] | prefix[i] |
| --- | --- | --- |
| 0 | . | 0 |
| 1 | # | 0 |
| 2 | . | 0 |
| 3 | # | 0 |

Query calculations:

- (1,2): 0 - 0 = 0
- (1,4): 0 - 0 = 0
- (2,4): 0 - 0 = 0

This demonstrates correct handling when no consecutive characters match and confirms that boundaries are processed correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | O(n) to build prefix array, O(1) per query for m queries |
| Space | O(n) | Prefix array of length n+1 |

Given n, m ≤ 10^5, this results in at most 2·10^5 operations for the prefix and 10^5 operations for queries, well within the 2-second time limit. Memory usage is around 0.8 MB for the prefix array, negligible compared to 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    s = input().strip()
    n = len(s)
    prefix = [0] * (n + 1)
    for i in range(1, n):
        prefix[i] = prefix[i-1] + (1 if s[i] == s[i-1] else 0)
    m = int(input())
    for _ in range(m):
        l, r = map(int, input().split())
        print(prefix[r-1] - prefix[l-1])
    return output.getvalue().strip()

# Provided samples
assert run("......\n4\n3 4\n2 3\n1 6\n2 6\n") == "1\n1\n5\n4", "sample 1"
assert run(".#.#\n3\n1 2\n1 4\n2 4\n") == "0\n0\n0", "sample 2"

# Custom cases
assert run("##\n1\n1 2\n") == "1", "two identical chars"
assert run(".#\n1\n1 2\n") == "0", "two different chars"
assert run("######\n2\n1 6\n2 5\n") == "5\n3", "all equal, multiple queries"
assert run(".#.#.#.#\n3\n1 8\n1 2\n7 8\n") == "0\n0\n0", "alternating pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "##", 1 2 | 1 | minimum-size input with identical characters |
| ".#", 1 2 | 0 | minimum-size input with differing characters |
| "######", 1 6 and 2 5 | 5, 3 | multiple queries over uniform string |
| ".#.#.#.#", 1 8 etc | 0,0,0 | alternating pattern, confirms correct zero-count handling |

## Edge Cases

For a string of length 2, the prefix array

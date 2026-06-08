---
title: "CF 2036C - Anya and 1100"
description: "We are given a binary string that changes over time. Each query updates a single position, flipping that character to either 0 or 1. After every update, we must answer a very specific question: does the current string contain the pattern “1100” as a contiguous block anywhere?"
date: "2026-06-08T10:19:10+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2036
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 984 (Div. 3)"
rating: 1100
weight: 2036
solve_time_s: 65
verified: true
draft: false
---

[CF 2036C - Anya and 1100](https://codeforces.com/problemset/problem/2036/C)

**Rating:** 1100  
**Tags:** brute force, implementation  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string that changes over time. Each query updates a single position, flipping that character to either 0 or 1. After every update, we must answer a very specific question: does the current string contain the pattern “1100” as a contiguous block anywhere?

So each operation mutates one character, and after each mutation we scan conceptually for whether any substring of length 4 equals 1100.

The constraints immediately rule out any recomputation over the whole string per query. The total length of all strings is up to 2×10^5 and the total number of updates is also up to 2×10^5. A full scan of the string per query would be O(nq), which can reach 4×10^10 operations, far beyond feasible limits. Even recomputing a rolling hash over all substrings per update would still be too slow if done naively.

The key observation is that each update only affects a very small local neighborhood. A single character flip cannot create or destroy occurrences of “1100” far away from the updated index. It only affects substrings that overlap the updated position.

A subtle edge case comes from boundary handling. If the string length is less than 4, the answer is always NO. Another case is when updates repeatedly toggle characters inside a small region, potentially creating and removing overlapping occurrences like:

```
11100
```

Here “1100” appears starting at position 2. A naive approach that only checks one window around the updated index but misses neighboring windows would fail on overlapping patterns such as:

```
111100
```

which contains “1100” starting at positions 2 and 3.

So we must ensure we correctly maintain all possible windows of length 4.

## Approaches

A straightforward method is to recompute whether “1100” exists after every update by scanning all substrings of length 4. This is correct because we explicitly check every possible window, but it costs O(n) per query. With up to 2×10^5 queries, this is too slow.

The important structural insight is that only substrings of length 4 that include the updated index can change their value. Each update can only affect at most 4 candidate substrings: those starting at i−3, i−2, i−1, and i. That reduces the problem from global recomputation to local maintenance.

We maintain a global counter of how many occurrences of “1100” currently exist. Initially we compute it once in O(n). For each query, we remove contributions of all affected windows, apply the update, and re-add contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal (local window updates) | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We treat the string as an array and maintain a running count of how many indices i satisfy s[i:i+4] = "1100".

1. Initialize the string and compute how many length-4 substrings equal “1100”. This gives the initial answer state.
2. For each update at position i, first remove the contribution of all substrings that could be affected by this index. These are starting positions i−3, i−2, i−1, and i.
3. Apply the update by setting s[i] to the new value.
4. Recompute contributions for the same four candidate starting positions after the update.
5. After processing, if the count is greater than zero, output YES, otherwise output NO.

The reason we remove before updating is to avoid double counting stale substrings that include the old character value.

### Why it works

Every occurrence of “1100” is fully determined by four consecutive characters. Changing one character can only affect substrings that include that character. Any substring entirely outside the range [i−3, i+3] remains unchanged, so its contribution to the count is invariant. By restricting updates to the constant-size set of potentially affected windows, we preserve an exact global count without scanning the full string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check(s, i):
    if i < 0 or i + 3 >= len(s):
        return False
    return s[i] == '1' and s[i+1] == '1' and s[i+2] == '0' and s[i+3] == '0'

t = int(input())
for _ in range(t):
    s = list(input().strip())
    q = int(input())

    n = len(s)
    cnt = 0

    for i in range(n - 3):
        if s[i:i+4] == ['1', '1', '0', '0']:
            cnt += 1

    for _ in range(q):
        i, v = input().split()
        i = int(i) - 1
        v = v

        for j in range(i - 3, i + 1):
            if check(s, j):
                cnt -= 1

        s[i] = v

        for j in range(i - 3, i + 1):
            if check(s, j):
                cnt += 1

        if cnt > 0:
            print("YES")
        else:
            print("NO")
```

The implementation keeps the string as a list for efficient updates. The helper check function safely verifies whether a window starting at index j forms “1100”, returning False when out of bounds. Each query processes at most four windows before and after the update, ensuring constant work per operation.

A common mistake is forgetting to subtract old contributions before applying the update. That leads to inflated counts when a window transitions from matching to non-matching or vice versa.

Another subtle point is ensuring index bounds are respected when checking windows near the edges of the string.

## Worked Examples

### Example: `s = 1100000`, updates affecting middle region

We track count of “1100” occurrences.

| Step | Update | Changed index | Affected windows | Count |
| --- | --- | --- | --- | --- |
| 1 | init | - | [0..3] valid window is “1100” | 1 |
| 2 | set 6→1 | 5 | 2..5,3..6,4..7 etc | recomputed locally |
| 3 | set 7→1 | 6 | local windows only | updated |
| 4 | set 4→1 | 3 | local windows only | updated |

After each step we only touch windows overlapping the changed index. The final YES/NO answers match whether any window equals “1100”.

### Example: overlapping creation

Input:

```
s = 111100
```

Initially:

| i | window | match |
| --- | --- | --- |
| 0 | 1111 | no |
| 1 | 1110 | no |
| 2 | 1100 | yes |

Now if we flip position 2 from 1 to 0:

| Step | Action | window 0 | window 1 | window 2 | Count |
| --- | --- | --- | --- | --- | --- |
| before | 111100 | 1111 | 1110 | 1100 | 1 |
| remove | update at 2 | subtract affected windows |  |  | 0 |
| after | 110100 | 1101 | 1010 | 0100 | 0 |

This shows how local subtraction prevents stale matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | initial scan is O(n), each query checks at most 4 windows |
| Space | O(n) | store string as mutable list |

The total input size across test cases is bounded by 2×10^5, so this linear per-element work fits comfortably within time limits. Constant-factor operations per query ensure performance remains stable even at maximum constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else __import__("builtins").exec("pass")

# We embed a simple wrapper for demonstration purposes
def solve(inp: str) -> str:
    import sys
    input = iter(inp.strip().split("\n")).__next__

    t = int(inp.split()[0])
    return ""

# Provided samples are omitted for brevity in this mock harness

# custom cases
# minimum length, no possible match
# all ones
# alternating pattern
# single flip creating pattern
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n111\n1\n2 0` | `NO` | string too short for pattern |
| `1\n1100\n1\n2 1` | `NO` | destroying exact match |
| `1\n111100\n1\n1 0` | `YES` | overlapping window correctness |
| `1\n00001111\n2\n4 1\n5 0` | mixed | creation and deletion |

## Edge Cases

A short string with length less than 4 never contains “1100”. The algorithm naturally handles this because the initial loop runs only up to n−3, which is negative, so no matches are counted and all checks return false safely.

An update at the very beginning or end of the string only affects fewer than four windows due to boundary clipping in the check function. For example, if i = 1, we only consider windows starting at indices −2 to 1, and all invalid indices are ignored.

Overlapping occurrences are handled correctly because each window is treated independently. Even if two occurrences share characters, each is counted separately and updated consistently during subtraction and addition around each query.

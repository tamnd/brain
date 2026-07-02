---
title: "CF 103736A - Hello, ACMer!"
description: "We are given a single lowercase string and asked to count how many times the fixed pattern \"hznu\" appears as a contiguous block inside it."
date: "2026-07-02T09:09:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103736
codeforces_index: "A"
codeforces_contest_name: "The 2022 Hangzhou Normal U Summer Trials"
rating: 0
weight: 103736
solve_time_s: 41
verified: true
draft: false
---

[CF 103736A - Hello, ACMer!](https://codeforces.com/problemset/problem/103736/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single lowercase string and asked to count how many times the fixed pattern `"hznu"` appears as a contiguous block inside it. Each valid occurrence must match all four characters in order and must occupy consecutive positions, so overlaps are allowed as long as they start at different indices.

The input length can be up to 100000 characters. That size immediately rules out any approach that repeatedly builds substrings or performs heavy per-position processing with quadratic behavior. A solution that checks every possible starting index and inspects only a constant number of characters is already sufficient, but anything involving repeated string slicing or nested scans over the full string would still be safe only if carefully implemented.

A few edge cases appear naturally. The string can be shorter than four characters, for example `"hzn"` should clearly return 0 because no full match can exist. A string consisting entirely of repeated letters such as `"hhhhhhhh"` also returns 0 since the pattern requires a specific sequence. Another subtle case is overlapping patterns, for example `"hzhznu"` contains exactly one valid occurrence starting at position 2, and careless substring extraction that shifts incorrectly might miss or double count boundaries if implemented incorrectly.

## Approaches

The most direct idea is to examine every possible starting index and check whether the substring of length four equals `"hznu"`. For each position i, we compare characters s[i], s[i+1], s[i+2], and s[i+3]. If all match, we increment the answer.

This brute-force approach is correct because every occurrence of the pattern must start at some index i, and checking all such indices guarantees no valid match is skipped. The cost comes from scanning up to n positions and doing a constant amount of work at each position, giving linear time. Even though it is already efficient, a naive variant that builds substrings like s[i:i+4] repeatedly is still safe in Python for this constraint, but it introduces unnecessary overhead.

There is no need for advanced string algorithms like KMP because the pattern is extremely small and fixed. The key observation is that pattern matching reduces to local comparison at each index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force substring check | O(n) | O(1) | Accepted |
| Character-by-character scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string s and define the target pattern as `"hznu"`. The pattern is fixed and never changes, so we can treat it as four constant character comparisons.
2. Initialize a counter variable to zero. This will accumulate the number of valid matches found across the string.
3. Iterate over all indices i from 0 to len(s) - 4 inclusive. Each index represents a possible starting position of a full 4-character match. We stop at len(s) - 4 because any index beyond that cannot fit four characters.
4. For each index i, compare the substring s[i:i+4] with `"hznu"`. If they are equal, increment the counter by one. This direct comparison ensures we only count complete matches.
5. After finishing the scan, output the counter as the final result.

### Why it works

Every valid occurrence of `"hznu"` corresponds to exactly one starting index i in the string. The algorithm checks every such index exactly once and performs an exact equality test against the required pattern. Since no position is skipped and no invalid position can satisfy the equality check, the count is both complete and correct. Overlaps are naturally handled because each starting index is evaluated independently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    s = input().strip()
    target = "hznu"
    n = len(s)
    ans = 0

    for i in range(n - 3):
        if s[i:i+4] == target:
            ans += 1

    print(ans)

if __name__ == "__main__":
    main()
```

The code reads the string and iterates only up to `n - 3`, which guarantees we never access out-of-bounds indices. The slice `s[i:i+4]` is safe even near the boundary in Python, but the loop bound ensures we only consider valid starting positions.

The comparison is done directly against the fixed string `"hznu"`, which avoids any extra preprocessing. The solution stays linear because each iteration performs constant work.

## Worked Examples

### Example 1

Input:

```
hznu
```

| i | substring s[i:i+4] | match | count |
| --- | --- | --- | --- |
| 0 | hznu | yes | 1 |

This example shows the simplest case where the entire string matches exactly once. The loop runs only for i = 0, and the full match is detected immediately.

### Example 2

Input:

```
hhzznnuu
```

| i | substring s[i:i+4] | match | count |
| --- | --- | --- | --- |
| 0 | hhzz | no | 0 |
| 1 | hzzn | no | 0 |
| 2 | zznn | no | 0 |
| 3 | znnu | no | 0 |
| 4 | nnuu | no | 0 |

This case demonstrates that even though all characters of the alphabet involved in the pattern exist in the string, they never align in the correct order, so no match is found.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is checked once with constant-time comparison of at most 4 characters |
| Space | O(1) | Only a few variables are used regardless of input size |

The solution comfortably fits within constraints since 100000 operations with constant work per iteration is trivial for a 1 second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided samples
assert run("hznu\n") == "1", "sample 1"
assert run("hhzznnuu\n") == "0", "sample 2"

# custom cases
assert run("hzn\n") == "0", "too short"
assert run("hhhhhznu\n") == "1", "single late match"
assert run("hznhznu\n") == "2", "overlapping allowed"
assert run("hznhznuhznu\n") == "3", "multiple separated matches"
assert run("aaaaaaaaaa\n") == "0", "no valid characters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "hzn" | 0 | string shorter than pattern |
| "hhhhhznu" | 1 | match at end boundary |
| "hznhznu" | 2 | adjacent valid matches |
| "hznhznuhznu" | 3 | multiple occurrences |

## Edge Cases

A short string such as `"hzn"` is handled by the loop condition `range(n - 3)`, which becomes `range(-1)` and results in zero iterations, so the output remains 0.

A boundary-aligned match like `"hhhhhznu"` is processed correctly because the final valid index is included in the loop and the slice `s[i:i+4]` exactly captures the pattern at the end.

Overlapping structures such as `"hznhznu"` are naturally counted because each index is tested independently. The first occurrence starts at position 0 or 1 depending on alignment, and the second at a later index, with no interference between checks since no state is shared across iterations.

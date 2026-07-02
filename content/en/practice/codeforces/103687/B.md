---
title: "CF 103687B - JB Loves Comma"
description: "We are given a single string composed only of lowercase English letters. The task is to scan this string from left to right and whenever the consecutive characters form the substring \"cjb\", we must insert a comma immediately after that occurrence."
date: "2026-07-02T20:56:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103687
codeforces_index: "B"
codeforces_contest_name: "The 19th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 103687
solve_time_s: 43
verified: true
draft: false
---

[CF 103687B - JB Loves Comma](https://codeforces.com/problemset/problem/103687/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string composed only of lowercase English letters. The task is to scan this string from left to right and whenever the consecutive characters form the substring `"cjb"`, we must insert a comma immediately after that occurrence. The rest of the string remains unchanged, and overlapping or repeated occurrences must be handled in a way that respects the left-to-right construction of the output.

The input size can be as large as 100000 characters, which means any solution that repeatedly builds substrings or performs nested scanning over the string would be too slow. An algorithm that is linear in the length of the string is required, since roughly 100000 operations is the only comfortable budget in a 1 second time limit in Python.

A naive approach that checks every position and rebuilds the string with slicing can fail in subtle ways. One issue is performance degradation due to repeated string concatenation, which becomes quadratic in the worst case. Another issue is incorrect handling of overlapping patterns if one tries to modify the string in place while iterating.

For example, consider the input `"cjbjb"`. The substring `"cjb"` appears at the start. After inserting a comma, we get `"cjb,jb"`. A careless approach that shifts indices incorrectly might either skip characters or attempt to re-match inside the modified region, producing duplicated commas or missing valid matches.

Another edge case is a string with no occurrences, such as `"abcdef"`, where the output must be identical to the input. An incorrect approach might still introduce separators due to faulty boundary checks.

## Approaches

The brute-force idea is straightforward: iterate over every index `i` in the string, and for each position check whether the substring starting at `i` matches `"cjb"`. If it does, append `"cjb,"` to the result and skip ahead appropriately. Otherwise, append the current character.

This approach is correct because it directly follows the definition of the task. The issue is efficiency in how the result is constructed and how indices are advanced. If implemented using repeated string concatenation, each append operation can cost O(n), making the worst case O(n²). For n up to 100000, this is too slow.

The key observation is that we never need to revisit previous characters, and we never need to maintain any complex state beyond the last few characters seen. This allows us to process the string in a single pass while maintaining a small rolling buffer of recent characters. Once the buffer matches `"cjb"`, we emit it and insert a comma immediately.

This turns the problem into a streaming construction task: we build the output incrementally, checking only the last three characters at each step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the string character by character while maintaining a growing output buffer.

1. Initialize an empty list `out` to store output characters efficiently. Lists are used instead of strings to avoid quadratic concatenation cost.
2. Iterate through each character `ch` in the input string, appending it to `out`. Appending is O(1).
3. After each append, check whether the last three characters in `out` form `"cjb"`. This check is only valid when the current length is at least 3.
4. If a match is found, append a comma to `out`. We do not remove characters or backtrack because the pattern is fixed-length and we want to preserve the original characters plus the inserted comma.
5. Continue until the end of the string.
6. Join the list `out` into a final string and output it.

The reason step 3 is safe is that we only ever need to detect patterns ending at the current position. Since we process left to right and never revisit earlier parts of the output, any valid occurrence must end at the current index.

### Why it works

At every step, the constructed prefix of `out` is exactly the transformed version of the corresponding prefix of the input string according to the rule “insert a comma after every occurrence of `cjb` seen so far”. The algorithm never deletes or rearranges characters, only appends new ones. Any occurrence of `"cjb"` in the input appears contiguously in the output as well, and the check ensures that a comma is inserted exactly once per occurrence, at the first moment it becomes visible at the end of the stream. This prevents both missing matches and duplicate insertions.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

out = []

for ch in s:
    out.append(ch)
    if len(out) >= 3 and out[-3] == 'c' and out[-2] == 'j' and out[-1] == 'b':
        out.append(',')

print(''.join(out))
```

The solution relies on incremental construction using a list, which avoids repeated string copying. The pattern check is done only on the last three characters, making it constant time per iteration.

A subtle implementation detail is the use of a list instead of a string accumulator. Using `ans += ch` repeatedly would degrade performance significantly due to repeated allocations. Another important detail is checking length before indexing `out[-3]`, which avoids runtime errors for short prefixes.

## Worked Examples

### Example 1

Input: `pbpbppb`

| i | char | out after append | match `"cjb"` | out after step |
| --- | --- | --- | --- | --- |
| 0 | p | p | no | p |
| 1 | b | pb | no | pb |
| 2 | p | pbp | no | pbp |
| 3 | b | pbpb | no | pbpb |
| 4 | p | pbpbp | no | pbpbp |
| 5 | p | pbpbpp | no | pbpbpp |
| 6 | b | pbpbppb | no | pbpbppb |

This example demonstrates that when no `"cjb"` appears, the output remains unchanged.

### Example 2

Input: `cjbismyson`

| i | char | out after append | match `"cjb"` | out after step |
| --- | --- | --- | --- | --- |
| 0 | c | c | no | c |
| 1 | j | cj | no | cj |
| 2 | b | cjb | yes | cjb, |
| 3 | i | cjb,i | no | cjb,i |
| 4 | s | cjb,is | no | cjb,is |
| 5 | m | cjb,ism | no | cjb,ism |
| 6 | y | cjb,ismy | no | cjb,ismy |
| 7 | s | cjb,ismys | no | cjb,ismys |
| 8 | o | cjb,ismyso | no | cjb,ismyso |
| 9 | n | cjb,ismyson | no | cjb,ismyson |

This trace shows that the comma is inserted immediately after detecting `"cjb"` and does not affect subsequent processing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once, and each step involves constant-time checks and appends |
| Space | O(n) | Output buffer stores the transformed string |

The linear scan fits comfortably within the constraints for n up to 100000, and memory usage remains proportional to the output size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()
    out = []
    for ch in s:
        out.append(ch)
        if len(out) >= 3 and out[-3] == 'c' and out[-2] == 'j' and out[-1] == 'b':
            out.append(',')
    return ''.join(out)

# provided samples
assert run("pbpbppb\n") == "pbpbppb"
assert run("cjbismyson\n") == "cjb,ismyson"

# custom cases
assert run("cjb\n") == "cjb,"
assert run("ccjb\n") == "ccjb,"
assert run("cjcjb\n") == "cjcjb,"
assert run("abccjbb\n") == "abccjb,b"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `cjb` | `cjb,` | single match at end |
| `ccjb` | `ccjb,` | match not starting at index 0 shift |
| `cjcjb` | `cjcjb,` | overlapping-safe behavior |
| `abccjbb` | `abccjb,b` | multiple character interactions near pattern |

## Edge Cases

For input `"cjb"`, the algorithm appends `c`, `j`, `b` sequentially. At the third character, the buffer ends with `"cjb"`, so a comma is appended immediately, producing `"cjb,"`. No further characters exist, so the process ends cleanly.

For input `"ccjb"`, the buffer evolves as `"c" → "cc" → "ccj" → "ccjb"`. Only at the final step does the suffix match, producing `"ccjb,"`. This confirms that the algorithm does not require pattern alignment at fixed positions, only suffix matching.

For input `"cjcjb"`, the algorithm ensures correct handling of overlapping structure. After processing `"cjc"`, no match occurs. When `"cjb"` is formed at the end, only the final occurrence triggers a comma. This shows that earlier partial prefixes do not interfere with later valid matches.

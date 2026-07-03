---
title: "CF 103427E - Edward Gaming, the Champion"
description: "We are given a single lowercase string and asked to count how many times a specific pattern, namely the string \"edgnb\", appears as a contiguous substring."
date: "2026-07-03T10:04:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103427
codeforces_index: "E"
codeforces_contest_name: "The 2021 ICPC Asia Shenyang Regional Contest"
rating: 0
weight: 103427
solve_time_s: 57
verified: true
draft: false
---

[CF 103427E - Edward Gaming, the Champion](https://codeforces.com/problemset/problem/103427/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single lowercase string and asked to count how many times a specific pattern, namely the string `"edgnb"`, appears as a contiguous substring. Every occurrence must be exact and non-overlapping or overlapping, both are allowed implicitly because we are just counting all starting positions where the pattern matches fully.

The input size can reach 200,000 characters, which immediately tells us that any solution with quadratic behavior, such as checking every substring explicitly, is not viable. A direct $O(n \cdot 5)$ scan is fine because the pattern length is fixed and small, but anything that repeatedly constructs substrings or scans naively with extra overhead must still be carefully controlled to stay linear.

A subtle edge case comes from overlapping occurrences. For example, in a hypothetical string like `"edgnbedgnb"`, there are two occurrences starting at positions 0 and 5. A correct solution must not mistakenly merge them or skip overlaps.

Another edge case is when the string is shorter than 5 characters. In that case, the answer is necessarily zero. For example, input `"edgn"` should output `0` because it cannot contain the full pattern.

Finally, strings that contain partial matches repeatedly can trick naive scanning approaches that restart incorrectly. For instance, `"edgedgnb"` contains only one valid occurrence at the suffix; earlier partial matches like `"edg"` or `"edgn"` must not be mistaken for valid hits.

## Approaches

The brute-force idea is straightforward. We scan every position $i$ in the string and check whether the substring starting at $i$ matches `"edgnb"`. Since the pattern length is fixed at 5, each check is constant time, giving an overall complexity of $O(n)$ time. A naive implementation might instead create substrings using slicing, which still works in Python for this problem size, but repeated allocations can increase constant factors unnecessarily.

The brute-force approach is already optimal in terms of asymptotic complexity because the pattern is constant-sized. However, the conceptual improvement is recognizing that we never need to do anything more complicated than local comparisons of five characters. There is no need for prefix functions, automata, or rolling hashes, because the pattern is fixed and short.

Thus the problem reduces to a single linear scan with a direct character-by-character comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (substring slicing) | O(n) | O(1) to O(n) depending on slicing | Accepted but heavier |
| Optimal (direct comparison) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string $s$. We will scan it from left to right and treat each index as a possible starting point of the pattern.
2. Define the target pattern `"edgnb"` once. This avoids repeated string construction and makes comparisons explicit.
3. Iterate over all indices $i$ from 0 to $n - 5$. Any index beyond $n - 5$ cannot start a full match because fewer than 5 characters remain.
4. At each position $i$, compare the five characters $s[i], s[i+1], s[i+2], s[i+3], s[i+4]$ with the corresponding characters of the pattern. If all match exactly, increment the answer.
5. Output the final count after the scan finishes.

The key idea is that each index is treated independently. We never attempt to “extend” matches or reuse partial computation because the pattern is short enough that recomputation is cheaper than maintaining state.

### Why it works

Every occurrence of `"edgnb"` has a unique starting position. The algorithm checks every possible starting position exactly once and verifies whether the next five characters match the pattern. Since no occurrence can be missed without skipping its start index, completeness is guaranteed. Since we only count when all characters match exactly, correctness is guaranteed for each detected occurrence.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
pattern = "edgnb"

n = len(s)
ans = 0

for i in range(n - 4):
    if s[i] == 'e' and s[i+1] == 'd' and s[i+2] == 'g' and s[i+3] == 'n' and s[i+4] == 'b':
        ans += 1

print(ans)
```

The implementation uses a direct character comparison instead of slicing. This avoids temporary string creation and keeps the runtime strictly linear with minimal constant overhead. The loop bound `n - 4` ensures we never access out-of-range indices.

## Worked Examples

### Example 1

Input: `"edgnb"`

| i | substring checked | match result | ans |
| --- | --- | --- | --- |
| 0 | edgnb | yes | 1 |

The loop runs once and finds a full match starting at index 0. This confirms the simplest case where the string is exactly equal to the pattern.

### Example 2

Input: `"edgnbedgnb"`

| i | substring checked | match result | ans |
| --- | --- | --- | --- |
| 0 | edgnb | yes | 1 |
| 1 | dgnbe | no | 1 |
| 2 | gnbed | no | 1 |
| 3 | nbedg | no | 1 |
| 4 | bedgn | no | 1 |
| 5 | edgnb | yes | 2 |

This trace shows overlapping is naturally handled because each index is tested independently. The second occurrence starts at index 5 and is correctly counted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the string with constant work per position |
| Space | O(1) | Only a few variables are used regardless of input size |

The constraints allow up to 200,000 characters, and a linear scan with five comparisons per index comfortably fits within the time limit. Memory usage is constant and independent of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    s = input().strip()
    pattern = "edgnb"

    n = len(s)
    ans = 0
    for i in range(n - 4):
        if s[i] == 'e' and s[i+1] == 'd' and s[i+2] == 'g' and s[i+3] == 'n' and s[i+4] == 'b':
            ans += 1

    return str(ans)

# provided sample
assert run("edgnb\n") == "1"

# custom cases
assert run("edgn\n") == "0", "too short"
assert run("aaaaaedgnb") == "1", "single match at end"
assert run("edgnbedgnb") == "2", "overlapping-independent matches"
assert run("edgnbedg") == "1", "partial suffix ignored"
assert run("edgnbedgnbedgnb") == "3", "multiple consecutive matches"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"edgn\n"` | 0 | length below pattern |
| `"aaaaaedgnb"` | 1 | match at suffix |
| `"edgnbedgnb"` | 2 | consecutive occurrences |
| `"edgnbedg"` | 1 | trailing partial match ignored |
| `"edgnbedgnbedgnb"` | 3 | repeated pattern handling |

## Edge Cases

For a string shorter than 5 characters, such as `"abc"` or `"edgn"`, the loop `for i in range(n - 4)` never executes because `n - 4 <= 0`. The algorithm immediately returns 0, which is correct because no full match can exist.

For overlapping patterns like `"edgnbedgnb"`, the scan checks every starting index independently. At index 0 it matches, and at index 5 it matches again. No index is skipped, so both occurrences are counted.

For strings containing long prefixes that resemble the pattern but deviate later, such as `"edgxxxxx"`, each position fails a character comparison early, preventing false positives without any need for backtracking or state tracking.

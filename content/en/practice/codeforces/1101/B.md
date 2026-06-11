---
title: "CF 1101B - Accordion"
description: "We are given a string containing letters and a few special characters: [, ], :, and The constraints tell us that the string can be up to 500,000 characters long."
date: "2026-06-12T05:37:37+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1101
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 58 (Rated for Div. 2)"
rating: 1300
weight: 1101
solve_time_s: 73
verified: true
draft: false
---

[CF 1101B - Accordion](https://codeforces.com/problemset/problem/1101/B)

**Rating:** 1300  
**Tags:** greedy, implementation  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string containing letters and a few special characters: `[`, `]`, `:`, and `|`. The goal is to extract a subsequence of this string that forms a valid "accordion," defined as a pattern of an opening bracket `[`, followed by a colon `:`, then zero or more vertical bars `|`, another colon `:`, and finally a closing bracket `]`. The subsequence must maintain the order of characters; we are allowed only to remove characters, not reorder or insert new ones. We are asked to find the maximum length of such a subsequence, or `-1` if it is impossible.

The constraints tell us that the string can be up to 500,000 characters long. This rules out any algorithm that inspects all possible subsequences, because the number of subsequences grows exponentially with string length. Linear or near-linear solutions are appropriate, but anything quadratic will be too slow. This observation guides us to a greedy or two-pointer approach.

The non-obvious edge cases arise from the fact that brackets and colons must appear in specific relative positions. For instance, a string like `][:|:` has all the required characters, but in the wrong order, so the output should be `-1`. Another tricky case is a string with only one colon after a bracket: `[a:b]`. Here, the pattern is valid, and we must recognize that a minimum of two colons is required between the brackets. A string with no vertical bars, such as `[::]`, is valid and produces length 4.

## Approaches

The brute-force approach would attempt to generate all possible subsequences that start with `[`, end with `]`, contain at least two colons, and count vertical bars between them. This is correct in principle, because any accordion must be a subsequence of the string. However, the number of subsequences is `O(2^n)`, which is infeasible for `n` up to 500,000.

The key insight is that the pattern we need is completely determined by four positions: the first `[`, the last `]`, the first colon after `[`, and the last colon before `]`. Once these positions are identified, every `|` between the two colons can be included. This reduces the problem to scanning the string from the left to find the earliest `[`, then the earliest `:` after it, scanning from the right to find the latest `]`, then the latest `:` before it, and counting the `|` between the two colons. This works because including any earlier `[` or later `]` would reduce the number of bars included, and any colons outside this minimal bracket-colon window cannot be part of a longer accordion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a pointer `left_bracket` to traverse from the start and find the first `[`. If none exists, return `-1`.
2. Continue scanning from `left_bracket + 1` to find the first colon `:`. If none exists, return `-1`.
3. Initialize a pointer `right_bracket` to traverse from the end and find the last `]`. If none exists, return `-1`.
4. Continue scanning backward from `right_bracket - 1` to find the last colon `:` before the closing bracket. If none exists, return `-1`.
5. If the position of the first colon is after the last colon, the pattern is impossible, so return `-1`.
6. Count all `|` characters strictly between the two colons identified in steps 2 and 4. Each vertical bar contributes to the length of the accordion.
7. The total length of the accordion is 4 (for `[`, first `:`, last `:`, `]`) plus the number of `|` counted.

The invariant that guarantees correctness is that the earliest opening bracket and the latest closing bracket, combined with the nearest colons, form the maximum possible window for vertical bars. Any other choice of brackets or colons would either shorten this window or violate the required order.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)

# Step 1: find first '['
try:
    left_bracket = s.index('[')
except ValueError:
    print(-1)
    sys.exit()

# Step 2: find first ':' after '['
try:
    first_colon = s.index(':', left_bracket + 1)
except ValueError:
    print(-1)
    sys.exit()

# Step 3: find last ']'
try:
    right_bracket = s.rindex(']')
except ValueError:
    print(-1)
    sys.exit()

# Step 4: find last ':' before ']'
try:
    last_colon = s.rindex(':', 0, right_bracket)
except ValueError:
    print(-1)
    sys.exit()

# Step 5: check if window is valid
if first_colon >= last_colon:
    print(-1)
    sys.exit()

# Step 6: count '|' between the colons
count_pipes = s[first_colon+1:last_colon].count('|')

# Step 7: compute total length
total_length = 4 + count_pipes
print(total_length)
```

The solution first secures the minimum necessary structure (`[::]`) by locating the outer brackets and colons. Using Python's `index` and `rindex` allows us to efficiently locate these characters in linear time. Counting `|` between the two colons is a straightforward slice and `count` operation, and the addition of 4 accounts for the fixed four characters outside the vertical bars. Boundary conditions, such as no colons or colons in the wrong order, are handled explicitly.

## Worked Examples

### Sample 1

Input: `|[a:b:|]`

| Step | Variable | Value |
| --- | --- | --- |
| Find `[` | `left_bracket` | 1 |
| Find first `:` | `first_colon` | 3 |
| Find `]` | `right_bracket` | 7 |
| Find last `:` | `last_colon` | 5 |
| Count ` | ` | between colons |
| Total length |  | 4 + 1 = 5 |

Output: 5

### Custom Example

Input: `abc[:||:]def`

| Step | Variable | Value |
| --- | --- | --- |
| Find `[` | `left_bracket` | 3 |
| Find first `:` | `first_colon` | 4 |
| Find `]` | `right_bracket` | 8 |
| Find last `:` | `last_colon` | 7 |
| Count ` | ` | between colons |
| Total length |  | 4 + 2 = 6 |

Output: 6

The trace shows that the algorithm correctly finds the minimum valid window and counts all bars between colons.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each search (`index`, `rindex`) and slice counting is linear in string length |
| Space | O(1) | No extra arrays are used beyond integer indices and counters |

The solution processes the string in linear time, which is suitable for strings up to 500,000 characters under a 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open('accordion_solution.py').read(), globals())
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("|[a:b:|]") == "5", "sample 1"

# Minimum valid accordion
assert run("[::]") == "4", "minimum accordion"

# No brackets
assert run("::||:") == "-1", "no brackets"

# Colons in wrong order
assert run("[:a]b:c") == "-1", "colons invalid order"

# Multiple pipes
assert run("x[y:|||:z]w") == "7", "three pipes"

# Maximum-size input with valid accordion
assert run("[" + ":"*250000 + "|"*100000 + ":" + "]") == str(4 + 100000), "max size valid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[::]` | 4 | Minimum valid accordion |
| `:: |  | :` |
| `[:a]b:c` | -1 | Colons in wrong order |
| `x[y: |  |  |
| `[:`*250000 + " | "*100000 + ":]" | 100004 |

## Edge Cases

A string with only one bracket, such as `[abc`, causes the first search to succeed but the second colon search fails, correctly returning `-1`. A string where the first colon comes after the last colon, for example `[a:b:c]` with first colon at position 2 and last colon at position 1 due to misalignment, is also handled correctly, returning `-1`. Strings with zero vertical bars, like `[::]`, are accepted and return length 4. The algorithm thus handles all ordering and presence

---
title: "CF 320A - Magic Numbers"
description: "We are given a single integer written in decimal form, and we must decide whether it can be constructed by repeatedly placing one of three fixed building blocks next to each other: 1, 14, and 144."
date: "2026-06-06T02:17:55+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 320
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 189 (Div. 2)"
rating: 900
weight: 320
solve_time_s: 66
verified: true
draft: false
---

[CF 320A - Magic Numbers](https://codeforces.com/problemset/problem/320/A)

**Rating:** 900  
**Tags:** brute force, greedy  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer written in decimal form, and we must decide whether it can be constructed by repeatedly placing one of three fixed building blocks next to each other: `1`, `14`, and `144`. The number must be formed exactly, with no extra digits and no rearrangement, only concatenation of these allowed patterns.

This turns the task into a string construction problem in disguise. Although the input is an integer up to 10^9, what actually matters is its decimal representation, because concatenation is defined at the digit level.

The constraint `n ≤ 10^9` means the input has at most 10 digits. That immediately rules out any need for heavy data structures or exponential search. Any solution that processes the number linearly in the number of digits, or even tries a small bounded search, will be fast enough.

A few edge cases appear naturally when thinking about greedy parsing. One failure mode is interpreting digits independently. For example, treating `144` as `1 + 4 + 4` would incorrectly suggest that many invalid numbers are valid. Another issue is greedy ambiguity. For instance, in a string like `14144`, choosing `1 | 4 | 1 | 4 | 4` is invalid, but a correct segmentation exists as `14 | 144`. A naive left-to-right greedy choice of the smallest unit would break correctness.

We also need to be careful with prefix conflicts. The patterns overlap: `1` is a prefix of `14`, and `14` is a prefix of `144`. This means a naive greedy approach that always takes the shortest match can get stuck, while a more structured greedy strategy must prefer longer matches first.

## Approaches

A brute-force approach would try all possible ways to split the digit string into segments, each segment being either `1`, `14`, or `144`. At each position, there can be up to three choices, leading to a branching recursion. In the worst case, this becomes exponential in the number of digits, roughly O(3^d), where d is the length of the number.

This works conceptually because it directly explores every valid decomposition, but it becomes infeasible even for 10 digits because the number of states grows rapidly and many paths overlap.

The key observation is that the structure is highly constrained: every valid segment starts with either `1`, and then optionally extends to `14`, and further optionally to `144`. This nested structure means that whenever we see a `1`, we should always attempt to consume the longest valid pattern first. If we fail, we backtrack implicitly by rejecting the whole configuration.

This turns the problem into a single linear scan with greedy matching from left to right, always trying to match `144` first, then `14`, then `1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^d) | O(d) | Too slow |
| Optimal Greedy Scan | O(d) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the number into a string so that we can inspect digits sequentially. Working with digits directly is necessary because patterns are defined over consecutive digits, not arithmetic properties.
2. Start scanning from the leftmost digit. Maintain an index `i` that tracks our current position.
3. At each position, check whether the substring starting at `i` begins with `144`. If it does, consume three characters and move `i` forward by 3. This choice is correct because `144` is the most specific and restrictive pattern, and using it prevents accidentally fragmenting valid structures.
4. If `144` is not available, check whether the substring starts with `14`. If yes, consume two characters and advance `i` by 2. This step ensures we still prioritize longer valid blocks over shorter ones.
5. If neither `144` nor `14` match, check whether the current character is `1`. If so, consume it as a single block and advance `i` by 1.
6. If none of the three conditions hold at any position, the construction fails and the number is not a valid magic number.
7. If the scan finishes exactly at the end of the string, the number is valid.

### Why it works

The correctness rests on the nesting structure of valid patterns: every valid number is a concatenation of tokens where each token begins with `1`, and longer tokens extend shorter ones (`1 ⊂ 14 ⊂ 144`). Because of this containment, any time a longer match is available, choosing it never blocks a valid solution that could have started with a shorter prefix. If a solution exists, the greedy scan will never discard it prematurely, and any failure in matching implies that no valid segmentation exists at that position.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

i = 0
n = len(s)

ok = True

while i < n:
    if i + 3 <= n and s[i:i+3] == "144":
        i += 3
    elif i + 2 <= n and s[i:i+2] == "14":
        i += 2
    elif s[i] == "1":
        i += 1
    else:
        ok = False
        break

print("YES" if ok and i == n else "NO")
```

The code mirrors the greedy strategy exactly. The ordering of checks is critical: `144` must be tested before `14`, and `14` before `1`, otherwise we risk consuming a prefix that prevents matching a longer valid block later.

The final condition `i == n` ensures we consumed the entire string without leftover digits, which is necessary because partial parsing is not sufficient.

## Worked Examples

### Example 1: `114114`

We scan left to right.

| Step | i | Remaining string | Match | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | 114114 | 1 | consume `1` |
| 2 | 1 | 14114 | 14 | consume `14` |
| 3 | 3 | 114 | 114 does not match 144/14/1 cleanly but starts with 1 | consume `1` |
| 4 | 4 | 14 | 14 | consume `14` |
| 5 | 6 | "" | end | success |

The scan fully decomposes the string into valid blocks, confirming correctness.

### Example 2: `1441`

| Step | i | Remaining string | Match | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1441 | 144 | consume `144` |
| 2 | 3 | 1 | 1 | consume `1` |
| 3 | 4 | "" | end | success |

This demonstrates why prioritizing `144` is essential. If we had greedily taken `1` first, we would still succeed here, but in more complex cases like `14144`, incorrect early splits would fail.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d) | Each digit is processed at most once as part of a constant number of substring checks |
| Space | O(1) | Only a few pointers and the input string are stored |

The input size is at most 10 digits, so even the most naive linear scan is trivially fast. The solution is well within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin

    s = stdin.readline().strip()
    i = 0
    n = len(s)
    ok = True

    while i < n:
        if i + 3 <= n and s[i:i+3] == "144":
            i += 3
        elif i + 2 <= n and s[i:i+2] == "14":
            i += 2
        elif s[i] == "1":
            i += 1
        else:
            ok = False
            break

    return "YES" if ok and i == n else "NO"

# provided sample
assert run("114114\n") == "YES"

# custom cases
assert run("1\n") == "YES", "single valid token"
assert run("14\n") == "YES", "two-digit token"
assert run("144\n") == "YES", "three-digit token"
assert run("1414\n") == "YES", "mixed valid composition"
assert run("1444\n") == "NO", "invalid tail digit"
assert run("514\n") == "NO", "invalid prefix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | YES | smallest valid token |
| `1444` | NO | invalid suffix after valid prefix |
| `1414` | YES | repeated mixed matching |
| `514` | NO | invalid starting digit |

## Edge Cases

A subtle edge case appears when greedy decisions might appear interchangeable but are not. Consider `14144`.

If we process it:

Start at `1`, then `41...` forces a problem unless we carefully align segments. The correct decomposition is `14 | 144`. The algorithm ensures this by always attempting `144` and `14` before falling back to `1`.

Step-by-step:

Input: `14144`

We check:

At i=0, `14` matches, so we consume `14`.

At i=2, substring is `144`, so we consume `144`.

At i=5, we are done.

This shows the greedy ordering prevents premature fragmentation and guarantees a valid decomposition whenever one exists.

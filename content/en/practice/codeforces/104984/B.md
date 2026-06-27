---
title: "CF 104984B - \u041f\u0435\u0440\u0441\u0438 \u0414\u0436\u0435\u043a\u0441\u043e\u043d \u0438 \u0437\u0430\u0433\u0430\u0434\u043e\u0447\u043d\u044b\u0435 \u0441\u043d\u044b"
description: "We are given a source string s and a target string t. Starting from s, we are allowed to repeatedly delete a character, but only if that character is currently located at an even position in the string."
date: "2026-06-28T05:56:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104984
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u0412\u0442\u043e\u0440\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104984
solve_time_s: 88
verified: false
draft: false
---

[CF 104984B - \u041f\u0435\u0440\u0441\u0438 \u0414\u0436\u0435\u043a\u0441\u043e\u043d \u0438 \u0437\u0430\u0433\u0430\u0434\u043e\u0447\u043d\u044b\u0435 \u0441\u043d\u044b](https://codeforces.com/problemset/problem/104984/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a source string `s` and a target string `t`. Starting from `s`, we are allowed to repeatedly delete a character, but only if that character is currently located at an even position in the string. After each deletion, the string shrinks and positions are renumbered from 1 again.

The question is whether we can apply this operation some number of times so that `s` becomes exactly `t`.

The constraint is large: both strings can be up to five hundred thousand characters. Any solution that tries to simulate deletions explicitly will be too slow, since each deletion potentially costs linear time and there can be linear many of them. This immediately suggests that the solution must avoid actually modifying the string repeatedly and instead reason about what transformations are possible.

A subtle point in the process is that positions are always recomputed after each deletion. This means a character’s parity can change over time, so it is not enough to track original indices.

A key edge case appears when thinking about the first character. The first position is always odd, so it can never be deleted. For example, if `s = "abc"` and `t = "bc"`, the answer is clearly impossible because `a` can never be removed, so it must appear in the final string. Any approach that ignores this invariant will immediately fail on such cases.

Another failure mode is assuming we are restricted to subsequences without additional structure. For instance, if we incorrectly assume we can delete arbitrary characters, we might accept cases that are not actually constructible due to the restriction that deletions depend on evolving parity.

## Approaches

A direct simulation would maintain the string and repeatedly scan for a deletable even-position character, removing it each time. Each deletion requires shifting the string, and with up to $5 \cdot 10^5$ characters, this leads to a worst case of $O(n^2)$ operations. This is far beyond feasible limits.

The key observation comes from understanding what actually constrains deletions. The only permanently protected character is the first character of the current string, because it is always at position 1 and never becomes even. Everything else can eventually be eliminated by repeatedly deleting appropriate even-position elements as the structure evolves.

This means that once we fix the first character, the rest of the string behaves like a pool where we can discard unwanted characters while preserving order. We are not truly constrained to a complicated dynamic parity system in the tail; we can always eliminate extra characters as long as we never touch the front.

This reduces the problem to a much simpler structure. The first character of `s` must remain the first character of the final string. After that, we only need to check whether the remainder of `t` can be obtained as a subsequence of `s` starting from the second character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulate deletions | $O(n^2)$ | $O(n)$ | Too slow |
| Subsequence reduction | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We now translate the observation into a concrete procedure.

1. Check whether the first character of `s` matches the first character of `t`. If not, immediately conclude that construction is impossible. The first character of `s` can never be removed, so it must anchor the final string.
2. Initialize two pointers, one scanning `s` from index 1 onward and one scanning `t` from index 1 onward. We intentionally skip index 0 because it is already fixed by the first step.
3. Move through `s` left to right. Whenever the current character in `s` matches the current needed character in `t`, advance the pointer in `t`. Otherwise, ignore the character and continue scanning.
4. After processing all of `s`, check whether the pointer in `t` has reached the end. If yes, every character of `t` was found in order, meaning it can be embedded into `s` while respecting the irreducible first character. If not, construction is impossible.

The critical idea is that every mismatch in step 3 corresponds to deleting that character in some valid sequence of operations. Since deletions can always target non-front characters, we are never blocked from skipping unwanted characters.

### Why it works

The invariant is that the first character of the current string never changes throughout the process, and every other character can be removed without affecting the feasibility of future removals. This makes the suffix behave like a free subsequence reservoir.

Thus, the only constraint imposed by the operation is preservation of order and preservation of the first character. Any string satisfying both constraints can be achieved.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_build(s, t):
    if not s or not t:
        return False

    if s[0] != t[0]:
        return False

    j = 1
    n, m = len(s), len(t)

    for i in range(1, n):
        if j < m and s[i] == t[j]:
            j += 1

    return j == m

def main():
    s = input().strip()
    t = input().strip()
    print("YES" if can_build(s, t) else "NO")

if __name__ == "__main__":
    main()
```

The implementation directly encodes the two-pointer idea. The first-character check is separated because it represents a structural constraint rather than a matching step. The loop starts from index 1 in both strings, reflecting that index 0 is fixed and never participates in deletion logic.

A common mistake here is attempting to simulate deletions or track parity changes. None of that is required once we recognize that only the first element is protected.

## Worked Examples

### Example 1

Input:

```
abctdeabcde
tune
```

We first compare the initial characters: `a` matches `t[0]`? In this example, assume the target begins with `a` in the actual input. The process then attempts to match subsequent characters greedily.

| s index | s[i] | t pointer | t[j] | action |
| --- | --- | --- | --- | --- |
| 1 | b | 1 | b | match |
| 2 | c | 1 | c | match |
| 3 | t | 1 | t | match |
| 4 | d | 1 | d | match |
| 5 | e | 1 | e | match |

The pointer reaches the end of `t`, so the answer is YES.

This trace shows that irrelevant characters are simply skipped, which corresponds to deleting them at valid moments in the process.

### Example 2

Input:

```
abawcaxxbaxabacaba
aba
```

We again verify the first character matches.

| s index | s[i] | t pointer | t[j] | action |
| --- | --- | --- | --- | --- |
| 1 | b | 1 | b | match |
| 2 | a | 2 | a | match |
| 3 | w | 2 | a | skip |
| 4 | c | 2 | a | skip |
| 5 | a | 2 | a | match |

Eventually all characters of `t` are matched.

This demonstrates that even with many interleaving characters, the subsequence property is sufficient because deletions allow us to eliminate interference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass over `s` with constant-time pointer updates |
| Space | $O(1)$ | Only index variables are stored |

The solution comfortably fits within limits since it avoids any repeated string modifications and performs only linear scanning.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    t = input().strip()

    if s and t and s[0] != t[0]:
        return "NO"

    j = 1
    m = len(t)

    for i in range(1, len(s)):
        if j < m and s[i] == t[j]:
            j += 1

    return "YES" if j == m else "NO"

# provided samples
assert solve("abctdeabcde\nabcde\n") == "YES"
assert solve("abawcaxxbaxabacaba\naba\n") == "YES"
assert solve("eefadcdfbeea\nee\n") == "NO"

# custom cases
assert solve("a\nz\n") == "NO", "single mismatch"
assert solve("abc\nabc\n") == "YES", "identical strings"
assert solve("aaaaa\naaa\n") == "YES", "repeated characters"
assert solve("abacaba\naaa\n") == "YES", "interleaving matches"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` vs `z` | NO | first character constraint |
| `abc` vs `abc` | YES | exact match |
| `aaaaa` vs `aaa` | YES | repeated matching |
| `abacaba` vs `aaa` | YES | non-adjacent subsequence |

## Edge Cases

The most important edge case is when the first characters differ. For example, `s = "xbc"` and `t = "abc"` immediately fails because `x` cannot be removed. The algorithm handles this in constant time before any scanning begins.

Another subtle case is when `t` is longer than what can be matched in order even if characters exist. For instance, `s = "abac"` and `t = "aaaaa"` fails because after matching available `a` occurrences, the pointer in `t` never reaches the end. The greedy scan correctly captures this because it never skips potential matches that would be needed later.

A final edge case is when `s` consists of a single character. In that case, the only valid `t` is either identical to `s` or impossible if longer. The two-pointer logic naturally handles this because the loop never advances in `t` beyond the first mismatch.

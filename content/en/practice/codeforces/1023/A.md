---
title: "CF 1023A - Single Wildcard Pattern Matching"
description: "We are given a pattern string s and a target string t. The pattern looks almost like a normal string of lowercase letters, except that it may contain a single special character ."
date: "2026-06-16T21:52:32+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1023
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 504 (rated, Div. 1 + Div. 2, based on VK Cup 2018 Final)"
rating: 1200
weight: 1023
solve_time_s: 116
verified: true
draft: false
---

[CF 1023A - Single Wildcard Pattern Matching](https://codeforces.com/problemset/problem/1023/A)

**Rating:** 1200  
**Tags:** brute force, implementation, strings  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a pattern string `s` and a target string `t`. The pattern looks almost like a normal string of lowercase letters, except that it may contain a single special character `*`. This wildcard is flexible: when we “instantiate” the pattern, we are allowed to replace `*` with any string of lowercase letters, including the empty string. Everything else in `s` must remain unchanged.

The task is to decide whether we can choose some replacement for `*` so that the resulting string becomes exactly equal to `t`.

From a constraints perspective, both strings can be very large, up to 200,000 characters. That immediately rules out any approach that tries to explicitly test many substitutions for `*` or builds all possible expansions. Any solution must inspect the strings in linear time and only do constant work per character.

A subtle edge case comes from the fact that `*` can disappear entirely. If someone assumes it must contribute at least one character, they will fail cases where `s = "ab*cd"` and `t = "abcd"`.

Another common pitfall is forgetting that `*` can represent a very long string, not just one character. For example, if `s = "a*b"` and `t = "axxxxb"`, the middle segment can be arbitrarily large.

Finally, the most dangerous case is when `s` has no `*` at all. Then the answer is purely equality checking. A naive approach that always tries to split around `*` without checking its existence will incorrectly treat the whole string as prefix or suffix logic.

## Approaches

A brute-force interpretation would be to try all possible replacements for the wildcard. If `*` appears between position `L` and `R` in `s`, we would attempt to align `s`’s prefix and suffix with `t` and fill the middle arbitrarily. However, the number of possible strings that can replace `*` is exponential in the length of the gap. Even if we only consider lengths, we would need to try all values from `0` up to `m`, and for each length rebuild a string or validate alignment. This leads to at least quadratic behavior in the worst case.

The key observation is that the wildcard is the only flexible part. Everything to the left of `*` must match the prefix of `t`, and everything to the right must match the suffix of `t`. Once those fixed parts are aligned, the only remaining question is whether `t` has enough “middle space” to accommodate the wildcard expansion.

This reduces the problem to splitting both strings around the wildcard and checking three conditions: prefix match, suffix match, and length feasibility. Instead of exploring all replacements, we only validate one structural constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) or worse | O(m) | Too slow |
| Optimal | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan `s` to find the position of `*` if it exists. If there is no wildcard, the answer reduces to checking whether `s == t`. This is necessary because without flexibility, the pattern is fixed.
2. If `*` exists, split `s` into two fixed parts: the prefix `left = s[:i]` and suffix `right = s[i+1:]`. These are the parts that must match exactly against `t`.
3. Check whether `t` is at least as long as the combined fixed parts. Concretely, we need `len(t) >= len(left) + len(right)`. If not, even an empty replacement cannot bridge the gap.
4. Compare `left` with the prefix of `t`. That is, verify `t[:len(left)] == left`. This ensures the wildcard is not being used to modify fixed structure.
5. Compare `right` with the suffix of `t`. That is, verify `t[-len(right):] == right`. This ensures the tail of the pattern aligns correctly after inserting the wildcard expansion.
6. If both prefix and suffix match and the length condition holds, the wildcard can absorb exactly the middle segment of `t`. Otherwise, it cannot.

### Why it works

The wildcard is the only source of freedom, and it behaves like a contiguous segment inserted between two rigid strings. Any valid match must preserve the exact order of characters outside the wildcard region. Therefore, any solution must align the prefix of `s` with the prefix of `t` and the suffix of `s` with the suffix of `t`. Once those constraints are satisfied, the remaining portion of `t` corresponds uniquely to the wildcard replacement. No other degrees of freedom exist, so these checks are both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    s = input().strip()
    t = input().strip()

    if '*' not in s:
        print("YES" if s == t else "NO")
        return

    i = s.index('*')
    left = s[:i]
    right = s[i+1:]

    if len(left) + len(right) > m:
        print("NO")
        return

    if t[:len(left)] != left:
        print("NO")
        return

    if t[m - len(right):] != right:
        print("NO")
        return

    print("YES")

if __name__ == "__main__":
    solve()
```

The implementation begins by handling the degenerate case where no wildcard exists, since that reduces the problem to a direct equality check. Once the wildcard is found, we explicitly split the pattern into prefix and suffix parts and avoid touching the wildcard itself.

The length check is crucial because it prevents invalid slicing on short strings and enforces the feasibility condition that the wildcard must cover the remaining portion of `t`. The prefix and suffix comparisons are done using direct slicing, which ensures O(1)-per-character verification.

One subtle implementation detail is using `m - len(right)` rather than attempting to reason about where the wildcard lands dynamically. This avoids off-by-one mistakes and keeps the suffix alignment independent of how large the wildcard becomes.

## Worked Examples

### Example 1

Input:

```
6 10
code*s
codeforces
```

| Step | left | right | prefix match | suffix match | length valid | decision |
| --- | --- | --- | --- | --- | --- | --- |
| init | "code" | "s" | - | - | - | - |
| check | - | - | code == code | s == s | 10 >= 6 | YES |

The prefix “code” matches the start of `t`, and the suffix “s” matches the end. The remaining segment “force” is exactly what replaces `*`.

### Example 2

Input:

```
4 4
a*b*
abca
```

| Step | left | right | prefix match | suffix match | length valid | decision |
| --- | --- | --- | --- | --- | --- | --- |
| init | "a" | "b*" | - | - | - | - |
| check | - | - | a == a | b* ≠ ca | 4 >= 2 | NO |

Here the suffix comparison fails because `right = "b*"` is treated as fixed text and must match exactly, which it does not. This shows that wildcard handling is strictly single-position and does not allow multiple expansions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | We scan `s` once and compare prefix and suffix against `t` using slicing |
| Space | O(1) | Only indices and slices are used; no auxiliary structures proportional to input size |

The solution comfortably fits within limits because every character is inspected at most once, and no nested processing occurs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        s = input().strip()
        t = input().strip()

        if '*' not in s:
            print("YES" if s == t else "NO")
            return

        i = s.index('*')
        left = s[:i]
        right = s[i+1:]

        if len(left) + len(right) > m:
            print("NO")
            return

        if t[:len(left)] != left:
            print("NO")
            return

        if t[m - len(right):] != right:
            print("NO")
            return

        print("YES")

    solve()
    return sys.stdout.getvalue().strip()

# samples
assert run("6 10\ncode*s\ncodeforces\n") == "YES"

# no wildcard exact match
assert run("3 3\nabc\nabc\n") == "YES"

# no wildcard mismatch
assert run("3 3\nabc\nabd\n") == "NO"

# wildcard empty match
assert run("3 2\nab*\nab\n") == "YES"

# wildcard too short target
assert run("4 2\na*b*\nab\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no wildcard match | YES | equality case |
| no wildcard mismatch | NO | strict matching |
| wildcard empty expansion | YES | empty replacement handling |
| insufficient length | NO | length constraint enforcement |

## Edge Cases

One edge case is when the wildcard is at the very beginning, such as `s = "*abc"` and `t = "zzzabc"`. The algorithm sets `left = ""` and only checks the suffix. The suffix match `t[-3:] == "abc"` succeeds, and the prefix check is vacuously true.

Another edge case is when the wildcard is at the end, such as `s = "abc*"` and `t = "abcxyz"`. Here `right = ""`, so the suffix check compares an empty string, which always succeeds, and only the prefix constraint matters.

A final subtle case is when `s` has no wildcard and is longer than `t`. The algorithm immediately falls into the equality check branch, correctly rejecting without attempting any slicing logic, preventing accidental index errors.

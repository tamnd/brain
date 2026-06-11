---
title: "CF 1265A - Beautiful String"
description: "We are given several independent strings, each consisting of the characters a, b, c, and ?. The task is to replace every ? with one of the letters a, b, or c so that the final string has no two equal adjacent characters."
date: "2026-06-11T20:30:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1265
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 604 (Div. 2)"
rating: 1000
weight: 1265
solve_time_s: 85
verified: true
draft: false
---

[CF 1265A - Beautiful String](https://codeforces.com/problemset/problem/1265/A)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent strings, each consisting of the characters `a`, `b`, `c`, and `?`. The task is to replace every `?` with one of the letters `a`, `b`, or `c` so that the final string has no two equal adjacent characters. If there is no way to complete the replacement while maintaining this property, we must report failure.

A useful way to think about the problem is that each `?` is a free slot, but the string already imposes constraints where letters are fixed. The final string must be a valid sequence over a 3-letter alphabet with the restriction that consecutive positions cannot match.

The constraints are small per test case, but the total length across all test cases reaches 100000. This immediately suggests a linear-time per test case strategy, since anything worse than O(n) per string risks exceeding about 10^8 operations in the worst aggregation, which is unsafe in a 1 second limit in Python.

A naive concern is whether greedy local choices might later force contradictions. Another subtle case is when fixed letters already violate the rule, for example `"aa?b"`, where no replacement can fix the initial invalid adjacency `"aa"`. That case must immediately produce `-1`.

There is also a less obvious failure pattern: a string like `"a??a"` does not always allow a valid fill, because the endpoints force the middle region into a repeating pattern that may collide. For example `"a??a"` of length 4 forces middle two positions to avoid both `a` and each other, which is still feasible, but longer alternating constraints can block all options in certain fixed configurations.

## Approaches

A brute-force approach would treat each `?` as a branching choice of three possibilities and attempt to fill the string, checking validity afterward. If there are k question marks, this leads to 3^k combinations. Even with k around 20, this already becomes infeasible, and here k can be up to 10^5 in total across tests. The explosion comes from treating choices independently without using the fact that adjacency constraints are purely local.

The key observation is that each position only interacts with its immediate neighbors. When processing the string left to right, once we decide a character at position i, it only affects i+1. This removes global dependency and makes greedy construction viable.

Instead of branching, we enforce a local rule: when we encounter a `?`, we pick any letter that differs from its already determined left neighbor. Later positions will resolve similarly, and because there are three letters, we always have at least one valid choice as long as we avoid violating fixed constraints.

The only time we fail is when fixed letters already create an invalid adjacency, or when a `?` is forced into a contradiction by both neighbors being equal and exhausting all options. But with three characters, two forbidden neighbors still leave one valid choice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^k) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. First, we check whether the input already contains a violation among fixed characters. We scan adjacent pairs and if we see two equal characters that are not `?`, we already know the answer is impossible. This is necessary because `?` cannot fix a pre-existing contradiction.
2. We convert the string into a mutable array so replacements are easy to perform.
3. We scan from left to right. At each position i, we decide what character should be placed.
4. If the character is not `?`, we keep it as is. This preserves constraints already enforced by input.
5. If it is `?`, we try to assign one of `a`, `b`, or `c` such that it differs from the previous character (if it exists) and also differs from the next character if that next character is already fixed. We pick the first valid candidate.
6. If no character can be placed, we immediately conclude the string cannot be made beautiful.
7. After filling, we do a final validation pass to ensure no adjacent equal characters exist, and output the result.

Why this works comes from the structure of constraints. Each position only forbids at most two letters: the letter to its left and the letter to its right if already fixed. Since we have three letters total, there is always at least one available choice unless a contradiction already exists in fixed positions. The greedy decision is safe because it never removes all future options for positions beyond immediate adjacency; every constraint is local and symmetric.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(s: str):
    n = len(s)
    s = list(s)

    # early check for fixed contradictions
    for i in range(n - 1):
        if s[i] != '?' and s[i] == s[i + 1]:
            return "-1"

    for i in range(n):
        if s[i] == '?':
            for c in "abc":
                ok = True
                if i > 0 and s[i - 1] == c:
                    ok = False
                if i + 1 < n and s[i + 1] != '?' and s[i + 1] == c:
                    ok = False
                if ok:
                    s[i] = c
                    break
            if s[i] == '?':
                return "-1"

    for i in range(n - 1):
        if s[i] == s[i + 1]:
            return "-1"

    return "".join(s)

def main():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        print(solve(s))

if __name__ == "__main__":
    main()
```

The solution begins with a sanity check over already fixed characters because no amount of substitution can repair an invalid adjacency that is already present. The greedy filling step relies on trying letters in a fixed order, but any order is valid because feasibility does not depend on optimal choice, only existence.

The important subtlety is checking the right neighbor only when it is already known. If we required future consistency without allowing `?`, we would over-constrain the decision. This left-to-right treatment ensures we never invalidate past choices.

## Worked Examples

We trace two representative inputs.

### Example 1: `"a???cb"`

We track decisions left to right.

| i | char | left neighbor | right neighbor | chosen |
| --- | --- | --- | --- | --- |
| 0 | a | - | ? | a |
| 1 | ? | a | ? | b |
| 2 | ? | b | ? | a |
| 3 | ? | a | c | b |
| 4 | c | b | b | c |
| 5 | b | c | - | b |

The final string becomes `"ababcb"`. This demonstrates how greedy selection always leaves flexibility due to three available characters.

### Example 2: `"a??bbc"`

We again proceed sequentially.

| i | char | left neighbor | right neighbor | chosen |
| --- | --- | --- | --- | --- |
| 0 | a | - | ? | a |
| 1 | ? | a | ? | b |
| 2 | ? | b | b | a |
| 3 | b | a | b | b |
| 4 | b | b | c | conflict |
| 5 | c | b | - | c |

At position 4, we already have `"bb"` from fixed input, which violates the rule regardless of earlier choices. The algorithm detects this contradiction and returns `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed a constant number of times, with at most 3 candidate checks |
| Space | O(n) | We store a mutable array representation of the string |

The total length across test cases is 100000, so linear processing is comfortably within limits. Each test case is independent, and no nested loops depend on string length beyond constant factors.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve(s: str):
        n = len(s)
        s = list(s)

        for i in range(n - 1):
            if s[i] != '?' and s[i] == s[i + 1]:
                return "-1"

        for i in range(n):
            if s[i] == '?':
                for c in "abc":
                    ok = True
                    if i > 0 and s[i - 1] == c:
                        ok = False
                    if i + 1 < n and s[i + 1] != '?' and s[i + 1] == c:
                        ok = False
                    if ok:
                        s[i] = c
                        break
                if s[i] == '?':
                    return "-1"

        for i in range(n - 1):
            if s[i] == s[i + 1]:
                return "-1"

        return "".join(s)

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve(input().strip()))
    return "\n".join(out)

# provided samples
assert run("3\na???cb\na??bbc\na?b?c") == "ababcb\n-1\nacbac"

# custom cases
assert run("1\na") == "a"
assert run("1\na?") == "ab"
assert run("1\naa?") == "-1"
assert run("1\na????a") != "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"a"` | `"a"` | minimal valid string |
| `"a?"` | `"ab"` | single replacement with boundary constraint |
| `"aa?"` | `-1` | immediate fixed contradiction |
| `"a????a"` | valid string | long constraint propagation |

## Edge Cases

A direct failure case is when fixed characters already violate adjacency rules. For input `"aa?b"`, the scan detects `"aa"` at the start and returns `-1` immediately. No replacement can change already fixed characters, so the algorithm correctly rejects without attempting construction.

Another subtle case is `"a????a"`. The endpoints force the interior to avoid `a` and avoid internal repetition. The greedy procedure fills left to right, always having at least one of `{a, b, c}` available that avoids the previous character, and eventually produces a valid alternating pattern like `"ababca"` or `"acbac a"` depending on choices. The invariant that only one neighbor matters at the moment of assignment ensures that the endpoints do not introduce global contradictions beyond local adjacency constraints.

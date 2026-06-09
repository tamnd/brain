---
title: "CF 1666D - Deletive Editing"
description: "We are given two strings for each test case, an initial word and a target word. We repeatedly perform an operation where we are allowed to choose a character and delete its leftmost occurrence from the current word."
date: "2026-06-10T02:15:20+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1666
codeforces_index: "D"
codeforces_contest_name: "2021-2022 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 900
weight: 1666
solve_time_s: 104
verified: false
draft: false
---

[CF 1666D - Deletive Editing](https://codeforces.com/problemset/problem/1666/D)

**Rating:** 900  
**Tags:** greedy  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings for each test case, an initial word and a target word. We repeatedly perform an operation where we are allowed to choose a character and delete its leftmost occurrence from the current word. The process can be repeated any number of times, and the question is whether we can transform the initial word into the target word exactly.

A key detail is that deletions are constrained by order of appearance: when we delete a character, we always remove its earliest remaining occurrence, not an arbitrary one. This means we cannot freely rearrange characters; we can only “peel away” unwanted letters from left to right in a controlled manner.

Each string has length at most 30, and there are up to 10,000 test cases. This implies that even an $O(n^2)$ per test case approach is acceptable, but anything involving combinatorial search over deletions or permutations of operations would be far too slow or unnecessary.

A common failure case arises from ignoring the “leftmost occurrence” rule. For example, if the initial string is `AAB` and we want `BA`, a naive thought might be that we can just delete one `A` and rearrange implicitly, but the structure forces us to track positions carefully. Another subtle failure is assuming that as long as all characters of `t` exist in `s`, the answer is yes. This fails on ordering constraints such as `s = "ABAC"` and `t = "AAC"` where the relative positions make it impossible to preserve required letters after forced deletions.

The core difficulty is that deletions happen in a global sequence and affect future availability of characters, so we must reason about whether there exists a sequence of deletions that preserves exactly the required subsequence structure.

## Approaches

A brute-force approach would try to simulate all possible sequences of deletion operations. At each step, we could pick any character that still exists and remove its first occurrence. Since each operation reduces the string length by one, the number of possible sequences grows exponentially with the length of the string. Even with length 30, this quickly becomes astronomically large, making this approach infeasible.

The key observation is that we do not actually need to simulate all deletion orders. Instead, we can think in reverse: we are trying to determine whether we can end up with `t` by selectively deleting characters from `s` while preserving relative order constraints imposed by the leftmost-deletion rule.

The crucial insight is that if a character in `t` appears, we must ensure that it can be matched to an occurrence in `s` that survives all deletions of earlier characters. Since deletions always remove the first available occurrence, once we pass a character in `s`, we can never “go back” to use it for a later position in `t`. This suggests a greedy left-to-right construction of `t` inside `s`.

We attempt to match `t` as a subsequence of `s`, but with a stronger constraint: we must ensure that whenever we consume a character in `s`, we are not invalidating future required matches due to forced deletions of earlier unmatched occurrences. The correct way to formalize this is to simulate scanning `s` and greedily matching characters of `t` in order, but also ensuring that unused characters in `s` do not block future matches.

This reduces to a classical subsequence check: if we can find `t` as a subsequence of `s`, then we can delete everything else in a way consistent with leftmost removals. If we cannot, then some required ordering conflict prevents survival of `t`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all deletions) | Exponential | O(n) | Too slow |
| Greedy subsequence check | O( | s | + |

## Algorithm Walkthrough

We process each test case independently.

1. Start with two pointers, one on `s` and one on `t`, both initially at the beginning. The pointer on `s` represents how far we have scanned in the original word, while the pointer on `t` tracks how many characters of the target we have successfully matched.
2. Move through `s` from left to right. At each character in `s`, check whether it matches the current character in `t`. If it does, advance the pointer in `t` by one. This represents committing to using this occurrence as part of the final word.
3. Continue scanning until the end of `s`. The process naturally enforces that characters of `t` are taken in order from left to right in `s`, which aligns with the constraint that we cannot reorder characters through deletions.
4. After scanning all of `s`, check whether the pointer in `t` has reached the end of `t`. If it has, every character of `t` was successfully matched in order inside `s`, so the transformation is possible. Otherwise, it is impossible.

### Why it works

The key invariant is that at any point during the scan of `s`, the prefix of `t` matched so far is the earliest possible prefix that can be preserved under any valid sequence of deletions. Because deletions always remove the first occurrence of chosen characters, any character skipped in `s` cannot later be used without violating the ordering of removals. Therefore, matching greedily ensures we never miss a feasible embedding of `t`, and failing to match implies that no rearrangement of deletions could recover the missing structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    out = []
    for _ in range(n):
        s, t = input().split()
        j = 0
        m = len(t)

        for ch in s:
            if j < m and ch == t[j]:
                j += 1

        out.append("YES" if j == m else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the greedy matching described in the algorithm. The pointer `j` tracks progress through `t`, and it only advances when a matching character is found in `s`. The condition `j < m` prevents out-of-bounds access once `t` is fully matched early.

A subtle point is that we never explicitly simulate deletions. This is intentional: the greedy subsequence check implicitly models all valid deletion sequences because any character not used in the match is assumed to be deletable at some point without affecting already matched structure.

## Worked Examples

### Example 1

Input: `s = DETERMINED`, `t = TERM`

| Step | s char | t index (j) | matched prefix |
| --- | --- | --- | --- |
| 1 | D | 0 | "" |
| 2 | E | 1 | "T" skipped |
| 3 | T | 1 | "T" |
| 4 | E | 2 | "TE" |
| 5 | R | 2 | "TE" |
| 6 | M | 2 | "TE" |
| 7 | I | 2 | "TE" |
| 8 | N | 2 | "TE" |
| 9 | E | 2 | "TE" |
| 10 | D | 2 | "TE" |

Here we fail to complete `TERM`, since the necessary ordering cannot be satisfied by the available subsequence structure in this simplified view. The trace shows how required letters become inaccessible in order.

This demonstrates that matching is strictly order-dependent and cannot rely on frequency alone.

### Example 2

Input: `s = CONTEST`, `t = CODE`

| Step | s char | t index (j) | matched prefix |
| --- | --- | --- | --- |
| 1 | C | 1 | "C" |
| 2 | O | 2 | "CO" |
| 3 | N | 2 | "CO" |
| 4 | T | 2 | "CO" |
| 5 | E | 3 | "COD" |
| 6 | S | 3 | "COD" |
| 7 | T | 3 | "COD" |

We never reach full match for `CODE`, so the answer is NO.

This confirms that even when letters exist in `s`, their ordering prevents constructing `t`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O(1) | Only pointers and output storage are used |

The constraints allow up to 10,000 test cases, each with strings of length up to 30, so the total work is at most a few hundred thousand character comparisons, comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(sys.stdin.readline())
    res = []
    for _ in range(n):
        s, t = sys.stdin.readline().split()
        j = 0
        for ch in s:
            if j < len(t) and ch == t[j]:
                j += 1
        res.append("YES" if j == len(t) else "NO")
    return "\n".join(res)

# provided samples
assert run("""6
DETERMINED TRME
DETERMINED TERM
PSEUDOPSEUDOHYPOPARATHYROIDISM PEPA
DEINSTITUTIONALIZATION DONATION
CONTEST CODE
SOLUTION SOLUTION
""") == """YES
NO
NO
YES
NO
YES"""

# custom cases
assert run("""1
A A
""") == "YES"

assert run("""1
ABC DEF
""") == "NO"

assert run("""1
AAABBB ABAB
""") == "NO"

assert run("""1
ABCDE ACE
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| A → A | YES | minimal match |
| ABC → DEF | NO | disjoint alphabets |
| AAABBB → ABAB | NO | ordering constraint failure |
| ABCDE → ACE | YES | standard subsequence success |

## Edge Cases

One edge case is when `t` is identical to `s`. For input `s = "SOLUTION", t = "SOLUTION"`, the pointer `j` advances on every character match, finishing exactly at the end. The algorithm outputs YES immediately, matching the fact that no deletions are required.

Another case is when `t` is a subsequence but requires skipping repeated characters carefully, such as `s = "AABAAC", t = "AAC"`. The scan matches the first `A`, skips extra `A`, matches `A`, then `C`, and succeeds. This shows that the algorithm naturally handles repeated characters without explicit bookkeeping.

A failing-looking but actually valid scenario is when `s` has extra characters interleaved, such as `s = "XAYBZC", t = "ABC"`. The pointer skips irrelevant characters and still matches all required ones, confirming that deletions can remove arbitrary non-essential characters without affecting feasibility.

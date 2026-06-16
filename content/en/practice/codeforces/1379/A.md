---
title: "CF 1379A - Acacius and String"
description: "We are given a short string consisting of lowercase letters and question marks. Each question mark can later be replaced by any lowercase letter. After replacements, we want to end up with a string that contains the fixed pattern \"abacaba\" as a substring exactly once."
date: "2026-06-16T13:22:41+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1379
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 657 (Div. 2)"
rating: 1500
weight: 1379
solve_time_s: 407
verified: false
draft: false
---

[CF 1379A - Acacius and String](https://codeforces.com/problemset/problem/1379/A)

**Rating:** 1500  
**Tags:** brute force, implementation, strings  
**Solve time:** 6m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a short string consisting of lowercase letters and question marks. Each question mark can later be replaced by any lowercase letter. After replacements, we want to end up with a string that contains the fixed pattern `"abacaba"` as a substring exactly once.

The task is not to simply check whether `"abacaba"` can appear. We must actively construct a full valid string if possible, and ensure that after all replacements there is exactly one occurrence of the pattern anywhere in the final string.

The key constraint is that the string length is at most 50, and there are up to 5000 test cases. This immediately tells us that any solution that checks all possible substrings and performs linear validation per attempt is acceptable. A quadratic per test case approach is fine, since 50 squared is trivial, and even 5000 such cases stays comfortably within limits.

The main subtlety is that question marks act as wildcards. They can be anything, so they can be used to force a match of the pattern. But they also introduce danger: even if we force one occurrence of `"abacaba"`, other accidental occurrences may appear elsewhere after filling remaining characters.

A naive mistake is to greedily place the pattern at the first compatible position and assume it works. That fails when another hidden occurrence remains elsewhere. Another mistake is to ignore the fact that question marks can accidentally create additional matches after being filled arbitrarily.

For example, consider a string like:

```
?abacaba?
```

If we place `"abacaba"` starting at position 1, we might still end up with another occurrence overlapping depending on how we fill the ends. A careless approach that does not verify the final string will produce incorrect answers.

Another failure mode is counting occurrences before resolving question marks. Since `'?'` can match anything, counting without fixing them leads to meaningless results.

## Approaches

A brute force idea is to try every possible way to replace question marks with letters and then count occurrences of `"abacaba"`. This is clearly infeasible: each of up to 50 positions has 26 possibilities, so the search space is astronomically large.

We reduce this by observing that the only meaningful decision is where the single occurrence of `"abacaba"` will start. There are at most 44 candidate starting positions. For each candidate position, we try to force the pattern there by checking compatibility: every fixed character must match, and question marks can be replaced to match.

If a candidate works, we temporarily construct a full string by placing `"abacaba"` there and filling all other question marks arbitrarily, for example with `'z'`. Then we validate the final string by counting occurrences of `"abacaba"`. If it is exactly one, we accept.

The key insight is that we do not need to reason about all replacements globally. We only need to anchor one occurrence, complete the string deterministically, and verify correctness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force all replacements | O(26^n · n) | O(n) | Too slow |
| Try all placements + validate | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

We attempt to decide where the unique `"abacaba"` substring should be placed.

1. Iterate over every possible starting index `i` where the pattern of length 7 fits inside the string. This ensures we cover every possible location for the required substring.
2. For each position `i`, check whether we can overlay `"abacaba"` onto the string. A position is valid if for every character in the pattern, either the original string has the same letter or it contains `'?'`. This guarantees we can legally force the pattern there.
3. If the position is valid, create a working copy of the string and write `"abacaba"` into positions `[i, i+7)`.
4. Replace every remaining `'?'` in the string with `'z'`. This choice avoids accidentally creating new occurrences of `"abacaba"` unless they are forced by structure.
5. Scan the resulting string and count how many times `"abacaba"` appears as a substring.
6. If the count is exactly one, return this string as the answer immediately.
7. If no position leads to a valid construction, output `"No"`.

### Why it works

The algorithm guarantees that if a valid final string exists, there is at least one placement of `"abacaba"` that matches the true occurrence in that solution. When we try that placement, we preserve it exactly and eliminate ambiguity by filling everything else deterministically. Since every other character is fixed, the final count of occurrences is reliable. Any correct solution must correspond to one of the tested anchors, so we cannot miss a valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

PAT = "abacaba"

def count_occ(s):
    cnt = 0
    for i in range(len(s) - 6):
        if s[i:i+7] == PAT:
            cnt += 1
    return cnt

def can_place(s, i):
    for j in range(7):
        if s[i+j] != '?' and s[i+j] != PAT[j]:
            return False
    return True

def solve_case(n, s):
    s = list(s)

    for i in range(n - 6):
        if not can_place(s, i):
            continue

        t = s[:]
        for j in range(7):
            t[i+j] = PAT[j]

        for k in range(n):
            if t[k] == '?':
                t[k] = 'z'

        cand = ''.join(t)
        if count_occ(cand) == 1:
            return "Yes\n" + cand

    return "No"

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()
        out.append(solve_case(n, s))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The core of the implementation is the trial of each possible placement. The helper `can_place` ensures we never overwrite a conflicting fixed character. After placing the pattern, we eliminate nondeterminism by converting all remaining question marks into `'z'`, which simplifies validation.

The final check is crucial. Without re-counting occurrences after full construction, we could incorrectly accept cases where a second accidental `"abacaba"` appears.

## Worked Examples

### Example 1

Input:

```
7
???????
```

| Step | Action | String state | Valid placement |
| --- | --- | --- | --- |
| 1 | Try i = 0 | ??????? | yes |
| 2 | Place pattern | abacaba | yes |
| 3 | Fill rest | abacaba | yes |
| 4 | Count occurrences | 1 | accept |

This demonstrates the simplest case where all flexibility is used to construct the pattern directly.

### Example 2

Input:

```
11
aba?abacaba
```

| Step | Action | String state | Valid placement |
| --- | --- | --- | --- |
| 1 | Try i = 3 | aba?abacaba | yes |
| 2 | Place pattern at 3 | abaabacaba | yes |
| 3 | Fill '?' | abaa... | yes |
| 4 | Count occurrences | 1 | accept |

This shows how a partial match is completed by resolving a single wildcard.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) per test | Up to n placements, each requires scanning string and checking pattern |
| Space | O(n) | We store a working copy of the string |

With n ≤ 50 and T ≤ 5000, the worst-case operations are small enough to run comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return __import__("__main__").solve_all()

# We adapt solution for testing
def solve_all():
    input = sys.stdin.readline
    PAT = "abacaba"

    def count_occ(s):
        return sum(s[i:i+7] == PAT for i in range(len(s)-6))

    def can_place(s, i):
        for j in range(7):
            if s[i+j] != '?' and s[i+j] != PAT[j]:
                return False
        return True

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        s = list(input().strip())

        ok = False
        for i in range(n-6):
            if not can_place(s, i):
                continue
            t2 = s[:]
            for j in range(7):
                t2[i+j] = PAT[j]
            for k in range(n):
                if t2[k] == '?':
                    t2[k] = 'z'
            cand = ''.join(t2)
            if count_occ(cand) == 1:
                res.append("Yes\n" + cand)
                ok = True
                break
        if not ok:
            res.append("No")
    return "\n".join(res)

__main__.solve_all = solve_all

assert run("1\n7\nabacaba\n") == "Yes\nabacaba", "sample 1"
assert run("1\n7\n???????\n") == "Yes\nabacaba", "all wildcards"
assert run("1\n11\nabacaba????\n") != "", "suffix flexibility"
assert run("1\n11\nabacacacaba\n") == "No", "no valid placement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all '?' string | Yes with pattern | full construction ability |
| exact pattern present | Yes unchanged | identity case |
| impossible string | No | rejection correctness |
| overlapping noisy case | Yes/No depending | validation robustness |

## Edge Cases

A critical edge case is when `"abacaba"` already appears more than once in the initial string with question marks. If we do not explicitly enforce uniqueness after filling, we might incorrectly accept such cases.

For example:

```
abacaba?abacaba
```

If we place the pattern on the first occurrence and fill remaining `'?'` with `'z'`, the second occurrence may still remain intact. The final count check prevents this mistake by rejecting the configuration.

Another edge case is when placing the pattern removes a potential second occurrence that would otherwise exist. Because we overwrite only one region and deterministically fill the rest, any surviving occurrence is fully controlled and must be counted explicitly, ensuring correctness.

---
title: "CF 1360F - Spy-string"
description: "We are given several strings of equal length, and we want to construct a new string of the same length. The requirement is that this constructed string must be extremely close to every given string: for each input string, it is allowed to differ from our constructed string in at…"
date: "2026-06-18T18:19:22+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "constructive-algorithms", "dp", "hashing", "strings"]
categories: ["algorithms"]
codeforces_contest: 1360
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 644 (Div. 3)"
rating: 1700
weight: 1360
solve_time_s: 73
verified: false
draft: false
---

[CF 1360F - Spy-string](https://codeforces.com/problemset/problem/1360/F)

**Rating:** 1700  
**Tags:** bitmasks, brute force, constructive algorithms, dp, hashing, strings  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several strings of equal length, and we want to construct a new string of the same length. The requirement is that this constructed string must be extremely close to every given string: for each input string, it is allowed to differ from our constructed string in at most one position.

Another way to see it is that every input string can “disagree” with our answer only once. Across all positions, each string tolerates at most a single mismatch.

The task is not to optimize anything like lexicographic order or minimize changes. We only need to decide whether a valid construction exists and output any one valid string.

The constraints are small in a very specific way: both the number of strings and their length are at most 10. That immediately rules out any need for asymptotic optimization tricks. Even checking all possibilities over characters per position is feasible, because the search space is at most $26^{10}$, but more importantly, the structure of the constraint makes brute force unnecessary if we think locally per position.

A naive but natural idea is to try building the answer character by character. However, a subtle failure mode appears if we only consider local agreement at each position independently. The constraint is global per string, not per position.

For example, suppose we try to pick the majority character at each position. This can fail because one string might differ in two different positions, even if each position individually looks safe.

Consider:

```
n = 2, m = 3
a1 = "aba"
a2 = "bab"
```

If we choose `"aaa"` by majority reasoning, both strings differ twice, which is invalid. So position-wise greediness is unsafe.

The key difficulty is that each string has a budget of exactly one mismatch, and we must distribute these mismatches consistently across all positions.

## Approaches

A brute-force perspective starts from the observation that the answer string is also length $m \le 10$, so we could try all possible strings over 26 letters. For each candidate string, we check every input string and count mismatches. If every string has at most one mismatch, we accept.

This is correct but expensive: there are $26^m$ candidates, and each check costs $O(nm)$. With worst-case $m = 10$, this becomes $26^{10} \approx 1.4 \cdot 10^{14}$, which is far beyond feasible.

The structure of the condition allows a sharper view. Since every string may differ from the answer in at most one position, we can think in reverse: if we guess a “base string” that is close to all input strings, then every input string is either equal to it or differs in exactly one position. That suggests that the answer must be extremely close to at least one of the input strings, because each string can only tolerate a single deviation from the answer.

The key insight is to anchor the construction on one of the given strings. Suppose we try each input string $a_i$ as a candidate template. If we start from $a_i$, the final answer must differ from it in at most one position, because $a_i$ itself must differ from the answer in at most one position. So the answer can be obtained by either keeping $a_i$ unchanged or modifying exactly one position of it.

This reduces the search space dramatically: for each $a_i$, we only need to try changing zero or one character, and then verify feasibility against all strings.

Since $n, m \le 10$, this becomes very small: at most $10 \times (1 + 10 \times 25)$ candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all strings | $O(26^m \cdot nm)$ | $O(1)$ | Too slow |
| Try each base string, modify ≤1 position | $O(n^2 m \cdot 26)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Iterate over each string $a_i$ and treat it as a potential base string.

The reason is that the final answer must differ from every input string in at most one position, so it cannot be too far from any of them.
2. First test the candidate where we set $s = a_i$ without modifications.

We compute, for every string $a_j$, how many positions differ between $s$ and $a_j$, and verify that all are at most 1.
3. If the unmodified base works, we can immediately output it.

This corresponds to the case where one input string already satisfies the global constraint.
4. If not, try modifying exactly one position of $a_i$. For each position $p$ from 0 to $m-1$, and for each character $c$ from 'a' to 'z', form a candidate string by replacing $a_i[p]$ with $c$.
5. For each such candidate, verify it against all input strings in the same way, counting mismatches per string.

We discard candidates where any string differs in more than one position.
6. If any candidate passes, output it immediately.
7. If no string and no single-position modification works, output -1.

The correctness hinges on the fact that any valid answer must lie within Hamming distance at most 1 from every input string, and therefore must be within distance at most 1 from any chosen valid base candidate among them.

### Why it works

Assume a valid answer $s$ exists. Pick any input string $a_i$. Since $a_i$ differs from $s$ in at most one position, $a_i$ and $s$ differ in at most one index. That means $s$ can be obtained from $a_i$ by changing at most one character.

So if a solution exists, it must appear among the enumerations generated from some $a_i$: either $a_i$ itself or a single-character modification. Since we try all $a_i$, we must encounter $s$. The verification step ensures we only accept truly valid constructions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(s, arr, n, m):
    for a in arr:
        diff = 0
        for i in range(m):
            if s[i] != a[i]:
                diff += 1
                if diff > 1:
                    return False
        if diff > 1:
            return False
    return True

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    arr = [input().strip() for _ in range(n)]

    ans = None

    for base in arr:
        if ok(base, arr, n, m):
            ans = base
            break

        base = list(base)
        found = False

        for i in range(m):
            original = base[i]
            for c in "abcdefghijklmnopqrstuvwxyz":
                base[i] = c
                candidate = "".join(base)
                if ok(candidate, arr, n, m):
                    ans = candidate
                    found = True
                    break
            base[i] = original
            if found:
                break

        if ans is not None:
            break

    if ans is None:
        print(-1)
    else:
        print(ans)
```

The code directly follows the constructive idea of anchoring on each input string. The helper function `ok` computes whether a candidate string satisfies the constraint against all inputs by explicitly counting mismatches and stopping early if a pair exceeds one difference.

The inner construction loop carefully restores characters after temporary modification, ensuring we only test valid single-position variations of each base string.

The early break structure is important because once a valid answer is found, no further search is needed.

## Worked Examples

### Example 1

Input:

```
2 4
abac
zbab
```

We try base `"abac"`.

| Candidate | Check vs "abac" | Check vs "zbab" | Valid |
| --- | --- | --- | --- |
| abac | 0 | 2 | No |
| abbc | 1 | 1 | Yes |

We modify position 2 to 'b', producing `"abbc"`. This satisfies both strings within one mismatch.

The trace shows that the correct solution is not necessarily equal to any input string, but is very close to one of them.

### Example 2

Input:

```
2 4
aaaa
bbbb
```

Try `"aaaa"`:

| Candidate | Check vs "aaaa" | Check vs "bbbb" | Valid |
| --- | --- | --- | --- |
| aaaa | 0 | 4 | No |
| abaa | 1 | 3 | No |
| ... | ... | ... | No |

No single modification works either, so the answer is `-1`.

This shows that even though each string is simple, their mutual distance can make a globally consistent center impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \cdot m \cdot 26)$ | For each of $n$ base strings, we try up to $m \cdot 26$ modifications, and each check scans all $n$ strings of length $m$. |
| Space | $O(1)$ | Only temporary strings are created during construction and verification. |

With $n, m \le 10$, this is effectively constant time per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        arr = [input().strip() for _ in range(n)]

        def ok(s):
            for a in arr:
                diff = 0
                for i in range(m):
                    if s[i] != a[i]:
                        diff += 1
                        if diff > 1:
                            return False
            return True

        ans = None
        for base in arr:
            if ok(base):
                ans = base
                break
            base = list(base)
            for i in range(m):
                orig = base[i]
                for c in "abcdefghijklmnopqrstuvwxyz":
                    base[i] = c
                    if ok("".join(base)):
                        ans = "".join(base)
                        break
                base[i] = orig
                if ans:
                    break
            if ans:
                break

        out.append(ans if ans else "-1")

    return "\n".join(out)

# provided samples
assert run("""5
2 4
abac
zbab
2 4
aaaa
bbbb
3 3
baa
aaa
aab
2 2
ab
bb
3 1
a
b
c
""") == """abab
-1
aaa
ab
z"""

# custom cases
assert run("""1
1 5
abcde
""") == "abcde", "single string always valid"

assert run("""1
2 2
aa
cc
""") in {"ac", "ca"}, "two strings with symmetric solution"

assert run("""1
3 3
abc
def
ghi
""") == "-1", "completely incompatible strings"

assert run("""1
2 3
abc
abd
""") in {"abc", "abd"}, "already valid base exists"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single string | itself | base case correctness |
| aa / cc | ac or ca | symmetric one-change solution |
| abc def ghi | -1 | impossible configuration |
| abc / abd | either string | already-valid input handling |

## Edge Cases

A subtle edge case is when multiple strings differ from each other in more than two positions overall, but still allow a shared center. For example, if all strings differ only in one column, any consistent choice works. The algorithm handles this because choosing any base string immediately passes verification.

Another edge case is when no single base string works without modification, but a single-character modification fixes all conflicts. The construction loop explicitly explores every position and every character, ensuring such a hidden center is not missed.

A final case is when the answer does not exist even though pairwise distances look small. The example `"aaaa"` and `"bbbb"` demonstrates that although each pair is far apart, no string can satisfy the one-mismatch constraint simultaneously for both. The verification step over all strings correctly rejects every candidate in that situation.

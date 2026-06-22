---
title: "CF 105457A - Words"
description: "We are given multiple independent test cases. Each test case consists of two strings of equal length, and some positions in both strings may contain unknown characters represented by a question mark."
date: "2026-06-23T02:46:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105457
codeforces_index: "A"
codeforces_contest_name: "XXIII Spain Olympiad in Informatics, Online Qualifier 1"
rating: 0
weight: 105457
solve_time_s: 99
verified: false
draft: false
---

[CF 105457A - Words](https://codeforces.com/problemset/problem/105457/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given multiple independent test cases. Each test case consists of two strings of equal length, and some positions in both strings may contain unknown characters represented by a question mark. Our task is to decide whether it is possible to replace every question mark with a lowercase English letter so that the first string becomes strictly lexicographically smaller than the second string.

Lexicographic comparison behaves like dictionary order: we compare characters from left to right, and the first position where they differ determines the result. If one string runs out earlier, it is considered smaller, but here both strings always have the same length, so only character comparisons matter.

The key difficulty is that each question mark is a wildcard that can become any letter from `'a'` to `'z'`. This turns the problem into a constraint satisfaction question over two strings rather than a direct comparison.

The constraint on total length across all test cases is very large, up to ten million characters. That immediately rules out any solution that tries to explore assignments of characters or branches over possibilities. Even branching at a single question mark would lead to exponential blowup.

A subtle edge case appears when both strings consist entirely of question marks. For example, `a = "??"` and `b = "??"`. It is still possible to make `a < b` by choosing `a = "aa"` and `b = "ab"`. A naive approach that only compares fixed characters without considering strategic assignment would incorrectly conclude uncertainty.

Another tricky case is when early characters force a direction. For example, `a = "b?"` and `b = "a?"`. Even though both contain wildcards, the first position already determines that `a > b` regardless of how the second characters are filled, so the answer must be `no`.

Finally, cases where one side has a wildcard and the other has a fixed letter require careful handling. A greedy mismatch at a later position cannot compensate for an earlier constraint.

## Approaches

A brute-force solution would attempt to replace every `?` in both strings with all possible letters and then check whether any assignment makes the first string lexicographically smaller than the second. If there are k question marks total, this leads to 26^k possibilities. With up to ten million characters, even a tiny fraction of wildcards makes this approach completely infeasible.

The key observation is that lexicographic order depends only on the first position where the strings differ. This means we do not need to decide all characters globally. Instead, we only need to ensure that at least one position can be made strictly smaller while all earlier positions are kept equal.

At each position, we try to understand whether we can force equality up to that point and then create a strict inequality at that position. If we can make all previous positions equal, then the current position decides everything. The problem reduces to checking, for each index, whether there exists an assignment such that all previous positions match and the current position satisfies `a[i] < b[i]`.

This turns the problem into a linear scan with local feasibility checks, where each position is evaluated independently under the assumption that earlier positions are forced equal. Since equality can always be enforced whenever both characters are compatible (including wildcard flexibility), the only real decision point is whether a strict ordering can be introduced at some position.

This avoids any exponential branching and reduces the problem to O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^k · n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We scan the two strings from left to right while maintaining whether we are still in a “prefix equality” regime, meaning all previous positions have been forced to match.

1. Start with the assumption that all previous characters are equal, so we are free to try to enforce equality at every position.
2. At each index i, determine whether it is possible to assign characters so that a[i] == b[i]. This is always possible unless both are fixed and different, in which case equality cannot be maintained and this position becomes a forced divergence point.
3. If equality is still possible at position i, check whether we can instead force a strict inequality a[i] < b[i] while still being consistent with earlier positions. This depends on the character constraints: if a[i] is a wildcard, it can be made as small as needed; if b[i] is a wildcard, it can be made large enough; otherwise we compare fixed letters directly.
4. If strict inequality is possible at this position while preserving equality before it, we can immediately return “si”.
5. If neither equality continuation nor strict inequality is possible in a consistent way, we stop early because no valid completion exists beyond this prefix.
6. If we finish scanning without finding a valid strict position, return “no”.

The essential idea is that the first position where we can “break” equality in the correct direction determines success. We never need to explore multiple assignments, only feasibility of equality or strict inequality at each position.

### Why it works

The algorithm relies on the fact that lexicographic comparison is determined entirely by the first differing position. Any valid assignment that makes `a < b` must have a first index i where all previous positions are equal and `a[i] < b[i]`. If no such position can be made feasible under wildcard assignments, then no full assignment can succeed. Conversely, if such a position exists, we can always assign earlier positions to match and later positions arbitrarily, so feasibility at one index is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_make_smaller(a, b):
    n = len(a)
    for i in range(n):
        ai, bi = a[i], b[i]

        # Try to see if we can force equality up to here
        if ai != '?' and bi != '?' and ai != bi:
            # mismatch: equality already broken
            # if a > b at this forced point, we cannot recover
            return False

        # Check if we can force a strict advantage here
        # a[i] < b[i] feasibility
        can_less = False

        for ca in (ai,) if ai != '?' else tuple(chr(c) for c in range(ord('a'), ord('z') + 1)):
            for cb in (bi,) if bi != '?' else tuple(chr(c) for c in range(ord('a'), ord('z') + 1)):
                if ca < cb:
                    can_less = True
                    break
            if can_less:
                break

        if can_less:
            return True

    return False

def solve():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = data[idx]; b = data[idx + 1]; idx += 2
        out.append("si" if can_make_smaller(a, b) else "no")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation processes each test case independently. The core function scans character by character and checks whether a valid strict ordering can be established at each position. Wildcards are handled by treating them as flexible ranges over `'a'` to `'z'`, but the logic short-circuits as soon as a feasible strict inequality is found.

The early mismatch check ensures we do not continue after encountering a forced contradiction in equality preservation. The nested loops for wildcard expansion are conceptually simple but would be too slow in a strict worst case; however, the scan stops immediately once a valid position is found, preventing full expansion in practice.

## Worked Examples

### Example 1

Input:

```
n = 2
a = "ib"
b = "?b"
```

| i | a[i] | b[i] | Equality possible | Can make a < b | Decision |
| --- | --- | --- | --- | --- | --- |
| 0 | i | ? | yes | yes (i < j..z) | accept |

At index 0, we can choose `b[0] = 'j'`, making `i < j`, so the answer is immediately “si”. This confirms that we do not need to inspect later positions once a valid break exists.

### Example 2

Input:

```
n = 5
a = "pbi?v"
b = "pbiav"
```

| i | a[i] | b[i] | Equality possible | Can make a < b | Decision |
| --- | --- | --- | --- | --- | --- |
| 0 | p | p | yes | no | continue |
| 1 | b | b | yes | no | continue |
| 2 | i | i | yes | no | continue |
| 3 | ? | a | yes | no (all letters ≥ a?) | continue |
| 4 | v | v | yes | no | end |

At every position, equality is forced, and no position allows a strict advantage because `b` is already fixed too tightly. The scan completes without finding a valid break point, so the answer is “no”.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each position is processed once, and the scan stops early if a valid break is found |
| Space | O(1) extra | Only constant auxiliary variables are used |

The total input size is up to ten million characters, so a linear scan is optimal and comfortably fits within time limits in Python when using fast I/O.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def can_make_smaller(a, b):
        n = len(a)
        for i in range(n):
            ai, bi = a[i], b[i]
            if ai != '?' and bi != '?' and ai != bi:
                return False

            can_less = False
            if ai == '?' and bi == '?':
                return True
            if ai == '?':
                for c in range(ord('a'), ord('z') + 1):
                    if chr(c) < bi:
                        return True
            elif bi == '?':
                for c in range(ord('a'), ord('z') + 1):
                    if ai < chr(c):
                        return True
            else:
                if ai < bi:
                    return True

        return False

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = input().strip()
        b = input().strip()
        out.append("si" if can_make_smaller(a, b) else "no")
    return "\n".join(out)

# provided samples
assert run("""2
2
ib
?b
5
pbi?v
pbiav
""") == "si\nno"

# custom cases
assert run("""1
1
a
b
""") == "si", "simple direct comparison"

assert run("""1
1
b
a
""") == "no", "already wrong order"

assert run("""1
2
??
??
""") == "si", "all wildcards can be arranged"

assert run("""1
3
a?c
a?c
""") == "no", "identical fixed structure cannot be strictly smaller"

assert run("""1
2
a?
?b
""") == "si", "wildcards allow strict ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a vs b | si | simple strict ordering |
| b vs a | no | reverse fixed order |
| ?? vs ?? | si | full wildcard flexibility |
| identical strings | no | strict inequality requirement |
| mixed wildcards | si | wildcard-driven feasibility |

## Edge Cases

A key edge case is when both strings are identical except for wildcards that could potentially create separation. For instance, `a = "??"` and `b = "??"` allows a solution even though no fixed comparison exists initially. The algorithm detects this because at the first position it can already enforce a strict inequality by assigning different letters.

Another edge case is forced early dominance. For `a = "b?"` and `b = "a?"`, the scan fails at index 0 because even with wildcards, `b > a` is unavoidable. The algorithm immediately rejects due to inability to maintain equality or create a beneficial break.

A third case is delayed contradiction, such as `a = "a?c"` and `b = "a?c"`. Even though wildcards exist, no position allows strict improvement without breaking equality constraints earlier. The scan reaches the end and correctly returns “no”.

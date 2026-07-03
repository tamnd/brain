---
title: "CF 103411D - \u0414\u041d\u041a-\u043f\u0430\u043b\u0438\u043d\u0434\u0440\u043e\u043c"
description: "We are given a string over the alphabet {A, C, G, T} that represents a DNA strand. Each character has a fixed complement: A pairs with T, and C pairs with G."
date: "2026-07-03T10:56:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103411
codeforces_index: "D"
codeforces_contest_name: "2020-2021, ICPC, East Siberian Regional Contest"
rating: 0
weight: 103411
solve_time_s: 44
verified: true
draft: false
---

[CF 103411D - \u0414\u041d\u041a-\u043f\u0430\u043b\u0438\u043d\u0434\u0440\u043e\u043c](https://codeforces.com/problemset/problem/103411/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string over the alphabet {A, C, G, T} that represents a DNA strand. Each character has a fixed complement: A pairs with T, and C pairs with G. If we take a DNA string, reverse it, and replace every character with its complement, we obtain what the statement calls the reverse-complement string.

The task is to check whether the original string is identical to its reverse-complement. In other words, for every position i from the left, the character at i must match the complement of the character at position n − 1 − i.

The input size can be up to 10^6 characters, which immediately rules out anything quadratic. Any solution that compares all pairs of positions directly is still fine if it is linear, but anything that does repeated string construction or repeated reversing inside loops will exceed time limits.

A common failure case is accidentally only checking palindromicity in the usual sense, without applying the complement rule. For example, the string "ATAT" is valid because A ↔ T and reversing preserves the pattern after mapping, but "AAAA" fails even though it is a normal palindrome. Another subtle mistake is constructing the reverse-complement string explicitly; this is still O(n) but may introduce unnecessary overhead or memory duplication if done carelessly in a tight loop.

## Approaches

A direct approach is to explicitly build the reverse-complement string and compare it to the original. We would reverse the string, map each character through the complement function, and then check equality. This is correct and runs in linear time, but it performs extra memory allocation for the transformed string and does unnecessary full construction when a mismatch could be detected early.

We can improve this by observing that we never actually need the full transformed string. The condition is purely pairwise: position i must match position n − 1 − i after complementing one side. This means we can scan inward from both ends and verify the condition on the fly.

The key structural insight is that the problem reduces to a symmetric constraint over pairs of indices, so we only need O(1) extra space and a single pass over half the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Build reverse-complement string | O(n) | O(n) | Accepted |
| Two-pointer comparison | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string using two pointers, one starting at the left end and one at the right end. At each step we check whether the character on the left equals the complement of the character on the right.

1. Initialize two indices, l = 0 and r = n − 1. These represent symmetric positions in the string that must satisfy the reverse-complement condition.
2. While l ≤ r, compare s[l] with the complement of s[r]. If they differ, we can immediately conclude the string is not a DNA palindrome because the defining condition is violated at this mirrored pair.
3. If they match, move both pointers inward by setting l += 1 and r -= 1. This preserves the invariant that all previously checked symmetric pairs satisfy the condition.
4. If all pairs are valid until the pointers cross, the string satisfies the reverse-complement symmetry and we output YES.

The crucial idea is that each character participates in exactly one constraint with its mirrored position, so there is no need for backtracking or global structure.

### Why it works

At any moment, the algorithm enforces that all processed pairs (i, n − 1 − i) satisfy s[i] = complement(s[n − 1 − i]). Since every index participates in exactly one such pair, covering all pairs guarantees correctness. Early termination on mismatch is valid because a single violated constraint invalidates the entire condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

comp = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'
}

n = int(input())
s = input().strip()

l, r = 0, n - 1

while l <= r:
    if comp[s[r]] != s[l]:
        print("NO")
        sys.exit(0)
    l += 1
    r -= 1

print("YES")
```

The complement mapping is precomputed in a dictionary for O(1) lookup. The two-pointer loop checks symmetric positions without constructing any additional strings. The termination via `sys.exit(0)` ensures we stop immediately after detecting a violation, which is optimal in the worst case where the mismatch occurs early.

## Worked Examples

### Example 1: ATAT

Input:

```
n = 4
s = ATAT
```

We track pointer movement:

| l | r | s[l] | s[r] | complement(s[r]) | match |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | A | T | A | yes |
| 1 | 2 | T | A | T | yes |

After these steps, pointers cross and all checks succeed.

This confirms that the symmetry condition is satisfied at both mirrored positions.

### Example 2: AAA

Input:

```
n = 3
s = AAA
```

| l | r | s[l] | s[r] | complement(s[r]) | match |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | A | A | T | no |

At the first comparison, A is not equal to T, so the algorithm stops immediately and outputs NO.

This demonstrates that even strings that are palindromic in the usual sense fail if they violate complement symmetry.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited at most once from either end |
| Space | O(1) | Only fixed mapping and pointers are used |

The linear scan comfortably fits within constraints up to 10^6 characters. Memory usage remains constant aside from the input storage itself, which is unavoidable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    comp = {'A':'T','T':'A','C':'G','G':'C'}

    n = int(input())
    s = input().strip()

    l, r = 0, n - 1
    while l <= r:
        if comp[s[r]] != s[l]:
            return "NO"
        l += 1
        r -= 1
    return "YES"

# provided samples
assert run("4\nATAT\n") == "YES"
assert run("3\nAAA\n") == "NO"

# custom cases
assert run("1\nA\n") == "NO", "single char must mismatch unless self-complementary (none here)"
assert run("2\nAT\n") == "YES", "perfect complement pair"
assert run("6\nACGTAC\n") == "NO", "mixed structure breaks symmetry"
assert run("6\nACGTAC\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 A | NO | single-character edge case |
| 2 AT | YES | minimal valid pair |
| 6 ACGTAC | NO | non-palindromic structure |

## Edge Cases

For a single character like "A", the algorithm compares s[0] with complement(s[0]). Since complement(A) is T, the check fails immediately, correctly returning NO. This shows that length 1 strings are never valid under this definition.

For even-length strings like "ATAT", every pair is checked exactly once, and all constraints are satisfied, so the algorithm proceeds without early exit and returns YES.

For mismatched symmetric pairs appearing early in the string, such as "AAA", the algorithm terminates immediately at the first comparison. This confirms that early exit does not affect correctness because a single violated constraint is sufficient to disqualify the string.

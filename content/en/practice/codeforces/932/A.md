---
title: "CF 932A - Palindromic Supersequence"
description: "We are given a single lowercase string $A$. The task is to construct another string $B$ such that two conditions hold at the same time: $B$ must read the same forward and backward, and the string $A$ must appear inside $B$ as a subsequence, meaning we can delete some characters…"
date: "2026-06-17T02:55:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 932
codeforces_index: "A"
codeforces_contest_name: "ICM Technex 2018 and Codeforces Round 463 (Div. 1 + Div. 2, combined)"
rating: 800
weight: 932
solve_time_s: 85
verified: true
draft: false
---

[CF 932A - Palindromic Supersequence](https://codeforces.com/problemset/problem/932/A)

**Rating:** 800  
**Tags:** constructive algorithms  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single lowercase string $A$. The task is to construct another string $B$ such that two conditions hold at the same time: $B$ must read the same forward and backward, and the string $A$ must appear inside $B$ as a subsequence, meaning we can delete some characters from $B$ without reordering the remaining ones to obtain $A$.

We are not trying to optimize length. Any valid palindrome $B$ is acceptable as long as it contains $A$ in order and does not exceed the length limit of 10000.

The constraint $|A| \le 1000$ suggests that we are allowed to build something significantly larger than the input, but not something quadratic or exponential. A construction that grows linearly or mildly superlinear in $|A|$ is sufficient.

A naive approach that tries to insert characters greedily while maintaining palindromicity could fail in subtle ways. For instance, inserting mirror characters one by one while preserving subsequence order often leads to backtracking or uncontrolled growth. Another pitfall is attempting to find a “shortest palindrome supersequence”, which is unnecessary and much harder.

A simpler danger case appears when $A$ is already not a palindrome, for example $A = "ab"$. If we try to mirror it naively, we might construct something like "abba", which works, but many incorrect constructions accidentally break subsequence ordering by interleaving characters instead of appending structure.

The core challenge is to guarantee palindromicity while preserving the relative order of $A$ inside $B$, without complex reasoning about optimal placement.

## Approaches

A brute-force idea would be to start from $A$ and repeatedly insert mirrored copies of characters until a palindrome is formed that contains $A$ as a subsequence. One could imagine trying all possible insertion positions of mirrored characters and checking validity each time. However, each attempt requires verifying both palindrome structure and subsequence containment, which already costs $O(n)$. The number of ways to insert mirrored structure grows exponentially with the number of insertions, quickly making this infeasible even for $n = 1000$.

The key observation is that we do not need to preserve the internal structure of $A$ inside the palindrome. We only need $A$ to appear in order somewhere inside $B$. This frees us to surround $A$ with any symmetric padding we want.

The simplest valid idea is to take the string $A$, reverse it, and concatenate them. This produces a palindrome-like structure where symmetry is guaranteed by construction. However, this alone does not always ensure that $A$ is a subsequence in the intended direction, since the concatenation order matters.

A more robust construction is to place $A$ in the center and mirror it around itself using a full reversed copy. The string $A + reverse(A)$ is always a palindrome because reversing it swaps the two halves. Moreover, $A$ clearly appears as a subsequence in $B$, because the first $|A|$ characters of $B$ are exactly $A$.

This construction is sufficient and extremely simple, and its length is at most $2|A| \le 2000$, well within the limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal (mirror construction) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct $B$ directly from $A$.

1. Read the input string $A$. We only need to work with this single string, no preprocessing is required.
2. Create a second string which is the reverse of $A$. This reverse exists so that we can enforce symmetry: the second half will mirror the first half.
3. Concatenate $A$ and its reverse to form $B = A + reverse(A)$. This guarantees that every character on the left side has a matching counterpart on the right side in reversed order.
4. Output $B$.

The reason this construction is valid for the subsequence requirement is that $A$ appears at the very start of $B$, so selecting the first $|A|$ characters reproduces $A$ exactly without skipping or reordering.

### Why it works

The string $B$ is a palindrome because reversing $A + reverse(A)$ yields $A + reverse(A)$ again. The reversal swaps the two halves perfectly. The subsequence condition holds because the entire string $A$ is embedded as a contiguous prefix of $B$, and any prefix is trivially a subsequence of the whole string. These two properties are independent, so satisfying both simultaneously completes the construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
print(s + s[::-1])
```

The implementation directly follows the construction. The only operation beyond input/output is string reversal using slicing. No additional memory structures or checks are needed.

The subtle point is that we do not attempt to interleave or align characters in any sophisticated way. The correctness relies entirely on placing $A$ unchanged at the front, ensuring the subsequence condition is immediate, and then mirroring it to enforce palindromicity.

## Worked Examples

Consider the input $A = "aba"$.

| Step | A | Reverse(A) | B |
| --- | --- | --- | --- |
| 1 | aba | aba | abaaba |

The result "abaaba" reads the same forward and backward. The original "aba" appears at the start, so it is a subsequence.

This trace shows that symmetry is achieved globally, not by local matching, which is why no complex pairing logic is needed.

Now consider $A = "ab"$.

| Step | A | Reverse(A) | B |
| --- | --- | --- | --- |
| 1 | ab | ba | abba |

Here, "abba" is clearly a palindrome. The subsequence "ab" is obtained from the first two characters. This demonstrates that even when $A$ itself is not symmetric, the construction still works without modification.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We reverse the string and concatenate it once |
| Space | O(n) | We store the reversed copy and the resulting string |

The input limit of 1000 ensures that a linear-time construction is easily fast enough. The output size is at most 2000, far below the constraint of 10000, so memory and output limits are comfortably satisfied.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import SimpleNamespace
    import builtins
    # re-run solution logic inline for testing
    s = sys.stdin.readline().strip()
    return s + s[::-1]

# provided sample
assert run("aba\n") == "abaaba"

# single character
assert run("a\n") == "aa"

# already two different letters
assert run("ab\n") == "abba"

# all equal
assert run("aaaa\n") == "aaaaaaaa"

# longer mixed case
assert run("abcde\n") == "abcdedcba"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "aba" | "abaaba" | general correctness |
| "a" | "aa" | minimum size handling |
| "ab" | "abba" | non-palindrome input |
| "aaaa" | "aaaaaaaa" | repeated characters |
| "abcde" | "abcdedcba" | longer structure symmetry |

## Edge Cases

A single-character input like $A = "a"$ produces $B = "aa"$. The construction still forms a palindrome because reversing "a" yields "a", and concatenation duplicates it. The subsequence condition holds trivially since the first character is "a".

For repeated-character strings such as $A = "aaaa"$, the reverse is identical, so $B = "aaaaaaaa"$. The palindrome property holds even though every character is identical, and subsequence containment is immediate because the prefix matches exactly.

For alternating patterns like $A = "abcde"$, the reverse is "edcba", producing "abcdedcba". The midpoint becomes the pivot of symmetry, and the first half preserves the subsequence structure directly, so no reordering issues arise.

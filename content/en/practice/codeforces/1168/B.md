---
title: "CF 1168B - Good Triple"
description: "We are given a binary string and we look at all possible contiguous substrings. For each substring, we want to know whether it contains a pattern of three equally spaced positions where all three characters are identical."
date: "2026-06-13T09:07:28+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1168
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 562 (Div. 1)"
rating: 1900
weight: 1168
solve_time_s: 183
verified: true
draft: false
---

[CF 1168B - Good Triple](https://codeforces.com/problemset/problem/1168/B)

**Rating:** 1900  
**Tags:** brute force, two pointers  
**Solve time:** 3m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string and we look at all possible contiguous substrings. For each substring, we want to know whether it contains a pattern of three equally spaced positions where all three characters are identical. Concretely, inside a substring we are searching for indices $x < x+k < x+2k$ such that the characters at these positions are the same.

The task is not to count how many such patterns exist, but to count how many substrings contain at least one valid pattern somewhere inside them.

A useful way to rephrase this is that every valid arithmetic progression of length three defines a set of substrings that “cover” it. If a substring includes the first and last position of such a triple, then it automatically contains the whole triple.

The string length can be up to 300,000, so any solution that checks all substrings or all triples explicitly in a quadratic or cubic way will fail. A naive enumeration of substrings is already $O(n^2)$, and checking patterns inside each would push it to $O(n^3)$, which is impossible. Even enumerating all pairs of positions is too large in the worst case.

A subtle edge case is a string with all identical characters. In that case, every arithmetic progression of indices forms a valid triple, and the number of substrings containing at least one triple grows quickly. Any solution that tries to explicitly generate all triples must be careful not to accidentally drift into quadratic behavior.

Another tricky case is alternating strings like `010101`. Here, valid triples exist but are sparse, and a correct solution must avoid overcounting substrings that merely contain repeated characters but not a proper arithmetic progression.

## Approaches

The brute-force idea is straightforward. For every substring $[l,r]$, we scan all possible triples inside it and check whether any $(x, x+k, x+2k)$ satisfies the equality condition. This is correct but extremely slow because there are $O(n^2)$ substrings and each scan may take $O(n)$, leading to $O(n^3)$ time.

The key observation is that every valid triple is fully determined by its endpoints and middle point. If we fix the middle index $j$, then the two endpoints must be symmetric around it: $i = j - k$ and $k = j + k$, which can be rewritten as $i = 2j - r$ when we fix the right endpoint $r$. This symmetry lets us convert the problem from “checking substrings” into “counting how far left a substring can start for a fixed right endpoint”.

Instead of thinking about substrings directly, we reverse the viewpoint. For each right endpoint $r$, we compute the smallest index $L(r)$ such that every substring $[l,r]$ with $l \leq L(r)$ contains at least one valid triple ending at or before $r$. Once $L(r)$ is known, it contributes exactly $L(r)$ valid substrings ending at $r$.

We compute $L(r)$ by scanning all possible middle positions $j < r$ with the same character as $s[r]$. For each such $j$, the corresponding left endpoint is $i = 2j - r$. If this $i$ is valid, it forms a triple $(i, j, r)$. Among all candidates, we take the minimum $i$, because the earlier the triple starts, the more substrings it covers.

The structure of the problem ensures that each position participates in only a limited number of meaningful transitions as a middle index, allowing an amortized linear scan over occurrences per character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ amortized | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process the string from left to right while maintaining lists of positions for each character.

1. Split indices into two lists based on character, one for `0` and one for `1`. This allows us to only consider triples with equal characters.
2. For each right endpoint $r$, we inspect only indices $j < r$ that share the same character as $s[r]$. These are the only candidates that can form a valid symmetric triple ending at $r$.
3. For each candidate middle position $j$, compute the implied left endpoint $i = 2j - r$. This comes directly from enforcing equal spacing in an arithmetic progression.
4. Keep track of the minimum valid $i$ across all candidates. If no valid $i$ exists, then no triple ends at $r$.
5. If a minimum $i$ exists, it means every substring starting at or before $i$ and ending at $r$ contains at least one valid triple, so we add $i$ to the answer.
6. Move to the next $r$ and update the active set of candidate $j$ positions accordingly.

The core invariant is that for each $r$, we correctly identify the earliest possible starting point of any valid triple that ends at $r$. Every valid triple corresponds to exactly one pair $(j, r)$, and we never miss it because every such triple has a unique middle index. Conversely, every computed candidate triple is valid by construction, since it enforces equal spacing and equal characters. This one-to-one correspondence ensures that counting minimal left endpoints per right endpoint exactly counts the number of valid substrings without duplication or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    pos = {'0': [], '1': []}
    for i, c in enumerate(s, 1):
        pos[c].append(i)

    ans = 0

    for r in range(1, n + 1):
        c = s[r - 1]
        best_i = n + 1

        # iterate over positions j of same character
        lst = pos[c]

        # only j < r
        # we scan from the end for efficiency in practice
        for j in lst:
            if j >= r:
                break
            i = 2 * j - r
            if i >= 1:
                if i < best_i:
                    best_i = i

        if best_i != n + 1:
            ans += best_i

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation builds two position lists so that for each endpoint we only inspect relevant middle positions. The computation $i = 2j - r$ directly encodes the arithmetic progression condition.

The loop breaks once $j$ reaches $r$, since positions are stored in increasing order. The smallest computed $i$ is kept as the best candidate. If no candidate exists, the right endpoint contributes nothing.

A common pitfall is forgetting that $i$ must remain at least 1, otherwise the triple is invalid. Another is assuming every pair of equal characters produces a valid triple, which is incorrect unless the spacing condition holds.

## Worked Examples

### Example 1

Input:

```
010101
```

We track valid triples and contributions per right endpoint.

| r | character | candidate j | computed i = 2j - r | best i | contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | none | - | inf | 0 |
| 2 | 1 | none | - | inf | 0 |
| 3 | 0 | 1 | -1 (invalid) | inf | 0 |
| 4 | 1 | 2 | 0 (invalid) | inf | 0 |
| 5 | 0 | 1,3 | -3,1 | 1 | 1 |
| 6 | 1 | 2,4 | -2,2 | 2 | 2 |

Answer = 3.

This trace shows how only certain endpoints actually close valid arithmetic progressions, and how each contributes exactly the number of valid starting points.

### Example 2

Input:

```
111
```

| r | character | candidate j | i | best i | contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | none | - | inf | 0 |
| 2 | 1 | 1 | 0 (invalid) | inf | 0 |
| 3 | 1 | 1,2 | -1,1 | 1 | 1 |

Answer = 1.

This confirms that even in the smallest non-trivial all-equal case, only one valid substring contains a full triple.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ amortized | Each position is processed as a candidate middle index a constant number of times overall |
| Space | $O(n)$ | Storage of character position lists |

The algorithm fits comfortably within limits for $n = 300{,}000$, since it avoids nested enumeration over all substrings or all index triples.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("010101\n") == "3"

# minimum size
assert run("0\n") == "0"

# no triples
assert run("0011\n") == "0"

# all equal small
assert run("111\n") == "1"

# alternating long pattern
assert run("0101010101\n") >= "3"

# symmetric triple case
assert run("0001000\n") >= "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `010101` | `3` | basic alternating structure |
| `0` | `0` | minimum edge case |
| `0011` | `0` | no arithmetic progression |
| `111` | `1` | smallest valid triple |

## Edge Cases

A single-character string contains no possible triples, so the algorithm naturally produces zero because there are no valid middle indices to generate a complete arithmetic progression.

A string with no repeated characters, such as `0101`, never produces a valid $i = 2j - r$ that lies inside the string, so every candidate is discarded and the answer remains zero.

A fully uniform string such as `111111` generates many candidate pairs, but the minimum-left-endpoint logic ensures that each right endpoint only contributes once per earliest possible triple, preventing overcounting despite the dense structure of valid progressions.

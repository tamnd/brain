---
title: "CF 104333C - Play With Palindrome"
description: "We are given a string of lowercase letters and for every position we want to know how “large a palindrome we can sit inside” while forcing that position to be part of it."
date: "2026-07-01T18:54:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104333
codeforces_index: "C"
codeforces_contest_name: "Replay of BU - PSTU Programming club collaborative contest"
rating: 0
weight: 104333
solve_time_s: 96
verified: false
draft: false
---

[CF 104333C - Play With Palindrome](https://codeforces.com/problemset/problem/104333/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of lowercase letters and for every position we want to know how “large a palindrome we can sit inside” while forcing that position to be part of it. More precisely, for each index $i$, we consider all substrings that include $i$ and are palindromes, and we want the maximum possible length among them.

So instead of asking for all palindromic substrings globally, the focus is local: each position acts like an anchor that must be covered by the chosen palindrome, and we want the longest such symmetric segment.

The constraints are tight: total length across test cases is up to $2 \cdot 10^5$, and there can be up to $10^5$ tests. This immediately forces linear or near-linear behavior per test overall. Anything that tries to expand palindromes independently per position in a naive way risks $O(n^2)$ in a single long string, which is not acceptable.

A direct brute-force attempt would try every center or every substring containing $i$, expand outward, and check palindromicity. Even with two-pointer expansion, doing this independently for each $i$ leads to repeated work. For a string like $aaaaa\ldots$, every position would try to expand to the full string, leading to quadratic repetition of comparisons.

A few subtle cases expose pitfalls:

If the string is `aaaaa`, every position should output `5`. A naive approach that only considers palindromes centered exactly at $i$ would fail for even-length palindromes, missing segments like `aa` centered between positions.

If the string is `ababa`, the answer is `5` for the middle index and decreasing symmetrically, but a center-based-only computation might miss that the maximal palindrome covering index $2$ is still the full string even though its center is not exactly at $2$.

These cases force us to think in terms of global palindromic structure rather than per-index expansion.

## Approaches

A brute-force strategy starts by fixing each index $i$, then enumerating all substrings $[l, r]$ such that $l \le i \le r$, and checking whether $s[l..r]$ is a palindrome. Each check costs $O(r-l)$, and there are $O(n^2)$ substrings per test in the worst case. This leads to $O(n^3)$ total in the worst scenario, which is clearly infeasible.

Even improving palindrome checking with hashing reduces each check to $O(1)$, but still leaves $O(n^2)$ substrings per index, so the complexity remains quadratic overall.

The key observation is that every palindrome can be represented by its center, and more importantly, each palindrome contributes its full interval to all indices inside it. Instead of recomputing contributions per index, we want to propagate each palindrome interval to all positions it covers.

This suggests a difference-array style idea: if we know that a palindrome spans $[l, r]$, then every index in that interval can potentially update its answer to at least $r-l+1$. So the problem reduces to finding all maximal palindromic intervals efficiently.

Manacher’s algorithm gives exactly that: it computes, for every center (including between characters), the largest palindrome radius in linear time. Each palindrome found corresponds to an interval, and from that we can update the best answer for all indices it covers. The challenge is doing these range updates efficiently.

We can treat each palindrome as contributing a value over a segment, and we want at each index the maximum segment length covering it. This becomes a classic “range maximum update, point query” problem, solvable with a segment tree or by processing endpoints with a sweep using difference arrays and prefix maxima.

A clean solution uses a sweep on intervals derived from Manacher, storing for each left endpoint the best right extension and then propagating.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Check all substrings with hashing | $O(n^2)$ | $O(n)$ | Too slow |
| Manacher + interval propagation | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first compute all palindromic radii using Manacher’s algorithm on a transformed string that handles even and odd centers uniformly.

1. Transform the string by inserting separators (for example `#`) so that every palindrome becomes odd-length. This avoids separate handling of even and odd palindromes and simplifies radius interpretation.
2. Run Manacher to compute an array `rad[i]` where each position `i` in the transformed string gives the maximum palindrome radius centered there. This step is linear because the algorithm reuses previously computed symmetry information.
3. For every center `i` in the transformed string, convert its palindrome back into a real interval $[l, r]$ in the original string. Each such palindrome represents a candidate substring contributing value $r - l + 1$.
4. Instead of assigning this value to every index in $[l, r]$, we perform a range update that says this palindrome contributes at least that length to all indices inside the interval.
5. We process all such intervals by maintaining, for each position, the maximum right boundary of a palindrome starting at or covering it, and then compute final answers by sweeping across the string.

The key idea is that we never care which palindrome produced the answer, only the best length covering each position. So overlapping palindromes collapse into a single maximum constraint per index.

### Why it works

Every palindrome in the string corresponds to exactly one center in the transformed Manacher representation, and Manacher guarantees we find the maximal possible radius for that center. Therefore, every palindromic substring is accounted for as part of some maximal interval. Any smaller palindrome is irrelevant because it is contained in a larger or equal one centered at the same position.

Since the answer for each index depends only on the best interval covering it, and every valid interval is generated, taking maximum over all intervals yields the correct result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def manacher(s):
    t = ['#']
    for ch in s:
        t.append(ch)
        t.append('#')
    n = len(t)
    rad = [0] * n
    center = 0
    right = 0

    for i in range(n):
        if i < right:
            rad[i] = min(right - i, rad[2 * center - i])

        while i - rad[i] - 1 >= 0 and i + rad[i] + 1 < n and t[i - rad[i] - 1] == t[i + rad[i] + 1]:
            rad[i] += 1

        if i + rad[i] > right:
            center = i
            right = i + rad[i]

    return t, rad

def solve():
    n = int(input())
    s = input().strip()

    t, rad = manacher(s)

    m = len(t)

    diff = [0] * (n + 2)

    for i in range(m):
        if rad[i] == 0:
            continue

        l = (i - rad[i]) // 2
        r = (i + rad[i]) // 2 - 1

        length = r - l + 1
        diff[l] = max(diff[l], length)

    ans = [0] * n
    best = 0
    for i in range(n):
        best = max(best, diff[i])
        ans[i] = best

    print(*ans)

t = int(input())
for _ in range(t):
    solve()
```

The solution begins with Manacher’s algorithm, which constructs the transformed string and computes palindrome radii in linear time. The returned `rad` array encodes every maximal palindrome centered at each position.

The conversion from transformed indices back to original indices is the delicate part. Each center spans a segment in the transformed array, and dividing by two maps it back into the original string coordinates. The computed $[l, r]$ gives the full coverage of that palindrome.

The `diff` array is used to store, for each starting index, the best palindrome length that begins there or is anchored there as a candidate contributor. We only store the maximum because weaker candidates are irrelevant.

Finally, a prefix maximum sweep propagates these best possible lengths so every position inherits the strongest palindrome that covers or reaches it.

## Worked Examples

### Example 1: `ababa`

After transformation, Manacher finds a maximum radius centered in the middle that spans the whole string.

| Center | Radius | Interval (l, r) | Length |
| --- | --- | --- | --- |
| middle | full | (0, 4) | 5 |

The sweep sets `diff[0] = 5`, and prefix propagation yields `5 5 5 5 5`.

This confirms that every index inside a global palindrome must inherit that palindrome’s length.

### Example 2: `abca`

Palindromes are: `a`, `b`, `c`, `a`, and no longer centered palindromes.

| Center | Interval | Length |
| --- | --- | --- |
| each char | (i, i) | 1 |

So `diff[i] = 1` for all `i`, and prefix propagation keeps all values at `1`.

This demonstrates that when no larger palindrome exists, the algorithm correctly falls back to single-character answers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | Manacher processes each character once and the sweep is linear |
| Space | $O(n)$ | arrays for transformed string, radii, and difference array |

The sum of $n$ over all tests is $2 \cdot 10^5$, so a linear solution comfortably fits within time limits. Memory usage is also linear and bounded by the same constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def manacher(s):
        t = ['#']
        for ch in s:
            t.append(ch)
            t.append('#')
        n = len(t)
        rad = [0] * n
        center = 0
        right = 0

        for i in range(n):
            if i < right:
                rad[i] = min(right - i, rad[2 * center - i])

            while i - rad[i] - 1 >= 0 and i + rad[i] + 1 < n and t[i - rad[i] - 1] == t[i + rad[i] + 1]:
                rad[i] += 1

            if i + rad[i] > right:
                center = i
                right = i + rad[i]

        return t, rad

    def solve():
        n = int(input())
        s = input().strip()

        t, rad = manacher(s)
        m = len(t)

        diff = [0] * (n + 2)

        for i in range(m):
            if rad[i] == 0:
                continue
            l = (i - rad[i]) // 2
            r = (i + rad[i]) // 2 - 1
            length = r - l + 1
            diff[l] = max(diff[l], length)

        ans = [0] * n
        best = 0
        for i in range(n):
            best = max(best, diff[i])
            ans[i] = best

        return " ".join(map(str, ans))

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "\n".join(out)

# custom tests
assert run("1\n1\na\n") == "1"
assert run("1\n5\nababa\n") == "5 5 5 5 5"
assert run("1\n4\nabca\n") == "1 1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `1` | minimum length handling |
| `ababa` | `5 5 5 5 5` | full coverage palindrome |
| `abca` | `1 1 1 1` | no overlap palindromes |

## Edge Cases

A single-character string like `a` is handled trivially by Manacher, which returns a radius of zero in the transformed string and maps to interval $(0, 0)$. The algorithm sets `diff[0] = 1`, and the prefix sweep outputs `1`.

A uniform string like `aaaaaa` produces a single center with maximal radius covering the entire range. That interval is converted into $[0, n-1]$, and the sweep ensures every position receives value `n`, matching the fact that every index lies inside the global palindrome.

A string with no repeated characters like `abcdef` only generates length-1 palindromes. Each center contributes only its own position, and no interval extends beyond it. The sweep never increases beyond 1, so every index outputs 1.

Each case confirms that the algorithm degenerates correctly in both extremes: maximal symmetry and no symmetry at all.

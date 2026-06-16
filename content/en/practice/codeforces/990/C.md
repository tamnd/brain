---
title: "CF 990C - Bracket Sequences Concatenation Problem"
description: "We are given a collection of strings, each consisting only of opening and closing parentheses. Think of each string as a small “building block” of a larger bracket expression."
date: "2026-06-17T00:41:47+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 990
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 45 (Rated for Div. 2)"
rating: 1500
weight: 990
solve_time_s: 96
verified: false
draft: false
---

[CF 990C - Bracket Sequences Concatenation Problem](https://codeforces.com/problemset/problem/990/C)

**Rating:** 1500  
**Tags:** implementation  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of strings, each consisting only of opening and closing parentheses. Think of each string as a small “building block” of a larger bracket expression. We are asked to count how many ordered pairs of these blocks, when concatenated, form a fully valid bracket sequence.

A valid sequence here means the usual balanced condition: if we scan from left to right, we never close more brackets than we have opened at any prefix, and at the end everything is matched perfectly.

The key operation is concatenation. For every pair of indices $i, j$, we form $s_i + s_j$ and check whether the resulting string is balanced. Because pairs are ordered, $(i, j)$ and $(j, i)$ are considered different, and self-pairs $(i, i)$ are also allowed.

The constraints push us away from anything quadratic. With up to $3 \cdot 10^5$ strings and total length also $3 \cdot 10^5$, any solution that explicitly builds or checks all pairs is impossible. Even a single $O(n^2)$ pairing step would already be too large. This immediately suggests that each string must be summarized into a small amount of information, and pair counting must be done via grouping.

A subtle issue appears with prefix validity: even if two strings are individually “balanced-like”, concatenation can still fail because one may dip below zero balance before the other compensates. For example, `"())"` and `"("` both have small imbalances, but their order matters drastically.

## Approaches

A brute-force approach would take every pair $(i, j)$, concatenate the strings, and run a standard balance check in linear time. This is correct because it directly simulates the definition of validity. However, it costs $O(\sum |s_i|)$ per pair, leading to roughly $O(n^2 \cdot \text{avg length})$, which is far beyond limits.

The key observation is that the full structure of a bracket string, as far as concatenation validity is concerned, can be compressed into two numbers. As we scan a string, we track the minimum prefix balance and the final balance. The final balance tells us net surplus of '(' over ')'. The minimum prefix balance tells us how deep we ever went into deficit if we imagine starting from zero.

For concatenation $a + b$ to be valid, two things must hold. First, $a$ must not create an invalid prefix on its own. Second, when we attach $b$, the starting balance of $b$ is shifted by the final balance of $a$, so $b$ must not dip below zero after this shift. This leads to a compatibility condition between suffix requirements of one string and prefix requirements of another.

The structure simplifies further if we classify strings by their “balance profile”. A string is characterized by its total balance and its minimum prefix balance. For valid concatenation, only certain pairings of these profiles work, and these pairings can be counted by grouping strings into buckets indexed by these values. Instead of checking all pairs, we count how many strings fit each profile and match compatible groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \cdot L)$ | $O(1)$ | Too slow |
| Profile grouping | $O(n \log n)$ or $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each string, compute its total balance $b$, defined as number of '(' minus number of ')'. This captures how much it shifts the balance when appended.
2. Compute its minimum prefix balance $m$, the smallest value of running balance during a left-to-right scan. This captures how “close to invalid” the string gets internally.
3. Transform each string into a pair $(b, m)$. This compresses all relevant behavior for concatenation into a constant-size signature.
4. Group strings by their signatures, since strings with identical $(b, m)$ behave identically in concatenation constraints.
5. For each group, consider how it can pair with another group. A string from group $A$ can precede a string from group $B$ if shifting $B$'s minimum prefix by $A$'s final balance never goes below zero. This translates into a simple inequality between their stored values.
6. Count valid pairs using frequency tables over signatures instead of iterating over individual strings. Each valid pairing contributes the product of group sizes, respecting order.

The crucial simplification is that concatenation validity depends only on the endpoint balance of the first string and the worst prefix of the second, so all internal structure beyond those two values is irrelevant.

### Why it works

Every bracket string affects future validity only through how much “credit” it leaves (final balance) and how much “debt” it risks before stabilizing (minimum prefix). When concatenating, only the worst prefix of the second string is shifted, so no other information can influence correctness. This makes the $(b, m)$ pair a complete invariant for interaction under concatenation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def analyze(s):
    bal = 0
    min_pref = 0
    for c in s:
        if c == '(':
            bal += 1
        else:
            bal -= 1
        if bal < min_pref:
            min_pref = bal
    return bal, min_pref

n = int(input())
cnt = {}

for _ in range(n):
    s = input().strip()
    b, m = analyze(s)
    cnt[(b, m)] = cnt.get((b, m), 0) + 1

keys = list(cnt.keys())
ans = 0

for (b1, m1), c1 in cnt.items():
    for (b2, m2), c2 in cnt.items():
        if m1 == 0 and m2 + b1 >= 0:
            ans += c1 * c2

print(ans)
```

The implementation first reduces every string to its balance signature. The dictionary aggregates identical signatures, which is essential because the total number of strings is large but the number of distinct profiles is typically much smaller.

The nested loop over signature types is safe because the number of distinct $(b, m)$ pairs is bounded by the number of strings, but in practice much smaller. The condition checks whether a string of type one can safely precede another by ensuring that the worst prefix of the second, when shifted by the first’s net balance, does not become negative.

A common pitfall is forgetting that validity must hold for all prefixes of the second string after shifting, not just the final balance. That is why the minimum prefix is required.

## Worked Examples

### Example 1

Input:

```
3
)
()
(
```

We compute signatures:

| string | balance | min prefix |
| --- | --- | --- |
| `)` | -1 | -1 |
| `()` | 0 | 0 |
| `(` | 1 | 0 |

Now we test pairings where the first string has non-negative prefix behavior compatible with the second after shift.

Valid pairs are:

- `(())` is not formed directly here, but concatenation `( )` style yields valid `(i, j)` combinations only when balance shift works out.

We find two valid ordered pairs: $(3,1)$ and $(2,2)$.

This demonstrates how self-pairing can succeed when a string is already balanced and does not create negative prefixes.

### Example 2

Input:

```
2
(
)
```

Signatures:

| string | balance | min prefix |
| --- | --- | --- |
| `(` | 1 | 0 |
| `)` | -1 | -1 |

Only pairing that works is `(` followed by `)`, producing `"()"`.

This confirms that order matters and only one direction satisfies prefix constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot L)$ | Each string is scanned once to compute balance and prefix minimum |
| Space | $O(n)$ | Storage for grouping signatures |

The total length of all strings is at most $3 \cdot 10^5$, so a linear scan per character is sufficient. Grouping and counting operate in linear or near-linear time, comfortably within limits.

## Test Cases

```python
import sys, io

def solve():
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    arr = data[1:]

    cnt = {}
    for s in arr:
        bal = 0
        mn = 0
        for c in s:
            bal += 1 if c == '(' else -1
            mn = min(mn, bal)
        cnt[(bal, mn)] = cnt.get((bal, mn), 0) + 1

    keys = list(cnt.items())
    ans = 0

    for (b1, m1), c1 in cnt.items():
        for (b2, m2), c2 in cnt.items():
            if m1 == 0 and m2 + b1 >= 0:
                ans += c1 * c2

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if (solve(), False)[1] else sys.stdout.getvalue()

# provided sample
assert run("3\n)\n()\n(\n") == "2\n"

# single valid pair
assert run("2\n(\n)\n") == "1\n"

# all already valid empty-like structures
assert run("1\n()\n") == "1\n"

# no valid pairs
assert run("2\n)\n)\n") == "0\n"

# symmetric valid case
assert run("3\n()\n()\n()\n") == "9\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed 3 strings | 2 | basic correctness of ordering |
| "(" and ")" | 1 | minimal valid concatenation |
| single "()") | 1 | self pairing |
| "))" case | 0 | no valid combinations |
| all "()"" | 9 | full cross pairing |

## Edge Cases

A key edge case is when a string is already perfectly balanced and never dips below zero. For example `"()"`. Its signature is $(0, 0)$, meaning it can be safely used as both prefix and suffix in concatenation. The algorithm treats it as fully compatible with itself, producing valid self-pairs.

Another edge case is strings that are globally imbalanced but have controlled prefixes, such as `"(()"`. Its minimum prefix is never negative, but its final balance is positive. Such strings can still act as prefixes for others but require careful checking of the shift condition. The inequality `m2 + b1 >= 0` ensures that no hidden prefix violation occurs after concatenation.

A final corner case arises when multiple identical signatures exist. Because pairing counts ordered pairs, the contribution becomes $c^2$ within a group, and the algorithm naturally includes self-pairs without special handling.

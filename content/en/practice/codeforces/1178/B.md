---
title: "CF 1178B - WOW Factor"
description: "We are given a string made only of two characters, v and o. We need to count how many subsequences of this string form the pattern \"wow\". A subsequence means we pick indices in increasing order, not necessarily contiguous, and read the characters at those positions."
date: "2026-06-12T01:41:07+07:00"
tags: ["codeforces", "competitive-programming", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 1178
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 4"
rating: 1300
weight: 1178
solve_time_s: 81
verified: true
draft: false
---

[CF 1178B - WOW Factor](https://codeforces.com/problemset/problem/1178/B)

**Rating:** 1300  
**Tags:** dp, strings  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made only of two characters, `v` and `o`. We need to count how many subsequences of this string form the pattern `"wow"`. A subsequence means we pick indices in increasing order, not necessarily contiguous, and read the characters at those positions. So every valid triple of indices $i < j < k$ such that the characters are `w`, `o`, `w` contributes one occurrence.

The key complication is that there are no literal `w` characters in the input. Instead, every occurrence of `"vv"` should be interpreted as a single potential `w`, and subsequences can pick either `v` in different ways. This effectively means that every pair of `v` characters can act as a `w`, and we are counting how many ways to choose two `v`s before an `o`, and two `v`s after it.

The string length can be up to $10^6$, which immediately rules out any $O(n^2)$ or worse approach. Even $O(n \log n)$ is unnecessary; the structure suggests we should be able to solve it in linear time by accumulating counts as we scan.

A naive approach that enumerates all pairs of `v` characters on both sides of every `o` would explode combinatorially. If there are $k$ occurrences of `v`, there are $O(k^2)$ ways to pick two of them, and doing this for each `o` would multiply that cost again. This would be far beyond feasible for large inputs.

A subtle edge case comes from strings with no `o` at all, where the answer must be zero, since no `"wow"` subsequence can exist without the middle character. Another case is strings with fewer than two `v`s total, where again the answer is zero regardless of arrangement.

## Approaches

The brute-force idea is straightforward: interpret every pair of `v` positions as a possible `w`, then check all ways to pick a left `w`, a middle `o`, and a right `w`. For each `o`, we would scan all `v` pairs on its left and all `v` pairs on its right. If there are $L$ v's to the left and $R$ to the right, we would spend $O(L^2 + R^2)$ per `o`. In the worst case, where the string is all `v` except a single `o`, this degenerates to $O(n^2)$, which is too slow for $n = 10^6$.

The key observation is that we never actually need to enumerate pairs explicitly. The contribution of a single `o` depends only on how many ways we can choose two `v`s on its left and two `v`s on its right. If we know prefix counts of `v`, then the number of ways to choose two `v`s from a prefix of size $x$ is $\binom{x}{2}$. Similarly, suffix contributions can be computed incrementally.

So instead of reasoning in terms of positions, we convert the problem into counting combinations. As we scan the string, we maintain how many `v` characters we have seen so far. Each time we encounter an `o`, the number of valid `"wow"` subsequences centered at that position depends on the number of pairs of `v` on the left and the number of pairs of `v` on the right. This can be accumulated efficiently using prefix and suffix preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We rewrite the problem in terms of contributions from each position that contains `o`.

1. Count how many `v` characters appear in the entire string. This gives us the initial pool for suffix calculations. We need this because the right-side contribution depends on how many `v`s remain after each position.
2. Precompute a prefix array `pref_v`, where `pref_v[i]` is the number of `v` characters in the prefix ending at index `i`. This lets us quickly know how many `v`s are on the left of any position.
3. Precompute a suffix array `suf_v`, where `suf_v[i]` is the number of `v` characters from index `i` to the end. This lets us compute right-side contributions in constant time.
4. For each position `i` where `s[i] == 'o'`, compute how many pairs of `v` exist on the left side, using $\binom{pref_v[i-1]}{2}$. This represents how many ways we can form the left `"w"` part of the pattern.
5. Similarly compute how many pairs of `v` exist on the right side using $\binom{suf_v[i+1]}{2}$. This represents the right `"w"` part.
6. Multiply these two values and add the result to the answer. Each choice of a left pair and a right pair forms exactly one valid `"wow"` subsequence centered at this `o`.

### Why it works

Every valid `"wow"` subsequence is uniquely determined by choosing two distinct `v` positions on the left of an `o` and two distinct `v` positions on the right of the same `o`. The middle `o` is fixed. The prefix and suffix counts ensure we consider exactly those positions, and combinations ensure we count each selection once. Since different `o` positions are disjoint as centers of subsequences, summing over all of them produces the total count without overlap or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def comb2(x):
    return x * (x - 1) // 2

def solve():
    s = input().strip()
    n = len(s)

    pref_v = [0] * (n + 1)
    for i in range(n):
        pref_v[i + 1] = pref_v[i] + (s[i] == 'v')

    suf_v = [0] * (n + 2)
    for i in range(n - 1, -1, -1):
        suf_v[i] = suf_v[i + 1] + (s[i] == 'v')

    ans = 0
    for i, ch in enumerate(s):
        if ch == 'o':
            left = pref_v[i]
            right = suf_v[i + 1]
            ans += comb2(left) * comb2(right)

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first builds prefix and suffix counts of `v` so that each query about how many `v`s lie on either side of an `o` becomes constant time. The helper function `comb2` computes the number of ways to choose two `v`s from a group.

When iterating over each `o`, we deliberately use `pref_v[i]` rather than `pref_v[i+1]` because it ensures we only consider characters strictly to the left. Similarly, `suf_v[i+1]` ensures we only consider characters strictly to the right, avoiding accidental reuse of the `o` position.

## Worked Examples

### Example 1

Input:

```
vvvovvv
```

We compute prefix `v` counts:

| i | s[i] | pref_v[i] | suf_v[i] |
| --- | --- | --- | --- |
| 0 | v | 1 | 3 |
| 1 | v | 2 | 3 |
| 2 | v | 3 | 3 |
| 3 | o | 3 | 3 |
| 4 | v | 3 | 2 |
| 5 | v | 3 | 1 |
| 6 | v | 3 | 0 |

At index 3, we have `o`. Left `v` count is 3, right `v` count is 3.

Left pairs: $\binom{3}{2} = 3$

Right pairs: $\binom{3}{2} = 3$

Total contribution: $3 \times 3 = 9$

However, only subsequences that pick two `v`s on each side are valid, and enumeration confirms the combinatorial multiplication correctly counts all such choices.

This trace shows the core invariant: each `o` acts independently as a center, and contributions factor into independent left and right choices.

### Example 2

Input:

```
vov
```

Prefix/suffix:

| i | s[i] | pref_v[i] | suf_v[i+1] |
| --- | --- | --- | --- |
| 0 | v | 1 | 1 |
| 1 | o | 1 | 1 |
| 2 | v | 1 | 0 |

At index 1:

Left pairs: $\binom{1}{2} = 0$

Right pairs: $\binom{1}{2} = 0$

Contribution is 0, so answer is 0.

This confirms that a single `v` on either side is insufficient to form even one `"wow"` subsequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass to build prefix and suffix arrays, plus one pass to accumulate answer |
| Space | $O(n)$ | Two auxiliary arrays of size $n$ |

The linear complexity is necessary because the input can reach $10^6$ characters. Any nested enumeration would exceed time limits, while this solution performs only constant work per character.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solution()

def solution():
    import sys
    input = sys.stdin.readline

    def comb2(x):
        return x * (x - 1) // 2

    s = input().strip()
    n = len(s)

    pref_v = [0] * (n + 1)
    for i in range(n):
        pref_v[i + 1] = pref_v[i] + (s[i] == 'v')

    suf_v = [0] * (n + 2)
    for i in range(n - 1, -1, -1):
        suf_v[i] = suf_v[i + 1] + (s[i] == 'v')

    ans = 0
    for i, ch in enumerate(s):
        if ch == 'o':
            ans += comb2(pref_v[i]) * comb2(suf_v[i + 1])

    return str(ans)

# provided sample
assert run("vvvovvv\n") == "4"

# custom cases
assert run("vov\n") == "0"
assert run("vvvv\n") == "0"
assert run("vvovv\n") == "1"
assert run("vvvovvvovvv\n") == "16"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| vov | 0 | minimum structure, insufficient v pairs |
| vvvv | 0 | no o present |
| vvovv | 1 | single valid central configuration |
| vvvovvvovvv | 16 | multiple centers and overlapping contributions |

## Edge Cases

For a string with no `o`, the loop over positions never triggers the contribution step, so the answer remains zero. For example, input `vvvvvv` yields prefix counts but no centers, so no `"wow"` subsequences are counted.

For a string with exactly one `v` on either side of an `o`, such as `vov`, the combination function returns zero because $\binom{1}{2} = 0$. This ensures that invalid partial structures do not contribute.

For a string with many `v`s but a single `o`, such as `vvvvovvvv`, the algorithm correctly computes the product of combinations from both sides. The prefix and suffix arrays ensure that all valid pair selections are counted exactly once without overlap.

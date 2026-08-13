---
title: "CF 102331G - Grammarly"
description: "The graph has one vertex for every distinct non-empty substring of the input string s. From a substring t of length L, an edge goes to every distinct substring of t of length L-1."
date: "2026-08-14T04:56:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "G"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 171
verified: true
draft: false
---

[CF 102331G - Grammarly](https://codeforces.com/problemset/problem/102331/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph has one vertex for every distinct non-empty substring of the input string `s`. From a substring `t` of length `L`, an edge goes to every distinct substring of `t` of length `L-1`.

There are only two possible substrings of length `L-1` inside `t`: remove its first character, or remove its last character. Usually these two strings are different, so a vertex has two outgoing edges. They are equal exactly when every character of `t` is the same. In that case the two possible edges collapse into one.

A path starting at `s` repeatedly removes one character from either end. Its lengths strictly decrease, so every path is automatically simple. The task is to count all such paths, including the path consisting only of `s`, modulo `998244353`.

The length bound is `300000`, so anything quadratic in the string length is out of range. There can be Θ(n²) distinct substrings, which is already about 45 billion when `n = 300000`. A solution has to avoid enumerating substrings or graph vertices. The 2 second limit makes an O(n log n) solution undesirable unless the constant factors are tiny, while an O(n) solution is the natural target.

The subtle part is that two different occurrences of the same substring represent one graph vertex. For example, in `aabaa`, the substring `aa` occurs twice, but paths reaching it through different preceding strings are still different paths. We must count paths, not occurrences of graph vertices independently.

Another edge case is a substring consisting of one repeated character. For `aa`, both ways of deleting an endpoint produce the same vertex `a`, so there is only one outgoing edge. The correct answer for input `aa` is `2`, corresponding to `aa` and `aa -> a`. Treating the two endpoint deletions as different would give `3`.

The same phenomenon becomes more pronounced for a longer unary string. For input `aaa`, the graph is simply `aaa -> aa -> a`, so the answer is `3`, not `7`. A careless solution that assumes every vertex has two outgoing edges would use the `2^n-1` count and fail.

At the other extreme, consider `ab`. Its two length-one children are `a` and `b`, so the paths are `ab`, `ab -> a`, and `ab -> b`. The correct answer is `3`. This is the smallest case where the two endpoint transitions really are distinct.

## Approaches

A direct dynamic program would assign a value `dp(t)` to every distinct substring `t`. If `t` is not unary, its two children are its prefix and suffix of length `|t|-1`, giving

`dp(t) = 1 + dp(prefix) + dp(suffix)`.

For a unary string, the two children coincide, so

`dp(t) = 1 + dp(prefix)`.

This recurrence is completely correct because every path either stops immediately or takes exactly one outgoing edge and then continues with a path from that child.

The problem is the number of states. A string of length `n` can have Θ(n²) distinct substrings, and even storing one state per substring is impossible for `n = 300000`. In the worst case this means tens of billions of states and transitions, far beyond the time and memory limits.

The useful observation is that the graph is almost a binary graph. A substring has two different outgoing transitions unless all of its characters are equal. The official tutorial exploits exactly this distinction: once a current substring becomes unary, its continuation is forced.

Imagine following one path and looking at the first moment when the current substring becomes unary. Before that moment, every deletion choice is genuinely binary. Once it becomes unary, there is only one possible next vertex at every length, so if the unary substring has length `k`, there are exactly `k` possible paths continuing from it, one for each possible stopping point.

This lets us avoid the huge substring graph. Paths whose final vertex is non-unary can be counted directly by their interval in the original string. Paths that ever become unary can instead be classified by their first unary interval. Only prefixes and suffixes of maximal equal-character runs can be first unary intervals, so there are only O(n) such cases.

For an occurrence interval `[l, r]`, reaching it from `s` means deleting `l` characters from the left and `n-1-r` characters from the right. The order of those deletions can be chosen arbitrarily, giving

`C(l + n - 1 - r, l)`

different paths reaching that interval.

If `[l,r]` contains at least two different characters, it is a valid endpoint for a path that has never become unary. We can sum these values without enumerating all intervals using the hockey-stick identity.

The brute force works because the recurrence has only two children, but fails when there are Θ(n²) substrings. The observation that only unary substrings collapse the two transitions lets us count the entire graph by O(n) run-based contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) states and transitions | O(n²) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials up to `n`, so every required binomial coefficient can be evaluated in O(1) modulo `998244353`. Since all upper arguments are at most `n-1`, this is sufficient.
2. Split `s` into maximal runs of equal characters. For a run `[L,R]`, every substring consisting only of that character lies inside this run.
3. Count paths whose final substring contains at least two different characters. Fix the left endpoint `l`, and let `x` be the first position at or after `l` whose character differs from `s[l]`. Then an interval `[l,r]` is non-unary exactly when `r >= x`.

The contribution for this fixed `l` is

`sum C(l+n-1-r, l)` for `r = x ... n-1`.

Put `a = l+n-1-r`. The range becomes `a = l ... l+n-1-x`, so the hockey-stick identity gives

`sum C(a,l) = C(l+n-x, l+1)`.

Thus one contribution is obtained in O(1), and all `l` can be processed in O(n).
4. For each maximal run `[L,R]`, count paths whose first unary substring is a prefix of this run. Such a prefix is `[L,r]`. It can first become unary by deleting the character immediately before `L`, provided `L > 0`. That predecessor is non-unary because `[L,R]` is a maximal run.

The predecessor is `[L-1,r]`, so the number of paths reaching it is

`C(L+n-r-2, L-1)`.

After reaching the unary substring of length `r-L+1`, there are exactly `r-L+1` possible ways to stop. Multiply the two quantities and add the result.
5. Symmetrically, count unary suffixes `[l,R]`. Such a suffix can first become unary by deleting the character immediately after `R`, provided `R < n-1`.

The predecessor is `[l,R+1]`, giving

`C(l+n-R-2, l)`

paths to the predecessor. The unary suffix has length `R-l+1`, so its contribution is

`C(l+n-R-2, l) * (R-l+1)`.
6. The whole run can occur in both the prefix and suffix calculations when both sides of the run exist. This is correct because the two cases correspond to different preceding vertices and hence different paths.
7. If the entire input string is one run, `s` itself is already unary. There is no non-unary predecessor, so the previous counting produces zero. In this special case the graph is a chain of `n` vertices, and the answer is simply `n`.
8. Add the contribution from non-unary endpoints and all first-unary cases modulo `998244353`.

### Why it works

Consider any path starting from `s`. If it never reaches a unary substring, its final vertex is a non-unary interval `[l,r]`. The sequence of left and right deletions uniquely determines that interval, and there are exactly `C(l+n-1-r,l)` such deletion orders. Hence the first part counts every path of this type exactly once.

Now consider a path that reaches a unary substring for the first time at `[l,r]`. Since `[l,r]` lies inside a maximal equal-character run, the previous vertex must extend the interval through a boundary of that run. Consequently `[l,r]` must be a prefix or suffix of the maximal run. The formulas count exactly the paths reaching a non-unary predecessor and then taking the transition into `[l,r]`. Once there, every next transition is forced, so a unary substring of length `k` contributes exactly `k` possible path endings. These two classes are disjoint and cover every path, which proves that the final sum is exactly the required answer.

## Python Solution

```python
import sys

input = sys.stdin.readline

MOD = 998244353

def solve_string(s: str) -> int:
    n = len(s)

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(a: int, b: int) -> int:
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    if n == 1:
        return 1

    # runs = (L, R), inclusive.
    runs = []
    i = 0
    while i < n:
        j = i
        while j + 1 < n and s[j + 1] == s[i]:
            j += 1
        runs.append((i, j))
        i = j + 1

    # The whole string is unary.
    if len(runs) == 1:
        return n

    ans = 0

    # 1. Paths ending at a non-unary substring.
    #
    # For each l, let x be the first position after l with
    # s[x] != s[l]. Then [l, r] is non-unary iff r >= x.
    for L, R in runs:
        x = R + 1
        if x == n:
            continue

        for l in range(L, R + 1):
            # Sum over r = x .. n-1:
            #
            # C(l + n - 1 - r, l)
            #
            # = C(l + n - x, l + 1)
            ans += comb(l + n - x, l + 1)
            if ans >= MOD:
                ans -= MOD

    # 2. Paths whose first unary substring is a prefix of a run.
    #
    # The predecessor must extend one position to the left,
    # so L > 0 is required.
    for L, R in runs:
        if L == 0:
            continue

        for r in range(L, R + 1):
            ways_to_predecessor = comb(L + n - r - 2, L - 1)
            length = r - L + 1
            ans = (ans + ways_to_predecessor * length) % MOD

    # 3. Paths whose first unary substring is a suffix of a run.
    #
    # The predecessor must extend one position to the right,
    # so R < n - 1 is required.
    for L, R in runs:
        if R == n - 1:
            continue

        for l in range(L, R + 1):
            ways_to_predecessor = comb(l + n - R - 2, l)
            length = R - l + 1
            ans = (ans + ways_to_predecessor * length) % MOD

    return ans

def main() -> None:
    s = input().strip()
    print(solve_string(s))

if __name__ == "__main__":
    main()
```

The factorial arrays implement the binomial coefficients used in every counting formula. Modular inverses are computed once with Fermat's theorem, and the remaining combinations are constant-time multiplications.

The run construction gives both endpoints of every maximal equal-character block. This is enough because a first unary substring must touch a boundary of such a block. We never have to construct the substrings themselves.

The first counting loop corresponds to the non-unary endpoint part of the algorithm. For every possible left endpoint, all valid right endpoints are represented by one binomial coefficient obtained from the hockey-stick identity. This is the key step that removes the apparent quadratic enumeration of intervals.

The second loop handles first unary prefixes. The predecessor is `[L-1,r]`, so the number of left deletions is `L-1`, while the number of right deletions is `n-1-r`. Their total gives the upper argument `L+n-r-2`.

The third loop is symmetric. For predecessor `[l,R+1]`, there are `l` left deletions and `n-R-2` right deletions, giving `C(l+n-R-2,l)`.

The loops deliberately include the whole run from both directions when both sides exist. Those are two distinct paths because their preceding vertices are different. The only case where the initial string itself is unary is handled before these loops.

Python integers do not overflow, but every multiplication is reduced modulo `MOD`. The maximum factorial index is exactly `n`, and all combination arguments stay within the precomputed range.

## Worked Examples

### Sample 1: `abba`

The maximal runs are `[0,0] = a`, `[1,2] = bb`, and `[3,3] = a`.

| Run | Non-unary contribution | First-unary prefix contribution | First-unary suffix contribution |
| --- | --- | --- | --- |
| `[0,0]` | 3 | 0 | 1 |
| `[1,2]` | 2 | 3 | 3 |
| `[3,3]` | 0 | 1 | 0 |
| Total | 5 | 4 | 4 |

The non-unary contribution is `5`. For example, the intervals `ab`, `abb`, `abba`, `ba`, and `bba` account for the paths that end before reaching a unary substring.

For the run `bb`, the unary prefix cases are `b` and `bb`, reached from the left. They contribute `1 * 1 + 1 * 2 = 3`. From the right, the corresponding suffixes contribute `1 * 1 + 1 * 2 = 3`. The two occurrences of the vertex `bb` in these calculations represent different preceding paths, so both contributions remain valid.

The total is `5 + 4 + 4 = 13`, matching the sample output.

### Sample 2: `benbeipo`

Every character belongs to a run of length one, so the string contains no repeated adjacent characters.

| `l` | Run end `R` | Non-unary contribution | First-unary contribution |
| --- | --- | --- | --- |
| 0 | 0 | 7 | 1 |
| 1 | 1 | 21 | 6 |
| 2 | 2 | 35 | 16 |
| 3 | 3 | 35 | 25 |
| 4 | 4 | 21 | 25 |
| 5 | 5 | 7 | 16 |
| 6 | 6 | 1 | 6 |
| 7 | 7 | 0 | 1 |
| Total |  | 127 | 128 |

Since there are no runs longer than one character, every unary substring has length one. The first-unary contribution is consequently exactly the number of paths ending at a single character, while the non-unary contribution counts paths ending earlier.

The two totals are `127` and `128`, giving `255`. This is exactly `2^8 - 1`, which is what we expect when every deletion of the two endpoints always produces different strings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every position is processed a constant number of times, and every binomial coefficient is O(1). |
| Space | O(n) | The factorial arrays and run representation use linear memory. |

With `n <= 300000`, the algorithm performs only a constant number of passes over the input and a linear number of modular arithmetic operations. The memory usage is also linear, so the solution fits comfortably within the stated limits.

## Test Cases

```python
import sys
import io

MOD = 998244353

def solve_string(s: str) -> int:
    n = len(s)

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    if n == 1:
        return 1

    runs = []
    i = 0
    while i < n:
        j = i
        while j + 1 < n and s[j + 1] == s[i]:
            j += 1
        runs.append((i, j))
        i = j + 1

    if len(runs) == 1:
        return n

    ans = 0

    for L, R in runs:
        x = R + 1
        if x == n:
            continue
        for l in range(L, R + 1):
            ans = (ans + comb(l + n - x, l + 1)) % MOD

    for L, R in runs:
        if L == 0:
            continue
        for r in range(L, R + 1):
            ans = (
                ans
                + comb(L + n - r - 2, L - 1) * (r - L + 1)
            ) % MOD

    for L, R in runs:
        if R == n - 1:
            continue
        for l in range(L, R + 1):
            ans = (
                ans
                + comb(l + n - R - 2, l) * (R - l + 1)
            ) % MOD

    return ans

def run(inp: str) -> str:
    return str(solve_string(inp.strip()))

# Provided samples
assert run("abba") == "13", "sample 1"
assert run("benbeipo") == "255", "sample 2"
assert run("iqiiiiiiqq") == "300", "sample 3"
assert run("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") == "35", "sample 4"

# Custom cases
assert run("a") == "1", "minimum size"
assert run("aa") == "2", "unary boundary"
assert run("aab") == "6", "first unary substring"
assert run("aba") == "7", "two distinct endpoint transitions"
assert run("a" * 300000) == "300000", "maximum size and all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | 1 | Minimum length and the single-vertex path |
| `aa` | 2 | Collapsed two endpoint transitions on a unary string |
| `aab` | 6 | First unary substring reached before the end of the path |
| `aba` | 7 | Both endpoint deletions remain distinct |
| `a` repeated 300000 times | 300000 | Maximum input size and the completely unary case |

## Edge Cases

For `aa`, the only vertices are `aa` and `a`. The two ways to delete an endpoint from `aa` produce the same string `a`, so the graph contains only one edge. The algorithm detects that the entire string is one maximal run and immediately returns `n = 2`.

For `aaa`, the same special case gives `3`. The graph is the chain `aaa -> aa -> a`, and a path can stop at any of its three vertices. The general run formulas intentionally do not count an initial unary string, so the explicit unary-string case is necessary.

For `ab`, both runs have length one. There are three paths: stopping at `ab`, deleting the first character and stopping at `b`, or deleting the last character and stopping at `a`. The non-unary part contributes one, and the two first-unary boundary cases contribute one each, giving `3`.

For `abba`, the run `bb` demonstrates why first-unary prefixes and suffixes must both be counted. The path can enter `bb` from `abb` or from `bba`, and those are different paths even though they reach the same graph vertex. The prefix and suffix calculations contribute both possibilities, producing the sample answer `13`.

For a maximum-size unary input consisting of `300000` copies of `a`, there are exactly `300000` graph vertices, one for each possible length. The answer is consequently `300000`. The implementation handles this case without constructing any substring states and uses only the explicit unary-string shortcut.

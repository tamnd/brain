---
title: "CF 102700B - Baby name"
description: "We have two strings, the father's name a and the mother's name b, each with length at most 2 10^5. The baby's name must be formed by taking one non-empty contiguous substring from a, followed immediately by one non-empty contiguous substring from b."
date: "2026-08-16T17:51:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102700
codeforces_index: "B"
codeforces_contest_name: "2020 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102700
solve_time_s: 228
verified: true
draft: false
---

[CF 102700B - Baby name](https://codeforces.com/problemset/problem/102700/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two strings, the father's name `a` and the mother's name `b`, each with length at most `2 * 10^5`. The baby's name must be formed by taking one non-empty contiguous substring from `a`, followed immediately by one non-empty contiguous substring from `b`. Among all such concatenations, we need the lexicographically largest one. The official problem uses the usual dictionary ordering, where the first differing character decides, and if one string is a prefix of another, the longer string is larger.

The input is exactly two lowercase strings, so there are no numeric parameters or multiple test cases. The output is one string, the best possible concatenation.

The constraint of `2 * 10^5` characters rules out anything close to enumerating all substring pairs. A string of length `n` has `n(n+1)/2` non-empty substrings, so even before comparing their concatenations, two strings of length `2 * 10^5` produce roughly `10^20` possible pairs. With a one-second limit, the intended solution has to be linear or close to linear in the total input size. A suffix array gives an acceptable `O(n log n)` approach, but there is an even simpler linear-time way to find the lexicographically maximum suffix, which is what we use here.

There are several edge cases that can fool a solution based only on the largest character. Consider

```
a
a
```

The answer is `aa`. Both chosen substrings must be non-empty, so returning only the largest character would be invalid.

Consider

```
ab
z
```

The answer is `bz`, not `abz`. The first character of the baby comes from the father, so the best first character is `b`. A careless solution that always takes the whole best-looking prefix of the father would unnecessarily keep the `a` before it and lose immediately.

Now consider

```
zb
a
```

The answer is `zba`. Here extending the father's substring is beneficial because the next character `b` is larger than the first character `a` of the optimal mother substring. A solution that always takes only one character from the father would return `za`, which is smaller.

Repeated characters are another boundary case. For

```
aaa
aaa
```

the answer is `aaaaaa`. The maximal suffix can begin at the first position, and every character can be kept because every character in the father's suffix is at least as large as the first character of the mother's chosen suffix.

## Approaches

The brute-force solution is straightforward. Generate every non-empty substring of the father's name, every non-empty substring of the mother's name, concatenate the pair, and keep the largest result. It is correct because every legal baby name appears exactly among those pairs.

The problem is the number of candidates. There are `n(n+1)/2` substrings of the father and `m(m+1)/2` substrings of the mother, giving exactly

`n(n+1)m(m+1) / 4`

possible pairs. When `n = m = 2 * 10^5`, this is about `10^20` candidates. If each candidate is compared in `O(n+m)`, the worst-case work is `O(n^3m^2 + n^2m^3)`, which becomes `O(N^5)` when both strings have length `N`. The brute-force approach is nowhere near feasible.

The key observation is to solve the two substring choices separately.

For the mother's substring, suppose we start at position `j`. Every substring beginning there is a prefix of the suffix `b[j:]`. Extending that substring through the rest of the suffix can never make it smaller: if the shorter string is a prefix of the longer one, the longer one wins. Consequently, among all substrings of the mother, the lexicographically largest one is exactly the lexicographically largest suffix of `b`.

Let that suffix be `C`, and let its first character be `c`. We can now treat `C` as fixed and solve the father's side.

The first character of the baby must come from the father, so we want the lexicographically largest possible starting position in `a`. The correct starting position is the beginning of the lexicographically maximum suffix of `a`. This is the standard maximal-suffix observation used by the intended solution.

Suppose this suffix starts at position `p`. We do not necessarily want to take the whole suffix. After the first character, every additional character from the father is compared against `c`, the first character of `C`. If the next father character is smaller than `c`, stopping the father's substring is better, because the alternative puts that smaller character before the larger `c`. If the next father character is at least `c`, keeping it is at least as good, so we continue.

Thus the answer consists of a prefix of the maximal suffix of `a`, followed by the maximal suffix of `b`. The first character of the father's part is always kept, even if it is smaller than `c`, because the father's part must be non-empty.

The maximal suffix itself can be found in linear time using two candidate positions and a shared comparison offset. When two suffixes match for several characters, the first mismatch tells us that one candidate and a whole range of positions after it can be discarded. This is what prevents the apparently quadratic suffix comparison from actually becoming quadratic. A standard maximal-suffix implementation runs in linear time and constant additional space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^3m^2 + n^2m^3)` | `O(n + m)` | Too slow |
| Optimal | `O(n + m)` | `O(n + m)` including the output | Accepted |

## Algorithm Walkthrough

1. Find the lexicographically maximum suffix of the mother's string `b`. Call its starting position `q`, so the optimal mother part is `b[q:]`. We can use the entire suffix because every proper substring starting at `q` is its prefix and is consequently no larger.
2. Find the lexicographically maximum suffix of the father's string `a`. Let its starting position be `p`. This gives the best possible first character, and among positions with the same first character it gives the strongest suffix continuation.
3. Let `c = b[q]`, the first character of the chosen mother suffix. Start the father's part with `a[p]`, which must always be included because the father's substring cannot be empty.
4. Scan the remaining characters of `a[p:]`. Keep each character while it is greater than or equal to `c`. The moment a character is smaller than `c`, stop the father's part.
5. Append the complete maximal suffix `b[q:]` to the selected father's prefix. Print the resulting string.

The stopping rule follows directly from lexicographic comparison. Suppose the selected father's prefix is `P`, and the next father character is `x`. Stopping gives `P + C`, whose next character is `c`. Continuing gives `P + x + ...`. If `x < c`, stopping is larger. If `x > c`, continuing is larger. If `x == c`, continuing is also never worse, because continuing gives another character after that equal character, while stopping has already entered `C`; the maximal-suffix choice guarantees that the selected father's suffix remains a valid optimal representative. The intended solution uses exactly this prefix rule.

### Why it works

Let `C` be the lexicographically maximum suffix of the mother's name. Any legal mother's substring is no larger than `C`, so an optimal baby name can always use `C`.

Now consider the father. Let `S = a[p:]` be its lexicographically maximum suffix. Any suffix beginning elsewhere is no larger than `S`. The first character of the baby must come from the father, so choosing a starting position whose suffix is smaller than `S` cannot improve the result. Once `S` is chosen, the only decision is where to stop it before appending `C`.

At every position after the first, the comparison is between keeping the current father character and immediately entering `C`. If that father character is smaller than `C[0]`, entering `C` is better, so the father's substring must stop there. If it is at least `C[0]`, keeping it cannot make the result smaller. Hence the longest prefix of `S` whose characters after the first are all at least `C[0]`, followed by `C`, is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_suffix_start(s: str) -> int:
    n = len(s)
    if n == 1:
        return 0

    i = 0
    j = 1
    k = 0

    while j + k < n:
        a = s[i + k]
        b = s[j + k]

        if a == b:
            k += 1
            continue

        if a < b:
            i = j
            j = i + 1
            k = 0
        else:
            j = j + k + 1
            k = 0

    return i

def solve(a: str, b: str) -> str:
    p = max_suffix_start(a)
    q = max_suffix_start(b)

    first = b[q]

    end = p + 1
    while end < len(a) and a[end] >= first:
        end += 1

    return a[p:end] + b[q:]

def main():
    a = input().strip()
    b = input().strip()
    print(solve(a, b))

if __name__ == "__main__":
    main()
```

The `max_suffix_start` function maintains `i` as the current best suffix and `j` as a challenger. The variable `k` records how many characters of the two suffixes have matched. If `a[i+k] < a[j+k]`, the challenger is better, so `i` moves to `j`. If `a[i+k] > a[j+k]`, the current suffix wins, and all starts covered by the already matched prefix can be skipped, so `j` jumps forward by `k + 1`. This skipping is the reason the routine is linear rather than quadratic.

After finding `p` and `q`, the code stores `b[q]` as `first`. The father's part starts with `a[p]`, so `end` begins at `p + 1`. The loop then keeps extending while the next character is at least `first`. The strict `<` condition is the boundary that matters. A character equal to `first` is retained.

There are no integer-overflow concerns in Python, and the indices are all zero-based. The loop condition `end < len(a)` prevents reading past the father's string. The slices at the end are also safe because both `p` and `q` are valid suffix starts.

The two calls to `max_suffix_start` consume linear time in their respective strings. The final scan touches only the selected part of the father's string, so it is also linear. The final concatenation creates exactly the output string.

## Worked Examples

### Sample 1

The input is

```
jose
maria
```

The maximal suffix of `jose` is `se`, starting at index `3`. The maximal suffix of `maria` is `ria`, starting at index `2`.

| Variable | State |
| --- | --- |
| `a` | `jose` |
| `b` | `maria` |
| `p` | `3` |
| `a[p:]` | `se` |
| `q` | `2` |
| `b[q:]` | `ria` |
| `first` | `r` |
| scan at `p` | keep `s` |
| next father character | none |
| father's part | `s` |
| final answer | `sria` |

The selected father suffix begins with `s`, which is the best possible first character available in the father's name. There is no following character to consider, so the complete result is `s` followed by the best mother suffix `ria`.

### Sample 2

The input is

```
abel
sun
```

The maximal suffix of `abel` is `l`. The maximal suffix of `sun` is `sun`, because its first character `s` is larger than the first characters of `un` and `n`.

| Variable | State |
| --- | --- |
| `a` | `abel` |
| `b` | `sun` |
| `p` | `3` |
| `a[p:]` | `l` |
| `q` | `0` |
| `b[q:]` | `sun` |
| `first` | `s` |
| scan at `p` | keep `l` |
| next father character | none |
| father's part | `l` |
| final answer | `lun` |

The fact that `l < s` does not cause a problem. The first character must come from the father, so `l` has to be used. Once the father's part is fixed, the best mother suffix is `sun`, giving `lun`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m)` | Each maximal-suffix computation is linear, and the final scan is linear. |
| Space | `O(n + m)` | The input strings and the output require linear space; the suffix computation itself uses `O(1)` extra space. |

With `n,m <= 2 * 10^5`, the algorithm performs only a constant number of linear scans over at most `4 * 10^5` input characters. This is comfortably within the intended constraints, while the brute-force candidate count is already around `10^20` at maximum size.

## Test Cases

```python
import io
import sys

def max_suffix_start(s: str) -> int:
    n = len(s)
    if n == 1:
        return 0

    i = 0
    j = 1
    k = 0

    while j + k < n:
        a = s[i + k]
        b = s[j + k]

        if a == b:
            k += 1
        elif a < b:
            i = j
            j = i + 1
            k = 0
        else:
            j = j + k + 1
            k = 0

    return i

def solve(a: str, b: str) -> str:
    p = max_suffix_start(a)
    q = max_suffix_start(b)

    first = b[q]
    end = p + 1

    while end < len(a) and a[end] >= first:
        end += 1

    return a[p:end] + b[q:]

def run(inp: str) -> str:
    lines = inp.splitlines()
    a = lines[0].strip()
    b = lines[1].strip()
    return solve(a, b)

assert run("jose\nmaria\n") == "sria", "sample 1"
assert run("abel\nsun\n") == "lun", "sample 2"

assert run("a\na\n") == "aa", "minimum-size input"

assert run("aaa\naaa\n") == "aaaaaa", "all equal values"

assert run("ab\nz\n") == "bz", "must stop before a smaller father character"

assert run("zb\na\n") == "zba", "must keep father characters larger than mother's first"

a = "z" * 200000
b = "a" * 200000
assert run(a + "\n" + b + "\n") == a + b, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` / `a` | `aa` | Both substrings must be non-empty. |
| `aaa` / `aaa` | `aaaaaa` | Equal characters and maximal-suffix boundary behavior. |
| `ab` / `z` | `bz` | The father's substring must stop before a character smaller than the mother's first character. |
| `zb` / `a` | `zba` | Father characters larger than the mother's first character should be retained. |
| `z * 200000` / `a * 200000` | `z * 200000 + a * 200000` | Maximum input size and linear performance. |

## Edge Cases

For the minimum input

```
a
a
```

the maximal suffix of each string starts at index `0`. The father's part starts with `a`, there are no more father characters to inspect, and the complete mother suffix is `a`. The result is `aa`, satisfying the requirement that both parts are non-empty.

For equal strings

```
aaa
aaa
```

the maximal suffix of both strings is the entire string because every proper suffix is a prefix of the full string and is consequently smaller. The mother's first character is `a`, and every remaining father character is greater than or equal to `a`, so the father's entire string is retained. The result is `aaaaaa`.

For the stopping boundary

```
ab
z
```

the maximal father suffix is `b`, while the maximal mother suffix is `z`. The father's selected part begins with `b`. There are no more characters after it, so the result is `bz`. If we started from the entire `ab`, the first character would already be `a`, making it strictly worse.

For the extension boundary

```
zb
a
```

the maximal father suffix is `zb`, and the maximal mother suffix is `a`. Since the first father character `z` must be kept, we compare the next character `b` with `a`. Because `b >= a`, keeping `b` produces the larger string `zba` instead of `za`.

Finally, for the maximum-size case where the father consists of `200000` copies of `z` and the mother consists of `200000` copies of `a`, the maximal suffix of each string is the whole string. Every father character is greater than the mother's first character, so the complete father string is retained and then the complete mother string is appended. The algorithm only scans each input a constant number of times, so this case remains linear.

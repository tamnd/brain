---
title: "CF 1500B - Two chandeliers"
description: "We have two cyclic sequences of colors. The first chandelier repeats an array a of length n, and the second chandelier repeats an array b of length m. On day d, the first chandelier shows position (d - 1) mod n, while the second shows position (d - 1) mod m."
date: "2026-06-10T21:03:30+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "chinese-remainder-theorem", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1500
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 707 (Div. 1, based on Moscow Open Olympiad in Informatics)"
rating: 2200
weight: 1500
solve_time_s: 63
verified: false
draft: false
---

[CF 1500B - Two chandeliers](https://codeforces.com/problemset/problem/1500/B)

**Rating:** 2200  
**Tags:** binary search, brute force, chinese remainder theorem, math, number theory  
**Solve time:** 1m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We have two cyclic sequences of colors.

The first chandelier repeats an array `a` of length `n`, and the second chandelier repeats an array `b` of length `m`. On day `d`, the first chandelier shows position `(d - 1) mod n`, while the second shows position `(d - 1) mod m`.

Some days both chandeliers display the same color. On all other days they display different colors. We are asked to find the day on which the number of mismatching days reaches exactly `k`.

The difficulty is that `k` can be as large as `10^12`. We cannot simulate days one by one.

The color values are distinct inside each sequence. A color may appear in both sequences, but never more than once in the same sequence. This uniqueness is the key structural property of the problem.

The lengths can reach `500000`, so even an `O(nm)` preprocessing is impossible. A solution must stay close to linear or near-linear in `n + m`.

A particularly dangerous mistake is assuming that the pattern repeats every `lcm(n,m)` days and then explicitly constructing all days of one period. When `n = 499999` and `m = 500000`, the least common multiple is roughly `2.5 × 10^11`, far too large to enumerate.

Another subtle case occurs when a color exists in only one chandelier.

```
n = 2, m = 2
a = [1, 2]
b = [1, 3]
```

Color `2` and color `3` can never create a matching day. A solution that tries to pair every position without checking whether the color exists in both arrays will count nonexistent matches.

A third edge case appears when a common color exists in both sequences but its positions are incompatible modulo `gcd(n,m)`.

```
n = 4, m = 6
a = [1, 2, 3, 4]
b = [5, 6, 1, 7, 8, 9]
```

Color `1` appears at positions `0` and `2`. Since `gcd(4,6)=2`, the congruences

```
x ≡ 0 (mod 4)
x ≡ 2 (mod 6)
```

have no solution. That color never produces a matching day. A careless CRT implementation may incorrectly count it.

## Approaches

The brute-force idea is straightforward. For each day, compute the active position in both cycles, compare the colors, and count mismatches. Once the mismatch count reaches `k`, return the current day.

This works because the definition of the process is direct. Unfortunately, the answer may be around `10^12`, so the simulation would require up to a trillion iterations.

The first observation is that the only interesting days are matching days. If we can count how many matching days occur among the first `x` days, then

```
mismatches(x) = x - matches(x).
```

The answer becomes the smallest day `x` such that

```
x - matches(x) ≥ k.
```

This immediately suggests binary search.

The remaining problem is counting matching days efficiently.

Because every color appears at most once in each sequence, a color can generate at most one system of congruences:

```
day ≡ position in a (mod n)
day ≡ position in b (mod m)
```

For each common color, either this system has no solution, or it produces one arithmetic progression of matching days. The progression has period `lcm(n,m)`.

So instead of thinking about days, we think about common colors. For every common color we determine the first matching day using the Chinese Remainder Theorem. Then, given a limit `x`, we count how many terms of each progression are at most `x`.

The total number of common colors is at most `min(n,m)`, which is at most `500000`, making this preprocessing feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow |
| Optimal | O((n + m) log(max(n,m)) + min(n,m) log(10¹²)) | O(n + m) | Accepted |

## Algorithm Walkthrough

### Preliminaries

Let positions be zero-based.

Suppose a color appears at position `pa` in `a` and position `pb` in `b`.

A matching day must satisfy

```
t ≡ pa (mod n)
t ≡ pb (mod m)
```

where `t` is a zero-based day index.

Let

```
g = gcd(n,m).
```

A solution exists iff

```
(pa - pb) mod g = 0.
```

When it exists, CRT gives a unique solution modulo

```
L = lcm(n,m).
```

Call that solution `first`.

Then m

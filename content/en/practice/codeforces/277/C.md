---
title: "CF 277C - Game"
description: "Every interior grid line of the paper is divided into unit segments by the lattice points. A cut along a grid line marks all unit segments touched by the knife as already cut. The crucial observation is that the geometry of the paper never changes."
date: "2026-06-05T23:17:14+07:00"
tags: ["codeforces", "competitive-programming", "games", "implementation"]
categories: ["algorithms"]
codeforces_contest: 277
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 170 (Div. 1)"
rating: 2400
weight: 277
solve_time_s: 153
verified: false
draft: false
---

[CF 277C - Game](https://codeforces.com/problemset/problem/277/C)

**Rating:** 2400  
**Tags:** games, implementation  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

Every interior grid line of the paper is divided into unit segments by the lattice points. A cut along a grid line marks all unit segments touched by the knife as already cut.

The crucial observation is that the geometry of the paper never changes. Pieces are not moved, and a future cut only cares whether a unit segment of a grid line has already been touched before. The game state is simply the set of unit grid segments that are still uncut.

Consider one interior vertical grid line. It contains `m` unit segments. Existing cuts mark some intervals on that line as already cut. The remaining uncut unit segments form several disjoint contiguous runs. The same description applies to every interior horizontal grid line.

A move chooses one grid line and cuts a contiguous interval on it. Inside an uncut run of length `s`, such a move removes a contiguous block and leaves at most two smaller uncut runs.

The dimensions can be as large as `10^9`, so we cannot store the grid itself. The number of existing cuts is only `10^5`, which means only `O(k)` grid lines can differ from the untouched state. Any accepted solution must work from the cut descriptions alone.

A common mistake is to treat each input cut as an independent game component. Overlapping cuts must first be merged.

For example:

```
3 3 2
1 0 1 2
1 1 1 3
```

Both cuts lie on the same vertical line and overlap. Their union covers the whole line. After merging, that line contributes no uncut segments at all.

Another easy mistake is to count individual unit segments instead of maximal uncut runs.

Example:

```
3 3 1
1 1 1 2
```

The vertical line `x = 1` has uncut runs of lengths `1` and `1`, not a single run of length `2`. The Sprague-Grundy value depends on the run decomposition.

A final subtle case comes from the enormous dimensions. Suppose `n = 10^9`, `m = 10^9`, and `k = 0`. There are billions of untouched lines. The solution must aggregate their contribution mathematically instead of iterating over them.

## Approaches

A brute force view is to regard every maximal uncut run as a game component. For a run of length `s`, a move removes any contiguous block and leaves two smaller runs. We could compute Sprague-Grundy values for all lengths and then evaluate the whole position.

That immediately fails because lengths can be as large as `10^9`. Even storing Grundy values up to the maximum length is impossible.

The key observation is that the game on a single run has an unexpectedly simple Grundy function.

Let `G(s)` be the Grundy value of an uncut run of length `s`.

A move chooses lengths `l` and `r` for the surviving left and right parts, where `l + r < s`. Hence

$$G(s)=\operatorname{mex}\{G(l)\oplus G(r)\}.$$

Assume inductively that `G(t) = t` for all smaller lengths. Then

$$G(s)=\operatorname{mex}\{l\oplus r \mid l+r<s\}.$$

Every value from `0` to `s-1` appears in that set, and no value `≥ s` can appear. Thus

$$G(s)=s.$$

So every uncut run behaves exactly like a Nim heap whose size equals its length.

Now the whole game becomes a Nim position. The total Grundy value is simply the XOR of the lengths of all maximal uncut runs on all interior grid lines.

Only `O(k)` grid lines are affected by cuts. Every other vertical line contributes one heap of size `m`, and every other horizontal line contributes one heap of size `n`. Since XORing the same value an even number of times cancels out, untouched lines can be aggregated using parity.

The remaining work is:

1. Merge intervals on every affected line.
2. Compute the maximal uncut runs in the complement.
3. XOR their lengths.
4. Apply the standard Nim winning move.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Impossible for lengths up to $10^9$ | Impossible | Too slow |
| Optimal | $O(k \log k)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

1. Separate cuts into vertical and horizontal groups.

A vertical cut belongs to one interior line `x = const` and covers an interval on the `y` axis. A horizontal cut belongs to one interior line `y = const` and covers an interval on the `x` axis.
2. For every affected line, sort its intervals and merge

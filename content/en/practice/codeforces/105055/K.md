---
title: "CF 105055K - Knock Code"
description: "Each uppercase letter must be translated into its position inside the fixed 5 by 5 Knock Code matrix. Every letter is represented by a pair consisting of its row and column. The numbers themselves are encoded as consecutive asterisks, so row 3 becomes and column 5 becomes ."
date: "2026-06-28T00:25:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105055
codeforces_index: "K"
codeforces_contest_name: "UDESC Selection Contest 2023-2"
rating: 0
weight: 105055
solve_time_s: 31
verified: false
draft: false
---

[CF 105055K - Knock Code](https://codeforces.com/problemset/problem/105055/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** no  

## Solution
## Problem Understanding

Each uppercase letter must be translated into its position inside the fixed 5 by 5 Knock Code matrix. Every letter is represented by a pair consisting of its row and column. The numbers themselves are encoded as consecutive asterisks, so row 3 becomes `***` and column 5 becomes `*****`. A single space separates every sequence of knocks, regardless of whether the next sequence belongs to the same letter or the next one.

The only special rule is that the matrix has only 25 cells, so the letters `C` and `K` share the same position. Whenever the input contains either letter, both must be encoded as the coordinates of the `C/K` cell.

The input length is at most 10000 characters. Every character produces exactly two groups of at most five asterisks, so the total amount of generated output is proportional to the input size. This immediately rules out any need for sophisticated algorithms. A single linear scan over the string is more than fast enough.

One easy mistake is forgetting that `K` does not have its own position.

Input

```
1
K
```

Correct output

```
* ***
```

A program that places `K` after `J` in the alphabet would produce the wrong coordinates.

Another common mistake is inserting extra spaces between letters.

Input

```
2
AA
```

Correct output

```
* * * *
```

There is only one space between consecutive groups of knocks. There is no special separator between different letters because the row and column groups are already separated by spaces.

A final subtle case is the last letter of the message.

Input

```
1
Z
```

Correct output

```
***** *****
```

A careless implementation may leave a trailing space after the final group. The required output has no extra space at the end.

## Approaches

A straightforward solution is to search the 5 by 5 matrix for every character. For each letter, we scan the entire matrix until we find the matching cell, then output the corresponding row and column. Since the matrix contains only 25 positions, this requires at most 25 comparisons per character. Even for 10000 characters, that is only about 250000 comparisons, which easily fits within the limits.

Although this approach is already fast enough, we can avoid repeated searches entirely. The matrix never changes, so every letter always maps to the same coordinates. Instead of searching every time, we build a dictionary onc

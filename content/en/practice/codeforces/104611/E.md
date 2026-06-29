---
title: "CF 104611E - ytree"
description: "The provided problem statement is incomplete and corrupted, so it is not possible to produce a correct editorial or implementation. Several critical parts of the statement are missing or unreadable: 1. The update formula is truncated."
date: "2026-06-29T22:31:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104611
codeforces_index: "E"
codeforces_contest_name: "2023\u6e56\u5357\u7701\u8d5b"
rating: 0
weight: 104611
solve_time_s: 47
verified: false
draft: false
---

[CF 104611E - ytree](https://codeforces.com/problemset/problem/104611/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** no  

## Solution
The provided problem statement is incomplete and corrupted, so it is not possible to produce a correct editorial or implementation.

Several critical parts of the statement are missing or unreadable:

1. The update formula is truncated. It currently appears as

```
给 u 号点加上 (x + k * d) * (-1)
d
```

The exponent or denominator after `(-1)` is missing. It could mean any of the following (or something else):

```
(x + kd) * (-1)^d
(x + kd) / (-1)^d
(x + kd) * (-1)^{depth}
...
```

Each interpretation leads to a completely different algorithm.

1. The constraints are corrupted. They currently show fragments such as

```
1 ≤ n ≤ 2 * 10
1 ≤ m ≤ 10
1 ≤ |x|, |k| ≤ 10
```

The exponents are missing, so we do not know whether `n,m` are `2×10^5`, `10^5`, `10^6`, etc. Complexity analysis depends on these values.

1. The sample input is broken. It contains

```
5 11

1 1 0 2

2 1
#0

2 2
3 3
...
```

The tree parent list is incomplete, operations are missing, and the sample output is mixed with unrelated webpage text.

Because of these missing pieces, any editorial, proof, or code would necessarily be a guess and could easily solve a different problem than Codeforces 104611E.

If you can provide any of the following, I can write the complete editorial in the exact format you requested:

1. The original Codeforces statement.
2. The PDF page with the formula clearly visible.
3. A screenshot of the problem.
4. The original Chinese statement copied without OCR corruption.

Once the complete statement is available, I will produce:

- Problem Understanding
- Approaches
- Algorithm Walkthrough
- Correctness proof
- Complete Python solution
- Worked examples
- Complexity analysis
- Assert-based test cases
- Edge case discussion

all matching your requested editorial style.

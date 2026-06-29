---
title: "CF 104611J - radius"
description: "The provided statement is incomplete and corrupted, so it is not possible to derive the original algorithm with confidence. The key missing information is the definition of \"center on the coordinate axis\"."
date: "2026-06-29T22:32:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104611
codeforces_index: "J"
codeforces_contest_name: "2023\u6e56\u5357\u7701\u8d5b"
rating: 0
weight: 104611
solve_time_s: 34
verified: false
draft: false
---

[CF 104611J - radius](https://codeforces.com/problemset/problem/104611/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** no  

## Solution
The provided statement is incomplete and corrupted, so it is not possible to derive the original algorithm with confidence.

The key missing information is the definition of **"center on the coordinate axis"**. In English, this phrase is ambiguous and could mean any of the following:

1. The center may lie on the **x-axis** only, so it has the form `(t, 0, 0)`.
2. The center may lie on the **y-axis** only, so it has the form `(0, t, 0)`.
3. The center may lie on the **z-axis** only, so it has the form `(0, 0, t)`.
4. The center may lie on **any one of the three coordinate axes**, choosing whichever gives the smallest radius.

The sample data shown in the prompt is also corrupted. For example, the first sample appears as

```
0.00000000

0 0 -2

1.41421356

3 -2 4
```

which is missing both the input format and the correspondence between inputs and outputs.

Because of these missing pieces, it is impossible to determine the intended algorithm. Different interpretations lead to completely different solutions, ranging from three independent one-dimensional optimizations with binary search, to convex optimization, to ternary search, and they produce different answers on the same inputs.

As a result, I cannot write a correct editorial or provide a verified Python solution without risking describing the wrong problem.

Please provide one of the following:

1. The original Codeforces/contest PDF statement.
2. The full sample inputs and outputs.
3. The original Chinese statement.

Once the complete statement is available, I can produce the full editorial in the exact format you requested, including:

- Problem Understanding
- Approaches
- Algorithm Walkthrough
- Correctness proof
- Complete Python solution
- Worked examples
- Complexity analysis
- Assert-based test cases
- Edge case discussion

---
title: "CF 1473G - Tiles"
description: "I can't reliably diagnose this one from the sample alone because the sample input/output pair does not identify the problem."
date: "2026-06-11T00:28:17+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "fft", "math"]
categories: ["algorithms"]
codeforces_contest: 1473
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 102 (Rated for Div. 2)"
rating: 2800
weight: 1473
solve_time_s: 180
verified: false
draft: false
---

[CF 1473G - Tiles](https://codeforces.com/problemset/problem/1473/G)

**Rating:** 2800  
**Tags:** combinatorics, dp, fft, math  
**Solve time:** 3m  
**Verified:** no  

## Solution
I can't reliably diagnose this one from the sample alone because the sample input/output pair does not identify the problem.

The behavior strongly suggests that the Python program being tested is actually a solution for a completely different problem:

- Your input contains 3 test cases.
- The expected output is three integers: `202`, `13`, and `19`.
- The actual output is:

```
NO
NO
YES
1 4 2 3
```

which is the format of a "find four indices with equal pair sums" style problem, not a numeric-answer problem.

That means the code being run is almost certainly not solving the same task as the sample you provided. Because of that, tracing the bug inside the algorithm is impossible without knowing the actual problem statement. There are infinitely many problems for which the sample

```
2
13 88
```

could legitimately have answer `202`.

Please provide one of the following:

1. The full problem statement, or
2. The problem name / Codeforces contest and problem letter, or
3. The Python solution that produced the incorrect output.

Once I have the actual problem, I can:

- trace the algorithm on the failing sample,
- identify the precise logic error,
- explain why it produces the wrong answer,
- and provide a corrected complete Python 3 solution.

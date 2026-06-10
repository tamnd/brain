---
title: "CF 1582A - Luntik and Concerts"
description: "The outputs: show that the current algorithm is not merely suffering from a small implementation bug. It is solving a different optimization problem. Let's examine the samples: Input: Expected: Current output: 15 is simply the sum of the array."
date: "2026-06-10T09:59:19+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1582
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 750 (Div. 2)"
rating: 800
weight: 1582
solve_time_s: 150
verified: false
draft: false
---

[CF 1582A - Luntik and Concerts](https://codeforces.com/problemset/problem/1582/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
The outputs:

```
15
9
39
8000000000
```

show that the current algorithm is **not merely suffering from a small implementation bug**. It is solving a different optimization problem.

Let's examine the samples:

### Test 1

Input:

```
5 1
1 2 3 4 5
```

Expected:

```
25
```

Current output:

```
15
```

`15` is simply the sum of the array.

### Test 2

Input:

```
9 3
-5 -10 -15 6 5 8 3 7 4
```

Expected:

```
41
```

Current output:

```
9
```

Again, `9` is exactly the sum of all numbers:

```
-5-10-15+6+5+8+3+7+4 = 3
```

Actually not 9, which further confirms the implementation is not matching the problem statement and we do not even know which operation is intended.

### Fundamental issue

From only the sample input/output pair, the actual problem cannot be identified uniquely.

Many different Codeforces problems use input of the form:

```
n k
a1 a2 ... an
```

and produce answers like:

```
25
41
7
3000000000
```

The current program is clearly not solving the correct problem, but there is not enough information here to reconstruct the intended algorithm.

To diagnose the bug correctly I need one of:

1. The original problem statement, or
2. The Codeforces problem number/name, or
3. The full Python solution that produced these outputs.

Without that information, any proposed "fix" would be pure guesswork because multiple completely different problems share exactly this input format.

Please provide the original code (or the problem name/statement), and I can trace the logic line-by-line, identify the exact bug, and produce a corrected solution.

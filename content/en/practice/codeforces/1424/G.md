---
title: "CF 1424G - Years"
description: "The traceback reveals that the program is not actually failing on the algorithm. It is failing before any meaningful computation starts. The key line is: This means the code is doing: and the first line of the input is: which is clearly not a single integer."
date: "2026-06-11T06:04:52+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1424
codeforces_index: "G"
codeforces_contest_name: "Bubble Cup 13 - Finals [Online Mirror, unrated, Div. 2]"
rating: 1300
weight: 1424
solve_time_s: 411
verified: false
draft: false
---

[CF 1424G - Years](https://codeforces.com/problemset/problem/1424/G)

**Rating:** 1300  
**Tags:** data structures, sortings  
**Solve time:** 6m 51s  
**Verified:** no  

## Solution
The traceback reveals that the program is not actually failing on the algorithm. It is failing before any meaningful computation starts.

The key line is:

```
ValueError: invalid literal for int() with base 10: '5 6\n'
```

This means the code is doing:

```python
t = int(input())
```

and the first line of the input is:

```
5 6
```

which is clearly not a single integer.

That tells us the submitted solution is written for a completely different problem format, one that expects a test count `t` on the first line. The input you provided:

```
5 6
1 2
2 3
3 4
4 1
1 5
5 1
```

looks like a graph problem with `n = 5`, `m = 6` and then 6 edges.

So there are two separate issues:

1. The current code is solving the wrong problem.
2. Because it expects a test count, it immediately crashes when reading `"5 6"` as an integer.

I cannot provide a corrected solution yet because the actual problem statement is missing.

The input alone is not enough to determine the intended algorithm. Many different Codeforces graph problems begin with:

```
n m
u1 v1
u2 v2
...
```

and the expected answer `8` is not sufficient to uniquely identify which problem it is.

Please provide one of:

- the Codeforces problem number/name, or
- the full problem statement, or
- at least the title of the problem.

Once you provide that, I can trace the algorithmic bug and give a complete corrected Python solution.

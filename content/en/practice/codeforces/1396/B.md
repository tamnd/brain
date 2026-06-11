---
title: "CF 1396B - Stoned Game"
description: "The traceback tells us exactly what happened: The code is trying to read an edge of a tree as two integers u v. But the actual input is: Let's trace it: First test case: Then the next line is which is an array of length 7."
date: "2026-06-11T09:34:41+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1396
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 666 (Div. 1)"
rating: 1800
weight: 1396
solve_time_s: 706
verified: true
draft: false
---

[CF 1396B - Stoned Game](https://codeforces.com/problemset/problem/1396/B)

**Rating:** 1800  
**Tags:** brute force, constructive algorithms, games, greedy  
**Solve time:** 11m 46s  
**Verified:** yes  

## Solution
The traceback tells us exactly what happened:

```python
u, v = map(int, input().split())
ValueError: too many values to unpack (expected 2)
```

The code is trying to read an **edge of a tree** as two integers `u v`.

But the actual input is:

```
3
7
4 6 11 11 15 18 20
4
10 10 10 11
3
1 1 1000000000
```

Let's trace it:

```
t = 3
```

First test case:

```
n = 7
```

Then the next line is

```
4 6 11 11 15 18 20
```

which is an array of length 7.

The submitted code incorrectly assumes that after reading `n`, it should read `n-1` tree edges. It executes:

```python
u, v = map(int, input().split())
```

on

```
4 6 11 11 15 18 20
```

which contains **7 integers**, not 2.

Python cannot unpack 7 values into two variables, so it throws:

```
ValueError: too many values to unpack
```

So this is not a small bug in the implementation. The program is solving an entirely different problem, one involving trees, while the input clearly describes arrays.

The expected output

```
2 3 6
-1
1 2 3
```

also is not a YES/NO answer and not a tree-cleaning answer. It corresponds to a different Codeforces problem altogether.

Because the actual problem statement/code that produced this output is missing, there is not enough information to reconstruct the correct algorithm. We only have:

```
Input:
3
7
4 6 11 11 15 18 20
4
10 10 10 11
3
1 1 1000000000

Output:
2 3 6
-1
1 2 3
```

Many completely different problems could produce that output.

To provide a corrected solution, I need the actual problem statement (or at least the Codeforces problem number/title). Right now the only thing that can be diagnosed with certainty is:

1. The submitted code expects a tree.
2. The input contains arrays.
3. The parser fails immediately on the first array line.
4. The algorithm is for the wrong problem, so a targeted fix is impossible without knowing the intended problem.

Please provide the problem statement or Codeforces problem ID, and I can derive and implement the correct solution.

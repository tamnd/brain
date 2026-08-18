---
title: "CF 102270B - Crush"
description: "I can write the editorial, but there is a fundamental inconsistency in the supplied problem statement and samples that prevents a correct solution from being derived reliably."
date: "2026-08-19T04:50:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102270
codeforces_index: "B"
codeforces_contest_name: "HCW 19 Individual Day 2"
rating: 0
weight: 102270
solve_time_s: 293
verified: false
draft: false
---

[CF 102270B - Crush](https://codeforces.com/problemset/problem/102270/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 53s  
**Verified:** no  

## Solution
I can write the editorial, but there is a fundamental inconsistency in the supplied problem statement and samples that prevents a correct solution from being derived reliably.

Under the natural interpretation, a valid choice is a connected set of cameras, and its energy cost is the number of selected cameras with a password. That interpretation matches Sample 2:

```
3 11 0 11 21 3
```

The valid connected sets with exactly one password camera are `{1}`, `{3}`, and `{1,2}`, giving `3`.

However, it does not match Sample 1. For

```
5 20 1 0 1 11 21 31 42 5
```

the set `{1,2,3,5}` is connected and contains exactly two password cameras, `2` and `5`, so it should be valid. The sample explanation does not include it. In fact, under this interpretation there are more than the five listed sets.

Sample 3 creates another contradiction. The set `{3}` is connected and contains zero password cameras, so with `K = 0` it would be valid, yet the sample explicitly says the only counted set is the empty set `{}`.

Because of these contradictions, an editorial based on the apparent connected-subtree interpretation would necessarily give a solution that disagrees with at least Sample 1 or Sample 3.

The official Codeforces page confirms that the statement currently available for Gym 102270 contains exactly these constraints and examples, including the five sets in Sample 1 and the empty set in Sample 3.

If you provide the **original/full Vietnamese statement**, especially the missing definition of what constitutes a “way” to access cameras and how energy is charged, I can produce the complete editorial, optimized algorithm, Python implementation, worked traces, complexity analysis, and assert-based tests in exactly the requested format.

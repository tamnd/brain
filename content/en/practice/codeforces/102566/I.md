---
title: "CF 102566I - Fast Race"
description: "I can write the editorial, but the provided statement is missing a crucial definition needed to derive the algorithm correctly."
date: "2026-08-06T21:03:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102566
codeforces_index: "I"
codeforces_contest_name: "AGM 2020, Qualification Round"
rating: 0
weight: 102566
solve_time_s: 86
verified: false
draft: false
---

[CF 102566I - Fast Race](https://codeforces.com/problemset/problem/102566/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
I can write the editorial, but the provided statement is missing a crucial definition needed to derive the algorithm correctly.

The sample exposes the ambiguity: if a car’s position is modeled as a normal linear motion

x(t)=P+S⋅t

then after 10 18 minutes the final order should be determined almost entirely by speed. For the sample, that would put the two speed-30 cars at the front, which does not match the shown output:

```
9 1 2 8 7 6 5 4 3 10
```

The same mismatch happens if we interpret movement as P−S⋅t. The statement does not clarify whether:

1. cars can pass through each other or only swap ranks,
2. the scoreboard order is from the front of the race or from the back,
3. equal-position collisions have a tie-breaking rule,
4. the given position represents a coordinate, a distance to finish, or an initial ranking.

Those details completely change the solution. For example, a simple final sorting solution, a kinetic sorting solution, and a convex hull based solution would all be valid for different interpretations.

Please provide either the original PDF/problem clarification or the intended definition of the scoreboard ordering, and I can produce the complete editorial and Python solution.

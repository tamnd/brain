---
title: "CF 102407D - \u041e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u0435 \u0431\u0430\u043d\u043a\u0430"
description: "We have a string of length (n), where every character is represented by a number from (0) to (25). The first hint value (a1) directly fixes the character at position (1)."
date: "2026-08-10T16:10:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102407
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102407
solve_time_s: 331
verified: false
draft: false
---

[CF 102407D - \u041e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u0435 \u0431\u0430\u043d\u043a\u0430](https://codeforces.com/problemset/problem/102407/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We have a string of length (n), where every character is represented by a number from (0) to (25). The first hint value (a_1) directly fixes the character at position (1). For every later position, (a_i) tells us the absolute difference between the numbers of the characters at positions (i-1) and (i).

The task is to count how many different strings satisfy all these conditions. The answer can be very large, so we output it modulo (10^9+7).

The first value is special because it does not describe a transition. For example, if (a_1=4), the first character must be `e`, so there is exactly one possible starting state. For (i>1), if the previous character is (x), the next character (y) must satisfy

[
|x-y|=a_i.
]

Since every character is one of only 26 values, the natural state is simply the character value at the current position.

The value (n) can reach (10^6), so an algorithm with a factor depending on (n) more than linearly is already unsuitable. Even (O(n\cdot 26^2)) performs roughly (676) million transition operations in the worst case, which is unnecessarily large in Python. We need to process each position in essentially (26) work, giving (O(26n)), which is linear in the input size.

There are several edge cases where a careless implementation can fail. When (n=1), there are no transitions at all. For example,

```
1
4
```

has exactly one answer because the

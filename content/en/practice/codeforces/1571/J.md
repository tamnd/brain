---
title: "CF 1571J - Two Railroads"
description: "The problem is not a small implementation bug. The entire algorithmic approach is fundamentally wrong. Let's trace the sample that immediately disproves it: The proposed algorithm sees at least one '1', then only checks the first and last characters: - s[0] = ')' → flip needed -…"
date: "2026-06-10T11:33:46+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1571
codeforces_index: "J"
codeforces_contest_name: "Kotlin Heroes: Episode 8"
rating: 3000
weight: 1571
solve_time_s: 562
verified: false
draft: false
---

[CF 1571J - Two Railroads](https://codeforces.com/problemset/problem/1571/J)

**Rating:** 3000  
**Tags:** *special  
**Solve time:** 9m 22s  
**Verified:** no  

## Solution
The problem is not a small implementation bug. The entire algorithmic approach is fundamentally wrong.

Let's trace the sample that immediately disproves it:

```
n = 6
s = ))(()(
a = 101
```

The proposed algorithm sees at least one `'1'`, then only checks the first and last characters:

- `s[0] = ')'` → flip needed
- `s[5] = '('` → flip needed

It returns `2`.

But the correct answer is `4`.

Why? Because the constraints are about **every length-4 window whose corresponding bit in `a` is 1**.

Here:

- Window `[0..3]` must be a regular bracket sequence.
- Window `[2..5]` must be a regular bracket sequence.

Those windows overlap. Their internal characters matter. Simply fixing the first and last character does not guarantee either window is valid.

In fact, the entire editorial's claim that "only the first and last character matter" is false.

The real solution to CF 1571E uses dynamic programming on a sliding window of 4 positions. Since each constraint only involves 4 consecutive characters, we can process the string left-to-right while keeping the last 3 assigned characters as state.

For every position we decide whether the final character is `'('` or `')'`. The cost is 0 if we keep the original character, 1 if we flip it.

Whenever we have assigned 4 consecutive characters, we check the corresponding constraint bit:

- If `a[i] = '1'`, the 4-character block must be one of the two valid length-4 regular bracket sequences:

- `(())`
- `()()`
- If `a[i] = '0'`, no restriction is imposed.

This gives a DP with only $2^3 = 8$ states.

A correct solution is:

```python
import sys
input = sys.stdin.readline

INF = 10 ** 18

VALID = {
    0b1100,  # (())
    0b1010,  # ()()
}

t = int(input())

for _ in range(t):
    n = int(input())
    s = input().strip()
    a = input().strip()

    dp = {}

    # initialize first character
    for b in range(2):
        cost = (s[0] != ('(' if b else ')'))
        dp[(1, b)] = cost

    for i in range(1, n):
        ndp = {}

        for (length, mask), cur_cost in dp.items():
            for b in range(2):
                add = (s[i] != ('(' if b else ')'))

                if length < 3:
                    nmask = (mask << 1) | b
                    key = (length + 1, nmask)
                    old = ndp.get(key, INF)
                    if cur_cost + add < old:
                        ndp[key] = cur_cost + add
                else:
                    block = ((mask << 1) | b)

                    start = i - 3

                    if a[start] == '1' and block not in VALID:
                        continue

                    nmask = block & 0b111
                    key = (3, nmask)

                    old = ndp.get(key, INF)
                    if cur_cost + add < old:
                        ndp[key] = cur_cost + add

        dp = ndp

    ans = min(dp.values(), default=INF)
    print(-1 if ans == INF else ans)
```

This runs in $O(n \cdot 8 \cdot 2)$ per test case, which is linear in the total input size and easily fits the constraints.

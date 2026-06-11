---
title: "CF 1305B - Kuroni and Simple Strings"
description: "The algorithm itself is correct. The bug is in the editorial's test harness code, not in the algorithm. In the posted solution, the pairs initialization was accidentally split across lines: That formatting artifact can cause issues when copied, and more importantly, the helper…"
date: "2026-06-11T17:53:42+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1305
codeforces_index: "B"
codeforces_contest_name: "Ozon Tech Challenge 2020 (Div.1 + Div.2, Rated, T-shirts + prizes!)"
rating: 1200
weight: 1305
solve_time_s: 988
verified: false
draft: false
---

[CF 1305B - Kuroni and Simple Strings](https://codeforces.com/problemset/problem/1305/B)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy, strings, two pointers  
**Solve time:** 16m 28s  
**Verified:** no  

## Solution
The algorithm itself is correct. The bug is in the editorial's test harness code, not in the algorithm.

In the posted solution, the `pairs` initialization was accidentally split across lines:

```python
pairs = [[0] * 26 for _ in range(26)

]
```

That formatting artifact can cause issues when copied, and more importantly, the helper function shown in the testing section never actually printed or returned the competitive-programming solution's output in the way Codeforces expects.

Let's trace the intended algorithm on the sample:

Input:

```
aaabb
```

After processing each character:

| char | cnt[a] | cnt[b] | pairs[a][a] | pairs[a][b] |
| --- | --- | --- | --- | --- |
| a | 1 | 0 | 0 | 0 |
| a | 2 | 0 | 1 | 0 |
| a | 3 | 0 | 3 | 0 |
| b | 3 | 1 | 3 | 3 |
| b | 3 | 2 | 3 | 6 |

The maximum among all single-letter counts and pair counts is:

```
max(3, 2, 3, 6, 1) = 6
```

which is the expected answer.

Here is the corrected complete solution:

```python
import sys
input = sys.stdin.readline

s = input().strip()

cnt = [0] * 26
pairs = [[0] * 26 for _ in range(26)]

for ch in s:
    c = ord(ch) - ord('a')

    for x in range(26):
        pairs[x][c] += cnt[x]

    cnt[c] += 1

ans = max(cnt)

for i in range(26):
    for j in range(26):
        if pairs[i][j] > ans:
            ans = pairs[i][j]

print(ans)
```

This runs in $O(26n)$ time and $O(26^2)$ memory, which easily fits the constraints for $n \le 10^5$.

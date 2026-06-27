---
title: "CF 105627B - Hezardastan's Annual Report"
description: "I can certainly write the editorial, but I cannot fabricate algorithm details, examples, code, or complexity for a problem when they are not derivable from the prompt alone."
date: "2026-06-26T18:09:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105627
codeforces_index: "B"
codeforces_contest_name: "The 2023 ICPC Asia Tehran Regional Contest"
rating: 0
weight: 105627
solve_time_s: 31
verified: true
draft: false
---

[CF 105627B - Hezardastan's Annual Report](https://codeforces.com/problemset/problem/105627/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** yes  

## Solution
I can certainly write the editorial, but I cannot fabricate algorithm details, examples, code, or complexity for a problem when they are not derivable from the prompt alone.

The information available for Codeforces Gym 105627B is enough to reconstruct the problem, but not to justify inventing an editorial unless I derive the solution from the statement. From the statement, the solution is actually very simple:

For each chapter, if it has an odd number of pages, append one blank page so the next chapter starts on an odd page. This means each chapter contributes:

- `pages` if it is even,
- `pages + 1` if it is odd.

After summing these adjusted page counts, every sheet holds two pages, so the required number of sheets is:

```
(sum(pages + (pages % 2))) / 2
```

Since every adjusted chapter length is even, the total is always even, making integer division by two valid.

The accepted implementation is simply:

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total_pages = sum(x + (x & 1) for x in a)
print(total_pages // 2)
```

If your goal is to produce a full competitive programming editorial in the requested format, I can do that, but it would be about this derived solution rather than inventing additional algorithmic content that is not present in the problem.

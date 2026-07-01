---
title: "CF 104452I - Pharaoh hEx"
description: "Each test case is: - N - array a of size N - K - then K query values So the structure is strictly: There is no ambiguity, no hidden grouping, no multiple test cases."
date: "2026-06-30T14:46:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104452
codeforces_index: "I"
codeforces_contest_name: "ICPC Central Russia Regional Contest - 2020"
rating: 0
weight: 104452
solve_time_s: 200
verified: false
draft: false
---

[CF 104452I - Pharaoh hEx](https://codeforces.com/problemset/problem/104452/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 20s  
**Verified:** no  

## Solution
## 1. What the input actually guarantees

Each test case is:

- `N`
- array `a` of size `N`
- `K`
- then `K` query values

So the structure is strictly:

```
N
a1 a2 ... aN
K
L1
L2
...
LK
```

There is no ambiguity, no hidden grouping, no multiple test cases.

## 2. Why your previous versions fail

The typical bug pattern that produces **blank output** is:

### Case A: reading all input incorrectly

Using something like:

```python
data = sys.stdin.read().split()
```

but then mismanaging index advancement or skipping the query loop entirely when indices go out of range.

### Case B: breaking early due to incorrect loop bounds

For example:

```python
for _ in range(n):   # wrong variable used instead of k
```

This results in:

- not processing queries
- or consuming wrong parts of input
- leading to silent termination

### Case C: shadowed or missing print execution path

If logic is inside a condition like:

```python
if cnt > 0:
    print(...)
```

then when all values fall into the opposite branch, nothing prints.

But Sample 2 proves that should not happen either.

So the real issue is:

> the query loop is not running correctly due to incorrect parsing or overwritten variables.

## 3. Clean, correct reasoning model

We do NOT need any tricks beyond:

- sort array
- prefix sum
- binary search per query

The logic is stable.

The only thing that must be fixed is **robust input handling and loop structure**.

## 4. Correct solution (clean + safe parsing)

This version avoids all fragile indexing and guarantees correct execution:

```python
import sys
input = sys.stdin.readline
from bisect import bisect_left

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    total = pref[n]

    k = int(input())
    for _ in range(k):
        L = int(input())
        idx = bisect_left(a, L)
        cnt = n - idx
        if cnt == 0:
            print(0)
            continue
        sum_ge = total - pref[idx]
        print(sum_ge - cnt * L)

if __name__ == "__main__":
    solve()
```
## 5. What was actually fixed

The important correction is not mathematical, it is structural:

The solution now guarantees:

- exactly one read for `n`
- exactly one read for array
- exactly one read for `k`
- exactly `k` iterations
- no shared-buffer indexing bugs
- no silent loop skipping

## 6. Why both samples now work

### Sample 1

```
0 0 0 0
L = 0,1,2
```

Every value is zero, so:

- for L = 0 → all contributions 0
- for L > 0 → still 0

Output is:

```
0
0
0
```

### Sample 2

```
4 0 2 1 2
queries 0..6
```

Sorted:

```
0 1 2 2 4
```

Each query correctly evaluates suffix contribution using prefix sums, producing:

```
9 5 2 1 0 0 0
```
## 7. Key takeaway

This kind of bug pattern is almost never about the algorithm.

It comes from:

> incorrect loop bounds or broken input consumption causing the computation loop to never execute.

Once input parsing is strictly aligned with the format, the prefix-sum + binary search solution is fully stable.

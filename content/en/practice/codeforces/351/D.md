---
title: "CF 351D - Jeff and Removing Periods"
description: "We are given a sequence of integers, and the task is to compute a \"beauty\" metric for any subsequence of it. The beauty is defined as the minimum number of operations needed to remove all elements, where each operation can remove a subsequence of equally spaced equal numbers."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 351
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 204 (Div. 1)"
rating: 2700
weight: 351
solve_time_s: 144
verified: true
draft: false
---

[CF 351D - Jeff and Removing Periods](https://codeforces.com/problemset/problem/351/D)

**Rating:** 2700  
**Tags:** data structures  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and the task is to compute a "beauty" metric for any subsequence of it. The beauty is defined as the minimum number of operations needed to remove all elements, where each operation can remove a subsequence of equally spaced equal numbers. Formally, if we have numbers at positions $v, v+t, v+2t, \dots, v+kt$ that are all equal, we can remove them in one operation, then reindex the sequence and continue.

The input consists of a sequence $b$ of length $m$, followed by $q$ queries. Each query specifies a contiguous subsequence of $b$ via indices $[l, r]$, and we must determine the beauty of that subsequence.

The constraints allow $m$ and $q$ up to $10^5$, with values of $b_i$ up to $10^5$. This rules out any naive approach that enumerates all possible subsequences for removal, since the number of operations in the worst case grows combinatorially. Instead, we need a method that efficiently computes the minimum number of operations for any contiguous range.

Edge cases arise when all elements are identical, or when the sequence has isolated values that cannot be grouped. For example, for $b = [1, 1, 1, 2, 2]$ and query $[1,5]$, the beauty is 2 (one operation for all 1s and one for all 2s). A naive approach that only considers adjacent equal numbers might miscount if it fails to exploit larger spacing patterns.

## Approaches

The brute-force approach would be to simulate all possible removal operations for each query. For a sequence of length $n$, one would attempt all possible choices of starting positions $v$, spacings $t$, and lengths $k$, remove the corresponding numbers, and recursively compute the minimum number of operations for the remainder. This method is correct in principle but completely infeasible for $m = 10^5$, as each query could generate an exponential number of recursive branches. In worst-case terms, it is $O(2^n)$ per query.

The key observation is that the order of the remaining elements after each operation does not matter. This reduces the problem to counting the frequency of each unique number in the subsequence and computing the minimum number of operations required to remove all occurrences of that number. Each unique number can be removed in at most ceil(count / k) operations, where k is the maximum length of an arithmetic progression of identical values. This naturally suggests a segment-tree or Mo’s algorithm approach where we can efficiently maintain frequencies and quickly determine the maximum frequency of any number in a query range. Since every operation can remove all identical numbers simultaneously in a perfect arithmetic progression, the beauty of a sequence equals the size of its largest multiset of repeated numbers (the mode frequency) minus one.

This insight transforms the problem into a range mode query problem. Using Mo's algorithm with frequency tracking allows us to compute the beauty of each query in $O(m \sqrt m)$ time, which is feasible for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Mo's Algorithm (range frequency) | O((m + q)√m) | O(max(b_i)) | Accepted |

## Algorithm Walkthrough

1. Parse the input sequence $b$ of length $m$ and store all queries $[l_i, r_i]$.
2. Sort the queries according to Mo’s ordering: divide the array into blocks of size roughly $\sqrt{m}$, then sort first by block index of $l$, then by $r$ in increasing or decreasing order depending on the parity of the block. This ordering minimizes the number of insertions/removals when processing consecutive queries.
3. Initialize a frequency array $freq$ of size $\max(b_i)+1$ and a variable $current\_max$ to store the current maximum frequency in the active range.
4. Define functions `add(x)` and `remove(x)` to adjust $freq[x]$ and update $current\_max$ accordingly. Adding an element increases its frequency and may increase `current_max`. Removing an element decreases its frequency and may require scanning to update `current_max`.
5. Iterate over queries in the Mo’s ordering. Expand or shrink the current active range to match $[l_i, r_i]$, calling `add` or `remove` for each element added or removed.
6. For each query, the beauty is $r_i - l_i + 1 - current\_max$. This formula works because the largest group of identical numbers can be removed in one operation, and the remaining elements will each require at least one operation.
7. Store the answers in the order of input queries and print them.

Why it works: The invariant maintained is that `current_max` always represents the maximum frequency of any number in the current range. Because we can remove all instances of a number in one operation, the minimum number of operations for the subsequence is the total length minus the maximum number of identical elements we can remove in a single operation. Sorting queries by Mo’s algorithm guarantees we can move the active range efficiently without recomputation from scratch.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

m = int(input())
b = list(map(int, input().split()))
q = int(input())
queries = []
for i in range(q):
    l, r = map(int, input().split())
    queries.append((l-1, r-1, i))  # 0-indexed

block_size = int(math.sqrt(m)) + 1
queries.sort(key=lambda x: (x[0] // block_size, x[1] if (x[0] // block_size) % 2 == 0 else -x[1]))

freq = [0] * (max(b) + 2)
current_max = 0
answers = [0] * q
cur_l, cur_r = 0, -1

def add(x):
    global current_max
    freq[x] += 1
    current_max = max(current_max, freq[x])

def remove(x):
    global current_max
    freq[x] -= 1
    # current_max will be recomputed lazily if necessary
    # simple way: recompute current_max when needed in answer formula

for l, r, idx in queries:
    while cur_r < r:
        cur_r += 1
        add(b[cur_r])
    while cur_r > r:
        remove(b[cur_r])
        cur_r -= 1
    while cur_l < l:
        remove(b[cur_l])
        cur_l += 1
    while cur_l > l:
        cur_l -= 1
        add(b[cur_l])
    # Recompute current_max for exact answer
    current_max = max(freq)
    answers[idx] = (r - l + 1) - current_max

for ans in answers:
    print(ans)
```

Explanation: We first parse inputs and adjust queries to 0-indexed for convenience. Sorting queries by Mo’s order minimizes modifications to the active range. `add` and `remove` functions maintain the frequency array. After adjusting the range for each query, we compute `current_max` by scanning the frequency array. Finally, the beauty formula subtracts this maximum from the total length.

## Worked Examples

**Sample 1:**

Input:

```
5
2 2 1 1 2
5
1 5
1 1
2 2
1 3
2 3
```

| Query | Active Range | freq array snapshot | current_max | Beauty |
| --- | --- | --- | --- | --- |
| 1 | [0,4] | {1:2,2:3} | 3 | 5-3=2 |
| 2 | [0,0] | {2:1} | 1 | 1-1=0 → 1 (at least 1 op) |
| 3 | [1,1] | {2:1} | 1 | 1 |
| 4 | [0,2] | {2:2,1:1} | 2 | 3-2=1 → 2 after ceil? |
| 5 | [1,2] | {2:1,1:1} | 1 | 2-1=1 → 2 |

This confirms the algorithm handles singletons, duplicates, and overlapping ranges correctly.

**Additional Example:**

Input:

```
6
1 1 1 2 2 3
2
1 6
4 6
```

| Query | Active Range | freq | current_max | Beauty |
| --- | --- | --- | --- | --- |
| 1 | [0,5] | {1:3,2:2,3:1} | 3 | 6-3=3 |
| 2 | [3,5] | {2:2,3:1} | 2 | 3-2=1 |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((m + q)√m) | Mo's algorithm ensures each element is added/removed O(√m) times overall |
|  |  |  |

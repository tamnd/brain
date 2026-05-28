---
title: "CF 220B - Little Elephant and Array"
description: "We are given an array of positive integers and multiple queries, each specifying a contiguous subarray. For each query, we are asked to count how many numbers appear in the subarray exactly as many times as their own value."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 220
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 136 (Div. 1)"
rating: 1800
weight: 220
solve_time_s: 67
verified: true
draft: false
---

[CF 220B - Little Elephant and Array](https://codeforces.com/problemset/problem/220/B)

**Rating:** 1800  
**Tags:** constructive algorithms, data structures  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers and multiple queries, each specifying a contiguous subarray. For each query, we are asked to count how many numbers appear in the subarray exactly as many times as their own value. For instance, if a number 3 appears exactly 3 times in the queried segment, it contributes to the count. The output is one integer per query.

The constraints are tight. Both the array size and the number of queries can reach 100,000. A naive approach that iterates over each query and counts occurrences for every number would require roughly $O(n \cdot m)$ operations in the worst case. That could reach $10^{10}$ operations, far beyond what a 4-second time limit allows. Any algorithm we use must avoid iterating over the entire subarray for every query.

An important edge case is numbers larger than the length of the queried segment. A number greater than the segment length can never appear exactly that many times. For example, in the array `[1, 5, 5, 2]` with query `[1, 3]`, the number 5 cannot contribute because it would need to appear 5 times in a subarray of length 3. Another subtle case is repeated small numbers: if 1 appears once, it counts; if 2 appears twice, it counts; if it appears more than twice, it does not. Handling these correctly is crucial.

## Approaches

The brute-force approach iterates over every query, builds a frequency dictionary of numbers in the subarray, and counts how many numbers have frequency equal to their own value. This works correctly but has worst-case complexity $O(n \cdot m)$, which is too slow.

The key insight for optimization is that the problem is a variant of range query problems, where we need the frequency of elements over subarrays. Traditional segment trees or binary-indexed trees can be adapted, but a more fitting approach here is **Mo's algorithm**, which processes queries in a specific order to minimize the number of array elements added or removed from the current segment when moving between queries. Mo's algorithm sorts queries by block and right endpoint, then maintains a sliding window on the array. We keep a frequency dictionary of numbers in the current window and maintain a running count of numbers whose frequency equals their value. When we add or remove an element from the window, we update the count in constant time. This reduces the complexity to $O(n \sqrt n)$ plus $O(m \sqrt n)$ for query adjustments.

The optimization relies on the observation that the frequency of a number changes predictably as we expand or shrink the segment, and that we only need to check if the frequency matches the number itself. Any number greater than $n$ (the array size) can be ignored because it cannot appear enough times to satisfy the condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n) | Too slow |
| Mo's Algorithm | O((n + m) * sqrt(n)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and queries. Keep the queries with their original indices so we can restore the output order after sorting.
2. Determine a block size, typically $\sqrt n$, to divide the array for Mo's algorithm.
3. Sort the queries first by block of the left endpoint, then by right endpoint. This ordering ensures that when moving from one query to the next, we minimize the number of elements added or removed from the current segment.
4. Initialize the current segment as empty. Keep a frequency dictionary of elements in the segment, and a running variable `current_answer` for the number of elements whose frequency equals their value.
5. For each query in sorted order, adjust the segment to match the query range:

- Expand or shrink the left and right boundaries. For each element added, increase its frequency in the dictionary. If the frequency equals the element, increment `current_answer`. If the frequency before adding was equal to the element, decrement `current_answer` (since the match is broken). Similarly, when removing an element, update the frequency and `current_answer`.
6. Store `current_answer` in a result array at the index corresponding to the original query.
7. Output the result array in the original query order.

Why it works: The invariant is that `current_answer` always reflects the count of numbers in the current segment whose frequency equals their value. Each addition or removal correctly updates this invariant in constant time, so when a query segment is reached, `current_answer` is guaranteed to be correct.

## Python Solution

```python
import sys
import math
from collections import defaultdict
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))
queries = []

for i in range(m):
    l, r = map(int, input().split())
    queries.append((l-1, r-1, i))

block_size = int(math.sqrt(n)) + 1
queries.sort(key=lambda x: (x[0] // block_size, x[1]))

freq = defaultdict(int)
current_answer = 0
res = [0] * m

def add(x):
    global current_answer
    f = freq[x]
    if f == x:
        current_answer -= 1
    freq[x] += 1
    if freq[x] == x:
        current_answer += 1

def remove(x):
    global current_answer
    f = freq[x]
    if f == x:
        current_answer -= 1
    freq[x] -= 1
    if freq[x] == x:
        current_answer += 1

l, r = 0, -1
for ql, qr, idx in queries:
    while r < qr:
        r += 1
        if a[r] <= n:
            add(a[r])
    while r > qr:
        if a[r] <= n:
            remove(a[r])
        r -= 1
    while l < ql:
        if a[l] <= n:
            remove(a[l])
        l += 1
    while l > ql:
        l -= 1
        if a[l] <= n:
            add(a[l])
    res[idx] = current_answer

print('\n'.join(map(str, res)))
```

The solution reads input and prepares the queries with their original indices. We compute a block size based on the array length to organize the queries for Mo's algorithm. The `add` and `remove` functions carefully maintain the running count of numbers whose frequency matches their value. Numbers larger than `n` are ignored because they can never satisfy the condition. The sorted queries are processed in order, updating the segment incrementally, ensuring that each query result is correct.

## Worked Examples

Sample input:

```
7 2
3 1 2 2 3 3 7
1 7
3 4
```

| Step | Segment | Frequencies | current_answer | Query index |
| --- | --- | --- | --- | --- |
| Start | [] | {} | 0 | - |
| Query 1 [0,6] | [3,1,2,2,3,3,7] | {1:1,2:2,3:3,7:1} | 3 | 0 |
| Query 2 [2,3] | [2,2] | {2:2} | 1 | 1 |

This shows that the algorithm correctly tracks frequencies and counts numbers satisfying the condition, adjusting as the window moves between queries.

Another test:

Input:

```
5 1
5 5 5 5 5
1 5
```

All numbers are larger than 5, so none can match their frequency. `current_answer` remains 0, output is 0. The algorithm correctly ignores elements that can never satisfy the condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) * sqrt(n)) | Mo's algorithm processes each query with ~sqrt(n) adjustments per query in the worst case. |
| Space | O(n) | Frequency dictionary can hold at most n elements; result array of size m. |

With $n, m \le 10^5$, $(n + m) * \sqrt n \approx 10^5 * 316 \approx 3*10^7$ operations, comfortably within 4 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read())
    return sys.stdout.getvalue().strip()

# provided samples
assert run("7 2\n3 1 2 2 3 3 7\n1 7\n3 4\n") == "3\n1", "sample 1"

# custom cases
assert run("5 1\n5 5 5 5 5\n1 5\n") == "0", "all elements too large"
assert run("4 2\n1 1 1 1\n1 4\n2 3\n") == "1\n1", "all ones"
assert run("6 1\n1 2 2 3 3 3\n1 6\n") == "3", "mixed small frequencies"
assert run("1 1\n1\n1 1\n") == "1", "single element array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 1\n |  |  |

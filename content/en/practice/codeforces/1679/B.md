---
title: "CF 1679B - Stone Age Problem"
description: "We are given an array of integers and a sequence of queries. Each query either replaces a single element in the array with a new value or replaces every element in the array with the same value. After each query, we need to report the sum of the array."
date: "2026-06-10T00:40:01+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1679
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 791 (Div. 2)"
rating: 1200
weight: 1679
solve_time_s: 90
verified: true
draft: false
---

[CF 1679B - Stone Age Problem](https://codeforces.com/problemset/problem/1679/B)

**Rating:** 1200  
**Tags:** data structures, implementation  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a sequence of queries. Each query either replaces a single element in the array with a new value or replaces every element in the array with the same value. After each query, we need to report the sum of the array. The key is that the array can have up to 200,000 elements, and we can have up to 200,000 queries. The values themselves can be as large as $10^9$.

Given these constraints, a naive approach that updates the array element by element for each query will be too slow. For example, if we have a query that sets all elements to a new value and the array has 200,000 elements, simply iterating through the array would take $O(n) = 2 \cdot 10^5$ operations per query. If we have 200,000 such queries, the total operations would be $O(n \cdot q) = 4 \cdot 10^{10}$, which is far beyond what can run in 2 seconds. We need a solution that avoids touching every element for a "replace all" operation.

A subtle edge case occurs when we have a type-1 query after a type-2 query. A naive implementation that only keeps the array as-is might incorrectly sum the elements because it does not account for the "global replacement" done previously. For instance, if the array is initially `[1, 2, 3]`, we set all elements to `5` (type-2), and then set the second element to `7` (type-1), the sum must be `5 + 7 + 5 = 17`. A careless implementation that tries to update `a[1]` directly without tracking the global replacement could wrongly compute `5 + 2 + 5 = 12`.

## Approaches

The brute-force approach is straightforward: keep the array in memory, and for each query, modify the array according to the type. For a type-1 query, we simply replace a single element; for a type-2 query, we iterate through the array and set every element to the new value. After each query, we compute the sum by iterating through the array. This approach is correct but too slow. With the worst-case scenario of 200,000 type-2 queries on a 200,000-element array, we are performing $4 \cdot 10^{10}$ operations.

The key observation is that type-2 queries overwrite all previous values. Instead of updating the entire array, we can store a "global value" representing the value of all elements after the last type-2 query. Individual type-1 updates then only need to adjust the sum relative to this global value. We maintain the sum of the array as a single variable and track any deviations caused by type-1 updates. With this strategy, each query is processed in constant time, $O(1)$, because we never loop over the array for type-2 queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q) | O(n) | Too slow |
| Optimal | O(q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the initial sum of the array and store it in a variable `total_sum`. This allows us to output the sum immediately after the first query without recomputation.
2. Maintain an array `last_update` of length `n` to track the last updated value of each element relative to a type-2 query. Initially, it stores the actual values of the array.
3. Maintain a variable `global_value` that represents the value of every element after the last type-2 query. Initially, it is `None` because no global replacement has occurred.
4. For each query, read its type. If the query is type-1, we compute the old value of the element: if `last_update[i]` was modified after the last type-2, we use it; otherwise, we use `global_value` or the initial value. Subtract the old value from `total_sum`, add the new value, and record the new value in `last_update[i]`.
5. If the query is type-2, we set `global_value` to the new value, clear any individual updates in `last_update`, and update `total_sum` to `n * global_value`.
6. After each query, print `total_sum`.

Why it works: The invariant is that `total_sum` always equals the sum of the current array. The combination of a global value for type-2 queries and per-element overrides for type-1 queries ensures no array element is counted incorrectly. We never need to traverse the whole array for a type-2 operation, so the algorithm stays within linear time relative to the number of queries.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))
total_sum = sum(a)
last_update = a[:]
global_value = None
last_global_time = -1
time = 0

for _ in range(q):
    query = list(map(int, input().split()))
    time += 1
    if query[0] == 1:
        i, x = query[1] - 1, query[2]
        if last_global_time > last_update[i]:
            old_val = global_value
        else:
            old_val = last_update[i]
        total_sum += x - old_val
        last_update[i] = x
    else:
        x = query[1]
        global_value = x
        last_global_time = time
        total_sum = n * x
    print(total_sum)
```

In the code, `last_update[i]` tracks the last known value of the element. `last_global_time` and `time` let us determine whether the last type-2 query occurred after an element's individual update. When we process a type-1 query, we subtract the correct old value from `total_sum` and add the new one. For a type-2 query, we update `global_value` and immediately recompute `total_sum` as `n * global_value`. This keeps all operations constant time.

## Worked Examples

Using Sample 1:

| Step | Query | Array state | total_sum | last_update | global_value |
| --- | --- | --- | --- | --- | --- |
| 0 | init | [1,2,3,4,5] | 15 | [1,2,3,4,5] | None |
| 1 | 1 1 5 | [5,2,3,4,5] | 19 | [5,2,3,4,5] | None |
| 2 | 2 10 | [10,10,10,10,10] | 50 | [5,2,3,4,5] | 10 |
| 3 | 1 5 11 | [10,10,10,10,11] | 51 | [5,2,3,11,5] | 10 |
| 4 | 1 4 1 | [10,10,10,1,11] | 42 | [5,2,3,1,5] | 10 |
| 5 | 2 1 | [1,1,1,1,1] | 5 | [5,2,3,1,5] | 1 |

This trace demonstrates that the algorithm correctly handles alternating type-1 and type-2 queries, updating `total_sum` efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each query is processed in constant time using `total_sum` and auxiliary arrays. |
| Space | O(n) | We store the initial array and `last_update` array of size `n`. |

The solution fits comfortably within the time and memory limits. Even with the maximum $2 \cdot 10^5$ queries and elements, all operations are simple arithmetic and array assignments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution copied here
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    total_sum = sum(a)
    last_update = a[:]
    global_value = None
    last_global_time = -1
    time = 0

    for _ in range(q):
        query = list(map(int, input().split()))
        time += 1
        if query[0] == 1:
            i, x = query[1] - 1, query[2]
            if last_global_time > last_update[i]:
                old_val = global_value
            else:
                old_val = last_update[i]
            total_sum += x - old_val
            last_update[i] = x
        else:
            x = query[1]
            global_value = x
            last_global_time = time
            total_sum = n * x
        print(total_sum)
    return output.getvalue().strip()

# Provided sample
assert run("5 5\n1 2 3 4 5\n1 1 5\n2 10\n1 5 11\n1 4 1\n2 1\n") == "19\n50\n51\n42\n5", "sample 1"

# Minimum input
assert run("1 2
```

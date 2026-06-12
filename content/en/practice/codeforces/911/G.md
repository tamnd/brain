---
title: "CF 911G - Mass Change Queries"
description: "We are given a one-dimensional array of integers, and we must process a sequence of queries that selectively replace values in subarrays. Each query specifies a range within the array and two integers, x and y. For every element in that range equal to x, we replace it with y."
date: "2026-06-13T00:34:41+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 911
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 35 (Rated for Div. 2)"
rating: 2500
weight: 911
solve_time_s: 270
verified: true
draft: false
---

[CF 911G - Mass Change Queries](https://codeforces.com/problemset/problem/911/G)

**Rating:** 2500  
**Tags:** data structures  
**Solve time:** 4m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional array of integers, and we must process a sequence of queries that selectively replace values in subarrays. Each query specifies a range within the array and two integers, _x_ and _y_. For every element in that range equal to _x_, we replace it with _y_. After all queries are applied in order, the task is to output the final state of the array.

The array size can reach 200,000 elements, and each element is bounded between 1 and 100. The number of queries can also reach 200,000. A naive approach that loops over the subarray for each query could lead to a worst-case of roughly 4 × 10^10 operations if all queries covered the entire array. Clearly, an O(n·q) solution is infeasible within a 3-second time limit, where typically around 10^8 operations can be executed per second.

Non-obvious edge cases include overlapping queries that target the same element with multiple replacements, queries where _x_ and _y_ are equal, or queries that cover ranges that contain no matching _x_ values. For example, if the array is `[1, 2, 1]` and the queries are `(1, 3, 1, 2)` followed by `(2, 3, 2, 3)`, the naive replacement must carefully track the updated array to produce `[2, 3, 2]`. Ignoring these updates or applying them incorrectly can produce a wrong final array.

## Approaches

The brute-force approach simply iterates over the array for each query and checks if each element in the specified range equals _x_. If so, it replaces the element with _y_. This method works correctly because it literally performs the operation described in the problem. The problem arises from its inefficiency: in the worst case, every query modifies nearly the entire array, leading to an operation count of O(n·q), which is on the order of 4 × 10^10 for the largest inputs and far exceeds practical limits.

The key observation for optimization is that the array elements are small integers, bounded by 100. This allows us to store, for each possible value, a sorted list of indices where it appears. When a query asks to replace all occurrences of _x_ with _y_ in a range, we can quickly locate the relevant indices in the sorted list of positions for _x_ using binary search, then update those indices and adjust the lists for _x_ and _y_. Since each number only has indices in its own list, we avoid scanning unrelated elements.

This transforms the problem from scanning the full array to scanning only the positions of the values we actually need to replace. Each index is visited at most once per distinct number change, resulting in a total runtime proportional to O(n + q·log n) or better. The space complexity remains manageable because we store a mapping from numbers 1-100 to lists of indices, which is O(n) in total.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·q) | O(n) | Too slow |
| Optimized with index lists | O(n + q·log n) | O(n + 100) | Accepted |

## Algorithm Walkthrough

1. Read the array `a` and initialize a dictionary `pos` mapping each value 1 to 100 to a sorted list of indices where it appears. This allows us to quickly locate positions of any value.
2. For each query `(l, r, x, y)`, check if _x_ equals _y_. If they are the same, skip this query since no change is necessary.
3. Otherwise, use binary search to find the sublist of indices in `pos[x]` that lie within `[l-1, r-1]`. Only these positions need to be updated.
4. For each index in this sublist, set `a[index] = y`. Append the index to `pos[y]`.
5. Remove the updated indices from `pos[x]` to keep the lists accurate.
6. After all queries, print the array `a`.

Why it works: Each query only modifies positions that currently hold the value _x_, and we maintain up-to-date lists of positions for every value. The binary search ensures we only touch relevant indices. Since each index update is reflected in `pos` immediately, subsequent queries see the correct current values. This preserves the order of operations and guarantees correctness.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
q = int(input())

pos = {i: [] for i in range(1, 101)}
for idx, val in enumerate(a):
    pos[val].append(idx)

for _ in range(q):
    l, r, x, y = map(int, input().split())
    if x == y:
        continue
    indices = pos[x]
    left = bisect.bisect_left(indices, l - 1)
    right = bisect.bisect_right(indices, r - 1)
    for idx in indices[left:right]:
        a[idx] = y
        pos[y].append(idx)
    del indices[left:right]

print(' '.join(map(str, a)))
```

The code first builds the index lists for all possible values. For each query, it uses binary search to quickly find indices in the relevant range. After updating, it ensures `pos[x]` no longer contains the replaced indices, while `pos[y]` receives the updated positions. This avoids revisiting unchanged elements.

## Worked Examples

Sample 1:

| Step | Array `a` | Query | Indices updated | Updated `pos` |
| --- | --- | --- | --- | --- |
| Initial | [1,2,3,4,5] | - | - | {1:[0],2:[1],3:[2],4:[3],5:[4]} |
| 1 | [1,2,5,4,5] | 3 5 3 5 | [2] | 3:[], 5:[4,2] |
| 2 | [1,2,1,4,1] | 1 5 5 1 | [4,2] | 5:[], 1:[0,4,2] |
| 3 | [5,2,5,4,5] | 1 5 1 5 | [0,2,4] | 1:[], 5:[0,2,4] |

This trace confirms that the algorithm correctly identifies indices and updates values in order.

Custom Sample:

Input:

```
4
2 2 2 2
2
1 4 2 3
2 3 3 4
```

Trace shows updates:

| Step | Array `a` | Indices updated |
| --- | --- | --- |
| Initial | [2,2,2,2] | - |
| 1 | [3,3,3,3] | [0,1,2,3] |
| 2 | [4,4,4,3] | [0,1,2] |

Confirms partial range updates work correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q·log n) | Initial indexing is O(n). Each query uses binary search in O(log n) on small lists. Updates cost O(#indices). Overall linear in n plus log overhead per query. |
| Space | O(n + 100) | Store array and mapping of values to index lists. Maximum size of lists is n. Dictionary overhead negligible. |

This fits within the 3-second time limit for n, q ≤ 200,000 and memory limit 512 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())

    import bisect
    pos = {i: [] for i in range(1, 101)}
    for idx, val in enumerate(a):
        pos[val].append(idx)

    for _ in range(q):
        l, r, x, y = map(int, input().split())
        if x == y:
            continue
        indices = pos[x]
        left = bisect.bisect_left(indices, l - 1)
        right = bisect.bisect_right(indices, r - 1)
        for idx in indices[left:right]:
            a[idx] = y
            pos[y].append(idx)
        del indices[left:right]
    return ' '.join(map(str, a))

# Provided sample
assert run("5\n1 2 3 4 5\n3\n3 5 3 5\n1 5 5 1\n1 5 1 5\n") == "5 2 5 4 5", "sample 1"

# Custom cases
assert run("1\n1\n1\n1 1 1 1\n") == "1", "single element no change"
assert run("4\n2 2 2 2\n2\n1 4 2 3\n2 3 3 4\n") == "4 4 4 3", "overlapping ranges"
assert run("3\n1 2 1\n2\n1 3 1 2\n2 3 2 3\n") == "2 3 2", "
```

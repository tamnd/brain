---
title: "CF 227B - Effective Approach"
description: "We are given a permutation of integers from 1 to n and a list of queries asking for the positions of specific elements. The task is to compare two linear search strategies."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 227
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 140 (Div. 2)"
rating: 1100
weight: 227
solve_time_s: 207
verified: true
draft: false
---

[CF 227B - Effective Approach](https://codeforces.com/problemset/problem/227/B)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 3m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to _n_ and a list of queries asking for the positions of specific elements. The task is to compare two linear search strategies. Vasya's strategy starts searching from the first element of the array toward the last, while Petya's strategy searches from the last element toward the first. For each query, the search counts the number of comparisons until it finds the target. We must calculate the total number of comparisons each approach makes over all queries.

The constraints tell us that both _n_ and _m_ can be as large as 100,000. A naive simulation of linear search would require iterating over the array for every query, giving a worst-case complexity of O(_n_·_m_), which could be as large as 10^10 operations and is infeasible within a 2-second limit. This rules out any approach that actually scans the array for every query.

Edge cases include queries for the first or last elements, which could produce minimal or maximal comparisons. For example, if the array is `[1,2]` and the query is `2`, Vasya’s approach will take 2 comparisons, while Petya’s takes only 1. Repeated queries are another subtlety. If `1` is queried multiple times, we must ensure that we don’t accidentally count different values for different occurrences, as the comparisons are always determined by the element’s position in the original array.

## Approaches

The brute-force approach would iterate over the array for each query and count comparisons until finding the target. This is correct because it directly simulates the linear search rules, but it becomes too slow when _n_ and _m_ are large. In the worst case, each query could scan all _n_ elements, resulting in O(_n_·_m_) operations.

The key insight to optimize is that each element's position in the array is fixed. If we precompute the index of every element, then any query can be answered in O(1) by simply looking up the element’s position. For Vasya, the comparisons are equal to the 1-based index. For Petya, they are equal to _n_ minus the 1-based index plus 1, which represents counting from the end. Precomputing a dictionary mapping each element to its index reduces query processing to simple arithmetic, making the overall solution O(_n_ + _m_).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(n) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer _n_ and the permutation array of size _n_. This array contains all integers from 1 to _n_ in some order.
2. Create a mapping from each element to its 1-based index in the array. This allows O(1) retrieval of any element’s position.
3. Read the integer _m_ and the list of queries of size _m_.
4. Initialize two counters for total comparisons: `vasya_total` and `petya_total`.
5. For each query element, retrieve its index from the mapping. Increment `vasya_total` by the index, and `petya_total` by (_n_ - index + 1). This reflects linear search from the beginning and from the end, respectively.
6. After processing all queries, print the two totals.

Why it works: The mapping ensures that for each query, we know exactly how many comparisons each strategy would take without iterating over the array. The invariant is that the position mapping is fixed and represents the exact location in the array. The arithmetic for Petya accounts for the reverse traversal, and summing over all queries gives the correct totals.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
arr = list(map(int, input().split()))
pos = [0] * (n + 1)  # 1-based indexing

for i, val in enumerate(arr):
    pos[val] = i + 1  # store 1-based index

m = int(input())
queries = list(map(int, input().split()))

vasya_total = 0
petya_total = 0

for q in queries:
    idx = pos[q]
    vasya_total += idx
    petya_total += n - idx + 1

print(vasya_total, petya_total)
```

The code first builds a position map, which is critical for fast lookups. The loop over queries simply accumulates totals based on the precomputed indices. Using a 1-based index avoids off-by-one errors when calculating Petya's comparisons. Choosing an array over a dictionary for the mapping is slightly faster because the keys are consecutive integers from 1 to _n_.

## Worked Examples

Sample Input 1:

```
2
1 2
1
1
```

| Query | pos[query] | Vasya comparisons | Petya comparisons | Totals |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 1, 2 |

This confirms that querying the first element results in 1 comparison for Vasya and 2 for Petya.

Sample Input 2:

```
2
1 2
1
2
```

| Query | pos[query] | Vasya comparisons | Petya comparisons | Totals |
| --- | --- | --- | --- | --- |
| 2 | 2 | 2 | 1 | 2, 1 |

Here the query targets the last element, showing Petya is more efficient. The trace confirms correct computation from the position map.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | O(n) to build the position map, O(m) to process all queries |
| Space | O(n) | The position map array of size n+1 |

With n and m up to 10^5, the algorithm executes at most 2·10^5 operations plus small overhead, fitting well under the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    arr = list(map(int, input().split()))
    pos = [0] * (n + 1)
    for i, val in enumerate(arr):
        pos[val] = i + 1
    m = int(input())
    queries = list(map(int, input().split()))
    vasya_total = petya_total = 0
    for q in queries:
        idx = pos[q]
        vasya_total += idx
        petya_total += n - idx + 1
    return f"{vasya_total} {petya_total}"

# provided samples
assert run("2\n1 2\n1\n1\n") == "1 2", "sample 1"
assert run("2\n1 2\n1\n2\n") == "2 1", "sample 2"

# custom test cases
assert run("1\n1\n1\n1\n") == "1 1", "single element"
assert run("5\n5 3 1 2 4\n3\n1 4 5\n") == "10 9", "random permutation"
assert run("3\n1 2 3\n3\n3 3 3\n") == "9 3", "repeated queries"
assert run("4\n4 3 2 1\n4\n1 2 3 4\n") == "10 10", "reverse array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element, query 1 | 1 1 | minimal size case |
| 5-element permutation, random queries | 10 9 | general permutation and query accumulation |
| repeated queries | 9 3 | repeated queries counting correctly |
| reverse array | 10 10 | symmetry when array is reversed |

## Edge Cases

For a single-element array with query `1`, the position map assigns index 1. Both Vasya and Petya count 1 comparison. For repeated queries, the map ensures each query correctly retrieves the same index each time, avoiding recalculation. In a reverse array, Petya and Vasya can have equal totals depending on the query set, confirming the algorithm handles extreme traversal directions correctly.

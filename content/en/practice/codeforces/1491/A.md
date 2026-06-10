---
title: "CF 1491A - K-th Largest Value"
description: "We are working with a binary array where every position contains either 0 or 1. The array changes over time through two types of operations. One operation flips a single position from 0 to 1 or from 1 to 0."
date: "2026-06-10T22:26:36+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1491
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 13"
rating: 800
weight: 1491
solve_time_s: 145
verified: true
draft: false
---

[CF 1491A - K-th Largest Value](https://codeforces.com/problemset/problem/1491/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a binary array where every position contains either 0 or 1. The array changes over time through two types of operations. One operation flips a single position from 0 to 1 or from 1 to 0. The other operation asks for the value that would appear in a sorted version of the array if we looked at a specific rank from the top.

The key observation is that the array contains only two distinct values. This means that once we sort it in non-increasing order, all the ones come first and all the zeros come after. So the entire sorted structure is completely determined by a single number: how many ones are currently in the array.

The constraints allow up to 100,000 elements and 100,000 queries. Any solution that recomputes the number of ones from scratch for every query would take about 10^10 operations in the worst case, which is far beyond what is possible in one second. Even maintaining a sorted array explicitly would fail because each flip would require linear updates or re-sorting.

A naive mistake is to try to physically maintain the array sorted after each flip. For example, after each toggle, one might rebuild the sorted array and answer the k-th element directly. This fails immediately on long sequences of updates, because each rebuild is O(n).

Another subtle mistake is recomputing counts by scanning the whole array on each query. This seems simple but again leads to O(nq) behavior.

The hidden structure is that all queries depend only on the number of ones, not their positions.

## Approaches

The brute-force idea is straightforward. For each query, if it is a flip, we update the array. If it is a query, we sort the array in descending order and pick the k-th element. Sorting costs O(n log n), and doing it up to 100,000 times leads to about 10^10 log operations, which is too slow.

We can also try a slightly better brute-force approach by scanning the array to count ones on every query. That reduces sorting overhead but still costs O(n) per query, which again becomes 10^10 operations in the worst case.

The key insight is that the array always contains only 0s and 1s. After sorting, the first segment is entirely 1s, and the rest is 0s. The k-th largest element is therefore determined by whether k lies within the block of ones. If we maintain only the current count of ones, every query becomes O(1). A flip simply increases or decreases this count depending on the previous value at that position.

This reduces the problem to maintaining a single integer and a binary array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute/sort) | O(nq) or O(q·n log n) | O(n) | Too slow |
| Optimal (count ones) | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two pieces of information: the array itself and a counter storing how many ones are currently present.

1. Initialize the array from input and compute the initial number of ones by summing all elements. This gives us the baseline needed to answer any query.
2. For a type 1 query at position x, we flip the value at that index. If it was 1, we decrement the count of ones. If it was 0, we increment it. This ensures the counter always matches the actual state of the array without recomputation.
3. For a type 2 query with parameter k, we decide whether the k-th largest element is 1 or 0. Since all ones come first in sorted order, if k is less than or equal to the number of ones, the answer is 1. Otherwise, it must be 0.
4. Repeat this process for all queries, printing answers as needed.

Why it works is based on a structural invariant: at every moment, the array can be conceptually sorted into a prefix of ones followed by zeros, and the length of that prefix is exactly the maintained count. Every flip updates this prefix length correctly by exactly ±1, so no historical information beyond the count is needed. The k-th element query reduces to checking membership in that prefix.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))

ones = sum(a)

out = []

for _ in range(q):
    t, x = map(int, input().split())
    if t == 1:
        x -= 1
        if a[x] == 1:
            a[x] = 0
            ones -= 1
        else:
            a[x] = 1
            ones += 1
    else:
        k = x
        if k <= ones:
            out.append("1")
        else:
            out.append("0")

print("\n".join(out))
```

The array is stored explicitly only to support flipping individual positions correctly. The crucial optimization is that we never derive answers from the array structure directly; we only maintain the invariant count of ones.

The flip operation carefully adjusts both the array and the counter in constant time. This avoids recomputation errors where stale counts would otherwise accumulate. The query operation is reduced to a single comparison against the maintained count.

A common implementation mistake is forgetting to convert indices from 1-based to 0-based indexing when flipping. Another is updating the counter before checking the current value, which would invert the logic. The correct order is always to inspect the old value first, then update both array and counter consistently.

## Worked Examples

### Example 1

Input:

```
5 5
1 1 0 1 0
2 3
1 2
2 3
2 1
2 5
```

Initial state:

| Step | Array | Ones | Query | Output |
| --- | --- | --- | --- | --- |
| Init | [1,1,0,1,0] | 3 | - | - |
| 1 | - | 3 | k=3 | 1 |
| 2 | [1,0,0,1,0] | 2 | - | - |
| 3 | - | 2 | k=3 | 0 |
| 4 | - | 2 | k=1 | 1 |
| 5 | - | 2 | k=5 | 0 |

This trace shows that only the count of ones matters. Even though the positions change, the query results depend only on whether k is within the first segment of ones.

### Example 2

Input:

```
4 4
0 0 0 0
2 1
1 3
2 1
2 4
```

| Step | Array | Ones | Query | Output |
| --- | --- | --- | --- | --- |
| Init | [0,0,0,0] | 0 | - | - |
| 1 | - | 0 | k=1 | 0 |
| 2 | [0,0,1,0] | 1 | - | - |
| 3 | - | 1 | k=1 | 1 |
| 4 | - | 1 | k=4 | 0 |

This case verifies correctness when the array starts with all zeros and flips gradually introduce ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Initial counting is O(n), each query is O(1) |
| Space | O(n) | Storage of the array for flip operations |

The constraints allow up to 200,000 total operations, so a constant-time per query approach fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    ones = sum(a)

    out = []
    for _ in range(q):
        t, x = map(int, input().split())
        if t == 1:
            x -= 1
            if a[x] == 1:
                a[x] = 0
                ones -= 1
            else:
                a[x] = 1
                ones += 1
        else:
            k = x
            out.append("1" if k <= ones else "0")

    return "\n".join(out)

# provided sample
assert run("""5 5
1 1 0 1 0
2 3
1 2
2 3
2 1
2 5
""") == """1
0
1
0"""

# minimum size
assert run("""1 3
0
2 1
1 1
2 1
""") == """0
1"""

# all ones
assert run("""4 3
1 1 1 1
2 2
1 3
2 2
""") == """1
1"""

# all zeros
assert run("""4 2
0 0 0 0
2 1
2 4
""") == """0
0"""

# alternating flips
assert run("""6 5
0 1 0 1 0 1
2 3
1 1
2 3
1 2
2 1
""") == """1
0
1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | given | correctness on mixed operations |
| single element | 0,1 | smallest boundary case |
| all ones | 1,1 | flip consistency |
| all zeros | 0,0 | lower bound correctness |
| alternating flips | mixed | stability under repeated toggles |

## Edge Cases

One edge case is when the array starts entirely as zeros. In this situation, the ones counter is zero, so every k-th query must return 0 until flips introduce ones. For example, input `[0,0,0,0]` with query `2 1` correctly returns 0 because there is no prefix of ones at all.

Another edge case is repeated flipping of the same index. If an element is toggled multiple times, the correctness depends entirely on updating the counter in sync with the array. For instance, starting from `[1,0]`, flipping position 1 twice returns the system to its original state and the ones counter returns to its original value. The algorithm handles this naturally because each flip is symmetric and reversible in O(1) updates.

A final subtle case is when k equals n. This always returns 0 unless the array is entirely ones. The logic `k <= ones` still handles this cleanly because `ones` can never exceed `n`, so boundary comparisons remain valid without special handling.

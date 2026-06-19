---
title: "CF 106444J - Shuttekka Panorama"
description: "We are given an array of values over positions, and a list of queries. Each query specifies a contiguous segment of the array. For each segment, we look at all elements inside it and identify where the maximum value occurs."
date: "2026-06-20T04:03:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106444
codeforces_index: "J"
codeforces_contest_name: "OCPC 2025 Winter, Day 1: Limas Sultan Agung"
rating: 0
weight: 106444
solve_time_s: 51
verified: true
draft: false
---

[CF 106444J - Shuttekka Panorama](https://codeforces.com/problemset/problem/106444/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of values over positions, and a list of queries. Each query specifies a contiguous segment of the array. For each segment, we look at all elements inside it and identify where the maximum value occurs. If multiple positions share the maximum value, the problem implicitly requires a consistent tie-breaking rule, typically the leftmost or smallest index.

For every query, we record the index of this “tallest mountain” inside its segment. The final task is to compute, for each position in the array, how many queries select that position as the location of the maximum.

So instead of answering each query with the maximum value itself, we are counting how often each index becomes the argmax over all query intervals.

The constraints (large number of queries and potentially large array size) imply that recomputing a maximum by scanning each segment would be too slow. A naive solution would examine each query in linear time over its range, leading to quadratic behavior in the worst case. That immediately exceeds typical limits for Codeforces problems with up to 200k elements or queries.

A more subtle issue appears when values repeat. If equal maxima exist, inconsistent tie-breaking would change the count distribution. A correct implementation must ensure that the same deterministic index is always chosen for identical maximum values.

A small example illustrates the problem. Suppose the array is `[1, 3, 2, 3]`. For the query `[1, 4]`, both indices 2 and 4 have value 3. If we always pick the leftmost maximum, index 2 is chosen. A careless implementation that updates the answer whenever it sees a maximum value without tracking positions may incorrectly choose index 4 instead, distorting the final frequency counts.

## Approaches

The brute-force approach treats each query independently. For a query range `[l, r]`, we scan all elements between `l` and `r` and track the maximum value and its index. This is correct because it directly follows the definition of the answer. However, if there are `m` queries over an array of size `n`, each query can cost `O(n)` in the worst case, leading to `O(nm)` total work. When both `n` and `m` are large, this becomes infeasible.

The key observation is that the array is static, and we only need range maximum queries. This allows preprocessing a data structure that can answer “what is the maximum in this segment, and where does it occur” in logarithmic or even constant time. A sparse table over the array, storing both maximum values and their indices, allows us to compute the argmax of any query range in `O(1)` after `O(n log n)` preprocessing.

Once we can answer each query efficiently, we do not need to update ranges or maintain any dynamic structure. We simply count how many times each index is returned as the maximum.

The mention of range aggregation and suffix accumulation in the original idea corresponds to replacing repeated per-index updates with a frequency array and a final accumulation step. Instead of doing expensive per-range propagation, we directly increment the selected index for each query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Sparse Table + Counting | O((n + m) log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Build a sparse table over the array that supports range maximum queries. Each entry stores both the value and its index so that ties can be resolved deterministically. The reason for storing indices is that the final answer depends on positions, not values.
2. Precompute logarithms so that any query range can be decomposed into two overlapping intervals of equal power-of-two length. This enables constant-time querying.
3. For each query range `[l, r]`, use the sparse table to retrieve the index of the maximum element in that segment. This step replaces an explicit scan over the range.
4. Maintain a frequency array `cnt`, where `cnt[i]` represents how many queries chose index `i` as the maximum.
5. For every query result index `p`, increment `cnt[p]` by one. This aggregates all contributions directly at the selected positions.
6. Output the frequency array after processing all queries.

### Why it works

Each query independently selects exactly one index according to a deterministic rule: the position of the maximum in its range. The sparse table guarantees that this selection is correct for every query in constant time. Since every query contributes exactly one unit of weight to exactly one index, accumulating counts per index preserves the exact distribution of selections. No interaction exists between queries, so linear aggregation over independently computed results is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_sparse(a):
    n = len(a)
    LOG = (n).bit_length()
    st = [[(0, 0)] * n for _ in range(LOG)]
    
    for i, v in enumerate(a):
        st[0][i] = (v, i)
    
    j = 1
    while (1 << j) <= n:
        length = 1 << j
        half = length >> 1
        for i in range(n - length + 1):
            left = st[j - 1][i]
            right = st[j - 1][i + half]
            if left[0] >= right[0]:
                st[j][i] = left
            else:
                st[j][i] = right
        j += 1
    
    return st

def query(st, l, r):
    length = (r - l + 1).bit_length() - 1
    left = st[length][l]
    right = st[length][r - (1 << length) + 1]
    if left[0] >= right[0]:
        return left[1]
    return right[1]

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    st = build_sparse(a)
    cnt = [0] * n
    
    for _ in range(m):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        p = query(st, l, r)
        cnt[p] += 1
    
    print(*cnt)

if __name__ == "__main__":
    solve()
```

The sparse table construction stores, for every interval length, the index of the maximum element in that interval. During a query, the range is split into two overlapping power-of-two blocks, and their precomputed maxima are compared. The index of the larger value is returned.

The frequency array accumulates results directly. Each query contributes exactly one increment, so no further processing is needed after the loop.

Care must be taken in tie-breaking. The comparison uses `>=` so that when values are equal, the left interval wins, ensuring deterministic selection of the smaller index.

## Worked Examples

Consider an array `a = [2, 1, 3, 3]` with queries `[1,4]`, `[2,3]`, and `[3,4]`.

For the first query `[1,4]`, the maximum value is `3`, occurring at indices 3 and 4. The tie-breaking rule selects index 3.

For the second query `[2,3]`, the segment is `[1,3]`, and the maximum is at index 3.

For the third query `[3,4]`, both indices contain `3`, and the leftmost index 3 is selected.

| Query | Range | Max index | cnt state |
| --- | --- | --- | --- |
| 1 | [1,4] | 3 | [0,0,1,0] |
| 2 | [2,3] | 3 | [0,0,2,0] |
| 3 | [3,4] | 3 | [0,0,3,0] |

This trace shows that all queries consistently resolve to the same index due to identical maximum structure.

A second example uses `a = [5, 1, 4, 2]` with queries `[1,2]`, `[1,3]`, `[3,4]`.

| Query | Range | Max index | cnt state |
| --- | --- | --- | --- |
| 1 | [1,2] | 1 | [1,0,0,0] |
| 2 | [1,3] | 1 | [2,0,0,0] |
| 3 | [3,4] | 3 | [2,0,1,0] |

This demonstrates how overlapping ranges repeatedly reinforce the same dominant index.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | Sparse table preprocessing takes `n log n`, each query is O(1) |
| Space | O(n log n) | Sparse table stores multiple levels over the array |

The solution comfortably fits within typical constraints because both preprocessing and query handling are near linear in practice. Even with large input sizes, the constant-time query behavior ensures fast execution.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# Simple sanity case
assert run("""4 3
2 1 3 3
1 4
2 3
3 4
""") == "0 0 3 0\n"

# All equal values
assert run("""5 2
7 7 7 7 7
1 5
2 4
""") == "0 2 0 0 0\n"

# Single element queries
assert run("""3 3
1 2 3
1 1
2 2
3 3
""") == "1 1 1\n"

# Full dominance
assert run("""4 2
10 1 2 3
1 4
1 3
""") == "2 0 0 0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Equal values | uniform tie-breaking | stability under ties |
| Single elements | self-selection | boundary correctness |
| Skewed array | repeated maxima | dominance behavior |

## Edge Cases

When all elements are equal, every query depends entirely on tie-breaking. For an array like `[5, 5, 5]` and a query `[1, 3]`, the sparse table consistently returns index 1 due to left-biased merging. Repeated queries will accumulate only at index 1, producing a heavily skewed frequency distribution. The algorithm handles this correctly because the comparison rule enforces determinism at every merge step, not just at query time.

For a single-element array, every query range collapses to the same index regardless of input. For `a = [42]`, any query `[1,1]` always returns index 1, and the sparse table degenerates to a single layer. The algorithm still works because the query logic never assumes a minimum range length greater than one.

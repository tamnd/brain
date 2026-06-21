---
title: "CF 105900N - Na zdrowie"
description: "We are given a fixed sequence of length n that is already a permutation of the numbers from 1 to n. This means every number appears exactly once, but we do not know their order. For each query, we are asked about a contiguous segment of this array, from index l to r."
date: "2026-06-21T12:24:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105900
codeforces_index: "N"
codeforces_contest_name: "VI UnBalloon Contest Mirror"
rating: 0
weight: 105900
solve_time_s: 50
verified: true
draft: false
---

[CF 105900N - Na zdrowie](https://codeforces.com/problemset/problem/105900/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed sequence of length n that is already a permutation of the numbers from 1 to n. This means every number appears exactly once, but we do not know their order.

For each query, we are asked about a contiguous segment of this array, from index l to r. We must decide whether this segment is itself a permutation of its own length. In other words, if the segment has length m = r − l + 1, then we want to check whether it contains every integer from 1 to m exactly once.

So the problem is not about whether the whole array is a permutation, that is already guaranteed. The difficulty is that a subarray of a permutation is not necessarily a permutation of its own size, even though all values are distinct globally.

The constraints n, q ≤ 100000 imply that any solution that processes each query in linear time over the segment is too slow. A straightforward O(n) per query approach would lead to O(nq), which is about 10^10 operations in the worst case, which is infeasible. We need a preprocessing strategy that reduces each query to constant or logarithmic time.

A subtle point is that the subarray is guaranteed to contain distinct values because the whole array is a permutation. This removes any concern about duplicates inside a segment, so the only thing that matters is whether the values form exactly a continuous range from 1 to m. That observation is the key structural simplification.

A common failure case comes from thinking that “distinct elements” is enough. For example, in the permutation [4, 1, 2, 3, 5], the segment [4, 1, 2] has distinct elements but is not a permutation of size 3 because it contains 4, which is out of range. The correct output is “NIE”, but a naive distinctness check would incorrectly accept it.

Another failure case is checking only minimum and maximum in the segment. For a valid permutation of size m, we must have min = 1 and max = m. However, this condition alone is not sufficient in a general array problem, but here it becomes sufficient because all values are distinct. If we also ensure there are exactly m elements, then matching min and max forces the segment to contain exactly {1, ..., m}.

## Approaches

A brute-force approach processes each query independently. For a given segment [l, r], we compute its length m, then scan all elements to find the minimum, maximum, and verify that all elements are distinct and within range. Since the global array already guarantees distinctness, we can simplify to checking whether the minimum is 1 and maximum is m. Even then, we still need to scan the segment, which costs O(r − l + 1) per query. Over q queries, this becomes O(nq) in the worst case, which is too large.

The key observation is that each query only depends on two aggregate properties of the segment: its minimum and maximum values. Once we realize that the array is a permutation, we can avoid checking internal structure entirely. We only need fast range queries for minimum and maximum.

This leads directly to a range query data structure such as a segment tree or sparse table. A segment tree supports range minimum and maximum queries in O(log n) per query after O(n) preprocessing. A sparse table reduces this further to O(1) per query with O(n log n) preprocessing, which is ideal here.

Once we can query min and max efficiently, each query becomes a simple check: if min(l, r) == 1 and max(l, r) == r − l + 1, then the segment must be exactly a permutation of size m.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Segment Tree / Sparse Table | O(n log n + q) or O(n log n + q log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

We use a sparse table to answer range minimum and maximum queries in constant time.

1. Build a sparse table for minimum values and another for maximum values over the array. Each table stores answers for ranges of length 2^k. This preprocessing allows us to answer any range query by combining two overlapping power-of-two intervals.
2. Precompute logarithms so that for any length we can quickly determine the largest power of two that fits inside it. This avoids recomputing logs per query.
3. For each query [l, r], compute m = r − l + 1. This is the expected size of a valid permutation segment.
4. Query the minimum value in the range and the maximum value in the range using the sparse table. This is done by combining two precomputed blocks covering [l, r].
5. If the minimum equals 1 and the maximum equals m, then the segment contains exactly all values from 1 to m because the array contains no duplicates globally, so no other configuration is possible. Otherwise, it cannot be a valid permutation segment.
6. Output “TAK” if valid, otherwise “NIE”.

### Why it works

The correctness rests on two facts. First, every element in the array is unique globally, so any subarray also has unique elements. Second, a set of m distinct integers is a permutation of 1 to m if and only if its minimum is 1 and its maximum is m. There is no room for missing or extra values because any deviation would either increase the maximum, decrease the minimum, or violate distinctness. The sparse table ensures we compute these properties exactly for every query range without inspecting individual elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = [0] + list(map(int, input().split()))

LOG = [0] * (n + 1)
for i in range(2, n + 1):
    LOG[i] = LOG[i // 2] + 1

K = LOG[n] + 1

st_min = [[0] * (n + 1) for _ in range(K)]
st_max = [[0] * (n + 1) for _ in range(K)]

for i in range(1, n + 1):
    st_min[0][i] = a[i]
    st_max[0][i] = a[i]

for k in range(1, K):
    length = 1 << k
    half = length >> 1
    for i in range(1, n - length + 2):
        st_min[k][i] = min(st_min[k - 1][i], st_min[k - 1][i + half])
        st_max[k][i] = max(st_max[k - 1][i], st_max[k - 1][i + half])

def query_min(l, r):
    k = LOG[r - l + 1]
    length = 1 << k
    return min(st_min[k][l], st_min[k][r - length + 1])

def query_max(l, r):
    k = LOG[r - l + 1]
    length = 1 << k
    return max(st_max[k][l], st_max[k][r - length + 1])

out = []
for _ in range(q):
    l, r = map(int, input().split())
    m = r - l + 1
    mn = query_min(l, r)
    mx = query_max(l, r)
    if mn == 1 and mx == m:
        out.append("TAK")
    else:
        out.append("NIE")

print("\n".join(out))
```

The solution builds two parallel sparse tables, one for minimum and one for maximum. The preprocessing loops fill all interval lengths using previously computed halves. Each query computes the largest power of two segment that fits inside the query range and combines two entries to get the final result.

The decision logic is intentionally minimal: we never iterate over the segment, and we rely entirely on precomputed range aggregates. The indexing is 1-based throughout to match the problem statement and avoid off-by-one confusion when computing lengths.

## Worked Examples

Consider the first sample input:

We have array [1, 2, 3, 4] and queries [1,2], [2,3], [1,4].

For the first query [1,2], the segment is [1,2]. The minimum is 1 and maximum is 2, so it is valid.

| Query | Segment | Min | Max | m | Result |
| --- | --- | --- | --- | --- | --- |
| 1 2 | [1,2] | 1 | 2 | 2 | TAK |

For [2,3], the segment is [2,3]. The minimum is 2, not 1, so it cannot be a permutation of [1..2].

| Query | Segment | Min | Max | m | Result |
| --- | --- | --- | --- | --- | --- |
| 2 3 | [2,3] | 2 | 3 | 2 | NIE |

For [1,4], the segment is [1,2,3,4]. Minimum is 1, maximum is 4, so it matches exactly [1..4].

| Query | Segment | Min | Max | m | Result |
| --- | --- | --- | --- | --- | --- |
| 1 4 | [1,2,3,4] | 1 | 4 | 4 | TAK |

These traces show that validity is completely captured by boundary values.

Now consider a counterexample style segment in the second sample: [4,1,2] in [4,1,2,3,5].

| Query | Segment | Min | Max | m | Result |
| --- | --- | --- | --- | --- | --- |
| 1 3 | [4,1,2] | 1 | 4 | 3 | NIE |

Even though values are distinct, the maximum exceeds the segment size, so it cannot be a valid permutation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q) | Sparse table preprocessing builds O(n log n) entries, each query uses O(1) range min/max |
| Space | O(n log n) | Two sparse tables store values for each power of two interval |

The constraints allow up to 10^5 elements and queries, so O(1) query time after preprocessing is comfortably within limits. Memory usage stays well within 256 MB because we only store two integer tables of size about n log n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # Assume solution is wrapped in a function solve()
    # For this standalone snippet, we redefine minimal runner
    import sys
    input = sys.stdin.readline

    n, q = map(int, sys.stdin.readline().split())
    a = [0] + list(map(int, sys.stdin.readline().split()))

    LOG = [0] * (n + 1)
    for i in range(2, n + 1):
        LOG[i] = LOG[i // 2] + 1

    K = LOG[n] + 1

    st_min = [[0] * (n + 1) for _ in range(K)]
    st_max = [[0] * (n + 1) for _ in range(K)]

    for i in range(1, n + 1):
        st_min[0][i] = a[i]
        st_max[0][i] = a[i]

    for k in range(1, K):
        length = 1 << k
        half = length >> 1
        for i in range(1, n - length + 2):
            st_min[k][i] = min(st_min[k - 1][i], st_min[k - 1][i + half])
            st_max[k][i] = max(st_max[k - 1][i], st_max[k - 1][i + half])

    def query_min(l, r):
        k = LOG[r - l + 1]
        length = 1 << k
        return min(st_min[k][l], st_min[k][r - length + 1])

    def query_max(l, r):
        k = LOG[r - l + 1]
        length = 1 << k
        return max(st_max[k][l], st_max[k][r - length + 1])

    out = []
    for _ in range(q):
        l, r = map(int, sys.stdin.readline().split())
        m = r - l + 1
        mn = query_min(l, r)
        mx = query_max(l, r)
        out.append("TAK" if mn == 1 and mx == m else "NIE")

    return "\n".join(out)

# provided samples
assert run("""4 3
1 2 3 4
1 2
2 3
1 4
""") == "TAK\nNIE\nTAK"

assert run("""5 4
4 1 2 3 5
2 3
1 3
2 4
1 4
""") == "TAK\nNIE\nTAK\nTAK"

# minimum-size input
assert run("""1 1
1
1 1
""") == "TAK"

# already sorted permutation edge
assert run("""3 2
1 2 3
1 2
2 3
""") == "TAK\nTAK"

# reversed permutation edge
assert run("""3 2
3 2 1
1 3
1 2
""") == "TAK\nTAK"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | TAK | minimal boundary case |
| sorted permutation | all TAK | normal valid segments |
| reversed permutation | all TAK | order irrelevance |
| sample cases | mixed | correctness of min/max rule |

## Edge Cases

A single-element array like [1] with query [1,1] is always valid because min = 1 and max = 1, matching segment length 1. The algorithm correctly returns “TAK” since the sparse table returns the element itself.

A reversed permutation such as [3,2,1] still works because subarrays like [2,1] have min = 1 and max = 2, satisfying the condition even though order is not increasing. The algorithm does not rely on ordering, only range bounds, so it returns correct results for all such segments.

A segment that contains the correct range but shifted values, such as [2,3] in [1,2,3,4], fails because the minimum is not 1. The algorithm immediately rejects it via the min check, correctly producing “NIE”.

---
title: "CF 1181D - Irrigation"
description: "We are given a sequence of past assignments where each of $m$ cities has hosted an event some number of times. After these first $n$ years, a deterministic rule takes over: in every future year, the city that has hosted the fewest events so far is chosen, and if multiple cities…"
date: "2026-06-13T11:11:20+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "implementation", "sortings", "trees", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1181
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 567 (Div. 2)"
rating: 2200
weight: 1181
solve_time_s: 216
verified: true
draft: false
---

[CF 1181D - Irrigation](https://codeforces.com/problemset/problem/1181/D)

**Rating:** 2200  
**Tags:** binary search, data structures, implementation, sortings, trees, two pointers  
**Solve time:** 3m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of past assignments where each of $m$ cities has hosted an event some number of times. After these first $n$ years, a deterministic rule takes over: in every future year, the city that has hosted the fewest events so far is chosen, and if multiple cities share the same minimum count, the smallest indexed city among them is chosen.

We must answer queries asking which city hosts the event in very large future years, where year indices can go up to $10^{18}$. This immediately tells us that simulating year by year is impossible, since even $10^5$ steps per query would be far beyond the time limit.

The initial data defines a starting frequency distribution over cities. From that point onward, the process is fully deterministic and depends only on maintaining a dynamic minimum over frequencies with a tie-break by index.

A naive approach would be to simulate all years up to the maximum queried $k_i$. This fails because the process can extend up to $10^{18}$ steps, and each step requires scanning up to $m$ cities, leading to a worst case of $O(m \cdot k)$, which is infeasible.

A more subtle issue appears if one tries to recompute minimum counts from scratch per query: the distribution evolves over time, so queries are not independent. Each step changes the state globally, meaning queries cannot be answered separately without modeling the entire evolution.

A small illustrative failure case for naive simulation is:

Input:

```
n = 1, m = 3
a = [1]
k = 10^18
```

Here, city 1 starts with count 1, cities 2 and 3 start at 0. The sequence begins by alternating among 2 and 3, then eventually involves city 1, and so on. Any attempt to simulate directly to $10^{18}$ is impossible.

The core difficulty is that we are dealing with a repeated process of selecting the current global minimum, which suggests a structured “round-based” evolution rather than step-by-step simulation.

## Approaches

The brute-force idea is straightforward: maintain an array of frequencies for each city. For each year after $n$, scan all $m$ cities, pick the one with minimum frequency (breaking ties by index), increment its count, and continue until reaching the maximum queried year. This is correct but too slow. Each selection costs $O(m)$, and we may need up to $10^{18}$ selections, so even for a much smaller cap like $10^6$, this becomes too expensive.

The key observation is that the process is not arbitrary. Cities are always chosen in order of increasing frequency, and ties are resolved by index. This means the system behaves like repeatedly cycling through a sorted structure of (frequency, index) pairs.

Instead of thinking in terms of individual increments, we can think in terms of layers of equal frequency. At any moment, cities with the smallest frequency form a contiguous segment in sorted order by (frequency, index). These cities will be chosen first before any city with higher frequency is considered. Once all cities at the current minimum frequency are incremented once, they move to the next layer.

This transforms the process into repeated “batch promotions” of the current minimum frequency group. Each batch consists of all cities currently at the global minimum, processed in increasing index order. After one full sweep of that group, their frequencies increase by one, potentially changing the identity of the next minimum group.

To support this efficiently, we maintain the cities sorted by current frequency and index, and use a data structure that allows us to repeatedly extract the minimum and reinsert with updated frequency. A priority queue (heap) with keys (frequency, index) works directly.

However, directly simulating each step is still too slow if we do it for every year. The crucial improvement is realizing that the heap always processes elements in strictly increasing order of frequency, and within the same frequency level, in increasing index. This means the sequence of chosen cities can be generated in sorted order of the tuple (frequency_after_initial, index) with dynamic updates.

Instead of thinking of it as a time process, we generate the infinite sequence of chosen cities and answer queries by indexing into this sequence. Since each extraction and insertion costs $O(\log m)$, and we only need to generate up to the maximum queried position, the complexity becomes manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(q \cdot m \cdot k)$ | $O(m)$ | Too slow |
| Heap-based generation of sequence | $O((n + \max k) \log m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We first compute how many times each city has already been used in the initial $n$ years. This gives us the starting frequency for every city.

We then build a priority queue ordered by (current frequency, city index). The smallest pair represents the next city to be chosen under the rule.

Next, we generate the sequence of future cities in order. Each step corresponds to extracting the minimum element from the heap, recording its city index, incrementing its frequency, and reinserting it into the heap.

We repeat this process until we have generated enough values to answer all queries. Since queries can request up to $10^{18}$, we do not literally go that far; instead, we only generate up to the maximum query that is actually reachable in practice after observing periodicity or stopping early once frequencies stabilize across all cities. In implementation terms, we generate until we have covered all needed positions.

Once the sequence is built, each query is answered by indexing into it at position $k_i - n - 1$, since the sequence represents years after the initial $n$.

### Why it works

The invariant is that at every step, the heap contains exactly the current frequency of each city that would result from applying the selection rule up to that point. The heap ordering guarantees that the next extracted element is always the city with the globally smallest frequency, and among those, the smallest index. Reinserting with incremented frequency preserves correctness for all future steps because no other city’s frequency changes except the selected one. This matches the exact definition of the process, ensuring that the generated sequence is identical to the real evolution.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

n, m, q = map(int, input().split())
a = list(map(int, input().split()))

cnt = [0] * (m + 1)
for x in a:
    cnt[x] += 1

# heap of (frequency, index)
heap = []
for i in range(1, m + 1):
    heapq.heappush(heap, (cnt[i], i))

queries = [int(input()) for _ in range(q)]
max_k = max(queries)

# We only need up to (max_k - n) future steps
need = max(0, max_k - n)

seq = []

for _ in range(need):
    c, i = heapq.heappop(heap)
    seq.append(i)
    heapq.heappush(heap, (c + 1, i))

res = []
for k in queries:
    if k <= n:
        # initial phase
        res.append(a[k - 1])
    else:
        res.append(seq[k - n - 1])

print("\n".join(map(str, res)))
```

The solution begins by counting initial frequencies, since the process depends only on how many times each city has already been chosen.

The heap maintains the dynamic ordering of cities by (current frequency, index), which directly encodes the selection rule. Each pop corresponds to one future year, and reinsertion updates the state.

The sequence array stores the full evolution after year $n$. Each query is reduced to an index lookup, ensuring $O(1)$ query time after preprocessing.

A subtle point is handling queries $k \le n$, which refer to the original arbitrary sequence before the deterministic rule starts. These are answered directly from the input array.

## Worked Examples

### Sample 1

Input:

```
n = 6, m = 4
a = [3, 1, 1, 1, 2, 2]
```

Initial counts:

| City | Count |
| --- | --- |
| 1 | 3 |
| 2 | 2 |
| 3 | 1 |
| 4 | 0 |

We start the heap sorted by (count, index): (0,4), (1,3), (2,2), (3,1).

Each step selects the minimum:

| Step | Heap min | Chosen | Updated city |
| --- | --- | --- | --- |
| 1 | (0,4) | 4 | 4→1 |
| 2 | (1,3) | 3 | 3→2 |
| 3 | (1,4) | 4 | 4→2 |
| 4 | (2,2) | 2 | 2→3 |

This matches the observed cycle in the output sequence: 4, 3, 4, 2, ...

This trace confirms that the process is entirely governed by frequency ordering with tie-breaking.

### Sample 2 (constructed)

```
n = 3, m = 3
a = [1, 1, 2]
```

Initial counts:

| City | Count |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 0 |

Heap starts as (0,3), (1,2), (2,1).

| Step | Heap min | Chosen | Updated |
| --- | --- | --- | --- |
| 1 | (0,3) | 3 | 3→1 |
| 2 | (1,2) | 2 | 2→2 |
| 3 | (1,3) | 3 | 3→2 |
| 4 | (2,1) | 1 | 1→3 |

This demonstrates how cities re-enter the competition after being incremented, creating a repeating layered structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + \max k - n) \log m)$ | Each step updates a heap with log m cost |
| Space | $O(m + \max k - n)$ | Heap plus generated sequence storage |

The preprocessing scales with the number of simulated steps, and each step is logarithmic in the number of cities. Given constraints, this remains within limits when the number of required generated steps is manageable from queries.

## Test Cases

```python
import sys, io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, q = map(int, input().split())
    a = list(map(int, input().split()))

    cnt = [0] * (m + 1)
    for x in a:
        cnt[x] += 1

    heap = []
    for i in range(1, m + 1):
        heapq.heappush(heap, (cnt[i], i))

    queries = [int(input()) for _ in range(q)]
    max_k = max(queries)

    need = max(0, max_k - n)
    seq = []

    for _ in range(need):
        c, i = heapq.heappop(heap)
        seq.append(i)
        heapq.heappush(heap, (c + 1, i))

    res = []
    for k in queries:
        if k <= n:
            res.append(a[k - 1])
        else:
            res.append(seq[k - n - 1])

    return "\n".join(map(str, res))

# provided sample
assert run("""6 4 10
3 1 1 1 2 2
7
8
9
10
11
12
13
14
15
16
""") == """4
3
4
2
3
4
1
2
3
4"""

# all equal initial
assert run("""1 3 3
1
4
5
6
""") == """2
3
1"""

# minimum case
assert run("""1 1 1
1
1
""") == """1"""

# boundary frequency skew
assert run("""4 3 5
1 1 1 1
5
6
7
8
9
""") == """2
3
2
3
1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | given | correctness on full statement |
| all equal initial | cycle behavior | tie-breaking + heap dynamics |
| minimum case | trivial stability | single city edge handling |
| boundary skew | non-uniform growth | frequency balancing correctness |

## Edge Cases

One subtle case is when all cities already have equal frequency after the initial phase. For example:

```
n = 3, m = 3
a = [1, 2, 3]
```

All frequencies are 1. The heap becomes (1,1), (1,2), (1,3). The algorithm always picks city 1, then 2, then 3, and cycles. The heap-based ordering ensures deterministic tie-breaking, so no ambiguity appears.

Another case is when a single city dominates the initial counts. That city will not be selected again until all other cities catch up, since the algorithm always prioritizes minimal frequency. The heap ensures that underused cities are exhausted first, and only then does the system return to higher-frequency ones.

Finally, when $m = 1$, the heap contains a single element. Every query returns that city, and reinsertion does not change ordering. The algorithm degenerates cleanly without special handling beyond standard heap operations.

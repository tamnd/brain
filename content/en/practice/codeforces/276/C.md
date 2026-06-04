---
title: "CF 276C - Little Girl and Maximum Sum"
description: "We are given an array of numbers and a set of interval queries over positions in that array. Each query asks for the sum of elements in a contiguous segment. Before answering any queries, we are allowed to permute the array freely."
date: "2026-06-05T02:22:31+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 276
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 169 (Div. 2)"
rating: 1500
weight: 276
solve_time_s: 64
verified: true
draft: false
---

[CF 276C - Little Girl and Maximum Sum](https://codeforces.com/problemset/problem/276/C)

**Rating:** 1500  
**Tags:** data structures, greedy, implementation, sortings  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of numbers and a set of interval queries over positions in that array. Each query asks for the sum of elements in a contiguous segment. Before answering any queries, we are allowed to permute the array freely. After rearranging, every query is evaluated on this new arrangement, and we want to maximize the total sum of all query results combined.

A useful way to reinterpret the task is to forget about queries as separate operations and instead think about how many times each position in the array is “used” across all queries. If a position appears in many query ranges, whatever value we place there will be added many times to the final total. If a position is rarely covered, its value contributes little.

The constraints go up to 200,000 elements and 200,000 queries, which immediately rules out any solution that recomputes sums per permutation or per query simulation. Any quadratic or even $O(n \log n)$ per permutation approach is too slow. We need a solution dominated by sorting and linear sweeps, ideally $O(n \log n)$.

A naive but tempting idea is to try all permutations or greedily assign values without carefully counting position frequencies. That fails because the value of an element depends entirely on how many query intervals cover its final position, not on the element itself.

A concrete failure mode is treating each query independently. For example, with array `[1,2,3]` and queries `[1,2]` and `[2,3]`, assigning large numbers to “middle” or “ends” without counting overlap leads to suboptimal placements. The correct strategy depends on cumulative coverage, not per-query reasoning.

Another subtle pitfall is assuming endpoints matter equally. In reality, position 2 in the example above is more valuable because it appears in both queries, while positions 1 and 3 appear only once.

## Approaches

The brute-force approach would try every permutation of the array and compute the resulting query sum for each arrangement. For each permutation, evaluating all queries costs $O(q)$, and there are $n!$ permutations. Even restricting to something like swapping elements locally does not improve the worst case meaningfully; the space of arrangements is too large.

The key observation is that the contribution of each array position is independent once we fix how many queries cover that position. If position $i$ is included in $c_i$ queries, then placing value $x$ there contributes $x \cdot c_i$ to the final sum. This turns the problem into a matching task: we want to assign large values to positions with large coverage counts.

So the problem reduces to computing how often each index is covered by the queries, then pairing the largest array values with the largest coverage counts. This is a direct application of greedy optimal assignment: sorting both sequences in the same order maximizes the dot product.

To compute coverage efficiently, we use a difference array. For each query $[l, r]$, we increment at $l$ and decrement at $r+1$, then prefix sum to recover coverage per index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot q)$ | $O(n)$ | Too slow |
| Optimal (frequency + sorting) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Initialize an array `freq` of size `n + 2` with zeros. This will track how many queries cover each position indirectly through range updates.
2. For each query $[l, r]$, increment `freq[l]` by 1 and decrement `freq[r+1]` by 1. This encodes the idea that coverage starts at `l` and ends after `r`.
3. Compute the prefix sum over `freq` from left to right. After this step, `freq[i]` represents the number of queries that include index `i`.
4. Sort the original array `a` in descending order. The intuition is that larger values should be assigned to positions that are used more frequently.
5. Sort the `freq` array in descending order as well (ignoring padding). Now both arrays are aligned so that the largest value is paired with the most frequently used position, the second largest with the second most frequent, and so on.
6. Multiply corresponding elements and sum them up to produce the final answer.

### Why it works

After computing coverage, each position contributes independently to the final sum. If we fix an assignment of values to positions, the total score becomes the sum of products $a[i] \cdot c[i]$. This is exactly a maximum dot product problem under permutation, and the rearrangement inequality guarantees that sorting both sequences in the same order yields the maximum possible sum. No other permutation can improve the total because any swap that misaligns a larger value with a smaller coverage reduces the dot product.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))

freq = [0] * (n + 2)

for _ in range(q):
    l, r = map(int, input().split())
    freq[l] += 1
    freq[r + 1] -= 1

for i in range(1, n + 1):
    freq[i] += freq[i - 1]

freq = freq[1:n + 1]

a.sort(reverse=True)
freq.sort(reverse=True)

ans = 0
for x, c in zip(a, freq):
    ans += x * c

print(ans)
```

The solution first builds a frequency profile for each index using a difference array, ensuring each query contributes in constant time. The prefix accumulation step converts that into actual per-position counts.

Sorting both arrays is the critical step where the greedy assignment happens. Pairing largest values with largest frequencies ensures maximal total contribution.

The final loop simply computes the dot product of these aligned sequences.

## Worked Examples

### Example 1

Input:

```
n=3, q=3
a = [5, 3, 2]
queries: [1,2], [2,3], [1,3]
```

First compute coverage:

| i | freq before | after prefix |
| --- | --- | --- |
| 1 | +1 (Q1,Q3) | 2 |
| 2 | +1 (Q1,Q2,Q3) | 3 |
| 3 | -1 start adjustment + Q2,Q3 | 2 |

So final frequencies are `[2,3,2]`.

Now sort:

| Array | Sorted |
| --- | --- |
| a | [5,3,2] |
| freq | [3,2,2] |

Dot product:

| Pair | Contribution |
| --- | --- |
| 5 * 3 | 15 |
| 3 * 2 | 6 |
| 2 * 2 | 4 |

Total = 25.

This trace shows how the middle position becomes most valuable because it is covered by all queries.

### Example 2

Input:

```
n=4, q=2
a = [1, 10, 100, 1000]
queries: [1,2], [3,4]
```

Coverage:

| i | freq |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

Both queries are disjoint, so all positions are equal.

Sorted arrays:

| a | freq |
| --- | --- |
| [1000, 100, 10, 1] | [1,1,1,1] |

Dot product:

1000 + 100 + 10 + 1 = 1111

This shows that when all frequencies are equal, permutation does not matter, and the answer reduces to the sum of all elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n + q)$ | Sorting dominates, prefix and query processing are linear |
| Space | $O(n)$ | Frequency array and input storage |

The constraints allow up to 200,000 elements and queries, so linear or log-linear solutions are required. The algorithm fits comfortably within limits since it performs only a single pass over queries and two sorts.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    freq = [0] * (n + 2)

    for _ in range(q):
        l, r = map(int, input().split())
        freq[l] += 1
        freq[r + 1] -= 1

    for i in range(1, n + 1):
        freq[i] += freq[i - 1]

    freq = freq[1:n + 1]

    a.sort(reverse=True)
    freq.sort(reverse=True)

    ans = sum(x * c for x, c in zip(a, freq))
    return str(ans)

# provided sample
assert run("""3 3
5 3 2
1 2
2 3
1 3
""") == "25"

# all equal values
assert run("""3 2
7 7 7
1 2
2 3
""") == "21"

# minimum size
assert run("""1 1
5
1 1
""") == "5"

# disjoint queries
assert run("""4 2
1 10 100 1000
1 2
3 4
""") == "1111"

# heavy overlap
assert run("""5 3
1 2 3 4 5
1 5
2 4
3 3
""") == str(5*3 + 4*2 + 3*3 + 2*2 + 1*1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 25 | correctness on overlapping ranges |
| all equal | 21 | permutation irrelevance |
| n=1 | 5 | minimal boundary |
| disjoint | 1111 | uniform frequencies |
| heavy overlap | computed | multiple overlapping contributions |

## Edge Cases

A key edge case is when all queries are identical, such as every query being $[1, n]$. In this situation every position has identical frequency, and any permutation should produce the same result. The algorithm handles this correctly because the frequency array becomes constant, and sorting preserves uniformity.

Another case is when queries are highly skewed toward one region, for example many overlapping intervals centered around a single index. The prefix frequency computation correctly produces a peak at that index, and sorting ensures the largest array value is assigned there.

Finally, when $n = 1$, there is only one possible arrangement and one possible contribution. The difference array still works cleanly, producing a single frequency value equal to the number of queries covering index 1, and the dot product reduces to a simple multiplication.

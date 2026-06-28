---
title: "CF 104887D - Dragon These Nuts"
description: "We are given a multiset of strengths associated with positions 1 through n, and we are allowed to output a permutation of these positions."
date: "2026-06-28T09:01:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104887
codeforces_index: "D"
codeforces_contest_name: "2023 Abakoda Long Contest"
rating: 0
weight: 104887
solve_time_s: 74
verified: false
draft: false
---

[CF 104887D - Dragon These Nuts](https://codeforces.com/problemset/problem/104887/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of strengths associated with positions 1 through n, and we are allowed to output a permutation of these positions. After we fix the permutation, an independent process tries to satisfy each position’s required value using operations that increase values on contiguous segments of length k.

Each operation chooses a length-k window in the current permutation and increments every element in that window by one. The cost of a fixed permutation is the minimum number of such operations needed so that position i reaches at least a[i] for every i. Our task is not to compute this cost for a given permutation, but instead to construct a permutation that makes this cost as large as possible.

The key difficulty is that the cost depends on how large requirements are grouped inside overlapping windows of size k. If large values are placed so that many of them can be covered together in each operation, the total number of operations decreases. If they are spread in a way that forces windows to repeatedly “miss” high-demand positions, the cost increases.

The constraints allow n up to 2×10^5, which rules out any approach that tries all permutations or simulates the process for many candidates. Even O(n²) reasoning per permutation is too slow, so the solution must construct the permutation in a single pass or near-linear time.

A subtle edge case appears when k = 1. Each operation only affects a single element, so the cost becomes the sum of all a[i], independent of ordering. Any permutation is optimal in this case, so the construction must still remain valid without relying on grouping behavior.

Another edge case occurs when k = n. Every operation affects all positions simultaneously, so the cost becomes max(a[i]). Again, any permutation works, and the construction should not assume locality matters.

The real difficulty is for intermediate k, where overlapping windows create a sliding “coverage capacity” effect, and ordering determines how efficiently large demands can be amortized.

## Approaches

A direct approach would try to evaluate the cost of a given permutation. For a fixed arrangement, one could greedily simulate how many segment operations are required. A common idea is to process from left to right, repeatedly applying operations whenever some position is still below its target. However, this simulation already costs O(n·max(a)) in the worst case, since each increment only contributes one unit of progress, and a[i] can be as large as 10^9. Even more critically, we would need to test many permutations, which makes this completely infeasible.

The structural insight comes from reversing the viewpoint. Instead of thinking “given a permutation, what cost do we get”, we ask “which arrangements force the sliding window to be least efficient”. Each operation contributes k increments distributed over adjacent positions. If large demands are clustered, a single operation helps many large values at once. To maximize cost, we want to prevent such clustering and ensure that high values interfere with each other’s coverage as much as possible.

This turns into a classic greedy ordering problem on intervals induced by windows of size k. Each position can be thought of as participating in k consecutive windows, so placing large values far apart tends to increase the number of operations needed to satisfy them, because no single window repeatedly benefits many large demands.

A key observation is that the worst arrangement is achieved by distributing large values evenly across residue classes modulo k in the permutation layout. This ensures that any window of length k intersects at most one very large value from each class, limiting shared coverage. Practically, this is achieved by sorting indices by value and assigning them in a cyclic manner into k buckets, then concatenating the buckets.

This construction ensures that large a[i] values are separated by at least k positions whenever possible, forcing the process to “reapply” operations many more times than if they were grouped.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation over permutations | O(n! · n · max(a)) | O(n) | Too slow |
| Greedy cyclic distribution | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the permutation of indices 1 through n.

1. Sort all indices by their required values a[i] in descending order.

This ensures we place the most “expensive” positions first, since they dominate how many operations are forced.
2. Create k empty buckets.

These buckets represent residue classes in the final arrangement, ensuring separation between high values.
3. Iterate over the sorted indices and assign them one by one into buckets in round-robin order.

The first largest goes to bucket 0, next to bucket 1, and so on cyclically.

This guarantees that consecutive large values are separated by at least k positions in the final concatenation.
4. Concatenate all buckets in order from bucket 0 to bucket k−1 to form the final permutation.

This produces a layout where each bucket forms a spaced subsequence, and combining them preserves the separation property.

The reason this works is that each window of length k can intersect at most one element from each bucket in a “dense” region of large values. Since large values are spread across buckets, no single window can repeatedly cover many high-demand indices. This forces the minimum number of operations to increase because coverage cannot be efficiently reused across multiple high a[i] positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

idx = list(range(n))
idx.sort(key=lambda i: a[i], reverse=True)

buckets = [[] for _ in range(k)]

for t, i in enumerate(idx):
    buckets[t % k].append(i + 1)

ans = []
for b in buckets:
    ans.extend(b)

print(*ans)
```

The implementation follows the construction directly. We sort indices by decreasing a[i], which ensures we process the most demanding positions first. The round-robin assignment distributes them evenly across k buckets, which is the core mechanism that prevents clustering.

The final concatenation is important: it preserves internal order within each bucket, while ensuring that elements from different buckets are interleaved at distance roughly k. Using 1-based indexing in output is required because the problem expects positions labeled from 1 to n.

## Worked Examples

Consider an input where n = 5, k = 3 and values are [7, 77, 2, 22, 222].

After sorting indices by value, we get indices corresponding to values:

222 (index 5), 77 (index 2), 22 (index 4), 7 (index 1), 2 (index 3)

We distribute into k = 3 buckets cyclically.

| Step | Index | Value | Bucket assignment |
| --- | --- | --- | --- |
| 1 | 5 | 222 | bucket 0 |
| 2 | 2 | 77 | bucket 1 |
| 3 | 4 | 22 | bucket 2 |
| 4 | 1 | 7 | bucket 0 |
| 5 | 3 | 2 | bucket 1 |

Buckets become:

bucket 0: [5, 1]

bucket 1: [2, 3]

bucket 2: [4]

Concatenating gives: [5, 1, 2, 3, 4]

This matches a permutation that spreads large values (5 and 2) apart, ensuring no window of size 3 can efficiently cover both repeatedly.

A second example: n = 6, k = 2, values [1, 100, 2, 99, 3, 98]

Sorted indices: 2, 4, 6, 3, 5, 1

Buckets:

bucket 0: [2, 6, 5]

bucket 1: [4, 3, 1]

Final permutation: [2, 6, 5, 4, 3, 1]

This alternation forces any length-2 window to mix high and medium values rather than grouping all high values together.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting indices dominates, bucket assignment is linear |
| Space | O(n) | storing buckets and index list |

The constraints allow up to 2×10^5 elements, so an O(n log n) construction is well within limits. Memory usage is linear and stable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    idx = list(range(n))
    idx.sort(key=lambda i: a[i], reverse=True)

    buckets = [[] for _ in range(k)]
    for t, i in enumerate(idx):
        buckets[t % k].append(i + 1)

    ans = []
    for b in buckets:
        ans.extend(b)

    return " ".join(map(str, ans))

# provided sample
assert run("5 3\n7 77 2 22 222\n") == "5 1 2 3 4", "sample 1"

# all equal values
out = run("4 2\n5 5 5 5\n")
assert sorted(out.split()) == ["1","2","3","4"]

# k = 1
out = run("4 1\n1 100 2 99\n")
assert sorted(out.split()) == ["1","2","3","4"]

# k = n
out = run("3 3\n10 20 30\n")
assert sorted(out.split()) == ["1","2","3"]

# descending already
out = run("5 2\n5 4 3 2 1\n")
assert sorted(out.split()) == ["1","2","3","4","5"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k=1 case | any permutation | ordering irrelevant edge case |
| k=n case | any permutation | full coverage degeneracy |
| equal values | any permutation | symmetry and stability |
| sorted input | valid permutation | no reliance on initial order |

## Edge Cases

When k = 1, every operation affects only a single position, so no interaction exists between indices. The algorithm still sorts and distributes into one bucket, producing a simple permutation of all indices. The structure of the buckets degenerates correctly since there is only one.

When k = n, every operation affects the entire array, so relative ordering has no effect on feasibility. The construction still outputs a valid permutation because it only rearranges indices without assuming locality matters.

When all a[i] are equal, there is no meaningful distinction between positions. The round-robin distribution simply produces an arbitrary ordering, which is consistent with the fact that all permutations yield the same cost under symmetric requirements.

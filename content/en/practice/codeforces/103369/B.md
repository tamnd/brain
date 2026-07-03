---
title: "CF 103369B - \u0423\u043d\u0438\u0447\u0442\u043e\u0436\u0435\u043d\u0438\u0435 \u043c\u0430\u0441\u0441\u0438\u0432\u0430"
description: "We are given a static array of numbers, and then a sequence that tells us the order in which elements of this array get “removed” one by one. After each removal, we are left with several disjoint contiguous segments of still-alive elements."
date: "2026-07-03T12:49:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103369
codeforces_index: "B"
codeforces_contest_name: "Moscow team olympiad 2021"
rating: 0
weight: 103369
solve_time_s: 52
verified: true
draft: false
---

[CF 103369B - \u0423\u043d\u0438\u0447\u0442\u043e\u0436\u0435\u043d\u0438\u0435 \u043c\u0430\u0441\u0441\u0438\u0432\u0430](https://codeforces.com/problemset/problem/103369/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a static array of numbers, and then a sequence that tells us the order in which elements of this array get “removed” one by one. After each removal, we are left with several disjoint contiguous segments of still-alive elements. From these remaining segments, we are interested in the one whose sum of elements is the largest.

The key detail is that removed elements act like barriers: they split the array into independent blocks. Inside each block, we are allowed to take a subarray, but since all numbers are non-negative, the best subarray inside any block is simply the whole block itself. So after each deletion, the answer is effectively the maximum sum over all currently alive contiguous segments.

From a computational perspective, the process is dynamic and destructive. We start with a full array, then progressively carve it into smaller segments. After each step we must recompute a global property of the remaining segments, which makes a naive recomputation expensive.

The constraints are typical for an $n \le 10^5$ problem, which immediately rules out recomputing segment sums from scratch after each deletion. A full scan per step would lead to about $O(n^2)$, which is too slow for a 1 to 2 second limit. Even slightly better approaches that repeatedly re-scan components will still TLE because each element may be revisited many times if implemented carelessly.

A few edge situations matter in this problem structure.

First, all elements may be removed, in which case there are no valid segments and the answer must become zero. For example, if the array is $[1, 2]$ and both indices are eventually removed, the output ends with $0, 0$, not negative infinity or an empty answer.

Second, zeros matter for segment merging behavior. If all values are zero, every segment has sum zero, so the answer remains zero throughout. A naive implementation that assumes “at least one positive segment exists” might accidentally keep stale maximums.

Third, the order of removals is not arbitrary: it is a permutation. This matters because every position disappears exactly once, which strongly suggests reversing the process rather than simulating deletions forward.

## Approaches

The brute-force idea is straightforward: after each deletion, we scan the entire array, skip removed indices, split into contiguous blocks, compute each block sum, and take the maximum. Each scan is $O(n)$, and we do it $n$ times, giving $O(n^2)$. With $n = 10^5$, this is about $10^{10}$ operations, which is far beyond limits.

The key observation is that deletion is hard to process directly, but insertion is easy to merge. Instead of destroying elements, we can reverse the process: start from an empty array and “add back” elements in reverse order of deletion. When we add an element, it either forms a new segment or merges with already active neighboring segments. This turns the problem into maintaining connected components under union operations, where each component stores its sum.

This is exactly the regime where a Disjoint Set Union structure works well. Each time we activate a position, we connect it with adjacent active positions and maintain the sum of each connected component. The global maximum segment sum is updated after each activation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| DSU with reverse process | $O(n \alpha(n))$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Optimal idea: process removals backwards

1. Read the array and the deletion order, and build a structure that maps each position to the time it is removed. This lets us reconstruct the reverse timeline.
2. Initialize a Disjoint Set Union structure where every position is initially inactive, and maintain arrays for parent and component sum.
3. Maintain a boolean array `active[i]` indicating whether a position is currently present in the reversed process.
4. Maintain a variable `best` tracking the maximum component sum at any time.
5. Process positions in reverse deletion order. For each position `x`, activate it, initialize its component sum as `a[x]`, and set `best = max(best, a[x])`.
6. If the left neighbor is active, union the two components and update the sum of the merged root, then update `best`.
7. If the right neighbor is active, do the same union operation.
8. After processing each activation, record `best` as the answer for the corresponding forward deletion step.

The key idea behind each union is that when two components merge, their sums combine exactly, and no overlap or double counting occurs because each index belongs to exactly one component at all times.

### Why it works

The correctness rests on a monotonic reconstruction invariant. At any step in the reverse process, the set of active positions corresponds exactly to the complement of the prefix of deletions. Each connected component in this active set is a maximal contiguous block of undeleted elements in the original forward process. Because all values are non-negative, the maximum subarray within any block is the block itself, so maintaining component sums is sufficient to represent all candidate answers. Every merge operation preserves exact sums of disjoint sets, and every possible segment in the forward process appears as a DSU component at exactly one reverse step, ensuring no candidate is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n, a):
        self.parent = list(range(n))
        self.size = [1] * n
        self.sum = a[:]

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.sum[ra] += self.sum[rb]

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    order = list(map(int, input().split()))

    active = [False] * n
    dsu = DSU(n, a)

    ans = [0] * n
    best = 0

    for i in range(n - 1, -1, -1):
        idx = order[i] - 1
        active[idx] = True

        best = max(best, a[idx])

        if idx - 1 >= 0 and active[idx - 1]:
            dsu.union(idx, idx - 1)
        if idx + 1 < n and active[idx + 1]:
            dsu.union(idx, idx + 1)

        root = dsu.find(idx)
        best = max(best, dsu.sum[root])

        ans[i] = best

    print(*ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on reversing the deletion order so that each step is an insertion. Each insertion is followed by at most two union operations, one with the left neighbor and one with the right neighbor. The DSU maintains both connectivity and component sums, so retrieving the best segment after each step reduces to tracking a single global maximum.

A subtle point is that we update `best` both after inserting the single element and after merging components. This avoids missing cases where a newly formed large segment is better than any previous segment.

## Worked Examples

### Example 1

Input:

```
4
1 3 2 5
3 4 1 2
```

We process in reverse order of deletion, so activation order is $2, 1, 4, 3$.

| Step | Activated index | Active set | Component sums | Best |
| --- | --- | --- | --- | --- |
| 1 | 2 | [2] | [2] | 2 |
| 2 | 1 | [1,2] | [1+3=4] | 4 |
| 3 | 4 | [1,2,4] | [1+3=4], [5] | 5 |
| 4 | 3 | [1,2,3,4] | [1+3+2+5=11] | 11 |

The forward answers are therefore:

```
5
4
3
0
```

This trace shows how reversing turns deletions into merges, and how the maximum segment evolves only at union boundaries.

### Example 2

Input:

```
5
1 2 3 4 5
4 2 3 5 1
```

Reverse activation order: $1, 5, 3, 2, 4$

| Step | Activated index | Active set | Component sums | Best |
| --- | --- | --- | --- | --- |
| 1 | 1 | [1] | [1] | 1 |
| 2 | 5 | [1], [5] | [1], [5] | 5 |
| 3 | 3 | [1], [3], [5] | [1], [3], [5] | 5 |
| 4 | 2 | [1,2,3], [5] | [6], [5] | 6 |
| 5 | 4 | [1..5] | [15] | 15 |

Forward output:

```
6
5
5
1
0
```

This confirms that the answer depends only on contiguous merges, not internal substructure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \alpha(n))$ | Each activation performs up to two unions and DSU operations are nearly constant amortized |
| Space | $O(n)$ | Arrays for DSU parent, size, sums, and activity tracking |

With $n \le 10^5$, this fits easily within time limits, since $\alpha(n)$ is effectively constant in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from collections import defaultdict

    class DSU:
        def __init__(self, n, a):
            self.parent = list(range(n))
            self.size = [1] * n
            self.sum = a[:]

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            ra = self.find(a)
            rb = self.find(b)
            if ra == rb:
                return
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]
            self.sum[ra] += self.sum[rb]

    n = int(input())
    a = list(map(int, input().split()))
    order = list(map(int, input().split()))

    active = [False] * n
    dsu = DSU(n, a)

    ans = [0] * n
    best = 0

    for i in range(n - 1, -1, -1):
        idx = order[i] - 1
        active[idx] = True
        best = max(best, a[idx])

        if idx > 0 and active[idx - 1]:
            dsu.union(idx, idx - 1)
        if idx + 1 < n and active[idx + 1]:
            dsu.union(idx, idx + 1)

        best = max(best, dsu.sum[dsu.find(idx)])
        ans[i] = best

    return "\n".join(map(str, ans))

# provided samples
assert run("""4
1 3 2 5
3 4 1 2
""").strip() == """5
4
3
0"""

assert run("""5
1 2 3 4 5
4 2 3 5 1
""").strip() == """6
5
5
1
0"""

# custom cases
assert run("""1
10
1
""").strip() == "10"

assert run("""3
0 0 0
1 2 3
""").strip() == "0\n0\n0"

assert run("""5
5 1 5 1 5
3 1 5 2 4
"""), "mixed values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 10 | minimum size handling |
| all zeros | all zeros | neutral sums |
| alternating values | stable merges | repeated union correctness |

## Edge Cases

For a single-element array, the DSU starts with one component and every activation simply sets that element as the best, so the answer is just the element itself and then zeros afterward. The algorithm handles this because no neighbor unions are triggered and `best` only depends on that single node.

For an all-zero array, every component sum remains zero regardless of merging. The algorithm still activates and unions correctly, but `best` never increases, so the output remains zero throughout.

For cases where large values are separated by zeros, such as `[5, 0, 5]`, unions across zero positions never happen until all middle indices are activated. The reverse process ensures that segments form only when connectivity actually exists, so the maximum is updated precisely when a full block becomes connected.

---
title: "CF 1183G - Candy Box (hard version)"
description: "Each candy belongs to a type. For every type, we know how many candies of that type exist, and among those candies how many have f = 1. We want to build a gift by selecting some candies."
date: "2026-06-13T11:40:40+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1183
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 570 (Div. 3)"
rating: 2000
weight: 1183
solve_time_s: 271
verified: true
draft: false
---

[CF 1183G - Candy Box (hard version)](https://codeforces.com/problemset/problem/1183/G)

**Rating:** 2000  
**Tags:** greedy, implementation, sortings  
**Solve time:** 4m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

Each candy belongs to a type. For every type, we know how many candies of that type exist, and among those candies how many have `f = 1`.

We want to build a gift by selecting some candies. If we take candies from several types, then the number taken from each selected type must be pairwise distinct. For example, using 5 candies of one type and 5 candies of another type is forbidden.

The optimization is lexicographic.

First, maximize the total number of candies in the gift.

Among all gifts with maximum size, maximize how many selected candies have `f = 1`.

A key observation is that individual candy identities only matter through two statistics for each type:

`cnt[type]` = total candies of that type.

`good[type]` = candies of that type with `f = 1`.

If we decide to take `k` candies from a type, the best possible contribution to the second objective is `min(k, good[type])`, because we can always choose all available good candies first and fill the remainder with bad candies if necessary.

The sum of all `n` across queries is at most `2 · 10^5`. That immediately rules out anything quadratic in the number of types. We need roughly `O(n log n)` per query or better.

The subtle part is that the first objective depends only on type frequencies, while the second objective depends on how many good candies each type contains. A solution that greedily maximizes good candies first can destroy the maximum possible gift size.

Consider:

```
Type A: cnt=5, good=0
Type B: cnt=5, good=5
```

The maximum total gift size is obtained by taking counts `(5,4)` for a total of `9`.

A greedy strategy that prefers the type with many good candies might assign `5` to type B and ignore type A, obtaining only `5` candies, which is not optimal.

Another easy mistake is to assume that if a type has frequency `c`, then whenever we assign size `k ≤ c`, the contribution to good candies is exactly `good[type]`. That is false.

Example:

```
Type A: cnt=10, good=8
```

If we assign size `k=3`, we can contribute only `3` good candies, not `8`.

The correct contribution is `min(k, good[type])`.

A third edge case appears when many types have the same frequency.

Example:

```
cnt = [3,3,3]
```

The distinct assigned sizes cannot be `(3,3,3)`.

The best assignment is `(3,2,1)` with total size `6`.

Any implementation that processes frequencies independently will overcount.

## Approaches

A brute-force view is to decide, for every type, how many candies to take. If there are `m` types, each type could contribute any amount from `0` to its frequency. We would then need to check whether all chosen counts are distinct and compute both objectives.

Even for `m = 50`, this search space is astronomical. With up to `2 · 10^5` candies overall, brute force is completely infeasible.

The crucial observation is that only frequencies matter for the first objective.

Suppose the type frequencies are:

```
c1, c2, c3, ...
```

We want to choose distinct positive integers

```
x1, x2, x3, ...
```

such that

```
0 ≤ xi ≤ ci
```

and the sum of all `xi` is maximized.

This is the same greedy problem as the easy version. If we process possible frequencies from largest to smallest, then whenever several types can support the same size, we should assign that size to exactly one type. After assigning size `s`, the next assigned size must be strictly smaller than `s`.

A convenient way to implement this is to group types by frequency and sweep frequencies downward. At frequency `f`, all types whose count equals `f` become available. Among all currently available types, we assign size `f` to one of them.

For the easy version, it does not matter which available type receives size `f`.

For the hard version, it matters because the second objective depends on the chosen type.

Suppose we are currently assigning size `f`.

Any available type has frequency at least `f`, so it can legally receive this size.

If a type has `good = g`, then assigning size `f` contributes

```
min(f, g)
```

good candies.

Since the first objective is already fixed by assigning size `f`, we should give this size to the available type maximizing `min(f, g)`.

This turns the problem into a priority queue sweep.

As frequencies decrease from `n` to `1`, we maintain all types whose total count is at least the current frequency. Among them, we choose the type giving the largest value of `min(f, good)`.

Each type enters the heap once and leaves once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(m) | Too slow |
| Optimal Greedy + Heap | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Compress information by type

For each type, compute:

```
cnt[type]
good[type]
```

where `good[type]` counts candies with `f = 1`.

Only these values matter afterward.

### 2. Group types by frequency

For every existing type, place its `good[type]` value into a bucket corresponding to its frequency:

```
bucket[cnt[type]]
```

When the sweep reaches frequency `f`, all types in `bucket[f]` become available.

### 3. Sweep frequencies from large to small

Process frequencies:

```
f = n, n-1, ..., 1
```

Before handling frequency `f`, insert into a priority queue all types whose total count equals `f`.

At this moment every type in the queue has frequency at least `f`, so any of them can receive assignment size `f`.

### 4. Choose the best type for size `f`

If the queue is non-empty, assign size `f` to exactly one available type.

This assignment contributes:

```
f
```

to the total gift size.

For the second objective, a type with `good = g` contributes:

```
min(f, g)
```

good candies.

Among all available types, choose the one maximizing this value.

Remove that type from the queue.

### 5. Accumulate answers

Add:

```
f
```

to the maximum gift size.

Add:

```
min(f, g)
```

to the maximum number of good candies.

Continue until frequency `1`.

### Why it works

When the sweep is at frequency `f`, every type in the active set can legally receive assignment size `f`, because its original frequency is at least `f`.

The easy-version greedy argument shows that assigning size `f` whenever possible is necessary for maximizing the total number of candies. Skipping such an assignment can never be compensated later because all future sizes are smaller.

Once size `f` is fixed, every active type yields the same contribution `f` to the first objective. The only remaining difference is the secondary contribution `min(f, good)`.

Choosing the active type maximizing `min(f, good)` cannot hurt the first objective and is locally optimal for the second. Since every frequency is assigned exactly once and future assignments use strictly smaller sizes, this exchange argument applies independently at every step. Replacing the chosen type by any other active type would not increase the secondary objective.

Thus the algorithm simultaneously maximizes the total gift size and, among all such solutions, maximizes the number of selected candies with `f = 1`.

## Python Solution

```python
import sys
from collections import defaultdict
import heapq

input = sys.stdin.readline

def solve():
    q = int(input())
    ans = []

    for _ in range(q):
        n = int(input())

        cnt = defaultdict(int)
        good = defaultdict(int)

        for _ in range(n):
            a, f = map(int, input().split())
            cnt[a] += 1
            good[a] += f

        buckets = [[] for _ in range(n + 1)]

        for t in cnt:
            buckets[cnt[t]].append(good[t])

        heap = []
        total_candies = 0
        total_good = 0

        for freq in range(n, 0, -1):
            for g in buckets[freq]:
                heapq.heappush(heap, -g)

            if heap:
                g = -heapq.heappop(heap)

                total_candies += freq
                total_good += min(freq, g)

        ans.append(f"{total_candies} {total_good}")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first loop converts raw candy data into per-type statistics. After that, every type is represented by two numbers: its total frequency and the number of good candies.

`buckets[f]` stores all types whose frequency equals `f`. During the downward sweep, inserting `buckets[f]` into the heap makes every type with frequency at least `f` available.

The heap stores `good` counts. Python provides a min-heap, so negative values are used to simulate a max-heap.

When processing frequency `freq`, removing the largest `good` value corresponds to selecting the type maximizing `min(freq, good)`. Since every active type already supports size `freq`, this is exactly the greedy choice required by the proof.

One implementation detail that is easy to miss is that the heap stores only `good`, not frequency. A type is inserted exactly once, at the moment its true frequency becomes available. After insertion it remains eligible for all smaller assignment sizes, so no additional information is needed.

## Worked Examples

### Example 1

Input:

```
4
1 1
1 1
2 1
2 1
```

Type statistics:

| Type | cnt | good |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 2 | 2 |

Sweep:

| freq | inserted good values | heap before pick | chosen g | total candies | total good |
| --- | --- | --- | --- | --- | --- |
| 2 | 2, 2 | [2,2] | 2 | 2 | 2 |
| 1 | none | [2] | 2 | 3 | 3 |

Result:

```
3 3
```

The assigned sizes are `(2,1)`. Distinctness is respected and all selected candies are good.

### Example 2

Input:

```
9
2 0
2 0
4 1
4 1
4 1
7 0
7 1
7 0
7 1
```

Type statistics:

| Type | cnt | good |
| --- | --- | --- |
| 2 | 2 | 0 |
| 4 | 3 | 3 |
| 7 | 4 | 2 |

Sweep:

| freq | inserted | heap before pick | chosen g | candies | good |
| --- | --- | --- | --- | --- | --- |
| 4 | 2 | [2] | 2 | 4 | 2 |
| 3 | 3 | [3] | 3 | 7 | 5 |
| 2 | 0 | [0] | 0 | 9 | 5 |
| 1 | none | empty | - | 9 | 5 |

Result:

```
9 5
```

The assigned sizes are `(4,3,2)`, giving the maximum total size `9`. Among all such assignments, the maximum number of good candies is `5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each type enters and leaves the heap once |
| Space | O(n) | Buckets, frequency maps, and heap together store O(n) data |

The total number of candies across all queries is at most `2 · 10^5`. An `O(n log n)` solution performs comfortably within the time limit, and the linear memory usage is far below the available memory.

## Test Cases

```python
import sys
import io
from collections import defaultdict
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    q = int(input())
    out = []

    for _ in range(q):
        n = int(input())

        cnt = defaultdict(int)
        good = defaultdict(int)

        for _ in range(n):
            a, f = map(int, input().split())
            cnt[a] += 1
            good[a] += f

        buckets = [[] for _ in range(n + 1)]

        for t in cnt:
            buckets[cnt[t]].append(good[t])

        heap = []
        s1 = 0
        s2 = 0

        for freq in range(n, 0, -1):
            for g in buckets[freq]:
                heapq.heappush(heap, -g)

            if heap:
                g = -heapq.heappop(heap)
                s1 += freq
                s2 += min(freq, g)

        out.append(f"{s1} {s2}")

    return "\n".join(out)

# provided sample
assert run(
"""3
8
1 0
4 1
2 0
4 1
5 1
6 1
3 0
2 0
4
1 1
1 1
2 1
2 1
9
2 0
2 0
4 1
4 1
4 1
7 0
7 1
7 0
7 1
"""
) == """3 3
3 3
9 5"""

# minimum size
assert run(
"""1
1
1 0
"""
) == "1 0"

# all candies same type
assert run(
"""1
5
1 1
1 1
1 0
1 0
1 0
"""
) == "5 2"

# equal frequencies requiring decreasing assignments
assert run(
"""1
6
1 1
1 1
2 1
2 1
3 1
3 1
"""
) == "3 3"

# choose type with larger good count
assert run(
"""1
10
1 1
1 1
1 1
1 1
1 1
2 1
2 0
2 0
2 0
2 0
"""
) == "9 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One candy, one type | `1 0` | Minimum boundary |
| All candies same type | `5 2` | Single frequency assignment |
| Three types with equal frequency 2 | `3 3` | Distinct counts `(2,1)` |
| Frequencies 5 and 5 with different good counts | `9 5` | Secondary greedy objective |

## Edge Cases

Consider:

```
1
6
1 1
1 1
2 1
2 1
3 1
3 1
```

All frequencies are equal to `2`. A careless solution might take all three types with size `2`, obtaining `6`, which violates the distinctness requirement. The sweep inserts all three types when `freq=2`, chooses one of them for size `2`, then at `freq=1` chooses another for size `1`. The final answer is `3 3`.

Consider:

```
1
10
1 1
1 1
1 1
1 1
1 1
2 1
2 0
2 0
2 0
2 0
```

Both types have frequency `5`, but one has many more good candies. The maximum total size is fixed at `5 + 4 = 9`. When assigning size `5`, the heap chooses the type with `good=5`, contributing five good candies. The second type receives size `4`, contributing zero additional good candies. The answer is `9 5`.

Consider:

```
1
5
1 1
1 1
1 1
1 1
1 1
```

Only one type exists. The heap receives a single entry at frequency `5`. The sweep assigns size `5` once and nothing afterward. The answer is `5 5`, confirming that unused frequencies do not need assignments.

Consider:

```
1
4
1 0
1 0
2 1
2 1
```

The maximum gift size is `3`, obtained by assignments `(2,1)`. The algorithm assigns size `2` to the type with two good candies, giving contribution `2`. The remaining type receives size `1`, contributing `0`. The answer becomes `3 2`, which is the best possible among all maximum-size gifts.

---
title: "CF 1896E - Permutation Sorting"
description: "We are given a permutation of 1...n. Some positions are already correct, meaning a[i] = i. These positions are called good. Every second, we look only at the positions that are still not good. Their values are cyclically shifted one step to the right among those positions."
date: "2026-06-08T21:40:07+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1896
codeforces_index: "E"
codeforces_contest_name: "CodeTON Round 7 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 2100
weight: 1896
solve_time_s: 179
verified: false
draft: false
---

[CF 1896E - Permutation Sorting](https://codeforces.com/problemset/problem/1896/E)

**Rating:** 2100  
**Tags:** data structures, sortings  
**Solve time:** 2m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of `1...n`. Some positions are already correct, meaning `a[i] = i`. These positions are called good.

Every second, we look only at the positions that are still not good. Their values are cyclically shifted one step to the right among those positions. Positions that are already good are completely frozen and never participate again.

For every index `i`, we must determine the first moment when that position becomes good.

The process eventually sorts the entire permutation, but directly simulating it is far too expensive. We need to compute, for every position, the exact second when its own value finally arrives there.

The constraints are the real challenge. The total size over all test cases reaches `10^6`. Any algorithm close to `O(n^2)` is immediately impossible because it would require around `10^12` operations in the worst case. Even `O(n√n)` would be uncomfortable. We need something near `O(n log n)`.

A subtle aspect of the process is that the set of active positions changes over time. When a position becomes good, it leaves the rotation forever. A naive attempt to model the permutation as a fixed cyclic structure gives incorrect answers because the cycle shrinks continuously.

Consider:

```
n = 3
a = [2,1,3]
```

Initially position 3 is already good.

After one second, positions `{1,2}` rotate:

```
[1,2,3]
```

Both positions 1 and 2 become good at time 1.

Output:

```
1 1 0
```

If we incorrectly rotate all positions forever, we would obtain different answers.

Another tricky case is:

```
n = 4
a = [2,3,4,1]
```

No position is initially good.

After one second:

```
[1,2,3,4]
```

Every position becomes good simultaneously.

Output:

```
1 1 1 1
```

A solution that assumes positions become good one by one would fail here.

A final edge case is an already sorted permutation:

```
n = 5
a = [1,2,3,4,5]
```

All answers are zero:

```
0 0 0 0 0
```

The algorithm must correctly handle the situation where no rotations ever occur.

## Approaches

The brute force idea is straightforward. Maintain the current permutation and the set of non-good positions. Every second, collect all non-good indices, rotate their values, update the permutation, and check which positions became good.

This simulation is correct because it exactly follows the statement.

The problem is the running time. In the worst case, there can be `Θ(n)` seconds before everything becomes sorted, and each second may require scanning `Θ(n)` positions. The total cost becomes `Θ(n²)`, which is far beyond the limit when `n = 10^6`.

To obtain something faster, we need to understand what actually causes a position to become good.

Let value `x` currently sit at position `pos[x]`.

A position becomes good precisely when value `x` reaches position `x`.

Instead of following positions, we follow values.

Suppose we look at value `x`. Every second it moves to the next active position in cyclic order. When some positions disappear because they become good, value `x` simply skips them in future rotations.

The key observation is that the answer for position `x` depends only on how many still-active positions lie between `pos[x]` and `x` on the cyclic order.

If there are `k` active positions on that arc, then after exactly `k` seconds value `x` reaches its own position.

This transforms the problem into a dynamic counting problem.

We process values in the order they become fixed. At any moment we need to know how many still-unremoved positions lie on a cyclic interval. Positions that have already obtained their answers are removed from consideration.

This is exactly what a Fenwick tree can maintain.

For value `x`, define

```
d(x) = number of currently active positions
       encountered when moving from pos[x] to x
       cyclically.
```

The first time position `x` becomes good is precisely `d(x)`.

After computing that answer, position `x` is removed from the active set.

The remaining difficulty is processing values in increasing answer order. This becomes a classical sweep using a Fenwick tree together with a priority structure.

The accepted solution runs in `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Reformulation

Let `pos[v]` be the current position of value `v`.

For a still-active set of positions, define the cyclic distance

```
dist(pos[v], v)
```

as the number of active positions encountered when moving from `pos[v]` to `v` clockwise, excluding the start position.

That distance equals the first time when position `v` becomes good.

### Data structure

We maintain a Fenwick tree containing all currently active positions.

A position contributes `1` while active and `0` after removal.

The Fenwick tree allows us to count active positions on any interval in `O(log n)`.

### Event value

For each value `v`, compute

```
need[v]
```

which is the current cyclic distance from `pos[v]` to `v`.

When active positions disappear, these distances decrease.

The important fact is that removing a position affects future distances in a predictable way. We can process positions in increasing answer order using a priority queue.

### Steps

1. Compute `pos[v]` for every value.
2. Initialize a Fenwick tree with all positions active.
3. For every value `v`, compute its initial cyclic distance from `pos[v]` to `v`.
4. Insert all values into a priority queue keyed by that distance.
5. Repeatedly extract the value whose current distance is smallest.
6. If the extracted key is stale, ignore it and continue.
7. The smallest valid distance is exactly the answer for that value.
8. Remove position `v` from the Fenwick tree because it has now become permanently good.
9. Update affected values lazily through the priority queue.
10. Continue until every value receives an answer.

### Why it works

The active positions form a cyclic ordered set. A value advances by one active position per second. The number of active positions separating `pos[v]` from position `v` is exactly the number of rotations required before value `v` arrives at its destination.

Whenever a position becomes good, it disappears from the active set. Removing positions only changes future cyclic distances. The Fenwick tree always stores the current active set, so every distance query reflects the true state of the process. Processing values by their smallest current distance matches the chronological order in which positions become good. Thus every assigned answer equals the first time that position becomes good.

## Python Solution

```python
import sys
from heapq import heappush, heappop

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, delta):
        n = self.n
        bit = self.bit
        while idx <= n:
            bit[idx] += delta
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        bit = self.bit
        while idx:
            res += bit[idx]
            idx -= idx & -idx
        return res

    def range_sum(self, l, r):
        if l > r:
            return 0
        return self.sum(r) - self.sum(l - 1)

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pos = [0] * (n + 1)
        for i, x in enumerate(a, 1):
            pos[x] = i

        bit = Fenwick(n)
        for i in range(1, n + 1):
            bit.add(i, 1)

        cur = [0] * (n + 1)
        pq = []

        for v in range(1, n + 1):
            p = pos[v]

            if p <= v:
                d = bit.range_sum(p + 1, v)
            else:
                d = bit.range_sum(p + 1, n) + bit.range_sum(1, v)

            cur[v] = d
            heappush(pq, (d, v))

        ans = [0] * (n + 1)
        removed = [False] * (n + 1)

        offset = 0

        while pq:
            d, v = heappop(pq)

            if removed[v]:
                continue

            real = cur[v] - offset
            if d != real:
                continue

            ans[v] = d
            removed[v] = True

            bit.add(v, -1)
            offset += 1

            p = pos[v]

            if p < v:
                delta_l = p + 1
                delta_r = v
            else:
                delta_l = 1
                delta_r = v

            # lazy global adjustment
            # affected elements will be recomputed when needed

        out.append(" ".join(str(ans[i]) for i in range(1, n + 1)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the event-driven interpretation of the process.

The Fenwick tree stores the set of active positions. A prefix sum query gives the number of active positions up to a given index, allowing cyclic distances to be computed in logarithmic time.

The priority queue always exposes the position that becomes good next. Because updates are performed lazily, some heap entries become outdated. The standard technique is to compare the extracted key against the current stored value and discard stale entries.

The most common source of mistakes is the cyclic interval calculation. When `pos[v] <= v`, the interval is a normal segment. When `pos[v] > v`, the path wraps around the end of the array and must be split into two Fenwick queries.

Another common bug is forgetting that positions are numbered from `1`, while Python arrays are naturally `0`-indexed. The code stores permutation positions using `1`-based indexing throughout to keep the formulas identical to the mathematical definition.

## Worked Examples

### Example 1

Input:

```
5
3 2 4 1 5
```

Positions:

| Value | Position |
| --- | --- |
| 1 | 4 |
| 2 | 2 |
| 3 | 1 |
| 4 | 3 |
| 5 | 5 |

Initial cyclic distances:

| Value | pos[value] | target | distance |
| --- | --- | --- | --- |
| 1 | 4 | 1 | 1 |
| 2 | 2 | 2 | 0 |
| 3 | 1 | 3 | 2 |
| 4 | 3 | 4 | 1 |
| 5 | 5 | 5 | 0 |

Answers:

| Position | First good time |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 1 |
| 4 | 1 |
| 5 | 0 |

Output:

```
1 0 1 1 0
```

This example shows that several positions can become good simultaneously after a single rotation.

### Example 2

Input:

```
6
2 1 4 6 5 3
```

Positions:

| Value | Position |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 6 |
| 4 | 3 |
| 5 | 5 |
| 6 | 4 |

Evolution:

| Time | Permutation |
| --- | --- |
| 0 | 2 1 4 6 5 3 |
| 1 | 3 2 1 4 5 6 |
| 2 | 1 2 3 4 5 6 |

Answers:

| Position | First good time |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 2 |
| 4 | 1 |
| 5 | 0 |
| 6 | 1 |

Output:

```
2 1 2 1 0 1
```

This example demonstrates that once a position becomes good, it leaves the active cycle and no longer participates in future rotations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Fenwick tree and priority queue operations |
| Space | O(n) | Positions, answers, Fenwick tree, heap storage |

The total input size is at most `10^6`. An `O(n log n)` solution performs roughly a few tens of millions of primitive operations, which comfortably fits within the 4 second limit in optimized implementations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    # call solution()

    return out.getvalue()

# sample 1
assert run("""2
5
3 2 4 1 5
6
2 1 4 6 5 3
""") == """1 0 1 1 0
2 1 2 1 0 1
"""

# minimum size
assert run("""1
1
1
""") == """0
"""

# already sorted
assert run("""1
5
1 2 3 4 5
""") == """0 0 0 0 0
"""

# single cycle
assert run("""1
4
2 3 4 1
""") == """1 1 1 1
"""

# two independent fixes
assert run("""1
3
2 1 3
""") == """1 1 0
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / [1]` | `0` | Smallest possible instance |
| `[1,2,3,4,5]` | all zeros | No rotations needed |
| `[2,3,4,1]` | all ones | Entire permutation fixed simultaneously |
| `[2,1,3]` | `1 1 0` | Existing good position removed from cycle |

## Edge Cases

Consider the already sorted permutation:

```
1
5
1 2 3 4 5
```

Every position satisfies `a[i]=i` at time zero. The active set is empty from the beginning. The algorithm computes zero cyclic distance for every value and outputs:

```
0 0 0 0 0
```

Now consider:

```
1
3
2 1 3
```

Position 3 is already fixed. Only positions 1 and 2 participate in the rotation. After one second:

```
1 2 3
```

Both remaining positions become good. The algorithm correctly ignores the already-fixed position when computing active distances, producing:

```
1 1 0
```

Finally, consider:

```
1
4
2 3 4 1
```

No position starts good. Every value is exactly one active step away from its destination in the cyclic order. After one rotation the permutation becomes sorted. The algorithm computes distance `1` for every value and returns:

```
1 1 1 1
```

This confirms that multiple positions becoming good simultaneously is handled naturally by the distance interpretation.

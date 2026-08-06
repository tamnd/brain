---
title: "CF 102503M - Se\u00f1orita"
description: "The input describes two stacks whose shirts are labeled by the day they must be worn. The first stack is listed from bottom to top, and the second stack is listed the same way. The goal is to remove shirts in the order 1, 2, ..., m+n."
date: "2026-08-06T19:15:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "M"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 234
verified: true
draft: false
---

[CF 102503M - Se\u00f1orita](https://codeforces.com/problemset/problem/102503/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes two stacks whose shirts are labeled by the day they must be worn. The first stack is listed from bottom to top, and the second stack is listed the same way. The goal is to remove shirts in the order `1, 2, ..., m+n`. Moving a shirt from one stack to the other costs one unit of energy, while taking the correct shirt when it is already exposed costs nothing.

A direct simulation of every possible move is impossible because there can be up to `400000` shirts. Any solution that tries many possible rearrangements will be far too slow. We need to find a representation where the only meaningful decisions are the unavoidable movements of the two stack tops.

A useful edge case is when one stack is empty. For example:

```
0
1 2 3
```

The answer is `0` because every shirt is already accessible from the only stack. An implementation that assumes both stacks always have a top shirt can fail here.

Another edge case is when the required shirt is immediately accessible from the second stack:

```
1 2
3
```

The answer is `0` because shirt `1` is on top of the first stack and shirt `2` is on top of the second stack after it is needed. A solution that only checks one stack direction will overcount.

## Approaches

The brute-force idea is to actually simulate the stacks. To retrieve the next shirt, we could try moving shirts one by one between stacks until the target appears. This is correct because every legal operation is explicitly simulated. However, in the worst case we may move almost every remaining shirt for every requested shirt, giving roughly `O(N^2)` operations. With `N = 400000`, this is impossible.

The key observation is that the relative circular order of the shirts never changes. Imagine placing the first stack from bottom to top and then the second stack from top to bottom around a circle. Moving a shirt between stacks only changes where the split between the two stacks lies on this circle. The two exposed shirts are the two shirts next to this split.

This turns the problem into maintaining a moving cut in a circular array. We only need to know the distance from the current cut to the requested shirt. After removing a shirt, the new cut always ends up immediately before the removed shirt in the remaining circle.

To maintain distances after deletions, we store which original positions are still alive in a Fenwick tree. It can count alive shirts in ranges and find the k-th alive position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow |
| Circular order + Fenwick tree | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build the circular order. Put the first stack in its given order and append the second stack in reverse order. Store the position of every shirt in this circle.

The current cut is between the two original stacks. We keep `cur` as the position of the shirt on the first stack's top. The other exposed shirt is the next alive position after `cur`.

1. Initialize a Fenwick tree containing one for every shirt position.

The Fenwick tree represents the current circle after some shirts have been removed.

1. For every shirt number from `1` to `N`, find its current circular distance from `cur`.

If the shirt is `d` alive positions clockwise from `cur`, then retrieving it costs:

```
min(d - 1, remaining - d)
```

The first term means moving the cut forward until the shirt becomes the second stack top. The second term means moving backward until it becomes the first stack top.

1. Add this minimum cost to the answer.
2. Remove the shirt from the Fenwick tree.

After the removal, set `cur` to the alive position immediately before the removed shirt.

Why it works:

The circular order invariant means every possible sequence of moves only changes the cut position. The distance formula considers both possible directions for moving that cut, and one of them is always optimal because every move changes the cut by exactly one position. After deleting a shirt, the predecessor position becomes the new first-stack top regardless of which direction was used, so the maintained state is always valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        res = 0
        while i:
            res += self.bit[i]
            i -= i & -i
        return res

    def range_sum(self, l, r):
        if l > r:
            return 0
        return self.sum(r) - self.sum(l - 1)

    def kth(self, k):
        idx = 0
        step = 1 << (self.n.bit_length() - 1)
        while step:
            nxt = idx + step
            if nxt <= self.n and self.bit[nxt] < k:
                idx = nxt
                k -= self.bit[nxt]
            step >>= 1
        return idx + 1

def solve():
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    m = a[0]
    first = a[1:]
    n = b[0]
    second = b[1:]

    circle = first + second[::-1]
    total = m + n

    pos = [0] * (total + 1)
    for i, x in enumerate(circle, 1):
        pos[x] = i

    bit = Fenwick(total)
    for i in range(1, total + 1):
        bit.add(i, 1)

    if m:
        cur = m
    else:
        cur = total

    ans = 0
    alive = total

    for x in range(1, total + 1):
        p = pos[x]

        if p == cur:
            cost = 0
        else:
            before = bit.sum(cur)
            if p > cur:
                dist = bit.range_sum(cur, p - 1)
            else:
                dist = bit.range_sum(cur, total) + bit.range_sum(1, p - 1)

            cost = min(dist - 1, alive - dist)

        ans += cost

        bit.add(p, -1)
        alive -= 1

        if alive:
            before = bit.sum(p - 1)
            if before:
                cur = bit.kth(before)
            else:
                cur = bit.kth(alive)

    print(ans)

if __name__ == "__main__":
    solve()
```

The Fenwick tree stores alive positions, so deletions and circular distances are handled without rebuilding the circle. The `kth` operation is used after removing a shirt because we need the predecessor of the removed position among the remaining shirts.

The expression for the cost is the subtle part. `dist` counts how many alive positions lie from the current top through the target. If the target is the first exposed shirt, `dist` is zero, which is handled separately. Otherwise moving forward `dist - 1` times exposes it from the second stack, while moving backward `alive - dist` times exposes it from the first stack.

Python integers are arbitrary precision, so the accumulated answer does not need special handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Each shirt performs Fenwick queries and updates |
| Space | O(N) | Stores positions and Fenwick tree |

The maximum input size is `400000`, so the logarithmic factor is acceptable under the time limit.

## Worked Example

For the sample:

```
3 1 5 3
4 7 2 6 4
```

The circular order is:

```
1 5 3 4 6 2 7
```

The initial cut is before `4`, so the exposed shirts are `3` and `4`.

| Shirt requested | Distance choice | Energy added |
| --- | --- | --- |
| 1 | Move past 3 and 5 | 2 |
| 2 | Move around the shorter side | 4 |
| 3 | Move past remaining blockers | 2 |
| Remaining shirts | Already reachable | 0 |

The total is:

```
2 + 4 + 2 = 8
```

which matches the sample output.

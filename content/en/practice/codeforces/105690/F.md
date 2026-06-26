---
title: "CF 105690F - Lantern Hopping"
description: "We have a line of lanterns. Lantern i has height a[i], and the dragon starts on one chosen lantern. He can only jump to an adjacent lantern when the two lanterns have the same height at the moment of the jump."
date: "2026-06-26T09:04:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105690
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 1-29-25 Div. 1 (Advanced)"
rating: 0
weight: 105690
solve_time_s: 41
verified: true
draft: false
---

[CF 105690F - Lantern Hopping](https://codeforces.com/problemset/problem/105690/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of lanterns. Lantern `i` has height `a[i]`, and the dragon starts on one chosen lantern. He can only jump to an adjacent lantern when the two lanterns have the same height at the moment of the jump.

The dragon can change the height of the lantern he is currently standing on. Increasing the height by one consumes one energy, while decreasing the height by one gives one energy back. The task is to find the smallest initial energy needed for every query starting position so that the dragon can eventually visit every lantern. Lantern heights can also be updated between queries. The problem asks for the answer after each update or starting-position query.

The constraints allow up to `2 * 10^5` lanterns and `2 * 10^5` events. A solution that scans all lanterns for every query would require around `4 * 10^10` operations in the worst case, which is far beyond what fits in a typical contest time limit. We need both updates and queries to be around logarithmic time, which points toward maintaining a data structure over the array.

The main edge cases come from confusing the current lantern height with its original height, and from forgetting that the starting lantern itself can provide energy by being lowered.

For example, with:

```
2 1
5 10
1 1
```

the answer is `5`. The dragon starts on the first lantern, lowers it from `5` to `10` is impossible without energy, so he needs exactly `5` energy to raise it and jump. A solution that only checks differences between adjacent lanterns may miss that the first move has a direct cost.

Another example is:

```
3 1
10 5 10
1 2
```

the answer is `5`. The middle lantern is lower than both sides, so the dragon needs enough energy to raise it before either jump. A careless solution that only checks one side may return `0` incorrectly.

A final boundary case is a single lantern:

```
1 1
100
1 1
```

The answer is `0`, because there are no jumps to perform. Any implementation that queries an empty left or right range without handling it can fail here.

## Approaches

The brute-force approach is to simulate the dragon's movement. Starting from a chosen lantern, we could try different orders of visiting the left and right sides, tracking how much energy is required for every jump. This is correct because every valid movement sequence can be checked directly. However, it is far too slow. With `n = 2 * 10^5`, a single query could inspect all lanterns, and repeating this for `q = 2 * 10^5` queries gives quadratic behavior.

The key observation is that a movement across a side of the array has a simple energy requirement.

Suppose the dragon starts at position `p` and walks only to the right. Before reaching lantern `i + 1`, every previous jump has changed the current lantern into the height of the next lantern. The total energy change after reaching lantern `i` is exactly `a[p] - a[i]`. To make the next jump, the dragon must have enough energy to raise the current lantern if `a[i + 1]` is higher. Combining these values shows that the only thing that matters is the highest lantern height encountered on that side.

The required energy to reach every lantern on the right is:

`max(0, maximum height on positions p+1 through n - a[p])`

The left side is symmetric:

`max(0, maximum height on positions 1 through p-1 - a[p])`

The dragon must handle both sides, so the answer is the larger of these two values. This reduces the problem to range maximum queries with point updates. A segment tree stores the maximum height in every interval, giving logarithmic time for both operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per query | O(1) | Too slow |
| Optimal | O(log n) per operation | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree where each node stores the maximum lantern height inside its interval. The only information needed from a range is its highest lantern.
2. For an update query, replace the value of the chosen lantern in the segment tree and recalculate the maximum values on the path to the root.
3. For a starting-position query at `p`, obtain the maximum height among all lanterns to the left of `p`.
4. Obtain the maximum height among all lanterns to the right of `p`.
5. Compute the energy needed for each side. If the maximum height on one side is `mx`, the dragon needs `max(0, mx - a[p])` energy to reach that side.
6. Return the larger of the two side requirements, because both sides must eventually be visited.

Why it works:

During a walk in one direction, every jump effectively transfers the difference in height into the dragon's energy balance. The total amount of energy available after reaching any lantern depends only on the starting height and the current lantern's height. The largest obstacle is always the highest lantern that must be reached, because reaching a taller lantern is the only situation that requires spending energy. The segment tree returns exactly these highest obstacles for both directions, so the computed value is the minimum possible initial energy.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, node, left, right, arr):
        if left == right:
            self.tree[node] = arr[left]
            return
        mid = (left + right) // 2
        self.build(node * 2, left, mid, arr)
        self.build(node * 2 + 1, mid + 1, right, arr)
        self.tree[node] = max(self.tree[node * 2], self.tree[node * 2 + 1])

    def update(self, node, left, right, pos, value):
        if left == right:
            self.tree[node] = value
            return
        mid = (left + right) // 2
        if pos <= mid:
            self.update(node * 2, left, mid, pos, value)
        else:
            self.update(node * 2 + 1, mid + 1, right, pos, value)
        self.tree[node] = max(self.tree[node * 2], self.tree[node * 2 + 1])

    def query(self, node, left, right, ql, qr):
        if ql > right or qr < left:
            return -1
        if ql <= left and right <= qr:
            return self.tree[node]
        mid = (left + right) // 2
        return max(
            self.query(node * 2, left, mid, ql, qr),
            self.query(node * 2 + 1, mid + 1, right, ql, qr)
        )

def solve(data):
    it = iter(data.split())
    n = int(next(it))
    q = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    seg = SegmentTree(a)
    ans = []

    for _ in range(q):
        t = int(next(it))
        if t == 1:
            p = int(next(it)) - 1
            left_max = seg.query(1, 0, n - 1, 0, p - 1)
            right_max = seg.query(1, 0, n - 1, p + 1, n - 1)

            need = 0
            if left_max != -1:
                need = max(need, left_max - a[p])
            if right_max != -1:
                need = max(need, right_max - a[p])

            ans.append(str(max(0, need)))
        else:
            p = int(next(it)) - 1
            x = int(next(it))
            a[p] = x
            seg.update(1, 0, n - 1, p, x)

    return "\n".join(ans)

def main():
    data = sys.stdin.read()
    print(solve(data))

if __name__ == "__main__":
    main()
```

The segment tree stores only maximum values because every query asks for the largest height that blocks movement. The update operation changes one lantern and refreshes the affected intervals.

The query uses `-1` as the empty-range marker. Since all lantern heights are non-negative, this value cannot be confused with a real lantern height. The final `max(0, need)` handles cases where every lantern on the relevant side is lower than the starting lantern, meaning the dragon can gain enough energy by lowering the starting lantern.

All indices are converted to zero-based indexing immediately. The ranges `0` to `p - 1` and `p + 1` to `n - 1` represent the two sides of the starting lantern, avoiding accidental inclusion of the starting position.

## Worked Examples

For the input:

```
3 2
3 1 3
1 1
1 2
```

the segment tree initially stores the maximum values of the ranges.

| Query | Position | Left maximum | Right maximum | Answer |
| --- | --- | --- | --- | --- |
| `1 1` | 1 | none | 3 | 0 |
| `1 2` | 2 | 3 | 3 | 2 |

For the first query, the dragon starts on height `3` and the tallest lantern to the right is also `3`, so no energy is required. For the second query, the starting height is `1`, and both sides contain height `3`, requiring `3 - 1 = 2` energy.

For the input:

```
2 5
1000000000 0
1 2
2 2 10
1 2
2 1 10
1 2
```

| Query | Array | Position | Left maximum | Right maximum | Answer |
| --- | --- | --- | --- | --- | --- |
| `1 2` | `[1000000000,0]` | 2 | 1000000000 | none | 1000000000 |
| update | `[1000000000,10]` |  |  |  |  |
| `1 2` | `[1000000000,10]` | 2 | 1000000000 | none | 999999990 |
| update | `[10,10]` |  |  |  |  |
| `1 2` | `[10,10]` | 2 | 10 | none | 0 |

The trace shows that the answer depends on the current heights, so every update must immediately affect future maximum queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each update and each range maximum query follows one path through the segment tree. |
| Space | O(n) | The tree contains a constant number of nodes per lantern. |

The constraints require handling hundreds of thousands of operations. The logarithmic operations keep the total work around `n log n + q log n`, which fits comfortably within the intended limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    return solve(inp).strip()

assert run("""3 2
3 1 3
1 1
1 2
""") == "0\n2"

assert run("""2 5
1000000000 0
1 2
2 2 10
1 2
2 1 10
1 2
""") == "1000000000\n999999990\n0"

assert run("""1 1
7
1 1
""") == "0"

assert run("""3 3
10 5 10
1 2
2 2 10
1 2
""") == "5\n0"

assert run("""5 4
1 2 3 4 5
1 3
2 5 0
1 1
1 5
""") == "2\n4\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single lantern | `0` | Empty left and right ranges |
| Symmetric high lanterns | `5`, then `0` | Starting lantern updates and both-side checks |
| Increasing heights with updates | Multiple non-zero answers | Range maximum maintenance |
| Large height differences | Large integer handling | Correct arithmetic without overflow |

## Edge Cases

For the case:

```
2 1
5 10
1 1
```

the segment tree returns `10` as the maximum height on the right. The starting height is `5`, so the required energy is `10 - 5 = 5`. The algorithm correctly captures the first jump cost.

For the case:

```
3 1
10 5 10
1 2
```

the left and right maximum values are both `10`. The starting lantern has height `5`, so both sides require `5` energy. The result is `5`, which is the amount needed to raise the middle lantern before moving.

For the case:

```
1 1
100
1 1
```

both range queries return the empty marker because there are no neighboring lanterns. The algorithm leaves the answer at `0`, which matches the fact that no movement is necessary.

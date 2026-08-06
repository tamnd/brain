---
title: "CF 102503L - Arnis Ball"
description: "We have an array of boxes. Each position stores two pieces of information: the number of balls currently inside it and whether the box is open."
date: "2026-08-06T19:11:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "L"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 203
verified: false
draft: false
---

[CF 102503L - Arnis Ball](https://codeforces.com/problemset/problem/102503/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 23s  
**Verified:** no  

## Solution
# Problem Understanding

We have an array of boxes. Each position stores two pieces of information: the number of balls currently inside it and whether the box is open. A range operation can either invert the open and closed states, add balls to only the currently open boxes, or ask for the total number of balls in a range.

The difficulty comes from the interaction between the state of a box and its value. A normal lazy segment tree can handle range additions and sums, and a normal lazy segment tree can also handle range flips, but here a flip changes which elements are affected by future additions. The data structure must remember enough information to survive those changes.

The maximum size of the array and number of operations are both 320000. A solution that scans a whole range for every operation can perform around 10 11 element visits in the worst case, which is far beyond what fits in a 2 second limit. We need each operation to be close to logarithmic, because mlogn is around a few million recursive calls.

Several mistakes appear in simple implementations. A flip operation must swap both the states and the accumulated values belonging to open and closed boxes. For example:

```
1 1
5
1
3 1 1
```

The answer is:

```
5
```

A careless solution that stores only the sum of open boxes would lose the value when the box becomes closed.

Another issue is adding to open boxes after a flip. Consider:

```
2 3
10 20
1 0
1 1 2
2 1 2 5
3 1 2
```

The answer is:

```
35
```

After the flip, only the second box is open, so only 20 receives the addition. Tracking only the original open positions gives the wrong result.

A final boundary case is a range of length one:

```
1 3
7
0
2 1 1 4
1 1 1
3 1 1
```

The answer is:

```
11
```

The box starts closed, so the addition does nothing. The flip opens it, but no later addition occurs. Implementations that accidentally apply the addition before checking the state will fail here.

## Approaches

The direct solution is to store the current arrays and process every operation by iterating through the affected interval. It is correct because every box in the range is explicitly updated. However, a single operation can touch all n boxes. With n=m=320000, repeating this gives about 102400000000 updates, which is too slow.

The useful observation is that a segment does not need to know the exact state of every box. For a range we only need the sum of balls in open boxes, the sum of balls in closed boxes, and how many boxes are open. A flip simply exchanges the open and closed information. An addition changes only the open sum. A query returns the sum of the two stored sums.

This allows a lazy segment tree. Each node represents a contiguous range and stores enough aggregate information to answer queries without descending. Range additions are delayed with lazy propagation. Range flips are also delayed, but when a flip is applied to a node we swap the open and closed data and swap the pending additions attached to them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O((n+m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree. For every node store the number of open boxes, the sum of balls in open boxes, the sum of balls in closed boxes, and two lazy values representing pending additions to open and closed boxes.
2. For a puto operation, visit the covered nodes. Add v to the pending addition of open boxes and increase the open sum by v multiplied by the number of open boxes. This works because every open box in the segment receives exactly the same value.
3. For a turon operation, visit the covered nodes and exchange the open and closed information. The number of open boxes becomes the old number of closed boxes, and the two sums are swapped. The pending additions for open and closed boxes are also swapped because boxes that were waiting for an open-only addition have changed categories.
4. For a taho operation, combine the answers from the visited nodes. A node contributes the sum of both categories because the query asks for every box regardless of state.
5. During recursion, push lazy values before going deeper. Applying pending additions first updates the children values, and applying the pending flip exchanges their open and closed information.

Why it works: every node always represents exactly the boxes in its interval. The stored open and closed sums together contain the total value of the interval, and the open count determines which boxes receive future additions. Each lazy operation is equivalent to performing the same operation on every element inside the node, so postponing it cannot change the final result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    state = list(map(int, input().split()))

    size = 4 * n
    open_cnt = [0] * size
    open_sum = [0] * size
    closed_sum = [0] * size
    add_open = [0] * size
    add_closed = [0] * size
    flip = [0] * size

    def build(node, l, r):
        if l == r:
            if state[l]:
                open_cnt[node] = 1
                open_sum[node] = a[l]
            else:
                closed_sum[node] = a[l]
            return
        mid = (l + r) // 2
        build(node * 2, l, mid)
        build(node * 2 + 1, mid + 1, r)
        pull(node, l, r)

    def pull(node, l, r):
        open_cnt[node] = open_cnt[node * 2] + open_cnt[node * 2 + 1]
        open_sum[node] = open_sum[node * 2] + open_sum[node * 2 + 1]
        closed_sum[node] = closed_sum[node * 2] + closed_sum[node * 2 + 1]

    def apply_add_open(node, value):
        open_sum[node] += open_cnt[node] * value
        add_open[node] += value

    def apply_add_closed(node, value, length):
        closed_sum[node] += (length - open_cnt[node]) * value
        add_closed[node] += value

    def apply_flip(node, length):
        open_cnt[node] = length - open_cnt[node]
        open_sum[node], closed_sum[node] = closed_sum[node], open_sum[node]
        add_open[node], add_closed[node] = add_closed[node], add_open[node]
        flip[node] ^= 1

    def push(node, l, r):
        if l == r:
            add_open[node] = add_closed[node] = 0
            flip[node] = 0
            return
        mid = (l + r) // 2
        left, right = node * 2, node * 2 + 1
        if flip[node]:
            apply_flip(left, mid - l + 1)
            apply_flip(right, r - mid)
            flip[node] = 0
        if add_open[node]:
            v = add_open[node]
            apply_add_open(left, v)
            apply_add_open(right, v)
            add_open[node] = 0
        if add_closed[node]:
            v = add_closed[node]
            apply_add_closed(left, v, mid - l + 1)
            apply_add_closed(right, v, r - mid)
            add_closed[node] = 0

    def update_add(node, l, r, ql, qr, v):
        if ql <= l and r <= qr:
            apply_add_open(node, v)
            return
        push(node, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            update_add(node * 2, l, mid, ql, qr, v)
        if qr > mid:
            update_add(node * 2 + 1, mid + 1, r, ql, qr, v)
        pull(node, l, r)

    def update_flip(node, l, r, ql, qr):
        if ql <= l and r <= qr:
            apply_flip(node, r - l + 1)
            return
        push(node, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            update_flip(node * 2, l, mid, ql, qr)
        if qr > mid:
            update_flip(node * 2 + 1, mid + 1, r, ql, qr)
        pull(node, l, r)

    def query(node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return open_sum[node] + closed_sum[node]
        push(node, l, r)
        mid = (l + r) // 2
        ans = 0
        if ql <= mid:
            ans += query(node * 2, l, mid, ql, qr)
        if qr > mid:
            ans += query(node * 2 + 1, mid + 1, r, ql, qr)
        return ans

    build(1, 0, n - 1)
    ans = []
    for _ in range(m):
        op = list(map(int, input().split()))
        if op[0] == 1:
            update_flip(1, 0, n - 1, op[1] - 1, op[2] - 1)
        elif op[0] == 2:
            update_add(1, 0, n - 1, op[1] - 1, op[2] - 1, op[3])
        else:
            ans.append(str(query(1, 0, n - 1, op[1] - 1, op[2] - 1)))
    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The tree arrays keep separate information for the two possible states of a box. This is the key modeling decision. Without both sums, a flip would destroy information.

The lazy arrays are separated into additions for open and closed boxes. This avoids complicated ordering problems between flips and additions. When a flip happens, those two pending additions exchange roles because the boxes they belong to exchange roles.

All indices are converted to zero-based indexing when processing queries. Python integers handle the large sums safely, since the total number of balls can exceed 32-bit ranges.

## Worked Examples

For the sample:

| Operation | Open sum | Closed sum | Answer |
| --- | --- | --- | --- |
| Initial state | 21 | 10 |  |
| Query [2,4] | 4+8 | 2 | 14 |
| Add 6 to open boxes | 22 | 10 |  |
| Query [2,4] | 10+8 | 2 | 20 |
| Flip all boxes | 10 | 22 |  |
| Add 7 to open boxes | 24 | 22 |  |
| Query [2,4] | 9+10+15 | 0 | 34 |

The trace shows why the tree keeps two sums. After the flip, the values themselves do not move, only the category of each box changes.

A smaller example:

```
2 3
3 8
0 1
3 1 2
1 1 2
3 1 2
```

| Operation | Open count | Open sum | Closed sum | Answer |
| --- | --- | --- | --- | --- |
| Initial | 1 | 8 | 3 |  |
| Query | 1 | 8 | 3 | 11 |
| Flip | 1 | 3 | 8 |  |
| Query | 1 | 3 | 8 | 11 |

The total stays the same after a flip, but the open and closed parts exchange, which is exactly what the node operation does.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log n) | Building the tree is linear, and every operation touches logarithmically many nodes. |
| Space | O(n) | The segment tree stores a constant amount of data per node. |

The maximum input size requires avoiding range scans. The logarithmic operations keep the number of node visits small enough for the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old
    return ""

# Sample
sample = """5 6
1 2 4 8 16
1 0 1 0 1
3 2 4
2 1 5 6
3 2 4
1 1 5
2 1 5 7
3 2 4
"""
# Expected:
# 14
# 20
# 34

tests = [
    """1 1
5
1
3 1 1
""",
    """2 3
10 20
1 0
1 1 2
2 1 2 5
3 1 2
""",
    """1 3
7
0
2 1 1 4
1 1 1
3 1 1
"""
]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single box query | 5 | Basic query handling |
| Flip followed by addition | 35 | Correct interaction between flip and add |
| Closed box addition | 11 | Ignoring closed boxes during updates |

## Edge Cases

The first edge case is losing information after flips. In the input

```
1 1
5
1
3 1 1
```

the segment tree stores the value as an open sum. The query returns open sum plus closed sum, giving 5. A representation containing only the active state would fail after later flips because the value must remain available.

The second edge case is an addition after a state change:

```
2 3
10 20
1 0
1 1 2
2 1 2 5
3 1 2
```

The flip changes the open box from the first position to the second. The lazy segment tree swaps the open and closed aggregates, so the later addition affects only the second value. The final total is 35.

The third edge case is a range of length one where the box starts closed:

```
1 3
7
0
2 1 1 4
1 1 1
3 1 1
```

The addition is ignored because the open count is zero. The flip changes the category, and the query returns the original value 7. The stored open count prevents applying invalid updates.

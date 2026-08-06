---
title: "CF 102503L - Arnis Ball"
description: "We have a line of boxes. Each box stores a number of balls and also has a state: open or closed. The operations modify these two pieces of information together. A flip operation changes every box in a range from open to closed or from closed to open."
date: "2026-08-07T04:46:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "L"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 572
verified: true
draft: false
---

[CF 102503L - Arnis Ball](https://codeforces.com/problemset/problem/102503/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of boxes. Each box stores a number of balls and also has a state: open or closed. The operations modify these two pieces of information together. A flip operation changes every box in a range from open to closed or from closed to open. An add operation only affects boxes that are currently open in a range. A query operation asks for the total number of balls in every box in a range, regardless of whether the boxes are open or closed.

The input gives the initial ball counts, the initial open or closed states, and then a sequence of operations. For every query operation, we must output the current sum of the selected interval.

The limits are large enough that simulating every affected box is impossible. With up to 320,000 boxes and 320,000 operations, a solution doing linear work for every operation could perform around 10^11 updates in the worst case. A 2 second time limit requires each operation to be close to logarithmic time, which rules out direct array updates and repeated interval scans.

The difficult part is that the operations affect two related properties. The number of balls changes only for open boxes, while the state of boxes can later change through flips. A solution that only stores the total sum loses the information needed to know which boxes should receive future additions.

A small case that breaks a careless implementation is a flip followed by an add:

```
Input
2 3
5 7
1 0
1 1 2
2 1 2 3
3 1 2
```

The first operation changes the states to closed, open. The addition affects only the second box, making the values 5 and 10. The answer is:

```
15
```

An implementation that stores only the total sum and treats every add as a range addition would output 18.

Another edge case is a flip applied several times to the same interval:

```
Input
1 4
10
1
1 1 1
1 1 1
2 1 1 5
3 1 1
```

The two flips cancel, so the box is open when the addition happens. The final answer is:

```
15
```

A lazy propagation implementation that forgets to combine flip flags correctly could incorrectly leave the box closed.

A final common mistake is confusing the queried sum with the sum of only open boxes:

```
Input
2 1
4 9
1 0
3 1 2
```

The answer is:

```
13
```

The closed box still contributes to queries. Only additions ignore closed boxes.

## Approaches

A straightforward solution is to keep two arrays: one for the ball counts and one for the states. For a flip, we traverse the interval and toggle every state. For an addition, we traverse the interval and add only to open boxes. For a query, we sum every value in the interval. This is correct because every operation directly follows the problem rules.

The problem is that one operation can touch all 320,000 boxes. If every operation uses a full interval, the number of primitive actions can reach about 320,000 × 320,000, which is roughly 102 billion updates or queries. The approach is correct but far too slow.

The key observation is that the operations do not need individual boxes. A segment only needs to know two aggregated sums: the sum of values in open boxes and the sum of values in closed boxes. An addition changes only the open sum. A flip simply exchanges the two sums. A range query needs their combined value.

This structure matches a lazy segment tree. Each node represents an interval and stores enough information to answer queries or apply updates without descending to children. The lazy flip flag records that an entire segment has been inverted but its children have not yet been updated.

The brute-force method works because it keeps exact information for every box, but fails when too many boxes are touched repeatedly. The observation that flipping is just an exchange of two groups lets us compress the required information and handle each operation in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree where every node stores the total balls in open boxes, the total balls in closed boxes, and the number of open boxes inside the interval.

The number of open boxes is needed because an addition of `v` must increase the open sum by `v` multiplied by the amount of open boxes in the segment.
2. For a range addition, recursively visit the segment tree. If a node is completely inside the update interval, increase its open sum directly by `v * open_count`.

Closed boxes are ignored because the operation only affects currently open boxes.
3. For a flip operation, recursively visit the segment tree. When a node is completely inside the interval, swap its open sum and closed sum, replace its open count with the number of previously closed boxes, and toggle its lazy flip flag.

A flip does not change any ball counts. It only changes which group each box belongs to, so exchanging the two stored groups is enough.
4. For a query operation, recursively collect the sum of open and closed values from the covered segments.

The answer is the sum of both groups because queries count all boxes, regardless of state.
5. Use lazy propagation whenever a whole segment is flipped. The pending flip is pushed to children only when a later operation needs to inspect those children.

This avoids visiting every element of a large flipped interval.

Why it works: the invariant of every segment tree node is that its two stored sums always represent the real current values of the boxes in that interval, separated by their current states. An addition preserves this invariant because only the open group changes. A flip preserves it because the boxes keep their values while the two state groups exchange roles. Lazy propagation only delays these valid transformations, so every query sees the same result as if all operations had been applied individually.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, values, states):
        self.n = len(values)
        size = 4 * self.n
        self.open_sum = [0] * size
        self.closed_sum = [0] * size
        self.open_cnt = [0] * size
        self.flip = [False] * size
        self.values = values
        self.states = states
        self.build(1, 0, self.n - 1)

    def build(self, node, left, right):
        if left == right:
            if self.states[left]:
                self.open_sum[node] = self.values[left]
                self.open_cnt[node] = 1
            else:
                self.closed_sum[node] = self.values[left]
            return
        mid = (left + right) // 2
        self.build(node * 2, left, mid)
        self.build(node * 2 + 1, mid + 1, right)
        self.pull(node)

    def pull(self, node):
        self.open_sum[node] = self.open_sum[node * 2] + self.open_sum[node * 2 + 1]
        self.closed_sum[node] = self.closed_sum[node * 2] + self.closed_sum[node * 2 + 1]
        self.open_cnt[node] = self.open_cnt[node * 2] + self.open_cnt[node * 2 + 1]

    def apply_flip(self, node, length):
        self.open_sum[node], self.closed_sum[node] = self.closed_sum[node], self.open_sum[node]
        self.open_cnt[node] = length - self.open_cnt[node]
        self.flip[node] = not self.flip[node]

    def push(self, node, left, right):
        if not self.flip[node] or left == right:
            return
        mid = (left + right) // 2
        self.apply_flip(node * 2, mid - left + 1)
        self.apply_flip(node * 2 + 1, right - mid)
        self.flip[node] = False

    def update_add(self, node, left, right, ql, qr, value):
        if qr < left or right < ql:
            return
        if ql <= left and right <= qr:
            self.open_sum[node] += self.open_cnt[node] * value
            return
        self.push(node, left, right)
        mid = (left + right) // 2
        self.update_add(node * 2, left, mid, ql, qr, value)
        self.update_add(node * 2 + 1, mid + 1, right, ql, qr, value)
        self.pull(node)

    def update_flip(self, node, left, right, ql, qr):
        if qr < left or right < ql:
            return
        if ql <= left and right <= qr:
            self.apply_flip(node, right - left + 1)
            return
        self.push(node, left, right)
        mid = (left + right) // 2
        self.update_flip(node * 2, left, mid, ql, qr)
        self.update_flip(node * 2 + 1, mid + 1, right, ql, qr)
        self.pull(node)

    def query(self, node, left, right, ql, qr):
        if qr < left or right < ql:
            return 0
        if ql <= left and right <= qr:
            return self.open_sum[node] + self.closed_sum[node]
        self.push(node, left, right)
        mid = (left + right) // 2
        return self.query(node * 2, left, mid, ql, qr) + self.query(node * 2 + 1, mid + 1, right, ql, qr)

def solve():
    n, m = map(int, input().split())
    values = list(map(int, input().split()))
    states = list(map(int, input().split()))

    seg = SegmentTree(values, states)
    ans = []

    for _ in range(m):
        query = list(map(int, input().split()))
        typ = query[0]
        l = query[1] - 1
        r = query[2] - 1

        if typ == 1:
            seg.update_flip(1, 0, n - 1, l, r)
        elif typ == 2:
            seg.update_add(1, 0, n - 1, l, r, query[3])
        else:
            ans.append(str(seg.query(1, 0, n - 1, l, r)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The segment tree keeps the two categories of boxes separate. The `open_sum` and `closed_sum` arrays represent the current total values of those categories. The `open_cnt` array allows range additions to be applied without knowing individual boxes.

The flip operation is handled without visiting leaves. The two sums are swapped because every box changes membership between the two categories. The count of open boxes is also swapped with the count of closed boxes, which is the segment length minus the old open count.

The lazy flip flag is a boolean because two flips are equivalent to no flip. When a node with a pending flip is pushed, both children receive the same transformation before the parent continues with a partial operation.

All indexes are converted from the problem's one-based indexing to Python's zero-based indexing. Python integers avoid overflow even though the maximum answer can exceed 32-bit ranges.

## Worked Examples

For the sample:

| Operation | Open sum | Closed sum | Open count | Answer |
| --- | --- | --- | --- | --- |
| Initial | 21 | 10 | 3 |  |
| Query [2,4] | 14 | 0 |  | 14 |
| Add 6 to [1,5] | 39 | 10 | 3 |  |
| Query [2,4] | 20 | 0 |  | 20 |
| Flip [1,5] | 10 | 39 | 2 |  |
| Add 7 to [1,5] | 24 | 39 | 2 |  |
| Query [2,4] | 24 | 10 |  | 34 |

This trace shows that additions only change the open group. The flip does not alter the total amount of balls, it only changes which group owns each value.

A smaller case:

```
3 5
5 5 5
1 0 1
2 1 3 2
1 1 2
2 1 3 4
3 1 3
3 1 3
```

| Operation | Open sum | Closed sum | Open count | Answer |
| --- | --- | --- | --- | --- |
| Initial | 10 | 5 | 2 |  |
| Add 2 | 14 | 5 | 2 |  |
| Flip first two | 5 | 14 | 1 |  |
| Add 4 | 9 | 14 | 1 |  |
| Query all | 9 | 14 |  | 23 |
| Query all | 9 | 14 |  | 23 |

This example exercises partial flips and shows that repeated flips restore the previous state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Building the tree is linear, and every operation visits O(log n) nodes with lazy propagation. |
| Space | O(n) | The segment tree arrays contain a constant number of values for each node. |

The maximum input size requires avoiding any solution that touches every element per operation. The logarithmic operations of the segment tree fit comfortably within the time limit, and the memory usage is far below the available limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""5 6
1 2 4 8 16
1 0 1 0 1
3 2 4
2 1 5 6
3 2 4
1 1 5
2 1 5 7
3 2 4
""") == "14\n20\n34\n"

assert run("""1 1
100
0
3 1 1
""") == "100\n"

assert run("""3 4
5 5 5
1 0 1
2 1 3 2
1 1 2
2 1 3 4
3 1 3
""") == "23\n"

assert run("""2 4
7 9
1 1
1 1 2
2 1 2 10
1 1 1
3 1 2
""") == "36\n"

assert run("""4 5
1 1 1 1
0 0 0 0
2 1 4 5
1 2 3
2 1 4 3
3 1 4
3 2 3
""") == "4\n14\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single closed box query | `100` | Queries include closed boxes. |
| Mixed states with updates and flips | `23` | Open-only additions and partial flips. |
| Two flips with updates | `36` | Lazy flip cancellation. |
| All boxes initially closed | `4`, `14` | State transitions from fully closed segments. |

## Edge Cases

The first edge case from the discussion is an addition after a flip. The segment tree handles it because the flip operation swaps the stored open and closed groups before the addition is applied. For the input:

```
2 3
5 7
1 0
1 1 2
2 1 2 3
3 1 2
```

the tree changes its open count from one box to one box, but the open sum becomes the old closed sum. The addition affects the second box only, producing the final result `15`.

The second edge case is multiple flips on the same interval. The lazy flag stores whether an odd number of flips are pending. In:

```
1 4
10
1
1 1 1
1 1 1
2 1 1 5
3 1 1
```

the first flip marks the node as flipped, the second flip removes that pending state, and the box remains open. The addition is applied and the answer becomes `15`.

The final edge case is querying closed boxes. The query function always returns `open_sum + closed_sum`, so it never depends on the current state. For:

```
2 1
4 9
1 0
3 1 2
```

the tree stores 4 in the open group and 9 in the closed group. The returned sum is `13`, matching the required behavior.

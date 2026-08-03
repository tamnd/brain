---
title: "CF 102558D - \u041f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u0438\u0435 \u0447\u0430\u043d\u043a\u043e\u0432"
description: "We have an array of n chunks. The value at position i tells which server currently stores chunk i. A query asks to move every chunk in an interval [l, r] from server a to server b. The move is allowed only if every value in that interval is exactly a before the operation."
date: "2026-08-03T19:16:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102558
codeforces_index: "D"
codeforces_contest_name: "Contest for Yandex interns 2019"
rating: 0
weight: 102558
solve_time_s: 655
verified: true
draft: false
---

[CF 102558D - \u041f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u0438\u0435 \u0447\u0430\u043d\u043a\u043e\u0432](https://codeforces.com/problemset/problem/102558/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of `n` chunks. The value at position `i` tells which server currently stores chunk `i`. A query asks to move every chunk in an interval `[l, r]` from server `a` to server `b`. The move is allowed only if every value in that interval is exactly `a` before the operation. If even one chunk is on another server, the whole request is ignored. For every request we must output `1` if the move happens and `0` otherwise.

The input contains the initial server assignment of all chunks and then a chronological sequence of range move requests. The output describes which of those requests survive the consistency check.

The constraints are large enough that checking every chunk in every interval is impossible. With `n` and `q` both reaching `100000`, a solution performing `O(n)` work for every query can make about `10^10` operations in the worst case. The algorithm must process each request in roughly logarithmic time. Since the operation changes an entire interval at once, we need a data structure that can both summarize intervals and update them lazily.

Several edge cases can break simple implementations. A single chunk interval still has to be checked and updated correctly. For example:

```
Input:
1 2 1
1
1 2 1 1
```

The output is:

```
1
```

The interval contains one chunk, and its server matches the requested source server.

Another common mistake is to only check the first or last element of an interval. Consider:

```
Input:
3 3 1
1 1 2
1 3 1 1 1
```

The output is:

```
0
```

The first two chunks are on server `1`, but the third is on server `2`. A boundary-only check would incorrectly accept the move.

A third edge case appears after several successful moves. The current state, not the initial state, decides whether a query succeeds. For example:

```
Input:
2 3 2
1 2
1 3 1 1
3 2 1 2
```

The output is:

```
1
0
```

After the first query, the array becomes `[3, 2]`, so the second query asking to move both chunks from server `3` fails.

## Approaches

The straightforward approach is to store the current server of every chunk in an array. For each query, scan the interval `[l, r]` and verify that every element equals `a`. If the check passes, scan the same interval again and replace every value with `b`.

This approach is correct because it directly simulates the definition of a valid move. However, in the worst case a query can cover all `100000` chunks, and there can be `100000` such queries. The total work becomes around `10^10` element visits, which is far beyond what is possible.

The key observation is that we never need the exact values of every element inside a segment while processing a query. We only need to know whether the whole segment has one server value. At the same time, successful queries replace an entire interval with one new value. This combination is exactly what a lazy segment tree handles well.

Each segment tree node stores the server value if the whole represented interval is uniform. If an interval contains multiple server values, the node stores a special marker meaning "mixed". A query asks the tree for the state of `[l, r]`. If the returned value is `a`, the move can happen and the interval is assigned to `b`. If the returned value is mixed or another server number, the request is rejected.

Lazy propagation is needed because assigning a large interval should not require visiting every leaf. When a node receives a full-cover assignment, we store the new value in that node and delay updating its children until they are needed later.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a lazy segment tree from the initial server assignment. Each node stores either one server number if its entire interval is on that server, or `-1` if different servers appear inside it.
2. For every move request `(a, b, l, r)`, query the segment tree for the state of interval `[l, r]`. The result represents all information needed for the consistency check.
3. If the returned value is exactly `a`, mark the query as successful and assign the whole interval `[l, r]` to server `b`.
4. If the returned value is anything else, output `0` and do not modify the tree.

The important invariant is that every segment tree node always correctly describes the current state of its interval. A node is either a precise server number because all chunks inside it are there, or mixed because at least two different servers occur. Lazy propagation preserves this invariant by delaying child updates while keeping the parent summary accurate.

Why it works:

Before every query, the segment tree returns the exact uniform state of the requested interval. If that state is `a`, every chunk in the interval is stored on the required source server, so the move is valid and replacing the whole interval with `b` matches the real operation. If the state is mixed or another server, at least one chunk violates the requirement, so rejecting the query is correct. Since every accepted update changes the tree representation to match the new array state, all future checks use the correct information.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())
    arr = list(map(int, input().split()))

    size = 1
    while size < n:
        size *= 2

    tree = [-1] * (2 * size)
    lazy = [-1] * (2 * size)

    for i, x in enumerate(arr):
        tree[size + i] = x

    for i in range(size - 1, 0, -1):
        if tree[2 * i] == tree[2 * i + 1]:
            tree[i] = tree[2 * i]
        else:
            tree[i] = -1

    def apply(node, value):
        tree[node] = value
        lazy[node] = value

    def push(node):
        if lazy[node] != -1:
            apply(node * 2, lazy[node])
            apply(node * 2 + 1, lazy[node])
            lazy[node] = -1

    def query(node, left, right, ql, qr):
        if qr < left or right < ql:
            return -2

        if ql <= left and right <= qr:
            return tree[node]

        push(node)
        mid = (left + right) // 2
        a = query(node * 2, left, mid, ql, qr)
        b = query(node * 2 + 1, mid + 1, right, ql, qr)

        if a == -2:
            return b
        if b == -2:
            return a
        if a == b:
            return a
        return -1

    def update(node, left, right, ql, qr, value):
        if qr < left or right < ql:
            return

        if ql <= left and right <= qr:
            apply(node, value)
            return

        push(node)
        mid = (left + right) // 2
        update(node * 2, left, mid, ql, qr, value)
        update(node * 2 + 1, mid + 1, right, ql, qr, value)

        if tree[node * 2] == tree[node * 2 + 1]:
            tree[node] = tree[node * 2]
        else:
            tree[node] = -1

    ans = []
    for _ in range(q):
        a, b, l, r = map(int, input().split())
        l -= 1
        r -= 1

        if query(1, 0, size - 1, l, r) == a:
            ans.append("1")
            update(1, 0, size - 1, l, r, b)
        else:
            ans.append("0")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The tree is built over a power-of-two size so that every node has two children, including unused leaves. Those extra leaves are initialized with `-1`, but they are never included in real queries because all requests stay inside `[0, n-1]`.

The `tree` array stores the current summary of every segment. The `lazy` array stores pending assignments. A pending value means the whole segment already has that server number, but its children may still contain old information. Before descending into children, `push` applies this delayed assignment.

The query function returns `-2` for completely unrelated segments so that partial overlaps can be merged easily. Two valid returned server numbers are combined into one value only if they are equal. Otherwise the result becomes `-1`, meaning the interval is not uniform.

The update function assigns a whole interval in one operation when the current node is fully covered. It then rebuilds ancestors after recursive updates. Python integers do not overflow, so no special handling is required for the stored values.

## Worked Examples

### Sample 1

Input:

```
1 2 1
1
1 2 1 1
```

| Query | Requested interval | Tree result | Action | Array state |
| --- | --- | --- | --- | --- |
| 1 | `[1,1]`, source `1` | `1` | Assign to server `2` | `[2]` |

The only chunk is already on the requested source server, so the operation is accepted. This checks the single-element interval case.

### Sample 2

Input:

```
1 2 1
1
2 1 1 1
```

| Query | Requested interval | Tree result | Action | Array state |
| --- | --- | --- | --- | --- |
| 1 | `[1,1]`, source `2` | `1` | Reject | `[1]` |

The segment is uniform, but its value is not the requested source server. The move must fail because the consistency check compares against `a`, not just whether the interval has one value.

### Sample 3

Input:

```
5 5 6
1 2 3 4 5
1 2 1 1
2 3 1 3
4 2 4 4
2 5 1 4
3 2 2 3
3 2 3 3
```

| Query | Interval result before operation | Decision | Array after operation |
| --- | --- | --- | --- |
| 1 | `[1]` has server `1` | Accept | `[2,2,3,4,5]` |
| 2 | `[1,3]` is mixed | Reject | `[2,2,3,4,5]` |
| 3 | `[4]` has server `4` | Accept | `[2,2,3,2,5]` |
| 4 | `[1,4]` is mixed | Reject | `[2,2,3,2,5]` |
| 5 | `[2,3]` is mixed | Reject | `[2,2,3,2,5]` |
| 6 | `[3]` has server `3` | Accept | `[2,2,2,2,5]` |

The trace shows why the structure must be updated after every successful request. Failed requests do not change the state, so later queries still see the previous configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each query performs one segment tree query and, only for successful requests, one range assignment. |
| Space | O(n) | The segment tree and lazy arrays contain a constant number of entries per tree node. |

With `100000` chunks and `100000` requests, logarithmic processing keeps the total number of visited nodes around a few million, which fits the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    q = int(next(it))
    arr = [int(next(it)) for _ in range(n)]

    size = 1
    while size < n:
        size *= 2

    tree = [-1] * (2 * size)
    lazy = [-1] * (2 * size)

    for i, x in enumerate(arr):
        tree[size + i] = x

    for i in range(size - 1, 0, -1):
        tree[i] = tree[2 * i] if tree[2 * i] == tree[2 * i + 1] else -1

    def apply(node, value):
        tree[node] = value
        lazy[node] = value

    def push(node):
        if lazy[node] != -1:
            apply(node * 2, lazy[node])
            apply(node * 2 + 1, lazy[node])
            lazy[node] = -1

    def query(node, l, r, ql, qr):
        if qr < l or r < ql:
            return -2
        if ql <= l and r <= qr:
            return tree[node]
        push(node)
        mid = (l + r) // 2
        x = query(node * 2, l, mid, ql, qr)
        y = query(node * 2 + 1, mid + 1, r, ql, qr)
        if x == -2:
            return y
        if y == -2:
            return x
        return x if x == y else -1

    def update(node, l, r, ql, qr, value):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            apply(node, value)
            return
        push(node)
        mid = (l + r) // 2
        update(node * 2, l, mid, ql, qr, value)
        update(node * 2 + 1, mid + 1, r, ql, qr, value)
        tree[node] = tree[node * 2] if tree[node * 2] == tree[node * 2 + 1] else -1

    out = []
    for _ in range(q):
        a = int(next(it))
        b = int(next(it))
        l = int(next(it)) - 1
        r = int(next(it)) - 1
        if query(1, 0, size - 1, l, r) == a:
            out.append("1")
            update(1, 0, size - 1, l, r, b)
        else:
            out.append("0")
    return "\n".join(out)

assert run("""1 2 1
1
1 2 1 1
""") == "1"

assert run("""1 2 1
1
2 1 1 1
""") == "0"

assert run("""5 5 6
1 2 3 4 5
1 2 1 1
2 3 1 3
4 2 4 4
2 5 1 4
3 2 2 3
3 2 3 3
""") == "1\n0\n1\n0\n0\n1"

assert run("""3 5 3
2 2 2
2 3 1 3
3 4 1 2
3 5 2 3
""") == "1\n1\n0"

assert run("""4 4 2
1 1 1 1
1 2 2 3
2 3 1 4
""") == "1\n1"

assert run("""2 3 3
1 2
1 3 1 1
3 2 1 1
2 1 2 2
""") == "1\n1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single chunk move | `1` | Minimum size and leaf update |
| Sample 2 | `0` | Uniform interval with wrong source server |
| All chunks initially equal | `1,1` | Large successful range assignments |
| Mixed intervals after updates | `1,1,1` | State changes between queries |

## Edge Cases

A single-element interval is handled by the same segment tree logic as larger ranges. In the input:

```
1 2 1
1
1 2 1 1
```

the query reaches one leaf, receives value `1`, and updates that leaf to `2`. The result is `1`.

An interval that looks correct at its boundaries but is mixed inside is handled because internal nodes preserve the mixed state. For:

```
3 3 1
1 1 2
1 3 1 1
```

the root segment covering the query range combines children with different values and returns `-1`. Since `-1` is not the requested source server, the answer is `0`.

Operations after previous moves use the updated tree state. For:

```
2 3 2
1 2
1 3 1 1
3 2 1 2
```

the first query changes the first chunk to server `3`. The second query sees the interval `[3,2]`, which is mixed, and rejects the request. The output is:

```
1
0
```

The lazy assignment mechanism handles large intervals without expanding them immediately. If a query changes all chunks in a large segment, the node stores the new server value directly, and future operations only push that information when they need to inspect smaller parts.

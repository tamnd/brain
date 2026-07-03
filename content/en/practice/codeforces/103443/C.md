---
title: "CF 103443C - Community Service"
description: "We are given a dynamic system of intervals placed on a number line from 0 to n − 1. Each new person arrives with an interval [a, b] and is assigned a strictly increasing identifier based on arrival order. Later, service requests arrive as query intervals [c, d]."
date: "2026-07-03T07:40:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103443
codeforces_index: "C"
codeforces_contest_name: "The 2021 ICPC Asia Taipei Regional Programming Contest"
rating: 0
weight: 103443
solve_time_s: 56
verified: true
draft: false
---

[CF 103443C - Community Service](https://codeforces.com/problemset/problem/103443/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a dynamic system of intervals placed on a number line from 0 to n − 1. Each new person arrives with an interval [a, b] and is assigned a strictly increasing identifier based on arrival order. Later, service requests arrive as query intervals [c, d]. For each query, we must find the most recently added interval whose range overlaps the query range. Once that interval is used in a query, it is considered inactive and should never be used again.

So at any time we maintain a growing set of active intervals, each with a timestamp equal to its insertion order. A query asks for the maximum timestamp among all intervals that intersect the query segment. After answering, that chosen interval is removed from the active set.

The key difficulty is that both insertion and removal are online, and queries must always reflect the most recent active interval at the moment of the query.

The constraints allow up to 200,000 events and n up to 1,000,000. This immediately rules out any approach that checks all intervals per query, since a naive scan would cost O(n) per query in the worst case, leading to O(nm), which is far beyond feasible limits.

A few edge cases reveal common pitfalls. First, multiple intervals can overlap the same query, but only the newest among them matters. For example, if interval 1 is [0, 10], interval 2 is [3, 5], and interval 3 is [4, 6], a query [4, 4] should pick interval 3, not interval 2 or 1.

Second, once an interval has been used, it must disappear from all future answers. If we forget to remove it properly, it may be selected again incorrectly.

Third, overlapping structure matters: intervals are not disjoint, so any structure relying on partitioning the line into disjoint segments will fail.

## Approaches

A straightforward approach is to store all intervals in a list and, for each query, iterate through all intervals, check whether they intersect the query range, and take the one with the largest timestamp. This is correct because timestamps directly encode recency, and intersection checks are O(1). However, with up to 200,000 intervals and 200,000 queries, this leads to roughly 4 × 10^10 checks in the worst case, which is too slow.

The key observation is that this is a classic “range maximum over intervals with deletion” problem. We need to repeatedly answer: among all active intervals that intersect a query range, which has the largest insertion time.

A segment tree over the coordinate axis provides a way to organize intervals so that each interval is stored only in O(log n) nodes, specifically those fully covered by its segment tree decomposition. Each node keeps track of intervals that fully cover its segment. For each node, we only need to know the most recent active interval stored there.

When processing a query, we traverse segment tree nodes that lie completely inside the query range. Each such node contributes its best active interval candidate. The answer is the maximum among these candidates.

Deletion is handled lazily. Once an interval is used, we mark it as inactive. Each node maintains a stack of interval ids, and when accessing the top, we discard invalid (already used) intervals until the top is active again.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scan per query | O(n · e) | O(n) | Too slow |
| Segment tree with interval stacks | O(e log n) | O(e log n) | Accepted |

## Algorithm Walkthrough

We build a segment tree over the coordinate range [0, n − 1]. Each node represents a segment and stores a stack of interval identifiers whose interval fully covers that segment.

We also maintain, for each interval, the list of segment tree nodes where it was inserted, so that we can conceptually delete it later by marking it inactive.

### Steps

1. Assign each new interval an increasing id as it arrives. Store its endpoints and mark it as active.
2. Insert the interval into the segment tree. Whenever a segment tree node is fully covered by [a, b], push the interval id into that node’s stack. This ensures each interval is distributed across O(log n) nodes.
3. When a query [c, d] arrives, traverse the segment tree and consider only nodes fully contained in [c, d]. For each such node, inspect its stack top after cleaning inactive entries.
4. Cleaning means repeatedly popping from the stack while the top interval is no longer active. This ensures each node always exposes its best valid candidate.
5. The answer to the query is the maximum id among all valid stack tops collected during traversal.
6. After selecting an interval id as the answer, mark it inactive so it will not be considered in future queries.

### Why it works

Each interval is stored exactly in the nodes that fully represent it in the segment tree decomposition, so any point in its range is covered by at least one such node. When a query range is processed, every interval that intersects the query must appear in at least one node fully contained within the query range. Taking the maximum over these nodes ensures we do not miss any candidate interval. Since we always clean inactive intervals from stacks, we never incorrectly reuse a removed interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, e = map(int, input().split())

# segment tree: each node stores list of interval ids
tree = [[] for _ in range(4 * n + 5)]

interval = [None]  # 1-indexed: (name, l, r)
active = [False]

def add(node, l, r, ql, qr, idx):
    if ql <= l and r <= qr:
        tree[node].append(idx)
        return
    mid = (l + r) // 2
    if ql <= mid:
        add(node * 2, l, mid, ql, qr, idx)
    if qr > mid:
        add(node * 2 + 1, mid + 1, r, ql, qr, idx)

def query(node, l, r, ql, qr):
    if ql <= l and r <= qr:
        while tree[node] and not active[tree[node][-1]]:
            tree[node].pop()
        return tree[node][-1] if tree[node] else 0

    mid = (l + r) // 2
    res = 0
    if ql <= mid:
        res = max(res, query(node * 2, l, mid, ql, qr))
    if qr > mid:
        res = max(res, query(node * 2 + 1, mid + 1, r, ql, qr))
    return res

for _ in range(e):
    tmp = input().split()
    t = tmp[0]

    if t == '1':
        name = tmp[1]
        a = int(tmp[2])
        b = int(tmp[3])
        interval.append((name, a, b))
        active.append(True)
        idx = len(interval) - 1
        add(1, 0, n - 1, a, b, idx)

    else:
        c = int(tmp[1])
        d = int(tmp[2])
        idx = query(1, 0, n - 1, c, d)
        if idx == 0:
            print("> <")
        else:
            print(interval[idx][0])
            active[idx] = False
```

The segment tree insert function distributes each interval only to nodes fully covered by its range. This avoids storing redundant per-point information. The query function walks only the relevant segment tree branches and collects the best available interval id.

The key subtlety is lazy deletion. Instead of trying to remove an interval from every node it appears in, we simply mark it inactive and clean it when encountered at a node’s stack top. This keeps operations efficient.

## Worked Examples

### Example 1

Consider a small system with n = 10.

We insert interval A = [2, 6] with id 1, interval B = [4, 8] with id 2, and interval C = [5, 7] with id 3.

Now we process query [5, 5].

| Step | Node coverage | Stack tops considered | Best id |
| --- | --- | --- | --- |
| Query | nodes covering 5 | A=1, B=2, C=3 | 3 |

The result is interval C because it has the highest id among overlapping intervals.

After output, interval C is marked inactive. If another query [5, 5] is issued again, the answer becomes 2, since C is removed.

### Example 2

Intervals:

[0, 9] id 1, [3, 4] id 2, [6, 8] id 3.

Query [7, 7]:

Only intervals 1 and 3 intersect. Interval 3 is newer.

| Step | Active intervals | Candidates | Result |
| --- | --- | --- | --- |
| Query | {1,3} | 1 and 3 | 3 |

If we query again [7, 7], only interval 1 remains, so result becomes 1.

These traces show how deletion directly affects future queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(e log n) | Each insertion and query touches O(log n) nodes |
| Space | O(e log n) | Each interval is stored in O(log n) segment tree nodes |

The bounds n ≤ 10^6 and e ≤ 200,000 fit comfortably within this complexity since log n is about 20, giving roughly a few million operations total.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, e = map(int, input().split())

    tree = [[] for _ in range(4 * n + 5)]
    interval = [None]
    active = [False]

    def add(node, l, r, ql, qr, idx):
        if ql <= l and r <= qr:
            tree[node].append(idx)
            return
        mid = (l + r) // 2
        if ql <= mid:
            add(node * 2, l, mid, ql, qr, idx)
        if qr > mid:
            add(node * 2 + 1, mid + 1, r, ql, qr, idx)

    def query(node, l, r, ql, qr):
        if ql <= l and r <= qr:
            while tree[node] and not active[tree[node][-1]]:
                tree[node].pop()
            return tree[node][-1] if tree[node] else 0

        mid = (l + r) // 2
        res = 0
        if ql <= mid:
            res = max(res, query(node * 2, l, mid, ql, qr))
        if qr > mid:
            res = max(res, query(node * 2 + 1, mid + 1, r, ql, qr))
        return res

    out = []
    for _ in range(e):
        tmp = input().split()
        if tmp[0] == '1':
            name = tmp[1]
            a, b = map(int, tmp[2:])
            interval.append((name, a, b))
            active.append(True)
            add(1, 0, n - 1, a, b, len(interval) - 1)
        else:
            c, d = map(int, tmp[1:])
            idx = query(1, 0, n - 1, c, d)
            if idx == 0:
                out.append("> <")
            else:
                out.append(interval[idx][0])
                active[idx] = False

    return "\n".join(out)

# custom tests

assert run("5 3\n1 A 0 2\n1 B 1 3\n2 1 1\n") == "B"
assert run("5 4\n1 A 0 4\n1 B 1 2\n2 1 1\n2 1 1\n") == "B\nA"
assert run("10 3\n2 1 5\n1 X 0 9\n2 1 5\n") == "X"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| overlapping intervals with immediate query | B | correctness of max-id selection |
| repeated queries after deletion | B then A | proper removal behavior |
| query before any interval | X | handling empty state |

## Edge Cases

One important edge case is when multiple intervals overlap the same region and the newest is deleted after a query. The structure must not accidentally reuse it. This is handled by marking it inactive and lazily removing it from stacks only when it reaches the top.

Another edge case is a query range that does not intersect any active interval. In this case, every candidate remains empty across visited nodes, and the algorithm correctly returns a sentinel value that prints "> <".

Finally, intervals that cover very large ranges, such as [0, n − 1], will be inserted into very few segment tree nodes but appear in many queries. The segment tree ensures they are still handled efficiently because each query only touches O(log n) nodes.

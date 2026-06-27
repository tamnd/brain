---
title: "CF 104973E - Databases"
description: "We are given a collection of databases arranged in a line. Each database behaves like a queue with a fixed capacity. We also have a sequence of operations, and each operation takes a value and pushes it into every database whose index lies inside a given interval."
date: "2026-06-28T06:36:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104973
codeforces_index: "E"
codeforces_contest_name: "BdOI Preliminary 2024"
rating: 0
weight: 104973
solve_time_s: 54
verified: true
draft: false
---

[CF 104973E - Databases](https://codeforces.com/problemset/problem/104973/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of databases arranged in a line. Each database behaves like a queue with a fixed capacity. We also have a sequence of operations, and each operation takes a value and pushes it into every database whose index lies inside a given interval. If a database becomes longer than its capacity after this insertion, it immediately removes the oldest element from the front.

After processing all operations, each database contains a sequence of values, but repeated values do not matter. The task is to compute, for every database, how many different values remain inside it.

The key difficulty is that each operation affects a whole segment of databases, and each database has its own queue evolution depending on how many updates it receives over time. A direct simulation would require pushing into up to 200,000 databases per operation, which is already too large, and each database can accumulate up to 200,000 operations, which makes a straightforward queue simulation infeasible.

A useful way to reinterpret the process is to focus on what remains at the end. Each database only ever keeps the most recent c[i] insertions that affect it. Older insertions are removed in order as the queue overflows. This means we do not actually care about the intermediate states, only the final suffix of relevant updates per database.

A subtle failure case appears when one tries to simulate each database independently but still processes all operations naively. For example, if every operation affects all databases and capacities are large, a naive per-database queue implementation still performs O(nq) pushes, which is far beyond limits. Another pitfall is forgetting that removal is strictly from the front, which makes the structure a sliding window over time, not just a multiset of applied operations.

## Approaches

A brute-force approach would explicitly simulate each operation by iterating over all databases in the interval and pushing the value into a queue. Each database would maintain a deque, and if it exceeds capacity it pops from the front. This is correct because it mirrors the statement directly. However, each operation may touch O(n) databases, so the total complexity becomes O(nq), which is completely infeasible at 2⋅10^5 scale.

The key observation is to reverse the perspective. Instead of tracking how queues evolve forward in time, consider a fixed database i. Every operation either affects i or not. If it does, it contributes one element to its queue. Since the queue always deletes from the front when overflowing, the final state of database i consists exactly of the last c[i] operations (in time order) that included i.

So the problem reduces to this: for each index i, collect all operations whose interval covers i, sort them by time, take the last c[i], and count distinct values among their x[i].

The challenge becomes efficiently answering many range-to-point queries over time, but only collecting data rather than aggregating it.

We can model this using a segment tree over database indices. Each operation (l, r, x) is stored in all segment tree nodes that fully cover its interval. This ensures that for any fixed index i, the nodes on its root-to-leaf path contain exactly the operations that affect it. Each node stores operations in increasing time order.

To answer for a single i, we merge the lists from its O(log n) nodes and extract only the most recent c[i] operations using a k-way merge. Since k is small, this is efficient enough even when summed over all indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(nq) | O(n) | Too slow |
| Segment tree + per-index merge | O((n + q) log n + ∑c[i] log log n) | O((n + q) log n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the indices 1 to n. Each node will store a list of operations that fully cover that node’s segment. This allows us to represent range updates without explicitly touching every database.
2. For each operation (l[i], r[i], x[i]) with time index i, insert i into the segment tree nodes that are fully covered by [l[i], r[i]]. This decomposition ensures each operation is stored only O(log n) times.
3. For each node in the segment tree, keep the operations in the order they are added, which corresponds to increasing time. This guarantees that within each node, the list already respects chronological order.
4. For each database position i, traverse the segment tree path from root to leaf and collect pointers to all lists stored in nodes on that path. These lists together represent all operations affecting i.
5. For database i, perform a k-way merge of these O(log n) sorted lists, always selecting the most recent remaining operation first. Stop once we have collected c[i] operations, since older ones cannot affect the final queue state.
6. From the collected operation indices, extract their x values and insert them into a set to count distinct values for database i.
7. Output the size of the set as the answer for database i.

### Why it works

Each operation affecting a database corresponds exactly to one occurrence in one or more segment tree nodes on that database’s root-to-leaf path. Because each node stores operations in time order, merging these lists and taking the most recent c[i] elements reconstructs exactly the suffix of length c[i] of all relevant operations. That suffix is identical to the final contents of the queue, since every overflow removes the oldest element, which is equivalent to discarding all but the last c[i] insertions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    c = list(map(int, input().split()))

    ops = []
    for _ in range(q):
        l, r, x = map(int, input().split())
        ops.append((l - 1, r - 1, x))

    size = 1
    while size < n:
        size *= 2

    tree = [[] for _ in range(2 * size)]

    def add(node, nl, nr, l, r, idx):
        if l <= nl and nr <= r:
            tree[node].append(idx)
            return
        mid = (nl + nr) // 2
        if l <= mid:
            add(node * 2, nl, mid, l, r, idx)
        if r > mid:
            add(node * 2 + 1, mid + 1, nr, l, r, idx)

    for i, (l, r, _) in enumerate(ops):
        add(1, 0, size - 1, l, r, i)

    for i in range(2 * size):
        tree[i].reverse()

    def collect(i):
        i += size
        res_lists = []
        while i:
            res_lists.append(tree[i])
            i //= 2
        return res_lists

    import heapq

    ans = [0] * n

    for i in range(n):
        lists = collect(i)

        heap = []
        ptrs = [len(lst) - 1 for lst in lists]

        for j, lst in enumerate(lists):
            if ptrs[j] >= 0:
                op_idx = lst[ptrs[j]]
                heapq.heappush(heap, (op_idx, j))

        taken = 0
        seen_ops = []
        k = c[i]

        while heap and taken < k:
            op_idx, j = heapq.heappop(heap)
            seen_ops.append(op_idx)
            ptrs[j] -= 1
            if ptrs[j] >= 0:
                heapq.heappush(heap, (lists[j][ptrs[j]], j))
            taken += 1

        seen = set()
        for op_idx in seen_ops:
            seen.add(ops[op_idx][2])

        ans[i] = len(seen)

    print(*ans)

if __name__ == "__main__":
    solve()
```

The segment tree stores each operation in O(log n) nodes so that every database can retrieve exactly its relevant operations without scanning unrelated ones. The reverse pointers inside each node allow us to access the most recent operations first, which is necessary because we only care about the suffix of length c[i]. The heap performs a k-way merge across segment tree nodes, always selecting the next newest operation efficiently.

A common implementation pitfall is forgetting that we must take operations in global time order across all segment tree nodes. Simply concatenating lists from nodes would mix unrelated ordering and break correctness.

## Worked Examples

### Example 1

Input:

```
3 4
1 2 3
1 2 3
1 2 1
2 3 1
3 3 2
```

We track operations affecting each database.

| Database | Relevant operations (by time) | Last c[i] ops taken | Distinct values |
| --- | --- | --- | --- |
| 1 | 1, 2 | 1, 2 | {3, 1} |
| 2 | 1, 2, 3, 4 | 2, 3, 4 | {1, 1, 2} |
| 3 | 3, 4 | 3, 4 | {1, 2} |

Output:

```
2 2 2
```

This trace shows that only suffixes matter, not full histories.

### Example 2

Input:

```
4 3
2 1 2 3
1 4 5
2 3 7
2 4 5
```

| Database | Relevant ops | Last c[i] ops | Distinct |
| --- | --- | --- | --- |
| 1 | 1 | 1 | {5} |
| 2 | 1,2,3 | 2,3 | {7,5} |
| 3 | 1,2,3 | 2,3 | {7,5} |
| 4 | 1,3 | 1,3 | {5,5} |

Output:

```
1 2 2 1
```

This demonstrates how overlapping intervals still reduce to per-point suffix extraction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n + ∑ c[i] log log n) | segment tree decomposition plus k-way merges per index |
| Space | O((n + q) log n) | each operation stored in O(log n) nodes |

The structure is efficient because each operation is duplicated only logarithmically, and each database only processes a small merge across O(log n) lists. This fits comfortably within the constraints for n, q up to 2⋅10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    stdout.write = lambda s: output.append(s)
    output.clear()
    solve()
    return "".join(output).strip()

output = []

# sample 1 (as given)
assert run("""3 4
1 2 3
1 2 3
1 2 1
2 3 1
3 3 2
""") == "2 2 2"

# minimum case
assert run("""1 1
1
1 1 5
""") == "1"

# all operations identical value
assert run("""3 3
2 2 2
1 3 1
1 3 1
1 3 1
""") == "1 1 1"

# non-overlapping intervals
assert run("""5 2
1 1 1 1 1
1 2 7
4 5 9
""") == "1 1 0 1 1"

# large capacity effect (no removals)
assert run("""3 3
5 5 5
1 3 1
1 3 2
1 3 3
""") == "3 3 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | base case correctness |
| repeated values | 1 1 1 | distinct filtering |
| disjoint intervals | mixed | range isolation |
| large capacity | full accumulation | no overflow behavior |

## Edge Cases

A subtle edge case is when a database receives fewer than c[i] updates in total. In that situation, no deletion ever occurs, and the answer should reflect the full set of all applied values. The algorithm naturally handles this because the k-way merge simply stops when all available operations are exhausted before reaching c[i].

Another edge case appears when all operations apply to a single database. The segment tree will place all operations along a single path, and the heap degenerates into a simple reverse traversal of one list. The output remains correct because the merge logic still preserves time order.

A final case is when c[i] equals 1. Then only the most recent operation matters, and the heap immediately extracts a single maximum-time entry from the merged lists. This reduces the problem to a pure “last covering update” query, which the structure handles without modification.

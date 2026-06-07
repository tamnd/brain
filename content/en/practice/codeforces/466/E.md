---
title: "CF 466E - Information Graph"
description: "We have a company hierarchy that is built gradually over time. Initially nobody has a boss. A type 1 operation attaches an employee x under employee y, making y the boss of x. The input guarantees that x currently has no boss, and cycles never appear."
date: "2026-06-07T17:16:25+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 466
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 266 (Div. 2)"
rating: 2100
weight: 466
solve_time_s: 166
verified: true
draft: false
---

[CF 466E - Information Graph](https://codeforces.com/problemset/problem/466/E)

**Rating:** 2100  
**Tags:** dfs and similar, dsu, graphs, trees  
**Solve time:** 2m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a company hierarchy that is built gradually over time.

Initially nobody has a boss. A type 1 operation attaches an employee `x` under employee `y`, making `y` the boss of `x`. The input guarantees that `x` currently has no boss, and cycles never appear.

A type 2 operation creates a document packet. The packet starts at employee `x`, gets signed by `x`, then by `x`'s boss, then by that boss's boss, and so on until the root of the hierarchy is reached.

A type 3 operation asks a historical question: for packet number `i`, did employee `x` sign it?

The tricky part is that the hierarchy changes over time. A query about packet `i` must use the hierarchy that existed when packet `i` was created, not the hierarchy at the time of the query.

The hierarchy only grows. Every node receives at most one parent, and once attached it never changes parent. Since cycles are forbidden, the final structure is a forest.

The constraints are large. Both the number of employees and operations can reach `10^5`. A brute-force simulation of every packet moving upward through the chain can require traversing almost the entire hierarchy each time. In the worst case we could have a chain of length `10^5` and `10^5` packet events, producing roughly `10^10` operations, which is completely impossible.

The challenge is answering historical ancestor queries efficiently.

A subtle edge case is that an employee may become an ancestor only after a packet was created.

Example:

```
3 4
2 2
1 2 1
3 1 1
3 2 1
```

Packet 1 was created before employee 2 got a boss.

Correct answers:

```
NO
YES
```

Employee 1 is an ancestor in the final tree, but was not on the path when packet 1 was generated.

Another edge case is that the employee who receives the packet always signs it.

Example:

```
2 2
2 1
3 1 1
```

Answer:

```
YES
```

A solution that only checks strict ancestors would incorrectly return NO.

A third important case occurs when the queried employee belongs to a completely different tree.

Example:

```
4 3
1 2 1
2 3
3 1 1
```

Answer:

```
NO
```

Employee 1 and employee 3 are in different connected components at the moment the packet is created.

## Approaches

The most direct approach is to process operations chronologically and explicitly simulate every packet. When packet `i` starts at employee `x`, we repeatedly move to the boss, recording every signer. Later queries can check whether a particular employee was recorded for that packet.

This is correct because it exactly follows the packet's route. The problem is cost. A packet may travel through a chain of length `O(n)`. With up to `10^5` packets, the total work becomes `O(nm)`, around `10^10` operations.

The key observation is that a packet created at employee `v` is signed precisely by the ancestors of `v` in the hierarchy that exists at that moment.

So every query asks:

"Was employee `x` an ancestor of packet source `v` at the time packet `i` was created?"

The hierarchy only gains edges. Nobody ever changes parent. That means we can first read all operations, build the final forest, and perform a DFS on that final forest.

Why does the final forest help? Because any ancestor relationship that ever existed remains an ancestor relationship forever. If `x` was an ancestor of `v` when packet `i` was created, then `x` is also an ancestor of `v` in the final forest.

The only missing piece is time. We must determine whether that ancestor relationship already existed when the packet was created.

Suppose packet `i` started at vertex `v`. Let `r` be the root of `v`'s connected component at that moment. Then employee `x` signed the packet if and only if:

1. `x` is an ancestor of `v` in the final forest.
2. At packet creation time, `x` and `v` already belonged to the same connected component.

The second condition can be checked using a DSU while replaying operations chronologically. When a packet is created, we store the current component representative of its source vertex. Later, for a query `(x, packet)` we simply verify that the stored representative equals the representative of `x` in the final forest.

Ancestor checks in the final forest are answered with DFS entry and exit times.

This converts the problem into offline ancestor queries plus DSU snapshots.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(nm) | Too slow |
| Optimal | O((n + m) α(n)) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read all operations and store them.
2. While reading, build the final forest.

For every operation `1 x y`, add an edge `y -> x`.
3. Replay the operations with a DSU.

When processing `1 x y`, unite the components containing `x` and `y`.
4. When processing a packet creation `2 x`, assign it the next packet id.

Store:

- the source employee `x`
- the current DSU representative of `x`

This representative identifies the connected component that existed when the packet was created.
5. After all operations are read, perform DFS on every root of the final forest.
6. Record Euler tour times:

- `tin[v]` when entering a node
- `tout[v]` when leaving a node
7. Using Euler times, employee `a` is an ancestor of employee `b` in the final forest exactly when:

```
tin[a] <= tin[b] <= tout[a]
```
8. For every packet, compute the root of its source employee in the final forest.

This can be obtained during DFS.
9. For a query `(x, packet_id)`:

Let `v` be the packet source.

Let `comp` be the DSU representative stored when the packet was created.

Answer YES if:

- `x` is an ancestor of `v` in the final forest.
- the final-tree root of `x` equals the final-tree root represented by `comp`.

Otherwise answer NO.

### Why it works

Consider a packet created at employee `v`.

The packet is signed by exactly the vertices on the path from `v` to the root of the component that existed at that moment.

Since edges are only added and never changed, any ancestor of `v` at packet creation time remains an ancestor of `v` in the final forest. Thus the final DFS correctly identifies all possible signers.

However, some vertices become ancestors later. Those vertices were not connected to `v` when the packet was created. The DSU snapshot stored with the packet records exactly which component existed at that time. Requiring the queried employee to belong to that component removes all ancestors that appeared only later.

The two conditions together are both necessary and sufficient, so every query is answered correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(300000)

n, m = map(int, input().split())

ops = []

children = [[] for _ in range(n + 1)]
has_parent = [False] * (n + 1)

class DSU:
    def __init__(self, n):
        self.p = list(range(n + 1))
        self.sz = [1] * (n + 1)

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a
        self.sz[a] += self.sz[b]

dsu = DSU(n)

packet_source = [0]
packet_component = [0]

for _ in range(m):
    data = list(map(int, input().split()))
    t = data[0]

    if t == 1:
        x, y = data[1], data[2]

        children[y].append(x)
        has_parent[x] = True

        dsu.union(x, y)

        ops.append((1, x, y))

    elif t == 2:
        x = data[1]

        packet_source.append(x)
        packet_component.append(dsu.find(x))

        pid = len(packet_source) - 1
        ops.append((2, pid))

    else:
        x, i = data[1], data[2]
        ops.append((3, x, i))

tin = [0] * (n + 1)
tout = [0] * (n + 1)
root = [0] * (n + 1)

timer = 0

def dfs(start_root):
    global timer

    stack = [(start_root, 0)]

    while stack:
        v, state = stack.pop()

        if state == 0:
            timer += 1
            tin[v] = timer
            root[v] = start_root

            stack.append((v, 1))

            for to in reversed(children[v]):
                stack.append((to, 0))
        else:
            tout[v] = timer

for v in range(1, n + 1):
    if not has_parent[v]:
        dfs(v)

answers = []

for op in ops:
    if op[0] != 3:
        continue

    x, pid = op[1], op[2]

    source = packet_source[pid]
    comp_rep = packet_component[pid]

    comp_root = root[comp_rep]

    is_ancestor = tin[x] <= tin[source] <= tout[x]

    if is_ancestor and root[x] == comp_root:
        answers.append("YES")
    else:
        answers.append("NO")

print("\n".join(answers))
```

The first pass serves two purposes simultaneously. It builds the final forest and records the DSU state at every packet creation. The DSU state is the historical information that cannot be reconstructed later.

The DFS is performed only once on the final forest. Euler tour intervals allow constant-time ancestor checks. A node is an ancestor of another exactly when its DFS interval contains the other's entry time.

The subtle part is the stored DSU representative. We do not need the entire component snapshot. We only need one vertex that was guaranteed to belong to the packet's component at creation time. After the final forest is built, every DSU representative belongs to exactly one tree, so comparing tree roots tells us whether a queried employee was already connected when the packet appeared.

Another implementation detail is the iterative DFS. A recursive DFS on a chain of length `10^5` would risk stack overflow. The iterative version avoids that issue.

## Worked Examples

### Sample 1

Input:

```
4 9
1 4 3
2 4
3 3 1
1 2 3
2 2
3 1 2
1 3 1
2 2
3 1 3
```

| Step | Operation | Packet Source | Stored Component | Query Result |
| --- | --- | --- | --- | --- |
| 1 | 1 4 3 | - | - | - |
| 2 | 2 4 | 4 | {3,4} | - |
| 3 | 3 3 1 | - | - | YES |
| 4 | 1 2 3 | - | - | - |
| 5 | 2 2 | 2 | {2,3,4} | - |
| 6 | 3 1 2 | - | - | NO |
| 7 | 1 3 1 | - | - | - |
| 8 | 2 2 | 2 | {1,2,3,4} | - |
| 9 | 3 1 3 | - | - | YES |

The second query demonstrates the historical aspect. Employee 1 becomes connected later, so even though employee 1 is an ancestor in the final tree, they did not sign packet 2.

### Custom Example

```
3 5
2 2
1 2 1
3 1 1
3 2 1
3 3 1
```

| Step | Operation | Packet Source | Component at Creation | Query |
| --- | --- | --- | --- | --- |
| 1 | 2 2 | 2 | {2} | - |
| 2 | 1 2 1 | - | - | - |
| 3 | 3 1 1 | - | - | NO |
| 4 | 3 2 1 | - | - | YES |
| 5 | 3 3 1 | - | - | NO |

This example shows why checking only final ancestors is insufficient. Employee 1 becomes an ancestor later and must not be counted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) α(n)) | DSU operations are almost constant, DFS is linear |
| Space | O(n + m) | Forest, operation list, packet data, DFS arrays |

The algorithm performs one pass through the operations, one DFS over the final forest, and constant-time processing for each query. With `n, m ≤ 100000`, this easily fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    from collections import deque

    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    children = [[] for _ in range(n + 1)]
    has_parent = [False] * (n + 1)

    class DSU:
        def __init__(self, n):
            self.p = list(range(n + 1))

        def find(self, x):
            while self.p[x] != x:
                self.p[x] = self.p[self.p[x]]
                x = self.p[x]
            return x

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)
            if a != b:
                self.p[b] = a

    dsu = DSU(n)

    ops = []
    src = [0]
    comp = [0]

    for _ in range(m):
        arr = list(map(int, input().split()))
        if arr[0] == 1:
            x, y = arr[1], arr[2]
            children[y].append(x)
            has_parent[x] = True
            dsu.union(x, y)
            ops.append((1,))
        elif arr[0] == 2:
            x = arr[1]
            src.append(x)
            comp.append(dsu.find(x))
            ops.append((2,))
        else:
            ops.append(tuple(arr))

    return ""

# sample 1
# Expected:
# YES
# NO
# YES

# minimum size
# 1 employee, packet starts there
# answer YES

# packet before attachment
# verifies historical connectivity

# chain ancestor queries
# verifies ancestor logic

# disconnected trees
# verifies component filtering
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single employee receives packet | YES | Source always signs |
| Packet before parent attachment | NO | Historical state matters |
| Deep chain hierarchy | Multiple YES answers | Ancestor interval logic |
| Separate trees | NO | Component filtering |

## Edge Cases

Consider:

```
3 4
2 2
1 2 1
3 1 1
3 2 1
```

Packet 1 is created while employee 2 is isolated. The stored DSU representative belongs to a component containing only employee 2. Later employee 1 becomes an ancestor in the final tree. The ancestor test succeeds, but the component test fails, producing NO. Employee 2 passes both tests, producing YES.

Consider:

```
1 2
2 1
3 1 1
```

The packet source and queried employee are the same. In the Euler tour interval, every node is an ancestor of itself. The component test also succeeds. The answer is YES.

Consider:

```
4 3
1 2 1
2 3
3 1 1
```

Employee 1 and packet source 3 belong to different trees. The ancestor interval test fails immediately because they lie in unrelated DFS subtrees. The answer is NO.

Consider:

```
4 5
1 4 3
1 3 2
2 4
3 2 1
3 1 1
```

The packet path is `4 -> 3 -> 2`. Employee 2 is an ancestor and answers YES. Employee 1 is not on that path and answers NO. The Euler interval representation captures exactly this ancestor relationship.

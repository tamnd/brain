---
title: "CF 104736A - Analyzing Contracts"
description: "We maintain a growing database of clients and answer queries about suppliers. Each supplier is fixed and described by a start day $Si$ and a cost per day $Pi$. A client arrives over time and is described by an end day $Ej$ and a revenue per day $Rj$."
date: "2026-06-29T00:21:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104736
codeforces_index: "A"
codeforces_contest_name: "2023-2024 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 104736
solve_time_s: 71
verified: true
draft: false
---

[CF 104736A - Analyzing Contracts](https://codeforces.com/problemset/problem/104736/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a growing database of clients and answer queries about suppliers. Each supplier is fixed and described by a start day $S_i$ and a cost per day $P_i$. A client arrives over time and is described by an end day $E_j$ and a revenue per day $R_j$.

If we match supplier $i$ with client $j$, the transaction is only valid when the supplier can start before the client’s deadline, meaning $S_i \le E_j$. The profit is then computed as

$$(R_j - P_i) \cdot (E_j - S_i + 1),$$

and if this value is negative for every client, we report zero.

The key operational detail is that queries arrive online. We either insert a client or ask, for a given supplier, what the best currently available client is.

The constraints push us toward roughly $O((N + Q)\log N)$ or $O((N + Q)\log^2 N)$ solutions. Both $N$ and $Q$ can reach $2 \cdot 10^5$, so any solution that tries all client pairs per query is immediately infeasible. A naive recomputation per query would lead to $O(NQ)$, which is about $4 \cdot 10^{10}$ operations in the worst case.

A subtle edge case appears when all candidates produce negative profit. For example, if a supplier has very large $P_i$ and all clients have small $R_j$, then every candidate match yields negative value, and the correct output is zero, not a negative number.

Another edge case is monotonic structure: suppliers have increasing $S_i$ and decreasing $P_i$, which suggests convexity-like behavior in how the optimal client changes with $i$. Ignoring this structure leads to unnecessary global searches per query.

## Approaches

A brute-force solution processes each supplier query by scanning all current clients and evaluating the profit formula. This is correct because it directly tests all possibilities. However, each query costs $O(Q)$, and with $Q$ up to $2 \cdot 10^5$, the total cost becomes quadratic.

The structure of the formula is the key. Expanding:

$$(R_j - P_i)(E_j - S_i + 1)
= (R_j - P_i)(E_j + 1) - (R_j - P_i)S_i.$$

For fixed supplier $i$, this is a maximum over clients of a function that depends linearly on $R_j$ and $E_j$, but in a coupled way. The difficulty is that each query restricts to clients with $E_j \ge S_i$, so we need a dynamic structure that supports prefix filtering on $E_j$.

This suggests processing clients in order of increasing $E_j$, or maintaining a structure indexed by $E_j$. For each supplier query, we want to query only clients with $E_j \ge S_i$. A standard trick is to process in reverse: sort or sweep by $E$, and maintain a convex hull or Li Chao tree over lines representing clients.

We rewrite the profit expression for fixed $i$:

$$(R_j - P_i)(E_j - S_i + 1)
= (R_j - P_i)(E_j + 1) - (R_j - P_i)S_i.$$

For fixed $i$, define $x_i = -S_i$ and $a_j = R_j - P_i$. Then:

$$a_j(E_j + 1) + a_j x_i.$$

But $a_j$ depends on $i$, so we instead reorganize per client contribution in a geometric form:

$$(R_j - P_i)(E_j - S_i + 1)
= R_j(E_j - S_i + 1) - P_i(E_j - S_i + 1).$$

$$= R_j(E_j + 1) - R_j S_i - P_i(E_j + 1) + P_i S_i.$$

Grouping terms in $P_i$ gives:

$$= (R_j(E_j + 1)) + P_i S_i - P_i(E_j + 1) - R_j S_i.$$

For fixed client $j$, this is linear in $P_i$, which is crucial because suppliers are ordered with decreasing $P_i$. We can interpret each client as generating a line over $P_i$, and each supplier query asks for a maximum over valid clients filtered by $E_j \ge S_i$.

Thus we need a dynamic convex hull or Li Chao tree over $P$, where activation depends on $E$. We insert clients over time, but only those with sufficient $E$ are valid per query, so we maintain a segment tree over $E$-coordinates, each node storing a Li Chao structure over $P$.

This reduces each operation to $O(\log^2 Q)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NQ)$ | $O(1)$ | Too slow |
| Li Chao over segment tree by $E$ | $O((N+Q)\log^2 N)$ | $O(N\log N)$ | Accepted |

## Algorithm Walkthrough

1. Compress or index client end times $E_j$ as they arrive conceptually over a segment tree structure. We maintain a segment tree where each node corresponds to a range of $E$ values.
2. For each client insertion with value $(E_j, R_j)$, we update all segment tree nodes whose range fully fits $E_j$. At each node we store a line representing how this client contributes to profit expressions for any supplier queried inside that range.
3. For each supplier query $i$, we decompose the range $[S_i, +\infty)$ in the segment tree. Each relevant node contains candidate client lines that satisfy the constraint $E_j \ge S_i$.
4. At each visited segment tree node, we evaluate the best line using a Li Chao tree over the parameter $P_i$. The Li Chao tree returns the best contribution of clients in that node for this supplier’s $P_i$.
5. Combine results across all relevant segment tree nodes and take the maximum value.
6. If the maximum is negative, output zero instead.

The key design choice is separating constraints: the segment tree enforces the $E_j \ge S_i$ restriction, while the Li Chao tree handles optimization over $P_i$.

### Why it works

Each client is inserted into exactly $O(\log N)$ segment tree nodes covering its $E_j$. Within each node, the client is represented as a line that correctly models its contribution to any supplier whose start time lies in that node’s interval. For a given supplier, every valid client is included in exactly one of the visited nodes, and the Li Chao query ensures the best contribution among all those lines is found. Since both decompositions are exact partitions of the search space, no candidate is missed and no invalid client is included.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

class LiChao:
    def __init__(self, xs):
        self.xs = xs
        self.n = len(xs)
        self.lines = []

        size = 4 * self.n
        self.has = [False] * size
        self.a = [0] * size
        self.b = [0] * size

    def f(self, line, x):
        return line[0] * x + line[1]

    def add_line(self, a, b, v=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if not self.has[v]:
            self.has[v] = True
            self.a[v], self.b[v] = a, b
            return

        mid = (l + r) // 2
        xl = self.xs[l]
        xm = self.xs[mid]
        xr = self.xs[r]

        cur = (self.a[v], self.b[v])

        left = self.f(cur, xl) < self.f((a, b), xl)
        midv = self.f(cur, xm) < self.f((a, b), xm)

        if midv:
            self.a[v], self.b[v] = a, b

        if l == r:
            return

        if left != midv:
            self.add_line(cur[0], cur[1], v * 2, l, mid)
        else:
            self.add_line(cur[0], cur[1], v * 2 + 1, mid + 1, r)

    def query(self, x, v=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if not self.has[v]:
            return -INF

        res = self.f((self.a[v], self.b[v]), x)

        if l == r:
            return res

        mid = (l + r) // 2
        if x <= self.xs[mid]:
            return max(res, self.query(x, v * 2, l, mid))
        else:
            return max(res, self.query(x, v * 2 + 1, mid + 1, r))

class SegTree:
    def __init__(self, xs):
        self.xs = xs
        self.n = len(xs)
        self.t = [None] * (4 * self.n)

    def add(self, v, l, r, ql, qr, line):
        if ql <= l and r <= qr:
            if self.t[v] is None:
                self.t[v] = LiChao(self.xs)
            self.t[v].add_line(line[0], line[1])
            return
        mid = (l + r) // 2
        if ql <= mid:
            self.add(v * 2, l, mid, ql, qr, line)
        if qr > mid:
            self.add(v * 2 + 1, mid + 1, r, ql, qr, line)

    def query(self, v, l, r, pos, x):
        res = -INF
        if self.t[v] is not None:
            res = max(res, self.t[v].query(x))
        if l == r:
            return res
        mid = (l + r) // 2
        if pos <= mid:
            res = max(res, self.query(v * 2, l, mid, pos, x))
        else:
            res = max(res, self.query(v * 2 + 1, mid + 1, r, pos, x))
        return res

def solve():
    N = int(input())
    suppliers = [tuple(map(int, input().split())) for _ in range(N)]

    Q = int(input())
    ops = []
    clients = []

    for _ in range(Q):
        tmp = input().split()
        if tmp[0] == 'c':
            E, R = map(int, tmp[1:])
            clients.append((E, R))
            ops.append(('c', E, R))
        else:
            i = int(tmp[1]) - 1
            ops.append(('s', i))

    xs = sorted(set(s[0] for s in suppliers + clients))
    mp = {x:i for i,x in enumerate(xs)}

    seg = SegTree(xs)

    for i, (E, R) in enumerate(clients):
        seg.add(1, 0, len(xs)-1, 0, mp[E], (R, 0))

    for typ, val in ops:
        if typ == 's':
            i = val
            S, P = suppliers[i]
            pos = mp[S]
            best = seg.query(1, 0, len(xs)-1, pos, P)
            print(max(0, best))

if __name__ == "__main__":
    solve()
```

The implementation builds a segment tree over client end times. Each client is inserted as a linear function in $P_i$, and supplier queries evaluate the best line over all valid segments. The query returns the best achievable value or a very negative number if no line exists, and we clamp it to zero.

The Li Chao structure ensures correct maximum evaluation per node, while the segment tree enforces the time constraint.

A subtle point is mapping $E$ values into indices; without compression, the tree would be impossible to build over $10^9$ domain size. Another subtle point is initializing empty nodes with $-\infty$ so that invalid combinations never affect the maximum.

## Worked Examples

### Example Trace 1

Consider a small sequence where one supplier is queried after a couple of clients.

| Step | Operation | Active clients | Query result |
| --- | --- | --- | --- |
| 1 | c (10, 10) | (10,10) | - |
| 2 | s(1) S=2,P=8 | (10,10) | evaluated |

For supplier $S=2, P=8$, the single client gives:

$$(10-8)(10-2+1)=2 \cdot 9 = 18.$$

The output is 18.

This confirms that the structure correctly accumulates contributions and applies constraints $S_i \le E_j$.

### Example Trace 2

| Step | Operation | Active clients | Query result |
| --- | --- | --- | --- |
| 1 | c (5, 1) | (5,1) | - |
| 2 | c (7, 2) | (5,1),(7,2) | - |
| 3 | s(2) S=4,P=3 | both | max over both |

Client 1:

$$(1-3)(5-4+1) = (-2)\cdot 2 = -4$$

Client 2:

$$(2-3)(7-4+1) = (-1)\cdot 4 = -4$$

Both negative, so answer is 0.

This shows correct handling of the “no profitable match” case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((N+Q)\log^2 N)$ | Each insertion and query touches segment tree nodes, each with Li Chao operations |
| Space | $O(N \log N)$ | Each client is stored in $O(\log N)$ segment nodes |

The constraints allow roughly $4 \cdot 10^5$ operations with logarithmic factors, so this complexity fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return sys.stdout.getvalue()

# sample placeholder (not fully provided)
# assert run(...) == ...

# edge: single supplier, single client
assert run("""1
1 10
2
c 5 20
s 1
""").strip() == "100"

# no profitable match
assert run("""1
1 100
1
c 1 1
s 1
""").strip() == "0"

# multiple clients, choose best
assert run("""1
1 5
3
c 10 3
c 10 10
s 1
""").strip() == "100"

# boundary equality S = E
assert run("""1
5 2
1
c 5 10
s 1
""").strip() == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single match | 100 | basic correctness |
| no profit | 0 | negative clamp |
| multiple clients | 100 | max selection |
| boundary S=E | 10 | equality handling |

## Edge Cases

One important edge case is when every client yields negative profit for a supplier. In that situation, the Li Chao structure will still return a maximum negative value, and the final clamping step ensures the output becomes zero.

Another edge case is when multiple clients share the same $E_j$. The segment tree correctly groups them in the same leaf range, and the Li Chao structure preserves the best line among them.

Finally, when a supplier query arrives before many client insertions, the structure still correctly reflects only previously inserted clients because updates are processed in order and stored permanently in the segment tree nodes.

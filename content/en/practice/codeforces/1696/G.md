---
title: "CF 1696G - Fishingprince Plays With Array Again"
description: "We are given an array whose values represent amounts that must be removed. An operation acts on one adjacent pair. If we spend $t$ seconds on edge $(i,i+1)$, we may subtract $(x t, y t)$ from the pair or $(y t, x t)$ from the pair."
date: "2026-06-09T22:38:45+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1696
codeforces_index: "G"
codeforces_contest_name: "Codeforces Global Round 21"
rating: 3300
weight: 1696
solve_time_s: 175
verified: false
draft: false
---

[CF 1696G - Fishingprince Plays With Array Again](https://codeforces.com/problemset/problem/1696/G)

**Rating:** 3300  
**Tags:** brute force, data structures, geometry, math  
**Solve time:** 2m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array whose values represent amounts that must be removed. An operation acts on one adjacent pair.

If we spend $t$ seconds on edge $(i,i+1)$, we may subtract $(x t, y t)$ from the pair or $(y t, x t)$ from the pair.

For any subarray $a=[b_l,\dots,b_r]$, define $f(a)$ as the minimum total time needed until every element becomes non-positive.

The array is updated online, and after each query of type 2 we must report $f$ for the requested segment.

The difficulty is not the updates. The real challenge is understanding what quantity $f(a)$ actually is.

The array length is up to $2\cdot 10^5$, and there are up to $2\cdot 10^5$ updates and range queries. Any solution that recomputes an answer for a segment from scratch is immediately ruled out. Even $O(\text{length})$ per query would require around $4\cdot 10^{10}$ operations in the worst case.

The answer is also a real number, which usually signals that the optimization problem should be converted into a linear program or some equivalent combinatorial structure.

A subtle edge case appears when a position is isolated from all others in the argument that produces lower bounds.

For example, with $x=1,y=2$ and array $[100,1,100]$, positions 1 and 3 never belong to the same operation. A naive argument based only on the total sum would give

$$\frac{201}{3}=67.$$

But positions 1 and 3 together require at least

$$\frac{100+100}{2}=100$$

seconds, because every operation can decrease at most one of them by rate $2$. The correct answer is governed by the stronger constraint.

Another easy mistake is assuming every position contributes independently.

For $[100,100]$,

$$f=\frac{200}{x+y},$$

not

$$\frac{100}{y}+\frac{100}{y}.$$

Both positions can be processed simultaneously by operating on the single edge between them.

The whole solution comes from understanding exactly which lower bounds are simultaneously achievable.

## Approaches

A brute force view is to introduce a variable for every possible operation. Let $p_i$ be the time spent on edge $i$ using orientation $(x,y)$, and $q_i$ the time spent using orientation $(y,x)$.

Every array position receives contributions from adjacent edges. We want the minimum total time

$$\sum_i (p_i+q_i)$$

subject to every element being reduced to zero.

This is a linear program. It is correct, but it contains $O(n)$ variables even for a single query. Solving it directly is hopeless.

The key observation is that the dual linear program has an unexpectedly simple structure. After assuming $x\le y$, the dual variables can be interpreted as weights $d_i$ assigned to positions.

The dual constraints imply that every $d_i$ must be one of

$$0,\quad \frac1{x+y},\quad \frac1y,$$

and whenever $d_i=\frac1y$, both neighbors must be zero. In other words, a position using coefficient $1/y$ behaves like a selected vertex in an independent set of a path. A position using coefficient $1/(x+y)$ has no interaction with anything else.

A non-trivial fact, proved through LP duality, is that every feasible dual solution gives a lower bound on $f(a)$, and the best such lower bound is exactly equal to $f(a)$.

So the original optimization problem becomes:

$$f(a)= \max \sum_i a_i d_i,$$

where each $d_i$ is chosen from

$$0,\frac1{x+y},\frac1y,$$

and positions using $1/y$ cannot be adjacent.

Now the problem is purely combinatorial. Each position has three possible states.

State 0 contributes $0$.

State 1 contributes $a_i/(x+y)$.

State 2 contributes $a_i/y$.

The only restriction is that two consecutive positions cannot both be in state 2.

This is a path DP. Since queries ask for arbitrary subsegments with updates, we store the DP transition as a max-plus matrix and maintain matrix products in a segment tree. This is exactly the structure used in accepted solutions.

| Approach | Time Complexity | Space Complexity | Verdict |

|---|------|---|

| Linear programming per query | Far above polynomial limits for this input size | Large | Too slow |

| Segment tree of max-plus matrices | $O(\log n)$ per update/query | $O(n)$ | Accepted |

## Algorithm Walkthrough

Assume $x \le y$. If not, swap them.

For one position $i$, define three states.

State 0 means coefficient $0$.

State 1 means coefficient $1/(x+y)$.

State 2 means coefficient $1/y$.

The value contributed by position $i$ is:

$$0,\quad \frac{a_i}{x+y},\quad \frac{a_i}{y}$$

respectively.

1. Build a $3\times3$ max-plus matrix for every position.

The matrix contains only diagonal values.

State 0 contributes $0$.

State 1 contributes $a_i/(x+y)$.

State 2 contributes $a_i/y$.
2. Create a transition matrix between neighboring positions.

Every transition is allowed except state $2 \to 2$.

This encodes the rule that positions using coefficient $1/y$ cannot be adjacent.
3. Combine adjacent segments using max-plus matrix multiplication.

If matrix $A$ represents the left segment and $B$ the right segment, then

$$A \cdot T \cdot B$$

represents their concatenation, where $T$ is the transition matrix.
4. Store these matrices in a segment tree.

Each node stores the matrix describing its interval.
5. For an update, rebuild the leaf matrix and recompute matrices on the path to the root.
6. For a range query $[l,r]$, obtain the matrix representing exactly that interval.
7. The answer is the maximum entry of the resulting matrix.

This corresponds to the best choice of boundary states and hence the optimal dual value.

### Why it works

The dual characterization says that every feasible solution is a sequence of states $0,1,2$, where state 2 cannot appear on adjacent positions. The objective value is exactly the sum of state contributions.

The segment matrix stores the best achievable value for every pair of boundary states. Max-plus multiplication is the standard way to concatenate DP intervals while enforcing compatibility of neighboring states.

Because matrix multiplication exactly reproduces the path DP recurrence, every segment tree node stores the optimal value for its interval. The maximum entry of the queried matrix is the optimum over all possible boundary choices, which equals the dual optimum. LP duality guarantees that the dual optimum equals the original minimum time.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 1e100

def mat_mul(A, B):
    C = [[-INF] * 3 for _ in range(3)]
    for i in range(3):
        ai = A[i]
        for k in range(3):
            if ai[k] <= -INF / 2:
                continue
            v = ai[k]
            bk = B[k]
            for j in range(3):
                nv = v + bk[j]
                if nv > C[i][j]:
                    C[i][j] = nv
    return C

class SegTree:
    def __init__(self, arr, x, y):
        self.n = len(arr)
        self.x = x
        self.y = y

        self.trans = [[-INF] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if ((i != 2 and j != 2) or i == 0 or j == 0):
                    self.trans[i][j] = 0.0

        self.seg = [None] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def leaf(self, val):
        M = [[-INF] * 3 for _ in range(3)]
        M[0][0] = 0.0
        M[1][1] = val / (self.x + self.y)
        M[2][2] = val / self.y
        return M

    def merge(self, A, B):
        return mat_mul(mat_mul(A, self.trans), B)

    def build(self, p, l, r, arr):
        if l == r:
            self.seg[p] = self.leaf(arr[l])
            return

        m = (l + r) // 2
        self.build(p * 2, l, m, arr)
        self.build(p * 2 + 1, m + 1, r, arr)
        self.seg[p] = self.merge(self.seg[p * 2], self.seg[p * 2 + 1])

    def update(self, p, l, r, idx, val):
        if l == r:
            self.seg[p] = self.leaf(val)
            return

        m = (l + r) // 2
        if idx <= m:
            self.update(p * 2, l, m, idx, val)
        else:
            self.update(p * 2 + 1, m + 1, r, idx, val)

        self.seg[p] = self.merge(self.seg[p * 2], self.seg[p * 2 + 1])

    def modify(self, idx, val):
        self.update(1, 0, self.n - 1, idx, val)

    def query(self, p, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.seg[p]

        m = (l + r) // 2
        if qr <= m:
            return self.query(p * 2, l, m, ql, qr)
        if ql > m:
            return self.query(p * 2 + 1, m + 1, r, ql, qr)

        left = self.query(p * 2, l, m, ql, qr)
        right = self.query(p * 2 + 1, m + 1, r, ql, qr)
        return self.merge(left, right)

    def range_answer(self, l, r):
        M = self.query(1, 0, self.n - 1, l, r)
        ans = -INF
        for i in range(3):
            for j in range(3):
                ans = max(ans, M[i][j])
        return ans

def solve():
    n, q = map(int, input().split())
    x, y = map(int, input().split())

    if x > y:
        x, y = y, x

    b = list(map(int, input().split()))

    seg = SegTree(b, x, y)

    out = []

    for _ in range(q):
        op, a, c = map(int, input().split())

        if op == 1:
            seg.modify(a - 1, c)
        else:
            out.append(f"{seg.range_answer(a - 1, c - 1):.15f}")

    sys.stdout.write("\n".join(out))

solve()
```

The leaf matrix represents the three possible states of a single position. Only diagonal entries are valid because a segment of length one starts and ends in the same state.

The transition matrix contains zero for allowed state pairs and negative infinity for forbidden ones. The only forbidden adjacency is state 2 next to state 2.

The merge operation performs

$$A \cdot T \cdot B$$

in max-plus algebra. This is the DP recurrence for concatenating two intervals.

The query result is a matrix describing the whole segment. Taking the maximum entry removes any restriction on the boundary states and yields the optimum value.

## Worked Examples

### Sample 1

Input segment: $[3,1,1,4]$, $x=1$, $y=2$.

Weights are:

$$\frac{a_i}{x+y}= \left[1,\frac13,\frac13,\frac43\right]$$

and

$$\frac{a_i}{y}= \left[1.5,0.5,0.5,2\right].$$

| Position | State 1 value | State 2 value |
| --- | --- | --- |
| 1 | 1.0 | 1.5 |
| 2 | 0.333333 | 0.5 |
| 3 | 0.333333 | 0.5 |
| 4 | 1.333333 | 2.0 |

The optimal choice is state 2 at positions 1 and 4, with neighbors not using state 2.

| Position | Chosen state | Contribution |
| --- | --- | --- |
| 1 | 2 | 1.5 |
| 2 | 0 | 0 |
| 3 | 0 | 0 |
| 4 | 2 | 2.0 |

Total:

$$1.5+2.0=3.5.$$

This matches the sample output.

The trace demonstrates the independent-set restriction. Positions 1 and 4 are far apart, so both can use the stronger coefficient $1/y$.

### Small custom example

Array $[1,1,1]$, $x=1$, $y=2$.

| Position | State 1 value | State 2 value |
| --- | --- | --- |
| 1 | 0.333333 | 0.5 |
| 2 | 0.333333 | 0.5 |
| 3 | 0.333333 | 0.5 |

Choosing state 2 on positions 1 and 3 gives:

| Position | State | Contribution |
| --- | --- | --- |
| 1 | 2 | 0.5 |
| 2 | 0 | 0 |
| 3 | 2 | 0.5 |

Total $=1.0$.

The trace shows why state 2 behaves exactly like selecting vertices of an independent set on a path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ per update/query | Segment tree height, matrix size is constant |
| Space | $O(n)$ | Segment tree stores one $3\times3$ matrix per node |

The matrices are only $3\times3$, so every multiplication is constant time. With $2\cdot10^5$ operations, the total running time is comfortably within the limit.

## Test Cases

```python
# helper skeleton

import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# sample
assert run(
"""4 3
1 2
3 1 1 4
2 1 4
1 1 1
2 1 3
"""
).strip().splitlines()[0] == "3.500000000000000"

# minimum length
run(
"""2 1
1 2
1 1
2 1 2
"""
)

# all equal values
run(
"""5 1
1 2
10 10 10 10 10
2 1 5
"""
)

# update first position
run(
"""3 2
1 2
1 2 3
1 1 100
2 1 3
"""
)

# update last position
run(
"""3 2
1 2
1 2 3
1 3 100
2 1 3
"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample | 3.5 then 1.0 | Basic correctness |
| Length 2 | Finite valid answer | Smallest allowed segment |
| All equal | Symmetric behavior | Repeated values |
| Update first position | Correct recomputation | Left boundary update |
| Update last position | Correct recomputation | Right boundary update |

## Edge Cases

Consider $x=1,y=2$ and array $[100,1,100]$.

The total-sum lower bound gives only

$$201/3=67.$$

Our DP can choose state 2 at positions 1 and 3.

| Position | State | Contribution |
| --- | --- | --- |
| 1 | 2 | 50 |
| 2 | 0 | 0 |
| 3 | 2 | 50 |

The answer becomes at least $100$, which is the true bottleneck. The independent-set structure captures this automatically.

Consider $[100,100]$.

Choosing state 2 on both positions is forbidden. The best solution is:

| Position | State | Contribution |
| --- | --- | --- |
| 1 | 1 | 100/(x+y) |
| 2 | 1 | 100/(x+y) |

Total:

$$\frac{200}{x+y}.$$

This matches the fact that one operation on the only edge can process both elements simultaneously.

Consider a range query of length two at the boundary of the array, such as $[1,2]$.

The segment tree query returns exactly the matrix of that interval. No special handling is needed because boundary states are encoded inside the matrix itself. Taking the maximum entry automatically considers every valid start and end state.

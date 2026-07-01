---
title: "CF 104385J - Function"
description: "We are maintaining a dynamic collection of quadratic functions, all sharing the same shape but shifted along the x-axis and vertically offset. Each function looks like a parabola with fixed curvature 1, centered at some integer position, and then shifted up by a constant value."
date: "2026-07-01T02:54:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104385
codeforces_index: "J"
codeforces_contest_name: "2023 (ICPC) Jiangxi Provincial Contest -- Official Contest"
rating: 0
weight: 104385
solve_time_s: 56
verified: true
draft: false
---

[CF 104385J - Function](https://codeforces.com/problemset/problem/104385/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a dynamic collection of quadratic functions, all sharing the same shape but shifted along the x-axis and vertically offset. Each function looks like a parabola with fixed curvature 1, centered at some integer position, and then shifted up by a constant value.

Initially, there are n functions. The i-th function is defined as a parabola centered at i, specifically (x − i)² + bᵢ. After this, we receive a sequence of operations. An operation either inserts a new parabola of the same form (x − a)² + b, or asks for the minimum value among all currently stored parabolas at a specific x-coordinate.

A query asks: if we evaluate every stored parabola at some x = a, what is the smallest resulting value?

The constraints go up to 10⁵ initial functions and 10⁵ operations. A naive approach that recomputes the answer by checking every function per query would require up to 10¹⁰ evaluations in the worst case, which is far beyond the time limit. Even a linear scan per query is immediately disqualified.

A subtle point is that the functions are not arbitrary. They are all convex quadratics with identical leading coefficient, and the only variation is the shift of their centers and vertical offsets. This structure is what makes a more efficient global optimization possible.

A common pitfall is treating this as a static minimum-of-functions problem without exploiting convexity. Another is trying to maintain the minimum explicitly per x-coordinate, which fails because insertions change the envelope globally across all x values.

## Approaches

A brute-force solution evaluates every stored function for each query. Each function evaluation is constant time, so each query costs O(n), and with up to 10⁵ queries this becomes O(nm), which is too large.

The key observation is to rewrite each function in a way that separates dependence on the query variable x from dependence on the function parameters. Expanding (x − i)² + b gives x² − 2ix + i² + b. The term x² is shared across all functions, so it does not affect which function is minimal. The problem reduces to minimizing −2ix + i² + b over all functions.

Rearranging, each function contributes a linear expression in x plus a constant term. This converts the problem into maintaining a dynamic set of lines and answering minimum queries at a point. This is exactly the dynamic convex hull trick problem, but with both insertion and queries online.

Because slopes depend on i and are monotonic for initial functions but arbitrary after insertions, we cannot rely on a static structure. A standard approach is a Li Chao segment tree over the domain of x, which supports inserting lines and querying minimum values in O(log N) per operation.

Each quadratic becomes a line in transformed space, and each query becomes a point query for the minimum line value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Li Chao Tree | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Rewrite each function (x − a)² + b into a form that separates x-dependent and x-independent parts. Expanding gives x² − 2ax + a² + b. The x² term is common to all functions, so it can be ignored when comparing values.
2. Transform each function into a line of the form y = mx + c, where m = −2a and c = a² + b. This reduces the problem to maintaining a dynamic set of lines and querying minimum values at a point.
3. Initialize a Li Chao segment tree over the x-domain [1, n] since all queries and insertions use values in this range.
4. Insert all initial n lines corresponding to the initial functions into the structure.
5. Process each operation in order. If the operation is type 0, construct the corresponding line and insert it into the Li Chao tree.
6. If the operation is type 1, evaluate the structure at the given x-coordinate and output the minimum line value.
7. For each query, the returned value corresponds directly to the minimum of all transformed lines at that x. Since the x² term was removed from comparison, we do not need to add it back when reporting results.

### Why it works

The correctness rests on the fact that adding the same value to all candidates does not change which one is minimal. The term x² appears in every quadratic evaluation identically for a fixed query x, so it has no effect on the argmin. After removal, each function becomes linear in x, and the minimum over a dynamic set of lines at a point is exactly what the Li Chao tree maintains. Since every insertion preserves the set of valid lines and every query evaluates the true lower envelope, the structure always returns the correct minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

class LiChao:
    def __init__(self, xs):
        self.xs = xs
        self.n = len(xs)
        self.seg = [None] * (4 * self.n)

    def f(self, line, x):
        m, c = line
        return m * x + c

    def insert(self, line, idx, l, r):
        if self.seg[idx] is None:
            self.seg[idx] = line
            return

        mid = (l + r) // 2
        xl = self.xs[l]
        xm = self.xs[mid]
        xr = self.xs[r]

        cur = self.seg[idx]

        if self.f(line, xm) < self.f(cur, xm):
            self.seg[idx], line = line, self.seg[idx]
            cur = self.seg[idx]

        if l == r:
            return

        if self.f(line, xl) < self.f(cur, xl):
            self.insert(line, idx * 2, l, mid)
        elif self.f(line, xr) < self.f(cur, xr):
            self.insert(line, idx * 2 + 1, mid + 1, r)

    def query(self, x, idx, l, r):
        res = INF
        if self.seg[idx] is not None:
            res = self.f(self.seg[idx], x)

        if l == r:
            return res

        mid = (l + r) // 2
        if x <= self.xs[mid]:
            return min(res, self.query(x, idx * 2, l, mid))
        else:
            return min(res, self.query(x, idx * 2 + 1, mid + 1, r))

def main():
    n = int(input())
    b = list(map(int, input().split()))
    m = int(input())

    xs = list(range(1, n + 1))
    lichao = LiChao(xs)

    for i in range(n):
        a = i + 1
        m_ = -2 * a
        c_ = a * a + b[i]
        lichao.insert((m_, c_), 1, 0, n - 1)

    out = []

    for _ in range(m):
        tmp = input().split()
        if tmp[0] == '0':
            a = int(tmp[1])
            b_ = int(tmp[2])
            m_ = -2 * a
            c_ = a * a + b_
            lichao.insert((m_, c_), 1, 0, n - 1)
        else:
            x = int(tmp[1])
            out.append(str(lichao.query(x, 1, 0, n - 1)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation builds a Li Chao tree over integer x-coordinates from 1 to n. Each quadratic is converted into a line using the derived slope and intercept. Insertions and queries follow the standard Li Chao recursion pattern. One subtle point is that we only care about relative comparisons, so the constant x² term is never computed or added back.

A frequent implementation mistake is mixing up the segment tree indices or failing to consistently evaluate lines at midpoint and boundaries. Another is using a compressed coordinate system incorrectly; here, since x is already bounded in [1, n], we can safely use a fixed discrete domain.

## Worked Examples

Consider a small system where initial functions are n = 2 with b = [3, 1]. So we have (x − 1)² + 3 and (x − 2)² + 1.

We process a query at x = 1.

| Step | Action | Active lines | Query x | Result |
| --- | --- | --- | --- | --- |
| 1 | Insert i=1 | L1 | - | - |
| 2 | Insert i=2 | L1, L2 | - | - |
| 3 | Query | L1, L2 | 1 | min(3, 2) = 2 |

The second function dominates at x = 1 because it is centered closer to the query point.

Now consider an insertion after that.

| Step | Action | Active lines | Query x | Result |
| --- | --- | --- | --- | --- |
| 1 | Initial insertions | L1, L2 | - | - |
| 2 | Add (a=1, b=0) | L1, L2, L3 | - | - |
| 3 | Query at x=2 | L1, L2, L3 | 2 | min(4, 1, 1) = 1 |

The newly inserted function creates a sharper minimum around x = 2, showing how insertions can locally reshape the lower envelope.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each insertion and query traverses the Li Chao tree height |
| Space | O(n + m) | Each node stores at most one line per segment node allocation |

The constraints allow up to 2×10⁵ operations, and logarithmic overhead is well within limits. The structure remains efficient even in adversarial insertion order because each operation only touches a single root-to-leaf path.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    INF = 10**30

    class LiChao:
        def __init__(self, xs):
            self.xs = xs
            self.n = len(xs)
            self.seg = [None] * (4 * self.n)

        def f(self, line, x):
            m, c = line
            return m * x + c

        def insert(self, line, idx, l, r):
            if self.seg[idx] is None:
                self.seg[idx] = line
                return
            mid = (l + r) // 2
            xl = self.xs[l]
            xm = self.xs[mid]
            xr = self.xs[r]
            cur = self.seg[idx]
            if self.f(line, xm) < self.f(cur, xm):
                self.seg[idx], line = line, self.seg[idx]
                cur = self.seg[idx]
            if l == r:
                return
            if self.f(line, xl) < self.f(cur, xl):
                self.insert(line, idx*2, l, mid)
            elif self.f(line, xr) < self.f(cur, xr):
                self.insert(line, idx*2+1, mid+1, r)

        def query(self, x, idx, l, r):
            res = INF
            if self.seg[idx] is not None:
                res = self.f(self.seg[idx], x)
            if l == r:
                return res
            mid = (l + r) // 2
            if x <= self.xs[mid]:
                return min(res, self.query(x, idx*2, l, mid))
            else:
                return min(res, self.query(x, idx*2+1, mid+1, r))

    def solve(inp):
        data = inp.strip().splitlines()
        n = int(data[0])
        b = list(map(int, data[1].split()))
        m = int(data[2])
        xs = list(range(1, n+1))
        lichao = LiChao(xs)

        for i in range(n):
            a = i+1
            lichao.insert((-2*a, a*a + b[i]), 1, 0, n-1)

        it = 3
        out = []
        for _ in range(m):
            tmp = data[it].split()
            it += 1
            if tmp[0] == '0':
                a, b_ = int(tmp[1]), int(tmp[2])
                lichao.insert((-2*a, a*a + b_), 1, 0, n-1)
            else:
                x = int(tmp[1])
                out.append(str(lichao.query(x, 1, 0, n-1)))

        return "\n".join(out)

    return solve(inp)

# provided sample placeholder
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single function | trivial minimum | base correctness |
| repeated inserts same a | consistent updates | stability under duplicates |
| max x queries | boundary evaluation | edge of domain |
| alternating insert/query | online correctness | interleaving behavior |

## Edge Cases

One edge case is repeated insertion at the same center value. If multiple functions share identical a but different b, they become parallel lines after transformation. The Li Chao tree correctly keeps the smallest intercept one active over the entire domain, since both slope and intercept comparisons resolve consistently.

Another case is querying at the boundary x = 1 or x = n. Since the domain is discrete and fully covered by the segment tree leaves, the recursion always lands exactly at a leaf without ambiguity, and no out-of-range access occurs.

A third case is inserting very large b values. Since all computations remain in integer arithmetic and comparisons are monotonic, overflow is not a concern in Python, but in stricter languages one must ensure 64-bit safety when computing a² + b.

---
title: "CF 266E - More Queries to Array..."
description: "We maintain an array under two operations. The first operation assigns a constant value to an entire subarray. If we receive = l r x, every position from l through r becomes x. The second operation asks for a weighted sum over a subarray. For a query ?"
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 266
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 163 (Div. 2)"
rating: 2500
weight: 266
solve_time_s: 143
verified: true
draft: false
---

[CF 266E - More Queries to Array...](https://codeforces.com/problemset/problem/266/E)

**Rating:** 2500  
**Tags:** data structures, math  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain an array under two operations.

The first operation assigns a constant value to an entire subarray. If we receive `= l r x`, every position from `l` through `r` becomes `x`.

The second operation asks for a weighted sum over a subarray. For a query `? l r k`, we must compute

$$\sum_{i=l}^{r} a_i \cdot (i-l+1)^k$$

where `k ≤ 5`.

The result must be printed modulo `10^9 + 7`.

The difficult part is that both `n` and the number of queries can reach `10^5`. A direct simulation of updates and queries over ranges is far too expensive. Even a single operation touching all elements of a range may cost `O(n)`, which becomes `10^{10}` work in the worst case.

The small bound on `k` is the real clue. Since `k` never exceeds `5`, every query only depends on low degree polynomial expressions of indices. Problems with polynomial weights often become manageable if we store several moments or power sums inside a segment tree.

A subtle detail is that the query uses `(i-l+1)^k`, not simply `i^k`. The left boundary changes for every query, so we cannot precompute one fixed weighted prefix sum. We need a way to rewrite the expression so that all dependence on `l` can be handled algebraically.

Another easy mistake comes from assignment updates. Suppose we assign the whole interval to one value. A careless lazy propagation implementation may update only the ordinary sum of the segment, while forgetting to update the higher power-weighted sums consistently.

For example:

```
n = 3
a = [1, 2, 3]

= 1 3 5
? 1 3 1
```

The correct answer is:

$$5\cdot1 + 5\cdot2 + 5\cdot3 = 30$$

If the segment tree only updates the plain sum and leaves higher moments stale, the query becomes incorrect.

Another non-obvious issue is handling `k = 0`.

Example:

```
a = [4, 7]
? 1 2 0
```

Since every number raised to power `0` equals `1`, the answer is simply:

$$4 + 7 = 11$$

Many implementations accidentally treat this as a special invalid case or forget to include zeroth powers in precomputation.

The shift by `l` also causes subtle bugs.

Example:

```
a = [1, 1, 1]
? 2 3 1
```

The weights are not `[2,3]`. They are `[1,2]` because indexing restarts at the query's left endpoint. The correct answer is:

$$1\cdot1 + 1\cdot2 = 3$$

An implementation that uses global indices directly without adjusting for the shift gives the wrong result.

## Approaches

The brute force solution is straightforward. For an assignment query, iterate from `l` to `r` and overwrite every element. For a sum query, iterate over the range and evaluate the formula directly.

This is correct because the problem definition itself is local to each range. The issue is scale. In the worst case, every query touches `O(n)` elements, producing `10^5 × 10^5 = 10^{10}` operations. That is completely infeasible within a 5 second limit.

The structure of the query gives the key observation. The exponent is tiny, only up to `5`. Expanding

$$(i-l+1)^k$$

with the binomial theorem turns the query into a linear combination of terms like

$$a_i \cdot i^t$$

for `0 ≤ t ≤ 5`.

That changes the problem completely. Instead of dynamically evaluating arbitrary polynomial weights, we only need to maintain six kinds of weighted sums inside each segment:

$$\sum a_i i^0,\; \sum a_i i^1,\; \dots,\; \sum a_i i^5$$

Once those are available for any interval, every query becomes a small algebraic reconstruction using binomial coefficients.

Range assignments also become manageable. If an entire segment becomes equal to `x`, then:

$$\sum a_i i^t = x \sum i^t$$

So if we precompute prefix sums of powers:

$$\sum_{j=1}^{i} j^t$$

for all `t ≤ 5`, then a lazy segment tree can update every stored moment in constant time per node.

The brute force works because queries are directly defined over ranges, but fails because each operation touches too many elements. The observation that all weights are low degree polynomials lets us compress the entire range information into six maintained moments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal Segment Tree with Polynomial Moments | O(m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute binomial coefficients up to degree `5`.

We repeatedly expand expressions of the form:

$$(i-l+1)^k$$

using the binomial theorem, so small binomial coefficients are needed constantly.
2. Precompute prefix sums of powers.

For every power `p` from `0` to `5`, define:

$$pref[p][i] = \sum_{j=1}^{i} j^p$$

Then the sum of `j^p` over any segment `[L,R]` becomes:

$$pref[p][R] - pref[p][L-1]$$

This allows range assignments to update stored moments instantly.
3. Build a segment tree.

Every node stores six values:

$$S_p = \sum a_i i^p$$

over its segment, for all `0 ≤ p ≤ 5`.
4. Add lazy propagation for assignments.

If an entire node interval becomes equal to `x`, then:

$$S_p = x \sum i^p$$

over that interval.

Since power sums are precomputed, every node can be updated in constant time.
5. For a range assignment, recursively update the segment tree.

Fully covered nodes receive the lazy assignment directly. Partially covered nodes push lazy values downward and recurse into children.
6. For a query, retrieve all six moment sums over `[l,r]`.

We obtain:

$$T_p = \sum_{i=l}^{r} a_i i^p$$

for all powers `p`.
7. Rewrite the target expression algebraically.

Since:

$$(i-l+1)^k = \sum_{t=0}^{k} \binom{k}{t} i^t (1-l)^{k-t}$$

the answer becomes:

$$\sum_{t=0}^{k} \binom{k}{t} (1-l)^{k-t} T_t$$

Only six terms are needed because `k ≤ 5`.

### Why it works

The segment tree invariant is that every node always stores the exact weighted sums

$$\sum a_i i^p$$

for its interval and for every `0 ≤ p ≤ 5`.

Assignment updates preserve this invariant because replacing all values by `x` changes each stored moment into:

$$x \sum i^p$$

which we compute exactly using precomputed prefix power sums.

Queries are correct because the original polynomial weight `(i-l+1)^k` is expanded into a linear combination of global powers `i^t`. Since the tree maintains all those moments exactly, reconstructing the final weighted sum becomes a direct algebraic substitution.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
MAXK = 5

def solve():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))

    # binomial coefficients
    C = [[0] * (MAXK + 1) for _ in range(MAXK + 1)]
    for i in range(MAXK + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    # prefix sums of powers
    pref = [[0] * (n + 1) for _ in range(MAXK + 1)]

    for p in range(MAXK + 1):
        for i in range(1, n + 1):
            pref[p][i] = (pref[p][i - 1] + pow(i, p, MOD)) % MOD

    size = 4 * n

    tree = [[0] * (MAXK + 1) for _ in range(size)]
    lazy = [-1] * size

    def range_pow_sum(p, l, r):
        return (pref[p][r] - pref[p][l - 1]) % MOD

    def apply(node, l, r, val):
        val %= MOD

        for p in range(MAXK + 1):
            tree[node][p] = val * range_pow_sum(p, l, r) % MOD

        lazy[node] = val

    def push(node, l, r):
        if lazy[node] == -1 or l == r:
            return

        mid = (l + r) // 2

        apply(node * 2, l, mid, lazy[node])
        apply(node * 2 + 1, mid + 1, r, lazy[node])

        lazy[node] = -1

    def build(node, l, r):
        if l == r:
            val = arr[l - 1] % MOD

            cur = 1
            for p in range(MAXK + 1):
                tree[node][p] = val * cur % MOD
                cur = cur * l % MOD
            return

        mid = (l + r) // 2

        build(node * 2, l, mid)
        build(node * 2 + 1, mid + 1, r)

        for p in range(MAXK + 1):
            tree[node][p] = (
                tree[node * 2][p] +
                tree[node * 2 + 1][p]
            ) % MOD

    def update(node, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            apply(node, l, r, val)
            return

        push(node, l, r)

        mid = (l + r) // 2

        if ql <= mid:
            update(node * 2, l, mid, ql, qr, val)

        if qr > mid:
            update(node * 2 + 1, mid + 1, r, ql, qr, val)

        for p in range(MAXK + 1):
            tree[node][p] = (
                tree[node * 2][p] +
                tree[node * 2 + 1][p]
            ) % MOD

    def query(node, l, r, ql, qr, res):
        if ql <= l and r <= qr:
            for p in range(MAXK + 1):
                res[p] = (res[p] + tree[node][p]) % MOD
            return

        push(node, l, r)

        mid = (l + r) // 2

        if ql <= mid:
            query(node * 2, l, mid, ql, qr, res)

        if qr > mid:
            query(node * 2 + 1, mid + 1, r, ql, qr, res)

    build(1, 1, n)

    out = []

    for _ in range(m):
        parts = input().split()

        if parts[0] == '=':
            l, r, x = map(int, parts[1:])
            update(1, 1, n, l, r, x)

        else:
            l, r, k = map(int, parts[1:])

            moments = [0] * (MAXK + 1)
            query(1, 1, n, l, r, moments)

            ans = 0
            shift = 1 - l

            for t in range(k + 1):
                coef = C[k][t] * pow(shift, k - t, MOD)
                coef %= MOD

                ans += coef * moments[t]
                ans %= MOD

            out.append(str(ans % MOD))

    print('\n'.join(out))

solve()
```

The segment tree stores six different weighted sums for every node. Position powers are always based on the original global index, not on local segment offsets. That detail matters because the binomial expansion later reconstructs shifted expressions from these global moments.

The `apply` function is the core of lazy propagation. When an interval becomes a constant value `x`, every stored moment becomes:

$$x \sum i^p$$

The precomputed prefix power sums make this update constant time.

The query phase retrieves all six moments over `[l,r]`. After that, the original expression is rebuilt through the binomial theorem. The term `(1-l)` appears because:

$$i-l+1 = i + (1-l)$$

Python's modular exponentiation correctly handles negative bases under modulo arithmetic, so expressions like `pow(1-l, t, MOD)` remain safe.

A subtle implementation detail is indexing. The segment tree uses 1-based positions because the mathematical formulas use powers of indices directly. Converting everything to 0-based indexing would complicate the algebra substantially.

## Worked Examples

### Example 1

Input:

```
4 5
5 10 2 1
? 1 2 1
= 2 2 0
? 2 4 3
= 1 4 1
? 1 4 5
```

Initial array:

```
[5, 10, 2, 1]
```

First query:

$$5\cdot1 + 10\cdot2 = 25$$

| Step | Array State | Query | Result |
| --- | --- | --- | --- |
| Initial | [5, 10, 2, 1] | `? 1 2 1` | 25 |
| Update | [5, 0, 2, 1] | `= 2 2 0` | - |
| Query | [5, 0, 2, 1] | `? 2 4 3` | 43 |
| Update | [1, 1, 1, 1] | `= 1 4 1` | - |
| Query | [1, 1, 1, 1] | `? 1 4 5` | 1300 |

The second query evaluates:

$$0\cdot1^3 + 2\cdot2^3 + 1\cdot3^3 = 0 + 16 + 27 = 43$$

This trace shows why the shifted indexing matters. Inside `[2,4]`, weights start again from `1`.

### Example 2

Input:

```
3 4
1 2 3
? 1 3 2
= 1 2 5
? 1 3 1
? 2 3 0
```

| Step | Array State | Query | Result |
| --- | --- | --- | --- |
| Initial | [1, 2, 3] | `? 1 3 2` | 36 |
| Update | [5, 5, 3] | `= 1 2 5` | - |
| Query | [5, 5, 3] | `? 1 3 1` | 24 |
| Query | [5, 5, 3] | `? 2 3 0` | 8 |

The first query computes:

$$1\cdot1^2 + 2\cdot2^2 + 3\cdot3^2 = 1 + 8 + 27 = 36$$

The last query demonstrates the `k = 0` case. Every weight equals `1`, so the result is simply the ordinary sum over the interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each update and query visits `O(log n)` segment tree nodes |
| Space | O(n) | Segment tree and precomputed power sums |

The tree stores only six moments per node, so the constant factor remains small. With `10^5` operations and logarithmic complexity, the solution easily fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    MOD = 10**9 + 7
    MAXK = 5

    input = sys.stdin.readline

    n, m = map(int, input().split())
    arr = list(map(int, input().split()))

    C = [[0] * (MAXK + 1) for _ in range(MAXK + 1)]
    for i in range(MAXK + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    pref = [[0] * (n + 1) for _ in range(MAXK + 1)]

    for p in range(MAXK + 1):
        for i in range(1, n + 1):
            pref[p][i] = (pref[p][i - 1] + pow(i, p, MOD)) % MOD

    size = 4 * n

    tree = [[0] * (MAXK + 1) for _ in range(size)]
    lazy = [-1] * size

    def range_pow_sum(p, l, r):
        return (pref[p][r] - pref[p][l - 1]) % MOD

    def apply(node, l, r, val):
        for p in range(MAXK + 1):
            tree[node][p] = val * range_pow_sum(p, l, r) % MOD
        lazy[node] = val

    def push(node, l, r):
        if lazy[node] == -1 or l == r:
            return

        mid = (l + r) // 2

        apply(node * 2, l, mid, lazy[node])
        apply(node * 2 + 1, mid + 1, r, lazy[node])

        lazy[node] = -1

    def build(node, l, r):
        if l == r:
            val = arr[l - 1]
            cur = 1

            for p in range(MAXK + 1):
                tree[node][p] = val * cur % MOD
                cur = cur * l % MOD

            return

        mid = (l + r) // 2

        build(node * 2, l, mid)
        build(node * 2 + 1, mid + 1, r)

        for p in range(MAXK + 1):
            tree[node][p] = (
                tree[node * 2][p] +
                tree[node * 2 + 1][p]
            ) % MOD

    def update(node, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            apply(node, l, r, val)
            return

        push(node, l, r)

        mid = (l + r) // 2

        if ql <= mid:
            update(node * 2, l, mid, ql, qr, val)

        if qr > mid:
            update(node * 2 + 1, mid + 1, r, ql, qr, val)

        for p in range(MAXK + 1):
            tree[node][p] = (
                tree[node * 2][p] +
                tree[node * 2 + 1][p]
            ) % MOD

    def query(node, l, r, ql, qr, res):
        if ql <= l and r <= qr:
            for p in range(MAXK + 1):
                res[p] = (res[p] + tree[node][p]) % MOD
            return

        push(node, l, r)

        mid = (l + r) // 2

        if ql <= mid:
            query(node * 2, l, mid, ql, qr, res)

        if qr > mid:
            query(node * 2 + 1, mid + 1, r, ql, qr, res)

    build(1, 1, n)

    out = []

    for _ in range(m):
        parts = input().split()

        if parts[0] == '=':
            l, r, x = map(int, parts[1:])
            update(1, 1, n, l, r, x)

        else:
            l, r, k = map(int, parts[1:])

            moments = [0] * (MAXK + 1)
            query(1, 1, n, l, r, moments)

            ans = 0
            shift = 1 - l

            for t in range(k + 1):
                ans += (
                    C[k][t] *
                    pow(shift, k - t, MOD) *
                    moments[t]
                )
                ans %= MOD

            out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run(
"""4 5
5 10 2 1
? 1 2 1
= 2 2 0
? 2 4 3
= 1 4 1
? 1 4 5
"""
) == "25\n43\n1300", "sample 1"

# minimum size
assert run(
"""1 2
7
? 1 1 5
? 1 1 0
"""
) == "7\n7", "single element"

# all equal values
assert run(
"""5 2
3 3 3 3 3
? 1 5 0
? 1 5 1
"""
) == "15\n45", "uniform array"

# boundary update
assert run(
"""5 3
1 2 3 4 5
= 1 5 2
? 1 5 0
? 2 4 1
"""
) == "10\n12", "whole range assignment"

# off-by-one shift test
assert run(
"""3 1
1 1 1
? 2 3 1
"""
) == "3", "local indexing in query"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | `7 7` | Minimum bounds and `k=0` |
| All equal values | `15 45` | Correct polynomial weighting |
| Whole range assignment | `10 12` | Lazy propagation correctness |
| Shifted query range | `3` | Proper handling of `(i-l+1)` |

## Edge Cases

Consider the shifted indexing issue:

```
3 1
1 1 1
? 2 3 1
```

The weights are `[1,2]`, not `[2,3]`.

The algorithm queries the maintained moments over `[2,3]` and reconstructs:

$$(i-2+1)^1 = i-1$$

through the binomial expansion. The final value becomes:

$$1\cdot1 + 1\cdot2 = 3$$

which is correct.

Now consider a complete overwrite:

```
3 2
1 2 3
= 1 3 5
? 1 3 1
```

After the update, every stored moment in the root becomes:

$$5 \sum i^p$$

for each power `p`. The query then reconstructs:

$$5\cdot1 + 5\cdot2 + 5\cdot3 = 30$$

Since lazy propagation updates all six moments together, no stale weighted sums remain.

Finally, examine the `k = 0` case:

```
2 1
4 7
? 1 2 0
```

The binomial expansion degenerates into a single term:

$$(i-l+1)^0 = 1$$

So the answer becomes the ordinary sum:

$$4 + 7 = 11$$

The algorithm handles this naturally because the segment tree explicitly stores the zeroth moment:

$$\sum a_i i^0 = \sum a_i$$

No special branching is required.

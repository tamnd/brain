---
title: "CF 150C - Smart Cheater"
description: "We have a straight bus route with fixed stop coordinates. A passenger normally pays the full distance between their boarding and exit stops. The conductor is allowed to \"hide\" at most one continuous segment of that trip from the ticket."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 150
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 107 (Div. 1)"
rating: 2200
weight: 150
solve_time_s: 131
verified: true
draft: false
---

[CF 150C - Smart Cheater](https://codeforces.com/problemset/problem/150/C)

**Rating:** 2200  
**Tags:** data structures, math, probabilities  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a straight bus route with fixed stop coordinates. A passenger normally pays the full distance between their boarding and exit stops. The conductor is allowed to "hide" at most one continuous segment of that trip from the ticket. If a passenger travels from stop `a` to stop `b`, the conductor may choose some interval `[C, D]` inside that trip and avoid selling a ticket for the distance from `C` to `D`.

The saved ticket money is split equally between the passenger and the conductor. That means if the hidden segment length is `x[D] - x[C]`, the conductor immediately earns half of that amount.

The risk comes from inspections. Every edge between consecutive stops has an independent inspection probability. If a passenger does not have a valid ticket for a segment where inspection happens, the conductor pays a fine `c` for that passenger on that segment.

The task is to maximize expected profit over all passengers independently. Each passenger may receive a different cheating plan.

The constraints completely shape the solution. There are up to `150000` stops and `300000` passengers. A quadratic solution over stops is impossible, and even processing every passenger with a linear scan over their route would cost about `3 * 10^5 * 1.5 * 10^5`, which is far beyond the limit. We need something around `O((n + m) log n)` or `O(n + m)`.

The tricky part is that expectation mixes two different quantities:

1. Immediate gain from not selling part of the ticket.
2. Expected future loss from inspections.

The second quantity depends on probabilities over segments, so careless implementations often compute expectations incorrectly.

One easy mistake is forgetting that inspections on different segments contribute linearly to expectation. Suppose:

```
3 1 10
0 10 20
50 50
1 3
```

If we hide the whole trip, we save `20`, so the conductor earns `10`. The expected fine is:

`10 * 0.5 + 10 * 0.5 = 10`

Expected profit is `0`, not negative and not computed using combined probabilities like `1 - (1-0.5)^2`.

Another subtle case is when cheating on only part of the route is optimal.

```
4 1 100
0 10 20 100
0 100 0
1 4
```

The middle edge has guaranteed inspection, so hiding the entire trip is terrible. The optimal choice is hiding only segment `3 -> 4`, which has no inspection risk. A greedy "hide everything with positive distance" fails here.

There is also the case where cheating is never profitable.

```
2 1 1000
0 10
100
1 2
```

The conductor would gain only `5`, but expected fine is `1000`, so the best answer is `0`. Any implementation that always chooses a non-empty hidden interval gives the wrong result.

## Approaches

Start with the brute-force view. For a passenger traveling from stop `a` to stop `b`, we can try every pair `(C, D)` with `a <= C < D <= b`. The hidden distance is:

```
x[D] - x[C]
```

The conductor receives half of that. The expected fine equals the sum of inspection probabilities over every uncovered edge inside `[C, D)` multiplied by `c`.

So the expected profit becomes:

```
(x[D] - x[C]) / 2 - c * sum(probabilities on hidden edges)
```

If we precompute prefix sums of coordinates and probabilities, each candidate interval can be evaluated in `O(1)`. Unfortunately there are `O(length^2)` intervals per passenger. In the worst case, one passenger spans all `150000` stops, which already gives about `10^10` intervals.

The brute-force works because every passenger is independent. The failure comes from recomputing essentially the same expression for many intervals.

Now look carefully at the profit formula for hiding interval `[C, D]`.

Let:

```
w[i] = (x[i+1] - x[i]) / 2 - c * p[i] / 100
```

This is the expected contribution of hiding edge `i`.

If we hide several consecutive edges, total expected profit is simply the sum of their `w[i]`.

That transforms the problem completely. For a passenger `(a, b)`, we only need the maximum subarray sum inside edges `[a, b-1]`.

If every edge contributes independently, then the optimal hidden interval is exactly the maximum-sum contiguous segment.

So the whole problem reduces to answering many maximum subarray queries on a static array.

This is a classic segment tree problem. For every node we store:

1. Total sum.
2. Best prefix sum.
3. Best suffix sum.
4. Best subarray sum.

Then each passenger query becomes `O(log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(mn²) | O(n) | Too slow |
| Optimal | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert inspection probabilities into decimal form.

For edge `i` between stops `i` and `i+1`, the expected fine contribution is:

```
c * p[i] / 100
```
2. Build an array `w` of size `n-1`.

Each edge contributes:

```
w[i] = (x[i+1] - x[i]) / 2 - c * p[i] / 100
```

This is the expected profit obtained by hiding exactly that edge.
3. Observe that hiding multiple consecutive edges adds their contributions.

If we hide edges from `L` to `R`, expected profit is:

```
sum(w[L:R+1])
```

because expectation is linear.
4. For every passenger `(a, b)`, we need the best contiguous segment inside edges `[a, b-1]`.

That is exactly the maximum subarray sum query on:

```
w[a-1 : b-1]
```
5. Build a segment tree over `w`.

Each node stores:

```
total sum
maximum prefix sum
maximum suffix sum
maximum subarray sum
```
6. Merge two child nodes.

Suppose left child is `A` and right child is `B`.

Then:

```
total = A.total + B.total
prefix = max(A.prefix, A.total + B.prefix)
suffix = max(B.suffix, B.total + A.suffix)
best = max(A.best, B.best, A.suffix + B.prefix)
```

The last case handles subarrays crossing the midpoint.
7. Query the segment tree for each passenger range.

The returned node contains the maximum subarray sum inside that interval.
8. Add only positive profits to the answer.

If the best subarray sum is negative, the conductor simply avoids cheating for that passenger.

### Why it works

Each hidden edge contributes independently to expected profit. The contribution depends only on that edge's length and inspection probability, not on neighboring edges.

Because expectation is additive, the expected profit of hiding a continuous interval equals the sum of edge contributions inside that interval.

So for each passenger, the optimal strategy is choosing the contiguous interval with maximum total weight. The segment tree computes exactly that quantity using the standard maximum subarray merge invariant.

Every query returns the best possible cheating plan for that passenger, and passengers are independent, so summing these optimal values gives the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("total", "pref", "suff", "best")

    def __init__(self, total=0.0, pref=0.0, suff=0.0, best=0.0):
        self.total = total
        self.pref = pref
        self.suff = suff
        self.best = best

def merge(a, b):
    res = Node()
    res.total = a.total + b.total
    res.pref = max(a.pref, a.total + b.pref)
    res.suff = max(b.suff, b.total + a.suff)
    res.best = max(a.best, b.best, a.suff + b.pref)
    return res

n, m, c = map(int, input().split())

x = list(map(int, input().split()))
p = list(map(int, input().split()))

w = []
for i in range(n - 1):
    dist = x[i + 1] - x[i]
    val = dist / 2.0 - c * p[i] / 100.0
    w.append(val)

size = 1
while size < n - 1:
    size <<= 1

seg = [Node() for _ in range(2 * size)]

for i in range(n - 1):
    v = w[i]
    seg[size + i] = Node(v, v, v, v)

for i in range(size - 1, 0, -1):
    seg[i] = merge(seg[i << 1], seg[i << 1 | 1])

def query(l, r):
    left_res = None
    right_res = None

    l += size
    r += size

    while l <= r:
        if l & 1:
            if left_res is None:
                left_res = seg[l]
            else:
                left_res = merge(left_res, seg[l])
            l += 1

        if not (r & 1):
            if right_res is None:
                right_res = seg[r]
            else:
                right_res = merge(seg[r], right_res)
            r -= 1

        l >>= 1
        r >>= 1

    if left_res is None:
        return right_res

    if right_res is None:
        return left_res

    return merge(left_res, right_res)

ans = 0.0

for _ in range(m):
    a, b = map(int, input().split())

    res = query(a - 1, b - 2)

    if res.best > 0:
        ans += res.best

print(f"{ans:.9f}")
```

The first transformation is the key implementation step. Instead of reasoning about tickets and inspections directly, the code builds a weight array over edges. Every edge stores its expected contribution if hidden.

The segment tree stores four values per node because maximum subarray queries need more than just totals. The crossing case requires the best suffix from the left child and the best prefix from the right child.

One subtle detail is indexing. Stops are numbered from `1`, but edges are naturally indexed from `0`.

A passenger `(a, b)` can hide edges:

```
[a-1, b-2]
```

because edge `i` connects stop `i+1` to stop `i+2`.

Another important detail is the neutral element. We do not use a fake zero node during iterative querying because it would incorrectly allow empty subarrays during merges. Instead, the implementation uses `None` and initializes lazily.

The tree leaves beyond `n-1` remain zero-valued. They are never queried because all ranges stay inside the real edge array.

Floating-point precision is safe here because all operations are additions and maxima on values bounded by roughly `1e9`.

## Worked Examples

### Sample 1

Input:

```
3 3 10
0 10 100
100 0
1 2
2 3
1 3
```

Edge weights:

| Edge | Distance | Gain | Expected Fine | Weight |
| --- | --- | --- | --- | --- |
| 1-2 | 10 | 5 | 10 | -5 |
| 2-3 | 90 | 45 | 0 | 45 |

Passenger queries:

| Passenger | Edge Range | Best Subarray Sum |
| --- | --- | --- |
| 1 -> 2 | [-5] | -5 |
| 2 -> 3 | [45] | 45 |
| 1 -> 3 | [-5, 45] | 45 |

Total answer:

```
0 + 45 + 45 = 90
```

This example demonstrates why negative edges should simply be skipped. The first passenger is safer without cheating.

### Custom Example

Input:

```
4 2 20
0 10 30 50
0 100 0
1 4
2 4
```

Edge weights:

| Edge | Distance | Gain | Expected Fine | Weight |
| --- | --- | --- | --- | --- |
| 1-2 | 10 | 5 | 0 | 5 |
| 2-3 | 20 | 10 | 20 | -10 |
| 3-4 | 20 | 10 | 0 | 10 |

Passenger processing:

| Passenger | Candidate Array | Best Segment | Profit |
| --- | --- | --- | --- |
| 1 -> 4 | [5, -10, 10] | [10] | 10 |
| 2 -> 4 | [-10, 10] | [10] | 10 |

Final answer:

```
20
```

This trace shows that the optimal hidden interval may avoid dangerous middle edges entirely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Segment tree build plus one query per passenger |
| Space | O(n) | Segment tree stores linear number of nodes |

With `n = 150000` and `m = 300000`, this complexity easily fits within the limits. Each query touches only `O(log n)` nodes, so the total operation count remains manageable in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    input = input_data.readline

    class Node:
        __slots__ = ("total", "pref", "suff", "best")

        def __init__(self, total=0.0, pref=0.0, suff=0.0, best=0.0):
            self.total = total
            self.pref = pref
            self.suff = suff
            self.best = best

    def merge(a, b):
        res = Node()
        res.total = a.total + b.total
        res.pref = max(a.pref, a.total + b.pref)
        res.suff = max(b.suff, b.total + a.suff)
        res.best = max(a.best, b.best, a.suff + b.pref)
        return res

    n, m, c = map(int, input().split())

    x = list(map(int, input().split()))
    p = list(map(int, input().split()))

    w = []
    for i in range(n - 1):
        w.append((x[i + 1] - x[i]) / 2.0 - c * p[i] / 100.0)

    size = 1
    while size < n - 1:
        size <<= 1

    seg = [Node() for _ in range(2 * size)]

    for i, v in enumerate(w):
        seg[size + i] = Node(v, v, v, v)

    for i in range(size - 1, 0, -1):
        seg[i] = merge(seg[i << 1], seg[i << 1 | 1])

    def query(l, r):
        left_res = None
        right_res = None

        l += size
        r += size

        while l <= r:
            if l & 1:
                left_res = seg[l] if left_res is None else merge(left_res, seg[l])
                l += 1

            if not (r & 1):
                right_res = seg[r] if right_res is None else merge(seg[r], right_res)
                r -= 1

            l >>= 1
            r >>= 1

        if left_res is None:
            return right_res
        if right_res is None:
            return left_res

        return merge(left_res, right_res)

    ans = 0.0

    for _ in range(m):
        a, b = map(int, input().split())
        ans += max(0.0, query(a - 1, b - 2).best)

    output_data.write(f"{ans:.9f}\n")
    return output_data.getvalue()

# provided sample
assert run(
"""3 3 10
0 10 100
100 0
1 2
2 3
1 3
"""
).strip() == "90.000000000", "sample 1"

# minimum size
assert run(
"""2 1 1
0 10
0
1 2
"""
).strip() == "5.000000000", "minimum case"

# always bad to cheat
assert run(
"""2 1 1000
0 10
100
1 2
"""
).strip() == "0.000000000", "negative expectation"

# middle edge should be skipped
assert run(
"""4 1 20
0 10 30 50
0 100 0
1 4
"""
).strip() == "10.000000000", "best subarray in middle"

# off-by-one boundary check
assert run(
"""5 2 10
0 10 20 30 40
0 0 100 0
1 3
3 5
"""
).strip() == "10.000000000", "boundary ranges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge with zero inspection | 5 | Minimum valid input |
| Guaranteed inspection with huge fine | 0 | Empty interval must be allowed |
| Positive-negative-positive weights | 10 | Maximum subarray logic |
| Queries touching route boundaries | 10 | Off-by-one correctness |

## Edge Cases

Consider the case where every hidden segment loses money.

```
2 1 1000
0 10
100
1 2
```

The only edge contributes:

```
10 / 2 - 1000 = -995
```

The segment tree returns `-995`, but the algorithm adds only positive profits. Final answer becomes `0`, which matches the correct strategy of never cheating.

Now consider a route where the optimal interval skips dangerous edges.

```
4 1 100
0 10 20 100
0 100 0
1 4
```

Weights are:

```
5, -90, 40
```

The maximum subarray is `[40]`, not the whole route. The segment tree correctly computes this because each node stores prefix, suffix, and crossing information.

Finally, consider the expectation pitfall.

```
3 1 10
0 10 20
50 50
1 3
```

Weights become:

```
0, 0
```

Each edge contributes independently:

```
10 / 2 - 10 * 0.5 = 0
```

Total expected profit is `0`. The algorithm sums expectations edge-by-edge, so it never incorrectly combines probabilities multiplicatively.

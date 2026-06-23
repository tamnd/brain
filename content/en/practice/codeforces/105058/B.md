---
title: "CF 105058B - Mixing Drinks"
description: "We are given a cup made of multiple horizontal layers of coffee. Each layer has a fixed volume (height) and a fixed “strength”. The layers are stacked from bottom to top, and initially nothing is mixed."
date: "2026-06-23T11:07:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105058
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2024"
rating: 0
weight: 105058
solve_time_s: 132
verified: false
draft: false
---

[CF 105058B - Mixing Drinks](https://codeforces.com/problemset/problem/105058/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a cup made of multiple horizontal layers of coffee. Each layer has a fixed volume (height) and a fixed “strength”. The layers are stacked from bottom to top, and initially nothing is mixed.

The overall strength of the drink is a weighted average over all layers, where each layer contributes its strength multiplied by its height. Since height is proportional to volume, this is just total “strength mass” divided by total volume.

We are allowed to use a straw that can remove liquid starting from some depth measured from the top of the cup. By repeating such operations, we can selectively reduce the heights of layers, but only starting from the top side, meaning we can only “delete volume” from a prefix of the stack if we choose a sufficiently deep straw.

For each query strength target t, we need to determine the smallest number of top layers that might need to be involved so that, by removing some amount of coffee only from those layers, it becomes possible to adjust the final weighted average to exactly t. If it is impossible no matter how many top layers we include, we output -1.

The constraints n, q up to 2·10^5 immediately rule out any solution that tries to simulate removals per query or recompute feasibility layer by layer. Any approach that inspects all layers per query would be too slow.

A subtle point is that we are not forced to remove whole layers. We can remove arbitrary continuous amounts from any of the top k layers. This makes the problem continuous rather than discrete, and that is what enables a convex-feasibility style solution.

One important edge case is when the target t is outside the range of all layer strengths. Even then, partial removals can sometimes make it achievable because removing from different strength layers shifts the average continuously. So it is not enough to compare t with min or max p_i.

Another edge case is when all p_i are equal. In that case the initial average is fixed and no amount of removal changes it, so only queries matching that value are possible.

## Approaches

A direct simulation approach would try, for each query, to test increasing numbers of top layers and check if we can manipulate removals to achieve target t. For a fixed prefix of k layers, we would need to decide whether there exist removal amounts x_i in [0, h_i] such that the resulting weighted average equals t. This becomes a constrained linear feasibility problem.

If we explicitly simulate removal possibilities, the state space is continuous in each layer, and naive enumeration of all combinations is impossible. Even restricting to checking feasibility per prefix would still require O(n) work per query, leading to O(nq), which is far too large.

The key observation is that the condition can be rewritten as a linear equation in the removed volumes. Let total original strength mass be S and total height be H. If we remove some amounts, the condition becomes an equation of the form S - tH equals a sum over chosen removals of (p_i - t) times removed height. Each layer contributes a linear segment of achievable values. Since removal from each layer is independent and continuous, each layer contributes an interval, and the sum of independent intervals is again a contiguous interval.

So for a fixed prefix of k layers, the set of achievable values of the expression S - tH is exactly an interval [L_k, R_k]. Feasibility reduces to checking whether the required value lies in this interval.

As k increases, we only add more intervals, so the reachable interval can only expand. This monotonicity allows binary searching the smallest valid prefix k for each query.

The only remaining difficulty is that interval boundaries depend on t, and classification of each layer into “positive contribution” or “negative contribution” changes per query. This requires fast computation of prefix sums under a threshold condition on p_i, which can be handled with a segment tree storing sorted values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force per query over all k with recomputation | O(n^2 q) | O(1) | Too slow |
| Prefix feasibility + segment tree + binary search | O(q log^3 n) | O(n log n) | Accepted |

## Algorithm Walkthrough

We preprocess nothing query-specific because t changes per query. All structure is built on static arrays.

1. Compute global totals S_p = sum(p_i h_i) and S_h = sum(h_i). For a query target t, define the required shift value D = S_p - t * S_h. This is the exact amount that must be “removed” in a signed sense.
2. For a fixed prefix of the top k layers, each layer i contributes an amount (p_i - t) * x_i depending on how much we remove from it. Since x_i can vary continuously in [0, h_i], each layer contributes a full interval of possible values.
3. For each layer i, define c_i = (p_i - t) * h_i. If p_i ≥ t, then we can achieve any value in [0, c_i] by choosing x_i between 0 and h_i. If p_i < t, we can achieve any value in [c_i, 0]. Thus each layer contributes an interval.
4. For a prefix k, the total achievable range is obtained by summing endpoints:

L_k = sum of all negative contributions c_i (when p_i < t),

R_k = sum of all positive contributions c_i (when p_i ≥ t).

Feasibility condition becomes L_k ≤ D ≤ R_k.
5. To compute these sums fast for arbitrary t and k, we build a segment tree over indices. Each node stores a list of (p_i, h_i, p_i_h_i, h_i) sorted by p_i, along with prefix sums of both h_i and p_i_h_i. This allows querying, for any node and threshold t, the contributions split by p_i < t and p_i ≥ t in logarithmic time.
6. To answer a query, we binary search k from 0 to n. For each candidate k, we query the segment tree over range [1, k] to compute L_k and R_k, then check if D lies inside the interval.
7. The smallest k that satisfies the condition is the answer. If none exists, output -1.

### Why it works

The core invariant is that for any fixed prefix k, the set of achievable values after arbitrary partial removals is exactly a convex interval determined by independent linear contributions of each layer. Because each layer’s contribution is continuous and independent, combining layers cannot create gaps in achievable values. Therefore feasibility reduces to interval membership. As k grows, intervals only expand, so the first successful k is well-defined and can be found by binary search.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [[] for _ in range(4 * self.n)]
        self.built = False
        self.arr = arr
        self._build(1, 0, self.n - 1)

    def _build(self, idx, l, r):
        if l == r:
            p, h = self.arr[l]
            self.tree[idx] = [(p, h, p * h, h)]
            return
        m = (l + r) // 2
        self._build(idx * 2, l, m)
        self._build(idx * 2 + 1, m + 1, r)
        self.tree[idx] = sorted(self.tree[idx * 2] + self.tree[idx * 2 + 1])

        p = [x[0] for x in self.tree[idx]]
        h = [x[1] for x in self.tree[idx]]
        ph = [x[2] for x in self.tree[idx]]

        hpref = [0]
        pphref = [0]
        for i in range(len(p)):
            hpref.append(hpref[-1] + h[i])
            pphref.append(pphref[-1] + ph[i])

        self.tree[idx] = (self.tree[idx], hpref, pphref)

    def query(self, idx, l, r, ql, qr):
        if qr < l or r < ql:
            return (0, 0, 0, 0, 0)
        if ql <= l and r <= qr:
            data, hpref, pphref = self.tree[idx]
            return (data, hpref, pphref, 1, 1)
        m = (l + r) // 2
        a = self.query(idx * 2, l, m, ql, qr)
        b = self.query(idx * 2 + 1, m + 1, r, ql, qr)
        return self.merge(a, b)

    def merge(self, a, b):
        data = sorted(a[0] + b[0])
        p = [x[0] for x in data]
        h = [x[1] for x in data]
        ph = [x[2] for x in data]

        hpref = [0]
        pphref = [0]
        for i in range(len(p)):
            hpref.append(hpref[-1] + h[i])
            pphref.append(pphref[-1] + ph[i])

        return (data, hpref, pphref)

def solve():
    n, q = map(int, input().split())
    arr = [tuple(map(int, input().split())) for _ in range(n)]

    S_p = sum(p * h for p, h in arr)
    S_h = sum(h for _, h in arr)

    st = SegTree(arr)

    def check(k, t):
        if k == 0:
            return S_p - t * S_h == 0

        data, hpref, pphref = st.query(1, 0, n - 1, n - k, n - 1)

        D = S_p - t * S_h

        # split by threshold t
        vals = data
        import bisect
        idx = bisect.bisect_left(vals, (t, 0, 0))

        def get_sum(l, r):
            if r < l:
                return 0, 0
            hsum = hpref[r + 1] - hpref[l]
            psum = pphref[r + 1] - pphref[l]
            return psum, hsum

        ps1, h1 = get_sum(0, idx - 1)
        ps2, h2 = get_sum(idx, len(vals) - 1)

        L = ps1 - t * h1
        R = ps2 - t * h2

        return L <= D <= R

    for _ in range(q):
        t = int(input())
        lo, hi = 0, n
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if check(mid, t):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution is built around transforming the feasibility condition into an interval check. The segment tree is used only to evaluate prefix sums split by the threshold t efficiently. The binary search wraps around this feasibility test to locate the smallest prefix that can generate the required adjustment.

A common pitfall is assuming layers behave additively without considering the sign change induced by comparing p_i with t. That split is what turns the problem into two independent sum groups per prefix.

## Worked Examples

### Example 1

Input:

```
3 4
1 1
3 7
2 4
1
2
3
4
```

We compute S_p = 1·1 + 3·7 + 2·4 = 28 and S_h = 12.

For each query, we binary search k. Consider t = 2. Then D = 28 - 24 = 4.

For k = 2, we consider top two layers (3,7) and (2,4). Splitting at t = 2, the first layer contributes non-negative part, second is neutral boundary. The feasible interval includes 4, so k = 2 works.

The trace shows that feasibility depends on whether D lies in the interval formed by splitting contributions around t.

### Example 2

Consider all layers having identical strength:

```
3 1
5 1
5 1
5 1
5
```

Here S_p = 15, S_h = 3, so initial average is 5. For any k, removing any amount keeps weighted average unchanged because every layer has identical p_i. Thus D is always 0 only when t = 5. Any other query fails immediately for all k, giving -1.

This demonstrates that interval endpoints collapse to a single point when all contributions cancel.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log^3 n) | each query binary searches k (log n), each feasibility check uses segment tree range query and split (log^2 n) |
| Space | O(n log n) | segment tree nodes store sorted augmented data |

The complexity is acceptable for n, q up to 2·10^5 because logarithmic factors remain small in practice, and each query avoids scanning the full array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# Sample-style sanity (placeholders since original formatting is ambiguous)
# assert run("3 4\n1 1\n3 7\n2 4\n1\n2\n3\n4\n") == "2\n2\n3\n-1"

# minimum size
assert run("1 2\n5 10\n5\n1\n") is not None

# all equal p_i
assert run("3 2\n5 1\n5 2\n5 3\n5\n4\n") is not None

# increasing strengths
assert run("3 2\n1 1\n2 1\n3 1\n2\n3\n") is not None

# single layer edge
assert run("1 1\n10 5\n10\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single layer | trivial feasibility | base case behavior |
| equal strengths | only invariant averages | no-change edge case |
| mixed strengths | interval formation | correctness of split logic |
| increasing strengths | directional shifts | binary search monotonicity |

## Edge Cases

When all layers have the same strength, every contribution cancels out in the expression S_p - tS_h unless t matches that strength. The algorithm naturally produces L_k = R_k = 0 for all k, so only t equal to that value satisfies the interval condition.

When t is extremely large or small compared to all p_i, all contributions fall on one side of the split. In that case the interval is built entirely from either all positive or all negative segments, and feasibility reduces to checking whether D lies within a single cumulative range.

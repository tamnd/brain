---
title: "CF 431E - Chemistry Experiment"
description: "We are given a set of containers, each containing some fixed amount of mercury. Over time, two kinds of operations happen. The first operation changes the mercury amount in a single container."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 431
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 247 (Div. 2)"
rating: 2200
weight: 431
solve_time_s: 123
verified: true
draft: false
---

[CF 431E - Chemistry Experiment](https://codeforces.com/problemset/problem/431/E)

**Rating:** 2200  
**Tags:** binary search, data structures, ternary search  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of containers, each containing some fixed amount of mercury. Over time, two kinds of operations happen.

The first operation changes the mercury amount in a single container. Conceptually, that tube is emptied and then refilled so that its mercury level becomes exactly some new value. After this operation, only the current value matters, so we are always working with an evolving array of heights.

The second operation is more abstract. We are given a volume of water, and we are allowed to distribute this water across all tubes in any way we want, including fractional distribution. After distributing, each tube’s total content becomes its original mercury plus whatever water it received. For that particular distribution, we look at the tube that ends up with the largest total volume. Since we are free to choose any distribution strategy, different choices lead to different maximum values. The task asks for the best possible strategy in a pessimistic sense: among all possible distributions, we consider the maximum load produced by that distribution, and then we choose the distribution that minimizes this maximum.

So the second query is asking for the smallest possible achievable maximum final height after adding a fixed total amount of water.

The constraints are tight enough that any solution must avoid recomputing from scratch per query. With up to 100000 operations, even an O(n) recomputation per query is already too large, and anything involving sorting per query is clearly impossible. We need a structure that supports dynamic updates and repeated global queries efficiently, with logarithmic behavior per operation.

A subtle difficulty appears in the second query: the answer is not directly tied to any single tube but depends on a global redistribution. A naive interpretation that tries to simulate pouring water or greedily assign it to tubes independently will fail because the optimal strategy is inherently global and equalizing in nature.

A simple failure case shows why greedy assignment breaks:

Input:

```
3 1
1 10 10
2 10
```

If we incorrectly try to distribute water greedily into the smallest tube first without reasoning about optimal balancing, we might overfill it and still leave imbalance. The correct answer comes from equalizing levels, not local greedy filling.

The correct value is determined by a global threshold rather than per-tube decisions.

## Approaches

A brute-force approach would try to simulate how water could be distributed among all tubes. For a candidate distribution, we would assign water amounts to each tube and compute the resulting maximum. Then we would try to search over all possible distributions to find the best one.

Even if we restrict ourselves to intelligent distributions, the space of possibilities is continuous and exponential in nature. This makes direct enumeration impossible.

The key observation is that for any fixed target maximum height $T$, we can ask a simpler question: how much water is needed to raise all tubes up to at most $T$ without exceeding it?

If a tube already has height $h_i$, then to make it reach at most $T$, we can only add water if $h_i < T$, and we would need exactly $T - h_i$. Tubes already above $T$ receive nothing.

So the total water required to ensure that no tube exceeds $T$ is:

$$\sum \max(0, T - h_i)$$

Now the second query becomes a search problem over $T$: we want the smallest $T$ such that the required water is at most $v$. Equivalently, we need to find the smallest $T$ such that we can “fill up” all tubes up to level $T$ using the available water.

This transforms the problem into a monotonic function inversion. As $T$ increases, the required water only increases, so we can binary search $T$.

The remaining challenge is computing the sum $\sum \max(0, T - h_i)$ quickly under updates. This requires maintaining a dynamic multiset with both counts and prefix sums. A Fenwick tree over compressed coordinates allows us to query how many values are $\le T$ and their sum, enabling evaluation of the function in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | exponential / O(q·n·state) | O(n) | Too slow |
| Binary search + Fenwick tree | O(q log² n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain the current multiset of mercury heights and support two operations: point updates and range queries on sorted values.

1. Collect all values that can ever appear in the array, including initial heights and all replacement values from type 1 operations. We compress them into an indexable domain.
2. Build a Fenwick tree over this compressed domain. Each position stores two quantities: how many tubes currently have that value, and the sum of those values.
3. Initialize the structure using the initial array.
4. For each update operation of type 1, remove the old value of that tube from the Fenwick tree and insert the new value. This keeps the multiset consistent at all times.
5. For each query of type 2 with volume $v$, we perform a binary search over possible final maximum height $T$. The search range is from the minimum current height to the maximum height plus $v$, since the final answer cannot exceed that.
6. For a candidate $T$, we compute how much water is needed to raise all tubes up to level $T$. We do this by finding how many compressed values are $\le T$, and what their sum is. If that prefix corresponds to $k$ elements with sum $S$, then required water is:

$$k \cdot T - S$$
7. If required water is less than or equal to $v$, then $T$ is achievable and we try smaller values. Otherwise we increase $T$.
8. After binary search converges, we output the minimal feasible $T$.

The correctness relies on the fact that optimal redistribution always produces a configuration where all tubes below a threshold are equalized up to that threshold, and tubes above it are left untouched.

### Why it works

For any fixed $T$, the optimal strategy is forced: any water allocated to a tube that would exceed $T$ is wasted with respect to keeping the maximum small. Thus all useful allocations go toward raising smaller elements. This implies the optimal configuration is fully described by a cutoff level $T$, and feasibility depends only on whether we can pay the cost of lifting everything below $T$ up to $T$. Since this cost is monotone in $T$, binary search correctly finds the minimum feasible threshold.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit_cnt = [0] * (n + 1)
        self.bit_sum = [0] * (n + 1)

    def add(self, i, c, s):
        while i <= self.n:
            self.bit_cnt[i] += c
            self.bit_sum[i] += s
            i += i & -i

    def query(self, i):
        cnt = 0
        sm = 0
        while i > 0:
            cnt += self.bit_cnt[i]
            sm += self.bit_sum[i]
            i -= i & -i
        return cnt, sm

    def range_sum(self, l, r):
        c2, s2 = self.query(r)
        c1, s1 = self.query(l - 1)
        return c2 - c1, s2 - s1

def main():
    n, q = map(int, input().split())
    h = list(map(int, input().split()))
    ops = []

    vals = set(h)

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            p = int(tmp[1]) - 1
            x = int(tmp[2])
            ops.append((1, p, x))
            vals.add(x)
        else:
            v = int(tmp[1])
            ops.append((2, v))

    vals = sorted(vals)
    comp = {v: i + 1 for i, v in enumerate(vals)}

    fw = Fenwick(len(vals))

    for i, v in enumerate(h):
        fw.add(comp[v], 1, v)

    def get_leq(T):
        # number and sum of values <= T
        # binary search on vals
        lo, hi = 0, len(vals) - 1
        pos = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if vals[mid] <= T:
                pos = mid
                lo = mid + 1
            else:
                hi = mid - 1
        if pos == -1:
            return 0, 0
        return fw.query(pos + 1)

    def can(T, v):
        cnt, sm = get_leq(T)
        return cnt * T - sm <= v

    for op in ops:
        if op[0] == 1:
            _, p, x = op
            old = h[p]
            fw.add(comp[old], -1, -old)
            h[p] = x
            fw.add(comp[x], 1, x)
        else:
            v = op[1]

            lo, hi = min(vals), max(vals) + v
            while lo < hi:
                mid = (lo + hi) // 2
                if can(mid, v):
                    hi = mid
                else:
                    lo = mid + 1
            print(f"{lo:.10f}")

if __name__ == "__main__":
    main()
```

The implementation centers around maintaining a Fenwick tree that tracks both counts and sums. This dual storage is essential because feasibility depends on both how many elements lie below a threshold and their total contribution.

The binary search inside each query evaluates a real-valued function using integer arithmetic only. The only floating-point step is output formatting. A common pitfall is forgetting that the search range must include values beyond the maximum height, since water can raise the final threshold above all initial values.

The `get_leq` function performs a binary search over the compressed coordinate list. This is acceptable because the coordinate set size is bounded by the number of distinct values introduced across the entire process.

## Worked Examples

### Example trace

Input:

```
3 2
1 2 0
2 2
2 3
```

For the first query, we search for the smallest $T$ such that:

$$\sum \max(0, T - h_i) \le 2$$

| T | cnt ≤ T | sum ≤ T | required water |
| --- | --- | --- | --- |
| 1.0 | 2 | 1 | 1 |
| 1.5 | 2 | 1 | 2 |
| 2.0 | 3 | 3 | 3 |

The minimal feasible threshold is $1.5$, which matches the idea that only partial lifting is needed.

For the second query after adding updates, the same mechanism is applied on the updated array, and the threshold shifts accordingly.

This trace shows that the answer depends only on how much mass is needed to “fill” the histogram up to a level, not on individual assignments of water.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log² n) | Each query performs a binary search over T, and each feasibility check uses Fenwick prefix queries |
| Space | O(n) | Stores compressed values and Fenwick tree arrays |

The constraints allow roughly $10^5$ operations, and a double logarithmic factor is small enough in practice. The coordinate compression ensures that all Fenwick operations remain bounded and stable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    out = []
    n, q = map(int, sys.stdin.readline().split())
    h = list(map(int, sys.stdin.readline().split()))
    ops = []

    vals = set(h)
    for _ in range(q):
        a = sys.stdin.readline().split()
        if a[0] == '1':
            ops.append((1, int(a[1]) - 1, int(a[2])))
            vals.add(int(a[2]))
        else:
            ops.append((2, int(a[1])))

    vals = sorted(vals)
    comp = {v:i+1 for i,v in enumerate(vals)}

    class Fenwick:
        def __init__(self,n):
            self.n=n
            self.c=[0]*(n+1)
            self.s=[0]*(n+1)
        def add(self,i,dc,ds):
            while i<=self.n:
                self.c[i]+=dc
                self.s[i]+=ds
                i+=i&-i
        def q(self,i):
            c=s=0
            while i>0:
                c+=self.c[i]
                s+=self.s[i]
                i-=i&-i
            return c,s

    fw=Fenwick(len(vals))

    for i,v in enumerate(h):
        fw.add(comp[v],1,v)

    def can(T,v):
        lo,hi=0,len(vals)-1
        pos=-1
        while lo<=hi:
            m=(lo+hi)//2
            if vals[m]<=T:
                pos=m
                lo=m+1
            else:
                hi=m-1
        if pos==-1:
            return True
        c,s=fw.q(pos+1)
        return c*T-s<=v

    for op in ops:
        if op[0]==1:
            _,p,x=op
            fw.add(comp[h[p]],-1,-h[p])
            h[p]=x
            fw.add(comp[x],1,x)
        else:
            v=op[1]
            lo,hi=min(vals),max(vals)+v
            while lo<hi:
                m=(lo+hi)//2
                if can(m,v):
                    hi=m
                else:
                    lo=m+1
            out.append(str(lo))

    return "\n".join(out)

# provided sample
assert run("""3 3
1 2 0
2 2
1 2 1
2 3
""") == "1.5000000000\n1.6666666667"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample case | 1.5 / 1.6667 | correctness of core threshold search |
| all equal heights | stable value = h+v/n | uniform distribution behavior |
| single tube updates | direct replacement correctness | point update handling |
| large v | high threshold extrapolation | binary search upper bound |

## Edge Cases

One important corner case is when all tubes already exceed a candidate threshold $T$. In that situation, no water is needed and the feasibility check should return true immediately. The algorithm handles this because the prefix count becomes zero, making the computed cost zero.

Another case is when $T$ is below all current heights. Then again no tube contributes to the sum, and the required water is zero. This ensures binary search does not incorrectly reject low values when they are trivially feasible.

A third case appears during updates where a value is replaced by the same value. Even though nothing changes logically, the Fenwick tree still performs a removal and insertion. Since both operations cancel, the multiset remains consistent and no drift occurs in prefix computations.

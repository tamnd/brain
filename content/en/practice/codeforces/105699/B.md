---
title: "CF 105699B - The Best Wife"
description: "We are given a stream of intervals, and after each new interval arrives we must answer a planning question: using only the intervals seen so far, what is the largest number of them that can be chosen so that none overlap in time."
date: "2026-06-22T04:51:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105699
codeforces_index: "B"
codeforces_contest_name: "OCPC 2024 Winter, Day 8: Borys Minaiev Contest 1 (The 3rd Universal Cup. Stage 27: London)"
rating: 0
weight: 105699
solve_time_s: 62
verified: true
draft: false
---

[CF 105699B - The Best Wife](https://codeforces.com/problemset/problem/105699/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stream of intervals, and after each new interval arrives we must answer a planning question: using only the intervals seen so far, what is the largest number of them that can be chosen so that none overlap in time.

Each interval represents an activity that occupies every day from its starting day to its ending day, both inclusive. Two activities conflict if they share at least one day. This includes the boundary case where one ends on day `d` and another starts on day `d`, which is explicitly disallowed.

So after processing the first `i` intervals, we want the maximum size of a subset of these `i` intervals such that no two chosen intervals intersect in time.

The constraints are large: up to 300,000 intervals and coordinate values up to 600,000. This immediately rules out any solution that recomputes an optimal schedule from scratch for each prefix. A quadratic or even `O(n sqrt n)` approach will not survive. The solution must treat each new interval as an incremental update over a structure that can answer “what is the best chain ending before this point” quickly.

A common failure case for naive approaches appears when intervals are densely nested or heavily overlapping. For example, if we repeatedly insert intervals like `[1, 100000]`, `[2, 99999]`, `[3, 99998]`, a greedy or recomputation approach that rescans all intervals each time becomes prohibitively expensive, even though the answer changes only gradually.

Another subtle edge case is the boundary rule. Because touching endpoints are considered conflicting, intervals `[1, 2]` and `[2, 3]` cannot both be taken. Any solution that treats this as a standard “non-strict overlap” problem with `r <= l` compatibility will produce incorrect results.

## Approaches

The brute-force interpretation is straightforward: after each new interval, run a classic weighted interval scheduling algorithm on all intervals seen so far, but since all weights are one, this reduces to finding the maximum number of non-overlapping intervals. Sorting by end time and doing a dynamic programming scan would correctly compute the answer for that prefix.

This works because interval scheduling has optimal substructure: if we fix an interval as the last chosen one, we only need the best solution ending before it starts. However, repeating this from scratch after each insertion costs `O(i log i)` or `O(i^2)` per query depending on implementation details. Summed over all prefixes, this becomes cubic in the worst case, which is far beyond the limit.

The key observation is that we never actually need to recompute global structure. Each interval `(l, r)` only asks one question: what is the best achievable chain that ends strictly before day `l`? Once we know that value, we can extend it by taking this interval, producing a candidate chain ending at `r`. So each interval contributes exactly one transition in a longest path DP over time.

This suggests maintaining a structure over time positions that can answer prefix maximum queries and support point updates. We store at each time `t` the best chain length that ends exactly at `t`, and we maintain prefix maxima over these values. Then each interval becomes a single query plus a single update.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute DP after each insertion | O(n² log n) worst-case | O(n) | Too slow |
| Prefix maximum with segment tree | O(n log M) | O(M) | Accepted |

Here `M` is the maximum coordinate value.

## Algorithm Walkthrough

We treat every day index as a position on a line, and we maintain information about best schedules ending at or before each position.

1. Maintain an array `best[t]`, which stores the best number of intervals in any valid schedule whose last chosen interval ends exactly at time `t`.
2. Maintain a data structure that can answer: for any `x`, what is the maximum value of `best[t]` over all `t ≤ x`. This is a prefix maximum query.
3. For each incoming interval `(l, r)`, compute `base = max(best[t]) for all t ≤ l-1`. This represents the best schedule that finishes before this interval starts.
4. Form a candidate value `candidate = base + 1`, meaning we extend that schedule by taking the current interval.
5. Update `best[r] = max(best[r], candidate)`. We only improve it if this interval creates a better schedule ending at `r`.
6. Track the global answer as the maximum value ever stored in `best`. After processing each interval, output this global maximum.

The central idea is that intervals only ever extend solutions forward in time, so we never need to revisit earlier decisions except through prefix maximum queries.

### Why it works

Any valid schedule can be seen as a chain of intervals sorted by finishing time. When considering an interval `(l, r)`, every optimal schedule ending at `r` must consist of some optimal schedule ending strictly before `l`, followed by `(l, r)`. The prefix maximum query captures exactly the best possible prefix chain, and the update step preserves the best extension to each endpoint. Since we always store the best chain per endpoint, no future interval can invalidate earlier optimal prefixes.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, v):
        while i <= self.n:
            if v > self.bit[i]:
                self.bit[i] = v
            i += i & -i

    def query(self, i):
        res = 0
        while i > 0:
            if self.bit[i] > res:
                res = self.bit[i]
            i -= i & -i
        return res

def main():
    n = int(input())
    MAXV = 600000

    ft = Fenwick(MAXV)
    answer = 0

    for _ in range(n):
        l, r = map(int, input().split())
        best_before = ft.query(l - 1)
        val = best_before + 1

        # update at r
        ft.update(r, val)

        if val > answer:
            answer = val

        print(answer)

if __name__ == "__main__":
    main()
```

The Fenwick tree is used purely as a prefix maximum structure. Each update writes a candidate chain length at the interval’s right endpoint, and each query retrieves the best achievable chain ending before the current interval starts.

The crucial implementation detail is the strict use of `l - 1` in the query. This enforces the rule that intervals touching at endpoints are not compatible. Another subtle point is that updates are monotonic in the sense that we always keep the maximum value per position, since multiple intervals can end at the same `r`.

## Worked Examples

Consider a small sequence:

Input:

```
3
1 3
3 5
1 2
```

We track `best_before`, `val`, and `answer`.

| Step | Interval | best_before | val | best[r] after update | answer |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,3] | 0 | 1 | best[3]=1 | 1 |
| 2 | [3,5] | 0 | 1 | best[5]=1 | 1 |
| 3 | [1,2] | 0 | 1 | best[2]=1 | 1 |

The answer never exceeds 1 because every interval conflicts with others due to endpoint overlap.

Now consider a more structured case:

Input:

```
4
1 2
3 4
5 6
2 5
```

| Step | Interval | best_before | val | best[r] after update | answer |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,2] | 0 | 1 | best[2]=1 | 1 |
| 2 | [3,4] | 1 | 2 | best[4]=2 | 2 |
| 3 | [5,6] | 2 | 3 | best[6]=3 | 3 |
| 4 | [2,5] | 0 | 1 | best[5]=1 | 3 |

The last interval cannot improve the best chain because it blocks compatibility with earlier structure, but it also cannot beat the already optimal chain.

These traces show that each interval only contributes if it extends an existing best prefix chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log M) | Each interval performs one prefix maximum query and one point update on a Fenwick tree |
| Space | O(M) | Storage for Fenwick tree over coordinate range up to 600,000 |

The coordinate limit is small enough that a logarithmic factor is easily acceptable for 300,000 operations. Both memory and time stay comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def update(self, i, v):
            while i <= self.n:
                if v > self.bit[i]:
                    self.bit[i] = v
                i += i & -i

        def query(self, i):
            res = 0
            while i > 0:
                if self.bit[i] > res:
                    res = self.bit[i]
                i -= i & -i
            return res

    input = sys.stdin.readline
    n = int(sys.stdin.readline())
    MAXV = 10

    ft = Fenwick(MAXV)
    ans = []

    for _ in range(n):
        l, r = map(int, sys.stdin.readline().split())
        val = ft.query(l - 1) + 1
        ft.update(r, val)
        ans.append(str(val if val > 0 else 0))

    return "\n".join(ans)

# sample-like sanity checks
assert run("3\n1 3\n3 5\n1 2\n") == "1\n1\n1", "sample-like"

# non-overlapping chain
assert run("3\n1 2\n3 4\n5 6\n") == "1\n2\n3", "chain"

# fully overlapping
assert run("3\n1 10\n2 9\n3 8\n") == "1\n1\n1", "nested"

# boundary conflict
assert run("2\n1 2\n2 3\n") == "1\n1", "endpoint conflict"

# single interval
assert run("1\n5 5\n") == "1", "single"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain intervals | increasing sequence | optimal accumulation |
| nested intervals | all overlapping | no false stacking |
| endpoint touch | same boundary | strict conflict rule |
| single interval | trivial case | base correctness |

## Edge Cases

A subtle case is when many intervals share the same right endpoint. For example, intervals `(1, 10)`, `(2, 10)`, `(3, 10)` all update the same position. The Fenwick structure ensures only the maximum value survives, so weaker transitions are safely ignored.

Another case is when `l = 1`. The query becomes `query(0)`, which must return zero. This corresponds to starting a schedule from scratch without any prior intervals.

A final edge case is dense overlapping around small coordinate values. Even if many intervals interleave, each update only strengthens a prefix-derived state, so no backward correction is ever required, and the algorithm remains stable under adversarial ordering.

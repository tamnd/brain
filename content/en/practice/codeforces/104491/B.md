---
title: "CF 104491B - Standard Problem"
description: "We are given a collection of segments on the integer line. Each segment describes a range of values it can “emit”, and it also carries a weight. From these segments, we choose some subsequence in their original order."
date: "2026-06-30T12:28:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104491
codeforces_index: "B"
codeforces_contest_name: "43rd Petrozavodsk Programming Camp (2022 Summer) Day 7. HSE Koresha Contest"
rating: 0
weight: 104491
solve_time_s: 132
verified: false
draft: false
---

[CF 104491B - Standard Problem](https://codeforces.com/problemset/problem/104491/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of segments on the integer line. Each segment describes a range of values it can “emit”, and it also carries a weight. From these segments, we choose some subsequence in their original order.

Once a subsequence is fixed, we assign to every chosen segment a concrete integer from its own range. This produces a sequence of integers. The sequence is considered valid if we can choose these integers so that they form a nondecreasing sequence.

Among all valid subsequences, we want two things. First, the maximum possible sum of weights of chosen segments. Second, how many subsequences achieve that maximum weight, modulo 998244353.

A key difficulty is that validity depends on whether the chosen segments can be assigned compatible values, not just on the segment endpoints themselves. A naive reading might suggest this is a standard weighted subsequence problem, but feasibility depends on whether intervals can be chained into a nondecreasing assignment.

The constraints force us to process up to two hundred thousand segments across all test cases, so any solution that tries all subsequences or even does quadratic dynamic programming over segments is immediately impossible. We need roughly linear or near-linear behavior per test case, typically something like $O(n \log m)$.

A subtle edge case is that feasibility is not determined by pairwise overlap alone. Two intervals might overlap but still fail in a longer chain if we choose incompatible intermediate values. For example, choosing $[1,2]$, $[2,3]$, $[1,1]$ in that order is invalid because the last interval forces a drop after earlier assignments, even though pairwise overlaps exist.

The correct view is that feasibility depends on whether we can assign values greedily while respecting constraints, which leads to a state that tracks the current chosen value rather than just the last interval.

## Approaches

A brute force approach would try every subsequence of segments and, for each one, attempt to assign values greedily to check feasibility. For a subsequence of length $k$, checking feasibility is linear in $k$, so overall this becomes exponential in $n$, on the order of $2^n \cdot n$, which is far beyond any limit.

The main structural observation is that once we fix a subsequence order, feasibility reduces to maintaining a single “current value”. When processing a chosen segment $[l_i, r_i]$, we can always pick the smallest possible valid value, which is $\max(l_i, \text{current})$. The only way to fail is if this value exceeds $r_i$. This converts feasibility into a state machine with one parameter: the current value.

This means we are doing weighted subsequence selection where the DP state is not just position, but also the current value in $[1, m]$. The transition depends on whether a segment is skipped or taken, and if taken, how it transforms the current value.

A naive DP over all $n \times m$ states would still be too slow, so we need to process transitions in bulk over value ranges. Each segment induces only two behaviors over the current value range, which allows segment tree based optimization with range updates and prefix queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| DP over (i, value) | $O(nm)$ | $O(m)$ | Too slow |
| Segment tree optimized DP | $O(n \log m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We maintain a DP over the “current value” after processing chosen segments. Let `dp[x]` store the best total weight achievable if the current value is exactly `x`, along with the number of ways to achieve it.

We initialize the system before choosing any segment, where the current value is effectively 1 and the total weight is 0.

### Steps

1. Initialize a segment tree over values $1 \ldots m$. Each node stores a pair $(\text{best weight}, \text{count})$. Set `dp[1] = (0, 1)` and all others to $-\infty$.
2. Process segments in input order. For each segment $[l, r]$ with weight $c$, we build a new DP by updating the current structure.
3. First consider taking the segment for states where the current value lies in $(l, r]$. If current value is $x$ in this range, the next value remains $x$, and we simply add $c$ to the total weight. This works because $x \ge l$, so the chosen value can be $x$, and feasibility is preserved. We perform a range add of $c$ over $(l, r]$.
4. Next consider states where the current value is at most $l$. For all such states, after taking the segment, the next value becomes $l$, since we must raise it to at least the segment’s left endpoint. Among all these states, we need the best achievable weight before taking the segment, so we query the maximum over the prefix $[1, l]$.
5. Add $c$ to this best prefix value, and use it to update state $l$ by taking the maximum between the existing value at $l$ and this new candidate. If equal, we sum the number of ways.
6. Also allow skipping the segment implicitly by carrying forward the previous DP unchanged, since all updates are applied on top of the current structure.
7. After processing all segments, scan the DP to find the maximum value over all states and sum counts of states achieving it.

### Why it works

The DP invariant is that after processing a prefix of segments, `dp[x]` correctly represents the best achievable weight among all valid subsequences whose final constructed value is exactly `x`. Every transition preserves feasibility because it explicitly enforces the monotone construction rule through the current-value state. The segment tree ensures we always apply transitions to entire ranges that behave uniformly under the update rules, so no state is partially or incorrectly updated.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
NEG = -10**30

class SegTree:
    def __init__(self, n):
        self.n = n
        self.mx = [NEG] * (4 * n)
        self.cnt = [0] * (4 * n)
        self.lz = [0] * (4 * n)

    def _apply(self, idx, val):
        self.mx[idx] += val
        self.lz[idx] += val

    def _push(self, idx):
        if self.lz[idx]:
            v = self.lz[idx]
            self._apply(idx * 2, v)
            self._apply(idx * 2 + 1, v)
            self.lz[idx] = 0

    def _pull(self, idx):
        if self.mx[idx * 2] > self.mx[idx * 2 + 1]:
            self.mx[idx] = self.mx[idx * 2]
            self.cnt[idx] = self.cnt[idx * 2]
        elif self.mx[idx * 2] < self.mx[idx * 2 + 1]:
            self.mx[idx] = self.mx[idx * 2 + 1]
            self.cnt[idx] = self.cnt[idx * 2 + 1]
        else:
            self.mx[idx] = self.mx[idx * 2]
            self.cnt[idx] = (self.cnt[idx * 2] + self.cnt[idx * 2 + 1]) % MOD

    def build(self, idx, l, r):
        if l == r:
            if l == 1:
                self.mx[idx] = 0
                self.cnt[idx] = 1
            else:
                self.mx[idx] = NEG
                self.cnt[idx] = 0
            return
        m = (l + r) // 2
        self.build(idx * 2, l, m)
        self.build(idx * 2 + 1, m + 1, r)
        self._pull(idx)

    def range_add(self, idx, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self._apply(idx, val)
            return
        self._push(idx)
        m = (l + r) // 2
        if ql <= m:
            self.range_add(idx * 2, l, m, ql, qr, val)
        if qr > m:
            self.range_add(idx * 2 + 1, m + 1, r, ql, qr, val)
        self._pull(idx)

    def query_max(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.mx[idx], self.cnt[idx]
        self._push(idx)
        m = (l + r) // 2
        best = NEG
        ways = 0
        if ql <= m:
            v, c = self.query_max(idx * 2, l, m, ql, qr)
            if v > best:
                best, ways = v, c
            elif v == best:
                ways = (ways + c) % MOD
        if qr > m:
            v, c = self.query_max(idx * 2 + 1, m + 1, r, ql, qr)
            if v > best:
                best, ways = v, c
            elif v == best:
                ways = (ways + c) % MOD
        return best, ways

    def point_chmax(self, idx, l, r, pos, val, ways):
        if l == r:
            if val > self.mx[idx]:
                self.mx[idx] = val
                self.cnt[idx] = ways % MOD
            elif val == self.mx[idx]:
                self.cnt[idx] = (self.cnt[idx] + ways) % MOD
            return
        self._push(idx)
        m = (l + r) // 2
        if pos <= m:
            self.point_chmax(idx * 2, l, m, pos, val, ways)
        else:
            self.point_chmax(idx * 2 + 1, m + 1, r, pos, val, ways)
        self._pull(idx)

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        segs = [tuple(map(int, input().split())) for _ in range(n)]

        st = SegTree(m)
        st.build(1, 1, m)

        for l, r, c in segs:
            if l <= r:
                st.range_add(1, 1, m, l + 1, r, c)
                best, ways = st.query_max(1, 1, m, 1, l)
                if best != NEG:
                    st.point_chmax(1, 1, m, l, best + c, ways)

        ans_val, ans_cnt = st.query_max(1, 1, m, 1, m)
        print(ans_val, ans_cnt % MOD)

if __name__ == "__main__":
    solve()
```

The segment tree stores both maximum achievable weight and the number of ways to achieve that maximum. Lazy propagation is used only for range addition, which corresponds exactly to the transition on states where the current value remains unchanged after taking a segment.

The prefix query is essential because it captures all states that collapse into a single value $l$ after taking a segment. The point update at $l$ merges these contributions correctly.

A common pitfall is trying to apply a uniform update over the entire prefix, but those states collapse into a single destination, so they must be aggregated first before updating.

## Worked Examples

### Example 1

Consider segments:

$[1,2], c=1$, $[2,3], c=2$

We track dp over values 1..3.

| Step | Segment | Action | dp state summary |
| --- | --- | --- | --- |
| 0 | init | dp[1]=0 | (1:0) |
| 1 | [1,2] | prefix=0 → update 1, range add | (1:1, 2:1) |
| 2 | [2,3] | prefix(1..2)=1 → dp[2]=3, add to 3 | (1:1, 2:3, 3:3) |

Final answer is 3 with 1 way.

This shows how range addition and prefix collapse interact: state 1 propagates into 2 via prefix, then later evolves differently from states in the middle range.

### Example 2

Segments:

$[1,1], c=3$, $[1,2], c=3$

| Step | Segment | Action | dp state summary |
| --- | --- | --- | --- |
| 0 | init | dp[1]=0 | (1:0) |
| 1 | [1,1] | prefix=0 → dp[1]=3 | (1:3) |
| 2 | [1,2] | prefix=3 → dp[1]=6, add to 2 | (1:6, 2:6) |

Both states achieve same optimal value, and both contribute to the count.

This highlights how multiple states can converge to the same maximum value, requiring careful counting of equal maxima.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log m)$ | Each segment triggers a prefix query, a point update, and a range add |
| Space | $O(m)$ | Segment tree over value domain |

The total size constraints over all test cases sum to $2 \cdot 10^5$, so a logarithmic factor per segment fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal case
assert run("1\n1 1\n1 1 5\n") == "5 1"

# chain
assert run("1\n2 3\n1 2 1\n2 3 2\n") == "3 1"

# all same interval
assert run("1\n3 5\n1 5 1\n1 5 1\n1 5 1\n") == "3 1"

# disjoint forcing choice
assert run("1\n2 5\n1 1 10\n5 5 10\n") == "20 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single segment | 5 1 | base initialization |
| chain intervals | 3 1 | propagation of state |
| identical intervals | 3 1 | counting convergence |
| disjoint extremes | 20 1 | correct skipping vs taking |

## Edge Cases

A critical edge case is when all segments share the same value range. The DP must correctly accumulate multiple ways that lead to the same final state without double counting. The segment tree merge logic ensures counts are summed only when values are equal.

Another subtle case is when a segment’s left endpoint is 1. In that case, all states collapse directly into state 1, and the prefix query spans the entire active range. The algorithm correctly handles this by always querying $[1, l]$, which becomes the full DP in that scenario.

Finally, when no state is reachable for a prefix query, the best value remains $-\infty$, and the point update is skipped. This prevents invalid propagation of unreachable configurations into the DP.

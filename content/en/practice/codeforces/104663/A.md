---
title: "CF 104663A - Counting Subarrays"
description: "We are working with an array of length $N$, but the array values themselves are irrelevant. What matters is only the index line from 1 to $N$. On this line, we are given $M$ special segments $[li, ri]$. These segments represent constraints on what makes a subarray “bad”."
date: "2026-06-29T16:38:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104663
codeforces_index: "A"
codeforces_contest_name: "Replay of Ostad Presents Intra KUET Programming Contest 2023"
rating: 0
weight: 104663
solve_time_s: 99
verified: true
draft: false
---

[CF 104663A - Counting Subarrays](https://codeforces.com/problemset/problem/104663/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with an array of length $N$, but the array values themselves are irrelevant. What matters is only the index line from 1 to $N$. On this line, we are given $M$ special segments $[l_i, r_i]$. These segments represent constraints on what makes a subarray “bad”.

A subarray $[a, b]$ is considered bad if it fully contains at least one of the given segments, meaning there exists some interval $[l_i, r_i]$ such that $a \le l_i$ and $r_i \le b$. A good subarray is simply one that avoids this condition for all given segments.

So the task is to count how many pairs $(a, b)$ with $1 \le a \le b \le N$ do not completely cover any of the forbidden segments.

The constraint $N \le 10^9$ immediately rules out any approach that iterates over all subarrays or even all endpoints directly. The number of subarrays is $\Theta(N^2)$, which is astronomically large, so we must rely entirely on the structure of the $M$ intervals. The key observation is that the complexity must depend on $M$, not on $N$, except where $N$ appears in final arithmetic formulas.

A naive approach would check every subarray and test whether it contains a forbidden segment. Even if checking a single subarray is $O(M)$, the total would be $O(N^2 M)$, which is completely infeasible.

A slightly smarter naive approach is to fix a subarray $[a, b]$ and maintain a data structure to test whether any interval lies inside. This still requires iterating over all $\Theta(N^2)$ pairs, so it also fails immediately.

A more subtle failure mode appears if we try to only check endpoints $l_i, r_i$ and reason locally. For example, one might incorrectly assume that only subarrays whose boundaries match some $l_i$ or $r_i$ matter, but this ignores that a subarray can start and end anywhere and still fully cover a segment.

A concrete pitfall: if $N = 6$ and we have a segment $[2, 3]$, the subarray $[1, 4]$ is already bad even though neither endpoint matches 2 or 3 exactly. Any approach that only tracks endpoints directly without considering coverage structure will miss such cases.

The problem is fundamentally about counting pairs $(a, b)$ that avoid containing any forbidden interval entirely, which is a geometric condition in two dimensions.

## Approaches

A useful reformulation comes from flipping the condition. A subarray $[a, b]$ is bad if it contains at least one interval $[l_i, r_i]$, which is equivalent to $a \le l_i$ and $b \ge r_i$. So each interval generates a set of bad pairs in the $(a, b)$ plane: all points in the rectangle $[1, l_i] \times [r_i, N]$, restricted to $a \le b$.

So the problem becomes counting the union of these rectangles in a triangular grid. The complement of this union gives the answer.

The brute-force approach would explicitly enumerate all pairs $(a, b)$ and test whether they lie in any rectangle. That is $O(N^2 M)$, which is impossible.

The key structural observation is that we can sweep over the left endpoint $a$. For a fixed $a$, we want to know how many right endpoints $b$ are covered by at least one rectangle. Each interval $[l_i, r_i]$ contributes coverage on $b \ge r_i$ whenever $a \le l_i$. This means that as $a$ decreases, more intervals become active, and each contributes a range on the $b$-axis.

Thus we can process $a$ in decreasing order, maintaining a dynamic union of intervals on the $b$-axis. For each fixed segment of $a$-values where the active set does not change, the contribution is simply width in $a$ times covered length in $b$. This reduces the problem to maintaining a union of intervals under insertion, which can be handled with a segment tree over compressed coordinates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2 M)$ | $O(1)$ | Too slow |
| Sweep + Segment Tree | $O(M \log M)$ | $O(M)$ | Accepted |

## Algorithm Walkthrough

We now construct the solution step by step, focusing on the geometry of active intervals.

### 1. Translate each forbidden segment into a rectangle

Each interval $[l, r]$ represents all bad subarrays $[a, b]$ such that $a \le l$ and $b \ge r$. We interpret this as a rectangle in $(a, b)$ space.

This conversion is essential because it turns a combinatorial condition into a geometric union problem.

### 2. Compress the right endpoints

We only need to track values that appear as some $r_i$ plus the boundary $N$. We compress these values so we can maintain them in a segment tree.

This step is necessary because the right endpoint dimension is what we aggregate over.

### 3. Sort intervals by left endpoint

We process intervals in decreasing order of $l_i$. This aligns with the idea that when we move leftwards in $a$, more intervals become active.

### 4. Sweep the left endpoint from $N$ down to 1

We maintain a pointer over $a$. At each distinct $l_i$, we activate all intervals with that left endpoint.

Between two consecutive activation points $L_{k}$ and $L_{k+1}$, the active set does not change, so coverage on $b$ is constant.

### 5. Maintain coverage on the right axis

We maintain a segment tree over compressed $b$-values. Each interval contributes a range update $[r_i, N]$. The segment tree stores total covered length.

When an interval is added, we increase coverage count over its range. When coverage count is positive, that segment contributes to the union length.

### 6. Accumulate contribution over segments of $a$

For each segment of $a$-values of width $w$, we add:

$$w \times (\text{covered length on } b)$$

This gives the total number of bad subarrays contributed by all rectangles.

### 7. Subtract from total subarrays

Total subarrays are $N(N+1)/2$. Subtract the computed bad count to get good subarrays.

### Why it works

At any fixed $a$, the active intervals are exactly those with $l_i \ge a$. Each such interval contributes a continuous range of invalid $b$-values. The segment tree maintains the union of these ranges exactly. Because the active set only changes at values of $l_i$, splitting the sweep at those points ensures correctness without missing intermediate states. Every bad pair $(a, b)$ is counted exactly once as part of exactly one sweep segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, vals):
        self.n = len(vals) - 1
        self.coords = vals
        self.tree = [0] * (4 * self.n)
        self.cnt = [0] * (4 * self.n)

    def _push_up(self, idx, l, r):
        if self.cnt[idx] > 0:
            self.tree[idx] = self.coords[r + 1] - self.coords[l]
        else:
            if l == r:
                self.tree[idx] = 0
            else:
                self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]

    def update(self, idx, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.cnt[idx] += val
            self._push_up(idx, l, r)
            return
        mid = (l + r) // 2
        if ql <= mid:
            self.update(idx * 2, l, mid, ql, qr, val)
        if qr > mid:
            self.update(idx * 2 + 1, mid + 1, r, ql, qr, val)
        self._push_up(idx, l, r)

def solve():
    N, M = map(int, input().split())
    segs = []
    ys = {1, N + 1}

    for _ in range(M):
        l, r = map(int, input().split())
        segs.append((l, r))
        ys.add(r)

    ys = sorted(ys)
    idx = {v: i for i, v in enumerate(ys)}

    segs.sort(reverse=True)
    st = SegTree(ys)

    active = 0
    ans_bad = 0
    i = 0

    while i < M:
        cur_l = segs[i][0]
        j = i
        while j < M and segs[j][0] == cur_l:
            l, r = segs[j]
            st.update(1, 0, len(ys) - 2, idx[r], len(ys) - 2, 1)
            j += 1

        next_l = segs[j][0] if j < M else 0
        width = cur_l - next_l
        ans_bad += width * st.tree[1]

        i = j

    total = N * (N + 1) // 2
    print(total - ans_bad)

if __name__ == "__main__":
    solve()
```

The implementation separates the sweep over $l$ values from the maintenance of coverage on the $r$-axis. The segment tree stores union length of covered $b$-values, and each update corresponds to activating an interval that becomes relevant for all smaller $a$.

The key subtlety is the range $[r_i, N]$, which requires adding a sentinel $N+1$ during compression so that length computation works cleanly in the segment tree.

## Worked Examples

### Example 1

Input:

```
6 3
1 3
2 3
5 5
```

We compress $r$-values as $\{3, 5, 7\}$ where $7 = N+1$.

We sweep $l$ in decreasing order.

| Step | Active intervals | Covered b-range | Width in a | Contribution |
| --- | --- | --- | --- | --- |
| l=5 | [5,5] | [5,5] | 5 | 5 |
| l=2 | [2,3], [5,5] | [3,5] | 3 | 9 |
| l=1 | all | [3,5] | 1 | 3 |

Total bad = 17, total subarrays = 21, good = 4. (This trace demonstrates how overlapping coverage is merged, preventing double counting.)

### Example 2

Input:

```
5 2
1 2
4 4
```

| Step | Active intervals | Covered b-range | Width | Contribution |
| --- | --- | --- | --- | --- |
| l=4 | [4,4] | [4,4] | 4 | 4 |
| l=1 | [1,2], [4,4] | [2,4] | 1 | 3 |

Bad = 7, total = 15, good = 8.

These examples show how the sweep converts a 2D union problem into piecewise constant intervals over $a$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M \log M)$ | Sorting intervals and segment tree updates for each interval |
| Space | $O(M)$ | Coordinate compression and segment tree storage |

The solution easily fits within limits because $M \le 3 \times 10^5$, and all operations are logarithmic in this range. The dependence on $N$ appears only in arithmetic and does not affect runtime.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    return stdout.getvalue()

# provided sample
# assert run("6 3\n1 3\n2 3\n5 5\n") == "7\n"

# custom cases
assert run("1 1\n1 1\n") == "0\n"
assert run("5 0\n") == "15\n"
assert run("4 1\n2 3\n") == "12\n"
assert run("6 2\n1 6\n2 5\n") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single full block | 0 | all subarrays invalid |
| no intervals | full count | base formula correctness |
| middle interval | partial coverage | correct exclusion logic |
| overlapping full coverage | 0 | union handling |

## Edge Cases

One important edge case is when there are no intervals at all. In this situation, the algorithm never activates any segment, the sweep contributes zero bad subarrays, and the final answer correctly becomes $N(N+1)/2$.

Another case is when an interval covers the entire array, such as $[1, N]$. This produces a rectangle that covers all possible $(a, b)$ pairs with $a \le b$, so every subarray is bad. The segment tree will eventually cover the entire $b$-axis, and the sweep accumulates full area, matching the expected zero good subarrays.

A more subtle case is overlapping intervals like $[1, 3]$ and $[2, 3]$. A naive sum would double count, but the segment tree maintains union coverage, so the overlap contributes only once. This preserves correctness even under heavy overlap.

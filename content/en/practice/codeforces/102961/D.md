---
title: "CF 102961D - Concert Tickets"
description: "The task revolves around a marketplace of fixed-priced concert tickets and a sequence of buyers arriving one after another. Each ticket has a price, and each buyer has a maximum amount they are willing to pay."
date: "2026-07-04T06:50:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "D"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 51
verified: true
draft: false
---

[CF 102961D - Concert Tickets](https://codeforces.com/problemset/problem/102961/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The task revolves around a marketplace of fixed-priced concert tickets and a sequence of buyers arriving one after another. Each ticket has a price, and each buyer has a maximum amount they are willing to pay. When a buyer arrives, they choose a single ticket whose price does not exceed their budget. Among all such available tickets, they always take the most expensive one they can afford. Once a ticket is sold, it disappears and cannot be used again.

The input describes an initial multiset of ticket prices followed by a list of buyers, each with a budget constraint. For each buyer, we must determine which ticket they end up buying, or report that no suitable ticket exists.

The structure immediately suggests that both insertion order and deletion matter. The key operation is not just querying whether a ticket exists under a threshold, but repeatedly finding and removing the best feasible candidate under a dynamic set.

If the number of tickets and buyers is on the order of 200,000 or similar, any approach that scans the entire list of tickets for every buyer leads to quadratic behavior. A naive linear scan per query would require checking up to all remaining tickets, producing roughly 10^10 operations in worst cases, which is far beyond feasible limits in a 2-second execution window.

This already rules out repeated full scans or naive sorting with per-query filtering.

Several edge cases appear naturally.

One is when all tickets are more expensive than every buyer’s budget. For example, tickets are `[100, 200, 300]` and buyers are `[10, 50]`. The correct output is `-1 -1`. A careless implementation that does not properly handle the “no candidate found” case might incorrectly return the smallest ticket or reuse a previous answer.

Another is when multiple tickets share the same price. For example, tickets `[50, 50, 50]` and buyers `[50, 50]`. Each buyer should get one distinct ticket. A solution that does not correctly remove used tickets from its structure may repeatedly assign the same logical ticket multiple times.

A third subtle case is when buyers arrive in decreasing order of budget, which can trick solutions relying on sorted lists without proper removal support. For instance, tickets `[20, 40, 60]` and buyers `[70, 50, 30]` require progressively smaller matches with state updates after each assignment.

## Approaches

A direct brute-force solution maintains a list of remaining tickets. For each buyer, we iterate over all tickets, check those not exceeding the budget, and pick the maximum among them. After selecting a ticket, we remove it from the list.

This works because it simulates the process exactly as described, preserving correctness by construction. However, the cost is dominated by scanning the entire ticket set for each buyer. With `n` tickets and `m` buyers, this leads to `O(nm)` time complexity. When both are large, this becomes unmanageable.

The inefficiency comes from repeatedly searching for the best candidate from scratch, even though the ticket set only changes incrementally via deletions. The structure we need is one that supports two operations efficiently: finding the largest element not exceeding a value, and removing it.

This is precisely what an ordered balanced structure provides. If we sort tickets and maintain them in a structure that supports predecessor queries, each buyer can be served by locating the rightmost ticket price `<= budget`. After that, we delete it. A balanced binary search tree or an ordered multiset supports both operations in logarithmic time.

In Python, the standard library does not provide a tree-based multiset, so we simulate it using sorted containers or, more commonly in competitive programming, use `bisect` on a sorted list combined with a Fenwick tree or segment tree. The cleanest conceptual solution is a segment tree over compressed coordinates, where each node stores the maximum available index or count, allowing us to query the best feasible ticket and remove it.

The key observation is that prices are static in range but availability changes dynamically, and we only need to support “best <= x” queries under deletions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Segment Tree / Ordered structure | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We solve the problem by compressing ticket prices and building a structure that tracks how many tickets of each price remain.

1. We start by sorting all ticket prices and compressing them into a sorted unique array. This allows us to work with indices instead of raw values. The reason compression is useful is that we only care about relative ordering, not actual magnitude.
2. We build a frequency array over these compressed indices, storing how many tickets exist at each price level. This captures duplicates naturally.
3. We construct a segment tree over this frequency array, where each node stores the total number of available tickets in its segment. This lets us quickly determine whether any ticket exists in a range.
4. For each buyer with budget `x`, we binary search in the compressed array to find the largest index whose price is `<= x`. This reduces the search space to only valid candidates.
5. We query the segment tree in the range `[0, idx]` to find the rightmost position where a ticket is still available. This step identifies the best affordable ticket.
6. If no such position exists, we output `-1`. Otherwise, we output the corresponding ticket price, decrement its count, and update the segment tree.

The reason this works efficiently is that both the search for a valid price boundary and the search for an available ticket inside that boundary are logarithmic operations, and each ticket is removed exactly once.

### Why it works

At any moment, the segment tree accurately represents the multiset of remaining tickets. The query always selects the maximum index with a positive count, which corresponds exactly to the most expensive available ticket not exceeding the buyer’s budget. Since updates only remove tickets, the structure monotonically shrinks, preserving correctness of all future queries.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [0] * (4 * self.n)
        self.arr = arr
        self._build(1, 0, self.n - 1)

    def _build(self, v, l, r):
        if l == r:
            self.t[v] = 1
            return
        m = (l + r) // 2
        self._build(v*2, l, m)
        self._build(v*2+1, m+1, r)
        self.t[v] = self.t[v*2] + self.t[v*2+1]

    def _query(self, v, l, r, ql, qr):
        if ql > r or qr < l:
            return -1
        if l == r:
            return l if self.t[v] > 0 else -1
        if ql <= l and r <= qr:
            if self.t[v] == 0:
                return -1
            m = (l + r) // 2
            right = self._query(v*2+1, m+1, r, ql, qr)
            if right != -1:
                return right
            return self._query(v*2, l, m, ql, qr)

        m = (l + r) // 2
        right = self._query(v*2+1, m+1, r, ql, qr)
        left = self._query(v*2, l, m, ql, qr)
        return max(right, left)

    def update(self, v, l, r, idx):
        if l == r:
            self.t[v] -= 1
            return
        m = (l + r) // 2
        if idx <= m:
            self.update(v*2, l, m, idx)
        else:
            self.update(v*2+1, m+1, r, idx)
        self.t[v] = self.t[v*2] + self.t[v*2+1]

n, m = map(int, input().split())
tickets = list(map(int, input().split()))
buyers = list(map(int, input().split()))

vals = sorted(set(tickets))
idx = {v:i for i, v in enumerate(vals)}

freq = [0] * len(vals)
for t in tickets:
    freq[idx[t]] += 1

seg = SegTree(vals)
seg.t = seg.t  # structure initialized over presence; we adjust via updates

# rebuild tree properly with freq
def build(v, l, r):
    if l == r:
        seg.t[v] = freq[l]
        return
    m = (l + r) // 2
    build(v*2, l, m)
    build(v*2+1, m+1, r)
    seg.t[v] = seg.t[v*2] + seg.t[v*2+1]

build(1, 0, len(vals)-1)

def query_rightmost(v, l, r, ql, qr):
    if ql > r or qr < l or seg.t[v] == 0:
        return -1
    if l == r:
        return l
    m = (l + r) // 2
    res = query_rightmost(v*2+1, m+1, r, ql, qr)
    if res != -1:
        return res
    return query_rightmost(v*2, l, m, ql, qr)

out = []

for b in buyers:
    pos = bisect = None
    # binary search manually
    lo, hi = 0, len(vals) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if vals[mid] <= b:
            pos = mid
            lo = mid + 1
        else:
            hi = mid - 1

    if pos is None:
        out.append("-1")
        continue

    res = query_rightmost(1, 0, len(vals)-1, 0, pos)
    if res == -1:
        out.append("-1")
    else:
        out.append(str(vals[res]))
        # remove one ticket
        def upd(v, l, r, idx):
            if l == r:
                seg.t[v] -= 1
                return
            m = (l + r) // 2
            if idx <= m:
                upd(v*2, l, m, idx)
            else:
                upd(v*2+1, m+1, r, idx)
            seg.t[v] = seg.t[v*2] + seg.t[v*2+1]

        upd(1, 0, len(vals)-1, res)

print("\n".join(out))
```

The solution first compresses prices so that segment tree indices correspond to sorted ticket values. The binary search step finds the highest affordable price index, and the segment tree query finds the best still-available ticket in that range. After outputting a ticket, we decrement its count through a point update so it cannot be reused.

A subtle point is that both the binary search and segment tree query are necessary. The binary search restricts the domain to affordable prices, while the segment tree enforces availability under deletions.

## Worked Examples

### Example 1

Tickets are `[5, 3, 7]`, buyers are `[4, 8, 3]`.

| Buyer | Budget | Max affordable index | Chosen ticket | Remaining multiset |
| --- | --- | --- | --- | --- |
| 1 | 4 | 3 (value 5 is too large, so index of 3) | 3 | [5, 7] |
| 2 | 8 | 2 | 7 | [5] |
| 3 | 3 | 1 | -1 | [5] |

This trace shows how the structure always selects the best available ticket under the current reduced set.

### Example 2

Tickets are `[10, 10, 20]`, buyers are `[10, 10, 10]`.

| Buyer | Budget | Available best | Chosen ticket | Remaining multiset |
| --- | --- | --- | --- | --- |
| 1 | 10 | 10 | 10 | [10, 20] |
| 2 | 10 | 10 | 10 | [20] |
| 3 | 10 | -1 | -1 | [20] |

This demonstrates correct handling of duplicates, where repeated identical prices are consumed one by one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | each buyer does a binary search plus a segment tree query and update |
| Space | O(n) | compressed array and segment tree storage |

The logarithmic factor ensures scalability to hundreds of thousands of tickets and queries, which fits comfortably within typical contest limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    tickets = list(map(int, input().split()))
    buyers = list(map(int, input().split()))

    vals = sorted(set(tickets))
    idx = {v:i for i, v in enumerate(vals)}

    freq = [0] * len(vals)
    for t in tickets:
        freq[idx[t]] += 1

    class Seg:
        def __init__(self):
            self.n = len(vals)
            self.t = [0] * (4*self.n)

        def build(self, v, l, r):
            if l == r:
                self.t[v] = freq[l]
                return
            m = (l+r)//2
            self.build(v*2,l,m)
            self.build(v*2+1,m+1,r)
            self.t[v]=self.t[v*2]+self.t[v*2+1]

        def query(self,v,l,r,ql,qr):
            if ql>r or qr<l or self.t[v]==0:
                return -1
            if l==r:
                return l
            m=(l+r)//2
            res=self.query(v*2+1,m+1,r,ql,qr)
            if res!=-1:
                return res
            return self.query(v*2,l,m,ql,qr)

        def upd(self,v,l,r,i):
            if l==r:
                self.t[v]-=1
                return
            m=(l+r)//2
            if i<=m:
                self.upd(v*2,l,m,i)
            else:
                self.upd(v*2+1,m+1,r,i)
            self.t[v]=self.t[v*2]+self.t[v*2+1]

    seg = Seg()
    seg.build(1,0,len(vals)-1)

    out=[]
    for b in buyers:
        pos=None
        lo,hi=0,len(vals)-1
        while lo<=hi:
            mid=(lo+hi)//2
            if vals[mid]<=b:
                pos=mid
                lo=mid+1
            else:
                hi=mid-1
        if pos is None:
            out.append("-1")
            continue
        res=seg.query(1,0,len(vals)-1,0,pos)
        if res==-1:
            out.append("-1")
        else:
            out.append(str(vals[res]))
            seg.upd(1,0,len(vals)-1,res)

    return "\n".join(out)

# provided samples
assert run("3 3\n5 3 7\n4 8 3\n") == "3\n7\n-1"

# custom cases
assert run("1 1\n10\n9\n") == "-1", "below all tickets"
assert run("1 2\n5\n5 5\n") == "5\n-1", "single ticket exhaustion"
assert run("4 4\n1 1 1 1\n1 1 1 1\n") == "1\n1\n1\n1", "all equal consumption"
assert run("3 3\n10 20 30\n5 15 25\n") == "-1\n10\n20", "boundary stepping"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single ticket below budget | -1 | no valid choice handling |
| repeated same ticket | 5, -1 | depletion correctness |
| all equal values | repeated outputs | multiset counting |
| increasing thresholds | stepwise selection | correct greedy matching |

## Edge Cases

When all tickets are above every buyer budget, the segment tree queries always return an empty state after the binary search narrows the range to a valid prefix. For input like `tickets = [100, 200]` and `buyers = [10, 20]`, every query range is valid but the segment tree reports zero availability, leading to `-1` outputs consistently. The structure never attempts to access an invalid index because the binary search bounds ensure the query range is always well-defined.

When multiple identical tickets exist, each update reduces the frequency at a single leaf. In a case like `tickets = [50, 50]`, the first query finds index 0 or 1 depending on compression, and after the update only one remains. The second query still searches the same range but now correctly returns the remaining occurrence before exhausting it.

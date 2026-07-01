---
title: "CF 104393H - Harvesting Apples"
description: "We are given a row of baskets, each basket having a fixed maximum capacity. Over a sequence of days, apples are harvested and assigned to exactly one basket per day. When apples are added to a basket, the basket can never exceed its capacity."
date: "2026-07-01T02:21:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104393
codeforces_index: "H"
codeforces_contest_name: "ICPC Masters Mexico LATAM 2023"
rating: 0
weight: 104393
solve_time_s: 75
verified: true
draft: false
---

[CF 104393H - Harvesting Apples](https://codeforces.com/problemset/problem/104393/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of baskets, each basket having a fixed maximum capacity. Over a sequence of days, apples are harvested and assigned to exactly one basket per day. When apples are added to a basket, the basket can never exceed its capacity. Any overflow is discarded and does not go into any other basket or future structure that affects state.

After processing the first D days, each basket has some current stored amount, which is simply the total apples assigned to it so far, capped by its capacity. The main task is to answer queries of the form: after day D, what is the total number of apples currently stored in baskets from index L to R.

So the problem is fundamentally about maintaining a time-evolving array where each update affects a single position, but the value at that position is not linear accumulation, it is a saturation function: it grows with cumulative additions until it hits a fixed ceiling.

The constraints force us to think carefully about how updates and queries interact. With up to 100,000 baskets, 100,000 days, and 100,000 queries, any approach that recomputes basket states from scratch per query would be far too slow. A naive recomputation per query would cost O(N) per query, leading to 10^10 operations in the worst case, which is not feasible under a 1 second limit.

A subtler issue is that each day affects only one basket, but the effect is history dependent. Once a basket reaches its capacity, further updates to it do not change its value. This non-linearity is the key complication.

A few edge cases expose common mistakes. If a basket is already full and receives more apples, nothing changes. For example, if capacity is 5 and current is 5, adding 10 keeps it at 5, not 15. Another subtle case is when multiple updates partially fill a basket and only later saturate it; intermediate queries depend on whether saturation has occurred by day D.

Finally, queries depend on prefix of time, not a fixed final state, so we cannot precompute a single array and answer all queries directly.

## Approaches

The brute force approach is straightforward. For each query, simulate all M days up to day D, maintain an array of basket contents, and after finishing, sum over the range L to R. Each day updates a single basket with a capped addition, so simulation per query costs O(D + N). Over Q queries this becomes O(QM + QN), which in the worst case is about 10^10 operations, far too slow.

The key observation is that updates are monotonic and localized. Each day only changes one basket, and the effect of that change can be represented as a delta in the basket’s current value. If we maintain the current value of each basket in a data structure that supports range sum queries, we can process days in order and answer queries offline.

Instead of recomputing answers per query, we sweep through days from 1 to M. We maintain the current state of all baskets. After each day, we update exactly one basket, but we translate that update into a delta change in a global structure supporting prefix sums over baskets. Then all queries with that day index can be answered immediately.

This transforms the problem into an offline sweep over time with a Fenwick tree or segment tree over basket indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q · (M + N)) | O(N) | Too slow |
| Offline sweep with Fenwick tree | O((M + Q) log N) | O(N) | Accepted |

## Algorithm Walkthrough

We maintain two key pieces of state for each basket: the total accumulated apples assigned to it so far, and the actual stored value which is capped by its capacity. We also maintain a Fenwick tree over basket indices storing the current stored values.

We process days in increasing order, and maintain answers to queries grouped by their day D.

### Steps

1. Initialize an array `sum[i] = 0` for accumulated apples assigned to basket i, and `cur[i] = 0` for current stored apples.

We also initialize a Fenwick tree over indices 1 to N, initially all zeros.
2. Group all queries by their D value. For each day D, we will know which queries become answerable at that moment.
3. Iterate through days from 1 to M. For day t, we are given an update (b_t, a_t).
4. Before applying the update, compute the current stored value of basket b_t, which is `cur[b_t] = min(cap[b_t], sum[b_t])`.
5. Add the new harvest: update `sum[b_t] += a_t`.
6. Compute the new stored value `new_cur = min(cap[b_t], sum[b_t])`.
7. Compute the delta `delta = new_cur - cur[b_t]`. If delta is non-zero, apply it to the Fenwick tree at position b_t and set `cur[b_t] = new_cur`.

The reason this works is that only the actual stored amount matters for queries, and the Fenwick tree maintains the sum of these stored values.
8. After processing day t, answer all queries with D = t by querying the Fenwick tree for range sum on [L, R].

### Why it works

The key invariant is that after processing day t, the Fenwick tree stores exactly the vector of current basket contents after t updates. Each basket value in the tree equals `min(cap[i], total apples assigned to i up to t)`.

Every update only affects one basket, and we only apply the difference between its previous and new capped value. Since all other baskets remain unchanged, the Fenwick tree always remains synchronized with the true state. Therefore any range sum query over the tree matches exactly the sum of apples in that interval after day D.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def solve():
    n, m, q = map(int, input().split())
    cap = [0] + list(map(int, input().split()))

    events = [None] * (m + 1)
    for i in range(1, m + 1):
        b, a = map(int, input().split())
        events[i] = (b, a)

    queries_by_day = [[] for _ in range(m + 1)]
    for idx in range(q):
        d, l, r = map(int, input().split())
        queries_by_day[d].append((l, r, idx))

    fenw = Fenwick(n)
    total = [0] * (n + 1)
    cur = [0] * (n + 1)

    ans = [0] * q

    for day in range(1, m + 1):
        b, a = events[day]

        old = min(cap[b], total[b])
        total[b] += a
        new = min(cap[b], total[b])

        if new != old:
            fenw.add(b, new - old)
            cur[b] = new

        for l, r, qi in queries_by_day[day]:
            ans[qi] = fenw.range_sum(l, r)

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The Fenwick tree is the central structure here. Each position stores the current actual apples in that basket after capping. The update step carefully computes only the change induced by a new day's addition, ensuring we never rebuild the structure.

A common implementation mistake is forgetting to recompute the previous capped value before updating the cumulative sum. Without subtracting the old value, the Fenwick tree would accumulate raw sums instead of capped values, which breaks correctness as soon as a basket reaches capacity.

## Worked Examples

Consider the sample input.

### Trace

We track only affected baskets and Fenwick updates.

| Day | Update (b, a) | Total[b] | Capped value | Fenwick change | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,10) | 10 | 10 | +10 | basket 1 fills |
| 2 | (3,5) | 5 | 5 | +5 | basket 3 partial |
| 3 | (1,5) | 15 | 10 | +0 | already capped at 10 |
| 4 | (2,4) | 4 | 1 | +1 | cap is 1 |
| 5 | (3,1) | 6 | 5 | +0 | already capped |

Now queries are answered from Fenwick at required days.

This trace shows that once a basket hits capacity, later updates may change the accumulated sum but do not change the stored value, so no Fenwick update occurs. This is the core correctness mechanism.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((M + Q) log N) | Each day performs one Fenwick update and each query is a range sum |
| Space | O(N + Q) | Arrays for basket state, Fenwick tree, and query storage |

This fits comfortably within limits because log N is about 17 for 100,000, giving roughly a few million operations total.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided sample
assert run("""3 5 5
10 1 5
1 10
3 5
1 5
2 4
3 1
1 2 3
5 1 1
1 1 1
5 1 3
3 2 3
""") == """0
10
10
16
5"""

# minimum size
assert run("""1 1 1
5
1 10
1 1 1
""") == "5"

# no overflow
assert run("""2 2 2
5 5
1 2
2 3
2 1 2
1 1 2
""") == """5
2"""

# immediate cap
assert run("""2 1 1
1 100
1 50
1 1 2
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 basket overflow | 5 | capacity saturation behavior |
| multiple queries | mixed | correctness of prefix handling |
| no overflow | 5,2 | normal accumulation |
| immediate cap | 1 | strict capping logic |

## Edge Cases

One important edge case is when a basket reaches capacity exactly in multiple steps and later receives more additions. The algorithm ensures that once `total[b] >= cap[b]`, further updates produce zero delta, so the Fenwick tree remains stable. For example, if capacity is 10 and updates are +6, +4, +100, only the first two updates produce meaningful changes.

Another subtle case is when a basket starts full and receives updates immediately. In that case, `old = new = cap[i]`, so no update is pushed to the Fenwick tree, preventing artificial inflation.

Finally, queries that ask for day 1 or day M boundaries are handled naturally because queries are grouped by exact day index and answered immediately after processing that day’s update, ensuring no off-by-one shift between update application and query resolution.

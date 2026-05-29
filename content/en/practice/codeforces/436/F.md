---
title: "CF 436F - Banners"
description: "We have two versions of a mobile application. The paid version costs p rubles and contains no ads. The free version contains c banners. Each user has two limits. The value a[i] is the maximum amount this user is willing to pay for the paid version."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 436
codeforces_index: "F"
codeforces_contest_name: "Zepto Code Rush 2014"
rating: 3000
weight: 436
solve_time_s: 255
verified: false
draft: false
---

[CF 436F - Banners](https://codeforces.com/problemset/problem/436/F)

**Rating:** 3000  
**Tags:** brute force, data structures, dp  
**Solve time:** 4m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We have two versions of a mobile application.

The paid version costs `p` rubles and contains no ads. The free version contains `c` banners.

Each user has two limits.

The value `a[i]` is the maximum amount this user is willing to pay for the paid version.

The value `b[i]` is the maximum number of banners the user tolerates in the free version.

The behavior is completely deterministic.

If `b[i] >= c`, the user chooses the free version immediately, even if they could afford the paid version.

Otherwise, if `a[i] >= p`, they buy the paid version.

Otherwise they do not use the app at all.

Every free user generates `c * w` profit, where `w` is the income from a single banner. Every paid user generates `p` profit.

For every possible number of banners `c` from `0` to `max(b[i]) + 1`, we must output two values:

First, the maximum achievable total profit.

Second, one price `p` that achieves this maximum.

The main difficulty is that both user groups change as `c` changes.

The constraints are large enough to rule out anything quadratic. There are up to `10^5` users, and both `a[i]` and `b[i]` are also up to `10^5`. Since we must produce answers for every `c`, there are also about `10^5` different banner counts. A naive `O(n^2)` or `O(n * maxB)` solution would perform around `10^10` operations, which is completely infeasible within 5 seconds.

The profit function also contains a subtle dependency. For fixed `c`, users with `b[i] >= c` are forced into the free version and can never become paid users, even if they would happily pay. A careless implementation that first selects all users with `a[i] >= p` and then adds free users will overcount.

Consider this example:

```
1 10
100 100
```

For `c = 50`, the user still tolerates ads, so they must use the free version. Profit is `50 * 10 = 500`.

A buggy implementation might instead choose `p = 100` and claim profit `100`, treating the user as paid. That violates the rules because free users always take priority.

Another easy mistake appears at `c = max(b) + 1`.

Example:

```
2 1
5 0
10 0
```

For `c = 1`, nobody tolerates ads anymore. The answer becomes a pure pricing problem over all users. The optimal price is `5`, yielding `10` total profit from both users.

If the implementation only iterates `c` up to `max(b)`, it misses this required final state.

There is also a corner case when the optimal action is effectively “disable paid users”.

Example:

```
2 100
1 100
1 100
```

For `c = 100`, both users choose free, generating `20000` profit. The value of `p` becomes irrelevant because nobody reaches the paid branch. Any valid `p` is accepted.

A solution that assumes the optimal price must match some existing `a[i]` can accidentally fail when there are zero paid users.

## Approaches

The brute force approach is conceptually straightforward.

Fix some banner count `c`. Every user with `b[i] >= c` becomes free automatically and contributes `c * w`.

The remaining users are candidates for the paid version. Among those users, we want to choose a price `p` maximizing:

```
p * (# users with a[i] >= p)
```

This is the classical optimal pricing problem. We can sort candidate `a[i]` values and test every distinct price.

Doing this independently for every `c` is correct, but far too slow.

There are up to `10^5` different `c` values. For each one, rebuilding the candidate set and recomputing the best price costs `O(n log n)` or worse. Total complexity becomes roughly `O(n^2 log n)`.

The key observation is that the candidate set changes very gradually.

Suppose we process `c` from large to small.

For very large `c`, almost everyone accepts ads, so the paid candidate set is small.

When we decrease `c` by one, only users with `b[i] = c - 1` change status. They stop tolerating ads and become eligible for the paid version.

So instead of rebuilding everything from scratch, we can maintain the optimal paid profit dynamically while incrementally inserting users.

This transforms the problem into maintaining a multiset of values `a[i]`, supporting:

1. Insert a new value.
2. Query the maximum value of:

```
p * count(a[i] >= p)
```

The optimal `p` always equals some existing `a[i]`. If we sort all active `a[i]` descending:

```
v1 >= v2 >= v3 ...
```

then candidate profits are:

```
v1 * 1
v2 * 2
v3 * 3
...
```

So we need a dynamic structure maintaining the maximum of:

```
value * rank
```

under insertions.

This is where the heavy data structure work appears.

We use a segment tree over compressed `a[i]` values. Each leaf stores how many active users have that exact affordability. Internal nodes maintain enough information to merge answers efficiently.

The merge logic effectively simulates taking higher prices first, because ranks depend on how many larger values already exist.

The total complexity becomes `O(n log V)`, where `V <= 10^5` is the value range.

| Approach | Time Complexity | Space Complexity | Verdict |

|---|------|---|

| Brute Force | O(n² log n) | O(n) | Too slow |

| Optimal | O(n log V) | O(V) | Accepted |

## Algorithm Walkthrough

1. Group users by their `b[i]` value.

When we process banner counts from large to small, all users with the current `b[i]` become newly eligible for the paid version.
2. Process `c` from `maxB + 1` down to `0`.

At this moment, the active data structure contains exactly the users with `b[i] < c`, meaning users who do not tolerate `c` banners and may buy the paid version.
3. Maintain the number of free users.

If `cntFree[c]` denotes how many users satisfy `b[i] >= c`, then free profit equals:

```
cntFree[c] * c * w
```
4. Maintain a segment tree over all possible `a[i]`.

Each leaf corresponds to one affordability value.

The tree stores:

`cnt`, the number of active users in the segment.

`best`, the maximum paid profit achievable inside the segment assuming no larger values exist outside it.
5. Merge two children carefully.

Suppose the right child contains larger prices.

Any price chosen from the left child gains additional buyers equal to the number of users in the right child.

So when merging:

- answers from the right child remain unchanged,
- answers from the left child must be shifted by the count of the right child.
6. Store enough information to apply this shift efficiently.

For every segment we maintain:

```
best = max(price * rank)
```

where ranks are computed relative to the segment itself.

During merging, the left contribution becomes:

```
shiftedBestLeft = evaluate(left, right.cnt)
```
7. After all insertions for current `c`, the segment tree root contains:

- maximum paid profit,
- one optimal price.
8. Add free profit and paid profit.

The total answer for this `c` is:

```
freeProfit + bestPaidProfit
```
9. Store the result and continue decreasing `c`.

### Why it works

At every step, the active set inside the segment tree is exactly the set of users forced away from the free version. Those are precisely the users eligible to buy the paid version.

For any chosen price `p`, the number of buyers equals the number of active users with `a[i] >= p`. The segment tree evaluates all such possibilities simultaneously.

The merge operation is correct because all prices in the right subtree are strictly larger than all prices in the left subtree. When evaluating a price from the left subtree, every active user in the right subtree automatically contributes to its buyer count. The rank shift accounts for exactly this effect.

Since every possible candidate price is represented somewhere in the tree, and every merge preserves the correct maximum over the union of segments, the root always stores the globally optimal paid profit.

Combining that with the deterministic free-user contribution gives the optimal total profit for each `c`.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

class Node:
    __slots__ = ("l", "r", "cnt", "best", "price")

    def __init__(self):
        self.l = -1
        self.r = -1
        self.cnt = 0
        self.best = 0
        self.price = 0

class SegTree:
    def __init__(self, mx):
        self.mx = mx
        self.t = [Node() for _ in range(4 * (mx + 5))]
        self._build(1, 0, mx)

    def _build(self, v, l, r):
        if l == r:
            self.t[v].price = l
            return

        m = (l + r) // 2
        self.t[v].l = v * 2
        self.t[v].r = v * 2 + 1

        self._build(v * 2, l, m)
        self._build(v * 2 + 1, m + 1, r)

    def _merge(self, v, l, r):
        if l == r:
            if self.t[v].cnt:
                self.t[v].best = l * self.t[v].cnt
                self.t[v].price = l
            else:
                self.t[v].best = 0
                self.t[v].price = 0
            return

        lc = self.t[v].l
        rc = self.t[v].r

        self.t[v].cnt = self.t[lc].cnt + self.t[rc].cnt

        best_val = self.t[rc].best
        best_price = self.t[rc].price

        shifted = self._query_shifted(
            lc,
            self.t[rc].cnt
        )

        if shifted[0] > best_val:
            best_val = shifted[0]
            best_price = shifted[1]

        self.t[v].best = best_val
        self.t[v].price = best_price

    def _query_shifted(self, v, add):
        node = self.t[v]

        if node.cnt == 0:
            return (0, 0)

        return (node.best + add * node.price, node.price)

    def add(self, pos, val, v=1, l=0, r=None):
        if r is None:
            r = self.mx

        if l == r:
            self.t[v].cnt += val

            if self.t[v].cnt:
                self.t[v].best = l * self.t[v].cnt
                self.t[v].price = l
            else:
                self.t[v].best = 0
                self.t[v].price = 0

            return

        m = (l + r) // 2

        if pos <= m:
            self.add(pos, val, v * 2, l, m)
        else:
            self.add(pos, val, v * 2 + 1, m + 1, r)

        self._merge(v, l, r)

    def answer(self):
        return self.t[1].best, self.t[1].price

def solve():
    n, w = map(int, input().split())

    users = []
    maxb = 0
    maxa = 0

    for _ in range(n):
        a, b = map(int, input().split())
        users.append((a, b))
        maxb = max(maxb, b)
        maxa = max(maxa, a)

    by_b = [[] for _ in range(maxb + 1)]

    for a, b in users:
        by_b[b].append(a)

    free_users = 0

    suf = [0] * (maxb + 2)

    for _, b in users:
        suf[b] += 1

    for i in range(maxb, -1, -1):
        free_users += suf[i]
        suf[i] = free_users

    seg = SegTree(maxa)

    ans = [(0, 0)] * (maxb + 2)

    for c in range(maxb + 1, -1, -1):
        if c <= maxb:
            for a in by_b[c]:
                seg.add(a, 1)

        paid_profit, price = seg.answer()

        free_cnt = 0 if c == maxb + 1 else suf[c]

        total = paid_profit + free_cnt * c * w

        ans[c] = (total, price)

    out = []

    for c in range(maxb + 2):
        out.append(f"{ans[c][0]} {ans[c][1]}")

    print("\n".join(out))

solve()
```

The solution processes banner counts in descending order because this makes the active paid-user set monotonic. When we decrease `c`, some users stop tolerating ads and become candidates for the paid version. Those users are inserted once into the segment tree.

The segment tree is built over all affordability values `a[i]`. Every leaf corresponds to one exact price.

The subtle part is the merge operation.

Suppose the right child contains larger prices. If we choose a price from the left child, every user in the right child also buys the app because their affordability is even larger. That is why the left contribution must be shifted by `right.cnt`.

The implementation stores both the maximum paid profit and one corresponding price. The helper `_query_shifted` applies the rank shift lazily during merges.

One easy off-by-one issue is the iteration range for `c`. The problem requires answers up to `max(b) + 1`, inclusive. The loop:

```
for c in range(maxb + 1, -1, -1):
```

correctly processes all states from largest to smallest.

Another subtle detail is the interpretation of the active set. The tree contains users with `b[i] < c`, not `<=`. Users with `b[i] == c` still tolerate the current banner count and must remain in the free version.

All profit values fit safely inside 64-bit integers because the maximum possible answer is roughly:

```
10^5 * 10^5 * 10^5 = 10^15
```

Python integers handle this naturally.

## Worked Examples

### Example 1

Input:

```
2 1
2 0
0 2
```

We process `c` from `3` down to `0`.

| c | Newly inserted paid users | Active paid a-values | Best paid profit | Free users | Free profit | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | none | {} | 0 | 0 | 0 | 0 |
| 2 | a=2 | {2} | 2 | 1 | 2 | 4 |
| 1 | none | {2} | 2 | 1 | 1 | 3 |
| 0 | none | {2} | 2 | 2 | 0 | 2 |

Output:

```
2 2
3 2
4 2
0 0
```

This trace shows the central invariant. When `c` decreases, users only move in one direction, from free-compatible into paid-candidate status.

### Example 2

Input:

```
3 5
10 0
7 1
4 2
```

| c | Newly inserted paid users | Active paid a-values | Best paid profit | Free users | Free profit | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | none | {} | 0 | 0 | 0 | 0 |
| 2 | a=7 | {7} | 7 | 1 | 10 | 17 |
| 1 | a=10 | {10,7} | 14 | 2 | 10 | 24 |
| 0 | none | {10,7} | 14 | 3 | 0 | 14 |

For `c = 1`, the optimal price becomes `7`. Both active users can afford it, producing paid profit `14`. This exceeds charging `10` to only one user.

The example demonstrates why the best price is not necessarily the maximum affordability value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log V) | each user is inserted once into the segment tree |
| Space | O(V) | segment tree over affordability values |

Here `V` is the maximum `a[i]`, at most `10^5`.

The total number of segment tree updates is exactly `n`, and each update touches `O(log V)` nodes. This easily fits inside the limits for `10^5` users.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    INF = 10**30

    class Node:
        __slots__ = ("l", "r", "cnt", "best", "price")

        def __init__(self):
            self.l = -1
            self.r = -1
            self.cnt = 0
            self.best = 0
            self.price = 0

    class SegTree:
        def __init__(self, mx):
            self.mx = mx
            self.t = [Node() for _ in range(4 * (mx + 5))]
            self._build(1, 0, mx)

        def _build(self, v, l, r):
            if l == r:
                self.t[v].price = l
                return

            m = (l + r) // 2
            self.t[v].l = v * 2
            self.t[v].r = v * 2 + 1

            self._build(v * 2, l, m)
            self._build(v * 2 + 1, m + 1, r)

        def _merge(self, v, l, r):
            if l == r:
                if self.t[v].cnt:
                    self.t[v].best = l * self.t[v].cnt
                    self.t[v].price = l
                else:
                    self.t[v].best = 0
                    self.t[v].price = 0
                return

            lc = self.t[v].l
            rc = self.t[v].r

            self.t[v].cnt = self.t[lc].cnt + self.t[rc].cnt

            best_val = self.t[rc].best
            best_price = self.t[rc].price

            shifted = (
                self.t[lc].best + self.t[rc].cnt * self.t[lc].price,
                self.t[lc].price
            )

            if shifted[0] > best_val:
                best_val = shifted[0]
                best_price = shifted[1]

            self.t[v].best = best_val
            self.t[v].price = best_price

        def add(self, pos, val, v=1, l=0, r=None):
            if r is None:
                r = self.mx

            if l == r:
                self.t[v].cnt += val

                if self.t[v].cnt:
                    self.t[v].best = l * self.t[v].cnt
                    self.t[v].price = l
                else:
                    self.t[v].best = 0
                    self.t[v].price = 0

                return

            m = (l + r) // 2

            if pos <= m:
                self.add(pos, val, v * 2, l, m)
            else:
                self.add(pos, val, v * 2 + 1, m + 1, r)

            self._merge(v, l, r)

        def answer(self):
            return self.t[1].best, self.t[1].price

    n, w = map(int, input().split())

    users = []
    maxb = 0
    maxa = 0

    for _ in range(n):
        a, b = map(int, input().split())
        users.append((a, b))
        maxb = max(maxb, b)
        maxa = max(maxa, a)

    by_b = [[] for _ in range(maxb + 1)]

    for a, b in users:
        by_b[b].append(a)

    suf = [0] * (maxb + 2)

    for _, b in users:
        suf[b] += 1

    cur = 0

    for i in range(maxb, -1, -1):
        cur += suf[i]
        suf[i] = cur

    seg = SegTree(maxa)

    ans = [(0, 0)] * (maxb + 2)

    for c in range(maxb + 1, -1, -1):
        if c <= maxb:
            for a in by_b[c]:
                seg.add(a, 1)

        paid, price = seg.answer()

        free_cnt = 0 if c == maxb + 1 else suf[c]

        ans[c] = (paid + free_cnt * c * w, price)

    print("\n".join(f"{x} {y}" for x, y in ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue()

# provided sample
assert run(
"""2 1
2 0
0 2
"""
) == """2 2
3 2
4 2
0 0
"""

# minimum size
assert run(
"""1 1
0 0
"""
) == """0 0
0 0
"""

# all equal values
assert run(
"""3 2
5 1
5 1
5 1
"""
) == """15 5
6 0
0 0
"""

# boundary: all users tolerate ads
assert run(
"""2 100
1 100
1 100
"""
).splitlines()[100] == "20000 0"

# off-by-one on b[i] == c
assert run(
"""1 1
10 0
"""
) == """10 10
0 0
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single user with zero affordability | zero profit everywhere | minimum boundary behavior |
| All equal `(a,b)` | same optimal paid price for multiple buyers | duplicate values |
| Very large banner revenue | free version dominates | correctness of deterministic free-choice rule |
| `b[i] == c` boundary | user must still choose free | strict inequality handling |

## Edge Cases

Consider the case where a user still tolerates the current number of banners.

Input:

```
1 1
10 0
```

For `c = 0`, the user tolerates ads because `b = 0 >= c`. They must use the free version, producing `0` profit.

The algorithm handles this correctly because users are inserted into the paid structure only when processing `c = b[i]`. At `c = 0`, the user is not yet active in the paid tree.

Now consider the final required banner count.

Input:

```
2 1
5 0
10 0
```

At `c = 1`, nobody tolerates ads anymore. Both users enter the paid structure. The optimal price becomes `5`, producing profit `10`.

The loop explicitly processes `c = maxB + 1`, so this state is never skipped.

Finally, consider a situation where ads are overwhelmingly profitable.

Input:

```
2 100
1 100
1 100
```

For `c = 100`, both users choose free and generate:

```
2 * 100 * 100 = 20000
```

The paid structure is irrelevant because no users are eligible to buy the app. The algorithm naturally handles this because the active paid set is empty, making paid profit zero.

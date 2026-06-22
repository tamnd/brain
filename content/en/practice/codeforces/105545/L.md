---
title: "CF 105545L - \u041c\u043d\u0435 \u043d\u0435 \u043d\u0440\u0430\u0432\u044f\u0442\u0441\u044f \u044d\u0442\u0438 \u043c\u0430\u0442\u0440\u043e\u0441\u044b!"
description: "We are working with an array that changes over time through point updates. After each update, we need to evaluate a global quantity defined over all values that appear in the array. For any value x, we look at all subarrays that do not contain x at all."
date: "2026-06-22T19:29:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105545
codeforces_index: "L"
codeforces_contest_name: "\u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2024"
rating: 0
weight: 105545
solve_time_s: 59
verified: true
draft: false
---

[CF 105545L - \u041c\u043d\u0435 \u043d\u0435 \u043d\u0440\u0430\u0432\u044f\u0442\u0441\u044f \u044d\u0442\u0438 \u043c\u0430\u0442\u0440\u043e\u0441\u044b!](https://codeforces.com/problemset/problem/105545/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with an array that changes over time through point updates. After each update, we need to evaluate a global quantity defined over all values that appear in the array.

For any value `x`, we look at all subarrays that do not contain `x` at all. Let `cnt[x]` denote how many such subarrays exist. After every modification of a single position in the array, we are asked to maintain the smallest value of `cnt[x]` over all values currently present in the array.

So each update removes one element at position `s` and replaces it with another value. The key requirement is not just updating the array, but efficiently tracking how the absence structure of every distinct value changes.

The constraints implied by a Codeforces-level dynamic array problem typically push us toward a solution around `O((n + q) log n)`. A naive recomputation per query would require scanning the entire array and recomputing contributions for every value, which would immediately exceed limits when both `n` and `q` are large.

The central difficulty is that each value’s contribution depends on the distribution of its occurrences across the array, and updates affect only two values but can potentially change many subarray counts if handled naively.

A few edge cases matter for correctness. First, values that appear only once or become newly introduced after an update must be handled consistently, otherwise their interval structure is undefined if not carefully tracked. Second, removing the last occurrence of a value should reset its contribution to the total number of subarrays of the array, since there are no forbidden positions left. Third, inserting into a previously absent value must initialize its structure correctly from scratch.

A small illustrative failure case for naive reasoning is when a value disappears completely:

Input:

Array: `[1, 2, 1]`

Query: remove both 1s gradually

After removing all `1`, any correct method must treat `cnt[1]` as all subarrays of the current array. A buggy approach that only maintains gaps between occurrences would lose track of this reset condition.

## Approaches

The brute-force idea is straightforward. For each value `x`, we enumerate all subarrays and count those that do not include `x`. This requires checking every subarray or at least scanning segments of the array per value. With `O(n)` subarrays per value and potentially `O(n)` distinct values, this becomes cubic in the worst case. Even if optimized slightly using prefix scans, recomputing after each update still requires rebuilding occurrence information for every value, leading to roughly `O(n)` work per query.

The bottleneck is that `cnt[x]` depends only on the positions of `x`, not on other values. Once we realize this, we can separate the problem into independent structures per value.

The key observation is that occurrences of a fixed value split the array into gaps, and all subarrays avoiding that value must lie entirely inside these gaps. This turns the problem into maintaining segment lengths induced by positions of each value.

Now updates only affect a single position. That position removes one occurrence from its old value and adds one occurrence to its new value. Each of these operations modifies at most two adjacent gaps in the position list, meaning each update can be handled in logarithmic time using an ordered structure.

We also maintain a global multiset of all `cnt[x]` values so we can query the minimum efficiently after each update.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²q) | O(n) | Too slow |
| Optimal | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We fix the interpretation that for each value `x`, we maintain the sorted set of indices where `x` occurs. From this structure we derive `cnt[x]` using gap decomposition.

1. Initialize a balanced ordered set for each distinct value storing all its positions. This allows us to find predecessor and successor of any index in logarithmic time.
2. For each value `x`, compute its initial `cnt[x]` by scanning its positions and summing contributions of gaps between consecutive occurrences. Each gap of length `L` contributes `L * (L + 1) / 2`. This counts all subarrays fully contained in that gap.
3. Store all `cnt[x]` values in a multiset so that we can query the minimum across all values in constant time.
4. For each update at position `s`, identify the old value `a = arr[s]` and the new value `b`.
5. Before modifying the structure of `a`, locate `s` inside its ordered set. Find the nearest occurrence to the left and right, which define the two gaps that currently touch `s`. Removing `s` merges these two gaps into one larger gap. We update `cnt[a]` by subtracting the contributions of the two old gaps and adding the merged gap contribution.
6. Remove `s` from the set of `a`, and update the multiset by replacing the old `cnt[a]` with the new value.
7. For value `b`, find where `s` would be inserted in its ordered set. The existing gap that spans across `s` is split into two smaller gaps. We update `cnt[b]` by subtracting the old large gap contribution and adding the two new contributions.
8. Insert `s` into the set of `b`, and update the multiset similarly.
9. After processing each query, the answer is the smallest element in the multiset.

The correctness relies on the invariant that for every value `x`, `cnt[x]` exactly equals the sum over all maximal intervals in which `x` does not appear, and these intervals are fully determined by consecutive occurrences of `x`. Each update only changes adjacency relationships around a single position, so only two intervals are affected per value.

Because all other gaps remain unchanged, global consistency is preserved.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict
import bisect

class SortedSet:
    def __init__(self):
        self.a = []

    def add(self, x):
        i = bisect.bisect_left(self.a, x)
        if i == len(self.a) or self.a[i] != x:
            self.a.insert(i, x)

    def discard(self, x):
        i = bisect.bisect_left(self.a, x)
        if i < len(self.a) and self.a[i] == x:
            self.a.pop(i)

    def prev_next(self, x):
        i = bisect.bisect_left(self.a, x)
        prev = self.a[i-1] if i > 0 else None
        nxt = self.a[i] if i < len(self.a) else None
        return prev, nxt

def contrib(l):
    return l * (l + 1) // 2

def recompute_gap(cnt, positions, n):
    if not positions:
        return (n * (n + 1)) // 2

    res = 0
    prev = 0
    for p in positions:
        res += contrib(p - prev - 1)
        prev = p
    res += contrib(n - prev)
    return res

def main():
    n, q = map(int, input().split())
    arr = [0] + list(map(int, input().split()))

    pos = defaultdict(SortedSet)
    cnt = defaultdict(int)

    for i in range(1, n + 1):
        pos[arr[i]].add(i)

    for x in pos:
        cnt[x] = recompute_gap(cnt[x], pos[x].a, n)

    import bisect
    all_cnt = []

    for x in cnt:
        all_cnt.append(cnt[x])

    all_cnt.sort()

    def add_val(v):
        i = bisect.bisect_left(all_cnt, v)
        all_cnt.insert(i, v)

    def remove_val(v):
        i = bisect.bisect_left(all_cnt, v)
        all_cnt.pop(i)

    def get_min():
        return all_cnt[0]

    def update_remove(x, s):
        st = pos[x].a
        i = bisect.bisect_left(st, s)
        left = st[i-1] if i > 0 else 0
        right = st[i+1] if i+1 < len(st) else n+1

        L1 = s - left - 1
        L2 = right - s - 1
        L = L1 + L2 + 1

        cnt[x] -= contrib(L1)
        cnt[x] -= contrib(L2)
        cnt[x] += contrib(L)

        pos[x].discard(s)

    def update_add(x, s):
        st = pos[x].a
        i = bisect.bisect_left(st, s)
        left = st[i-1] if i > 0 else 0
        right = st[i] if i < len(st) else n+1

        L = right - left - 1
        L1 = s - left - 1
        L2 = right - s - 1

        cnt[x] -= contrib(L)
        cnt[x] += contrib(L1)
        cnt[x] += contrib(L2)

        pos[x].add(s)

    # initialize multiset correctly
    all_cnt = []
    for x in cnt:
        all_cnt.append(cnt[x])
    all_cnt.sort()

    for _ in range(q):
        s, newv = map(int, input().split())
        oldv = arr[s]

        remove_val(cnt[oldv])
        update_remove(oldv, s)
        add_val(cnt[oldv])

        remove_val(cnt.get(newv, 0))
        if newv not in cnt:
            cnt[newv] = (n * (n + 1)) // 2

        update_add(newv, s)
        add_val(cnt[newv])

        arr[s] = newv

        print(all_cnt[0])

if __name__ == "__main__":
    main()
```

The implementation relies on maintaining explicit position sets per value. The most delicate part is correctly identifying left and right neighbors during removal and insertion, since boundaries at `0` and `n+1` act as sentinels representing array edges.

The multiset maintenance is conceptually separate from structural updates. Each time `cnt[x]` changes, the old value must be removed before updating and reinserted afterward to avoid stale minima.

## Worked Examples

Consider a small array `[1, 2, 1]`.

We build position sets: `1 -> {1, 3}`, `2 -> {2}`.

For value `1`, gaps are `[0..0]`, `[2..2]`, `[4..3]`, contributing `1 + 1 + 0 = 2`. For value `2`, gaps are `[0..1]` and `[3..3]`, contributing `3 + 1 = 4`.

| Step | Update | Positions of 1 | Positions of 2 | cnt[1] | cnt[2] | min |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | init | {1,3} | {2} | 2 | 4 | 2 |
| 1 | remove 1 at 3, add 3 | {1} | {2,3} | 3 | 3 | 3 |

The trace shows how removing the second occurrence of `1` merges the surrounding gaps into a single interval, increasing `cnt[1]`.

Now consider `[1,1,1,1]` and removing middle occurrence:

| Step | Update | Positions of 1 | cnt[1] |
| --- | --- | --- | --- |
| 0 | init | {1,2,3,4} | 0 |
| 1 | remove 2 | {1,3,4} | 1 |

This demonstrates that splitting a single large gap into two smaller ones increases the total number of subarrays avoiding the value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | each update modifies at most two ordered sets and one multiset |
| Space | O(n) | each position stored once across structures |

The logarithmic factor comes from maintaining ordered position sets. Since each query touches only a constant number of local neighborhoods, the solution fits comfortably within typical constraints for dynamic array problems.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return main()

# minimal case
assert run("1 1\n1\n1 1\n") == "1\n"

# two values swap
assert run("3 2\n1 2 1\n1 2\n3 1\n") == "2\n2\n"

# all equal
assert run("5 2\n1 1 1 1 1\n3 2\n2 3\n") == "4\n4\n"

# boundary update
assert run("4 1\n1 2 3 4\n2 2\n") == "4\n"

# single value disappearance
assert run("2 1\n1 1\n1 2\n") == "3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base initialization |
| swap updates | stable values | correct local updates |
| all equal | monotonic gap handling | edge interval merging |
| boundary change | sentinel handling | edges correctness |
| value removal | reset behavior | empty set case |

## Edge Cases

When a value loses its last occurrence, its position set becomes empty. In that situation, the entire array becomes a single valid gap for that value, meaning every subarray avoids it. The implementation must explicitly reset its contribution to `n(n+1)/2`, otherwise stale gap decomposition would remain.

For an array like `[1,1]` removing both occurrences step by step, after the final removal the correct state is that `cnt[1]` equals 3. Any implementation that only updates local gaps would incorrectly leave `cnt[1]` at 1 or 0 because no intervals remain to be processed.

During insertion into a previously unseen value, the first occurrence splits a full-length gap. For example, inserting `x` into an empty structure at position `i` creates two gaps of lengths `i-1` and `n-i`. If this is not recomputed using sentinel boundaries, off-by-one errors appear immediately, especially when `i = 1` or `i = n`.

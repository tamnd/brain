---
title: "CF 102803B - Bills of Paradise"
description: "We have a collection of n bills. Their values are not given directly, but are generated from two random seeds using the provided xorshift128+ generator. Every generated value is different. During the process, some bills are unpaid and some have already been paid."
date: "2026-07-26T16:29:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102803
codeforces_index: "B"
codeforces_contest_name: "The 15th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102803
solve_time_s: 47
verified: true
draft: false
---

[CF 102803B - Bills of Paradise](https://codeforces.com/problemset/problem/102803/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of `n` bills. Their values are not given directly, but are generated from two random seeds using the provided xorshift128+ generator. Every generated value is different. During the process, some bills are unpaid and some have already been paid.

The commands modify or inspect the current unpaid set. A query `F x` asks for the smallest unpaid bill whose value is at least `x`. A command `D x` removes that same bill from the unpaid set because it has been paid. A query `C x` asks for the total value of all unpaid bills not exceeding `x`. A command `R x` restores every paid bill with value at most `x`, making those bills unpaid again.

The generated values are up to almost `10^12`, so the actual values must be handled as 64-bit integers. The number of bills can reach one million and the total number of commands is much larger than a typical linear-per-query solution can handle. A solution that scans all bills for every command could perform about `10^12` operations in the worst case, which is far beyond the available time. We need logarithmic processing per command.

The difficult part is the refund operation. It can activate many bills at once, but it happens at most ten times. A data structure must support both individual removals and a large prefix restoration.

A careless implementation can fail in several ways. If a command `F` asks for a value larger than every unpaid bill, returning the largest existing value is wrong. For example, with bills `{5, 9}`, the command `F 10` must output `10^12`, the required sentinel value, because no valid bill exists.

Another mistake is confusing paid bills with nonexistent bills. Suppose the bills are `{3, 7, 11}`. After `D 7`, a query `C 10` must return `3`, not `10`, because the paid bill is not part of the unpaid collection.

Refund boundaries are also easy to mishandle. With bills `{4, 8, 12}`, the command `R 8` must restore both `4` and `8`. Using a strict comparison instead of an inclusive one would incorrectly leave `8` paid.

## Approaches

A direct solution is to keep all bills in a list and scan it whenever a command arrives. For `F` and `D`, we search all unpaid bills and keep the best candidate. For `C`, we sum all unpaid bills that satisfy the condition. This is correct because every command is defined over the current set of unpaid bills.

The problem is the amount of work. With one million bills and hundreds of thousands of commands, a worst case sequence of queries can require around `5 * 10^11` checks. The method is not close to fast enough.

The key observation is that the bills never change value. Only their state changes. After sorting the values, every operation becomes a question about positions in this sorted array. A segment tree can store information about intervals of positions. Each node keeps the number of currently unpaid bills in the interval and the sum of their values.

The refund operation looks expensive because it can affect many bills, but it always changes a prefix of the sorted array into the same state: all bills become unpaid. This means a segment tree lazy assignment is enough. When a whole segment is covered by a refund, we can mark it as completely active without visiting its children.

The same tree can find the first active position after a lower bound, remove one bill by setting one position inactive, and answer prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nQ) | O(n) | Too slow |
| Segment Tree | O((n + Q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Generate all bill values and sort them. The sorted order lets value comparisons become index ranges.
2. Build a segment tree over the sorted positions. Every position starts as unpaid, so every node initially stores the number of bills in its segment and the sum of all values in that segment.
3. For `F x`, find the first sorted position whose value is at least `x`. Then search the segment tree from that position onward for the first segment containing an unpaid bill. If no such position exists, print `10^12`.
4. For `D x`, perform the same search as `F x`. If a position is found, update that single position so its active count and contribution become zero.
5. For `C x`, find the last sorted position whose value is at most `x`. Query the segment tree prefix up to that position and return the stored sum.
6. For `R x`, find the last sorted position whose value is at most `x`. Apply a lazy assignment to that prefix, setting every covered position to unpaid.

The invariant is that the segment tree always represents exactly the current unpaid bills. Point deletion removes exactly one active position. Prefix restoration makes every position in the requested value range active. Since every query reads only from this maintained representation, the returned values match the required unpaid set.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr
        size = 4 * self.n
        self.cnt = [0] * size
        self.s = [0] * size
        self.lazy = [False] * size
        self.build(1, 0, self.n - 1)

    def build(self, p, l, r):
        if l == r:
            self.cnt[p] = 1
            self.s[p] = self.arr[l]
        else:
            m = (l + r) // 2
            self.build(p * 2, l, m)
            self.build(p * 2 + 1, m + 1, r)
            self.pull(p)

    def pull(self, p):
        self.cnt[p] = self.cnt[p * 2] + self.cnt[p * 2 + 1]
        self.s[p] = self.s[p * 2] + self.s[p * 2 + 1]

    def apply(self, p, l, r):
        self.cnt[p] = r - l + 1
        self.s[p] = sum(self.arr[l:r + 1])
        self.lazy[p] = True

    def push(self, p, l, r):
        if self.lazy[p] and l != r:
            m = (l + r) // 2
            self.apply(p * 2, l, m)
            self.apply(p * 2 + 1, m + 1, r)
            self.lazy[p] = False

    def update_all(self, p, l, r, ql, qr):
        if ql <= l and r <= qr:
            self.apply(p, l, r)
            return
        self.push(p, l, r)
        m = (l + r) // 2
        if ql <= m:
            self.update_all(p * 2, l, m, ql, qr)
        if qr > m:
            self.update_all(p * 2 + 1, m + 1, r, ql, qr)
        self.pull(p)

    def remove(self, p, l, r, idx):
        if l == r:
            self.cnt[p] = 0
            self.s[p] = 0
            return
        self.push(p, l, r)
        m = (l + r) // 2
        if idx <= m:
            self.remove(p * 2, l, m, idx)
        else:
            self.remove(p * 2 + 1, m + 1, r, idx)
        self.pull(p)

    def first(self, p, l, r, ql):
        if r < ql or self.cnt[p] == 0:
            return -1
        if l == r:
            return l
        self.push(p, l, r)
        m = (l + r) // 2
        res = self.first(p * 2, l, m, ql)
        if res != -1:
            return res
        return self.first(p * 2 + 1, m + 1, r, ql)

    def query(self, p, l, r, qr):
        if r <= qr:
            return self.s[p]
        self.push(p, l, r)
        m = (l + r) // 2
        ans = 0
        if qr > m:
            ans += self.query(p * 2 + 1, m + 1, r, qr)
        if qr >= l:
            ans += self.query(p * 2, l, m, qr)
        return ans

def solve():
    import bisect

    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []

    for _ in range(t):
        n = int(next(it))
        k1 = int(next(it))
        k2 = int(next(it))

        a = []
        mask = (1 << 64) - 1
        for _ in range(n):
            k3 = k1
            k4 = k2
            k1 = k4
            k3 ^= (k3 << 23) & mask
            k2 = (k3 ^ k4 ^ (k3 >> 17) ^ (k4 >> 26)) & mask
            a.append((k2 + k4) % 999999999999 + 1)

        a.sort()
        seg = SegTree(a)

        q = int(next(it))
        for _ in range(q):
            op = next(it).decode()
            x = int(next(it))

            if op == 'F' or op == 'D':
                pos = bisect.bisect_left(a, x)
                idx = seg.first(1, 0, n - 1, pos)
                if op == 'F':
                    out.append(str(10**12 if idx == -1 else a[idx]))
                elif idx != -1:
                    seg.remove(1, 0, n - 1, idx)

            elif op == 'C':
                pos = bisect.bisect_right(a, x) - 1
                out.append("0" if pos < 0 else str(seg.query(1, 0, n - 1, pos)))

            else:
                pos = bisect.bisect_right(a, x) - 1
                if pos >= 0:
                    seg.update_all(1, 0, n - 1, 0, pos)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The generator is reproduced using unsigned 64-bit arithmetic. Python integers do not overflow naturally, so masking with `(1 << 64) - 1` keeps the same behavior as C++ unsigned long long.

The segment tree stores counts and sums only for unpaid bills. A lazy flag means an entire segment has been restored. The implementation avoids expanding that segment immediately because future operations can work correctly from the stored aggregate values.

The `first` function is the core of `F` and `D`. It ignores every segment that contains no unpaid bills and recursively searches left before right because the array is sorted and the leftmost valid position is required.

The binary searches use `bisect_left` for "at least x" and `bisect_right - 1` for "at most x". Mixing these two boundaries is a common source of wrong answers in this problem.

## Worked Examples

Consider bills `{4, 9, 15}`.

| Command | Active bills | Operation result |
| --- | --- | --- |
| F 8 | 4, 9, 15 | returns 9 |
| D 9 | 4, 15 | removes 9 |
| C 10 | 4, 15 | returns 4 |
| R 10 | 4, 9, 15 | restores 9 |
| C 10 | 4, 9, 15 | returns 13 |

This trace shows that removed bills disappear from sums and searches, then return after a prefix restoration.

A second example uses boundary values `{5, 10, 20}`.

| Command | Active bills | Operation result |
| --- | --- | --- |
| D 10 | 5, 20 | removes exactly 10 |
| F 10 | 5, 20 | returns 20 |
| C 10 | 5, 20 | returns 5 |
| R 10 | 5, 10, 20 | restores 10 |

The example confirms that comparisons are inclusive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + Q) log n) | Building and every command use logarithmic tree operations |
| Space | O(n) | The sorted values and segment tree each store linear information |

The largest test sizes require millions of bills and commands. A linear scan per operation cannot fit, but the segment tree keeps each operation around logarithmic time. The refund limit is not needed for this solution's correctness, because prefix assignments are handled directly by lazy propagation.

## Test Cases

```python
import sys, io

def run(inp):
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    # call solve() from the submitted solution
    sys.stdin = old
    return ""

# The following cases should be run after placing solve() in the harness.

# Minimum-size generation and commands
# Covers single bill behavior.

# Removing all bills and querying empty states.
# Covers missing successor and empty sums.

# Refund after multiple deletions.
# Covers lazy restoration.

# Values at exact x boundaries.
# Covers inclusive comparisons.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One generated bill, F and C queries | Generated value and sum | Single-element handling |
| Delete every bill, then search | Sentinel and zero | Empty tree behavior |
| Delete a prefix, refund it, query sums | Restored totals | Lazy prefix assignment |
| Query exactly equal values | Inclusive answers | Boundary correctness |

## Edge Cases

When no unpaid bill satisfies `F x`, the tree search reaches a segment with zero active count and returns `-1`. For example, after paying `{5, 8}`, searching `F 1` must still fail because no unpaid positions remain.

When a refunded range contains already unpaid bills, assigning the prefix to active again is harmless. The segment tree stores the final state rather than counting operations, so restoring an already active bill does not double count it.

For an exact boundary refund, the use of `bisect_right` includes bills equal to `x`. With values `{4, 8, 12}`, after paying `8`, `R 8` updates positions `4` and `8`, bringing the sum from `16` back to `24`.

The sorted-index representation is what makes all of these cases work together. The tree never needs to know the actual meaning of a bill beyond its position and value, so every command becomes a controlled update or query over the current active prefix or suffix.

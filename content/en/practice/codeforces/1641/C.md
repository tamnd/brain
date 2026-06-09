---
title: "CF 1641C - Anonymity Is Important"
description: "We have a line of n people. Every person is either sick or healthy. As information arrives, we receive two kinds of statements. A statement with x = 0 says that nobody in the interval [l, r] is sick. Every person in that range becomes definitely healthy."
date: "2026-06-10T04:21:22+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "dsu", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1641
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 773 (Div. 1)"
rating: 2200
weight: 1641
solve_time_s: 122
verified: true
draft: false
---

[CF 1641C - Anonymity Is Important](https://codeforces.com/problemset/problem/1641/C)

**Rating:** 2200  
**Tags:** binary search, brute force, data structures, dsu, greedy, sortings  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of `n` people. Every person is either sick or healthy.

As information arrives, we receive two kinds of statements.

A statement with `x = 0` says that nobody in the interval `[l, r]` is sick. Every person in that range becomes definitely healthy.

A statement with `x = 1` says that there is at least one sick person somewhere inside `[l, r]`. This does not identify who is sick, it only guarantees that the interval contains at least one sick person.

Intermixed with those statements are queries asking about a single position `j`. We must answer:

`NO` if person `j` is definitely healthy.

`YES` if person `j` is definitely sick.

`N/A` if both possibilities are still consistent with all information seen so far.

The constraints are the real challenge. Both `n` and `q` are as large as `2 · 10^5`. Any solution that scans an interval during updates or scans all stored constraints during a query immediately becomes too slow. A quadratic approach would perform on the order of `4 · 10^10` operations.

The tricky cases come from the interaction between positive and negative information.

Suppose we know:

```
0 1 2 0
0 1 3 1
```

The first statement makes positions `1` and `2` healthy. The second statement says there is a sick person in `[1,3]`. Since only position `3` remains possible, the answer for position `3` is `YES`.

A naive solution that only stores the interval `[1,3]` and never incorporates later eliminations would miss this deduction.

Another subtle case is nested positive intervals.

```
[2,10] contains a sick person
[4,6] contains a sick person
```

The second statement is strictly stronger. Once we know `[4,6]` contains a sick person, the larger interval contributes nothing new. Keeping both intervals only creates redundant work.

That observation is the key to the accepted solution.

## Approaches

The brute force idea is straightforward.

Maintain the status of every person. For every statement with `x = 0`, mark the whole interval healthy. For every statement with `x = 1`, store the interval. When asked about position `j`, inspect all stored intervals and check whether the accumulated information forces `j` to be sick.

This is correct because it directly models the constraints, but it becomes hopelessly slow. With `2 · 10^5` operations and intervals of length `2 · 10^5`, the worst case reaches tens of billions of operations.

The crucial observation is that healthy people are the only positions that ever become permanently known. Once a person is proven healthy, they can be removed from consideration forever.

Imagine maintaining the set of people whose status is still unknown.

For a positive statement `[l, r]`, all we really care about is that among the currently unknown positions in that interval, at least one must eventually be sick.

Now consider two positive intervals where one contains the other.

If `[4,6]` already guarantees a sick person, then `[2,10]` adds no new information. Any assignment satisfying the smaller interval automatically satisfies the larger one.

So we only need to keep minimal positive intervals under containment.

When a query asks about position `j`, let:

`L` = previous unknown position before `j`

`R` = next unknown position after `j`

Then `(L, R)` contains exactly one unknown person, namely `j`.

If there exists a stored positive interval entirely inside `(L, R)` and containing `j`, that interval has only one remaining candidate. The required sick person must be `j`.

That transforms the problem into maintaining:

A dynamic set of still-unknown positions.

A collection of non-redundant positive intervals ordered by their left endpoint.

Both can be handled in logarithmic time.

The accepted solution uses a DSU-like "next alive" structure to delete healthy positions efficiently and an ordered map of minimal positive intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n + q) | Too slow |
| Optimal | O((n + q) log n) | O(n + q) | Accepted |

## Algorithm Walkthrough

1. Maintain the set of positions whose status is still unknown.

Initially every position belongs to this set.
2. For a statement `[l, r]` with `x = 0`, remove every position in that interval from the unknown set.

Those people are now definitely healthy.
3. Use a DSU "next pointer" structure to skip already removed positions.

Each position is deleted at most once, so all removals are nearly linear overall.
4. For a statement `[l, r]` with `x = 1`, insert the interval into an ordered map of positive constraints.
5. If an existing stored interval is completely contained in `[l, r]`, the new interval is redundant and can be ignored.

The smaller interval is strictly stronger.
6. Otherwise insert `[l, r]` and remove any previously stored intervals that contain it.

After this step, no stored interval contains another.
7. For a query on position `j`, first check whether `j` still belongs to the unknown set.

If not, answer `NO`.
8. Let `L` be the previous unknown position and `R` the next unknown position.

Since unknown positions are stored in order, these neighbors can be found in logarithmic time.
9. Search for the first stored interval whose left endpoint is greater than `L`.
10. If such an interval starts at or before `j` and ends before `R`, answer `YES`.

That interval lies entirely inside the block whose only unknown position is `j`, so its required sick person must be `j`.
11. Otherwise answer `N/A`.

### Why it works

The unknown set always contains exactly the positions that have not been proven healthy.

The interval structure stores only minimal positive constraints. Removing a larger interval that contains a smaller one never changes the set of valid assignments, because satisfying the smaller interval automatically satisfies the larger interval.

For a queried position `j`, the neighbors `L` and `R` delimit the maximal segment whose only unknown position is `j`. Every other position inside that segment is already known healthy.

If a positive interval lies completely inside `(L, R)` and contains `j`, then that interval has exactly one possible sick candidate left. Hence `j` must be sick.

If no such interval exists, we can always construct a valid assignment where `j` is healthy, so the information is insufficient to force sickness.

Those two facts exactly match the required answers.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right
import random

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        n = self.n
        while idx <= n:
            self.bit[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

    def kth(self, k):
        idx = 0
        bitmask = 1 << (self.n.bit_length())
        while bitmask:
            nxt = idx + bitmask
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                idx = nxt
            bitmask >>= 1
        return idx + 1

class DSU:
    def __init__(self, n):
        self.p = list(range(n + 3))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def erase(self, x):
        self.p[x] = self.find(x + 1)

class Node:
    __slots__ = ("l", "r", "prio", "left", "right")

    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.prio = random.randint(1, 1 << 30)
        self.left = None
        self.right = None

def split(root, key):
    if not root:
        return (None, None)
    if root.l < key:
        a, b = split(root.right, key)
        root.right = a
        return (root, b)
    a, b = split(root.left, key)
    root.left = b
    return (a, root)

def merge(a, b):
    if not a or not b:
        return a or b
    if a.prio > b.prio:
        a.right = merge(a.right, b)
        return a
    b.left = merge(a, b.left)
    return b

def insert(root, node):
    if not root:
        return node
    if node.prio > root.prio:
        node.left, node.right = split(root, node.l)
        return node
    if node.l < root.l:
        root.left = insert(root.left, node)
    else:
        root.right = insert(root.right, node)
    return root

def lower_bound(root, key):
    ans = None
    while root:
        if root.l >= key:
            ans = root
            root = root.left
        else:
            root = root.right
    return ans

def predecessor(root, key):
    ans = None
    while root:
        if root.l < key:
            ans = root
            root = root.right
        else:
            root = root.left
    return ans

def erase_key(root, key):
    if not root:
        return None
    if root.l == key:
        return merge(root.left, root.right)
    if key < root.l:
        root.left = erase_key(root.left, key)
    else:
        root.right = erase_key(root.right, key)
    return root

n, q = map(int, input().split())

fw = Fenwick(n + 2)
for i in range(n + 2):
    fw.add(i + 1, 1)

alive = [True] * (n + 2)

dsu = DSU(n + 2)
root = None

out = []

for _ in range(q):
    data = list(map(int, input().split()))

    if data[0] == 0:
        l, r, x = data[1], data[2], data[3]

        if x == 0:
            p = dsu.find(l)
            while p <= r:
                if alive[p]:
                    alive[p] = False
                    fw.add(p + 1, -1)
                dsu.erase(p)
                p = dsu.find(p)

        else:
            cur = lower_bound(root, l)

            if cur and cur.r <= r:
                continue

            root = insert(root, Node(l, r))

            while True:
                prv = predecessor(root, l)
                if prv is None or prv.r < r:
                    break
                root = erase_key(root, prv.l)

    else:
        j = data[1]

        if not alive[j]:
            out.append("NO")
            continue

        rank = fw.sum(j + 1)

        left_pos = fw.kth(rank - 1) - 1
        right_pos = fw.kth(rank + 1) - 1

        cur = lower_bound(root, left_pos + 1)

        if cur and cur.l <= j and cur.r < right_pos:
            out.append("YES")
        else:
            out.append("N/A")

sys.stdout.write("\n".join(out))
```

The DSU is responsible only for interval deletions. Once a position becomes healthy, it never returns, so every index is removed at most once.

The Fenwick tree maintains the ordered set of unknown positions. It lets us find the predecessor and successor of a queried position through order statistics.

The treap stores the minimal positive intervals ordered by their left endpoint. Insertions remove larger redundant intervals, preserving the invariant that no stored interval contains another.

The query logic follows the proof directly. If an interval is trapped inside the gap whose only unknown position is `j`, then `j` must be the sick person required by that interval.

## Worked Examples

### Sample 1

Input:

```
6 9
0 4 5 0
1 5
1 6
0 4 6 1
1 6
0 2 5 1
0 2 2 0
1 3
1 2
```

| Operation | Unknown Positions | Stored Positive Intervals | Answer |
| --- | --- | --- | --- |
| 0 4 5 0 | {1,2,3,6} | {} |  |
| 1 5 | {1,2,3,6} | {} | NO |
| 1 6 | {1,2,3,6} | {} | N/A |
| 0 4 6 1 | {1,2,3,6} | {[4,6]} |  |
| 1 6 | {1,2,3,6} | {[4,6]} | YES |
| 0 2 5 1 | {1,2,3,6} | {[2,5]} |  |
| 0 2 2 0 | {1,3,6} | {[2,5]} |  |
| 1 3 | {1,3,6} | {[2,5]} | YES |
| 1 2 | {1,3,6} | {[2,5]} | NO |

The key moment is after position `2` becomes healthy. The interval `[2,5]` still needs a sick person, and position `3` is the only remaining candidate inside that region.

### Custom Example

```
5 4
0 1 5 1
1 3
0 1 4 0
1 5
```

| Operation | Unknown Positions | Stored Positive Intervals | Answer |
| --- | --- | --- | --- |
| 0 1 5 1 | {1,2,3,4,5} | {[1,5]} |  |
| 1 3 | {1,2,3,4,5} | {[1,5]} | N/A |
| 0 1 4 0 | {5} | {[1,5]} |  |
| 1 5 | {5} | {[1,5]} | YES |

Initially any position could satisfy the positive interval. After positions `1..4` become healthy, only position `5` remains.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each deletion happens once, every tree operation is logarithmic |
| Space | O(n + q) | DSU, Fenwick tree, and stored intervals |

With `n, q ≤ 2 · 10^5`, logarithmic updates and queries easily fit inside the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    # call solve() here in a real test harness
    pass

# sample 1
assert run(
"""6 9
0 4 5 0
1 5
1 6
0 4 6 1
1 6
0 2 5 1
0 2 2 0
1 3
1 2
"""
) == """NO
N/A
YES
YES
NO"""

# minimum size
assert run(
"""1 2
1 1
1 1
"""
) == """N/A
N/A"""

# single forced sick person
assert run(
"""3 3
0 1 2 0
0 1 3 1
1 3
"""
) == "YES"

# everybody healthy
assert run(
"""4 3
0 1 4 0
1 1
1 4
"""
) == """NO
NO"""

# boundary positions
assert run(
"""5 4
0 2 4 0
0 1 5 1
1 1
1 5
"""
) == """N/A
N/A"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum-size case | N/A | No information available |
| Forced survivor | YES | Positive interval collapses to one candidate |
| All healthy | NO | Range deletion logic |
| Boundary positions | N/A | Predecessor/successor handling near ends |

## Edge Cases

Consider:

```
3 3
0 1 2 0
0 1 3 1
1 3
```

After the first statement, positions `1` and `2` are removed from the unknown set. The interval `[1,3]` still requires a sick person. The only remaining candidate is `3`, so the algorithm finds that the interval lies entirely inside the gap whose sole unknown position is `3` and answers `YES`.

Now consider nested intervals:

```
5 3
0 1 5 1
0 2 4 1
1 3
```

The interval `[2,4]` is stronger than `[1,5]`. The algorithm keeps only the minimal interval. Removing the larger interval does not change any valid assignment, which is exactly why the containment pruning is correct.

Finally, consider:

```
4 2
0 1 4 0
1 2
```

Position `2` is removed immediately when the healthy interval arrives. The query never even examines positive constraints and directly answers `NO`, which is the only possible result.

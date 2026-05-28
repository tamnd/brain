---
title: "CF 121E - Lucky Array"
description: "We have an array whose values are always at most 10000. Two operations must be processed online. The first operation adds a value d to every element inside a segment [l, r]."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 121
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 91 (Div. 1 Only)"
rating: 2400
weight: 121
solve_time_s: 141
verified: true
draft: false
---

[CF 121E - Lucky Array](https://codeforces.com/problemset/problem/121/E)

**Rating:** 2400  
**Tags:** data structures  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array whose values are always at most `10000`. Two operations must be processed online.

The first operation adds a value `d` to every element inside a segment `[l, r]`.

The second operation asks how many numbers inside `[l, r]` are lucky, where a lucky number is composed only of digits `4` and `7`.

The difficulty is not recognizing lucky numbers. There are very few of them below `10000`. The real challenge is supporting up to `10^5` range additions and `10^5` range queries fast enough.

A direct simulation immediately runs into trouble. Suppose every operation updates almost the whole array. Recomputing the affected values one by one costs `O(n)` per update. With `10^5` operations and `10^5` elements, this becomes roughly `10^10` updates, far beyond the limit.

The bound that every value always stays at most `10000` is the crucial structural property. There are only `2 + 4 + 8 + 16 = 30` lucky numbers in this range. Instead of tracking exact values expensively, we can track how far each value is from becoming lucky.

Several edge cases make naive optimizations fail.

Consider this input:

```
3 2
3 4 5
add 1 3 1
count 1 3
```

After the addition the array becomes `[4,5,6]`, so the answer is `1`. Any implementation that only updates previously lucky positions would miss that `3` became lucky.

Another subtle case:

```
3 3
4 7 44
add 1 3 1
add 1 3 1
count 1 3
```

The array evolves as `[5,8,45]` then `[6,9,46]`. The correct answer is `0`. A lazy structure that stores only whether a position is currently lucky, without recalculating transitions, will incorrectly keep stale lucky counts.

A third important situation appears when a segment receives many lazy additions:

```
5 3
1 2 3 4 5
add 1 5 100
add 1 5 200
count 1 5
```

The final array is `[301,302,303,304,305]`, and only `304` is lucky? No, it is not, because lucky numbers contain only digits `4` and `7`. The correct answer is `0`. This catches implementations that accidentally interpret “contains 4 or 7” instead of “all digits are 4 or 7”.

## Approaches

The brute force solution is straightforward. For every `add` operation, iterate through the entire interval and update each element. For every `count` operation, iterate again and test each number individually.

Checking whether a number is lucky takes at most four digit inspections because values never exceed `10000`. So the expensive part is scanning intervals repeatedly.

In the worst case, every operation touches the whole array. That gives `10^5 × 10^5 = 10^10` element updates or checks. Even in C++ this is hopeless under a 4 second limit.

The key observation is that the set of lucky numbers is tiny. There are only 30 lucky numbers up to `10000`.

For a value `x`, what matters is not the exact number itself, but the distance to the next lucky number. Suppose the next lucky number at or above `x` is `L`. Define:

```
delta = L - x
```

If `delta == 0`, the number is currently lucky.

Now consider adding `d` to the entire segment. The value becomes `x + d`, so the new distance becomes:

```
L - (x + d) = delta - d
```

A range addition simply subtracts `d` from all deltas.

This transforms the problem into something segment trees handle very naturally.

For every segment tree node we maintain:

```
mn = minimum delta in this segment
cnt = how many positions have delta == 0
```

When we apply a lazy addition, all deltas shift uniformly, so `mn` also shifts uniformly.

The crucial trick is this:

If after subtracting `d`, the node still has `mn > 0`, then no element in the segment became lucky. We can stop immediately without descending further.

We only push deeper when some delta becomes non-positive. Since every element can cross a lucky threshold only about 30 times total, the total number of expensive descents remains manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nm)` | `O(n)` | Too slow |
| Optimal | `O((n + m) log n log C)` amortized | `O(n)` | Accepted |

Here `C` is the maximum value bound, around `10000`.

## Algorithm Walkthrough

1. Precompute all lucky numbers up to `10000`.

A DFS or BFS over digits `4` and `7` generates only 30 numbers, so this step is trivial.
2. For every initial array value `a[i]`, compute the next lucky number `L >= a[i]`.

Store:

```
delta[i] = L - a[i]
```

If `delta[i] == 0`, then `a[i]` is already lucky.
3. Build a segment tree.

Each node stores:

```
mn  = minimum delta in the segment
cnt = number of zeros in the segment
lazy = pending subtraction applied to all deltas
```

A leaf with `delta == 0` has `cnt = 1`, otherwise `cnt = 0`.
4. For a `count l r` query, return the sum of `cnt` values over the requested interval.

A position contributes exactly when its delta is zero.
5. For an `add l r d` operation, subtract `d` from all deltas inside the interval.

Conceptually, every value moved `d` closer to its next lucky number.
6. When updating a segment tree node fully covered by the update, decrease:

```
mn -= d
lazy -= d
```

If afterward `mn > 0`, then every delta is still positive, so no element became lucky. The node remains valid.
7. If `mn <= 0`, at least one element crossed a lucky boundary.

We must descend recursively to recompute the affected leaves.
8. At a leaf, when `delta <= 0`, the current value has reached or passed its tracked lucky number.

We update the actual array value, recompute the next lucky number, and rebuild the leaf state.
9. After recursive updates, merge children upward:

```
mn = min(left.mn, right.mn)
cnt = left.cnt + right.cnt
```

### Why it works

Each leaf always stores the distance from its current value to the next lucky number greater than or equal to it.

A range addition decreases these distances uniformly. If all distances stay positive, then no value became lucky and no recomputation is needed.

Whenever a distance becomes non-positive, that position has crossed a lucky threshold. Recomputing the next lucky number restores the invariant.

Because every value crosses at most one lucky number at a time and there are only 30 lucky numbers below `10000`, each element is rebuilt only a small number of times across the entire execution. The segment tree always maintains correct lucky counts for every interval.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def generate_lucky():
    res = []

    def dfs(x):
        if x > 10000:
            return
        if x:
            res.append(x)
        dfs(x * 10 + 4)
        dfs(x * 10 + 7)

    dfs(0)
    res.sort()
    return res

LUCKY = generate_lucky()

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr[:]

        size = 4 * self.n + 5
        self.mn = [0] * size
        self.cnt = [0] * size
        self.lazy = [0] * size

        self.build(1, 0, self.n - 1)

    def next_delta(self, x):
        idx = bisect_left(LUCKY, x)
        return LUCKY[idx] - x

    def apply(self, node, val):
        self.mn[node] += val
        self.lazy[node] += val

    def push(self, node):
        if self.lazy[node]:
            v = self.lazy[node]
            self.apply(node * 2, v)
            self.apply(node * 2 + 1, v)
            self.lazy[node] = 0

    def pull(self, node):
        self.mn[node] = min(self.mn[node * 2], self.mn[node * 2 + 1])
        self.cnt[node] = self.cnt[node * 2] + self.cnt[node * 2 + 1]

    def build(self, node, l, r):
        if l == r:
            d = self.next_delta(self.arr[l])
            self.mn[node] = d
            self.cnt[node] = 1 if d == 0 else 0
            return

        mid = (l + r) // 2

        self.build(node * 2, l, mid)
        self.build(node * 2 + 1, mid + 1, r)

        self.pull(node)

    def rebuild_leaf(self, node, idx):
        d = self.next_delta(self.arr[idx])
        self.mn[node] = d
        self.cnt[node] = 1 if d == 0 else 0

    def range_add(self, node, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.apply(node, -val)

            if self.mn[node] > 0:
                return

        if l == r:
            self.arr[l] += val
            self.rebuild_leaf(node, l)
            return

        self.push(node)

        mid = (l + r) // 2

        if ql <= mid:
            self.range_add(node * 2, l, mid, ql, qr, val)

        if qr > mid:
            self.range_add(node * 2 + 1, mid + 1, r, ql, qr, val)

        self.pull(node)

    def query(self, node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.cnt[node]

        self.push(node)

        mid = (l + r) // 2
        ans = 0

        if ql <= mid:
            ans += self.query(node * 2, l, mid, ql, qr)

        if qr > mid:
            ans += self.query(node * 2 + 1, mid + 1, r, ql, qr)

        return ans

def solve():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))

    seg = SegTree(arr)

    out = []

    for _ in range(m):
        parts = input().split()

        if parts[0] == "add":
            l = int(parts[1]) - 1
            r = int(parts[2]) - 1
            d = int(parts[3])

            seg.range_add(1, 0, n - 1, l, r, d)

        else:
            l = int(parts[1]) - 1
            r = int(parts[2]) - 1

            out.append(str(seg.query(1, 0, n - 1, l, r)))

    sys.stdout.write("\n".join(out))

solve()
```

The first part generates all lucky numbers up to `10000`. Since the count is tiny, recursive generation is simpler and cleaner than checking every integer individually.

The segment tree never stores actual values except at leaves through `self.arr`. Internal nodes only track the minimum distance to a lucky number and the count of currently lucky positions.

The most subtle detail is the sign convention during updates.

If a value increases by `d`, then its distance to the next lucky number decreases by `d`. That is why updates apply `-d` to `mn` and `lazy`.

Another easy mistake is stopping recursion too early. We may stop only when `mn > 0`. If `mn == 0`, some element is exactly lucky and the node must preserve that information accurately.

At leaves, we rebuild using the actual updated value. We cannot simply keep subtracting deltas forever because once a value passes its tracked lucky number, the “next lucky” changes.

The implementation stores pending lazy values even for nodes that later recurse. This guarantees children always receive the correct accumulated updates before further operations.

## Worked Examples

### Sample 1

Input:

```
3 6
2 3 4
count 1 3
count 1 2
add 1 3 2
count 1 3
add 2 3 3
count 1 3
```

Initial deltas:

| Position | Value | Next Lucky | Delta |
| --- | --- | --- | --- |
| 1 | 2 | 4 | 2 |
| 2 | 3 | 4 | 1 |
| 3 | 4 | 4 | 0 |

First query:

| Query | Lucky positions | Answer |
| --- | --- | --- |
| count 1 3 | {3} | 1 |

Second query:

| Query | Lucky positions | Answer |
| --- | --- | --- |
| count 1 2 | {} | 0 |

After `add 1 3 2`:

| Position | Old Value | New Value | New Delta |
| --- | --- | --- | --- |
| 1 | 2 | 4 | 0 |
| 2 | 3 | 5 | 2 |
| 3 | 4 | 6 | 1 |

Third query:

| Query | Lucky positions | Answer |
| --- | --- | --- |
| count 1 3 | {1} | 1 |

After `add 2 3 3`:

| Position | Old Value | New Value | New Delta |
| --- | --- | --- | --- |
| 1 | 4 | 4 | 0 |
| 2 | 5 | 8 | 36 |
| 3 | 6 | 9 | 35 |

Final query:

| Query | Lucky positions | Answer |
| --- | --- | --- |
| count 1 3 | {1} | 1 |

This trace shows why leaves must be rebuilt after crossing a lucky threshold. Position 2 moved from targeting lucky number `7` to targeting `44`.

### Sample 2

Input:

```
4 3
4 44 5 6
count 1 4
add 3 4 1
count 1 4
```

Initial state:

| Position | Value | Lucky |
| --- | --- | --- |
| 1 | 4 | Yes |
| 2 | 44 | Yes |
| 3 | 5 | No |
| 4 | 6 | No |

First query:

| Query | Answer |
| --- | --- |
| count 1 4 | 2 |

After update:

| Position | Old Value | New Value | Lucky |
| --- | --- | --- | --- |
| 3 | 5 | 6 | No |
| 4 | 6 | 7 | Yes |

Second query:

| Query | Answer |
| --- | --- |
| count 1 4 | 3 |

This example demonstrates that a non-lucky value can become lucky exactly when its delta reaches zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n + m) log n log C)` amortized | Each rebuild descends through the tree, and every element crosses only a small number of lucky thresholds |
| Space | `O(n)` | Segment tree arrays and stored values |

There are only 30 lucky numbers below `10000`, so each position can trigger expensive rebuild logic only a bounded number of times. The amortized complexity easily fits inside the limits for `10^5` operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def generate_lucky():
        res = []

        def dfs(x):
            if x > 10000:
                return
            if x:
                res.append(x)
            dfs(x * 10 + 4)
            dfs(x * 10 + 7)

        dfs(0)
        res.sort()
        return res

    LUCKY = generate_lucky()

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.arr = arr[:]

            size = 4 * self.n + 5
            self.mn = [0] * size
            self.cnt = [0] * size
            self.lazy = [0] * size

            self.build(1, 0, self.n - 1)

        def next_delta(self, x):
            idx = bisect_left(LUCKY, x)
            return LUCKY[idx] - x

        def apply(self, node, val):
            self.mn[node] += val
            self.lazy[node] += val

        def push(self, node):
            if self.lazy[node]:
                v = self.lazy[node]
                self.apply(node * 2, v)
                self.apply(node * 2 + 1, v)
                self.lazy[node] = 0

        def pull(self, node):
            self.mn[node] = min(self.mn[node * 2], self.mn[node * 2 + 1])
            self.cnt[node] = self.cnt[node * 2] + self.cnt[node * 2 + 1]

        def build(self, node, l, r):
            if l == r:
                d = self.next_delta(self.arr[l])
                self.mn[node] = d
                self.cnt[node] = 1 if d == 0 else 0
                return

            mid = (l + r) // 2

            self.build(node * 2, l, mid)
            self.build(node * 2 + 1, mid + 1, r)

            self.pull(node)

        def rebuild_leaf(self, node, idx):
            d = self.next_delta(self.arr[idx])
            self.mn[node] = d
            self.cnt[node] = 1 if d == 0 else 0

        def range_add(self, node, l, r, ql, qr, val):
            if ql <= l and r <= qr:
                self.apply(node, -val)

                if self.mn[node] > 0:
                    return

            if l == r:
                self.arr[l] += val
                self.rebuild_leaf(node, l)
                return

            self.push(node)

            mid = (l + r) // 2

            if ql <= mid:
                self.range_add(node * 2, l, mid, ql, qr, val)

            if qr > mid:
                self.range_add(node * 2 + 1, mid + 1, r, ql, qr, val)

            self.pull(node)

        def query(self, node, l, r, ql, qr):
            if ql <= l and r <= qr:
                return self.cnt[node]

            self.push(node)

            mid = (l + r) // 2
            ans = 0

            if ql <= mid:
                ans += self.query(node * 2, l, mid, ql, qr)

            if qr > mid:
                ans += self.query(node * 2 + 1, mid + 1, r, ql, qr)

            return ans

    n, m = map(int, input().split())
    arr = list(map(int, input().split()))

    seg = SegTree(arr)

    out = []

    for _ in range(m):
        parts = input().split()

        if parts[0] == "add":
            l = int(parts[1]) - 1
            r = int(parts[2]) - 1
            d = int(parts[3])

            seg.range_add(1, 0, n - 1, l, r, d)

        else:
            l = int(parts[1]) - 1
            r = int(parts[2]) - 1

            out.append(str(seg.query(1, 0, n - 1, l, r)))

    return "\n".join(out)

# provided sample
assert run(
"""3 6
2 3 4
count 1 3
count 1 2
add 1 3 2
count 1 3
add 2 3 3
count 1 3
"""
) == "1\n0\n1\n1"

# minimum size
assert run(
"""1 2
4
count 1 1
count 1 1
"""
) == "1\n1"

# becoming lucky after update
assert run(
"""2 2
3 6
add 1 2 1
count 1 2
"""
) == "2"

# all equal values
assert run(
"""5 3
7 7 7 7 7
count 1 5
add 2 4 1
count 1 5
"""
) == "5\n2"

# boundary interval update
assert run(
"""5 4
1 2 3 4 5
add 1 5 3
count 1 5
add 5 5 2
count 4 5
"""
) == "2\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element already lucky | `1 1` | Minimum-size handling |
| Values becoming lucky | `2` | Crossing lucky thresholds |
| All values initially lucky | `5 2` | Correct decrement after updates |
| Full-range and suffix updates | `2 1` | Boundary correctness and indexing |

## Edge Cases

Consider the case where a value becomes lucky exactly after an update.

Input:

```
1 2
3
add 1 1 1
count 1 1
```

Initially the next lucky number is `4`, so `delta = 1`. After adding `1`, the segment update subtracts `1` from delta, producing `0`. Since `mn <= 0`, the algorithm descends to the leaf and rebuilds it. The value becomes `4`, which is lucky, so `cnt = 1`. The query correctly returns `1`.

Now consider leaving a lucky number.

Input:

```
1 2
4
add 1 1 1
count 1 1
```

Initially `delta = 0`. After adding `1`, delta becomes `-1`, forcing a rebuild. The new value is `5`, whose next lucky number is `7`, so the rebuilt delta becomes `2` and `cnt = 0`. The answer is correctly `0`.

Finally, consider repeated lazy updates without rebuilding most nodes.

Input:

```
5 3
1 1 1 1 1
add 1 5 1
add 1 5 1
count 1 5
```

Each value moves from `1` to `3`. Their next lucky number remains `4`, so deltas evolve from `3` to `2` to `1`. Since the segment minimum never becomes non-positive, the algorithm never descends unnecessarily. The final answer is `0`, and the update cost stays near logarithmic instead of touching every leaf.

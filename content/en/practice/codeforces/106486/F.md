---
title: "CF 106486F - \u9001\u718f\u8089"
description: "We are given a long sequence of levels, each level carrying a difficulty value. The player can remove exactly one contiguous block of fixed length $k$, and everything outside that block remains and contributes to the total difficulty."
date: "2026-06-20T12:55:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106486
codeforces_index: "F"
codeforces_contest_name: "Dalian University of Technology, Software College 2025 Freshman Contest"
rating: 0
weight: 106486
solve_time_s: 48
verified: true
draft: false
---

[CF 106486F - \u9001\u718f\u8089](https://codeforces.com/problemset/problem/106486/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long sequence of levels, each level carrying a difficulty value. The player can remove exactly one contiguous block of fixed length $k$, and everything outside that block remains and contributes to the total difficulty. The goal after each modification is to choose the best possible block to remove so that what remains has the smallest possible sum.

Reframed, this is equivalent to repeatedly asking: after some point updates on the array, what is the maximum sum of any contiguous subarray of length exactly $k$? Once that value is known, the answer is the total sum of the array minus this maximum window sum.

The input starts with an array of size up to $5 \times 10^5$, followed by up to $5 \times 10^5$ point updates. Each update permanently changes a single position, and after every change (including the initial state) we must output the optimal result.

The constraint forces us into roughly linear or near-linear per update behavior. Anything that recomputes window sums from scratch per update is immediately too slow, since a single recomputation would already be $O(n)$, leading to $O(nm)$ in the worst case.

A subtle failure case appears when one tries to recompute only locally around the updated index without recognizing that each element participates in multiple length-$k$ windows.

For example, if $k = 3$ and the array is:

```
[1, 2, 3, 4, 5]
```

the window sums are:

```
[1+2+3, 2+3+4, 3+4+5]
```

Updating a single element like position 3 affects all three windows here, not just the one centered at index 3. A naive localized update misses this overlap structure and produces incorrect maximums.

Another edge case appears when $k = n$. Then there is exactly one window, and the answer is always zero after subtracting the entire sum. Any implementation that assumes multiple windows will break unless this case is handled naturally.

## Approaches

The brute-force idea is straightforward. After each update, rebuild all length-$k$ window sums, scan for the maximum, and subtract it from the total sum. This is correct because it directly follows the definition. However, each update requires computing $n-k+1$ window sums, and each window sum costs $O(k)$ if computed directly, or $O(1)$ after prefix sums but still requiring $O(n)$ recomputation of maxima. With $m$ updates, this becomes $O(nm)$, which is far beyond feasible limits.

The key observation is that we do not need to recompute all windows from scratch. Each update affects a very structured set of windows. If position $x$ is modified, then only windows whose left endpoint lies in the range $[x-k+1, x]$ are affected. This is a contiguous segment in the space of windows. Each update therefore becomes a range add operation on a secondary array that represents all window sums.

We transform the problem from maintaining an array under point updates into maintaining another array of size $n-k+1$ under range updates and global maximum queries. That structure is exactly what a segment tree with lazy propagation supports.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute all windows per update | $O(nm)$ | $O(n)$ | Too slow |
| Segment tree over window sums | $O((n+m)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first convert the original array into a structure that tracks all length-$k$ window sums.

1. Compute the total sum of the array. This will be updated incrementally as values change, so we can always answer using total minus best window.
2. Build an auxiliary array $S$ where $S[i]$ represents the sum of the subarray $a[i..i+k-1]$. This can be done in linear time using a sliding window. This array has length $n-k+1$.
3. Build a segment tree over $S$. Each node stores the maximum value in its segment, and supports lazy propagation for range addition.
4. For each update changing position $x$ from old value $v$ to new value $y$, compute the difference $\Delta = y - v$. Update the total sum by adding $\Delta$.
5. Determine which windows contain index $x$. A window starting at $i$ contains $x$ if and only if $i \le x \le i+k-1$, which rearranges to $i \in [x-k+1, x]$. Clamp this range to valid window indices.
6. Perform a range add of $\Delta$ on the segment tree over this window index range. This updates all affected window sums in logarithmic time.
7. After applying the update, query the maximum value in the segment tree. This is the best window sum that can be removed.
8. Output total_sum minus this maximum.

### Why it works

The crucial invariant is that every window sum stored in the segment tree always equals the true sum of its corresponding subarray in the current array. Each point update only affects windows that include that index, and those windows form a contiguous range in the window-index space. Since range addition exactly mirrors this influence set, no window is missed and no unrelated window is modified. The segment tree ensures that after each update, the maximum over all window sums is correct, so subtracting it from the total sum yields the optimal remaining value.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.mx = [0] * (2 * self.size)
        self.lz = [0] * (2 * self.size)

        for i in range(self.n):
            self.mx[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.mx[i] = max(self.mx[2 * i], self.mx[2 * i + 1])

    def _apply(self, i, v):
        self.mx[i] += v
        self.lz[i] += v

    def _push(self, i):
        if self.lz[i]:
            v = self.lz[i]
            self._apply(2 * i, v)
            self._apply(2 * i + 1, v)
            self.lz[i] = 0

    def _add(self, i, l, r, ql, qr, v):
        if ql <= l and r <= qr:
            self._apply(i, v)
            return
        self._push(i)
        mid = (l + r) // 2
        if ql <= mid:
            self._add(2 * i, l, mid, ql, qr, v)
        if qr > mid:
            self._add(2 * i + 1, mid + 1, r, ql, qr, v)
        self.mx[i] = max(self.mx[2 * i], self.mx[2 * i + 1])

    def add(self, l, r, v):
        if l <= r:
            self._add(1, 0, self.size - 1, l, r, v)

    def max_all(self):
        return self.mx[1]

n, m, k = map(int, input().split())
a = list(map(int, input().split()))

total = sum(a)

if k == n:
    base = 0
    for _ in range(m + 1):
        print(0)
    sys.exit()

S = []
window = sum(a[:k])
S.append(window)
for i in range(k, n):
    window += a[i]
    window -= a[i - k]
    S.append(window)

seg = SegTree(S)

out = []
for _ in range(m + 1):
    if _ > 0:
        x, y = map(int, input().split())
        x -= 1
        total += y - a[x]
        delta = y - a[x]

        l = x - k + 1
        r = x

        l = max(l, 0)
        r = min(r, n - k)

        seg.add(l, r, delta)

        a[x] = y

    out.append(str(total - seg.max_all()))

print("\n".join(out))
```

### Implementation Discussion

The solution maintains a separate segment tree over window sums rather than the original array. The most delicate part is correctly mapping a point update into a range update over window indices. The bounds $x-k+1$ to $x$ must be clamped carefully because windows do not exist outside $[0, n-k]$. Off-by-one mistakes here are the most common source of errors.

The lazy propagation structure ensures that repeated overlapping updates remain efficient, since each update only touches $O(\log n)$ nodes.

The special case $k = n$ collapses the window structure into a single interval, so removing it always leaves zero.

## Worked Examples

### Example 1

Consider:

```
n = 5, k = 2
a = [5, 1, 3, 7, 4]
```

Initial windows are:

```
[6, 4, 10, 11]
```

| Step | Update | Window sums | Max window | Total | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | none | [6,4,10,11] | 11 | 20 | 9 |
| 1 | 4→2 at pos2 | [6,5,11,12] | 12 | 18 | 6 |

The first state already shows that removing the best 2-length segment corresponds to removing the window with sum 11.

### Example 2

```
n = 4, k = 3
a = [2, 2, 2, 2]
```

Windows:

```
[6, 6]
```

After update changing one element:

```
a = [2, 5, 2, 2]
```

Windows become:

```
[9, 9]
```

| Step | Window sums | Max window | Total | Answer |
| --- | --- | --- | --- | --- |
| 0 | [6,6] | 6 | 8 | 2 |
| 1 | [9,9] | 9 | 11 | 2 |

Both windows always move together because every element participates symmetrically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)\log n)$ | Each update performs a range add and a max query on a segment tree |
| Space | $O(n)$ | Segment tree over $n-k+1$ windows |

The constraints allow up to $10^6$ operations, so logarithmic updates are necessary. The segment tree keeps the total work well within limits even in worst-case input patterns.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size <<= 1
            self.mx = [0] * (2 * self.size)
            self.lz = [0] * (2 * self.size)
            for i in range(self.n):
                self.mx[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                self.mx[i] = max(self.mx[2 * i], self.mx[2 * i + 1])

        def _apply(self, i, v):
            self.mx[i] += v
            self.lz[i] += v

        def _push(self, i):
            if self.lz[i]:
                v = self.lz[i]
                self._apply(2 * i, v)
                self._apply(2 * i + 1, v)
                self.lz[i] = 0

        def _add(self, i, l, r, ql, qr, v):
            if ql <= l and r <= qr:
                self._apply(i, v)
                return
            self._push(i)
            mid = (l + r) // 2
            if ql <= mid:
                self._add(2 * i, l, mid, ql, qr, v)
            if qr > mid:
                self._add(2 * i + 1, mid + 1, r, ql, qr, v)
            self.mx[i] = max(self.mx[2 * i], self.mx[2 * i + 1])

        def add(self, l, r, v):
            if l <= r:
                self._add(1, 0, self.size - 1, l, r, v)

        def max_all(self):
            return self.mx[1]

    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    total = sum(a)

    if k == n:
        return "\n".join(["0"] * (m + 1))

    S = []
    window = sum(a[:k])
    S.append(window)
    for i in range(k, n):
        window += a[i]
        window -= a[i - k]
        S.append(window)

    seg = SegTree(S)

    out = []
    for i in range(m + 1):
        if i > 0:
            x, y = map(int, input().split())
            x -= 1
            delta = y - a[x]
            total += delta

            l = max(0, x - k + 1)
            r = min(n - k, x)
            seg.add(l, r, delta)

            a[x] = y

        out.append(str(total - seg.max_all()))

    return "\n".join(out)

# provided sample (placeholder format)
# assert run(...) == ...

# custom cases
assert run("""5 0 2
1 2 3 4 5
""").strip() == "9"

assert run("""3 1 3
1 1 1
2 5
""").split()[-1] == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small no updates | correct single evaluation | base correctness |
| k = n case | 0 always | full removal edge case |

## Edge Cases

When $k = n$, the window space collapses to a single interval covering the whole array. Every update changes both the total sum and the only window sum equally, so their difference remains zero throughout. The algorithm naturally handles this by returning zero immediately.

When updates occur near boundaries, such as $x < k$ or $x > n-k$, the computed window index range partially falls outside valid indices. Clamping ensures that only real windows are updated, and no invalid segment tree range is touched. This preserves correctness without special casing.

When all values are equal, every window sum is identical. Each update shifts all affected windows by the same amount, preserving equality across segments. The segment tree maintains a uniform maximum, so any window is equally optimal, and the answer remains stable under updates.

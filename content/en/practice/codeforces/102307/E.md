---
title: "CF 102307E - Extreme Image"
description: "We have (n) luminous bodies, each described by its distance from Earth and its angular position around Earth. The observatory can choose any radial interval of length (d), written as ([x,x+d]), and any angular interval of length (alpha), written as ([omega,omega+alpha])."
date: "2026-08-13T23:41:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102307
codeforces_index: "E"
codeforces_contest_name: "2019 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102307
solve_time_s: 80
verified: true
draft: false
---

[CF 102307E - Extreme Image](https://codeforces.com/problemset/problem/102307/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) luminous bodies, each described by its distance from Earth and its angular position around Earth. The observatory can choose any radial interval of length (d), written as ([x,x+d]), and any angular interval of length (\alpha), written as ([\omega,\omega+\alpha]). The angular coordinate is circular, so an interval can cross (360^\circ) and continue from (0^\circ).

The task is to choose both intervals so that the number of bodies whose distance and angle are simultaneously inside them is as large as possible. The answer is that maximum number of captured bodies.

The input contains up to (10^5) bodies, distances are integers up to (10^5), and all angles and (\alpha) have at most two digits after the decimal point. The (10^5) bound rules out checking every pair of bodies, since an (O(n^2)) algorithm would perform about (10^{10}) operations in the worst case. A solution around (O(n\log n)) is appropriate for a two second limit.

The two decimal places on angles give us another useful bound. After multiplying every angle by (100), every relevant angle is an integer from (0) through (35999). This lets us use a segment tree over only (36000) possible angular positions instead of building a structure whose size depends on (n).

The first boundary case is (\alpha=0). For example,

```
1 10 0.00
5 20.00
```

has answer (1), because an angular interval of zero length can still contain a body exactly at its chosen angle. An implementation that treats zero length as an empty interval would incorrectly return (0).

The second boundary case is an angular interval crossing (360^\circ). For example,

```
2 10 20.00
5 350.00
5 10.00
```

has answer (2). Choosing the angular interval ([350^\circ,10^\circ]) captures both bodies. A linear, non-circular interval implementation would miss one of them.

The third boundary case is inclusivity. For example,

```
2 10 10.00
1 0.00
11 10.00
```

has answer (2), because both distance endpoints and both angular endpoints are included. A strict comparison such as (r > x) or (\theta < \omega+\alpha) would lose a body lying exactly on an endpoint.

Finally, duplicate positions must all be counted. For example,

```
3 5 0.00
10 25.00
10 25.00
10 25.00
```

has answer (3). The bodies are distinct even though their coordinates are identical, so the data structure must perform one update per input body.

## Approaches

The direct approach is to enumerate every possible radial interval and every possible angular interval. We can reduce the first part slightly by observing that an optimal radial interval can be moved until its right endpoint reaches the distance of some body, so there are only (n) relevant radial windows. For each such window, however, checking all possible angular starts or all pairs of angular endpoints still takes (O(n)) work. In the worst case this becomes (O(n^2)), around (10^{10}) body-level operations for (n=10^5), which is far beyond the time limit.

The brute force is correct because every captured set is defined by one radial interval and one angular interval, and trying all relevant choices eventually examines an optimal pair. The problem is that the angular problem is recomputed from scratch after each radial change.

The key observation is that the radial interval can be swept. Sort the bodies by distance and maintain exactly the bodies whose distances belong to the current window ([r-d,r]), where (r) is the distance of the current rightmost body. When we move to the next body, some bodies enter the window and some leave it. Each body is inserted once and removed once.

We still need to answer a dynamic angular question: among the currently active bodies, what is the maximum number contained in an angular interval of length (\alpha)?

Because every input angle has two decimal places, scale angles by (100). There are only (36000) possible hundredth-degree positions. Instead of storing the number of bodies at each possible interval start directly, think about what one body contributes.

Suppose a body has angle (\theta). An angular interval beginning at (s) captures it exactly when

[
s \leq \theta \leq s+\alpha
]

on the circle. Rearranging gives

[
\theta-\alpha \leq s \leq \theta.
]

Thus, from the perspective of possible interval starts, one body contributes (+1) to a circular range of starts from (\theta-\alpha) through (\theta). Adding a body is therefore a circular range addition, and removing it is a circular range subtraction.

A segment tree can support range addition and the maximum value over the entire array in (O(\log 36000)). Its root always stores the best angular interval for the currently active radial window. Combining this with the distance sweep gives an (O(n\log n+n\log 36000)) algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n\log n+n\log 36000)) | (O(n+36000)) | Accepted |

## Algorithm Walkthrough

1. Multiply every angle and (\alpha) by (100), converting the input into exact integers. This avoids floating-point comparisons at boundaries such as (10.00) versus (10.01).
2. Sort all bodies by their distance. We will process them in increasing distance order and use the current body's distance as the right endpoint of the active radial window.
3. Build a segment tree with (36000) leaves. Leaf (s) represents choosing the angular interval to start at the scaled angle (s). Initially every leaf contains zero because no bodies are active.
4. When a body with scaled angle (\theta) becomes active, add (1) to all possible starts in the circular interval ([\theta-\alpha,\theta]). Every such start captures this body, so increasing exactly those values updates the capture count for every affected angular interval.
5. If the update interval crosses zero, split it into two ordinary ranges, one ending at (35999) and one beginning at zero. If it does not cross zero, one ordinary range update is enough.
6. After inserting the current body, remove every body whose distance is smaller than (r-d), where (r) is the current body's distance. The strict inequality is deliberate because the radial interval is closed, so a body at exactly (r-d) must remain active.
7. Read the maximum value stored at the root of the segment tree and update the global answer. The root represents the best angular interval among all starts for the current radial window.
8. Continue through all bodies. Every optimal radial interval can be shifted until its right endpoint reaches the distance of one of its captured bodies, so one of these sweep positions represents an optimal radial choice.

### Why it works

At every sweep position, the active set is exactly the set of bodies whose distances lie in the closed interval ([r-d,r]). For this fixed radial set, the value stored at a segment-tree leaf (s) is exactly the number of active bodies whose angles lie in the circular interval ([s,s+\alpha]). This is true because every active body contributes one range update precisely to the starts that capture it. Consequently, the segment-tree root is the maximum number of active bodies captured by any angular interval.

Consider an optimal pair of radial and angular intervals. If the optimal radial interval contains at least one body, move it to the right until its right endpoint reaches the farthest captured body's distance. No captured body is lost during this movement, so there is an equally good solution whose right endpoint is one of the processed distances. At that sweep position, the segment tree considers every possible angular start and therefore finds an angular interval capturing exactly the maximum possible number for that radial choice. The algorithm consequently examines a solution at least as good as the global optimum, while no computed value can exceed the number captured by some valid pair of intervals.

## Python Solution

```python
import sys
input = sys.stdin.readline

ANGLE_COUNT = 36000
INF = 10**30

def parse_scaled(s):
    if '.' in s:
        whole, frac = s.split('.')
        frac = (frac + '00')[:2]
    else:
        whole, frac = s, '00'
    return int(whole) * 100 + int(frac)

class SegmentTree:
    def __init__(self, n):
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.mx = [0] * (2 * size)
        self.lazy = [0] * (2 * size)

    def _apply(self, node, value):
        self.mx[node] += value
        self.lazy[node] += value

    def _push(self, node):
        value = self.lazy[node]
        if value:
            self._apply(node * 2, value)
            self._apply(node * 2 + 1, value)
            self.lazy[node] = 0

    def _add(self, node, left, right, ql, qr, value):
        if ql <= left and right <= qr:
            self._apply(node, value)
            return

        self._push(node)
        mid = (left + right) // 2

        if ql <= mid:
            self._add(node * 2, left, mid, ql, qr, value)
        if qr > mid:
            self._add(node * 2 + 1, mid + 1, right, ql, qr, value)

        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])

    def add(self, left, right, value):
        if left > right:
            return
        self._add(1, 0, self.size - 1, left, right, value)

    def maximum(self):
        return self.mx[1]

def solve():
    n, d, alpha_text = input().split()
    n = int(n)
    d = int(d)
    alpha = parse_scaled(alpha_text)

    points = []

    for _ in range(n):
        r_text, angle_text = input().split()
        r = int(r_text)
        angle = parse_scaled(angle_text)
        points.append((r, angle))

    points.sort()

    seg = SegmentTree(ANGLE_COUNT)

    def update_angle(theta, delta):
        if alpha == 0:
            seg.add(theta, theta, delta)
            return

        left = theta - alpha

        while left < 0:
            left += ANGLE_COUNT

        if left <= theta:
            seg.add(left, theta, delta)
        else:
            seg.add(left, ANGLE_COUNT - 1, delta)
            seg.add(0, theta, delta)

    left = 0
    answer = 0

    for right in range(n):
        r, theta = points[right]

        update_angle(theta, 1)

        while points[left][0] < r - d:
            old_theta = points[left][1]
            update_angle(old_theta, -1)
            left += 1

        answer = max(answer, seg.maximum())

    print(answer)

if __name__ == "__main__":
    solve()
```

The first parsing detail is deliberate. Python floating-point values should not be used for the angular comparisons because decimal values such as `0.01` are generally not represented exactly in binary floating point. Since the input has at most two decimal places, multiplying by (100) gives an exact integer representation.

The `points` array is sorted by distance, which gives the sweep its one-dimensional structure. The pointer `left` always marks the first body that is still inside the current radial window.

The function `update_angle` implements the contribution of one body to possible angular starts. For a body at angle `theta`, valid starts range from `theta - alpha` through `theta`. When this range wraps around zero, it is represented by two segment-tree updates.

The special case `alpha == 0` deserves its own branch. The valid start is then exactly `theta`, so the update must affect one leaf rather than accidentally creating a large wrapped interval.

The removal condition is `points[left][0] < r - d`. A body at exactly `r-d` belongs to the closed radial interval and must not be removed. The same inclusive interpretation is already built into the angular range updates because both endpoints are updated.

The segment tree stores a lazy value for each node. A range update changes the maximum of that entire node by the same amount, so it can be applied without descending to every leaf. The root consequently gives the best angular interval after every insertion and deletion.

There is no integer overflow concern in Python. In a fixed-width language, the maximum count is only (10^5), so a 32-bit signed integer would already be sufficient for the stored counts.

## Worked Examples

The statement source lists the following sample and its output is (3).

```
7 80 60.00
220 20.00
360 45.00
180 45.00
200 150.00
200 75.00
180 315.00
360 225.00
```

After scaling angles, (\alpha=6000). The distance window has width (80). The sweep state can be summarized as follows.

| Current distance | Active distances | Current best angular count | Global answer |
| --- | --- | --- | --- |
| 180 | 180, 180 | 2 | 2 |
| 200 | 180, 180, 200, 200 | 2 | 2 |
| 220 | 180, 180, 200, 200, 220 | 3 | 3 |
| 360 | 360 | 1 | 3 |

At distance (220), the active radial interval is ([140,220]), so it contains the two bodies at distance (180), both bodies at (200), and the body at (220). The segment tree finds an angular interval of width (60^\circ) containing three of them, giving the final answer (3).

For a second example, consider a radial boundary and an angular wrap at the same time.

```
4 10 20.00
5 350.00
15 10.00
15 20.00
16 5.00
```

The sweep behaves as follows.

| Current distance | Active bodies by angle | Best angular start | Best count |
| --- | --- | --- | --- |
| 5 | 350 | 350 | 1 |
| 15 | 350, 10, 20 | 350 | 2 |
| 16 | 10, 20, 5 | 350 | 3 |

At distance (15), the radial interval is ([5,15]), so the body at distance (5) remains active because the boundary is inclusive. The angular interval starting at (350^\circ) covers (350^\circ), (10^\circ), and (10^\circ)-side positions up to (10^\circ), but not (20^\circ), so the best count there is (2). At distance (16), the body at distance (5) is removed because (5 < 16-10), leaving the three bodies at distances (15,15,16). The same circular angular interval can capture all three because (350^\circ), (5^\circ), and (10^\circ) fit inside a (20^\circ) wrapped interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n+n\log 36000)) | Sorting costs (O(n\log n)), and every body is inserted and removed once using (O(\log 36000)) range updates. |
| Space | (O(n+36000)) | The sorted bodies require (O(n)) space and the segment tree requires (O(36000)) space. |

Since (36000) is fixed by the two-decimal angular precision, the segment-tree part is effectively (O(n)) with a small logarithmic constant. The dominant operation is sorting (10^5) bodies, which is easily suitable for the stated constraints.

## Test Cases

The original statement's displayed sample output is (3).

```python
import sys
import io

ANGLE_COUNT = 36000

def parse_scaled(s):
    if '.' in s:
        whole, frac = s.split('.')
        frac = (frac + '00')[:2]
    else:
        whole, frac = s, '00'
    return int(whole) * 100 + int(frac)

class SegmentTree:
    def __init__(self, n):
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.mx = [0] * (2 * size)
        self.lazy = [0] * (2 * size)

    def _apply(self, node, value):
        self.mx[node] += value
        self.lazy[node] += value

    def _push(self, node):
        value = self.lazy[node]
        if value:
            self._apply(node * 2, value)
            self._apply(node * 2 + 1, value)
            self.lazy[node] = 0

    def _add(self, node, left, right, ql, qr, value):
        if ql <= left and right <= qr:
            self._apply(node, value)
            return

        self._push(node)
        mid = (left + right) // 2

        if ql <= mid:
            self._add(node * 2, left, mid, ql, qr, value)
        if qr > mid:
            self._add(node * 2 + 1, mid + 1, right, ql, qr, value)

        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])

    def add(self, left, right, value):
        if left <= right:
            self._add(1, 0, self.size - 1, left, right, value)

    def maximum(self):
        return self.mx[1]

def solve():
    input = sys.stdin.readline

    n, d, alpha_text = input().split()
    n = int(n)
    d = int(d)
    alpha = parse_scaled(alpha_text)

    points = []
    for _ in range(n):
        r_text, angle_text = input().split()
        points.append((int(r_text), parse_scaled(angle_text)))

    points.sort()

    seg = SegmentTree(ANGLE_COUNT)

    def update(theta, delta):
        if alpha == 0:
            seg.add(theta, theta, delta)
            return

        left = theta - alpha
        if left < 0:
            left += ANGLE_COUNT

        if left <= theta:
            seg.add(left, theta, delta)
        else:
            seg.add(left, ANGLE_COUNT - 1, delta)
            seg.add(0, theta, delta)

    left = 0
    answer = 0

    for right in range(n):
        r, theta = points[right]
        update(theta, 1)

        while points[left][0] < r - d:
            update(points[left][1], -1)
            left += 1

        answer = max(answer, seg.maximum())

    return str(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solve().strip()
    finally:
        sys.stdin = old_stdin

sample1 = """\
7 80 60.00
220 20.00
360 45.00
180 45.00
200 150.00
200 75.00
180 315.00
360 225.00
"""

assert run(sample1) == "3", "sample 1"

assert run("""\
1 1 0.00
1 0.00
""") == "1", "minimum-size case"

assert run("""\
3 5 0.00
10 25.00
10 25.00
10 25.00
""") == "3", "zero angular width and duplicates"

assert run("""\
2 10 20.00
5 350.00
5 10.00
""") == "2", "angular interval wraps around 360 degrees"

assert run("""\
2 10 10.00
1 0.00
11 10.00
""") == "2", "both radial and angular boundaries are inclusive"

# Maximum-size stress case. All bodies are at the same position,
# so the answer must be n.
n = 100000
large = [f"{n} 100000 359.99\n"]
large.extend(f"1 0.00\n" for _ in range(n))
assert run("".join(large)) == str(n), "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0.00 / 1 0.00` | 1 | Minimum input size and zero angular width |
| Three identical bodies with `alpha = 0` | 3 | Duplicate bodies and exact angular matching |
| Bodies at `350.00` and `10.00` with `alpha = 20.00` | 2 | Circular angular interval |
| Distances `1` and `11` with `d = 10` | 2 | Inclusive radial and angular boundaries |
| 100000 identical bodies with `alpha = 359.99` | 100000 | Maximum input size and large segment-tree counts |

## Edge Cases

For zero angular width, consider

```
1 1 0.00
1 0.00
```

The scaled angular width is zero. When the only body is inserted, `update` changes exactly the leaf representing (0^\circ). The segment-tree maximum becomes (1), so the algorithm returns (1). No interval of positive length is accidentally created.

For circular wrapping, consider

```
2 10 20.00
5 350.00
5 10.00
```

For the first body, the valid interval starts are from (330^\circ) through (350^\circ). For the second body, they range from (350^\circ) through (10^\circ), which crosses zero. The update is split into the ranges ([350^\circ,359.99^\circ]) and ([0^\circ,10^\circ]). The start at (350^\circ) consequently receives both contributions, giving a maximum of (2).

For inclusive distance boundaries, consider

```
2 10 10.00
1 0.00
11 10.00
```

When the current right distance is (11), the radial window is ([1,11]). The removal condition checks whether a distance is strictly less than (1), so the body at distance (1) remains active. Both bodies can also lie on the angular interval's endpoints, so the segment tree counts both and returns (2).

For duplicate bodies, consider

```
3 5 0.00
10 25.00
10 25.00
10 25.00
```

Each input line causes a separate range update, even though all three updates target the same leaf. The leaf value becomes (3), representing three distinct luminous bodies at that coordinate. The result is consequently (3).

The same logic handles (\alpha=359.99). A body contributes to every possible start except the tiny complementary angular interval of width (0.01^\circ). Since the segment tree explicitly represents all (36000) hundredth-degree starts, there is no approximation or floating-point ambiguity at this extreme value.

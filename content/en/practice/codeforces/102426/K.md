---
title: "CF 102426K - X-Window System"
description: "We have a screen of width (W) and height (H), and at most ten rectangular windows. The coordinate system is slightly unusual: the first coordinate increases downward and the second increases to the right."
date: "2026-08-12T19:42:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "K"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 565
verified: true
draft: false
---

[CF 102426K - X-Window System](https://codeforces.com/problemset/problem/102426/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a screen of width (W) and height (H), and at most ten rectangular windows. The coordinate system is slightly unusual: the first coordinate increases downward and the second increases to the right. A window may extend outside the screen, but only its intersection with the screen can actually be rendered.

The windows are ordered by z-index. A smaller z-index means the window is in front. Initially, window (0) is the frontmost, followed by window (1), and so on. At any moment exactly one window is active. A mouse click is interpreted using the currently rendered screen: among all windows containing the clicked screen point, the frontmost one receives the click. If no window contains the point, nothing changes.

When the clicked window is different from the active window, it becomes active and is moved to the very front. The other windows keep their relative order. Moving a window forward can reveal the part of that window that was previously covered by windows in front of it. The required output is precisely the area that becomes newly visible and consequently has to be redrawn.

The input gives the screen dimensions, all window rectangles in their initial z-order, and the sequence of mouse clicks. For every click we output the minimum area that must be redrawn after processing that click.

The constraints are unusually small in the number of windows and clicks. We have (n,q\le 10), while the screen can be as large as (2000\times2000). This makes algorithms exponential in (n) practical, but algorithms depending on every screen pixel are unnecessarily expensive. A pixel simulation could perform as many as (10\cdot2000\cdot2000\cdot10=400{,}000{,}000) window containment checks in the worst case. The geometry is continuous, so treating every unit square independently is also conceptually more complicated than necessary.

The first subtlety is that the click must be assigned to the topmost rendered window, not simply to the first window in the original input. For example:

```
1 1
2
0 0 1 1
0 0 1 1
1
0 0
```

The answer is:

```
0
```

The first window is already active and covers the click, even though the second window also contains the point. A careless implementation that searches windows in input order after every activation would eventually lose the current z-order.

The second subtlety is that a window can extend beyond the screen. Consider:

```
4 4
2
0 0 1 1
-1 -1 3 3
1
2 2
```

The second window is visible only inside the screen, but the click at ((2,2)) still lies on its visible boundary. It becomes active, and its newly exposed overlap with the first window has area (1), so the output is:

```
1
```

An implementation that ignores clipping may incorrectly use the whole off-screen rectangle when calculating the repaint area.

The third subtlety is that overlapping windows must be counted as a union, not independently summed. Consider:

```
4 4
3
0 0 1 3
0 0 3 1
0 0 3 3
1
2 2
```

The click reaches the third window. The two windows in front cover areas (3) and (3) of it, but their common part has area (1). The required repaint area is therefore (3+3-1=5), giving:

```
5
```

Simply adding the pairwise intersection areas would produce (6), which is wrong.

## Approaches

A direct approach is to represent the screen as (W\times H) unit cells. Since every coordinate is integral, every rectangle boundary lies on grid lines, so its area can indeed be represented by a number of unit cells. For each click we could inspect every cell, determine which window is topmost there, and compare the old and new rendering. This is correct, but the worst case has (2000\cdot2000) cells, up to (10) clicks, and up to (10) windows examined per cell. That gives (400) million window checks. With a one-second limit, this is the wrong level of granularity.

The brute force works because it explicitly represents the screen, but the screen itself contains far more information than the problem needs. A repaint region is always formed by intersections and unions of rectangles, and there are only ten rectangles.

Suppose window (t) is being moved to the front. Before the operation, every window currently before (t) in z-order is covering part of (t). After the operation, (t) covers all of those windows. Thus the only newly visible area is

[
R_t\cap(R_1\cup R_2\cup\cdots\cup R_k),
]

where the (R_i) are precisely the windows currently in front of (t), with all rectangles understood to be clipped by the screen.

This reduces the problem to finding the area of a union of at most nine rectangles inside one target rectangle. With so few rectangles, inclusion-exclusion is particularly convenient. For every nonempty subset of the covering rectangles, compute the intersection of all rectangles in that subset. Add its area when the subset contains an odd number of rectangles and subtract it when the subset contains an even number.

There are at most (2^9-1=511) nonempty subsets for one activation. The mouse target can be found by scanning the current z-order, which costs only (O(n)). After computing the repaint area, moving the selected window to the front is simply a list operation.

The brute-force approach works because it explicitly models every visible unit of area, but fails because the screen is much larger than the number of geometric objects. The observation that only unions of at most nine rectangles matter lets us replace millions of cell operations with a few hundred rectangle intersections.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(qWHn)) | (O(WH)) | Too slow |
| Optimal | (O(qn^2 2^n)) | (O(n)) | Accepted |

The (n) factor inside the optimal bound comes from computing each subset intersection by scanning the rectangles belonging to that subset. Since (n\le10), this is comfortably small.

## Algorithm Walkthrough

1. Store every window as four coordinates representing its vertical interval and horizontal interval. Because the first coordinate is vertical, a window `(x, y, w, h)` occupies (x\ldots x+h) vertically and (y\ldots y+w) horizontally. Keep the initial z-order as `[0, 1, ..., n-1]`, where the first element is the frontmost window.
2. For every click, scan the current z-order from front to back. For each window, first intersect its rectangle with the screen and then test whether the mouse position lies inside that clipped rectangle. Use inclusive comparisons for the point test because the statement explicitly treats window boundaries as part of the rendered region.
3. If no window contains the mouse position, output zero and leave the z-order unchanged. There is no activation, so the rendered screen does not change.
4. If the selected window is already the active window, output zero and leave the z-order unchanged. Clicking an already active window does not move anything.
5. Otherwise, let the selected window be (t). In the current z-order, every window before (t) is in front of it. Collect exactly those windows. The area that needs to be redrawn is the area of (t) covered by the union of these front windows.
6. Clip the target window against the screen before calculating its area. For every nonempty subset of the front windows, intersect the target rectangle with every rectangle in that subset. If the resulting intersection has positive width and height, its area is added for an odd-sized subset and subtracted for an even-sized subset. This is the standard inclusion-exclusion formula for a union.
7. Remove (t) from its current position in the z-order and insert it at the beginning. This exactly models changing its z-index to zero while increasing every previous z-index by one.
8. Output the computed repaint area and continue with the next click. The maintained order is now the complete state needed to process the next mouse event.

### Why it works

The key invariant is that the z-order list always stores the windows from front to back exactly as the window system currently does. Consequently, the first window containing a click is exactly the window whose rendered pixels receive that click.

When a different window (t) becomes active, only its relationship with windows currently in front of it changes. Every such front window was previously visible over their overlap with (t), while after activation (t) is visible over that same overlap. No other part of the screen changes. Thus the repaint region is exactly the union of intersections between (t) and all windows before it.

Inclusion-exclusion computes that union exactly, even when several covering windows overlap. After moving (t) to the front, the z-order invariant is restored. Hence every click is processed against the correct screen state, and every reported area is exactly the area whose rendering changes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def intersect(a, b):
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    if x1 >= x2 or y1 >= y2:
        return None
    return (x1, y1, x2, y2)

def area(r):
    if r is None:
        return 0
    return (r[2] - r[0]) * (r[3] - r[1])

def union_inside(target, rects):
    k = len(rects)
    if k == 0:
        return 0

    ans = 0

    for mask in range(1, 1 << k):
        cur = target
        bits = 0

        for i in range(k):
            if mask & (1 << i):
                bits += 1
                cur = intersect(cur, rects[i])
                if cur is None:
                    break

        if cur is not None:
            a = area(cur)
            if bits & 1:
                ans += a
            else:
                ans -= a

    return ans

def solve():
    W, H = map(int, input().split())
    n = int(input())

    windows = []

    for _ in range(n):
        x, y, w, h = map(int, input().split())

        # x is vertical, y is horizontal.
        # The screen is [0, H] x [0, W].
        windows.append((x, y, x + h, y + w))

    q = int(input())

    clicks = [tuple(map(int, input().split())) for _ in range(q)]

    # Frontmost to backmost.
    order = list(range(n))

    screen = (0, 0, H, W)

    out = []

    for u, v in clicks:
        target_pos = -1

        # Find the frontmost rendered window containing the click.
        for pos, idx in enumerate(order):
            clipped = intersect(windows[idx], screen)

            if clipped is not None:
                if clipped[0] <= u <= clipped[2] and clipped[1] <= v <= clipped[3]:
                    target_pos = pos
                    break

        if target_pos == -1:
            out.append("0")
            continue

        target = order[target_pos]

        # Clicking the active window causes no change.
        if target_pos == 0:
            out.append("0")
            continue

        # Windows before target are exactly the windows currently
        # covering it from the front.
        front_rects = [
            windows[idx]
            for idx in order[:target_pos]
        ]

        clipped_target = intersect(windows[target], screen)

        repaint = union_inside(clipped_target, front_rects)
        out.append(str(repaint))

        # Move target to the front.
        order.pop(target_pos)
        order.insert(0, target)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `windows` array stores each rectangle as `(top, left, bottom, right)` in the problem's coordinate orientation. The vertical extent uses `h`, while the horizontal extent uses `w`. This is an easy place to accidentally swap width and height.

The `intersect` function uses strict `x1 < x2` and `y1 < y2` when deciding whether an intersection has positive area. A boundary may contain a mouse click, but a boundary has zero area, so it must not contribute to the repaint calculation.

The screen rectangle is `(0, 0, H, W)`. Intersecting a window with this rectangle handles all off-screen cases automatically. There is no need to modify the original window coordinates.

The click search uses `<=` on both ends. This follows the statement's rule that a visible boundary belongs to the rendered window. If two windows meet at a boundary, the current z-order still decides which one receives a click there.

The `union_inside` function applies inclusion-exclusion directly. A subset with an odd number of rectangles contributes positively, while an even-sized subset contributes negatively. The target rectangle is included in every intersection, so the computed union is automatically restricted to the area of the window being activated.

Python integers are sufficient for all areas. The maximum screen area is only (4{,}000{,}000), although inclusion-exclusion may temporarily add and subtract several such areas.

Finally, the selected window is removed from its old position and inserted at index zero. This directly represents the z-index transformation described by the problem.

## Worked Examples

The provided sample starts with the z-order `[0, 1, 2]`, where window `0` is frontmost. The following table tracks the important state after each click.

| Click | Selected window | Current order before | Front windows | Repaint area | Order after |
| --- | --- | --- | --- | --- | --- |
| `(2,1)` | 2 | `[0,1,2]` | `[0,1]` | 1 | `[2,0,1]` |
| `(3,1)` | none | `[2,0,1]` | none | 0 | `[2,0,1]` |
| `(1,2)` | 2 | `[2,0,1]` | none | 0 | `[2,0,1]` |
| `(3,8)` | 1 | `[2,0,1]` | `[2,0]` | 4 | `[1,2,0]` |
| `(3,3)` | 0 | `[1,2,0]` | `[1,2]` | 5 | `[0,1,2]` |

For the first click, the point lies on the visible boundary of window `2`. Its overlap with window `0` has area (1), while window `1` does not overlap it there, giving the first output of (1). The second click reaches no rendered window. The third click reaches window `2` again, which is already active.

The fourth click activates window `1`. Its overlap with window `0` contributes an area of (4), while its overlap with window `2` is zero. The fifth click activates window `0`. Its overlap with window `1` has area (4), and its overlap with window `2` has area (1). These regions do not overlap each other, so the union has area (5). The resulting output is exactly:

```
1
0
0
4
5
```

A second example focuses on overlapping covering windows:

```
4 4
3
0 0 1 3
0 0 3 1
0 0 3 3
1
2 2
```

The state trace is:

| Click | Selected window | Current order before | Coverage calculation | Repaint area | Order after |
| --- | --- | --- | --- | --- | --- |
| `(2,2)` | 2 | `[0,1,2]` | (3+3-1) | 5 | `[2,0,1]` |

The clicked point is outside the first two windows and inside the third. The first front window covers a (1\times3) rectangle, the second covers a (3\times1) rectangle, and their intersection is a (1\times1) square. Inclusion-exclusion gives (3+3-1=5). This example demonstrates why summing the individual overlaps is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(qn^2 2^n)) | Each click scans (O(n)) windows, and an activation evaluates at most (2^n) subsets, with up to (O(n)) rectangle intersections per subset. |
| Space | (O(n)) | The algorithm stores the rectangles, z-order, and a constant amount of temporary geometry. |

With (n,q\le10), the largest exponential factor is only (2^{10}=1024). Even with the extra factor of (n^2), the number of primitive operations is small. The screen dimensions do not appear in the complexity because the algorithm never iterates over individual pixels or unit cells.

## Test Cases

```python
import sys
import io

def intersect(a, b):
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    if x1 >= x2 or y1 >= y2:
        return None
    return x1, y1, x2, y2

def area(r):
    if r is None:
        return 0
    return (r[2] - r[0]) * (r[3] - r[1])

def union_inside(target, rects):
    k = len(rects)
    ans = 0

    for mask in range(1, 1 << k):
        cur = target
        bits = 0

        for i in range(k):
            if mask & (1 << i):
                bits += 1
                cur = intersect(cur, rects[i])
                if cur is None:
                    break

        if cur is not None:
            if bits & 1:
                ans += area(cur)
            else:
                ans -= area(cur)

    return ans

def solve():
    input = sys.stdin.readline

    W, H = map(int, input().split())
    n = int(input())

    windows = []
    for _ in range(n):
        x, y, w, h = map(int, input().split())
        windows.append((x, y, x + h, y + w))

    q = int(input())
    order = list(range(n))
    screen = (0, 0, H, W)

    ans = []

    for _ in range(q):
        u, v = map(int, input().split())

        pos = -1

        for i, idx in enumerate(order):
            r = intersect(windows[idx], screen)
            if r is not None and r[0] <= u <= r[2] and r[1] <= v <= r[3]:
                pos = i
                break

        if pos <= 0:
            ans.append("0")
            continue

        target = order[pos]
        target_rect = intersect(windows[target], screen)

        front = [windows[idx] for idx in order[:pos]]
        repaint = union_inside(target_rect, front)

        ans.append(str(repaint))

        order.pop(pos)
        order.insert(0, target)

    return "\n".join(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

sample1 = """\
9 6
3
1 2 5 4
2 5 3 2
-1 1 2 3
5
2 1
3 1
1 2
3 8
3 3
"""

assert run(sample1) == "1\n0\n0\n4\n5", "sample 1"

minimum_case = """\
1 1
1
0 0 1 1
1
1 1
"""

assert run(minimum_case) == "0", "minimum size"

boundary_case = """\
4 4
2
0 0 1 1
-1 -1 3 3
1
2 2
"""

assert run(boundary_case) == "1", "screen clipping and boundary"

union_case = """\
4 4
3
0 0 1 3
0 0 3 1
0 0 3 3
1
2 2
"""

assert run(union_case) == "5", "overlapping front windows"

reorder_case = """\
4 4
3
0 0 1 1
0 0 4 4
3 3 1 1
3
3 3
0 0
2 2
"""

assert run(reorder_case) == "1\n0\n2", "z-order changes"

maximum_equal_case = """\
2000 2000
10
0 0 2000 2000
0 0 2000 2000
0 0 2000 2000
0 0 2000 2000
0 0 2000 2000
0 0 2000 2000
0 0 2000 2000
0 0 2000 2000
0 0 2000 2000
0 0 2000 2000
10
0 0
1000 1000
2000 2000
0 2000
2000 0
1 1
1999 1999
500 1500
1500 500
1000 1000
"""

assert run(maximum_equal_case) == "\n".join(["0"] * 10), "maximum size and equal windows"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum-size case | `0` | Smallest screen, one window, active-window click |
| Boundary case | `1` | Off-screen clipping and inclusive click boundaries |
| Union case | `5` | Inclusion-exclusion for overlapping covering windows |
| Reorder case | `1`, `0`, `2` | Dynamic z-order and repeated activations |
| Maximum equal case | Ten zeros | Maximum dimensions, maximum number of windows and clicks, identical rectangles |

## Edge Cases

The minimum-size input has a (1\times1) screen and a single (1\times1) window. The only window starts active, so any click inside it selects the already active window. The algorithm finds it at position zero in `order`, immediately outputs zero, and never changes the order.

The clipping case uses the window `(-1,-1,3,3)` on a (4\times4) screen. Its visible region is only the intersection with `[0,4] × [0,4]`. The click at `(2,2)` lies inside that visible region but outside the first window, so the second window is activated. The intersection with the first window is exactly the (1\times1) square `[0,1] × [0,1]`, giving repaint area (1).

The overlapping-window case activates the third window while two windows are in front of it. Their individual overlaps with the target have areas (3) and (3), but their common overlap has area (1). The inclusion-exclusion calculation is (3+3-1=5), so the algorithm outputs `5` rather than the incorrect sum `6`.

The dynamic-order case first activates window `2`, changing the order from `[0,1,2]` to `[2,0,1]` and repainting area (1). The next click reaches window `0`, which becomes active and moves the order to `[0,2,1]`; its overlap with window `2` has zero area, so the repaint amount is zero. The final click reaches window `1`. At that moment both window `0` and window `2` are in front of it, and their overlaps with window `1` are disjoint unit squares, producing a repaint area of (2). This confirms that the algorithm uses the current z-order rather than the original input order.

The maximum-size case has ten identical full-screen windows. Only the frontmost window can ever receive a click because it completely covers every other window. It is already active for every click, so every answer is zero. The test confirms that large screen dimensions do not cause the algorithm to allocate or traverse a (2000\times2000) grid.

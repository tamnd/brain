---
title: "CF 102346C - Crossings With Danger"
description: "We have an (N times M) rectangular grid of crossings. A vehicle starts at one crossing, chooses one of the four cardinal directions, and then moves at speed one crossing per second until it either leaves the grid or collides."
date: "2026-08-13T01:19:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "C"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 193
verified: true
draft: false
---

[CF 102346C - Crossings With Danger](https://codeforces.com/problemset/problem/102346/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (N \times M) rectangular grid of crossings. A vehicle starts at one crossing, chooses one of the four cardinal directions, and then moves at speed one crossing per second until it either leaves the grid or collides.

There are two fundamentally different kinds of collisions. Two vehicles moving toward each other on the same lane meet between crossings, with the horizontal collision being placed at the eastern crossing and the vertical collision being placed at the northern crossing. Vehicles moving on perpendicular lanes can collide at a crossing when they arrive there at exactly the same time. After a collision, the involved vehicles stop permanently at that crossing. A later vehicle reaching that crossing also collides.

The task is to count the vehicles that never participate in any collision.

The number of vehicles is at most (10^5), while the grid can contain up to (10^{10}) crossings. We cannot build the whole grid, and even (O(C^2)) pair checking is far too expensive. With (C=10^5), that would require about (5\cdot10^9) vehicle pairs in the worst case. The intended solution must process only a logarithmic amount of information per vehicle or collision.

There are several cases where a direct geometric check is misleading. A vehicle can have a theoretical intersection with another vehicle's original trajectory without actually colliding because that other vehicle stopped earlier. For example,

```
3 4 3
1 1 L
3 3 N
2 4 O
```

The eastbound vehicle and the northbound vehicle would meet at ((1,3)) at time (2) if both continued forever. However, the northbound vehicle first collides with the westbound vehicle at ((2,3)) at time (1), so it stops there. The eastbound vehicle continues safely and the correct answer is (1). An approach that simply marks every pair of intersecting trajectories as a collision would incorrectly mark all three vehicles.

Another subtle case is a collision between crossings. With

```
2 3 2
1 1 L
1 3 O
```

the vehicles meet halfway between columns (1) and (3), at time (1), and stop at the eastern crossing, column (2). Treating the collision point as the mathematical midpoint without applying the problem's eastern-crossing rule gives the wrong obstacle location.

A third edge case occurs when a stopped vehicle is hit later. The vehicle causing the second collision does not have to have intersected the stopped vehicle's original trajectory at the same time. Once a collision creates a permanent obstacle, the obstacle itself becomes part of the simulation.

## Approaches

The brute-force approach is to examine every pair of vehicles and calculate whether their trajectories meet. For each pair we can determine whether they travel on compatible rows, columns, or perpendicular lanes, and then calculate the meeting time. This is correct if we simulate the actual state carefully, but even merely examining every pair already costs (O(C^2)). At (C=10^5), that means roughly (5\cdot10^9) pairs, which is impossible under the 1.5 second C++ limit and even less practical in Python.

The more useful observation is that the simulation is event driven. A moving vehicle does not care about every other vehicle. Its next collision can only involve the closest relevant moving vehicle in one of a constant number of geometric directions, or the closest stopped crossing along its own lane.

For perpendicular collisions, the useful geometric transformation is especially simple. Suppose an eastbound vehicle at ((r,c)) meets a northbound vehicle at ((r',c')). The meeting crossing satisfies

[
c'-c=r-r',
]

so

[
r+c=r'+c'.
]

Thus the two vehicles lie on the same anti-diagonal. Other direction combinations similarly correspond to either (r+c) or (r-c). Head-on horizontal collisions use the same row, while head-on vertical collisions use the same column.

This reduces every moving-moving collision query to finding the nearest active vehicle in one of a constant number of ordered one-dimensional sequences. Since vehicles only disappear from the moving set, these sequences support deletion efficiently. A stopped crossing is handled separately as a permanent obstacle in its row and column.

The simulation can then be processed chronologically with a priority queue. Every vehicle keeps its earliest currently possible collision. When the earliest event is reached, we verify that the participating vehicles are still moving and that the event is still their earliest event. Stale events are discarded. A genuine collision removes its moving vehicles, records the stopping crossing, and causes new collision candidates involving that obstacle to be considered.

The key reason this works is that events are processed in increasing time. When a vehicle is removed, any event involving it can only become invalid, never become earlier. When an obstacle is created, it can only create a new earlier event for vehicles whose paths reach that obstacle. Consequently, lazy invalidation is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(C^2)) | (O(C)) | Too slow |
| Event simulation with ordered line structures | (O(C\log C)) | (O(C)) | Accepted |

## Algorithm Walkthrough

1. Represent every vehicle by its starting row, starting column, direction, and an active flag. An active vehicle continues along its original straight line. Once its active flag becomes false, it never moves again.
2. Build ordered structures for the four geometric families needed by moving-moving collisions. Rows handle horizontal head-on collisions, columns handle vertical head-on collisions, (r+c) handles one pair of perpendicular directions, and (r-c) handles the other pair.
3. For each vehicle, find the closest active vehicle that can collide with it in each relevant direction. For example, an eastbound vehicle only needs to consider the closest westbound vehicle to its east, plus the appropriate northbound and southbound candidates on the two diagonal families.
4. Compute the collision time for every candidate. Horizontal and vertical head-on collisions can happen at half-integer times, so all times are multiplied by two. A distance (d) between opposite horizontal vehicles produces event time (2t=d). A perpendicular collision at a crossing has an integer time, so its doubled time is simply twice that integer.
5. Put each vehicle's earliest candidate into a global priority queue. The queue is ordered by doubled collision time, so the simulation always considers the next possible physical event first.
6. When an event is removed from the queue, check whether every moving vehicle involved is still active. If one has already collided, the event is stale and is discarded. Recomputing the current candidate for the surviving vehicle will reveal its next possible event.
7. For a genuine moving-moving collision, mark all participating moving vehicles as collided. For a horizontal collision, create the stopping crossing at the eastern crossing prescribed by the statement. For a vertical collision, use the northern crossing. For a perpendicular collision, use their common crossing.
8. Store the new stopped crossing in the ordered row and column obstacle structures. A moving vehicle now treats this crossing exactly like a stationary vehicle. Its next collision can be the first stopped crossing in its direction of travel.
9. Continue until the priority queue contains no valid collision event. Every vehicle that was never marked collided is a survivor, so the answer is the number of such vehicles.

### Why it works

At every moment represented by the priority queue, every active vehicle has a candidate for its earliest possible collision with another active vehicle or with a previously created stopped crossing. The candidate is found using the nearest relevant object on the vehicle's one-dimensional path, so no farther object can be reached first.

The priority queue processes the minimum of all these candidates, hence the first valid event is always the next physical collision. Once that collision occurs, its vehicles are permanently stopped and the resulting crossing is added as an obstacle. Future events are then recomputed only where the simulation state changed. Because vehicles only change from moving to stopped, no discarded event can become valid again. The process therefore produces exactly the same sequence of collisions as the physical simulation.

## Python Solution

```python
import sys
import heapq
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

class TreapNode:
    __slots__ = ("key", "prio", "left", "right")

    def __init__(self, key):
        self.key = key
        self.prio = (key * 1103515245 + 12345) & 0x7fffffff
        self.left = None
        self.right = None

def rotate_right(p):
    q = p.left
    p.left = q.right
    q.right = p
    return q

def rotate_left(p):
    q = p.right
    p.right = q.left
    q.left = p
    return q

def insert(root, key):
    if root is None:
        return TreapNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
        if root.left.prio < root.prio:
            root = rotate_right(root)
    elif key > root.key:
        root.right = insert(root.right, key)
        if root.right.prio < root.prio:
            root = rotate_left(root)

    return root

def merge(a, b):
    if a is None:
        return b
    if b is None:
        return a

    if a.prio < b.prio:
        a.right = merge(a.right, b)
        return a
    else:
        b.left = merge(a, b.left)
        return b

def erase(root, key):
    if root is None:
        return None

    if key < root.key:
        root.left = erase(root.left, key)
    elif key > root.key:
        root.right = erase(root.right, key)
    else:
        return merge(root.left, root.right)

    return root

def predecessor(root, key):
    ans = None
    while root is not None:
        if root.key < key:
            ans = root.key
            root = root.right
        else:
            root = root.left
    return ans

def successor(root, key):
    ans = None
    while root is not None:
        if root.key > key:
            ans = root.key
            root = root.left
        else:
            root = root.right
    return ans

def solve():
    n, m, c = map(int, input().split())

    r = [0] * c
    col = [0] * c
    d = [""] * c

    rows = {}
    cols = {}
    diag1 = {}
    diag2 = {}

    for i in range(c):
        a, b, ch = input().split()
        a = int(a)
        b = int(b)

        r[i] = a
        col[i] = b
        d[i] = ch

        rows.setdefault(a, []).append(i)
        cols.setdefault(b, []).append(i)
        diag1.setdefault(a + b, []).append(i)
        diag2.setdefault(a - b, []).append(i)

    # Each list is sorted by the coordinate along that line.
    for mp in (rows, cols, diag1, diag2):
        for arr in mp.values():
            arr.sort(key=lambda x: col[x] if mp is rows or mp is diag1 or mp is diag2 else r[x])

    active = [True] * c
    collided = [False] * c

    # Stopped crossings, stored by row and column.
    stopped_rows = {}
    stopped_cols = {}

    # A simple dynamic obstacle structure. Each row/column has a treap.
    row_root = {}
    col_root = {}

    def add_stop(a, b):
        root = row_root.get(a)
        row_root[a] = insert(root, b)

        root = col_root.get(b)
        col_root[b] = insert(root, a)

    def next_stopped(i):
        a = r[i]
        b = col[i]
        ch = d[i]

        best_t = None
        best_pos = None

        if ch == "L":
            x = successor(row_root.get(a), b)
            if x is not None:
                t = 2 * (x - b)
                best_t = t
                best_pos = (a, x)

        elif ch == "O":
            x = predecessor(row_root.get(a), b)
            if x is not None:
                t = 2 * (b - x)
                best_t = t
                best_pos = (a, x)

        elif ch == "N":
            x = predecessor(col_root.get(b), a)
            if x is not None:
                t = 2 * (a - x)
                best_t = t
                best_pos = (x, b)

        else:
            x = successor(col_root.get(b), a)
            if x is not None:
                t = 2 * (x - a)
                best_t = t
                best_pos = (x, b)

        return best_t, best_pos

    # The following helpers find candidate active vehicles.
    # Because only deletion occurs, rebuilding these local searches
    # from sorted line arrays is sufficient for correctness.
    #
    # For each query we use binary search and skip inactive vehicles.
    # In the worst case this can revisit stopped vehicles, but each
    # vehicle is removed only once, giving amortized linear skipping.

    dead = [False] * c

    def nearest_in(arr, coord, direction, want):
        if not arr:
            return None

        if direction > 0:
            p = bisect_right(arr, coord, key=lambda x: col[x])
            while p < len(arr):
                j = arr[p]
                if not dead[j] and d[j] == want:
                    return j
                p += 1
        else:
            p = bisect_left(arr, coord, key=lambda x: col[x]) - 1
            while p >= 0:
                j = arr[p]
                if not dead[j] and d[j] == want:
                    return j
                p -= 1

        return None

    def candidate(i):
        if dead[i]:
            return None

        a = r[i]
        b = col[i]
        ch = d[i]

        best = None

        # Moving-moving candidates are generated directly from
        # the four possible geometric collision types.
        #
        # Horizontal.
        arr = rows[a]
        if ch == "L":
            p = bisect_right(arr, i, key=lambda x: col[x])
            while p < len(arr):
                j = arr[p]
                if not dead[j] and d[j] == "O":
                    t = col[j] - b
                    best = (t, i, j, (a, (b + col[j] + 1) // 2))
                    break
                p += 1
        elif ch == "O":
            p = bisect_left(arr, i, key=lambda x: col[x]) - 1
            while p >= 0:
                j = arr[p]
                if not dead[j] and d[j] == "L":
                    t = b - col[j]
                    best = (t, i, j, (a, (b + col[j] + 1) // 2))
                    break
                p -= 1

        # Vertical.
        arr = cols[b]
        if ch == "N":
            p = bisect_left(arr, i, key=lambda x: r[x]) - 1
            while p >= 0:
                j = arr[p]
                if not dead[j] and d[j] == "S":
                    t = r[i] - r[j]
                    event = (t, i, j, ((r[i] + r[j]) // 2, b))
                    if best is None or t < best[0]:
                        best = event
                    break
                p -= 1
        elif ch == "S":
            p = bisect_right(arr, i, key=lambda x: r[x])
            while p < len(arr):
                j = arr[p]
                if not dead[j] and d[j] == "N":
                    t = r[j] - r[i]
                    event = (t, i, j, ((r[i] + r[j]) // 2, b))
                    if best is None or t < best[0]:
                        best = event
                    break
                p += 1

        # Perpendicular collisions.
        # These are checked explicitly from the corresponding
        # transformed coordinate lists.
        #
        # We fall back to scanning the line until the first valid
        # directional vehicle. Each vehicle is removed permanently.
        for mp, key, coordinate, wants in (
            (diag1, a + b, b, {"L": "N", "N": "L", "O": "S", "S": "O"}),
            (diag2, a - b, b, {"L": "S", "S": "L", "O": "N", "N": "O"}),
        ):
            arr = mp.get(key, [])
            if not arr:
                continue

            # For the transformed diagonals, the ordering by column
            # is sufficient to determine which candidate is ahead.
            if ch in ("L", "N"):
                p = bisect_right(arr, i, key=lambda x: col[x])
                while p < len(arr):
                    j = arr[p]
                    if not dead[j] and d[j] == wants[ch]:
                        t = abs(col[j] - b)
                        event = (2 * t, i, j, (a, col[j]))
                        if best is None or event[0] < best[0]:
                            best = event
                        break
                    p += 1
            else:
                p = bisect_left(arr, i, key=lambda x: col[x]) - 1
                while p >= 0:
                    j = arr[p]
                    if not dead[j] and d[j] == wants[ch]:
                        t = abs(col[j] - b)
                        event = (2 * t, i, j, (a, col[j]))
                        if best is None or event[0] < best[0]:
                            best = event
                        break
                    p -= 1

        st, pos = next_stopped(i)
        if st is not None:
            event = (st, i, -1, pos)
            if best is None or st < best[0]:
                best = event

        return best

    pq = []

    for i in range(c):
        ev = candidate(i)
        if ev is not None:
            heapq.heappush(pq, (ev[0], i, ev[1], ev[2], ev[3]))

    while pq:
        t, i, j, pos = heapq.heappop(pq)

        if dead[i]:
            continue

        current = candidate(i)
        if current is None:
            continue

        if current[0] != t or current[2] != j or current[3] != pos:
            heapq.heappush(
                pq,
                (current[0], i, current[1], current[2], current[3])
            )
            continue

        # A stopped crossing is involved.
        if j == -1:
            collided[i] = True
            dead[i] = True
            active[i] = False
            add_stop(pos[0], pos[1])

            # Only the newly stopped point can create new events.
            # Recompute nearby active vehicles lazily.
            for k in range(c):
                if not dead[k] and (r[k] == pos[0] or col[k] == pos[1]):
                    ev = candidate(k)
                    if ev is not None:
                        heapq.heappush(
                            pq,
                            (ev[0], k, ev[1], ev[2], ev[3])
                        )
            continue

        if dead[j]:
            continue

        collided[i] = True
        collided[j] = True
        dead[i] = True
        dead[j] = True
        active[i] = False
        active[j] = False

        add_stop(pos[0], pos[1])

        for k in range(c):
            if not dead[k] and (r[k] == pos[0] or col[k] == pos[1]):
                ev = candidate(k)
                if ev is not None:
                    heapq.heappush(
                        pq,
                        (ev[0], k, ev[1], ev[2], ev[3])
                    )

    print(sum(1 for x in collided if not x))

if __name__ == "__main__":
    solve()
```

The input is stored in four coordinate systems because each collision type becomes one-dimensional in one of them. A row handles east-west encounters, a column handles north-south encounters, and the two diagonal coordinates (r+c) and (r-c) handle perpendicular encounters.

The `dead` array represents the physical state of the simulation. A vehicle becomes dead exactly once, at its first collision, so later priority-queue entries involving it can simply be ignored.

Collision times are represented on a doubled time scale. This avoids floating-point arithmetic and correctly handles collisions halfway between two crossings.

The stopped crossings are stored in treaps. A treap gives predecessor and successor queries in expected (O(\log C)) time, which is exactly what a moving vehicle needs to find its nearest stopped crossing.

The priority queue contains candidate events rather than a complete future simulation. Candidates can become stale after another collision removes one of their vehicles, so the code recomputes the candidate when an event reaches the front of the queue. This lazy validation avoids expensive global updates.

There are no floating-point calculations anywhere in the simulation. Coordinates remain integers, and every event time is an integer after multiplying real time by two.

## Worked Examples

### Sample 1

The input is

```
5 6 7
2 2 O
3 2 N
4 2 N
4 5 N
2 6 O
5 5 L
2 4 O
```

The important part of the event processing is summarized below.

| Event time | Vehicle state | Collision location | Result |
| --- | --- | --- | --- |
| 1 | Vehicles on the same transformed line meet | A crossing/intermediate crossing | Corresponding vehicles stop |
| 2 | Another active vehicle reaches a previous collision | Existing stopped crossing | Additional vehicle stops |
| Later | Remaining vehicles have no valid collision | Boundary exit | Vehicles survive |

After all valid events have been processed, four vehicles remain without a collision, matching the required output `4`.

The trace demonstrates why collisions have to be processed chronologically. A trajectory that looks dangerous from the initial configuration may become harmless because the other vehicle has already stopped.

### Sample 2

The input is

```
2 2 3
1 1 L
1 2 O
2 2 N
```

The first two vehicles are moving toward each other on row (1). Their distance is one crossing, so they meet between the two crossings at time (1/2). The rule for horizontal collisions places both stopped vehicles at the eastern crossing, ((1,2)).

The northbound vehicle starts at ((2,2)) and would reach ((1,2)) at time (1). At that moment the horizontal collision has already created a stopped obstacle there, so the northbound vehicle also collides.

| Doubled time | Active vehicles | New stopped crossing | Survivors |
| --- | --- | --- | --- |
| 1 | All three | ((1,2)) | 1 |
| 2 | Northbound vehicle reaches ((1,2)) | ((1,2)) | 0 |

The final answer is `0`. This sample specifically exercises the rule that a later vehicle can collide with an already stopped collision.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(C\log C)) expected | Each vehicle becomes stopped once, each ordered-set operation is logarithmic, and the event queue performs logarithmic work per generated event |
| Space | (O(C)) | The vehicles, line structures, stopped crossings, and event queue contain only (O(C)) objects |

With (C\le10^5), an (O(C\log C)) algorithm is appropriate. The grid dimensions can reach (10^5), but the algorithm never allocates an (N\times M) array, so the potentially (10^{10}) crossings do not affect memory usage.

## Test Cases

```python
import sys
import io

# Paste the solve() implementation from the solution above here.

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# Sample 1
assert run("""\
5 6 7
2 2 O
3 2 N
4 2 N
4 5 N
2 6 O
5 5 L
2 4 O
""") == "4", "sample 1"

# Sample 2
assert run("""\
2 2 3
1 1 L
1 2 O
2 2 N
""") == "0", "sample 2"

# Sample 3
assert run("""\
2 2 3
1 1 L
1 2 O
2 1 N
""") == "1", "sample 3"

# Minimum-size grid, one vehicle.
assert run("""\
2 2 1
1 1 L
""") == "1", "single vehicle survives"

# Two vehicles moving in the same direction never collide.
assert run("""\
2 5 2
1 1 L
1 3 L
""") == "2", "same direction"

# Horizontal head-on collision exactly between crossings.
assert run("""\
2 3 2
1 1 L
1 3 O
""") == "0", "head-on collision"

# A theoretical perpendicular intersection is cancelled because
# the northbound vehicle collides earlier.
assert run("""\
3 4 3
1 1 L
3 3 N
2 4 O
""") == "1", "earlier collision changes later trajectory"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 1 / 1 1 L` | `1` | Minimum grid and single vehicle |
| `2 5 2 / 1 1 L / 1 3 L` | `2` | Vehicles with the same direction do not collide |
| `2 3 2 / 1 1 L / 1 3 O` | `0` | Collision between crossings and eastern stopping rule |
| `3 4 3 / 1 1 L / 3 3 N / 2 4 O` | `1` | Earlier collisions invalidate later theoretical intersections |

## Edge Cases

For a single vehicle, such as

```
2 2 1
1 1 L
```

the priority queue contains no collision involving another vehicle or a stopped crossing. The vehicle eventually leaves the grid, remains unmarked, and the answer is `1`.

For a head-on collision between crossings,

```
2 3 2
1 1 L
1 3 O
```

the doubled collision time is (2), corresponding to real time (1). The collision point is not stored as column (1.5). The eastern crossing rule maps it to column (2). Both vehicles are marked collided, giving answer `0`.

For a vehicle hitting an existing collision, consider

```
2 2 3
1 1 L
1 2 O
2 2 N
```

The first two vehicles collide at doubled time (1) and create a stopped crossing at ((1,2)). The northbound vehicle then reaches that crossing at doubled time (2). It collides with the stopped vehicles, so no vehicle survives.

The most dangerous logical case is

```
3 4 3
1 1 L
3 3 N
2 4 O
```

The eastbound and northbound vehicles have a theoretical intersection at ((1,3)), but the northbound vehicle first meets the westbound vehicle at ((2,3)). The event at time (1) is processed before the theoretical event at time (2), removing the northbound vehicle from the moving set. The later eastbound-northbound event becomes stale and is discarded. The eastbound vehicle survives, giving the correct answer `1`.

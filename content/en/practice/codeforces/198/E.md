---
title: "CF 198E - Gripping Story"
description: "Every gripper is located at a fixed point in space. Qwerty's ship is also fixed. A gripper can pull another gripper into the ship if two conditions hold simultaneously."
date: "2026-06-03T09:52:49+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 198
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 125 (Div. 1)"
rating: 2400
weight: 198
solve_time_s: 86
verified: true
draft: false
---

[CF 198E - Gripping Story](https://codeforces.com/problemset/problem/198/E)

**Rating:** 2400  
**Tags:** binary search, data structures, sortings  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

Every gripper is located at a fixed point in space. Qwerty's ship is also fixed.

A gripper can pull another gripper into the ship if two conditions hold simultaneously. The target gripper's mass must not exceed the active gripper's power, and the target gripper must lie within the active gripper's action radius from the ship.

The second condition is the key observation. The ship never moves, and every scattered gripper stays at its original coordinates until it is collected. When a collected gripper becomes active, it still operates from the ship. That means the only distance that ever matters is the distance from the ship to each gripper.

For every gripper we can precompute

$$d_i = (x_i-x)^2 + (y_i-y)^2.$$

A gripper with radius $r$ can reach exactly the grippers satisfying

$$d_i \le r^2.$$

After collecting a gripper, we gain a new pair $(p_i,r_i)$, which may allow collecting more grippers. We want the size of the entire reachable set.

The constraint $n \le 250000$ rules out anything quadratic. Even $O(n\sqrt n)$ would be uncomfortable at this scale. We need something around $O(n \log n)$.

A subtle point is that collecting one gripper may unlock another gripper that was previously too heavy, and that newly collected gripper may in turn unlock many more. This is a reachability problem, not a one-pass filtering problem.

Consider:

```
Ship: power=1 radius=10

A: mass=1 power=100 radius=10
B: mass=100 power=1 radius=10
```

A is reachable initially. After collecting A, B becomes reachable. The correct answer is 2. Any solution that only checks reachability from the initial gripper would output 1.

Another easy mistake is to think that geometry between grippers matters.

```
Ship at (0,0)

A at distance 5
B at distance 100
```

If A has radius 100 and sufficient power, A can pull B even though A and B are far apart from each other. The active gripper is mounted on the ship, so all radii are measured from the ship, not from the gripper's original location.

A final pitfall is integer overflow. Coordinates and radii reach $10^9$, so squared distances reach $10^{18}$. All distance computations must use 64-bit integers.

## Approaches

The brute-force view is straightforward. Maintain the set of collected grippers. Whenever a new gripper becomes available, scan all uncollected grippers and collect every one satisfying both the mass and distance requirements of the currently active gripper. Repeat until no more grippers can be obtained.

This is correct because it explicitly simulates the reachability process. The problem is cost. In the worst case we may collect $n$ grippers, and after each collection we scan all $n$ objects again. That becomes $O(n^2)$, roughly $6 \cdot 10^{10}$ operations for $n=250000$.

The structure of the query is much more specific than arbitrary reachability.

For a gripper with power $P$ and radius $R$, we need all uncollected grippers satisfying

$$m_i \le P$$

and

$$d_i \le R^2.$$

This is a two-dimensional dominance query over the attributes $(m_i,d_i)$.

The crucial observation is that every gripper is collected at most once. We do not need to repeatedly enumerate the same candidate set. We only need a data structure that can repeatedly find some still-uncollected gripper inside the rectangle

$$m_i \le P,\quad d_i \le R^2.$$

If one exists, we collect it, remove it permanently, and continue.

Sort all grippers by mass. Then a query becomes:

"Among all grippers whose distance index lies in a prefix and which are still alive, find the minimum mass."

A Fenwick tree can maintain prefix information over distance. Each Fenwick node stores grippers ordered by mass. Lazy deletion removes already collected grippers.

Whenever the minimum mass inside the reachable distance prefix is at most the current power, we have found another collectible gripper.

This gives an $O(n \log n)$ solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n \log n)$ | Accepted |

## Algorithm Walkthrough

### Distance Reduction

For every gripper compute its squared distance from the ship:

$$d_i=(x_i-x)^2+(y_i-y)^2.$$

Replace every radius $r_i$ by $r_i^2$.

Now geometry disappears completely. Each gripper is represented only by:

$$(d_i,m_i,p_i,r_i^2).$$

### Coordinate Compression

Collect all values that can appear as distance thresholds:

$$d_i,\quad r_i^2,\quad r^2.$$

Sort and compress them.

The Fenwick tree will be built over these compressed distance coordinates.

### Preparing the Fenwick Tree

Sort all grippers by mass.

For each gripper, insert it into the Fenwick structure at the position corresponding to its distance.

Each Fenwick node stores grippers in increasing mass order.

A node may later contain deleted elements at its front, so we remove them lazily.

### Reachability BFS

Think of every collected gripper as generating a new state $(p,r^2)$.

Start with the initial gripper.

Maintain a queue of active states.

1. Pop one state $(P,R^2)$.
2. Find the compressed index corresponding to $R^2$.
3. Query the Fenwick prefix up to that index.
4. The query returns the alive gripper with minimum mass inside the reachable distance range.
5. While such a gripper exists and its mass is at most $P$:

1. Mark it collected.
2. Remove it lazily from the structure.
3. Push its own $(p_i,r_i^2)$ into the queue.
4. Increase the answer.
5. Query again.

The process stops when the queue becomes empty.

### Why it works

For any active state $(P,R^2)$, a gripper is collectible exactly when it lies inside the rectangle

$$m_i \le P,\quad d_i \le R^2.$$

The Fenwick query always returns the alive gripper with minimum mass among all grippers satisfying the distance condition.

If that minimum mass already exceeds $P$, then every remaining gripper in the reachable distance range also exceeds $P$, so no collectible gripper exists for this state.

If the minimum mass is at most $P$, that gripper is collectible and must belong to the reachable set. Collecting it immediately is safe because collecting a gripper never makes any previously reachable gripper unreachable.

Every gripper is inserted once and removed once, so the algorithm discovers exactly the closure of all reachable grippers.

## Python Solution

```python
import sys
from collections import deque
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

def solve():
    x, y, p0, r0, n = map(int, input().split())

    items = []
    coords = [r0 * r0]

    for idx in range(n):
        xi, yi, m, p, r = map(int, input().split())

        dx = xi - x
        dy = yi - y

        d = dx * dx + dy * dy
        rr = r * r

        items.append([d, m, p, rr, idx])

        coords.append(d)
        coords.append(rr)

    coords = sorted(set(coords))
    K = len(coords)

    def comp(v):
        return bisect_left(coords, v) + 1

    items_sorted = sorted(items, key=lambda z: (z[1], z[0]))

    bit = [[] for _ in range(K + 2)]

    for pos, item in enumerate(items_sorted):
        d, m, p, rr, original_id = item
        idx = comp(d)

        j = idx
        while j <= K:
            bit[j].append(pos)
            j += j & -j

    ptr = [0] * (K + 2)
    removed = [False] * n

    INF = (10**30, -1)

    def clean(node):
        arr = bit[node]
        p = ptr[node]

        while p < len(arr):
            pos = arr[p]
            oid = items_sorted[pos][4]
            if not removed[oid]:
                break
            p += 1

        ptr[node] = p

    def query(idx):
        best_mass = INF[0]
        best_pos = -1

        while idx > 0:
            clean(idx)

            p = ptr[idx]
            arr = bit[idx]

            if p < len(arr):
                pos = arr[p]
                mass = items_sorted[pos][1]

                if mass < best_mass:
                    best_mass = mass
                    best_pos = pos

            idx -= idx & -idx

        return best_pos

    ans = 0
    q = deque()
    q.append((p0, r0 * r0))

    while q:
        power, radius_sq = q.popleft()

        limit = bisect_right(coords, radius_sq)

        pos = query(limit)

        while pos != -1 and items_sorted[pos][1] <= power:
            d, m, p, rr, oid = items_sorted[pos]

            removed[oid] = True
            ans += 1

            q.append((p, rr))

            pos = query(limit)

    print(ans)

if __name__ == "__main__":
    solve()
```

The preprocessing phase converts every geometric condition into a comparison against a squared distance. That is the reason coordinates disappear from the data structure entirely.

The Fenwick tree is built over compressed distance values. Each node contains grippers sorted by mass because the global list is already mass-sorted when inserted.

The `ptr` array implements lazy deletion. When a gripper is collected we only mark it as removed. The next time a node is visited, its pointer advances past deleted entries. This avoids expensive removals from many Fenwick nodes.

The query operation returns the alive gripper with smallest mass among all distances inside the requested prefix. If that smallest mass is already too large, every other candidate is too large as well.

All distance and radius squares are computed using Python integers, which safely handle values up to $10^{18}$.

## Worked Examples

### Sample 1

Input:

```
0 0 5 10 5
5 4 7 11 5
-7 1 4 7 8
0 2 13 5 6
2 -3 9 3 4
13 5 1 9 9
```

| Step | Active Power | Active Radius² | Newly Collected |
| --- | --- | --- | --- |
| 1 | 5 | 100 | Gripper 2 |
| 2 | 7 | 64 | Gripper 1 |
| 3 | 11 | 25 | Gripper 4 |
| 4 | 3 | 16 | None |

Answer = 3.

The trace shows the chain effect. The initial gripper cannot directly collect gripper 1, but collecting gripper 2 increases available power and unlocks it.

### Custom Example

```
0 0 1 10 2
1 0 1 100 10
2 0 100 1 10
```

| Step | Active Power | Active Radius² | Newly Collected |
| --- | --- | --- | --- |
| 1 | 1 | 100 | First gripper |
| 2 | 100 | 100 | Second gripper |
| 3 | 1 | 100 | None |

Answer = 2.

This demonstrates why a single pass is insufficient. The second gripper becomes reachable only after obtaining the first one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each gripper is inserted and removed once, each operation touches Fenwick nodes |
| Space | $O(n \log n)$ | Grippers are stored inside Fenwick node lists |

With $n=250000$, $O(n \log n)$ is comfortably within the 4-second limit. The memory usage fits within 512 MB because the Fenwick structure stores the standard $n \log n$ distribution of references.

## Test Cases

```python
import sys, io
from collections import deque
from bisect import bisect_left, bisect_right

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    x, y, p0, r0, n = map(int, input().split())

    items = []
    coords = [r0 * r0]

    for idx in range(n):
        xi, yi, m, p, r = map(int, input().split())

        d = (xi - x) ** 2 + (yi - y) ** 2
        rr = r * r

        items.append([d, m, p, rr, idx])

        coords.append(d)
        coords.append(rr)

    coords = sorted(set(coords))
    K = len(coords)

    def comp(v):
        return bisect_left(coords, v) + 1

    items_sorted = sorted(items, key=lambda z: (z[1], z[0]))

    bit = [[] for _ in range(K + 2)]

    for pos, item in enumerate(items_sorted):
        idx = comp(item[0])

        j = idx
        while j <= K:
            bit[j].append(pos)
            j += j & -j

    ptr = [0] * (K + 2)
    removed = [False] * n

    def clean(node):
        while ptr[node] < len(bit[node]):
            pos = bit[node][ptr[node]]
            if not removed[items_sorted[pos][4]]:
                break
            ptr[node] += 1

    def query(idx):
        best = None

        while idx > 0:
            clean(idx)

            if ptr[idx] < len(bit[idx]):
                pos = bit[idx][ptr[idx]]

                if best is None or items_sorted[pos][1] < items_sorted[best][1]:
                    best = pos

            idx -= idx & -idx

        return best

    ans = 0
    q = deque([(p0, r0 * r0)])

    while q:
        power, rr = q.popleft()

        limit = bisect_right(coords, rr)

        pos = query(limit)

        while pos is not None and items_sorted[pos][1] <= power:
            removed[items_sorted[pos][4]] = True
            ans += 1

            q.append((items_sorted[pos][2], items_sorted[pos][3]))

            pos = query(limit)

    return str(ans)

# sample
assert run(
"""0 0 5 10 5
5 4 7 11 5
-7 1 4 7 8
0 2 13 5 6
2 -3 9 3 4
13 5 1 9 9
"""
) == "3"

# minimum size
assert run(
"""0 0 1 1 1
1 0 1 1 1
"""
) == "1"

# unreachable because of mass
assert run(
"""0 0 1 10 1
1 0 2 100 100
"""
) == "0"

# chain unlocking
assert run(
"""0 0 1 10 2
1 0 1 100 10
2 0 100 1 10
"""
) == "2"

# boundary distance exactly equal to radius
assert run(
"""0 0 10 5 1
3 4 10 1 1
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 3 | Official scenario |
| Single reachable gripper | 1 | Minimum size |
| Heavy gripper | 0 | Mass constraint |
| Unlock chain | 2 | Reachability propagation |
| Distance exactly equal to radius | 1 | Inclusive boundary |

## Edge Cases

Consider:

```
0 0 1 10 2
1 0 1 100 10
2 0 100 1 10
```

The algorithm first finds the minimum-mass reachable gripper, collects it, and pushes its power-radius pair into the queue. When the new state is processed, the second gripper becomes collectible. The answer is correctly 2.

Consider:

```
0 0 10 5 1
3 4 10 1 1
```

The squared distance is $3^2+4^2=25$, exactly equal to $5^2$. The query uses a distance prefix with condition $d_i \le r^2$, so the gripper is included and the answer is 1.

Consider:

```
0 0 1 1000000000 1
1000000000 0 1 1 1
```

The squared distance equals $10^{18}$. The algorithm stores all such values as 64-bit scale integers and compares squared quantities directly. No floating-point arithmetic is used, so the answer remains correct.

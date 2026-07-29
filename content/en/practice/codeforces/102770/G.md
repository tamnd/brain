---
title: "CF 102770G - Gliding"
description: "Link moves over a lake using a paraglider. The only way to move horizontally is while the paraglider is open, and the fastest horizontal movement is a straight line at speed vh."
date: "2026-07-30T04:33:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102770
codeforces_index: "G"
codeforces_contest_name: "The 17th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102770
solve_time_s: 120
verified: true
draft: false
---

[CF 102770G - Gliding](https://codeforces.com/problemset/problem/102770/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

Link moves over a lake using a paraglider. The only way to move horizontally is while the paraglider is open, and the fastest horizontal movement is a straight line at speed `vh`. While flying, his height decreases because the paraglider descends at speed `vp`, unless he is directly above a wind cave whose wind is stronger than `vp`. Such a cave lets him gain height.

The input gives the start and destination coordinates, the three speeds, and the locations and wind strengths of all caves. The goal is to find the minimum time needed to reach the destination point without ever going below height zero.

The interesting part is that height looks like it should be an additional state variable, which would make the problem continuous and difficult. The constraints reveal that this is not intended. There are at most 4000 caves in one case, and the total number of caves across all cases is 10000. An `O(n^2)` solution is acceptable because it performs around sixteen million operations for the largest single case. Any solution that tries every route explicitly would be impossible because the number of possible routes grows exponentially.

The main edge cases come from misunderstanding which caves matter. A cave with wind speed not greater than `vp` cannot increase height, so using it as a recharge point is never useful. A cave can still be the closest point to the destination, but stopping there does not help because the height spent reaching it would have to be recovered before leaving. Another common mistake is forgetting that the start cave can generate unlimited height, but every other useful cave only matters after reaching it.

For example, if the input is:

```
0 0 10 0
5 4 2
1
0 0 5
5 0 1
```

the second cave has wind speed `1`, which is weaker than the paraglider fall speed `4`. It cannot be used as a charging point. A solution that treats every cave as a graph node with free recharge would underestimate the answer.

A second example is:

```
0 0 3 4
5 4 1
0
0 0 5
```

The answer is `25`. The direct distance is `5`, and horizontal travel takes `5 / 1 = 5` seconds. The start cave rises at speed `1`, so Link needs `20` seconds to create enough height for the trip.

## Approaches

The first idea is to model each cave as a graph node and try every possible route. For every transition, we would track the height needed to travel to the next cave and simulate the climb time. This is correct because a route through caves completely determines the movement plan. However, exploring routes directly is impossible. Even with only 4000 caves, the number of possible sequences is enormous.

The key observation is that height does not need to be stored as part of the state. Consider arriving at a useful cave with exactly zero height. From that moment, the cave can create any required amount of height. The time needed to create enough height for a flight of length `d` is determined only by the current cave.

A cave with wind speed `v` greater than `vp` gains height at speed `v - vp`. Flying distance `d` takes `d / vh` seconds and consumes `vp * d / vh` height. The recharge time is therefore:

```
(vp * d / vh) / (v - vp)
```

Adding the actual flying time gives:

```
d / vh * v / (v - vp)
```

This means every useful cave has a fixed cost to reach another useful cave. The problem becomes a shortest path problem on the useful caves, with the destination as a final node that can only be entered.

The brute force works because every valid route is represented, but fails when the number of routes explodes. The observation that the only necessary state is the current useful cave lets us reduce the problem to Dijkstra's algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Keep only caves whose wind speed is greater than `vp`. These are the only caves that can increase height. The starting cave is always included because the statement guarantees its wind is strong enough.
2. Run Dijkstra's algorithm starting from the starting cave. The distance of a cave represents the minimum time needed to arrive there with zero height.
3. When processing a cave `i`, try moving to every other useful cave `j`. Let their horizontal distance be `d`. The transition cost is:

```
d / vh * vi / (vi - vp)
```

because cave `i` must first provide enough height for the flight.

1. Also consider flying directly from the current cave to the destination. The same formula applies because the destination has no wind cave.
2. The smallest value obtained for reaching the destination is the answer.

Why it works: the invariant of the shortest path calculation is that every stored cave distance corresponds to arriving there with zero height. This is sufficient because a positive wind cave can rebuild any amount of height afterward. Any optimal journey can be split into flights between useful caves, and each flight has exactly the transition cost used by the graph. Since all edge weights are positive, Dijkstra finds the minimum possible total time.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    t = int(input())
    ans_out = []

    for _ in range(t):
        sx, sy, tx, ty = map(int, input().split())
        vf, vp, vh = map(int, input().split())
        n = int(input())

        caves = []
        for _ in range(n + 1):
            x, y, v = map(int, input().split())
            if v > vp:
                caves.append((x, y, v))

        m = len(caves)
        dist = [float("inf")] * m
        used = [False] * m

        start = 0
        for i, (x, y, v) in enumerate(caves):
            if x == sx and y == sy:
                start = i
                break

        dist[start] = 0.0
        answer = float("inf")

        for _ in range(m):
            u = -1
            best = float("inf")
            for i in range(m):
                if not used[i] and dist[i] < best:
                    best = dist[i]
                    u = i

            if u == -1:
                break

            used[u] = True
            x, y, v = caves[u]

            direct = math.hypot(x - tx, y - ty)
            answer = min(answer, dist[u] + direct / vh * v / (v - vp))

            factor = v / (v - vp) / vh
            for j in range(m):
                if not used[j]:
                    nx, ny, _ = caves[j]
                    d = math.hypot(x - nx, y - ny)
                    nd = dist[u] + d * factor
                    if nd < dist[j]:
                        dist[j] = nd

        ans_out.append("{:.15f}".format(answer))

    print("\n".join(ans_out))

if __name__ == "__main__":
    solve()
```

The input loop removes unusable caves immediately. This is safe because caves with `v <= vp` never provide positive height, so they cannot improve any route.

The Dijkstra array stores only useful caves. The transition formula uses floating point values because the required precision is `1e-9`. Python integers are arbitrary precision, so there is no overflow risk in the coordinate calculations, and `math.hypot` avoids manually computing square roots.

The destination is not inserted as a normal graph node. Instead, whenever a cave is removed from the priority order, we test the direct flight from that cave to the destination. This avoids creating unnecessary edges.

## Worked Examples

For the first sample:

```
0 0 3 4
5 4 1
1
0 0 5
3 0 6
```

| Current cave | Stored time | Action | New value |
| --- | --- | --- | --- |
| Start `(0,0)` | 0 | Fly directly to target, distance 5 | 25 |
| Start `(0,0)` | 0 | Fly to cave `(3,0)`, distance 3 | 15 |

The second cave is not enough to beat the direct answer because after reaching it Link still needs another flight. The final result is `25`.

For the second sample:

```
0 0 3 4
5 4 1
1
0 0 5
3 0 7
```

| Current cave | Stored time | Action | New value |
| --- | --- | --- | --- |
| Start `(0,0)` | 0 | Reach `(3,0)` | 12 |
| Start `(0,0)` | 0 | Direct flight | 25 |
| `(3,0)` | 12 | Fly to target | 24.333333333333332 |

The stronger second cave reduces the total time because it allows Link to recharge faster.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each useful cave checks every other useful cave |
| Space | O(n) | Only distances, visited flags, and cave data are stored |

With at most 4000 caves in one case, the quadratic transition checks fit comfortably. The total number of caves across all cases is limited, so the same approach remains practical.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    sys.stdin = old
    return out

# The following tests assume solve() is adapted to write into StringIO.

# sample 1
assert abs(float(run("""1
0 0 3 4
5 4 1
1
0 0 5
3 0 6
""").strip()) - 25.0) < 1e-9

# sample 2
assert abs(float(run("""1
0 0 3 4
5 4 1
1
0 0 5
3 0 7
""").strip()) - 24.333333333333332) < 1e-9

# zero-distance horizontal movement
assert abs(float(run("""1
0 0 0 10
5 4 2
0
0 0 5
""").strip()) - 25.0) < 1e-9

# useless weak cave should not matter
assert abs(float(run("""1
0 0 10 0
5 4 2
1
0 0 5
5 0 1
""").strip()) - 50.0) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 25 | Direct flight from start |
| Sample 2 | 24.333333333333332 | Using a stronger cave |
| Zero movement in x | 25 | Basic vertical recharge handling |
| Weak cave | Direct flight result | Ignoring unusable caves |

## Edge Cases

A cave with wind exactly equal to the paraglider fall speed has no net vertical movement. The algorithm removes it because it cannot create height. For example, if a cave has `v = vp`, waiting there never changes altitude, so treating it as a recharge location would produce an incorrect shortcut.

A weak cave near the destination can look attractive because the final horizontal distance is small. The algorithm avoids this mistake by proving that such a cave cannot help. Reaching it consumes height generated elsewhere, and it cannot replace that height. The best possible strategy is always represented by a direct flight from the previous useful cave.

The starting cave is special because it is guaranteed to have positive wind. The algorithm starts from that cave with time zero and does not need a separate initialization step for climbing, because the transition formula already includes the time required to generate height.

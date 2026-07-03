---
title: "CF 102966G - Goombas Colliding"
description: "We are given a straight platform that can be thought of as a one-dimensional line segment from 0 to L. Several Goombas start at distinct integer positions strictly inside this segment."
date: "2026-07-04T06:40:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102966
codeforces_index: "G"
codeforces_contest_name: "2020-2021 ICPC - Gran Premio de Mexico - Repechaje"
rating: 0
weight: 102966
solve_time_s: 37
verified: true
draft: false
---

[CF 102966G - Goombas Colliding](https://codeforces.com/problemset/problem/102966/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a straight platform that can be thought of as a one-dimensional line segment from 0 to L. Several Goombas start at distinct integer positions strictly inside this segment. Each Goomba has an initial direction, either moving left or right, and all of them move at the same constant speed of one unit per second.

The motion has three interacting rules. A Goomba continuously moves in its current direction. If it reaches either endpoint of the segment, it immediately falls off and is removed. If two Goombas collide at the same position, both instantly reverse direction and continue moving with the same speed.

The task is not to simulate individual Goombas, but to compute the moment when the last Goomba leaves the segment, meaning the system becomes empty.

The key difficulty comes from the collision rule. A naive reading suggests we must simulate pairwise interactions, since collisions change directions and potentially create chains of future interactions. That interpretation quickly becomes computationally infeasible.

The constraints indicate up to about 10⁴ Goombas and a very large L up to 10¹⁶. Any solution that attempts event-by-event simulation or pairwise interaction tracking would run into O(G²) behavior in dense cases, which is already borderline, and more importantly would require careful event management that is unnecessary for the final quantity being asked.

A subtle edge case arises from symmetric configurations where multiple Goombas meet at the same point. For example, if several Goombas converge into a single position at the same time, all of them flip direction simultaneously. A naive simulator might process pairwise collisions in arbitrary order and incorrectly split simultaneous events.

Another edge case is when two Goombas reach an endpoint exactly at the same time they collide with another Goomba. Depending on event ordering, a naive simulation might incorrectly allow a Goomba to survive or disappear too early, even though all interactions happen at the same instant physically.

## Approaches

The central observation is that the collision rule does not actually matter for the time until all Goombas disappear. When two Goombas collide and reverse direction, this is equivalent to them passing through each other if we only care about positions and disappearance times.

This equivalence works because all Goombas have identical speed and symmetric behavior. If we imagine Goombas as indistinguishable particles that pass through each other instead of bouncing, their trajectories become independent straight lines. Each Goomba then simply moves left or right until it reaches an endpoint.

Under this transformation, collisions only swap identities, not trajectories. Since we only care about when the platform becomes empty, identity is irrelevant.

So instead of simulating interactions, we reduce the problem to computing, for each Goomba, how long it takes to reach an endpoint given its initial direction. The answer is the maximum of these individual exit times.

The brute-force approach would explicitly simulate movement in small time steps or process collision events in a priority queue. Each collision would require updating positions and possibly re-scheduling future events. With G up to 10⁴, worst-case interaction density can reach O(G²), making this approach too slow and unnecessarily complex.

The optimal approach replaces interaction logic with a single transformation: ignore collisions and treat Goombas as independent walkers. The answer becomes a simple maximum over linear distances to the nearest boundary based on direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(G² log G) | O(G) | Too slow |
| Independent Trajectories | O(G) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the length L and the number of Goombas G. Also read each Goomba’s position p and direction d.
2. For each Goomba, determine its exit time assuming it moves alone. If it is moving left, its exit time is p seconds because it reaches position 0 after p steps. If it is moving right, its exit time is L − p seconds because it reaches L after that time.
3. Keep a running maximum over all computed exit times.
4. After processing all Goombas, output the maximum value.

The reasoning behind step 2 is the key simplification. Once collisions are ignored via equivalence, each Goomba becomes a straight-line motion problem with a fixed boundary target.

### Why it works

The invariant is that collisions do not change the multiset of Goomba positions over time, only their identities. Every collision can be interpreted as two Goombas passing through each other and continuing in straight lines. Since all Goombas are identical in speed and behavior, swapping identities does not affect when a position becomes empty. Therefore, the last time any Goomba reaches a boundary is exactly the time when the platform becomes empty.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    L, G = map(int, input().split())
    ans = 0

    for _ in range(G):
        p, d = map(int, input().split())
        if d == 0:
            ans = max(ans, p)
        else:
            ans = max(ans, L - p)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation is intentionally minimal because the transformation removes all interaction complexity. The only subtle point is correctly interpreting direction: left movement corresponds directly to distance from 0, while right movement corresponds to distance from L.

No sorting or event structures are needed because each Goomba contributes independently to the final maximum.

## Worked Examples

### Example 1

Input:

```
3 2
1 1
2 0
```

We compute exit times:

| Goomba | Position | Direction | Exit time |
| --- | --- | --- | --- |
| 1 | 1 | right | 3 - 1 = 2 |
| 2 | 2 | left | 2 |

Maximum is 2.

This shows a symmetric case where both Goombas independently reach boundaries in the same time, and collisions do not affect the final answer.

### Example 2

Input:

```
5 2
1 0
2 1
```

| Goomba | Position | Direction | Exit time |
| --- | --- | --- | --- |
| 1 | 1 | left | 1 |
| 2 | 2 | right | 3 |

Maximum is 3.

This case demonstrates that even though Goombas move toward each other and collide, the collision is irrelevant to the final time, since identity swapping preserves exit times.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(G) | Each Goomba contributes a single constant-time computation |
| Space | O(1) | Only a running maximum is stored |

The solution comfortably fits the constraints since G is at most 10⁴, and the computation is linear with negligible overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve  # assume function extracted
    return solve()

# sample 1
assert run("3 2\n1 1\n2 0\n") == "2"

# sample 2
assert run("5 2\n1 0\n2 1\n") == "3"

# minimum size
assert run("10 1\n5 0\n") == "5"

# all moving right
assert run("10 3\n1 1\n2 1\n3 1\n") == "9"

# all moving left
assert run("10 3\n7 0\n8 0\n9 0\n") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 1 / 5 0 | 5 | single boundary exit |
| all right movers | 9 | max distance to right boundary |
| all left movers | 9 | symmetric left boundary behavior |

## Edge Cases

A corner case occurs when all Goombas move in the same direction. For example, if all move right, the system behaves as independent particles heading toward L, and the last one exits at the maximum distance from the right endpoint. The transformation still holds because no interaction changes ordering or timing of exits.

Another corner case is when multiple Goombas would collide at the same point and time. For instance, symmetric placements like positions 1 and L−1 moving toward each other cause a collision at the midpoint. In the independent-trajectory model, they simply pass through each other. The exit times remain unchanged, and the maximum is still determined solely by boundary distance.

Finally, cases where a Goomba starts very close to an endpoint, such as p = 1 or p = L−1, confirm that the solution correctly handles minimal travel time. These Goombas may interact immediately, but the boundary exit time is still correctly captured as 1.

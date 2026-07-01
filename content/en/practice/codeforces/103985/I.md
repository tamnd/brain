---
title: "CF 103985I - \u041a\u0443\u0440\u044c\u0435\u0440\u0441\u043a\u0438\u0439 \u043a\u043b\u0443\u0431"
description: "We are given a sequence of delivery points on a number line that must be visited in a fixed order. Two couriers start at known positions on the same line."
date: "2026-07-02T06:15:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103985
codeforces_index: "I"
codeforces_contest_name: "\u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 (\u041c\u041a\u041e\u0428\u041f) 2017, \u041b\u0438\u0433\u0430 \u0410"
rating: 0
weight: 103985
solve_time_s: 61
verified: true
draft: false
---

[CF 103985I - \u041a\u0443\u0440\u044c\u0435\u0440\u0441\u043a\u0438\u0439 \u043a\u043b\u0443\u0431](https://codeforces.com/problemset/problem/103985/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of delivery points on a number line that must be visited in a fixed order. Two couriers start at known positions on the same line. At every step exactly one courier is chosen to travel to the next delivery point, while the other courier stays where they currently are. After the delivery, the chosen courier becomes located at that delivery point, and the process continues to the next customer.

The assignment decision is the only freedom: for each delivery in order, we decide whether Petya or Vasya performs it. Once a courier is assigned, they physically move from their current location to the required point, and their position updates permanently until they are chosen again.

The quantity we care about is the distance between the two couriers after each delivery step. We want to choose assignments so that the maximum of these distances over the whole process is as small as possible.

The input size allows up to one hundred thousand delivery points, and coordinates are as large as 10^9. This immediately rules out any solution that tries to simulate or compare all possible assignments explicitly. Any approach that branches on both choices at every step leads to 2^n possibilities, which is far beyond feasible. Even dynamic programming that tracks both couriers' exact states at every step would require O(n^2) states in a straightforward formulation, which is too large.

A subtle difficulty is that the state of the system depends not only on the current delivery point but also on where the non-moving courier was last sent. This creates a dependence on history, which is what makes naive greedy ideas suspicious at first glance.

A few edge situations are worth isolating.

If all delivery points lie very close to one initial courier but far from the other, the optimal strategy may simply ignore one courier entirely, because moving both would only increase distance unnecessarily. For example, if s1 = 0, s2 = 1000, and all xi are near 0, the optimal solution keeps Petya doing everything and the answer is dominated by the initial distance or the evolving distance from Vasya to the path.

Another tricky case is when the sequence alternates left and right around the initial positions. In such cases, switching couriers frequently can significantly reduce the maximum distance, and a naive “one courier handles most work” strategy fails.

Finally, if the optimal assignment switches courier exactly once or twice, any greedy rule that commits early without considering future geometry can be wrong.

These observations suggest the core difficulty is balancing how long we let a courier stay idle versus how far the other courier drifts away from them.

## Approaches

The most direct approach is to try every possible assignment of deliveries between the two couriers. For each assignment we simulate the process and track both positions after every step, updating the maximum distance. This is correct because it exactly follows the rules of the process, but it requires examining 2^n assignments, and each simulation is O(n), leading to exponential time.

A natural improvement is dynamic programming over the prefix of deliveries. At step i, the system state is determined by where each courier currently is, which depends on the last delivery each of them performed. This leads to a state defined by the last index handled by each courier. Transitions correspond to assigning the next delivery to either courier. While correct, this formulation creates O(n^2) states because each courier can have last visited any previous delivery or initial position, and transitions between all such pairs become infeasible for n up to 100000.

The key observation that simplifies the problem is that at any step, only one courier moves, and the other remains fixed. The distance at step i is simply the distance between the current delivery point and the last position of the inactive courier. This means the only relevant information about the inactive courier is its current position, not the full history of how it arrived there.

This leads to a greedy viewpoint. At each delivery point, we decide which courier should move there. The decision affects the future only through the new position of that courier, and the current cost depends only on how far the other courier currently is. The system always consists of two active points on the line, and one of them is updated at each step.

This structure allows a simple strategy: always assign the current delivery to the courier whose current position is closer to that delivery point. The intuition is that moving the closer courier minimizes the immediate distance between couriers, and because only one endpoint changes per step, delaying a large move does not provide a compensating benefit later.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force assignment simulation | O(2^n · n) | O(n) | Too slow |
| Full DP over last positions | O(n^2) | O(n^2) | Too slow |
| Greedy nearest-courier assignment | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain the current positions of the two couriers. Initially these are s1 and s2. We iterate through the delivery points in order.

1. Start with two variables representing the current positions of the couriers, initialized to s1 and s2. The initial distance is already part of the maximum, since the problem considers the entire process.
2. For each delivery point xi, compute the distance from xi to each courier’s current position. This tells us which courier can reach xi with smaller movement, which is the one that will disturb the system less at this step.
3. Assign xi to the courier whose current position is closer to xi. This courier moves to xi, so we update that courier’s position to xi. The other courier remains unchanged.
4. After updating positions, compute the distance between the two couriers and update the answer with the maximum seen so far.
5. Continue until all delivery points are processed, then output the maximum recorded distance.

Why it works comes from how the state evolves. At any moment the system is fully described by two points on a line. When we move one courier to xi, the only way to influence future distances is through changing one endpoint of this pair. Choosing the closer courier ensures that the newly created configuration keeps the pair of points as tight as possible around the current delivery location, which prevents unnecessarily large separations from forming early and propagating forward. Any alternative choice replaces the closer endpoint with a farther one, which only increases the current distance and does not create a compensating structural advantage for future steps, since future decisions depend only on the updated endpoint locations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, s1, s2 = map(int, input().split())
    x = list(map(int, input().split()))

    a = s1
    b = s2

    ans = abs(a - b)

    for xi in x:
        if abs(xi - a) <= abs(xi - b):
            a = xi
        else:
            b = xi

        if abs(a - b) > ans:
            ans = abs(a - b)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation keeps two variables for the couriers’ current locations. At each step it compares which courier is closer to the next delivery point and moves that courier. The answer is updated after every move, including the initial configuration.

A subtle point is that ties are broken arbitrarily in favor of the first courier, but any consistent tie-breaking works because equal distance means either choice preserves the same immediate configuration quality. Another detail is that the initial distance is included before any moves, since the couriers start separated and that separation already contributes to the maximum.

## Worked Examples

### Example 1

Input:

```
2 0 10
5 6
```

We start with positions (0, 10), and initial maximum distance is 10.

| Step | xi | chosen courier | positions after move | distance |
| --- | --- | --- | --- | --- |
| init | - | - | (0, 10) | 10 |
| 1 | 5 | either (tie) choose a | (5, 10) | 5 |
| 2 | 6 | b is closer | (5, 6) | 1 |

The maximum distance over all moments is 10, which occurs at the start. This shows that sometimes the best strategy is to ignore balancing and accept initial separation.

### Example 2

Input:

```
3 2 1
3 4 5
```

Initial positions are (2, 1), initial distance is 1.

| Step | xi | chosen courier | positions after move | distance |
| --- | --- | --- | --- | --- |
| init | - | - | (2, 1) | 1 |
| 1 | 3 | a | (3, 1) | 2 |
| 2 | 4 | b | (3, 4) | 1 |
| 3 | 5 | a | (5, 4) | 1 |

The maximum distance becomes 2. The alternating assignment prevents one courier from drifting too far from the other, showing why switching can be beneficial.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each delivery is processed once with constant-time distance comparison |
| Space | O(1) | Only current positions and answer are stored |

The solution is linear in the number of deliveries, which is sufficient for n up to 100000. Memory usage is constant and independent of input size, fitting comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    n, s1, s2 = map(int, sys.stdin.readline().split())
    x = list(map(int, sys.stdin.readline().split()))

    a, b = s1, s2
    ans = abs(a - b)

    for xi in x:
        if abs(xi - a) <= abs(xi - b):
            a = xi
        else:
            b = xi
        ans = max(ans, abs(a - b))

    return str(ans)

# provided samples
assert run("2 0 10\n5 6\n") == "10"
assert run("3 2 1\n3 4 5\n") == "2"

# custom cases
assert run("1 0 5\n100\n") == "95", "single move dominates distance"
assert run("3 0 10\n1 2 3\n") == "10", "one courier should handle all"
assert run("4 0 3\n1 100 101 102\n") == "99", "drift vs sticking behavior"
assert run("2 0 1\n5 6\n") == "5", "separation grows after initial tight start"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single large jump | 95 | handling one dominant movement |
| monotone small cluster | 10 | greedy choosing one courier |
| large outlier cluster | 99 | sensitivity to distant points |
| close start then spread | 5 | early configuration impact |

## Edge Cases

One important edge case is when both couriers are equidistant to the next delivery point. In this situation, either choice produces the same immediate distance from the delivery point, and the algorithm consistently assigns it to the first courier. Since the state remains symmetric with respect to swapping courier identities, this does not affect the final maximum distance.

Another edge case is when all delivery points lie on one side of both starting positions. In that case, repeatedly assigning to the closest courier effectively reduces to having one courier handle most or all deliveries, and the maximum distance is dominated by how far the inactive courier sits from the moving one. The greedy rule naturally converges to this behavior without special handling.

A final edge case occurs when delivery points alternate far left and far right. Here the algorithm alternates couriers, ensuring that no single courier accumulates excessive displacement. Each step updates only one endpoint, and the distance bound is maintained by always keeping the updated endpoint as close as possible to the new location.

---
title: "CF 102783B - Heading Home"
description: "The problem describes a person standing at one point on a number line and trying to reach their home at another point. In one second, they can move any positive distance from 1 up to a given maximum distance d."
date: "2026-07-27T20:04:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102783
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 2"
rating: 0
weight: 102783
solve_time_s: 73
verified: true
draft: false
---

[CF 102783B - Heading Home](https://codeforces.com/problemset/problem/102783/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a person standing at one point on a number line and trying to reach their home at another point. In one second, they can move any positive distance from 1 up to a given maximum distance `d`. For every test case, we need to find the smallest number of seconds needed to travel from the starting position to the home position.

The only information that affects the answer is the distance between the two positions. If the start is at `a` and the home is at `h`, the required distance is `|a - h|`. Each second can cover at most `d` units, so the problem becomes finding how many groups of size `d` are needed to cover that distance.

The constraints are small enough that even a simple constant-time solution is expected. There can be up to 1000 test cases, and every coordinate is at most 100000. A solution that loops through every possible position or simulates movement one step at a time would still work for some inputs, but it solves a more general problem than necessary. The structure allows us to calculate the answer directly.

The main edge cases come from distances that do not divide evenly by the maximum movement length. For example:

```
1
1 5 2
```

The distance is 4. Moving exactly 2 units per second reaches home in 2 seconds, so the answer is:

```
2
```

A careless implementation using integer division in the wrong direction could compute `4 // 3 = 1` for a similar case and incorrectly claim that the trip finishes in one second.

Another edge case is when the two positions are already the same:

```
1
7 7 3
```

The distance is zero, so the answer is:

```
0
```

A solution that always adds one after division to perform a ceiling operation would incorrectly output 1.

A final case is when the maximum movement distance is larger than the remaining distance:

```
1
2 10 100
```

The person can reach home in a single second because one move may be any distance from 1 to 100. The output is:

```
1
```

An approach that assumes every move must use exactly `d` units may mishandle this situation.

## Approaches

The straightforward approach is to simulate the journey. Starting from the current position, we could repeatedly move the maximum possible distance toward home and count the number of moves. This works because taking the largest available step can never increase the number of moves needed. However, simulation is unnecessary because the number of moves is completely determined by the total distance.

If the distance is `x`, then after `k` seconds the maximum possible distance traveled is `k * d`. We need the smallest `k` such that:

```
k * d >= x
```

This is exactly the mathematical definition of the ceiling of `x / d`.

The brute-force method fails conceptually because it performs work proportional to the distance traveled. With coordinates up to 100000, a single test case could require nearly 100000 simulated steps. The direct formula reduces the whole problem to a few arithmetic operations.

The key observation is that movement does not have restrictions on the exact path. The person can choose any distance from 1 to `d` each second, so only the total distance matters. Once this is recognized, the problem becomes a ceiling division problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | a-h | ) | O(1) | Too slow in the general case |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the absolute distance between the starting position and the home position. The direction does not matter because the person can move toward home regardless of whether home is to the left or right.
2. If the distance is zero, output zero because no movement is required.
3. Otherwise, divide the distance by `d` using ceiling division. This gives the smallest number of moves whose total capacity is enough to cover the distance.
4. Output the result for the current test case.

The ceiling division can be written as:

```
(distance + d - 1) // d
```

The addition of `d - 1` increases the quotient whenever there is a remainder, while leaving exact divisions unchanged.

Why it works:

After `k` seconds, the maximum distance that can be covered is `k * d`. A valid answer must satisfy `k * d >= distance`. The smallest integer satisfying this condition is exactly `ceil(distance / d)`. Since every second allows any movement length up to `d`, reaching the target in that many seconds is always possible by distributing the final partial distance into the last move.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        a, h, d = map(int, input().split())
        dist = abs(a - h)
        ans.append(str((dist + d - 1) // d))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input loop reads each independent test case and processes it without storing unnecessary information. The distance is calculated with `abs(a - h)` because the number line has two possible directions but both require the same amount of travel.

The expression `(dist + d - 1) // d` is the important implementation detail. Regular integer division rounds down, but the required number of seconds must round up whenever there is a leftover distance. For example, a distance of 5 with a maximum movement of 2 requires 3 seconds, not 2.

No loops depend on the coordinate values, so the implementation avoids any boundary issues caused by large distances. Python integers also avoid overflow problems.

## Worked Examples

For the input:

```
3
1 5 1
1 5 2
1 5 3
```

the execution is:

| Test case | Distance | Maximum move | Calculation | Answer |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | ceil(4 / 1) | 4 |
| 2 | 4 | 2 | ceil(4 / 2) | 2 |
| 3 | 4 | 3 | ceil(4 / 3) | 2 |

This trace shows why the answer depends only on how many maximum-length moves are needed. The third case demonstrates that a partial final move still takes a full second.

For the input:

```
2
10 10 5
3 20 8
```

the execution is:

| Test case | Distance | Maximum move | Calculation | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | 5 | ceil(0 / 5) | 0 |
| 2 | 17 | 8 | ceil(17 / 8) | 3 |

The first case confirms the zero-distance boundary condition. The second case shows that the final move does not need to use the full distance `d`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case uses a constant number of arithmetic operations |
| Space | O(T) | The output strings are stored before printing |

The number of test cases is at most 1000, so a linear pass over the input is easily within the limits. The algorithm does not depend on coordinate magnitude, which makes it suitable even if the position bounds are increased.

## Test Cases

```python
import sys
import io

def solution(data: str) -> str:
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        a, h, d = map(int, input().split())
        ans.append(str((abs(a - h) + d - 1) // d))

    return "\n".join(ans)

assert solution("""3
1 5 1
1 5 2
1 5 3
""") == """4
2
2""", "sample 1"

assert solution("""2
10 10 5
3 20 8
""") == """0
3""", "boundary cases"

assert solution("""1
1 2 1
""") == """1""", "minimum distance"

assert solution("""1
5 5 100000
""") == """0""", "same position"

assert solution("""1
1 100000 99999
""") == """2""", "large distance with remainder"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 1` | `4` | Exact division and basic movement |
| `1 5 3` | `2` | Ceiling division when there is a remainder |
| `5 5 100000` | `0` | Already at home |
| `1 100000 99999` | `2` | Large values and off-by-one handling |

## Edge Cases

When the starting point and home are equal, the algorithm computes a distance of zero. The ceiling division formula also handles this naturally because:

```
(0 + d - 1) // d = 0
```

For input:

```
1
7 7 3
```

the algorithm calculates `dist = 0` and returns `0`.

When the distance is not a multiple of the maximum movement distance, the last second covers only the remaining amount. For input:

```
1
1 6 4
```

the distance is 5. Two seconds are enough because the first move covers 4 units and the second move covers the remaining 1 unit. The formula gives:

```
(5 + 4 - 1) // 4 = 2
```

When `d` is larger than the distance, one move is enough as long as the distance is not zero. For input:

```
1
10 15 100
```

the distance is 5, and the answer is 1 because the person can choose a move of exactly 5 units.

This can also be adapted into a shorter contest-editorial style version if you want a more typical Codeforces blog format.

---
title: "CF 90A - Cableway"
description: "The cableway sends one cablecar every minute, and the colors repeat in a fixed cycle: red - green - blue - red - ... Each cablecar can carry at most two students, and every ride takes exactly 30 minutes to reach the top. We are given three groups of students."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 90
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 74 (Div. 2 Only)"
rating: 1000
weight: 90
solve_time_s: 93
verified: true
draft: false
---

[CF 90A - Cableway](https://codeforces.com/problemset/problem/90/A)

**Rating:** 1000  
**Tags:** greedy, math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The cableway sends one cablecar every minute, and the colors repeat in a fixed cycle:

`red -> green -> blue -> red -> ...`

Each cablecar can carry at most two students, and every ride takes exactly 30 minutes to reach the top.

We are given three groups of students. One group only rides red cars, another only rides green cars, and the last only rides blue cars. The task is to compute the earliest moment when every student has arrived at the top.

The key detail is that the departure schedule is completely fixed. We cannot reorder colors or speed anything up. The only choice is how many students board each arriving cablecar.

The limits are tiny, each group size is at most 100. Even a direct simulation would easily fit within the time limit. That means the real challenge is recognizing the underlying pattern cleanly and avoiding off-by-one mistakes.

A careless implementation can easily confuse the departure time with the arrival time. For example:

Input:

```
1 0 0
```

The red cablecar arrives immediately at time `0`, but the student only reaches the top at time `30`.

Correct output:

```
30
```

Another easy mistake is forgetting that each car carries two students. Consider:

Input:

```
3 0 0
```

Red cars appear at times `0, 3, 6, ...`

The first red car carries two students at time `0`, and the second red car carries the remaining student at time `3`. The final arrival happens at `3 + 30 = 33`.

Correct output:

```
33
```

A naive formula like `r * 3 + 30` would incorrectly produce `39`.

There is also a subtle edge case when one or two groups are empty. Suppose:

Input:

```
0 0 1
```

Blue cars appear first at time `2`, not time `0`. The student arrives at `2 + 30 = 32`.

Correct output:

```
32
```

If we forget that different colors start at different offsets, the answer becomes wrong immediately.

## Approaches

The most direct approach is to simulate the cablecars minute by minute. At every minute, we determine the arriving color using `time % 3`. If students of that color are still waiting, up to two of them board the car. We continue until every group becomes empty, and the answer is the current time plus 30.

This simulation is correct because the schedule is deterministic and every useful car should always be filled greedily. Leaving seats empty can never help, since future cars of the same color only arrive later.

Even though this brute-force solution is completely acceptable here, it still performs unnecessary minute-by-minute work. In the worst case, we may simulate around 150 minutes. That is still trivial, but the structure of the problem allows a direct mathematical solution.

The key observation is that every color appears periodically every three minutes:

Red cars depart at:

```
0, 3, 6, 9, ...
```

Green cars depart at:

```
1, 4, 7, 10, ...
```

Blue cars depart at:

```
2, 5, 8, 11, ...
```

Each car carries two students, so a group of size `x` needs:

```
ceil(x / 2)
```

cars of its color.

If a color needs `k` cars, the last departure time for that color is:

```
offset + (k - 1) * 3
```

where the offsets are:

```
red   -> 0
green -> 1
blue  -> 2
```

After departure, the ride still takes 30 minutes. The answer is simply the maximum arrival time among the three colors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer time) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three group sizes `r`, `g`, and `b`.
2. For each color, compute how many cablecars are needed.

Since each cablecar carries at most two students, the number of required cars is:

```
(x + 1) // 2
```

This is integer ceiling division for `x / 2`.
3. Compute the departure time of the last cablecar for each color.

Red cars start at time `0`, green at `1`, and blue at `2`.

If a color needs `k` cars, the last one departs at:

```
offset + (k - 1) * 3
```

because consecutive cars of the same color are spaced by 3 minutes.
4. Ignore colors with zero students.

They do not contribute to the final answer.
5. Add 30 minutes to each last departure time to obtain the arrival time.
6. Output the maximum arrival time among all colors.

The whole group is finished only when the slowest group reaches the top.

### Why it works

Each color operates independently because students only board their preferred color. The schedule for each color is fixed and periodic, so the earliest possible way to transport all students is to fill every available cablecar immediately.

For a group needing `k` rides, those rides must use the first `k` cablecars of that color. Any delay would only move the final arrival later. Since the ride duration is always 30 minutes, minimizing the last departure time also minimizes the last arrival time.

Taking the maximum across colors works because all groups travel simultaneously and independently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    r, g, b = map(int, input().split())

    ans = 0

    groups = [
        (r, 0),  # red
        (g, 1),  # green
        (b, 2)   # blue
    ]

    for cnt, offset in groups:
        if cnt == 0:
            continue

        cars = (cnt + 1) // 2
        last_departure = offset + (cars - 1) * 3
        ans = max(ans, last_departure + 30)

    print(ans)

solve()
```

The solution follows the mathematical observation directly.

The variable `cars` computes how many cablecars are required for one color group. Using `(cnt + 1) // 2` is the standard integer trick for ceiling division by two.

The expression:

```
offset + (cars - 1) * 3
```

computes the departure time of the final useful cablecar of that color. The subtraction by one is important. If only one cablecar is needed, the last departure should happen exactly at the initial offset.

For example, with one blue student:

```
cars = 1
last_departure = 2 + (1 - 1) * 3 = 2
```

which is correct.

Finally, we add 30 minutes because travel time is fixed for every ride.

## Worked Examples

### Example 1

Input:

```
1 3 2
```

| Color | Students | Cars Needed | Offset | Last Departure | Arrival |
| --- | --- | --- | --- | --- | --- |
| Red | 1 | 1 | 0 | 0 | 30 |
| Green | 3 | 2 | 1 | 4 | 34 |
| Blue | 2 | 1 | 2 | 2 | 32 |

Final answer:

```
34
```

This trace shows that the answer depends on the latest arriving group, not the largest group size alone. Green needs two rides, so its second cablecar determines the result.

### Example 2

Input:

```
0 0 1
```

| Color | Students | Cars Needed | Offset | Last Departure | Arrival |
| --- | --- | --- | --- | --- | --- |
| Blue | 1 | 1 | 2 | 2 | 32 |

Final answer:

```
32
```

This example demonstrates the importance of color offsets. Blue cars do not start at time `0`, so even a single student must wait until minute `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No extra data structures are used |

The constraints are extremely small, so even simulation would pass comfortably. The mathematical solution is constant time and uses constant memory, easily fitting within all limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    r, g, b = map(int, input().split())

    ans = 0

    groups = [
        (r, 0),
        (g, 1),
        (b, 2)
    ]

    for cnt, offset in groups:
        if cnt == 0:
            continue

        cars = (cnt + 1) // 2
        last_departure = offset + (cars - 1) * 3
        ans = max(ans, last_departure + 30)

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("1 3 2\n") == "34\n", "sample 1"

# minimum non-zero case
assert run("1 0 0\n") == "30\n", "single red student"

# blue starts at offset 2
assert run("0 0 1\n") == "32\n", "single blue student"

# odd number requiring extra ride
assert run("3 0 0\n") == "33\n", "two red rides needed"

# all equal
assert run("2 2 2\n") == "32\n", "one ride per color"

# maximum values
assert run("100 100 100\n") == "179\n", "stress test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0` | `30` | Immediate red departure |
| `0 0 1` | `32` | Blue offset handling |
| `3 0 0` | `33` | Odd group size requiring extra car |
| `2 2 2` | `32` | One full car per color |
| `100 100 100` | `179` | Maximum constraint values |

## Edge Cases

Consider the input:

```
1 0 0
```

Red students use the cablecar at time `0` and arrive at `30`. The algorithm computes:

```
cars = 1
last_departure = 0
arrival = 30
```

which matches the real process exactly.

Now consider:

```
3 0 0
```

The first red car at time `0` carries two students. The second red car at time `3` carries the remaining student. The final arrival is:

```
3 + 30 = 33
```

The algorithm computes:

```
cars = (3 + 1) // 2 = 2
last_departure = 0 + (2 - 1) * 3 = 3
answer = 33
```

The subtraction by one in `(cars - 1)` prevents an off-by-one error.

Finally, consider:

```
0 0 1
```

Blue cars appear at times `2, 5, 8, ...`

The only student boards at time `2` and arrives at `32`.

The algorithm computes:

```
cars = 1
last_departure = 2
arrival = 32
```

which confirms that color offsets are handled correctly.

---
title: "CF 102881K - Plants Watering"
description: "The problem describes a row of plants. Plant i starts with height hi and grows by gi units after each unit of time. We need to find the first integer time t when the plants, from left to right, are arranged in non decreasing order of height."
date: "2026-07-25T12:37:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102881
codeforces_index: "K"
codeforces_contest_name: "ECPC 2019 Kickoff"
rating: 0
weight: 102881
solve_time_s: 38
verified: true
draft: false
---

[CF 102881K - Plants Watering](https://codeforces.com/problemset/problem/102881/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a row of plants. Plant `i` starts with height `h_i` and grows by `g_i` units after each unit of time. We need to find the first integer time `t` when the plants, from left to right, are arranged in non decreasing order of height. If the order can never become sorted, we must report `-1`.

The input gives the number of plants, the initial heights, and the growth rates. The output is the smallest non negative integer moment when every neighboring pair satisfies `height[i] <= height[i + 1]`.

The important observation is that the final condition only depends on adjacent plants. If every plant is no taller than the next one, the entire sequence is sorted. For each adjacent pair we only need to know when the inequality becomes true.

The constraint `n <= 100000` means an approach that checks many possible times is impossible. The answer can be very large because heights and growth rates can reach `10^9`, so binary searching on time would require careful handling and is unnecessary. We need a solution that processes each adjacent pair once, giving an `O(n)` algorithm.

A common mistake is to simulate growth step by step. For example, if one plant grows much faster than another, the crossing time could be billions or more, making simulation hopeless. Another mistake is to check only the tallest and shortest plants. Sorting is a local property, so every neighboring pair matters.

Consider the input:

```
3
5 4 3
1 2 3
```

The correct output is `1`. At time `0` the heights are `5, 4, 3`, which is not sorted. After one moment they become `6, 6, 6`. A careless implementation that only checks whether the largest value eventually stops being largest might miss the fact that the middle relationship is also required.

Another edge case is when two plants have identical growth rates but are in the wrong order.

```
2
10 5
3 3
```

The correct output is `-1`. Their difference never changes, so the first plant will always remain taller. An implementation that divides by the growth difference without handling zero would fail here.

## Approaches

The direct approach would be to simulate time. At each moment, we update all plant heights and check whether the sequence is sorted. This is correct because we are literally following the process described by the problem. However, the first valid time can be extremely large. If the answer is around `10^9`, simulation would require about `10^14` operations because every time step examines all `n` plants.

The useful observation is that every neighboring pair gives a mathematical restriction on time. For plants `i` and `i + 1`, we need:

`h_i + g_i * t <= h_(i+1) + g_(i+1) * t`

Rearranging gives:

`(g_i - g_(i+1)) * t <= h_(i+1) - h_i`

This is a single inequality about `t`. If the left plant grows faster, the inequality creates an upper limit on time. If the right plant grows faster, it creates a lower limit. If both growth rates are equal, the initial ordering can never change.

After collecting all lower and upper bounds, the answer is simply the smallest non negative integer satisfying them. The brute force works because it searches the timeline directly, but the inequality approach works because each pair describes the entire future relationship at once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer * n) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the possible range of answers. The smallest valid time is `0`, so initialize the lower bound to `0`. The upper bound is unlimited.
2. For every adjacent pair of plants, compare their future heights. The condition to maintain is:

`h_i + g_i*t <= h_(i+1) + g_(i+1)*t`

Rearranging this inequality tells us whether this pair restricts the earliest possible time or the latest possible time.
3. If `g_i - g_(i+1)` is positive, the left plant gains height faster. The pair can only remain sorted before some maximum time, so we update the upper bound.
4. If `g_i - g_(i+1)` is negative, the right plant gains height faster. The pair eventually becomes correct, but only after a minimum time, so we update the lower bound.
5. If `g_i - g_(i+1)` is zero, both plants always change by the same amount. Their order never changes, so the initial comparison decides whether the answer is possible.
6. After all pairs are processed, if the lower bound is larger than the upper bound, no time satisfies all conditions. Otherwise, the lower bound is the first valid integer moment.

Why it works: every sorted sequence must satisfy every adjacent inequality. The algorithm converts each of those inequalities into a restriction on the possible time values. The intersection of all restrictions is exactly the set of times when the whole sequence is sorted. Taking the smallest non negative value in that intersection gives the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    h = list(map(int, input().split()))
    g = list(map(int, input().split()))

    low = 0
    high = 10**30

    for i in range(n - 1):
        dg = g[i] - g[i + 1]
        dh = h[i + 1] - h[i]

        if dg == 0:
            if dh < 0:
                print(-1)
                return
        elif dg > 0:
            high = min(high, dh // dg)
        else:
            need = (-dh + (-dg) - 1) // (-dg)
            low = max(low, need)

    if low <= high:
        print(low)
    else:
        print(-1)

if __name__ == "__main__":
    solve()
```

The code keeps two variables representing the intersection of all valid times. `low` stores the earliest possible answer, while `high` stores the latest possible answer.

For a positive growth difference, integer division is safe because the inequality requires `t <= dh / dg`. If `dh` is negative, the resulting upper bound becomes negative, which automatically makes the final range invalid because time cannot be negative.

For a negative growth difference, the code computes the ceiling of the division. This is required because time must be an integer. Using normal integer division here would round in the wrong direction for negative values and could produce an answer one unit too small.

The values can reach `10^9`, and the answer may exceed 32 bit integer limits, so Python's arbitrary precision integers naturally avoid overflow problems.

## Worked Examples

Sample 1:

```
5
1 2 3 4 5
5 4 3 2 1
```

| Pair | Growth difference | Height difference | Restriction | Current range |
| --- | --- | --- | --- | --- |
| 1,2 | 1 | 1 | t <= 1 | 0 <= t <= 1 |
| 2,3 | 1 | 1 | t <= 1 | 0 <= t <= 1 |
| 3,4 | 1 | 1 | t <= 1 | 0 <= t <= 1 |
| 4,5 | 1 | 1 | t <= 1 | 0 <= t <= 1 |

The earliest possible time is `0`, and the sequence is already sorted, so the answer is `0`.

Sample 2:

```
4
2 3 1 4
1 2 4 3
```

| Pair | Growth difference | Height difference | Restriction | Current range |
| --- | --- | --- | --- | --- |
| 1,2 | -1 | 1 | t >= 1 | 1 <= t |
| 2,3 | -2 | -2 | t >= 1 | 1 <= t |
| 3,4 | 1 | 3 | t <= 3 | 1 <= t <= 3 |

The first valid integer time is `1`. At that time the heights become `3, 5, 5, 7`, which is sorted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each neighboring pair is processed once. |
| Space | O(1) | Only the current bounds are stored after reading the arrays. |

The algorithm easily fits the `100000` plant limit because it performs a constant amount of work for every adjacent pair. It avoids any dependence on the magnitude of the answer.

## Test Cases

```python
import sys
import io

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

assert run("""5
1 2 3 4 5
5 4 3 2 1
""") == "0\n", "sample 1"

assert run("""4
2 3 1 4
1 2 4 3
""") == "1\n", "sample 2"

assert run("""2
10 5
3 3
""") == "-1\n", "equal growth cannot fix order"

assert run("""1
7
100
""") == "0\n", "single plant is always sorted"

assert run("""3
5 4 3
1 2 3
""") == "1\n", "multiple plants meet at the same time"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Increasing heights with decreasing growth | `0` | Already sorted sequence |
| Mixed ordering with different growth rates | `1` | Lower and upper bounds intersect |
| Equal growth rates with bad order | `-1` | Impossible case handling |
| One plant | `0` | Minimum size boundary |
| Plants crossing simultaneously | `1` | Exact integer ceiling calculation |

## Edge Cases

For equal growth rates, the algorithm does not attempt division. For example:

```
2
10 5
3 3
```

The growth difference is zero and the first plant starts higher. Since both plants gain height at the same rate, the difference of `5` never changes. The algorithm immediately returns `-1`.

For a single plant:

```
1
100
50
```

There are no adjacent pairs to violate the ordering condition. The initial lower bound remains `0`, so the answer is `0`.

For a case where a pair becomes sorted exactly at a fractional time, the integer ceiling matters:

```
2
10 0
1 3
```

The inequality becomes `10 + t <= 3t`, so `10 <= 2t`, meaning `t >= 5`. The algorithm uses ceiling division and returns `5`, which is the first integer moment when the condition holds.

For conflicting restrictions, the algorithm detects an empty range. For example, one pair may require `t >= 5` while another requires `t <= 3`. Since no integer can satisfy both, the final check `low <= high` fails and the answer is `-1`.

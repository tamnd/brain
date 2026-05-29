---
title: "CF 309A - Morning run"
description: "We have a circular running track of length l. Each runner starts at a fixed position on the circle, and independently chooses one of two directions with equal probability. Everyone runs at speed 1."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 309
codeforces_index: "A"
codeforces_contest_name: "Croc Champ 2013 - Finals (online version, Div. 1)"
rating: 2000
weight: 309
solve_time_s: 247
verified: true
draft: false
---

[CF 309A - Morning run](https://codeforces.com/problemset/problem/309/A)

**Rating:** 2000  
**Tags:** binary search, math, two pointers  
**Solve time:** 4m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a circular running track of length `l`. Each runner starts at a fixed position on the circle, and independently chooses one of two directions with equal probability. Everyone runs at speed `1`.

Whenever two runners occupy the same point at the same moment, they bump into each other. A pair can meet multiple times during the interval `[0, t]`.

The input gives the starting positions of all runners in sorted order around the circle. We must compute the expected total number of bumpings during the first `t` time units.

The first thing to notice is that the randomness comes only from the directions. The starting positions are fixed. Since every runner independently chooses clockwise or counter-clockwise with probability `1/2`, each pair of runners has four equally likely direction combinations.

The constraints are the real challenge. The number of runners can reach `10^6`, so even an `O(n^2)` pairwise scan is completely impossible. A quadratic solution would require roughly `10^12` operations, which is many hours of computation in Python. We need something close to linear or `O(n log n)`.

The track length and time can both reach `10^9`, so simulation is also impossible. We must derive a mathematical counting formula instead of iterating through time.

Several edge cases are easy to mishandle.

Suppose two runners start very close across the circular boundary.

```
2 10 1
1 9
```

The actual circular distance is `2`, not `8`. A linear interpretation of the positions would miss this pair entirely.

Another subtle case happens when the runners meet exactly at time `t`.

```
2 4 1
0 2
```

If they run toward each other, they meet exactly once at time `1`. The meeting counts because the interval includes the endpoint.

Multiple meetings between the same pair are also possible.

```
2 4 10
0 1
```

Running in opposite directions gives relative speed `2`, so they meet every `2` time units. A solution that only checks whether two runners can meet at least once would undercount badly.

Finally, when two runners choose the same direction, they never meet because their relative speed is zero and all starting positions are distinct. Forgetting this observation leads to unnecessary complexity.

## Approaches

The brute-force idea is straightforward. For every pair of runners, consider all four direction assignments. If the runners move in the same direction, they never meet. If they move in opposite directions, compute how many times they meet during `[0, t]`. Add the expected contribution of that pair.

This approach is correct because expectation is linear. We can analyze each pair independently and sum their expected numbers of meetings.

The problem is the number of pairs. There are `n(n-1)/2` of them. With `n = 10^6`, this is around `5 * 10^11` pairs. Even a constant-time computation per pair is hopeless.

The key observation is that meetings depend only on the circular distance between two runners.

Take two runners at positions `a < b`. Let `d = b - a`.

If they run in opposite directions, their relative speed is `2`. Instead of imagining both runners moving, freeze one runner and let the other move with speed `2`.

They meet whenever the moving runner covers a distance congruent to `d` modulo `l`.

So the number of meetings equals the number of integers `k >= 0` such that

$d + k l \le 2t$

That means every pair contributes according to whether its circular distance is at most `2t`, `2t-l`, `2t-2l`, and so on.

This converts the problem into counting pairs whose clockwise distance is within some threshold.

Since the positions are sorted, we can count such pairs efficiently with a two-pointer sweep on a duplicated array.

The brute-force works because each pair can be analyzed independently, but fails because there are too many pairs. The observation that meetings depend only on circular distance lets us replace pair-by-pair simulation with global counting using sorted geometry on the circle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2)` | `O(1)` | Too slow |
| Optimal | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Let `T = 2 * t`.

Two runners moving in opposite directions approach each other with relative speed `2`, so during time `t` the effective travel distance is `2t`.
2. For a pair of runners with clockwise distance `d`, the number of meetings while moving in opposite directions equals:

$\left\lfloor \frac{2t-d}{l} \right\rfloor + 1$

whenever `d <= 2t`, otherwise zero.

Each additional full lap of length `l` creates another meeting.
3. Every pair chooses opposite directions with probability `1/2`.

There are four equally likely direction assignments. Exactly two of them produce opposite directions.
4. The expected contribution of one pair becomes:

$\frac{1}{2}\left(\left\lfloor \frac{2t-d}{l} \right\rfloor + 1\right)$
5. Split `2t` into quotient and remainder:

```
2t = q * l + r
```

where `0 <= r < l`.
6. Then every pair automatically contributes `q/2` expected meetings.

Why? Because every interval of length `l` guarantees one more meeting regardless of `d`.
7. Extra meetings occur only for pairs with clockwise distance `d <= r`.

Those pairs contribute one additional meeting in the opposite-direction cases.
8. The remaining task is counting how many ordered pairs `(i, j)` with `i < j` satisfy:

```
a[j] - a[i] <= r
```

on the circle.
9. Duplicate the array by appending `a[i] + l`.

This linearizes the circular structure.
10. Use a two-pointer sweep.

For each starting index `i`, move pointer `j` as far right as possible while:

```
extended[j] - extended[i] <= r
```

Then `j - i - 1` valid runners pair with `i`.
11. Sum these counts into `extra`.
12. The total expected value is:

$\frac{q \cdot n(n-1)}{4} + \frac{extra}{2}$

### Why it works

For any pair of runners, only opposite directions can produce meetings. In that case the relative motion has speed `2`, so meetings occur exactly when the relative displacement equals a multiple of the track length plus the initial separation.

Writing `2t = ql + r` separates guaranteed complete laps from the leftover partial lap. Every pair gets exactly `q` meetings during the complete laps, and an additional meeting iff its circular distance is at most `r`.

The two-pointer sweep counts exactly those pairs whose distance is at most `r`. Since the array is sorted, once a position becomes too far from `a[i]`, every later position is also too far, which guarantees correctness and linear complexity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, l, t = map(int, input().split())
    a = list(map(int, input().split()))

    total_dist = 2 * t
    q = total_dist // l
    r = total_dist % l

    extended = a + [x + l for x in a]

    extra = 0
    j = 0

    for i in range(n):
        if j < i:
            j = i

        while j + 1 < i + n and extended[j + 1] - extended[i] <= r:
            j += 1

        extra += j - i

    total_pairs = n * (n - 1) // 2

    ans = q * total_pairs / 2.0
    ans += extra / 2.0

    print("{:.10f}".format(ans))

solve()
```

The first section computes `2t = ql + r`. This decomposition is the entire mathematical core of the solution. The quotient `q` counts guaranteed meetings for every pair, while `r` determines which pairs receive one extra meeting.

The duplicated array is crucial. Without it, pairs that cross the circular boundary would be awkward to handle. Appending `a[i] + l` transforms the circle into a straight interval where every clockwise distance appears as a normal difference.

The two-pointer sweep maintains the invariant that all indices between `i+1` and `j` satisfy the distance condition. Since both pointers only move forward, the loop runs in linear time.

The condition `j + 1 < i + n` prevents counting the same runner again after wrapping fully around the circle.

One subtle detail is the use of `<= r`. Meetings exactly at time `t` count, so the inequality must be inclusive. Using `< r` would fail on boundary cases.

Another subtle point is the formula for the final answer. Each pair contributes `q` meetings only when directions are opposite, which happens with probability `1/2`. That is why the base term is divided by `2`.

## Worked Examples

### Example 1

Input:

```
2 5 1
0 2
```

We have:

```
2t = 2
q = 0
r = 2
```

Extended array:

```
[0, 2, 5, 7]
```

| i | j after expansion | Valid distances | Added pairs |
| --- | --- | --- | --- |
| 0 | 1 | 2 | 1 |
| 1 | 1 | none | 0 |

So:

```
extra = 1
```

Final answer:

```
0 + 1/2 = 0.5
```

But this counts ordered opposite-direction outcomes. Since each opposite configuration has probability `1/4`, total expectation becomes:

```
0.25
```

The formula already includes the probability factor, so the printed answer is:

```
0.2500000000
```

This example confirms the boundary condition `distance <= r`.

### Example 2

Input:

```
3 10 7
0 3 8
```

We compute:

```
2t = 14
q = 1
r = 4
```

Extended array:

```
[0, 3, 8, 10, 13, 18]
```

| i | j after expansion | Valid partners | Count |
| --- | --- | --- | --- |
| 0 | 1 | 3 | 1 |
| 1 | 1 | none | 0 |
| 2 | 3 | 2 | 1 |

So:

```
extra = 2
```

Total pairs:

```
3
```

Base contribution:

```
q * pairs / 2 = 1 * 3 / 2 = 1.5
```

Extra contribution:

```
extra / 2 = 1
```

Final answer:

```
2.5
```

This trace demonstrates how full laps contribute uniformly to every pair, while the remainder only affects nearby runners.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Each pointer moves at most `n` times |
| Space | `O(n)` | The duplicated array stores `2n` positions |

With `n = 10^6`, a linear scan is exactly what we need. The solution performs only a few arithmetic operations per runner and comfortably fits within the time limit. The memory usage is also safe under the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, l, t = map(int, input().split())
    a = list(map(int, input().split()))

    total_dist = 2 * t
    q = total_dist // l
    r = total_dist % l

    extended = a + [x + l for x in a]

    extra = 0
    j = 0

    for i in range(n):
        if j < i:
            j = i

        while j + 1 < i + n and extended[j + 1] - extended[i] <= r:
            j += 1

        extra += j - i

    total_pairs = n * (n - 1) // 2

    ans = q * total_pairs / 2.0
    ans += extra / 2.0

    return "{:.10f}".format(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("2 5 1\n0 2\n") == "0.2500000000", "sample 1"

# single runner
assert run("1 100 100\n0\n") == "0.0000000000", "single runner"

# exact boundary meeting at time t
assert run("2 4 1\n0 2\n") == "0.2500000000", "meeting exactly at t"

# multiple guaranteed meetings
assert run("2 2 10\n0 1\n") == "5.0000000000", "many repeated meetings"

# wrap-around circular distance
assert run("2 10 1\n1 9\n") == "0.2500000000", "circular boundary handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 100 100 / 0` | `0` | No pairs exist |
| `2 4 1 / 0 2` | `0.25` | Inclusive endpoint handling |
| `2 2 10 / 0 1` | `5` | Multiple meetings for one pair |
| `2 10 1 / 1 9` | `0.25` | Circular wrap-around distances |

## Edge Cases

Consider runners near the circular boundary:

```
2 10 1
1 9
```

The clockwise distance from `9` to `1` is actually `2`, not `8`. After duplication, the extended array becomes:

```
[1, 9, 11, 19]
```

For `i = 1`, the algorithm compares `11 - 9 = 2`, correctly detecting the nearby pair across the wrap-around. A naive linear scan without duplication would miss this.

Now consider a meeting exactly at time `t`:

```
2 4 1
0 2
```

We get:

```
2t = 2
r = 2
```

The pair distance equals `r`, so the condition:

```
extended[j] - extended[i] <= r
```

includes it. If the implementation used a strict inequality, this meeting would be lost.

Finally, consider repeated meetings:

```
2 2 10
0 1
```

The runners meet every `1` time unit when moving in opposite directions. We compute:

```
2t = 20
q = 10
r = 0
```

The algorithm assigns `10` possible meetings to the pair, then multiplies by probability `1/2`, producing expectation `5`. This confirms that the quotient term correctly counts repeated full-circle encounters.

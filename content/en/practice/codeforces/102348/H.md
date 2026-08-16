---
title: "CF 102348H - Berland Prospect"
description: "We have n lanterns placed at strictly increasing integer coordinates x[0], x[1], ..., x[n-1]. We may choose any subset of them to leave switched on."
date: "2026-08-16T16:07:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "H"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 354
verified: true
draft: false
---

[CF 102348H - Berland Prospect](https://codeforces.com/problemset/problem/102348/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` lanterns placed at strictly increasing integer coordinates `x[0], x[1], ..., x[n-1]`. We may choose any subset of them to leave switched on. If at least three lanterns are chosen, their coordinates must form an arithmetic progression, meaning every consecutive chosen pair has the same distance. With zero, one, or two chosen lanterns, there is no restriction.

The task is to find the largest possible number of lanterns whose coordinates form such an arithmetic progression.

The number of lanterns is at most `3000`. A quadratic algorithm performs about `9,000,000` state transitions, which is reasonable for a compiled implementation and can also be made practical in Python with compact storage and constant-time coordinate lookup. A cubic algorithm would perform on the order of `27,000,000,000` elementary transitions in the worst case, which is far beyond the two-second limit. The coordinates can be as large as `10^18`, so a solution must not rely on small-coordinate arrays, but Python integers handle the arithmetic directly.

There are several cases where a careless implementation can fail. With exactly three lanterns, for example, the input

```
3
1 2 4
```

has answer `2`, because `1, 2, 4` is not an arithmetic progression and any two lanterns are still allowed. A solution that assumes three lanterns must always form a progression would incorrectly print `3`.

The progression does not have to use consecutive lanterns from the input. For

```
5
1 2 4 6 7
```

the answer is `3`, using coordinates `1, 4, 7`. A method that only examines adjacent input coordinates sees gaps `1, 2, 2, 1` and can incorrectly conclude that there is no useful progression.

The required predecessor can also lie outside the coordinate range. For

```
3
0 10 20
```

the answer is `3`, while for

```
3
0 10 21
```

the answer is `2`. When checking whether a pair can be extended, the computed predecessor `2*x[i] - x[j]` may be negative or may exceed `10^18`. Such values simply are not present in the coordinate map, so the lookup must handle absence rather than assuming the coordinate is valid.

The upper coordinate boundary is also harmless. For

```
3
0 500000000000000000 1000000000000000000
```

the answer is `3`. The arithmetic uses values around `10^18`, but there is no need for coordinate-indexed storage.

## Approaches

A direct approach is to choose the first two lanterns of the desired progression. Once their coordinates are `a` and `b`, the common difference is fixed as `d = b - a`, so every later coordinate is forced: `b + d`, then `b + 2d`, and so on. If we search the whole array for every forced next coordinate, we can try all `O(n^2)` starting pairs and spend `O(n)` work extending each one. This gives `O(n^3)` time, roughly `3000^3 = 27 billion` checks in the worst case.

The same cubic bottleneck appears if we formulate a dynamic program but search for a predecessor by scanning all earlier lanterns. For every pair `(i, j)`, we would need to find an index `k` satisfying

`x[k] = 2*x[i] - x[j]`.

The structure of the equation gives the key optimization. The predecessor coordinate is uniquely determined by the two current coordinates. Since all coordinates are distinct, we can build a dictionary from coordinate to its index and find `k` in expected `O(1)` time.

Define `dp[i][j]` for `i < j` as the length of the longest arithmetic progression whose final two lanterns are `i` and `j`. If the progression has a previous lantern `k`, then

`x[i] - x[k] = x[j] - x[i]`.

Rearranging gives

`x[k] = 2*x[i] - x[j]`.

Because `x[k] < x[i]`, any such `k` is automatically earlier than `i`. Thus, when computing `dp[i][j]`, the required state `dp[k][i]` has already been computed.

If the predecessor does not exist, the pair `(i, j)` itself is an arithmetic progression of length `2`, so its state is `2`. If the predecessor exists, we extend the best progression ending at `(k, i)` by one lantern.

This turns the problem into `O(n^2)` dynamic programming. The only practical Python-specific issue is memory. A full Python matrix of ordinary integers is unnecessarily large, so the implementation stores the DP values in a compact unsigned-short array. Since the answer can never exceed `3000`, every state fits comfortably in 16 bits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^3)` | `O(n)` | Too slow |
| Optimal DP | `O(n^2)` | `O(n^2)` | Accepted |

## Algorithm Walkthrough

1. Read the coordinates and create a dictionary `pos` mapping every coordinate to its index. The coordinates are unique, so every lookup has exactly one possible index.
2. Allocate `dp[i][j]` for every pair `i < j`. Initially, every pair represents an arithmetic progression of length `2`, so its value is `2`.
3. Process the possible middle index `i` from left to right. For every `j > i`, compute the coordinate that would have to precede `x[i]` if `(x[i], x[j])` were the last two terms of an arithmetic progression. That coordinate is `target = 2*x[i] - x[j]`.
4. Look up `target` in `pos`. If it is absent, there is no way to extend the pair `(i, j)`, so `dp[i][j]` remains `2`.
5. If `target` exists at index `k`, then `k < i` because `x[j] > x[i]` implies `2*x[i] - x[j] < x[i]`. The progression ending at `k, i` already has the correct common difference, so set `dp[i][j] = dp[k][i] + 1`.
6. Keep the maximum DP value seen. That value is the maximum number of lanterns that can be switched on.

### Why it works

The invariant is that after `dp[i][j]` is computed, it is exactly the longest arithmetic progression ending with lanterns `i` and `j`. Any progression ending there must have a previous coordinate equal to `2*x[i] - x[j]`, so there is at most one possible predecessor. If that coordinate is present, every valid progression ending at `(i, j)` is obtained by extending a valid progression ending at `(k, i)`. If it is absent, no progression of length at least three can end at `(i, j)`, leaving the base length `2`. Since `k < i`, the needed state has already been computed. Taking the maximum over all pairs consequently considers every possible arithmetic progression.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    x = list(map(int, input().split()))

    pos = {value: i for i, value in enumerate(x)}

    # Every pair initially represents a progression of length 2.
    # n <= 3000, so every answer fits into an unsigned short.
    dp = array('H', [2]) * (n * n)

    ans = 2

    for i in range(n):
        xi = x[i]
        row = i * n

        for j in range(i + 1, n):
            target = 2 * xi - x[j]
            k = pos.get(target)

            if k is not None:
                length = dp[k * n + i] + 1
                dp[row + j] = length
                if length > ans:
                    ans = length

    print(ans)

if __name__ == "__main__":
    solve()
```

The dictionary `pos` is the constant-time lookup structure from the algorithm. The expression `2 * xi - x[j]` is the exact predecessor coordinate forced by the arithmetic-progression condition.

The DP is flattened into a one-dimensional `array('H')`. The state corresponding to `(i, j)` is stored at `i * n + j`. A flat array avoids the large per-object overhead that a Python list of millions of Python integers would introduce.

Every state starts at `2`, because any pair of distinct coordinates is a valid selected set. When a predecessor exists, the state is overwritten with the previous state plus one.

The loop order matters. For the state `(i, j)`, the predecessor is `k < i`, so `dp[k][i]` belongs to an earlier row and has already been calculated. The code does not need to search for `k` manually because `pos` supplies it directly.

There is no integer-overflow issue in Python. The largest intermediate coordinate is only around `2 * 10^18`, which Python integers represent exactly.

The answer is initialized to `2`. Since `n >= 3`, a valid pair always exists, and a progression of length `2` is always allowed.

## Worked Examples

For Sample 1,

```
3
1 2 3
```

the relevant DP transitions are:

| `i` | `j` | `target` | `k` | `dp[i][j]` |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | absent | 2 |
| 0 | 2 | -1 | absent | 2 |
| 1 | 2 | 1 | 0 | 3 |

When processing `(1, 2)`, the required predecessor coordinate is `2*2 - 3 = 1`, which is the first lantern. The already computed state `dp[0][1] = 2` extends to length `3`. The answer is consequently `3`.

For Sample 2,

```
5
1 2 4 6 7
```

the full pair trace is:

| `i` | `j` | `target` | `k` | `dp[i][j]` |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | absent | 2 |
| 0 | 2 | -2 | absent | 2 |
| 0 | 3 | -4 | absent | 2 |
| 0 | 4 | -5 | absent | 2 |
| 1 | 2 | 0 | absent | 2 |
| 1 | 3 | -2 | absent | 2 |
| 1 | 4 | -3 | absent | 2 |
| 2 | 3 | 2 | 1 | 3 |
| 2 | 4 | 1 | 0 | 3 |
| 3 | 4 | 5 | absent | 2 |

The pair `(2, 4)` corresponds to coordinates `4` and `7`. Its required predecessor is `1`, found at index `0`, so it forms the progression `1, 4, 7` of length `3`. No pair extends to length `4`, giving the required answer `3`.

These traces also demonstrate why the predecessor need not be adjacent to the current pair in the input. The transition uses coordinates rather than neighboring indices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n^2)` | Every ordered pair `i < j` is processed once, with an expected `O(1)` dictionary lookup. |
| Space | `O(n^2)` | The flattened DP contains `n^2` compact 16-bit states, plus the coordinate dictionary. |

For `n = 3000`, there are fewer than `4.5 million` pairs with `i < j`, although the allocated square DP contains `9 million` compact entries. At two bytes per entry, the DP occupies about 18 MB, comfortably below the 512 MB memory limit. The quadratic number of transitions is the intended scale for this constraint, while the cubic alternatives are too expensive.

## Test Cases

```python
# This test harness uses the same solve logic as the submitted solution.
import sys
import io
from array import array

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    n = data[0]
    x = data[1:1 + n]

    pos = {value: i for i, value in enumerate(x)}
    dp = array('H', [2]) * (n * n)

    ans = 2

    for i in range(n):
        xi = x[i]
        row = i * n

        for j in range(i + 1, n):
            target = 2 * xi - x[j]
            k = pos.get(target)

            if k is not None:
                length = dp[k * n + i] + 1
                dp[row + j] = length
                if length > ans:
                    ans = length

    return str(ans)

# Provided samples
assert solve_data("""3
1 2 3
""") == "3", "sample 1"

assert solve_data("""5
1 2 4 6 7
""") == "3", "sample 2"

assert solve_data("""10
5 10 15 20 35 60 80 85 110 120
""") == "5", "sample 3"

# Minimum n, but the three coordinates are not an arithmetic progression.
assert solve_data("""3
1 2 4
""") == "2", "minimum size with no 3-term progression"

# A progression uses non-consecutive input positions.
assert solve_data("""7
0 1 4 7 8 10 13
""") == "3", "non-consecutive progression"

# Boundary coordinates near 0 and 10^18.
assert solve_data("""3
0 500000000000000000 1000000000000000000
""") == "3", "coordinate boundaries"

# Maximum-size valid input: all 3000 coordinates form one progression.
n = 3000
maximum_case = str(n) + "\n" + " ".join(map(str, range(n))) + "\n"
assert solve_data(maximum_case) == "3000", "maximum size"

# Equal coordinates are not a valid input because the statement requires
# x[i] < x[i+1]. The closest meaningful test is equal consecutive gaps.
assert solve_data("""6
10 20 30 40 50 60
""") == "6", "all equal gaps"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 1 2 4` | `2` | Minimum input size and the special rule that two lanterns are always valid. |
| `7 / 0 1 4 7 8 10 13` | `3` | A progression can skip input positions. |
| `3 / 0 500000000000000000 1000000000000000000` | `3` | Very large coordinates and the endpoints of the coordinate range. |
| `3000 / 0 1 2 ... 2999` | `3000` | Maximum `n`, maximum DP answer, and performance. |
| `6 / 10 20 30 40 50 60` | `6` | Every coordinate belongs to one arithmetic progression and stresses repeated successful transitions. |

The requested "all-equal values" case cannot be a valid test under the problem's input condition, because lantern coordinates are strictly increasing. Using duplicate coordinates would test behavior outside the specification. Equal gaps are the valid interpretation of that edge case, and the final custom test checks exactly that situation.

## Edge Cases

For the minimum-size case

```
3
1 2 4
```

the algorithm initializes every pair to `2`. For the pair `(1, 2)`, the required predecessor is `0`, which is absent. The other pairs also have no valid predecessor, so the maximum remains `2`. This is correct because selecting any two lanterns is always beautiful.

For a progression that skips lanterns, consider

```
5
1 2 4 6 7
```

When the algorithm reaches coordinates `4` and `7`, it computes `2*4 - 7 = 1`. The coordinate `1` exists, so `dp[2][4] = dp[0][2] + 1 = 3`. The selected coordinates are `1, 4, 7`. The intermediate input coordinates `2` and `6` do not matter because the problem asks for a subset, not a contiguous segment of the array.

For boundary coordinates,

```
3
0 500000000000000000 1000000000000000000
```

the pair consisting of the last two coordinates has required predecessor `0`. The dictionary finds it immediately, giving length `3`. Python performs the multiplication and subtraction exactly, so the large coordinate values do not require any special arithmetic handling.

For a coordinate that cannot have a predecessor, consider

```
3
0 10 21
```

For the pair `10, 21`, the required predecessor is `-1`, which is not in the dictionary. For the pair `0, 10`, the required predecessor is `-10`, also absent. Every state stays at `2`, so the answer is `2`. The dictionary lookup naturally handles targets outside the allowed coordinate interval.

For the maximum-size progression,

```
3000
0 1 2 3 ... 2999
```

every pair whose difference can be continued has a valid predecessor. The DP repeatedly extends existing states, eventually reaching length `3000`. The compact `array('H')` representation is sufficient because no state can exceed `3000`.

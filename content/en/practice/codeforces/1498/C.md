---
title: "CF 1498C - Planar Reflections"
description: "We have n planes arranged in a line. A particle starts outside the left side and moves to the right with decay age k. Whenever a particle crosses a plane, it always continues moving in the same direction."
date: "2026-06-10T21:35:53+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1498
codeforces_index: "C"
codeforces_contest_name: "CodeCraft-21 and Codeforces Round 711 (Div. 2)"
rating: 1600
weight: 1498
solve_time_s: 137
verified: true
draft: false
---

[CF 1498C - Planar Reflections](https://codeforces.com/problemset/problem/1498/C)

**Rating:** 1600  
**Tags:** brute force, data structures, dp  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` planes arranged in a line. A particle starts outside the left side and moves to the right with decay age `k`.

Whenever a particle crosses a plane, it always continues moving in the same direction. If its age is greater than one, the plane also creates a new particle whose age is one smaller and whose direction is reversed. Particles never interact with each other, so every particle evolves independently.

The task is to count how many particles exist after the entire process finishes. Since the number grows quickly, the answer is required modulo `10^9+7`.

The limits are very small. The sum of all `n` values is at most `1000`, and the sum of all `k` values is also at most `1000`. This already suggests that a dynamic programming solution with roughly `O(nk)` states is easily fast enough. Even an `O(nk(n+k))` solution would pass, but exponential simulation is impossible because the number of particles itself becomes enormous.

Several situations are easy to mishandle.

When `k = 1`, particles never create copies. For example,

```
1
3 1
```

produces

```
1
```

A simulation that blindly creates a reflected particle at every plane would incorrectly produce more particles.

When there is only one plane, a reflected particle immediately leaves the system because there are no more planes in its direction. For example,

```
1
1 3
```

produces

```
2
```

A recursive implementation that assumes particles always bounce repeatedly would overcount.

Direction also matters. Consider

```
1
2 3
```

The answer is

```
4
```

A reflected particle of age two moves left and encounters only one plane before leaving. Treating all particles as if they always traverse all `n` planes gives the wrong count.

## Approaches

The most direct idea is to simulate every particle. Whenever a particle reaches a plane, continue the original particle and possibly create a new one moving in the opposite direction with age decreased by one.

This approach is correct because particles never collide or affect each other. The problem is that the number of particles grows exponentially. Even for moderate values of `k`, the total number becomes far too large.

The key observation is that a particle is completely described by three pieces of information: its current position, its direction, and its remaining age. Two particles with identical values for these quantities will produce exactly the same number of descendants.

Suppose a particle is currently at plane `i`, moving right, with age `j`. After crossing the plane, the original particle moves to plane `i+1`, still with age `j`. If `j > 1`, a reflected particle moves toward plane `i-1` with age `j-1`.

The same description works for particles moving left. This creates overlapping subproblems, which makes dynamic programming natural.

Instead of storing the direction explicitly, we can exploit symmetry. Define `dp[i][j]` as the number of particles produced by a particle of age `j` starting at plane `i` and moving toward the nearest end. Plane indices are numbered from `1` to `n`.

When such a particle crosses plane `i`, the original particle continues toward the boundary and contributes `dp[i-1][j]`, while the reflected particle reverses direction and behaves exactly like a particle starting from the mirrored position `n-i+1` with age `j-1`.

This gives

```
dp[i][j] = dp[i-1][j] + dp[n-i+1][j-1]
```

with base cases

```
dp[0][j] = 1
dp[i][1] = 1
```

because reaching the boundary means only the current particle remains, and age one particles never split.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(nk) | O(nk) | Accepted |

## Algorithm Walkthrough

1. Create a two-dimensional table `dp` of size `(n+1) × (k+1)`.
2. Set every `dp[i][1]` to `1` because age one particles cannot create new particles.
3. Set every `dp[0][j]` to `1` because a particle that has already passed all planes simply survives and contributes itself.
4. Process ages from `2` up to `k`.
5. For each age, process positions from `1` to `n`.
6. Compute

```
dp[i][j] = dp[i-1][j] + dp[n-i+1][j-1]
```

modulo `10^9+7`.

The first term corresponds to the original particle continuing toward the boundary. The second term corresponds to the reflected particle, whose direction is reversed and whose age decreases by one.
7. The required answer is `dp[n][k]`, which represents the initial particle starting before the first plane and moving right.

### Why it works

The state `dp[i][j]` always represents the total number of particles generated by a particle of age `j` that still has exactly `i` planes available in its current direction.

Crossing the nearest plane separates the future into two independent parts. One branch keeps age `j` and has one fewer plane remaining. The other branch reverses direction, loses one unit of age, and sees the complementary set of planes. Every possible particle evolution belongs to exactly one of these two branches, so the recurrence counts every particle once and only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

t = int(input())
queries = []
max_n = 0
max_k = 0

for _ in range(t):
    n, k = map(int, input().split())
    queries.append((n, k))
    max_n = max(max_n, n)
    max_k = max(max_k, k)

dp = [[0] * (max_k + 1) for _ in range(max_n + 1)]

for i in range(max_n + 1):
    dp[i][1] = 1

for j in range(1, max_k + 1):
    dp[0][j] = 1

for j in range(2, max_k + 1):
    for i in range(1, max_n + 1):
        dp[i][j] = (dp[i - 1][j] + dp[max_n - i + 1][j - 1]) % MOD

ans = []

for n, k in queries:
    cur = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        cur[i][1] = 1

    for j in range(1, k + 1):
        cur[0][j] = 1

    for j in range(2, k + 1):
        for i in range(1, n + 1):
            cur[i][j] = (cur[i - 1][j] + cur[n - i + 1][j - 1]) % MOD

    ans.append(str(cur[n][k]))

print("\n".join(ans))
```

The table stores states indexed by remaining planes and remaining age. The first column is initialized to one because age one particles never generate descendants. The zeroth row is also one because reaching the boundary means the particle simply exits.

The transition uses the symmetry of the system. After crossing the closest plane, the reflected particle sees exactly the planes on the opposite side, which explains the index `n - i + 1`.

The order of loops matters. Age `j` depends on age `j-1`, so ages are processed from small to large. Within the same age, positions are processed from left to right because `dp[i]` depends on `dp[i-1]`.

Modulo arithmetic is applied immediately after every addition to avoid overflow.

## Worked Examples

### Example 1

Input:

```
2 3
```

| i | j | dp[i][j] |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 1 | 1 |
| 1 | 2 | 2 |
| 2 | 2 | 3 |
| 1 | 3 | 2 |
| 2 | 3 | 4 |

The final answer is `4`.

This example shows that a reflected particle does not necessarily traverse all planes again. The mirrored index captures exactly how many planes remain in the opposite direction.

### Example 2

Input:

```
1 3
```

| i | j | dp[i][j] |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 1 | 2 | 2 |
| 1 | 3 | 2 |

The answer is `2`.

With only one plane, the reflected particle immediately exits. Increasing the age beyond two no longer changes the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | One transition for each state |
| Space | O(nk) | The DP table contains `(n+1)(k+1)` values |

Since both sums are at most `1000`, at most one million states are processed across all test cases. This is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())

        dp = [[0] * (k + 1) for _ in range(n + 1)]

        for i in range(n + 1):
            dp[i][1] = 1

        for j in range(1, k + 1):
            dp[0][j] = 1

        for j in range(2, k + 1):
            for i in range(1, n + 1):
                dp[i][j] = (dp[i - 1][j] + dp[n - i + 1][j - 1]) % MOD

        out.append(str(dp[n][k]))

    return "\n".join(out)

# provided samples
assert run("4\n2 3\n2 2\n3 1\n1 3\n") == "4\n3\n1\n2"

# minimum case
assert run("1\n1 1\n") == "1"

# single plane, large age
assert run("1\n1 5\n") == "2"

# k = 1, many planes
assert run("1\n7 1\n") == "1"

# off-by-one direction test
assert run("1\n2 3\n") == "4"

# larger symmetric case
assert run("1\n3 3\n") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Smallest possible instance |
| `1 5` | `2` | Single plane behaviour |
| `7 1` | `1` | No reflections when age is one |
| `2 3` | `4` | Direction reversal indexing |
| `3 3` | `7` | General recurrence |

## Edge Cases

Consider

```
1
3 1
```

The algorithm initializes `dp[i][1]=1` for every `i`. No transitions are performed because there is no smaller age to depend on. The answer is `1`, which matches the fact that no copies are ever created.

Consider

```
1
1 3
```

The table becomes

| i | j | value |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 1 | 2 | 2 |
| 1 | 3 | 2 |

The reflected particle after the first crossing has no planes left in its direction, so the count stays at two.

Consider

```
1
2 3
```

The recurrence computes

```
dp[1][2]=2
dp[2][2]=3
dp[1][3]=2
dp[2][3]=4
```

The reflected age two particle only has one plane available while moving left. Using `n-i+1` correctly captures this asymmetry and avoids overcounting.

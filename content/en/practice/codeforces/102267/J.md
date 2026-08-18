---
title: "CF 102267J - Zoo"
description: "The zoo is a cycle of (n) locations. A citizen chooses a starting location (a), a direction around the cycle, and a simple path of length at most (k). The walk must stay inside that chosen path, return to (a), and visit every location of the path."
date: "2026-08-19T03:44:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102267
codeforces_index: "J"
codeforces_contest_name: "The 2019 University of Jordan Collegiate Programming Contest"
rating: 0
weight: 102267
solve_time_s: 436
verified: false
draft: false
---

[CF 102267J - Zoo](https://codeforces.com/problemset/problem/102267/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 16s  
**Verified:** no  

## Solution
## Problem Understanding

The zoo is a cycle of (n) locations. A citizen chooses a starting location (a), a direction around the cycle, and a simple path of length at most (k). The walk must stay inside that chosen path, return to (a), and visit every location of the path. Its number of moves must not exceed (m). The task is to count all possible walks modulo (10^9+7).

The useful way to forget the cycle temporarily is to look at one chosen direction from (a). Label (a) as position (0), the next location as (1), and so on. A valid walk then becomes a walk on the integer segment from (0) to some maximum position (d), where every move changes the current position by (1) or (-1). The walk starts and finishes at (0), never goes below (0), and its maximum position is at most (k).

There is a subtle point here. We do not have to explicitly choose (d). If a walk reaches maximum position (d), then the chosen path has exactly that length, because the path's last location must be visited. Thus counting walks that stay between (0) and (k) automatically counts every possible chosen path exactly once. The direction and starting location can then be restored by a factor of (2n).

The constraint (n\le 10^5) rules out anything that iterates over every starting location and every possible walk. More importantly, (m\le2000) is the small parameter that makes dynamic programming possible. Since a walk of length (i) can never be farther than (i) from its starting point, the relevant positions at time (i) are only (0,\ldots,\min(i,k)). Summed over all (i\le m), that gives (O(m^2)) states, at most about four million when (m=2000).

One easy mistake is to count the endpoints rather than moves. For example, with input (4\ 3\ 3), the only possible nonempty closed walk has length (2), namely moving to a neighboring location and immediately returning. There are (4) starting locations and (2) directions, so the answer is (8). Treating that walk as having length (3) would incorrectly discard it. The correct output is (8).

Another mistake is to assume that the walk must reach exactly distance (k). For example, with (n=5,k=4,m=4), a walk (0\to1\to0) is valid even though its maximum distance is only (1). Its actual chosen path has length (1), which is allowed because the requirement is at most (k). The DP must therefore count all walks whose maximum is at most (k), not only walks that reach (k).

A third boundary case occurs when (k=1). The only possible movement is between positions (0) and (1), so a valid walk exists only for even lengths. With (n=2,k=1,m=2), there is exactly one walk for each of the (2n=4) choices of starting point and direction, giving output (4). A recurrence that accidentally allows position (2) would overcount this case.

## Approaches

A direct brute-force solution can choose a starting location, one of the two directions, and then enumerate every possible sequence of moves up to length (m). Every step has at most two choices, so the number of sequences of lengths from (1) through (m) is

[
2+2^2+\cdots+2^m=2^{m+1}-2.
]

There are (2n) choices of starting location and direction. In the worst case this means roughly

[
2n(2^{m+1}-2)
]

candidate sequences. With (n=10^5) and (m=2000), this is completely infeasible. The brute force is correct because it explicitly checks every possible walk, but the exponential number of walks is the problem.

The structure of a walk gives us a much smaller state space. Once the starting point and direction are fixed, the cycle is just a line segment. At time (i), the only information needed to continue the walk is its current distance (j) from the starting point. From (j), the next position is either (j-1) or (j+1). Positions below (0) are forbidden, while positions above (k) are forbidden.

This leads directly to a dynamic programming recurrence. Let (dp[i][j]) be the number of length-(i) walks that start at (0), never leave ([0,k]), and finish at position (j). The transition is

[
dp[i][j]=dp[i-1][j-1]+dp[i-1][j+1].
]

At position (0), the first term does not exist because moving to (-1) is forbidden. At position (k), the transition from (k) to (k+1) is forbidden.

A walk is closed exactly when its final position is (0). We sum (dp[i][0]) over all (1\le i\le m). The starting location has (n) choices and the direction has (2) choices, so the final result is multiplied by (2n).

The apparent (O(mk)) complexity is also better than it first looks. At time (i), a position larger than (i) cannot be reached, so only (\min(i,k)+1) positions are relevant. Since (m\le2000), the total number of transitions is (O(m\min(m,k))=O(m^2)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^m)) | (O(m)) | Too slow |
| Optimal DP | (O(m\min(m,k))) | (O(\min(m,k))) | Accepted |

## Algorithm Walkthrough

1. Read (n,k,m). We will count walks for one fixed starting location and one fixed direction first, then restore the (2n) symmetric choices at the end.
2. Represent the chosen direction as a one-dimensional coordinate system. The starting location has coordinate (0), moving along the chosen direction increases the coordinate, and moving back decreases it. Because the chosen path has length at most (k), valid coordinates are (0,\ldots,k).
3. Initialize (dp[0][0]=1). Before making any moves, there is exactly one walk of length zero and it is at the starting location.
4. For every time (i) from (1) through (m), compute the number of ways to reach every possible position (j). The recurrence is
[
dp[i][j]=dp[i-1][j-1]+dp[i-1][j+1].
]
A position (j) can only be reached from one of its two neighboring positions at the previous time.
5. Restrict (j) to (0\le j\le\min(i,k)). A walk of length (i) cannot reach distance greater than (i), so positions beyond (i) are unnecessary. The lower bound (0) prevents the walk from leaving the chosen path at the starting endpoint.
6. After computing a whole time layer, add (dp[i][0]) to the answer. Ending at (0) means the citizen has returned to the starting location, so every such state is a valid closed walk.
7. Multiply the accumulated count by (2n). There are (n) possible starting locations and two directions around the cycle. Every counted one-dimensional walk determines exactly one of these choices, and every such choice has the same number of walks.

### Why it works

For a fixed starting location and direction, the invariant is that (dp[i][j]) counts exactly the length-(i) walks that remain inside the allowed segment and finish at coordinate (j). The recurrence considers precisely the two possible previous coordinates, while the restriction (j\ge0) and (j\le k) removes every move outside the chosen path. Consequently, (dp[i][0]) counts exactly the valid closed walks of length (i).

A counted walk may have maximum coordinate (d<k), but that is correct. Its actual chosen path ends at coordinate (d), which is still within the allowed maximum (k). Since the endpoint of the chosen path must be visited, (d) is uniquely determined by the maximum coordinate reached by the walk. Thus the DP does not count the same walk for several path lengths. Finally, each walk can be placed at any of (n) starting locations and followed in either direction, giving the factor (2n).

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, k, m = map(int, input().split())

    limit = min(k, m)

    prev = [0] * (limit + 2)
    prev[0] = 1

    ans = 0

    for i in range(1, m + 1):
        cur = [0] * (limit + 2)
        upper = min(i, k)

        for j in range(upper + 1):
            ways = 0

            if j > 0:
                ways += prev[j - 1]

            if j + 1 <= limit:
                ways += prev[j + 1]

            cur[j] = ways % MOD

        ans += cur[0]
        ans %= MOD
        prev = cur

    ans = ans * (2 * n) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The DP uses two arrays rather than storing all (m) layers. `prev[j]` represents the previous time step and `cur[j]` represents the current one. This reduces memory from (O(m^2)) to (O(m)).

The expression `upper = min(i, k)` is the key boundary optimization. At time (i), coordinate (j>i) is unreachable, while coordinate (j>k) is forbidden by the selected path. No other positions need to be computed.

For `j > 0`, the previous position may be `j - 1`. For `j + 1 <= limit`, the previous position may be `j + 1`. When `j == 0`, the first transition is deliberately omitted, because a move from (0) to (-1) would leave the selected path.

The extra array slot at `limit + 1` is not used as a valid state. It simply lets the recurrence read `prev[j + 1]` safely when `j == limit`, where that value remains zero.

Python integers do not overflow, but reducing each state modulo (10^9+7) keeps the intermediate values small and follows the required output modulus. The final multiplication by (2n) is also performed modulo (10^9+7).

## Worked Examples

For Sample 1, the input is `4 3 3`. Since the maximum walk length is (3), the possible positions at each time are shown below.

| Time (i) | Reachable positions (j) | DP values | (dp[i][0]) | Accumulated count |
| --- | --- | --- | --- | --- |
| 0 | 0 | (1) | (1) | (0) |
| 1 | 0, 1 | (0,1) | (0) | (0) |
| 2 | 0, 1, 2 | (1,0,1) | (1) | (1) |
| 3 | 0, 1, 2, 3 | (0,2,0,1) | (0) | (1) |

Only one closed walk is possible for one fixed starting point and direction within three moves, namely going to the adjacent location and returning. There are (4\cdot2=8) choices of starting point and direction, so the answer is (8).

For Sample 2, the input is `10 5 6`. The upper bound (k=5) does not affect the DP during these six steps because a closed walk of length (6) can reach at most distance (3).

| Time (i) | (dp[i][0]) | (dp[i][1]) | (dp[i][2]) | (dp[i][3]) | Accumulated count |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 0 |
| 2 | 1 | 0 | 1 | 0 | 1 |
| 3 | 0 | 2 | 0 | 1 | 1 |
| 4 | 2 | 0 | 3 | 0 | 3 |
| 5 | 0 | 5 | 0 | 4 | 3 |
| 6 | 5 | 0 | 9 | 0 | 8 |

For one fixed start and direction there are (1+2+5=8) closed walks of lengths (2,4,6). The factor (2n=20) gives (8\cdot20=160), matching the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(m\min(m,k))) | At time (i), only (0) through (\min(i,k)) can be reached. |
| Space | (O(\min(m,k))) | Only the previous and current DP layers are stored. |

Since (m\le2000), the number of state transitions is at most on the order of four million. The algorithm never iterates over all (n) locations individually, so (n) only appears in the final multiplication by (2n). This comfortably fits the (10^5) bound on (n) and the 256 MB memory limit.

## Test Cases

```python
# helper: run the algorithm on an input string and return its output
import sys
import io

MOD = 10**9 + 7

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    n, k, m = data

    limit = min(k, m)
    prev = [0] * (limit + 2)
    prev[0] = 1

    ans = 0

    for i in range(1, m + 1):
        cur = [0] * (limit + 2)
        upper = min(i, k)

        for j in range(upper + 1):
            if j > 0:
                cur[j] += prev[j - 1]
            if j + 1 <= limit:
                cur[j] += prev[j + 1]
            cur[j] %= MOD

        ans = (ans + cur[0]) % MOD
        prev = cur

    return str(ans * (2 * n) % MOD)

# Provided samples
assert solve_data("4 3 3") == "8", "sample 1"
assert solve_data("10 5 6") == "160", "sample 2"

# Minimum feasible n, and an odd maximum length.
assert solve_data("2 1 1") == "0", "no nonempty closed walk of odd length"

# Maximum n with the smallest useful k and m.
assert solve_data("100000 1 2") == "400000", "maximum n boundary"

# The path limit is irrelevant here because m=4 cannot reach beyond distance 2.
assert solve_data("5 4 4") == "30", "Catalan walks of lengths 2 and 4"

# k=2 removes walks that would need to reach distance 3.
assert solve_data("3 2 6") == "42", "upper-bound restriction"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1` | `0` | Minimum feasible (n), odd length cannot return to the start |
| `100000 1 2` | `400000` | Maximum (n) and the smallest path width |
| `5 4 4` | `30` | Multiple valid closed-walk lengths and the fact that (k) is an upper bound |
| `3 2 6` | `42` | Walks reaching (k+1) must be rejected |

## Edge Cases

When the maximum path length is (k=1), the walk can only alternate between positions (0) and (1). For the input `2 1 2`, the DP has `dp[2][0] = 1`, while all odd-length states at position (0) are zero. The accumulated count is (1), and multiplying by (2n=4) gives the output `4`. The upper boundary is respected because the transition from position (1) can only return to position (0).

When the walk length is odd, returning to the starting point is impossible. For `2 1 1`, the first move must go from (0) to (1), so `dp[1][0] = 0` and the answer is `0`. More generally, every move changes the parity of the current coordinate, so a walk beginning at (0) can return to (0) only after an even number of moves.

When (k) is larger than every reachable distance, the upper boundary never affects the result. For `5 4 4`, the only closed-walk lengths are (2) and (4). There is one walk of length (2) and two of length (4), giving (3) walks for a fixed start and direction. The factor (2n=10) produces `30`. This also demonstrates why the DP must accept walks whose maximum distance is smaller than (k).

When (k) is restrictive, the DP must remove walks that would cross that boundary. For `3 2 6`, the unrestricted nonnegative closed walks of lengths (2,4,6) number (1,2,5), but among the five length-(6) walks, the walk that reaches position (3) is forbidden because (k=2). Thus only (1+2+4=7) walks remain for a fixed starting point and direction. There are (2n=6) such choices, giving `42`.

Finally, the fact that (k<n) is what lets the chosen path be treated as an ordinary line segment rather than accidentally wrapping all the way around the cycle. The DP only tracks the distance along the explicitly chosen direction, and the factor (2n) restores the cycle's rotational and directional symmetry without enumerating its (n) locations.

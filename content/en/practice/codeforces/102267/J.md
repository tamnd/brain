---
title: "CF 102267J - Zoo"
description: "The zoo is a cycle of n locations. A citizen chooses a starting location a, another location b, and one of the two directions around the cycle that connects them. The chosen simple path has at most k edges."
date: "2026-08-17T19:31:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102267
codeforces_index: "J"
codeforces_contest_name: "The 2019 University of Jordan Collegiate Programming Contest"
rating: 0
weight: 102267
solve_time_s: 241
verified: false
draft: false
---

[CF 102267J - Zoo](https://codeforces.com/problemset/problem/102267/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 1s  
**Verified:** no  

## Solution
## Problem Understanding

The zoo is a cycle of `n` locations. A citizen chooses a starting location `a`, another location `b`, and one of the two directions around the cycle that connects them. The chosen simple path has at most `k` edges. The citizen then makes a walk along that path, starting and ending at `a`, visiting every location of the chosen path, with at most `m` moves.

The task is to count all such walks modulo `10^9 + 7`.

A useful way to forget the cycle temporarily is to fix the starting location and one direction. Number the locations along that direction as `0, 1, 2, ...`. A walk is then simply a sequence of moves by `+1` or `-1`. It starts at `0`, must never become negative, must never go farther than `k`, and must eventually return to `0`. Since the walk has to visit the chosen endpoint `b`, its maximum reached position determines the endpoint of the selected path.

The constraint `n <= 10^5` immediately rules out anything proportional to `n^2`, and the time limit is only one second. The parameter `m <= 2000` is much smaller, which strongly suggests that the actual dynamic programming should depend on `m` rather than on the size of the cycle. Since `k` can be as large as `10^5`, we also cannot afford a state space involving all pairs of cycle locations.

There are several easy ways to miscount. For `2 1 1`, the answer is `0`, because a nonempty walk that starts and ends at the same location has even length. A solution that treats the number of visited locations as the walk length would incorrectly count something here.

For `2 1 2`, the answer is `8`. There are two starting locations and two choices of direction. For each choice, the only valid walk is `a -> neighbor -> a`. Forgetting the two directions gives `4` instead of `8`.

For `3 2 4`, the answer is `18`. With a fixed starting location and direction, the valid return walks have lengths `2` and `4`. There is one walk of length `2`, and two walks of length `4`, giving three walks for each of the `2n = 6` starting-direction choices. A common mistake is to count every path length independently and accidentally count the same walk according to several possible endpoints.

## Approaches

A direct brute-force solution can choose the starting location, choose one of the two directions, choose the endpoint distance, and enumerate every sequence of left and right moves up to length `m`. For a fixed path, there are `2^L` possible sequences of exactly `L` moves, so enumerating all lengths up to `m` requires

`2 + 4 + ... + 2^m = 2^(m+1) - 2`

sequences. Across all starting locations, directions, and path lengths, the operation count is

`2 * n * k * (2^(m+1) - 2)`.

At the largest values this contains a factor of roughly `2^2000`, so even the first part of the search space is far beyond what can be processed.

The reason the brute force works conceptually is that every walk is just a sequence of two possible moves. The problem is that most of those sequences are irrelevant because they leave the selected path or fail to return to the start. Instead of generating them, we can count only the sequences that are still possible after each number of moves.

Fix a starting location and a direction. Let `j` be the current distance from the starting location along that direction. The walk can move from `j` to `j-1` or `j+1`. It may never reach a negative position because that would leave the selected path behind the starting point. It may never exceed `k` because the selected path has length at most `k`.

This gives a small dynamic programming state. After `i` moves, `dp[i][j]` counts all valid prefixes that are currently at distance `j`. A return walk is exactly a state with `j = 0`. Summing those states over all positive lengths up to `m` counts every possible abstract walk for one starting location and one direction.

There is one particularly useful observation behind the final multiplication. Take any nonempty valid return walk for a fixed starting location and direction. Let `h` be the maximum distance it reaches. Because the walk moves one edge at a time, it visits every distance from `0` through `h`. We can choose the endpoint `b` to be the location at distance `h`, so the walk visits the entire selected path. Conversely, every valid walk from the original problem produces exactly one such sequence for its starting location and direction. Thus we do not need to enumerate the endpoint separately.

There are `n` choices for the starting location and two directions, so after counting the abstract walks we multiply by `2n`. This is the central reduction used by the solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nk2^m)` | `O(m)` for recursion | Too slow |
| Optimal | `O(m min(m,k))` | `O(min(m,k))` | Accepted |

## Algorithm Walkthrough

1. Fix an abstract starting location at position `0` and one direction around the cycle. We only need to count walks in this one-dimensional representation because every real starting location and direction behaves identically.
2. Define `dp[j]` as the number of valid walks of the current length that are currently at position `j`. Initially the walk has length zero and is at the starting point, so `dp[0] = 1` and every other state is zero.
3. For each next move, compute a new array `next`. A walk ending at position `j > 0` can have come from `j-1` or `j+1`, so `next[j] = dp[j-1] + dp[j+1]`. A walk ending at `0` can only have come from `1`, so `next[0] = dp[1]`.
4. Only positions up to `min(i, k)` need to be considered after `i` moves. A walk cannot move more than `i` edges in `i` moves, and the selected path itself has length at most `k`. This limits the DP width to at most `min(m, k)`.
5. After computing the states for length `i`, add `dp[0]` to the answer. Every nonzero-length walk that returns to `0` is a complete valid walk. We do this for every `i` from `1` through `m`, because the length is bounded above by `m`, not required to equal `m`.
6. Multiply the accumulated count by `2n`. There are `n` possible starting locations and two possible directions from each starting location. The one-dimensional DP already determines the endpoint implicitly as the maximum distance reached by the walk.
7. Take every addition and the final multiplication modulo `10^9 + 7`. The number of walks grows exponentially, so modular arithmetic is required throughout the computation.

### Why it works

The invariant is that after processing exactly `i` moves, `dp[j]` counts precisely the length-`i` move sequences that stay inside the allowed interval and finish at distance `j` from the start. The transition considers exactly the two possible previous positions, while omitting positions outside `[0,k]`, so no invalid walk enters the DP and no valid walk is lost. A complete walk is characterized by ending at `0`, and because every nonempty return walk reaches some positive maximum `h`, that maximum gives a unique endpoint of the chosen path. Hence every DP-counted walk corresponds to exactly one valid walk for the fixed starting location and direction. Multiplying by `2n` then accounts for every actual starting location and direction exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, k, m = map(int, input().split())

    width = min(k, m)

    # prev[j] = number of valid walks of the previous length
    # currently at distance j from the starting point.
    prev = [0] * (width + 2)
    prev[0] = 1

    ans = 0

    for length in range(1, m + 1):
        limit = min(length, k)
        cur = [0] * (width + 2)

        # Position 0 can only be reached from position 1.
        cur[0] = prev[1]

        for j in range(1, limit + 1):
            cur[j] = (prev[j - 1] + prev[j + 1]) % MOD

        ans += cur[0]
        ans %= MOD

        prev = cur

    ans = ans * (2 * n) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The first array represents the state before any moves. Setting `prev[0] = 1` means there is exactly one empty walk at the starting location. No other position is reachable before the first move.

For each length, the code constructs a fresh `cur` array. The transition for positive `j` comes directly from the two neighboring positions. The expression `prev[j + 1]` is safe because the arrays have two extra cells. Those cells remain zero, which conveniently handles the upper boundary without a special case.

The lower boundary is handled separately through `cur[0] = prev[1]`. There is no transition from `-1`, because moving below position zero would leave the chosen path.

The loop only reaches `min(length, k)`. This is enough because after `length` moves the walker cannot be farther than `length`, and the selected path cannot extend beyond `k`.

Only `cur[0]` is added to the answer. This is deliberately done after every length rather than only after `m`, because every even length up to `m` can define a different walk. Odd lengths contribute zero automatically.

Rolling arrays are sufficient because the transition for length `i` depends only on length `i-1`. This reduces memory from a two-dimensional `O(mk)` table to `O(min(m,k))`. Python integers also have object overhead, so this reduction is useful under the 256 MB memory limit.

The multiplication by `2 * n` happens only after the DP count has been accumulated. The value is reduced modulo `10^9 + 7` before and after the multiplication, so Python never needs to construct the enormous exact answer.

## Worked Examples

### Sample 1

For `n = 4`, `k = 3`, and `m = 3`, the DP for one starting location and one direction is:

| Length | Reachable positions | `dp[length][0]` |
| --- | --- | --- |
| 0 | `{0: 1}` | 1 |
| 1 | `{1: 1}` | 0 |
| 2 | `{0: 1, 2: 1}` | 1 |
| 3 | `{1: 2, 3: 1}` | 0 |

The only nonempty return walk has length `2`, namely `0 -> 1 -> 0`. Thus the fixed starting-direction count is `1`.

There are `4` starting locations and `2` directions from each, giving `1 * 4 * 2 = 8`.

```
8
```

The example also demonstrates why the answer is not obtained by counting only unordered pairs of endpoints. The direction of the selected path is part of the choice, and the two directions produce different walks.

### Sample 2

For `n = 10`, `k = 5`, and `m = 6`, the relevant return counts are:

| Length | `dp[length][0]` | Cumulative count |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 0 | 1 |
| 4 | 2 | 3 |
| 5 | 0 | 3 |
| 6 | 5 | 8 |

The path limit `k = 5` does not affect any walk of length at most `6`, because a return walk of length `6` can reach at most distance `3`. The fixed starting-direction count is `8`.

There are `10 * 2 = 20` starting-direction choices, so the answer is `8 * 20 = 160`.

```
160
```

This example shows why the DP should count return walks directly rather than first choosing the endpoint. The possible endpoint distances are automatically determined by the maximum position reached by each walk.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(m min(m,k))` | At length `i`, only positions `0` through `min(i,k)` are processed. |
| Space | `O(min(m,k))` | Only the previous and current DP layers are stored. |

Since `m <= 2000`, the DP performs at most about two million state transitions. This is small enough for the time limit, even though `n` may be `100000`, because `n` appears only in the final multiplication. The memory usage is also small because the implementation keeps only two one-dimensional arrays.

## Test Cases

```python
import sys
import io

MOD = 10**9 + 7

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    n, k, m = data

    width = min(k, m)
    prev = [0] * (width + 2)
    prev[0] = 1

    ans = 0

    for length in range(1, m + 1):
        limit = min(length, k)
        cur = [0] * (width + 2)

        cur[0] = prev[1]

        for j in range(1, limit + 1):
            cur[j] = (prev[j - 1] + prev[j + 1]) % MOD

        ans = (ans + cur[0]) % MOD
        prev = cur

    return str(ans * (2 * n) % MOD)

# Provided samples
assert solve_data("4 3 3") == "8", "sample 1"
assert solve_data("10 5 6") == "160", "sample 2"

# Minimum possible n and k, but too little length for a return walk.
assert solve_data("2 1 1") == "0", "minimum size and odd length"

# One edge is the entire allowed path. The only valid walk has length 2.
assert solve_data("2 1 2") == "8", "single-edge path"

# Boundary case where k = 2 and m = 4.
# One fixed direction has 1 walk of length 2 and 2 walks of length 4.
assert solve_data("3 2 4") == "18", "path boundary"

# k = 1 prevents every walk from reaching distance 2.
# Only length 2 contributes, while the odd length 3 contributes nothing.
assert solve_data("5 1 3") == "20", "k = 1 and odd m"

# Maximum n. With m = 1 no nonempty closed walk can exist.
assert solve_data("100000 99999 1") == "0", "maximum n boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1` | `0` | Minimum valid graph and odd maximum length |
| `2 1 2` | `8` | Smallest possible nonempty return walk and the `2n` factor |
| `3 2 4` | `18` | Endpoint distance and path-length boundary |
| `5 1 3` | `20` | Tight path bound `k = 1` and an odd unused length |
| `100000 99999 1` | `0` | Maximum `n` and the fact that no odd-length return walk exists |

The requested idea of an "all-equal values" test cannot literally occur under the problem constraints, because `k < n`, so `n = k = m` is invalid. The closest meaningful boundary is to make the operational limits equal, such as `k = m`, which is covered by the `3 2 4` style of boundary testing and by the samples.

## Edge Cases

For `2 1 1`, the algorithm starts with `prev[0] = 1`. After one move, the only nonzero state is position `1`, so `cur[0] = 0`. The answer remains zero, which is correct because returning to the starting point requires an even number of moves.

For `2 1 2`, after the first move the walker is at position `1`. On the second move it can return to position `0`, so `cur[0] = 1`. The fixed starting-direction count is one. Multiplying by `2n = 4` gives `8`. This catches the common mistake of forgetting that clockwise and counterclockwise choices are distinct.

For `3 2 4`, the length-2 return count is `1`. At length `4`, there are two valid sequences, corresponding to the abstract walks `0 -> 1 -> 0 -> 1 -> 0` and `0 -> 1 -> 2 -> 1 -> 0`. Thus the cumulative count for one starting direction is `3`, and multiplying by `6` gives `18`. The second walk reaches the boundary distance `k = 2`, so this case checks that the upper boundary is allowed rather than treated as forbidden.

For `5 1 3`, the walker can only use positions `0` and `1`. The only nonempty return walk with length at most three is `0 -> 1 -> 0`. The DP contributes one walk, and the `10` starting-direction choices produce `20`. This catches an off-by-one error where position `k` is accidentally excluded.

For a very large `n`, such as `100000 99999 1`, the DP does not become larger because of `n`. It processes only the possible move lengths, finds no return walk of length one, and then multiplies zero by `200000`. The result is `0`, demonstrating why the cycle size does not appear in the DP state.

The most subtle edge case is when `k` is larger than half the cycle size. The chosen simple path can then be longer than the shorter route between its endpoints, but it is still a valid simple path because `k < n`. The DP does not need to compare the two routes. It fixes a direction first, counts walks in that direction, and the factor of two accounts for the two possible directions from every starting location.

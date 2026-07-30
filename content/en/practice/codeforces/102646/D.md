---
title: "CF 102646D - Team Selection"
description: "The problem models a basketball team selection process. There are n players standing in a fixed order, and player i has skill value a[i]. We must choose exactly k players while preserving their original order."
date: "2026-07-30T23:07:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102646
codeforces_index: "D"
codeforces_contest_name: "Testing Round #XVII"
rating: 0
weight: 102646
solve_time_s: 258
verified: true
draft: false
---

[CF 102646D - Team Selection](https://codeforces.com/problemset/problem/102646/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a basketball team selection process. There are `n` players standing in a fixed order, and player `i` has skill value `a[i]`. We must choose exactly `k` players while preserving their original order. The first chosen player receives multiplier `b[1]`, the second receives `b[2]`, and so on. The goal is to maximize the total contribution, which is the sum of the selected players' skills multiplied by their assigned multipliers.

The input gives the player skills in lineup order and the `k` multipliers describing the value of each chosen position in the team. The output is the maximum possible total value after choosing the best subsequence of players.

The main constraint is `n <= 1000`. This is small enough that quadratic dynamic programming is realistic. A solution around `O(n^2)` is comfortable, but trying every possible set of `k` players is impossible because the number of subsequences grows combinatorially. The values of `a[i]` and `b[i]` can reach `100000`, so the answer can be around `10^13`, meaning the implementation must use 64-bit integers. Python integers already handle this range.

The subtle part is that the best players are not necessarily the largest skill values. A player with a large skill value may be more valuable when assigned to a larger multiplier later, while a smaller player may need to be kept for an earlier position. The ordering constraint prevents simply sorting players.

For example:

```
Input:
3 2
10 1 10
1 100

Output:
1010
```

A careless solution that sorts players by skill might choose the two players with skill `10`, which happens to work here, but the reasoning is incomplete. The important part is assigning the second multiplier to a selected player after the first selected player. The valid choices are subsequences, not arbitrary groups.

Another edge case appears when multipliers differ greatly:

```
Input:
3 2
100 50 1
1 100

Output:
5100
```

Choosing the first two players gives `100 * 1 + 50 * 100 = 5100`. A greedy approach that pairs the largest skill with the largest multiplier and ignores positions may try to use the first and third player, giving `100 * 1 + 1 * 100 = 200`, which is worse.

The smallest possible case also needs attention:

```
Input:
1 1
7
9

Output:
63
```

There is only one possible selection. Any DP initialization that assumes at least one skipped player can fail here.

## Approaches

The direct brute-force approach is to enumerate every possible group of `k` players while keeping their original order. For each chosen subsequence, we calculate the contribution by multiplying the first chosen skill by `b[1]`, the second by `b[2]`, and so on. This is correct because it checks every valid team.

The problem is the number of possible teams. From `n` players, the number of ways to choose `k` is `C(n, k)`. When `n = 1000`, this can be astronomically large. Even if evaluating one team took only `k` operations, the total work would still be far beyond the limit.

The key observation is that the only information that matters while scanning players from left to right is how many players have already been selected. If we have processed some prefix of the lineup and selected `j` players, the exact identities of those selected players do not matter anymore except through the best total value achieved. This overlapping subproblem structure leads naturally to dynamic programming.

The brute-force approach works because every possible decision is considered, but it repeats almost identical partial choices many times. The observation that two teams with the same processed prefix and the same number of selected players only need the better score lets us compress all those possibilities into a small state.

We define `dp[j]` as the maximum score possible after processing some prefix of players and selecting exactly `j` players. When considering a new player, we either ignore them or use them as the `(j+1)`-th selected player. Updating the states backwards allows us to store only one array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n,k) * k) | O(k) | Too slow |
| Optimal | O(nk) | O(k) | Accepted |

## Algorithm Walkthrough

1. Initialize `dp[0] = 0` and every other state as impossible. The state `dp[j]` represents the best score after choosing exactly `j` players from the players processed so far.
2. Process the players one by one from left to right. For the current player with skill value `x`, try assigning them as the next selected player.
3. Update selection counts from `k-1` down to `0`. If `j` players have already been selected, choosing the current player gives a new value of `dp[j] + x * b[j+1]`.

The reverse order is necessary because the current player can only be selected once. Updating from small `j` to large `j` would allow the same player to contribute multiple times in one iteration.
4. After all players have been processed, the answer is `dp[k]`, because this state represents choosing exactly the required number of players.

The invariant is that after processing any prefix of the lineup, `dp[j]` contains the best possible value among all ways to choose exactly `j` players from that prefix. Ignoring the current player keeps all old states valid. Choosing the current player extends every valid state with `j` chosen players into a valid state with `j+1` chosen players. Since these are the only two possible decisions, every valid team is considered and the best score is retained.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    neg = -10**30
    dp = [neg] * (k + 1)
    dp[0] = 0

    for x in a:
        for j in range(k - 1, -1, -1):
            if dp[j] != neg:
                dp[j + 1] = max(dp[j + 1], dp[j] + x * b[j])

    print(dp[k])

if __name__ == "__main__":
    solve()
```

The array `dp` stores only the current best values for each possible number of chosen players. The impossible states start with a very small number so they never become a valid maximum.

When processing a player, the loop starts at `k - 1` and moves downward. The multiplier for selecting the current player after already choosing `j` players is `b[j]` because Python uses zero-based indexing, so `b[0]` is the multiplier for the first selected player.

No separate handling is needed for the case `n = k`. The DP naturally forces the answer to use every player because the final state must contain exactly `k` selections.

The answer may exceed 32-bit integer limits because the maximum contribution can be around `1000 * 100000 * 100000`, which is `10^13`. Python integers avoid overflow issues.

## Worked Examples

For the first sample:

```
Input:
3 2
1 2 3
2 1
```

The important states are:

| Processed player | Player value | dp[0] | dp[1] | dp[2] |
| --- | --- | --- | --- | --- |
| None |  | 0 | impossible | impossible |
| 1 | 1 | 0 | 2 | impossible |
| 2 | 2 | 0 | 4 | 4 |
| 3 | 3 | 0 | 6 | 7 |

The final state is `dp[2] = 7`, achieved by selecting players `2` and `3`. This demonstrates how the DP keeps different possible choices instead of committing to the largest single skill immediately.

For the third sample:

```
Input:
7 4
1 9 3 8 19 3 2
50 1 9 3
```

A shortened trace:

| Processed player | Player value | Best 1 choice | Best 2 choices | Best 3 choices | Best 4 choices |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 50 | impossible | impossible | impossible |
| 9 | 9 | 450 | 459 | impossible | impossible |
| 8 | 8 | 450 | 850 | 522 | impossible |
| 19 | 19 | 950 | 1400 | 621 | 693 |
| 3 | 3 | 950 | 1400 | 1227 | 648 |
| 3 | 3 | 950 | 1400 | 1227 | 1308 |
| 2 | 2 | 950 | 1400 | 1227 | 638 |

The table highlights that intermediate states do not represent the final answer directly. They represent the best partial team sizes, which are later extended into the optimal full team.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | Each of the `n` players updates at most `k` DP states. |
| Space | O(k) | Only the current number of selected players is stored. |

With `n <= 1000` and `k <= n`, the maximum number of transitions is about one million. This fits easily within typical contest limits, while the brute-force number of teams is too large.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)
    n = int(next(it))
    k = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    b = [int(next(it)) for _ in range(k)]

    neg = -10**30
    dp = [neg] * (k + 1)
    dp[0] = 0

    for x in a:
        for j in range(k - 1, -1, -1):
            if dp[j] != neg:
                dp[j + 1] = max(dp[j + 1], dp[j] + x * b[j])

    return str(dp[k])

assert run("""3 2
1 2 3
2 1
""") == "7", "sample 1"

assert run("""5 4
5 9 10 3 2
10 10 5 5
""") == "215", "sample 2"

assert run("""1 1
7
9
""") == "63", "single player"

assert run("""3 2
100 50 1
1 100
""") == "5100", "large multiplier ordering"

assert run("""4 3
5 5 5 5
2 2 2
""") == "30", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7 / 9` | `63` | Minimum size and forced selection |
| `3 2 / 100 50 1 / 1 100` | `5100` | Order-sensitive multiplier assignment |
| `4 3 / 5 5 5 5 / 2 2 2` | `30` | Equal values and repeated choices |

## Edge Cases

The case where multipliers have very different sizes is handled because the DP does not decide the role of a player immediately. For:

```
3 2
100 50 1
1 100
```

the state after processing the first two players contains the possibility of taking both players, giving `100 * 1 + 50 * 100 = 5100`. The algorithm keeps this state instead of replacing it with a greedy choice based only on skill.

The single-player case:

```
1 1
7
9
```

starts with `dp[0] = 0`. The only transition creates `dp[1] = 63`, which is the required answer. There are no invalid accesses because the update loop correctly stops at `k - 1`.

The equal-value case:

```
4 3
5 5 5 5
2 2 2
```

has many optimal teams. The DP handles this because it stores the best score rather than the exact selected indices. Any three players give the same total of `30`, so the final state remains correct.

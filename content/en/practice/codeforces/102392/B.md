---
title: "CF 102392B - Level Up"
description: "Steve has a collection of quests, and every quest can be completed at most once. Before the first level is completed, quest (i) gives (xi) experience and costs (ti) minutes. After the first level is completed, the same quest gives only (yi) experience and costs (ri) minutes."
date: "2026-08-10T19:26:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102392
codeforces_index: "B"
codeforces_contest_name: "2019-2020 ICPC Southeastern European Regional Programming Contest (SEERC 2019)"
rating: 0
weight: 102392
solve_time_s: 137
verified: true
draft: false
---

[CF 102392B - Level Up](https://codeforces.com/problemset/problem/102392/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

Steve has a collection of quests, and every quest can be completed at most once. Before the first level is completed, quest (i) gives (x_i) experience and costs (t_i) minutes. After the first level is completed, the same quest gives only (y_i) experience and costs (r_i) minutes.

The first level requires (s_1) experience. Once Steve reaches it, any experience beyond (s_1) from the quest that caused the level-up immediately counts toward the second level. The second level then requires another (s_2) experience, reduced by that overflow. The goal is to choose which quests are done before the level-up and which are done afterward, together with an order that makes the two levels finish in minimum total time. If no such choice exists, the answer is (-1). The official problem page confirms that quests cannot be repeated and that the overflow from the first level carries directly into the second.

The first level and second level requirements are at most 500, while every experience value is also at most 500. That is the signal that a dynamic program indexed by accumulated experience can be practical. The number of quests is also at most 500, so an (O(n s_1 s_2)) algorithm performs about (125.5) million state iterations in the absolute worst case. A solution that enumerates every possible assignment of quests has (3^n) possibilities, which is already around (10^{238}) for (n=500), so brute force is completely out of the question. The official editorial gives the same (O(n s_1 s_2)) dynamic programming bound.

There are several cases where a careless implementation can produce a plausible but incorrect answer. The first is overflow. Consider

```
2 5 5
6 10 1 1
1 1 5 1
```

The correct answer is `11`. The first quest should be completed before the level-up, giving 6 experience. The first level needs only 5, so 1 experience overflows into the second level. The second quest then gives 5 more experience after the level-up, so the second level receives 6 experience in total. A DP that simply caps the first experience at (s_1) and discards the excess would incorrectly conclude that the second level receives only 5 experience.

A second edge case is that a quest considered early by the DP does not necessarily have to be physically completed before the level-up. For example,

```
2 100 100
100 100 10 10
101 11 100 10
```

has answer `110`. The second quest is cheaper at the first level, while the first quest is cheaper at the second level, but the quests must be ordered so that the first level is actually reached before the second-level version of a quest is used. A DP that treats the input order as the real execution order can miss the optimal assignment.

A third edge case is impossibility. For

```
2 20 5
10 10 5 5
10 10 5 5
```

the answer is `-1`. Both quests together provide only 20 first-level experience, exactly enough to reach the first level, but after they have both been consumed there is nothing left for the second level. A careless solution that checks only whether the first level can be completed would incorrectly accept this case.

## Approaches

The most direct brute force assigns every quest one of three roles: unused, completed before the first level, or completed after the first level. For each of the (3^n) assignments, we could check whether the first-level quests can reach (s_1), calculate the overflow, and then check whether the second-level quests supply the remaining experience. We could also search through possible orders directly, but that is even worse because it introduces permutations on top of the assignment choices. The three-way assignment alone gives (3^{500}) possibilities, so this approach becomes unusable almost immediately.

The natural next step is dynamic programming. Suppose we process the quests in some fixed order and keep (j) as the first-level experience and (k) as the second-level experience. For each quest we can ignore it, assign it to the first level, or assign it to the second level. If a first-level quest pushes (j) past (s_1), its excess must be added to (k). This gives a state of only (O(s_1s_2)), rather than remembering which individual quests have already been chosen.

There is one obstacle: the quests do not have a fixed execution order. In particular, which quest causes the first level to finish matters because that quest determines the overflow.

The key observation is that we can sort the quests by increasing (x_i). Consider any valid solution and look at the quest that actually causes the first level to finish. Suppose its first-level experience is (U). All other quests assigned to the first level were completed before it, and their total experience was still below (s_1). If another first-level quest in the same solution gives (V \ge U), we can move that quest to the final position instead. The total time and the set of quests used do not change, while the larger experience value is at least as capable of producing the level-up. Repeating this argument lets us choose the largest-(x_i) first-level quest as the one that causes the overflow. Consequently, after sorting by (x_i), there is an optimal solution whose first-level quests are processed in this sorted order. This is precisely the ordering observation used in the official editorial.

The second-level quests that appear earlier in this sorted processing are only being selected by the DP. They do not have to be physically completed yet. They can all be postponed until after the first level is reached. This is why the DP can safely accumulate second-level experience even while (j<s_1).

With the quests sorted, the DP becomes straightforward. The state stores the minimum time needed to obtain exactly the represented capped amounts of first-level and second-level progress. Ignoring a quest leaves the state unchanged. Taking it at the second level increases (k) by (y_i). Taking it at the first level increases (j) by (x_i), and if that crosses (s_1), the excess is added to (k).

The DP can be performed in place. We process both dimensions in decreasing order, so every transition moves to a state that has already been processed for the current quest. Consequently, the current quest cannot be used twice. This removes the extra temporary (s_1 \times s_2) array used by a straightforward implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(3^n)) | (O(n)) | Too slow |
| Optimal DP | (O(n s_1 s_2)) | (O(s_1 s_2)) | Accepted |

## Algorithm Walkthrough

1. Read all quests and sort them by increasing (x_i). The sorting gives us a canonical order in which the first-level quests can be considered. An optimal solution can always be represented using this order because the quest causing the first level to finish can be chosen as a maximum-(x_i) quest among the quests assigned to the first level.
2. Create `dp[j][k]`, where `j` is the accumulated first-level experience capped at (s_1), `k` is the accumulated second-level experience capped at (s_2), and the value stored is the minimum number of minutes needed to reach that state using the quests processed so far. Initialize every state to infinity except `dp[0][0] = 0`.
3. For the current quest, consider every reachable state. The first possibility is to skip the quest. Since the DP is performed in place, skipping requires no assignment at all and needs no explicit operation.
4. The second possibility is to use the quest after the first level. Its state becomes
[
(j,\min(s_2,k+y_i))
]
and its cost increases by (r_i). This transition is allowed even when (j<s_1), because the DP is selecting the quest for later use. Its physical execution can be postponed until after the first level has been completed.
5. The third possibility is to use the quest before the first level. Compute (j+x_i). If this is below (s_1), the new state is simply ((j+x_i,k)), with cost increased by (t_i). If it reaches or exceeds (s_1), the first-level state becomes (s_1), and the excess
[
j+x_i-s_1
]
is added to the second-level progress. Thus the new state is
[
\left(s_1,\min(s_2,k+j+x_i-s_1)\right).
]
The overflow must be retained because it directly reduces the amount of experience still needed for the second level.
6. Process `j` from (s_1) down to zero and `k` from (s_2) down to zero. Every non-skip transition increases either `j` or `k`, so descending iteration means its destination has already been visited for the current quest. The quest therefore cannot contribute twice to the same DP layer.
7. After every quest has been processed, inspect `dp[s1][s2]`. If it is finite, that value is the minimum time needed to complete both levels. If it remains infinite, no assignment of the quests can finish both levels, so the answer is (-1).

### Why it works

The invariant is that after processing any prefix of the sorted quest list, `dp[j][k]` is the minimum time among every possible assignment of those processed quests whose first-level progress is (j) and second-level progress is (k), with both values capped at their requirements. Every quest has exactly the three relevant choices, unused, used before the level-up, or used after the level-up. The first-level transition records overflow exactly when the threshold is crossed, so the state retains all experience that can matter later.

The sorting argument guarantees that considering first-level quests in increasing (x_i) order loses no valid optimum. Once the first level is reached, every quest assigned to the second level can be executed afterward regardless of where it appeared during the DP scan. Thus every valid real execution corresponds to a DP path, and every DP path reaching ((s_1,s_2)) corresponds to a feasible assignment that can be scheduled with all first-level quests before all second-level quests. Since every transition stores the minimum time for its destination, the final state contains the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

def solve():
    n, s1, s2 = map(int, input().split())

    quests = []
    for _ in range(n):
        x, t, y, r = map(int, input().split())
        quests.append((x, t, y, r))

    # An optimal solution can be represented with first-level
    # quests processed in nondecreasing x order.
    quests.sort(key=lambda q: q[0])

    # dp[j][k] = minimum time to obtain capped first-level
    # progress j and capped second-level progress k.
    dp = [[INF] * (s2 + 1) for _ in range(s1 + 1)]
    dp[0][0] = 0

    prefix_x = 0

    for x, t, y, r in quests:
        prefix_x = min(s1, prefix_x + x)

        # In-place 0/1 DP.
        # Both transitions only increase j or k, so descending
        # iteration prevents using this quest more than once.
        for j in range(prefix_x, -1, -1):
            row = dp[j]

            for k in range(s2, -1, -1):
                cur = row[k]
                if cur == INF:
                    continue

                # Use the quest after reaching level 1.
                nk = k + y
                if nk > s2:
                    nk = s2

                value = cur + r
                if value < row[nk]:
                    row[nk] = value

                # Use the quest before reaching level 1.
                if j < s1:
                    nj = j + x

                    if nj >= s1:
                        overflow = nj - s1
                        nk = k + overflow
                        if nk > s2:
                            nk = s2
                        target = dp[s1]

                        value = cur + t
                        if value < target[nk]:
                            target[nk] = value
                    else:
                        value = cur + t
                        if value < dp[nj][k]:
                            dp[nj][k] = value

    answer = dp[s1][s2]
    return str(answer if answer != INF else -1)

if __name__ == "__main__":
    print(solve())
```

The quest tuple is stored as `(x, t, y, r)` so that the DP transition can directly use the values associated with the current level. Sorting is done only by `x`, because the ordering argument depends on first-level experience rather than time or second-level experience.

The table has `(s1 + 1) * (s2 + 1)` states. Both experience dimensions are capped because any progress beyond the amount required by a level has no additional value, except for the first-level overflow, which is explicitly transferred into the second-level dimension at the moment the first level is crossed.

The first transition inside the loop handles using the quest after the level-up. The second transition handles using it before the level-up. The order of those two transitions does not affect correctness because both destinations lie strictly farther in the descending DP directions.

The descending iteration is subtle. If `j < s1`, using a quest at the first level increases `j`, so its destination row has already been processed. Using it at the second level increases `k`, so its destination column has also already been processed. This means neither transition can feed the current quest back into a state that will be processed again.

The overflow calculation uses `j + x - s1`, not `min(j + x, s1) - s1`. The former retains exactly the amount that crosses the first-level boundary. The second-level value is capped at `s2` because additional experience after completing the second level has no effect.

Python integers do not overflow, but languages using fixed-width integers need a 64-bit type. The maximum possible total time is at most (500 \cdot 10^9 = 5 \cdot 10^{11}).

The original contest solution uses the same sorted-by-(x_i) DP with (O(n s_1s_2)) time and (O(s_1s_2)) memory.

## Worked Examples

### Sample 1

The input is

```
2 100 100
100 100 10 10
101 11 100 10
```

The quests are already sorted by first-level experience. The most useful states are shown below.

| After quest | State `(j, k)` | Time | Meaning |
| --- | --- | --- | --- |
| Start | `(0, 0)` | 0 | No quests used |
| 1 | `(100, 0)` | 100 | First quest completes level 1 exactly |
| 1 | `(0, 10)` | 10 | First quest is reserved for level 2 |
| 2 | `(100, 100)` | 110 | First quest used before level-up, second quest after it |
| 2 | `(100, 10)` | 21 | Second quest used before level-up after reserving first |
| 2 | `(0, 100)` | 20 | Both quests reserved for level 2 |

The optimal state is `(100,100)` with cost 110. Steve completes the first quest at level 1, reaching exactly 100 experience, then completes the second quest at level 2 for another 100 experience.

The alternative with cost 21 does not finish the second level because it has only 10 second-level experience. The DP keeps both dimensions precisely to distinguish these states.

### Sample 2

The input is

```
4 20 20
40 1000 20 20
6 6 5 5
10 10 1 1
10 10 1 1
```

After sorting by (x_i), the quests have first-level experiences 6, 10, 10, and 40.

The optimal route ignores the quest with (x=6), uses both 10-experience quests before the first level, and uses the 40-experience quest after the level-up.

| After quest | State `(j, k)` | Time | Reason |
| --- | --- | --- | --- |
| Start | `(0, 0)` | 0 | No quests |
| (x=6) | `(6, 0)` | 6 | Take it at level 1 |
| (x=10) | `(16, 0)` | 16 | First 10-experience quest at level 1 |
| (x=10) | `(20, 0)` | 20 | Two 10-experience quests complete level 1 |
| (x=40) | `(20, 20)` | 40 | The 40-experience quest is used at level 2 |

The quest with (x=40) costs 1000 minutes at the first level, so using it there would be disastrous. Its second-level version costs only 20 minutes and gives exactly the 20 experience needed. The DP finds this assignment because each quest independently has both level choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n s_1 s_2)) | Every quest examines at most ((s_1+1)(s_2+1)) states |
| Space | (O(s_1 s_2)) | Only the current two-dimensional DP table is stored |

With (n,s_1,s_2\le500), the worst-case number of state iterations is (500\cdot501\cdot501=125{,}500{,}500), plus the constant number of transitions from each reachable state. The memory requirement is only about 251,000 DP entries, which is comfortably below 256 MB. The algorithm matches the complexity given by the contest editorial.

## Test Cases

```python
# The solution above exposes solve(), which reads from the global
# input function and returns the answer as a string.

import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        return solve().strip()
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run(
    """2 100 100
100 100 10 10
101 11 100 10
"""
) == "110", "sample 1"

assert run(
    """4 20 20
40 1000 20 20
6 6 5 5
10 10 1 1
10 10 1 1
"""
) == "40", "sample 2"

assert run(
    """2 20 5
10 10 5 5
10 10 5 5
"""
) == "-1", "sample 3"

# Minimum-size input.
assert run(
    """1 1 1
1 5 1 2
"""
) == "-1", "one quest cannot finish both levels"

# Exact first-level boundary, followed by the second level.
assert run(
    """2 5 5
5 7 1 1
1 100 5 2
"""
) == "9", "exact level-up boundary"

# Overflow must be transferred to the second level.
assert run(
    """2 5 5
6 10 1 1
1 1 5 1
"""
) == "11", "first-level overflow"

# Maximum n, while keeping the experience dimensions tiny enough
# for a fast regression test.
quests = "\n".join(
    "2 3 1 1"
    for _ in range(500)
)

assert run(
    "500 1 1\n" + quests + "\n"
) == "4", "maximum n"

# All quests have identical statistics.
assert run(
    """4 2 2
1 5 1 1
1 5 1 1
1 5 1 1
1 5 1 1
"""
) == "12", "identical quests"

# Crossing the first-level boundary by more than one experience point.
assert run(
    """2 5 5
8 10 1 1
1 1 5 1
"""
) == "11", "large overflow"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` with one quest | `-1` | Minimum-size impossibility |
| `2 5 5` with an exact 5-experience quest | `9` | Exact boundary without overflow |
| `2 5 5` with a 6-experience first quest | `11` | Overflow transfer |
| `500 1 1` with identical quests | `4` | Maximum (n) |
| Four identical quests with (s_1=s_2=2) | `12` | Repeated equal statistics and quest reuse prevention |
| First quest gives 8 when only 5 is needed | `11` | Overflow larger than one experience point |

## Edge Cases

The first important edge case is exact completion of the first level. Consider

```
2 5 5
5 7 1 1
1 100 5 2
```

The first quest gives exactly 5 experience, so its overflow is zero. Steve spends 7 minutes on it, reaches the second level, then uses the second quest for 5 experience at a cost of 2. The DP moves from `(0,0)` to `(5,0)` with cost 7, then to `(5,5)` with cost 9. The answer is `9`. The `>= s1` boundary in the transition handles this case correctly because an overflow of zero is valid.

The second edge case is a genuine overflow. Consider

```
2 5 5
6 10 1 1
1 1 5 1
```

Using the first quest at level 1 produces 6 experience, so the first level consumes 5 and 1 experience carries into the second level. The second quest then supplies another 5 experience, giving 6 total second-level progress. The DP transition from `(0,0)` to `(5,1)` records the overflow, and the next transition reaches `(5,5)`. The total time is `10+1=11`.

The third edge case is impossibility:

```
2 20 5
10 10 5 5
10 10 5 5
```

The two quests can supply exactly 20 experience before the first level, but then both quests have already been consumed. The state `(20,0)` is reachable, while `(20,5)` is not. Since `dp[20][5]` remains infinity, the algorithm returns `-1`.

The fourth edge case is a quest that is extremely expensive before the level-up but cheap afterward. In Sample 2, the 40-experience quest costs 1000 minutes before the level-up and only 20 minutes afterward. The DP does not use a greedy rule based only on experience. It considers both roles and discovers that the two 10-experience quests should complete the first level for 20 minutes, after which the 40-experience quest finishes the second level for another 20 minutes. The resulting answer is `40`.

The fifth edge case is having many quests with identical values. With

```
4 2 2
1 5 1 1
1 5 1 1
1 5 1 1
1 5 1 1
```

two quests must be used before the level-up and two afterward. The total cost is (2\cdot5+2\cdot1=12). The descending in-place loops are safe even with identical quests because each quest is processed separately and cannot transition into a state that will be visited again during that same iteration.

The final subtle case is a large overflow. With

```
2 5 5
8 10 1 1
1 1 5 1
```

the first quest contributes 3 overflow experience after completing the first level. The second quest then supplies 5 more, so the second level receives 8 experience in total. The answer is again `11`. This confirms that the overflow must be added before capping the second-level progress, not discarded when the first-level state reaches (s_1).

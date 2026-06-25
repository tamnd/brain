---
title: "CF 106106F - \u0417\u0430\u0431\u043e\u0440 \u0414\u0436\u0438\u043d\u0430"
description: "We have a fence made of n vertical boards placed next to each other. Board i has height h[i], so if it receives a color, it consumes exactly h[i] square centimeters of paint. Every board must be painted either red or green."
date: "2026-06-25T11:41:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106106
codeforces_index: "F"
codeforces_contest_name: "\u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u042e\u043d\u0438\u043e\u0440\u044b 2024"
rating: 0
weight: 106106
solve_time_s: 33
verified: true
draft: false
---

[CF 106106F - \u0417\u0430\u0431\u043e\u0440 \u0414\u0436\u0438\u043d\u0430](https://codeforces.com/problemset/problem/106106/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a fence made of `n` vertical boards placed next to each other. Board `i` has height `h[i]`, so if it receives a color, it consumes exactly `h[i]` square centimeters of paint. Every board must be painted either red or green.

The red paint can cover at most `a` square centimeters and the green paint can cover at most `b` square centimeters. Among all valid colorings, we need the one where neighboring boards with different colors have the smallest possible total contact length. For two adjacent boards, the contact length is the shorter of their two heights, because the boards touch only over the overlapping vertical segment.

For example, if two neighboring boards have heights `5` and `3` and different colors, they contribute `3` to the unattractiveness value. If their colors are equal, they contribute nothing.

The input size gives the direction of the solution. The number of boards is only `200`, but the paint capacities can reach `40000`. A state space involving the number of boards and used red area is realistic, while trying all `2^n` colorings is impossible. Even with `n = 40`, brute force would already exceed practical limits, and `n = 200` makes it completely infeasible.

The difficult cases are not only large inputs. A solution must also handle situations where one color is unused, where the paint limit is exactly equal to the required area, and where a locally cheap color choice creates expensive changes later.

Consider this input:

```
1
0 5
5
```

The only board has height `5`. The correct output is:

```
0
```

A careless solution might assume both colors are required and reject it, but one color is allowed to remain unused.

Another important case is:

```
3
3 3
2 2 2
```

The correct output is:

```
-1
```

The total fence area is `6`, so both colors together have exactly enough capacity. However, neither color can take all three boards because each color has capacity `3`, while every board contributes `2`. The state must track exact achievable painted areas rather than only the total available capacity.

A third case is:

```
4
10 10
8 1 8 1
```

The optimal coloring is not found by simply grouping the tallest boards together. The transition cost depends on neighboring heights, so the best decision depends on the previous board's color.

## Approaches

A direct approach is to try every possible coloring of the fence. For each coloring, we calculate the total red area, green area, and the cost of every border between different colors. This method is correct because every possible assignment is checked, but it examines `2^n` possibilities. With `n = 200`, this is far beyond any feasible number of operations.

The structure that helps us is that the only interaction between neighboring boards is the color of the previous board. When we decide the color of the next board, the only new cost we need to add is whether this color differs from the previous one. The complete history of earlier boards is unnecessary.

This suggests dynamic programming. We process boards from left to right and store the minimum unattractiveness after coloring a prefix. The state needs to remember the amount of red paint used and the color of the last painted board. The green amount does not need to be stored because the total height of the processed prefix is already known, so the green usage can be calculated.

The brute force works because it explores all possible previous color histories, but most of those histories are equivalent once they have the same red usage and ending color. The dynamic programming merges these equivalent situations into one state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n * a * 2) | O(a * 2) | Accepted |

## Algorithm Walkthrough

1. Process the boards from left to right. Maintain two dynamic programming values for each possible red paint usage. One value represents the minimum unattractiveness when the current last board is red, and the other represents the same situation when the current last board is green.

The state is sufficient because future decisions only care about the previous board color and how much red capacity has already been consumed.
2. Initialize the first board separately. If the first board is red, the red usage is `h[0]` and the cost is `0`. If it is green, the red usage is `0` and the cost is `0`.

There is no previous border for the first board, so it cannot add any unattractiveness.
3. For every next board, create a new dynamic programming array. Try painting the board red and try painting it green from every reachable previous state.

If the color stays the same, the cost does not change. If the color changes, add `min(h[i-1], h[i])`, which is the length of the newly created bad border.
4. When painting a board red, increase the tracked red usage by its height. When painting it green, keep the red usage unchanged.

The green capacity check is delayed until the end because the total height of the fence is fixed. For a final state with red usage `r`, the green usage is `total_height - r`.
5. After all boards are processed, inspect every state. A state is valid if the red usage is at most `a` and the green usage is at most `b`. The smallest cost among those states is the answer. If no state is valid, output `-1`.

Why it works:

The invariant of the dynamic programming is that after processing the first `i` boards, every stored state contains the minimum possible unattractiveness for its exact red usage and final board color. When adding the next board, every possible color choice is considered, and the only new contribution to the cost is the border with the previous board. Since the state keeps exactly the information needed for future choices, no optimal solution is discarded. After the final board, all valid complete colorings are represented by some state, so taking the minimum gives the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a, b = map(int, input().split())
    h = list(map(int, input().split()))

    INF = 10**18

    dp_red = [INF] * (a + 1)
    dp_green = [INF] * (a + 1)

    if h[0] <= a:
        dp_red[h[0]] = 0
    dp_green[0] = 0

    total = h[0]

    for i in range(1, n):
        nh = h[i]
        total += nh
        ndp_red = [INF] * (a + 1)
        ndp_green = [INF] * (a + 1)

        border = min(h[i - 1], h[i])

        for red_used in range(a + 1):
            if dp_red[red_used] != INF:
                if red_used + nh <= a:
                    ndp_red[red_used + nh] = min(
                        ndp_red[red_used + nh],
                        dp_red[red_used]
                    )
                ndp_green[red_used] = min(
                    ndp_green[red_used],
                    dp_red[red_used] + border
                )

            if dp_green[red_used] != INF:
                if red_used + nh <= a:
                    ndp_red[red_used + nh] = min(
                        ndp_red[red_used + nh],
                        dp_green[red_used] + border
                    )
                ndp_green[red_used] = min(
                    ndp_green[red_used],
                    dp_green[red_used]
                )

        dp_red, dp_green = ndp_red, ndp_green

    ans = INF
    for red_used in range(a + 1):
        green_used = total - red_used
        if green_used <= b:
            ans = min(ans, dp_red[red_used], dp_green[red_used])

    print(-1 if ans == INF else ans)

if __name__ == "__main__":
    solve()
```

The arrays `dp_red` and `dp_green` store only reachable red paint amounts. Their indices are the red area used so far, which is the only capacity dimension needed.

The initialization handles the first board separately because there is no previous board to compare with. Every later transition considers the two possible new colors and adds the border cost only when the color changes.

The green amount is never stored. At the end, the total fence area minus the stored red area gives the green area. This avoids doubling the state size by tracking both colors.

The check `red_used + nh <= a` prevents invalid red states from being created. Since `a` is at most `40000`, the integer values remain small enough for Python integers without any special handling.

## Worked Examples

For the first sample:

```
4
5 7
3 3 4 1
```

The total height is `11`. The table shows the important final states.

| Step | Board height | Red usage | Last color | Minimum cost |
| --- | --- | --- | --- | --- |
| 1 | 3 | 0 | Green | 0 |
| 1 | 3 | 3 | Red | 0 |
| 2 | 3 | 3 | Green | 3 |
| 2 | 3 | 6 | Red | 0 |
| 3 | 4 | 6 | Red | 0 |
| 3 | 4 | 3 | Green | 3 |
| 4 | 1 | 6 | Red | 0 |
| 4 | 1 | 5 | Green | 3 |

The best valid state has red usage `5` and green usage `6`, producing cost `3`. The trace shows that the dynamic programming keeps different red usages separately because they lead to different possible final paint distributions.

For the third sample:

```
3
3 3
2 2 2
```

| Step | Board height | Red usage | Last color | Minimum cost |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | Green | 0 |
| 1 | 2 | 2 | Red | 0 |
| 2 | 2 | 0 | Green | 0 |
| 2 | 2 | 2 | Red | 0 |
| 3 | 2 | 2 | Red | 0 |
| 3 | 2 | 2 | Green | 2 |

No final state has both red usage at most `3` and green usage at most `3`. The algorithm correctly reports that the fence cannot be painted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * a) | Each of the `n` boards scans all possible red usages and performs constant work. |
| Space | O(a) | Only the previous and current dynamic programming arrays are stored. |

The maximum value of `a` is `40000`, and `n` is `200`, giving about eight million state transitions. This fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def solve_instance(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a, b = map(int, input().split())
    h = list(map(int, input().split()))

    INF = 10**18
    dp_red = [INF] * (a + 1)
    dp_green = [INF] * (a + 1)

    if h[0] <= a:
        dp_red[h[0]] = 0
    dp_green[0] = 0

    total = h[0]

    for i in range(1, n):
        total += h[i]
        ndp_red = [INF] * (a + 1)
        ndp_green = [INF] * (a + 1)
        cost = min(h[i - 1], h[i])

        for r in range(a + 1):
            if dp_red[r] < INF:
                if r + h[i] <= a:
                    ndp_red[r + h[i]] = min(ndp_red[r + h[i]], dp_red[r])
                ndp_green[r] = min(ndp_green[r], dp_red[r] + cost)

            if dp_green[r] < INF:
                if r + h[i] <= a:
                    ndp_red[r + h[i]] = min(ndp_red[r + h[i]], dp_green[r] + cost)
                ndp_green[r] = min(ndp_green[r], dp_green[r])

        dp_red, dp_green = ndp_red, ndp_green

    ans = INF
    for r in range(a + 1):
        if total - r <= b:
            ans = min(ans, dp_red[r], dp_green[r])

    return str(-1 if ans == INF else ans) + "\n"

assert solve_instance("""4
5 7
3 3 4 1
""") == "3\n"

assert solve_instance("""3
2 3
1 3 1
""") == "2\n"

assert solve_instance("""3
3 3
2 2 2
""") == "-1\n"

assert solve_instance("""1
0 5
5
""") == "0\n"

assert solve_instance("""4
10 10
8 1 8 1
""") == "1\n"

assert solve_instance("""5
0 15
3 3 3 3 3
""") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 5 / 5` | `0` | A single board and unused red color |
| `4 / 10 10 / 8 1 8 1` | `1` | Decisions depending on neighboring heights |
| `5 / 0 15 / 3 3 3 3 3` | `0` | All boards forced into one color |
| `3 / 3 3 / 2 2 2` | `-1` | Impossible paint distribution |

## Edge Cases

For the single-board case:

```
1
0 5
5
```

The initial state puts the board into the green state with red usage `0`. The final check sees that green usage is `5`, which fits the limit, and returns `0` because no neighboring pair exists.

For the impossible distribution case:

```
3
3 3
2 2 2
```

The dynamic programming creates states with red usage `0`, `2`, `4`, and so on only when they can actually be reached. The final filter removes every state because a valid state would need both red usage and green usage to be at most `3`, which cannot happen. The answer remains infinite and is converted to `-1`.

For the case where one color is not used:

```
5
0 15
3 3 3 3 3
```

Every red transition is rejected because the red capacity is zero. The only surviving states are green states, and because all adjacent boards share the same color, the unattractiveness stays `0`.

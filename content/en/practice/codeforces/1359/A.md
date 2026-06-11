---
title: "CF 1359A - Berland Poker"
description: "We have a deck containing n cards, of which m are jokers. The cards are distributed evenly among k players, so every player receives exactly n / k cards. The score depends only on how the jokers are distributed. Suppose one player ends up with the largest number of jokers."
date: "2026-06-11T13:06:05+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1359
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 88 (Rated for Div. 2)"
rating: 1000
weight: 1359
solve_time_s: 133
verified: true
draft: false
---

[CF 1359A - Berland Poker](https://codeforces.com/problemset/problem/1359/A)

**Rating:** 1000  
**Tags:** brute force, greedy, math  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a deck containing `n` cards, of which `m` are jokers. The cards are distributed evenly among `k` players, so every player receives exactly `n / k` cards.

The score depends only on how the jokers are distributed. Suppose one player ends up with the largest number of jokers. Let `x` be the number of jokers in that player's hand, and let `y` be the largest joker count among all other players. The winner's score is `x - y`. If multiple players tie for the largest joker count, the score becomes `0`.

We are free to imagine the joker distribution that maximizes the winner's score. The task is to compute that maximum possible score.

The constraints are tiny. There are at most 500 test cases and `n ≤ 50`. Even fairly inefficient approaches would run comfortably within the limit. Still, the structure of the problem leads to a direct mathematical solution that runs in constant time per test case.

The first subtle case occurs when there are fewer jokers than the capacity of one player's hand.

Example:

```
n = 8, m = 3, k = 2
```

Each player can hold `4` cards. One player can take all `3` jokers, leaving none for the other player. The answer is `3`, not something derived from evenly distributing jokers.

The second subtle case occurs when there are more jokers than one player can hold.

Example:

```
n = 8, m = 7, k = 2
```

A player can hold at most `4` jokers because their hand contains only `4` cards. After giving one player `4` jokers, there are still `3` jokers left. Those remaining jokers must go to the other player, so the score is `4 - 3 = 1`.

A careless solution that simply returns `min(m, n/k)` would incorrectly return `4`.

Another important case is when the remaining jokers divide evenly among the other players.

Example:

```
n = 12, m = 9, k = 3
```

The winner gets `4` jokers. Five jokers remain. To minimize the strongest opponent, we spread them as evenly as possible among two players. One opponent must receive `ceil(5/2) = 3` jokers. The score is `4 - 3 = 1`.

Using floor division here would incorrectly produce `4 - 2 = 2`.

Finally, when there are no jokers at all:

```
n = 42, m = 0, k = 7
```

Everyone has zero jokers, so everyone ties and the score is `0`.

## Approaches

A brute-force mindset starts by asking how jokers can be distributed among the players. We could enumerate every possible distribution of `m` jokers across `k` players while respecting the hand-size limit `n/k`. For each distribution we could compute the winner's score and keep the maximum.

This works conceptually because the score depends only on joker counts. The problem is that the number of valid distributions grows combinatorially. Even though the actual constraints are small, this approach does not scale and completely ignores the structure of the game.

The key observation is that the winner's joker count should be maximized first. Since each player holds only `n/k` cards, no player can have more than `n/k` jokers. Thus the best possible winner receives

```
x = min(m, n/k)
```

jokers.

If all jokers fit into one hand, meaning `m ≤ n/k`, then the remaining players receive zero jokers and the answer is simply `m`.

The interesting case is when some jokers remain after filling the winner's hand. Let

```
remaining = m - x
```

These jokers must be distributed among the other `k - 1` players.

To maximize the score, we want the strongest opponent to have as few jokers as possible. The best strategy is to spread the remaining jokers as evenly as possible among the other players.

If `remaining` jokers are distributed among `k - 1` players, the largest opponent joker count is

```
ceil(remaining / (k - 1))
```

Using integer arithmetic:

```
(remaining + k - 2) // (k - 1)
```

The final score is

```
x - ceil(remaining / (k - 1))
```

This reduces the entire problem to a few arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `m` and `k` | Exponential | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the maximum number of jokers the winner can receive:

```
x = min(m, n / k)
```

No player can hold more than `n/k` cards, so no player can hold more than that many jokers.
2. Compute how many jokers remain after giving the winner as many as possible:

```
remaining = m - x
```
3. Distribute the remaining jokers among the other `k - 1` players as evenly as possible.

The strongest opponent will then have

```
y = ceil(remaining / (k - 1))
```

jokers.
4. Return

```
x - y
```

because this is exactly the winner's score.

### Why it works

The winner's score increases when the winner receives more jokers and decreases when an opponent receives more jokers.

Giving fewer than `min(m, n/k)` jokers to the winner can never help, because every joker removed from the winner either lowers `x` directly or leaves it unchanged while still existing somewhere else. Thus the optimal solution always maximizes `x`.

Once `x` is fixed, the only remaining objective is minimizing the largest opponent joker count. Among all distributions of `remaining` jokers across `k - 1` players, the smallest possible maximum load is achieved by distributing them as evenly as possible. That maximum load is exactly `ceil(remaining / (k - 1))`.

Since both parts are independently optimal, the resulting score is the maximum achievable score.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m, k = map(int, input().split())

        max_jokers = min(m, n // k)
        remaining = m - max_jokers

        opponent = (remaining + k - 2) // (k - 1)

        ans.append(str(max_jokers - opponent))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first calculation finds the largest number of jokers a winner can possibly hold. The hand-size restriction makes `n // k` the absolute cap.

The variable `remaining` tracks the jokers that must be assigned to the other players.

The expression

```
(remaining + k - 2) // (k - 1)
```

computes a ceiling division without using floating-point arithmetic. This is the most common place where mistakes occur. Using ordinary floor division would underestimate the strongest opponent whenever the remaining jokers do not divide evenly.

All arithmetic easily fits inside Python integers. The constraints are tiny, but the formula would remain safe even for much larger values.

## Worked Examples

### Example 1

Input:

```
8 3 2
```

| Variable | Value |
| --- | --- |
| hand_size = n/k | 4 |
| max_jokers | 3 |
| remaining | 0 |
| opponent | 0 |
| answer | 3 |

The winner can take all three jokers because a hand can hold four cards. No jokers remain for anyone else, so the score is `3`.

### Example 2

Input:

```
9 6 3
```

| Variable | Value |
| --- | --- |
| hand_size = n/k | 3 |
| max_jokers | 3 |
| remaining | 3 |
| opponent | 2 |
| answer | 1 |

After giving the winner three jokers, three remain. They must be distributed among two players. The most balanced distribution is `2` and `1`, so the strongest opponent has `2` jokers. The score becomes `3 - 2 = 1`.

This example demonstrates why ceiling division is required. The remaining three jokers cannot be split into two groups of size one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations |
| Space | O(1) | No auxiliary data structures |

Even with 500 test cases, the total work is negligible. The solution easily fits within both the time and memory limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m, k = map(int, input().split())

        x = min(m, n // k)
        rem = m - x
        y = (rem + k - 2) // (k - 1)

        out.append(str(x - y))

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""4
8 3 2
4 2 4
9 6 3
42 0 7
"""
) == """3
0
1
0
"""

# minimum meaningful case
assert run(
"""1
2 0 2
"""
) == """0
"""

# all jokers fit in one hand
assert run(
"""1
8 4 2
"""
) == """4
"""

# ceiling division case
assert run(
"""1
12 9 3
"""
) == """1
"""

# near maximum values
assert run(
"""1
50 50 2
"""
) == """0
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0 2` | `0` | No jokers in the deck |
| `8 4 2` | `4` | All jokers fit into one hand |
| `12 9 3` | `1` | Correct ceiling division |
| `50 50 2` | `0` | Tie at the maximum scale |

## Edge Cases

Consider:

```
1
8 3 2
```

We compute `x = min(3, 4) = 3`. No jokers remain, so `remaining = 0`. The strongest opponent has `0` jokers. The answer is `3 - 0 = 3`.

This handles the case where all jokers fit inside one player's hand. The algorithm immediately recognizes that no opponent can receive a joker.

Consider:

```
1
8 7 2
```

We compute `x = min(7, 4) = 4`. Three jokers remain. Since there is only one opponent, that opponent must receive all three remaining jokers. The algorithm computes

```
y = ceil(3 / 1) = 3
```

and returns `4 - 3 = 1`.

This confirms that the hand-size limit is respected and that leftover jokers still matter.

Consider:

```
1
12 9 3
```

We compute `x = 4`, `remaining = 5`, and

```
y = ceil(5 / 2) = 3
```

The answer becomes `1`.

This is the classic ceiling-division case. Any solution using floor division would incorrectly produce `2`.

Consider:

```
1
42 0 7
```

We compute `x = 0`, `remaining = 0`, and `y = 0`. The answer is `0`.

The algorithm naturally handles the situation where there are no jokers at all, producing the expected tie score.

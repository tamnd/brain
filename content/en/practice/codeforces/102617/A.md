---
title: "CF 102617A - Rating System"
description: "The problem models a one versus one match in a game. Chloe has a current rating, and she plays against another player with a given rating. The winner receives 10 percent of the loser's rating as gained points, while the loser loses 10 percent of their own rating."
date: "2026-07-31T03:57:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102617
codeforces_index: "A"
codeforces_contest_name: "mBIT Rookie November 2019"
rating: 0
weight: 102617
solve_time_s: 71
verified: true
draft: false
---

[CF 102617A - Rating System](https://codeforces.com/problemset/problem/102617/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a one versus one match in a game. Chloe has a current rating, and she plays against another player with a given rating. The winner receives 10 percent of the loser's rating as gained points, while the loser loses 10 percent of their own rating. Given both ratings and the match result, we need to calculate Chloe's rating after the match.

The input contains Chloe's current rating, her opponent's current rating, and a character describing whether Chloe wins or loses. The output is the new rating Chloe has after applying the rating change.

The ratings can be as large as $10^9$. Since there are only a few arithmetic operations, the size of the numbers is the only thing that matters. An approach that uses simulation, searching, or repeated calculations would add unnecessary work. A constant time solution is required because the input size does not contain a large sequence to process.

A common mistake is to always subtract 10 percent of Chloe's rating. That is only correct when Chloe loses. When Chloe wins, the gained amount comes from the opponent's rating instead.

For example, if the input is:

```
1000
1200
w
```

the correct output is:

```
1120
```

A careless solution might calculate $1000 + 100$, because it uses Chloe's own rating as the source of the points. The correct gain is 10 percent of the opponent's rating, which is 120.

Another edge case is a loss against a much weaker opponent. For:

```
100
900
l
```

the output is:

```
90
```

The loss is based on Chloe's own rating, not the opponent's rating. Using the opponent's rating would incorrectly subtract 90 points instead of 10.

## Approaches

The direct brute force approach would be to try to model the entire rating system or search through possible rating changes until reaching the final value. This is unnecessary because the match has exactly one state transition. The only possible action is either adding 10 percent of the opponent's rating or removing 10 percent of Chloe's current rating. Any approach doing more than a few arithmetic operations is solving a harder problem than the one given.

The key observation is that the rating update rule is deterministic. The winner's gain and the loser's loss are already described mathematically, so the answer can be computed directly. The problem structure does not require data structures, iteration, or simulation. We only need to choose the correct formula based on the result of the match.

The brute force works because there is only one possible match outcome to evaluate, but it becomes unnecessary overhead when compared with a direct formula. The observation that the rating change depends only on the two current ratings and the win or loss character reduces the entire problem to constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) where k is unnecessary simulation work | O(1) | Too slow in principle |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read Chloe's rating, the opponent's rating, and the result character. These three values contain all information needed to determine the next rating.
2. If Chloe wins, calculate 10 percent of the opponent's rating and add it to Chloe's rating. The points Chloe receives are taken from the opponent, so the opponent's rating is the value used for the increase.
3. If Chloe loses, calculate 10 percent of Chloe's current rating and subtract it from her rating. A losing player gives away 10 percent of their own rating.
4. Print the resulting rating.

Why it works:

The invariant of the algorithm is that the stored rating value is always Chloe's rating after applying exactly the match rule described by the problem. A win changes her rating by the opponent's contribution, and a loss changes her rating by her own contribution. Since these are the only two possible transitions, the algorithm covers every valid case and applies the exact required update.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    c = int(input())
    o = int(input())
    result = input().strip()

    if result == "w":
        c += o // 10
    else:
        c -= c // 10

    print(c)

if __name__ == "__main__":
    solve()
```

The first two lines read the two ratings as integers. Python integers handle the possible $10^9$ values safely without overflow concerns.

The condition checks the match result. For a win, the added amount is computed from the opponent's rating. Since all ratings are divisible by 10, integer division by 10 gives the exact number of points gained. For a loss, the subtraction is based on Chloe's current rating.

The order of operations matters in the losing case. The amount removed must be calculated from Chloe's rating before the update. Writing the formula as `c -= c // 10` preserves that behavior because the right side is evaluated before the assignment.

## Worked Examples

Example 1:

Input:

```
1000
1200
w
```

| Step | Chloe rating | Opponent rating | Result | Change |
| --- | --- | --- | --- | --- |
| Initial | 1000 | 1200 | w | none |
| Apply win rule | 1120 | 1200 | w | +120 |
| Output | 1120 | 1200 | w | finished |

This example demonstrates that the gain comes from the opponent's rating. The algorithm keeps Chloe's original rating until the win update is applied.

Example 2:

Input:

```
1500
800
l
```

| Step | Chloe rating | Opponent rating | Result | Change |
| --- | --- | --- | --- | --- |
| Initial | 1500 | 800 | l | none |
| Apply loss rule | 1350 | 800 | l | -150 |
| Output | 1350 | 800 | l | finished |

This example shows the opposite direction. Chloe loses points based on her own rating, even though the opponent's rating is different.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs only input parsing and a fixed number of arithmetic operations. |
| Space | O(1) | Only three integer or string variables are stored. |

The solution uses constant resources, so it easily fits within the limits even when ratings reach their maximum values.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    c = int(sys.stdin.readline())
    o = int(sys.stdin.readline())
    result = sys.stdin.readline().strip()

    if result == "w":
        c += o // 10
    else:
        c -= c // 10

    sys.stdin = old_stdin
    return str(c)

# provided sample
assert solve("""1000
1200
w
""") == "1120", "sample 1"

# custom cases
assert solve("""100
900
l
""") == "90", "minimum values and loss calculation"

assert solve("""1000000000
1000000000
w
""") == "1100000000", "large values"

assert solve("""5000
7000
w
""") == "5700", "win uses opponent rating"

assert solve("""5000
7000
l
""") == "4500", "loss uses own rating"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `100, 900, l` | `90` | Checks the lower boundary and losing formula |
| `1000000000, 1000000000, w` | `1100000000` | Checks large integer handling |
| `5000, 7000, w` | `5700` | Confirms wins use opponent rating |
| `5000, 7000, l` | `4500` | Confirms losses use Chloe's rating |

## Edge Cases

For the case where Chloe wins against a stronger opponent, such as:

```
1000
1200
w
```

the algorithm enters the win branch and adds `1200 // 10`, producing 1120. A solution that uses Chloe's rating for both outcomes would fail here because it would add only 100.

For the case where Chloe loses against an opponent with a very different rating:

```
100
900
l
```

the algorithm enters the loss branch and subtracts `100 // 10`. The opponent's rating is irrelevant for this calculation, so the result is 90. This catches implementations that incorrectly use the opponent's rating when calculating every change.

For equal ratings:

```
5000
5000
w
```

the algorithm adds 500 points and returns 5500. The same arithmetic works because the winner and loser values happen to be equal, confirming that no special handling is needed for this situation.

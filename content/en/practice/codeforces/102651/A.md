---
title: "CF 102651A - The Battle of Giants"
description: "Two teams play an unknown number of matches. A win gives three points to the winner, a draw gives one point to both teams, and a loss gives no points. We know only the final number of points of the first team and the second team."
date: "2026-07-30T22:36:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102651
codeforces_index: "A"
codeforces_contest_name: "Innopolis Open 2020-2021, qualification, contest 1"
rating: 0
weight: 102651
solve_time_s: 402
verified: true
draft: false
---

[CF 102651A - The Battle of Giants](https://codeforces.com/problemset/problem/102651/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

Two teams play an unknown number of matches. A win gives three points to the winner, a draw gives one point to both teams, and a loss gives no points. We know only the final number of points of the first team and the second team. The task is to determine whether this score is achievable and, if it is, find a way to split the matches into first-team wins, draws, and second-team wins using the smallest possible number of matches.

Let `a` be the final score of the first team and `b` be the final score of the second team. The answer must contain three values: how many matches the first team won, how many were draws, and how many the second team won. If no sequence of matches can produce the score, we output `-1`.

The scores can be as large as `10^9`, so trying to simulate matches or iterate over possible numbers of games is impossible. Even a loop of size `a` or `b` could require a billion iterations. The solution has to use arithmetic properties of the scoring system and finish in constant time.

Several boundary situations can break a naive solution. For example, the input

```
0
1
```

has no answer. The difference between the scores is `-1`, but every match changes the score difference by a multiple of three, so this score cannot appear.

Another case is:

```
2
2
```

The correct output is:

```
0 2 0
```

A careless approach might try to represent both scores with wins because three points per win seems efficient, but neither team can have a win without giving the opponent zero points in that match. Two draws are the only way to create two points for both teams.

The case

```
3
0
```

must produce:

```
1 0 0
```

A method that only searches for draws first might miss that a single win already gives the exact score with the minimum number of matches.

## Approaches

A direct brute-force method would try every possible number of wins and draws for the first team, then check whether the second team's score can be formed from the remaining matches. Since the score can reach `10^9`, such a search would need up to billions of iterations in the worst case. The approach is logically correct because it enumerates possible match combinations, but it cannot fit the limits.

The useful observation comes from looking at the score difference. Let `x` be first-team wins, `y` be draws, and `z` be second-team wins. The final scores satisfy:

```
3x + y = a
y + 3z = b
```

Subtracting these equations removes the draws:

```
3x - 3z = a - b
```

So:

```
x - z = (a - b) / 3
```

The difference between the teams' scores must be divisible by three. After checking that condition, the remaining task is to choose the number of wins and losses.

To minimize the total number of matches, we should maximize the number of wins that can replace draws. A win contributes three points to one team, while a draw contributes only one point to each team, so using as many wins as possible reduces the number of matches.

If the first team has a score advantage, we keep the required extra wins for the first team and maximize the second team's wins. The second team can have at most `b // 3` wins. The opposite case is symmetric.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max(a, b)) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the score difference `a - b`. If it is not divisible by three, output `-1`. The difference between the teams' scores is created only by wins, and every win changes the difference by exactly three points.
2. Compute `k = (a - b) / 3`. This value represents how many more wins the first team has than the second team. A positive value means the first team has extra wins, while a negative value means the second team does.
3. If `k` is non-negative, let the second team win as many matches as possible. Set `z = b // 3`, because every second-team win consumes three points from the second team's score. The remaining points of the second team become draws: `y = b - 3z`. The first team then needs `x = z + k` wins to keep the required difference.
4. If `k` is negative, perform the mirrored calculation. Let the first team win as many matches as possible by setting `x = a // 3`. The remaining points become draws, and the second team's wins are `z = x - k`.
5. Output `x`, `y`, and `z`.

Why it works:

The score difference equation fixes the difference between the numbers of wins of the two teams. The algorithm never changes that difference. After assigning the maximum possible number of wins to the team without a required advantage, the leftover points are always less than three, so they can only be produced by draws. This construction produces a valid score. Since every replacement of a draw by a win reduces the number of matches, maximizing wins minimizes the total number of matches.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = int(input())
    b = int(input())

    diff = a - b

    if diff % 3 != 0:
        print(-1)
        return

    k = diff // 3

    if k >= 0:
        z = b // 3
        y = b - 3 * z
        x = z + k
    else:
        x = a // 3
        y = a - 3 * x
        z = x - k

    print(x, y, z)

if __name__ == "__main__":
    solve()
```

The first part checks the only impossible condition. Python integers do not overflow, so values near `10^9` are safe throughout the calculations.

When `k` is positive, the code starts by taking as many second-team wins as possible. This is the key minimization step because those wins replace several draws while preserving the required score difference. The remaining points of the second team are exactly the number of draws.

When `k` is negative, the same idea is applied with the teams swapped. The expression `z = x - k` works because `k` is negative, so it adds the required extra wins for the second team.

The divisions use integer floor division. The remainders after removing all possible wins are always `0`, `1`, or `2`, which are valid numbers of draws. No special handling is needed for zero scores because the formulas naturally produce zero matches.

## Worked Examples

For the input:

```
2
1
```

the trace is:

| a | b | diff | k | x | y | z |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1 | 1 | invalid |  |  |  |

The difference is not divisible by three, so no sequence of matches can create this score. The algorithm rejects it immediately.

For the input:

```
3
0
```

the trace is:

| a | b | diff | k | x | y | z |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 0 | 3 | 1 |  |  |  |
| 3 | 0 | 3 | 1 | 1 | 0 | 0 |

The first team needs one more win than the second team. The second team has no points available for wins or draws, so the answer is one first-team win. This also demonstrates that the construction naturally handles a score where one team has zero points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations are performed |
| Space | O(1) | Only a few integer variables are stored |

The maximum scores are `10^9`, but the algorithm never depends on their size through iteration. It uses a fixed number of calculations, so it easily fits the time and memory limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        a = int(input())
        b = int(input())

        diff = a - b

        if diff % 3 != 0:
            return "-1"

        k = diff // 3

        if k >= 0:
            z = b // 3
            y = b - 3 * z
            x = z + k
        else:
            x = a // 3
            y = a - 3 * x
            z = x - k

        return f"{x} {y} {z}"

    ans = solve()
    sys.stdin = old_stdin
    return ans

assert solution("2\n1\n") == "-1", "sample 1"
assert solution("3\n0\n") == "1 0 0", "sample 2"
assert solution("0\n0\n") == "0 0 0", "both teams score zero"
assert solution("2\n2\n") == "0 2 0", "only draws"
assert solution("1000000000\n1000000000\n") == "333333333 1 333333333", "large equal scores"
assert solution("1\n4\n") == "0 1 1", "second team advantage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 / 0` | `0 0 0` | Empty tournament result |
| `2 / 2` | `0 2 0` | Scores that require draws |
| `1000000000 / 1000000000` | `333333333 1 333333333` | Large values and integer arithmetic |
| `1 / 4` | `0 1 1` | Negative score difference handling |

## Edge Cases

For `0` and `1`, the algorithm calculates `diff = -1`. Since `-1` is not divisible by three, it returns `-1` immediately. This handles the impossible score caused by a difference that no combination of wins can create.

For `2` and `2`, the difference is zero, so the teams must have the same number of wins. The algorithm removes all possible wins with `a // 3 = 0` and leaves two points as draws. It outputs `0 2 0`, which uses the minimum possible number of matches.

For `3` and `0`, the difference is three, so `k = 1`. The first team must have exactly one more win than the second team. The second team has no points, giving `z = 0` and `y = 0`, and the result is `x = 1`. The algorithm avoids creating unnecessary draws and returns the smallest possible tournament.

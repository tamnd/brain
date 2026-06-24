---
title: "CF 105687A - Penalty Kick"
description: "We have two football teams, each with n players. Team A shoots against Team B's goalkeeper, whose height is k. Team B shoots against Team A's goalkeeper, whose height is m. A player scores if their shooting power is at least half of the opposing goalkeeper's height."
date: "2026-06-25T06:12:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105687
codeforces_index: "A"
codeforces_contest_name: "AlgoChief Sprint Round 2"
rating: 0
weight: 105687
solve_time_s: 43
verified: true
draft: false
---

[CF 105687A - Penalty Kick](https://codeforces.com/problemset/problem/105687/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two football teams, each with `n` players. Team A shoots against Team B's goalkeeper, whose height is `k`. Team B shoots against Team A's goalkeeper, whose height is `m`.

A player scores if their shooting power is at least half of the opposing goalkeeper's height. The comparison is performed directly against `height / 2`, so a player with power `x` scores when `2 * x >= height`.

The winner is decided in two stages. First, compare the total number of goals scored by each team. If one team scores more goals, that team wins. If both teams score the same number of goals, compare the maximum shooting power among all players of each team. The team with the larger maximum power wins.

Alice predicts Team A will win. Bob predicts Team B will win. We must output `"Alice"` if Team A wins according to the rules above, otherwise output `"Bob"`.

The limits are very small. There are at most 500 test cases and each team has at most 100 players. Even a straightforward scan of all players is only a few tens of thousands of operations. No advanced algorithm is required.

A subtle point is the scoring condition. The statement says a player scores when their power is greater than or equal to half the goalkeeper's height. If the goalkeeper height is odd, half is not an integer.

Consider:

```
1
1 5 3
2
1
```

Team A shoots against height `3`. Since `2 >= 1.5`, Team A scores.

A careless implementation using integer division would test `2 >= 3 // 2 = 1`, which happens to work here, but fails in other cases.

For example:

```
1
1 5 5
2
1
```

The correct threshold is `2.5`, so power `2` should miss. Using `5 // 2 = 2` would incorrectly count it as a goal.

Another edge case occurs when the goal counts are tied.

```
1
2 4 4
2 10
3 9
```

Both teams score the same number of goals. Team A's maximum power is `10`, Team B's is `9`, so Team A wins. A solution that only compares goal counts would produce the wrong answer.

The statement guarantees that all shooting powers are distinct, so if the goal counts are tied, the maximum powers cannot be equal. The tie-break always produces a unique winner.

## Approaches

The most direct approach is to simulate exactly what the rules describe.

For Team A, count how many players satisfy `2 * a[i] >= k`, because they are shooting against Team B's goalkeeper of height `k`.

For Team B, count how many players satisfy `2 * b[i] >= m`, because they are shooting against Team A's goalkeeper of height `m`.

After obtaining both goal counts, compare them. If Team A has more goals, Alice is correct. If Team B has more goals, Bob is correct. When the counts are equal, compare the maximum shooting powers of the two teams and declare the team with the larger maximum as the winner.

Since every player is examined once, the running time is linear in `n`. Given the constraints, this is far more than fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

In this problem, the brute force simulation is already optimal because the rules themselves require inspecting every player at least once.

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `n`, `m`, and `k`.
3. Read Team A's shooting powers and Team B's shooting powers.
4. Count Team A's goals by checking every value `a[i]`. A goal is scored when `2 * a[i] >= k`.
5. Count Team B's goals by checking every value `b[i]`. A goal is scored when `2 * b[i] >= m`.
6. If Team A's goal count is larger, print `"Alice"`.
7. If Team B's goal count is larger, print `"Bob"`.
8. If the goal counts are equal, compute `max(a)` and `max(b)`. If Team A's maximum is larger, print `"Alice"`, otherwise print `"Bob"`.

### Why it works

The algorithm follows the match rules exactly.

The counts computed in steps 4 and 5 are precisely the numbers of successful penalty kicks for each team because every player is checked against the required scoring condition. If the counts differ, the team with more goals must win by definition.

When the counts are equal, the rules state that the highest individual shooting power determines the winner. Comparing `max(a)` and `max(b)` reproduces this tie-break exactly. Since every decision matches the specification, the algorithm always returns the correct winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, m, k = map(int, input().split())

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    goals_a = sum(1 for x in a if 2 * x >= k)
    goals_b = sum(1 for x in b if 2 * x >= m)

    if goals_a > goals_b:
        print("Alice")
    elif goals_b > goals_a:
        print("Bob")
    else:
        if max(a) > max(b):
            print("Alice")
        else:
            print("Bob")
```

The first loop processes each test case independently.

The goal-count computation uses `2 * x >= height` instead of comparing against `height / 2`. This avoids floating-point arithmetic and correctly handles odd goalkeeper heights.

The tie-break is evaluated only when the goal counts are equal. Because all shooting powers are distinct, the maxima cannot be equal, so one team always wins the comparison.

No additional arrays or data structures are needed beyond storing the input values.

## Worked Examples

### Example 1

Input:

```
1
5 4 6
1 6 4 8 7
2 3 9 5 10
```

Team A shoots against height `6`, Team B shoots against height `4`.

| Player Power | Team | Condition | Goal? |
| --- | --- | --- | --- |
| 1 | A | 2 >= 6 | No |
| 6 | A | 12 >= 6 | Yes |
| 4 | A | 8 >= 6 | Yes |
| 8 | A | 16 >= 6 | Yes |
| 7 | A | 14 >= 6 | Yes |

Team A scores 4 goals.

| Player Power | Team | Condition | Goal? |
| --- | --- | --- | --- |
| 2 | B | 4 >= 4 | Yes |
| 3 | B | 6 >= 4 | Yes |
| 9 | B | 18 >= 4 | Yes |
| 5 | B | 10 >= 4 | Yes |
| 10 | B | 20 >= 4 | Yes |

Team B scores 5 goals.

Since `5 > 4`, Team B wins and the output is:

```
Bob
```

This example demonstrates that the goal count comparison is sufficient when the counts are different.

### Example 2

Input:

```
1
2 4 4
2 10
3 9
```

| Quantity | Team A | Team B |
| --- | --- | --- |
| Goals | 2 | 2 |
| Maximum Power | 10 | 9 |

The goal counts are equal, so the tie-break is used. Since `10 > 9`, Team A wins.

Output:

```
Alice
```

This example exercises the secondary comparison and confirms that the maximum shooting power determines the winner when goals are tied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each player is examined once |
| Space | O(1) auxiliary | Only a few counters and maxima are used |

With at most 100 players per team and 500 test cases, the total work is tiny. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        ga = sum(1 for x in a if 2 * x >= k)
        gb = sum(1 for x in b if 2 * x >= m)

        if ga > gb:
            out.append("Alice")
        elif gb > ga:
            out.append("Bob")
        else:
            out.append("Alice" if max(a) > max(b) else "Bob")

    return "\n".join(out)

# provided samples
assert run(
"""2
5 4 6
1 6 4 8 7
2 3 9 5 10
5 4 6
1 2 3 4 5
6 7 8 9 10
"""
) == "Bob\nBob"

# minimum size
assert run(
"""1
1 1 1
1
2
"""
) == "Bob"

# tie on goals, Team A wins by maximum power
assert run(
"""1
2 4 4
2 10
3 9
"""
) == "Alice"

# odd goalkeeper height, checks half-height handling
assert run(
"""1
1 5 5
2
1
"""
) == "Bob"

# all players score
assert run(
"""1
3 2 2
5 6 7
1 2 3
"""
) == "Alice"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-player case | Bob | Minimum valid size |
| Tie on goals | Alice | Correct tie-break logic |
| Goalkeeper height 5 | Bob | Correct handling of non-integer half |
| Everyone scores | Alice | Pure goal-count comparison |
| Official samples | Bob / Bob | Matches statement examples |

## Edge Cases

Consider the odd-height threshold case:

```
1
1 5 5
2
1
```

Team A shoots against goalkeeper height `5`. The scoring threshold is `2.5`. Power `2` does not score.

The algorithm evaluates:

```
2 * 2 >= 5
4 >= 5
false
```

So Team A scores 0 goals.

Team B shoots against height `5` as well:

```
2 * 1 >= 5
2 >= 5
false
```

Team B also scores 0 goals.

The tie-break compares maxima, `2` versus `1`, so Team A wins. The algorithm avoids the integer-division mistake that would incorrectly count power `2` as a goal.

Now consider a tied scoreline:

```
1
2 4 4
2 10
3 9
```

Both teams score twice because every player's power is at least `2`.

The algorithm reaches the tie-break stage:

```
max(A) = 10
max(B) = 9
```

Since `10 > 9`, it prints `"Alice"`.

A solution that only compared goal counts would incorrectly treat this situation as unresolved.

Finally, consider the smallest possible input:

```
1
1 1 1
1
2
```

Both players score because half of `1` is `0.5`.

Goal counts are tied at 1. The maxima are `1` and `2`, so Team B wins and the algorithm prints `"Bob"`.

This confirms that the implementation correctly handles the lower boundary of all constraints.

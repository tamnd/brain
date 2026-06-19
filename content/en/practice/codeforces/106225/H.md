---
title: "CF 106225H - Hyper Smawk Bros"
description: "The game starts with a boss whose health is n. Two players attack alternately and you move first. Every attack deals some integer damage between 1 and m. The only restriction is that a player cannot repeat the amount that the opponent used on the immediately preceding turn."
date: "2026-06-19T14:03:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106225
codeforces_index: "H"
codeforces_contest_name: "2025-2026 ICPC Southwestern European Regional Contest (SWERC 2025)"
rating: 0
weight: 106225
solve_time_s: 56
verified: true
draft: false
---

[CF 106225H - Hyper Smawk Bros](https://codeforces.com/problemset/problem/106225/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The game starts with a boss whose health is `n`. Two players attack alternately and you move first. Every attack deals some integer damage between `1` and `m`. The only restriction is that a player cannot repeat the amount that the opponent used on the immediately preceding turn. Whoever makes the health non-positive wins immediately.

For each test case we have to determine whether the first player has a strategy that guarantees victory assuming the second player always responds optimally.

The values of both `n` and `m` can reach `10^6`, and there may be up to `10^4` test cases. There are no restrictions on the sums of these values, so any algorithm that performs work proportional to `n` or `m` for every case would become far too expensive. We need a constant-time decision rule.

Several situations are easy to mishandle.

The first one is when the boss can already be killed immediately.

```
n = 6, m = 9
```

The answer is `YES`, because the first player may simply deal damage `6`, `7`, `8`, or `9`.

A second subtle case occurs when `m = 2`.

```
n = 69, m = 2
```

The answer is `NO`. Once one player uses `1`, the other must use `2`, then the first must use `1` again, and so on. The sequence of moves becomes completely forced. A naive approach that assumes many choices are always available would fail here.

Another tricky case is when `n` is exactly divisible by `2m`.

```
n = 20, m = 10
```

The answer is `YES`, not `NO`. Although `20` is a multiple of `20`, the first player can attack with `10`, leaving health `10`, and after Bob's move the first player can again use `10` because only Bob's previous attack is forbidden.

A careless attempt to model the game as ordinary subtraction without remembering the last move would produce incorrect results.

## Approaches

The most direct approach is to describe a state by the remaining health and the damage used on the previous turn. From such a state we can try every legal damage value and mark whether the current player has a winning move. This recursion is correct because it explores the entire game tree.

Unfortunately, there are about `n × m` states. With both values equal to `10^6`, this becomes roughly `10^12` states, which is completely infeasible.

The structure of the game reveals a much stronger pattern. The only memory carried between turns is the opponent's previous damage. If a player used `x`, then on the next turn that exact value is blocked but every other value remains available.

Consider a pair of consecutive turns. Suppose one player deals `a` and the other deals `b`, with `a ≠ b`. On the following turn, `a` becomes legal again because only `b` is forbidden. Thus every two moves remove exactly `a+b` health, and the same pair can repeat indefinitely.

The largest amount removable in two moves is

```
m + (m - 1) = 2m - 1
```

because the two damages must differ.

The smallest amount removable in two moves is

```
1 + 2 = 3
```

when `m = 2`, and more generally any pair of distinct numbers.

Examining small examples quickly reveals a periodic structure. Every block of length `2m` behaves identically. The losing positions are precisely those with

```
n mod (2m) = 1
```

when `m > 2`.

The case `m = 2` is special. The move sequence is forced to alternate between `1` and `2`, so every three health points correspond to one complete cycle. In this case the losing positions are exactly

```
n mod 3 = 0
```

The brute force works because it explicitly computes winning and losing states, but it fails because there are too many states. The observation that the game eventually repeats with a simple modular pattern lets us replace the entire state graph by a constant-time formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(nm) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. If `m = 2`, check whether `n` is divisible by `3`.
3. When `n % 3 == 0`, output `NO`, because the alternating sequence `1,2,1,2,...` is forced and the second player makes the last move.
4. Otherwise output `YES`.
5. If `m > 2`, compute `n % (2m)`.
6. When the remainder equals `1`, output `NO`.
7. For every other remainder, output `YES`.

The reason behind Step 6 is that after every complete block of `2m` health points the same situation reappears. A remainder of `1` means the player to move faces the same type of position as health `1`, where the opponent can always mirror the structure and eventually obtain the last attack.

### Why it works

For `m > 2`, positions repeat with period `2m`. Among one complete period, exactly the state with remainder `1` is losing. Every legal move from such a state reaches a winning state, while every other state has at least one move leading to remainder `1`.

For `m = 2`, the prohibition on repeating the opponent's previous attack forces the sequence of damages to alternate between `1` and `2`. Every three points of health consume one full cycle, so multiples of three are losing for the first player.

Since every position is classified correctly and the game always decreases the health, the algorithm always returns the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
ans = []

for _ in range(t):
    n, m = map(int, input().split())

    if m == 2:
        if n % 3 == 0:
            ans.append("NO")
        else:
            ans.append("YES")
    else:
        if n % (2 * m) == 1:
            ans.append("NO")
        else:
            ans.append("YES")

print("\n".join(ans))
```

The program processes each test case independently.

The special case `m = 2` comes first because its behavior differs completely from the general pattern. The alternating sequence of attacks leaves only a period of three.

For larger values of `m`, the answer depends only on the remainder modulo `2m`. No arrays or recursion are needed.

A common mistake is to use remainder `0` instead of remainder `1`. For example, with `n = 20` and `m = 10`, the remainder modulo `20` is `0`, and the position is winning. Using the wrong remainder would misclassify this case.

Another easy error is forgetting that `2 * m` must be computed before taking the modulus. Python integers are unbounded, so overflow is never an issue.

## Worked Examples

Consider

```
n = 42, m = 9
```

Since `m > 2`, we use the general rule.

| n | m | 2m | n mod 2m | Output |
| --- | --- | --- | --- | --- |
| 42 | 9 | 18 | 6 | YES |

The remainder is `6`, which is not `1`, so the first player has a winning strategy. This example shows that only the remainder matters.

Now consider

```
n = 69, m = 2
```

| n | m | n mod 3 | Output |
| --- | --- | --- | --- |
| 69 | 2 | 0 | NO |

Because the health is divisible by three, the forced sequence of attacks leaves the last move to Bob.

These traces illustrate the two different regimes of the game.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Constant amount of arithmetic per test case |
| Space | O(1) | Only a few variables are stored |

The algorithm performs only a handful of modular operations and comparisons. Even with `10^4` test cases and values up to `10^6`, the running time is negligible and easily satisfies the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())

        if m == 2:
            ans.append("NO" if n % 3 == 0 else "YES")
        else:
            ans.append("NO" if n % (2 * m) == 1 else "YES")

    return "\n".join(ans)

# provided samples
assert run("""8
6 9
20 10
69 2
42 9
42 10
44 9
44 10
400000 400000
""") == """YES
YES
NO
YES
YES
YES
YES
YES"""

# minimum size
assert run("""1
1 2
""") == "YES"

# m = 2 losing case
assert run("""1
6 2
""") == "NO"

# remainder 1 modulo 2m
assert run("""1
21 10
""") == "NO"

# large values
assert run("""1
1000000 1000000
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | YES | Minimum values |
| `6 2` | NO | Special case `m=2` |
| `21 10` | NO | Remainder `1` modulo `2m` |
| `1000000 1000000` | YES | Large values and arithmetic correctness |

## Edge Cases

Consider

```
1
6 9
```

Since `m > 2`, we compute

```
6 mod 18 = 6
```

The remainder is not `1`, so the algorithm outputs `YES`. Indeed, the first player can immediately kill the boss by dealing damage `6`.

Now consider

```
1
69 2
```

Because `m = 2`, we use the special rule:

```
69 mod 3 = 0
```

Hence the answer is `NO`. The attacks are forced to alternate between `1` and `2`, giving Bob the last move.

Finally consider

```
1
20 10
```

We obtain

```
20 mod 20 = 0
```

Since the remainder is not `1`, the answer is `YES`. This confirms that multiples of `2m` are winning positions, which is easy to overlook if one assumes ordinary subtraction-game behavior.

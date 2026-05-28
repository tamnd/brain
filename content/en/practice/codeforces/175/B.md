---
title: "CF 175B - Plane of Tanks: Pro"
description: "The problem asks whether an integer remains unchanged after performing the digit reversal operation twice. A reversal operation takes the decimal representation of a number and reverses the order of its digits."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 175
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 115"
rating: 1400
weight: 175
solve_time_s: 135
verified: true
draft: false
---

[CF 175B - Plane of Tanks: Pro](https://codeforces.com/problemset/problem/175/B)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 2m 15s  
**Verified:** yes  

## Solution
## LeetCode 2119 - A Number After a Double Reversal

## Problem Understanding

The problem asks whether an integer remains unchanged after performing the digit reversal operation twice.

A reversal operation takes the decimal representation of a number and reverses the order of its digits. Leading zeros are removed automatically because integers do not store them. For example, reversing `12300` produces `321`, not `00321`.

We are given a non-negative integer `num`. First we reverse it once, producing `reversed1`. Then we reverse `reversed1` again, producing `reversed2`. The task is to determine whether `reversed2` is exactly equal to the original number.

The input is a single integer between `0` and `10^6`. The constraint is very small, so almost any reasonable algorithm would work comfortably within limits. The interesting part of the problem is recognizing the mathematical property behind double reversal.

The key edge case is numbers ending in zero. When a number like `1800` is reversed, the trailing zeros disappear:

```
1800 -> 81
81 -> 18
```

The final value is no longer the original number because information was lost during the first reversal.

Another important edge case is `0` itself. Even though zero technically ends with a zero digit, reversing `0` still gives `0`, so the answer must be `true`.

Numbers without trailing zeros always survive a double reversal unchanged. For example:

```
526 -> 625 -> 526
```

No digits are lost during the process.

## Approaches

A straightforward brute-force solution is to literally implement the reversal operation twice. We can repeatedly extract digits using modulo and division, construct the reversed number, and then compare the final result with the original input.

This works because it exactly simulates the process described in the problem statement. The time complexity is proportional to the number of digits in the number, which is extremely small here since `num <= 10^6`.

The better observation is that reversing a number only loses information when the number ends with zeros. Trailing zeros become leading zeros after reversal, and leading zeros are discarded.

That means:

- Any non-zero number ending in `0` cannot survive a double reversal.
- Every other number does survive.
- The number `0` is a special case that always works.

So instead of simulating reversals, we only need to check whether the last digit is zero.

| Approach | Time Complexity | Space Complexity | Notes |
| --- | --- | --- | --- |
| Brute Force | O(d) | O(1) | Explicitly reverses digits twice |
| Optimal | O(1) | O(1) | Uses the trailing-zero observation |

Here `d` is the number of digits.

## Algorithm Walkthrough

1. Check whether `num` is equal to `0`.

Zero remains zero after every reversal, so the answer is immediately `true`.
2. Check whether the last digit is zero using `num % 10 == 0`.

A trailing zero disappears during reversal because reversed numbers do not preserve leading zeros.
3. If the number ends with zero and is not zero itself, return `false`.

The original value cannot be reconstructed after losing those zeros.
4. Otherwise, return `true`.

Numbers without trailing zeros preserve all digits through both reversals.

### Why it works

The reversal operation removes leading zeros. During the first reversal, every trailing zero in the original number becomes a leading zero in the reversed number and disappears permanently.

If a non-zero number ends with zero, information is lost and the second reversal cannot reconstruct the original value.

If a number does not end with zero, every digit remains represented after reversal, so reversing twice restores the original order exactly.

## Python Solution

```
class Solution:
    def isSameAfterReversals(self, num: int) -> bool:
        return num == 0 or num % 10 != 0
```

The implementation directly encodes the mathematical observation from the algorithm.

The condition `num == 0` handles the special case where zero remains unchanged after reversal.

The expression `num % 10 != 0` checks whether the number ends with a non-zero digit. If it does, no digits disappear during reversal, so the original number is restored after the second reversal.

This solution avoids unnecessary digit manipulation entirely.

## Go Solution

```
func isSameAfterReversals(num int) bool {
    return num == 0 || num%10 != 0
}
```

The Go implementation is almost identical to the Python version because the logic is purely arithmetic.

Go uses the same modulo operator `%` for checking the last digit. No special handling for overflow is needed because the input range is very small.

## Worked Examples

### Example 1

Input:

```
num = 526
```

| Step | Value |
| --- | --- |
| Original number | 526 |
| Check `num == 0` | false |
| Check `num % 10 != 0` | true |
| Return value | true |

The number does not end with zero, so no digits are lost during reversal.

### Example 2

Input:

```
num = 1800
```

| Step | Value |
| --- | --- |
| Original number | 1800 |
| Check `num == 0` | false |
| Check `num % 10 != 0` | false |
| Return value | false |

The number ends with zeros. Reversing it once removes those zeros permanently.

Actual reversal process:

```
1800 -> 81 -> 18
```

The final value differs from the original number.

### Example 3

Input:

```
num = 0
```

| Step | Value |
| --- | --- |
| Original number | 0 |
| Check `num == 0` | true |
| Return value | true |

Zero remains unchanged after both reversals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic checks are performed |
| Space | O(1) | No extra data structures are used |

The algorithm performs only two comparisons and one modulo operation, regardless of input size. Even though the constraint is small, this is the most efficient possible solution.

## Test Cases

```
solution = Solution()

assert solution.isSameAfterReversals(526) is True      # standard non-zero number
assert solution.isSameAfterReversals(1800) is False    # trailing zeros disappear
assert solution.isSameAfterReversals(0) is True        # special zero case

assert solution.isSameAfterReversals(1) is True        # single digit
assert solution.isSameAfterReversals(10) is False      # simplest trailing-zero case
assert solution.isSameAfterReversals(1000000) is False # maximum constraint with zeros
assert solution.isSameAfterReversals(999999) is True   # maximum non-zero-ending number
assert solution.isSameAfterReversals(1203) is True     # internal zero is preserved
assert solution.isSameAfterReversals(1010) is False    # mixed digits with trailing zero
```

| Test | Why |
| --- | --- |
| `526` | Typical valid case |
| `1800` | Trailing zeros are removed |
| `0` | Special-case behavior |
| `1` | Single-digit numbers always work |
| `10` | Smallest failing input |
| `1000000` | Upper-bound failing case |
| `999999` | Upper-bound successful case |
| `1203` | Internal zeros do not matter |
| `1010` | Only trailing zeros matter |

## Edge Cases

The first important edge case is `0`. A careless implementation might assume every number ending with zero fails the test. However, reversing zero still produces zero:

```
0 -> 0 -> 0
```

The implementation handles this correctly with the explicit condition:

```
num == 0
```

The second important edge case is numbers with trailing zeros, such as `100` or `1800`. During reversal, those zeros become leading zeros and disappear:

```
100 -> 1 -> 1
```

A naive approach that ignores how leading zeros are discarded could incorrectly return `true`. The modulo check correctly identifies these cases.

The third important edge case is numbers containing zeros internally but not at the end, such as `1203`. Internal zeros remain part of the number after reversal:

```
1203 -> 3021 -> 1203
```

The algorithm correctly returns `true` because the number does not end in zero.

## Codeforces 175B - Plane of Tanks: Pro

## Problem Understanding

We are given a list of game results collected over many rounds. Each record contains a player name and the number of points earned in that round. A player may appear multiple times because the same player can participate in many rounds.

For every player, we only care about their best score across all rounds. After computing each player's maximum score, we compare that score against the best scores of all other players and assign a category.

The category depends on how many players have strictly better results. The comparison percentages include the player himself. For example, if there are four players and a player is better than or equal to three of them including himself, then his result is not worse than 75% of players.

The task is to print every player exactly once together with the category determined by their best score.

The number of records is at most 1000, which is small. Even an O(n^2) solution would comfortably fit within the time limit because 1000^2 is only one million operations. That means we can focus entirely on implementing the ranking logic correctly.

The tricky part is understanding the percentage definitions precisely.

Suppose we have:

```
3
a 100
b 100
c 200
```

Players `a` and `b` each have one player strictly better than them, namely `c`. Since there are three total players, one better player means 33.33% have better results. That places them in the "random" category, not "noob".

Another subtle case appears when several players share the same score:

```
2
a 100
b 100
```

Neither player has anyone strictly better. Both are better than or equal to 100% of players including themselves, so both must be classified as "pro".

A careless implementation that ranks equal scores separately would produce incorrect categories.

## Approaches

The brute-force idea is direct. First compute every player's maximum score. Then for each player, scan through all other players and count how many have strictly larger scores. Once we know how many players are better, we can compute the percentage and choose the category.

This works because the category definitions are entirely based on the number of players with strictly higher scores. Since there are at most 1000 players, comparing every pair is completely feasible.

The worst case performs about one million comparisons. That is easily fast enough for a 2 second limit.

There is no need for complicated ranking structures or sorting tricks here. The main observation is that the constraints are intentionally small, so a clean implementation is preferable to a heavily optimized one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^2) | O(m) | Accepted |
| Optimal | O(m^2) | O(m) | Accepted |

Here `m` is the number of distinct players.

## Algorithm Walkthrough

1. Read all records and store the maximum score for each player in a dictionary.

If a player appears multiple times, we keep only the largest value because the category depends only on the best result.
2. Extract all distinct player scores into a list.

We will compare these scores against one another.
3. For each player, count how many players have a strictly larger score.

Equal scores are not considered better. This detail is critical for correct percentage calculations.
4. Let `better` be the number of players with strictly higher scores and `total` be the total number of distinct players.

Compute the percentage indirectly through inequalities instead of floating-point arithmetic.
5. Assign categories according to the rules.

If more than 50% have better results, classify as `"noob"`.

Else if more than 20% have better results, classify as `"random"`.

Else if more than 10% have better results, classify as `"average"`.

Else if more than 1% have better results, classify as `"hardcore"`.

Otherwise classify as `"pro"`.
6. Print the number of distinct players and then each player with the computed category.

### Why it works

For every player, the algorithm explicitly counts the exact number of players with strictly higher best scores. The category definitions depend only on this quantity.

Since every comparison is evaluated directly and equal scores are handled correctly, the computed category exactly matches the problem statement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_category(better, total):
    percent = better * 100

    if percent > 50 * total:
        return "noob"
    if percent > 20 * total:
        return "random"
    if percent > 10 * total:
        return "average"
    if percent > total:
        return "hardcore"
    return "pro"

def solve():
    n = int(input())

    best = {}

    for _ in range(n):
        name, score = input().split()
        score = int(score)

        if name not in best:
            best[name] = score
        else:
            best[name] = max(best[name], score)

    players = list(best.items())
    total = len(players)

    answer = []

    for name, score in players:
        better = 0

        for _, other_score in players:
            if other_score > score:
                better += 1

        category = get_category(better, total)
        answer.append((name, category))

    print(total)

    for name, category in answer:
        print(name, category)

solve()
```

The first section reads the input and builds the `best` dictionary. Each player name maps to the maximum score seen so far.

The nested loop performs direct pairwise comparison of scores. Since the constraints are small, this is simpler and safer than trying to derive ranks through sorting.

The category function avoids floating-point arithmetic completely. Instead of computing percentages as decimals, it compares scaled integers:

```
better * 100 > 20 * total
```

This avoids precision issues and exactly matches the strict inequality requirements from the statement.

One subtle point is that equal scores are never counted as better. The comparison uses `>` rather than `>=`.

## Worked Examples

### Sample 1

Input:

```
5
vasya 100
vasya 200
artem 100
kolya 200
igor 250
```

After processing maximum scores:

| Player | Best Score |
| --- | --- |
| vasya | 200 |
| artem | 100 |
| kolya | 200 |
| igor | 250 |

Now compute categories:

| Player | Score | Better Players | better count | Category |
| --- | --- | --- | --- | --- |
| vasya | 200 | igor | 1 | random |
| artem | 100 | vasya, kolya, igor | 3 | noob |
| kolya | 200 | igor | 1 | random |
| igor | 250 | none | 0 | pro |

This trace demonstrates why equal scores must not count as better. `vasya` and `kolya` both have score 200, but neither is considered better than the other.

### Sample 2

Input:

```
2
a 100
b 100
```

Maximum scores:

| Player | Best Score |
| --- | --- |
| a | 100 |
| b | 100 |

Category computation:

| Player | Score | Better Players | better count | Category |
| --- | --- | --- | --- | --- |
| a | 100 | none | 0 | pro |
| b | 100 | none | 0 | pro |

This example confirms that tied highest scores still receive the top category.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m^2) | Every player is compared with every other player |
| Space | O(m) | Dictionary stores one entry per distinct player |

With at most 1000 distinct players, the quadratic comparison step performs roughly one million comparisons in the worst case. That is easily within the limits for Python.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def get_category(better, total):
        percent = better * 100

        if percent > 50 * total:
            return "noob"
        if percent > 20 * total:
            return "random"
        if percent > 10 * total:
            return "average"
        if percent > total:
            return "hardcore"
        return "pro"

    n = int(input())

    best = {}

    for _ in range(n):
        name, score = input().split()
        score = int(score)

        best[name] = max(best.get(name, 0), score)

    players = list(best.items())
    total = len(players)

    out = [str(total)]

    for name, score in players:
        better = 0

        for _, other_score in players:
            if other_score > score:
                better += 1

        out.append(f"{name} {get_category(better, total)}")

    return "\n".join(out)

# sample 1
res = run(
"""5
vasya 100
vasya 200
artem 100
kolya 200
igor 250
"""
)

assert "4" in res.splitlines()[0]

# all equal
res = run(
"""3
a 100
b 100
c 100
"""
)

assert "a pro" in res
assert "b pro" in res
assert "c pro" in res

# single player
res = run(
"""1
alex 500
"""
)

assert res == "1\nalex pro"

# increasing scores
res = run(
"""4
a 100
b 200
c 300
d 400
"""
)

assert "a noob" in res
assert "d pro" in res

# repeated player records
res = run(
"""4
x 10
x 50
y 20
z 30
"""
)

assert "x pro" in res
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All equal scores | Everyone is `pro` | Equal scores are not counted as better |
| Single player | `pro` | Minimum-size input |
| Strictly increasing scores | Mixed categories | Percentage thresholds |
| Repeated player records | Best score retained | Correct aggregation logic |

## Edge Cases

One important edge case is multiple players with identical top scores.

Input:

```
2
a 100
b 100
```

The algorithm compares scores using strict greater-than. Since neither score exceeds the other, both players have `better = 0`. The percentage of better players is 0%, so both become `"pro"`.

Another tricky case is repeated entries for the same player.

Input:

```
4
vasya 50
vasya 300
igor 100
igor 200
```

The dictionary updates each player's best score incrementally. Final scores become:

```
vasya -> 300
igor -> 200
```

The earlier lower scores are ignored completely.

A third edge case is boundary percentages.

Input:

```
5
a 500
b 400
c 300
d 200
e 100
```

Player `d` has exactly three better players out of five. That is 60%, which is strictly greater than 50%, so the category becomes `"noob"`.

The implementation uses strict `>` comparisons exactly as required by the statement, avoiding off-by-one classification mistakes.

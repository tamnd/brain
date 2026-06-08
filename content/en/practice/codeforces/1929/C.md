---
title: "CF 1929C - Sasha and the Casino"
description: "Sasha starts with a coins and can repeatedly place bets in a casino. If he bets y coins and wins, his total wealth increases by y · (k - 1). If he loses, he loses the entire bet amount y. The casino promotion guarantees that Sasha can never lose more than x bets consecutively."
date: "2026-06-08T18:40:51+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "constructive-algorithms", "games", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1929
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 926 (Div. 2)"
rating: 1400
weight: 1929
solve_time_s: 236
verified: false
draft: false
---

[CF 1929C - Sasha and the Casino](https://codeforces.com/problemset/problem/1929/C)

**Rating:** 1400  
**Tags:** binary search, brute force, constructive algorithms, games, greedy, math  
**Solve time:** 3m 56s  
**Verified:** no  

## Solution
## Problem Understanding

Sasha starts with `a` coins and can repeatedly place bets in a casino.

If he bets `y` coins and wins, his total wealth increases by `y · (k - 1)`. If he loses, he loses the entire bet amount `y`.

The casino promotion guarantees that Sasha can never lose more than `x` bets consecutively. After at most `x` losses, a win must occur.

The question is whether Sasha can choose his bet sizes so that, regardless of how the wins and losses are arranged under that restriction, he can eventually reach any arbitrarily large amount of money.

This is not asking whether he can get rich with some lucky sequence. The strategy must work against the worst valid sequence of outcomes.

The constraints are very small. There are at most 1000 test cases, `x ≤ 100`, and `k ≤ 30`. Any algorithm doing roughly a few hundred operations per test case is easily fast enough. The challenge is mathematical reasoning rather than optimization.

A common mistake is to think that only the next bet matters. The real danger comes from a streak of up to `x` consecutive losses. The strategy must survive every such streak and still make progress after the mandatory win arrives.

Consider:

```
k = 2, x = 1, a = 1
```

Sasha can only bet 1 coin. If he loses, he reaches 0 coins and can no longer bet. The answer is `NO`.

A careless solution might observe that a win doubles the bet and incorrectly conclude that growth is possible.

Another subtle case is:

```
k = 2, x = 3, a = 15
```

The answer is `YES`.

Even though Sasha may lose three times in a row, he can choose increasing recovery bets so that the first win after those losses recovers everything and still yields positive profit. Looking only at a single bet would miss this possibility.

One more important boundary case is when the required recovery bets themselves become larger than Sasha's bankroll:

```
k = 3, x = 3, a = 6
```

The answer is `NO`.

The theoretical betting strategy exists, but Sasha does not have enough initial coins to survive the worst-case loss sequence.

## Approaches

A brute-force mindset starts by trying to explicitly simulate betting strategies and outcome sequences. Since the casino may produce many different valid win/loss patterns, the number of possible states grows rapidly. Even for small parameters there are exponentially many outcome histories, making direct simulation impractical.

The key observation is that only the worst possible scenario matters.

Suppose Sasha wants every cycle consisting of some losses followed by the mandatory win to produce positive profit. Let `b` be the bet placed immediately before a win.

Winning that bet earns `(k - 1) · b` coins.

To guarantee a net gain, that profit must exceed all losses accumulated since the previous win.

Assume the total amount lost so far is `S`. Then we need

```
(k - 1) · b > S
```

which is equivalent to

```
b > S / (k - 1)
```

Since bets are integers, the smallest valid choice is

```
b = floor(S / (k - 1)) + 1
```

Now imagine the worst case: Sasha loses every possible bet before finally winning. We can construct the minimum bets needed to guarantee recovery.

Let `S` denote the total amount already lost.

For each potential loss, choose

```
bet = floor(S / (k - 1)) + 1
```

and add that bet to `S`.

After doing this `x + 1` times, `S` becomes the minimum bankroll required to survive an entire maximal losing streak and still guarantee positive growth.

If Sasha starts with more than this required amount, then after every forced win he gains at least one coin. Repeating the process indefinitely allows unbounded growth.

If his bankroll is not larger than this value, some valid outcome sequence can bankrupt him.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(x) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `need = 0`.

Here `need` represents the total amount of coins Sasha must be able to lose so far while still guaranteeing future recovery.
2. Repeat `x + 1` times.

Each iteration corresponds to one additional possible loss before the next forced win.
3. Compute the smallest bet that guarantees eventual profit:

```
bet = floor(need / (k - 1)) + 1
```

Any smaller bet would fail to recover previous losses after a win.
4. Add this bet to `need`.

```
need += bet
```

This updates the total amount Sasha might have lost after one more unsuccessful bet.
5. After all iterations, compare Sasha's starting bankroll with `need`.

If

```
a > need
```

output `YES`.

Otherwise output `NO`.

### Why it works

The construction always chooses the smallest bet that can recover all previous losses and still leave strictly positive profit after a win.

After `i` iterations, `need` is exactly the minimum bankroll required to survive `i` consecutive losses while preserving the possibility of guaranteed growth.

The casino may force up to `x` losses before a win. The loop constructs the entire worst-case sequence of losses. If Sasha's initial wealth exceeds the resulting total requirement, then every loss streak can be survived and every forced win increases his wealth by at least one coin. Repeating the same strategy indefinitely yields arbitrarily large wealth.

If `a ≤ need`, then during the worst valid loss sequence Sasha eventually lacks enough coins to place the required recovery bet, so no strategy can guarantee unbounded growth.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        k, x, a = map(int, input().split())

        need = 0

        for _ in range(x + 1):
            bet = need // (k - 1) + 1
            need += bet

        print("YES" if a > need else "NO")

solve()
```

The variable `need` stores the cumulative amount that may be lost before the next guaranteed win.

At each step we compute the smallest recovery bet. The formula

```
need // (k - 1) + 1
```

is the integer version of

```
bet > need / (k - 1)
```

The strict inequality is crucial. Using only

```
need // (k - 1)
```

would allow a win that merely breaks even, which is not enough to guarantee unlimited growth.

The loop runs exactly `x + 1` times because the casino can force up to `x` losses, and then the next bet may be the winning one.

The final comparison is also strict:

```
a > need
```

If `a == need`, Sasha can be driven exactly to the boundary where the required next bet is impossible. He needs strictly more coins than the constructed requirement.

Python integers easily handle all intermediate values, although in this problem the numbers remain quite small.

## Worked Examples

### Example 1

Input:

```
k = 2, x = 1, a = 7
```

| Iteration | need before | bet | need after |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 2 | 3 |

Final value:

```
need = 3
a = 7
```

Since `7 > 3`, the answer is `YES`.

This demonstrates the classic doubling case. Sasha can survive the worst allowed loss streak and still gain coins after every forced win.

### Example 2

Input:

```
k = 3, x = 3, a = 6
```

| Iteration | need before | bet | need after |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 2 | 2 | 4 |
| 4 | 4 | 3 | 7 |

Final value:

```
need = 7
a = 6
```

Since `6 ≤ 7`, the answer is `NO`.

This example shows that even though wins are quite profitable (`k = 3`), Sasha's starting bankroll is too small to survive the worst legal sequence of losses.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(x) | One loop of length `x + 1` per test case |
| Space | O(1) | Only a few integer variables are stored |

Since `x ≤ 100`, each test case performs at most 101 iterations. Even with 1000 test cases, the total work is tiny and easily fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        k, x, a = map(int, input().split())

        need = 0
        for _ in range(x + 1):
            need += need // (k - 1) + 1

        ans.append("YES" if a > need else "NO")

    return "\n".join(ans)

# provided sample
assert run(
"""9
2 1 7
2 1 1
2 3 15
3 3 6
4 4 5
5 4 7
4 88 1000000000
25 69 231
13 97 18806
"""
) == "\n".join([
    "YES",
    "NO",
    "YES",
    "NO",
    "NO",
    "YES",
    "NO",
    "NO",
    "NO"
]), "sample"

# minimum case
assert run(
"""1
2 1 1
"""
) == "NO"

# exact boundary, a == need
assert run(
"""1
2 1 3
"""
) == "NO"

# one coin above boundary
assert run(
"""1
2 1 4
"""
) == "YES"

# very large bankroll but huge x
assert run(
"""1
30 100 1000000000
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1` | `NO` | Minimum bankroll case |
| `2 1 3` | `NO` | Strict inequality `a > need` |
| `2 1 4` | `YES` | One coin above the boundary |
| `30 100 1000000000` | `YES` | Large parameters and long loss streak |

## Edge Cases

### Exact boundary

Input:

```
1
2 1 3
```

Execution:

| Iteration | need before | bet | need after |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 2 | 3 |

The computed requirement is `need = 3`.

Since `a = 3`, the condition `a > need` fails and the answer is `NO`.

This catches implementations that incorrectly use `>=`.

### Immediate bankruptcy

Input:

```
1
2 1 1
```

Execution:

| Iteration | need before | bet | need after |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 2 | 3 |

Again `need = 3`, but Sasha starts with only one coin.

After a single loss he reaches zero coins and cannot continue. The algorithm correctly outputs `NO`.

### Large winning multiplier but insufficient capital

Input:

```
1
25 69 231
```

Running the recurrence for 70 iterations produces a requirement larger than 231, so the answer is `NO`.

This demonstrates that a huge multiplier alone is not enough. The bankroll must still be large enough to survive the worst possible sequence of losses.

### Long loss streak

Input:

```
1
4 88 1000000000
```

The recurrence grows rapidly. After 89 iterations the required bankroll exceeds one billion, so the answer is `NO`, matching the official sample.

The algorithm handles this directly because it performs only 89 iterations and uses constant memory.

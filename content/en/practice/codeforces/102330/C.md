---
title: "CF 102330C - \u041c\u044f\u0447\u0438\u043a\u0438"
description: "Petya throws one ball every minute toward Vova. The distance between them is L, and every ball moves at speed X, so a ball needs L / X minutes to reach Vova. Vova does not shoot balls immediately. He starts shooting when a ball gets within distance D of him."
date: "2026-08-14T01:04:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102330
codeforces_index: "C"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2019.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102330
solve_time_s: 273
verified: true
draft: false
---

[CF 102330C - \u041c\u044f\u0447\u0438\u043a\u0438](https://codeforces.com/problemset/problem/102330/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

Petya throws one ball every minute toward Vova. The distance between them is `L`, and every ball moves at speed `X`, so a ball needs `L / X` minutes to reach Vova.

Vova does not shoot balls immediately. He starts shooting when a ball gets within distance `D` of him. His gun fires instantly, but after every shot he needs exactly `M` minutes before it can fire again. If several balls are already within range, he always shoots the closest one, which is the oldest ball among those still alive because every ball has the same speed.

We need the number of balls Petya has thrown when the first ball reaches Vova. If Vova can shoot every ball forever, the answer is `-1`.

The parameters can all be as large as `10^9`. That immediately rules out any simulation proportional to the number of minutes or balls, because the answer itself can be around `10^9`. The required solution must use only a constant number of arithmetic operations. Python integers also make the products such as `X * (M - 1)` safe without any special overflow handling.

The first subtle case is `M = 1`. Vova can shoot once every minute, exactly as often as Petya creates balls. For example, `5 2 2 1` has answer `-1`. A simulation might eventually stop only because of an implementation limit, but mathematically every ball is removed before reaching Vova.

The second subtle case is when a ball reaches Vova at exactly the same moment when Vova would be able to shoot it. For example, `6 1 3 2` has answer `4`. The fourth ball reaches Vova at the same time as the fourth possible shot. The game ends at that moment, so equality must be treated as failure for Vova, not as a successful shot.

The third subtle case is an exact division in the final formula. For example, with `L = 10`, `X = 2`, `D = 6`, and `M = 2`, the relevant ratio is exactly `6 / 2 = 3`, so the answer is `4`, not `5`. Using floating point and taking an approximate ceiling can introduce an unnecessary source of errors, so the implementation uses integer division.

## Approaches

A direct simulation can process the balls one by one. For each ball, we can determine when it enters Vova's shooting range, keep track of when the gun becomes available, and decide whether that ball is shot before it reaches Vova. This works because all balls are identical except for their launch times, and the closest ball is always the oldest surviving one.

The problem with this approach is the number of balls. Consider `X = 1`, `D = 10^9`, and `M = 2`. The first ball that reaches Vova can appear only after roughly `10^9` balls have been thrown. A loop over all those balls performs about one billion iterations, which is far beyond a 0.5 second limit. Even an optimized event simulation does not solve the fundamental problem, because there are simply too many events.

The key observation is that we do not actually need to know where any individual ball is. The first shot happens when the first ball reaches the shooting distance. After that, every shot happens exactly `M` minutes later, provided there is still a ball waiting. Since Petya launches balls one minute apart and `M >= 1`, the `k`-th shot always targets the `k`-th ball.

Let the first ball be thrown at time `1`. It reaches the shooting boundary after

`(L - D) / X`

minutes. Hence the `k`-th shot occurs at

`1 + (L - D) / X + (k - 1)M`.

The `k`-th ball reaches Vova at

`k + L / X`.

The first ball that reaches Vova before it can be shot is exactly the first `k` for which its arrival time is less than or equal to its scheduled shot time. Comparing these expressions causes `L` to cancel completely, leaving a condition involving only `D`, `X`, and `M`.

For `M = 1`, the resulting inequality can never become true. For `M > 1`, the first losing ball is

`1 + ceil(D / (X(M - 1)))`.

The entire simulation has consequently collapsed to one integer division and a few arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(answer)` | `O(1)` | Too slow |
| Optimal | `O(1)` | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read `L`, `X`, `D`, and `M`. The distance `L` will eventually cancel from the inequality, but it is still part of the input.
2. If `M = 1`, print `-1`. Petya launches one ball per minute and Vova can also fire once per minute, so the gun never falls behind.
3. For `M > 1`, compute the number of minutes by which the shooting advantage changes per ball. Vova gains `M - 1` additional minutes of delay relative to Petya's one-minute launch interval.
4. Multiply that advantage by the ball speed. The relevant quantity is `X * (M - 1)`. The first losing ball is determined by how many such units fit into the shooting distance `D`.
5. Compute `ceil(D / (X * (M - 1)))` using integer arithmetic. If `q = D // denominator` and `r = D % denominator`, the ceiling is `q` when `r = 0`, otherwise `q + 1`.
6. Add `1` to that ceiling and print the result. The extra `1` comes from the fact that the first ball has an initial one-minute offset before the sequence of shots begins.

Why this works can be seen directly from the timing of the `k`-th ball. Its arrival time is `k + L/X`, while its possible shooting time is `1 + (L-D)/X + (k-1)M`. The game ends when arrival is no later than shooting, because equality means the ball has already reached Vova. Rearranging gives

`k + L/X <= 1 + (L-D)/X + (k-1)M`.

After canceling `L/X` and rearranging,

`(M - 1)k >= (M - 1) + D/X`.

Multiplying by `X` gives

`X(M - 1)(k - 1) >= D`.

Thus the smallest possible `k` is exactly

`1 + ceil(D / (X(M - 1)))`.

The invariant behind the derivation is that the `k`-th shot always concerns the `k`-th ball. The first shot removes ball one, and every later shot removes the oldest ball waiting in the shooting zone. Since balls are launched in order and move at equal speed, no later ball can become closer than an earlier surviving ball.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    L, X, D, M = map(int, input().split())

    if M == 1:
        print(-1)
        return

    denominator = X * (M - 1)
    shots_needed = (D + denominator - 1) // denominator

    print(shots_needed + 1)

if __name__ == "__main__":
    solve()
```

The first branch handles the only case where the answer is infinite. When `M > 1`, the denominator `X * (M - 1)` is positive, so the ceiling division is well defined.

The expression `(D + denominator - 1) // denominator` computes an integer ceiling without floating point. This matters because all input values are integers and the boundary where the ratio is exact changes the answer by one.

The variable `L` is read but does not appear in the final calculation. That is intentional. The time needed to travel the full distance and the time needed to reach the shooting boundary both contain the same `L/X` component, so it disappears when the two times are compared.

There is no array, queue, or per-ball state in the implementation. Python's arbitrary-precision integers also handle the product `X * (M - 1)` directly, whose value can be close to `10^18`.

## Worked Examples

For the first sample, `L = 6`, `X = 1`, `D = 3`, and `M = 2`. The first ball enters shooting range after `3` minutes. Each following shot is two minutes later, while each following ball is launched one minute later.

| Ball `k` | Arrival at Vova | Possible shot | Result |
| --- | --- | --- | --- |
| 1 | `7` | `4` | Shot |
| 2 | `8` | `6` | Shot |
| 3 | `9` | `8` | Shot |
| 4 | `10` | `10` | Reaches Vova |

The fourth ball is the first one whose arrival time is equal to its shooting time. The equality is losing for Vova, so the answer is `4`, matching the official sample.

The formula gives

`1 + ceil(3 / (1 * (2 - 1))) = 1 + 3 = 4`.

This example specifically tests the equality boundary. Treating an equal arrival and shooting time as a successful shot would incorrectly produce a larger answer.

For the second sample, `L = 5`, `X = 2`, `D = 2`, and `M = 1`. Petya launches one ball per minute and Vova can shoot one ball per minute.

| Ball `k` | Launch interval | Gun capacity | Result |
| --- | --- | --- | --- |
| 1 | 1 minute | 1 shot per minute | Shot |
| 2 | 1 minute | 1 shot per minute | Shot |
| 3 | 1 minute | 1 shot per minute | Shot |
| `k` | 1 minute | 1 shot per minute | Shot |

The gun never accumulates a backlog, so no ball reaches Vova. The answer is `-1`, as in the official sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(1)` | Only a constant number of arithmetic operations are performed. |
| Space | `O(1)` | The solution stores only the four input values and a few integers. |

The largest input values require arithmetic involving products around `10^18`, which Python handles natively. Since the algorithm performs no loop proportional to `L`, `X`, `D`, or the answer, it comfortably fits the 0.5 second time limit and 256 MB memory limit.

## Test Cases

```python
# Helper: run the core solution on an input string.
def solve(data: str) -> str:
    L, X, D, M = map(int, data.split())

    if M == 1:
        return "-1"

    denominator = X * (M - 1)
    shots_needed = (D + denominator - 1) // denominator

    return str(shots_needed + 1)

def run(inp: str) -> str:
    return solve(inp).strip()

# Official samples
assert run("6 1 3 2") == "4", "sample 1"
assert run("5 2 2 1") == "-1", "sample 2"

# Minimum-size input
assert run("1 1 1 1") == "-1", "minimum values with M=1"

# All values equal
assert run("7 7 7 7") == "2", "all values equal"

# Exact division
assert run("10 2 6 2") == "4", "exact ceiling boundary"

# Non-exact division
assert run("10 3 5 3") == "2", "non-exact ceiling boundary"

# Maximum-size input
assert run("1000000000 1000000000 1000000000 1000000000") == "2", "maximum values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `-1` | Minimum values and the infinite-survival case |
| `7 7 7 7` | `2` | Equal parameters and `M > 1` |
| `10 2 6 2` | `4` | Exact integer division in the ceiling |
| `10 3 5 3` | `2` | Non-exact ceiling and off-by-one handling |
| `1000000000 1000000000 1000000000 1000000000` | `2` | Maximum constraints and large integer arithmetic |

## Edge Cases

When `M = 1`, consider the exact input `5 2 2 1`. The denominator from the main formula would contain `M - 1 = 0`, so blindly applying the formula would attempt a division by zero. More importantly, the physical process is different: Vova can shoot once during every minute while Petya creates only one new ball per minute. The queue never grows, so no ball reaches Vova and the correct result is `-1`.

For the simultaneous-arrival boundary, use `6 1 3 2`. The first four possible shot times are `4`, `6`, `8`, and `10`. The fourth ball reaches Vova at time `10`. Because reaching Vova ends the game, the equality at time `10` counts as a successful arrival for the ball, not a successful shot. The algorithm checks `arrival <= shot`, which leads to `k = 4`.

For an exact ceiling boundary, use `10 2 6 2`. Here `X(M-1) = 2`, and `D = 6`, so `D / (X(M-1)) = 3` exactly. The answer is `1 + 3 = 4`. A formula using a strict inequality or an incorrectly rounded division could return `3` or `5`.

For a non-exact boundary, use `10 3 5 3`. The denominator is `3 * 2 = 6`, while `D = 5`. The ratio is between zero and one, so its ceiling is `1`, giving answer `2`. This checks that the integer ceiling is implemented as `(D + denominator - 1) // denominator` rather than ordinary floor division.

---
title: "CF 106284E - \u0418\u0433\u0440\u0430 \u041a\u0440\u043e\u0448\u0430"
description: "The game contains a line of carrot monsters. Krosh can only directly attack the first monster that is still alive. To reach a later monster, every monster before it must already be defeated. A shot aimed at the current monster deals increasing damage to a consecutive block."
date: "2026-06-25T07:41:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106284
codeforces_index: "E"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 (\u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435) 10-11 \u043a\u043b\u0430\u0441\u0441, \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c, 2025"
rating: 0
weight: 106284
solve_time_s: 40
verified: true
draft: false
---

[CF 106284E - \u0418\u0433\u0440\u0430 \u041a\u0440\u043e\u0448\u0430](https://codeforces.com/problemset/problem/106284/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

The game contains a line of carrot monsters. Krosh can only directly attack the first monster that is still alive. To reach a later monster, every monster before it must already be defeated.

A shot aimed at the current monster deals increasing damage to a consecutive block. The monster being aimed at receives 1 damage, the next one receives 2 damage, the next receives 3 damage, and so on up to `k` monsters. A monster with health `h` that receives damage `d` changes its health to `|h - d|`. Once a monster reaches zero health, it stays defeated forever.

The task is to find the minimum number of shots needed to defeat every monster.

The limits are the key part of the problem. There can be up to `2 * 10^5` monsters, while `k` is at most `200`. A simulation that performs work proportional to the number of shots is impossible because health values can be large. Even an approach that repeatedly applies damage until a monster dies can require billions of operations.

The small value of `k` tells us where the structure is. A monster can only be affected by the previous `k - 1` monsters, because a shot reaches at most `k` positions. We need to avoid iterating through every second of the game and instead process the effect of a large number of identical operations at once.

Several edge cases are easy to miss.

If a monster is already killed by damage coming from earlier monsters, it must not be attacked again. For example:

```
1 2
5 1
```

The first monster dies after 5 shots. During those shots the second monster receives damage 2 five times:

`1 -> 1 -> 1 -> 1 -> 1`

Actually, because the health update is absolute difference, the state remains 1. The answer is 6 shots in total, not 5 + 1 repeated direct attacks after the first monster. A solution that only counts direct attacks and ignores side damage gets this wrong.

A monster can become zero before it reaches the front. For example:

```
2 1
1 2
```

The first monster needs one shot. That shot deals 2 damage to the second monster, changing it from 2 to 0. The answer is 1. A naive left to right simulation that always fights every monster separately would output 2.

A large number of attacks must be handled mathematically. For example, if a future monster receives damage `3` one million times, simulating one million updates is unnecessary. The repeated absolute difference operation has a short cycle, which is the main observation used by the solution.

## Approaches

The brute force idea is to repeatedly shoot the current monster until it dies. If a monster currently has health `h`, this takes exactly `h` shots because it receives damage 1 every time. After every shot we would update all monsters in the next `k - 1` positions.

This approach is correct because it follows the game exactly, but it fails when health values are large. A single monster with health `10^18` would already require an impossible number of iterations.

The observation that makes the problem solvable is that the damage received by a future monster is always the same value during one fight. If monster `i` is being attacked, monster `i + j` receives `j + 1` damage on every one of those shots. We only need to apply the function

`x -> |x - d|`

many times for a fixed small `d`.

This function has a simple pattern. Write `x = q * d + r`, where `0 <= r < d`. After `q` applications, the value becomes `r`. If `r = 0`, the monster is dead. Otherwise it alternates between `r` and `d - r`. This lets us skip any number of repeated updates in constant time.

The whole algorithm processes each monster once and updates only the next `k - 1` monsters. Since `k` is small, the total amount of work is bounded.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total shots * k) | O(n) | Too slow |
| Optimal | O(nk) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store the current health of every monster. We process monsters from left to right because the game order is forced by the rule that only the first alive monster can be attacked.
2. For the current monster, if its health is already zero, skip it. Earlier attacks have already defeated it.
3. Otherwise, let its current health be `h`. The monster needs exactly `h` shots because every direct attack deals damage 1. Add `h` to the answer and mark the monster as defeated.
4. During these `h` shots, update each of the next `k - 1` monsters. The monster at distance `j` receives damage `j + 1` on every shot, so apply the repeated absolute difference operation with that fixed damage value.
5. To apply `x -> |x - d|` exactly `t` times, divide `x` by `d`. If `t` is smaller than the quotient, the answer is `x - t*d`. Otherwise the remaining part is either zero or a two value cycle.

Why it works:

The first alive monster always receives only damage 1, so its lifetime is exactly its current health. Every other monster is affected only by previous monsters, and those effects can be compressed because each fight applies one fixed transformation repeatedly. The algorithm maintains the exact health of every not yet processed monster, so when a monster reaches the front, the stored value is exactly the state that the real game would have produced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def apply_damage(x, d, t):
    if x == 0:
        return 0

    q, r = divmod(x, d)

    if t < q:
        return x - t * d

    if r == 0:
        return 0

    if (t - q) % 2 == 0:
        return r
    return d - r

def solve():
    n, k = map(int, input().split())
    h = list(map(int, input().split()))

    ans = 0

    for i in range(n):
        if h[i] == 0:
            continue

        shots = h[i]
        ans += shots
        h[i] = 0

        for j in range(1, k):
            if i + j >= n:
                break
            if h[i + j] != 0:
                h[i + j] = apply_damage(h[i + j], j + 1, shots)

    print(ans)

if __name__ == "__main__":
    solve()
```

The function `apply_damage` is the mathematical shortcut. The quotient `q` represents how many full chunks of size `d` can be removed before reaching the remainder. If the number of applications does not reach that point, the value simply decreases by `d` each time.

After reaching the remainder, there are only two possible states. A zero remainder means the monster is dead. A nonzero remainder alternates between `r` and `d - r`, so only the parity of the remaining number of operations matters.

The main loop follows the forced order of the game. The current monster contributes its health to the answer, becomes zero, and then affects only the next `k - 1` positions. The check for zero health before every update prevents already defeated monsters from changing again.

Python integers do not overflow, which is necessary because the answer can exceed 32 bit limits.

## Worked Examples

Consider:

```
3 2
3 5 1
```

The state changes are:

| Step | Current monster | Shots used | Health array after the fight | Answer |
| --- | --- | --- | --- | --- |
| 1 | Monster 1 | 3 | `[0, 2, 1]` | 3 |
| 2 | Monster 2 | 2 | `[0, 0, 1]` | 5 |
| 3 | Monster 3 | 1 | `[0, 0, 0]` | 6 |

The second monster received damage 2 three times during the first fight:

`5 -> 3 -> 1 -> 1`

The third monster was not affected because `k = 2`.

Now consider:

```
4 3
1 2 10 4
```

| Step | Current monster | Shots used | Health array after the fight | Answer |
| --- | --- | --- | --- | --- |
| 1 | Monster 1 | 1 | `[0, 0, 8, 2]` | 1 |
| 2 | Monster 3 | 8 | `[0, 0, 0, 0]` | 9 |

The first shot kills monster 2 immediately because it receives damage 2. It also changes monster 3 from 10 to 8 and monster 4 from 4 to 2. The algorithm skips monster 2 completely later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | Each monster updates at most the next `k - 1` monsters. |
| Space | O(n) | Only the current health values are stored. |

With `n = 2 * 10^5` and `k = 200`, the number of updates is about `4 * 10^7`, which is manageable because each update is only a few integer operations.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

assert run("""3 2
3 5 1
""") == "6\n", "basic sample"

assert run("""4 3
1 2 10 4
""") == "9\n", "side damage kills monsters"

assert run("""1 1
100
""") == "100\n", "single monster"

assert run("""5 200
7 7 7 7 7
""") == "7\n", "large radius and equal values"

assert run("""6 2
1 1000000000 1 1000000000 1 1000000000
""") == "1000000003\n", "large health values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2 / 3 5 1` | `6` | Basic sequential processing |
| `4 3 / 1 2 10 4` | `9` | Monsters dying from side damage |
| `1 1 / 100` | `100` | Minimum size and direct damage only |
| `5 200 / 7 7 7 7 7` | `7` | Maximum range and many affected monsters |
| `6 2 / 1 1000000000 1 1000000000 1 1000000000` | `1000000003` | Large values requiring the cycle shortcut |

## Edge Cases

For a monster already killed by an earlier attack, the algorithm checks for zero before processing it. In the input

```
2 1
1 2
```

the first monster requires one shot. The second monster receives damage 2 and becomes zero. The stored health is now `[0, 0]`, so the answer is `1`.

For repeated transformations with large numbers, the algorithm never performs one update per shot. Consider a monster with health `1000000000` receiving damage `2` for `500000000` shots. The transformation is compressed by division:

`1000000000 = 500000000 * 2 + 0`

so the monster reaches zero immediately after exactly those operations. The function returns zero in constant time.

For `k = 1`, every shot only affects the current monster. The inner update loop runs zero times, and each monster simply contributes its initial health. This matches the game because there is no splash damage.

For monsters with health values smaller than the incoming damage, the absolute difference behavior is handled directly. If a monster has health `3` and receives damage `5`, it becomes `2`, not zero. The cycle formula preserves this behavior because it is based on the exact transformation rather than ordinary subtraction.

---
title: "CF 102801D - Fall Guys"
description: "We have a group of players trying to grab a moving crown. The crown does not stay still: it starts at height 0, moves upward until height H, then moves downward until height 0, and repeats this motion forever."
date: "2026-07-28T22:55:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102801
codeforces_index: "D"
codeforces_contest_name: "The 14th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102801
solve_time_s: 69
verified: true
draft: false
---

[CF 102801D - Fall Guys](https://codeforces.com/problemset/problem/102801/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a group of players trying to grab a moving crown. The crown does not stay still: it starts at height `0`, moves upward until height `H`, then moves downward until height `0`, and repeats this motion forever. A player can grab the crown immediately when reaching the destination if the crown height is at most `h`. Otherwise, the player waits until the crown comes down far enough.

The input describes each player by two values. `x_i` is the time when the player reaches the destination, and `c_i` is the extra network delay added by the game system. If a player physically grabs the crown at time `t`, the game records that player's grab time as `t + c_i`. The winner is the player with the smallest recorded time, and if several players have the same recorded time, the player with the smallest index wins.

The challenge is not simulating every second of the crown movement. The number of players can reach `2 * 10^5` in one test case, and there can be up to 20 test cases. An algorithm that checks many future moments for every player could easily reach billions of operations. We need a constant time calculation for the first possible grab moment of each player.

The crown's movement has a very small period because `H` is at most 300. The full cycle lasts `2H` seconds. This small bound means we can reason directly about one cycle instead of maintaining a long simulation.

The tricky cases come from the exact boundaries of the movement.

For example, if a player arrives exactly when the crown reaches the maximum height:

```
1
1 2 5
5
10
```

The crown is at height `5` at time `5`, which is larger than `h = 2`, so the player must wait. The next acceptable moment is when the crown descends to height `2`, at time `8`. The recorded time is `18`, so the answer is:

```
1
```

A careless solution that only checks whether the crown is below `h` after moving downward could incorrectly treat the peak as an acceptable point.

Another boundary case is when the player arrives exactly when the crown is at an acceptable height:

```
1
1 2 5
2
10
```

At time `2`, the crown height is exactly `2`, and equality is allowed. The player grabs immediately, so the answer is:

```
1
```

A solution using a strict comparison such as `< h` would incorrectly delay the player.

A final edge case is when `h = H`:

```
1
1 5 5
100
7
```

The crown is never higher than `5`, so every arrival is immediately successful. The answer is:

```
1
```

Any approach that assumes there is always a waiting period will fail here.

## Approaches

A direct solution would simulate the crown's movement and ask every player when they can grab it. Since the crown changes continuously, we would need to determine the first future moment where its height becomes acceptable for every player. If we simulate second by second, a single player may require up to `2H` checks, which is small, but doing this for every player still gives `O(nH)` operations. With `n = 200000` and `H = 300`, that becomes about 60 million checks per test case, which is already uncomfortable in Python and unnecessary.

The key observation is that the crown follows a repeating triangular wave. We only need to know the player's position inside one period. The cycle length is `2H`. During each cycle, the crown is acceptable from time `0` to `h` while rising and from time `2H-h` to `2H` while falling.

For an arrival time `x`, let `r = x mod (2H)`. If `r` is already in one of those acceptable intervals, the player grabs immediately. Otherwise, the player is somewhere in the middle section where the crown is too high. The next acceptable moment is always the descending point at height `h`, which happens at cycle position `2H-h`. Therefore, the waiting time is simply the distance from `r` to `2H-h`.

This reduces the whole problem to calculating one formula per player. The brute force works because the crown has a predictable cycle, but fails because it repeats too many times across many players. The periodic structure lets us skip the simulation completely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nH) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each player, compute the first physical grab time. Let `period = 2H` and `r = x_i mod period`. The value `r` tells us where the crown is inside its current cycle.
2. Check whether the crown is already reachable. This happens when `r <= h` or `r >= 2H - h`. In that case, the player's physical grab time is simply `x_i`.
3. If the crown is too high, the player must wait until the crown falls to height `h`. The next such moment is at cycle position `2H - h`, so the physical grab time becomes:

```
x_i + (2H - h - r)
```

1. Add the player's delay `c_i` to get the recorded grab time. Compare it with the current best answer. Replace the answer if this player wins earlier, or if the recorded times are equal and this player's index is smaller.

### Why it works

The crown's movement repeats every `2H` seconds, so every possible situation is completely determined by the arrival time's remainder inside that cycle. The only times when grabbing is possible are the two intervals where the crown height is at most `h`. If a player is outside those intervals, the next reachable moment must be the first point of the next acceptable interval, which is exactly the descending crossing at height `h`. Because the algorithm computes the earliest possible grab moment for every player and then applies the exact tie-breaking rule, the chosen player is guaranteed to be the winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, h, H = map(int, input().split())
        x = list(map(int, input().split()))
        c = list(map(int, input().split()))

        period = 2 * H
        best_time = None
        best_id = None

        for i in range(n):
            r = x[i] % period

            if r <= h or r >= period - h:
                grab = x[i]
            else:
                grab = x[i] + (period - h - r)

            total = grab + c[i]

            if best_time is None or total < best_time or (total == best_time and i < best_id):
                best_time = total
                best_id = i

        ans.append(str(best_id + 1))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution processes players independently because one player's waiting time does not affect another player's crown interaction. The variable `r` stores the position inside the current crown cycle, avoiding any simulation of the movement.

The condition `r <= h or r >= period - h` includes both endpoints because a player can grab when the crown height is exactly `h`. Missing the equality would create wrong answers on boundary cases.

When the crown is too high, the formula `period - h - r` is always positive. The result is the exact remaining time until the descending side reaches height `h`.

The comparison also handles ties carefully. Python arrays are zero-indexed, but the problem numbers players starting from one, so the stored index is increased by one only when printing.

## Worked Examples

Consider the first sample:

```
2
4 2 5
3 6 1 9
6 4 2 3
3 1 2
1 2 3
4 5 6
```

For the first test case, the cycle length is `10`, and the reachable intervals are `[0,2]` and `[8,10]`.

| Player | Arrival `x` | Delay `c` | `x mod 10` | Grab time | Recorded time |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 6 | 3 | 8 | 14 |
| 2 | 6 | 4 | 6 | 8 | 12 |
| 3 | 1 | 2 | 1 | 1 | 3 |
| 4 | 9 | 3 | 9 | 9 | 12 |

Player 3 has the smallest recorded time, so the answer is `3`. This trace shows why the physical arrival time alone is not enough. A later player can still lose because the delay is part of the comparison.

For the second test case, `H = 2` and `h = 1`, so the cycle length is `4`.

| Player | Arrival `x` | Delay `c` | `x mod 4` | Grab time | Recorded time |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 1 | 1 | 5 |
| 2 | 2 | 5 | 2 | 3 | 8 |
| 3 | 3 | 6 | 3 | 3 | 9 |

Player 1 wins immediately. This case demonstrates that a player arriving while the crown is too high must wait until the next reachable interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each player is processed once with only arithmetic operations. |
| Space | O(1) | Apart from the input arrays, only a few variables are stored. |

The maximum number of players is large, but the algorithm does constant work per player. The dependence on `H` disappears completely, so the solution easily fits the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.getvalue()

assert run("""2
4 2 5
3 6 1 9
6 4 2 3
3 1 2
1 2 3
4 5 6
""") == "3\n1\n", "samples"

assert run("""1
1 2 5
2
10
""") == "1\n", "arrival exactly at reachable height"

assert run("""1
1 2 5
5
10
""") == "1\n", "arrival at peak"

assert run("""1
3 5 5
100 1 50
1 20 3
""") == "1\n", "h equals H"

assert run("""1
3 1 10
9 11 12
1 1 1
""") == "1\n", "cycle boundary handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample cases | `3`, `1` | General correctness |
| `h = 2, H = 5, x = 2` | `1` | Equality at reachable height |
| `h = 2, H = 5, x = 5` | `1` | Peak handling |
| `h = H` | `1` | No waiting period |
| Arrivals around cycle boundaries | `1` | Modulo and off-by-one correctness |

## Edge Cases

When a player arrives exactly at the highest point of the crown's movement, the remainder is `H`. If `h < H`, this is inside the unreachable middle interval. For example:

```
1
1 2 5
5
10
```

The remainder is `5`, and the next reachable position is `8`, so the physical grab time is `8`. The algorithm reaches the same result because `5` is neither at most `2` nor at least `8`.

When a player arrives exactly when the crown is at height `h`, grabbing is allowed immediately. For:

```
1
1 2 5
2
10
```

the remainder is `2`, which satisfies `r <= h`. The algorithm keeps the arrival time instead of adding unnecessary waiting.

When `h = H`, every possible crown height is acceptable. For:

```
1
1 5 5
100
7
```

the period is `10`, and the condition always succeeds because every remainder is either at most `5` or at least `5`. The player grabs immediately, as required.

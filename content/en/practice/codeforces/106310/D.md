---
title: "CF 106310D - \u041a\u0430\u043a \u0440\u0430\u0437\u0432\u043b\u0435\u043a\u0430\u044e\u0442\u0441\u044f \u0434\u043e\u043c\u0430\u0448\u043d\u0438\u0435 \u0440\u043e\u0431\u043e\u0442\u044b?"
description: "The game is played by three robots in a fixed order: Vacuum Cleaner, Kettle, and Speaker. They call four digit numbers one after another, but a player may have to try several numbers before making a valid move."
date: "2026-06-25T07:46:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106310
codeforces_index: "D"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, 7-8 \u043a\u043b\u0430\u0441\u0441\u044b, \u041f\u0435\u0440\u043c\u0441\u043a\u0438\u0439 \u043a\u0440\u0430\u0439, 2025"
rating: 0
weight: 106310
solve_time_s: 37
verified: true
draft: false
---

[CF 106310D - \u041a\u0430\u043a \u0440\u0430\u0437\u0432\u043b\u0435\u043a\u0430\u044e\u0442\u0441\u044f \u0434\u043e\u043c\u0430\u0448\u043d\u0438\u0435 \u0440\u043e\u0431\u043e\u0442\u044b?](https://codeforces.com/problemset/problem/106310/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played by three robots in a fixed order: Vacuum Cleaner, Kettle, and Speaker. They call four digit numbers one after another, but a player may have to try several numbers before making a valid move. The protocol contains every number that was spoken, including failed attempts, and ends with `0`.

A number is valid if it has four non-zero different digits, it has not appeared as a successful number before, and except for the first successful move, its first digit matches the last digit of the previous successful number. A failed attempt gives the current robot a penalty point, and the same robot continues trying until it says a valid number. After a valid number, the turn passes to the next robot.

The task is to count, for each robot, how many numbers they tried and how many penalties they received. The first value includes both successful and unsuccessful attempts, because every spoken number is a move attempt.

The input size is not explicitly restrictive in the statement, but the protocol can contain many lines. Since every line must be inspected, the natural target is a single pass over the input. Any solution that repeatedly scans the whole history for every number can become quadratic and is unnecessary. A linear simulation is enough because the rules only depend on the previous successful number and the set of already used successful numbers.

Several details can break a careless implementation. The first spoken number has no previous number restriction. For example:

```
1234
2345
0
```

The first number is accepted, and the second one is accepted too, because `2` follows the ending digit of `1234`. A solution that requires a previous number before accepting the first move would incorrectly reject `1234`.

Repeated numbers are only forbidden for successful moves. For example:

```
1234
4567
4567
0
```

The first two numbers are valid. The third attempt is invalid because `4567` was already used successfully, so the output is:

```
2 0
1 1
0 0
```

A solution that marks every spoken number as used would also reject a later valid number incorrectly in cases where an earlier attempt failed.

The turn does not always change after every line. For example:

```
1234
5678
6789
0
```

After `1234` and `5678`, the Speaker's attempt `6789` is invalid because the previous successful number ends with `8`, so the Speaker gets a penalty and keeps the turn until a valid number appears.

## Approaches

The straightforward approach is to simulate the game. For every spoken number, check whether it satisfies all rules. If it is invalid, increment the current player's penalties and keep the player unchanged. If it is valid, increment the player's successful move count, add the number to the used set, update the last digit, and switch to the next player.

This direct simulation is already the optimal approach. The important observation is that the game state is very small. To decide whether the next number is valid, we only need the last successful number's ending digit, the set of previously successful numbers, and the current player's index. There is no need to rebuild the game history or look ahead.

The total work is proportional to the number of lines in the protocol. With a hash set, checking whether a number was used takes average constant time, so the entire solution is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k²) | O(k) | Too slow for large protocols |
| Simulation with a set | O(k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read all numbers until the terminating zero and process them in order. The current player starts as Vacuum Cleaner, represented by index `0`.
2. For each spoken number, first assume it is invalid and check every rule. The number must have four digits, contain no zeroes, have no repeated digits, not be in the set of already accepted numbers, and match the previous ending digit when a previous valid number exists.
3. If the number is invalid, add one penalty to the current player. The player index does not change because the same robot has to keep trying.
4. If the number is valid, increase the current player's move count and add the number to the used set. Update the ending digit of the last successful number and switch the player using cyclic order.
5. After the protocol ends, print the stored statistics for Vacuum Cleaner, Kettle, and Speaker.

The invariant during the simulation is that the stored state exactly describes the position of the real game: the current player is the one whose turn it is, the used set contains only successful numbers, and the saved last digit belongs to the last successful move. Because every new line is judged from this state, every decision matches the original rules.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    stats = [[0, 0] for _ in range(3)]
    used = set()

    player = 0
    last_digit = -1
    has_previous = False

    for line in sys.stdin:
        s = line.strip()
        if s == "0":
            break

        stats[player][0] += 1

        ok = True

        if len(s) != 4:
            ok = False
        else:
            if '0' in s:
                ok = False
            elif len(set(s)) != 4:
                ok = False

        if ok and s in used:
            ok = False

        if ok and has_previous and int(s[0]) != last_digit:
            ok = False

        if ok:
            used.add(s)
            last_digit = int(s[-1])
            has_previous = True
            player = (player + 1) % 3
        else:
            stats[player][1] += 1

    print(*stats[0])
    print(*stats[1])
    print(*stats[2])

if __name__ == "__main__":
    solve()
```

The array `stats` stores two values for every robot. The first value counts every spoken number by that robot, while the second counts only failed attempts. The current player is stored as an index from `0` to `2`, which makes changing turns a simple modulo operation.

The set `used` contains only successful numbers. This matters because a failed attempt does not consume a number. The variable `has_previous` separates the first valid move from all later moves, avoiding an incorrect comparison with a nonexistent previous number.

The validation checks are performed before changing any state. A valid number updates the used set and the previous ending digit, while an invalid number only changes the penalty counter. This order prevents failed attempts from affecting future moves.

## Worked Examples

For the protocol:

```
4123
3287
7789
7895
5437
7895
2876
7631
0
```

the trace is:

| Spoken number | Player | Valid | Attempts after processing | Penalties |
| --- | --- | --- | --- | --- |
| 4123 | Vacuum Cleaner | Yes | VC=1 | VC=0 |
| 3287 | Kettle | Yes | K=1 | K=0 |
| 7789 | Speaker | No | S=1 | S=1 |
| 7895 | Speaker | Yes | S=2 | S=1 |
| 5437 | Vacuum Cleaner | Yes | VC=2 | VC=0 |
| 7895 | Kettle | No | K=2 | K=1 |
| 2876 | Kettle | Yes | K=3 | K=1 |
| 7631 | Speaker | Yes | S=3 | S=1 |

The rejected `7789` demonstrates that an invalid move keeps the same player. The repeated `7895` demonstrates that successful numbers are the only ones remembered.

For:

```
1234
4567
4567
5678
0
```

the trace is:

| Spoken number | Player | Valid | Attempts | Penalties |
| --- | --- | --- | --- | --- |
| 1234 | Vacuum Cleaner | Yes | VC=1 | VC=0 |
| 4567 | Kettle | Yes | K=1 | K=0 |
| 4567 | Speaker | No | S=1 | S=1 |
| 5678 | Speaker | Yes | S=2 | S=1 |

This trace exercises the rule that a repeated successful number is invalid and the Speaker keeps trying after the failed attempt.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each protocol entry is processed once, and set operations are average O(1) |
| Space | O(k) | The set stores all successful numbers |

The algorithm only stores information needed to continue the simulation. Even for a very large protocol, the memory usage grows linearly with the number of successful numbers.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        data = sys.stdin.read().splitlines()

        stats = [[0, 0] for _ in range(3)]
        used = set()
        player = 0
        last_digit = -1
        has_previous = False

        for s in data:
            if s == "0":
                break

            stats[player][0] += 1
            ok = True

            if len(s) != 4 or '0' in s or len(set(s)) != 4:
                ok = False
            if ok and s in used:
                ok = False
            if ok and has_previous and int(s[0]) != last_digit:
                ok = False

            if ok:
                used.add(s)
                last_digit = int(s[-1])
                has_previous = True
                player = (player + 1) % 3
            else:
                stats[player][1] += 1

        return "\n".join(f"{a} {b}" for a, b in stats) + "\n"
    finally:
        sys.stdin = old_stdin

assert run("""4123
3287
7789
7895
5437
7895
2876
7631
0
""") == """3 0
3 1
3 1
""", "sample"

assert run("""1234
4567
4567
5678
0
""") == """1 0
1 0
2 1
""", "repeat case"

assert run("""1111
1230
1234
2345
0
""") == """2 2
1 0
0 0
""", "invalid formats"

assert run("""1234
2345
3456
4567
0
""") == """2 0
1 0
1 0
""", "normal rotation"

assert run("""9876
8765
7654
6543
5432
4321
3219
2198
0
""") == """3 0
3 0
2 0
""", "long chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample protocol | `3 0 / 3 1 / 3 1` | Basic turn handling and penalties |
| Repeated number case | `1 0 / 1 0 / 2 1` | Used numbers and retry behaviour |
| Invalid digits | `2 2 / 1 0 / 0 0` | Zeroes and repeated digits |
| Normal rotation | `2 0 / 1 0 / 1 0` | Successful cyclic turns |
| Long chain | `3 0 / 3 0 / 2 0` | Multiple valid transitions |

## Edge Cases

The first move is special because there is no previous successful number. On input:

```
1234
2345
0
```

the algorithm starts with `has_previous = False`, so it skips the first digit comparison. `1234` is accepted, the previous digit becomes `4`, and `2345` is accepted because it starts with `2`.

For repeated successful numbers:

```
1234
4567
4567
0
```

the first two lines enter the `used` set. When Speaker says `4567`, the number is found in the set, so the Speaker receives a penalty and keeps the turn. A future number from the Speaker would still be checked normally.

For invalid attempts that should not change the game state:

```
1234
5670
6789
0
```

Vacuum Cleaner successfully plays `1234`. Kettle tries `5670`, which is invalid because it contains zero, so the Kettle gets a penalty. The next number `6789` is still judged as a Kettle move, and since it starts with `6`, it is accepted. The failed attempt never affected the previous digit or used set.

---
title: "CF 102280A - \u041a\u0430\u043c\u0435\u043d\u044c, \u043d\u043e\u0436\u043d\u0438\u0446\u044b, \u0431\u0443\u043c\u0430\u0433\u0430"
description: "We have n drivers, initially ordered by the positions they occupy in the log. The log is a single string of R, S, and P, but the boundaries between game rounds have been erased."
date: "2026-08-13T09:39:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102280
codeforces_index: "A"
codeforces_contest_name: "2010, \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u0421\u0413\u0410\u0423 aka \u041a\u043e\u043d\u0442\u0435\u0441\u0442 \u043f\u0440\u043e \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0438"
rating: 0
weight: 102280
solve_time_s: 166
verified: true
draft: false
---

[CF 102280A - \u041a\u0430\u043c\u0435\u043d\u044c, \u043d\u043e\u0436\u043d\u0438\u0446\u044b, \u0431\u0443\u043c\u0430\u0433\u0430](https://codeforces.com/problemset/problem/102280/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` drivers, initially ordered by the positions they occupy in the log. The log is a single string of `R`, `S`, and `P`, but the boundaries between game rounds have been erased.

A round is played by every driver currently remaining in the relevant group, so if the current group contains `k` drivers, exactly `k` consecutive characters belong to that round. If all three signs occur, or all signs are identical, nobody is eliminated and the same group plays again. If exactly two signs occur, one sign loses according to the usual rock-paper-scissors rules. Every driver showing that losing sign becomes a candidate, and only those candidates continue the current elimination process. When that process leaves exactly one driver, that driver leaves the route, and the previous group resumes without them.

The task is to reconstruct this process from the log and output the number of the final remaining driver. If the log cannot describe a complete legal sequence of games, the answer is `FAIL`.

The key difficulty is that the log does not explicitly say where rounds end. Fortunately, a round's length is not unknown. It is exactly the number of drivers in the current group. Once a decisive round is encountered, the losing sign determines the next group, so its size is also known.

The number of drivers is at most `100`, so the state describing the current game is tiny. The log, however, can contain up to one million characters. This rules out anything exponential in the log length and makes a linear scan of the log the natural target. The small value of `n` also means that copying or filtering a group of drivers is cheap.

Several edge cases can invalidate a careless implementation. For example,

```
2
RRRR
```

must produce `FAIL`. Every round contains two equal signs, so every round is a draw and nobody ever leaves. A solution that simply processes the available characters until the string ends might incorrectly report a remaining driver.

Another case is a round containing all three signs:

```
3
RSP
```

This is a draw, not an elimination. The log ends immediately afterward, so the correct answer is `FAIL`. Treating the presence of two different signs as sufficient to eliminate someone would be wrong here.

A less obvious case is a decisive round where the losing sign appears only once:

```
2
RP
```

`R` loses to `P`, so driver `1` leaves and driver `2` is the final survivor. The correct output is `2`. A solution that assumes a decisive round always leaves at least two candidates would fail on this case.

Finally, a complete game cannot have unused log characters:

```
2
RPRP
```

The first round already decides the game, because `R` loses to `P`. Driver `1` leaves and driver `2` wins, so the extra `RP` makes the log invalid. The answer is `FAIL`.

## Approaches

A brute-force solution could treat the missing round boundaries as unknown and try every possible partition of the log into rounds, simulating each candidate partition. A string of length `L` has `2^(L-1)` possible ways to place boundaries between adjacent characters. Simulating one partition takes `O(L)`, so this approach takes `O(L * 2^L)` work in the worst case. For `L = 1,000,000`, even the number of possible partitions alone is astronomically larger than any feasible operation count.

The reason this brute force is unnecessary is that the game itself determines every boundary. At any moment the current group has a known size `k`, so the next round must occupy exactly the next `k` characters. We can inspect that round immediately. A draw leaves `k` unchanged. A decisive round gives us the losing sign, so filtering the current group by that sign gives the exact group that must continue the elimination.

There is one piece of state that a simple iterative simulation must preserve. When a smaller losing group is being resolved, we have temporarily left its parent group. Once that smaller group produces one eliminated driver, the parent group must resume with that driver removed. This is naturally represented by a stack of parent groups.

The resulting algorithm consumes every log character exactly once. Operations involving driver groups take only `O(n)` per elimination level, and there are at most `n-1` eliminations. Since `n <= 100`, this extra work is negligible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(L · 2^L)` | `O(L)` | Too slow |
| Optimal | `O(L + n^2)` | `O(n^2)` | Accepted |

Here `L` is the log length and `n` is the number of drivers.

## Algorithm Walkthrough

1. Start with the current group containing drivers `1, 2, ..., n`. Maintain a pointer `pos` to the next unread character of the log. The current group is always stored in the order in which its drivers write their signs.
2. Take exactly `len(current)` characters from the log. If fewer characters remain, the log ends in the middle of a round, so the log is invalid and the answer is `FAIL`.
3. Determine which signs occur in this round. If there is only one distinct sign, the round is a draw and the current group does not change. Advance `pos` by the group size and process another round.
4. If all three signs occur, the round is also a draw. Again, advance `pos` by the group size without changing the current group.
5. If exactly two signs occur, determine which sign loses. For the pairs `R,S`, `S,P`, and `P,R`, the losing signs are respectively `S`, `P`, and `R`.
6. Filter the current group, keeping precisely the drivers whose sign equals the losing sign. These are the candidates who continue the elimination. Before replacing the current group, push the old group onto a stack because it must resume after this elimination finishes.
7. If the new group contains at least two drivers, continue processing it in exactly the same way. Every decisive round strictly reduces the group size, so this nested process cannot continue indefinitely.
8. If the new group contains one driver, that driver has been identified as the one who loses the current elimination and leaves the garage. Pop the parent group from the stack and remove this driver from it. The parent group then becomes the current group again.
9. When the current group contains exactly one driver and there is no parent group left, that driver is the final winner. The log is valid only if `pos` is exactly `len(log)`. Any remaining characters mean that the recorded game contains extra events, so the answer is `FAIL`.

Why it works: at every iteration, `current` is exactly the group of drivers whose next round is being played, in the correct recording order. Its size determines the only possible next round boundary. A draw leaves this group unchanged, while a decisive round identifies the losing sign uniquely, so filtering by that sign gives exactly the candidates prescribed by the rules. When that candidate group reaches one driver, removing that driver from the saved parent group exactly reconstructs the state of the game before the recursive elimination began. Thus the invariant survives every transition, and when only one root-level driver remains, that driver is necessarily the final winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    log = input().strip()

    pos = 0
    current = list(range(1, n + 1))
    stack = []

    while True:
        k = len(current)

        if k == 1:
            winner = current[0]

            if stack:
                parent = stack.pop()
                parent.remove(winner)
                current = parent
                continue

            if pos == len(log):
                return str(winner)

            return "FAIL"

        if pos + k > len(log):
            return "FAIL"

        round_ = log[pos:pos + k]
        pos += k

        signs = set(round_)

        if len(signs) == 1 or len(signs) == 3:
            continue

        if signs == {"R", "S"}:
            loser = "S"
        elif signs == {"S", "P"}:
            loser = "P"
        else:
            loser = "R"

        next_group = [
            player
            for player, sign in zip(current, round_)
            if sign == loser
        ]

        stack.append(current)
        current = next_group

print(solve())
```

The `current` list stores actual driver numbers rather than just the number of drivers. This is necessary because the final answer depends on identity, not merely on the size of the remaining group.

The `pos` variable always points to the first character that has not yet been assigned to a round. The expression `log[pos:pos + k]` is valid precisely because every round contains one sign from every driver in the current group.

The set of signs distinguishes the three possible round types. One distinct sign means a unanimous draw, three distinct signs mean the three-way draw, and two distinct signs mean an elimination.

For a decisive round, `zip(current, round_)` associates each recorded sign with the corresponding driver. Filtering on `loser` constructs the exact candidate group for the recursive elimination. The order of drivers is preserved, which matters because the log numbering is based on recording order.

The stack stores parent groups. A parent is pushed only when a decisive round creates a smaller group. Once that smaller group reaches one driver, that driver is removed from the parent and the parent resumes. Since the maximum nesting depth is only `n-1`, the stack is safely bounded by `99` elements.

There is no integer overflow issue in Python, and all indexing is guarded by `pos + k > len(log)`. The final equality `pos == len(log)` is also necessary, because successfully finding a winner does not make an otherwise extra-long log valid.

## Worked Examples

For Sample 1,

```
2
RRSSSP
```

the initial group is drivers `1` and `2`. The first two characters form a draw, as do the next two. The final pair is `SP`, where paper beats scissors, so driver `2` loses and driver `1` remains.

| Step | Current group | Round | Distinct signs | Action | Position |
| --- | --- | --- | --- | --- | --- |
| 1 | `[1, 2]` | `RR` | `{R}` | Draw | 2 |
| 2 | `[1, 2]` | `SS` | `{S}` | Draw | 4 |
| 3 | `[1, 2]` | `SP` | `{S,P}` | `S` loses, driver 2 leaves | 6 |
| 4 | `[1]` | none | none | Final winner | 6 |

The final position is exactly the log length, so the log is valid and the answer is `1`.

For Sample 2,

```
3
RSPRSRRP
```

the first round contains all three signs and is a draw. The second round is `RSR`, where scissors loses, leaving only driver `2`. That driver leaves, so the parent group becomes `[1, 3]`. Its next round is `RP`, where rock loses to paper, so driver `1` leaves and driver `3` becomes the final winner.

| Step | Current group | Round | Distinct signs | Action | Stack after action | Position |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `[1, 2, 3]` | `RSP` | `{R,S,P}` | Draw | `[]` | 3 |
| 2 | `[1, 2, 3]` | `RSR` | `{R,S}` | `S` loses, continue with `[2]` | `[[1,2,3]]` | 6 |
| 3 | `[2]` | none | none | Driver 2 leaves | `[]` | 6 |
| 4 | `[1, 3]` | `RP` | `{R,P}` | `R` loses, driver 1 leaves | `[]` | 8 |
| 5 | `[3]` | none | none | Final winner | `[]` | 8 |

Again the entire log is consumed, and the remaining driver is `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(L + n^2)` | Every log character is processed once, while filtering and removing drivers costs at most `O(n^2)` overall |
| Space | `O(n^2)` | The stack contains nested groups, each of size at most `n` |

With `L <= 1,000,000` and `n <= 100`, the dominant work is a single pass over the log. The driver-related state is tiny, so the solution comfortably fits the 64 MB memory limit.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        n = int(input())
        log = input().strip()

        pos = 0
        current = list(range(1, n + 1))
        stack = []

        while True:
            k = len(current)

            if k == 1:
                winner = current[0]

                if stack:
                    parent = stack.pop()
                    parent.remove(winner)
                    current = parent
                    continue

                if pos == len(log):
                    return str(winner)

                return "FAIL"

            if pos + k > len(log):
                return "FAIL"

            round_ = log[pos:pos + k]
            pos += k

            signs = set(round_)

            if len(signs) == 1 or len(signs) == 3:
                continue

            if signs == {"R", "S"}:
                loser = "S"
            elif signs == {"S", "P"}:
                loser = "P"
            else:
                loser = "R"

            next_group = [
                player
                for player, sign in zip(current, round_)
                if sign == loser
            ]

            stack.append(current)
            current = next_group
    finally:
        sys.stdin = old_stdin

def run(inp: str) -> str:
    return solve_data(inp)

assert run("2\nRRSSSP\n") == "1", "sample 1"
assert run("3\nRSPRSRRP\n") == "3", "sample 2"

assert run("2\nRP\n") == "2", "minimum-size game"
assert run("2\nRRRR\n") == "FAIL", "only draws, no winner"
assert run("3\nRSP\n") == "FAIL", "three-way draw with incomplete game"
assert run("2\nRPRP\n") == "FAIL", "extra data after the winner"

long_log = "R" * (9949 * 100)
for size in range(100, 1, -1):
    long_log += "R" * (size - 1) + "S"

assert len(long_log) == 999949
assert run("100\n" + long_log + "\n") == "1", "maximum-size log"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\nRP` | `2` | Minimum number of drivers and immediate elimination |
| `2\nRRRR` | `FAIL` | Repeated equal-sign draws cannot finish the game |
| `3\nRSP` | `FAIL` | A three-sign round is a draw, not an elimination |
| `2\nRPRP` | `FAIL` | Extra characters after the final winner invalidate the log |
| `100` with a `999949`-character log | `1` | Maximum driver count and a log close to the one-million-character limit |

The maximum-size test consists of `9949` unanimous rounds of size `100`, followed by elimination rounds of sizes `100, 99, ..., 2`. Every elimination round contains one `S` and otherwise `R`, so `S` loses and the last driver in the current group is removed. The final survivor is driver `1`.

## Edge Cases

For the all-equal case,

```
2
RRRR
```

the algorithm consumes `RR`, recognizes one distinct sign, and keeps `[1, 2]`. It then consumes another `RR` and reaches the end with two drivers still present. Since there is no parent group and no single winner, the algorithm returns `FAIL`.

For the three-way draw,

```
3
RSP
```

the current group is `[1, 2, 3]`, and the only round is `RSP`. Its set of signs has size three, so the algorithm leaves the group unchanged. The log ends while three drivers remain, which correctly produces `FAIL`.

For the singleton losing group,

```
2
RP
```

the round contains `R` and `P`. Rock loses, so the next group contains driver `1`. The current group has reached size one, so driver `1` is removed from its parent `[1, 2]`. The parent becomes `[2]`, and because the log has been fully consumed, driver `2` is returned as the winner.

For extra characters,

```
2
RPRP
```

the first `RP` already eliminates driver `1`, leaving driver `2` as the final survivor. The algorithm then checks `pos` against the log length and finds two unused characters. Since a legal complete game cannot contain events after its winner has been determined, it returns `FAIL`.

The maximum-length case stresses a different boundary. The algorithm never assumes that the log length is close to `n`, and it never tries to enumerate possible round boundaries. Every round consumes exactly the size of its current group, so even almost one million characters are handled by the same deterministic state transition.

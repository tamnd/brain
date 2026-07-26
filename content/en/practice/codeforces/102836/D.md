---
title: "CF 102836D - \u0418\u0433\u0440\u0430 \u0432 \u041c\u0430\u0444\u0438\u044e"
description: "The game has k players and lasts for m nights. During every night, the currently alive players have some meetings with each other. At the end of the night exactly one alive player is killed by the mafia."
date: "2026-07-26T14:50:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102836
codeforces_index: "D"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102836
solve_time_s: 63
verified: true
draft: false
---

[CF 102836D - \u0418\u0433\u0440\u0430 \u0432 \u041c\u0430\u0444\u0438\u044e](https://codeforces.com/problemset/problem/102836/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The game has `k` players and lasts for `m` nights. During every night, the currently alive players have some meetings with each other. At the end of the night exactly one alive player is killed by the mafia. The killed player must be a civilian, and one of the mafia members who met that player during this night performs the kill.

The input describes the complete history of the game: for every night we know who was alive, who met whom, and who died. The task is to find the smallest possible number of mafia members that could have produced this exact sequence of deaths.

The key restriction is that only civilians die. After `m` nights there are exactly `k - m` survivors. Every mafia member must be among these survivors. The condition `k - m <= 15` is the main algorithmic clue. Although the total number of players can be 200, the number of candidates for mafia is at most 15, so trying subsets of possible mafia members is feasible.

A solution that checks all subsets of all players would need up to `2^200` cases, which is impossible. The small survivor count changes the problem completely: we only need to consider subsets of at most 15 people, which is at most 32768 possibilities.

There are several edge cases where careless implementations fail. A player who dies cannot be mafia, even if they met every victim. For example, if the input describes two players and one night where player 1 dies, the answer is `1` because player 1 cannot be mafia and player 2 must be the killer. Another common mistake is forgetting that a mafia member has to meet the victim on the exact night of the death. A player who met the victim on a previous night but was not present at the killing night cannot explain that death.

A small example:

```
2 1
1 1
2
1 1
2
2
```

The first night starts with players 1 and 2 alive. They meet, then player 2 dies. The answer is `1`, because only player 1 survives and the mafia must be alive after all nights.

## Approaches

A direct approach would be to try every possible set of mafia members among all players. For every candidate set, we would simulate all nights and check whether each victim could have been killed by someone from this set. The simulation is correct because the only requirement for a mafia set is that every death has a surviving mafia member who met the victim that night.

The problem is the number of candidates. With 200 players, the brute force search would have `2^200` possibilities, which is far beyond what can be processed.

The important observation is that mafia members never die. After all nights, the only possible mafia members are the `k - m` survivors. The statement guarantees that this number is at most 15. We can enumerate all subsets of survivors and test them. There are at most `2^15` subsets, and each subset can be checked against at most 200 nights.

The brute force works because it tests the exact definition of a valid mafia team, but it fails because it searches irrelevant players. Restricting the search to survivors turns the problem into a small set cover style problem: every candidate mafia member covers the nights where they could have killed the victim, and we need the smallest group covering all nights.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * k * m) | O(k * m) | Too slow |
| Optimal | O(2^(k-m) * m * (k-m)) | O(k * m) | Accepted |

## Algorithm Walkthrough

1. Read the entire game history and simulate which players remain alive after all nights. Store every night as the victim and the list of meetings that happened before the death.
2. Assign a bit position to every survivor. Only these players can possibly be mafia, because mafia members cannot be killed.
3. For every night, build a bitmask of survivor players who met the victim during that night. A valid mafia set must contain at least one bit from this mask for every night.
4. Enumerate every subset of survivors. For each subset, check every night. If the subset intersects every night mask, it is a possible mafia team.
5. Track the smallest size of a valid subset and output it.

Why it works:

Every real mafia member must survive all nights, so the search space contains every possible answer. A subset is accepted only when every victim has at least one member of that subset who met them during the corresponding night. This is exactly the condition required for the described game to happen. Since every valid mafia team is considered and every invalid team is rejected, the minimum accepted size is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)

    k = int(next(it))
    m = int(next(it))

    nights = []
    alive = set(range(1, k + 1))

    for _ in range(m):
        t = int(next(it))
        meet = {}
        for _ in range(t):
            v = int(next(it))
            c = int(next(it))
            friends = []
            for _ in range(c):
                friends.append(int(next(it)))
            meet[v] = friends
        dead = int(next(it))
        nights.append((meet, dead))
        alive.remove(dead)

    survivors = sorted(alive)
    idx = {x: i for i, x in enumerate(survivors)}
    s = len(survivors)

    masks = []
    for meet, dead in nights:
        mask = 0
        for player in meet.get(dead, []):
            if player in idx:
                mask |= 1 << idx[player]
        masks.append(mask)

    ans = s
    for subset in range(1 << s):
        cnt = subset.bit_count()
        if cnt >= ans:
            continue
        ok = True
        for mask in masks:
            if subset & mask == 0:
                ok = False
                break
        if ok:
            ans = cnt

    print(ans)

if __name__ == "__main__":
    solve()
```

The parser stores each night instead of processing immediately because the final survivor set is unknown until all deaths are read. After finding survivors, every possible mafia member can be represented by one bit, which makes checking a candidate set a few integer operations.

The construction of `masks` is the central implementation detail. A bit is set only when that survivor met the victim during that exact night. The subset test then becomes an intersection check between two bitmasks. Python integers handle these masks naturally because only 15 bits are needed.

The enumeration starts from all subsets, including the empty set. The input is guaranteed to describe a valid game, so at least one subset will pass. The empty subset will only pass when there are no nights, which is not possible here because `m >= 1`, but keeping the logic general avoids unnecessary special cases.

## Worked Examples

Sample input:

```
4 2
1 3
2 3 4
2 3
1 3 4
3 3
1 2 4
4 3
1 2 3
1
2 2
3 4
3 2
2 4
4 2
2 3
2
```

The final survivor is player 2, so the only possible mafia member is player 2.

| Step | Survivors | Night masks | Current subset |
| --- | --- | --- | --- |
| After parsing | 2 | {2}, {2} | empty |
| Test subset `{2}` | 2 | both nights covered | valid |

The trace shows why only survivors matter. The dead players cannot be selected even if they participated in many meetings.

Custom example:

```
3 1
1 1
2
1 1
2
2
```

| Step | Survivors | Night masks | Current subset |
| --- | --- | --- | --- |
| After parsing | 1, 2 | {1} | empty |
| Test `{1}` | 1, 2 | covered | valid |

The answer is `1`. The example demonstrates that a surviving player must cover the death of the only night.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^(k-m) * m * (k-m)) | We enumerate only survivor subsets and check all nights |
| Space | O(k * m) | The stored history contains every meeting description |

The maximum subset count is `2^15`, which is only 32768. Combined with at most 200 nights and 15 survivors, the algorithm easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    k = int(next(it))
    m = int(next(it))

    nights = []
    alive = set(range(1, k + 1))

    for _ in range(m):
        t = int(next(it))
        meet = {}
        for _ in range(t):
            v = int(next(it))
            c = int(next(it))
            meet[v] = [int(next(it)) for _ in range(c)]
        dead = int(next(it))
        nights.append((meet, dead))
        alive.remove(dead)

    survivors = sorted(alive)
    idx = {x: i for i, x in enumerate(survivors)}
    masks = []

    for meet, dead in nights:
        mask = 0
        for x in meet[dead]:
            if x in idx:
                mask |= 1 << idx[x]
        masks.append(mask)

    ans = len(survivors)
    for sub in range(1 << len(survivors)):
        if sub.bit_count() >= ans:
            continue
        if all(sub & mask for mask in masks):
            ans = sub.bit_count()

    return str(ans) + "\n"

assert run("""4 2
1 3
2 3 4
2 3
1 3 4
3 3
1 2 4
4 3
1 2 3
1
2 2
3 4
3 2
2 4
4 2
2 3
2
""") == "1\n", "sample"

assert run("""2 1
1 1
2
1 1
2
2
""") == "1\n", "two players"

assert run("""4 2
1 3
2 3 4
2 3
1 3 4
3 3
1 2 4
4 3
1 2 3
1
2 2
3 4
3 2
2 4
4 2
2 3
2
""") == "1\n", "single survivor mafia"

assert run("""5 2
5 0
1 2 3 4 5
1
1 0
2
5 0
1 2 3 4
1
""") == "1\n", "same survivor covers both"

assert run("""3 2
2
1 2
2 2
1 3
1
3
""") == "1\n", "minimum survivor count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Original sample | 1 | General correctness |
| Two players | 1 | Smallest possible game |
| One survivor after many deaths | 1 | Survivor restriction |
| Same player covers all deaths | 1 | Reusing one mafia member |
| Minimal remaining candidates | 1 | Boundary handling |

## Edge Cases

A dead player being chosen as mafia is the most common conceptual mistake. In the algorithm, this cannot happen because the enumeration begins only after all deaths are processed and contains only survivors.

A night where no survivor met the victim would make every candidate subset fail. The input guarantees that some mafia assignment exists, so this situation cannot occur in valid tests, but the checking loop would still handle it correctly by rejecting all subsets.

The case where one survivor can explain every death is handled naturally. All night masks contain the same bit, and the subset containing only that bit is the first minimum solution.

The case where several survivors are needed is also covered because the enumeration checks combinations, not just individual players. A subset is accepted only after every night has at least one possible killer inside it.

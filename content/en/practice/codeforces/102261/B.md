---
title: "CF 102261B - \u0421\u043f\u043e\u0440\u0442\u0438\u0432\u043d\u044b\u0439 \u0442\u0443\u0440\u043d\u0438\u0440"
description: "We are given the list of chess games played in a single-elimination tournament. There were exactly (n=2^k-1) games, so the tournament must have had (2^k) players and (k) rounds."
date: "2026-08-17T20:36:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102261
codeforces_index: "B"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102261
solve_time_s: 120
verified: true
draft: false
---

[CF 102261B - \u0421\u043f\u043e\u0440\u0442\u0438\u0432\u043d\u044b\u0439 \u0442\u0443\u0440\u043d\u0438\u0440](https://codeforces.com/problemset/problem/102261/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the list of chess games played in a single-elimination tournament. There were exactly (n=2^k-1) games, so the tournament must have had (2^k) players and (k) rounds. For every game we know only the two participants, not the round in which the game happened and not who won.

The task has two parts at once. First, we must decide whether the recorded pairs can belong to some valid single-elimination bracket. Second, if such a bracket exists, we must print the two players who could have reached the final. Their actual winner is unknown, so both finalists are possible tournament winners. The official analysis uses the number of games played by each participant to reconstruct the rounds indirectly.

Let (d(v)) be the number of recorded games involving player (v). A player who loses in round (r) can play exactly (r) games, while a finalist plays all (k) rounds. Thus the two finalists must be precisely the players with (d(v)=k), provided the recorded bracket is valid.

The constraint (n\le 2^{16}-1=65535) means there can be up to (65536) distinct participants. Reading and processing every game a constant number of times is easily fast enough for one second, while anything quadratic in the number of games would already require roughly (4.3\cdot10^9) operations at the maximum size. We need a linear or near-linear solution.

There are several subtle cases where simply looking at the underlying graph is not enough. For example, with three games

```
3
A B
B C
C A
```

every player participates twice, so a careless implementation might think that the three participants are all possible finalists. The correct answer is `NO SOLUTION`, because three games in a four-player knockout tournament cannot form a cycle. The problem is not just about degrees, it is about whether games can be separated into valid rounds.

A second important case is

```
3
A B
C D
B C
```

The correct output is `B C`. Here (A) and (D) play once, while (B) and (C) play twice. The first two games can be the first round, and `B C` can be the final. A solution that assumes the input order is the chronological order would happen to accept this example, but that assumption is invalid in general.

A third case is repeated participation in the same inferred round:

```
3
A B
A B
C D
```

The counts are (d(A)=d(B)=2) and (d(C)=d(D)=1). The two games `A B` are both forced into the round corresponding to the smaller participation count, so the same player would have to play twice in one round. The correct answer is `NO SOLUTION`.

## Approaches

A direct brute-force approach would try to assign every recorded game to one of the (k) rounds. Round (r) must contain exactly (2^{k-r}) games, so the number of possible assignments of the (n) games to rounds is

[
\frac{n!}{\prod_{r=1}^{k}(2^{k-r})!}.
]

For every such assignment we could check whether no player appears twice in the same round and whether the resulting schedule forms a knockout tournament. Each candidate assignment takes (\Theta(n)) work to inspect, so the worst-case operation count is

[
\Theta\left(
n\cdot
\frac{n!}{\prod_{r=1}^{k}(2^{k-r})!}
\right).
]

Even for (n=7) this already considers many possibilities, and for (n=65535) the expression is completely infeasible. The brute force is conceptually useful because it tells us what a valid solution must eventually establish, but it treats the unknown round numbers as independent choices when they are actually determined by the participation counts.

The key observation is that a game between players (u) and (v) must have happened in round

[
\min(d(u),d(v)).
]

Suppose (d(u)=3) and (d(v)=5). Player (u) stopped participating after their third game, so their game against (v) had to be their third and final game. Hence the game belongs to round 3. There is no freedom left about its round once all participation counts are known.

This lets us define a pseudo-round for every game. A game ((u,v)) belongs to pseudo-round (r) when (\min(d(u),d(v))=r). In a real knockout tournament, round (r) contains exactly (2^{k-r}) games, and every player appears in at most one game in that round. The remarkable part is that these two conditions are not only necessary, they are sufficient. This is the central characterization used in the official solution.

Why is sufficiency plausible? Consider pseudo-round 1. Every participant must appear there, because anyone who played at least one game has to start the tournament in round 1. Once that first round is removed, every remaining participant has effectively played one fewer game, so the same argument applies recursively to a tournament with one fewer round. This gives an induction on (k).

The resulting algorithm needs only participation counts, pseudo-round assignment, and a check that each pseudo-round contains the required number of distinct participants.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta\left(n\cdot\frac{n!}{\prod_r(2^{k-r})!}\right)) | (O(n)) | Too slow |
| Optimal | (O(n)) expected | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all (n) games and count how many times every player occurs. Call this value (d(v)). This is the only information needed to infer the round of each game.
2. Compute (k=\log_2(n+1)). Since the input guarantees (n=2^k-1), in Python we can obtain it directly as `(n + 1).bit_length() - 1`.
3. For every recorded game ((u,v)), compute

[
r=\min(d(u),d(v)).
]

Put the game into pseudo-round (r). The smaller participation count identifies the participant who has already reached their last game, so this game cannot occur in a later round.
4. For every pseudo-round (r) from 1 through (k-1), verify that it contains exactly

[
2^{k-r}
]

games. A real round has exactly this many matches because there are (2^{k-r+1}) players still alive at its start.
5. For the same pseudo-round, maintain a set of participants. Reject the input if either endpoint of a game has already appeared in that set. A player cannot play twice in the same round of a knockout tournament.
6. Find all players with (d(v)=k). If the previous checks passed, there must be exactly two such players. They are the only players who survived through every round, so they are the two finalists.
7. Print those two names. If any validity check failed, print `NO SOLUTION`.

### Why it works

The invariant is that pseudo-round (r) contains exactly the games that must have happened in real round (r). For a game ((u,v)), at least one endpoint must stop playing immediately after that game, so its round is exactly the smaller of (d(u)) and (d(v)). Thus no valid bracket can place the game anywhere else.

If every pseudo-round has the correct number of games and no participant occurs twice inside one pseudo-round, the first pseudo-round consists of valid disjoint first-round matches. Each match has one player with participation count 1 and one player who continues. Removing that pseudo-round decreases the participation count of every surviving player by one and leaves exactly the same conditions for a tournament with (k-1) rounds. The base case is one game between two players. By induction, the entire set of games can be arranged as a valid knockout bracket.

## Python Solution

```python
import sys
from collections import Counter

input = sys.stdin.readline

def solve():
    n = int(input())
    games = [tuple(input().split()) for _ in range(n)]

    # n = 2^k - 1, so n + 1 = 2^k.
    k = (n + 1).bit_length() - 1

    degree = Counter()

    for u, v in games:
        degree[u] += 1
        degree[v] += 1

    rounds = [[] for _ in range(k + 1)]

    for u, v in games:
        r = min(degree[u], degree[v])

        if r < 1 or r > k:
            print("NO SOLUTION")
            return

        rounds[r].append((u, v))

    for r in range(1, k):
        expected = 1 << (k - r)

        if len(rounds[r]) != expected:
            print("NO SOLUTION")
            return

        used = set()

        for u, v in rounds[r]:
            if u in used or v in used:
                print("NO SOLUTION")
                return

            used.add(u)
            used.add(v)

    finalists = [name for name, cnt in degree.items() if cnt == k]

    if len(finalists) != 2:
        print("NO SOLUTION")
        return

    print(finalists[0], finalists[1])

if __name__ == "__main__":
    solve()
```

The first pass over `games` builds `degree`, which corresponds directly to the participation count (d(v)) from the algorithm. A `Counter` is convenient because every surname can be used as a dictionary key.

The second pass assigns each game to `rounds[min(degree[u], degree[v])]`. The input guarantees the total number of games has the form (2^k-1), so `k` can be recovered without floating-point logarithms. Using bit operations also avoids any rounding issue.

Only pseudo-rounds 1 through (k-1) need explicit collision checking. Once those rounds satisfy the characterization, the remaining games necessarily form the final round. The code still stores pseudo-round (k), but it does not need to inspect it separately.

The set `used` is recreated for every round. This is necessary because a player may legitimately occur once in several different rounds. Rejecting a name merely because it appeared in an earlier round would incorrectly reject players who reached the later stages.

Finally, a valid tournament has exactly two players with participation count (k), namely the two finalists. The explicit `len(finalists) != 2` check makes the implementation robust even if the input violates the structural assumptions in a way that causes the earlier checks to be insufficient.

## Worked Examples

### Sample 1

The seven games imply (k=3), so a valid tournament has four games in round 1, two games in round 2, and one final.

The participation counts are

| Player | Games played |
| --- | --- |
| GORBOVSKII | 3 |
| ABALKIN | 1 |
| SIKORSKI | 2 |
| KAMMERER | 1 |
| BYKOV | 2 |
| IURKOVSKII | 3 |
| PRIVALOV | 1 |
| KIVRIN | 1 |

Now classify every game by the smaller participation count.

| Game | Counts | Pseudo-round |
| --- | --- | --- |
| GORBOVSKII ABALKIN | 3, 1 | 1 |
| SIKORSKI KAMMERER | 2, 1 | 1 |
| SIKORSKI GORBOVSKII | 2, 3 | 2 |
| BYKOV IURKOVSKII | 2, 3 | 2 |
| PRIVALOV BYKOV | 1, 2 | 1 |
| GORBOVSKII IURKOVSKII | 3, 3 | 3 |
| IURKOVSKII KIVRIN | 3, 1 | 1 |

Pseudo-round 1 has four games and contains all eight players exactly once. Pseudo-round 2 has two games and contains `SIKORSKI`, `GORBOVSKII`, `BYKOV`, and `IURKOVSKII` exactly once. The final is `GORBOVSKII IURKOVSKII`.

The two players with degree 3 are `GORBOVSKII` and `IURKOVSKII`, so the algorithm prints them.

### Sample 2

Here (n=3), hence (k=2).

| Player | Games played |
| --- | --- |
| IVANOV | 2 |
| PETROV | 2 |
| BOSHIROV | 2 |

Every game has pseudo-round

[
\min(2,2)=2.
]

Thus pseudo-round 1 contains zero games instead of the required two, while pseudo-round 2 contains all three games instead of the required one.

The algorithm immediately rejects the input. This demonstrates why knowing that there are three participants with the same maximum degree is not enough. A valid four-player knockout bracket must have two first-round games before its final.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) expected | Each game is processed a constant number of times, and set operations are expected (O(1)). |
| Space | (O(n)) | There are at most (2n) participant occurrences and (n) stored games. |

At the maximum (n=65535), the algorithm performs only a few linear passes over roughly sixty-five thousand games. The number of distinct participants is at most (65536), so the dictionaries, lists, and temporary sets are comfortably within the 256 MB memory limit.

## Test Cases

```python
import sys
import io
from collections import Counter

def solve():
    input = sys.stdin.readline

    n = int(input())
    games = [tuple(input().split()) for _ in range(n)]

    k = (n + 1).bit_length() - 1

    degree = Counter()
    for u, v in games:
        degree[u] += 1
        degree[v] += 1

    rounds = [[] for _ in range(k + 1)]

    for u, v in games:
        r = min(degree[u], degree[v])
        if r < 1 or r > k:
            print("NO SOLUTION")
            return
        rounds[r].append((u, v))

    for r in range(1, k):
        expected = 1 << (k - r)

        if len(rounds[r]) != expected:
            print("NO SOLUTION")
            return

        used = set()

        for u, v in rounds[r]:
            if u in used or v in used:
                print("NO SOLUTION")
                return
            used.add(u)
            used.add(v)

    finalists = [name for name, cnt in degree.items() if cnt == k]

    if len(finalists) != 2:
        print("NO SOLUTION")
        return

    print(finalists[0], finalists[1])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def normalized(s: str):
    if s == "NO SOLUTION":
        return s
    return tuple(sorted(s.split()))

sample1 = """\
7
GORBOVSKII ABALKIN
SIKORSKI KAMMERER
SIKORSKI GORBOVSKII
BYKOV IURKOVSKII
PRIVALOV BYKOV
GORBOVSKII IURKOVSKII
IURKOVSKII KIVRIN
"""

sample2 = """\
3
IVANOV PETROV
PETROV BOSHIROV
BOSHIROV IVANOV
"""

assert normalized(run(sample1)) == ("GORBOVSKII", "IURKOVSKII"), "sample 1"
assert run(sample2) == "NO SOLUTION", "sample 2"

minimum_valid = """\
3
A B
C D
B C
"""
assert normalized(run(minimum_valid)) == ("B", "C"), "minimum valid bracket"

all_equal_degrees = """\
3
A B
B C
C A
"""
assert run(all_equal_degrees) == "NO SOLUTION", "cycle with equal degrees"

duplicate_in_round = """\
3
A B
A B
C D
"""
assert run(duplicate_in_round) == "NO SOLUTION", "same player twice in one round"

def make_maximum_valid():
    k = 16
    players = [f"P{i}" for i in range(1 << k)]
    current = players
    games = []

    while len(current) > 1:
        nxt = []
        for i in range(0, len(current), 2):
            u = current[i]
            v = current[i + 1]
            games.append((u, v))
            nxt.append(v)
        current = nxt

    lines = [str(len(games))]
    lines.extend(f"{u} {v}" for u, v in games)
    return "\n".join(lines) + "\n"

maximum_valid = make_maximum_valid()
maximum_answer = normalized(run(maximum_valid))
assert maximum_answer == ("P32767", "P65535"), "maximum valid bracket"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / A B / C D / B C` | `B C` | Minimum valid tournament and correct final-round detection |
| `3 / A B / B C / C A` | `NO SOLUTION` | All three participants have equal degree, but the games cannot form a bracket |
| `3 / A B / A B / C D` | `NO SOLUTION` | A participant appears twice in one inferred round |
| Generated (65535)-game bracket | `P32767 P65535` | Maximum input size, round boundaries, and linear-time processing |

## Edge Cases

The three-player cycle

```
3
A B
B C
C A
```

gives (k=2) and degrees (d(A)=d(B)=d(C)=2). Every game is assigned to pseudo-round 2, because the minimum degree is always 2. The required number of games in pseudo-round 1 is (2^{2-1}=2), but it contains zero, so the algorithm returns `NO SOLUTION`. This catches the mistake of treating the participant degrees alone as sufficient.

The minimum valid tournament

```
3
A B
C D
B C
```

has degrees (1,2,2,1). The games `A B` and `C D` are assigned to pseudo-round 1, while `B C` is assigned to pseudo-round 2. The first round contains two disjoint games, and the second contains the single final. The two players with degree 2 are `B` and `C`, so the output is `B C`.

The repeated game case

```
3
A B
A B
C D
```

has degrees (2,2,1,1). Both copies of `A B` are assigned to pseudo-round 2, while `C D` is assigned to pseudo-round 1. Pseudo-round 1 has the correct number of games, but pseudo-round 2 has two games instead of one. The count check rejects it before the repeated participants can cause any ambiguity.

At the maximum size, (n=65535) gives (k=16) and exactly (65536) players. The first pseudo-round must contain (32768) disjoint games, the second (16384), and so on until the final. The generated maximum test follows exactly this structure, and the two players that appear in all 16 rounds are `P32767` and `P65535`. The implementation never constructs the bracket tree itself, it only verifies the round structure implied by participation counts, which is why the same linear method handles the smallest and largest valid tournaments.

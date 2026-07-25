---
title: "CF 102873A - Catching the Impostor"
description: "The problem describes a group of n players where exactly one player is the hidden impostor. We are given observations of players who were seen completing tasks. A player who appears in the observation list cannot be the impostor."
date: "2026-07-25T13:10:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102873
codeforces_index: "A"
codeforces_contest_name: "Unofficial Div 4 Round #2 by ssense  SlavicG"
rating: 0
weight: 102873
solve_time_s: 47
verified: true
draft: false
---

[CF 102873A - Catching the Impostor](https://codeforces.com/problemset/problem/102873/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a group of `n` players where exactly one player is the hidden impostor. We are given observations of players who were seen completing tasks. A player who appears in the observation list cannot be the impostor. The list can contain the same player multiple times, because seeing someone do several tasks does not give any extra information.

The goal is to determine whether the observations leave exactly one possible impostor. If there is exactly one player who was never seen doing a task, the answer is `YES`. If there are two or more possible impostors, the crew cannot be certain and the answer is `NO`. There is one special case: if every player appears in the list, the information is inconsistent because the impostor must have faked a task, and the problem does not allow us to assume that happened. The answer is also `NO`.

The constraints are small, with both the number of players and the number of observations at most `1000`. This means even solutions using simple linear scans are easily fast enough. A solution around `O(n + k)` performs only a few thousand operations. More complicated approaches such as sorting multiple times or repeatedly checking all players are unnecessary, although they would still likely pass under these limits.

The main edge cases come from confusing appearances with unique players. Duplicate observations do not reduce the number of possible impostors because a player being seen ten times is still just one confirmed non-impostor.

For example:

```
3 3
1 2 2
```

The correct output is:

```
YES
```

Players `1` and `2` are confirmed safe, so only player `3` can be the impostor. A careless implementation that counts observations instead of distinct players might think three players were found and incorrectly answer `NO`.

Another case is when every player appears:

```
3 5
2 1 1 3 3
```

The correct output is:

```
NO
```

All three players were seen doing tasks. Since the impostor cannot normally complete a task, there is no player we can identify with certainty.

A final boundary case is when there are exactly two players:

```
2 2
2 2
```

The correct output is:

```
YES
```

Only player `2` is excluded from being the impostor, leaving player `1` as the unique possibility.

## Approaches

A straightforward brute-force method would try every player as the possible impostor. For each candidate, we could check whether that player appears in the task list. If the player appears, they are impossible. Otherwise, we count them as a possible answer. This is correct because the only information we have is whether a player was ever observed.

The problem with this approach is the repeated scanning. There are up to `1000` players and `1000` observations, so the worst case performs about `1,000,000` checks. This would still pass here, but it is solving a more general problem than necessary.

The key observation is that we do not care how many times a player appears. We only need to know which players appeared at least once. Once those players are marked, the answer is simply determined by how many players remain unmarked.

The brute-force approach works because it asks "is this player possible?" for every player individually, but the observation that all players are independent lets us answer all candidates at once. A boolean array records whether each player was seen, reducing the problem to counting unseen players.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(1) | Accepted here, but unnecessary |
| Optimal | O(n + k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an array that records whether each player has been seen doing a task. Initially every player is considered unseen.
2. Read every observed player and mark that player as seen. Repeated appearances do not change anything because we only care about whether the player appeared at least once.
3. Count the players who are still unseen. These players are exactly the candidates who could be the impostor.
4. If the count of possible impostors is exactly one, print `YES`. Otherwise print `NO`.

The reason this works is that every seen player is eliminated from consideration, and every unseen player remains possible. The crew can identify the impostor only when the remaining set contains exactly one player.

Why it works:

The algorithm maintains the invariant that after processing any prefix of the observation list, the marked players are exactly the players who have appeared in that prefix. At the end, every player who cannot be the impostor is marked. The only players left are those consistent with all observations. If there is one such player, the impostor is uniquely determined. If there are zero or multiple candidates, certainty is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    seen = [False] * (n + 1)

    for _ in range(k):
        x = int(input().strip()) if False else None

    # Re-read input handling the second line containing all values
    data = list(map(int, input().split()))
    for x in data:
        seen[x] = True

    possible = 0
    for i in range(1, n + 1):
        if not seen[i]:
            possible += 1

    print("YES" if possible == 1 else "NO")

if __name__ == "__main__":
    solve()
```

The implementation uses a boolean array indexed by player number. Since player numbers start at `1`, the array has size `n + 1` so that the index matches the player identifier directly.

After reading the observations, each player in the list is marked. The duplicate values do not require special handling because assigning `True` multiple times has the same effect as assigning it once.

The final loop counts unmarked players. The comparison with `1` is the only condition needed because both zero candidates and multiple candidates mean the impostor cannot be identified.

## Worked Examples

For the first sample:

```
3 3
1 2 2
```

| Step | Player processed | Seen array | Possible impostors |
| --- | --- | --- | --- |
| Start | None | [False, False, False] | 3 |
| 1 | Player 1 | [True, False, False] | 2 |
| 2 | Player 2 | [True, True, False] | 1 |
| 2 again | Player 2 | [True, True, False] | 1 |

The only unmarked player is player `3`, so the algorithm prints `YES`. This demonstrates why duplicate observations should not affect the answer.

For the second sample:

```
4 2
3 1
```

| Step | Player processed | Seen array | Possible impostors |
| --- | --- | --- | --- |
| Start | None | [False, False, False, False] | 4 |
| 3 | Player 3 | [False, False, True, False] | 3 |
| 1 | Player 1 | [True, False, True, False] | 2 |

Players `2` and `4` remain possible. Since there is more than one candidate, the output is `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | Each observation is processed once and every player is checked once |
| Space | O(n) | The boolean array stores whether each player was observed |

The constraints allow this approach comfortably. With at most `1000` players, the memory usage is tiny and the running time is far below the limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    n, k = map(int, sys.stdin.readline().split())
    seen = [False] * (n + 1)
    for x in map(int, sys.stdin.readline().split()):
        seen[x] = True

    cnt = sum(1 for i in range(1, n + 1) if not seen[i])
    print("YES" if cnt == 1 else "NO")

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("3 3\n1 2 2\n") == "YES\n", "sample 1"
assert run("4 2\n3 1\n") == "NO\n", "sample 2"
assert run("3 5\n2 1 1 3 3\n") == "NO\n", "sample 3"
assert run("2 2\n2 2\n") == "YES\n", "sample 4"

assert run("2 1\n1\n") == "YES\n", "minimum observations"
assert run("5 5\n1 2 3 4 4\n") == "YES\n", "duplicate values"
assert run("6 6\n1 2 3 4 5 6\n") == "NO\n", "all players seen"
assert run("10 1\n7\n") == "NO\n", "many possible impostors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1` | `YES` | Smallest player count and single remaining candidate |
| `5 5 / 1 2 3 4 4` | `YES` | Duplicate observations do not matter |
| `6 6 / 1 2 3 4 5 6` | `NO` | All players being seen is invalid |
| `10 1 / 7` | `NO` | Many remaining candidates cannot identify the impostor |

## Edge Cases

When observations contain duplicates, the algorithm only changes the state of a player from unseen to seen once.

For:

```
3 3
1 2 2
```

player `2` is processed twice, but the seen state remains the same after the first occurrence. The remaining unseen player is `3`, so the output is `YES`.

When every player appears at least once:

```
3 5
2 1 1 3 3
```

the final seen array marks every player. The count of possible impostors becomes zero. Since there is no player who can be identified as the impostor, the algorithm outputs `NO`.

When only one player is not seen:

```
2 2
2 2
```

the algorithm marks player `2` and leaves player `1` unmarked. The possible impostor count is exactly one, so the answer is `YES`. This case confirms that the number of observations does not matter, only the number of distinct players eliminated.

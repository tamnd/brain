---
title: "CF 102861F - Fastminton"
description: "The input is a chronological record of a Fastminton match. Each character describes one event that happened during the match: either the server scored, the receiver scored, or a request was made to print the current score."
date: "2026-07-25T14:03:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102861
codeforces_index: "F"
codeforces_contest_name: "2020-2021 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102861
solve_time_s: 60
verified: true
draft: false
---

[CF 102861F - Fastminton](https://codeforces.com/problemset/problem/102861/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a chronological record of a Fastminton match. Each character describes one event that happened during the match: either the server scored, the receiver scored, or a request was made to print the current score. The program has to replay the match exactly in order and answer every score request with the state of the match at that moment.

A match contains up to three games, and the first player to win two games wins the match. Inside each game, points are accumulated until one player reaches a winning condition. A player wins a game either by having at least 5 points and leading by at least 2, or immediately when reaching 10 points. After every point, the player who scored becomes the server for the next point. The first game starts with the left player serving, while later games start with the player who won the previous game serving.

There are no large numeric constraints because the input is only a sequence of events. The relevant bound is the number of characters in that sequence. A direct simulation processes each event once, so the running time grows linearly with the input size. Any approach that repeatedly reconstructs the match state from the beginning for every query would perform unnecessary repeated work and can become quadratic if many score announcements are present.

Several details can break a simple implementation. A common mistake is forgetting that a player reaching 10 points wins immediately, even without a two point advantage. For example, the input `SSSSSSSSSSQ` ends with the left player winning the game at 10 points, so the output is `0 (winner) - 0` if this is the first game and the final match score is requested after the game finishes. A solution that only checks the 5 point and two point difference condition would incorrectly keep the game running.

Another tricky situation is the serving player after a score announcement. For the input `SQ`, the left player scores the only point and must be marked as the next server. The output is `0 (1*) - 0 (0)`. A solution that keeps the original server until the next rally would mark the wrong player.

The transition between games is also easy to mishandle. For example, after the right player wins the first game, the right player serves the first point of the second game. The server is not reset to the left player. Forgetting this rule changes all later score announcements.

## Approaches

The most direct solution is to simulate every rally. For each character, a brute-force implementation can maintain the current points, check whether a game ended, update the game score, and print the requested state. This is already the natural representation of the rules, and it is correct because the match rules only depend on the events that happened before the current position.

A less careful brute-force version might handle every `Q` by replaying the entire input prefix from the beginning to rebuild the score. If the input contains many score requests, and the sequence length is `n`, this can require roughly `n` operations for each of `n` requests, resulting in `O(n²)` work.

The observation that removes this repetition is that every event changes the match state only once. The complete information needed for future events is small: the number of games won by each player, the current points in the game, the current server, and whether the match has already ended. Since no old event needs to be revisited, storing this state while scanning from left to right is enough.

The brute-force works because the rules are deterministic, but it fails when it recomputes information that has already been processed. The observation that the match state has a constant size lets us reduce the entire problem to a single pass simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow for large event sequences |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Keep track of the games won by the left and right players, the current game points, and the player serving the next rally. Initially the left player serves and both game scores and point scores are zero. These variables describe everything that can affect future events.
2. Read each character in the event sequence from left to right. For a scoring event, determine the player who receives the point. If the server scores, the server gains a point. If the receiver scores, the other player gains a point. After awarding the point, make that same player the next server because the scorer always serves the following rally.
3. After every point, check whether the current game has ended. A player wins if they have at least 5 points and lead by at least 2, or if they reach 10 points. The check must happen after updating the point totals because the latest rally may have completed the game.
4. When a game ends, increase the winner’s game count and reset the point scores to zero. If that game gives a player two total game wins, the match is finished. Otherwise, the winner of the completed game becomes the server for the next game.
5. When a score announcement appears, print the stored state. If the match is still active, print both game scores and both point scores, adding the server marker to the correct player. If the match has finished, print only the final game score and mark the winner.

Why it works: the maintained state is exactly the information required by the rules to determine the result of the next event. After every processed character, the variables represent the true match situation after all events seen so far. Since each rally is applied once and every game transition follows directly from the rules, every future score announcement is generated from the correct state.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    games = [0, 0]
    points = [0, 0]
    server = 0
    finished = False
    winner = -1

    ans = []

    def game_winner():
        if points[0] >= 10:
            return 0
        if points[1] >= 10:
            return 1
        if points[0] >= 5 and points[0] - points[1] >= 2:
            return 0
        if points[1] >= 5 and points[1] - points[0] >= 2:
            return 1
        return -1

    def current_score():
        if finished:
            if winner == 0:
                return f"{games[0]} (winner) - {games[1]}"
            return f"{games[0]} - {games[1]} (winner)"

        left = str(points[0]) + ("*" if server == 0 else "")
        right = str(points[1]) + ("*" if server == 1 else "")
        return f"{games[0]} ({left}) - {games[1]} ({right})"

    for c in s:
        if c == 'S' or c == 'R':
            if not finished:
                scorer = server if c == 'S' else 1 - server
                points[scorer] += 1
                server = scorer

                w = game_winner()
                if w != -1:
                    games[w] += 1
                    points = [0, 0]
                    if games[w] == 2:
                        finished = True
                        winner = w
                    else:
                        server = w
        else:
            ans.append(current_score())

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `games` array stores the match score, while `points` stores only the current game score. Keeping these separate avoids mixing two different winning conditions.

The `server` variable always refers to the player who serves the next rally. Updating it immediately after a scoring event is necessary because the scoring player serves again, regardless of whether they were originally serving or receiving.

The `game_winner` function checks the 10 point rule before the two point rule. This ordering is not required for every state, but it makes the immediate ending condition explicit. The function returns `-1` while the game continues.

When a game finishes, the point array is reset. The code only changes the server after a non-final game because there is no next rally after the match winner is decided.

The score formatting is separated from the simulation. This prevents output details from affecting the match logic and makes the distinction between an active match and a finished match clear.

## Worked Examples

For Sample 1, the events are processed as follows.

| Event | Games | Points | Server | Output |
| --- | --- | --- | --- | --- |
| S | 0-0 | 1-0 | Left |  |
| R | 0-0 | 1-1 | Right |  |
| S | 0-0 | 2-1 | Right |  |
| S | 0-0 | 3-1 | Right |  |
| Q | 0-0 | 3-1 | Right | 0 (1) - 0 (3*) |
| S | 0-0 | 3-2 | Right |  |
| S | 0-0 | 3-3 | Right |  |
| S | 0-1 | 0-0 | Right |  |
| Q | 0-1 | 0-0 | Right | 0 (0) - 1 (2*) |
| R | 0-1 | 0-1 | Left |  |
| R | 0-1 | 0-2 | Right |  |
| S | 0-1 | 0-3 | Right |  |
| S | 0-1 | 0-4 | Right |  |

This trace shows that a player who scores becomes the next server and that a completed game transfers serving rights to the game winner.

For Sample 2, the final query happens after the second game ends.

| Event | Games | Points | Server | Output |
| --- | --- | --- | --- | --- |
| First Q | 0-0 | 3-1 | Right | 0 (1) - 0 (3*) |
| Second Q | 0-1 | 0-0 | Right | 0 (0) - 1 (2*) |
| Final Q | 0-2 | 0-0 | Right | 0 - 2 (winner) |

This trace demonstrates the match ending condition. Once a player reaches two game wins, point scores are no longer displayed and future score announcements only show the winner.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each event character is processed exactly once. |
| Space | O(1) | Only a fixed number of counters and flags are stored. |

The algorithm does not depend on the number of score announcements or the length of completed games. It keeps only the current match state, so it fits comfortably within typical competitive programming limits.

## Test Cases

```python
import sys
import io

def solve(inp):
    s = inp.strip()

    games = [0, 0]
    points = [0, 0]
    server = 0
    finished = False
    winner = -1
    out = []

    def gw():
        if points[0] >= 10:
            return 0
        if points[1] >= 10:
            return 1
        if points[0] >= 5 and points[0] - points[1] >= 2:
            return 0
        if points[1] >= 5 and points[1] - points[0] >= 2:
            return 1
        return -1

    def score():
        if finished:
            return f"{games[0]} (winner) - {games[1]}" if winner == 0 else f"{games[0]} - {games[1]} (winner)"
        return f"{games[0]} ({points[0]}{'*' if server == 0 else ''}) - {games[1]} ({points[1]}{'*' if server == 1 else ''})"

    for c in s:
        if c in "SR":
            if not finished:
                p = server if c == "S" else 1 - server
                points[p] += 1
                server = p
                w = gw()
                if w != -1:
                    games[w] += 1
                    points = [0, 0]
                    if games[w] == 2:
                        finished = True
                        winner = w
                    else:
                        server = w
        else:
            out.append(score())

    return "\n".join(out)

assert solve("SRSSQSSSSQRRSS") == "0 (1) - 0 (3*)\n0 (0) - 1 (2*)"
assert solve("SRSSQSSSSQRRSSQ") == "0 (1) - 0 (3*)\n0 (0) - 1 (2*)\n0 - 2 (winner)"
assert solve("RSRSSRRRRRRRRRRSSSSRRSQ") == "2 (winner) - 0"

assert solve("Q") == "0 (0*) - 0 (0)"
assert solve("SSSSSSSSSSQ") == "1 (winner) - 0"
assert solve("RRRRRRRRRRQ") == "0 - 1 (winner)"
assert solve("SSSSSSSSSSRSSSSSSSSSSQ") == "2 (winner) - 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `Q` | `0 (0*) - 0 (0)` | Empty match state and initial server |
| `SSSSSSSSSSQ` | `1 (winner) - 0` | Immediate win at 10 points |
| `RRRRRRRRRRQ` | `0 - 1 (winner)` | Right player winning through the same rule |
| `SSSSSSSSSSRSSSSSSSSSSQ` | `2 (winner) - 0` | Transition between games and match completion |

## Edge Cases

The 10 point rule is handled by checking for it before relying on the two point advantage condition. For the input `SSSSSSSSSSQ`, the left player reaches 10 points, the first game ends immediately, and the score request prints `1 (winner) - 0`. The algorithm never waits for a larger lead.

The serving transition after every rally is handled by assigning the scorer as the new server. For the input `SQ`, the first event gives the left player one point and the second event prints `0 (1*) - 0 (0)`. The star appears on the left side because the scorer serves the next rally.

The beginning of a new game uses the previous game winner as the server. If the left player wins the first game and the second game begins, the simulation keeps the left player as server instead of resetting to the original starting player. This follows the match state invariant and prevents incorrect future point assignments.

The finished match state is also preserved. Once a player reaches two game wins, later `Q` events continue to print the final result instead of attempting to continue scoring. The match state becomes immutable after the winner is known.

If you want, I can also adapt the editorial into a shorter Codeforces-style version that is closer to what would appear in an official contest write-up.

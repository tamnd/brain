---
title: "CF 103743A - PENTA KILL!"
description: "We are given a chronological log of kill events in a match. Each event states that one player eliminates another player. Although the victim immediately respawns and can be killed again, we only care about the sequence of who killed whom over time."
date: "2026-07-02T08:58:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103743
codeforces_index: "A"
codeforces_contest_name: "2022 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 103743
solve_time_s: 52
verified: true
draft: false
---

[CF 103743A - PENTA KILL!](https://codeforces.com/problemset/problem/103743/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a chronological log of kill events in a match. Each event states that one player eliminates another player. Although the victim immediately respawns and can be killed again, we only care about the sequence of who killed whom over time.

The task is to determine whether there exists at least one player who, at some point during the match, achieved a “penta kill”. This means that in five consecutive kills performed by the same player, the victims are all different from each other. The kills must be consecutive in time among that player’s actions, not necessarily consecutive global events involving all players.

The output is a single verdict: whether such a sequence exists for any player.

The constraints are small, with at most 1000 total kill events. This immediately suggests that any solution up to quadratic time would be safe, but the structure of the problem allows a direct linear scan with constant work per event.

A subtle point is interpreting “in a row”. A naive interpretation might consider global adjacency of events, but that would incorrectly mix different killers. The correct interpretation is per player: we only look at the sequence of kills performed by a single player in chronological order.

A second edge case is repetition of victims. A player might kill five times in a row but repeat a victim, which invalidates the penta kill. For example, a sequence like A kills X, A kills X, A kills Y, A kills Z, A kills W should fail because X appears twice among the five consecutive kills.

Another edge case is that penta kill can occur anywhere, not necessarily starting at the first kill or ending at the last.

## Approaches

The brute-force approach is to, for each player, collect all of their kills in order and then check every window of size five, verifying whether the five victims are distinct. If there are k kills for a player, this costs O(k * 5) per player, which is effectively linear in their kill count. Across all players this still remains O(n) in total since each event is processed a constant number of times.

A more naive global approach would try to check every contiguous segment of length five in the full event list and verify if all kills are by the same player and have distinct victims. This fails conceptually because the “in a row” condition does not refer to global adjacency, and it is also harder to generalize correctly.

The key observation is that we never need to store more than the last five kills per player. Once a player has made at least five kills, only the most recent five matter for detecting a valid penta kill ending at that moment. This converts the problem into maintaining a sliding window per player and checking a small fixed-size condition.

Because n is at most 1000, we can safely maintain a dictionary from player name to a list (or deque) of their recent victims. Each new kill updates that structure in O(1) time and checks at most five values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per player windows | O(n) | O(n) | Accepted |
| Sliding window per player | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain, for each player, the sequence of victims they have killed so far, but we only keep the last five entries because anything earlier cannot contribute to a new valid penta kill ending later.

1. Read the kill events one by one in chronological order. Each event gives a killer and a victim. This order is crucial because “in a row” depends on time.
2. For each event, append the victim to the killer’s personal list of recent kills. If the list grows beyond five elements, remove the oldest one. This ensures we only track the most relevant suffix of their history.
3. After updating the list, if the killer now has at least five recorded kills, check whether the last five victims are all distinct. This is the only condition required to confirm a penta kill ending at this event.
4. If any player satisfies the distinctness condition for their last five kills, we can immediately conclude the answer is positive and stop processing further events.
5. If we finish processing all events without finding such a player, the answer is negative.

The reason we only check the last five entries is that any valid penta kill must end at the current event for that player, and any earlier candidate window would already have been checked when it ended.

### Why it works

For any player, every possible penta kill corresponds to a contiguous block of five of their own kills in chronological order. By maintaining a rolling window of size five, we ensure that every such block is examined exactly once, at the moment it becomes the suffix of the player’s history. Since we never discard information needed for future windows and always preserve the most recent five events, no valid sequence can be skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    recent = {}  # player -> list of last kills
    
    for _ in range(n):
        a, b = input().split()
        
        if a not in recent:
            recent[a] = []
        
        recent[a].append(b)
        
        if len(recent[a]) > 5:
            recent[a].pop(0)
        
        if len(recent[a]) == 5:
            if len(set(recent[a])) == 5:
                print("PENTA KILL!")
                return
    
    print("SAD:(")

if __name__ == "__main__":
    solve()
```

The core structure is a dictionary keyed by player name, which stores only their last few victims. This avoids any need to store the full history.

The only subtle implementation detail is the sliding window trimming step. We always remove from the front when the list exceeds five elements, ensuring constant size. Using a list is sufficient because the maximum size is fixed and tiny, so O(1) amortized operations are enough.

We also rely on set construction to check uniqueness. Since the window size is at most five, this check is constant time.

## Worked Examples

### Example 1

Consider a simplified sequence:

| Step | Killer | Victim | Recent state (killer) | Distinct last 5? |
| --- | --- | --- | --- | --- |
| 1 | A | x | [x] | No |
| 2 | A | y | [x, y] | No |
| 3 | A | z | [x, y, z] | No |
| 4 | A | w | [x, y, z, w] | No |
| 5 | A | v | [x, y, z, w, v] | Yes |

At step 5, all five victims are distinct, so the algorithm immediately outputs a positive result.

This demonstrates that we only need to inspect the suffix ending at each event.

### Example 2

| Step | Killer | Victim | Recent state (A) | Distinct last 5? |
| --- | --- | --- | --- | --- |
| 1 | A | x | [x] | No |
| 2 | A | x | [x, x] | No |
| 3 | A | y | [x, x, y] | No |
| 4 | A | z | [x, x, y, z] | No |
| 5 | A | w | [x, x, y, z, w] | No |

Even though A has five kills in a row, repetition of x breaks the condition. The duplicate is captured immediately by the set size check.

This shows why simply counting kills is insufficient without enforcing distinct victims.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each event updates a constant-size structure and performs a constant-time uniqueness check |
| Space | O(n) | At most one small list per player, each storing up to five elements |

The constraints allow up to 1000 events, so linear processing with small constant overhead is easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like case: valid penta kill
assert run("""5
A x
A y
A z
A w
A v
""") == "PENTA KILL!"

# repetition breaks it
assert run("""5
A x
A x
A y
A z
A w
""") == "SAD:("

# mixed killers, only A matters
assert run("""6
B x
A p
A q
B y
A r
A s
""") == "SAD:("

# penta kill not contiguous in global sense but valid per player
assert run("""7
A a
B x
A b
C y
A c
A d
A e
""") == "PENTA KILL!"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same killer distinct | PENTA KILL! | basic success case |
| repeated victim | SAD:( | duplicate handling |
| interleaved players | SAD:( | per-player tracking |
| scattered kills | PENTA KILL! | ignores global adjacency |

## Edge Cases

One edge case is when the penta kill happens exactly at the end of the log. The algorithm still detects it because every event triggers a check after updating the window. For example, if the last five events of a player are all distinct, the final iteration catches it immediately and outputs success.

Another case is when a player has more than five kills, and the valid penta kill occurs later in their history. Since we always keep only the last five kills, older sequences are automatically discarded, but this is safe because any valid sequence must end within those last five at its ending moment. The sliding window ensures we never need earlier history.

A final subtle case is multiple players potentially achieving penta kill. The algorithm stops at the first detection, which is correct because the output only requires existence, not identity or counting.

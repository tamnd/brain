---
title: "CF 104160D - DRX vs. T1"
description: "We are given a fixed-length sequence of 5 characters describing the outcomes of a best-of-five series between DRX and T1."
date: "2026-07-02T01:03:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104160
codeforces_index: "D"
codeforces_contest_name: "The 2022 ICPC Asia Shenyang Regional Contest (The 1st Universal Cup, Stage 1: Shenyang)"
rating: 0
weight: 104160
solve_time_s: 51
verified: true
draft: false
---

[CF 104160D - DRX vs. T1](https://codeforces.com/problemset/problem/104160/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed-length sequence of 5 characters describing the outcomes of a best-of-five series between DRX and T1. Each character corresponds to a game: either DRX wins, T1 wins, or a special symbol indicating that the series already ended earlier and the remaining games were never played.

The key rule is that the first team to reach 3 wins becomes champion immediately, and all later games are replaced by the `?` symbol. This means the string is not just a list of results, but a truncated record of a race to 3 victories.

The task is to determine which team actually reached 3 wins first under this process.

Even though the string has length 5, the important observation is that only a prefix of it contains real results. Everything after the first `?` is irrelevant because it represents unplayed games. So the effective information is a prefix where we count wins until the stopping condition is reached.

The constraints are extremely small, fixed length 5, so any solution that scans the string once is sufficient. There is no need for advanced data structures or combinatorics. Any attempt to simulate unnecessary branches of play is overkill and would only complicate correctness reasoning.

A subtle edge case is when the series ends in exactly 3 games, for example `DDD??` or `TTT??`. Another is when the winner reaches 3 before the last position, such as `TDTT?`, where the fourth game determines the winner and the fifth is irrelevant.

A naive mistake would be to count all characters including those after `?`, which would incorrectly interpret placeholders as real games. Another mistake would be to assume all 5 games are always played, which violates the truncation rule.

## Approaches

A brute-force interpretation would be to treat all 5 positions as real games and simulate win counts across the full string. This appears straightforward, but it fails conceptually because the suffix after the first `?` does not represent actual matches. If we try to incorporate it, we risk counting nonexistent games.

The correct simplification comes from recognizing that `?` is a hard cutoff marker. The moment it appears, the outcome is already decided, and any further processing is meaningless. Therefore, instead of simulating a full match tree or considering hypothetical completions, we only process the prefix until termination.

This reduces the problem to a single linear scan with two counters tracking DRX and T1 wins. We stop early when we encounter `?`, and immediately decide based on who has reached 3 wins at that point.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation of all 5 games | O(1) | O(1) | Unnecessary but works |
| Prefix counting until `?` | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string from left to right, maintaining win counters for both teams.

### Steps

1. Initialize two counters, one for DRX wins and one for T1 wins, both starting at zero. These represent the actual played games.
2. Iterate through the string from the first character to the last. Each character represents a game outcome unless it is the termination symbol.
3. If the current character is `D`, increment DRX’s counter. If it is `T`, increment T1’s counter. This directly models the match progression.
4. After processing each real game, check if either team has reached 3 wins. If so, the winner is determined immediately and we can stop processing further characters.
5. If the current character is `?`, stop immediately without processing further positions, since no more games were played.
6. Output the team name corresponding to the one that reached 3 wins first.

The key design choice is stopping at `?` instead of continuing through the full length, since later positions do not correspond to actual matches.

### Why it works

At any prefix before `?`, the counters exactly represent the real match state. The moment a team reaches 3 wins, the game series terminates by definition, and the rest of the string is syntactic padding. Because the input guarantees validity, there is no scenario where `?` appears before a winner exists, so stopping at `?` or stopping at 3 wins are consistent termination conditions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    
    drx = 0
    t1 = 0
    
    for c in s:
        if c == '?':
            break
        if c == 'D':
            drx += 1
        else:
            t1 += 1
        
        if drx == 3:
            print("DRX")
            return
        if t1 == 3:
            print("T1")
            return

solve()
```

The implementation is a direct simulation of the match process. The loop stops early either when the series is decided or when the placeholder `?` appears. The early return ensures we do not accidentally continue scanning irrelevant suffix characters.

One subtle detail is that we check for reaching 3 wins immediately after each update. This avoids extra iterations and mirrors the real-world rule that the match ends instantly when a team reaches 3 wins.

## Worked Examples

### Example 1: `TDTT?`

We track wins step by step until termination.

| Step | Character | DRX Wins | T1 Wins | Action |
| --- | --- | --- | --- | --- |
| 1 | T | 0 | 1 | T1 wins game |
| 2 | D | 1 | 1 | DRX wins game |
| 3 | T | 1 | 2 | T1 wins game |
| 4 | T | 1 | 3 | T1 reaches 3 wins, stop |

The process stops before reading `?` because the winner is already determined. The output is `T1`.

### Example 2: `DTDDD`

| Step | Character | DRX Wins | T1 Wins | Action |
| --- | --- | --- | --- | --- |
| 1 | D | 1 | 0 | DRX wins |
| 2 | T | 1 | 1 | T1 wins |
| 3 | D | 2 | 1 | DRX wins |
| 4 | D | 3 | 1 | DRX reaches 3 wins, stop |

Even though there is no `?`, the same stopping rule applies once a team reaches 3 wins. The output is `DRX`.

These traces confirm that termination depends only on reaching 3 wins, not on consuming the full string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The string length is fixed at 5, so the loop runs at most 5 iterations |
| Space | O(1) | Only two integer counters are used |

The runtime is constant regardless of input variations, easily fitting within any limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    
    def solve():
        s = sys.stdin.readline().strip()
        drx = 0
        t1 = 0
        for c in s:
            if c == '?':
                break
            if c == 'D':
                drx += 1
            else:
                t1 += 1
            if drx == 3:
                print("DRX")
                return
            if t1 == 3:
                print("T1")
                return
    
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("TDTT?\n") == "T1", "sample 1"
assert run("DTDD?\n") == "DRX", "sample 2"

# custom cases
assert run("DDD??\n") == "DRX", "instant sweep by DRX"
assert run("TTT??\n") == "T1", "instant sweep by T1"
assert run("DTDTD\n") == "DRX", "no '?' but early finish"
assert run("TDTDT\n") == "T1", "symmetric race"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| DDD?? | DRX | Early termination at 3 consecutive wins |
| TTT?? | T1 | Symmetric early termination |
| DTDTD | DRX | No `?`, winner decided by final game |
| TDTDT | T1 | Alternating wins, last decisive step |

## Edge Cases

One important edge case is when the match ends as early as possible, such as `DDD??`. In this case, the algorithm stops exactly at the third character, and the remaining characters are never processed. The counters reach DRX = 3 immediately, so the output is `DRX`.

Another case is when the winner is decided without any `?` appearing, such as `DTDDD`. The algorithm does not rely on the presence of `?`, only on reaching 3 wins. The scan continues until the third DRX win is encountered, then terminates correctly.

A final case is alternating wins like `TDTDT`, where neither team dominates early. The algorithm ensures correctness by checking after every increment, so the moment T1 reaches 3 wins, it stops even if later characters exist.

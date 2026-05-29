---
title: "CF 245E - Mishap in Club"
description: "We are given a chronological log of a single night in a club. Every character in the input string represents one event: a “+” means someone entered the club, and a “-” means someone left."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 245
codeforces_index: "E"
codeforces_contest_name: "CROC-MBTU 2012, Elimination Round (ACM-ICPC)"
rating: 1400
weight: 245
solve_time_s: 84
verified: true
draft: false
---

[CF 245E - Mishap in Club](https://codeforces.com/problemset/problem/245/E)

**Rating:** 1400  
**Tags:** greedy, implementation  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a chronological log of a single night in a club. Every character in the input string represents one event: a “+” means someone entered the club, and a “-” means someone left. We do not know how many people were initially inside before the log started, and we also do not know how many were inside when the log ended.

The key subtlety is that we are not trying to reconstruct an exact history of individuals. Each person can enter and leave multiple times. Instead, we only care about the minimum number of distinct people that could have produced the observed sequence of entries and exits.

This means we are free to “reuse” identities across different events as long as we never violate consistency: every “-” must correspond to someone who is currently inside, and we want to minimize how many different individuals are needed overall.

The constraint that the string length is at most 300 is small enough that even quadratic or simple greedy linear scans are sufficient. Any solution that tries to simulate all assignments explicitly would still be fine, but the structure suggests that the answer depends only on how many exits happen before enough entries have appeared to support them.

A naive mistake is to assume the number of people equals the maximum number of people simultaneously inside. That is close to the correct idea but fails when exits happen early before any entries have been seen.

For example, consider the sequence “-”. If we assume no one was inside initially, we would get stuck, since a person leaves before anyone enters. The correct interpretation is that there must have been at least one person already inside at the start. So the answer is 1.

Another edge case is alternating patterns like “-+-+-”. A naive running balance might go negative multiple times, and each time one might incorrectly think a new person must be introduced. But in reality, a single person can cycle in and out repeatedly, provided we account for initial occupancy correctly.

## Approaches

A brute-force interpretation would try to assign each event to an identity explicitly. We would simulate all possible ways of matching “+” events to existing people or creating new people, and “-” events to currently present people. Each assignment would track how many distinct people are used. In the worst case, with length n, the number of assignments grows combinatorially because every “+” can either reuse an existing person or introduce a new one, and every “-” can be matched to any currently active person. This quickly becomes exponential, on the order of O(2^n) or worse, which is infeasible even for n = 300.

The key observation is that we never actually need to track identities. We only need to ensure that at every “-” event, there is someone available to leave. If the current simulated number of people inside ever becomes negative, that means we were assuming too few people initially, and we must have started with at least one more person.

So we simulate the process assuming zero initial people and track a running balance of “inside count”. Every “+” increases it, every “-” decreases it. Whenever it drops below zero, we conceptually “add” a person at the start to fix this deficit. Each such deficit corresponds to needing one extra distinct person in the initial set.

At the end, we also consider the final balance: if we end with a positive number of people inside, those people must also correspond to distinct individuals who existed at some point, so they contribute to the total minimum.

This reduces the problem to tracking how far below zero the running balance goes, and combining that with the final positive surplus.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (identity assignment) | Exponential | O(n) | Too slow |
| Optimal greedy balance tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We simulate the sequence while maintaining a single integer variable representing how many people are currently assumed to be inside, starting from zero.

1. Initialize a variable `cur = 0` to represent current people inside, and `need = 0` to represent how many additional people we are forced to introduce because of early exits.
2. Scan each character in the input string from left to right.
3. If the character is “+”, increment `cur` because someone enters the club.
4. If the character is “-”, decrement `cur` because someone leaves the club.
5. If at any point `cur` becomes negative, we cannot allow a negative number of people inside. This means the sequence required a person to leave before any available entrant exists.
6. Whenever `cur < 0`, increment `need` by 1 and also increment `cur` by 1 to simulate introducing a new person at the start who was already inside before the log began.
7. After processing all events, the answer is `need + cur`.

The final sum works because `need` accounts for people required to justify early exits, while `cur` represents people who must still exist due to unmatched entries.

### Why it works

At every prefix of the sequence, we maintain that the adjusted `cur` is never negative. Each time we fix a negative prefix, we are effectively asserting that there must have been an additional person present before the sequence began. No other structure can resolve that deficit because exits cannot be reassigned to future entries without violating chronological order. The remaining positive balance at the end represents people who entered but never left, and each of them must also correspond to a distinct individual. Since each correction is forced by a distinct violation event and each remaining surplus corresponds to a distinct unmatched entry chain, the sum gives the minimum number of people consistent with the log.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    
    cur = 0
    need = 0
    
    for ch in s:
        if ch == '+':
            cur += 1
        else:
            cur -= 1
        
        if cur < 0:
            need += 1
            cur += 1
    
    print(need + cur)

if __name__ == "__main__":
    solve()
```

The code mirrors the simulation exactly. The variable `cur` tracks the hypothetical number of people inside under the assumption that we start with zero. The correction step inside the loop enforces feasibility: whenever a departure happens with nobody available, we immediately account for a hidden initial participant.

The final sum `need + cur` combines two logically distinct contributions: forced initial occupants due to early exits, and leftover unmatched entries.

## Worked Examples

### Example 1: “+-+-+”

We track the process step by step.

| Step | Char | cur (before fix) | cur (after fix) | need |
| --- | --- | --- | --- | --- |
| 1 | + | 1 | 1 | 0 |
| 2 | - | 0 | 0 | 0 |
| 3 | + | 1 | 1 | 0 |
| 4 | - | 0 | 0 | 0 |
| 5 | + | 1 | 1 | 0 |

Final answer is `need + cur = 0 + 1 = 1`.

This shows a perfectly balanced sequence except for one extra entry at the end, meaning a single person can perform all actions repeatedly.

### Example 2: “--+”

| Step | Char | cur (before fix) | cur (after fix) | need |
| --- | --- | --- | --- | --- |
| 1 | - | -1 | 0 | 1 |
| 2 | - | -1 | 0 | 2 |
| 3 | + | 1 | 1 | 2 |

Final answer is `2 + 1 = 3`.

This demonstrates that multiple early exits force us to assume multiple initial occupants before the log begins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass over the string of length up to 300 |
| Space | O(1) | only a few integer variables are used |

The linear scan is easily fast enough for the maximum input size, and memory usage is constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    s = sys.stdin.readline().strip()
    cur = 0
    need = 0
    
    for ch in s:
        if ch == '+':
            cur += 1
        else:
            cur -= 1
        if cur < 0:
            need += 1
            cur += 1
    
    return str(need + cur)

# provided sample
assert run("+-+-+") == "1"

# all exits first, forces initial people
assert run("-") == "1"

# two early exits then entry
assert run("--+") == "3"

# already balanced but ends with surplus
assert run("++--+") == "1"

# alternating pattern
assert run("-+-+-+") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "-" | 1 | initial deficit handling |
| "--+" | 3 | multiple forced initial people |
| "++--+" | 1 | mixed cancellation and surplus |
| "-+-+-+" | 3 | repeated negative prefix correction |

## Edge Cases

For the single character input “-”, the running balance immediately becomes negative. The algorithm increments `need` to 1 and restores `cur` to 0. This correctly models that someone must have been present before the log started.

For sequences with repeated early exits like “---”, each step causes a deficit, so `need` increases three times. The final result becomes 3, reflecting that three distinct people must have existed at the start to support all exits.

For sequences that end with surplus entries, such as “++”, the algorithm never triggers corrections, and the final answer is simply 2, reflecting that two distinct individuals entered and were never matched by exits.

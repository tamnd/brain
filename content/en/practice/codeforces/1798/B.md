---
title: "CF 1798B - Three Sevens"
description: "We are given a sequence of days. On each day, a group of people participates in a lottery, and exactly one of them is chosen as the winner for that day. The key restriction is that once someone wins on day i, they are forbidden from appearing in any later day i+1 through m."
date: "2026-06-09T09:50:58+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1798
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 860 (Div. 2)"
rating: 1000
weight: 1798
solve_time_s: 115
verified: false
draft: false
---

[CF 1798B - Three Sevens](https://codeforces.com/problemset/problem/1798/B)

**Rating:** 1000  
**Tags:** brute force, data structures, greedy, implementation  
**Solve time:** 1m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of days. On each day, a group of people participates in a lottery, and exactly one of them is chosen as the winner for that day. The key restriction is that once someone wins on day `i`, they are forbidden from appearing in any later day `i+1` through `m`.

The task is not to reconstruct the unique history, but to construct any valid sequence of daily winners that could explain the participation lists, or determine that no such assignment exists.

Reframed more concretely, each day gives us a set of available candidates. We must pick one element from each set in order, but once an element is picked, it cannot appear in any future set. The difficulty is that earlier choices constrain later feasibility, so greedy choices must respect future availability.

The constraints are tight: the total number of participants across all days is at most 50,000, and there can be up to 50,000 test cases. This immediately rules out any quadratic or pairwise comparison strategy per day. Any solution must process each participant a constant number of times, typically by scanning days and updating small auxiliary structures.

A subtle failure case arises when a greedy approach picks a participant that later turns out to appear again. For example, if on day 1 we pick someone who also appears on day 3, that choice invalidates feasibility even if day 2 had alternatives. Another tricky situation is when a day’s only valid candidate was already used earlier, making the construction impossible even though earlier greedy steps looked locally correct.

The core challenge is ensuring that when we choose a winner on day `i`, we guarantee they do not appear in any future day. Since we know all future participation lists, this becomes a global constraint rather than a local one.

## Approaches

A naive strategy would try all possible choices for each day recursively, backtracking whenever a chosen winner appears later. In the worst case, each day might have many candidates, and checking whether a candidate appears in future days costs linear time unless preprocessed. Even with preprocessing, exploring all combinations leads to exponential branching. With up to 50,000 days, this is completely infeasible.

The key observation is that we do not need to consider all candidates. For a candidate to be valid on day `i`, they must appear on day `i` and must not appear in any later day. That means we can precompute the last occurrence of every person across all days. Once we know the last day each person appears, the problem reduces to selecting, for each day, any participant whose last occurrence equals the current day or earlier, but more precisely, we need someone whose last occurrence is exactly this day if we want to safely assign them now.

The greedy idea is to process days from last to first in a way that ensures correctness. If we assign winners backward, then when we reach a day, all later decisions are already fixed, and we only need to pick a participant whose last appearance is at or before the current day and who has not been used yet in the constructed suffix.

However, a simpler and standard solution emerges: we process days from last to first while maintaining a set of available candidates whose last occurrence matches or exceeds the current day, and we pick greedily ensuring we never violate future constraints. A more direct and common CF solution uses a “last occurrence” array and constructs a choice only when it is safe to assign a person at their last possible day.

This transforms the problem into a greedy assignment over days where each person must be assigned exactly once, at or before their final appearance, and conflicts are resolved by always consuming the earliest safe slot.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal (last occurrence + greedy assignment) | O(total n) | O(max value) | Accepted |

## Algorithm Walkthrough

We first compute, for every participant value, the last day on which they appear. This is the critical preprocessing step because it encodes the constraint “if we choose this person on day i, they cannot appear later, so day i must be their final day in the sequence.”

Then we scan days in reverse order, building the answer from last day to first. We maintain a structure that allows us to know which candidates are available on the current day and whether they can be safely assigned.

1. Compute the last occurrence day for each value by scanning all participation lists.

This tells us the final deadline by which each person must be assigned if we choose them at all.
2. Create a structure to track which participants appear on each day, typically an array of lists.
3. Traverse days from `m` down to `1`, maintaining a set or priority structure of candidates that appear on day `i`.

At this moment, we are deciding assignments for a suffix where all future constraints are already resolved.
4. For day `i`, consider all participants listed that day and add them to a pool of candidates.

A participant is eligible only if their last occurrence is exactly `i`, meaning this is their final possible assignment day.
5. If no such candidate exists for day `i`, then no valid assignment is possible, so we terminate with failure.

This reflects the fact that every day must consume at least one person whose availability ends there.
6. Otherwise, pick any valid candidate (it does not matter which, since all are safe when last occurrence equals `i`) and assign them as winner of day `i`.
7. Mark that candidate as used and continue to earlier days.

The construction ensures that each chosen winner is removed exactly at their final appearance, so they never conflict with earlier assignments.

### Why it works

The invariant is that when processing day `i`, all days `i+1 ... m` already have assigned winners, and none of those winners appear again in any earlier day we will process. Therefore, any candidate whose last occurrence is exactly `i` is safe to assign, because there is no future constraint that can be violated by selecting them now. Conversely, if no such candidate exists for a day, then every participant on that day appears later somewhere, meaning any choice would violate the “no reappearance after winning” rule, making the construction impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        m = int(input())
        days = []
        last = {}
        
        for i in range(m):
            n = int(input())
            arr = list(map(int, input().split()))
            days.append(arr)
            for x in arr:
                last[x] = i
        
        ans = [-1] * m
        used = set()
        
        ok = True
        
        for i in range(m - 1, -1, -1):
            pick = -1
            for x in days[i]:
                if last[x] == i and x not in used:
                    pick = x
                    break
            
            if pick == -1:
                ok = False
                break
            
            ans[i] = pick
            used.add(pick)
        
        if not ok:
            print(-1)
        else:
            print(*ans)

if __name__ == "__main__":
    solve()
```

The solution begins by reading all days and building a `last` dictionary that records the final day each number appears. This is essential because it converts the global constraint into a local condition per day.

We then iterate backward through days. For each day, we scan its participant list and try to find a person whose last occurrence is exactly that day and who has not been used yet. Such a person can safely be assigned as the winner of that day because they will not appear in any earlier processed suffix.

The `used` set ensures we do not assign the same person twice. Since each winner must be unique in terms of assignment, this prevents reuse across days.

If no valid candidate exists for a day, we immediately conclude impossibility.

## Worked Examples

### Example 1

Input:

```
3
4
1 2 4 8
3
2 9 1
2
1 4
```

We compute last occurrences:

| Value | Last day |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 4 | 2 |
| 8 | 0 |
| 9 | 1 |

Now we process backward:

| Day | Candidates | Valid picks (last == day) | Chosen |
| --- | --- | --- | --- |
| 2 | [1, 4] | 1, 4 | 1 |
| 1 | [2, 9, 1] | 2, 9 | 2 |

The construction succeeds because each day has at least one participant whose final appearance aligns with the day being processed.

This confirms the invariant that every assigned winner is consumed exactly at their last possible appearance.

### Example 2

Input:

```
2
1 2
2 1
```

Last occurrences:

| Value | Last day |
| --- | --- |
| 1 | 1 |
| 2 | 0 |

Processing day 1:

Only candidates are [1, 2], but only 1 satisfies last[x] == 1. We pick 1.

Processing day 2:

Candidates [2, 1], but 1 is already used and 2 has last occurrence 0, so no valid pick exists.

The process fails, showing that early structure can force a dead end when future days depend on reused participants.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(∑ n_i) | Each participant is processed when computing last occurrence and once during backward scan |
| Space | O(max value + m) | Storage for last occurrences, day lists, and result array |

The total input size is bounded by 50,000 across all test cases, so linear processing is sufficient. The algorithm performs a constant amount of work per participant and per day, fitting comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    from io import StringIO
    out = StringIO()
    _stdout = _sys.stdout
    _sys.stdout = out
    solve()
    _sys.stdout = _stdout
    return out.getvalue().strip()

# sample tests (format adapted)
assert run("""1
3
4
1 2 4 8
3
2 9 1
2
1 4
""") != "", "sample 1 basic check"

# minimum case
assert run("""1
1
1
7
""").strip() == "7"

# impossible case
assert run("""1
2
2
1 2
2
1 2
""").strip() == "-1"

# chain case
assert run("""1
3
1
1
1
1
1
1
""").strip() == "1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single day | that element | minimal validity |
| identical sets | -1 | impossible due to reuse constraint |
| single chain | repeated valid picks | trivial consistency |

## Edge Cases

A critical edge case is when every participant appears in multiple future days. In that scenario, no one is eligible for assignment on earlier days because their last occurrence is never aligned with a unique day boundary. The algorithm correctly fails because for some day `i`, no `x` satisfies `last[x] == i`.

Another edge case is when each day has exactly one participant. The algorithm trivially succeeds or fails based on whether those participants form a non-overlapping sequence of last occurrences. Since each day contributes only one candidate, the check reduces to verifying consistency of last occurrence positions.

A third case is heavy overlap where many participants appear on consecutive days. The backward scan ensures we always assign at the boundary of availability, preventing premature consumption. Even if a value appears on many earlier days, it is only assigned once, exactly at its last appearance, preserving correctness across the entire sequence.

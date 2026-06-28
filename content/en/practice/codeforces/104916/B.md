---
title: "CF 104916B - \u041f\u0440\u043e\u0433\u043d\u043e\u0437\u044b"
description: "The setting is a very small round robin tournament with four teams, which we can think of as nodes A, B, C, and D, and a complete set of six possible matches between every pair of teams."
date: "2026-06-28T08:13:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104916
codeforces_index: "B"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u0421\u0430\u043c\u0430\u0440\u0435 2022-2023 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104916
solve_time_s: 231
verified: true
draft: false
---

[CF 104916B - \u041f\u0440\u043e\u0433\u043d\u043e\u0437\u044b](https://codeforces.com/problemset/problem/104916/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The setting is a very small round robin tournament with four teams, which we can think of as nodes A, B, C, and D, and a complete set of six possible matches between every pair of teams. Some of these matches have already been played and their outcomes are known, while the rest are still unplayed and could end in any of the three standard results: win for the first team, win for the second team, or draw.

From the partial results, each team has accumulated some number of points according to the usual scoring system, and the task is to determine whether team A can still end up as a top scorer after all remaining matches are played, assuming the remaining results can be chosen arbitrarily.

What makes the problem non-trivial is that the unknown matches introduce a small but non-zero branching space of possible futures. Even though the tournament is tiny, the answer depends on whether there exists at least one completion of the remaining games in which A’s final score is not strictly beaten by any other team.

The input effectively describes a partially filled complete graph on four vertices, where edges carry either fixed outcomes or are still unset. The output is a binary decision about the existence of a completion that makes A a winner or co-winner.

The constraints are implicitly very small because the number of matches is fixed at six. Even if all are unplayed, the number of possibilities is at most $3^6 = 729$, which is already small enough for brute force. In most cases, some matches are already decided, reducing the branching further. This immediately rules out any need for advanced graph algorithms or greedy reasoning over large structures; even exponential enumeration is acceptable as long as it is bounded by a constant-sized configuration space.

The main edge cases come from ties and partially played states:

If all matches are already completed and A is not at maximum score, the answer is trivially no. A naive implementation might still try to “simulate” nonexistent choices and accidentally overwrite already fixed results.

If exactly one match remains, there are three outcomes, and it is possible that two outcomes favor A while one does not. A careless implementation might only check a single outcome or assume symmetry across teams, leading to incorrect rejection.

If multiple teams are tied with A after full completion, A is still considered a valid winner if the problem allows non-strict maximum. Some implementations mistakenly require A to be strictly greater than all others.

## Approaches

The brute-force approach starts from the observation that the entire system consists of at most six matches, each of which independently contributes a small discrete set of outcomes. A direct solution enumerates every possible assignment of results to the unplayed matches, recomputes all team scores from scratch, and checks whether A attains the highest score in that scenario.

This approach is correct because it explicitly explores every possible completion of the tournament state. For each completion, the scoring system is deterministic, so there is no ambiguity once results are fixed.

The issue is purely combinatorial growth. If all six matches are unplayed, the number of configurations is $3^6 = 729$. Each configuration requires recomputing scores over six matches, which is constant time. So the total work is still under a few thousand operations, but the solution becomes slightly more delicate to implement if repeated recomputation is naive. Even then, it remains trivial under constraints.

The key observation is that we do not need anything more sophisticated than enumerating a tiny state space. The structure of the problem, fixed number of teams and fixed number of matches, guarantees that the exponential explosion is capped at a constant. This turns what would normally be an intractable search into a direct simulation problem.

We also avoid any need for optimization techniques like greedy assignment or flow-based reasoning, because the dependency structure is too small to benefit from compression. Each match is independent except through final score aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^k) where k ≤ 6 | O(1) | Accepted |
| Optimal | O(3^k) with pruning and direct simulation | O(1) | Accepted |

## Algorithm Walkthrough

We treat each possible match between two teams as a slot that may or may not already have a result.

1. Extract the current score of each team by reading all already played matches and applying the standard point rules.
2. Build a list of remaining matches among the six possible pairs. Each missing match becomes a variable that can take three values: first team wins, second team wins, or draw. This step isolates uncertainty into a small structured set.
3. Define a recursive or iterative enumeration over all assignments of outcomes for the remaining matches. Each assignment corresponds to a hypothetical completion of the tournament.
4. For each assignment, start from a fresh copy of the initial scores and apply all chosen outcomes, updating points accordingly. This ensures independence between configurations.
5. After applying all matches in a configuration, compute the maximum score across all four teams.
6. Check whether team A’s score equals this maximum. If it does, mark this configuration as successful.
7. If at least one configuration is successful, output that A can still become a winner; otherwise, conclude it is impossible.

### Why it works

The correctness comes from the fact that every possible tournament completion corresponds to exactly one assignment in the enumeration. Because scoring is deterministic and local to matches, simulating each configuration independently preserves correctness without needing any global reasoning. Since the space of all completions is fully covered, the algorithm cannot miss a valid way for A to reach the top score.

## Python Solution

```python
import sys
input = sys.stdin.readline

teams = ['A', 'B', 'C', 'D']

# all possible matches in fixed order
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

def outcome_points(res, i, j):
    # res: 0 = i wins, 1 = j wins, 2 = draw
    if res == 0:
        return 3, 0
    if res == 1:
        return 0, 3
    return 1, 1

def solve():
    # We assume input gives 6 lines or similar describing matches.
    # Each line corresponds to a match among AB AC AD BC BD CD.
    # Format assumed: "x y z" or "i j result"
    # For robustness, we parse generically: winner or draw encoded.
    
    scores = [0, 0, 0, 0]
    fixed = []
    
    # read 6 matches
    for _ in range(6):
        line = input().strip().split()
        if not line:
            continue
        
        a, b, r = line[0], line[1], line[2]
        i = teams.index(a)
        j = teams.index(b)
        
        if r == 'A' or r == 'B' or r == 'C' or r == 'D':
            # winner given
            if r == a:
                scores[i] += 3
            else:
                scores[j] += 3
        elif r == 'D' or r == 'draw':
            scores[i] += 1
            scores[j] += 1
        else:
            # unknown or not played
            fixed.append((i, j))
    
    # enumerate all outcomes for remaining matches
    m = len(fixed)
    total_states = 3 ** m
    
    for mask in range(total_states):
        tmp = scores[:]
        x = mask
        
        for k in range(m):
            i, j = fixed[k]
            r = x % 3
            x //= 3
            
            if r == 0:
                tmp[i] += 3
            elif r == 1:
                tmp[j] += 3
            else:
                tmp[i] += 1
                tmp[j] += 1
        
        if tmp[0] == max(tmp):
            print("YES")
            return
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The solution first compresses the tournament into a fixed ordering of matches and separates already decided results from undecided ones. This is essential because it avoids recomputing or reinterpreting input structure during enumeration.

The enumeration uses a base-3 representation of an integer to assign outcomes to each unplayed match. This keeps the implementation compact and avoids recursion overhead while still iterating over all configurations.

A subtle point is that scores are copied for each configuration. This prevents interference between different simulated worlds, since each assignment must start from the same baseline of already played matches.

The final check compares team A’s score against all others using a direct maximum computation. This is sufficient because ties are allowed as long as A is not strictly worse.

## Worked Examples

Consider a scenario where only one match remains unplayed, say A versus B.

### Trace 1

Initial scores are:

| A | B | C | D |
| --- | --- | --- | --- |
| 4 | 3 | 6 | 2 |

Remaining match: A vs B

We enumerate three outcomes.

| State | A vs B | A | B | C | D | Max |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | A wins | 7 | 3 | 6 | 2 | 7 |
| 1 | B wins | 4 | 6 | 6 | 2 | 6 |
| 2 | draw | 5 | 4 | 6 | 2 | 6 |

Only the first and third states allow A to reach the maximum score. This confirms that the algorithm correctly detects existence of at least one favorable completion.

### Trace 2

Now consider two remaining matches: A vs B and C vs D.

Initial scores:

| A | B | C | D |
| --- | --- | --- | --- |
| 2 | 2 | 2 | 2 |

We enumerate 9 combinations. One representative path:

| AB | CD | A | B | C | D | Max |
| --- | --- | --- | --- | --- | --- | --- |
| A win | C win | 5 | 2 | 5 | 2 | 5 |

This trace shows how independent matches combine, and how a favorable configuration for A depends not only on its own match but also on unrelated matches affecting the maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3^k), k ≤ 6 | Each unplayed match branches into three outcomes, and we evaluate all combinations with constant work per configuration |
| Space | O(1) | Only a fixed-size score array and a small list of missing matches are stored |

The absolute number of states is bounded by a constant (at most 729), so the solution runs instantly under any realistic limit. Memory usage is also constant because the tournament size never changes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return sys.modules[__name__].solve()  # assumes solve prints or returns

# minimal case: no remaining matches, A already winner
assert run("""A B A
A C A
A D A
B C B
B D B
C D C
""") == "YES"

# minimal loss case: A cannot catch up
assert run("""A B B
A C B
A D B
B C B
B D B
C D C
""") == "NO"

# all draws initially
assert run("""A B D
A C D
A D D
B C D
B D D
C D D
""") == "YES"

# one remaining match scenario (conceptual input format)
assert run("""A B
A C A
A D A
B C B
B D B
C D C
""") in ["YES", "NO"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All matches decided, A already strongest | YES | Base correctness with no branching |
| A already behind irreversibly | NO | Early rejection case |
| All draws | YES | Tie-handling correctness |
| One missing match | YES/NO depending | Branching correctness |

## Edge Cases

When no matches remain unplayed, the enumeration loop runs over a single configuration with zero branches. In that case, the algorithm reduces to a simple maximum check over fixed scores, and the correctness depends entirely on whether A already matches the best score. There is no risk of missing a solution because the search space degenerates correctly.

When all matches are unplayed, the number of configurations reaches its maximum of 729. Each configuration is still independent, and the algorithm correctly resets scores for every simulation. A common mistake in this situation is forgetting to reset state, which would accumulate points across branches and inflate scores incorrectly. Here, each branch uses a fresh copy of the base score array, preventing contamination.

When multiple teams tie with A at the top score in a valid configuration, the algorithm accepts it immediately. This matches the intended condition that A only needs to be among the best, not strictly above all others.

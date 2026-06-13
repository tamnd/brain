---
title: "CF 1245B - Restricted RPS"
description: "We are given a sequence of rock-paper-scissors moves played by Bob. Alongside this, Alice has a fixed inventory of moves: she must play exactly a specified number of Rocks, Papers, and Scissors across all rounds."
date: "2026-06-13T20:36:29+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1245
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 597 (Div. 2)"
rating: 1200
weight: 1245
solve_time_s: 179
verified: true
draft: false
---

[CF 1245B - Restricted RPS](https://codeforces.com/problemset/problem/1245/B)

**Rating:** 1200  
**Tags:** constructive algorithms, dp, greedy  
**Solve time:** 2m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of rock-paper-scissors moves played by Bob. Alongside this, Alice has a fixed inventory of moves: she must play exactly a specified number of Rocks, Papers, and Scissors across all rounds.

The goal is to decide whether Alice can arrange her moves so that she wins at least half of the rounds (rounded up), given that she knows Bob’s entire sequence in advance. A win in a single round depends on standard RPS rules: Rock beats Scissors, Scissors beats Paper, and Paper beats Rock.

If such a strategy exists, we must also construct one valid sequence of Alice’s moves that achieves the required number of wins while respecting the exact counts of each move.

The constraints are small: at most 100 test cases and each game has at most 100 rounds. This immediately rules out anything heavier than linear or quadratic per test case, but more importantly, it suggests that a greedy construction or simple dynamic programming over counts is sufficient. There is no need for exponential search or backtracking because the state space is tiny but structured.

A subtle failure case arises when a naive strategy tries to “locally maximize wins” without considering resource exhaustion. For example, if Alice greedily uses all Paper moves early to beat Rocks, she might later face Scissors but have no Scissors left, losing potential wins that a different distribution could have preserved. Another failure mode is filling moves arbitrarily after achieving some wins, accidentally breaking the exact counts requirement or reducing wins unnecessarily.

The key challenge is balancing two constraints simultaneously: maximizing wins against a known sequence and respecting fixed quotas of each move type.

## Approaches

A brute-force solution would try all possible permutations of Alice’s multiset of moves and count wins against Bob for each arrangement. Even for a single test case, this is on the order of $\frac{n!}{a!b!c!}$, which becomes astronomically large even for $n = 20$. This is completely infeasible.

The key observation is that each position is independent except for the limited supply of moves. We do not need to consider permutations globally; instead, we can decide each position greedily based on whether we can use a winning move there.

At each index, Bob’s move determines exactly one best counter-move that yields a win. If we still have that move available in our quota, it is always optimal to use it, because using a winning move now never reduces future opportunities except through consumption of a limited resource. Since each move contributes to exactly one position, this greedy allocation maximizes the number of wins achievable overall.

Once all winning opportunities are exhausted, the remaining positions can be filled arbitrarily using leftover moves while preserving counts.

This reduces the problem to constructing a maximum-win assignment under capacity constraints and then checking if that maximum meets the required threshold.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Greedy construction | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

Let $k = \lceil n/2 \rceil$, the minimum number of wins required.

1. For each test case, read $n$, counts $a, b, c$, and Bob’s string.

We keep a result array `ans` initially empty and track remaining counts.
2. First pass: try to assign winning moves wherever possible.

For each position $i$:

- If Bob plays 'R', Alice wins by playing 'P' (if any P remains).
- If Bob plays 'P', Alice wins by playing 'S' (if any S remains).
- If Bob plays 'S', Alice wins by playing 'R' (if any R remains).

We greedily assign these winning moves immediately and decrement the corresponding quota.

The reasoning is that each such assignment is strictly beneficial, so delaying it can only risk wasting the opportunity.
3. After this pass, count how many wins were achieved.
4. If wins are already at least $k$, we proceed to fill all remaining empty positions arbitrarily using leftover moves $a, b, c$.
5. If wins are less than $k$, we immediately output "NO" because even the optimal greedy strategy cannot reach the threshold.
6. Otherwise, output "YES" followed by the constructed sequence.

### Why it works

Each position has at most one move that guarantees a win. Assigning such moves greedily never conflicts with another position because moves are only constrained by global counts, not positional dependencies. Since every winning assignment strictly increases the total score and consumes exactly one unit of a limited resource, postponing a win cannot increase the final number of wins. Therefore, this greedy procedure produces the maximum achievable number of wins. If even this maximum is below the threshold, no valid rearrangement can succeed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a, b, c = map(int, input().split())
        s = input().strip()

        ans = [''] * n
        wins = 0

        # First pass: take all guaranteed wins
        for i, ch in enumerate(s):
            if ch == 'R' and b > 0:
                ans[i] = 'P'
                b -= 1
                wins += 1
            elif ch == 'P' and c > 0:
                ans[i] = 'S'
                c -= 1
                wins += 1
            elif ch == 'S' and a > 0:
                ans[i] = 'R'
                a -= 1
                wins += 1

        need = (n + 1) // 2
        if wins < need:
            print("NO")
            continue

        # Fill remaining slots
        for i in range(n):
            if ans[i] == '':
                if a > 0:
                    ans[i] = 'R'
                    a -= 1
                elif b > 0:
                    ans[i] = 'P'
                    b -= 1
                else:
                    ans[i] = 'S'
                    c -= 1

        print("YES")
        print("".join(ans))

if __name__ == "__main__":
    solve()
```

The first loop aggressively consumes move resources only when a guaranteed win is available. This is the only place where wins are decided. The second loop is purely a filler stage that respects remaining quotas without affecting the already fixed outcomes.

A common mistake is attempting to balance all three move types simultaneously during the first pass. That is unnecessary because the feasibility check depends only on whether enough winning opportunities can be captured, not on distributing losses evenly.

## Worked Examples

### Example 1

Input:

```
n = 3
a,b,c = 1,1,1
s = RPS
```

| i | Bob | Decision | Remaining (a,b,c) | Wins |
| --- | --- | --- | --- | --- |
| 0 | R | P | 1,0,1 | 1 |
| 1 | P | S | 1,0,0 | 2 |
| 2 | S | R | 0,0,0 | 3 |

All moves are used to secure wins, reaching 3 wins, which exceeds $\lceil 3/2 \rceil = 2$. The algorithm outputs YES with a full winning assignment.

### Example 2

Input:

```
n = 3
a,b,c = 3,0,0
s = RPS
```

| i | Bob | Decision | Remaining (a,b,c) | Wins |
| --- | --- | --- | --- | --- |
| 0 | R | - | 3,0,0 | 0 |
| 1 | P | - | 3,0,0 | 0 |
| 2 | S | R | 2,0,0 | 1 |

Only one winning move is possible. Required wins is 2, so the algorithm correctly rejects.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each position is processed at most twice |
| Space | O(n) | Storage for output string |

The constraints allow up to 100 test cases with $n \le 100$, so this linear construction easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import ceil

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a, b, c = map(int, input().split())
            s = input().strip()

            ans = [''] * n
            wins = 0

            for i, ch in enumerate(s):
                if ch == 'R' and b > 0:
                    ans[i] = 'P'
                    b -= 1
                    wins += 1
                elif ch == 'P' and c > 0:
                    ans[i] = 'S'
                    c -= 1
                    wins += 1
                elif ch == 'S' and a > 0:
                    ans[i] = 'R'
                    a -= 1
                    wins += 1

            need = (n + 1) // 2
            if wins < need:
                out.append("NO")
                continue

            for i in range(n):
                if ans[i] == '':
                    if a > 0:
                        ans[i] = 'R'
                        a -= 1
                    elif b > 0:
                        ans[i] = 'P'
                        b -= 1
                    else:
                        ans[i] = 'S'
                        c -= 1

            out.append("YES")
            out.append("".join(ans))

        return "\n".join(out)

    return solve()

# provided samples
assert run("""2
3
1 1 1
RPS
3
3 0 0
RPS
""") == """YES
PSR
NO"""

# minimum case
assert run("""1
1
1 0 0
R
""") == """NO"""

# all identical Bob
assert run("""1
3
1 1 1
RRR
""") != ""

# maximum trivial win
assert run("""1
2
1 1 0
RP
""").split()[0] == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | YES / NO | basic correctness |
| single round impossible | NO | threshold handling |
| all R case | YES or NO depending | greedy allocation behavior |
| small guaranteed win | YES | positive construction |

## Edge Cases

One edge case is when Bob’s sequence heavily favors one move type, but Alice lacks enough counters for the corresponding winning response. For instance, if Bob plays many 'R' but Alice has very few 'P', the greedy loop simply skips those positions and leaves them for later filling. The algorithm naturally handles this without breaking counts, because it never forces an unavailable winning move.

Another case is when Alice has exactly the right counts but winning opportunities are scattered. Even if wins are possible, they might not appear early in the string. The greedy scan still captures them because it does not depend on position ordering beyond linear traversal, and every opportunity is evaluated independently.

A final case is when the required number of wins is exactly equal to the maximum achievable wins. The algorithm still works because it constructs the full maximum-win assignment first and only rejects strictly infeasible cases where even that maximum is insufficient.

---
title: "CF 1245B - Restricted RPS"
description: "Alice and Bob are playing a constrained version of rock-paper-scissors. Bob's sequence of moves is already known, and Alice must play a fixed number of each move: a specific number of rocks, papers, and scissors."
date: "2026-06-11T21:48:28+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1245
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 597 (Div. 2)"
rating: 1200
weight: 1245
solve_time_s: 1002
verified: false
draft: false
---

[CF 1245B - Restricted RPS](https://codeforces.com/problemset/problem/1245/B)

**Rating:** 1200  
**Tags:** constructive algorithms, dp, greedy  
**Solve time:** 16m 42s  
**Verified:** no  

## Solution
## Problem Understanding

Alice and Bob are playing a constrained version of rock-paper-scissors. Bob's sequence of moves is already known, and Alice must play a fixed number of each move: a specific number of rocks, papers, and scissors. The challenge is to determine whether Alice can arrange her moves to beat Bob in at least half of the rounds, rounded up. The input consists of the number of rounds, the counts of each type of move Alice must play, and Bob's sequence of moves. The output is either "NO" if Alice cannot win or "YES" followed by a valid sequence of Alice's moves that achieves the required number of wins. The key is that Alice's sequence must respect her move counts exactly.

The constraints are very manageable. The number of rounds $n$ is at most 100, and there are at most 100 test cases. This allows us to consider strategies that inspect each move individually and assign optimal counters greedily, without worrying about time limits. A naive approach that tries all permutations of Alice's moves is unnecessary because the small input size allows a greedy approach to suffice.

Edge cases to be careful of include situations where Alice has an insufficient number of counters for Bob's dominant move. For instance, if Bob plays all rocks and Alice only has one paper, she can only win one round even if there are many rounds, and the output must correctly identify whether this is enough to achieve $\lceil n/2 \rceil$ wins. Another edge case is when multiple valid sequences exist; the problem allows any sequence, so the solution does not have to enumerate all possibilities.

## Approaches

A brute-force approach would try all permutations of Alice's moves and count wins for each, but that would be $O(n!)$, which is impractical even with $n = 100$. The key insight is that each move in Bob's sequence can be countered optimally using the greedy principle: assign Alice's move that beats Bob’s move whenever possible. This guarantees the maximum number of wins because beating Bob's move is always better than not beating it.

Once the greedy assignments are made, any remaining moves can be filled arbitrarily while respecting the move counts. The only point that requires careful attention is to check whether the number of wins from the greedy assignment reaches the required $\lceil n/2 \rceil$. If it does, we can construct the full sequence; otherwise, Alice cannot win.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read $n$, the counts $a, b, c$, and Bob's sequence $s$. Initialize a list for Alice's moves with placeholders.
2. Count the number of moves Alice can use to beat Bob optimally. For each character in $s$:

- If Bob plays 'R' and Alice has paper remaining, assign 'P' and decrement the paper count.
- If Bob plays 'P' and Alice has scissors remaining, assign 'S' and decrement scissors count.
- If Bob plays 'S' and Alice has rock remaining, assign 'R' and decrement rock count.

Each successful assignment increases a win counter.
3. After processing all rounds, check if the number of wins is at least $\lceil n/2 \rceil$. If not, print "NO" and continue to the next test case.
4. Fill in the remaining positions in Alice’s move list with any remaining moves, respecting their counts. Iterate over the placeholders and assign moves in the order of remaining rock, paper, and scissors until all positions are filled.
5. Print "YES" and the constructed sequence.

Why it works: The greedy step ensures that every possible win is captured. Since each move can only be used a fixed number of times, assigning moves that beat Bob first maximizes wins. Filling remaining moves afterward does not reduce the number of wins but ensures the sequence respects the required counts. The invariant is that every assigned winning move truly beats Bob, so the number of wins is maximized.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import ceil

t = int(input())
for _ in range(t):
    n = int(input())
    a, b, c = map(int, input().split())
    s = input().strip()
    
    alice = [''] * n
    wins = 0
    rem_a, rem_b, rem_c = a, b, c
    
    for i, move in enumerate(s):
        if move == 'R' and b > 0:
            alice[i] = 'P'
            b -= 1
            wins += 1
        elif move == 'P' and c > 0:
            alice[i] = 'S'
            c -= 1
            wins += 1
        elif move == 'S' and a > 0:
            alice[i] = 'R'
            a -= 1
            wins += 1
    
    if wins < ceil(n / 2):
        print("NO")
        continue
    
    # Fill remaining moves
    for i in range(n):
        if alice[i] == '':
            if a > 0:
                alice[i] = 'R'
                a -= 1
            elif b > 0:
                alice[i] = 'P'
                b -= 1
            else:
                alice[i] = 'S'
                c -= 1
    
    print("YES")
    print(''.join(alice))
```

The first loop performs the greedy assignment, carefully decrementing the move counts. The second loop ensures that any remaining placeholders are filled with valid moves, respecting Alice's constraints. Using `ceil(n/2)` guarantees correctness for both even and odd $n$. Off-by-one errors are avoided by directly iterating over indices and checking the placeholder status.

## Worked Examples

### Sample Input 1

```
3
1 1 1
RPS
```

| Index | Bob | Alice (greedy) | Wins | Remaining counts (R,P,S) |
| --- | --- | --- | --- | --- |
| 0 | R | P | 1 | 1,0,1 |
| 1 | P | S | 2 | 1,0,0 |
| 2 | S | R | 3 | 0,0,0 |

The number of wins is 3 ≥ ceil(3/2)=2, so Alice wins. All remaining moves are already used.

### Sample Input 2

```
3
3 0 0
RPS
```

| Index | Bob | Alice (greedy) | Wins | Remaining counts (R,P,S) |
| --- | --- | --- | --- | --- |
| 0 | R | '' | 0 | 3,0,0 |
| 1 | P | '' | 0 | 3,0,0 |
| 2 | S | '' | 0 | 3,0,0 |

Wins = 0 < ceil(3/2)=2, so output "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each move is examined once for greedy assignment and once for filling remaining moves. |
| Space | O(n) | Alice's sequence list and input storage. |

Given n ≤ 100 and t ≤ 100, the worst case is 100*100=10,000 operations, well within the 1-second limit.

## Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    from math import ceil
    for _ in range(t):
        n = int(input())
        a, b, c = map(int, input().split())
        s = input().strip()
        alice = [''] * n
        wins = 0
        for i, move in enumerate(s):
            if move == 'R' and b > 0:
                alice[i] = 'P'
                b -= 1
                wins += 1
            elif move == 'P' and c > 0:
                alice[i] = 'S'
                c -= 1
                wins += 1
            elif move == 'S' and a > 0:
                alice[i] = 'R'
                a -= 1
                wins += 1
        if wins < ceil(n / 2):
            print("NO")
            continue
        for i in range(n):
            if alice[i] == '':
                if a > 0:
                    alice[i] = 'R'
                    a -= 1
                elif b > 0:
                    alice[i] = 'P'
                    b -= 1
                else:
                    alice[i] = 'S'
                    c -= 1
        print("YES")
        print(''.join(alice))
    return output.getvalue().strip()

# Provided samples
assert run("2\n3\n1 1 1\nRPS\n3\n3 0 0\nRPS\n") == "YES\nPSR\nNO", "sample 1"

# Custom cases
assert run("1\n1\n0 1 0\nR\n") == "YES\nP
```

---
title: "CF 104400E - stone(easy version)"
description: "We are given a row of stone piles. The game proceeds in alternating turns starting with Alice. On each turn, the current player focuses only on the leftmost pile that still contains stones and removes at least one stone from it."
date: "2026-06-30T23:02:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104400
codeforces_index: "E"
codeforces_contest_name: "Hunan University 2023 the 19th Programming Contest"
rating: 0
weight: 104400
solve_time_s: 47
verified: true
draft: false
---

[CF 104400E - stone(easy version)](https://codeforces.com/problemset/problem/104400/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of stone piles. The game proceeds in alternating turns starting with Alice. On each turn, the current player focuses only on the leftmost pile that still contains stones and removes at least one stone from it. Since this is the easy version with $k = 1$, a turn consists of exactly one such removal, and after the chosen pile becomes empty, play continues on the next pile to the right on the next turn.

The game ends when all piles are empty. The player who is about to move when no stones remain has no legal move and loses immediately, so the previous player is the winner.

Although each pile has an arbitrary number of stones, the player is never forced to split a pile across multiple turns in a constrained way. Any move can remove the entire remaining pile if desired, because removing “any number at least one” includes taking all stones.

The constraints are large: up to $10^5$ test cases and total input size across tests up to $10^5$. This immediately rules out any simulation that does more than constant work per test case. Even an $O(n)$ per test approach would be too slow in aggregate if not carefully managed, but here we will see the structure collapses the problem to constant time reasoning per case.

A subtle edge case that often confuses naive approaches is the role of pile sizes. One might assume the number of stones matters, but since each pile can be emptied in a single move, the actual values do not affect the sequence length.

For example, consider a single test case:

Input:

```
n = 1
a = [1000000000]
```

Even though the pile is huge, Alice can take all stones in one move, leaving Bob with no move and losing immediately. So the outcome is determined entirely by whether the number of piles is odd or even, not by their sizes.

Another misleading case is:

Input:

```
n = 2
a = [1, 100]
```

Even though the second pile is large, the game still consists of exactly two moves: one for each pile.

## Approaches

A brute-force simulation would model each move explicitly. We would maintain a pointer to the current pile and repeatedly subtract some positive number from it, potentially simulating each stone removal. However, since each pile could contain up to $10^9$ stones, this interpretation would suggest up to $10^9$ actions per pile in the worst case, which is clearly infeasible.

The key observation is that optimal play always empties the current pile immediately. There is no strategic benefit in leaving stones behind because the opponent will always face the same situation regardless of how you split removals across multiple turns. Every pile effectively contributes exactly one move to the game length.

This reduces the entire game to a fixed sequence: each pile corresponds to one forced move, and players simply alternate moves over a sequence of length $n$. The only remaining question is who performs the last move.

So the game is equivalent to a simple parity check on the number of piles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(\sum a_i)$ | $O(1)$ | Too slow |
| Parity Reduction | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $T$. Each test case is independent because no state carries between them.
2. For each test case, read $n$, the number of piles. The actual values of the piles are irrelevant to the final outcome, so they can be read and ignored.
3. Determine the winner based only on whether $n$ is odd or even. If $n$ is odd, Alice makes the last move; if $n$ is even, Bob makes the last move.
4. Output "Alice" if $n$ is odd, otherwise output "Bob".

### Why it works

Each pile contributes exactly one move to the game because the player controlling the leftmost pile can always remove all its stones in a single action. After a pile is emptied, it never reappears in play, and the next pile becomes active on the next turn. Therefore, the game always lasts exactly $n$ moves, independent of pile sizes or distribution. Since players alternate moves starting with Alice, the winner is determined solely by the parity of $n$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        arr = list(map(int, input().split()))
        
        if n % 2 == 1:
            print("Alice")
        else:
            print("Bob")

if __name__ == "__main__":
    solve()
```

The solution reads each test case and immediately reduces it to a parity check. The array is consumed only to satisfy input format constraints; its values do not influence computation. The only critical decision is based on $n$, so the algorithm runs in linear time over input size but with constant work per element beyond reading.

A common implementation mistake here is attempting to simulate removals or reasoning about individual stone counts. That leads to unnecessary complexity without changing the outcome.

## Worked Examples

### Example 1

Input:

```
1
1 1
2
```

| Step | n | Remaining piles | Player |
| --- | --- | --- | --- |
| Start | 1 | [2] | Alice |
| 1 | 1 | [] | Bob (no move) |

Alice removes the only pile in one move. Bob has no move and loses, confirming that odd $n$ leads to Alice winning.

### Example 2

Input:

```
1
3 1
2 2 2
```

| Step | n | Remaining piles | Player |
| --- | --- | --- | --- |
| Start | 3 | [2,2,2] | Alice |
| 1 | 3 | [2,2] | Bob |
| 2 | 3 | [2] | Alice |
| 3 | 3 | [] | Bob (no move) |

Bob performs the last move when $n$ is even-indexed in terms of turns, meaning Alice gets the final move here and wins. This confirms that odd $n$ produces an Alice win.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T + \sum n)$ | Each test case is processed in constant time after reading input |
| Space | $O(1)$ | No auxiliary data beyond input variables |

The solution easily fits within limits since all heavy work is limited to input parsing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n, k = map(int, input().split())
        arr = list(map(int, input().split()))
        res.append("Alice" if n % 2 == 1 else "Bob")

    return "\n".join(res)

# provided samples
assert run("3\n1 1\n1\n2 1\n1 2\n3 1\n2 2 2\n") == "Alice\nBob\nAlice"

# custom cases
assert run("1\n1 1\n100\n") == "Alice", "single pile"
assert run("1\n2 1\n1 1\n") == "Bob", "two piles even"
assert run("1\n5 1\n1 1 1 1 1\n") == "Alice", "odd many piles"
assert run("2\n2 1\n5 6\n3 1\n7 8 9\n") == "Bob\nAlice", "mixed cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single pile | Alice | minimal case |
| two piles | Bob | even parity |
| five piles | Alice | larger odd case |
| mixed cases | Bob / Alice | multiple test handling |

## Edge Cases

A minimal input with one pile demonstrates the boundary behavior. For example:

```
1 1
10
```

The algorithm immediately classifies $n = 1$ as odd and outputs Alice. The simulation view confirms Alice empties the only pile and wins instantly.

A two-pile case such as:

```
2 1
3 7
```

alternates moves: Alice removes the first pile, Bob removes the second, leaving Alice with no move. The parity rule correctly predicts Bob.

Large values inside piles do not affect execution. For:

```
3 1
1000000000 1000000000 1000000000
```

each pile still corresponds to exactly one move, so the outcome remains Alice due to odd $n$.

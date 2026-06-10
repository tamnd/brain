---
title: "CF 1419A - Digit Game"
description: "We are asked to simulate a simple turn-based digit game between two agents, Raze and Breach. Each game starts with a positive integer consisting of $n$ digits. The digits are numbered from left to right, starting with 1."
date: "2026-06-11T06:43:05+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1419
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 671 (Div. 2)"
rating: 900
weight: 1419
solve_time_s: 73
verified: true
draft: false
---

[CF 1419A - Digit Game](https://codeforces.com/problemset/problem/1419/A)

**Rating:** 900  
**Tags:** games, greedy, implementation  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a simple turn-based digit game between two agents, Raze and Breach. Each game starts with a positive integer consisting of $n$ digits. The digits are numbered from left to right, starting with 1. Raze can only mark digits in odd positions, and Breach can only mark digits in even positions. They alternate marking digits until only one digit remains. The winner is determined by the parity of that last digit: if it is odd, Raze wins; if it is even, Breach wins. Raze always moves first. The input consists of $t$ independent games, and for each game we must print who wins.

The constraints are moderate. Each number can have up to 1000 digits, and there can be up to 100 games. This rules out any algorithm that would attempt to simulate every turn of marking digits, because that could require up to $n$ operations per game, which is acceptable, but we can do better by reasoning about the final digit without full simulation.

Edge cases are where $n = 1$, meaning there is only one digit and no moves are possible. In that case, the last digit is immediately the winner determinant. For example, input `1\n2` should output `2` because the single digit is even. Another subtle case is when all digits accessible to a player are of the wrong parity, forcing them into a suboptimal marking sequence. Recognizing these scenarios early allows us to compute the winner without simulating every move.

## Approaches

A brute-force approach would simulate each turn: keep track of which digits are unmarked, let Raze and Breach alternate marking a valid digit, and continue until one digit remains. At that point, we inspect its parity. This approach is correct, but it involves $O(n)$ operations per game. With up to 100 games of 1000 digits each, this results in roughly 100,000 operations, which is acceptable but not necessary. It also requires careful handling of alternating turns and indexing, which is error-prone.

The optimal approach arises from observing that the last digit is the only one that matters. Each player will always try to force the last remaining digit into their winning parity. Therefore, the key is to check whether the player who moves last has at least one digit they can leave unmarked of their preferred parity. For odd-length numbers, Raze moves last on odd positions, so we check if there is an odd digit in an odd position. If yes, Raze can ensure the last digit is odd. Otherwise, Breach wins. Similarly, for even-length numbers, Breach moves last on even positions, so we check for an even digit in an even position. This reasoning allows a direct $O(n)$ check per game, scanning the digits once, without simulating turns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per game | O(n) | Accepted but unnecessary |
| Optimal | O(n) per game | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of games $t$. For each game, read the number of digits $n$ and the string representing the integer.
2. Determine whether $n$ is odd or even. If $n$ is odd, Raze will have the final move relevant to odd positions; if $n$ is even, Breach will have the final move relevant to even positions.
3. If $n$ is odd, scan all digits in odd positions (1, 3, 5, ...) and check if any of them is odd. If at least one is odd, Raze can ensure the last digit left is odd, so Raze wins. Otherwise, Breach wins.
4. If $n$ is even, scan all digits in even positions (2, 4, 6, ...) and check if any of them is even. If at least one is even, Breach can ensure the last digit left is even, so Breach wins. Otherwise, Raze wins.
5. Output `1` if Raze wins or `2` if Breach wins for each game.

Why it works: The last remaining digit determines the winner, and each player can control their accessible positions optimally. By checking if the player who moves last has a winning digit available in their allowed positions, we guarantee the correct outcome without simulating each turn. No sequence of moves can override this because the opposing player cannot remove the only winning choice if it exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    if n % 2 == 1:
        # Raze has the final move on odd positions
        for i in range(0, n, 2):  # odd positions in 0-based indexing
            if int(s[i]) % 2 == 1:
                print(1)
                break
        else:
            print(2)
    else:
        # Breach has the final move on even positions
        for i in range(1, n, 2):  # even positions in 0-based indexing
            if int(s[i]) % 2 == 0:
                print(2)
                break
        else:
            print(1)
```

We use zero-based indexing to simplify position handling. The loop `for i in range(0, n, 2)` visits positions 1, 3, 5 in 1-based indexing. The `else` clause of the for loop runs if the loop did not break, meaning no winning digit was found. This avoids introducing a separate flag variable. We strip the input string to remove the trailing newline from `input()`.

## Worked Examples

### Sample Input Trace 1

Input:

```
1
3
102
```

| Step | n | Positions checked | Result |
| --- | --- | --- | --- |
| 1 | 3 | odd positions 1,3 → digits 1,2 | digit 1 is odd |
| 2 | n odd, Raze checks odd digits | found odd at position 1 | Raze wins |

This demonstrates that Raze wins because they can leave the last digit odd.

### Sample Input Trace 2

Input:

```
1
4
2069
```

| Step | n | Positions checked | Result |
| --- | --- | --- | --- |
| 1 | 4 | even positions 2,4 → digits 0,9 | digit 0 is even |
| 2 | n even, Breach checks even digits | found even at position 2 | Breach wins |

This confirms that the algorithm correctly identifies Breach's winning strategy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per game | We scan either odd or even positions once, which is linear in the number of digits |
| Space | O(1) | No additional memory beyond input string storage and loop variables |

Given $t \le 100$ and $n \le 1000$, the worst case is 100,000 digit checks, which is well within the 1-second limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        if n % 2 == 1:
            for i in range(0, n, 2):
                if int(s[i]) % 2 == 1:
                    print(1)
                    break
            else:
                print(2)
        else:
            for i in range(1, n, 2):
                if int(s[i]) % 2 == 0:
                    print(2)
                    break
            else:
                print(1)
    return output.getvalue().strip()

# Provided samples
assert run("4\n1\n2\n1\n3\n3\n102\n4\n2069\n") == "2\n1\n1\n2", "sample cases"

# Custom cases
assert run("2\n1\n1\n2\n8") == "1\n2", "single-digit edge cases"
assert run("2\n5\n13579\n6\n246802") == "1\n2", "all odd or all even"
assert run("1\n3\n222") == "2", "odd length, no odd digits"
assert run("1\n4\n1357") == "1", "even length, no even digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | 1 | Single-digit odd, Raze wins immediately |
| `1\n1\n2` | 2 | Single-digit even, Breach wins immediately |
| `5\n13579` | 1 | Odd-length all odd digits, Raze can win |
| `6\n246802` | 2 | Even-length all even digits, Breach can win |
| `3\n222` | 2 | Odd-length, no odd digits, Raze loses |
| `4\n1357` | 1 | Even-length, no even digits, Breach cannot win |

## Edge Cases

For `n = 1`, the algorithm immediately checks the only digit. For `1\n3`, Raze wins because the digit is odd

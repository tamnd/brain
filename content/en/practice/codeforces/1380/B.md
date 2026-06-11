---
title: "CF 1380B - Universal Solution"
description: "We are asked to play a sequence of rock-paper-scissors rounds against a predictable bot. The bot has a fixed sequence of moves stored in a string of length $n$, where each character is R, P, or S. However, we do not know the bot’s starting position within the string."
date: "2026-06-11T10:55:49+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1380
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 91 (Rated for Div. 2)"
rating: 1400
weight: 1380
solve_time_s: 110
verified: false
draft: false
---

[CF 1380B - Universal Solution](https://codeforces.com/problemset/problem/1380/B)

**Rating:** 1400  
**Tags:** greedy  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to play a sequence of rock-paper-scissors rounds against a predictable bot. The bot has a fixed sequence of moves stored in a string of length $n$, where each character is R, P, or S. However, we do not know the bot’s starting position within the string. The bot’s moves repeat cyclically if we play more than $n$ rounds. Our goal is to select our moves for $n$ rounds in such a way that the **average number of wins over all possible starting positions of the bot** is maximized.

The input is several test cases, each giving the bot’s string. The output is a string of our moves of equal length that maximizes our average wins. Since $n$ can be as large as $2 \cdot 10^5$ and there can be up to 1000 test cases, any approach that scales worse than $O(n)$ per test case will likely exceed the time limit.

Edge cases include strings of length 1, where the choice is trivial, and strings where all characters are the same. Another subtle case is when the bot’s moves are perfectly balanced (equal numbers of R, P, and S), where naive cyclic strategies may appear appealing but the optimal strategy is still to choose the move that beats the most frequent character.

## Approaches

The brute-force approach is straightforward. For each possible starting index, we could simulate all $n$ rounds and count wins for every possible sequence of our moves. Then we could average over starting positions and pick the sequence that maximizes this average. This works in theory, but its time complexity is $O(n^2)$ per test case, because there are $n$ starting positions and each requires $n$ comparisons. For $n = 2 \cdot 10^5$, this would result in about $4 \cdot 10^{10}$ operations, which is far too slow.

The key insight is that the bot’s starting position only shifts its string. We are asked for the sequence that maximizes **the average number of wins over all shifts**. This means that each character’s contribution is symmetric under rotation. Instead of worrying about exact positions, we can consider **frequency**: the optimal move is simply the one that beats the most frequent move in the string. This single choice repeated $n$ times maximizes our wins regardless of how the bot’s string is rotated. The problem reduces from analyzing all rotations to counting the frequency of R, P, and S.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal (frequency-based) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For a given string $s$, count the occurrences of each character: $count_R$, $count_P$, and $count_S$. These counts represent how many times the bot would play Rock, Paper, and Scissors respectively.
2. Determine which move beats the most frequent character. Rock beats Scissors, Paper beats Rock, and Scissors beats Paper. Compare $count_R$, $count_P$, and $count_S$ to see which gives the highest number of guaranteed wins.
3. Construct our output string by repeating that single move $n$ times. This ensures that, no matter the bot’s starting index, we are always choosing the move that maximizes the total wins averaged over rotations.
4. Print the result.

Why it works: Each rotation of the bot's string is just a cyclic shift, so the frequency of moves in the string does not change. Choosing the move that beats the most frequent bot move guarantees the maximum average number of wins, because this move wins against the largest subset of the bot’s moves regardless of the starting position.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    count_R = s.count('R')
    count_P = s.count('P')
    count_S = s.count('S')
    
    if count_R >= count_P and count_R >= count_S:
        print('P' * len(s))
    elif count_S >= count_R and count_S >= count_P:
        print('R' * len(s))
    else:
        print('S' * len(s))
```

The code first reads the number of test cases. For each test case, it counts the occurrences of each move in the bot’s string. We then choose the move that beats the most frequent bot move and repeat it $n$ times. The comparisons handle ties naturally because any of the moves that beat the highest-frequency character is valid. The `strip()` ensures we remove the newline character from the input string.

## Worked Examples

Sample 1:

| Variable | Value |
| --- | --- |
| s | "RRRR" |
| count_R | 4 |
| count_P | 0 |
| count_S | 0 |
| chosen move | P |
| output | "PPPP" |

This shows that when the bot always plays Rock, choosing Paper for every round guarantees a win every time.

Sample 2:

| Variable | Value |
| --- | --- |
| s | "RSP" |
| count_R | 1 |
| count_P | 1 |
| count_S | 1 |
| chosen move | P (or R or S) |
| output | "PPP" |

Here, all moves are equally frequent. Choosing Paper wins against Rock, loses to Scissors, and draws against Paper. Averaged over all rotations, this gives the maximum expected wins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the string once to count frequencies. |
| Space | O(1) | Only three counters are needed regardless of string length. |

Given the constraints (sum of lengths of all strings ≤ 2·10^5), this solution easily fits within 2 seconds and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open(__file__).read(), globals())
    return output.getvalue().strip()

# Provided samples
assert run("3\nRRRR\nRSP\nS\n") == "PPPP\nPPP\nR", "Sample tests"

# Custom cases
assert run("1\nP\n") == "S", "Single P"
assert run("1\nRS\n") == "PP", "Tie counts"
assert run("1\nRRRRRRRRRR\n") == "PPPPPPPPPP", "All equal R"
assert run("1\nRSPRSPRSPR\n") == "PPPPPPPPPP", "Mixed string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1\nP\n" | "S" | Single-character string |
| "1\nRS\n" | "PP" | Tied counts of R and S |
| "1\nRRRRRRRRRR\n" | "PPPPPPPPPP" | All moves the same |
| "1\nRSPRSPRSPR\n" | "PPPPPPPPPP" | Mixed moves |

## Edge Cases

For a single-character string such as `"S"`, the algorithm counts one Scissors, zero Rock, zero Paper. The optimal move is Rock, repeated once, yielding `"R"`. The frequency-based choice naturally handles this without special cases. For strings with equal counts of multiple characters like `"RSP"`, the algorithm picks any move that beats one of the highest-frequency characters, which maximizes the average number of wins over all rotations. The code handles ties correctly because the comparisons use `>=` to cover equality, and repeating a single move is still optimal.

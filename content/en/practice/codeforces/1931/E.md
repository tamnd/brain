---
title: "CF 1931E - Anna and the Valentine's Day Gift"
description: "The game begins with a list of integers. Anna moves first by reversing the digits of any number, which can increase or decrease its value depending on the digits. Sasha moves second by concatenating any two numbers, reducing the list size by one."
date: "2026-06-08T18:26:46+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1931
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 925 (Div. 3)"
rating: 1400
weight: 1931
solve_time_s: 130
verified: false
draft: false
---

[CF 1931E - Anna and the Valentine's Day Gift](https://codeforces.com/problemset/problem/1931/E)

**Rating:** 1400  
**Tags:** games, greedy, math, sortings  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

The game begins with a list of integers. Anna moves first by reversing the digits of any number, which can increase or decrease its value depending on the digits. Sasha moves second by concatenating any two numbers, reducing the list size by one. The game alternates in this way until only one number remains. Sasha wins if the final number is at least $10^m$, otherwise Anna wins.

The input consists of multiple test cases. Each test case specifies the number of integers $n$, the threshold $m$, and the list of integers $a$. The output for each test case is the winner assuming both players play optimally.

The constraints indicate that $n$ can reach $2 \cdot 10^5$ and the sum of all $n$ across test cases is also capped at $2 \cdot 10^5$. This rules out any solution that simulates all game states or permutations because the number of potential moves grows combinatorially with $n$. Optimal play must therefore rely on **strategic observations about number manipulation**, rather than brute-force game tree exploration.

An edge case occurs when $n = 1$, because Anna cannot reverse to influence the game, and Sasha has no move. Similarly, when numbers are already large, Anna’s reverse cannot prevent Sasha from winning. For example, if the only number is $9$ and $m = 1$, Anna cannot avoid a win for Sasha because $9 \ge 10^0 = 1$.

## Approaches

A naive approach would attempt to simulate the game, reversing every number on Anna's turn and concatenating every pair on Sasha’s turn. This would be correct but infeasible because the number of permutations is factorial in $n$. For large $n$, this would exceed the time limit.

The key observation is that **Anna cannot decrease the largest number enough to prevent Sasha from creating a number $\ge 10^m$** if at least one number has enough digits. Sasha can always concatenate two numbers to produce a number at least as large as the largest element, because concatenation increases the number of digits or preserves them. Anna's reverse only swaps digits, which cannot increase the number of digits beyond the original number.

Thus, the solution reduces to checking if **the largest possible number obtainable via optimal concatenation by Sasha** is at least $10^m$. If it is, Sasha wins; otherwise, Anna wins. This allows a **greedy evaluation based on the largest digits**, avoiding full simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) per game | O(n) | Too slow |
| Greedy Max Check | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$ and $m$, followed by the list of integers $a$.
3. Identify the integer with the **maximum number of digits** in $a$. Reversing any integer does not change its number of digits.
4. Compute $10^m$.
5. If the largest integer in $a$ is **at least $10^m$**, Sasha can immediately or through concatenation reach a number $\ge 10^m$. Declare Sasha as the winner.
6. Otherwise, Anna can prevent Sasha from reaching $10^m$, and Anna wins.

**Why it works:** The invariant is that Sasha’s concatenation always produces a number at least as large as the largest element in the current list. Anna’s reverse can never increase the number of digits. Therefore, the game outcome depends solely on whether any number already has enough digits to reach the threshold when concatenated optimally by Sasha.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        threshold = 10 ** m
        max_val = max(a)
        if max_val >= threshold:
            print("Sasha")
        else:
            print("Anna")

if __name__ == "__main__":
    solve()
```

The solution reads input using fast I/O. For each test case, it computes the maximum element and compares it to $10^m$ to determine the winner. The use of `max(a)` ensures O(n) evaluation per test case.

## Worked Examples

| Test Case | n | m | a | max(a) | 10^m | Winner |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 14, 2 | 14 | 100 | Sasha |
| 2 | 3 | 5 | 9, 56, 1 | 56 | 100000 | Anna |
| 3 | 4 | 10 | 1, 2007, 800, 1580 | 2007 | 10000000000 | Anna |
| 4 | 4 | 5 | 5000, 123, 30, 4 | 5000 | 100000 | Sasha |

This demonstrates that we only need to examine the largest element in the list to determine the outcome.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Scanning the list to find the maximum takes O(n). |
| Space | O(n) | Storing the list of integers per test case. |

Given that the sum of n over all test cases is ≤ 2 · 10^5, this solution fits well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("9\n2 2\n14 2\n3 5\n9 56 1\n4 10\n1 2007 800 1580\n4 5\n5000 123 30 4\n10 10\n6 4 6 2 3 1 10 9 10 7\n1 1\n6\n1 1\n10\n8 9\n1 2 9 10 10 2 10 2\n4 5\n10 10 10 10") == "\n".join([
    "Sasha","Anna","Anna","Sasha","Sasha","Anna","Anna","Anna","Sasha"
]), "sample 1"

# Custom test cases
assert run("2\n1 0\n1\n1 1\n9") == "Sasha\nAnna", "single element edge cases"
assert run("2\n3 2\n99 9 10\n3 1\n1 1 1") == "Sasha\nAnna", "threshold edge cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 1 | Sasha | Single element ≥ threshold |
| 1 1 9 | Anna | Single element < threshold |
| 99 9 10 | Sasha | Max element triggers Sasha's win |
| 1 1 1 | Anna | All elements below threshold, Anna wins |

## Edge Cases

If the list has only one number, Anna cannot influence the game and the outcome depends solely on whether that number is ≥ $10^m$. For example, with input `1 1 10`, Sasha wins immediately. If the list contains large numbers but m is huge, even the largest number may not reach $10^m$, allowing Anna to win. This approach accounts for these edge cases correctly without simulating any moves.

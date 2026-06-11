---
title: "CF 1374C - Move Brackets"
description: "We are given a string of brackets consisting of exactly half opening brackets '(' and half closing brackets ')', and our goal is to make it a valid, balanced bracket sequence."
date: "2026-06-11T11:07:50+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1374
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 653 (Div. 3)"
rating: 1000
weight: 1374
solve_time_s: 102
verified: true
draft: false
---

[CF 1374C - Move Brackets](https://codeforces.com/problemset/problem/1374/C)

**Rating:** 1000  
**Tags:** greedy, strings  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of brackets consisting of exactly half opening brackets '(' and half closing brackets ')', and our goal is to make it a valid, balanced bracket sequence. We are allowed to move a single bracket to either the beginning or the end of the string in one move, and we need to minimize the number of such moves. The output is simply the minimum number of moves required.

Since the string always has equal numbers of opening and closing brackets, a solution always exists. The input constraints are small: the length of each string is at most 50 and the number of test cases is at most 2000. This allows an algorithm with a time complexity on the order of $O(n)$ per test case without concern. We cannot assume that the brackets are in any initial order, so edge cases include strings that start with many closing brackets or end with many opening brackets, like ")))(((" or ")()(".

A naive approach might attempt to simulate moving each bracket and checking if the resulting string is balanced. This is wasteful because the number of possible moves grows combinatorially. The key insight is that we do not need to simulate every move: the minimal number of moves is determined by the maximum depth of imbalance encountered when scanning from left to right. For example, a prefix with more closing than opening brackets represents a deficit that must eventually be corrected by moving brackets to the front.

## Approaches

The brute-force approach would be to try moving every bracket to the beginning or the end, recursively generating all sequences, and checking if each sequence is balanced. Each check is $O(n)$, and the number of possible sequences grows factorially with $n$, making this infeasible even for $n=50$.

The optimal approach comes from tracking the prefix balance as we scan the string. Define a running sum where '(' increases it by 1 and ')' decreases it by 1. A negative balance means we have more closing brackets than opening brackets at that point, which indicates the minimum number of opening brackets we must move to the front to avoid negative prefixes. The answer is simply the largest negative value of this running sum, turned positive. This works because the bracket sequence is guaranteed to have equal counts, so correcting the worst deficit automatically guarantees the rest of the string can be balanced with no additional moves.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Prefix Balance | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `balance` to zero. This will track the net difference between opening and closing brackets as we iterate.
2. Initialize `max_deficit` to zero. This will record the largest negative balance encountered.
3. Iterate over each character in the string. For each '(', increment `balance` by 1. For each ')', decrement `balance` by 1.
4. After updating `balance`, if `balance` is negative, update `max_deficit` to be the maximum of its current value and `-balance`. This captures the worst prefix deficit we have seen so far.
5. After scanning the entire string, `max_deficit` contains the minimum number of moves required to correct all negative prefixes. Output `max_deficit`.

Why it works: The prefix balance captures exactly where the sequence goes below zero, which is the only situation requiring bracket movement. Each negative balance represents an unmatched closing bracket that needs a corresponding opening bracket moved to the front. Correcting the maximum negative prefix ensures no prefix in the final sequence is invalid, guaranteeing the resulting sequence is balanced.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    balance = 0
    max_deficit = 0
    for c in s:
        if c == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            max_deficit = max(max_deficit, -balance)
    print(max_deficit)
```

The solution reads input using fast I/O. For each test case, we maintain a running `balance` and record the maximum deficit whenever the balance drops below zero. This is sufficient because only the largest deficit dictates how many opening brackets must be moved to the front to make all prefixes non-negative. Edge conditions, such as the string starting with several closing brackets, are automatically handled because `balance` goes negative immediately, and `max_deficit` is updated accordingly.

## Worked Examples

Trace for the input `)))(((()))`:

| char | balance | max_deficit |
| --- | --- | --- |
| ')' | -1 | 1 |
| ')' | -2 | 2 |
| ')' | -3 | 3 |
| '(' | -2 | 3 |
| '(' | -1 | 3 |
| '(' | 0 | 3 |
| '(' | 1 | 3 |
| ')' | 0 | 3 |
| ')' | -1 | 3 |
| ')' | -2 | 3 |

The maximum deficit is 3, so we need 3 moves. This corresponds exactly to moving the first three opening brackets to the front.

Trace for `()()`:

| char | balance | max_deficit |
| --- | --- | --- |
| '(' | 1 | 0 |
| ')' | 0 | 0 |
| '(' | 1 | 0 |
| ')' | 0 | 0 |

No prefix ever goes negative, so zero moves are required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | Each test case is scanned once, n ≤ 50, t ≤ 2000 |
| Space | O(1) | Only a few integer variables are maintained per test case |

The total number of operations is at most 50 * 2000 = 100,000, which easily fits within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        balance = 0
        max_deficit = 0
        for c in s:
            if c == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                max_deficit = max(max_deficit, -balance)
        output.append(str(max_deficit))
    return "\n".join(output)

# provided samples
assert run("4\n2\n)(\n4\n()()\n8\n())()()(\n10\n)))((((())\n") == "1\n0\n1\n3", "sample 1"

# custom tests
assert run("1\n2\n()\n") == "0", "already balanced"
assert run("1\n6\n)))((("\n") == "3", "all closing then opening"
assert run("1\n6\n((()))\n") == "0", "already balanced nested"
assert run("1\n4\n)(()\n") == "1", "single move to correct prefix"
assert run("1\n10\n)()()()()(\n") == "1", "prefix deficit occurs only at first char"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n()\n | 0 | minimal size, already balanced |
| 6\n)))((\n | 3 | all closing then opening, maximum deficit |
| 6\n((()))\n | 0 | nested already correct |
| 4\n)(()\n | 1 | single move needed to fix prefix |
| 10\n)()()()()(\n | 1 | first char causes deficit only |

## Edge Cases

Consider the input `)))(((`. Scanning from left to right, the balance goes -1, -2, -3, -2, -1, 0. The largest negative balance is -3, so `max_deficit` becomes 3. Moving three opening brackets to the front produces `((()))`, which is fully balanced. The algorithm automatically handles strings that start with many closing brackets or have interleaved deficits without any special case handling. Similarly, an already balanced string like `()()` never triggers `balance < 0`, and the result is correctly zero moves.

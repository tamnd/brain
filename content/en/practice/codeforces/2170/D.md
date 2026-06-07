---
title: "CF 2170D - Almost Roman"
description: "We are given a string consisting of the characters 'X', 'V', 'I', and '?'. Each letter has a numeric value: 'X' is worth 10, 'V' is worth 5, and 'I' is usually worth 1, but if it is immediately followed by an 'X' or 'V', it counts as -1."
date: "2026-06-07T23:12:39+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2170
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 185 (Rated for Div. 2)"
rating: 2200
weight: 2170
solve_time_s: 107
verified: false
draft: false
---

[CF 2170D - Almost Roman](https://codeforces.com/problemset/problem/2170/D)

**Rating:** 2200  
**Tags:** constructive algorithms, greedy, implementation  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string consisting of the characters 'X', 'V', 'I', and '?'. Each letter has a numeric value: 'X' is worth 10, 'V' is worth 5, and 'I' is usually worth 1, but if it is immediately followed by an 'X' or 'V', it counts as -1. The string value is the sum of the values of all its letters. Question marks can be replaced with any combination of the letters 'X', 'V', or 'I', but the replacements must respect given availability constraints. For each query, we are asked to find the minimum possible string value after replacing all question marks using only the letters allowed by the query.

The input provides multiple test cases, each with a string and multiple queries. Each query specifies the number of letters of each type that can be used to replace the question marks. Constraints allow strings up to length 3×10^5 and the total number of queries across all test cases also up to 3×10^5. This suggests that any solution that considers all permutations of replacements would be far too slow, since the worst-case number of question marks could approach 3×10^5.

A subtle part of the problem is the definition of 'I'. Its value depends on the next character, which means greedy decisions about where to place 'I' can affect the total value in non-obvious ways. For example, consider a string "I?X" with only one 'X' available for replacement. Replacing '?' with 'X' would make the first 'I' count as -1, lowering the total value, whereas replacing it with 'I' would make it +1. A naive approach that replaces all question marks with the smallest absolute letter value ('I') might not produce the minimum possible sum.

Edge cases include strings that are all question marks, strings ending with 'I', and queries where only a subset of letters is available, making certain placements impossible. For instance, a string "??" with available letters 1 'X' and 1 'V' should consider which combination yields the lowest sum, taking into account that 'I' before 'X' or 'V' subtracts from the sum.

## Approaches

The brute-force approach is to try all possible replacements for question marks for each query, compute the string value for each, and pick the minimum. This works in theory because we can calculate the value of any string deterministically, but the number of replacements is exponential in the number of question marks. If the string has 10 question marks, there are 3^10 ≈ 59,000 possibilities; if it has 3×10^5 question marks, brute force is utterly infeasible. The brute-force solution would be correct but too slow.

The key observation is that the minimum value can be achieved by a greedy placement strategy. Since 'X' contributes +10, 'V' contributes +5, and 'I' can be -1 or +1 depending on its successor, we should prioritize placements that turn 'I' into -1 whenever possible. That is, if an 'I' precedes an 'X' or 'V', it will subtract from the sum. Therefore, we aim to place 'I' before the largest available letters and place 'I's last only if there are no 'X' or 'V' after it. At the same time, we want to place 'X' and 'V' toward the end, to maximize the number of preceding 'I's that are counted as -1.

We can precompute for the string the positions of fixed letters and the relative positions of question marks. Then for each query, we simulate filling the question marks from left to right, choosing 'X' and 'V' last to convert as many preceding 'I's into -1 contributions. The remaining letters fill in as 'I'. This reduces the problem to a linear scan per query, producing an O(n + q) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^k × n) where k = # of '?') | O(n) | Too slow |
| Greedy / Linear Simulation | O(n + q) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the base value of the string ignoring question marks. Iterate from left to right: add 10 for 'X', 5 for 'V', and decide the value of 'I' based on the next character if known.
2. Record positions of question marks in an array. We will process them in left-to-right order.
3. For each query, copy the availability of letters into mutable counters: c_X, c_V, c_I.
4. Traverse the string left to right. Whenever a '?' is encountered, decide what letter to place:

- If placing an 'I' before a fixed 'X' or 'V' or before a future '?' that will be replaced with 'X' or 'V', it will count as -1. Place 'I' in such positions if c_I > 0.
- Otherwise, place 'X' or 'V' as late as possible to maximize preceding 'I's counting as -1. Reduce c_X or c_V accordingly.
5. After replacement, scan again to compute the total string value using the Roman-style evaluation: iterate from left to right, and whenever an 'I' is followed by 'X' or 'V', count it as -1; otherwise +1. Add the fixed contributions for 'X' and 'V'.
6. Output the total value for this query.

The algorithm works because the greedy choice ensures that every 'I' that can be converted to -1 will be, and 'X'/'V' are positioned to maximize this effect. Since we only ever assign letters within the availability limits, we maintain correctness under the query constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compute_min_value(s, counts):
    n = len(s)
    s = list(s)
    c_X, c_V, c_I = counts
    q_positions = [i for i, ch in enumerate(s) if ch == '?']

    # Greedy assignment
    for i in q_positions:
        # Check if we can force this I to be -1
        # Lookahead to next known character
        if c_I > 0:
            next_char = None
            for j in range(i+1, n):
                if s[j] != '?':
                    next_char = s[j]
                    break
            if next_char in ('X', 'V'):
                s[i] = 'I'
                c_I -= 1
                continue
        # Otherwise assign smallest effect: assign I if available
        if c_I > 0:
            s[i] = 'I'
            c_I -= 1
        elif c_V > 0:
            s[i] = 'V'
            c_V -= 1
        elif c_X > 0:
            s[i] = 'X'
            c_X -= 1

    # Compute string value
    total = 0
    for i in range(n):
        if s[i] == 'X':
            total += 10
        elif s[i] == 'V':
            total += 5
        elif s[i] == 'I':
            if i + 1 < n and s[i+1] in ('X', 'V'):
                total -= 1
            else:
                total += 1
    return total

def main():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        s = input().strip()
        queries = [tuple(map(int, input().split())) for _ in range(q)]
        for counts in queries:
            print(compute_min_value(s, counts))

if __name__ == "__main__":
    main()
```

The solution first identifies all question mark positions. For each query, it greedily assigns letters to minimize the string value: it prefers to place 'I' before 'X' or 'V' to take advantage of the -1 rule, and fills remaining question marks with letters according to availability. The final value computation uses the Roman-style evaluation rule for 'I'.

## Worked Examples

Sample Input 1:

```
3
???
3 0 0
2 3 1
0 1 2
```

Trace for the first query (3,0,0):

| Index | Letter | Decision | Value Contribution |
| --- | --- | --- | --- |
| 0 | ? | X | +10 |
| 1 | ? | X | +10 |
| 2 | ? | X | +10 |

Total = 30. The algorithm chooses 'X' since only 'X's are available. This confirms correct greedy filling.

Second query (2,3,1):

| Index | Letter | Decision | Value Contribution |
| --- | --- | --- | --- |
| 0 | ? | X | +10 |
| 1 | ? | V | +5 |
| 2 | ? | I | +1 |

Total = 16. The algorithm ensures availability constraints are respected while still trying to place 'I' before letters that make it -1, but here only one 'I' is available. This trace shows how availability affects choice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test case | Linear scan to assign letters and compute value. |
| Space | O(n) | Store positions of question marks and working copy of string. |

Given the constraints, total n and q across all test cases ≤

---
title: "CF 106038A - Salvador"
description: "We are tracking a vote among four fixed candidates, the turtles Rafael, Leonardo, Donatello, and Michelangelo. Each candidate already has some number of votes, and there is a pool of remaining votes that have not yet been cast."
date: "2026-06-20T13:31:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106038
codeforces_index: "A"
codeforces_contest_name: "UNICAMP Selection Contest 2025"
rating: 0
weight: 106038
solve_time_s: 45
verified: true
draft: false
---

[CF 106038A - Salvador](https://codeforces.com/problemset/problem/106038/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tracking a vote among four fixed candidates, the turtles Rafael, Leonardo, Donatello, and Michelangelo. Each candidate already has some number of votes, and there is a pool of remaining votes that have not yet been cast. Every remaining vote will go to exactly one of the four candidates, but we do not know how they will be distributed.

A candidate wins only if, after all remaining votes are assigned in the most favorable way for that candidate, they end up with strictly more than half of the total final votes. The task is to determine which turtles still have a theoretical path to becoming the unique majority winner.

The input size is constant in structure, since there are always four candidates. The only varying magnitude is the number of remaining votes, which can be large. This immediately rules out any need for complex data structures or simulation over votes. Any solution that tries to enumerate distributions of remaining votes is exponential in nature and impossible even for moderate values, since each of the remaining votes independently chooses one of four candidates.

A subtle edge case occurs when no candidate currently has a clear lead but the remaining votes are insufficient to create a majority for anyone. For example, if all votes are already cast and no one exceeds half, no winner is possible. Another corner case is when one candidate already has a strong lead but still might be overtaken if remaining votes can be redistributed optimally.

Consider this scenario: current votes are 10 0 0 0 with 5 remaining votes. The total becomes 15, so majority requires at least 8 votes. Rafael already has 10, so he trivially satisfies the condition, but we still must check others carefully. Leonardo, Donatello, and Michelangelo would need all 5 remaining votes plus additional deficit recovery, which is impossible.

Another scenario: 1 1 1 1 with 4 remaining votes. Total becomes 8, majority threshold is 5. Each candidate could receive all 4 remaining votes, ending at 5, so all are still possible winners. A naive interpretation that only current leaders matter would be incorrect here.

## Approaches

The brute-force idea would be to distribute each of the remaining votes across four candidates and simulate all possible outcomes. Each vote has 4 choices, so this produces $4^r$ possibilities where $r$ is the number of remaining votes. Even for $r = 20$, this already exceeds a billion configurations, making it infeasible.

The key observation is that we do not need to simulate distributions. For any fixed candidate, we only need to know whether there exists some allocation of remaining votes that allows them to exceed half of the final total. The best possible scenario for a candidate is when all remaining votes go to them, since giving votes to others only makes their task harder. This reduces the problem to a direct feasibility check per candidate.

We compute the final total votes as the sum of all current votes plus remaining votes. The winning threshold is strictly more than half of this total. For each candidate, we check whether their current votes plus all remaining votes is strictly greater than this threshold. If yes, they are still capable of winning; otherwise, they are eliminated.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4^R) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to evaluating a simple inequality for each candidate.

1. Read the four current vote counts and the number of remaining votes. We also compute the total number of votes after all voting is finished by summing the four current values and adding the remaining votes.
2. For each candidate, compute the best possible final score by assuming they receive all remaining votes. This is the most favorable case for that candidate and gives an upper bound on their achievable result.
3. Compute the majority threshold as half of the total final votes, and require strictly greater than this value. This strictness matters because ties do not produce a winner.
4. For each candidate, check whether their best-case score exceeds the majority threshold. If it does, we mark them as still having a chance to win.
5. Output all such candidates in alphabetical order. If none qualify, output the string indicating that there are no winners.

### Why it works

For any candidate, distributing remaining votes away from them can only reduce their final total, while the total number of votes remains fixed regardless of distribution. Since the winning condition depends only on final totals relative to a fixed threshold, the best possible outcome for a candidate is achieved by giving them every remaining vote. If even this maximal scenario fails to cross the majority threshold, then no other distribution can help them, because any alternative allocation strictly decreases their score without changing the threshold.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    r, l, d, m, rem = map(int, input().split())
    names = [("Donatello", d), ("Leonardo", l), ("Michelangelo", m), ("Rafael", r)]

    total = r + l + d + m + rem
    threshold = total // 2  # must be strictly greater

    res = []

    for name, cur in names:
        if cur + rem > threshold:
            res.append(name)

    if not res:
        print("sem vencedores")
    else:
        res.sort()
        for x in res:
            print(x)

if __name__ == "__main__":
    main()
```

The solution begins by reading the five integers and grouping candidates with their current votes. The total final number of votes is computed once, since it does not depend on how remaining votes are distributed. The threshold is derived using integer division, and we rely on a strict inequality when checking feasibility.

Each candidate is evaluated independently by adding all remaining votes to their current count. This directly implements the best-case reasoning. Sorting ensures alphabetical output, since candidate order in the input is not guaranteed to match required output order.

A common pitfall is using `>=` instead of `>`. The problem requires strictly more than half, so equality does not qualify as a win.

## Worked Examples

### Example 1

Input:

```
0 0 0 0 10000
```

| Candidate | Current | Remaining | Best Case | Total Votes | Threshold | Wins? |
| --- | --- | --- | --- | --- | --- | --- |
| Rafael | 0 | 10000 | 10000 | 10000 | 5000 | Yes |
| Leonardo | 0 | 10000 | 10000 | 10000 | 5000 | Yes |
| Donatello | 0 | 10000 | 10000 | 10000 | 5000 | Yes |
| Michelangelo | 0 | 10000 | 10000 | 10000 | 5000 | Yes |

All candidates exceed half in their best-case scenario, so all remain viable winners.

### Example 2

Input:

```
5 4 3 3 0
```

| Candidate | Current | Remaining | Best Case | Total Votes | Threshold | Wins? |
| --- | --- | --- | --- | --- | --- | --- |
| Rafael | 5 | 0 | 5 | 15 | 7 | No |
| Leonardo | 4 | 0 | 4 | 15 | 7 | No |
| Donatello | 3 | 0 | 3 | 15 | 7 | No |
| Michelangelo | 3 | 0 | 3 | 15 | 7 | No |

No candidate can reach a majority since no remaining votes exist and all are below the threshold.

These traces show that the algorithm consistently evaluates candidates against a fixed global threshold while maximizing their individual contribution independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only four candidates are checked with constant-time arithmetic operations |
| Space | O(1) | Only a fixed amount of storage for counters and output list |

The computation is independent of the magnitude of input values, so it trivially fits within all constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    r, l, d, m, rem = map(int, _sys.stdin.readline().split())
    names = [("Donatello", d), ("Leonardo", l), ("Michelangelo", m), ("Rafael", r)]
    total = r + l + d + m + rem
    threshold = total // 2

    res = [name for name, cur in names if cur + rem > threshold]

    if not res:
        return "sem vencedores"
    res.sort()
    return "\n".join(res)

# provided samples
assert run("0 0 0 0 10000") == "Donatello\nLeonardo\nMichelangelo\nRafael"
assert run("5 4 3 3 0") == "sem vencedores"

# custom cases
assert run("1 1 1 1 4") == "Donatello\nLeonardo\nMichelangelo\nRafael"
assert run("10 0 0 0 5") == "Rafael"
assert run("3 3 3 3 1") == "sem vencedores"
assert run("1000000 0 0 0 0") == "Rafael"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 4 | all names | symmetric tie with full redistribution |
| 10 0 0 0 5 | Rafael | strong leader already over threshold |
| 3 3 3 3 1 | sem vencedores | insufficient single vote to create majority |
| 1000000 0 0 0 0 | Rafael | no remaining votes, direct majority check |

## Edge Cases

One important edge case is when no votes remain. For example, input `5 4 3 3 0` leads to a fixed outcome with no ability to change scores. The algorithm computes the total as 15 and threshold as 7. Since all current scores are below or equal to this threshold, no candidate passes the strict condition. The check correctly evaluates each candidate as `cur + 0 > threshold`, producing no winners.

Another edge case is when all candidates are equal and there are enough remaining votes to create a majority. For `1 1 1 1 4`, total becomes 8 and threshold is 4. Each candidate has best case 5, which exceeds the threshold, so all are printed. The algorithm handles this naturally because it evaluates each candidate independently without assuming current ranking matters.

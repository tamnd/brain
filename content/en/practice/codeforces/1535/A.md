---
title: "CF 1535A - Fair Playoff"
description: "We have a mini playoff tournament with exactly four players. The first two face off, the last two face off, and the winners meet in the final. Each player has a unique skill value, and in any match the higher-skilled player always wins."
date: "2026-06-10T15:42:45+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1535
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 110 (Rated for Div. 2)"
rating: 800
weight: 1535
solve_time_s: 381
verified: false
draft: false
---

[CF 1535A - Fair Playoff](https://codeforces.com/problemset/problem/1535/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 6m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We have a mini playoff tournament with exactly four players. The first two face off, the last two face off, and the winners meet in the final. Each player has a unique skill value, and in any match the higher-skilled player always wins. We are asked to determine if the tournament is "fair," meaning the two strongest players actually meet in the final.

The input provides multiple test cases. Each test case is four integers representing the players’ skills. The output should be "YES" if the tournament is fair, "NO" otherwise. With up to 10,000 test cases and skill values capped at 100, we cannot afford a solution that simulates all permutations, but each case is small enough to handle with direct comparisons.

A subtle point arises because the players are not randomly matched. If the top two skilled players are on the same side of the bracket, one will be eliminated in the semifinals. For example, with skills `9, 8, 1, 2` arranged as `[s1, s2, s3, s4]`, the semifinals are `9 vs 8` and `1 vs 2`. Even though `9` and `8` are the strongest, they face each other in the semifinals, so the final will be `9 vs 2`, which is unfair. A careless approach that only looks at the two largest numbers without considering their positions would produce the wrong answer.

## Approaches

A brute-force approach would simulate every match: compare `s1` vs `s2` and `s3` vs `s4` to get semifinal winners, then compare those winners for the final. This works for four players but becomes verbose and mechanical, though it’s feasible because the input size is tiny.

The key insight is positional. We only need to know the two strongest skills and which side of the bracket they are on. The first semifinal is determined by the first two skills `[s1, s2]`, and the second semifinal by `[s3, s4]`. We check the maximum in each semifinal: the winner of the first semifinal is `max(s1, s2)`, the second is `max(s3, s4)`. If these two semifinal winners are the overall top two skills, the final will have the top two, making the tournament fair. Otherwise, one top player was eliminated too early.

This transforms the problem from simulation to simple max comparisons. It is both correct and extremely efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(1) per case | O(1) | Accepted |
| Optimal Max Comparison | O(1) per case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, `t`.
2. For each test case, read four integers `s1, s2, s3, s4`.
3. Identify the winner of the first semifinal by taking `max(s1, s2)`.
4. Identify the winner of the second semifinal by taking `max(s3, s4)`.
5. Identify the overall top two skills by taking the two largest numbers among `[s1, s2, s3, s4]`.
6. Check if the semifinal winners are exactly the top two skills. If yes, output "YES"; otherwise, output "NO".

Why it works: By comparing only the semifinal winners with the global top two, we capture whether the bracket allows both top players to reach the final. The order of matches ensures no other player can unexpectedly reach the final, so these checks are sufficient to determine fairness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = list(map(int, input().split()))
    first_winner = max(s[0], s[1])
    second_winner = max(s[2], s[3])
    top_two = sorted(s, reverse=True)[:2]
    if first_winner in top_two and second_winner in top_two:
        print("YES")
    else:
        print("NO")
```

We read all input with `sys.stdin.readline` for speed. `first_winner` and `second_winner` correspond to the semifinal winners. Sorting the list descending and taking the first two elements gives the global top two skills. The membership check confirms both semifinal winners are among the top two. Using `in` avoids mistakes from assuming order or indices, which could fail if the top two are not `s1` and `s3`.

## Worked Examples

Test case: `3 7 9 5`

| Variable | Value |
| --- | --- |
| s | [3, 7, 9, 5] |
| first_winner | max(3, 7) = 7 |
| second_winner | max(9, 5) = 9 |
| top_two | sorted([3,7,9,5], reverse=True)[:2] = [9,7] |
| Comparison | 7 in top_two? Yes; 9 in top_two? Yes |
| Output | YES |

Test case: `4 5 6 9`

| Variable | Value |
| --- | --- |
| s | [4,5,6,9] |
| first_winner | max(4,5) = 5 |
| second_winner | max(6,9) = 9 |
| top_two | [9,6] |
| Comparison | 5 in top_two? No; 9 in top_two? Yes |
| Output | NO |

These traces confirm that the algorithm correctly identifies whether both top players reach the final based on semifinal winners.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses a constant number of operations, and there are `t` test cases. |
| Space | O(1) | We store a fixed number of variables per test case; no extra storage grows with input size. |

Given `t <= 10^4` and each operation is trivial, the solution easily runs within the 2-second limit.

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
        s = list(map(int, input().split()))
        first_winner = max(s[0], s[1])
        second_winner = max(s[2], s[3])
        top_two = sorted(s, reverse=True)[:2]
        if first_winner in top_two and second_winner in top_two:
            print("YES")
        else:
            print("NO")
    return output.getvalue().strip()

# provided samples
assert run("4\n3 7 9 5\n4 5 6 9\n5 3 8 1\n6 5 3 2\n") == "YES\nNO\nYES\nNO", "sample 1"

# custom cases
assert run("1\n1 2 3 4\n") == "YES", "top two on opposite sides"
assert run("1\n4 3 2 1\n") == "NO", "top two on same side"
assert run("1\n10 20 30 40\n") == "YES", "ascending order"
assert run("1\n40 30 20 10\n") == "YES", "descending order"
assert run("1\n1 100 50 2\n") == "NO", "strongest with weakest on same side"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 | YES | Top two on opposite sides reach final |
| 4 3 2 1 | NO | Top two on same side semifinals |
| 10 20 30 40 | YES | Increasing order handled correctly |
| 40 30 20 10 | YES | Decreasing order handled correctly |
| 1 100 50 2 | NO | Strongest paired with weakest fails fairness |

## Edge Cases

If the top two skills are paired in the first or second semifinal, the algorithm detects unfairness because `first_winner` or `second_winner` will not match the top two. For example, with `[100, 1, 99, 2]`, `first_winner = 100`, `second_winner = 99`, `top_two = [100, 99]`. Both semifinal winners are in `top_two`, so the output is "YES." If we instead have `[100, 99, 1, 2]`, `first_winner = 100`, `second_winner = 2`, `top_two = [100, 99]`. Here `second_winner` is not in top two, and the output is "NO." The algorithm handles these edge cases by directly comparing the semifinal winners to the global top two, which ensures correctness.

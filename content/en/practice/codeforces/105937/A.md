---
title: "CF 105937A - Card Master"
description: "We are given a single round of a very simple card game where exactly three cards are drawn. Each card has an integer value between 1 and 13. The score for the round is normally just the sum of the three values."
date: "2026-06-22T15:45:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105937
codeforces_index: "A"
codeforces_contest_name: "2025 Xian Jiaotong University Programming Contest"
rating: 0
weight: 105937
solve_time_s: 54
verified: true
draft: false
---

[CF 105937A - Card Master](https://codeforces.com/problemset/problem/105937/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single round of a very simple card game where exactly three cards are drawn. Each card has an integer value between 1 and 13. The score for the round is normally just the sum of the three values. However, there is one special rule: if all three cards show the same value, the player has a “triple match” condition, and the final score is increased by an additional 100 points.

So the task is purely to compute a modified sum of three integers with a conditional bonus based on whether all three inputs are identical.

The constraints are tiny, since we only read three numbers in a single test case. This immediately rules out any need for data structures or optimization concerns. Even a straightforward conditional check after computing the sum is sufficient.

There are no hidden edge cases involving ordering or multiple test cases. The only meaningful corner is when all values are equal, including the smallest possible case like 1 1 1 or the largest like 13 13 13. Another trivial boundary is when two values match but the third differs, for example 5 5 6, where no bonus should be applied even though there is partial repetition.

A naive mistake here would be to incorrectly apply the bonus whenever any two cards match, instead of requiring all three to match exactly.

## Approaches

The brute-force perspective is to interpret the rules literally: compute the sum of all three cards, then check whether the three values are equal. If they are, add the bonus.

There is no real combinatorial explosion or search space here, because the input size is constant. Even if we imagined generalizing this to more cards, the structure would still be a single pass equality check over the collection.

The key observation is that the scoring rule separates into two independent parts: an additive component (the sum) and a conditional indicator (all equal). The sum is always linear in the number of cards, and the equality condition reduces to checking whether a1 equals a2 and a2 equals a3.

So the solution is just one pass of arithmetic and comparisons, making it effectively O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (direct simulation) | O(1) | O(1) | Accepted |
| Optimal (sum + equality check) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three integers a1, a2, and a3 from input. These represent the values of the drawn cards.
2. Compute the base score by summing them: s = a1 + a2 + a3. This reflects the normal scoring rule without any bonus.
3. Check whether all three values are identical by verifying a1 == a2 and a2 == a3. This two-comparison chain is sufficient because equality is transitive.
4. If the condition holds, increase the score by 100. Otherwise, leave it unchanged.
5. Output the final score.

### Why it works

The scoring function is defined as a linear sum plus a binary indicator function that depends only on whether all three inputs are equal. The equality check exactly captures the definition of a “bomb” configuration, and the sum is independent of ordering or repetition structure. Since there are no other interactions between cards, combining these two computations produces the exact required score without omissions or double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

a1, a2, a3 = map(int, input().split())

score = a1 + a2 + a3

if a1 == a2 == a3:
    score += 100

print(score)
```

The solution reads the three integers in a single line and computes their sum directly. The chained comparison `a1 == a2 == a3` is the most concise and correct way to verify that all three values are identical.

The conditional addition of 100 is only triggered in the “all equal” case, matching the definition of a bomb. No further logic is required since there are no additional rules or interactions.

## Worked Examples

### Example 1: `6 6 6`

| Step | a1 | a2 | a3 | Sum | Equal Check | Score |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 6 | 6 | 6 | 0 | - | 0 |
| After sum | 6 | 6 | 6 | 18 | - | 18 |
| Check | 6 | 6 | 6 | 18 | True | 118 |

This case triggers the bonus because all three values match exactly. The final result confirms that the rule adds 100 to the normal sum.

### Example 2: `1 1 4`

| Step | a1 | a2 | a3 | Sum | Equal Check | Score |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 1 | 1 | 4 | 0 | - | 0 |
| After sum | 1 | 1 | 4 | 6 | - | 6 |
| Check | 1 | 1 | 4 | 6 | False | 6 |

Here, two cards match but the third differs, so the bonus is not applied. This confirms that partial equality is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations and comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The constraints involve exactly three integers, so the solution is trivially within both time and memory limits. Even in a high-volume test environment, this computation is constant-time per test.

## Test Cases

```python
import sys, io

def solve():
    a1, a2, a3 = map(int, input().split())
    score = a1 + a2 + a3
    if a1 == a2 == a3:
        score += 100
    print(score)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = old_stdin
    return out.getvalue().strip()

# provided samples
assert run("6 6 6") == "118"
assert run("1 1 4") == "6"

# custom cases
assert run("1 2 3") == "6"
assert run("13 13 13") == "139"
assert run("5 5 6") == "16"
assert run("1 2 2") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 | 6 | No equality, no bonus |
| 13 13 13 | 139 | Maximum values with bonus |
| 5 5 6 | 16 | Partial match does not trigger bonus |
| 1 2 2 | 5 | Mixed ordering, still no bonus |

## Edge Cases

The only meaningful edge case is distinguishing full equality from partial equality. For input `5 5 6`, the algorithm computes sum 16 and correctly skips the bonus because `a1 == a2` is true but `a2 == a3` is false, so the chained equality fails.

For `1 1 1`, the condition `a1 == a2 == a3` evaluates to true, so the algorithm adds 100 to the base sum 3, producing 103. This directly matches the “bomb” rule.

For `13 13 13`, the same logic applies at the upper boundary, producing 39 + 100 = 139. The comparison logic is unaffected by value magnitude, confirming correctness across the full input range.

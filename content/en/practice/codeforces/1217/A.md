---
title: "CF 1217A - Creating a Character"
description: "We are given a character with two base attributes: strength and intelligence. We are also given a pool of extra experience points that must all be distributed. Each point can increase either strength or intelligence by exactly one unit."
date: "2026-06-15T18:52:51+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 1217
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 72 (Rated for Div. 2)"
rating: 1300
weight: 1217
solve_time_s: 330
verified: true
draft: false
---

[CF 1217A - Creating a Character](https://codeforces.com/problemset/problem/1217/A)

**Rating:** 1300  
**Tags:** binary search, math  
**Solve time:** 5m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a character with two base attributes: strength and intelligence. We are also given a pool of extra experience points that must all be distributed. Each point can increase either strength or intelligence by exactly one unit. After distributing all points, we obtain a final pair of values.

The task is not to compute a single optimal build but to count how many different final configurations are valid under a constraint: after spending all experience points, the resulting strength must be strictly greater than the resulting intelligence. Two configurations are considered different if either final strength or final intelligence differs.

The key structure is that every valid outcome is fully determined by how many points we assign to strength. Once that is fixed, intelligence is determined automatically because all points must be used.

The constraints go up to 10^8 for all parameters, with up to 100 test cases. This immediately rules out any approach that tries all distributions explicitly, since even iterating over exp per test case could already reach 10^10 operations in the worst case. The solution must be O(1) per query.

A subtle edge case appears when no distribution is valid. This happens when intelligence starts too large relative to strength, so even putting all experience into strength does not make strength strictly greater. Another boundary case is when exp is zero, where there is exactly one possible build, and it is valid only if the initial inequality already holds.

## Approaches

A direct approach would try every possible split of experience points. If we assign x points to strength and exp - x to intelligence, then final values become:

strength = str + x

intelligence = int + (exp - x)

We could iterate x from 0 to exp and check the inequality for each case. This is correct because it enumerates all possible distributions, but it is linear in exp. With exp up to 10^8, this becomes completely infeasible.

The key observation is that the inequality constraint can be rewritten into a linear inequality in x. This turns the problem into counting integer solutions in a bounded interval. Once we do that, we only need to find the range of x that satisfies the constraint, then count how many integers lie in it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(exp) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We let x denote how many experience points are assigned to strength. Then intelligence gets exp - x points.

1. Express final attributes as equations:

strength = str + x, intelligence = int + exp - x.
2. Translate the condition strength > intelligence into an inequality:

str + x > int + exp - x.
3. Rearrange everything involving x on one side:

2x > int + exp - str.
4. Solve for x as an integer lower bound:

x > (int + exp - str) / 2.
5. Convert strict inequality into smallest integer x:

x_min = floor((int + exp - str) / 2) + 1.
6. Enforce feasibility constraints coming from how x is defined:

0 ≤ x ≤ exp.
7. The number of valid builds is the size of the interval [x_min, exp], if it exists.

Why it works: every valid build corresponds to exactly one integer x in [0, exp]. The inequality reduces to a single linear constraint, so the valid set of builds becomes a contiguous interval of integers. Counting solutions becomes counting integer points in that interval, and no two different x values produce the same (strength, intelligence) pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []
    
    for _ in range(T):
        str_val, int_val, exp = map(int, input().split())
        
        # Solve inequality:
        # str + x > int + (exp - x)
        # 2x > int + exp - str
        
        rhs = int_val + exp - str_val
        
        # minimal integer x satisfying strict inequality
        # x > rhs / 2
        x_min = rhs // 2 + 1
        
        if x_min < 0:
            x_min = 0
        
        if x_min > exp:
            out.append("0")
        else:
            out.append(str(exp - x_min + 1))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core of the implementation is computing the minimum valid value of x. The inequality produces a strict half-bound, so we convert it carefully using integer division. Because Python floors toward negative infinity, using `rhs // 2 + 1` correctly handles both positive and negative rhs cases.

After computing `x_min`, we clamp it to the valid domain [0, exp]. If it exceeds exp, no valid configuration exists. Otherwise, every integer from x_min through exp corresponds to one valid build, so we count them directly.

## Worked Examples

### Example 1

Input:

```
str = 5, int = 3, exp = 4
```

We compute rhs = 3 + 4 - 5 = 2.

| x | strength | intelligence | valid? |
| --- | --- | --- | --- |
| 0 | 5 | 7 | no |
| 1 | 6 | 6 | no |
| 2 | 7 | 5 | yes |
| 3 | 8 | 4 | yes |
| 4 | 9 | 3 | yes |

Valid x values are 2, 3, 4, giving 3 configurations.

This confirms that valid solutions form a contiguous suffix of the range.

### Example 2

Input:

```
str = 2, int = 1, exp = 0
```

rhs = 1 + 0 - 2 = -1, so inequality is already satisfied.

| x | strength | intelligence | valid? |
| --- | --- | --- | --- |
| 0 | 2 | 1 | yes |

Only one configuration exists, matching the fact that exp forces x = 0.

This shows that the algorithm correctly handles the zero-experience boundary case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case is solved using constant-time arithmetic |
| Space | O(1) | Only a few integer variables are stored |

The constraints allow up to 100 test cases with values up to 10^8, so a constant-time per query solution is sufficient and necessary.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    res = []
    for _ in range(T):
        a, b, c = map(int, input().split())
        rhs = b + c - a
        x_min = rhs // 2 + 1
        if x_min < 0:
            x_min = 0
        if x_min > c:
            res.append("0")
        else:
            res.append(str(c - x_min + 1))
    return "\n".join(res)

# provided samples
assert run("""4
5 3 4
2 1 0
3 5 5
4 10 6
""") == """3
1
2
0"""

# minimum exp
assert run("""1
5 1 0
""") == "1"

# no valid configuration
assert run("""1
1 10 0
""") == "0"

# all allocations valid
assert run("""1
10 1 5
""") == "6"

# boundary equality case
assert run("""1
5 3 0
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample set | given | correctness on mixed cases |
| 5 1 0 | 1 | exp = 0 boundary |
| 1 10 0 | 0 | impossible inequality |
| 10 1 5 | 6 | all x in full range valid |
| 5 3 0 | 1 | equality handling with no flexibility |

## Edge Cases

When exp is zero, x is forced to be zero. The algorithm sets x_min based on the inequality and then clamps it into [0, exp]. If the constraint allows x = 0, exactly one build is counted; otherwise, x_min exceeds exp and the answer becomes zero.

When intelligence is much larger than strength, rhs becomes large and positive, pushing x_min beyond exp. In that case, the interval [x_min, exp] is empty, and the algorithm correctly returns zero without iteration.

When strength is already large, rhs becomes negative, and x_min evaluates to a negative number. Clamping it to zero ensures we count all possible allocations, matching the fact that every split maintains strength dominance.

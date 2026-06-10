---
title: "CF 1462C - Unique Number"
description: "We are given a target sum of digits, and we must construct the smallest positive integer whose digits are all different and whose digits add up exactly to that target. The output is not just any valid number, but the smallest one in standard decimal ordering."
date: "2026-06-11T02:11:03+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1462
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 690 (Div. 3)"
rating: 900
weight: 1462
solve_time_s: 317
verified: false
draft: false
---

[CF 1462C - Unique Number](https://codeforces.com/problemset/problem/1462/C)

**Rating:** 900  
**Tags:** brute force, greedy, math  
**Solve time:** 5m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a target sum of digits, and we must construct the smallest positive integer whose digits are all different and whose digits add up exactly to that target.

The output is not just any valid number, but the smallest one in standard decimal ordering. That means we are effectively choosing a set of distinct digits, deciding their arrangement, and forming the lexicographically smallest number possible from them.

The key constraint is that digits must be unique. Since digits range only from 0 to 9, we can never use more than 10 distinct digits, and more importantly, the maximum achievable sum using distinct digits is fixed. The largest possible set is all digits 0 through 9, whose sum is 45. Any input larger than 45 is immediately impossible.

This creates a very tight search space: at most 10 digits, with a bounded sum.

A subtle edge case arises from the presence of zero. Zero contributes nothing to the sum but affects ordering. For example, using digit 0 is allowed, but it must not appear as the leading digit in the final number. A naive approach that sorts chosen digits without handling leading zero properly can accidentally produce invalid minimal representations.

Another edge case is small sums like 1 or 2, where greedy selection behaves differently depending on ordering strategy. For instance, choosing digits from smallest upward is not optimal if we are trying to minimize lexicographic value while satisfying a sum constraint.

## Approaches

A brute-force idea would be to try all subsets of digits from 1 to 9 (and optionally 0), check their sums, and then generate all permutations to find the smallest valid number. This is correct in principle because the search space is finite: there are at most $2^{10} = 1024$ subsets and at most 10! permutations per subset. However, this still leads to millions of candidate numbers in the worst case, which is unnecessary given the structure of the problem.

The key observation is that we want a subset of distinct digits whose sum is exactly $x$, and we want the resulting number to be as small as possible. To minimize the resulting number, we want smaller digits to appear as early as possible. However, smaller digits also reduce the total sum more slowly, which is the opposite of what we want when we need to reach a fixed target sum efficiently.

This creates a classic greedy tension: to reach a sum quickly while using distinct digits, we should prefer large digits first. But to minimize the final number, we should later arrange them in increasing order.

So the correct strategy is to select digits greedily from 9 down to 1, always taking a digit if it does not exceed the remaining sum. This ensures we use as few digits as possible and prioritize larger contributions early. After selecting the set, we sort it in increasing order to construct the smallest possible number.

Digit 0 is never useful for the sum itself, but it may be included if needed and will always be placed after all nonzero digits in sorted order, which naturally keeps it from becoming a leading digit unless it is the only digit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets and permutations | O(10! · 2^10) | O(1) | Too slow |
| Greedy selection + sorting | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check if the target sum $x$ is greater than 45. If so, output -1 immediately because even using all digits 0 through 9 cannot reach that sum. This removes impossible cases before any construction.
2. Initialize an empty list to store chosen digits and set a variable `rem = x` representing the remaining sum we still need to achieve.
3. Iterate digits from 9 down to 1. At each digit `d`, check if `d <= rem`. If it is, include `d` in the answer set and subtract `d` from `rem`. We skip 0 here because it does not help reduce the remaining sum.
4. After the loop, if `rem` is not zero, output -1. This means we cannot exactly represent the sum using distinct digits from 1 to 9.
5. Otherwise, sort the selected digits in increasing order and concatenate them to form the final number. Sorting is necessary because we want the smallest possible integer, and placing smaller digits earlier always reduces the numeric value.

### Why it works

The greedy selection from 9 downward ensures that we use the fewest digits possible, since larger digits reduce the remaining sum more aggressively. Because we never reuse digits, the construction is equivalent to choosing a subset of {1..9} whose sum is exactly x. Among all such subsets, any valid solution differs only in digit order, and sorting those digits increasingly always yields the smallest possible integer. Therefore, the algorithm separates the problem into subset selection (greedy optimal for feasibility) and ordering (sorted minimal representation), guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(x):
    if x > 45:
        return "-1"
    
    rem = x
    chosen = []
    
    for d in range(9, 0, -1):
        if d <= rem:
            chosen.append(d)
            rem -= d
    
    if rem != 0:
        return "-1"
    
    chosen.sort()
    return "".join(map(str, chosen))

t = int(input())
out = []
for _ in range(t):
    x = int(input())
    out.append(solve(x))

print("\n".join(out))
```

The implementation directly follows the greedy construction. The feasibility check `x > 45` avoids unnecessary work. The backward loop from 9 to 1 ensures we prioritize large digits, which minimizes the number of chosen elements. Sorting at the end is essential, since greedy selection alone does not guarantee minimal numeric order.

A common implementation mistake is to sort digits before selection or to iterate upward from 1, which tends to produce many small digits and may fail to reach the sum even when a solution exists.

## Worked Examples

### Example 1: x = 15

We track remaining sum and chosen digits.

| Step | Digit | Remaining before | Take digit | Remaining after | Chosen |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | 15 | yes | 6 | [9] |
| 2 | 8 | 6 | no | 6 | [9] |
| 3 | 7 | 6 | no | 6 | [9] |
| 4 | 6 | 6 | yes | 0 | [9, 6] |
| 5-9 | 5..1 | 0 | no | 0 | [9, 6] |

Sorting gives [6, 9], so output is 69.

This demonstrates that greedy selection finds a valid subset, and sorting ensures minimal numeric value.

### Example 2: x = 5

| Step | Digit | Remaining before | Take digit | Remaining after | Chosen |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | 5 | no | 5 | [] |
| 2 | 8 | 5 | no | 5 | [] |
| 3 | 7 | 5 | no | 5 | [] |
| 4 | 6 | 5 | no | 5 | [] |
| 5 | 5 | 5 | yes | 0 | [5] |
| 6-9 | 4..1 | 0 | no | 0 | [5] |

Result is 5.

This shows that when a single digit exactly matches the target, the algorithm naturally picks it, confirming that no unnecessary digits are introduced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only 9 iterations per test case plus constant sorting of at most 9 digits |
| Space | O(1) | Fixed-size digit array bounded by 9 elements |

The constraints allow up to 50 test cases, but each one runs in constant time due to the fixed digit range. The solution is comfortably within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve(x):
        if x > 45:
            return "-1"
        rem = x
        chosen = []
        for d in range(9, 0, -1):
            if d <= rem:
                chosen.append(d)
                rem -= d
        if rem != 0:
            return "-1"
        chosen.sort()
        return "".join(map(str, chosen))

    t = int(input())
    out = []
    for _ in range(t):
        x = int(input())
        out.append(solve(x))
    return "\n".join(out)

# provided samples
assert run("4\n1\n5\n15\n50\n") == "1\n5\n69\n-1"

# custom cases
assert run("1\n9\n") == "9", "single digit max"
assert run("1\n10\n") == "19", "smallest two-digit distinct sum"
assert run("1\n45\n") == "123456789", "all digits used"
assert run("1\n46\n") == "-1", "impossible maximum + 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 9 | 9 | single digit exact match |
| 10 | 19 | greedy split into smallest valid pair |
| 45 | 123456789 | full digit usage case |
| 46 | -1 | boundary infeasibility |

## Edge Cases

One important edge case is when the sum equals 45. The algorithm selects digits 9 down to 1, consuming all available digits exactly once. Sorting produces 123456789, which is the smallest possible permutation of all digits.

Another edge case is when the sum is slightly above a reachable subset boundary, such as 8 or 10. For x = 10, the greedy process skips 9 and 8, selects 7 (too large to fit), then eventually picks 9? actually it cannot, so it selects 9 is skipped, 8 skipped, 7 skipped, 6 skipped, 5 skipped, 4 skipped, 3 skipped, 2 skipped, then 1 and 9 cannot complete, so it picks 9? no, it does not fit. The final selection becomes [9? invalid], rem remains nonzero, so output is -1. This demonstrates that greedy selection is not just about picking until exhaustion; feasibility must be verified via remaining sum.

A final subtle case is x = 1. The algorithm directly selects digit 1 and produces a single-digit output. Any attempt to include 0 would be harmful because it cannot help satisfy the sum and could incorrectly affect ordering if mishandled.

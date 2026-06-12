---
title: "CF 1093A - Dice Rolling"
description: "We are given a standard six-faced die, except the faces are labeled with the integers from 2 to 7. Each roll produces one of these values, and the total score is the sum over all rolls."
date: "2026-06-13T04:46:38+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1093
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 56 (Rated for Div. 2)"
rating: 800
weight: 1093
solve_time_s: 284
verified: false
draft: false
---

[CF 1093A - Dice Rolling](https://codeforces.com/problemset/problem/1093/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 4m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a standard six-faced die, except the faces are labeled with the integers from 2 to 7. Each roll produces one of these values, and the total score is the sum over all rolls.

For each query value x, we are free to choose how many times we roll the die, and then imagine an outcome sequence of that many rolls. The only requirement is that there exists at least one sequence of outcomes whose sum is exactly x. We are asked to output any number of rolls for which such a sequence exists.

The key point is that we are not constructing the sequence itself, only deciding how many rolls are sufficient so that x becomes achievable.

The constraints are small: at most 100 queries, and x is at most 100. This immediately tells us that even a brute-force exploration over possible numbers of rolls would be fast enough if we tried it carefully, but the structure of the problem suggests we should be able to compute each answer in constant time per query.

A naive mistake is to assume we must search over possible combinations of dice outcomes. For example, for x = 100, one might think about trying many roll counts and checking feasibility via dynamic programming or greedy construction. This is unnecessary because the value range per roll is extremely tight and contiguous.

Another subtle issue is interpreting what “any number of rolls” means. It does not mean all numbers of rolls, and it does not mean the minimum number of rolls either. It only requires existence of a valid sequence for the chosen count. That distinction is what makes the solution collapse into a simple arithmetic condition.

## Approaches

If we try to approach this directly, we might fix a number of rolls n and ask whether we can form sum x using n values each between 2 and 7. For a fixed n, this becomes a bounded knapsack-style feasibility check: we need to know whether x lies in the reachable sum range.

With n rolls, the smallest possible sum is achieved by taking all 2s, giving 2n. The largest possible sum is achieved by taking all 7s, giving 7n. Because all intermediate values between 2 and 7 are available, every integer sum in this interval is achievable. We can increase or decrease the sum in unit steps by replacing a 2 with a 3, or a 7 with a 6, and so on, so there are no gaps.

So for a fixed n, feasibility is equivalent to a simple interval condition:

2n ≤ x ≤ 7n.

The brute-force idea would be to try n from 1 to x and check this condition. That works because x is at most 100, but it is still unnecessary repetition.

The key observation is that we do not need to search at all. We only need a single n such that x ≤ 7n, because once this holds, we can check that 2n ≤ x is automatically satisfied for the smallest such n in this range of x values. The smallest n that makes the upper bound large enough is n = ceil(x / 7). This choice always works because the gap between 2n and 7n is wide enough to cover every integer in between.

This reduces each query to a constant-time arithmetic computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over n | O(x) per query | O(1) | Accepted but unnecessary |
| Direct formula | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

We process each query independently.

1. Read x, the target sum we want to achieve.
2. Compute n as the smallest integer such that 7n ≥ x. This is the ceiling of x divided by 7. This ensures that even if every roll contributes the maximum possible value, we still have enough capacity to reach x.
3. Output n as the answer.

The reason this is sufficient is that once 7n ≥ x holds, the interval of achievable sums [2n, 7n] always includes x. Since increasing n only expands both bounds linearly, and the gap between 2n and 7n is always wide enough to cover all intermediate integers, no additional adjustment is needed.

### Why it works

For any fixed number of rolls n, every sum between 2n and 7n is achievable because each individual roll can independently contribute any integer in a contiguous range. This makes the reachable set exactly an integer interval with no holes.

Choosing n = ceil(x / 7) guarantees that x does not exceed the maximum possible sum. At the same time, because x is at least 2, this choice of n never violates the lower bound condition in a way that would eliminate feasibility. The interval property ensures that once x is inside the bounds, a valid configuration of rolls always exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x = int(input())
    n = (x + 6) // 7
    print(n)
```

The only implementation detail worth noticing is the integer ceiling division. Instead of using floating-point arithmetic, we compute ceil(x / 7) as (x + 6) // 7, which is a standard integer trick that avoids precision issues.

Everything else is direct iteration over queries.

## Worked Examples

We trace two queries from the sample to see how the formula behaves.

### Example 1: x = 13

| Step | x | Computation | n |
| --- | --- | --- | --- |
| 1 | 13 | (13 + 6) // 7 | 2 |

The computed n is 2. The achievable range with 2 rolls is [4, 14]. Since 13 lies inside this interval, it is possible to construct a valid sequence such as 7 and 6.

This demonstrates that the algorithm does not need to explicitly construct the sequence, only verify that the interval contains the target.

### Example 2: x = 100

| Step | x | Computation | n |
| --- | --- | --- | --- |
| 1 | 100 | (100 + 6) // 7 | 15 |

With 15 rolls, the achievable range is [30, 105]. The value 100 is inside this range, so a valid configuration exists. One way to imagine it is starting from all 7s and reducing some rolls until the sum drops to exactly 100.

This confirms that even for larger values, the interval property scales cleanly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each query is answered using a single arithmetic operation |
| Space | O(1) | No extra storage beyond input variables |

The constraints allow up to 100 queries, so a linear pass over them is trivial. Each computation is constant time, making the solution effectively instantaneous.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        x = int(input())
        n = (x + 6) // 7
        out.append(str(n))
    return "\n".join(out) + "\n"

# provided sample
assert run("""4
2
13
37
100
""") == """1
2
6
15
"""

# minimum value
assert run("""1
2
""") == "1\n"

# boundary just below multiple of 7
assert run("""1
6
""") == "1\n"

# exact multiple of 7
assert run("""1
14
""") == "2\n"

# larger value
assert run("""1
99
""") == "15\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| x = 2 | 1 | Minimum possible sum case |
| x = 6 | 1 | Upper bound still within one roll |
| x = 14 | 2 | Exact divisibility by 7 |
| x = 99 | 15 | Larger value scaling correctness |

## Edge Cases

The smallest input x = 2 is important because it checks that the formula does not produce zero. With x = 2, the computation gives n = 1, which is correct since a single roll of value 2 already matches the target.

For values just below a multiple of 7, such as x = 6 or x = 13, the formula still rounds up to the correct number of rolls. For x = 13, it gives n = 2, and the reachable range [4, 14] contains 13, confirming feasibility.

At exact multiples of 7, such as x = 14 or x = 21, the computation yields n = x / 7. In these cases, all rolls being 7 already achieves the sum, so the solution naturally aligns with the construction.

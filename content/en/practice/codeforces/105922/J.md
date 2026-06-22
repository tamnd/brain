---
title: "CF 105922J - Odd-Even Game"
description: "We are given two integers, and we are told a strict structural property about them: one of them is guaranteed to be odd and the other is guaranteed to be even. Each number represents a “player’s choice” in a very simple comparison game."
date: "2026-06-22T15:31:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105922
codeforces_index: "J"
codeforces_contest_name: "The 18th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 105922
solve_time_s: 53
verified: true
draft: false
---

[CF 105922J - Odd-Even Game](https://codeforces.com/problemset/problem/105922/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, and we are told a strict structural property about them: one of them is guaranteed to be odd and the other is guaranteed to be even. Each number represents a “player’s choice” in a very simple comparison game. One player prefers odd numbers, the other prefers even numbers, but the only thing that ultimately matters is the numeric comparison between the two values.

The task is to output which of the two numbers is larger, but the output is not the number itself. Instead, we output `1` if the larger number happens to be the odd one, and `2` if the larger number happens to be the even one.

The constraints are extremely small in algorithmic terms: values go up to 10^9, which easily fits in standard integer types. More importantly, there are only two values and no hidden structure like arrays, graphs, or multiple queries. This immediately rules out any need for preprocessing, data structures, or asymptotically efficient algorithms. Any solution that directly compares the two numbers runs in constant time.

There are no tricky hidden edge cases in terms of size, but there is a conceptual pitfall: the output is tied to parity, not to position. A naive reader might incorrectly assume “print 1 if a > b”, but that would ignore whether the larger number is odd or even, which is essential to the mapping of the answer.

A small example shows the structure clearly. If the input is `3 2`, the odd number is larger, so the output is `1`. If the input is `1 2`, the even number is larger, so the output is `2`. The confusion arises only if one forgets that parity determines which label to print, not which number is printed.

## Approaches

A brute-force interpretation would still look identical to the optimal one because there is nothing to iterate over. One might imagine “testing” both possibilities, but since there are only two numbers, any simulation or enumeration degenerates into a single comparison followed by a classification step. Even if we artificially framed it as checking conditions for both numbers, the work remains O(1).

The key observation is that the problem does not require constructing anything, only deciding which of the two candidates is both larger and has a known parity. Since exactly one number is odd and the other is even, we can safely identify parity using a modulus operation and then compare values directly.

The brute-force idea “try both and decide” collapses into the insight that the answer is determined by two facts: which number is greater, and whether that number is odd or even. Once we recognize that both facts can be computed in constant time, the problem becomes a direct conditional check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers `a` and `b`. These are the only inputs needed to determine the result.
2. Check which of the two numbers is larger. This determines which candidate is “winning” in the comparison sense.
3. Determine the parity of the larger number by checking whether it is divisible by 2.
4. If the larger number is odd, output `1`, because the odd-number player wins the comparison. Otherwise, output `2`, since the larger number must then be even.

The reasoning step that matters here is that parity is not used to decide ordering, only to map the winner to the required output label. Since the problem guarantees exactly one odd and one even number, there is no ambiguity in this mapping.

### Why it works

At all times, exactly one number is odd and the other is even, so the identity of the odd number is well-defined. The algorithm compares magnitudes independently of parity, ensuring the correct winner is selected. Once the larger value is identified, the parity check uniquely determines whether that winner corresponds to the odd or even player. Since both steps are deterministic and cover all possible valid inputs, the output must match the required rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = map(int, input().split())

mx = a if a > b else b

if mx % 2 == 1:
    print(1)
else:
    print(2)
```

The implementation is intentionally minimal because the structure of the problem does not require loops or auxiliary data structures. The first step reads the two integers directly. The second step selects the larger value using a simple conditional expression, which is sufficient because there are only two candidates.

The parity check `mx % 2 == 1` identifies whether the maximum is odd. Since the problem guarantees exactly one odd number and one even number, this automatically identifies which player’s number is being output. The final print statement maps this condition to the required output format.

A common mistake would be to check `a % 2` or `b % 2` independently without first identifying which is larger. That would lead to incorrect answers when the larger number is even but not `a`, or vice versa.

## Worked Examples

### Example 1: input `3 2`

| Step | a | b | mx | mx % 2 | Output |
| --- | --- | --- | --- | --- | --- |
| read input | 3 | 2 | - | - | - |
| compare | 3 | 2 | 3 | - | - |
| parity check | 3 | 2 | 3 | 1 | 1 |

Here the maximum is 3, which is odd, so the output is 1. This confirms that the odd-valued participant wins when they also hold the larger number.

### Example 2: input `1 2`

| Step | a | b | mx | mx % 2 | Output |
| --- | --- | --- | --- | --- | --- |
| read input | 1 | 2 | - | - | - |
| compare | 1 | 2 | 2 | - | - |
| parity check | 1 | 2 | 2 | 0 | 2 |

Here the maximum is 2, which is even, so the output is 2. This demonstrates the case where the even participant wins due to having the larger value.

These two traces cover both possible parity outcomes for the maximum value and confirm that the algorithm consistently maps the winner to the correct label.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of comparisons and arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

The constraints allow up to 10^9, but since only two integers are processed, the runtime is constant and trivially fits within any time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b = map(int, input().split())
    mx = a if a > b else b
    return str(1 if mx % 2 == 1 else 2)

# provided samples
assert run("1 2") == "2"
assert run("3 2") == "1"

# custom cases
assert run("2 1") == "2", "even larger"
assert run("5 4") == "1", "odd larger"
assert run("8 7") == "2", "even larger"
assert run("9 2") == "1", "odd larger"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 2 | even is larger and wins |
| 5 4 | 1 | odd is larger and wins |
| 8 7 | 2 | even wins in reversed order |
| 9 2 | 1 | odd wins with large gap |

## Edge Cases

The only structural edge condition is when the larger number is the even one, since it can be easy to accidentally return the parity of the wrong variable.

For input `2 1`, the algorithm computes `mx = 2`, then checks `2 % 2 == 0`, so it outputs `2`. A naive mistake would be to check `a % 2` first, see that `2` is even, and incorrectly assume output should be `2` without confirming that `a` is actually the maximum in all cases. The correct logic always anchors parity checking on the maximum value, which prevents this misclassification.

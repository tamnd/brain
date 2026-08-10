---
title: "CF 102397A - Bashar and SHAWERMA!"
description: "Bashar wants to buy exactly x shawerma sandwiches. Every sandwich costs exactly 2 JDs, so the required amount of money is the price of one sandwich multiplied by the number of sandwiches. The input contains one integer x, representing the number of sandwiches Bashar wants to buy."
date: "2026-08-10T17:51:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "A"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 255
verified: true
draft: false
---

[CF 102397A - Bashar and SHAWERMA!](https://codeforces.com/problemset/problem/102397/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

Bashar wants to buy exactly `x` shawerma sandwiches. Every sandwich costs exactly 2 JDs, so the required amount of money is the price of one sandwich multiplied by the number of sandwiches.

The input contains one integer `x`, representing the number of sandwiches Bashar wants to buy. The output should contain the total cost in JDs.

The constraint `1 <= x <= 30` makes the problem extremely small. Even a loop that performs one addition per sandwich would require at most 30 iterations, which is trivial within a 1.5 second time limit. More importantly, the fixed price of every sandwich means there is no need to inspect individual sandwiches or maintain any complicated state. The answer is determined directly from `x`.

There are no difficult boundary cases involving zero because the smallest allowed value is 1. For example, with input `1`, the correct output is `2`, since Bashar buys one sandwich. A careless solution that accidentally prints `x` would produce `1`, confusing the number of sandwiches with their total price.

At the other boundary, input `30` requires `60` JDs. A solution that performs only one multiplication by the wrong price, or accidentally treats the upper bound as 29, would produce an incorrect result. Since the answer is always exactly twice `x`, both boundaries are handled by the same formula.

## Approaches

A direct brute-force approach would start with a total cost of zero and add 2 JDs once for every sandwich. This is correct because each iteration accounts for exactly one sandwich, so after `x` iterations the accumulated amount is `2 + 2 + ... + 2`, with `x` copies of 2. At the maximum input value, this performs only 30 additions, so it is already fast enough for the given constraints.

The brute-force approach works because the input is tiny, but it is unnecessary. The key observation is that every iteration adds the same fixed amount, 2 JDs. Repeated addition of the same value `x` times is precisely multiplication by `x`. Thus the entire loop can be replaced by the expression `2 * x`.

There is no meaningful performance failure point for the brute-force method under the stated constraint, since 30 iterations is negligible. The optimal solution is still preferable because it expresses the mathematical structure directly and reduces the implementation to a single multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x), at most O(30) | O(1) | Accepted, but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `x`, the number of shawerma sandwiches Bashar wants to buy. This is the only value needed because every sandwich has the same price.
2. Multiply `x` by `2`. Each sandwich contributes exactly 2 JDs, so multiplying the number of sandwiches by the fixed price gives the total cost.
3. Print the resulting value. No rounding, division, or additional processing is necessary because the price and the number of sandwiches are both integers.

### Why it works

The total price is the sum of the price of every sandwich. Since each of the `x` sandwiches costs exactly 2 JDs, that sum is

`2 + 2 + ... + 2`

with `x` terms. By the definition of multiplication, this sum equals `2 * x`. The algorithm computes exactly this value, so the printed answer is always the required total cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

x = int(input())
print(2 * x)
```

The first line imports `sys`, and `input` is assigned to `sys.stdin.readline` as the standard fast-input pattern for competitive programming. The input consists of only one integer, so there is no need for special parsing logic.

The value read into `x` represents the number of sandwiches. The expression `2 * x` directly implements the mathematical formula for the total cost.

There are no off-by-one issues because the calculation does not use a loop or an index. There is also no integer overflow concern in Python, and even under the given constraint the largest possible result is only `60`.

The program then prints the result followed by a newline, which is exactly the required output format.

## Worked Examples

The statement provided in the prompt does not contain actual sample input and output values, so the following two traces use concrete valid inputs.

### Example 1

Input:

```
1
```

| Step | `x` | Price per sandwich | Total cost |
| --- | --- | --- | --- |
| Read input | 1 | 2 | 0 |
| Multiply | 1 | 2 | 2 |
| Print | 1 | 2 | 2 |

The input represents one sandwich. Multiplying one sandwich by its price of 2 JDs gives an output of `2`. This also checks the smallest allowed input.

### Example 2

Input:

```
7
```

| Step | `x` | Price per sandwich | Total cost |
| --- | --- | --- | --- |
| Read input | 7 | 2 | 0 |
| Multiply | 7 | 2 | 14 |
| Print | 7 | 2 | 14 |

Seven sandwiches cost `2 * 7 = 14` JDs. The trace shows that the algorithm does not need to simulate seven separate purchases because multiplication represents the same repeated addition directly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One integer multiplication and one output operation are performed. |
| Space | O(1) | Only the input value and the computed result are stored. |

The input is limited to at most 30 sandwiches, so even the straightforward repeated-addition solution would easily fit within the 1.5 second time limit and 256 MB memory limit. The multiplication-based solution is constant time and uses constant memory, making it comfortably within both limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    input = sys.stdin.readline

    x = int(input())
    print(2 * x)

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Custom test cases based on the problem's missing sample section.
assert run("1\n") == "2\n", "minimum input"
assert run("2\n") == "4\n", "small boundary case"
assert run("15\n") == "30\n", "middle value"
assert run("30\n") == "60\n", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `2` | Minimum allowed number of sandwiches |
| `2` | `4` | Small value and basic multiplication |
| `15` | `30` | A middle-range input |
| `30` | `60` | Maximum allowed input and upper boundary |

## Edge Cases

For the minimum input, the exact input is `1`. The algorithm reads `x = 1`, computes `2 * 1 = 2`, and prints `2`. A common mistake would be to print the input directly, which would confuse the number of sandwiches with the amount of money required.

For the maximum input, the exact input is `30`. The algorithm computes `2 * 30 = 60` and prints `60`. Since the calculation has no loop boundary, there is no possibility of accidentally processing only 29 sandwiches.

The value `2` is also useful for catching a misunderstanding of the price. With input `2`, Bashar buys two sandwiches, and the required amount is `2 + 2 = 4`, so the correct output is `4`. The formula produces exactly that value.

A middle value such as `15` gives `30` JDs. This confirms that the solution is not relying on a special case for either endpoint and that the same fixed-price relationship applies throughout the entire valid input range.

---
title: "CF 105575A - \u7edf\u8ba1\u9009\u624b"
description: "The task describes a very small computation: four integers are provided as input, and the program must output their total sum. There is no additional structure, no hidden transformation, and no dependency between the numbers beyond simple addition."
date: "2026-06-22T14:23:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105575
codeforces_index: "A"
codeforces_contest_name: "Southeast University 6th Programming Competition Competition (Winter, Novice Group) \u4e1c\u5357\u5927\u5b66\u7b2c\u516d\u5c4a\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u51ac\u5b63\u8d5b\uff08\u65b0\u624b\u7ec4\uff09"
rating: 0
weight: 105575
solve_time_s: 52
verified: true
draft: false
---

[CF 105575A - \u7edf\u8ba1\u9009\u624b](https://codeforces.com/problemset/problem/105575/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a very small computation: four integers are provided as input, and the program must output their total sum. There is no additional structure, no hidden transformation, and no dependency between the numbers beyond simple addition.

You can think of the input as four independent values placed on a table, and the output is the single value obtained after aggregating them with the addition operation.

Although the problem is simple, it still implicitly assumes a few implementation concerns. The integers may be positive, negative, or zero, so the sum must be computed using a type that safely handles the full range of possible values without overflow in intermediate steps. In Python this is naturally handled, but in lower level languages like C++ it would matter whether a 32 bit or 64 bit type is used.

Edge cases are minimal here, but still worth being explicit. If all four numbers are zero, the output must be zero. If all are negative, the result must still reflect correct accumulation without sign errors. For example, input `-1 -2 -3 -4` must produce `-10`. Any implementation that mistakenly treats input parsing or arithmetic incorrectly would fail immediately even on these small cases.

## Approaches

A brute force interpretation would be to treat the numbers as elements of a collection and compute their sum using repeated addition or an explicit loop over stored values. This would typically involve reading the values into an array and iterating through it, accumulating a running total. The correctness comes directly from the associativity of addition, since summing sequentially or summing in a single expression produces the same result.

In this particular problem, the brute force and optimal approaches collapse into the same idea because the input size is fixed at four. A loop over four elements performs a constant number of operations, so there is no meaningful performance difference between iterating and writing the sum directly.

The key observation is that the structure of the problem is entirely fixed. Since the number of inputs never changes, there is no need for general-purpose data structures or algorithms. The computation reduces to a single arithmetic expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (array + loop) | O(1) | O(1) | Accepted |
| Optimal (direct sum) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read four integers from standard input. This step establishes the raw values that must be combined.
2. Compute their sum using a single arithmetic expression that adds all four values together. This avoids any overhead of iteration or storage beyond temporary variables.
3. Output the computed sum as the final result.

### Why it works

Addition over integers is associative and commutative, so grouping or ordering does not affect the final result. Since every input value is included exactly once in the expression, the computed value must equal the mathematical sum of all four inputs. No intermediate transformations alter the values, so correctness follows directly from the definition of integer addition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x1, x2, x3, x4 = map(int, input().split())
    print(x1 + x2 + x3 + x4)

if __name__ == "__main__":
    solve()
```

The solution reads exactly four integers from a single input line and binds them to variables. This avoids storing them in a list, although doing so would also be correct. The sum is computed in one expression, ensuring minimal overhead and clear intent. The program then prints the result followed by a newline.

The only subtle point is input parsing. Using `map(int, input().split())` guarantees that arbitrary whitespace separation is handled correctly, which is standard in competitive programming input formats.

## Worked Examples

### Example 1

Input:

```
1 2 3 4
```

| Step | x1 | x2 | x3 | x4 | Current Sum |
| --- | --- | --- | --- | --- | --- |
| Read values | 1 | 2 | 3 | 4 | 0 |
| Compute sum | 1 | 2 | 3 | 4 | 10 |

Output:

```
10
```

This trace shows straightforward accumulation of four positive integers. Every value contributes exactly once to the final result.

### Example 2

Input:

```
-5 10 -3 2
```

| Step | x1 | x2 | x3 | x4 | Current Sum |
| --- | --- | --- | --- | --- | --- |
| Read values | -5 | 10 | -3 | 2 | 0 |
| Compute sum | -5 | 10 | -3 | 2 | 4 |

Output:

```
4
```

This example demonstrates handling of mixed signs. The algorithm treats negative and positive numbers uniformly, confirming that no special casing is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Exactly four additions and one input operation regardless of input values |
| Space | O(1) | Only four integer variables are stored |

The fixed input size guarantees constant time and constant memory usage. Even in a constrained environment, this computation is negligible compared to input/output overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        import sys
        input = sys.stdin.readline
        x1, x2, x3, x4 = map(int, input().split())
        print(x1 + x2 + x3 + x4)
    return out.getvalue().strip()

# provided sample-style cases
assert run("1 2 3 4\n") == "10"
assert run("-5 10 -3 2\n") == "4"

# custom cases
assert run("0 0 0 0\n") == "0"
assert run("1000000000 1000000000 1000000000 1000000000\n") == "4000000000"
assert run("-1 -1 -1 -1\n") == "-4"
assert run("7 0 -7 3\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 | 0 | all zeros |
| 1000000000 1000000000 1000000000 1000000000 | 4000000000 | large values and overflow safety |
| -1 -1 -1 -1 | -4 | all negative values |
| 7 0 -7 3 | 3 | cancellation and mixed signs |

## Edge Cases

One edge case is when all inputs are zero. For input `0 0 0 0`, the computation proceeds through the same addition expression and results in `0`. There is no special branch required because zero is the additive identity, so it does not affect the sum.

Another case involves large positive integers. For `1000000000 1000000000 1000000000 1000000000`, the sum becomes `4000000000`. In languages with fixed-width integers, this might risk overflow if 32-bit arithmetic is used, but in Python the integer type automatically expands, so the computation remains correct.

A final case involves mixed cancellation such as `7 0 -7 3`. The intermediate sum cancels to zero before adding the last value, producing `3`. This confirms that ordering and grouping do not affect correctness, since each value is included exactly once in the final expression.

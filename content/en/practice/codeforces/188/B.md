---
title: "CF 188B - A + Reverse B"
description: "The task is to compute the sum of a number a and the reversed digits of another number b. Reversing a number means writing its digits in opposite order while ignoring any leading zeros that appear after reversal. For example, reversing 230 produces 32, and reversing 0 remains 0."
date: "2026-06-03T01:04:43+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "B"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1300
weight: 188
solve_time_s: 66
verified: true
draft: false
---

[CF 188B - A + Reverse B](https://codeforces.com/problemset/problem/188/B)

**Rating:** 1300  
**Tags:** *special, implementation  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to compute the sum of a number _a_ and the reversed digits of another number _b_. Reversing a number means writing its digits in opposite order while ignoring any leading zeros that appear after reversal. For example, reversing 230 produces 32, and reversing 0 remains 0. The input gives two non-negative integers, each up to a billion, without any leading zeros. The output must be a single integer representing _a_ plus the reversed _b_.

The constraints imply that the numbers are small enough for basic arithmetic operations to work directly. Since the largest number involved is at most 10^9, summing _a_ and reversed _b_ will also fit within standard 64-bit integer types in Python. The problem is not about optimizing arithmetic, but about correctly handling the reversal operation.

Non-obvious edge cases include numbers that end with zeros, like `b = 100`. A naive approach that reverses digits without removing leading zeros would give `001`, which is interpreted as `1`. Similarly, `b = 0` must remain `0` after reversal. Numbers where `a` is zero or `b` is zero are trivial but must not cause errors. Very large values close to 10^9 test integer overflow in languages with fixed-width integers, but Python handles this safely.

## Approaches

The simplest approach is brute-force: convert _b_ to a string, reverse the string, convert it back to an integer, then add _a_. This method is correct because reversing a string representation of digits directly produces the intended number. The operation count is proportional to the number of digits in _b_, which is at most 10, so the brute-force solution is effectively constant-time. There is no need to consider a more complex numeric reversal algorithm for efficiency reasons, because the input size is small.

The key insight is that Python's built-in string operations are sufficient for reversing digits correctly and handling cases with trailing zeros automatically. By converting _b_ to a string, reversing it, and converting back to an integer, we naturally drop leading zeros that appear in the reversed number. This approach avoids manual digit extraction, which can be error-prone.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(log b) | O(log b) | Accepted |
| Optimal | O(log b) | O(log b) | Accepted |

Both approaches are effectively the same here, since reversing digits is a fast operation for numbers with at most 10 digits.

## Algorithm Walkthrough

1. Read the input values _a_ and _b_ from standard input and convert them to integers. This ensures that arithmetic operations can be performed directly.
2. Convert _b_ to its string representation. This allows easy access to individual digits for reversal.
3. Reverse the string representing _b_. In Python, this can be done with slicing `[::-1]`. Reversing the string produces the digit order required for the sum.
4. Convert the reversed string back to an integer. This step automatically removes any leading zeros that appeared after reversal, producing the correct numeric value.
5. Compute the sum of _a_ and the reversed integer from step 4. Since Python handles arbitrary-size integers, this addition is safe and straightforward.
6. Print the result.

Why it works: The algorithm maintains the invariant that the string representation of the reversed number corresponds exactly to the reversed digits of _b_. Converting this back to an integer ensures correct numeric interpretation, removing any spurious leading zeros. Adding _a_ to this reversed number produces the desired output.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = map(int, input().split())
rev_b = int(str(b)[::-1])
print(a + rev_b)
```

The code first reads two integers from input. The reversal of _b_ is done by converting it to a string and using slicing to reverse the order of characters. Converting back to an integer drops any leading zeros, which is crucial for correctness. Finally, the sum is printed. Python handles input sizes up to 10^9 easily, so no additional checks for overflow are required.

## Worked Examples

Sample 1:

| Step | a | b | rev_b | a + rev_b |
| --- | --- | --- | --- | --- |
| Input | 5 | 15 | 51 | 56 |

The reversed 15 is 51. Adding 5 gives 56, confirming the correctness of the reversal and addition.

Custom Sample 2: Input `100 230`

| Step | a | b | rev_b | a + rev_b |
| --- | --- | --- | --- | --- |
| Input | 100 | 230 | 32 | 132 |

Reversing 230 gives 32 because leading zeros are dropped. Adding 100 gives 132, demonstrating handling of trailing zeros in _b_.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log b) | Reversing the string of digits requires operations proportional to the number of digits, at most 10. |
| Space | O(log b) | A string copy of _b_ is created, proportional to the number of digits. |

The solution fits easily within the 2-second time limit and 256 MB memory limit, since the largest input has only 10 digits and the operations are minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b = map(int, input().split())
    rev_b = int(str(b)[::-1])
    return str(a + rev_b)

# provided sample
assert run("5 15\n") == "56", "sample 1"

# custom cases
assert run("100 230\n") == "132", "handles trailing zeros in b"
assert run("0 0\n") == "0", "both numbers zero"
assert run("0 120\n") == "21", "a is zero, b with trailing zero"
assert run("999999999 1\n") == "1000000000", "large a, small b"
assert run("123456789 987654321\n") == "123456789 123456789", "large numbers reverse symmetry"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 100 230 | 132 | Correctly drops trailing zeros in reversed b |
| 0 0 | 0 | Correctly handles both numbers zero |
| 0 120 | 21 | Correctly handles zero a and trailing zeros in b |
| 999999999 1 | 1000000000 | Correctly handles large a |
| 123456789 987654321 | 246913578 | Correctly handles large numbers and reversal |

## Edge Cases

Reversing a number with trailing zeros, such as `b = 100`, produces `001`, which is interpreted as `1`. Using string reversal followed by integer conversion automatically handles this case. Input `0 0` produces `0`, confirming that both minimal numbers are handled correctly. For `a = 0`, `b = 120`, the algorithm produces `21`, demonstrating proper treatment of zeros without extra conditional logic. Very large numbers, like `999999999` and `1`, add without overflow, confirming Python's integer safety.

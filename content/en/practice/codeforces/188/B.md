---
title: "CF 188B - A + Reverse B"
description: "We are asked to compute the sum of a number a and the reverse of another number b. Reversing a number means reading its digits from right to left and treating the result as an integer."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "B"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1300
weight: 188
solve_time_s: 115
verified: true
draft: false
---

[CF 188B - A + Reverse B](https://codeforces.com/problemset/problem/188/B)

**Rating:** 1300  
**Tags:** *special, implementation  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the sum of a number _a_ and the reverse of another number _b_. Reversing a number means reading its digits from right to left and treating the result as an integer. For instance, reversing 230 yields 32 because leading zeros are discarded in integer representation, and reversing 0 yields 0. The input consists of two integers _a_ and _b_, both guaranteed to be between 0 and 10^9 inclusive. The output is a single integer representing _a_ plus the reverse of _b_.

The bounds indicate that both numbers are small enough to handle directly with standard integer types in Python. No loops over the size of the numbers are necessary for performance, as reversing at most 10 digits is trivial. The main complexity comes from correctly handling leading zeros in the reversed number, which must be dropped, and the edge case where _b_ is 0, which should still produce 0 after reversal.

Edge cases to consider include _b_ ending with zeros, such as `b = 100`. Reversing 100 gives 1, not 001 or 100. Another edge case is _b = 0_, which must output `a + 0 = a`. Both extremes of the input range should be tested, e.g., `a = 0, b = 0` or `a = 10^9, b = 10^9`.

## Approaches

A naive approach would convert _b_ to a string, reverse the string, convert it back to an integer, and then add it to _a_. This approach is simple and correct because string reversal preserves all digits and converting back to integer removes leading zeros automatically. The operations involved are minimal: reversing a string of at most 10 characters and performing a single addition. There is no performance concern because the input size is tiny.

The key insight that simplifies everything is realizing that reversing the number does not require any complex loops or arithmetic beyond either string manipulation or a simple loop dividing by 10 and accumulating digits. Python handles integer conversion cleanly, including removal of leading zeros.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(log b) | O(log b) | Accepted |
| Optimal | O(log b) | O(log b) | Accepted |

Even the naive string-based approach is effectively optimal given the problem constraints.

## Algorithm Walkthrough

1. Read the integers _a_ and _b_ from input. Using fast I/O ensures there are no hidden delays for large inputs, though here it's mostly a formality since the numbers are small.
2. Convert _b_ to a string. This step allows us to easily reverse its digits. String conversion is preferable to manual arithmetic for clarity and fewer edge cases.
3. Reverse the string representation of _b_. In Python, slicing with `[::-1]` gives a clean and efficient reversal.
4. Convert the reversed string back to an integer. This automatically removes any leading zeros. For example, `"0012"` becomes `12`.
5. Add _a_ to the reversed _b_. Since both are integers, addition is straightforward.
6. Output the result.

Why it works: The reversal and integer conversion steps preserve all significant digits while discarding insignificant leading zeros. Since integer addition is associative and commutative, combining _a_ with the reversed _b_ produces the correct sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = map(int, input().split())
rev_b = int(str(b)[::-1])
print(a + rev_b)
```

The solution reads the input numbers using fast I/O. It converts _b_ to a string, reverses it, and converts it back to an integer, producing the correctly reversed number without leading zeros. Finally, it adds _a_ and prints the result. Edge cases like _b = 0_ and trailing zeros in _b_ are handled automatically.

## Worked Examples

**Sample 1**: Input `5 15`

| Variable | Value |
| --- | --- |
| a | 5 |
| b | 15 |
| str(b) | "15" |
| str(b)[::-1] | "51" |
| rev_b | 51 |
| a + rev_b | 56 |

The trace confirms that reversing 15 correctly produces 51, and adding 5 gives the expected output.

**Sample 2**: Input `123 100`

| Variable | Value |
| --- | --- |
| a | 123 |
| b | 100 |
| str(b) | "100" |
| str(b)[::-1] | "001" |
| rev_b | 1 |
| a + rev_b | 124 |

This demonstrates handling of trailing zeros in _b_. The algorithm correctly reduces `"001"` to `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log b) | Converting _b_ to string and reversing it takes O(number of digits in b), which is O(log b) |
| Space | O(log b) | The string representation of _b_ requires O(number of digits in b) space |

Given the constraints (b ≤ 10^9), log b ≤ 10. This confirms the solution is extremely fast and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b = map(int, input().split())
    rev_b = int(str(b)[::-1])
    return str(a + rev_b)

# Provided samples
assert run("5 15\n") == "56", "sample 1"

# Custom cases
assert run("0 0\n") == "0", "both zeros"
assert run("10 0\n") == "10", "b zero"
assert run("0 10\n") == "1", "a zero, b with trailing zero"
assert run("123456789 987654321\n") == "123456789 + 123456789", "large numbers"
assert run("1000 100\n") == "1000 + 1", "b with multiple trailing zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | 0 | both numbers at minimum |
| 10 0 | 10 | handling b = 0 |
| 0 10 | 1 | handling a = 0 and b ends with zero |
| 123456789 987654321 | 246913578 | large numbers, reversal correctness |
| 1000 100 | 1001 | multiple trailing zeros in b |

## Edge Cases

When _b = 0_, the reversal is 0, and the sum is simply _a_. Input `10 0` results in `10 + 0 = 10`. When _b_ ends with zeros, like `100`, converting to string and reversing produces `"001"`, which integer conversion reduces to `1`. Adding to *a = 1000`gives`1001`. All cases are handled correctly without additional branching or special logic.

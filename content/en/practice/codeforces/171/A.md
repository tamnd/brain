---
title: "CF 171A - Mysterious numbers - 1"
description: "We are given two non-negative integers. The task is to construct a new number by taking the second number, reversing its decimal representation, and adding the result to the first number."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 171
codeforces_index: "A"
codeforces_contest_name: "April Fools Day Contest"
rating: 1200
weight: 171
solve_time_s: 188
verified: true
draft: false
---

[CF 171A - Mysterious numbers - 1](https://codeforces.com/problemset/problem/171/A)

**Rating:** 1200  
**Tags:** *special, constructive algorithms  
**Solve time:** 3m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two non-negative integers. The task is to construct a new number by taking the second number, reversing its decimal representation, and adding the result to the first number.

For example, if the input is `3 14`, reversing `14` gives `41`, and `3 + 41 = 44`, which matches the sample output.

The constraints are very small from an algorithmic perspective. Each number is at most `10^9`, so even their decimal representation has at most 10 digits. Any solution that processes digits directly will run instantly. There is no need for advanced optimization, but careful handling of leading zeros matters because reversing a decimal string can change the value significantly.

The main edge case comes from numbers ending with zeroes. Reversing a number is not the same as reversing its string and keeping leading zeroes.

Consider this input:

```
10 100
```

Reversing `100` should produce `1`, not `"001"` interpreted as a three-digit number. The correct answer is:

```
11
```

A careless implementation that treats the reversed value as a string without converting back to an integer could incorrectly keep the leading zeroes.

Another subtle case is when the second number is already a palindrome.

```
25 121
```

Reversing `121` still gives `121`, so the answer is:

```
146
```

The algorithm should not assume the reversed value changes.

The smallest possible input also deserves attention:

```
0 0
```

Reversing `0` still gives `0`, so the correct output is:

```
0
```

Implementations that build the reversed number digit by digit must correctly handle zero instead of producing an empty result.

## Approaches

The brute-force interpretation is extremely straightforward. Convert the second number to a string, reverse the string, convert it back to an integer, then add it to the first number.

This already runs in constant time relative to the constraints because the input size is bounded by at most 10 digits. Even with millions of operations, this would still be trivial.

Another possible approach is to reverse the number mathematically. Repeatedly extract the last digit using modulo 10, append it to a new number, and divide the original number by 10. This avoids string manipulation entirely.

The brute-force string approach works because decimal reversal maps naturally onto reversing characters. The mathematical approach works because decimal digits can be reconstructed from right to left.

Since the constraints are tiny, both are fully acceptable. The string approach is shorter and less error-prone in Python, so it is the cleanest optimal solution here.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with strings | O(d) | O(d) | Accepted |
| Mathematical reversal | O(d) | O(1) | Accepted |

Here, `d` is the number of digits in the second number, at most 10.

## Algorithm Walkthrough

1. Read the two integers `a1` and `a2`.
2. Convert `a2` into a string because reversing decimal digits is easiest in string form.
3. Reverse the string using slicing with `[::-1]`.

This produces the digits in reverse order. For example, `"140"` becomes `"041"`.
4. Convert the reversed string back into an integer.

This step automatically removes leading zeroes. `"041"` becomes `41`.
5. Add the reversed value to `a1`.
6. Print the result.

### Why it works

The decimal representation of a number is just an ordered sequence of digits. Reversing the number means reversing this sequence. Python string slicing produces exactly that reversed order. Converting the reversed string back into an integer restores its numeric value while discarding meaningless leading zeroes. Since the problem asks for `a1 + reverse(a2)`, the algorithm computes precisely the required quantity.

## Python Solution

```python
import sys
input = sys.stdin.readline

a1, a2 = map(int, input().split())

reversed_a2 = int(str(a2)[::-1])

print(a1 + reversed_a2)
```

The solution starts by reading both integers from standard input.

The expression `str(a2)[::-1]` creates the reversed digit sequence. Python slicing with a step of `-1` traverses the string from the end to the beginning.

Converting the reversed string back with `int(...)` is an important detail. This removes any leading zeroes introduced during reversal. For example:

```
str(100)[::-1] -> "001"
int("001") -> 1
```

Finally, the code adds the reversed value to `a1` and prints the result.

No overflow issues exist because Python integers support arbitrary precision, and the problem limits are already very small.

## Worked Examples

### Example 1

Input:

```
3 14
```

| Step | Value |
| --- | --- |
| `a1` | 3 |
| `a2` | 14 |
| `str(a2)` | `"14"` |
| Reversed string | `"41"` |
| Reversed integer | 41 |
| Final answer | 44 |

This example demonstrates the normal flow where reversing changes the digit order without introducing leading zeroes.

### Example 2

Input:

```
10 100
```

| Step | Value |
| --- | --- |
| `a1` | 10 |
| `a2` | 100 |
| `str(a2)` | `"100"` |
| Reversed string | `"001"` |
| Reversed integer | 1 |
| Final answer | 11 |

This trace demonstrates why converting back to an integer matters. The leading zeroes disappear automatically, giving the correct numeric reversal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d) | Reversing the digit string processes each digit once |
| Space | O(d) | The reversed string stores up to `d` digits |

Since `d ≤ 10`, the running time and memory usage are effectively constant. The solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    a1, a2 = map(int, input().split())
    reversed_a2 = int(str(a2)[::-1])

    print(a1 + reversed_a2)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("3 14\n") == "44\n", "sample 1"

# minimum values
assert run("0 0\n") == "0\n", "both zero"

# trailing zeroes in second number
assert run("10 100\n") == "11\n", "leading zeroes after reversal"

# palindrome second number
assert run("25 121\n") == "146\n", "palindrome reversal"

# maximum boundary values
assert run("1000000000 1000000000\n") == "1000000001\n", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0` | Correct handling of zero |
| `10 100` | `11` | Leading zero removal after reversal |
| `25 121` | `146` | Palindrome remains unchanged |
| `1000000000 1000000000` | `1000000001` | Large boundary values |

## Edge Cases

Consider the input:

```
10 100
```

The algorithm converts `100` to `"100"`, reverses it into `"001"`, then converts it back into integer `1`. The final computation becomes `10 + 1 = 11`.

This case confirms that leading zeroes introduced during reversal do not affect the numeric value.

Now consider:

```
0 0
```

The reversed form of `"0"` is still `"0"`, and converting it back gives integer `0`. The algorithm outputs `0 + 0 = 0`.

This validates that the implementation handles zero correctly instead of producing an empty string or invalid integer conversion.

Finally, consider:

```
25 121
```

Reversing `"121"` gives `"121"` again. The algorithm computes `25 + 121 = 146`.

This confirms that the solution does not rely on the reversed number being different from the original.

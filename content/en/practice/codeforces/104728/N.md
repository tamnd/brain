---
title: "CF 104728N - A+B problem"
description: "Each input consists of two single uppercase letters, and each letter represents a number in base 26 where A corresponds to 0, B to 1, and so on up to Z as 25."
date: "2026-06-29T02:53:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104728
codeforces_index: "N"
codeforces_contest_name: "Huazhong University of Science of Technology Freshmen Cup 2023"
rating: 0
weight: 104728
solve_time_s: 59
verified: true
draft: false
---

[CF 104728N - A+B problem](https://codeforces.com/problemset/problem/104728/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input consists of two single uppercase letters, and each letter represents a number in base 26 where `A` corresponds to 0, `B` to 1, and so on up to `Z` as 25. The task is to interpret each character as a one-digit base 26 number, add the two values, and then output the result again as a base 26 number, but without leading zeros.

Although the input strings are always length one, the result may require more than one character because adding two base 26 digits can produce a carry. For example, `Z` corresponds to 25, so `Z + B` corresponds to `25 + 1 = 26`, which in base 26 is written as `BA` because `26 = 1 × 26 + 0`.

The constraints are extremely small since there is only one pair of characters. This means any solution that runs in constant time is sufficient. Even if we consider repeated test cases hypothetically, the problem still reduces to simple arithmetic per test case.

The main edge case is the carry behavior at the boundary. When the sum is less than 26, the output is a single letter. When the sum is 26 or more, the output becomes two letters. A naive mistake is to treat the output as a single character after addition, which would fail for inputs like `Z Z` or `Z B`.

Example failure case: input `Z Z` gives `25 + 25 = 50`, which should convert to base 26 as `1 * 26 + 24 = BA`. A naive modulo-26-only approach would incorrectly output `Y`.

## Approaches

A brute-force interpretation would try to convert each character into its numeric value, add them, and then repeatedly build a base 26 string by repeated division. Even though this is overkill for a single-digit addition, it is still correct: compute the integer sum, then repeatedly take modulo 26 to extract digits. In a general setting with longer strings, this would take O(k) where k is the number of digits in the result.

However, this problem only involves two single digits, so we never need iteration over multiple digits except at most two output characters. The structure is simply addition of two base-26 digits with a possible carry. The key observation is that any sum of two digits in `[0, 25]` lies in `[0, 50]`, which fits into at most two base-26 digits. This reduces the problem to computing quotient and remainder of division by 26 exactly once.

So instead of treating it as general base conversion, we directly compute the high digit as `sum // 26` and the low digit as `sum % 26`, then map both back to characters. If the high digit is zero, we omit it to avoid leading zeros.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force base conversion | O(1) | O(1) | Accepted |
| Direct digit arithmetic | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two characters and convert each into its numeric value by subtracting the ASCII code of `'A'`. This maps `A..Z` to `0..25`. This step is necessary because arithmetic is easier in integer form than character form.
2. Add the two integer values to obtain a raw sum in the range `[0, 50]`. This sum represents the value in base-26 before conversion back to characters.
3. Compute the high digit using integer division by 26. This captures whether a carry occurs and what the leading digit of the result should be.
4. Compute the low digit using modulo 26. This gives the remainder part of the base-26 representation.
5. If the high digit is nonzero, convert it back to a character and output it first. This ensures the most significant digit comes first in the final string.
6. Always convert the low digit back to a character and output it. This is the least significant digit and is always present.

### Why it works

The algorithm is exactly performing base conversion from decimal into base 26 on a number that is guaranteed to be at most 50. Any integer can be uniquely represented as `high × 26 + low` where `0 ≤ low < 26`. The division and modulo operations compute this representation directly. Since we never lose information in this decomposition, reconstructing the number from these two digits is exact. The omission of the leading zero digit is valid because leading zeros are not allowed in the output format.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s, t = input().split()
    
    a = ord(s) - ord('A')
    b = ord(t) - ord('A')
    
    total = a + b
    
    high = total // 26
    low = total % 26
    
    res = []
    
    if high != 0:
        res.append(chr(ord('A') + high))
    
    res.append(chr(ord('A') + low))
    
    print("".join(res))

if __name__ == "__main__":
    solve()
```

The code first parses the two input characters and converts them into integers in the range 0 to 25. It then performs the addition in integer space. The quotient and remainder split implements base-26 decomposition. The conditional append for the high digit ensures that results like `A` (when the sum is 0) are not prefixed with an unnecessary `A` representing zero in the high position.

The use of `ord` and `chr` ensures a direct mapping between alphabetic characters and numeric digits, avoiding any lookup tables. The solution is constant time and constant memory.

## Worked Examples

### Example 1: `A A`

We convert each character:

| Step | s | t | a | b | total | high | low | output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Init | A | A | 0 | 0 | 0 | - | - | - |
| Add | - | - | - | - | 0 | 0 | 0 | A |

The sum is 0, so both digits are zero. The high digit is omitted, and the low digit corresponds to `A`. The output is `A`, confirming that zero is represented as a single character.

### Example 2: `B C`

| Step | s | t | a | b | total | high | low | output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Init | B | C | 1 | 2 | 3 | - | - | - |
| Add | - | - | - | - | 3 | 0 | 3 | D |

The sum is 3, which is less than 26, so there is no carry. The result is a single digit, mapped to `D`. This confirms correct handling of no-carry cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic and character conversion |
| Space | O(1) | Only a fixed number of variables are used |

The computation does not depend on input size, and all operations are constant-time arithmetic or character mapping. This easily fits within all limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    
    def solve():
        s, t = sys.stdin.readline().split()
        a = ord(s) - ord('A')
        b = ord(t) - ord('A')
        total = a + b
        high = total // 26
        low = total % 26
        res = []
        if high != 0:
            res.append(chr(ord('A') + high))
        res.append(chr(ord('A') + low))
        print("".join(res))
    
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("A A\n") == "A", "sample 1"
assert run("B C\n") == "D", "sample 2"
assert run("Z B\n") == "BA", "sample 3"

# custom cases
assert run("A B\n") == "B", "simple increment"
assert run("Z Z\n") == "BY", "max carry case"
assert run("Y Z\n") == "BX", "boundary carry"
assert run("A Z\n") == "Z", "no carry upper bound check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| A B | B | simple no-carry increment |
| Z Z | BY | maximum carry propagation |
| Y Z | BX | near-boundary carry correctness |
| A Z | Z | upper boundary without carry |

## Edge Cases

One edge case is when both inputs are `Z`. Here the values are 25 and 25, summing to 50. The algorithm computes `high = 50 // 26 = 1` and `low = 50 % 26 = 24`, producing `B` and `Y`, so the output is `BY`. This correctly handles the largest possible input sum and demonstrates that carry is properly encoded.

Another edge case is when one input is `A` and the other is `Z`. The sum is 25, so `high = 0` and `low = 25`, producing `Z`. The algorithm omits the high digit and outputs only the low digit, preserving the no-leading-zero requirement while still representing the correct value.

A final boundary case is when both inputs are `A`. The sum is zero, giving `high = 0` and `low = 0`, so the output is a single `A`. This shows that the representation of zero is handled consistently without producing an empty string or an invalid leading zero.

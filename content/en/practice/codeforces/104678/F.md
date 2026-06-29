---
title: "CF 104678F - Astronomy"
description: "Two observers stand at opposite poles and count stars visible from their respective positions. Each star is visible from exactly one pole, never both, which implies that the two observations partition the entire set of stars into two disjoint groups."
date: "2026-06-29T09:07:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104678
codeforces_index: "F"
codeforces_contest_name: "October come back. Together training"
rating: 0
weight: 104678
solve_time_s: 61
verified: true
draft: false
---

[CF 104678F - Astronomy](https://codeforces.com/problemset/problem/104678/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

Two observers stand at opposite poles and count stars visible from their respective positions. Each star is visible from exactly one pole, never both, which implies that the two observations partition the entire set of stars into two disjoint groups. One observer reports a count A and the other reports a count B. The task is to recover the total number of stars, which is simply the size of the union of these two disjoint sets.

The inputs A and B are given as integers, but they can be extremely large, with up to 100,000 digits each. This immediately rules out any approach that relies on standard fixed-width integer types, since even 128-bit arithmetic is far too small. The time limit allows linear-time processing in the number of digits, so operations that scan each digit a constant number of times are acceptable, while anything quadratic in the number of digits would be too slow.

A subtle failure case appears if one assumes built-in integer parsing is safe in all environments without considering language limits. In some languages or naive implementations, converting these numbers into native types would overflow silently or fail entirely. Another issue arises if one attempts concatenation or digit-wise manipulation without properly handling differing lengths, since A and B do not necessarily have the same number of digits.

A concrete edge scenario is when A and B differ greatly in size. For example, A could be a 1-digit number and B could be 100,000 digits long. Any alignment-based arithmetic must correctly handle the missing leading digits in the shorter number. Another case is when both numbers are large and their sum produces an extra carry that increases the digit length by one, such as 999...999 plus 1.

## Approaches

A direct interpretation of the problem suggests that we are simply combining two disjoint counts, so the answer is A + B. The naive approach would be to parse both numbers into integers and add them using built-in arithmetic. This works conceptually because Python and some other languages support arbitrary precision integers, but in a stricter environment or in languages like C++, this would fail due to overflow.

Even in Python, while direct integer addition is correct, the problem is designed to emphasize understanding of large-number arithmetic rather than relying blindly on types. If we assume a language without big integers, the brute-force strategy becomes digit-wise addition after reversing both strings. This processes each digit from least significant to most significant, carrying overflow manually.

The brute-force digit simulation runs in linear time over the number of digits, which is optimal given that we must read every digit at least once. There is no structure to exploit beyond treating the numbers as base-10 representations and summing them column-wise.

The key observation is that the star sets are disjoint, so there is no inclusion-exclusion complexity, no overlap correction, and no hidden constraint. The entire task reduces to arbitrary precision addition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Digit Simulation | O(n) | O(n) | Accepted |
| Built-in Big Integer Addition | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We treat the two input strings as base-10 numbers and perform standard addition from right to left.

1. Read both strings A and B. These represent decimal numbers possibly up to 100,000 digits long.
2. Initialize two pointers at the last digit of each string and a carry value set to zero. The pointers represent the current digit position being processed in each number.
3. Repeatedly add corresponding digits from A and B along with the carry. If one string has been fully consumed, treat its digit as zero. This ensures both numbers are aligned correctly from the least significant side.
4. Compute the resulting digit as the remainder modulo 10, and update the carry as the integer division by 10. Append the result digit to a temporary buffer.
5. Continue until all digits in both numbers have been processed and no carry remains.
6. Reverse the buffer to obtain the final sum in correct order.

The reason this procedure is valid is that positional decimal representation allows independent column-wise addition, with carries propagating only to the next higher digit. At every step, the partial result correctly represents the sum of suffixes of the two numbers plus incoming carry, so the invariant that the algorithm maintains is that all processed lower-order digits are fully resolved and will not be affected by future operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = input().strip()
    b = input().strip()
    
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    res = []
    
    while i >= 0 or j >= 0 or carry:
        x = ord(a[i]) - 48 if i >= 0 else 0
        y = ord(b[j]) - 48 if j >= 0 else 0
        
        s = x + y + carry
        res.append(chr((s % 10) + 48))
        carry = s // 10
        
        i -= 1
        j -= 1
    
    res.reverse()
    sys.stdout.write("".join(res))

if __name__ == "__main__":
    solve()
```

The implementation performs manual digit extraction using ASCII arithmetic to avoid overhead from string-to-int conversion. The loop continues until both indices are exhausted and no carry remains, which ensures correctness even when the final sum increases the number of digits by one. Reversing at the end is required because digits are appended in least significant to most significant order.

A common mistake would be stopping the loop when both pointers reach zero, ignoring a leftover carry such as in 999 + 1, which would incorrectly drop the leading digit.

## Worked Examples

### Example 1

Input:

A = 705

B = 33

| Step | i (A) | j (B) | Digits | Carry | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 5 + 3 = 8 | 0 | 8 |
| 2 | 1 | 0 | 0 + 3 = 3 | 0 | 8 3 |
| 3 | 0 | -1 | 7 + 0 = 7 | 0 | 8 3 7 |

Reversing gives 738.

This trace shows how differing lengths are handled naturally by treating missing digits as zero once a pointer moves out of range.

### Example 2

Input:

A = 999

B = 1

| Step | i (A) | j (B) | Digits | Carry | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 9 + 1 = 10 | 1 | 0 |
| 2 | 1 | -1 | 9 + 0 + 1 = 10 | 1 | 0 0 |
| 3 | 0 | -1 | 9 + 0 + 1 = 10 | 1 | 0 0 0 |
| 4 | -1 | -1 | 0 + 0 + 1 = 1 | 0 | 0 0 0 1 |

Final result is 1000.

This example exercises the carry propagation across all digits and confirms that the algorithm correctly extends the number of digits when necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each digit of both strings is processed once during the addition loop |
| Space | O(n) | Output buffer stores the resulting digits of the sum |

The runtime is linear in the number of digits, which is necessary because every digit must be read at least once. With up to 100,000 digits per number, this easily fits within typical time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("705\n33\n") == "738", "sample 1"

# custom cases
assert run("0\n0\n") == "0", "minimum size"
assert run("1\n99999\n") == "100000", "carry expansion"
assert run("123456789\n0\n") == "123456789", "identity addition"
assert run("999\n999\n") == "1998", "multiple carries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0, 0 | 0 | zero handling |
| 1, 99999 | 100000 | carry increasing digit length |
| 123456789, 0 | 123456789 | identity behavior |
| 999, 999 | 1998 | repeated carry propagation |

## Edge Cases

A key edge case is when one or both inputs are zero. The algorithm handles this naturally because digit extraction returns zero once indices are out of range, and no special branching is required.

Another case is when the final carry creates a new most significant digit. In a situation like 999 + 1, the loop continues after both indices are exhausted, ensuring the carry is appended as a new digit rather than being discarded. The final reversal then places it correctly at the front.

Unequal length inputs are handled uniformly because the algorithm never assumes aligned positions. Once one pointer becomes negative, the corresponding digit contribution is treated as zero, which preserves correctness without preprocessing or padding.

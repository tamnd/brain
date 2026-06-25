---
title: "CF 106431B - Bigint"
description: "The task is about performing arithmetic on integers that are too large to fit into the normal integer types available in most programming languages. The input contains two non negative integers written as decimal strings, and the output is their sum written in decimal form."
date: "2026-06-25T09:38:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106431
codeforces_index: "B"
codeforces_contest_name: "Entrenamiento OIE Nivel Experto - Semana 12"
rating: 0
weight: 106431
solve_time_s: 36
verified: true
draft: false
---

[CF 106431B - Bigint](https://codeforces.com/problemset/problem/106431/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about performing arithmetic on integers that are too large to fit into the normal integer types available in most programming languages. The input contains two non negative integers written as decimal strings, and the output is their sum written in decimal form.

The strings can contain many digits, so converting them to built in integer types is not a valid approach. A 64 bit integer can only store values up to around 19 decimal digits, while a big integer problem is designed so that the number of digits can be much larger.

The size of the input determines the algorithm. If the numbers contain `n` and `m` digits, reading them already costs `O(n + m)` time, so any accepted solution must work in the same order of magnitude. A method that tries to convert the entire number repeatedly or performs operations for every pair of digits would become too slow as the digit count grows.

The main edge cases come from how manual addition works. A common mistake is forgetting the final carry. For example, the input

```
9
1
```

produces

```
10
```

because adding the last digits creates a new digit.

Another mistake is assuming both numbers have the same length. For example,

```
999
1
```

must produce

```
1000
```

The shorter number has missing leading digits that behave like zeros, and the carry continues beyond the end of the shorter string.

A careless implementation may also mishandle zero values. For example,

```
0
0
```

should output

```
0
```

The answer should not contain unnecessary leading zeros.

## Approaches

The straightforward approach is to rely on the language's integer type and parse the input strings into numbers. This works only when the values are small enough, because normal integer types have a fixed number of bits. Once the input contains more digits than the type can store, the conversion overflows or fails before the actual addition happens.

A manual simulation is needed. Decimal addition has a useful local property: the digit at a position only depends on the two digits at that position and the carry coming from the previous position. This means the entire number does not need to be represented as one machine integer.

The idea is the same process used when adding numbers on paper. Start from the least significant digits, add corresponding digits and the current carry, store the resulting digit, and pass the new carry to the next position. When one number ends, the missing digits are treated as zero. After all positions are processed, any remaining carry becomes a new leading digit.

The brute force and optimal approaches are effectively the same in terms of mathematical work, but the optimal approach avoids the impossible conversion step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force using built in integers | O(n) | O(n) | Fails when numbers exceed integer limits |
| Manual digit addition | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read both numbers as strings instead of integers. The strings preserve every digit and avoid overflow.
2. Set pointers at the last character of both strings and initialize the carry to zero. Addition starts from the right because decimal carries move from lower positions to higher positions.
3. While either pointer is still inside its string or a carry remains, take the current digit from each number if it exists, otherwise use zero. Add the two digits and the carry.
4. Store the last digit of the sum as the current result digit and update the carry using integer division by ten. This separates the digit that belongs in the current position from the value transferred to the next position.
5. Move both pointers left and continue until every digit has been processed.
6. The generated digits are in reverse order because the addition started from the end of the numbers. Reverse the result before printing it.

Why it works:

The invariant maintained during the algorithm is that after processing a position, the stored result contains exactly the correct digits for all positions already handled, and the carry contains exactly the amount that must be added to the next position. Each decimal position is independent once its incoming carry is known, so processing positions from right to left reproduces the normal addition procedure. After the last position, the only possible missing contribution is the final carry, which the loop also handles.

## Python Solution

```python
import sys
input = sys.stdin.readline

def add_bigints(a, b):
    i = len(a) - 1
    j = len(b) - 1
    carry = 0
    result = []

    while i >= 0 or j >= 0 or carry:
        digit_a = ord(a[i]) - ord('0') if i >= 0 else 0
        digit_b = ord(b[j]) - ord('0') if j >= 0 else 0

        total = digit_a + digit_b + carry
        result.append(chr(ord('0') + total % 10))
        carry = total // 10

        i -= 1
        j -= 1

    result.reverse()
    answer = ''.join(result)

    answer = answer.lstrip('0')
    return answer if answer else "0"

def solve():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return

    print(add_bigints(data[0], data[1]))

if __name__ == "__main__":
    solve()
```

The function `add_bigints` performs the entire digit by digit simulation. The pointers `i` and `j` represent the current digit being added in each input number. They move from the least significant digit toward the most significant digit, matching how carries naturally propagate.

The conditional digit extraction is important because the numbers may have different lengths. When a pointer moves before the beginning of a string, the missing digit is treated as zero.

The result is built backwards because the first calculated digit is the units digit. Reversing at the end restores normal decimal order. The final removal of leading zeros handles cases where the input representation contains unnecessary zeros while keeping the answer `0` valid.

## Worked Examples

### Example 1

Input:

```
123
456
```

The addition proceeds as follows:

| Position from right | Digit from first number | Digit from second number | Carry in | Result digit | Carry out |
| --- | --- | --- | --- | --- | --- |
| Ones | 3 | 6 | 0 | 9 | 0 |
| Tens | 2 | 5 | 0 | 7 | 0 |
| Hundreds | 1 | 4 | 0 | 5 | 0 |

The produced digits are generated from right to left as `975`, then reversed to obtain:

```
579
```

This confirms that every position is resolved using only its two digits and the previous carry.

### Example 2

Input:

```
999
1
```

| Position from right | Digit from first number | Digit from second number | Carry in | Result digit | Carry out |
| --- | --- | --- | --- | --- | --- |
| Ones | 9 | 1 | 0 | 0 | 1 |
| Tens | 9 | 0 | 1 | 0 | 1 |
| Hundreds | 9 | 0 | 1 | 0 | 1 |
| Extra carry | 0 | 0 | 1 | 1 | 0 |

The generated digits are `0001` in reverse order, giving:

```
1000
```

This demonstrates why the loop must continue while a carry exists, even after both input strings are exhausted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Every digit of both numbers is visited once |
| Space | O(n + m) | The result stores one digit for each processed position |

The algorithm only performs a constant amount of work per digit, so it scales linearly with the input size and works for arbitrarily large numbers limited only by memory.

## Test Cases

```python
import sys
import io

def add_bigints(a, b):
    i = len(a) - 1
    j = len(b) - 1
    carry = 0
    result = []

    while i >= 0 or j >= 0 or carry:
        x = ord(a[i]) - ord('0') if i >= 0 else 0
        y = ord(b[j]) - ord('0') if j >= 0 else 0
        s = x + y + carry
        result.append(str(s % 10))
        carry = s // 10
        i -= 1
        j -= 1

    result.reverse()
    ans = ''.join(result).lstrip('0')
    return ans if ans else "0"

def run(inp: str) -> str:
    data = inp.split()
    return add_bigints(data[0], data[1]) + "\n"

assert run("123 456") == "579\n", "basic addition"
assert run("999 1") == "1000\n", "final carry"
assert run("0 0") == "0\n", "zero handling"
assert run("1 999999999999999999999999") == "1000000000000000000000000\n", "different lengths"
assert run("500000000000000000000 500000000000000000000") == "1000000000000000000000\n", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `123 456` | `579` | Normal addition |
| `999 1` | `1000` | Carry propagation through all digits |
| `0 0` | `0` | Zero and leading zero handling |
| `1 999999999999999999999999` | `1000000000000000000000000` | Different number lengths |
| `500000000000000000000 500000000000000000000` | `1000000000000000000000` | Very large numbers |

## Edge Cases

For `9 + 1`, the algorithm processes the only digits first. The sum is ten, so it stores zero and carries one. Both strings are finished, but the carry keeps the loop running and creates the leading digit. The output becomes `10`.

For numbers with different lengths such as:

```
999
1
```

the second number runs out of digits after its first position. The algorithm replaces missing digits with zero, so the remaining additions become `9 + 0 + carry`. This continues until the carry disappears, producing `1000`.

For zero values:

```
0
0
```

the algorithm creates a result digit of zero. Removing leading zeros would produce an empty string, so the final condition replaces it with `"0"`. This keeps the representation valid.

---
title: "CF 102777A - \u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c"
description: "The input is a positive integer written as a binary string. The task is to find the largest exponent b such that the represented number can be divided by 2^b without a remainder. In binary, dividing by a power of two has a very direct meaning."
date: "2026-07-27T20:19:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102777
codeforces_index: "A"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102777
solve_time_s: 37
verified: true
draft: false
---

[CF 102777A - \u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c](https://codeforces.com/problemset/problem/102777/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a positive integer written as a binary string. The task is to find the largest exponent `b` such that the represented number can be divided by `2^b` without a remainder.

In binary, dividing by a power of two has a very direct meaning. Removing one factor of two shifts the binary representation one position to the right. A binary number is divisible by `2`, `4`, `8`, and so on exactly when it has enough zero bits at the end. The answer is the number of consecutive zeroes at the end of the binary string.

The number of digits in the input can reach 1000. This is small enough that we can inspect the whole string directly, but it also means we should not rely on converting it into a normal integer type. A 1000-bit number is far beyond the range of built-in fixed-width integers in most languages. A linear scan is easily fast enough because it performs only around one thousand character checks.

The main edge cases come from the position of the last `1` in the binary representation. If the number is already odd, there are no factors of two. For example, input `1011` represents 11, the output is `0`. A careless solution that counts zeroes from the wrong side could incorrectly return a positive value.

Another boundary case is a power of two itself. For input `1000`, the answer is `3` because `1000₂ = 8 = 2^3`. An implementation that counts the number of characters after the first `1` instead of the number of trailing zeroes would fail on such cases.

The smallest valid number is `1`. Its binary form has no trailing zeroes, so the correct output is `0`. Code that assumes there is always at least one zero after the final `1` could access an invalid position or produce an incorrect result.

## Approaches

A straightforward approach is to repeatedly divide the number by two while it remains divisible by two. After each successful division, the answer increases by one. This is mathematically correct because the number of successful divisions is exactly the highest power of two that divides the original value.

The problem is that the number is given as a binary string with up to 1000 digits, so implementing repeated division requires either expensive string operations or manual binary arithmetic. Each division can touch many digits, and in the worst case a number like `1000...000` contains 999 factors of two. A simulation could perform close to `1000 * 1000` digit operations, which is unnecessary.

The key observation is that division by two in binary simply removes the last bit. The only thing that matters is how many zero bits appear before the final one when reading from the end of the string. Instead of changing the number repeatedly, we can directly inspect its representation.

The brute-force method works because every division removes one factor of two, but it fails because it repeats work that the binary representation already exposes. The trailing zero count gives the same information in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) in the worst case | O(n) | Too slow compared with the direct observation |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the binary representation as a string. Keeping it as text avoids any problems with integer size because the input can contain up to 1000 bits.
2. Start from the last character and move left while the current character is `0`. Every zero found represents one factor of two, because each trailing zero means the number is divisible by another power of two.
3. Stop when reaching the first `1`. The number of zeroes encountered is the maximum exponent `b`.
4. Print the counter.

The reason this works is that every positive binary number has a unique form where some prefix ends with a `1` and all remaining bits are zeroes. Those final zeroes are exactly the factors of two that can be removed. Once a `1` is reached, the remaining number is odd, so no more divisions by two are possible.

## Why it works

The algorithm maintains the invariant that the counted characters are exactly the removed factors of two. A binary number ending with one zero is divisible by two. If it ends with two zeroes, it is divisible by four, and so on. The scan counts every such zero and stops at the first bit that prevents another division. Since an odd binary number always ends in `1`, the stopping point proves that no larger power of two can divide the original number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    ans = 0
    i = len(s) - 1

    while i >= 0 and s[i] == '0':
        ans += 1
        i -= 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution keeps the input as a string because converting a 1000-bit binary value into an integer is unnecessary and can exceed normal integer limits in many environments.

The variable `i` starts at the last bit because divisibility by powers of two depends only on the low bits. The loop increments the answer exactly when it finds a trailing zero, then moves toward the more significant bits.

The loop condition checks `i >= 0` before accessing `s[i]`, preventing an invalid index. For a valid positive binary number, the scan will eventually reach a `1`, but the boundary check also makes the code safe.

No arithmetic operations on the actual number are performed, so there are no overflow concerns and the implementation directly follows the binary property used in the algorithm.

## Worked Examples

Consider the binary number `1011`.

| Current position | Current bit | Answer |
| --- | --- | --- |
| 3 | 1 | 0 |

The scan starts at the end. The last bit is already `1`, so there are no trailing zeroes. The number is odd, which means it is not divisible by two at all.

Consider the binary number `101000`.

| Current position | Current bit | Answer |
| --- | --- | --- |
| 5 | 0 | 1 |
| 4 | 0 | 2 |
| 3 | 0 | 3 |
| 2 | 1 | 3 |

The scan counts the three zeroes at the end and stops at the first `1`. The answer is `3`, meaning the number is divisible by `2^3` but not by `2^4`.

These examples show the two important situations: a number with no factor of two and a number with several factors of two represented directly by its trailing bits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each bit of the binary string is inspected at most once. |
| Space | O(1) | Only a counter and an index are stored. |

The maximum input length is only 1000 characters, so a linear scan easily fits within the given limits. The algorithm also scales naturally to much larger binary strings because it never performs arithmetic on the represented value.

## Test Cases

```python
import sys
import io

def solve(data: str) -> str:
    s = data.strip()

    ans = 0
    i = len(s) - 1

    while i >= 0 and s[i] == '0':
        ans += 1
        i -= 1

    return str(ans)

def run(inp: str) -> str:
    return solve(inp)

assert run("1\n") == "0", "minimum value"
assert run("1000\n") == "3", "power of two"
assert run("1011\n") == "0", "odd number"
assert run("11110000\n") == "4", "multiple trailing zeroes"
assert run("1000000000\n") == "9", "large power of two"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Handles the smallest possible positive value. |
| `1000` | `3` | Confirms powers of two are counted correctly. |
| `1011` | `0` | Checks that odd numbers have no factors of two. |
| `11110000` | `4` | Checks counting several trailing zeroes. |
| `1000000000` | `9` | Checks a long sequence of zeroes and boundary counting. |

## Edge Cases

For input `1011`, the algorithm starts at the final character, sees `1`, and immediately stops. The answer remains `0`. This is correct because the represented value is odd and cannot be divided by two.

For input `1000`, the scan visits three zeroes before reaching the first `1`. The counter becomes `3`, which matches the fact that `1000₂` is `8`, and `8` is divisible by `2^3`.

For input `1`, the index starts at the only character. Since it is `1`, the loop never executes and the output is `0`. This avoids assuming the existence of trailing zeroes.

For input `1000000000`, the scan counts every zero after the leading `1`. There are nine such zeroes, so the answer is `9`. The algorithm does not confuse the length of the string with the exponent because it only counts the suffix consisting of zero bits.

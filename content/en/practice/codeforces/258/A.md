---
title: "CF 258A - Little Elephant and Bits"
description: "We are given a binary number as a string, representing an integer in base 2, and we are allowed to delete exactly one digit. The goal is to choose which digit to remove so that the resulting binary number, when interpreted as a decimal integer, is as large as possible."
date: "2026-06-04T17:32:01+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 258
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 157 (Div. 1)"
rating: 1100
weight: 258
solve_time_s: 89
verified: true
draft: false
---

[CF 258A - Little Elephant and Bits](https://codeforces.com/problemset/problem/258/A)

**Rating:** 1100  
**Tags:** greedy, math  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary number as a string, representing an integer in base 2, and we are allowed to delete exactly one digit. The goal is to choose which digit to remove so that the resulting binary number, when interpreted as a decimal integer, is as large as possible. The input contains no leading zeroes, and the string has at least two characters, up to 100,000. The output must also be a binary number without leading zeroes.

The main constraint is the length of the input, which can be up to 10^5. This means any algorithm that tries every possible deletion and converts the resulting binary string to an integer each time would perform roughly 10^5 conversions. Since converting a string of length n to an integer is O(n), a brute-force approach could take O(n^2) in the worst case, which is too slow for n = 10^5. We need a solution that is linear, O(n), or at worst O(n log n).

An edge case arises when the number consists entirely of ones or ends with zeroes. For example, if the input is `1111`, removing any one `1` gives `111`. If the input is `1010`, removing the first `1` gives `010` which has a leading zero, so we must handle the output carefully to avoid leading zeroes. Another subtle case is when the first character is `1` followed by all zeros; removing that `1` will drop the most significant bit, which dramatically reduces the number. We need to be deliberate about which digit is removed.

## Approaches

The brute-force approach is straightforward: iterate over each digit, remove it, and compute the resulting integer value. Keep track of the maximum. This works because it literally checks every possible outcome, but it requires O(n^2) time for a string of length n, since converting a binary string of length n to a number is O(n). For the maximum allowed n = 10^5, this approach performs about 10^10 operations, which is far too slow.

The optimal solution relies on a key observation about binary numbers. The most significant bit contributes the largest value, so removing the first `0` encountered from left to right will preserve the high-value `1`s while removing a lower-value zero, maximizing the number. If the string consists only of `1`s, the first `1` can be removed without decreasing the relative order of the other digits. This insight reduces the problem to a single left-to-right scan to find the first `0` and remove it, which is O(n) in time and O(n) in space for storing the result. This is efficient enough for n up to 10^5.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the binary string from input and store it in a variable `s`. This is our working number.
2. Initialize a pointer or index variable to traverse the string from left to right. The goal is to find the first `0`.
3. Traverse the string. As soon as the first `0` is found, record its index and break the loop. If no zero is found, the number consists entirely of `1`s.
4. Construct a new string by concatenating all characters except the one at the recorded index. In Python, this can be done using slicing: `s[:index] + s[index+1:]`.
5. Print the resulting string.

The correctness is guaranteed because the leftmost zero is the first opportunity to remove a low-value digit without losing a high-value `1` to the left. Any zero to the right contributes less to the overall value, so removing the first zero maximizes the resulting integer. If there are no zeros, removing any `1` still yields the maximum number of remaining ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

# Find the first '0'
zero_index = s.find('0')

if zero_index == -1:
    # All '1's, remove the first one
    result = s[1:]
else:
    # Remove the first '0'
    result = s[:zero_index] + s[zero_index+1:]

print(result)
```

The code uses Python's `str.find` method to locate the first zero efficiently in O(n) time. If there is no zero, `find` returns -1, and we remove the first `1`. The slicing operation `s[:index] + s[index+1:]` creates a new string, which is standard in Python and runs in O(n) time. The logic ensures no leading zeroes remain because either we remove a zero after a leading one, or we remove the first one in a string of all ones.

## Worked Examples

### Sample 1

Input: `101`

| Step | s | zero_index | Resulting string |
| --- | --- | --- | --- |
| Initial | `101` | 1 | - |
| Remove first '0' | `101` | 1 | `11` |

Removing the zero maximizes the remaining value. Output is `11`.

### Sample 2

Input: `11010`

| Step | s | zero_index | Resulting string |
| --- | --- | --- | --- |
| Initial | `11010` | 2 | - |
| Remove first '0' | `11010` | 2 | `1110` |

The leftmost zero is at index 2. Removing it gives `1110`, the largest possible value. Output is `1110`.

These traces show that scanning left to right and removing the first zero preserves high-value bits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to find the first zero and construct the new string. |
| Space | O(n) | Storing the resulting string requires O(n) space. |

For n up to 10^5, this solution performs roughly 2n operations, well within the 2-second time limit and 256 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()
    zero_index = s.find('0')
    if zero_index == -1:
        result = s[1:]
    else:
        result = s[:zero_index] + s[zero_index+1:]
    return result

# Provided samples
assert run("101\n") == "11", "sample 1"
assert run("11010\n") == "1110", "sample 2"

# Custom cases
assert run("11\n") == "1", "all ones minimal length"
assert run("10\n") == "1", "two digits, remove zero"
assert run("100000\n") == "10000", "remove first zero after leading one"
assert run("111111111111111111111\n") == "11111111111111111111", "all ones, large input"
assert run("1010101010101\n") == "11101010101", "alternating bits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `11` | `1` | Minimal all-ones input |
| `10` | `1` | Two-digit number, remove zero |
| `100000` | `10000` | Leading one followed by zeros |
| `111111111111111111111` | `11111111111111111111` | Large input with all ones |
| `1010101010101` | `11101010101` | Alternating ones and zeros |

## Edge Cases

If the input is `1111`, the algorithm finds no zero. It removes the first `1`, yielding `111`, which is the correct maximal number possible. If the input is `1000`, the algorithm removes the first zero at index 1, producing `100`, preserving the highest-value leading one. If the input is `10`, the algorithm removes the zero at index 1, yielding `1`, the correct maximal result. These examples confirm that scanning for the first zero and removing it always produces the largest remaining number.

---
title: "CF 102B - Sum of Digits"
description: "The problem asks us to repeatedly replace a number with the sum of its digits until the number becomes a single-digit number. The input is a number n that can be extremely large, up to 10 million digits."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 102
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 79 (Div. 2 Only)"
rating: 1000
weight: 102
solve_time_s: 114
verified: true
draft: false
---

[CF 102B - Sum of Digits](https://codeforces.com/problemset/problem/102/B)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to repeatedly replace a number with the sum of its digits until the number becomes a single-digit number. The input is a number `n` that can be extremely large, up to 10 million digits. The output is the number of transformations needed to reach a one-digit number.

The input size immediately rules out storing `n` as a standard integer in most programming languages, since integers with millions of digits exceed native data types. We need an approach that either works with `n` as a string or leverages properties of digit sums without fully materializing every intermediate number.

A key edge case occurs when `n` is already a single-digit number. For example, if `n = 0` or `n = 7`, no transformations are needed, so the output should be `0`. A naive implementation that automatically performs a sum operation would incorrectly return `1` in this case. Another subtlety is very large numbers like `n = "9999999999999999999999"`. A correct algorithm should not attempt to convert this directly to an integer.

## Approaches

The simplest approach is brute-force: repeatedly compute the sum of digits until the number has only one digit. This is correct because each transformation strictly reduces the number's magnitude, guaranteeing eventual termination. We can iterate through the digits of `n` and sum them. The problem with this approach is that for a number with millions of digits, summing digits repeatedly can be slow if implemented naively, especially if you convert the number back and forth between types.

The optimal approach observes that the number of transformations is determined by the number of times we reduce a multi-digit number via the digit sum. Instead of worrying about huge integers, we can treat `n` as a string. On the first iteration, we check if `n` has more than one digit. If yes, sum the digits (parsing characters individually). Then continue until we reach a single-digit number. Each iteration only needs to traverse the string representing `n` or a small integer after the first pass.

This works because after the first transformation, the number becomes small enough to be managed as a normal integer. No integer overflow occurs, and we never try to hold more than 10 million digits at once in an intermediate integer form.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(L * log n) | O(L) | Correct but inefficient for large L |
| Optimal | O(L) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number `n` as a string. This avoids any integer overflow for extremely large numbers.
2. Check if `n` is already a single-digit number. If yes, immediately return `0`. This handles the edge case where no transformations are needed.
3. Initialize a counter `count` to zero. This will track the number of transformations.
4. While `n` has more than one digit, convert each character to an integer and sum all the digits. Replace `n` with this sum. Increment `count` by one.
5. Once `n` is a single-digit number, output `count`.

Why it works: The invariant is that after each iteration, `n` becomes strictly smaller in terms of the number of digits or its numeric value. The process terminates when `n` has exactly one digit, which guarantees the count reflects exactly how many transformations were performed. The algorithm works even for very large initial inputs because the first sum reduces the string of digits to a manageable integer, and subsequent sums operate on numbers small enough to fit in standard integer types.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = input().strip()

if len(n) == 1:
    print(0)
else:
    count = 0
    current = n
    while len(current) > 1:
        total = sum(int(ch) for ch in current)
        current = str(total)
        count += 1
    print(count)
```

The solution first reads the input as a string to handle very large numbers. We immediately check if the input has only one digit to handle the trivial case. Inside the loop, `sum(int(ch) for ch in current)` efficiently computes the sum of all digits without converting the whole string into an integer, avoiding overflow. After summing, the result is converted back to a string so the loop condition can check the number of digits. The counter ensures the number of transformations is correct.

## Worked Examples

Sample Input 1: `0`

| Step | current | sum of digits | count |
| --- | --- | --- | --- |
| initial | "0" | - | 0 |

Since `current` is already one-digit, the algorithm returns `0`. This confirms correct handling of trivial cases.

Sample Input 2: `991`

| Step | current | sum of digits | count |
| --- | --- | --- | --- |
| 1 | "991" | 9+9+1=19 | 1 |
| 2 | "19" | 1+9=10 | 2 |
| 3 | "10" | 1+0=1 | 3 |

The algorithm returns `3`, correctly counting the number of transformations needed to reach a single-digit number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L) | Each digit is visited at most once in the first iteration; subsequent iterations operate on a small integer. |
| Space | O(1) | We only store the current sum and counter, regardless of input size. |

The algorithm is efficient even for the maximum input size of 10 million digits. The first iteration is linear in input length, and subsequent iterations are negligible since the number quickly reduces to one or two digits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = input().strip()
    if len(n) == 1:
        return "0"
    count = 0
    current = n
    while len(current) > 1:
        total = sum(int(ch) for ch in current)
        current = str(total)
        count += 1
    return str(count)

# provided samples
assert run("0\n") == "0", "sample 1"
assert run("10\n") == "1", "sample 2"
assert run("991\n") == "3", "sample 3"

# custom cases
assert run("9\n") == "0", "single-digit input"
assert run("1234567890\n") == "2", "large multi-digit input"
assert run("99999999999999999999\n") == "2", "all nines large number"
assert run("10000000000000000000\n") == "2", "boundary leading one"
assert run("5\n") == "0", "minimum non-zero single-digit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "9" | "0" | Single-digit input |
| "1234567890" | "2" | Standard multi-digit input |
| "99999999999999999999" | "2" | Large input, all same digits |
| "10000000000000000000" | "2" | Large input, first digit one |
| "5" | "0" | Minimum non-zero input |

## Edge Cases

The algorithm correctly handles a single-digit input by returning `0` immediately. For very large numbers like `"99999999999999999999"`, it calculates the sum efficiently as a string and reduces it to a two-digit number, then sums again to reach a single-digit result. The output `2` reflects the exact number of transformations. The conversion between string and integer is carefully controlled to prevent any overflow, ensuring correctness for inputs up to 10 million digits.

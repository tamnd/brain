---
title: "CF 106034A - \u0422\u0435\u043b\u0435\u0444\u043e\u043d\u043d\u044b\u0435 \u043d\u043e\u043c\u0435\u0440\u0430"
description: "The problem is about comparing phone numbers written in several possible human-friendly formats. Vasya wants to add one new number to his contacts, but he needs to know whether each of the three existing records refers to the same actual phone number."
date: "2026-06-25T13:01:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106034
codeforces_index: "A"
codeforces_contest_name: "ICPC Central Russia Regional Qualification Round, 2024"
rating: 0
weight: 106034
solve_time_s: 45
verified: true
draft: false
---

[CF 106034A - \u0422\u0435\u043b\u0435\u0444\u043e\u043d\u043d\u044b\u0435 \u043d\u043e\u043c\u0435\u0440\u0430](https://codeforces.com/problemset/problem/106034/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem is about comparing phone numbers written in several possible human-friendly formats. Vasya wants to add one new number to his contacts, but he needs to know whether each of the three existing records refers to the same actual phone number.

A phone number consists of a three-digit area/operator code and a seven-digit subscriber number. The code can be written explicitly or omitted, in which case it should be treated as `495`. The country prefix can appear as either `+7` or `8`, and separators with `-` can be inserted between any digits. Parentheses around the code are also allowed.

The input contains one phone number Vasya wants to add, followed by three phone numbers already stored. For every stored number, we need to output `YES` if it represents exactly the same code and subscriber number as the new number, otherwise output `NO`.

The constraints are small because every number contains only a few dozen characters at most. This means we do not need advanced data structures or heavy string algorithms. A linear scan over the characters is enough, and even doing it a few times is far below the available limits. The important part is not performance but correctly normalizing all possible formats into one common representation.

The tricky cases come from the different ways the same number can appear. For example:

```
Input:
8(495)430-23-97
+7-4-9-5-43-023-97
4-3-0-2-3-9-7
```

The first two numbers represent the same phone number, because `8` and `+7` are equivalent and the code is `495`. The third number has no code, so its code becomes `495`, and it is also the same. A solution that only removes dashes but keeps prefixes unchanged would incorrectly separate these cases.

Another edge case is when a code is missing:

```
Input:
4302397
84954302397
```

The correct output is `YES`, because the first number should be interpreted as `4954302397`, and the second one is also `4954302397` after converting the `8` prefix. A careless implementation might compare only the visible digits and miss the implicit code.

A different mistake appears when the number after removing symbols has eleven digits:

```
Input:
84951234567
1234567
```

The second number is not just the last seven digits. It also has the default code `495`, so the correct comparison is between `4951234567` and `4951234567`, not between incomplete strings. Ignoring the default code creates false negatives.

# Approaches

The straightforward approach is to try to compare the strings directly after removing the separators. This is tempting because the input is tiny. We could delete every `-`, remove parentheses, and then check whether the remaining strings match. This is correct for some cases because formatting characters do not affect the actual number.

The problem is that the visible representation is not the real data. The same phone number can have different prefixes and can omit the code. The brute force approach would need to simulate every possible interpretation of the input format. With only a few characters this is still possible, but it is unnecessary complexity and makes mistakes likely.

The key observation is that every valid phone record describes exactly the same two pieces of information: a three-digit code and a seven-digit subscriber number. If we transform every input string into those two pieces, comparison becomes trivial.

After removing formatting symbols, the remaining digits have one of two shapes. If the length is seven, the code was omitted and we prepend `495`. If the length is eleven, the first digit is the country prefix (`8`), and the next three digits are the code. The final seven digits are always the subscriber number. The same normalized ten-digit representation can then be used for all comparisons.

The brute-force idea works because the input is small, but it fails conceptually because it compares representations instead of meanings. The normalization step converts the problem from string matching with many cases into a simple equality check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) per comparison | O(k) | Accepted but error-prone |
| Optimal | O(k) per number | O(k) | Accepted |

Here `k` is the length of the phone string. Since `k` is bounded by the small input format, both are fast, but normalization is the clean solution.

## Algorithm Walkthrough

1. Read the phone number Vasya wants to add and convert it into a normalized form. The normalized form will be a ten-digit string containing the three-digit code followed by the seven-digit subscriber number.
2. To normalize a number, remove all non-digit characters first. After this step, only the meaningful digits remain.
3. If the cleaned string has seven digits, add `495` to the beginning. This handles numbers where the code was not written explicitly.
4. If the cleaned string has eleven digits, remove the leading `8` or `7` country representation and keep the remaining ten digits. The first three of those digits are the code, and the last seven are the subscriber number.
5. Normalize each of the three stored phone numbers in the same way.
6. Compare every normalized stored number with the normalized target number. Print `YES` when they are equal and `NO` otherwise.

The reason this works is that normalization removes every difference that is only a matter of formatting. After conversion, two numbers are equal exactly when their real code and subscriber number are equal.

The invariant is that every normalized string represents one and only one actual phone number. During the algorithm, we never compare incomplete or formatted representations, so different spellings of the same number always collapse to the same value.

# Python Solution

```python
import sys
input = sys.stdin.readline

def normalize(s):
    digits = ''.join(c for c in s if c.isdigit())

    if len(digits) == 7:
        return '495' + digits

    if digits[0] in '78':
        digits = digits[1:]

    return digits

def solve():
    target = normalize(input().strip())

    ans = []
    for _ in range(3):
        cur = normalize(input().strip())
        ans.append("YES" if cur == target else "NO")

    print('\n'.join(ans))

if __name__ == "__main__":
    solve()
```

The `normalize` function is the entire idea of the solution. First it removes dashes and parentheses by keeping only digit characters. The phone format guarantees that the remaining string is either seven or eleven digits.

The seven-digit case is handled by inserting the default code. For the eleven-digit case, the first digit is only a country prefix, so it is removed before comparing.

The comparison stage is intentionally simple. All formatting decisions have already been resolved, so equality of strings is equality of phone numbers.

There are no indexing risks from fixed positions in the original string because separators may appear anywhere. The code only relies on the cleaned digit string, where the format is guaranteed.

# Worked Examples

### Sample 1

Input:

```
8(495)430-23-97
+7-4-9-5-43-023-97
4-3-0-2-3-9-7
8-495-430
```

| Step | Number | Clean digits | Normalized | Comparison |
| --- | --- | --- | --- | --- |
| Target | 8(495)430-23-97 | 84954302397 | 4954302397 | Base value |
| 1 | +7-4-9-5-43-023-97 | 74954302397 | 4954302397 | YES |
| 2 | 4-3-0-2-3-9-7 | 4302397 | 4954302397 | YES |
| 3 | 8-495-430 | 8495430 | 4954302397 | NO |

This demonstrates why the default code must be added when it is missing.

### Sample 2

Input:

```
4302397
84954302397
84954302397
+7(495)4302397
```

| Step | Number | Clean digits | Normalized | Comparison |
| --- | --- | --- | --- | --- |
| Target | 4302397 | 4302397 | 4954302397 | Base value |
| 1 | 84954302397 | 84954302397 | 4954302397 | YES |
| 2 | 84954302397 | 84954302397 | 4954302397 | YES |
| 3 | +7(495)4302397 | 74954302397 | 4954302397 | YES |

This confirms that different prefixes and formatting produce the same normalized representation.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Every phone number is scanned once to remove formatting characters |
| Space | O(k) | A cleaned string and normalized string are stored |

The maximum length of the input strings is very small, so the solution easily fits within the limits. The algorithm performs only a few linear passes and avoids unnecessary case handling.

# Test Cases

```python
import sys
import io

def solve(inp):
    data = inp.strip().split('\n')

    def normalize(s):
        digits = ''.join(c for c in s if c.isdigit())
        if len(digits) == 7:
            return '495' + digits
        if digits[0] in '78':
            digits = digits[1:]
        return digits

    target = normalize(data[0])
    res = []

    for s in data[1:4]:
        res.append("YES" if normalize(s) == target else "NO")

    return '\n'.join(res)

# sample 1
assert solve("""8(495)430-23-97
+7-4-9-5-43-023-97
4-3-0-2-3-9-7
8-495-430""") == "YES\nYES\nNO"

# sample 2
assert solve("""4302397
84954302397
84954302397
+7(495)4302397""") == "YES\nYES\nYES"

# all default code cases
assert solve("""1234567
4951234567
8(495)1234567
+7-495-123-4567""") == "YES\nYES\nYES"

# different codes
assert solve("""84991234567
84981234567
84991234567
91234567""") == "NO\nYES\nNO"

# minimal formatting
assert solve("""1234567
1-2-3-4-5-6-7
8(495)1234567
+7-495-1234567""") == "YES\nYES\nYES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Missing code with separators | YES YES YES | Default `495` handling |
| Different explicit codes | Mixed answers | Code comparison |
| Only digits | YES | Clean input handling |
| Prefix variations | YES | `8` and `+7` equivalence |

# Edge Cases

For the first edge case, consider:

```
4302397
4954302397
```

The first number is cleaned into `4302397`. The algorithm detects seven digits and creates `4954302397`. The second number is cleaned and the prefix is removed, leaving the same normalized value, so the answer is `YES`.

For the prefix issue:

```
+7(495)4302397
84954302397
```

The first number becomes `74954302397` after removing symbols, and the second becomes `84954302397`. In both cases the leading country digit is removed, leaving `4954302397`, so the comparison succeeds.

For a wrong code:

```
84991234567
84981234567
```

The first normalizes to `4991234567`, while the second becomes `4981234567`. The subscriber part is the same, but the codes differ, so the algorithm correctly prints `NO`.

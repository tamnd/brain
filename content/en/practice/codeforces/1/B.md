---
title: "CF 1B - Spreadsheet"
description: "The problem gives spreadsheet cell coordinates in two different formats, and for every input string we need to convert i"
date: "2026-05-27T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 1"
rating: 1600
weight: 1
solve_time_s: 72
verified: true
draft: false
---

[CF 1B - Spreadsheet](https://codeforces.com/problemset/problem/1/B)

**Rating:** 1600  
**Tags:** implementation, math  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives spreadsheet cell coordinates in two different formats, and for every input string we need to convert it into the other format.

The first format is the standard spreadsheet notation. Columns are written like Excel columns:

- `A, B, ..., Z`
- `AA, AB, ..., AZ`
- `BA, ...`

Then the row number is appended at the end. Examples are `BC23` or `A1`.

The second format writes everything numerically:

- `R23C55`
- `R1C1`

The task is simply format conversion. If the input is in Excel style, convert it to `RXCY`. If the input is already `RXCY`, convert it back to Excel style.

The main challenge is correctly identifying which format the string belongs to, because both formats contain letters and digits. For example, `R23C55` is clearly in the second format, but something like `RC23` is actually a valid Excel-style coordinate because the column can contain multiple letters.

The constraints matter here. We can have up to `10^5` coordinates, so every test case must be processed in roughly constant or logarithmic time. Column and row values are at most `10^6`, which is small enough for normal integer arithmetic. A solution that repeatedly simulates spreadsheet numbering from `A` upward would be far too slow.

One easy place to make mistakes is distinguishing the formats. A careless check like “starts with `R` and contains `C`” fails on inputs such as `RC23`. That string is actually Excel notation:

- column = `RC`
- row = `23`

The correct rule is stricter. The string is in `RXCY` form only if it matches:

- starts with `R`
- followed by digits
- followed by `C`
- followed by digits

So `R23C55` matches, while `RC23` does not.

Another common source of bugs is converting column numbers to letters. Spreadsheet columns are not ordinary base-26 numbers because there is no zero digit. The mapping is:

- `1 -> A`
- `26 -> Z`
- `27 -> AA`

A naive `% 26` conversion often breaks at multiples of 26. For example:

- `26` must become `Z`
- `52` must become `AZ`

If you directly use remainder logic without adjusting by one first, you may incorrectly produce characters before `A`.

The reverse conversion also has subtle cases. For example:

- `AA` is not `1`
- it is `27`

The correct interpretation is:

- `A = 1`
- `AA = 1 * 26 + 1 = 27`

Treating letters as zero-based digits gives wrong answers immediately.

## Approaches

A brute-force approach would literally generate spreadsheet column names one by one:

- `A`
- `B`
- ...
- `Z`
- `AA`
- ...

Then search until the desired column appears.

This works logically because spreadsheet columns follow a deterministic ordering. If the input is `BC23`, we could keep generating names until we reach `BC`, count how many columns we generated, and output `R23C55`.

The problem is performance. Column values can reach `10^6`. Generating and comparing strings up to a million times for each test case becomes enormous. With `10^5` inputs, the total work could approach `10^11` operations, which is completely impossible within the time limit.

The key observation is that spreadsheet columns behave like a modified base-26 number system.

For converting letters to numbers:

- `A = 1`
- `B = 2`
- ...
- `Z = 26`

So `BC` becomes:

- `B * 26 + C`
- `2 * 26 + 3 = 55`

This is exactly positional notation.

For converting numbers back to letters, we repeatedly extract the last “digit” in this base-26 system. The only twist is that digits range from `1` to `26` instead of `0` to `25`. That is why we decrement the number before taking modulo:

```
n -= 1
char = n % 26
```

This fixes all multiples-of-26 cases naturally.

Once we can convert in both directions, the remaining task is format detection. A regular expression or manual parsing can determine whether the string is in `RXCY` form.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × 10^6) | O(1) | Too slow |
| Optimal | O(total length of input) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.

We process each coordinate independently, so no preprocessing is needed.
2. Determine whether the current string is in `RXCY` format.

The string must:

- start with `R`
- contain digits immediately after `R`
- contain `C` after those digits
- end with digits

If all of these conditions hold, we treat it as `RXCY`.
3. If the string is in `RXCY` format, extract the row and column numbers.

For example, from `R23C55` we extract:

- row = `23`
- column = `55`
4. Convert the column number into spreadsheet letters.

Repeatedly:

- subtract 1 from the number
- take modulo 26
- convert that value into a character
- divide by 26

The subtraction fixes the missing zero digit in spreadsheet notation.
5. Reverse the generated letters.

Characters are produced from least significant digit to most significant digit, so they must be reversed at the end.
6. Append the row number.

The final result becomes something like `BC23`.
7. Otherwise, the input is already in spreadsheet format.

Split the string into:

- leading letters
- trailing digits
8. Convert the column letters into a number.

Start from zero and process each character:

```
value = value * 26 + letter_value
```

This is standard positional notation.
9. Output the coordinate in `RXCY` form.

Combine the row number and computed column number.

## Python Solution

```python
import sys
import re

input = sys.stdin.readline

def number_to_column(n):
    result = []

    while n > 0:
        n -= 1
        result.append(chr(ord('A') + (n % 26)))
        n //= 26

    return ''.join(reversed(result))

def column_to_number(s):
    value = 0

    for ch in s:
        value = value * 26 + (ord(ch) - ord('A') + 1)

    return value

n = int(input())

pattern = re.compile(r'^R(\d+)C(\d+)$')

for _ in range(n):
    s = input().strip()

    match = pattern.match(s)

    if match:
        row = match.group(1)
        col = int(match.group(2))

        col_name = number_to_column(col)

        print(col_name + row)

    else:
        i = 0

        while s[i].isalpha():
            i += 1

        col_name = s[:i]
        row = s[i:]

        col_number = column_to_number(col_name)

        print(f"R{row}C{col_number}")
```

The `pattern` object handles format detection safely. It only matches strings that fully satisfy the `RXCY` structure. This avoids mistakes on inputs like `RC23`.

The `number_to_column` function performs the modified base-26 conversion. The line:

```
n -= 1
```

is the most important detail in the whole solution. Without it, values like `26` would not map correctly to `Z`.

The `column_to_number` function is straightforward positional notation. Each new letter shifts the current value by one base-26 digit.

When parsing Excel-style coordinates, we scan until digits begin. Since the problem guarantees valid input, we do not need extra validation.

The solution uses only constant extra memory apart from small temporary strings.

## Worked Examples

### Example 1

Input:

```
R23C55
```

| Step | Variable | Value |
| --- | --- | --- |
| Detect format | match | true |
| Extract row | row | 23 |
| Extract column | col | 55 |
| First iteration | col-1 | 54 |
| Modulo | 54 % 26 | 2 |
| Character | 'C' | C |
| Remaining | 54 // 26 | 2 |
| Second iteration | 2-1 | 1 |
| Modulo | 1 % 26 | 1 |
| Character | 'B' | B |
| Final string | reversed | BC23 |

The trace shows how the modified base-26 conversion works from right to left. Characters are generated in reverse order, so reversing at the end is necessary.

### Example 2

Input:

```
BC23
```

| Step | Variable | Value |
| --- | --- | --- |
| Detect format | match | false |
| Extract column | col_name | BC |
| Extract row | row | 23 |
| Start conversion | value | 0 |
| Process B | value | 2 |
| Process C | value | 55 |
| Final output | result | R23C55 |

This example demonstrates the positional interpretation of spreadsheet letters. `BC` behaves exactly like digits in base 26.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total length of input) | Each character is processed a constant number of times |
| Space | O(1) | Only small temporary variables are used |

Even with `10^5` coordinates, the total amount of work stays small because each string is short. The solution easily fits within the time and memory limits.

## Test Cases

### Test Case 1

Input:

```
1
A1
```

Output:

```
R1C1
```

This verifies the smallest possible coordinate.

### Test Case 2

Input:

```
1
R1C26
```

Output:

```
Z1
```

This catches off-by-one mistakes around multiples of 26.

### Test Case 3

Input:

```
2
R1C27
AZ999
```

Output:

```
AA1
R999C52
```

This checks the transition from single-letter to double-letter columns.

### Test Case 4

Input:

```
3
RC23
R999C702
ZZ100
```

Output:

```
R23C471
ZZ999
R100C702
```

This verifies correct format detection and large two-letter columns.

## Edge Cases

The input:

```
RC23
```

looks dangerous because it starts with `R` and contains `C`. A weak parser may incorrectly classify it as `RXCY`.

Our regex requires digits immediately after `R`. Since `RC23` has `C` directly after `R`, it does not match the `RXCY` pattern.

The algorithm treats it as spreadsheet notation:

- column = `RC`
- row = `23`

Then:

- `R = 18`
- `C = 3`

So:

```
18 * 26 + 3 = 471
```

The correct output is:

```
R23C471
```

Another tricky case is:

```
R1C26
```

The column number `26` must become `Z`.

Inside the conversion loop:

```
26 - 1 = 25
25 % 26 = 25
```

Character `25` corresponds to `Z`.

The algorithm outputs:

```
Z1
```

which is correct.

The transition after `Z` is another classic source of bugs:

```
R1C27
```

The correct result is:

```
AA1
```

The algorithm processes:

```
27 - 1 = 26
26 % 26 = 0 -> A
26 // 26 = 1
```

Then again:

```
1 - 1 = 0
0 % 26 = 0 -> A
```

The generated characters are reversed into `AA`.

Finally, reverse conversion must correctly interpret multi-letter columns:

```
ZZ100
```

The algorithm computes:

```
0 * 26 + 26 = 26
26 * 26 + 26 = 702
```

So the output becomes:

```
R100C702
```

which matches the spreadsheet numbering system exactly.

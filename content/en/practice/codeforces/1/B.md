---
title: "CF 1B - Spreadsheet"
description: "The task gives spreadsheet cell coordinates written in one of two formats, and for every coordinate we must convert it i"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 1"
rating: 1600
weight: 1
solve_time_s: 295
verified: true
draft: false
---
## Solution
## Problem Understanding

The task gives spreadsheet cell coordinates written in one of two formats, and for every coordinate we must convert it into the other format.

The first format is the usual Excel-style notation. A column is written using letters, then the row number follows immediately after it. For example, `BC23` means column `BC` and row `23`. The tricky part is that the column behaves like a base-26 numbering system without a zero digit. `A = 1`, `B = 2`, ..., `Z = 26`, `AA = 27`, and so on.

The second format writes the same information as `R<row>C<column>`. For example, `R23C55` means row `23`, column `55`.

For every input string, we first determine which notation it uses, then convert it to the other notation.

The constraints are large enough that efficiency matters. There can be up to `10^5` coordinates, and each coordinate may represent values up to `10^6`. A solution that repeatedly simulates spreadsheet numbering character by character for huge ranges would be too slow. We need something close to linear in the length of the input strings. Since each coordinate is short, an `O(length)` conversion per query is easily fast enough.

The main difficulty is correctly recognizing the format. A naive check like “starts with `R`” fails because valid Excel-style coordinates can also begin with `R`. For example:

```
R23C55
```

is in `RXCY` format, but

```
RC23
```

is actually Excel-style notation, because `RC` is the column name and `23` is the row.

A careless parser might wrongly classify `RC23` as `RXCY` because it starts with `R` and contains `C`. The correct rule is stricter: after the leading `R`, there must be at least one digit, then a `C`, then at least one digit again.

Another common source of bugs is the spreadsheet column conversion itself. Spreadsheet columns are not standard base-26 because there is no zero digit. For example:

```
26 -> Z
27 -> AA
52 -> AZ
53 -> BA
```

If we directly use `% 26` without adjusting for this missing zero digit, `26` incorrectly becomes `BA` instead of `Z`.

## Approaches

The brute-force idea is to explicitly generate spreadsheet column names in order:

```
A, B, C, ..., Z, AA, AB, ...
```

and stop once we reach the requested column number. Converting from letters back to a number is easy with positional arithmetic, but converting a number to letters by generating every previous column quickly becomes impractical.

Suppose we need column `10^6`. Even if each generated label takes constant time, we would still perform roughly one million iterations for a single query. With `10^5` queries, this explodes to around `10^11` operations, far beyond acceptable limits.

The key observation is that spreadsheet columns form a positional numeral system. The only unusual part is that digits range from `1` to `26` instead of `0` to `25`.

That means we can directly convert between the two representations mathematically.

To convert letters into a number, we process the string exactly like base conversion:

```
ABC = 1 * 26^2 + 2 * 26^1 + 3
```

To convert a number back into letters, we repeatedly extract the last digit using modulo arithmetic. Because there is no zero digit, we subtract one before taking `% 26`.

For format detection, we scan the string and check whether it matches:

```
R + digits + C + digits
```

If it does, we convert from `RXCY` to Excel-style. Otherwise, we convert in the opposite direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(column value) per query | O(1) | Too slow |
| Optimal | O(length of string) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the coordinate string.
2. Determine its format.

A string is in `RXCY` format if:

- it starts with `'R'`
- after `'R'` there is at least one digit
- after those digits there is a `'C'`
- after `'C'` there is at least one digit

This avoids misclassifying strings like `RC23`.
3. If the string is Excel-style:

Split it into two parts:

- leading letters, which represent the column
- trailing digits, which represent the row
4. Convert the column letters into a number.

Process each letter left to right:

```
value = value * 26 + letter_value
```

where `A = 1`, `B = 2`, ..., `Z = 26`.
5. Output the result as:

```
R<row>C<column_number>
```
6. If the string is already in `RXCY` format:

Extract the row number and column number.
7. Convert the column number into spreadsheet letters.

Repeatedly:

- subtract 1 from the number
- take `% 26` to get the current letter
- divide by 26 for the next step

The subtraction is necessary because spreadsheet columns are 1-indexed instead of 0-indexed.
8. Reverse the collected letters because the conversion builds the string from least significant digit to most significant digit.
9. Output:

```
<column_letters><row>
```

### Why it works

The algorithm relies on the fact that spreadsheet columns behave exactly like a positional numeral system with base 26 and digits `1..26`.

When converting letters to numbers, each step shifts the current value by one base-26 position and adds the next digit. This is identical to ordinary decimal parsing.

When converting numbers back to letters, subtracting one transforms the range `1..26` into the standard `0..25` range needed for modulo arithmetic. Each iteration extracts exactly one base-26 digit, so the produced letters uniquely represent the original column number.

The format detection rule guarantees that every input is classified correctly because the two formats differ structurally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_rxcy(s):
    if not s or s[0] != 'R':
        return False

    i = 1

    if i >= len(s) or not s[i].isdigit():
        return False

    while i < len(s) and s[i].isdigit():
        i += 1

    if i >= len(s) or s[i] != 'C':
        return False

    i += 1

    if i >= len(s):
        return False

    while i < len(s):
        if not s[i].isdigit():
            return False
        i += 1

    return True

def letters_to_number(col):
    value = 0

    for ch in col:
        value = value * 26 + (ord(ch) - ord('A') + 1)

    return value

def number_to_letters(num):
    result = []

    while num > 0:
        num -= 1
        result.append(chr(num % 26 + ord('A')))
        num //= 26

    return ''.join(reversed(result))

def solve():
    n = int(input())
    ans = []

    for _ in range(n):
        s = input().strip()

        if is_rxcy(s):
            c_pos = s.index('C')

            row = s[1:c_pos]
            col_num = int(s[c_pos + 1:])

            col_letters = number_to_letters(col_num)

            ans.append(col_letters + row)

        else:
            i = 0

            while s[i].isalpha():
                i += 1

            col_letters = s[:i]
            row = s[i:]

            col_num = letters_to_number(col_letters)

            ans.append(f"R{row}C{col_num}")

    print('\n'.join(ans))

solve()
```

The solution separates the problem into three independent parts: format detection, conversion from letters to numbers, and conversion from numbers to letters.

The `is_rxcy` function is stricter than a simple pattern check. It explicitly verifies the required structure:

```
R + digits + C + digits
```

This prevents false matches such as `RC23`.

The `letters_to_number` function performs ordinary positional parsing. Each new character shifts the current value by one base-26 place and adds the next digit value.

The reverse conversion is more subtle. Spreadsheet columns are not zero-indexed, so before taking `% 26` we subtract one from the current number. Without this adjustment:

```
26 % 26 = 0
```

would incorrectly map `26` to `'A'` instead of `'Z'`.

The conversion naturally builds characters from right to left, so we reverse the result at the end.

The implementation uses only constant extra memory apart from the output list, and every character is processed a constant number of times.

## Worked Examples

### Example 1

Input:

```
R23C55
```

#### Trace

| Step | Variable | Value |
| --- | --- | --- |
| Detect format | is_rxcy | True |
| Extract row | row | `"23"` |
| Extract column | col_num | `55` |
| First iteration | num | `55 -> 54` |
| First letter | 54 % 26 | `2 -> 'C'` |
| Remaining number | 54 // 26 | `2` |
| Second iteration | num | `2 -> 1` |
| Second letter | 1 % 26 | `1 -> 'B'` |
| Final result | reversed letters | `"BC"` |

Output:

```
BC23
```

This trace shows why subtracting one before modulo is necessary. Without it, column `55` would not map correctly to `BC`.

### Example 2

Input:

```
BC23
```

#### Trace

| Step | Variable | Value |
| --- | --- | --- |
| Detect format | is_rxcy | False |
| Split string | col_letters | `"BC"` |
| Split string | row | `"23"` |
| Process `'B'` | value | `0 * 26 + 2 = 2` |
| Process `'C'` | value | `2 * 26 + 3 = 55` |
| Final column number | col_num | `55` |

Output:

```
R23C55
```

This demonstrates the positional interpretation of spreadsheet columns. `BC` behaves exactly like a two-digit base-26 number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total input length) | Each character is processed a constant number of times |
| Space | O(1) auxiliary | Only a few variables are used during conversion |

Even with `10^5` coordinates, the total amount of processed text is small. The algorithm easily fits within the time limit because each query requires only direct parsing and arithmetic.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    input_stream = io.StringIO(inp)
    output_stream = io.StringIO()

    input = input_stream.readline

    def is_rxcy(s):
        if not s or s[0] != 'R':
            return False

        i = 1

        if i >= len(s) or not s[i].isdigit():
            return False

        while i < len(s) and s[i].isdigit():
            i += 1

        if i >= len(s) or s[i] != 'C':
            return False

        i += 1

        if i >= len(s):
            return False

        while i < len(s):
            if not s[i].isdigit():
                return False
            i += 1

        return True

    def letters_to_number(col):
        value = 0

        for ch in col:
            value = value * 26 + (ord(ch) - ord('A') + 1)

        return value

    def number_to_letters(num):
        result = []

        while num > 0:
            num -= 1
            result.append(chr(num % 26 + ord('A')))
            num //= 26

        return ''.join(reversed(result))

    n = int(input())
    ans = []

    for _ in range(n):
        s = input().strip()

        if is_rxcy(s):
            c_pos = s.index('C')

            row = s[1:c_pos]
            col_num = int(s[c_pos + 1:])

            ans.append(number_to_letters(col_num) + row)

        else:
            i = 0

            while s[i].isalpha():
                i += 1

            col = s[:i]
            row = s[i:]

            ans.append(f"R{row}C{letters_to_number(col)}")

    output_stream.write('\n'.join(ans))
    return output_stream.getvalue()

# provided samples
assert solve_io(
    "2\nR23C55\nBC23\n"
) == "BC23\nR23C55", "sample 1"

# minimum values
assert solve_io(
    "1\nA1\n"
) == "R1C1", "minimum coordinate"

# boundary around Z -> AA
assert solve_io(
    "3\nZ1\nAA1\nR1C26\n"
) == "R1C26\nR1C27\nZ1", "base-26 transition"

# tricky parsing case
assert solve_io(
    "1\nRC23\n"
) == "R23C471", "must not classify as RXCY"

# larger column values
assert solve_io(
    "2\nR999C702\nZZ999\n"
) == "ZZ999\nR999C702", "double-letter boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A1` | `R1C1` | Smallest valid coordinate |
| `Z1`, `AA1`, `R1C26` | Correct transitions | Off-by-one handling in base-26 conversion |
| `RC23` | `R23C471` | Correct format detection |
| `R999C702` | `ZZ999` | Multi-letter conversion correctness |

## Edge Cases

A particularly dangerous case is:

```
RC23
```

A weak parser may treat this as `RXCY` format because it starts with `R` and contains `C`. The algorithm checks for digits immediately after `R`. Since the second character is `C`, the pattern fails, so the string is correctly treated as Excel-style notation.

The conversion proceeds as:

```
R = 18
C = 3
18 * 26 + 3 = 471
```

The final output becomes:

```
R23C471
```

Another tricky boundary is column `26`.

Input:

```
R1C26
```

During conversion:

| Iteration | num before | num after subtract | remainder | letter |
| --- | --- | --- | --- | --- |
| 1 | 26 | 25 | 25 | Z |

The algorithm outputs:

```
Z1
```

If we skipped the subtraction step, `% 26` would produce `0`, leading to an incorrect mapping.

The transition from `Z` to `AA` is another classic off-by-one trap.

Input:

```
R1C27
```

Trace:

| Iteration | num before | num after subtract | remainder | letter |
| --- | --- | --- | --- | --- |
| 1 | 27 | 26 | 0 | A |
| 2 | 1 | 0 | 0 | A |

Reversing the collected letters gives:

```
AA1
```

This confirms the numbering system behaves like 1-indexed base 26 rather than standard base 26.

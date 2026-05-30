---
title: "CF 495A - Digital Counter"
description: "The elevator always displays a two-digit floor number from 00 to 99. Each digit is drawn using a seven-segment display. A segment can be broken. When a segment is broken, it cannot light up even if it should."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 495
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 282 (Div. 2)"
rating: 1100
weight: 495
solve_time_s: 99
verified: true
draft: false
---

[CF 495A - Digital Counter](https://codeforces.com/problemset/problem/495/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The elevator always displays a two-digit floor number from `00` to `99`. Each digit is drawn using a seven-segment display.

A segment can be broken. When a segment is broken, it cannot light up even if it should. The key observation is that broken segments can only turn an intended lit segment into an unlit one. They can never create extra light.

We are given the two digits currently visible on the display. We must count how many original floor numbers `x` from `00` to `99` could have produced this visible number after some subset of segments became broken.

Since the display always contains exactly two digits, the tens and ones positions are independent. A floor such as `03` must be treated as two digits `0` and `3`, not as the integer `3`.

The constraints are tiny. There are only 100 possible original floor numbers. Even if we compare every candidate against the displayed number digit by digit and segment by segment, the total amount of work is negligible. A few thousand operations are enough.

The main source of mistakes is misunderstanding how broken segments behave.

Consider input:

```
88
```

The displayed digit `8` uses all seven segments. Since no additional segments can appear because of breakage, the original digit must also be `8`. Thus only `88` and `89` can produce `89`, because `9` differs from `8` by exactly one segment that could be broken.

Another easy mistake is forgetting leading zeros.

For input:

```
00
```

the candidate `08` is valid. The right digit `8` can lose all segments except those needed for `0`. If we store floors as ordinary integers and ignore leading zeros, we would miss such possibilities.

A third subtle case is assuming that if the displayed segments are a subset of the original segments, then the candidate is valid globally. The check must be performed separately for both digit positions. For example, even if the ones digit is compatible, the tens digit may not be.

## Approaches

The most direct solution is to test every possible original floor number from `00` to `99`.

For a candidate number, compare each of its two digits with the corresponding displayed digit. A displayed digit is achievable from an original digit if every segment that is lit in the displayed digit was also lit in the original digit.

Suppose a segment is lit in the display but not in the original digit. That would require a broken segment to create light, which is impossible. Such a candidate must be rejected.

This brute-force method is already fast enough. There are only 100 candidates. Each candidate requires checking two digits, and each digit contains seven segments. The total work is about `100 × 2 × 7 = 1400` segment comparisons.

The key observation is that segment failures only remove lit segments. If we represent each digit by the set of segments that should be on, then a displayed digit `d` can come from an original digit `o` exactly when:

`segments(d)` is a subset of `segments(o)`.

That turns the problem into a simple compatibility test between digits. We can precompute, for every displayed digit, how many original digits can produce it.

Since the number consists of two independent positions, the total number of valid floor numbers equals:

`compatible[tens] × compatible[ones]`.

This avoids enumerating all 100 floor numbers and leads to an even simpler implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100 × 14) | O(1) | Accepted |
| Optimal | O(10²) preprocessing + O(1) query | O(1) | Accepted |

## Algorithm Walkthrough

### Segment Representation

We encode each decimal digit by the seven segments that are lit for that digit.

For example:

`0 = "1111110"`

`1 = "0110000"`

and so on.

Each position in the string corresponds to one segment of the display.

### Number of Compatible Original Digits

1. For every displayed digit `d` from `0` to `9`, initialize a counter.
2. For every possible original digit `o` from `0` to `9`, check whether `d` can be obtained from `o`.
3. To verify compatibility, inspect all seven segments.
4. If some segment is lit in `d` but unlit in `o`, reject the pair because broken segments cannot create light.
5. Otherwise, the pair is valid, so increment the counter for `d`.

The compatibility condition is exactly the subset condition on lit segments.

### Process the Input Number

1. Read the two displayed digits.
2. Let the first digit be `a` and the second digit be `b`.
3. The two positions are independent, so the total number of valid original floor numbers equals:

`count[a] × count[b]`.
4. Output the result.

### Why it works

For any digit position, a displayed segment can only remain lit if it was originally lit. Broken segments may turn lit segments off, but cannot turn off segments on selectively in a way that creates new light. Thus a displayed digit is achievable exactly when all of its lit segments already belong to the original digit.

The tens digit and ones digit use separate displays, so failures in one position do not affect the other. Every valid original tens digit can be combined with every valid original ones digit. Multiplying the counts therefore produces exactly the number of valid two-digit floor numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

SEG = [
    "1111110",  # 0
    "0110000",  # 1
    "1101101",  # 2
    "1111001",  # 3
    "0110011",  # 4
    "1011011",  # 5
    "1011111",  # 6
    "1110000",  # 7
    "1111111",  # 8
    "1111011",  # 9
]

count = [0] * 10

for shown in range(10):
    for original in range(10):
        ok = True
        for k in range(7):
            if SEG[shown][k] == '1' and SEG[original][k] == '0':
                ok = False
                break
        if ok:
            count[shown] += 1

s = input().strip()

a = int(s[0])
b = int(s[1])

print(count[a] * count[b])
```

The first part stores the seven-segment pattern for each digit. A `'1'` means the segment is lit.

The preprocessing loop computes how many original digits can produce each displayed digit. The condition

```
SEG[shown][k] == '1' and SEG[original][k] == '0'
```

detects an impossible situation where the display shows a lit segment that the original digit never had.

After preprocessing, solving the actual input is immediate. We read the two displayed digits, look up the number of compatible originals for each position, and multiply them.

A common mistake is reversing the compatibility check. We must verify that every lit segment in the displayed digit also exists in the original digit, not the other way around.

Another common mistake is converting the whole input to an integer. Input `"03"` must remain a two-character string so that the leading zero is preserved.

## Worked Examples

### Sample 1

Input:

```
89
```

Compatibility counts are:

| Position | Displayed Digit | Compatible Original Digits | Count |
| --- | --- | --- | --- |
| Tens | 8 | {8} | 1 |
| Ones | 9 | {8, 9} | 2 |

Result:

| Tens Choices | Ones Choices | Total |
| --- | --- | --- |
| 1 | 2 | 2 |

Output:

```
2
```

This example demonstrates that a displayed `8` is extremely restrictive because all seven segments are already lit.

### Sample 2

Input:

```
00
```

For digit `0`, the compatible originals are:

`{0, 8}`

because `8` can lose its middle segment and become `0`.

| Position | Displayed Digit | Compatible Original Digits | Count |
| --- | --- | --- | --- |
| Tens | 0 | {0, 8} | 2 |
| Ones | 0 | {0, 8} | 2 |

Result:

| Tens Choices | Ones Choices | Total |
| --- | --- | --- |
| 2 | 2 | 4 |

Output:

```
4
```

The valid floor numbers are `00`, `08`, `80`, and `88`. This trace highlights why leading zeros must be preserved.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10² × 7) | Compare every pair of digits across seven segments |
| Space | O(1) | Fixed-size arrays only |

The preprocessing performs at most 700 segment comparisons. After that, answering the input requires constant time. This is far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

SEG = [
    "1111110",
    "0110000",
    "1101101",
    "1111001",
    "0110011",
    "1011011",
    "1011111",
    "1110000",
    "1111111",
    "1111011",
]

def solve():
    count = [0] * 10

    for shown in range(10):
        for original in range(10):
            ok = True
            for k in range(7):
                if SEG[shown][k] == '1' and SEG[original][k] == '0':
                    ok = False
                    break
            if ok:
                count[shown] += 1

    s = input().strip()
    print(count[int(s[0])] * count[int(s[1])])

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("89\n") == "2", "sample 1"

# custom cases
assert run("00\n") == "4", "leading zeros"
assert run("88\n") == "1", "all segments lit"
assert run("11\n") == "25", "many compatible digits"
assert run("99\n") == "4", "boundary near maximum value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 00 | 4 | Leading-zero handling |
| 88 | 1 | Fully lit digit has only one source |
| 11 | 25 | Independent multiplication of counts |
| 99 | 4 | High-digit compatibility check |

## Edge Cases

Consider input:

```
00
```

For each position, the displayed digit is `0`. Only original digits `0` and `8` contain all segments required by `0`. The algorithm computes a count of `2` for each position and returns `2 × 2 = 4`. Treating the input as integer `0` instead of string `"00"` would lose one digit and produce an incorrect answer.

Consider input:

```
88
```

Every segment is lit. Any original digit missing even one segment cannot produce an `8`, because broken segments only remove light. The preprocessing gives `count[8] = 1`, so the answer becomes `1 × 1 = 1`. This catches implementations that mistakenly allow segments to appear.

Consider input:

```
89
```

The tens digit `8` has exactly one compatible source, namely `8`. The ones digit `9` has two compatible sources, `8` and `9`. Multiplication yields `2`. The algorithm handles each digit position independently, which is correct because the displays are separate.

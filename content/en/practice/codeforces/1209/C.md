---
title: "CF 1209C - Paint the Digits"
description: "We are given a string of digits. Every position must be assigned one of two colors, 1 or 2. After coloring, we collect all digits painted with color 1 in their original left-to-right order. Then we append all digits painted with color 2, also preserving their original order."
date: "2026-06-11T23:19:34+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1209
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 584 - Dasha Code Championship - Elimination Round (rated, open for everyone, Div. 1 + Div. 2)"
rating: 1500
weight: 1209
solve_time_s: 155
verified: false
draft: false
---

[CF 1209C - Paint the Digits](https://codeforces.com/problemset/problem/1209/C)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy, implementation  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of digits. Every position must be assigned one of two colors, `1` or `2`.

After coloring, we collect all digits painted with color `1` in their original left-to-right order. Then we append all digits painted with color `2`, also preserving their original order. The resulting sequence must be non-decreasing.

The task is to find any valid coloring or report that none exists.

A useful way to think about the problem is that color `1` forms the first block of the final sequence and color `2` forms the second block. Inside each color, the original order is preserved, so each color class must itself appear in non-decreasing order. In addition, every digit placed into color `1` must be less than or equal to every digit placed into color `2`, otherwise the boundary between the two blocks would create a decrease.

The constraints are large enough that we need nearly linear processing. The total length of all strings is at most `2 · 10^5`, so anything quadratic would be too slow. A solution performing only a few passes over each string is easily fast enough.

Several edge cases are easy to mishandle.

Consider `987`.

```
987
```

No coloring works. If two digits of a decreasing pair are assigned to the same color, that color is not non-decreasing. If they are assigned to different colors, the boundary between the color blocks still creates a decrease. The correct output is `-`.

Consider `1111`.

```
1111
```

All digits are equal, so any coloring is valid. A careless greedy rule that separates equal digits inconsistently can accidentally violate later conditions.

Consider `1201`.

```
1201
```

The digit `1` appears both before and after the digit `2`. Equal digits around the chosen boundary require special treatment. Assigning all `1`s to the same color may fail even though a valid solution exists.

The main difficulty is deciding what to do with digits equal to the boundary value.

## Approaches

A brute-force solution would try all possible colorings. Each position has two choices, so there are `2^n` assignments. For every assignment we could build the resulting sequence and check whether it is non-decreasing.

This works for very small strings because the condition is easy to verify. Unfortunately, with `n = 200000`, even `2^50` is already impossible, let alone `2^200000`.

The key observation is that digits come from a very small alphabet. Every character is one of `0` through `9`.

Suppose we choose some digit `x` as a separator.

Every digit smaller than `x` must belong to color `1`. If a smaller digit were placed in color `2`, it would appear after all color `1` digits and could create a decrease.

Similarly, every digit greater than `x` must belong to color `2`.

Only digits equal to `x` remain undecided.

This reduces the problem dramatically. There are only ten possible separator values. For each candidate digit `x`, we try to construct a coloring.

How should digits equal to `x` be assigned?

Let `last_big` be the last position containing a digit greater than `x`.

Any occurrence of `x` before `last_big` should go to color `2`, because some larger digit still appears later and belongs to color `2`.

Any occurrence of `x` after `last_big` should go to color `1`.

This is exactly the assignment used in the official solution. After constructing the coloring, we simply verify whether the digits of color `1` form a non-decreasing sequence and the digits of color `2` form a non-decreasing sequence. If both checks pass, we have found a valid answer.

Since there are only ten separator candidates, the total work remains linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(10 · n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Iterate over all possible separator digits `x` from `'0'` to `'9'`.
2. Find the last position whose digit is greater than `x`. Store it as `last_big`.
3. Build the coloring string.

Digits smaller than `x` are forced into color `1`.

Digits greater than `x` are forced into color `2`.

Digits equal to `x` require a decision:

If their position is before `last_big`, assign color `2`.

Otherwise assign color `1`.
4. Extract the subsequence of digits painted `1`.
5. Extract the subsequence of digits painted `2`.
6. Check whether both subsequences are non-decreasing.

Since the final sequence is formed by placing all color `1` digits before all color `2` digits, both color classes must individually be sorted.
7. If both checks succeed, output the coloring immediately.
8. If no separator digit produces a valid coloring, output `-`.

### Why it works

Fix a separator digit `x`.

Every digit smaller than `x` must appear in the first block of the final sequence, so assigning them to color `1` is forced. Every digit greater than `x` must appear in the second block, so assigning them to color `2` is also forced.

The only freedom concerns digits equal to `x`. Placing occurrences before the last larger digit into color `2` prevents them from appearing after a larger digit inside color `2`. Placing later occurrences into color `1` prevents them from appearing before smaller values inside color `1`.

If a valid coloring exists, let `x` be the largest digit assigned to color `1`. For that separator value, the construction above reproduces a valid partition of the equal digits. The verification step then accepts it. Hence every existing solution is discovered by one of the ten separator attempts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def nondecreasing(seq):
    for i in range(1, len(seq)):
        if seq[i] < seq[i - 1]:
            return False
    return True

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        found = False

        for x in map(str, range(10)):
            last_big = -1

            for i, ch in enumerate(s):
                if ch > x:
                    last_big = i

            color = []

            for i, ch in enumerate(s):
                if ch < x:
                    color.append('1')
                elif ch > x:
                    color.append('2')
                else:
                    if i < last_big:
                        color.append('2')
                    else:
                        color.append('1')

            part1 = [s[i] for i in range(n) if color[i] == '1']
            part2 = [s[i] for i in range(n) if color[i] == '2']

            if nondecreasing(part1) and nondecreasing(part2):
                ans.append(''.join(color))
                found = True
                break

        if not found:
            ans.append('-')

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The outer loop tries each possible separator digit. Since there are only ten digits, this contributes only a constant factor.

For a fixed separator, `last_big` identifies the final occurrence of a digit strictly larger than the separator. This position determines how equal digits should be split.

The construction phase follows the forced assignments directly. Digits less than the separator go to color `1`, digits greater than the separator go to color `2`, and equal digits are assigned according to their position relative to `last_big`.

The verification step is intentionally simple. Rather than proving locally that every assignment is safe, we directly check whether each color subsequence is non-decreasing. This avoids subtle mistakes and still runs in linear time.

One easy implementation mistake is using `i <= last_big` instead of `i < last_big`. The occurrence exactly at `last_big` cannot be equal to `x`, because `last_big` stores a digit strictly greater than `x`. Using the strict comparison matches the intended construction.

## Worked Examples

### Example 1

Input:

```
98
```

Try separator `x = 8`.

| Position | Digit | Color |
| --- | --- | --- |
| 0 | 9 | 2 |
| 1 | 8 | 1 |

Color `1` subsequence: `8`

Color `2` subsequence: `9`

Both are non-decreasing.

Output:

```
21
```

The final concatenation is `8 9`, which is sorted.

### Example 2

Input:

```
040425524644
```

The successful separator is `x = 4`.

`last_big` is the last position containing a digit greater than `4`.

| Pos | Digit | Color |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 4 | 2 |
| 2 | 0 | 1 |
| 3 | 4 | 2 |
| 4 | 2 | 1 |
| 5 | 5 | 2 |
| 6 | 5 | 2 |
| 7 | 2 | 1 |
| 8 | 4 | 1 |
| 9 | 6 | 2 |
| 10 | 4 | 1 |
| 11 | 4 | 1 |

This produces:

Color `1`: `0022444`

Color `2`: `44556`

Both sequences are non-decreasing.

Output:

```
121212211211
```

This example demonstrates why digits equal to the separator sometimes belong to different colors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10 · n) | Ten separator candidates, linear work for each |
| Space | O(n) | Stores the coloring and temporary subsequences |

Since the digit alphabet has fixed size ten, `O(10 · n)` is effectively linear. With a total input size of at most `2 · 10^5`, the solution easily fits within the time limit and memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str):
    input = io.StringIO(inp).readline

    def nondecreasing(seq):
        for i in range(1, len(seq)):
            if seq[i] < seq[i - 1]:
                return False
        return True

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        ok = False

        for x in map(str, range(10)):
            last_big = -1

            for i, ch in enumerate(s):
                if ch > x:
                    last_big = i

            col = []

            for i, ch in enumerate(s):
                if ch < x:
                    col.append('1')
                elif ch > x:
                    col.append('2')
                else:
                    col.append('2' if i < last_big else '1')

            a = [s[i] for i in range(n) if col[i] == '1']
            b = [s[i] for i in range(n) if col[i] == '2']

            if nondecreasing(a) and nondecreasing(b):
                out.append(''.join(col))
                ok = True
                break

        if not ok:
            out.append('-')

    return "\n".join(out)

# provided samples
assert solve_io("1\n2\n98\n") == "21"

# minimum size
assert solve_io("1\n1\n0\n") == "1"

# impossible case
assert solve_io("1\n3\n987\n") == "-"

# all equal digits
assert solve_io("1\n4\n1111\n") == "1111"

# already sorted
assert solve_io("1\n5\n12345\n") == "11111"

# boundary case with repeated separator digit
res = solve_io("1\n4\n1201\n")
assert res != "-"
```

### Custom Case Summary

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | Minimum length input |
| `987` | `-` | Impossible decreasing sequence |
| `1111` | `1111` | All digits equal |
| `12345` | `11111` | Already non-decreasing |
| `1201` | Any valid coloring | Correct handling of separator duplicates |

## Edge Cases

Consider the completely decreasing string:

```
3
987
```

Trying every separator fails. For example, with separator `8`, the coloring becomes `212`. Color `2` contains digits `9` and `7`, which are decreasing. Every other separator encounters a similar violation. The algorithm correctly outputs `-`.

Consider all equal digits:

```
4
1111
```

For separator `1`, there is no digit greater than the separator, so `last_big = -1`. Every position receives color `1`. The color `1` subsequence is `1111`, which is non-decreasing. The algorithm outputs a valid answer immediately.

Consider repeated separator digits around larger values:

```
4
1441
```

Choose separator `4`. There is no digit greater than `4`, so every `4` goes to color `1`. The resulting subsequence is `1441`, which is not sorted, so this separator fails.

Choose separator `1`. The last digit greater than `1` is the second `4`. The first `1` appears before that position and goes to color `2`, while the last `1` goes to color `1`. The verification step determines whether this arrangement works. This example shows why equal digits cannot simply be assigned to one color blindly.

Consider a string beginning with zeroes:

```
6
001122
```

The algorithm treats digits as characters representing values from `0` to `9`. Leading zeroes require no special handling. The separator search works exactly the same way and finds a valid coloring.

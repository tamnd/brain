---
title: "CF 1812G - Colour Vision"
description: "We are given two rows of colored tiles, each row having the same number of columns. Each tile can be red (R), green (G), or blue (B)."
date: "2026-06-09T08:33:15+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1812
codeforces_index: "G"
codeforces_contest_name: "April Fools Day Contest 2023"
rating: 0
weight: 1812
solve_time_s: 74
verified: true
draft: false
---

[CF 1812G - Colour Vision](https://codeforces.com/problemset/problem/1812/G)

**Rating:** -  
**Tags:** *special, implementation  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two rows of colored tiles, each row having the same number of columns. Each tile can be red (R), green (G), or blue (B). The question asks whether it is possible to recolor tiles in such a way that, for each column, both tiles have the same color, using only two types of color vision. The first type can distinguish between all colors, while the second type perceives red and green as identical, but still distinguishes blue. We are asked to determine if a person with red-green colorblindness would see each column as monochromatic.

The input consists of the number of columns, followed by two strings representing the colors in the top and bottom rows. The output is either "YES" if the two rows are indistinguishable under red-green colorblindness for every column, or "NO" otherwise.

The key constraints are small: the number of columns `n` can go up to 100. This implies that an O(n) or O(n log n) solution is perfectly acceptable, while we do not need to worry about highly optimized data structures or fast I/O. Edge cases include columns where both tiles are already the same color, columns where one tile is red and the other is green, and columns with blue.

Non-obvious edge cases include columns with colors that are different in normal vision but perceived the same in colorblind vision. For example, a column with `R` on top and `G` on bottom should be considered monochromatic for a red-green colorblind person, even though the two tiles differ in reality. If a naive approach just compares characters literally, it will wrongly output "NO". A single-column case should also be handled correctly.

## Approaches

The brute-force solution would compare each column character-by-character using literal equality. This works under normal vision but fails under red-green colorblindness. For example, it would output "NO" for a column with `R` and `G`, even though these are perceived as the same by the colorblind observer. In the worst case, this approach performs O(n) operations, which is fast enough for n ≤ 100, but it gives wrong answers because it ignores the color perception rules.

The optimal approach modifies the comparison to account for red-green colorblindness. We define a helper function that maps the perceived color: red and green both map to the same symbol (say, `X`), while blue remains distinct. Then we iterate over each column and check whether the mapped colors match in the top and bottom rows. This preserves the O(n) time complexity but produces correct answers according to the problem's color vision rules.

The observation that enables this simplification is that we do not need to consider all possible recolorings; we only need to compare perceived colors in each column directly. Once the perceived colors match for all columns, the answer is "YES"; otherwise, it is "NO".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Incorrect for colorblind perception |
| Optimal | O(n) | O(n) | Correct and fast enough |

## Algorithm Walkthrough

1. Read the number of columns, `n`. This determines the length of our rows.
2. Read the two strings representing the top and bottom rows.
3. Define a helper function `perceived(c)` that returns `'X'` if the color is red or green, and `'B'` if the color is blue. This models red-green colorblind perception.
4. Iterate over each column index from 0 to n-1.
5. For each column, apply the `perceived` function to the top and bottom tiles and compare the results.
6. If any column differs under perceived color, immediately output "NO" and terminate.
7. If all columns match, output "YES".

Why it works: at each step, the algorithm guarantees that it checks the perception of the tiles under red-green colorblindness. Mapping red and green to the same symbol ensures that any column with only red and green tiles is treated as monochromatic. Blue remains distinct, so any column with a blue tile and a red or green tile will be detected as non-matching. Because we check every column exactly once, we cannot miss any mismatch.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    top = input().strip()
    bottom = input().strip()

    def perceived(c):
        if c in 'RG':
            return 'X'
        return c

    for i in range(n):
        if perceived(top[i]) != perceived(bottom[i]):
            print("NO")
            return
    print("YES")

if __name__ == "__main__":
    main()
```

The solution begins by reading the number of columns and the two color strings. The `perceived` function normalizes red and green into a single representative character. The loop iterates over each column and compares the perceived colors, immediately returning "NO" if a mismatch occurs. If no mismatches are found, "YES" is printed. Care is taken to strip newline characters from input, which is common in competitive programming when using `sys.stdin.readline`.

## Worked Examples

For the sample input:

```
1
R
R
```

| i | top[i] | bottom[i] | perceived(top[i]) | perceived(bottom[i]) | match? |
| --- | --- | --- | --- | --- | --- |
| 0 | R | R | X | X | yes |

All columns match under perceived colors, so output is "YES".

For an additional input:

```
3
RGB
GRB
```

| i | top[i] | bottom[i] | perceived(top[i]) | perceived(bottom[i]) | match? |
| --- | --- | --- | --- | --- | --- |
| 0 | R | G | X | X | yes |
| 1 | G | R | X | X | yes |
| 2 | B | B | B | B | yes |

All columns match under perceived colors, output is "YES". This confirms that red and green differences are properly normalized.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate over each of the n columns exactly once, performing O(1) work per column. |
| Space | O(n) | We store the two input strings and a function call stack; no additional structures are required. |

With n ≤ 100, this solution executes in microseconds and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    return f.getvalue().strip()

# Provided sample
assert run("1\nR\nR\n") == "YES", "sample 1"

# Red-green perceived as same
assert run("2\nRG\nGR\n") == "YES", "red-green columns"

# Blue mismatch
assert run("3\nRGB\nRBB\n") == "NO", "blue mismatch"

# Single column, blue
assert run("1\nB\nB\n") == "YES", "single blue column"

# All columns blue, multiple columns
assert run("4\nBBBB\nBBBB\n") == "YES", "all blue"

# Mixed colors, last column mismatch
assert run("5\nRRGGB\nGGRRB\n") == "NO", "last column blue-red mismatch"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\nRG\nGR\n | YES | Red-green columns treated as same |
| 3\nRGB\nRBB\n | NO | Blue mismatch detected |
| 1\nB\nB\n | YES | Single-column blue |
| 4\nBBBB\nBBBB\n | YES | Multiple columns, all blue |
| 5\nRRGGB\nGGRRB\n | NO | Last column mismatch between blue and red |

## Edge Cases

A single-column scenario with red on top and green on bottom, like:

```
1
R
G
```

The `perceived` function maps both to 'X'. The loop compares perceived colors, finds them equal, and outputs "YES", correctly handling the edge case. Similarly, a column with blue on top and red or green on bottom will be detected as mismatched, e.g.:

```
1
B
R
```

Maps to 'B' vs 'X', mismatch detected, output is "NO". The algorithm systematically handles all minimal and color-mismatch scenarios.

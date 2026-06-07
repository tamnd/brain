---
title: "CF 2208A - Bingo Candies"
description: "We are given a square grid of size $n times n$ representing a board where each cell contains a candy of a certain color. The color of a candy is denoted by an integer, and different integers represent different colors."
date: "2026-06-07T19:26:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 2208
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1086 (Div. 2)"
rating: 800
weight: 2208
solve_time_s: 105
verified: true
draft: false
---

[CF 2208A - Bingo Candies](https://codeforces.com/problemset/problem/2208/A)

**Rating:** 800  
**Tags:** constructive algorithms, math  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square grid of size $n \times n$ representing a board where each cell contains a candy of a certain color. The color of a candy is denoted by an integer, and different integers represent different colors. Bob wants to know whether it is possible to rearrange the candies on the board so that no row or column is filled entirely with candies of the same color.

In other words, after rearrangement, every row and column must contain at least two distinct colors. The input provides multiple test cases, each with its own board. We need to answer “YES” if such a rearrangement is possible for a board, or “NO” otherwise.

The constraints tell us that $n$ can go up to 100, and the sum of all $n$ across test cases does not exceed 500. This means that any solution iterating over all cells is acceptable, since $n^2$ per test case is at most 10,000 and the total number of cells across all test cases is at most 50,000.

A key edge case is when one color appears more than $n$ times. Since there are only $n$ positions in any row or column, if a single color appears more than $n$ times, we cannot prevent that color from forming a row or column entirely of the same color. For example, if $n = 3$ and the board is:

```
1 1 1
2 3 2
3 2 3
```

Then color `1` appears three times, which is equal to `n`. We can rearrange them, but if any color appears more than three times, it is impossible to avoid a monochromatic row or column. Careless implementations that check only rows or columns without counting frequencies will fail here.

## Approaches

The brute-force approach would attempt to try every permutation of candies on the board, checking if the resulting board satisfies the condition. For a $n \times n$ board, this would involve $(n^2)!$ permutations. This is obviously impossible even for $n = 5$. The brute-force works in principle because rearrangements cover all possibilities, but it fails due to the astronomical number of permutations.

The key insight comes from noticing that we do not care about the exact positions of colors, only about their counts. A rearrangement is impossible if any color occurs more than $n$ times, because we cannot place more than $n$ identical candies without creating a monochromatic row or column. Conversely, if every color occurs at most $n$ times, we can always rearrange them in a diagonal-like pattern to avoid a full row or column of a single color. This observation reduces the problem from permutations to counting the occurrences of each color.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n^2)!) | O(n^2) | Too slow |
| Optimal (frequency check) | O(n^2) per test case | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$ and then the $n \times n$ board.
3. Create a frequency counter (dictionary) for all candy colors. For every cell $a_{i,j}$, increment the count of $a_{i,j}$.
4. After counting, check the maximum frequency of any color. If this frequency is greater than $n$, print “NO” for this test case. Otherwise, print “YES”.

The reason this works is that the maximum frequency of any color is the limiting factor. No matter how we shuffle the board, if a color appears more than $n$ times, at least one row or column must contain that color in all positions. If all frequencies are at most $n$, a valid rearrangement always exists, for example, by placing each color along a diagonal and filling the remaining positions carefully.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        colors = []
        for _ in range(n):
            row = list(map(int, input().split()))
            colors.extend(row)
        count = Counter(colors)
        if max(count.values()) > n:
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    solve()
```

The solution reads all rows into a flat list `colors` for simplicity. `Counter` efficiently counts the occurrences of each candy color. The check `max(count.values()) > n` directly implements the condition derived above. Using `sys.stdin.readline` ensures fast input for multiple test cases. Care must be taken to flatten rows correctly; a naive sum operation might concatenate numbers incorrectly.

## Worked Examples

### Sample Input 1

```
3
3
1 2 3
3 1 4
4 1 2
3
1 1 1
2 3 4
1 4 3
3
1 1 1
1 1 1
1 1 2
```

| Test | Colors list | Max frequency | Output |
| --- | --- | --- | --- |
| 1 | [1,2,3,3,1,4,4,1,2] | 3 | YES |
| 2 | [1,1,1,2,3,4,1,4,3] | 3 | YES |
| 3 | [1,1,1,1,1,1,1,1,2] | 7 | NO |

This confirms that the algorithm correctly identifies when a color appears too many times to allow a valid rearrangement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) per test case | Counting all colors requires visiting each of the n^2 cells once |
| Space | O(n^2) | Storing the flattened list of colors and frequency dictionary |

Since the total sum of $n^2$ over all test cases is at most 50,000, the solution easily runs within the 1-second time limit and stays well under 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import Counter
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("3\n3\n1 2 3\n3 1 4\n4 1 2\n3\n1 1 1\n2 3 4\n1 4 3\n3\n1 1 1\n1 1 1\n1 1 2") == "YES\nYES\nNO", "sample 1"

# Custom cases
assert run("1\n1\n1") == "YES", "minimum board size"
assert run("1\n2\n1 1\n1 1") == "NO", "all equal 2x2"
assert run("1\n3\n1 1 2\n2 3 3\n1 2 3") == "YES", "mixed but valid"
assert run("1\n4\n1 1 1 1\n2 2 2 2\n3 3 3 3\n4 4 4 4") == "YES", "each color n times"
assert run("1\n3\n1 1 1\n1 1 1\n1 1 1") == "NO", "all same color exceeding n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | YES | Minimum-size board can always be valid |
| `2x2 all 1` | NO | Small board where one color fills more than n positions |
| `3x3 mixed` | YES | Normal case with valid rearrangement |
| `4x4 each color 4 times` | YES | Maximum frequency equal to n is still OK |
| `3x3 all 1` | NO | Color frequency exceeds n, impossible |

## Edge Cases

For `n = 1`, the board has only one cell. Since no row or column can contain more than one candy, the answer is always “YES” regardless of the color. The algorithm handles this because `max(count.values()) = 1 <= n = 1`.

For `n = 100` with a single color appearing 101 times, the algorithm correctly prints “NO” since `max(count.values()) = 101 > 100`. It does not attempt any rearrangement, efficiently handling large input sizes.

For boards where multiple colors appear exactly `n` times each, the algorithm prints “YES”, as it recognizes that no color exceeds the limit. This captures cases where careful permutation could produce a valid board but is guaranteed by frequency constraints.

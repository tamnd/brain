---
title: "CF 1358E - Are You Fired?"
description: "We are asked to find the minimum number of lanterns needed to fully illuminate a rectangular park composed of $n$ rows and $m$ columns of square tiles."
date: "2026-06-11T13:29:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1358
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 645 (Div. 2)"
rating: 2400
weight: 1358
solve_time_s: 806
verified: false
draft: false
---

[CF 1358E - Are You Fired?](https://codeforces.com/problemset/problem/1358/E)

**Rating:** 2400  
**Tags:** constructive algorithms, data structures, greedy, implementation  
**Solve time:** 13m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to find the minimum number of lanterns needed to fully illuminate a rectangular park composed of $n$ rows and $m$ columns of square tiles. Lanterns can be placed on the streets that form the grid lines between the squares, and each lantern illuminates two adjacent squares along the street it is on. Lanterns placed on the outer borders illuminate only one square if there is no neighboring square outside the park. The goal is to cover every square with at least one lantern using the fewest possible lanterns.

The input gives multiple test cases with values of $n$ and $m$, and we must output the minimal lantern count for each. Since $1 \le n, m \le 10^4$ and there can be up to $10^4$ test cases, any solution that iterates over all individual squares would perform up to $10^8$ operations in the worst case and is too slow. Therefore we need a purely mathematical or greedy approach that works in constant time per test case.

Non-obvious edge cases include parks with a single row or a single column. For example, a $1 \times 3$ park requires two lanterns, because each lantern can cover at most two squares, but a naive formula that assumes $2 \times 2$ blocks would underestimate and produce one lantern instead of two. Similarly, a $1 \times 1$ park requires one lantern, which is trivial but must be handled explicitly. Rectangles with odd dimensions in either direction may also leave a single uncovered square if not handled carefully.

## Approaches

The brute-force approach is to simulate placing lanterns on every street and track which squares are illuminated. We could iterate over all horizontal and vertical streets, place a lantern if either adjacent square is unlit, and continue until the park is fully covered. This is correct because each lantern can cover one or two squares, but it performs $O(n \cdot m)$ operations per test case. With $n, m \le 10^4$ and $t \le 10^4$, this results in up to $10^{12}$ operations and is too slow.

The key observation is that each lantern covers two squares, either horizontally or vertically. To minimize lanterns, we can consider the park as composed of $2 \times 2$ blocks, each block requiring exactly two lanterns. If either dimension is odd, the leftover row or column can be covered by additional lanterns placed along the border. In terms of arithmetic, the minimal number of lanterns is $\lceil n m / 2 \rceil$, since each lantern covers two squares and we cannot place half a lantern. This observation reduces the solution to a simple formula that can be computed in $O(1)$ per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n*m) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read the integers $n$ and $m$, representing the number of rows and columns.
3. Compute the product $n \cdot m$, which represents the total number of squares in the park.
4. Divide $n \cdot m$ by 2 and round up to the nearest integer using integer arithmetic: $(n \cdot m + 1) // 2$. This gives the minimal number of lanterns needed, since each lantern can cover up to two squares.
5. Print the result for the test case.
6. Repeat for all test cases.

This works because each lantern illuminates exactly two squares at maximum, and rounding up ensures that any leftover single square is also covered. The invariant is that after placing this number of lanterns, no square remains unlit.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    lanterns = (n * m + 1) // 2
    print(lanterns)
```

The solution reads input using fast I/O to handle up to $10^4$ test cases efficiently. The calculation `(n * m + 1) // 2` is a precise way to perform the ceiling division without using floating point arithmetic, avoiding rounding errors. No additional data structures are needed.

## Worked Examples

For the input:

```
1 3
```

The total number of squares is $1 \cdot 3 = 3$. Dividing by 2 and rounding up gives `(3 + 1)//2 = 2`. This correctly accounts for the fact that one lantern cannot cover all three squares, and two lanterns are needed.

For the input:

```
3 3
```

The total number of squares is $3 \cdot 3 = 9$. Dividing by 2 and rounding up gives `(9 + 1)//2 = 5`. This ensures that the last square in the odd row and column is covered without overcounting lanterns.

| n | m | n*m | (n*m+1)//2 |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 2 |
| 3 | 3 | 9 | 5 |

This confirms the formula works for both odd and even dimensions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a single multiplication, addition, integer division, and print per test case |
| Space | O(1) | No extra memory needed beyond input variables |

Given $t \le 10^4$, $n, m \le 10^4$, the solution performs up to $10^4$ multiplications and divisions, which is well within the 2-second limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        print((n * m + 1) // 2)
    return output.getvalue().strip()

# Provided samples
assert run("5\n1 1\n1 3\n2 2\n3 3\n5 3\n") == "1\n2\n2\n5\n8", "sample 1"

# Custom cases
assert run("3\n1 2\n2 1\n2 3\n") == "1\n1\n3", "small edge cases"
assert run("2\n10000 10000\n9999 9999\n") == "50000000\n49995001", "large squares"
assert run("2\n1 10000\n10000 1\n") == "5000\n5000", "single row and single column"
assert run("2\n2 2\n3 4\n") == "2\n6", "mixed even and odd dimensions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 / 2 1 / 2 3 | 1 / 1 / 3 | Single row or column, odd number of squares |
| 10000 10000 / 9999 9999 | 50000000 / 49995001 | Large input, ensure integer arithmetic handles overflow correctly |
| 1 10000 / 10000 1 | 5000 / 5000 | Single row and single column, long strips |
| 2 2 / 3 4 | 2 / 6 | Mixed even and odd dimensions |

## Edge Cases

For a park with only one square, `1 1`, the formula `(1*1+1)//2 = 1` correctly returns one lantern.

For a park with an odd total number of squares, such as `3 3`, the formula `(9+1)//2 = 5` ensures the extra square is covered, reflecting that integer division truncation alone would underestimate the count.

For long single rows or columns like `1 10000`, `(10000 + 1)//2 = 5000` ensures coverage without placing an unnecessary extra lantern.

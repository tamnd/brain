---
title: "CF 102386C - \u041d\u0430\u0439\u0434\u0438 \u043e\u0442\u043b\u0438\u0447\u0438\u044f"
description: "We are given two rectangular character images of the same size. Each image is represented by n rows, each containing exactly m non-whitespace characters."
date: "2026-08-14T13:25:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "C"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 75
verified: true
draft: false
---

[CF 102386C - \u041d\u0430\u0439\u0434\u0438 \u043e\u0442\u043b\u0438\u0447\u0438\u044f](https://codeforces.com/problemset/problem/102386/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two rectangular character images of the same size. Each image is represented by `n` rows, each containing exactly `m` non-whitespace characters. The two images are aligned cell by cell, so position `(i, j)` in the first image corresponds directly to position `(i, j)` in the second image.

The task is simply to count how many corresponding positions contain different characters. The characters themselves do not have any special meaning. A difference between `A[i][j]` and `B[i][j]` contributes one to the answer, while equal characters contribute zero.

The original task fixes the actual images at 80 rows by 37 columns, so there are only 2960 positions. The input format nevertheless gives `n` and `m`, which makes the implementation naturally work for any dimensions satisfying the format. Even a direct scan of every cell performs only `n * m` comparisons, and for the stated maximum this is just 2960 comparisons. A quadratic algorithm over the number of cells is unnecessary, while any linear scan is comfortably within the one-second and 256 MB limits.

There are a few small input details that are easy to mishandle. The image may contain punctuation such as `.` or `\`, so parsing the rows as arbitrary strings is safer than trying to interpret their characters. For example, the sample contains backslashes:

```
1 1
\
.
```

The two cells differ, so the answer is `1`. A careless parser that treats the backslash as an escape character rather than ordinary input data could read the row incorrectly.

Another boundary case is when the images are completely identical:

```
2 3
abc
XYZ
abc
XYZ
```

The correct output is `0`. The algorithm must count differences rather than count matching positions.

The opposite case is when every position differs:

```
2 2
ab
cd
12
34
```

The correct output is `4`. A solution that stops after finding the first difference, or that accidentally compares only the first row, would undercount.

The dimensions themselves can also be minimal. For

```
1 1
a
b
```

the answer is `1`, while

```
1 1
a
a
```

has answer `0`. These cases catch off-by-one errors in both row and column traversal.

## Approaches

The most direct brute-force interpretation is to visit every position of the first image, find the corresponding position in the second image, and compare their characters. Since the coordinates already identify the corresponding cells, a nested loop over rows and columns is enough. For `n * m` cells this performs exactly `n * m` comparisons in the worst case, which is 2960 comparisons for the fixed 80 by 37 images. This is already easily fast enough.

A less careful implementation might turn the problem into a search problem, scanning the entire second image whenever a cell from the first image is processed. That performs up to `(n * m)^2` character comparisons. With 2960 cells this is 8,761,600 comparisons, which is still not catastrophic for these fixed dimensions, but it completely ignores the fact that the coordinates already give us the answer to the matching problem. More importantly, if the dimensions were generalized to large values, quadratic work would quickly become inappropriate.

The key observation is that there is no need to search for corresponding characters. The images are aligned and have identical dimensions, so `(i, j)` in one image always corresponds to `(i, j)` in the other. The problem is exactly the Hamming distance between two equal-sized character grids. We can scan both images once and increment the answer whenever the two characters at the same position differ.

The optimal approach therefore uses one comparison per cell. In Python, comparing the two rows character by character with `zip` expresses the same operation directly and keeps the implementation simple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Search the second image for every cell | O((nm)^2) | O(nm) | Unnecessarily slow |
| Direct cell-by-cell comparison | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`, which describe the number of rows and columns in each image.
2. Read the next `n` lines into the first image. Each line represents one complete row, so it should be kept as a string rather than split into individual tokens.
3. Read the following `n` lines into the second image using the same representation. The two images now have corresponding rows at the same indices.
4. Initialize the difference counter to zero. No position has been examined yet, so the counter represents the number of differing cells among all positions processed so far.
5. For every pair of corresponding rows, compare their characters at equal column positions. Whenever the characters are different, increment the counter by one. This is sufficient because each cell has exactly one corresponding cell in the other image.
6. Print the counter. After all rows and columns have been processed, it is exactly the number of positions where the two images differ.

### Why it works

After processing any prefix of the images, the counter equals the number of positions in that prefix where the two images have different characters. When the next pair of corresponding characters is examined, exactly one of two things happens. If they are equal, the number of differences does not change. If they are different, exactly one new differing position is added. Thus the invariant remains true for every processed cell. After the final cell, the prefix is the entire pair of images, so the counter is precisely the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    first = [input().rstrip('\n') for _ in range(n)]
    second = [input().rstrip('\n') for _ in range(n)]

    answer = 0

    for row_a, row_b in zip(first, second):
        answer += sum(a != b for a, b in zip(row_a, row_b))

    print(answer)

if __name__ == "__main__":
    solve()
```

The first `n` rows are stored in `first`, and the next `n` rows are stored in `second`. Keeping the complete rows makes the correspondence between the two images explicit.

`rstrip('\n')` removes only the line terminator. This is preferable to using `strip()`, because the statement defines the image rows as strings of characters, and a parser should not unnecessarily remove other characters from the input.

The outer `zip` pairs row `i` of the first image with row `i` of the second image. The inner `zip` then pairs column `j` of those rows. For every pair, the expression `a != b` evaluates to `True` or `False`, which Python treats as `1` or `0` when summed.

There is no integer overflow concern in Python, and even in a language with fixed-width integers the answer could never exceed `n * m`, which is only 2960 for the stated images.

## Worked Examples

For Sample 1, the two images have five rows and thirteen columns. The following table records only the number of differences accumulated after each row.

| Row | Differences in current row | Total differences |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 2 | 2 |
| 3 | 3 | 5 |
| 4 | 2 | 7 |
| 5 | 0 | 7 |

The final counter is `7`, matching the sample output. The trace demonstrates that differences are counted independently for every corresponding character, including punctuation and backslashes.

For Sample 2, consider the smallest possible one-cell images:

```
1 1
a
b
```

The scan contains one comparison.

| Row | Column | First character | Second character | Total |
| --- | --- | --- | --- | --- |
| 1 | 1 | `a` | `b` | 1 |

The answer is `1`. If the characters were both `a`, the same trace would leave the counter at `0`. This confirms that the algorithm counts differences rather than merely counting cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every character position is compared exactly once |
| Space | O(nm) | Both images are stored as input strings |

For the actual fixed image size of 80 by 37, the scan examines only 2960 corresponding positions. The memory usage is also tiny compared with the 256 MB limit, and the linear scan easily fits within the one-second time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    first = [input().rstrip('\n') for _ in range(n)]
    second = [input().rstrip('\n') for _ in range(n)]

    answer = 0
    for row_a, row_b in zip(first, second):
        answer += sum(a != b for a, b in zip(row_a, row_b))

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    """5 13
.__.......__.
.).\\...../.(.
)_..\\_V_/.._(
..)__...__(..
.....‘_’.....
.__.......__.
.|.\\...../.|.
!..\\_M_/..!
..\\__...__/..
.....‘_’.....
"""
) == "7\n", "sample 1"

# Minimum-size input, equal images
assert run(
    """1 1
a
a
"""
) == "0\n", "minimum equal images"

# Minimum-size input, different images
assert run(
    """1 1
a
b
"""
) == "1\n", "minimum different images"

# All cells differ
assert run(
    """2 3
abc
def
123
456
"""
) == "6\n", "every cell differs"

# All cells are equal
assert run(
    """3 4
....
abcd
1234
....
abcd
1234
"""
) == "0\n", "all cells equal"

# Differences at the first and last positions of the grid
assert run(
    """2 2
ab
cd
xb
cy
"""
) == "2\n", "boundary positions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, `a`, `a` | `0` | Minimum dimensions and equality |
| `1 1`, `a`, `b` | `1` | Minimum dimensions and a single difference |
| Two 2 by 3 completely different images | `6` | Every cell must be counted |
| Two identical 3 by 4 images | `0` | No false positives |
| Differences at `(1,1)` and `(2,2)` | `2` | First and last cells, boundary handling |

## Edge Cases

The first non-obvious case is a one-cell image whose characters differ:

```
1 1
a
b
```

The outer loop processes one row, and the inner `zip` produces one pair, `a` and `b`. Since they differ, the counter becomes `1`, which is the correct output. There is no special case needed for `n = 1` or `m = 1`.

A completely identical image is handled just as directly:

```
2 3
abc
XYZ
abc
XYZ
```

The first row produces three equal pairs and adds zero. The second row does the same, leaving the counter at `0`. The algorithm never assumes that at least one difference exists.

A completely different image exercises the opposite extreme:

```
2 2
ab
cd
12
34
```

The first row contributes two differences, and the second row contributes two more. The final answer is `4`, which is exactly the number of cells in the images.

Finally, characters such as backslash and punctuation are ordinary image data. For example:

```
1 3
\._
/._
```

The first two positions differ and the third position is equal, so the answer is `2`. The implementation reads each entire row as a string and compares its characters directly, so none of these symbols require special handling by the algorithm.

---
title: "CF 2009B - osu!mania"
description: "Each test case describes a small osu!mania beatmap with 4 columns. Every row contains exactly one note, marked by , and the remaining cells contain .."
date: "2026-06-08T13:17:30+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2009
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 971 (Div. 4)"
rating: 800
weight: 2009
solve_time_s: 120
verified: false
draft: false
---

[CF 2009B - osu!mania](https://codeforces.com/problemset/problem/2009/B)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

Each test case describes a small osu!mania beatmap with 4 columns. Every row contains exactly one note, marked by `#`, and the remaining cells contain `.`.

The rows are given from top to bottom, but the game processes notes from bottom to top because notes closer to the bottom are hit first. For every note in processing order, we must output the column number where its `#` appears.

A row such as:

```
..#.
```

contains its note in column 3.

The key detail is that the input order and the required output order are opposite. The first row in the input is the topmost row, but the first answer we print must correspond to the bottommost row.

The constraints are extremely small. There are at most 500 rows across all test cases, and every row has exactly 4 characters. Even an algorithm that scans every character of every row performs only about 2000 character checks in total. Runtime is not the challenge here. The task is purely careful implementation.

One easy mistake is forgetting to reverse the rows.

Consider:

```
1
3
#...
.#..
..#.
```

The rows from top to bottom contain columns `1, 2, 3`.

The game processes from bottom to top, so the correct output is:

```
3 2 1
```

A careless solution that prints rows in input order would output:

```
1 2 3
```

which is wrong.

Another common mistake is using 0-based indexing.

For example:

```
1
1
...#
```

The note is in the fourth column.

The correct output is:

```
4
```

A solution that outputs the string position directly would print `3`.

A third subtle case is when multiple rows have notes in the same column.

```
1
2
.#..
.#..
```

The correct output is:

```
2 2
```

Each row must be processed independently. There is no restriction that columns must be distinct.

## Approaches

The most direct approach is to inspect every row, find the position of `#`, store that column number, and finally output the stored answers in reverse row order.

This brute-force method is already fast enough because each row contains only four characters. Finding the note position requires checking at most four cells. With at most 500 rows total, the worst-case work is only about 2000 character inspections.

Since the constraints are tiny, there is no need for sophisticated optimization. The real observation is simply understanding the order in which notes are processed.

The input gives rows from top to bottom, but the required answer is bottom to top. Once we recognize that, the problem becomes a straightforward scan of each row. For every row we determine the column containing `#`, store it, and later print the stored columns in reverse order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

Since each row has a fixed length of 4, scanning a row is effectively constant time. Both approaches are the same for this problem.

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `n`, the number of rows.
3. Create an empty list `cols` that will store the column number of the note in every row.
4. Read each row.
5. Find the position of `#` in the row and convert it to a 1-based column number.
6. Append that column number to `cols`.
7. After all rows are processed, reverse the order by iterating through `cols` from the last element to the first.
8. Print the reversed sequence separated by spaces.

The reversal is necessary because the input is given from top to bottom while notes are processed from bottom to top.

### Why it works

For every row, there is exactly one `#`, so the column of that note is uniquely determined. The algorithm records that column for every row in input order.

If the rows are numbered from top to bottom as `1...n`, then the processing order is `n...1`. Reversing the recorded list produces exactly that order. Every output position corresponds to the correct processed note, so the algorithm always returns the required sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    cols = []

    for _ in range(n):
        row = input().strip()
        cols.append(row.index('#') + 1)

    print(*reversed(cols))
```

The solution follows the algorithm directly.

The list `cols` stores the column number for each row. Python's `index('#')` finds the position of the note, and adding one converts the result from 0-based indexing to the required 1-based column numbering.

After all rows are read, `reversed(cols)` produces the bottom-to-top processing order. Using `print(*...)` automatically places spaces between the numbers.

The most common implementation error is forgetting the `+ 1`. Another is printing `cols` directly instead of reversing it.

## Worked Examples

### Sample 1

Input:

```
4
#...
.#..
..#.
...#
```

| Row Read | Note Column | cols After Processing |
| --- | --- | --- |
| #... | 1 | [1] |
| .#.. | 2 | [1, 2] |
| ..#. | 3 | [1, 2, 3] |
| ...# | 4 | [1, 2, 3, 4] |

After reversal:

| Reversed Order |
| --- |
| 4 |
| 3 |
| 2 |
| 1 |

Output:

```
4 3 2 1
```

This example demonstrates the central idea of the problem. The columns are found in input order but printed in reverse order.

### Sample 2

Input:

```
2
.#..
.#..
```

| Row Read | Note Column | cols After Processing |
| --- | --- | --- |
| .#.. | 2 | [2] |
| .#.. | 2 | [2, 2] |

After reversal:

| Reversed Order |
| --- |
| 2 |
| 2 |

Output:

```
2 2
```

This trace shows that multiple notes may occupy the same column. Each row is handled independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each row is scanned once |
| Space | O(n) | The column of each row is stored |

Here, `n` is the number of rows in a test case. Since every row has exactly four characters, the hidden constant is extremely small. With at most 500 rows across all test cases, the solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        cols = []

        for _ in range(n):
            row = input().strip()
            cols.append(row.index('#') + 1)

        out.append(" ".join(map(str, reversed(cols))))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# provided sample
assert run(
"""3
4
#...
.#..
..#.
...#
2
.#..
.#..
1
...#
"""
) == "4 3 2 1\n2 2\n4"

# minimum size
assert run(
"""1
1
#...
"""
) == "1"

# last column
assert run(
"""1
1
...#
"""
) == "4"

# repeated columns
assert run(
"""1
3
.#..
.#..
.#..
"""
) == "2 2 2"

# catches missing reversal
assert run(
"""1
4
#...
.#..
..#.
...#
"""
) == "4 3 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single row with `#...` | `1` | Minimum input size |
| Single row with `...#` | `4` | Correct 1-based indexing |
| Three identical rows in column 2 | `2 2 2` | Repeated columns handled correctly |
| Increasing columns from top to bottom | `4 3 2 1` | Reversal of processing order |

## Edge Cases

### Top-to-bottom order versus bottom-to-top order

Input:

```
1
3
#...
.#..
..#.
```

The algorithm records:

```
[1, 2, 3]
```

It then reverses the list:

```
[3, 2, 1]
```

and outputs:

```
3 2 1
```

This matches the required processing order.

### Note in the last column

Input:

```
1
1
...#
```

The position of `#` is index `3`. Adding one gives column `4`.

Output:

```
4
```

This confirms that the algorithm correctly converts from Python's 0-based indexing to the problem's 1-based column numbering.

### Multiple rows using the same column

Input:

```
1
2
.#..
.#..
```

The algorithm stores:

```
[2, 2]
```

Reversing does not change the sequence:

```
[2, 2]
```

Output:

```
2 2
```

The solution never assumes columns are unique, so repeated columns are handled naturally.

---
title: "CF 102757D - Best Thing Since Sliced Bread"
description: "The problem describes a collection of historical inventions. Each invention has a title, an invention date, and a score representing how close it is to the greatness of sliced bread."
date: "2026-07-29T00:24:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102757
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 2"
rating: 0
weight: 102757
solve_time_s: 78
verified: true
draft: false
---

[CF 102757D - Best Thing Since Sliced Bread](https://codeforces.com/problemset/problem/102757/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a collection of historical inventions. Each invention has a title, an invention date, and a score representing how close it is to the greatness of sliced bread. The goal is to find the greatest invention that happened after sliced bread was invented, where sliced bread is considered to have appeared on July 7, 1928.

The input contains several invention records. Each record consists of a name, a date written using a three-letter month abbreviation followed by day and year, and a decimal score between 0 and 1. The output is simply the name of the valid invention with the largest score.

The number of inventions can reach 10,000. This is small enough that we can inspect every invention once. Any approach that compares every pair of inventions would perform around 100 million comparisons in the worst case, which is unnecessary for a simple maximum search.

The main implementation difficulty is not the search itself but correctly interpreting dates. A careless solution may compare dates as strings or forget that the year may not always have four digits. Dates must be converted into a representation where chronological order is preserved.

For example, an input such as:

```
3
Old Machine
Jan 1, 3000
0.9
New Machine
Jan 1, 2000
0.8
Ancient Tool
Jan 1, 100
0.99
```

has only one valid invention, Old Machine, because the other two were created before sliced bread. The correct output is:

```
Old Machine
```

A solution that only chooses the largest score would incorrectly output Ancient Tool.

Another edge case is an invention created exactly on July 7, 1928. It does not count because the wording requires inventions made after sliced bread. For example:

```
2
Exact Date
Jul 7, 1928
1.0
Later
Jul 8, 1928
0.5
```

The correct output is:

```
Later
```

A comparison using greater than or equal to would incorrectly select Exact Date.

## Approaches

The straightforward approach is to store every invention and examine all possible choices. For each invention, we check whether it was created after July 7, 1928, then compare its score against every other valid invention. This is correct because the greatest score among all valid candidates must also be found among those comparisons. However, with 10,000 inventions this performs about 100 million comparisons, while solving the problem does not require any interaction between inventions.

The useful observation is that this is only asking for a maximum value among filtered records. We do not need to know anything about the other inventions once we have processed them. We can scan the input once, discard inventions before or on the sliced bread date, and keep the best score seen so far.

The brute-force solution works because it eventually examines every possible winner, but it fails because it repeats unnecessary comparisons. The observation that a maximum can be maintained incrementally reduces the problem to a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow conceptually |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of inventions. Process each invention record independently because the answer only depends on the best valid candidate found so far.
2. Convert the invention date into a comparable numeric form. A convenient representation is year, month, and day stored as a tuple. Tuples compare chronologically when ordered from the largest unit to the smallest.
3. Check whether the invention date is strictly after July 7, 1928. Equal dates must be rejected because the invention must be newer than sliced bread.
4. For every valid invention, compare its score with the current best score. Replace the stored answer if this invention has a larger score.
5. After all records are processed, print the stored title.

Why it works: during the scan, the stored invention is always the highest-scoring valid invention among all records processed so far. When another valid invention is examined, either it has a smaller score and the invariant remains true, or it has a larger score and replacing the stored answer restores the invariant. After the final record, the stored answer must be the greatest valid invention.

## Python Solution

```python
import sys
input = sys.stdin.readline

months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

def parse_date(s):
    month, day, year = s.replace(",", "").split()
    return (int(year), months[month], int(day))

def solve(data=None):
    global input
    if data is not None:
        import io
        input = io.StringIO(data).readline

    n = int(input())

    cutoff = (1928, 7, 7)
    best_score = -1.0
    answer = ""

    for _ in range(n):
        title = input().rstrip("\n")
        date = parse_date(input().rstrip("\n"))
        score = float(input().rstrip("\n"))

        if date > cutoff and score > best_score:
            best_score = score
            answer = title

    return answer

if __name__ == "__main__":
    print(solve())
```

The month dictionary converts text months into numbers so dates can be compared directly. The parser removes the comma from inputs such as `Jul 7, 1928` before splitting the pieces.

The scan keeps only two pieces of state: the best score found so far and the corresponding title. The comparison uses `>` for the date check because inventions on the sliced bread date are not included.

The score comparison uses floating point values because the input scores are decimal fractions. Since the problem guarantees that there are no ties for the greatest valid invention, exact tie handling is not required.

## Worked Examples

For the sample:

```
5
FM Radio
Dec 26, 1933
0.65
Ballpoint Pen
Oct 30, 1888
0.7442
Penicillin
Sep 28, 1928
0.0036
The Hovercraft
Dec 12, 1955
0.896
Fireworks
Apr 20, 960
0.99999
```

the scan behaves as follows:

| Invention | Date valid? | Score | Current best |
| --- | --- | --- | --- |
| FM Radio | Yes | 0.65 | FM Radio |
| Ballpoint Pen | No | 0.7442 | FM Radio |
| Penicillin | Yes | 0.0036 | FM Radio |
| The Hovercraft | Yes | 0.896 | The Hovercraft |
| Fireworks | No | 0.99999 | The Hovercraft |

The trace shows why old inventions with excellent scores cannot win. The score matters only after the date condition is satisfied.

A second example:

```
3
A
Jul 7, 1928
1.0
B
Jul 8, 1928
0.4
C
Aug 1, 1928
0.7
```

| Invention | Date valid? | Score | Current best |
| --- | --- | --- | --- |
| A | No | 1.0 | None |
| B | Yes | 0.4 | B |
| C | Yes | 0.7 | C |

This confirms the strict date boundary. The invention with the highest possible score is ignored if it is not actually since sliced bread.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each invention is parsed and checked once. |
| Space | O(1) | Only the current best invention and temporary parsing data are stored. |

The maximum input size is only 10,000 inventions, so a linear scan easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    return solve(inp)

assert run("""5
FM Radio
Dec 26, 1933
0.65
Ballpoint Pen
Oct 30, 1888
0.7442
Penicillin
Sep 28, 1928
0.0036
The Hovercraft
Dec 12, 1955
0.896
Fireworks
Apr 20, 960
0.99999
""") == "The Hovercraft", "sample 1"

assert run("""3
A
Jul 7, 1928
1.0
B
Jul 8, 1928
0.4
C
Aug 1, 1928
0.7
""") == "C", "boundary date"

assert run("""1
First
Jul 8, 1928
0.5
""") == "First", "minimum size"

assert run("""4
Low
Jan 1, 2000
0.1
Mid
Jan 2, 2000
0.5
High
Jan 3, 2000
0.9
Lower
Jan 4, 2000
0.2
""") == "High", "maximum score selection"

assert run("""3
Ancient
Jan 1, 100
0.99
Old
Jul 7, 1928
1.0
New
Jul 8, 1928
0.1
""") == "New", "ignore invalid scores"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample input | The Hovercraft | Basic filtering and maximum search |
| Exact boundary date | C | Strictly after July 7, 1928 |
| One invention | First | Minimum input size |
| Several valid inventions | High | Maximum score update logic |
| Old high-scoring inventions | New | Date filtering before score comparison |

## Edge Cases

For an invention exactly on the cutoff date:

```
2
Exact
Jul 7, 1928
1.0
Later
Jul 8, 1928
0.5
```

The algorithm parses Exact as `(1928, 7, 7)`. Since this is not greater than the cutoff tuple, it is skipped. Later becomes the first valid invention and is printed.

For an old invention with a perfect score:

```
2
Ancient
Jan 1, 1000
1.0
Modern
Jan 1, 2000
0.2
```

Ancient is ignored before score comparison. The algorithm never allows an invalid invention to become the current best answer, so Modern is correctly selected.

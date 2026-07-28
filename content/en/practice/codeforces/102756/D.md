---
title: "CF 102756D - Best Thing Since Sliced Bread"
description: "The problem asks us to examine a collection of historical inventions. Each invention has a name, an invention date, and a score representing how great it is compared with sliced bread."
date: "2026-07-29T00:30:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102756
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 1"
rating: 0
weight: 102756
solve_time_s: 74
verified: true
draft: false
---

[CF 102756D - Best Thing Since Sliced Bread](https://codeforces.com/problemset/problem/102756/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to examine a collection of historical inventions. Each invention has a name, an invention date, and a score representing how great it is compared with sliced bread. We need to find the greatest invention among only the inventions created after sliced bread, which is considered to have been invented on July 7, 1928. The answer is the name of the invention with the largest score among those eligible inventions.

The input contains up to 10,000 invention descriptions. Each description occupies three lines: the invention title, the date in a human-readable month format, and a decimal score. Since the number of inventions is only 10,000, a linear scan is easily fast enough. Any approach that compares every pair of inventions would perform around 100 million comparisons in the worst case, which is unnecessary for such a simple selection problem.

The main difficulty is not the size of the data but correctly handling dates and filtering. A common mistake is to choose the largest score immediately while reading, without checking whether the invention happened after sliced bread. Another mistake is to compare the date strings directly. For example, the dates "Dec 1, 1930" and "Jan 1, 1931" do not sort correctly as strings because month names are not ordered chronologically.

An edge case occurs when the highest score belongs to an invention before sliced bread. Consider this input:

```
3
Ancient Fire
Apr 20, 960
0.99999
Radio
Dec 26, 1933
0.65
Hovercraft
Dec 12, 1955
0.896
```

The correct output is:

```
Hovercraft
```

A careless implementation that only tracks the maximum score would incorrectly print "Ancient Fire". The date filter must happen before comparing scores.

Another edge case is an invention created exactly on July 7, 1928. That invention is not considered to be since sliced bread, because only dates after that day qualify. For example:

```
2
Exact Date
Jul 7, 1928
1.0
Future Item
Jan 1, 1929
0.5
```

The output must be:

```
Future Item
```

The score comparison should only happen after confirming the invention is strictly later than the reference date.

## Approaches

The straightforward solution is to inspect every invention and keep the best eligible one found so far. This is correct because the answer is simply the maximum score among a filtered set. For each invention, we first check whether its date is after July 7, 1928. If it is, we compare its score with the current best score and replace the answer when necessary.

A brute-force approach could compare every invention with every other eligible invention to determine which one has the greatest score. This would still be correct, but with 10,000 inventions it could require about 100 million score comparisons. It also ignores the fact that finding a maximum does not require knowing the relationship between every pair of elements.

The key observation is that the problem has no interactions between inventions. The choice of the best invention depends only on each individual invention's eligibility and score. This allows us to maintain a single running maximum while reading the input. The date parsing converts each date into a numeric representation, making chronological comparison reliable.

The brute-force method works because it eventually discovers the maximum, but fails because it repeats unnecessary comparisons. The observation that a maximum can be maintained incrementally reduces the entire task to one pass through the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow for the general case |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of inventions and initialize variables to store the best score and the corresponding title.
2. Process each invention one at a time. Read its title, date, and score because storing all inventions is unnecessary.
3. Convert the date into a comparable numeric form. The month name is converted into its month number, and the date becomes a tuple containing year, month, and day. This representation follows chronological ordering naturally.
4. Check whether the invention date is strictly greater than July 7, 1928. If it is not, ignore this invention because it does not qualify.
5. For every qualifying invention, compare its score with the current best score. If the score is larger, update the stored answer.
6. After all inventions have been processed, print the stored title.

The reason a single stored answer is enough is that after processing any prefix of the input, the stored invention is always the best valid invention seen in that prefix. When another invention is processed, either it is worse and the current answer remains correct, or it is better and replacing the answer restores the same property.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
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

    sliced_bread_date = (1928, 7, 7)

    best_score = -1.0
    best_title = ""

    for _ in range(n):
        title = input().rstrip("\n")
        date_line = input().strip()
        score = float(input().strip())

        month, day_year = date_line.split(" ", 1)
        day, year = day_year.replace(",", "").split()

        date = (int(year), months[month], int(day))

        if date > sliced_bread_date and score > best_score:
            best_score = score
            best_title = title

    print(best_title)

if __name__ == "__main__":
    solve()
```

The month dictionary turns textual months into integers, which makes date comparison independent of string ordering. The tuple format `(year, month, day)` works because Python compares tuple elements from left to right, matching the order used in normal calendar comparisons.

The score is stored as a floating-point number because the input gives decimal ratings. Since there are no ties for the greatest valid invention, a simple strict comparison is enough. The initial score of `-1.0` guarantees that the first valid invention will replace the placeholder.

The date condition uses `>` rather than `>=`. This handles the boundary rule correctly because an invention on July 7, 1928 is not considered newer than sliced bread.

The algorithm never stores the complete list of inventions. It only keeps the current best title and score, which keeps memory usage constant.

## Worked Examples

For the sample input:

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

the trace is:

| Title | Date | Eligible? | Score | Current Best |
| --- | --- | --- | --- | --- |
| FM Radio | Dec 26, 1933 | Yes | 0.65 | FM Radio |
| Ballpoint Pen | Oct 30, 1888 | No | 0.7442 | FM Radio |
| Penicillin | Sep 28, 1928 | Yes | 0.0036 | FM Radio |
| The Hovercraft | Dec 12, 1955 | Yes | 0.896 | The Hovercraft |
| Fireworks | Apr 20, 960 | No | 0.99999 | The Hovercraft |

This trace demonstrates why filtering must happen before comparing scores. Fireworks has the largest score, but it cannot win because it predates sliced bread.

A second example:

```
4
Old Device
Jul 6, 1928
0.99
Boundary Device
Jul 7, 1928
0.98
New Device
Jul 8, 1928
0.5
Later Device
Jan 1, 1930
0.8
```

The trace is:

| Title | Date | Eligible? | Score | Current Best |
| --- | --- | --- | --- | --- |
| Old Device | Jul 6, 1928 | No | 0.99 | None |
| Boundary Device | Jul 7, 1928 | No | 0.98 | None |
| New Device | Jul 8, 1928 | Yes | 0.5 | New Device |
| Later Device | Jan 1, 1930 | Yes | 0.8 | Later Device |

This trace confirms the strict date comparison and shows that an eligible invention can start the answer even if earlier inventions have larger scores.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each invention is read and processed once |
| Space | O(1) | Only the current best invention and helper data are stored |

With at most 10,000 inventions, the linear solution uses far fewer operations than the available time limit requires. The memory usage remains constant regardless of the number of inventions.

## Test Cases

```python
import sys
import io

def solve(data):
    input = io.StringIO(data).readline

    n = int(input())

    months = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }

    sliced_bread_date = (1928, 7, 7)
    best_score = -1.0
    best_title = ""

    for _ in range(n):
        title = input().rstrip("\n")
        date_line = input().strip()
        score = float(input().strip())

        month, rest = date_line.split(" ", 1)
        day, year = rest.replace(",", "").split()
        date = (int(year), months[month], int(day))

        if date > sliced_bread_date and score > best_score:
            best_score = score
            best_title = title

    return best_title + "\n"

assert solve("""5
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
""") == "The Hovercraft\n"

assert solve("""1
Modern Thing
Jan 1, 2020
0.1
""") == "Modern Thing\n"

assert solve("""3
Old
Jan 1, 1900
0.9
Equal Boundary
Jul 7, 1928
1.0
New
Jul 8, 1928
0.2
""") == "New\n"

assert solve("""3
A
Jan 1, 2000
0.5
B
Jan 1, 2001
0.5
C
Jan 1, 2002
0.7
""") == "C\n"

assert solve("""2
First
Jul 8, 1928
0.01
Second
Dec 31, 1928
0.02
""") == "Second\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Original sample | The Hovercraft | Basic filtering and maximum selection |
| Single modern invention | Modern Thing | Minimum input size |
| Invention on Jul 7, 1928 | New | Boundary date handling |
| Several close scores | C | Maximum update logic |
| Multiple inventions after sliced bread | Second | Correct replacement order |

## Edge Cases

The first tricky case is when an older invention has a very high score. For the input:

```
3
Ancient Fire
Apr 20, 960
0.99999
Radio
Dec 26, 1933
0.65
Hovercraft
Dec 12, 1955
0.896
```

the algorithm first rejects Ancient Fire because its date tuple is `(960, 4, 20)`, which is smaller than `(1928, 7, 7)`. It then compares the two valid inventions and keeps Hovercraft because `0.896` is greater than `0.65`.

The second case is the exact sliced bread date:

```
2
Exact Date
Jul 7, 1928
1.0
Future Item
Jan 1, 1929
0.5
```

The first invention produces the tuple `(1928, 7, 7)`, which is equal to the reference date, so the strict comparison rejects it. The second invention produces `(1929, 1, 1)` and becomes the answer. This prevents the boundary condition from being handled incorrectly.

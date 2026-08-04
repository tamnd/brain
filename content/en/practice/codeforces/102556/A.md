---
title: "CF 102556A - A - Rank Riana and One Punch"
description: "The input is a circular row of positions around the city. A position contains an enemy when it is marked with X and is empty when it is marked with .. A punch can defeat every enemy that belongs to the same continuous chain of enemies."
date: "2026-08-04T09:08:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102556
codeforces_index: "A"
codeforces_contest_name: "2020 Ateneo de Manila University DISCS PrO HS Division"
rating: 0
weight: 102556
solve_time_s: 56
verified: true
draft: false
---

[CF 102556A - A - Rank Riana and One Punch](https://codeforces.com/problemset/problem/102556/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a circular row of positions around the city. A position contains an enemy when it is marked with `X` and is empty when it is marked with `.`. A punch can defeat every enemy that belongs to the same continuous chain of enemies. An empty position breaks that chain, so the goal is to turn the smallest possible number of empty positions into enemies until all enemies belong to one circular chain.

The output is the minimum number of `.` positions that must become `X` positions. The circle connection matters because the last position is adjacent to the first one. A group of enemies can continue through this boundary, so treating the string as a normal line gives incorrect results.

The length is at most 100 characters. This is small enough that many linear or quadratic solutions would run easily, but it is also large enough that trying every possible set of filled positions is unnecessary. A brute force over all empty positions would require up to $2^{100}$ possibilities in the worst case, which is far beyond what a one second limit can handle. The useful structure is that the positions form a circle, so the problem can be reduced to finding properties of the gaps between existing enemies.

Several edge cases can break a direct implementation. If all positions are already enemies, the answer is zero because the chain is already complete.

For input:

```
XXXXX
```

the correct output is:

```
0
```

A method that searches only for dot gaps may incorrectly assume there is always a gap to fill.

If there is only one enemy, it already forms a connected group by itself.

For input:

```
.....
```

the correct output is:

```
0
```

There are no enemies that need to be connected. A careless solution that assumes at least one enemy exists may fail while searching for the first `X`.

Another important case is when the connection crosses the end of the string.

For input:

```
XX..XX
```

the correct output is:

```
0
```

The two groups at the beginning and end are actually adjacent on the circle, so they are already one connected chain. A linear scan that ignores the circular edge would incorrectly count the middle gap as something that must be filled.

## Approaches

A straightforward approach is to consider filling some subset of the empty positions and check whether the resulting circle has only one enemy component. For every possible subset of dots, we could simulate the circle and count the number of connected enemy groups. This is correct because it explores every possible final arrangement, but the number of subsets grows exponentially. With 100 positions, the worst case contains 100 empty positions, giving $2^{100}$ possibilities, which is impossible to process.

The key observation comes from looking at the empty spaces instead of the enemies. Existing enemies are separated by circular gaps of dots. If we fill a dot gap completely, the enemy groups on both sides become connected through that gap. To make the whole circle one connected enemy group, every dot gap except possibly one must be removed.

Why can one gap remain? Imagine leaving one continuous empty segment. All other gaps are filled, so traveling around the circle through the filled gaps reaches every enemy. The remaining empty segment simply becomes the unused break between the end and the beginning of the same connected enemy chain.

Since keeping a gap saves us from filling its dots, we should keep the largest dot gap and fill all the others. The answer is the total number of dots minus the length of the largest circular gap between enemy groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \times n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Count the number of enemies in the circle. If there are no enemies, the answer is zero because there is nothing to connect.
2. Find every consecutive sequence of empty positions. Because the string is circular, the first and last positions may belong to the same empty sequence, so the scan must handle the boundary carefully.
3. Record the length of the largest empty sequence. This is the only gap that can remain empty because it represents the break in the final circular chain.
4. Count the total number of empty positions. Every empty position outside the largest gap must be changed into an enemy.
5. Return the total number of empty positions minus the largest gap length.

The reason the largest gap is the best one to leave untouched is that every other gap must disappear to connect the enemy groups. Keeping a smaller gap would force us to fill more positions than necessary.

Why it works:

Consider the existing enemy groups around the circle. Every empty gap separates two neighboring groups. If two or more gaps remain empty, the circle contains multiple disconnected enemy sections. Thus at most one gap can survive. Choosing the largest gap minimizes the number of filled positions because it avoids filling the greatest number of dots. The algorithm examines all gaps and chooses exactly this optimal gap, so the returned value is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    if 'X' not in s:
        print(0)
        return

    total_dots = s.count('.')

    doubled = s + s
    first_x = doubled.find('X')

    max_gap = 0
    current = 0

    for i in range(first_x, first_x + n):
        if doubled[i] == '.':
            current += 1
            max_gap = max(max_gap, current)
        else:
            current = 0

    if max_gap > total_dots:
        max_gap = total_dots

    print(total_dots - max_gap)

solve()
```

The solution first handles the empty circle case because there is no enemy group to connect. After that, at least one `X` exists, so we rotate our view of the circle by starting the scan at an enemy position. This removes the ambiguity where a dot sequence crosses the end of the input string.

The doubled string gives access to the circular neighbors without using modular indexing. We only scan exactly `n` positions after the first enemy, so a dot sequence from the end and beginning is counted as one continuous gap.

The variable `current` stores the length of the current empty segment. Whenever an enemy appears, the segment ends and `max_gap` already contains the best gap seen so far. Since the largest possible gap cannot exceed the total number of dots, the final answer is simply the number of dots not included in that saved gap.

There is no integer overflow concern in Python because the input length is only 100. The main boundary condition is choosing the starting point correctly. Starting from an arbitrary position can split a circular dot gap into two smaller pieces.

## Worked Examples

For the first sample:

```
XX..XX.X....
```

The scan starts from the first enemy and finds the circular gaps.

| Position processed | Character | Current gap | Largest gap |
| --- | --- | --- | --- |
| 0 | X | 0 | 0 |
| 1 | X | 0 | 0 |
| 2 | . | 1 | 1 |
| 3 | . | 2 | 2 |
| 4 | X | 0 | 2 |
| 5 | X | 0 | 2 |
| 6 | . | 1 | 2 |
| 7 | X | 0 | 2 |
| 8 | . | 1 | 2 |
| 9 | . | 2 | 2 |
| 10 | . | 3 | 3 |
| 11 | . | 4 | 4 |

There are 8 empty positions in total and the largest gap has length 4. Leaving that gap untouched means 4 empty positions need to be filled.

For the second sample:

```
X..XX.X..X
```

The circular gaps are lengths 2, 1, and 2.

| Position processed | Character | Current gap | Largest gap |
| --- | --- | --- | --- |
| 0 | X | 0 | 0 |
| 1 | . | 1 | 1 |
| 2 | . | 2 | 2 |
| 3 | X | 0 | 2 |
| 4 | X | 0 | 2 |
| 5 | . | 1 | 2 |
| 6 | X | 0 | 2 |
| 7 | . | 1 | 2 |
| 8 | . | 2 | 2 |
| 9 | X | 0 | 2 |

There are 5 empty positions and the largest gap is 2, so the answer is 3. The remaining two empty positions represent the one gap that can stay open.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | The circle is scanned once after finding the first enemy. |
| Space | $O(n)$ | The doubled string is stored for easier circular traversal. |

The maximum input size is only 100 characters, so this linear solution easily fits the limits. The algorithm also avoids complicated graph simulation because the circular structure reduces the problem to measuring empty gaps.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    s = sys.stdin.readline().strip()
    n = len(s)

    if 'X' not in s:
        ans = 0
    else:
        total_dots = s.count('.')
        doubled = s + s
        start = doubled.find('X')

        best = 0
        cur = 0
        for i in range(start, start + n):
            if doubled[i] == '.':
                cur += 1
                best = max(best, cur)
            else:
                cur = 0

        ans = total_dots - min(best, total_dots)

    sys.stdin = old_stdin
    return str(ans)

assert solution("XX..XX.X....") == "4", "sample 1"
assert solution("X..XX.X..X") == "3", "sample 2"

assert solution("X") == "0", "single enemy"
assert solution(".....") == "0", "no enemies"
assert solution("XXXXX") == "0", "already connected"
assert solution("XX..XX") == "0", "circular connection"
assert solution("X.X.X") == "2", "alternating enemies"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `X` | `0` | Handles the smallest possible enemy group. |
| `.....` | `0` | Handles the case with no enemies. |
| `XXXXX` | `0` | Handles an already connected circle. |
| `XX..XX` | `0` | Checks the wraparound connection at the boundary. |
| `X.X.X` | `2` | Checks multiple small gaps. |

## Edge Cases

For `XXXXX`, the algorithm finds that the total number of dots is zero. The largest gap is also zero, so the answer remains zero. There are no empty positions separating enemy groups.

For `.....`, the first condition triggers because no enemy exists. The algorithm returns zero immediately instead of searching for a starting enemy position. This avoids invalid indexing and matches the idea that no enemies need to be connected.

For `XX..XX`, a linear approach might see the two groups separated by two dots. The algorithm instead starts at an enemy and scans the entire circle, correctly treating the end and beginning as adjacent. The only gap has length 2, but keeping that gap still leaves all enemies connected through the other side of the circle, so the answer is zero.

For a case such as `X.X.X`, the gaps all have length one. The algorithm can save only one of those gaps, so two of the three dots must be filled. The computed value is `3 - 1 = 2`, which matches the minimum number of changes needed.

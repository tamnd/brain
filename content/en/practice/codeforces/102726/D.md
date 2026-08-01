---
title: "CF 102726D - Zoom Clumps"
description: "The problem models a row of people in a video call. After everyone has turned their head, each person is represented by a character: L if they face left and R if they face right. A clump is a maximal consecutive group of people facing the same direction."
date: "2026-08-01T22:06:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102726
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 9-11-20 Div. 1"
rating: 0
weight: 102726
solve_time_s: 94
verified: true
draft: false
---

[CF 102726D - Zoom Clumps](https://codeforces.com/problemset/problem/102726/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem models a row of people in a video call. After everyone has turned their head, each person is represented by a character: `L` if they face left and `R` if they face right. A clump is a maximal consecutive group of people facing the same direction. The task is to count how many such groups exist in the final row.

For example, the row `R L L R` contains three clumps: the first `R`, the middle `LL`, and the last `R`.

The input contains the number of people followed by their directions in order. The output is the number of contiguous segments in this sequence where every character inside a segment is identical.

The constraint allows up to 100,000 people. That means the solution should work in linear time. Algorithms that repeatedly compare many pairs of positions or try every possible segment can easily reach around 10^10 operations, which is far beyond what is possible in a typical contest time limit. A single scan over the row is enough because every person only needs to influence the answer once.

The main edge cases come from transitions between clumps. A row containing only one person must still create one clump. For the input:

```
1
L
```

the correct output is:

```
1
```

A solution that only counts changes between neighboring people would return zero because there are no transitions, but the first clump must be counted.

Another common mistake is forgetting that equal adjacent directions belong to the same clump. For:

```
4
L
L
L
L
```

the correct output is:

```
1
```

The entire row is one clump. Counting every occurrence of `L` or `R` separately would incorrectly produce four.

A final boundary case is when every adjacent pair is different:

```
4
L
R
L
R
```

The correct output is:

```
4
```

Every person starts a new clump, so the answer is the number of people.

## Approaches

The brute-force approach is to examine every possible contiguous group and determine whether it is a clump. Since there are O(N^2) possible segments and checking a segment can take O(N), the total work can reach O(N^3). Even a slightly improved brute-force that checks only neighboring positions for each segment still considers O(N^2) ranges, which becomes too slow when N reaches 100,000.

The key observation is that clumps are separated exactly at positions where the direction changes. We do not need to know the contents of an entire segment. We only need to know whether the current person continues the previous clump or starts a new one.

The row always contains at least one clump. We start with one clump for the first person, then increase the answer whenever a person faces a different direction from the person immediately before them. This reduces the problem to one left-to-right scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) or worse | O(1) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the directions of all people in their original order.
2. Initialize the answer to one because the first person always belongs to a clump.
3. Scan the row from the second person onward. Whenever the current direction differs from the previous direction, increment the number of clumps. A direction change is the only event that can create a new clump.
4. Output the final count.

Why it works:

During the scan, the current answer represents exactly the number of maximal groups among the people processed so far. The first person creates the first group. Each later person either joins the previous group when their direction matches, or starts a new group when their direction changes. Since every possible boundary between clumps is checked exactly once, the final count is correct.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n = int(input())
    prev = input().strip()
    
    ans = 1

    for _ in range(n - 1):
        cur = input().strip()
        if cur != prev:
            ans += 1
        prev = cur

    print(ans)

if __name__ == "__main__":
    solve()
```

The code keeps only the previous direction instead of storing the whole row. This is enough because a new clump can only be created by comparing two adjacent people.

The variable `ans` starts at one because the input is guaranteed to contain at least one person. The loop begins from the second person, and every direction change increases the answer.

Using `strip()` removes the newline character from each input line. The code avoids unnecessary memory usage by processing directions as they are read.

## Worked Examples

For the sample input:

```
4
R
L
L
R
```

the execution is:

| Person | Direction | Previous Direction | Clumps |
| --- | --- | --- | --- |
| 1 | R | R | 1 |
| 2 | L | R | 2 |
| 3 | L | L | 2 |
| 4 | R | L | 3 |

The answer is `3`. The trace shows that only changes between adjacent people affect the count.

Another example:

```
5
L
L
R
R
L
```

| Person | Direction | Previous Direction | Clumps |
| --- | --- | --- | --- |
| 1 | L | L | 1 |
| 2 | L | L | 1 |
| 3 | R | L | 2 |
| 4 | R | R | 2 |
| 5 | L | R | 3 |

The three clumps are `LL`, `RR`, and `L`. Equal neighbors do not create extra groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each person is processed once. |
| Space | O(1) | Only the previous direction and the current count are stored. |

The linear solution easily handles 100,000 people because it performs a constant amount of work per input character.

## Test Cases

```python
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    n = int(input())
    prev = input().strip()
    ans = 1

    for _ in range(n - 1):
        cur = input().strip()
        if cur != prev:
            ans += 1
        prev = cur

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return output

assert run("4\nR\nL\nL\nR\n") == "3\n", "sample 1"
assert run("1\nL\n") == "1\n", "single person"
assert run("5\nL\nL\nL\nL\nL\n") == "1\n", "all equal values"
assert run("4\nL\nR\nL\nR\n") == "4\n", "alternating directions"
assert run("6\nR\nR\nL\nL\nR\nR\n") == "3\n", "multiple boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 L` | `1` | Minimum size and initial count handling |
| `L L L L L` | `1` | All values equal |
| `L R L R` | `4` | Every person creates a new clump |
| `R R L L R R` | `3` | Correct handling of several transitions |

## Edge Cases

For a single person:

```
1
L
```

the algorithm initializes `ans` to one and performs no comparisons. The output is `1`, which matches the fact that the only person forms a complete clump by themselves.

For an entirely equal row:

```
4
L
L
L
L
```

each comparison finds the same direction as before, so the answer never increases. The final output is `1`, correctly treating the whole row as one clump.

For alternating directions:

```
4
L
R
L
R
```

every comparison detects a change. The answer starts at one and increases three more times, producing `4`. Each person is separated from the previous one, so each person forms an individual clump.

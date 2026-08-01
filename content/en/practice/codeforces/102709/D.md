---
title: "CF 102709D - Zoom Clumps"
description: "The problem describes a line of people in a Zoom call. After everyone looks in the chosen direction, each person is represented by either L or R, depending on the direction their face appears to be pointing in the screenshot."
date: "2026-08-01T22:04:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102709
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 9-11-20 Div. 2"
rating: 0
weight: 102709
solve_time_s: 119
verified: true
draft: false
---

[CF 102709D - Zoom Clumps](https://codeforces.com/problemset/problem/102709/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a line of people in a Zoom call. After everyone looks in the chosen direction, each person is represented by either `L` or `R`, depending on the direction their face appears to be pointing in the screenshot. A clump is a maximal consecutive group of people who all face the same direction. The task is to count how many such groups appear in the final line.

The input gives the number of people followed by their directions in order from left to right. The output is the number of contiguous segments where the character is constant.

The number of people can reach $10^5$, which means the solution must be close to linear. An approach that checks every pair of positions or repeatedly scans large parts of the line would perform around $10^{10}$ operations in the worst case, which is far beyond what a typical competitive programming time limit allows. A single pass over the line is enough because every person's direction only needs to be compared with their immediate neighbor.

The main edge cases come from handling changes correctly and not counting individual people incorrectly. For example:

```
Input
1
L

Output
1
```

A single person always forms exactly one clump. A solution that starts counting only after finding a change between neighbors could accidentally return zero.

Another case is:

```
Input
5
L
L
L
L
L

Output
1
```

The whole line is one clump. A careless implementation that counts every occurrence of `L` would return five instead of one.

A final case is:

```
Input
4
L
R
L
R

Output
4
```

Every adjacent pair is different, so every person starts a new clump. An implementation that only counts one type of direction or forgets the last position would miss some groups.

## Approaches

The direct brute force approach would try to identify every clump by starting from each position and expanding to the right while the direction remains the same. This is correct because every maximal segment can be found by growing from its first element. However, in the worst case, such as a line containing only `L` characters, the first expansion visits $N$ elements, the second visits $N-1$, and so on. The total work becomes:

$$N + (N-1) + \dots + 1 = O(N^2)$$

For $N = 100000$, this is roughly five billion comparisons.

The key observation is that a clump only begins when the direction changes from the previous person. We do not need to know the entire length of a clump. We only need to know whether the current person continues the previous group or starts a new one. This reduces the problem to a simple scan where each adjacent pair is inspected once.

The brute force works because it explicitly discovers every segment, but it repeats the same information many times. The observation that boundaries between clumps are exactly the positions where neighboring directions differ lets us count those boundaries directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the sequence of directions. The first person always starts the first clump, so initialize the answer to one.
2. Scan the people from the second position onward. Compare the current direction with the previous direction.
3. If the two directions are different, increase the clump count because a new contiguous group has started.
4. After processing the entire line, output the count.

The reason this works is that the only possible way for a new clump to appear is for two neighboring people to face different directions. The exact size of the previous clump does not matter.

Why it works:

During the scan, the answer always equals the number of clumps formed by the part of the line that has already been processed. Initially, the first person creates one clump. Every time a direction changes, the current person cannot belong to the previous clump, so a new clump must begin. When the scan finishes, every possible boundary has been checked, so the count is exactly the number of clumps in the entire line.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    directions = [input().strip() for _ in range(n)]

    ans = 1
    for i in range(1, n):
        if directions[i] != directions[i - 1]:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The input is stored as a list because the comparison needs access to the previous direction. Since there are only $10^5$ characters, this memory usage is small. The algorithm starts with one clump because a nonempty line always has at least one group.

The loop begins at index one because the first direction has no previous neighbor to compare with. Every time the current character differs from the previous character, the current person becomes the first member of a new clump.

There are no tricky boundary calculations or integer size concerns here. The important implementation detail is avoiding an empty input assumption, because the constraints guarantee at least one person.

## Worked Examples

For the input:

```
4
R
L
L
R
```

the scan behaves as follows:

| Position | Direction | Previous Direction | Clumps |
| --- | --- | --- | --- |
| 1 | R | none | 1 |
| 2 | L | R | 2 |
| 3 | L | L | 2 |
| 4 | R | L | 3 |

The first change from `R` to `L` creates a second clump. The middle `L` continues the same group. The final `R` starts another group, giving the answer 3.

For the input:

```
5
L
L
R
R
L
```

the scan is:

| Position | Direction | Previous Direction | Clumps |
| --- | --- | --- | --- |
| 1 | L | none | 1 |
| 2 | L | L | 1 |
| 3 | R | L | 2 |
| 4 | R | R | 2 |
| 5 | L | R | 3 |

This example shows that long clumps are counted once. The two consecutive `L` values and two consecutive `R` values each form single groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every person is examined once. |
| Space | O(N) | The direction list stores the input sequence. |

The time complexity fits the $10^5$ limit because it performs only a constant amount of work per person. The memory usage is also within limits. The algorithm can be reduced to O(1) extra space by processing the input online, but storing the sequence keeps the implementation simple.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    data = inp.strip().split()
    if not data:
        return ""

    n = int(data[0])
    arr = data[1:]

    ans = 1
    for i in range(1, n):
        if arr[i] != arr[i - 1]:
            ans += 1

    return str(ans) + "\n"

def run(inp: str) -> str:
    return solve_io(inp)

assert run("""4
R
L
L
R
""") == "3\n", "sample 1"

assert run("""5
L
L
R
R
L
""") == "3\n", "sample 2"

assert run("""1
L
""") == "1\n", "single person"

assert run("""6
R
R
R
R
R
R
""") == "1\n", "all equal values"

assert run("""5
L
R
L
R
L
""") == "5\n", "alternating directions"

assert run("""7
L
L
L
R
R
L
L
""") == "3\n", "boundary changes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One person facing left | 1 | Minimum size handling |
| All people facing the same way | 1 | No false counting of repeated values |
| Alternating directions | 5 | Every adjacent change creates a clump |
| Several long groups | 3 | Correct handling of group boundaries |

## Edge Cases

For a single person:

```
1
L
```

the algorithm initializes the answer to one and never enters the loop. It outputs one because the only person is already a complete clump.

For a line where everyone has the same direction:

```
5
L
L
L
L
L
```

every comparison finds equal neighbors, so the answer never increases from its initial value of one. The algorithm correctly treats the entire line as one group.

For a completely alternating line:

```
4
L
R
L
R
```

every comparison detects a change. The answer increases from one to four, matching the fact that every person belongs to a separate clump.

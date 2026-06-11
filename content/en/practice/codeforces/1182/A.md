---
title: "CF 1182A - Filling Shapes"
description: "We have a board with 3 rows and $n$ columns. The only pieces available are dominoes of size $2 times 1$, which may be placed either vertically or horizontally."
date: "2026-06-12T01:26:16+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1182
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 566 (Div. 2)"
rating: 1000
weight: 1182
solve_time_s: 83
verified: true
draft: false
---

[CF 1182A - Filling Shapes](https://codeforces.com/problemset/problem/1182/A)

**Rating:** 1000  
**Tags:** dp, math  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a board with 3 rows and $n$ columns. The only pieces available are dominoes of size $2 \times 1$, which may be placed either vertically or horizontally. The task is to count how many different ways the entire $3 \times n$ rectangle can be covered without overlaps and without leaving empty cells.

The input contains a single integer representing the number of columns. The output is the number of complete tilings of that board.

The bound $n \le 60$ is very small. Even an $O(n^2)$ or $O(n^3)$ solution would be easily fast enough. What matters is finding the right recurrence. Trying to enumerate all tilings directly quickly becomes infeasible because the number of possibilities grows exponentially.

Several edge cases are easy to miss.

Consider

```
1
```

The board contains three cells. Every domino covers two cells, so covering an odd number of cells is impossible. The correct answer is

```
0
```

A careless implementation might try to apply a recurrence blindly and produce a positive value.

Another example is

```
2
```

The answer is

```
1
```

There is exactly one tiling pattern for a $3\times2$ rectangle. Missing the base case would make all later values incorrect.

A larger even example is

```
4
```

whose answer is

```
4
```

Since only even widths are possible, forgetting to handle odd values separately leads to wrong answers for half of the inputs.

## Approaches

A brute-force approach would recursively place dominoes into the first uncovered cell and continue until the board is full. Since every placement creates several branches, the number of states grows exponentially. For $n=60$, the number of configurations is enormous, far beyond what can be explored within one second.

The reason brute force works conceptually is that every complete tiling is generated exactly once. Its weakness is that it repeatedly recomputes equivalent partial boards.

Looking at small values reveals a strong pattern. Odd widths always have zero ways. For even widths, the sequence begins

$$1,1,4,16,64,\dots$$

for widths

$$0,2,4,6,8,\dots$$

Each time we add two columns, there are exactly two independent choices for extending every previous tiling. Consequently,

$$f(n)=2f(n-2)$$

for even $n$.

This observation transforms the problem into a tiny dynamic programming problem. Starting from $f(0)=1$, we repeatedly multiply by two every time two columns are added.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the value of $n$.
2. If $n$ is odd, print 0 immediately because a $3\times n$ board contains $3n$ cells, which is odd. Dominoes cover two cells, so a perfect tiling cannot exist.
3. Initialize the answer as 1, corresponding to the empty board $f(0)=1$.
4. Repeatedly increase the width by two columns and multiply the answer by 2 each time.

The recurrence comes from the fact that every additional pair of columns introduces exactly two independent extension patterns.

1. Output the resulting value.

### Why it works

The invariant is that after processing width $i$, the variable `ans` equals the number of tilings of a $3\times i$ rectangle. Initially this is true for width zero because there is one empty tiling. Every increase of two columns doubles the number of possibilities, so the invariant remains valid. When width $n$ is reached, `ans` equals the desired number of tilings.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

if n % 2 == 1:
    print(0)
else:
    ans = 1
    for _ in range(n // 2):
        ans *= 2
    print(ans)
```

The first step checks whether the width is odd. Since the total number of cells would be odd, no complete covering is possible, so the answer is immediately zero.

For even widths, the variable `ans` stores the number of tilings for the current processed width. It starts from the base case $f(0)=1$. Each iteration corresponds to adding two columns, and every such extension doubles the number of valid tilings.

Python integers automatically grow to arbitrary size, so even the answer for $n=60$ fits safely without overflow concerns.

The loop runs exactly `n // 2` times. Using integer division avoids off-by-one mistakes when $n=0$ or $n=2$.

## Worked Examples

### Example 1

Input

```
4
```

| Step | Current width | ans |
| --- | --- | --- |
| Initial | 0 | 1 |
| After first iteration | 2 | 2 |
| After second iteration | 4 | 4 |

Output

```
4
```

This trace shows how each pair of columns doubles the number of configurations.

### Example 2

Input

```
1
```

| Step | Current width | ans |
| --- | --- | --- |
| Read n | 1 | - |
| Odd check | - | - |

Output

```
0
```

This example exercises the parity condition. Since the number of cells is odd, no domino tiling exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | The loop executes $n/2$ times |
| Space | $O(1)$ | Only a few variables are stored |

With $n\le60$, even linear time is trivial. The program performs at most thirty iterations and uses constant memory, comfortably satisfying the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())

    if n % 2 == 1:
        return "0\n"

    ans = 1
    for _ in range(n // 2):
        ans *= 2
    return str(ans) + "\n"

# provided sample
assert run("4\n") == "4\n", "sample 1"

# custom cases
assert run("1\n") == "0\n", "minimum odd width"
assert run("2\n") == "2\n", "smallest even width"
assert run("3\n") == "0\n", "another odd width"
assert run("60\n") == "1073741824\n", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Odd width has no solution |
| `2` | `2` | Smallest even width |
| `3` | `0` | Parity handling |
| `60` | `1073741824` | Maximum input size |

## Edge Cases

For the input

```
1
```

the algorithm immediately detects that $n$ is odd and prints

```
0
```

No loop iterations are performed. This prevents applying the recurrence to an impossible board.

For the input

```
2
```

the computation proceeds as follows.

| Width | ans |
| --- | --- |
| 0 | 1 |
| 2 | 2 |

The final answer is

```
2
```

This confirms that the base case $f(0)=1$ is propagated correctly.

For the input

```
5
```

the odd-width check again triggers immediately.

```
0
```

Without this check, a recurrence designed for even widths could incorrectly produce a positive answer.

For the maximum input

```
60
```

the loop executes thirty times, repeatedly doubling the count. Python's arbitrary-precision integers guarantee that the value

```
1073741824
```

is produced exactly without overflow.

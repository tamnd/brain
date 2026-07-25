---
title: "CF 102862F - Cell Borders"
description: "We have a row of n square cells. Between and around these cells there are n + 1 borders, and each border can either be colored or left uncolored. A cell touches the border immediately before it and the border immediately after it."
date: "2026-07-25T13:51:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102862
codeforces_index: "F"
codeforces_contest_name: "LU ICPC Selection Contest 2020 and KFU Open Contest 2020"
rating: 0
weight: 102862
solve_time_s: 33
verified: true
draft: false
---

[CF 102862F - Cell Borders](https://codeforces.com/problemset/problem/102862/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of `n` square cells. Between and around these cells there are `n + 1` borders, and each border can either be colored or left uncolored. A cell touches the border immediately before it and the border immediately after it. For every cell, we are told exactly how many of its two borders must be colored, which can be `0`, `1`, or `2`. The task is to decide whether there exists a coloring of the borders that satisfies every cell.

The input is a sequence `a`, where `a[i]` describes the required number of colored sides for the `i`-th cell. The output is only whether a valid assignment of the `n + 1` border states exists.

The constraint `n <= 100000` means we cannot try every possible border coloring. There are `n + 1` borders, each with two possible states, so a brute-force search would examine `2^(n+1)` possibilities, which becomes impossible even for a few dozen cells. The solution needs to process the array in linear time.

The tricky cases are caused by the fact that neighboring cells share a border. A choice made for one cell immediately affects the next one.

For example, with one cell:

```
Input:
1
0

Output:
Yes
```

Both outer borders can stay uncolored, so the answer is possible. A solution that assumes every cell needs a colored border would fail here.

Another boundary case is:

```
Input:
2
2 0

Output:
No
```

The first cell requires both of its borders to be colored. That means the shared border between the two cells is colored. The second cell already has one colored border, so it cannot end with zero colored borders. The contradiction comes from the shared boundary.

A third common mistake appears with long runs of `1`s. For example:

```
Input:
3
1 1 1

Output:
Yes
```

The borders can alternate between colored and uncolored. A greedy method that always chooses the same side for every `1` eventually gets stuck.

## Approaches

The direct approach is to decide the state of every border one by one. Since every border is binary, we could try all possible assignments and check whether each cell receives the required number of colored sides. This is correct because every possible coloring is considered. However, there are `n + 1` borders, giving `2^(n+1)` assignments. With `n = 100000`, this is far beyond what any time limit can handle.

The key observation is that this is not really a global search problem. The cells form a line, and each cell only depends on two neighboring borders. Once the left border of a cell is known, the right border is forced because the cell needs a fixed total number of colored borders.

Let the border before cell `i` be `x[i-1]` and the border after it be `x[i]`. The condition is:

```
x[i-1] + x[i] = a[i]
```

If we choose `x[0]`, every following border value is determined. Since the first border can only be `0` or `1`, there are only two possible paths to check.

For a chosen starting value, we move from left to right. At every cell, the next border is:

```
next_border = required - current_border
```

If this value is not `0` or `1`, the current choice is impossible. After processing all cells, the final border value is also valid automatically because it is generated as part of the sequence.

The brute-force method fails because it explores all border combinations. The structure of the array reduces the choices to only two possible starting states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Try the first possible color of the leftmost border. It can be either `0` or `1`. The whole sequence is determined after this choice, so checking both possibilities is enough.
2. Scan the cells from left to right while storing the color of the current left border. For the current cell, calculate the right border needed to satisfy its required value.
3. If the calculated right border is not `0` or `1`, reject this starting choice. A border cannot be partially colored or have any other state.
4. Otherwise, move to the next cell using this newly calculated border as its left border.
5. If either starting choice reaches the end successfully, print `Yes`. If both choices fail, print `No`.

Why it works:

The invariant during the scan is that before processing a cell, the stored border value is exactly the color chosen for the left side of that cell. The algorithm computes the only possible value for the right side that can satisfy the cell. If that value is invalid, no other choice exists for that cell because both sides are already restricted to binary values. Since the first border is the only free decision, testing both possibilities covers every valid coloring.

## Python Solution

```python
import sys

input = sys.stdin.readline

def check(a, first):
    cur = first
    for need in a:
        nxt = need - cur
        if nxt < 0 or nxt > 1:
            return False
        cur = nxt
    return True

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    if check(a, 0) or check(a, 1):
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The `check` function represents one possible coloring of the outermost left border. The variable `cur` stores the border shared with the current cell on its left side.

For every cell, the right border is forced. If the cell needs `need` colored borders and the left border already contributes `cur`, the other border must contribute `need - cur`. Since borders are binary, any value outside `0` or `1` immediately invalidates the attempt.

The main function only runs this simulation twice, once with an uncolored first border and once with a colored first border. No arrays are needed during the scan because only the current border state matters.

There are no overflow issues because every value involved is at most `2`, and the boundary conditions are handled by checking both possible initial borders.

## Worked Examples

For the input:

```
6
1 2 1 0 1 2
```

Starting with the first border uncolored:

| Cell | Current left border | Required value | Calculated right border |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 2 | 1 |
| 3 | 1 | 1 | 0 |
| 4 | 0 | 0 | 0 |
| 5 | 0 | 1 | 1 |
| 6 | 1 | 2 | 1 |

The scan finishes successfully, so the answer is `Yes`. This demonstrates how a chain of forced choices can satisfy a complicated-looking arrangement.

For the input:

```
2
2 0
```

Trying the first border as uncolored:

| Cell | Current left border | Required value | Calculated right border |
| --- | --- | --- | --- |
| 1 | 0 | 2 | 2 |

The required border value is impossible.

Trying the first border as colored:

| Cell | Current left border | Required value | Calculated right border |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 1 |
| 2 | 1 | 0 | -1 |

The second attempt also fails, so the answer is `No`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The array is scanned twice, once for each possible first border state. |
| Space | O(1) | Only the current border value is stored. |

The algorithm performs a constant amount of work for each cell. With `100000` cells, this easily fits within the time and memory limits.

## Test Cases

```python
import sys
import io

def solve_input(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def check(a, first):
        cur = first
        for need in a:
            nxt = need - cur
            if nxt < 0 or nxt > 1:
                return False
            cur = nxt
        return True

    n = int(input())
    a = list(map(int, input().split()))
    return "Yes\n" if check(a, 0) or check(a, 1) else "No\n"

assert solve_input("6\n1 2 1 0 1 2\n") == "Yes\n", "sample 1"
assert solve_input("2\n2 0\n") == "No\n", "sample 2"

assert solve_input("1\n0\n") == "Yes\n", "single zero cell"
assert solve_input("3\n1 1 1\n") == "Yes\n", "alternating borders"
assert solve_input("4\n2 2 2 2\n") == "No\n", "impossible chain"
assert solve_input("5\n0 1 2 1 0\n") == "Yes\n", "boundary propagation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `Yes` | Minimum size and empty borders |
| `3 / 1 1 1` | `Yes` | Alternating choices for consecutive ones |
| `4 / 2 2 2 2` | `No` | Conflicting shared borders |
| `5 / 0 1 2 1 0` | `Yes` | Correct propagation through boundaries |

## Edge Cases

The one-cell case is handled because the algorithm still tries both possible outer border values. For input:

```
1
0
```

Starting with `0` gives the next border as `0`, which is valid. The scan finishes and returns `Yes`.

The shared border contradiction appears in:

```
2
2 0
```

The first cell forces the middle border to be colored regardless of the initial choice. The second cell then cannot have zero colored borders. The algorithm catches this because the required next border becomes `-1`.

Long sequences of cells requiring one colored side are handled by the forced alternation. For:

```
3
1 1 1
```

Starting with the left border uncolored creates the sequence:

```
0, 1, 0, 1
```

Each cell sees exactly one colored border, so the algorithm accepts it.

The method does not need special handling for cells requiring two colored borders. A value of `2` simply forces both adjacent borders to be colored, and any conflict appears naturally when the next cell is processed.

This format can be adapted into a shorter contest editorial, a blog post style explanation, or a version with a more formal proof if needed.

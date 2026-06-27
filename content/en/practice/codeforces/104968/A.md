---
title: "CF 104968A - Pepperoni Paradise"
description: "The pizza is represented as a square grid of size $N times N$, where each cell contains a single alphabet character. Among these characters, only two symbols matter for us: uppercase ‘P’ and lowercase ‘p’."
date: "2026-06-28T06:47:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104968
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 2 (Beginner)"
rating: 0
weight: 104968
solve_time_s: 69
verified: true
draft: false
---

[CF 104968A - Pepperoni Paradise](https://codeforces.com/problemset/problem/104968/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The pizza is represented as a square grid of size $N \times N$, where each cell contains a single alphabet character. Among these characters, only two symbols matter for us: uppercase ‘P’ and lowercase ‘p’. Every occurrence of either of these characters represents one pepperoni placed on that cell of the pizza. All other letters are irrelevant decorations.

The task is to scan the entire grid and count how many pepperonis are present in total. Since each cell can contribute at most one pepperoni, the answer is simply the number of cells containing either ‘P’ or ‘p’.

The constraint $N \leq 100$ means the grid has at most $10^4$ cells. Even a straightforward scan over all cells is extremely cheap. A solution that checks each cell once is already optimal; anything more complex than linear scanning would be unnecessary.

The main edge cases are mostly about input interpretation rather than algorithmic difficulty. The grid is guaranteed to be exactly $N$ lines of $N$ characters each, but careless input parsing can still go wrong if one assumes space-separated tokens or forgets newline handling.

For example, if $N = 1$ and the grid is:

```
P
```

the answer is 1. If:

```
a
```

the answer is 0. If:

```
p
```

the answer is also 1. A common mistake is checking only uppercase ‘P’ and forgetting lowercase ‘p’, which would incorrectly output 0 for valid pepperonis.

## Approaches

The most direct approach is to iterate over every cell in the grid and check whether the character is ‘P’ or ‘p’. This works because each cell is independent and contributes a fixed value of either 1 or 0 to the total count. Summing these contributions gives the final answer.

A slightly more naive mental model might treat the grid as a collection of strings and repeatedly search for occurrences of “P” or “p” using substring search or repeated scanning. This is still linear in total input size, but introduces unnecessary overhead in string operations and repeated passes over the same data. In the worst case, it could still touch all $N^2$ characters multiple times, which is avoidable.

The key simplification is recognizing that no spatial relationships matter. There is no grouping, no adjacency, and no transformation. Each character independently determines whether to increment the answer. This collapses the problem into a single pass over the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force repeated scanning | O(N^2) to O(N^3) | O(1) | Too slow / unnecessary |
| Single pass counting | O(N^2) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $N$, which determines both the number of rows and the number of columns in the grid. This sets the total number of characters we will process.
2. Initialize a counter variable to zero. This variable accumulates the number of pepperonis encountered during the scan.
3. Iterate over each of the $N$ rows. Each row is a string of length $N$, representing one horizontal slice of the pizza grid.
4. For each character in the current row, check whether it is equal to ‘P’ or ‘p’. If it matches either, increment the counter by one. This step is justified because each matching cell contributes exactly one pepperoni.
5. After processing all rows and all characters, output the final value of the counter.

### Why it works

The algorithm relies on a direct one-to-one mapping between valid characters and contributions to the answer. Every grid cell is inspected exactly once, and each cell independently contributes either 0 or 1. Since there is no overlap or interaction between cells, summing local contributions produces the global total. The invariant maintained throughout the scan is that the counter equals the number of pepperoni cells seen so far, so at termination it equals the total count in the grid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    cnt = 0

    for _ in range(n):
        row = input().strip()
        for ch in row:
            if ch == 'P' or ch == 'p':
                cnt += 1

    print(cnt)

if __name__ == "__main__":
    solve()
```

The solution reads each row as a raw string and iterates character by character. Using `strip()` ensures that newline characters do not interfere with processing, which is a common source of off-by-one errors in grid problems. The condition explicitly checks both uppercase and lowercase forms, preventing missed matches.

The counter is updated immediately when a valid character is found, so there is no need for intermediate storage or preprocessing of the grid.

## Worked Examples

### Sample 1

Input:

```
3
SPWXjSSaO
```

We interpret this as a 3-character-per-row grid, but only one row is shown in the sample formatting. The key idea remains: we scan all characters and count ‘P’ and ‘p’.

| Step | Row | Character | Action | Counter |
| --- | --- | --- | --- | --- |
| 1 | SPWXjSSaO | S | ignore | 0 |
| 2 | SPWXjSSaO | P | increment | 1 |
| 3 | SPWXjSSaO | W | ignore | 1 |
| ... | ... | ... | ... | 1 |
| end | SPWXjSSaO | O | ignore | 1 |

Final output:

```
1
```

This confirms that only a single valid pepperoni character appears in the entire grid.

### Sample 2

Input:

```
4
APZaqPbpcCaAXyPZ
```

Again, we scan the full row-by-row structure.

| Step | Row | Character | Action | Counter |
| --- | --- | --- | --- | --- |
| 1 | APZaqPbpcCaAXyPZ | A | ignore | 0 |
| 2 | APZaqPbpcCaAXyPZ | P | increment | 1 |
| 3 | APZaqPbpcCaAXyPZ | Z | ignore | 1 |
| 4 | APZaqPbpcCaAXyPZ | a | ignore | 1 |
| 5 | APZaqPbpcCaAXyPZ | q | ignore | 1 |
| 6 | APZaqPbpcCaAXyPZ | P | increment | 2 |
| ... | ... | ... | ... | 4 |

Final output:

```
4
```

This demonstrates that both uppercase and lowercase variants contribute equally, and multiple occurrences are accumulated independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N^2) | Each of the $N^2$ cells is visited exactly once |
| Space | O(1) | Only a single counter is maintained regardless of grid size |

The maximum input size is $10^4$ characters, so a single linear scan is trivial under the time limit. Memory usage is constant aside from input storage, which is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (interpreted in grid form)
assert run("1\nP\n") == "1"
assert run("1\na\n") == "0"

# custom cases
assert run("2\nPP\npp\n") == "4", "all pepperonis both cases"
assert run("3\nabc\ndef\nghi\n") == "0", "no pepperonis"
assert run("3\nPpp\nPPP\nppp\n") == "9", "mixed grid"
assert run("1\nZ\n") == "0", "single non-match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 P | 1 | minimal positive case |
| 1x1 a | 0 | minimal negative case |
| mixed 2x2 | 4 | case sensitivity handling |
| all non-P/p | 0 | no false positives |
| full mixed grid | 9 | accumulation correctness |

## Edge Cases

One subtle case is when the grid contains only lowercase letters and no uppercase ‘P’. For input:

```
2
pp
pp
```

the scan processes each character and increments for every ‘p’, producing 4. A buggy implementation that checks only uppercase ‘P’ would return 0, but the correct logic treats both cases symmetrically.

Another case is the smallest grid:

```
1
P
```

The loop runs once, sees a match, and returns 1. The same logic also handles:

```
1
z
```

where no increments occur and the output remains 0. This confirms that the algorithm behaves consistently even at the boundary where the grid collapses to a single cell.

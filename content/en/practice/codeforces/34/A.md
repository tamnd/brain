---
title: "CF 34A - Reconnaissance 2"
description: "We are given the heights of soldiers standing in a circle. Two soldiers can form a reconnaissance unit if they stand nex"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 34
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 34 (Div. 2)"
rating: 800
weight: 34
solve_time_s: 78
verified: true
draft: false
---

[CF 34A - Reconnaissance 2](https://codeforces.com/problemset/problem/34/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the heights of soldiers standing in a circle. Two soldiers can form a reconnaissance unit if they stand next to each other and their height difference is as small as possible among all neighboring pairs.

The circular arrangement changes one important detail. The first and last soldiers are also neighbors. A linear scan that only checks adjacent positions from left to right would miss this pair.

The input is a small array of heights. We need to output the 1-based indices of any neighboring pair with the minimum absolute difference.

The constraints are tiny. At most 100 soldiers exist, so even an $O(n^2)$ solution would run comfortably within limits. Still, the structure of the problem naturally leads to a simpler linear scan. Since every valid pair must already be neighbors in the circle, we never need to compare every soldier against every other soldier.

The main edge case is the circular connection between the last and first soldiers.

Consider this input:

```
5
10 12 13 15 10
```

The smallest difference is between soldiers 5 and 1:

```
|10 - 10| = 0
```

A careless implementation that only checks pairs `(1,2), (2,3), (3,4), (4,5)` would incorrectly miss the optimal answer.

Another subtle case happens when multiple pairs share the same minimum difference.

```
4
5 7 9 11
```

Every neighboring pair has difference `2`. Any valid pair may be printed. An implementation should not assume uniqueness.

The minimum input size also matters:

```
2
100 1
```

There are only two soldiers, and because the arrangement is circular, they are neighbors in both directions. The answer must still be `1 2` or `2 1`.

## Approaches

The brute-force idea is straightforward. Compare every pair of soldiers, check whether they are neighbors in the circle, and track the minimum height difference. Since there are $n^2$ pairs, the worst-case operation count is about $100^2 = 10{,}000$, which is still completely acceptable.

The problem with brute force is not performance here, but unnecessary work. Most pairs are irrelevant because only neighboring soldiers are allowed. The structure of the problem already tells us exactly which comparisons matter.

Each soldier has only two neighbors. If we walk once around the circle and compare every adjacent pair, we will examine every valid candidate exactly once. That reduces the task to a simple linear scan.

The key observation is that the answer must come from one of these pairs:

```
(1,2), (2,3), ..., (n-1,n), (n,1)
```

No other pair is legal.

So the optimal solution checks all neighboring pairs, computes their absolute differences, and remembers the smallest one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of soldiers and their heights.
2. Initialize the current best difference with a very large value.
3. Iterate through all positions from `0` to `n-1`.
4. For each position `i`, determine its neighbor as `(i + 1) % n`.

The modulo operation is what makes the array circular. When `i` is the last index, the neighbor becomes the first soldier.
5. Compute the absolute difference between the two neighboring heights.
6. If this difference is smaller than the current best value, update the answer indices and store the new minimum difference.
7. After finishing the scan, print the stored pair using 1-based indexing.

### Why it works

The algorithm checks every valid neighboring pair exactly once. Since the problem only allows neighboring soldiers in the circle, no valid answer can exist outside this set. By maintaining the smallest absolute difference seen so far, the algorithm guarantees that the stored pair is optimal after the scan finishes.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

best_diff = float('inf')
ans_l = 1
ans_r = 2

for i in range(n):
    j = (i + 1) % n
    diff = abs(a[i] - a[j])

    if diff < best_diff:
        best_diff = diff
        ans_l = i + 1
        ans_r = j + 1

print(ans_l, ans_r)
```

The program begins by reading the soldier heights into an array.

`best_diff` stores the minimum difference found so far. It starts at infinity so the first pair always replaces it.

The loop scans every soldier once. For each index `i`, the next neighbor is computed with:

```
j = (i + 1) % n
```

This is the most important implementation detail. Without modulo, the last soldier would have no neighbor on the right, and the circular pair `(n,1)` would be skipped.

The comparison uses absolute difference because the order of heights does not matter:

```
diff = abs(a[i] - a[j])
```

The indices are converted back to 1-based form when stored because Codeforces problems usually expect indexing starting from 1.

The algorithm uses constant extra memory and only one traversal of the array.

## Worked Examples

### Example 1

Input:

```
5
10 12 13 15 10
```

| i | Pair Checked | Difference | Best Difference | Stored Answer |
| --- | --- | --- | --- | --- |
| 0 | (1,2) | 2 | 2 | (1,2) |
| 1 | (2,3) | 1 | 1 | (2,3) |
| 2 | (3,4) | 2 | 1 | (2,3) |
| 3 | (4,5) | 5 | 1 | (2,3) |
| 4 | (5,1) | 0 | 0 | (5,1) |

The last step demonstrates why the circular connection matters. The optimal pair only appears when the last soldier is compared with the first.

### Example 2

Input:

```
4
5 7 9 11
```

| i | Pair Checked | Difference | Best Difference | Stored Answer |
| --- | --- | --- | --- | --- |
| 0 | (1,2) | 2 | 2 | (1,2) |
| 1 | (2,3) | 2 | 2 | (1,2) |
| 2 | (3,4) | 2 | 2 | (1,2) |
| 3 | (4,1) | 6 | 2 | (1,2) |

This example shows that multiple optimal answers may exist. The algorithm simply keeps the first one it encounters, which is completely valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each neighboring pair is checked once |
| Space | O(1) | Only a few variables are stored |

With at most 100 soldiers, the solution easily fits within the limits. Even much slower approaches would pass, but the linear scan directly matches the structure of the problem and avoids unnecessary comparisons.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    best_diff = float('inf')
    ans_l = 1
    ans_r = 2

    for i in range(n):
        j = (i + 1) % n
        diff = abs(a[i] - a[j])

        if diff < best_diff:
            best_diff = diff
            ans_l = i + 1
            ans_r = j + 1

    print(ans_l, ans_r)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout
    return out.getvalue().strip()

# provided sample
assert run("5\n10 12 13 15 10\n") == "5 1", "sample 1"

# minimum size
assert run("2\n100 1\n") == "1 2", "minimum n"

# all equal values
assert run("4\n7 7 7 7\n") == "1 2", "all equal"

# circular edge case
assert run("5\n10 20 30 40 11\n") == "5 1", "last-first pair"

# multiple optimal answers
assert run("4\n1 3 5 7\n") == "1 2", "many valid answers"

# decreasing sequence
assert run("6\n20 18 16 14 12 10\n") == "1 2", "consistent differences"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 100 1` | `1 2` | Minimum input size |
| `4 / 7 7 7 7` | `1 2` | Zero differences everywhere |
| `5 / 10 20 30 40 11` | `5 1` | Circular neighbor handling |
| `4 / 1 3 5 7` | `1 2` | Multiple optimal answers |

## Edge Cases

Consider the circular boundary case:

```
5
10 12 13 15 10
```

The algorithm checks pairs in this order:

```
(1,2), (2,3), (3,4), (4,5), (5,1)
```

The final comparison gives difference `0`, which becomes the new minimum. Because the modulo operation connects the last soldier back to the first, the correct answer `5 1` is found.

Now consider equal heights:

```
4
7 7 7 7
```

Every neighboring pair has difference `0`. The first comparison already sets the minimum to `0`, and no later pair improves it. The algorithm returns `1 2`, which is valid because any optimal pair may be printed.

Finally, examine the smallest possible input:

```
2
100 1
```

The loop checks:

```
(1,2)
(2,1)
```

The first pair already achieves the minimum difference `99`. The algorithm stores and prints `1 2`. Even though the circle concept duplicates the same pair in reverse order, the answer remains correct.

---
title: "CF 228A - Is your horseshoe on the other hoof?"
description: "Valera has exactly four horseshoes. Each horseshoe has a color represented by an integer. For the party, he wants all four horseshoes to have different colors. If some of his horseshoes share the same color, he must buy replacement horseshoes of new colors."
date: "2026-06-04T09:08:59+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 228
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 141 (Div. 2)"
rating: 800
weight: 228
solve_time_s: 67
verified: true
draft: false
---

[CF 228A - Is your horseshoe on the other hoof?](https://codeforces.com/problemset/problem/228/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

Valera has exactly four horseshoes. Each horseshoe has a color represented by an integer. For the party, he wants all four horseshoes to have different colors.

If some of his horseshoes share the same color, he must buy replacement horseshoes of new colors. Since the store sells horseshoes of any color, the only question is how many additional horseshoes he needs to buy to end up with four distinct colors.

The input consists of four integers representing the colors of the horseshoes he currently owns. The output is a single integer, the minimum number of horseshoes that must be purchased.

The constraints are tiny. There are only four values, and each color can be as large as $10^9$. The magnitude of the color values does not matter because we never perform arithmetic on them. We only need to determine whether two colors are equal. With only four numbers, any reasonable algorithm easily fits within the time and memory limits.

The main source of mistakes is counting duplicates incorrectly.

Consider the input:

```
1 1 1 1
```

The correct answer is:

```
3
```

There is only one distinct color, so three horseshoes must be replaced. A careless implementation that counts duplicate pairs could produce a larger number.

Consider:

```
1 2 3 4
```

The correct answer is:

```
0
```

All colors are already different, so nothing needs to be purchased.

Consider:

```
5 5 7 8
```

The correct answer is:

```
1
```

There are three distinct colors. Only one additional color is needed.

The key observation is that the answer depends only on how many distinct colors already exist.

## Approaches

A brute-force approach would compare every pair of horseshoes and try to count repeated colors manually. Since there are only four horseshoes, this is actually feasible. There are only six pairs, so the work is constant.

The difficulty with this approach is not performance but correctness. When a color appears three or four times, pair counting becomes awkward because multiple duplicate pairs correspond to only a few replacements. For example, with colors `1 1 1 1`, there are six equal pairs, but the answer is only three.

The simpler observation is that every distinct color can be kept, and every extra horseshoe sharing an existing color must be replaced. If there are `k` distinct colors among the four horseshoes, then exactly `4 - k` horseshoes need replacement.

A set is a natural tool here because a set automatically stores only distinct values. By inserting all four colors into a set, the set size immediately tells us how many unique colors exist.

The answer becomes:

```
4 - number_of_distinct_colors
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4²) | O(1) | Accepted |
| Optimal | O(4) | O(4) | Accepted |

## Algorithm Walkthrough

1. Read the four color values.
2. Insert all four values into a set.

The set keeps only unique colors, automatically removing duplicates.
3. Compute the number of distinct colors as the size of the set.
4. Subtract that value from 4.

Every distinct color can remain, while every remaining horseshoe must be replaced.
5. Print the result.

### Why it works

The set contains exactly one copy of each color that appears among the four horseshoes. If the set size is `k`, then there are `k` colors that can already be used without modification. Since Valera needs four different colors in total, the remaining `4 - k` horseshoes must be replaced with new colors. No smaller number of purchases can work because each duplicate horseshoe contributes one missing distinct color.

## Python Solution

```python
import sys
input = sys.stdin.readline

colors = list(map(int, input().split()))
print(4 - len(set(colors)))
```

The solution reads the four integers and stores them in a list. Converting the list to a set removes all duplicate colors. The size of that set is the number of distinct colors already available.

The expression `4 - len(set(colors))` directly computes how many horseshoes are duplicates and therefore must be replaced.

There are no tricky boundary conditions. The smallest possible answer is `0` when all four colors differ. The largest possible answer is `3` when all four colors are identical.

## Worked Examples

### Example 1

Input:

```
1 7 3 3
```

| Colors | Set Contents | Distinct Count | Answer |
| --- | --- | --- | --- |
| 1 7 3 3 | {1, 7, 3} | 3 | 1 |

The set contains three distinct colors. One horseshoe duplicates color `3`, so one replacement is needed.

### Example 2

Input:

```
5 5 5 5
```

| Colors | Set Contents | Distinct Count | Answer |
| --- | --- | --- | --- |
| 5 5 5 5 | {5} | 1 | 3 |

Only one distinct color exists. Three additional colors must be obtained, so the answer is `3`.

This example demonstrates that the algorithm correctly handles the maximum number of duplicates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(4) | Four values are inserted into a set |
| Space | O(4) | The set stores at most four distinct colors |

Since the input size is fixed at four values, the running time and memory usage are effectively constant. The solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    colors = list(map(int, input().split()))
    print(4 - len(set(colors)))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("1 7 3 3\n") == "1\n", "sample 1"

# custom cases
assert run("1 2 3 4\n") == "0\n", "all distinct"
assert run("1 1 1 1\n") == "3\n", "all equal"
assert run("5 5 7 8\n") == "1\n", "one duplicate"
assert run("1000000000 1 1000000000 2\n") == "1\n", "large values"
assert run("9 9 8 8\n") == "2\n", "two duplicated colors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 4` | `0` | No purchases needed |
| `1 1 1 1` | `3` | Maximum number of replacements |
| `5 5 7 8` | `1` | Single duplicate color |
| `1000000000 1 1000000000 2` | `1` | Large color values |
| `9 9 8 8` | `2` | Multiple duplicated groups |

## Edge Cases

Consider the input:

```
1 1 1 1
```

The set becomes `{1}`. Its size is `1`, so the algorithm computes `4 - 1 = 3`. Three horseshoes must be replaced because only one distinct color exists.

Consider the input:

```
1 2 3 4
```

The set becomes `{1, 2, 3, 4}`. Its size is `4`, so the answer is `4 - 4 = 0`. Every horseshoe already has a unique color.

Consider the input:

```
5 5 7 8
```

The set becomes `{5, 7, 8}`. Its size is `3`, producing `4 - 3 = 1`. Only one horseshoe duplicates an existing color.

Consider the input:

```
9 9 8 8
```

The set becomes `{8, 9}`. Its size is `2`, producing `4 - 2 = 2`. Two additional distinct colors are required. The algorithm handles multiple duplicated color groups without any special logic because the set size captures all necessary information.

---
title: "CF 228A - Is your horseshoe on the other hoof?"
description: "Valera already owns four horseshoes, and each horseshoe has a color represented by an integer. He wants all four horseshoes to have distinct colors before going to the party. If some colors repeat, he must buy new horseshoes to replace the duplicates."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 228
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 141 (Div. 2)"
rating: 800
weight: 228
solve_time_s: 139
verified: true
draft: false
---

[CF 228A - Is your horseshoe on the other hoof?](https://codeforces.com/problemset/problem/228/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

Valera already owns four horseshoes, and each horseshoe has a color represented by an integer. He wants all four horseshoes to have distinct colors before going to the party. If some colors repeat, he must buy new horseshoes to replace the duplicates.

The input consists of four integers. Each integer is the color of one horseshoe. The output is a single integer, the minimum number of new horseshoes he needs to buy so that all four colors become different.

The constraints are tiny. There are always exactly four numbers, and each value can be as large as $10^9$. The large numeric range rules out using arrays indexed by color, but that does not matter because we only process four values. Any reasonable algorithm will run instantly within the time limit.

The tricky part is not performance, it is counting duplicates correctly.

One easy mistake is to count how many colors appear more than once instead of counting how many horseshoes must actually be replaced.

Consider this input:

```
1 1 1 1
```

The correct answer is:

```
3
```

There is only one unique color, so three horseshoes must be replaced. A careless solution that only counts "duplicate groups" would output `1`, which is wrong.

Another edge case is when there are two separate repeated pairs:

```
1 2 1 2
```

The correct answer is:

```
2
```

Both repeated horseshoes must be replaced. Counting repeated values incorrectly can easily produce `1`.

A final case is when all colors are already different:

```
1 2 3 4
```

The correct answer is:

```
0
```

No purchases are needed.

## Approaches

The brute-force idea is to compare every pair of horseshoes and count repeated colors manually. Since there are only four horseshoes, there are only six pairs to check. This works because duplicates can only appear through equal pairs.

For example, we could compare:

```
s1 with s2
s1 with s3
s1 with s4
s2 with s3
s2 with s4
s3 with s4
```

Then we could somehow track which horseshoes are duplicates. The problem is that this approach becomes messy when the same value appears three or four times. Avoiding double-counting requires extra bookkeeping.

The key observation is that the answer depends only on how many distinct colors exist.

If there are:

```
4 unique colors -> buy 0
3 unique colors -> buy 1
2 unique colors -> buy 2
1 unique color  -> buy 3
```

So the answer is simply:

```
4 - number_of_unique_colors
```

A set is perfect for this problem because a set automatically removes duplicates. By inserting all four colors into a set, the set size becomes the number of distinct colors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

Even though both are technically constant time because the input size is fixed at four, the set-based solution is cleaner, shorter, and less error-prone.

## Algorithm Walkthrough

1. Read the four horseshoe colors.
2. Insert the colors into a set.

A set stores only unique values, so repeated colors automatically collapse into one entry.
3. Compute the number of unique colors using `len(set_colors)`.
4. Subtract that value from `4`.

If there are only three distinct colors, one horseshoe must be replaced. If there are two distinct colors, two replacements are needed, and so on.
5. Print the result.

### Why it works

The algorithm relies on a simple invariant: every unique color can remain unchanged, while every extra occurrence of an already-used color must be replaced.

If there are `k` distinct colors among four horseshoes, then exactly `4 - k` horseshoes are duplicates. Replacing those duplicates is both necessary and sufficient to make all colors distinct.

## Python Solution

```python
import sys
input = sys.stdin.readline

colors = list(map(int, input().split()))

unique_colors = set(colors)

print(4 - len(unique_colors))
```

The program first reads the four integers into a list. Converting the list into a set removes repeated values automatically.

The expression `len(unique_colors)` gives the number of distinct colors already available. Since Valera needs four different colors total, the remaining number of horseshoes he must buy is `4 - len(unique_colors)`.

There are no overflow concerns because Python integers handle large values naturally. The only subtle point is remembering that the answer depends on unique colors, not on the number of repeated pairs.

## Worked Examples

### Example 1

Input:

```
1 7 3 3
```

| Step | Current colors | Unique set | Unique count | Answer |
| --- | --- | --- | --- | --- |
| Read input | 1 7 3 3 | {} | 0 | - |
| Build set | 1 7 3 3 | {1, 7, 3} | 3 | - |
| Compute result | - | {1, 7, 3} | 3 | 1 |

The set contains only three unique colors because `3` appears twice. One horseshoe must be replaced.

### Example 2

Input:

```
1 1 1 1
```

| Step | Current colors | Unique set | Unique count | Answer |
| --- | --- | --- | --- | --- |
| Read input | 1 1 1 1 | {} | 0 | - |
| Build set | 1 1 1 1 | {1} | 1 | - |
| Compute result | - | {1} | 1 | 3 |

All horseshoes have the same color, so only one unique color exists. Three horseshoes must be replaced.

This trace confirms that the algorithm correctly handles heavy duplication without double-counting mistakes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only four values are processed |
| Space | O(1) | The set stores at most four elements |

The solution easily fits within the limits because the input size is fixed and tiny. The program performs only a handful of operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline
    colors = list(map(int, input().split()))
    print(4 - len(set(colors)))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    
    backup_stdout = sys.stdout
    sys.stdout = out
    
    solve()
    
    sys.stdout = backup_stdout
    return out.getvalue()

# provided sample
assert run("1 7 3 3\n") == "1\n", "sample 1"

# custom cases
assert run("1 2 3 4\n") == "0\n", "all distinct"
assert run("5 5 5 5\n") == "3\n", "all equal"
assert run("1 2 1 2\n") == "2\n", "two repeated pairs"
assert run("1000000000 1 1000000000 2\n") == "1\n", "large values"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 4` | `0` | Already distinct colors |
| `5 5 5 5` | `3` | Maximum duplication |
| `1 2 1 2` | `2` | Multiple duplicate groups |
| `1000000000 1 1000000000 2` | `1` | Large integer values |

## Edge Cases

Consider the case where all horseshoes already have different colors:

```
1 2 3 4
```

The algorithm builds the set `{1, 2, 3, 4}`. The set size is `4`, so the answer becomes:

```
4 - 4 = 0
```

No purchases are needed.

Now consider the extreme duplicate case:

```
7 7 7 7
```

The set becomes `{7}`. Its size is `1`, so the answer becomes:

```
4 - 1 = 3
```

Three horseshoes must be replaced because only one color can stay.

Finally, consider two repeated pairs:

```
1 2 1 2
```

The set becomes `{1, 2}`. The size is `2`, so:

```
4 - 2 = 2
```

One duplicate `1` and one duplicate `2` must be replaced. The algorithm handles this naturally because the set keeps only distinct colors.

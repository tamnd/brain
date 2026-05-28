---
title: "CF 169A - Chores"
description: "We have a list of chore difficulties. Vasya must receive exactly b chores whose difficulty is at most x, while Petya must receive exactly a chores whose difficulty is strictly greater than x. The value x must be an integer. We need to count how many integers satisfy the split."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 169
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2012 Round 2 (Unofficial Div. 2 Edition)"
rating: 800
weight: 169
solve_time_s: 85
verified: true
draft: false
---

[CF 169A - Chores](https://codeforces.com/problemset/problem/169/A)

**Rating:** 800  
**Tags:** sortings  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a list of chore difficulties. Vasya must receive exactly `b` chores whose difficulty is at most `x`, while Petya must receive exactly `a` chores whose difficulty is strictly greater than `x`.

The value `x` must be an integer. We need to count how many integers satisfy the split.

After sorting the difficulties, the condition becomes much easier to reason about. Since exactly `b` chores must satisfy `h[i] ≤ x`, the first `b` smallest chores must belong to Vasya, and the remaining `a` chores must belong to Petya.

That immediately creates two boundary values:

- The largest chore Vasya gets is the `b`-th smallest value.
- The smallest chore Petya gets is the `(b + 1)`-th smallest value.

If we denote them as:

- `L = sorted_h[b - 1]`
- `R = sorted_h[b]`

then `x` must satisfy:

- `x ≥ L`, otherwise Vasya would receive fewer than `b` chores.
- `x < R`, otherwise Petya would receive fewer than `a` chores.

So every valid integer `x` lies in the interval `[L, R - 1]`.

The constraints are tiny here, only up to 2000 elements, so even quadratic solutions would pass comfortably. Still, the structure of the problem leads to a very compact `O(n log n)` solution after sorting.

The tricky cases come from duplicate values around the boundary.

Consider this input:

```
7 3 4
1 2 3 3 3 4 5
```

After sorting, the fourth smallest value is `3`, and the fifth smallest value is also `3`.

We would need:

```
3 ≤ x < 3
```

which is impossible. The correct answer is `0`.

A careless implementation might try to count numbers between the two boundary positions inclusively and accidentally return `1`.

Another subtle case happens when there is a large gap:

```
5 2 3
1 2 10 20 30
```

Here:

```
L = 2
R = 10
```

Any integer from `2` through `9` works, so the answer is `8`.

The valid values are not restricted to existing difficulties. They are all integers in the gap.

## Approaches

The brute-force idea is straightforward. We can try every possible integer `x`, count how many chores satisfy `h[i] ≤ x`, and check whether that count equals `b`.

The smallest difficulty is at least `1`, and the largest can reach `10^9`, so iterating through all possible `x` values is completely unrealistic. Even if each check took only `O(n)`, scanning up to `10^9` integers would require around `2 × 10^12` operations in the worst case.

The key observation is that only the boundary between Vasya's chores and Petya's chores matters.

Once the array is sorted, the first `b` elements must belong to Vasya and the remaining `a` elements must belong to Petya. The exact values inside those groups do not matter anymore.

Suppose:

```
sorted_h[b - 1] = L
sorted_h[b] = R
```

For Vasya to still receive exactly `b` chores, `x` must be at least `L`, because Vasya's hardest assigned chore must satisfy `h[i] ≤ x`.

For Petya to still receive exactly `a` chores, `x` must be strictly smaller than `R`, because Petya's easiest assigned chore must satisfy `h[i] > x`.

That means the valid integers are exactly:

```
L, L + 1, ..., R - 1
```

The count is:

```
R - L
```

If `L == R`, the answer naturally becomes `0`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^9 · n) | O(1) | Too slow |
| Optimal | O(n log n) | O(1) extra space apart from sorting | Accepted |

## Algorithm Walkthrough

1. Read the values `n`, `a`, and `b`, along with the list of chore difficulties.
2. Sort the difficulty array in nondecreasing order.

After sorting, the first `b` chores are the only possible chores Vasya can receive if he must take exactly `b` smallest acceptable chores.
3. Let:

```
L = h[b - 1]
R = h[b]
```

`L` is the largest difficulty assigned to Vasya, and `R` is the smallest difficulty assigned to Petya.
4. Every valid integer `x` must satisfy:

```
L ≤ x < R
```

The left condition guarantees Vasya keeps all his chores. The right condition guarantees Petya keeps all his chores.
5. The number of integers in that interval is:

```
R - L
```
6. Print `R - L`.

### Why it works

After sorting, the division point between the two brothers is fixed. Vasya must receive exactly the first `b` chores, and Petya must receive exactly the remaining `a` chores.

For every chore assigned to Vasya, we need `h[i] ≤ x`. The strongest restriction comes from Vasya's hardest chore, which has value `L`.

For every chore assigned to Petya, we need `h[i] > x`. The strongest restriction comes from Petya's easiest chore, which has value `R`.

So the valid integers are precisely those between these two boundaries. Any smaller value excludes one of Vasya's chores, and any larger value includes one of Petya's chores.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())
    h = list(map(int, input().split()))

    h.sort()

    print(h[b] - h[b - 1])

solve()
```

The solution relies entirely on the sorted order.

After sorting, index `b - 1` is the last chore assigned to Vasya, while index `b` is the first chore assigned to Petya. Python uses zero-based indexing, so these positions are correct even though the problem describes the chores conceptually using one-based ordering.

The answer is simply the number of integers from `h[b - 1]` through `h[b] - 1`, which equals `h[b] - h[b - 1]`.

A common off-by-one mistake is trying to use `h[a - 1]` and `h[a]`. The boundary is determined by Vasya's count, not Petya's count, because the first `b` sorted elements belong to Vasya.

Another easy mistake is subtracting one manually:

```
h[b] - h[b - 1] - 1
```

That would incorrectly exclude the left endpoint, even though `x = h[b - 1]` is valid.

## Worked Examples

### Sample 1

Input:

```
5 2 3
6 2 3 100 1
```

Sorted array:

```
[1, 2, 3, 6, 100]
```

| Step | Value |
| --- | --- |
| `b` | 3 |
| `h[b - 1]` | 3 |
| `h[b]` | 6 |
| Answer | `6 - 3 = 3` |

The valid integers are:

```
3, 4, 5
```

This trace shows that every integer inside the boundary gap works, not only values already present in the array.

### Sample 2

Suppose the input is:

```
7 3 4
1 2 3 3 3 4 5
```

Sorted array:

```
[1, 2, 3, 3, 3, 4, 5]
```

| Step | Value |
| --- | --- |
| `b` | 4 |
| `h[b - 1]` | 3 |
| `h[b]` | 3 |
| Answer | `3 - 3 = 0` |

There is no integer `x` satisfying:

```
3 ≤ x < 3
```

This example demonstrates the duplicate-boundary edge case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime |
| Space | O(1) extra space apart from sorting | Only a few variables are used |

With `n ≤ 2000`, the runtime is tiny. Sorting 2000 integers is effectively instantaneous within the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, a, b = map(int, input().split())
    h = list(map(int, input().split()))

    h.sort()

    print(h[b] - h[b - 1])

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue()

# provided sample
assert run(
    "5 2 3\n"
    "6 2 3 100 1\n"
) == "3\n", "sample 1"

# minimum size
assert run(
    "2 1 1\n"
    "1 2\n"
) == "1\n", "minimum size"

# all equal values
assert run(
    "4 2 2\n"
    "5 5 5 5\n"
) == "0\n", "all equal"

# large gap
assert run(
    "5 2 3\n"
    "1 2 10 20 30\n"
) == "8\n", "multiple valid x values"

# boundary duplicate
assert run(
    "7 3 4\n"
    "1 2 3 3 3 4 5\n"
) == "0\n", "duplicate boundary"

# off-by-one check
assert run(
    "5 4 1\n"
    "1 2 3 4 5\n"
) == "1\n", "single valid value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1 / 1 2` | `1` | Minimum valid input |
| `4 2 2 / 5 5 5 5` | `0` | All values equal |
| `5 2 3 / 1 2 10 20 30` | `8` | Large interval of valid integers |
| `7 3 4 / 1 2 3 3 3 4 5` | `0` | Duplicate boundary values |
| `5 4 1 / 1 2 3 4 5` | `1` | Off-by-one boundary correctness |

## Edge Cases

Consider the duplicate-boundary case:

```
7 3 4
1 2 3 3 3 4 5
```

After sorting:

```
[1, 2, 3, 3, 3, 4, 5]
```

We compute:

```
L = h[3] = 3
R = h[4] = 3
```

The algorithm returns:

```
3 - 3 = 0
```

This is correct because no integer can simultaneously satisfy:

```
x ≥ 3
x < 3
```

Now consider the large-gap case:

```
5 2 3
1 2 10 20 30
```

After sorting:

```
[1, 2, 10, 20, 30]
```

We get:

```
L = 2
R = 10
```

The algorithm returns:

```
10 - 2 = 8
```

The valid integers are:

```
2, 3, 4, 5, 6, 7, 8, 9
```

This confirms that the answer counts every integer in the interval, not only difficulties already present in the array.

Finally, examine the smallest possible input:

```
2 1 1
1 2
```

After sorting:

```
[1, 2]
```

We compute:

```
L = 1
R = 2
```

The algorithm returns `1`, meaning only `x = 1` works.

If `x = 0`, Vasya receives no chores. If `x = 2`, Petya receives no chores. The boundary logic still works perfectly at minimum size.

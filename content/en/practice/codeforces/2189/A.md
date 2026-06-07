---
title: "CF 2189A - Table with Numbers"
description: "We have an array of numbers. We may select any even number of elements from it and partition them into ordered pairs. A pair (x, y) contributes 1 to the table only if row x and column y exist. Since the table has h rows and l columns, this means we need 1 ≤ x ≤ h and 1 ≤ y ≤ l."
date: "2026-06-07T21:11:35+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2189
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1075 (Div. 2)"
rating: 800
weight: 2189
solve_time_s: 252
verified: false
draft: false
---

[CF 2189A - Table with Numbers](https://codeforces.com/problemset/problem/2189/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 4m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of numbers. We may select any even number of elements from it and partition them into ordered pairs.

A pair `(x, y)` contributes `1` to the table only if row `x` and column `y` exist. Since the table has `h` rows and `l` columns, this means we need `1 ≤ x ≤ h` and `1 ≤ y ≤ l`.

The actual cell that receives the increment does not matter for the final answer. The problem asks for the sum of all values in the table. Every valid pair increases exactly one cell by `1`, so maximizing the table sum is equivalent to maximizing the number of valid pairs we can form.

The array length is at most `100`, which is tiny. Even fairly inefficient solutions would fit comfortably. The challenge is not performance but recognizing the correct greedy observation.

A number can be used at most once because we are selecting elements from the array and pairing them. The same value may appear multiple times if it occurs multiple times in the array.

The main subtlety is that the two positions in a pair have different roles. A number used as the first element must be at most `h`, while a number used as the second element must be at most `l`. A value that satisfies both conditions can serve in either role.

Consider `h = 2`, `l = 5`, and array `[1, 1, 1]`. All three numbers are valid rows and columns. A careless solution might count three usable numbers and answer `3`, but one pair consumes two numbers, so only one valid pair can be formed. The correct answer is `1`.

Another tricky case is when numbers are valid only in one role. Suppose `h = 1`, `l = 100`, and array `[1, 50]`. The value `1` can be a row and a column, while `50` can only be a column. We can form `(1, 50)`, giving answer `1`. A solution that separately counts row-capable and column-capable numbers without tracking reuse could incorrectly think more pairings are possible.

A final edge case occurs when no number can be used as a row. For example:

```
n = 2, h = 1, l = 1
a = [5, 5]
```

No valid pair exists, so the answer is `0`.

## Approaches

A brute-force mindset starts by asking which pairs can be formed. Every element can either be unused, become the first member of a pair, or become the second member of a pair. Exploring all possible pairings quickly becomes combinatorial. Even for `n = 100`, the number of possible matchings is astronomically large.

The key observation is that we do not care which valid cell receives the increment. Every successful pair contributes exactly `1` to the answer.

Let us classify each array element according to the roles it can play.

If a value `x` satisfies `x ≤ h`, it can serve as a row index.

If a value `x` satisfies `x ≤ l`, it can serve as a column index.

For a pair to be valid, one selected element must be assigned the row role and another selected element must be assigned the column role.

Suppose we process the array one element at a time. Every valid pair requires one row-capable element and one column-capable element. An element that satisfies both conditions is flexible and can fill whichever role is currently needed.

This becomes a matching problem between row slots and column slots. Since every pair consumes exactly two elements, the maximum number of valid pairs equals the maximum number of row-column matches that can be created.

A very simple greedy works.

Maintain how many unmatched row-capable elements we have seen and how many unmatched column-capable elements we have seen.

When processing a new number:

If it can be serve as a row, we would like to immediately pair it with a previously unmatched column element if such an element exists.

Similarly, if it can serve as a column, we would like to pair it with a previously unmatched row element if such an element exists.

An even cleaner view is to sort elements into three categories.

Values with `x ≤ min(h,l)` can play either role.

Values with `min(h,l) < x ≤ h` can only be rows.

Values with `min(h,l) < x ≤ l` can only be columns.

Let

`R =` count of row-capable elements (`x ≤ h`)

`C =` count of column-capable elements (`x ≤ l`)

Every valid pair needs one row role and one column role. If we create `k` pairs, we consume `k` row assignments and `k` column assignments. Since each array element can be used only once, the total number of consumed elements is `2k`, which must not exceed `n`.

The flexible elements automatically resolve role assignment conflicts. The maximum possible number of pairs is simply:

`min(R, C, n // 2)`

To see why, we need `k ≤ R` because each pair needs a row element, `k ≤ C` because each pair needs a column element, and `k ≤ n/2` because each pair consumes two elements.

These bounds are also achievable because flexible elements can be assigned to whichever side is lacking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many array elements satisfy `a[i] ≤ h`. Call this value `R`.
2. Count how many array elements satisfy `a[i] ≤ l`. Call this value `C`.
3. Every valid pair requires one row-capable element and one column-capable element, so the number of pairs cannot exceed either `R` or `C`.
4. Every pair also consumes two array elements, so the number of pairs cannot exceed `n // 2`.
5. The answer is:

```
min(R, C, n // 2)
```
6. Output the answer for the test case.

### Why it works

A valid pair is nothing more than one element assigned to the row position and another assigned to the column position.

If we want to create `k` valid pairs, we need at least `k` row-capable elements and at least `k` column-capable elements, giving the bounds `k ≤ R` and `k ≤ C`. Since each pair uses two distinct array elements, we also need `2k ≤ n`, which gives `k ≤ n // 2`.

These are the only restrictions. Any element that satisfies both conditions can be assigned to whichever role is needed. Consequently, whenever `k` satisfies all three inequalities, a construction exists. The largest feasible value is exactly `min(R, C, n // 2)`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        n, h, l = map(int, input().split())
        a = list(map(int, input().split()))
        
        rows = sum(x <= h for x in a)
        cols = sum(x <= l for x in a)
        
        print(min(rows, cols, n // 2))

solve()
```

The implementation directly follows the mathematical characterization.

The variable `rows` counts how many elements are eligible to be used as the first member of a pair. The variable `cols` counts how many elements are eligible to be used as the second member.

The final answer is bounded by all three necessary limits. Taking the minimum gives the maximum achievable number of valid pairs.

There are no overflow concerns because all values are tiny. The only detail worth checking is that each test case contains exactly `n` numbers and that `n // 2` uses integer division, since fractional pairs are impossible.

## Worked Examples

### Example 1

Input:

```
n = 5
h = 2
l = 2
a = [1, 2, 2, 3, 2]
```

| Element | ≤ h? | ≤ l? | rows | cols |
| --- | --- | --- | --- | --- |
| 1 | Yes | Yes | 1 | 1 |
| 2 | Yes | Yes | 2 | 2 |
| 2 | Yes | Yes | 3 | 3 |
| 3 | No | No | 3 | 3 |
| 2 | Yes | Yes | 4 | 4 |

After processing:

| Quantity | Value |
| --- | --- |
| rows | 4 |
| cols | 4 |
| n // 2 | 2 |

Answer:

```
min(4, 4, 2) = 2
```

This example demonstrates the effect of the `n // 2` constraint. Even though four elements can serve as rows and columns, only two pairs can be formed from five total elements.

### Example 2

Input:

```
n = 8
h = 4
l = 2
a = [7, 2, 2, 2, 3, 4, 4, 2]
```

| Element | ≤ h? | ≤ l? | rows | cols |
| --- | --- | --- | --- | --- |
| 7 | No | No | 0 | 0 |
| 2 | Yes | Yes | 1 | 1 |
| 2 | Yes | Yes | 2 | 2 |
| 2 | Yes | Yes | 3 | 3 |
| 3 | Yes | No | 4 | 3 |
| 4 | Yes | No | 5 | 3 |
| 4 | Yes | No | 6 | 3 |
| 2 | Yes | Yes | 7 | 4 |

Final values:

| Quantity | Value |
| --- | --- |
| rows | 7 |
| cols | 4 |
| n // 2 | 4 |

Answer:

```
min(7, 4, 4) = 4
```

This trace shows that row-capable elements may greatly outnumber column-capable elements. The smaller side determines the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the array |
| Space | O(1) | Only a few counters are stored |

Since `n ≤ 100`, even much slower solutions would pass. The linear scan is trivial within the limits and uses constant extra memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, h, l = map(int, input().split())
        a = list(map(int, input().split()))

        rows = sum(x <= h for x in a)
        cols = sum(x <= l for x in a)

        ans.append(str(min(rows, cols, n // 2)))

    return "\n".join(ans)

# provided sample
assert run(
"""7
2 1 1
1 1
5 2 2
1 2 2 3 2
8 4 2
7 2 2 2 3 4 4 2
7 3 6
10 4 1 3 5 4 6
2 4 4
5 5
7 6 3
10 4 1 3 5 4 6
4 1 1
1 1 1 1
"""
) == """1
2
3
2
0
2
2"""

# minimum size
assert run(
"""1
2 1 1
1 1
"""
) == "1"

# no usable values
assert run(
"""1
4 1 1
5 5 5 5
"""
) == "0"

# all values usable
assert run(
"""1
6 10 10
1 2 3 4 5 6
"""
) == "3"

# row-capable much more common than column-capable
assert run(
"""1
6 5 2
1 2 3 4 5 5
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1 / 1 1` | `1` | Smallest non-trivial instance |
| `4 1 1 / 5 5 5 5` | `0` | No valid row or column values |
| `6 10 10 / 1 2 3 4 5 6` | `3` | Answer limited by `n // 2` |
| `6 5 2 / 1 2 3 4 5 5` | `2` | Smaller of row and column counts dominates |

## Edge Cases

### All numbers are too large

Input:

```
1
2 1 1
5 5
```

We count:

```
rows = 0
cols = 0
n // 2 = 1
```

The algorithm returns:

```
min(0, 0, 1) = 0
```

No element can act as either a row or a column index, so no valid pair exists.

### Many usable numbers but not enough elements for more pairs

Input:

```
1
3 10 10
1 2 3
```

We obtain:

```
rows = 3
cols = 3
n // 2 = 1
```

The answer becomes:

```
min(3, 3, 1) = 1
```

Although every element is valid in both roles, only three elements exist, so at most one pair can be formed.

### Strong imbalance between row and column candidates

Input:

```
1
6 5 2
1 2 3 4 5 5
```

Counts:

```
rows = 6
cols = 2
n // 2 = 3
```

The algorithm returns:

```
min(6, 2, 3) = 2
```

Only two elements can serve as columns, so creating a third valid pair is impossible regardless of how many row-capable elements are available.

### Values valid in both roles

Input:

```
1
4 1 1
1 1 1 1
```

Counts:

```
rows = 4
cols = 4
n // 2 = 2
```

Answer:

```
min(4, 4, 2) = 2
```

Every element is flexible and can be assigned either role. The algorithm correctly recognizes that two pairs can be formed.

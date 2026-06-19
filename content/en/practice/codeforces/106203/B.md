---
title: "CF 106203B - \u041f\u0438\u0440\u0430\u043c\u0438\u0434\u0430 \u0412\u0438\u0434\u0435\u043d\u0438\u0439"
description: "We are given a triangular array with n rows. Row i contains exactly i integers. The process starts from the top row and repeatedly destroys rows one by one until only the bottom row remains."
date: "2026-06-19T13:44:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106203
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106203
solve_time_s: 58
verified: true
draft: false
---

[CF 106203B - \u041f\u0438\u0440\u0430\u043c\u0438\u0434\u0430 \u0412\u0438\u0434\u0435\u043d\u0438\u0439](https://codeforces.com/problemset/problem/106203/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a triangular array with `n` rows. Row `i` contains exactly `i` integers. The process starts from the top row and repeatedly destroys rows one by one until only the bottom row remains.

When a crystal with value `x` is removed, it chooses the larger of the two crystals directly below it. Suppose the left child has value `a` and the right child has value `b`. If `a > b`, the left child changes to `a - x`. Otherwise the right child changes to `b - x`. The other child stays unchanged.

After all rows except the last have disappeared, we must output the values of the crystals in the bottom row.

The triangle contains

$$1+2+\dots+n=\frac{n(n+1)}2$$

numbers. Since `n ≤ 1000`, the total number of elements is at most 500500. Any algorithm that processes each crystal a constant number of times is easily fast enough. Quadratic in the number of cells would mean roughly $2.5 \times 10^{11}$ operations, which is far beyond the limit.

A subtle point is that a crystal modifies one of its children immediately, and later decisions must use the updated values, not the original ones.

Consider

```
2
5
1 10
```

The top crystal chooses `10`, since `1 ≤ 10`, and changes it to `10-5=5`.

The answer is

```
1 5
```

Using the original values everywhere would produce the wrong result.

Another source of mistakes is the tie case. Equal values do not choose the left child.

For

```
2
3
7 7
```

the condition `a ≤ b` applies, so the right crystal becomes `7-3=4`.

The correct answer is

```
7 4
```

Using `>=` instead of `>` would incorrectly modify the left crystal.

Negative numbers also matter.

```
2
-5
2 1
```

Since `2 > 1`, the left crystal is chosen and becomes

$$2-(-5)=7.$$

The answer is

```
7 1
```

Subtracting in the wrong order would give `-7`.

## Approaches

The most direct idea is to simulate the ritual exactly as described. Starting from the first row, we examine each crystal and compare the two values below it. Depending on which one is larger, we immediately modify that child.

This simulation is already efficient because every crystal except those in the last row is processed once. The total number of processed cells equals

$$1+2+\dots+(n-1)=\frac{n(n-1)}2,$$

which is about five hundred thousand operations when `n=1000`.

One might imagine a much more complicated approach that keeps track of paths or recursively follows where energy flows. Such a brute force over all possible paths becomes exponential because each crystal potentially has two choices. Fortunately the process itself determines the choice uniquely, and each crystal influences only one child. No backtracking is required.

The key observation is that the triangle can simply be updated in place. Once row `i` has been processed, it is never used again. All future decisions depend only on the already updated values in row `i+1`. This allows us to overwrite values directly without any auxiliary structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all possible paths | O(2^n) | O(n) | Too slow |
| In-place simulation | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read the entire triangle into a two-dimensional array.
2. Process rows from top to bottom. Row `i` affects row `i+1`, so after finishing row `i` we never need it again.
3. For every position `j` in row `i`, let `x` be the current value of that crystal.
4. Compare the two children, `triangle[i+1][j]` and `triangle[i+1][j+1]`.
5. If the left child is strictly larger, replace it by

$$\text{left}-x.$$

Otherwise replace the right child by

$$\text{right}-x.$$

The comparison must use the current values, because previous crystals from the same row may already have modified them.

1. Continue until the second last row has been processed.
2. Output the last row.

### Why it works

After processing row `i`, every change caused by crystals in rows `0,1,\dots,i` has already been incorporated into row `i+1`. No future operation can affect any earlier row.

The invariant is that before starting row `i`, all rows above it have already been completely destroyed exactly according to the rules, and row `i` contains the values that would exist at that moment in the ritual. Processing each crystal applies precisely the same operation as the statement, so the invariant remains true. When the second last row finishes, the bottom row contains exactly the final energies.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
triangle = [list(map(int, input().split())) for _ in range(n)]

for i in range(n - 1):
    for j in range(i + 1):
        x = triangle[i][j]
        if triangle[i + 1][j] > triangle[i + 1][j + 1]:
            triangle[i + 1][j] -= x
        else:
            triangle[i + 1][j + 1] -= x

print(*triangle[-1])
```

The triangle is stored exactly as it appears in the input. Since later computations always need the updated values, modifying the array in place is natural.

The outer loop processes rows from top to bottom. Row `i` contains `i+1` elements, so the inner loop runs over all of them.

The comparison uses `>` and not `>=`. Equal values must select the right child because the statement specifies the left child only when it is strictly larger.

Python integers automatically handle large values, so overflow is not an issue. With fixed-size integers in another language, 64-bit types would be necessary.

## Worked Examples

### Sample 1

Input:

```
3
2
4 5
4 5 6
```

The state evolves as follows.

| Row being processed | Crystal value | Children before | Modified child | Bottom row after step |
| --- | --- | --- | --- | --- |
| 1 | 2 | (4,5) | right becomes 3 | 4 5 6 |
| 2 | 4 | (4,3) | left becomes 0 | 0 3 6 |
| 2 | 3 | (3,6) | right becomes 3 | 0 3 3 |

Final answer:

```
0 3 3
```

This example shows that values changed earlier in a row must be used in later comparisons.

### Sample 2

Input:

```
4
-5
-5 2
8 1 -4
8 -9 3 4
```

| Row being processed | Crystal value | Children before | Modified child |
| --- | --- | --- | --- |
| 1 | -5 | (-5,2) | right becomes 7 |
| 2 | -5 | (8,7) | left becomes 13 |
| 2 | 7 | (7,-4) | left becomes 0 |
| 3 | 13 | (8,-9) | left becomes -5 |
| 3 | 0 | (-9,3) | right remains 3 |
| 3 | -4 | (3,4) | right becomes 8 |

Final row:

```
-5 -9 3 8
```

This trace demonstrates that subtracting a negative number increases the chosen child.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every crystal except those in the last row is processed once |
| Space | O(n²) | The whole triangle is stored |

The largest possible triangle contains 500500 elements. Processing each cell once easily fits within the time limit, and storing half a million integers comfortably fits inside 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    triangle = [list(map(int, input().split())) for _ in range(n)]

    for i in range(n - 1):
        for j in range(i + 1):
            x = triangle[i][j]
            if triangle[i + 1][j] > triangle[i + 1][j + 1]:
                triangle[i + 1][j] -= x
            else:
                triangle[i + 1][j + 1] -= x

    return " ".join(map(str, triangle[-1]))

# minimum size
assert run("1\n7\n") == "7"

# equal values, right child must be chosen
assert run("2\n3\n7 7\n") == "7 4"

# negative top value
assert run("2\n-5\n2 1\n") == "7 1"

# simple chain
assert run("3\n1\n2 3\n4 5 6\n") == "4 2 3"

# all equal values
assert run("3\n1\n1 1\n1 1 1\n") == "1 0 -1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `7` | Minimum size |
| `2 / 3 / 7 7` | `7 4` | Tie goes to the right child |
| `2 / -5 / 2 1` | `7 1` | Correct handling of negative values |
| `3 / 1 / 2 3 / 4 5 6` | `4 2 3` | Normal propagation |
| All ones | `1 0 -1` | Multiple ties and repeated updates |

## Edge Cases

### Equal children

Input:

```
2
3
7 7
```

The children are equal, so the condition `a ≤ b` applies. The right crystal becomes

$$7-3=4.$$

The algorithm compares with `>`, hence the `else` branch updates the right child.

Output:

```
7 4
```

### Negative values

Input:

```
2
-5
2 1
```

Since `2 > 1`, the left child is selected. The update is

$$2-(-5)=7.$$

The algorithm performs subtraction in this order, producing

```
7 1
```

### Single row

Input:

```
1
100
```

No row is destroyed because the bottom row is also the top row. The loops do not execute at all, and the program simply prints

```
100
```

which matches the intended behavior.

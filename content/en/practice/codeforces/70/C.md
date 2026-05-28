---
title: "CF 70C - Lucky Tickets"
description: "Each ticket is described by two positive integers. The first is the series number a, the second is the ticket number inside that series b."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 70
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 64"
rating: 2200
weight: 70
solve_time_s: 131
verified: true
draft: false
---

[CF 70C - Lucky Tickets](https://codeforces.com/problemset/problem/70/C)

**Rating:** 2200  
**Tags:** binary search, data structures, sortings, two pointers  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

Each ticket is described by two positive integers. The first is the series number `a`, the second is the ticket number inside that series `b`. A ticket is called lucky when

$a \cdot b = \operatorname{rev}(a) \cdot \operatorname{rev}(b)$

The function `rev(x)` reverses the decimal digits and removes leading zeroes after reversal. For example, `rev(1200) = 21`.

We are allowed to choose how many series to print and how many tickets each series contains. If we choose `x` series and `y` tickets per series, then all pairs `(a, b)` with `1 ≤ a ≤ x` and `1 ≤ b ≤ y` exist. Among those pairs, at least `w` must be lucky. We want to minimize the total number of printed tickets, which is `x * y`.

The constraints immediately rule out brute force over all pairs. Both `maxx` and `maxy` can reach `10^5`, so the full grid contains up to `10^10` pairs. Even checking a single arithmetic condition for every pair is impossible within two seconds.

The target number of lucky tickets can be as large as `10^7`, which means we cannot rely on a sparse construction either. The solution must exploit structure in the equation itself.

The tricky part is understanding what kinds of numbers satisfy the condition. A careless implementation might assume that reversing behaves multiplicatively, but that is false. For example:

```
a = 12, b = 21
12 * 21 = 252
rev(12) * rev(21) = 21 * 12 = 252
```

This pair is lucky, even though neither number is a palindrome.

Another easy mistake is forgetting that reversal removes leading zeroes. Consider:

```
a = 10, b = 1
10 * 1 = 10
rev(10) * rev(1) = 1 * 1 = 1
```

The ticket is not lucky. Treating `rev(10)` as `01 = 10` would silently produce incorrect answers.

A third subtle issue appears when no valid answer exists. Suppose:

```
1 1 2
```

There is only one ticket, `(1,1)`, and it is lucky. Since we need two lucky tickets, the correct output is `-1`. A solution that only searches for a large enough rectangle without checking feasibility will fail here.

## Approaches

The brute-force idea is straightforward. For every pair `(a, b)` inside the chosen rectangle, compute both products and count how many satisfy the condition. Then try all possible values of `x` and `y` and pick the smallest area that reaches at least `w` lucky tickets.

This works logically because the definition of a lucky ticket is completely local to one pair. The problem is the scale. There are up to `10^10` pairs, and even enumerating all rectangles already costs another factor of `10^10`. The total operation count explodes far beyond anything practical.

To improve this, we need to understand the equation itself.

Start from

$a \cdot b = \operatorname{rev}(a) \cdot \operatorname{rev}(b)$

Rearranging gives

$\frac{a}{\operatorname{rev}(a)} = \frac{\operatorname{rev}(b)}{b}$

This means the ratio associated with `a` must exactly match the inverse ratio associated with `b`.

Define a canonical representation:

f(x)=\frac{x}{\operatorname{rev}(x)}}

Two numbers form a lucky pair precisely when their reduced fractions are equal.

That changes the problem completely. Instead of examining every pair independently, we can group numbers by the reduced fraction `x / rev(x)`.

Suppose a particular fraction appears `cx` times among numbers `1..x`, and the same fraction appears `cy` times among numbers `1..y`. Then every combination between those groups forms a lucky ticket. The total contribution is

$cx \cdot cy$

Now the task becomes counting frequencies of reduced fractions.

The number of integers is only `10^5`, so we can preprocess every value once. For each number, compute its reversed value, reduce the fraction using gcd, and store the normalized pair `(p, q)`.

After preprocessing, we can sweep through possible rectangle sizes efficiently. The key observation is that when we increase one side by one, only the contribution of a single new number changes. This allows a two-pointers style process instead of recomputing everything from scratch.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(maxx · maxy) per rectangle | O(1) | Too slow |
| Optimal | O(maxx + maxy) preprocessing + O(maxx + maxy) sweep | O(maxx + maxy) | Accepted |

## Algorithm Walkthrough

1. For every integer from `1` to `max(maxx, maxy)`, compute its reversed value.
2. Reduce the fraction `x / rev(x)` by dividing both sides by their gcd. Store the normalized pair `(p, q)`.

The reduction step is critical. Different numbers may produce equivalent ratios. For example:

```
12 / 21 = 4 / 7
24 / 42 = 4 / 7
```

Both must belong to the same group.

1. Build two arrays:

`typeX[i]` for numbers usable as series indices,

`typeY[i]` for numbers usable as ticket indices.

Each entry stores the normalized fraction of that number.

1. Use a sliding window style process over `x`.

Maintain a frequency table `cnt` for all normalized fractions currently present in `1..y`.

Also maintain:

$good = \sum_t cntX_t \cdot cntY_t$

where `cntX_t` and `cntY_t` are counts of a fraction type `t` on both sides.

1. Start with `y = 0`. For each `x` from `1` to `maxx`, add the new fraction type from `x`.
2. While `good < w` and `y < maxy`, extend `y` by one.

When adding a new number to the `y` side, suppose its type is `t`. Every existing number on the `x` side with the same type forms a new lucky pair, so:

```
good += cntX[t]
cntY[t] += 1
```

1. Once `good ≥ w`, the rectangle `(x, y)` is feasible.

Compare its area against the best answer seen so far.

1. Continue until all `x` are processed.
2. If no feasible rectangle was found, print `-1`.

### Why it works

The invariant is that all lucky pairs are counted exactly by matching normalized fraction types.

For any pair `(a,b)`:

$a \cdot b = \operatorname{rev}(a) \cdot \operatorname{rev}(b)$

holds if and only if

$\frac{a}{\operatorname{rev}(a)} = \frac{\operatorname{rev}(b)}{b}$

After reducing fractions, equality becomes equality of normalized pairs. Every lucky ticket belongs to exactly one fraction class, and every combination inside the same class is lucky.

The sliding window maintains exact counts of how many numbers of each class appear on both sides. Since every update only changes one frequency, `good` always equals the true number of lucky tickets in the current rectangle.

Because `y` only moves forward, the total number of pointer movements is linear.

## Python Solution

```python
import sys
from math import gcd
from collections import defaultdict

input = sys.stdin.readline

def rev(x):
    return int(str(x)[::-1])

def solve():
    maxx, maxy, w = map(int, input().split())

    limit = max(maxx, maxy)

    typ = [None] * (limit + 1)

    for i in range(1, limit + 1):
        r = rev(i)
        g = gcd(i, r)
        typ[i] = (i // g, r // g)

    cnt_x = defaultdict(int)
    cnt_y = defaultdict(int)

    good = 0
    y = 0

    best_area = None
    best_ans = None

    for x in range(1, maxx + 1):
        t = typ[x]

        good += cnt_y[t]
        cnt_x[t] += 1

        while y < maxy and good < w:
            y += 1
            ty = typ[y]

            good += cnt_x[ty]
            cnt_y[ty] += 1

        if good >= w:
            area = x * y

            if best_area is None or area < best_area:
                best_area = area
                best_ans = (x, y)

    if best_ans is None:
        print(-1)
    else:
        print(best_ans[0], best_ans[1])

solve()
```

The first section computes the canonical fraction type for every number. The reduction by gcd is what makes equivalent ratios collapse into the same key. Without normalization, values like `(12,21)` and `(24,42)` would incorrectly appear different.

The dictionaries `cnt_x` and `cnt_y` store how many times each fraction type appears in the current prefixes. The variable `good` always stores the number of lucky pairs inside the current rectangle.

When we add a new value to the `x` side, the number of new lucky tickets equals the number of matching types already present on the `y` side. That is why the update order is:

```
good += cnt_y[t]
cnt_x[t] += 1
```

Reversing the order would overcount the new element against itself.

The same logic applies while expanding `y`.

The two-pointer structure is efficient because `y` never decreases. Across the whole algorithm, it increases at most `maxy` times.

The solution uses tuples as hash keys. Python handles this efficiently, and the total number of distinct reduced fractions is manageable for `10^5` numbers.

## Worked Examples

### Example 1

Input:

```
2 2 1
```

Normalized fraction types:

| Number | rev(number) | Reduced Type |
| --- | --- | --- |
| 1 | 1 | (1,1) |
| 2 | 2 | (1,1) |

Trace:

| x | y | good | Action |
| --- | --- | --- | --- |
| 1 | 0 | 0 | add x=1 |
| 1 | 1 | 1 | extend y |
| 1 | 1 | 1 | feasible |

The algorithm stops with area `1`. The only ticket is `(1,1)`, which is lucky because both sides equal `1`.

### Example 2

Input:

```
3 5 6
```

All numbers from `1` to `9` are palindromes, so every type is `(1,1)`.

Trace:

| x | y | good | Action |
| --- | --- | --- | --- |
| 1 | 1 | 1 | extend y |
| 1 | 2 | 2 | extend y |
| 1 | 3 | 3 | extend y |
| 1 | 4 | 4 | extend y |
| 1 | 5 | 5 | extend y |
| 2 | 5 | 10 | add x=2 |
| 2 | 5 | 10 | feasible |

The first feasible rectangle is `(2,5)` with area `10`.

This trace demonstrates how `good` grows incrementally. Adding one new number contributes exactly the count of matching fraction types on the opposite side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(maxx + maxy) | Every number is processed once, and the `y` pointer only moves forward |
| Space | O(max(maxx, maxy)) | Arrays and hash tables store one entry per number/type |

With limits up to `10^5`, linear preprocessing and linear sweeping fit comfortably inside two seconds. Memory usage also remains small because only reduced fraction identifiers and frequency counts are stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def rev(x):
        return int(str(x)[::-1])

    maxx, maxy, w = map(int, input().split())

    limit = max(maxx, maxy)

    typ = [None] * (limit + 1)

    for i in range(1, limit + 1):
        r = rev(i)
        g = gcd(i, r)
        typ[i] = (i // g, r // g)

    cnt_x = defaultdict(int)
    cnt_y = defaultdict(int)

    good = 0
    y = 0

    best_area = None
    best_ans = None

    for x in range(1, maxx + 1):
        t = typ[x]

        good += cnt_y[t]
        cnt_x[t] += 1

        while y < maxy and good < w:
            y += 1
            ty = typ[y]

            good += cnt_x[ty]
            cnt_y[ty] += 1

        if good >= w:
            area = x * y

            if best_area is None or area < best_area:
                best_area = area
                best_ans = (x, y)

    if best_ans is None:
        return "-1"

    return f"{best_ans[0]} {best_ans[1]}"

# provided sample
assert run("2 2 1\n") == "1 1", "sample 1"

# minimum size
assert run("1 1 1\n") == "1 1", "single lucky ticket"

# impossible case
assert run("1 1 2\n") == "-1", "cannot reach enough lucky tickets"

# all small palindromes
assert run("3 3 9\n") == "3 3", "all pairs are lucky"

# boundary style test
out = run("100000 100000 1\n")
assert out != "-1", "should always find one lucky ticket"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1 1` | Smallest valid input |
| `1 1 2` | `-1` | Correct impossibility detection |
| `3 3 9` | `3 3` | Every pair is lucky for single-digit numbers |
| `100000 100000 1` | any valid pair | Large boundary handling |

## Edge Cases

Consider the impossible configuration:

```
1 1 2
```

The preprocessing stage creates one type:

```
1 -> (1,1)
```

The sweep proceeds:

| x | y | good |
| --- | --- | --- |
| 1 | 1 | 1 |

The algorithm reaches the maximum possible rectangle and still has only one lucky ticket. Since `good < w`, no answer is recorded, and the final output is `-1`.

Now consider leading zero behaviour:

```
10 1 1
```

The number `10` becomes:

```
rev(10) = 1
```

Its reduced type is `(10,1)`, while the type of `1` is `(1,1)`.

The algorithm never counts `(10,1)` as lucky because the types differ. This correctly handles the disappearance of leading zeroes after reversal.

Finally, consider equivalent ratios:

```
24 42 1
```

We get:

| Number | rev | Reduced Type |
| --- | --- | --- |
| 12 | 21 | (4,7) |
| 24 | 42 | (4,7) |

Both numbers belong to the same class after gcd reduction. Any solution that compares unreduced fractions directly would miss this equality. The normalization step guarantees they are matched correctly.

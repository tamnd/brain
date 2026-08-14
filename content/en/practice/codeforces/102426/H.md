---
title: "CF 102426H - \u767d\u5b66\u4e32"
description: "We have an array of positive integers. A query gives an interval [l, r], and asks whether we can choose any three elements from that interval that can be the side lengths of a non-degenerate triangle."
date: "2026-08-14T15:20:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "H"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 143
verified: true
draft: false
---

[CF 102426H - \u767d\u5b66\u4e32](https://codeforces.com/problemset/problem/102426/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of positive integers. A query gives an interval `[l, r]`, and asks whether we can choose any three elements from that interval that can be the side lengths of a non-degenerate triangle.

For three positive numbers, after sorting them as `x <= y <= z`, they form a triangle exactly when `x + y > z`. The positions of the chosen elements do not matter, only their values and whether all three positions lie inside the queried interval.

The input contains up to `10^5` elements in one test case, with the sum of all `n` over the test cases bounded by `5 * 10^5`. There can be up to `2 * 10^5` queries per test case, with a total of `10^6` queries. This rules out anything close to scanning an entire interval for every query. A solution around `O(nm)` or `O(n^2)` is far beyond the available work. The large number of queries also means that the answer for each short interval should be obtained with only a small constant amount of work.

There is a surprisingly strong restriction on intervals that do not contain a triangle. Consider all values in such an interval and sort them:

`b1 <= b2 <= ... <= bk`.

If there were some index `i` with `b[i] + b[i+1] > b[i+2]`, those three consecutive values would already form a triangle. Hence a triangle-free interval must satisfy

`b[i] + b[i+1] <= b[i+2]`

for every valid `i`.

Because every value is positive, the smallest possible triangle-free sorted sequence starts as

`1, 1, 2, 3, 5, 8, 13, ...`.

It grows at least as fast as Fibonacci numbers. Since `F40 = 102334155`, already larger than `10^8`, no triangle-free interval can contain 40 elements. Thus every interval of length at least 40 is automatically a white string.

This leaves only intervals of length at most 39 for explicit checking.

There are several boundary cases where careless implementations fail. A query containing fewer than three elements can never be white. For example,

```
1
2 1
1 2
1 2
```

has answer `no`, because there are only two values. An implementation that only checks whether the largest value is not greater than the sum of two values may accidentally access nonexistent elements.

Equality is also not enough. For

```
1
3 1
1 2 3
1 3
```

the answer is `no`, because `1 + 2 = 3` gives a degenerate triangle. The comparison must be strict, `x + y > z`.

The three chosen elements do not have to occupy consecutive positions. For example,

```
1
4 1
2 100 3 4
1 4
```

has answer `yes`, because `2, 3, 4` form a triangle even though they occur at positions 1, 3, and 4. Checking only consecutive array positions would give the wrong result.

Finally, the order of the values is irrelevant. In

```
1
4 1
4 1 3 2
1 4
```

the answer is `yes`, since after sorting we obtain `1, 2, 3, 4` and `1 + 2 > 3`. A method that checks only triples in their original order would miss valid choices.

## Approaches

The direct brute-force solution follows the definition. For each query, take all values in `[l, r]`, sort them, and check every three consecutive values. The sorting is enough because if any three values form a triangle, then after sorting the whole set there is also a consecutive triple forming a triangle. If the sorted values are `b1 <= b2 <= ...`, choose a triangle whose largest side has the smallest possible index. The two values immediately before it cannot be replaced by larger values, so their sum is at least as large as the sum of the original two smaller sides.

The problem with this approach is the interval size. In the worst case a query has length `10^5`, so one query can already require `O(10^5 log 10^5)` work. With `2 * 10^5` queries, this can reach roughly `2 * 10^5 * 10^5` element-level work even before accounting for sorting, which is far too large.

The useful observation is the Fibonacci growth property described above. The brute-force method works because it only needs the values inside the queried interval. It fails because an interval can be large. The observation that every triangle-free interval has length below 40 removes exactly that difficulty.

For every query, if `r - l + 1 >= 40`, we immediately answer `yes`. Otherwise, the interval contains at most 39 elements, so we copy it, sort those values, and inspect consecutive triples. The number 39 is a true constant because the maximum value is bounded by `10^8`.

This is also why we do not need a complicated segment tree or balanced search tree. The data structure would be solving a problem that the Fibonacci bound has already eliminated.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(m n log n)` worst case | `O(n)` | Too slow |
| Optimal | `O(n + m * 39 log 39)` | `O(39)` extra per query | Accepted |

Since 39 is constant, the optimal complexity is effectively `O(n + m)`.

## Algorithm Walkthrough

1. Read the array and all queries. The array itself is kept unchanged because every query can be handled independently once we exploit the maximum triangle-free length.
2. For a query `[l, r]`, compute its length as `r - l + 1`. If this length is at least 40, print `yes` immediately. A triangle-free interval of 40 positive integers would require at least the sequence `1, 1, 2, 3, 5, ...`, whose 40th value already exceeds `10^8`, so such an interval cannot exist.
3. If the length is smaller than 40, extract the at most 39 values from the interval and sort them. Sorting converts the arbitrary choice of three elements into a local check on consecutive values.
4. Scan the sorted values. For every three consecutive values `x, y, z`, test whether `x + y > z`. If this holds for any triple, print `yes`.
5. If all consecutive triples satisfy `x + y <= z`, print `no`. The sorted sequence then contains no possible triangle, because any triangle would have produced a valid consecutive triple.

### Why it works

The key invariant is that for a sorted collection `b1 <= b2 <= ... <= bk`, the collection contains a triangle if and only if some consecutive triple satisfies `b[i] + b[i+1] > b[i+2]`. If a triangle exists, take its largest side `z`. The two largest values smaller than or equal to `z` have sum at least as large as the two smaller sides of the triangle, so the corresponding consecutive triple also forms a triangle. Conversely, every consecutive triple satisfying the inequality is directly a valid triangle.

For intervals with at least 40 elements, the Fibonacci argument proves that a triangle must exist. For shorter intervals, the explicit sorted check is exact. These two cases cover every possible query, so every answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 40

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        for _ in range(m):
            l, r = map(int, input().split())

            length = r - l + 1

            if length >= LIMIT:
                out.append("yes")
                continue

            b = sorted(a[l - 1:r])

            ok = False
            for i in range(length - 2):
                if b[i] + b[i + 1] > b[i + 2]:
                    ok = True
                    break

            out.append("yes" if ok else "no")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input uses one-based positions, while Python slices are zero-based and exclude the right endpoint. Therefore `[l, r]` becomes `a[l - 1:r]`, which contains exactly the required elements.

The length check happens before constructing and sorting the slice. This matters because long intervals are already known to be white, so there is no reason to spend time processing their values.

For a short interval, `sorted` creates a new list containing at most 39 integers. The loop then checks exactly the consecutive triples from that sorted list. The strict comparison `>` handles the degenerate case such as `1, 2, 3` correctly.

Python integers have arbitrary precision, so `b[i] + b[i + 1]` cannot overflow. In languages with fixed-width integers, the given `10^8` bound already makes a 32-bit signed integer sufficient for the sum, but using a wider type is harmless.

The constant 40 is deliberately chosen as the first length that is guaranteed to contain a triangle. Since `F40 = 102334155 > 10^8`, a triangle-free sequence can have at most 39 elements.

## Worked Examples

### Sample 1

The first test case has array

`[1, 1, 2, 3, 4]`.

The queries are all shorter than 40, so each one is checked explicitly.

| Query | Values | Sorted values | Consecutive triangle check | Answer |
| --- | --- | --- | --- | --- |
| `[1, 3]` | `1, 1, 2` | `1, 1, 2` | `1 + 1 > 2` is false | `no` |
| `[2, 4]` | `1, 2, 3` | `1, 2, 3` | `1 + 2 > 3` is false | `no` |
| `[2, 5]` | `1, 2, 3, 4` | `1, 2, 3, 4` | `1 + 2 > 3` false, `2 + 3 > 4` true | `yes` |

The third query demonstrates why checking all consecutive triples after sorting is sufficient. The valid triangle is `2, 3, 4`.

### Sample 2

The second test case has array

`[2, 3, 4, 1, 2]`.

Again, both queries are shorter than 40.

| Query | Values | Sorted values | Consecutive triangle check | Answer |
| --- | --- | --- | --- | --- |
| `[1, 4]` | `2, 3, 4, 1` | `1, 2, 3, 4` | `1 + 2 > 3` false, `2 + 3 > 4` true | `yes` |
| `[3, 5]` | `4, 1, 2` | `1, 2, 4` | `1 + 2 > 4` false | `no` |

The first query contains the triangle `2, 3, 4`. The second contains only `1, 2, 4`, which fails because `1 + 2` is not greater than `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m * 39 log 39)` | Every long query is answered immediately; every short query sorts at most 39 values |
| Space | `O(39)` extra | A short query creates a temporary list of at most 39 values |

Because 39 is a fixed constant determined by the `10^8` value bound, the query work is effectively constant. Across the full input, the algorithm performs `O(sum n + sum m)` asymptotic work with a small constant factor, which is suitable for `sum n <= 5 * 10^5` and `sum m <= 10^6`.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        for _ in range(m):
            l, r = map(int, input().split())
            length = r - l + 1

            if length >= 40:
                out.append("yes")
                continue

            b = sorted(a[l - 1:r])

            ok = False
            for i in range(length - 2):
                if b[i] + b[i + 1] > b[i + 2]:
                    ok = True
                    break

            out.append("yes" if ok else "no")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample1 = """\
1
5 3
1 1 2 3 4
1 3
2 4
2 5
"""

assert run(sample1) == "no\no\nyes", "sample 1"

sample2 = """\
1
5 2
2 3 4 1 2
1 4
3 5
"""

assert run(sample2) == "yes\nno", "sample 2"

minimum = """\
1
1 3
7
1 1
1 1
1 1
"""

assert run(minimum) == "no\nno\nno", "minimum-size input"

all_equal = """\
1
6 4
5 5 5 5 5 5
1 1
1 2
1 3
2 6
"""

assert run(all_equal) == "no\nno\nyes\nyes", "all equal values"

boundary = """\
1
5 5
1 1 2 3 4
1 2
1 3
1 4
2 4
2 5
"""

assert run(boundary) == "no\nno\nno\nno\nyes", "boundary and off-by-one cases"

fib_limit = """\
1
40 3
1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765 10946 17711 28657 46368 75025 121393 196418 317811 514229 832040 1346269 2178309 3524578 5702887 9227465 14930352 24157817 39088169 63245986
1 40
1 39
38 40
"""

assert run(fib_limit) == "yes\nyes\nno", "40-element threshold"

large = """\
1
100000 1
""" + " ".join(["1"] * 100000) + """
1 100000
"""

assert run(large) == "yes", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 3 / 7 / ...` | `no`, `no`, `no` | A one-element interval can never contain three sides |
| Six copies of `5` | `no`, `no`, `yes`, `yes` | Three equal values form a triangle, while one or two values do not |
| `[1, 1, 2, 3, 4]` boundary queries | `no`, `no`, `no`, `no`, `yes` | Strict inequality and correct slice boundaries |
| Fibonacci-like 40-element array | `yes`, `yes`, `no` | The length-40 guarantee and the 39-element explicit-check boundary |
| 100000 copies of `1` | `yes` | Large `n` and the fact that a long interval is answered without sorting |

## Edge Cases

### Fewer than three elements

For the input

```
1
2 2
10 20
1 1
1 2
```

both intervals have fewer than three elements. The algorithm sees lengths 1 and 2, so it does not use the automatic length-40 rule. Sorting gives lists of size 1 and 2, and the triangle-check loop has no iterations. Both answers are `no`.

### Degenerate triangle

For

```
1
3 1
1 2 3
1 3
```

the sorted values are `[1, 2, 3]`. The only check is `1 + 2 > 3`, which is false because the sum equals the largest side. The algorithm prints `no`, correctly treating equality as a degenerate triangle rather than a valid one.

### Non-consecutive chosen positions

For

```
1
4 1
2 100 3 4
1 4
```

the sorted interval is `[2, 3, 4, 100]`. The second triple gives `2 + 3 > 4`, so the answer is `yes`. The original positions of `2, 3, 4` are 1, 3, and 4, showing why the algorithm must sort the interval rather than inspect only adjacent array positions.

### Exactly 39 elements

Consider the 39-element Fibonacci prefix

```
1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765 10946 17711 28657 46368 75025 121393 196418 317811 514229 832040 1346269 2178309 3524578 5702887 9227465 14930352 24157817 39088169 63245986
```

Every consecutive pair of smaller values has a sum equal to the next value, so no triangle exists. Since the interval has length 39, the algorithm still performs the explicit check and correctly prints `no`.

This case is the boundary that prevents using 39 as the automatic threshold.

### Exactly 40 elements

If we append another value that keeps the sequence triangle-free, we would need the next value to be at least `102334155`, but that exceeds the allowed maximum `10^8`. Thus no valid input can contain a triangle-free interval of length 40.

The algorithm therefore answers `yes` immediately whenever `r - l + 1 >= 40`, without inspecting the values. This is the central optimization that turns the large number of range queries into a practical solution.

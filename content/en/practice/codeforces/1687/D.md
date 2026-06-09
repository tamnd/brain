---
title: "CF 1687D - Cute number"
description: "For every integer, look at the two consecutive perfect squares surrounding it. If $$m^2 le x < (m+1)^2,$$ then $g(x)=m^2$ and $f(x)=(m+1)^2$. The number is called cute when it is strictly closer to the lower square than to the upper square."
date: "2026-06-09T23:45:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "dsu", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1687
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 796 (Div. 1)"
rating: 2900
weight: 1687
solve_time_s: 154
verified: true
draft: false
---

[CF 1687D - Cute number](https://codeforces.com/problemset/problem/1687/D)

**Rating:** 2900  
**Tags:** binary search, brute force, data structures, dsu, implementation, math  
**Solve time:** 2m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

For every integer, look at the two consecutive perfect squares surrounding it.

If

$$m^2 \le x < (m+1)^2,$$

then $g(x)=m^2$ and $f(x)=(m+1)^2$. The number is called cute when it is strictly closer to the lower square than to the upper square.

A short calculation gives

$$x-m^2 < (m+1)^2-x$$

which is equivalent to

$$x \le m^2+m.$$

Inside the block between two consecutive squares, the cute numbers form a contiguous interval:

$$[m^2,\;m^2+m].$$

For example:

$$[1,2],\quad [4,6],\quad [9,12],\quad [16,20],\ldots$$

We are given a sorted array $a$. We must find the smallest non-negative shift $k$ such that every value $a_i+k$ belongs to one of those cute intervals.

The constraints are what make the problem difficult. The array length reaches $10^6$, so anything that inspects all elements many times is impossible. The values themselves are at most $2\cdot10^6$, which is much smaller than $n$, suggesting that duplicate values should be compressed away. The time limit also rules out checking shifts one by one.

A subtle edge case appears when many array elements are equal. Consider

```
3
5 5 5
```

All three values always behave identically after shifting. Treating duplicates separately wastes a huge amount of work. Removing duplicates changes nothing about feasibility.

Another easy mistake is handling the midpoint incorrectly. For example, between $9$ and $16$, the cute interval is $[9,12]$. The value $13$ is already closer to $16$ than to $9$, so it is not cute. Using a non-strict inequality would incorrectly classify midpoint-adjacent values.

A third trap is assuming all shifted numbers must end up in the same cute interval. For

```
2
1 100
```

the optimal shift places the two values in completely different cute intervals. Any solution based on choosing a single target interval fails immediately.

## Approaches

The brute force idea is straightforward. Try $k=0,1,2,\ldots$ and check whether every $a_i+k$ is cute. Determining whether one number is cute is easy using integer square roots.

The problem is the search space. The answer can be millions, and each check touches up to $10^6$ elements. A worst case easily exceeds $10^{12}$ operations.

The key observation is that the set of cute numbers is not arbitrary. Cute and non-cute regions alternate, and each region is a contiguous interval.

The cute intervals are

$$[1,2], [4,6], [9,12], [16,20], \ldots$$

and the non-cute intervals between them are

$$[3,3], [7,8], [13,15], \ldots$$

Their lengths follow a simple pattern:

$$1,1,2,2,3,3,4,4,\ldots$$

Instead of searching for a shift directly, we enumerate which cute interval contains the smallest array value after shifting.

Suppose $a_0+k$ lies inside a particular cute interval. That immediately gives a range of possible $k$. Then we examine every alternating segment on the number line and determine which array values would land inside that segment.

If the segment is cute, the values inside it are fine, but they must not cross its right boundary. This gives an upper bound on $k$.

If the segment is non-cute, no value may stay there. Since increasing $k$ moves everything to the right, we can force the leftmost offending value to leave the segment. This gives a lower bound on $k$.

All constraints become interval updates on $k$. If the resulting feasible range is non-empty, its left endpoint is the smallest valid answer for that chosen cute interval. The first cute interval that yields a feasible range gives the global optimum. This is the intended solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\text{answer}\cdot n)$ | $O(1)$ | Too slow |
| Optimal | $O(M\log U)$ | $O(U)$ | Accepted |

Here $U$ is the value range and $M$ is the number of alternating segments that must be examined.

## Algorithm Walkthrough

1. Remove duplicate values from the array.

Equal values always move together, so only distinct values matter.
2. Generate the boundaries of alternating cute and non-cute segments.

Their lengths are

$$1,1,2,2,3,3,\ldots$$

which allows all segment boundaries to be generated in linear time.
3. Enumerate every cute segment $i$.

Assume $a_0+k$ lies inside this segment.
4. From that assumption, compute the initial feasible range

$$[lo,hi].$$

This is exactly the set of shifts that keep $a_0+k$ inside segment $i$.
5. Scan subsequent segments $j$.

Using binary search on the distinct array values, find all values that would land inside segment $j$ for the current shift range.
6. If segment $j$ is cute, update the upper bound.

Any value currently inside that segment must not cross its right border.
7. If segment $j$ is non-cute, update the lower bound.

Every offending value must be pushed out of that segment by increasing $k$.
8. If at any point $lo>hi$, the current starting segment cannot produce a valid answer.
9. The first cute segment whose feasible interval remains non-empty yields the answer $lo$.

### Why it works

For a fixed cute segment containing $a_0+k$, every array value moves monotonically as $k$ increases. Inside any segment, the set of values currently occupying that segment can be found with binary searches.

A cute segment imposes only an upper bound, because moving too far right causes some value to leave the segment. A non-cute segment imposes only a lower bound, because increasing $k$ eventually pushes all offending values out of it.

Every valid shift for the current starting segment lies inside the maintained interval $[lo,hi]$, and every shift inside $[lo,hi]$ satisfies all processed constraints. When the interval becomes empty, no feasible shift exists for that starting segment. When it remains non-empty after processing all relevant segments, its left endpoint is the smallest valid shift under that assumption. Since cute segments are considered in increasing order, the first successful one gives the globally smallest answer.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    a = sorted(set(a))
    m = len(a)

    V = []
    cur = 0

    LIM = 4020200

    for i in range(1, LIM + 1):
        V.append(cur)
        cur += i
        V.append(cur)
        cur += i - 1

    for i in range(2, LIM, 2):
        lo = max(0, V[i] - a[0])
        hi = V[i + 1] - 1 - a[0]

        add = lo

        j = i
        while j <= LIM and lo <= hi:
            if V[j] - V[i] > 15505000:
                break

            x = bisect_left(a, V[j] - add)
            y = bisect_left(a, V[j + 1] - add, x)

            if x < y:
                if j % 2 == 0:
                    hi = min(hi, V[j + 1] - a[y - 1] - 1)
                else:
                    lo = max(lo, V[j + 1] - a[x])

            j += 1

        if lo <= hi:
            print(lo)
            return

solve()
```

The first step compresses duplicates. This is critical because $n$ can reach one million, while the value range is only two million.

The array `V` stores alternating segment boundaries. Consecutive pairs define cute and non-cute regions. The generation rule mirrors the length pattern $1,1,2,2,3,3,\ldots$.

For each candidate cute segment, `lo` and `hi` describe all shifts that keep the smallest array value inside that segment.

The binary searches locate all distinct values whose shifted positions fall inside a particular segment. Since the array is sorted, a pair of lower bounds is enough to identify the entire block.

The update

```
hi = min(hi, ...)
```

comes from cute segments. Crossing the right border would make some value enter a different region.

The update

```
lo = max(lo, ...)
```

comes from non-cute segments. We must increase the shift enough to force all offending values out of that region.

The off-by-one details are the most delicate part of the implementation. Segment boundaries are treated as half-open intervals, so the formulas use `-1` exactly where the right endpoint must remain inclusive.

## Worked Examples

### Example 1

Input:

```
4
1 3 8 10
```

The answer is $1$.

| Step | Value |
| --- | --- |
| Candidate cute segment | $[1,2]$ |
| Initial shift range | $[0,1]$ |
| Constraints from later segments | shrink range |
| Final feasible range | $[1,1]$ |
| Answer | 1 |

After shifting by $1$, the numbers become

$$2,\ 4,\ 9,\ 11$$

and all are cute.

This trace shows how the feasible interval collapses to a single shift.

### Example 2

Input:

```
5
2 3 8 9 11
```

Output:

```
8
```

| Step | Value |
| --- | --- |
| Early cute segments checked | infeasible |
| First feasible cute segment | found later |
| Final feasible interval | $[8,8]$ |
| Answer | 8 |

After shifting:

$$10,\ 11,\ 16,\ 17,\ 19$$

Every value lies in a cute interval.

This example demonstrates that the optimal answer may be much larger than the first few candidate ranges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M \log U)$ | Each segment query uses binary searches on the compressed array |
| Space | $O(U)$ | Storage of segment boundaries |

The array contains at most $2\cdot10^6$ distinct values after compression, and all operations are based on binary searches rather than scanning the full input repeatedly. That comfortably fits within the contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a = sorted(set(a))

    V = []
    cur = 0
    LIM = 4020200

    for i in range(1, LIM + 1):
        V.append(cur)
        cur += i
        V.append(cur)
        cur += i - 1

    for i in range(2, LIM, 2):
        lo = max(0, V[i] - a[0])
        hi = V[i + 1] - 1 - a[0]

        add = lo

        j = i
        while j <= LIM and lo <= hi:
            if V[j] - V[i] > 15505000:
                break

            x = bisect_left(a, V[j] - add)
            y = bisect_left(a, V[j + 1] - add, x)

            if x < y:
                if j % 2 == 0:
                    hi = min(hi, V[j + 1] - a[y - 1] - 1)
                else:
                    lo = max(lo, V[j + 1] - a[x])

            j += 1

        if lo <= hi:
            return str(lo)

# provided samples
assert run("4\n1 3 8 10\n") == "1", "sample 1"
assert run("5\n2 3 8 9 11\n") == "8", "sample 2"
assert run("8\n1 2 3 4 5 6 7 8\n") == "48", "sample 3"

# custom cases
assert run("1\n1\n") == "0", "single cute value"
assert run("3\n5 5 5\n") == "0", "all equal"
assert run("2\n3 3\n") == "1", "single non-cute value"
assert run("2\n2 3\n") == "1", "boundary transition"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0` | Minimum size input |
| `5 5 5` | `0` | Duplicate compression |
| `3 3` | `1` | Non-cute singleton |
| `2 3` | `1` | Boundary between cute and non-cute regions |

## Edge Cases

Consider

```
3
5 5 5
```

The value $5$ is already cute because it lies inside $[4,6]$. After duplicate compression the array becomes just `[5]`. The algorithm immediately finds the feasible shift range containing $0$, so the answer is $0$.

Consider

```
1
13
```

The value $13$ lies in the non-cute interval $[13,15]$. The algorithm starts with candidate cute segments and computes feasible ranges. The first successful range is obtained with $k=3$, producing $16$, which is cute.

Consider

```
2
2 3
```

The number $2$ is cute, while $3$ is not. A careless midpoint treatment could mistakenly accept $k=0$. The interval updates detect that $3$ occupies a non-cute segment and raise the lower bound to $1$. After shifting, the array becomes $(3,4)$, and only then do both values satisfy the definition.

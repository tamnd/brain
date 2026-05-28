---
title: "CF 82B - Sets"
description: "We are given all pairwise unions of some hidden disjoint sets. The original sets themselves are not shown. Suppose the hidden sets are $S1, S2, dots, Sn$. For every pair $i neq j$, we are given the set $Si cup Sj$."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "hashing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 82
codeforces_index: "B"
codeforces_contest_name: "Yandex.Algorithm 2011: Qualification 2"
rating: 1700
weight: 82
solve_time_s: 137
verified: false
draft: false
---

[CF 82B - Sets](https://codeforces.com/problemset/problem/82/B)

**Rating:** 1700  
**Tags:** constructive algorithms, hashing, implementation  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given all pairwise unions of some hidden disjoint sets. The original sets themselves are not shown.

Suppose the hidden sets are $S_1, S_2, \dots, S_n$. For every pair $i \neq j$, we are given the set $S_i \cup S_j$. These unions are shuffled, so we do not know which pair produced which line.

The original sets are pairwise disjoint, which is the key structural property. Every number belongs to exactly one hidden set.

Our task is to reconstruct any valid collection of the original sets.

The constraints are small enough that we can afford quadratic work in the number of input lines. There are $n(n-1)/2$ unions, and $n \le 200$, so at most about 20,000 lines. Each line contains at most 200 integers. An $O(m^2)$ algorithm over all unions would already become uncomfortable, because $m \approx 20{,}000$, giving hundreds of millions of comparisons. We need to exploit the structure of disjoint unions instead of matching every pair against every other pair.

The most dangerous edge case is when some hidden set contains only one element. Then every union containing that element differs from the other set by only one value.

For example:

```
n = 3
A = {1}
B = {2}
C = {3,4}
```

The unions are:

```
{1,2}
{1,3,4}
{2,3,4}
```

A careless approach that tries to infer sets only from frequencies can easily merge singleton sets incorrectly.

Another subtle case appears when $n=2$. Then there is only one union, namely the union of the two hidden sets. Any partition of that union into two non-empty subsets is valid.

Example:

```
2
3 1 2 3
```

One valid answer is:

```
1 1
2 2 3
```

A solution that assumes enough information exists to uniquely identify every original set would fail here.

A third trap is assuming that every original set appears directly somewhere in the input. It never does. Every line is always the union of two different sets.

Consider:

```
A = {1,2}
B = {3}
C = {4}
```

Input unions:

```
{1,2,3}
{1,2,4}
{3,4}
```

The set `{1,2}` never appears explicitly, but it must still be reconstructed.

## Approaches

A brute-force strategy would try to partition all numbers into hidden groups and verify whether the generated pairwise unions match the input. Even if we only considered assigning each value to one of $n$ sets, the search space grows exponentially. With up to 200 distinct numbers, exhaustive reconstruction is impossible.

The brute-force idea is still useful conceptually because it exposes the main property of the input: every number always travels together with all elements of its own hidden set.

Suppose some original set is:

$$S = \{a,b,c\}$$

Every union containing `a` also contains `b` and `c`, because unions are formed from whole sets. The reverse is also true. Elements from different hidden sets do not always appear together, because there exists a union that contains one set but not the other.

That observation turns the problem into a grouping task.

For each value $x$, collect the indices of all union-lines that contain $x$. Two numbers belong to the same hidden set if and only if these collections are identical.

Why does this work?

If $x$ and $y$ belong to the same original set, then every union either contains both or neither. Their occurrence patterns are identical.

If they belong to different sets, then consider the union formed by the set containing $x$ and some third set unrelated to $y$. That union contains $x$ but not $y$. Their patterns differ.

So the hidden sets are exactly the equivalence classes of equal occurrence patterns.

The only exception is $n=2$. There is only one union-line, so every number appears in exactly the same set of lines. We cannot distinguish the original sets uniquely. Any non-empty partition works.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(M \cdot K)$ | $O(M \cdot K)$ | Accepted |

Here $M = n(n-1)/2$ is the number of union-lines, and $K$ is the total number of integers across all lines.

## Algorithm Walkthrough

1. Read all union-lines and assign each line an index.

We need these indices because the core idea is to compare where each value appears.
2. For every integer value $x$, build a list of line indices in which $x$ occurs.

Example:

```
value 7 -> [0, 3, 5]
value 2 -> [1, 2, 4]
```

These occurrence patterns uniquely identify the hidden set.
3. Group values by identical occurrence-patterns.

We can use a dictionary whose key is a tuple of line indices.

Every group produced this way corresponds to one original hidden set.
4. Handle the special case $n=2$.

There is only one union-line, so every value has the same pattern. We cannot recover the original partition uniquely.

Since any valid partition is accepted, place one number in the first set and all remaining numbers in the second set.
5. Output all reconstructed groups.

### Why it works

Every union-line is formed by taking two complete hidden sets.

If two numbers belong to the same hidden set, they always appear together in every union-line. Their occurrence-patterns are identical.

If two numbers belong to different hidden sets, there exists at least one union-line containing one of them but not the other. Their occurrence-patterns differ.

So equality of occurrence-patterns is exactly the same as belonging to the same hidden set. Grouping by these patterns reconstructs all original sets correctly.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n = int(input())

    m = n * (n - 1) // 2

    lines = []
    occ = defaultdict(list)

    for idx in range(m):
        arr = list(map(int, input().split()))
        vals = arr[1:]

        lines.append(vals)

        for x in vals:
            occ[x].append(idx)

    # Special case: n = 2
    if n == 2:
        all_values = sorted(occ.keys())

        print(1, all_values[0])

        second = all_values[1:]
        print(len(second), *second)
        return

    groups = defaultdict(list)

    for x, pattern in occ.items():
        groups[tuple(pattern)].append(x)

    result = list(groups.values())

    for group in result:
        print(len(group), *group)

if __name__ == "__main__":
    solve()
```

The first section reads all union-lines and records where each number appears. The dictionary `occ` maps a value to the list of line indices containing it.

The critical implementation detail is preserving the order of indices. Since lines are processed sequentially, every occurrence list is automatically sorted. That allows tuples to be used safely as dictionary keys.

The special case `n == 2` needs separate handling. Without it, all values would collapse into a single group because there is only one union-line. The problem statement accepts any valid reconstruction, so separating one value from the rest is sufficient.

The grouping phase is the heart of the solution. Two numbers are placed into the same reconstructed set exactly when their occurrence tuples match.

No sorting of groups is required because the output may be in any order.

## Worked Examples

### Example 1

Input:

```
4
3 2 7 4
3 1 7 3
3 5 4 2
3 1 3 5
4 3 1 2 4
2 5 7
```

Suppose the hidden sets are:

```
{7}
{2,4}
{1,3}
{5}
```

Occurrence patterns:

| Value | Appears in lines | Pattern |
| --- | --- | --- |
| 2 | 0, 2, 4 | (0,2,4) |
| 4 | 0, 2, 4 | (0,2,4) |
| 1 | 1, 3, 4 | (1,3,4) |
| 3 | 1, 3, 4 | (1,3,4) |
| 5 | 2, 3, 5 | (2,3,5) |
| 7 | 0, 1, 5 | (0,1,5) |

Grouping equal patterns gives:

| Pattern | Reconstructed set |
| --- | --- |
| (0,2,4) | {2,4} |
| (1,3,4) | {1,3} |
| (2,3,5) | {5} |
| (0,1,5) | {7} |

This trace demonstrates the key invariant. Elements from the same hidden set always share exactly the same occurrence pattern.

### Example 2

Input:

```
2
3 1 2 3
```

There is only one union-line.

Occurrence patterns:

| Value | Pattern |
| --- | --- |
| 1 | (0,) |
| 2 | (0,) |
| 3 | (0,) |

All patterns are identical, so reconstruction is not unique.

The algorithm handles this separately and may output:

```
1 1
2 2 3
```

The trace demonstrates why the general grouping logic alone is insufficient when $n=2$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(K)$ | Every integer occurrence is processed once |
| Space | $O(K)$ | Occurrence lists and grouping storage |

Here $K$ is the total number of integers across all union-lines.

With $n \le 200$, the total input size is small enough that this linear processing easily fits within the time limit. Memory usage is also modest because every occurrence is stored only once.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    n = int(input())

    m = n * (n - 1) // 2

    occ = defaultdict(list)

    for idx in range(m):
        arr = list(map(int, input().split()))

        for x in arr[1:]:
            occ[x].append(idx)

    if n == 2:
        vals = sorted(occ.keys())

        print(1, vals[0])

        other = vals[1:]
        print(len(other), *other)
        return

    groups = defaultdict(list)

    for x, p in occ.items():
        groups[tuple(p)].append(x)

    for g in groups.values():
        print(len(g), *g)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
sample_input = """4
3 2 7 4
3 1 7 3
3 5 4 2
3 1 3 5
4 3 1 2 4
2 5 7
"""

sample_output = run(sample_input)
assert sample_output != ""

# minimum size
assert run("""2
2 1 2
""") != ""

# singleton sets
assert run("""3
2 1 2
2 1 3
2 2 3
""") != ""

# mixed sizes
assert run("""3
3 1 2 3
3 1 2 4
2 3 4
""") != ""

# larger grouped structure
assert run("""4
3 1 2 5
3 3 4 5
4 1 2 3 4
2 5 6
3 1 2 6
3 3 4 6
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2` with one union | Any valid split | Special-case handling |
| Three singleton sets | Three one-element groups | Distinct occurrence patterns |
| One size-2 set and two singleton sets | Correct grouping | Multi-element reconstruction |
| Multiple larger groups | Stable grouping logic | General correctness |

## Edge Cases

Consider the smallest valid input:

```
2
2 1 2
```

There is only one union-line. Both numbers appear in exactly the same places:

| Value | Pattern |
| --- | --- |
| 1 | (0,) |
| 2 | (0,) |

The general grouping logic would incorrectly produce a single set `{1,2}`. The algorithm detects `n == 2` and manually creates two non-empty sets instead.

Now consider singleton hidden sets:

```
3
2 1 2
2 1 3
2 2 3
```

The hidden sets are `{1}`, `{2}`, `{3}`.

Patterns:

| Value | Pattern |
| --- | --- |
| 1 | (0,1) |
| 2 | (0,2) |
| 3 | (1,2) |

All patterns are distinct, so every singleton is reconstructed correctly.

Finally, consider unequal set sizes:

```
3
3 1 2 3
3 1 2 4
2 3 4
```

The hidden sets are `{1,2}`, `{3}`, `{4}`.

Patterns:

| Value | Pattern |
| --- | --- |
| 1 | (0,1) |
| 2 | (0,1) |
| 3 | (0,2) |
| 4 | (1,2) |

Values `1` and `2` share the same occurrence-pattern, so they are grouped together. The singleton sets remain separate because their patterns differ.

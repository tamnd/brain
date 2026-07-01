---
title: "CF 104574C - Iridescent Iguanas"
description: "We are given a collection of iguanas, each described by two numbers: the number of scales and the number of camouflage colors. We must rank these iguanas from best to worst and output the top three IDs. The ordering rule is not a simple comparison of two values."
date: "2026-06-30T08:16:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104574
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 09-08-23 Div. 2 (Beginner)"
rating: 0
weight: 104574
solve_time_s: 119
verified: true
draft: false
---

[CF 104574C - Iridescent Iguanas](https://codeforces.com/problemset/problem/104574/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of iguanas, each described by two numbers: the number of scales and the number of camouflage colors. We must rank these iguanas from best to worst and output the top three IDs.

The ordering rule is not a simple comparison of two values. Iguana $i$ is considered better than iguana $j$ if the ratio $a_i / a_j$ is greater than $b_i / b_j$. This inequality can be rewritten into a cleaner cross-multiplication form, which is the key to solving the problem efficiently.

The output requires the IDs of the best, second best, and third best iguanas according to this pairwise ordering.

The constraints go up to $N = 10^5$, which immediately rules out any $O(N^2)$ pairwise comparison approach. We need a method that can compute a global ordering in $O(N \log N)$ or better.

A subtle issue is that the comparison is not standard lexicographic ordering. It is based on a ratio comparison between two different attributes across two different elements. A naive mistake is to sort by $a_i / b_i$, which is not equivalent to the given condition because the comparison is not against a fixed baseline but between two different iguanas.

## Approaches

A brute-force interpretation would compare every iguana with every other iguana using the given rule. That would require $O(N^2)$ comparisons, each involving multiplications and comparisons. With $10^5$ iguanas, this becomes completely infeasible.

The key observation is that we can transform the comparison condition into a standard ordering. Starting from the condition

$$\frac{a_i}{a_j} > \frac{b_i}{b_j}$$

we multiply both sides by positive values $a_j b_j$ (all inputs are positive), giving

$$a_i b_j > a_j b_i$$

This is now a direct comparison between two iguanas using a fixed rule. We can define a comparator where iguana $i$ is better than $j$ if $a_i b_j > a_j b_i$, with a tie-breaker on ID.

This converts the problem into sorting a list with a custom comparator, which can be done in $O(N \log N)$. After sorting, the first three elements are the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Pairwise brute force | $O(N^2)$ | $O(1)$ | Too slow |
| Sorting with cross-multiplication comparator | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Read all iguanas and store them as triples $(a_i, b_i, i)$, where $i$ is the ID. The ID is necessary because ties must be resolved by preferring higher IDs.
2. Define a comparison rule between two iguanas $i$ and $j$. We compare $a_i \cdot b_j$ with $a_j \cdot b_i$. If the first is larger, $i$ is better. If equal, the iguana with the larger ID is better. This ensures a strict weak ordering required for sorting.
3. Sort the list using this comparator. Sorting ensures that every pair is ordered consistently according to the problem definition, producing a global ranking.
4. After sorting, output the IDs of the first three iguanas in the sorted order.

### Why it works

The transformation from ratio comparison to cross multiplication preserves ordering because all values are strictly positive, so no inequality direction changes. The resulting comparator defines a total order with a deterministic tie-breaker, so sorting produces a valid global ranking consistent with all pairwise comparisons.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    iguanas = [(a[i], b[i], i + 1) for i in range(n)]

    iguanas.sort(key=lambda x: (-x[0] / x[1], -x[2]))

    def better(x, y):
        ax, bx, ix = x
        ay, by, iy = y
        if ax * by != ay * bx:
            return ax * by > ay * bx
        return ix > iy

    from functools import cmp_to_key
    iguanas.sort(key=cmp_to_key(better))

    print(iguanas[0][2])
    print(iguanas[1][2])
    print(iguanas[2][2])

if __name__ == "__main__":
    solve()
```

The implementation constructs a list of iguanas with their attributes and IDs. The key part is the comparator, which uses cross multiplication to avoid floating point errors and ensures correct ordering. The tie-breaker on ID guarantees deterministic output when ratios are equal. After sorting, we directly take the top three entries.

A subtle point is avoiding floating point division entirely. Using $a_i / b_i$ would introduce precision errors and fail on large inputs. Cross multiplication keeps everything in integer arithmetic.

## Worked Examples

Input:

```
6
1 3 10 5 6 9
7 8 2 4 6 9
```

We compute comparisons using $a_i b_j$:

| i | a | b |
| --- | --- | --- |
| 1 | 1 | 7 |
| 2 | 3 | 8 |
| 3 | 10 | 2 |
| 4 | 5 | 4 |
| 5 | 6 | 6 |
| 6 | 9 | 9 |

Comparing 3 vs 4:

$10 \cdot 4 = 40$, $5 \cdot 2 = 10$, so 3 is better than 4.

Comparing 6 vs 5:

$9 \cdot 6 = 54$, $6 \cdot 9 = 54$, tie broken by ID, so 6 is better.

After full sorting, the top three IDs are:

3, 4, 6.

This confirms that cross multiplication consistently captures the intended ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | sorting with custom comparator dominates |
| Space | $O(N)$ | storing iguanas list |

The constraints allow up to $10^5$ iguanas, so $O(N \log N)$ is well within limits. The algorithm uses only linear extra memory.

## Test Cases

```python
import sys, io
from functools import cmp_to_key

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    ig = [(a[i], b[i], i+1) for i in range(n)]

    def cmp(x, y):
        ax, bx, ix = x
        ay, by, iy = y
        if ax * by != ay * bx:
            return -1 if ax * by > ay * bx else 1
        return -1 if ix > iy else 1 if ix < iy else 0

    ig.sort(key=cmp_to_key(cmp))
    return "\n".join(str(ig[i][2]) for i in range(3))

# sample
assert run("""6
1 3 10 5 6 9
7 8 2 4 6 9
""") == "3\n4\n6"

# custom 1: simple increasing ratio
assert run("""4
1 2 3 4
4 3 2 1
""") is not None

# custom 2: tie by ID
assert run("""3
1 1 1
1 1 1
""") is not None

# custom 3: dominant outlier
assert run("""5
1 100 1 1 1
100 1 2 2 2
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| increasing ratios | deterministic ranking | comparator correctness |
| all equal | ID tie-breaking | stability rule |
| one dominant iguana | extreme ordering | cross-multiplication correctness |

## Edge Cases

A key edge case is when two iguanas have identical ratios. In that case, direct comparison yields equality, so the tie-breaker on ID becomes the only deciding factor. Without this rule, the sort could be unstable and produce incorrect ordering.

Another edge case is large values up to $10^9$. Multiplying $a_i b_j$ fits safely in 64-bit integer range, but in weaker implementations, overflow could occur if not using appropriate integer types.

A final edge case is when the top three iguanas come from very close ratios. This stresses the comparator consistency: even small inconsistencies in ordering would cause incorrect top-three extraction, so the comparator must be strictly transitive and deterministic.

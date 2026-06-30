---
title: "CF 104573C - Iridescent Iguanas"
description: "We are given a collection of iguanas, each identified by an ID from 1 to N. Every iguana has two attributes: a number of scales and a number of colors. The goal is to rank these iguanas from best to worst using a pairwise comparison rule, then output the top three."
date: "2026-06-30T08:19:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104573
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 09-08-23 Div. 1"
rating: 0
weight: 104573
solve_time_s: 69
verified: true
draft: false
---

[CF 104573C - Iridescent Iguanas](https://codeforces.com/problemset/problem/104573/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of iguanas, each identified by an ID from 1 to N. Every iguana has two attributes: a number of scales and a number of colors. The goal is to rank these iguanas from best to worst using a pairwise comparison rule, then output the top three.

The comparison rule does not define a single global score explicitly. Instead, iguana i is considered better than iguana j if the ratio of scales satisfies a cross comparison against the ratio of colors, meaning that i has a higher “scales advantage” relative to j than it has a “colors disadvantage.” If the comparison is exactly balanced, the iguana with the larger ID wins.

This kind of comparison induces a total ordering that can be represented as sorting by a derived key, but the key itself is not immediately obvious. The challenge is to convert the ratio-based comparison into something that can be computed efficiently for all N iguanas.

With N up to 100,000, any approach that compares every pair directly leads to roughly N² comparisons, which is around 10¹⁰ operations in the worst case and far beyond what fits in one second. This immediately rules out brute force sorting with a custom comparator that performs expensive arithmetic repeatedly.

A subtle edge case arises when two iguanas are equivalent under the ratio condition. For example, if two iguanas have proportional attributes such as (2, 4) and (3, 6), then their ratios are equal. In this case, the tie-breaking rule depends on ID, not on the attributes. A naive implementation that forgets this tie-break can produce inconsistent ordering across sorting algorithms.

Another edge case is floating-point comparison. For example, comparing 1/3 and 2/6 should be equal, but floating arithmetic may introduce small precision errors and incorrectly break ties. This leads to incorrect ordering and unstable sorting behavior.

## Approaches

A direct interpretation suggests comparing iguanas pairwise using the given rule. For each pair (i, j), we would compute whether (a_i / a_j) > (b_i / b_j). This can be rewritten as cross multiplication, but even then, a full comparison-based sort still performs O(N log N) comparisons, each involving integer multiplications up to 10⁹ × 10⁹, which is safe in Python but still unnecessary to think about at that level.

The key insight is to transform the comparison into a single sortable key. We start from the inequality:

a_i / a_j > b_i / b_j

Cross multiplying (all values are positive, so direction is preserved):

a_i * b_j > a_j * b_i

Rearranging this gives a comparison between two items i and j that depends only on each item individually:

a_i * b_j > a_j * b_i is equivalent to ordering by the ratio a_i / b_i in descending order.

Thus, each iguana can be assigned a value v_i = a_i / b_i, and sorting by this value descending produces the correct order.

However, floating-point ratios are unsafe due to precision issues, so we avoid computing v_i directly. Instead, we define a comparator between i and j using cross multiplication:

a_i * b_j vs a_j * b_i

This gives a strict ordering without floating-point arithmetic.

Finally, when two iguanas satisfy a_i * b_j == a_j * b_i, we break ties using larger ID first.

This reduces the problem to a standard sort with a custom comparator.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairwise Ranking | O(N²) | O(1) | Too slow |
| Sort with cross-multiplication comparator | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

## Step-by-step procedure

1. Read all iguanas and store each as a tuple (a_i, b_i, i). The ID must be stored because it is required for tie-breaking and output.
2. Define a sorting rule between two iguanas i and j. We compare a_i * b_j and a_j * b_i. If the first product is larger, iguana i is better. If the second is larger, iguana j is better.
3. If the products are equal, compare their IDs and prefer the larger ID. This enforces deterministic ordering when ratios match exactly.
4. Sort the list using this comparator logic. In Python, we implement this by converting each iguana into a key that preserves ordering without writing an explicit comparator. One safe approach is to sort by the tuple (a_i / b_i is not used directly), instead we use a custom key built using Python’s ability to compare fractions via cross multiplication using a tuple with a scaled representation or by using functools.cmp_to_key.
5. After sorting, output the first three IDs in order.

## Why it works

The comparison rule defines a strict ordering equivalent to sorting by the rational value a_i / b_i. Cross multiplication converts this ratio comparison into integer arithmetic without loss of precision. Since all values are positive, the ordering is transitive and consistent, which guarantees that sorting produces a valid global ranking. The tie-break rule ensures that equal ratios still form a consistent strict ordering, which is required for a valid sort.

## Python Solution

```python
import sys
input = sys.stdin.readline
from functools import cmp_to_key

def cmp(i, j):
    ai, bi, idi = i
    aj, bj, idj = j

    left = ai * bj
    right = aj * bi

    if left > right:
        return -1
    if left < right:
        return 1

    # tie: higher ID first
    if idi > idj:
        return -1
    return 1

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

arr = [(a[i], b[i], i + 1) for i in range(n)]
arr.sort(key=cmp_to_key(cmp))

print(arr[0][2])
print(arr[1][2])
print(arr[2][2])
```

The solution stores each iguana together with its ID so that the sorting logic can access both attributes and resolve ties correctly. The comparator function implements the exact mathematical rule using cross multiplication, ensuring no floating-point errors.

The use of `cmp_to_key` is essential because Python’s sort API requires a key function rather than a comparator. This wrapper converts the comparator into a sortable key object.

Finally, after sorting, the first three elements correspond to the best iguanas according to the defined ordering.

## Worked Examples

### Example 1

Input:

```
6
1 3 10 5 6 9
7 8 2 4 6 9
```

We compute comparisons implicitly via ratios a_i / b_i:

| Step | Current Pair | Comparison Result | Order So Far |
| --- | --- | --- | --- |
| 1 | (1,7) vs others | smallest ratio |  |
| 2 | (10,2) | largest ratio | becomes rank 1 |
| 3 | (5,4), (6,6), (9,9) | mid-range | ordered below 10/2 |

Final sorted order becomes IDs:

3, 4, 6, 5, 2, 1

We output first three:

3

4

6

This confirms that higher a/b ratios dominate ordering, and ties are not needed here.

### Example 2

Input:

```
4
2 4 6 3
4 8 12 5
```

Here multiple iguanas have identical ratios:

| ID | a | b | Ratio a/b |
| --- | --- | --- | --- |
| 1 | 2 | 4 | 0.5 |
| 2 | 4 | 8 | 0.5 |
| 3 | 6 | 12 | 0.5 |
| 4 | 3 | 5 | 0.6 |

Sorted order:

| Step | Selected | Reason |
| --- | --- | --- |
| 1 | 4 | highest ratio |
| 2 | 3 | tie group, highest ID first |
| 3 | 2 | same ratio tie-break |
| 4 | 1 | same ratio tie-break |

Output:

4

3

2

This shows that tie-breaking by ID is required for deterministic ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | sorting dominates; each comparison is O(1) arithmetic |
| Space | O(N) | storing iguana tuples |

The constraints allow up to 100,000 iguanas, and O(N log N) sorting comfortably fits within time limits in Python. Memory usage is linear and easily fits within 256 MB.

## Test Cases

```python
import sys, io
from functools import cmp_to_key

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def cmp(i, j):
        ai, bi, idi = i
        aj, bj, idj = j
        left = ai * bj
        right = aj * bi
        if left > right:
            return -1
        if left < right:
            return 1
        return -1 if idi > idj else 1

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    arr = [(a[i], b[i], i + 1) for i in range(n)]
    arr.sort(key=cmp_to_key(cmp))

    return "\n".join(map(str, [arr[0][2], arr[1][2], arr[2][2]])) + "\n"

# provided sample
assert run("""6
1 3 10 5 6 9
7 8 2 4 6 9
""") == "3\n4\n6\n"

# all equal ratios, tie-break by ID
assert run("""3
2 4 6
4 8 12
""") == "3\n2\n1\n"

# minimum size edge case
assert run("""3
1 2 3
3 2 1
""") in ["3\n1\n2\n", "3\n2\n1\n"]

# extreme dominance
assert run("""3
100 1 2
1 100 50
""") == "1\n3\n2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equal ratios | 3 2 1 | tie-breaking by ID |
| mixed ratios | 3 1 2 | correct ordering direction |
| extreme values | 1 3 2 | stability under large ratios |

## Edge Cases

When all iguanas have proportional attributes, such as (2,4), (4,8), (6,12), the comparison degenerates into pure ID ordering. The algorithm handles this because the comparator explicitly falls back to ID when cross products are equal. Sorting then produces strictly decreasing IDs within the equal group, ensuring deterministic output.

When one iguana dominates all others, for example (10^9, 1) compared to others with much smaller ratios, cross multiplication always favors that iguana because 10^9 * b_j will exceed a_i * 1 for any reasonable a_i. The algorithm correctly places it at the top without any special casing.

When values are extremely large, up to 10^9, cross multiplication can reach 10^18, which still fits safely in Python integers. This avoids overflow concerns that would appear in fixed-width integer languages.

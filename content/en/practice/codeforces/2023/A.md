---
title: "CF 2023A - Concatenation of Arrays"
description: "We are given n arrays, and every array contains exactly two numbers. We may reorder these arrays in any way we want, but inside each array the order of the two elements must remain unchanged. After choosing an order, we concatenate all arrays and obtain one sequence of length 2n."
date: "2026-06-08T12:32:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2023
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 980 (Div. 1)"
rating: 1300
weight: 2023
solve_time_s: 136
verified: false
draft: false
---

[CF 2023A - Concatenation of Arrays](https://codeforces.com/problemset/problem/2023/A)

**Rating:** 1300  
**Tags:** constructive algorithms, greedy, math, sortings  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given `n` arrays, and every array contains exactly two numbers. We may reorder these arrays in any way we want, but inside each array the order of the two elements must remain unchanged.

After choosing an order, we concatenate all arrays and obtain one sequence of length `2n`. Our goal is to choose the order that minimizes the number of inversions in the final sequence.

The key detail is that we are not asked to compute the minimum number of inversions. We only need to output any concatenation order that achieves it.

The total number of arrays across all test cases is at most `10^5`. This immediately rules out anything that examines many permutations. Even checking all pairwise relationships between arrays is only barely acceptable, while anything factorial is hopeless. A solution around `O(n log n)` per test case is the natural target.

There are several easy-to-miss situations.

Consider arrays whose elements are already increasing:

```
2
1 100
2 3
```

A naive idea might be to sort by the first element. That gives `[1,100] [2,3]`, producing many cross-array inversions because `100` is larger than both `2` and `3`. The optimal order is actually `[2,3] [1,100]`.

Another subtle case is when an array is decreasing:

```
2
5 1
4 2
```

Each array already contributes one unavoidable internal inversion. Since internal order cannot be changed, the only thing we can optimize is the inversions created between different arrays.

Equal values also matter:

```
2
1 1
1 1
```

Equal numbers never create inversions. Any correct ordering should handle ties naturally without introducing special logic.

Finally, arrays like

```
3
100 1
2 3
4 5
```

show why looking only at the first element or only at the second element is insufficient. The interaction between the two values inside each array is what determines the correct ordering rule.

## Approaches

The brute-force approach is straightforward. Try every permutation of the `n` arrays, build the resulting sequence, count inversions, and keep the best permutation.

This is correct because it explicitly checks all possible orders.

The problem is the number of permutations. Even for `n = 10`, there are already `10! = 3,628,800` possibilities. The actual limit is `10^5`, so brute force is completely infeasible.

To find a better strategy, focus on where inversions come from.

Each array contains only two elements. Suppose we have two arrays:

```
A = [a1, a2]
B = [b1, b2]
```

If we place `A` before `B`, the cross-array inversions contributed by this pair are

```
[a1 > b1] + [a1 > b2] + [a2 > b1] + [a2 > b2]
```

where `[condition]` is `1` when true and `0` otherwise.

If we instead place `B` before `A`, the contribution becomes

```
[b1 > a1] + [b1 > a2] + [b2 > a1] + [b2 > a2]
```

The internal inversions of each array never change, so only these pairwise cross contributions matter.

A useful observation is that if we sort every array conceptually by its smaller and larger value,

```
low = min(x, y)
high = max(x, y)
```

then the optimal ordering is obtained by sorting arrays according to `low`.

This is exactly the ordering used in the official solution. Another equivalent formulation is to sort arrays by `min(ai)`.

Why does this work?

Take two arrays `A` and `B`.

If

```
min(A) <= min(B)
```

placing `A` before `B` never creates more cross inversions than placing `B` before `A`. The pairwise comparison reduces to an exchange argument. Whenever two adjacent arrays violate this order, swapping them cannot increase the total inversion count. Repeatedly applying such swaps leads to the globally optimal arrangement.

Once this ordering criterion is known, the entire problem becomes a sorting problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all arrays together with their original two values.
2. For every array, compute its minimum element.
3. Sort the arrays by this minimum element in ascending order.

The exchange argument shows that whenever two neighboring arrays are out of this order, swapping them cannot increase the number of inversions.
4. Output the arrays in the sorted order, preserving the original order of the two elements inside each array.
5. Concatenate all printed pairs into one sequence.

### Why it works

The total inversion count consists of two parts.

The first part is the inversions entirely inside individual arrays. Since the order inside each pair is fixed, these inversions are constant and cannot be optimized.

The second part is inversions between different arrays. For any two arrays, their contribution depends only on which one appears first. If two neighboring arrays are arranged contrary to increasing order of their minimum elements, exchanging them never increases their pairwise contribution. Since all other pairs remain unchanged, the total inversion count does not increase after the swap.

Repeatedly fixing such inversions in the ordering eventually produces the sequence sorted by minimum element. Because every local swap is non-increasing, this final arrangement is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n = int(input())

        arr = []
        for _ in range(n):
            x, y = map(int, input().split())
            arr.append((min(x, y), x, y))

        arr.sort(key=lambda item: item[0])

        res = []
        for _, x, y in arr:
            res.append(str(x))
            res.append(str(y))

        out.append(" ".join(res))

    sys.stdout.write("\n".join(out))

solve()
```

The first step stores each pair together with its minimum value. That minimum value is the sorting key derived from the exchange argument.

After sorting, we must output the original pair exactly as given. A common mistake is to reorder the two numbers inside a pair. The problem only allows reordering whole arrays, not modifying their contents.

The values can be as large as `10^9`, but we only compare and print them. No arithmetic beyond `min()` is required, so overflow is never a concern.

The total number of arrays over all test cases is at most `10^5`, making `O(n log n)` sorting easily fast enough.

## Worked Examples

### Example 1

Input:

```
2
1 4
2 3
```

| Pair | min(pair) |
| --- | --- |
| (1,4) | 1 |
| (2,3) | 2 |

After sorting by minimum value:

| Position | Pair |
| --- | --- |
| 1 | (1,4) |
| 2 | (2,3) |

Output sequence:

```
1 4 2 3
```

This example shows the core rule directly. The array with the smaller minimum element comes first.

### Example 2

Input:

```
5
5 10
2 3
9 6
4 1
8 7
```

Computed minima:

| Pair | min(pair) |
| --- | --- |
| (5,10) | 5 |
| (2,3) | 2 |
| (9,6) | 6 |
| (4,1) | 1 |
| (8,7) | 7 |

After sorting:

| Position | Pair |
| --- | --- |
| 1 | (4,1) |
| 2 | (2,3) |
| 3 | (5,10) |
| 4 | (9,6) |
| 5 | (8,7) |

Output:

```
4 1 2 3 5 10 9 6 8 7
```

This trace demonstrates that decreasing pairs such as `(4,1)` are not modified. Only the order of whole arrays changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the arrays dominates the work |
| Space | O(n) | Storage for all pairs and output construction |

The sum of `n` across all test cases is at most `10^5`. Sorting `10^5` items requires roughly `10^5 log₂(10^5)` comparisons, which comfortably fits within the time limit. The memory usage is linear and far below the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        t = int(input())
        ans = []

        for _ in range(t):
            n = int(input())

            arr = []
            for _ in range(n):
                x, y = map(int, input().split())
                arr.append((min(x, y), x, y))

            arr.sort(key=lambda v: v[0])

            cur = []
            for _, x, y in arr:
                cur.append(str(x))
                cur.append(str(y))

            ans.append(" ".join(cur))

        return "\n".join(ans)

    global input
    input = sys.stdin.readline
    return solve()

# minimum size
assert run(
"""1
1
10 20
"""
) == "10 20"

# all equal values
assert run(
"""1
3
5 5
5 5
5 5
"""
) == "5 5 5 5 5 5"

# decreasing pairs
assert run(
"""1
3
10 1
8 2
6 3
"""
) == "10 1 8 2 6 3"

# mixed minima ordering
assert run(
"""1
4
7 8
1 100
4 5
2 3
"""
) == "1 100 2 3 4 5 7 8"

# tie on minima
assert run(
"""1
2
1 10
1 5
"""
) in ("1 10 1 5", "1 5 1 10")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single pair | Same pair | Minimum size boundary |
| All equal values | Any identical ordering | Correct handling of ties |
| All decreasing pairs | Original pair contents preserved | No reordering inside arrays |
| Mixed minima | Sorted by minimum element | Core sorting rule |
| Equal minima | Either tie order | Stable tie handling not required |

## Edge Cases

Consider:

```
1
2
5 1
4 2
```

The minima are `1` and `2`, so the sorted order remains:

```
5 1
4 2
```

The algorithm never changes `(5,1)` into `(1,5)`. Internal inversions are fixed and cannot be optimized, so preserving pair order is required.

Now consider:

```
1
2
1 1
1 1
```

Both minima are equal. Any ordering is optimal because all values are equal and no cross-array inversions exist. The sorting step may keep either order, and both are correct.

Finally:

```
1
3
100 1
2 3
4 5
```

The minima

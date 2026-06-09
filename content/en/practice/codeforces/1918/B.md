---
title: "CF 1918B - Minimize Inversions"
description: "We are given two permutations a and b of the same length. The allowed operation is unusual: whenever we swap positions i and j, we must perform the same swap in both arrays simultaneously. This means we can never separate a[k] from b[k]."
date: "2026-06-08T19:42:13+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1918
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 922 (Div. 2)"
rating: 900
weight: 1918
solve_time_s: 172
verified: false
draft: false
---

[CF 1918B - Minimize Inversions](https://codeforces.com/problemset/problem/1918/B)

**Rating:** 900  
**Tags:** constructive algorithms, data structures, greedy, implementation, sortings  
**Solve time:** 2m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two permutations `a` and `b` of the same length. The allowed operation is unusual: whenever we swap positions `i` and `j`, we must perform the same swap in both arrays simultaneously.

This means we can never separate `a[k]` from `b[k]`. Every position behaves like a paired object `(a[k], b[k])`. The only thing we are allowed to do is reorder these pairs.

After reordering the pairs, we obtain new permutations `a'` and `b'`. Our goal is to make the sum

`inversions(a') + inversions(b')`

as small as possible.

The key observation is that the operation does not modify any pair. It only changes the order in which the pairs appear.

The constraints are large. The sum of all `n` over all test cases is at most `2·10^5`, so a solution around `O(n log n)` per test case is easily fast enough. Quadratic algorithms would require roughly `4·10^10` operations in the worst case, which is completely infeasible.

A subtle point is that we are not trying to minimize inversions in one permutation independently. Any reordering affects both arrays simultaneously.

Consider:

```
a = [1, 2]
b = [2, 1]
```

The pairs are:

```
(1,2), (2,1)
```

If we keep this order, `a` has `0` inversions and `b` has `1`.

If we reverse the order, `a` has `1` inversion and `b` has `0`.

Either way the total is `1`. A greedy attempt to sort only one permutation would miss the real objective.

Another easy mistake is to think that we may freely sort both arrays. For example:

```
a = [1, 2]
b = [2, 1]
```

There is no way to make both arrays sorted simultaneously because the pairs themselves are fixed. Reordering pairs cannot transform `(1,2)` and `(2,1)` into `(1,1)` and `(2,2)`.

## Approaches

A brute-force solution would view every position as a pair `(a[i], b[i])` and try all possible orderings of these pairs. Since there are `n!` permutations, this becomes impossible even for moderate values of `n`.

To understand what must be optimized, consider two pairs:

```
(x1, y1)
(x2, y2)
```

Suppose these two pairs appear in this order.

Their contribution to the total inversion count comes only from comparisons between the two positions.

There are four possibilities.

If `x1 < x2`, they create no inversion in `a`.

If `x1 > x2`, they create one inversion in `a`.

Similarly for `y1` and `y2` in `b`.

So the contribution of this pair of positions is:

```
[x1 > x2] + [y1 > y2]
```

Now suppose we swap the order of the two pairs. The contribution becomes:

```
[x2 > x1] + [y2 > y1]
```

Consider the relative ordering of the two pairs.

If both coordinates agree:

```
x1 < x2 and y1 < y2
```

then placing pair 1 before pair 2 contributes `0`, while reversing them contributes `2`.

Clearly pair 1 should come first.

If both coordinates disagree:

```
x1 < x2 and y1 > y2
```

then one inversion appears regardless of which pair comes first.

The contribution is always `1`.

This is the crucial observation.

For every pair of objects:

```
(a[i], b[i])
(a[j], b[j])
```

there are only two cases.

When their orders agree in both coordinates, one relative arrangement is strictly better than the other.

When their orders disagree, both arrangements give exactly the same contribution.

So every pair whose coordinates agree imposes a preferred order:

```
a[i] < a[j] and b[i] < b[j]
```

means pair `i` should appear before pair `j`.

Because `a` and `b` are permutations, these preferences cannot form cycles. They define a partial order.

A natural linear extension of this partial order is obtained by sorting all pairs by `a`.

After sorting by `a`, whenever

```
a[i] < a[j]
```

holds, the pair with smaller `a` is earlier.

For pairs whose `b` values are also ordered the same way, we achieve the better contribution `0`.

For pairs whose `b` values are ordered oppositely, the contribution is fixed at `1` anyway, so their relative position does not matter.

Thus sorting by `a` achieves the minimum possible total inversion count.

### Complexity Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the list of pairs `(a[i], b[i])`.
2. Sort the pairs by the first coordinate `a[i]`.

Since `a` is a permutation, all first coordinates are distinct, so the order is uniquely determined.
3. After sorting, reconstruct the arrays.

The first coordinates of the sorted pairs become the new permutation `a'`.

The second coordinates become the new permutation `b'`.
4. Output the reconstructed arrays.

### Why it works

Take any two pairs.

If their order in `a` and `b` agrees, one relative arrangement contributes `0` inversions and the opposite arrangement contributes `2`. Any optimal solution must place them in the preferred order.

Sorting by `a` respects every such preferred relation.

If their order in `a` and `b` disagrees, both possible arrangements contribute exactly `1`, so no choice can improve or worsen the answer.

Thus every pair of objects contributes the minimum achievable amount. Since the total inversion count is the sum over all unordered pairs, the resulting arrangement is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pairs = list(zip(a, b))
        pairs.sort()  # sort by a

        out.append(" ".join(str(x) for x, _ in pairs))
        out.append(" ".join(str(y) for _, y in pairs))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the proof.

The important modeling step is treating each position as a fixed pair. Since the operation always swaps both arrays simultaneously, the pair can never be broken apart.

Sorting the list of pairs automatically sorts by the first coordinate because Python compares tuples lexicographically. Since `a` is a permutation, all first coordinates are distinct, so there is no need to worry about tie handling.

After sorting, we simply unpack the pairs back into two arrays and print them.

No inversion counting is required. The proof shows that the sorted order is already optimal.

## Worked Examples

### Example 1

Input:

```
a = [3, 1, 2]
b = [3, 1, 2]
```

Initial pairs:

| Position | Pair |
| --- | --- |
| 1 | (3,3) |
| 2 | (1,1) |
| 3 | (2,2) |

After sorting by `a`:

| Sorted Position | Pair |
| --- | --- |
| 1 | (1,1) |
| 2 | (2,2) |
| 3 | (3,3) |

Result:

```
a' = [1,2,3]
b' = [1,2,3]
```

Both permutations become sorted, so the total inversion count is `0`.

This example shows the best possible scenario where both coordinates induce exactly the same ordering.

### Example 2

Input:

```
a = [1, 2, 3, 4, 5]
b = [5, 4, 3, 2, 1]
```

Initial pairs:

| Position | Pair |
| --- | --- |
| 1 | (1,5) |
| 2 | (2,4) |
| 3 | (3,3) |
| 4 | (4,2) |
| 5 | (5,1) |

Sorting by `a` changes nothing:

| Sorted Position | Pair |
| --- | --- |
| 1 | (1,5) |
| 2 | (2,4) |
| 3 | (3,3) |
| 4 | (4,2) |
| 5 | (5,1) |

Result:

```
a' = [1,2,3,4,5]
b' = [5,4,3,2,1]
```

Every pair of positions disagrees between `a` and `b`, so each unordered pair contributes exactly one inversion no matter how the pairs are arranged. No reordering can improve the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the `n` pairs dominates |
| Space | O(n) | Storage for the pair list |

The sum of all `n` is at most `2·10^5`, so the total work is roughly `2·10^5 log(2·10^5)`, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            b = list(map(int, input().split()))

            pairs = list(zip(a, b))
            pairs.sort()

            out.append(" ".join(str(x) for x, _ in pairs))
            out.append(" ".join(str(y) for _, y in pairs))

        return "\n".join(out)

    return solve()

# sample 1
assert run(
"""1
3
3 1 2
3 1 2
"""
) == \
"""1 2 3
1 2 3"""

# minimum size
assert run(
"""1
1
1
1
"""
) == \
"""1
1"""

# already sorted a
assert run(
"""1
2
1 2
2 1
"""
) == \
"""1 2
2 1"""

# reverse permutation
assert run(
"""1
5
5 4 3 2 1
1 2 3 4 5
"""
) == \
"""1 2 3 4 5
5 4 3 2 1"""

# random small case
assert run(
"""1
4
2 4 1 3
3 1 4 2
"""
) == \
"""1 2 3 4
4 3 2 1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1` | Same arrays | Smallest valid instance |
| `[1,2]`, `[2,1]` | Unchanged after sorting by `a` | Opposite ordering case |
| Reverse `a` | Sorted `a` after reconstruction | Correct pair reordering |
| Random permutation | Proper pair sorting | General correctness |

## Edge Cases

Consider the smallest possible input:

```
1
1
1
1
```

There is only one pair `(1,1)`. Sorting leaves it unchanged. Both inversion counts are zero. The algorithm correctly handles the absence of any comparisons.

Consider completely opposite orderings:

```
a = [1,2,3]
b = [3,2,1]
```

The pairs are:

```
(1,3), (2,2), (3,1)
```

Sorting by `a` changes nothing. Every unordered pair disagrees between the two coordinates, so each pair contributes exactly one inversion regardless of arrangement. The algorithm achieves the optimum because no arrangement can do better.

Consider identical permutations:

```
a = [3,1,2]
b = [3,1,2]
```

Every pair comparison agrees in both coordinates. Sorting by `a` produces:

```
a' = [1,2,3]
b' = [1,2,3]
```

All inversions disappear. This demonstrates the case where every preferred ordering can be satisfied simultaneously.

Consider a mixed example:

```
a = [2,1,3]
b = [1,3,2]
```

Pairs:

```
(2,1), (1,3), (3,2)
```

After sorting by `a`:

```
(1,3), (2,1), (3,2)
```

giving

```
a' = [1,2,3]
b' = [3,1,2]
```

Pairs whose coordinate orders agree are placed optimally, while disagreeing pairs contribute a fixed amount no matter what. This is exactly the structure used in the correctness proof.

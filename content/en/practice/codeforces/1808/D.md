---
title: "CF 1808D - Petya, Petya, Petr, and Palindromes"
description: "For every subarray of odd length k, we want to know how many element replacements are needed to turn that subarray into a palindrome. The answer is the sum of those values over all length-k subarrays."
date: "2026-06-09T08:58:14+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1808
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 861 (Div. 2)"
rating: 2100
weight: 1808
solve_time_s: 137
verified: true
draft: false
---

[CF 1808D - Petya, Petya, Petr, and Palindromes](https://codeforces.com/problemset/problem/1808/D)

**Rating:** 2100  
**Tags:** binary search, brute force, data structures, two pointers  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

For every subarray of odd length `k`, we want to know how many element replacements are needed to turn that subarray into a palindrome. The answer is the sum of those values over all length-`k` subarrays.

For a fixed odd-length subarray, each position on the left is paired with a symmetric position on the right. If the two values are already equal, no replacement is needed for that pair. If they differ, exactly one replacement is enough. Because different symmetric pairs are independent, the palindromicity of a subarray is simply the number of mismatching symmetric pairs.

The array length is up to `2 * 10^5`, so examining every subarray and every pair inside it is impossible. There are up to `2 * 10^5` windows, and each window may contain up to `10^5` symmetric pairs. A quadratic or cubic solution is far beyond the limit.

A subtle case appears when `k = 1`. Every length-1 subarray is already a palindrome, so the answer is always `0`.

For example:

```
3 1
5 7 9
```

The correct output is:

```
0
```

A solution that assumes every window contributes at least one pair would fail here.

Another easy place to make a mistake is near the array borders.

```
5 3
1 2 1 2 1
```

The equal pair `(0, 2)` belongs to a valid length-3 window, and so does `(2, 4)`. The pair `(0, 4)` does not belong to any length-3 window even though it is symmetric around a center. Counting all equal pairs within distance constraints without checking whether the center can be the center of a valid window gives the wrong result.

A third pitfall is parity. Symmetric positions around an integer center always have the same parity. Positions `1` and `2` can never form a symmetric pair inside an odd-length window because their midpoint is not an array index.

## Approaches

The brute-force solution follows the definition directly. For every window of length `k`, compare every symmetric pair and count mismatches. This is correct because each mismatch requires one replacement and each matching pair requires none.

The problem is the cost. There are `n - k + 1` windows and `(k - 1) / 2` pairs per window. In the worst case this becomes roughly `2 * 10^10` comparisons, which is far too large.

The key observation is to stop thinking about windows and start thinking about symmetric pairs.

Let

```
m = (k - 1) / 2
```

Every valid window contributes exactly `m` symmetric pairs. Since there are `n - k + 1` windows, the total number of symmetric-pair appearances is

```
(n - k + 1) * m
```

If we counted every such pair as a mismatch, that would be the answer. The only correction is that equal symmetric pairs contribute `0` instead of `1`.

So the problem becomes:

```
How many valid symmetric pair appearances have equal values?
```

Each symmetric pair is identified by two positions `(i, j)`.

The pair is used by some length-`k` window if and only if:

```
1. i and j have the same parity.
2. j - i <= 2m.
3. Their midpoint lies inside the range of valid window centers.
```

Now we only need to count equal-value position pairs satisfying those conditions.

Positions with different values are irrelevant, so we group indices by value. Inside each value group, indices are sorted. For every index `i`, we compute the interval of positions `j` that satisfy all validity constraints, then count how many equal-valued indices fall inside that interval using binary search.

This reduces the problem to `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Let `m = (k - 1) // 2`.
2. Compute

```
total_pairs = (n - k + 1) * m
```

This is the number of symmetric-pair appearances across all windows.
3. Group array positions by value and parity.

Positions with different parity can never form a symmetric pair around an integer center, so we store two lists for each value.
4. For every position `p` inside one parity list, determine which equal-valued positions `q > p` can form a valid symmetric pair.
5. The midpoint condition gives

```
m <= (p + q) / 2 <= n - m - 1
```

which becomes

```
2m - p <= q <= 2(n - m - 1) - p
```
6. The distance condition gives

```
q <= p + 2m
```
7. Combining all constraints,

```
low = max(p + 1, 2m - p)
up  = min(p + 2m, 2(n - m - 1) - p)
```
8. Use binary search in the sorted parity list to count how many positions lie in `[low, up]`.
9. Sum all such counts into `equal_pairs`.
10. Every valid symmetric pair appearance contributes either `1` if values differ or `0` if values are equal, so

```
answer = total_pairs - equal_pairs
```

### Why it works

Every symmetric pair appearance in every window corresponds to exactly one pair of array positions `(i, j)` whose midpoint is the window center. The three derived conditions are precisely the conditions under which such a window exists.

`total_pairs` counts all symmetric pair appearances. `equal_pairs` counts exactly those appearances whose endpoints already match. Each matching pair contributes `0` to palindromicity instead of `1`, so subtracting them leaves exactly the number of mismatching symmetric pair appearances, which is the required sum of palindromicities.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict

input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

m = (k - 1) // 2

total_pairs = (n - k + 1) * m

pos = defaultdict(lambda: [[], []])

for i, x in enumerate(a):
    pos[x][i & 1].append(i)

equal_pairs = 0

for parity_lists in pos.values():
    for arr in parity_lists:
        for idx, p in enumerate(arr):
            low = max(p + 1, 2 * m - p)
            up = min(p + 2 * m, 2 * (n - m - 1) - p)

            if low > up:
                continue

            l = bisect_left(arr, low, idx + 1)
            r = bisect_right(arr, up)

            equal_pairs += r - l

print(total_pairs - equal_pairs)
```

The first part computes the total number of symmetric-pair appearances across all windows.

The dictionary groups indices by value and parity. Splitting by parity is crucial because symmetric positions around an integer center always have equal parity. Without this separation, pairs with non-integer midpoints would be counted incorrectly.

For a fixed position `p`, the interval `[low, up]` is the intersection of all validity constraints. Every equal-valued position inside that interval forms one matching symmetric pair appearance.

The binary searches count those positions in logarithmic time. Since every index belongs to exactly one list, the total work is `O(n log n)`.

All arithmetic fits comfortably inside Python integers. The answer can reach roughly `10^10`, so using 32-bit integers in other languages would be unsafe.

## Worked Examples

### Sample 1

Input:

```
8 5
1 2 8 2 5 2 8 6
```

Here:

```
m = 2
total_pairs = 4 * 2 = 8
```

Valid equal symmetric pairs:

| p | q | value | counted? |
| --- | --- | --- | --- |
| 1 | 3 | 2 | Yes |
| 2 | 6 | 8 | Yes |
| 3 | 5 | 2 | Yes |
| 1 | 5 | 2 | No |

The last pair is too far apart.

So:

| Quantity | Value |
| --- | --- |
| total_pairs | 8 |
| equal_pairs | 4 |
| answer | 4 |

Output:

```
4
```

This example shows that the answer is not computed window-by-window. We count all symmetric pair appearances globally and subtract the matching ones.

### Sample 2

Input:

```
9 9
1 2 3 4 5 4 3 2 1
```

Here:

```
m = 4
total_pairs = 1 * 4 = 4
```

The only window is already a palindrome.

| Symmetric pair | Equal? |
| --- | --- |
| (0, 8) | Yes |
| (1, 7) | Yes |
| (2, 6) | Yes |
| (3, 5) | Yes |

Thus:

| Quantity | Value |
| --- | --- |
| total_pairs | 4 |
| equal_pairs | 4 |
| answer | 0 |

Output:

```
0
```

This demonstrates that when every symmetric pair matches, the subtraction removes all contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each index participates in binary searches inside its value-parity group |
| Space | O(n) | Storage of grouped positions |

With `n ≤ 2 · 10^5`, an `O(n log n)` solution performs only a few million operations and easily fits within the time limit. The auxiliary memory is linear in the number of indices.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left, bisect_right
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    m = (k - 1) // 2
    total_pairs = (n - k + 1) * m

    pos = defaultdict(lambda: [[], []])

    for i, x in enumerate(a):
        pos[x][i & 1].append(i)

    equal_pairs = 0

    for parity_lists in pos.values():
        for arr in parity_lists:
            for idx, p in enumerate(arr):
                low = max(p + 1, 2 * m - p)
                up = min(p + 2 * m, 2 * (len(a) - m - 1) - p)

                if low > up:
                    continue

                l = bisect_left(arr, low, idx + 1)
                r = bisect_right(arr, up)

                equal_pairs += r - l

    return str(total_pairs - equal_pairs)

# provided sample
assert run("8 5\n1 2 8 2 5 2 8 6\n") == "4"

# minimum size
assert run("1 1\n7\n") == "0"

# all equal
assert run("5 3\n4 4 4 4 4\n") == "0"

# k = 1
assert run("4 1\n1 2 3 4\n") == "0"

# off-by-one around borders
assert run("5 3\n1 2 1 2 1\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7` | `0` | Minimum input size |
| `5 3 / 4 4 4 4 4` | `0` | Every window already palindromic |
| `4 1 / 1 2 3 4` | `0` | Special case `k = 1` |
| `5 3 / 1 2 1 2 1` | `0` | Border-center constraints and parity handling |

## Edge Cases

Consider:

```
3 1
5 7 9
```

We have `m = 0`, so

```
total_pairs = 0
```

No symmetric pairs exist in any window. The algorithm immediately returns `0`.

Consider:

```
5 3
1 2 1 2 1
```

Valid centers are positions `1`, `2`, and `3`.

The pair `(0, 4)` has equal values and an integer midpoint, but its distance is `4`, larger than `2m = 2`. It never appears as a symmetric pair in a length-3 window. The interval computation excludes it automatically.

Consider:

```
5 5
1 1 2 1 1
```

The pair `(0, 1)` has equal values but different parity. Its midpoint is not an integer array position, so it cannot be symmetric around the center of an odd-length window. Because indices are separated by parity before counting, this pair is never considered.

These cases are exactly where many incorrect implementations overcount matching pairs. The interval and parity conditions eliminate all invalid pairs.

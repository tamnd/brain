---
title: "CF 1269B - Modulo Equality"
description: "We have two arrays of equal length. We may choose a single non-negative value x, add it to every element of the first array, and take all results modulo m. After this transformation, the order of elements does not matter."
date: "2026-06-11T20:14:41+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1269
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 609 (Div. 2)"
rating: 1500
weight: 1269
solve_time_s: 118
verified: true
draft: false
---

[CF 1269B - Modulo Equality](https://codeforces.com/problemset/problem/1269/B)

**Rating:** 1500  
**Tags:** brute force, sortings  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two arrays of equal length. We may choose a single non-negative value `x`, add it to every element of the first array, and take all results modulo `m`.

After this transformation, the order of elements does not matter. We are allowed to rearrange the transformed array arbitrarily. The task is to find the smallest `x` for which the transformed multiset becomes exactly the same as the multiset represented by the second array.

The key detail is that we are comparing multisets, not positions. If two arrays contain the same values with the same frequencies, they are considered equal after some permutation.

The constraints are unusually revealing. The array length is at most 2000, while `m` can be as large as `10^9`. A solution that iterates over all possible values of `x` is impossible because the search space is far too large. On the other hand, `n = 2000` is small enough that an `O(n² log n)` solution is perfectly acceptable. Around eight million operations are manageable within the time limit.

Several edge cases can easily break a careless implementation.

Consider duplicate values:

```
n = 3, m = 5
a = [0, 0, 0]
b = [2, 2, 2]
```

The correct answer is `2`.

A solution that assumes all elements are distinct and tries to match positions instead of frequencies will fail.

Wrap-around modulo arithmetic is another source of mistakes:

```
n = 2, m = 10
a = [8, 9]
b = [0, 1]
```

The correct answer is `2` because:

```
(8 + 2) mod 10 = 0
(9 + 2) mod 10 = 1
```

Using ordinary subtraction without modulo handling would incorrectly produce a negative shift.

A more subtle case occurs when several shifts appear plausible:

```
n = 3, m = 7
a = [0, 1, 2]
b = [1, 2, 3]
```

Both arrays are already sorted, and the valid shift is `1`. A greedy matching strategy that does not verify the entire multiset could incorrectly accept another candidate.

The problem guarantees that at least one valid answer exists, but we must still find the smallest one.

## Approaches

A straightforward brute-force idea is to try every possible shift `x` from `0` to `m - 1`. For each candidate, transform every element of `a`, sort the resulting array, and compare it with the sorted version of `b`.

This works because the condition depends only on the multiset of values. If the sorted transformed array equals the sorted target array, then some permutation exists.

The issue is the size of `m`. Since `m` can reach `10^9`, checking every shift is completely infeasible.

The crucial observation comes from sorting.

Let:

```
A = sorted(a)
B = sorted(b)
```

Suppose some shift `x` is valid. After applying `x` modulo `m`, the smallest element of `B` must originate from some element of `A`.

Assume `A[i]` becomes the smallest element `B[0]`. Then:

```
(A[i] + x) mod m = B[0]
```

which implies

```
x = (B[0] - A[i] + m) mod m
```

For every position `i`, this formula generates one possible shift. There are only `n` such candidates.

Why is that enough? Because in any valid transformation, some element of `A` must map to the minimum value in `B`. The corresponding shift will appear among these `n` candidates.

Now the problem becomes much smaller. Generate all candidate shifts derived from matching an element of `A` to `B[0]`. For each candidate, transform every value of `A`, sort the result, and compare with `B`.

Among all valid candidates, return the minimum.

Since there are only `n` candidates and each verification costs `O(n log n)`, the total complexity becomes `O(n² log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m · n log n) | O(n) | Too slow |
| Optimal | O(n² log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and the two arrays.
2. Sort both arrays and store them as `A` and `B`.
3. For every index `i` in `A`, compute the candidate shift

```
x = (B[0] - A[i] + m) mod m
```

This corresponds to forcing `A[i]` to become the smallest value in the target multiset.
4. Apply this candidate shift to every element of `A`:

```
transformed[j] = (A[j] + x) mod m
```
5. Sort the transformed array.
6. Compare the sorted transformed array with `B`.

If they are equal, this shift is valid.
7. Keep the smallest valid shift encountered.
8. Output that minimum shift.

### Why it works

Assume `x*` is the correct answer.

After applying `x*`, the transformed values form exactly the multiset represented by `B`. The smallest value of `B`, namely `B[0]`, must come from some element `A[i]`.

For that element,

```
(A[i] + x*) mod m = B[0]
```

which rearranges to

```
x* = (B[0] - A[i] + m) mod m
```

Thus `x*` is one of the generated candidates.

Every candidate is checked by explicitly constructing the transformed multiset and comparing it with `B`. A candidate is accepted if and only if it produces exactly the required multiset.

Since every valid shift is examined and we return the smallest valid one, the algorithm always produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()
    b.sort()

    answer = m

    for v in a:
        x = (b[0] - v) % m

        transformed = sorted((num + x) % m for num in a)

        if transformed == b:
            answer = min(answer, x)

    print(answer)

if __name__ == "__main__":
    solve()
```

The first step is sorting both arrays because the problem is really about comparing multisets. Once sorted, equality of multisets becomes ordinary array equality.

The loop over `a` generates all candidate shifts. Each candidate comes from the observation that some element of the sorted source array must map to the minimum element of the sorted target array.

For each candidate, the code transforms every element using modular arithmetic. The expression

```
(num + x) % m
```

must be used exactly in this form. Forgetting the modulo operation would fail on wrap-around cases.

The transformed values are sorted before comparison. Even if the transformation is correct, modulo arithmetic can change the order of elements, so comparing without sorting would be incorrect.

The variable `answer` stores the minimum valid shift found so far. The problem asks for the smallest valid shift, not merely any valid shift.

## Worked Examples

### Example 1

Input:

```
4 3
0 0 2 1
2 0 1 1
```

After sorting:

```
A = [0, 0, 1, 2]
B = [0, 1, 1, 2]
```

| Candidate source value | x | Transformed sorted array | Valid |
| --- | --- | --- | --- |
| 0 | 0 | [0,0,1,2] | No |
| 0 | 0 | [0,0,1,2] | No |
| 1 | 2 | [0,0,2,2] | No |
| 2 | 1 | [0,1,1,2] | Yes |

The smallest valid shift is `1`.

This example shows why we must test all candidates. The first few shifts look reasonable but fail when the entire multiset is checked.

### Example 2

Input:

```
3 10
8 9 0
0 1 2
```

After sorting:

```
A = [0, 8, 9]
B = [0, 1, 2]
```

| Candidate source value | x | Transformed sorted array | Valid |
| --- | --- | --- | --- |
| 0 | 0 | [0,8,9] | No |
| 8 | 2 | [0,1,2] | Yes |
| 9 | 1 | [0,0,9] | No |

Answer:

```
2
```

This example demonstrates the wrap-around behavior of modulo arithmetic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² log n) | Up to `n` candidate shifts, each requiring a sort of `n` transformed values |
| Space | O(n) | Temporary transformed array |

With `n ≤ 2000`, the worst case is roughly:

```
2000 × 2000 × log2(2000)
```

operations, which comfortably fits within the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()
    b.sort()

    ans = m

    for v in a:
        x = (b[0] - v) % m
        cur = sorted((y + x) % m for y in a)
        if cur == b:
            ans = min(ans, x)

    return str(ans)

# provided sample
assert run(
"""4 3
0 0 2 1
2 0 1 1
"""
) == "1", "sample 1"

# minimum size
assert run(
"""1 100
37
37
"""
) == "0", "single element"

# all equal values
assert run(
"""3 5
0 0 0
2 2 2
"""
) == "2", "duplicates"

# wrap-around modulo
assert run(
"""2 10
8 9
0 1
"""
) == "2", "modulo wrap"

# smallest valid answer among multiple candidates
assert run(
"""3 7
0 1 2
1 2 3
"""
) == "1", "minimum valid shift"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | 0 | Minimum size boundary |
| All values equal | 2 | Correct handling of duplicates |
| Wrap-around case | 2 | Modular arithmetic correctness |
| Shift by one | 1 | Smallest valid answer selection |

## Edge Cases

Consider duplicated values:

```
3 5
0 0 0
2 2 2
```

After sorting:

```
A = [0,0,0]
B = [2,2,2]
```

Every candidate produces:

```
x = (2 - 0) mod 5 = 2
```

Transforming gives:

```
[2,2,2]
```

which matches `B`. The algorithm compares multisets, not positions, so duplicates are handled naturally.

Consider wrap-around arithmetic:

```
2 10
8 9
0 1
```

The candidate derived from `8` is:

```
x = (0 - 8 + 10) mod 10 = 2
```

Applying the shift:

```
(8 + 2) mod 10 = 0
(9 + 2) mod 10 = 1
```

The transformed multiset becomes exactly `[0,1]`. Negative differences never cause problems because all candidate shifts are computed modulo `m`.

Consider a case where an incorrect candidate appears plausible:

```
3 7
0 1 2
1 2 3
```

The candidate generated from `A[0]` is:

```
x = 1
```

which succeeds.

Another candidate might align one element correctly but produce a transformed multiset different from `B`. Since every candidate is verified by comparing the entire sorted arrays, partial matches cannot be accepted accidentally.

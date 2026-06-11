---
title: "CF 1363A - Odd Selection"
description: "We are given an array of integers and must choose exactly x elements from it. The chosen elements can come from any positions in the array. The question is whether there exists a selection of exactly x elements whose sum is odd."
date: "2026-06-11T12:28:14+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1363
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 646 (Div. 2)"
rating: 1200
weight: 1363
solve_time_s: 134
verified: true
draft: false
---

[CF 1363A - Odd Selection](https://codeforces.com/problemset/problem/1363/A)

**Rating:** 1200  
**Tags:** brute force, implementation, math  
**Solve time:** 2m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and must choose exactly `x` elements from it. The chosen elements can come from any positions in the array. The question is whether there exists a selection of exactly `x` elements whose sum is odd.

The actual values of the numbers do not matter beyond their parity. Every integer is either odd or even, and the parity of a sum depends only on how many odd numbers are included. A sum is odd if and only if it contains an odd number of odd elements.

The constraints are small. Each test case contains at most 1000 numbers, and there are at most 100 test cases. Even an `O(n²)` solution would be acceptable, but the parity observation allows an even simpler linear solution. There is no need for dynamic programming or subset enumeration.

Several edge cases are easy to miss.

Consider an array containing only even numbers:

```
1
4 3
2 4 6 8
```

The correct answer is `No`. Any sum of even numbers remains even. A careless solution that only checks whether `x` is odd would fail here.

Consider an array containing only odd numbers:

```
1
4 2
1 3 5 7
```

The correct answer is `No`. Choosing two odd numbers produces an even sum. Some implementations incorrectly assume that having odd numbers available is always sufficient.

Consider the case where we must take all elements:

```
1
3 3
1 2 3
```

The total sum is `6`, which is even, so the answer is `No`. When `x = n`, there is only one possible selection.

Another subtle case occurs when there are enough odd numbers to make the sum odd, but not enough total elements to fill the remaining slots with a valid parity:

```
1
3 3
1 2 2
```

We must take all three elements. The sum is `5`, so the answer is `Yes`. The feasibility depends on both the number of odd elements and the requirement to select exactly `x` elements.

## Approaches

A brute-force approach would enumerate all subsets of size `x` and check whether any of them has an odd sum. This is correct because it examines every possible choice. The problem is the number of such subsets. In the worst case we would need to inspect

$$\binom{1000}{500}$$

different selections, which is astronomically large and completely impossible within the time limit.

The key observation is that only parity matters. Let `odd` be the number of odd elements in the array and `even` be the number of even elements.

A selected sum is odd exactly when the number of selected odd elements is odd. Suppose we choose `k` odd elements. Then:

$$k + \text{chosen even elements} = x$$

Since the remaining selected elements must be even elements, we need:

$$x - k \le even$$

and also

$$k \le odd$$

The value `k` must be odd because the final sum must be odd.

The problem becomes: does there exist an odd integer `k` such that:

$$1 \le k \le odd$$

and

$$x-k \le even$$

and

$$k \le x$$

There are at most `x` possible values of `k`, so checking all odd values is trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n,x)) | O(x) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many elements in the array are odd and how many are even.
2. Try every odd value `k` from `1` up to `min(odd, x)`.
3. Treat `k` as the number of odd elements we want to select. Since `k` is odd, any valid selection using exactly `k` odd elements will have an odd sum.
4. Compute `need_even = x - k`. These are the remaining positions that must be filled with even elements.
5. Check whether `need_even` is non-negative and whether `need_even <= even`. If both conditions hold, we can build a selection of exactly `x` elements.
6. If any odd `k` satisfies the conditions, print `Yes`.
7. If no candidate works, print `No`.

### Why it works

The parity of a sum depends only on the count of odd numbers included. A sum is odd exactly when that count is odd.

The algorithm checks every possible odd count `k` that could appear in a valid selection. For each such `k`, it verifies whether enough odd elements exist to provide those `k` numbers and enough even elements exist to fill the remaining `x-k` positions.

If the algorithm finds a feasible `k`, an actual selection can be constructed directly from those counts. If every odd `k` fails, then no selection can have both the required size and odd parity. Since every valid solution must correspond to some odd value of `k`, the algorithm is complete and cannot miss a solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        odd = sum(v % 2 for v in a)
        even = n - odd

        possible = False

        for k in range(1, min(odd, x) + 1, 2):
            need_even = x - k
            if need_even <= even:
                possible = True
                break

        ans.append("Yes" if possible else "No")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first part of the solution counts odd and even elements. Nothing else about the values matters.

The loop over `k` checks every possible odd count of selected odd numbers. The step size is `2`, which guarantees that every candidate `k` is odd.

The condition `need_even <= even` verifies that enough even numbers exist to complete the selection. We do not need a separate check that `need_even >= 0` because the loop only considers `k <= x`.

As soon as one feasible configuration is found, the answer is known to be `Yes`, so the loop terminates early.

No special handling is required for large values because only counts are manipulated. Integer overflow is impossible in Python and the counts never exceed 1000 anyway.

## Worked Examples

### Example 1

Input:

```
1
2 2
51 50
```

| Step | odd | even | k | need_even | Valid? |
| --- | --- | --- | --- | --- | --- |
| Count parities | 1 | 1 | - | - | - |
| Try k=1 | 1 | 1 | 1 | 1 | Yes |

The algorithm finds that selecting one odd and one even number is possible. The resulting sum has odd parity, so the answer is `Yes`.

### Example 2

Input:

```
1
3 3
101 102 103
```

| Step | odd | even | k | need_even | Valid? |
| --- | --- | --- | --- | --- | --- |
| Count parities | 2 | 1 | - | - | - |
| Try k=1 | 2 | 1 | 1 | 2 | No |
| No more odd k values | 2 | 1 | - | - | - |

To select three elements with only one odd element chosen, we would need two even elements, but only one exists. Choosing three odd elements is impossible because only two odd numbers are present. No feasible configuration exists, so the answer is `No`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting parities dominates the work |
| Space | O(1) | Only a few counters are stored |

The array is scanned once per test case. With at most 1000 elements per test case and at most 100 test cases, the total amount of work is tiny compared to the available limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        odd = sum(v % 2 for v in a)
        even = n - odd

        ok = False
        for k in range(1, min(odd, x) + 1, 2):
            if x - k <= even:
                ok = True
                break

        out.append("Yes" if ok else "No")

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""5
1 1
999
1 1
1000
2 1
51 50
2 2
51 50
3 3
101 102 103
"""
) == """Yes
No
Yes
Yes
No
"""

# minimum size, odd element
assert run(
"""1
1 1
1
"""
) == "Yes\n", "single odd number"

# minimum size, even element
assert run(
"""1
1 1
2
"""
) == "No\n", "single even number"

# all even values
assert run(
"""1
5 3
2 4 6 8 10
"""
) == "No\n", "all sums remain even"

# all odd values, even selection size
assert run(
"""1
4 2
1 3 5 7
"""
) == "No\n", "two odd numbers give even sum"

# boundary case x=n
assert run(
"""1
3 3
1 2 2
"""
) == "Yes\n", "must take all elements"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | Yes | Smallest valid odd case |
| `1 1 / 2` | No | Smallest impossible case |
| All even numbers | No | Odd sum cannot be formed |
| All odd numbers with even x | No | Even number of odds gives even sum |
| `x=n` case | Yes | Handles forced full-array selection |

## Edge Cases

### All Elements Are Even

Input:

```
1
4 3
2 4 6 8
```

The algorithm counts `odd = 0` and `even = 4`. Since there is no odd value of `k` to try, the loop never finds a valid configuration. The output is `No`.

This matches the mathematical fact that any sum of even numbers is even.

### All Elements Are Odd, Selection Size Is Even

Input:

```
1
4 2
1 3 5 7
```

The algorithm counts `odd = 4` and `even = 0`.

It tries `k = 1`, which requires one even element, but none exist.

No larger odd `k` is allowed because `k > x`.

The output is `No`.

Every selection of exactly two odd numbers has an even sum, so the result is correct.

### Must Select Every Element

Input:

```
1
3 3
1 2 3
```

The algorithm counts `odd = 2` and `even = 1`.

Trying `k = 1` requires two even elements, but only one exists.

No other odd value is possible.

The output is `No`.

Since all three elements must be selected and their total sum is `6`, an even number, no valid selection exists.

### Exactly One Odd Number Available

Input:

```
1
5 5
1 2 2 2 2
```

The algorithm counts `odd = 1` and `even = 4`.

Trying `k = 1` gives `need_even = 4`, which is available.

The output is `Yes`.

Selecting the single odd element together with all four even elements produces an odd sum, confirming that the counting logic handles this boundary case correctly.

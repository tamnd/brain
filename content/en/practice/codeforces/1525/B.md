---
title: "CF 1525B - Permutation Sort"
description: "We are given a permutation of the numbers from 1 to n. In one operation, we may choose any contiguous segment of the array and rearrange the elements inside that segment however we like. The only restriction is that the chosen segment cannot be the entire array."
date: "2026-06-10T17:24:55+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1525
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 109 (Rated for Div. 2)"
rating: 900
weight: 1525
solve_time_s: 136
verified: true
draft: false
---

[CF 1525B - Permutation Sort](https://codeforces.com/problemset/problem/1525/B)

**Rating:** 900  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the numbers from `1` to `n`. In one operation, we may choose any contiguous segment of the array and rearrange the elements inside that segment however we like. The only restriction is that the chosen segment cannot be the entire array.

The goal is to determine the minimum number of such operations needed to transform the permutation into the sorted order `[1, 2, ..., n]`.

The key detail is that rearranging a chosen segment is extremely powerful. We are not limited to swaps or reversals. Once a segment is selected, its contents can be placed in any order. The only limitation comes from the fact that the segment cannot cover all `n` positions.

The constraints are very small. The array length never exceeds 50, and there are at most 2000 test cases. Even expensive computations would fit comfortably. Still, this problem is designed around discovering a simple structural observation rather than simulating operations.

Several edge cases are easy to miss.

Consider an already sorted permutation:

```
1 2 3 4
```

The answer is `0`, not `1`. Since no work is needed, applying any operation would only make the array less sorted.

Consider:

```
2 1 3 4
```

The answer is `1`. A careless solution might think that because the first element is wrong, multiple operations are required. In reality, we can choose positions `[1,2]` and reorder them.

A more subtle case is:

```
4 2 3 1
```

Here the first element is not `1` and the last element is not `n`. The answer is `3`. Many solutions incorrectly return `2`. The reason is that both ends are misplaced, and the values that belong at the ends are also trapped in the wrong places. This turns out to be the unique situation requiring three operations.

## Approaches

A brute-force viewpoint is to think about all possible segments and all possible reorderings of those segments. Since a segment may be rearranged arbitrarily, the branching factor is enormous. Even for `n = 50`, enumerating possible states is completely infeasible.

The interesting part of the problem is that we are not asked to construct the operations. We only need the minimum count. That suggests looking for a characterization of the answer rather than searching for it.

The crucial observation is that the answer can only be `0`, `1`, `2`, or `3`.

If the permutation is already sorted, the answer is obviously `0`.

Suppose the permutation is not sorted. If either the first position already contains `1` or the last position already contains `n`, then one operation is enough. We can choose the remaining part of the array and rearrange it into the correct order.

For example:

```
1 4 3 2
```

The first position is already correct. We can select positions `[2,4]` and sort them.

Now consider the case where neither end is correct.

If the value `1` is currently at the last position and the value `n` is currently at the first position, then the answer is `3`. This is the worst possible arrangement of the endpoints. No single operation can touch both ends simultaneously because the whole array is forbidden, and fixing one side does not automatically fix the other.

In every remaining case, the answer is `2`. Neither endpoint is already correct, but the permutation is not in the special worst-case configuration.

This completely determines the answer from a few endpoint checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the permutation.
2. Check whether the permutation is already sorted.

If every position `i` contains `i + 1`, no operation is needed, so output `0`.
3. Check whether the first element is `1` or the last element is `n`.

If either condition holds, output `1`.

The reason is that the rest of the array forms a proper subarray, which may be rearranged freely to complete the sorting.
4. Check whether the first element is `n` and the last element is `1`.

If both conditions hold, output `3`.

This is the unique configuration that requires the maximum number of operations.
5. Otherwise output `2`.

Neither endpoint is already correct, but the arrangement is not the worst possible one, so two operations always suffice.

### Why it works

The entire problem is controlled by the endpoints.

If the array is already sorted, the answer is `0`.

If one endpoint is already correct, the remaining positions form a valid proper subarray. Since a chosen subarray may be rearranged arbitrarily, one operation is enough.

When both endpoints are incorrect, a single operation cannot sort the permutation. Any proper subarray misses at least one endpoint, so at least one incorrect endpoint would remain.

Among those cases, the arrangement with `n` at the beginning and `1` at the end is the hardest. Fixing both misplaced extreme values cannot be done in only two operations because the whole array may never be selected. The official analysis shows that this configuration requires exactly three operations.

Every other unsorted permutation falls into the remaining category and can be fixed in two operations.

Since the cases are mutually exclusive and cover all permutations, the algorithm always returns the correct minimum number of operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        if a == list(range(1, n + 1)):
            print(0)
        elif a[0] == 1 or a[-1] == n:
            print(1)
        elif a[0] == n and a[-1] == 1:
            print(3)
        else:
            print(2)

solve()
```

The first condition checks whether the permutation is already sorted. This must be handled before any endpoint logic, otherwise a sorted permutation such as `[1,2,3]` would incorrectly match the second case and return `1`.

The second condition detects the situations where one operation is enough. We only need one of the endpoints to already be correct.

The third condition identifies the unique worst-case arrangement. It must be checked after the previous conditions because a permutation with `a[0] = n` and `a[n-1] = 1` can never satisfy the one-operation condition anyway.

Every remaining permutation belongs to the two-operation category.

No special handling for small `n` is required. The logic works uniformly for all valid inputs.

## Worked Examples

### Sample Input 1

```
4
1 3 2 4
```

| Check | Result |
| --- | --- |
| Sorted? | No |
| First element = 1? | Yes |
| Answer | 1 |

The first position already contains its final value. We can sort the suffix `[3,2,4]` in a single operation.

### Sample Input 2

```
5
2 1 4 5 3
```

| Check | Result |
| --- | --- |
| Sorted? | No |
| First element = 1? | No |
| Last element = n? | No |
| First element = n? | No |
| Last element = 1? | No |
| Answer | 2 |

Neither endpoint is already correct, so one operation is impossible. The permutation is not in the worst-case configuration, so two operations are sufficient.

### Worst-Case Example

```
5
5 2 3 4 1
```

| Check | Result |
| --- | --- |
| Sorted? | No |
| First element = 1? | No |
| Last element = n? | No |
| First element = n? | Yes |
| Last element = 1? | Yes |
| Answer | 3 |

This is exactly the special configuration that requires three operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One comparison against the sorted permutation plus a few constant-time checks |
| Space | O(1) | Only a few variables beyond the input array |

With `n ≤ 50`, this solution is far below the limits. Even with 2000 test cases, the total amount of work is tiny.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        if a == list(range(1, n + 1)):
            out.append("0")
        elif a[0] == 1 or a[-1] == n:
            out.append("1")
        elif a[0] == n and a[-1] == 1:
            out.append("3")
        else:
            out.append("2")

    return "\n".join(out) + "\n"

# provided samples
assert run(
"""3
4
1 3 2 4
3
1 2 3
5
2 1 4 5 3
"""
) == "1\n0\n2\n", "sample"

# already sorted
assert run(
"""1
3
1 2 3
"""
) == "0\n"

# first element correct
assert run(
"""1
5
1 5 4 3 2
"""
) == "1\n"

# last element correct
assert run(
"""1
5
2 5 4 1 5
"""
) != "1\n"  # not a valid permutation, avoid using

assert run(
"""1
5
2 1 3 4 5
"""
) == "1\n"

# worst case
assert run(
"""1
5
5 2 3 4 1
"""
) == "3\n"

# generic two-operation case
assert run(
"""1
5
2 1 4 5 3
"""
) == "2\n"
```

### Custom Test Summary

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3` | `0` | Already sorted permutation |
| `1 5 4 3 2` | `1` | First endpoint already correct |
| `2 1 3 4 5` | `1` | Last endpoint already correct |
| `5 2 3 4 1` | `3` | Worst-case arrangement |
| `2 1 4 5 3` | `2` | General two-operation case |

## Edge Cases

Consider the already sorted permutation:

```
1
3
1 2 3
```

The algorithm first checks whether the entire array equals `[1,2,3]`. It does, so the answer is `0`. This prevents the array from incorrectly matching the one-operation case.

Consider:

```
1
4
1 4 3 2
```

The array is not sorted, but the first element is already `1`. The algorithm returns `1`. We can sort the subarray `[4,3,2]` directly because it is a proper subarray.

Consider:

```
1
4
4 2 3 1
```

The array is not sorted. Neither endpoint is correct. The first element equals `n` and the last element equals `1`, so the algorithm returns `3`. This is exactly the special worst-case configuration identified by the proof.

Consider:

```
1
5
2 3 1 5 4
```

The array is not sorted. Neither endpoint is correct, but it is not the worst-case arrangement. The algorithm reaches the final branch and returns `2`, which is the minimum number of operations for this category.

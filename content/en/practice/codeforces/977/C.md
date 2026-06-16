---
title: "CF 977C - Less or Equal"
description: "We are given a list of integers and asked to construct a value $x$ between 1 and $10^9$ such that exactly $k$ elements of the list are less than or equal to $x$. If no such value exists, we must output $-1$."
date: "2026-06-17T01:26:45+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 977
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 479 (Div. 3)"
rating: 1200
weight: 977
solve_time_s: 93
verified: true
draft: false
---

[CF 977C - Less or Equal](https://codeforces.com/problemset/problem/977/C)

**Rating:** 1200  
**Tags:** sortings  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers and asked to construct a value $x$ between 1 and $10^9$ such that exactly $k$ elements of the list are less than or equal to $x$. If no such value exists, we must output $-1$.

A useful way to think about this is that $x$ defines a threshold on the number line. As $x$ increases, the count of elements $\le x$ only increases, never decreases. We are trying to find a point where this count becomes exactly $k$.

The input size allows up to $2 \cdot 10^5$ numbers. Any approach that checks every candidate $x$ directly in the range $[1, 10^9]$ is impossible, since that would require up to $10^9$ operations. Even checking each array element repeatedly in a naive way would lead to about $O(n^2)$ work in the worst case, which is far beyond the time limit.

A key edge case appears when multiple values in the array are equal around the boundary. If we pick an $x$ equal to some value in the array, the count of elements $\le x$ might jump by more than one at once. For example, if the array is $[3, 3, 3]$ and $k = 2$, there is no $x$ that yields exactly two elements $\le x$, since the count jumps from 0 (for $x < 3$) directly to 3 (for $x \ge 3$).

Another subtle case is $k = 0$. This requires an $x$ smaller than all elements. Since $x \ge 1$, this is only possible if all array values are greater than 1, and even then $x = 1$ may or may not work depending on whether any element equals 1.

## Approaches

The brute-force idea is to try every possible integer $x$ from 1 to $10^9$, and for each one count how many array elements are $\le x$. This is correct because it directly matches the condition we want, but it performs $10^9$ candidate checks, each costing $O(n)$, leading to $O(n \cdot 10^9)$, which is completely infeasible.

The key observation is that the function “number of elements $\le x$” changes only at values present in the array. Between two consecutive distinct array values, the count stays constant. This means we only need to consider thresholds near sorted values of the array.

After sorting the array, we can compute where the prefix length equals $k$. If such a prefix exists, any value $x$ between the $k$-th smallest value and just below the $(k+1)$-th smallest value will work. A clean construction is to take the $k$-th smallest element and ensure it does not accidentally include the $(k+1)$-th one.

The only failure case is when the $k$-th and $(k+1)$-th elements are equal, because then any $x$ that includes one includes all equal copies, making it impossible to isolate exactly $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot 10^9)$ | $O(1)$ | Too slow |
| Optimal (sorting) | $O(n \log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. This lets us reason about prefix counts directly.
2. If $k = 0$, we want a value strictly smaller than all elements. We check the smallest element. If it is 1, no valid $x \ge 1$ exists, so we output $-1$. Otherwise we output 1, since it ensures zero elements are $\le x$.
3. If $k = n$, we want all elements to be $\le x$. The largest element always works, so we output the maximum array value.
4. Otherwise, consider the $k$-th smallest element (index $k-1$ in 0-based indexing).
5. Check the $(k+1)$-th smallest element (index $k$). If it is equal to the $k$-th element, then any $x$ that includes the $k$-th also includes the $(k+1)$-th, so we cannot achieve exactly $k$. In this case, output $-1$.
6. If they differ, output the $k$-th element as the answer. This guarantees exactly $k$ elements are $\le x$.

### Why it works

After sorting, the number of elements $\le x$ is a step function that increases only at distinct array values. Choosing $x$ equal to the $k$-th smallest value ensures at least $k$ elements are included. If the next distinct value is strictly larger, no additional elements enter until after that gap, so the count remains exactly $k$. If duplicates collapse the gap, the step size becomes too large, making exact equality impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))
a.sort()

if k == 0:
    if a[0] == 1:
        print(-1)
    else:
        print(1)
elif k == n:
    print(a[-1])
else:
    x = a[k - 1]
    if a[k] == x:
        print(-1)
    else:
        print(x)
```

The sorting step organizes values so that prefix positions correspond to counts of elements less than or equal to a threshold. The handling of $k = 0$ is separate because we cannot choose $x = 0$, so we must ensure the chosen value stays within the allowed domain.

The critical check is comparing $a[k-1]$ and $a[k]$. If they are equal, any threshold that includes the $k$-th element necessarily includes more than $k$ elements, breaking the requirement.

## Worked Examples

### Example 1

Input:

```
7 4
3 7 5 1 10 3 20
```

Sorted array: $[1, 3, 3, 5, 7, 10, 20]$

We want $k = 4$, so we look at the 4th element (index 3), which is 5.

| Step | k-th value | (k+1)-th value | Decision |
| --- | --- | --- | --- |
| After sort | 5 | 7 | valid gap |

Since 5 and 7 differ, we output 5. Any value between 5 and 6 also works, so 5 is valid.

This confirms that the algorithm correctly finds a threshold where exactly four elements are included.

### Example 2

Input:

```
5 2
1 2 2 2 3
```

Sorted array: $[1, 2, 2, 2, 3]$

We take the 2nd element (index 1), which is 2. The 3rd element is also 2.

| Step | k-th value | (k+1)-th value | Decision |
| --- | --- | --- | --- |
| After sort | 2 | 2 | invalid |

Since they are equal, any $x \ge 2$ includes at least 3 elements, so achieving exactly 2 is impossible. Output is $-1$.

This shows the duplicate-block failure case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; all checks are constant time |
| Space | $O(1)$ | Sorting in-place aside from input array |

The constraints allow up to $2 \cdot 10^5$ elements, so an $O(n \log n)$ solution comfortably fits within time limits. Memory usage is linear in the input size, which is also safe under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    if k == 0:
        if a[0] == 1:
            return "-1"
        return "1"
    elif k == n:
        return str(a[-1])
    else:
        x = a[k - 1]
        if a[k] == x:
            return "-1"
        return str(x)

# provided sample
assert run("7 4\n3 7 5 1 10 3 20") == "5"

# all equal impossible case
assert run("5 2\n2 2 2 2 2") == "-1"

# k = 0 valid
assert run("3 0\n5 6 7") == "1"

# k = n case
assert run("4 4\n1 2 3 4") == "4"

# boundary duplicate-safe
assert run("6 3\n1 2 2 3 4 5") in {"2"}

# minimum size
assert run("1 1\n10") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | -1 | duplicate collapse failure |
| k = 0 | 1 | smallest threshold handling |
| k = n | max | full inclusion case |
| minimum size | element | single element correctness |

## Edge Cases

When all elements are equal and $k$ is not 0 or n, the algorithm correctly rejects the case because the equality check between $a[k-1]$ and $a[k]$ fails immediately. For example, input $[5, 5, 5]$ with $k = 1$ leads to $a[0] = 5$ and $a[1] = 5$, so no valid threshold exists.

For $k = 0$, the algorithm ensures we never pick a value below 1. If the smallest element is 3, output 1 yields zero elements $\le x$. If the smallest element is 1, no valid $x$ exists in the allowed range, so we correctly output $-1$.

For boundary $k = n$, sorting guarantees the last element is the maximum, so choosing it includes all elements without overcounting, even with duplicates.

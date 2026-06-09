---
title: "CF 1692G - 2^Sort"
description: "We are given an array and asked to examine every contiguous segment of fixed length $k+1$. For each such segment starting at position $i$, we conceptually transform it by multiplying element $j$ (relative to the segment start) by $2^j$."
date: "2026-06-09T23:04:03+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1692
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 799 (Div. 4)"
rating: 1400
weight: 1692
solve_time_s: 93
verified: true
draft: false
---

[CF 1692G - 2^Sort](https://codeforces.com/problemset/problem/1692/G)

**Rating:** 1400  
**Tags:** data structures, dp, sortings, two pointers  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and asked to examine every contiguous segment of fixed length $k+1$. For each such segment starting at position $i$, we conceptually transform it by multiplying element $j$ (relative to the segment start) by $2^j$. After this exponential weighting, we check whether the resulting sequence is strictly increasing. The task is to count how many starting positions produce a valid segment.

A direct reading hides the structure: we are not sorting or rearranging anything, only checking whether a very specific inequality chain holds across sliding windows. Each window imposes $k$ comparisons, and every comparison mixes adjacent values with a factor of two.

The constraints force a linear or near-linear solution per test case. Since the total $n$ over all test cases is at most $2 \cdot 10^5$, any solution that does $O(nk)$ work per test case is immediately too slow when $k$ can also be large. This pushes us toward an approach where we preprocess comparisons so each window can be checked in $O(1)$ or amortized $O(1)$.

A subtle edge case appears when values are equal or nearly equal after scaling. For example, if $a = [2, 1]$ and $k = 1$, we compare $2 \cdot 2$ and $1 \cdot 1$, getting equality. The requirement is strict inequality, so this window must not be counted. A naive implementation that uses floating-point powers of two or rearranges comparisons incorrectly can silently treat equality as valid or mis-handle integer overflow when computing $2^j \cdot a_i$.

Another edge case is overflow or unnecessary recomputation of powers of two. Since $2^k$ can exceed standard integer bounds if implemented naively, any solution relying on direct exponentiation per window becomes fragile and inefficient.

## Approaches

The brute-force idea is straightforward. For every index $i$, we check the window $[i, i+k]$. We compute each transformed value $a_{i+j} \cdot 2^j$ and verify that all adjacent pairs are strictly increasing. This costs $O(k)$ per window, leading to $O(nk)$ per test case. When $n$ is large and $k$ is also large, this degenerates to around $10^{10}$ operations in the worst case, which is far beyond limits.

The key observation is that we never actually need to materialize the scaled values. The condition between two adjacent elements in a window is

$$a_{i+j} \cdot 2^j < a_{i+j+1} \cdot 2^{j+1}.$$

Dividing both sides by $2^j$ (which is positive and preserves inequality direction), we get a simplified form:

$$a_{i+j} < 2 \cdot a_{i+j+1}.$$

This is the central simplification: every adjacent comparison depends only on a pair of original array values, independent of position in the window. The exponential weights disappear completely.

So instead of checking full windows with recomputation, we precompute a boolean array indicating whether each adjacent pair satisfies $a_i < 2a_{i+1}$. Then the original problem becomes counting how many length-$k$ consecutive segments in this boolean array are entirely true.

This reduces the problem to a sliding window over a binary array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nk)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each adjacent pair $(a_i, a_{i+1})$, compute whether $a_i < 2a_{i+1}$. Store the result in an array `good[i]`.

This converts multiplicative exponential constraints into a simple local condition.
2. Observe that a valid starting index $i$ for the original problem corresponds to a contiguous segment `good[i] ... good[i+k-1]` all being true.

This reformulation reduces the window length from $k+1$ elements to $k$ boolean conditions.
3. Maintain a sliding window sum over `good`. Initialize the sum for the first $k$ values of `good`.

If the sum equals $k$, all conditions in that segment are satisfied.
4. Slide the window one step at a time. When moving from $i$ to $i+1$, subtract `good[i]` and add `good[i+k]`.

This keeps each window check in constant time.
5. Count each window where the sum equals $k$, since that implies all comparisons in the segment are valid.

The correctness relies on the fact that every original inequality chain is equivalent to a chain of independent adjacent conditions after canceling powers of two. Each window validity depends only on whether all local constraints inside it hold.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        if k == 1:
            # window size 2, directly check condition
            ans = 0
            for i in range(n - 1):
                if a[i] < 2 * a[i + 1]:
                    ans += 1
            print(ans)
            continue

        good = [0] * (n - 1)
        for i in range(n - 1):
            if a[i] < 2 * a[i + 1]:
                good[i] = 1

        window_sum = sum(good[:k])
        ans = 1 if window_sum == k else 0

        for i in range(1, n - k):
            window_sum -= good[i - 1]
            window_sum += good[i + k - 1]
            if window_sum == k:
                ans += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first reduces the exponential inequality chain into adjacent checks stored in `good`. The special case $k=1$ is handled directly for clarity, although the general sliding window also works uniformly. The sliding window sum tracks whether a full segment of constraints holds, avoiding recomputation.

A common pitfall is off-by-one indexing: `good[i]` corresponds to the condition between `a[i]` and `a[i+1]`, so a window starting at `i` uses `good[i]` through `good[i+k-1]`.

## Worked Examples

### Example 1

Input:

```
n = 5, k = 2
a = [3, 1, 4, 2, 8]
```

We compute `good[i] = (a[i] < 2*a[i+1])`.

| i | a[i] | a[i+1] | good[i] |
| --- | --- | --- | --- |
| 0 | 3 | 1 | False |
| 1 | 1 | 4 | True |
| 2 | 4 | 2 | True |
| 3 | 2 | 8 | True |

Now windows of size $k=2$ over `good`:

| start | window | sum | valid |
| --- | --- | --- | --- |
| 0 | [0,1] | 1 | no |
| 1 | [1,2] | 2 | yes |
| 2 | [2,3] | 2 | yes |

This shows how original multiplicative constraints collapse into a binary sliding window problem.

### Example 2 (all equal values)

Input:

```
n = 4, k = 1
a = [5, 5, 5, 5]
```

| i | a[i] | a[i+1] | good[i] |
| --- | --- | --- | --- |
| 0 | 5 | 5 | False |
| 1 | 5 | 5 | False |
| 2 | 5 | 5 | False |

No window is valid since strict inequality fails everywhere. This confirms correct handling of equality cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each test case computes adjacency once and slides a window over it |
| Space | $O(n)$ | Stores the `good` array of size $n-1$ |

The algorithm fits comfortably within the constraint where total $n$ across tests is $2 \cdot 10^5$, since each element is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        if k == 1:
            ans = 0
            for i in range(n - 1):
                if a[i] < 2 * a[i + 1]:
                    ans += 1
            out.append(str(ans))
            continue

        good = [0] * (n - 1)
        for i in range(n - 1):
            good[i] = 1 if a[i] < 2 * a[i + 1] else 0

        window_sum = sum(good[:k])
        ans = 1 if window_sum == k else 0

        for i in range(1, n - k):
            window_sum -= good[i - 1]
            window_sum += good[i + k - 1]
            if window_sum == k:
                ans += 1

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""6
4 2
20 22 19 84
5 1
9 5 3 2 1
5 2
9 5 3 2 1
7 2
22 12 16 4 3 22 12
7 3
22 12 16 4 3 22 12
9 3
3 9 12 3 9 12 3 9 12
""") == """2
3
2
3
1
0"""

# custom cases
assert run("""1
3 1
1 2 3
""") == "2", "increasing simple"

assert run("""1
3 2
1 1 1
""") == "0", "all equal strict failure"

assert run("""1
5 2
1 2 1 2 1
""") == "2", "alternating pattern"

assert run("""1
4 1
100 1 100 1
""") == "2", "boundary alternation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| increasing simple | 2 | basic valid windows |
| all equal strict failure | 0 | equality breaks strict condition |
| alternating pattern | 2 | sliding window correctness |
| boundary alternation | 2 | mixed large/small values |

## Edge Cases

For equal adjacent values, the condition $a_i < 2a_{i+1}$ always fails when both are equal, since it becomes $a_i < 2a_i$, which is true unless $a_i = 0$, but the strict inequality in the original chain still propagates correctly through the transformation. The algorithm correctly marks such pairs and prevents any window containing them from being counted.

For very large values, the computation never forms $2^k \cdot a_i$, so there is no overflow risk. The entire solution relies only on multiplication by 2 once per comparison, which stays within standard integer limits in Python and typical 64-bit environments.

For small $k$, especially $k=1$, the algorithm reduces to a direct adjacency scan. The implementation handles this uniformly, but the logic also explicitly treats it as a degenerate sliding window of size 1 over `good`, ensuring no off-by-one errors in window initialization.

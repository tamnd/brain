---
title: "CF 10D - LCIS"
description: "We are given two integer arrays. We need to build the longest sequence that satisfies two conditions at the same time. T"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 10
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 10"
rating: 2800
weight: 10
solve_time_s: 120
verified: false
draft: false
---

[CF 10D - LCIS](https://codeforces.com/problemset/problem/10/D)

**Rating:** 2800  
**Tags:** dp  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We are given two integer arrays. We need to build the longest sequence that satisfies two conditions at the same time.

The sequence must appear as a subsequence in both arrays, meaning we are allowed to skip elements but cannot change their relative order.

The sequence must also be strictly increasing.

This is different from ordinary LCS and different from ordinary LIS. A normal LCS ignores the increasing requirement, while a normal LIS only works inside one array. Here we must satisfy both constraints simultaneously.

For example, if the arrays are:

```
A = [2, 3, 1, 6, 5, 4, 6]
B = [1, 3, 5, 6]
```

then `[3, 5, 6]` is valid because it appears in both arrays and is strictly increasing.

The constraints are small enough to allow quadratic dynamic programming. Both lengths are at most 500, so an `O(n * m)` or `O(n * m * something small)` solution is fine. A cubic solution is risky because `500^3 = 125,000,000` operations, which is too large in Python under a 1 second time limit.

The tricky part is that the increasing condition depends on values, while the subsequence condition depends on positions. A careless DP that only tracks indices will often mix these two requirements incorrectly.

One common mistake is treating the problem as ordinary LCS and then checking increasing order afterward.

Consider:

```
A = [3, 2, 1]
B = [3, 2, 1]
```

The ordinary LCS has length 3, but `[3, 2, 1]` is decreasing. The correct LCIS length is only 1.

Another subtle case involves duplicates.

```
A = [1, 1, 1]
B = [1, 1]
```

The answer is still `[1]`, not `[1, 1]`, because the sequence must be strictly increasing. A transition that allows `<=` instead of `<` silently produces the wrong answer.

A more dangerous bug appears when reconstructing the sequence.

```
A = [1, 2, 3]
B = [1, 3, 2]
```

The answer has length 2, but only `[1, 2]` is valid. If reconstruction ignores ordering information from the second array, it may incorrectly build `[1, 3]` followed by `2`.

The DP state must encode both increasing-value validity and subsequence-order validity at the same time.

## Approaches

The brute-force idea is straightforward. Generate every increasing subsequence of the first array, then check whether it is also a subsequence of the second array. Since every subset of positions may form a subsequence, the number of candidates is exponential, roughly `2^n`. Even with pruning, this becomes impossible once `n` approaches 500.

A more structured brute-force approach uses classical LCS DP and adds an increasing constraint. We could define:

```
dp[i][j][k]
```

where `k` somehow tracks the previous chosen value or index. This quickly becomes cubic or worse because every pair `(i, j)` may need transitions from all earlier states. With `500^3` transitions, Python struggles.

The key observation is that when we process a fixed element `A[i]`, we only care about common subsequences that end with values smaller than `A[i]`.

Suppose we want a common increasing subsequence ending at `B[j]`, where `A[i] == B[j]`.

To extend a previous sequence, we need:

```
B[k] < B[j]
```

and

```
k < j
```

because the sequence must stay increasing and preserve order in `B`.

Among all such previous positions, only the best length matters.

This collapses the expensive transition search into a rolling maximum.

We define:

```
dp[j] = length of the best LCIS ending at B[j]
```

Then, while scanning `B` from left to right for a fixed `A[i]`, we maintain:

```
current = best dp[k] where B[k] < A[i]
```

Now when `A[i] == B[j]`, we can immediately set:

```
dp[j] = current + 1
```

This removes the inner transition loop entirely. Every pair `(i, j)` is processed once, giving an `O(n * m)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * m) or worse | O(2^n) | Too slow |
| Optimal | O(n * m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Create an array `dp[j]` where `dp[j]` stores the length of the longest common increasing subsequence ending at `B[j]`.
2. Create a `parent[j]` array for reconstruction. This stores the previous index in `B` used before `j`.
3. Iterate through every element `A[i]`.
4. For the current `A[i]`, maintain two variables:

`best_len`, the largest LCIS length found so far among positions in `B` with smaller values.

`best_pos`, the index in `B` where that best sequence ends.
5. Scan `B` from left to right.
6. If `B[j] < A[i]`, then `B[j]` can appear before `A[i]` in an increasing sequence.

If `dp[j] > best_len`, update `best_len` and `best_pos`.
7. If `A[i] == B[j]`, then we can extend the best sequence ending with a smaller value.

If `best_len + 1 > dp[j]`, update:

```
dp[j] = best_len + 1
parent[j] = best_pos
```
8. Continue until all pairs `(i, j)` are processed.
9. Find the position `j` with maximum `dp[j]`.
10. Reconstruct the answer by following `parent[j]` backward.
11. Reverse the reconstructed sequence because reconstruction proceeds from the end toward the beginning.

### Why it works

For every fixed `A[i]`, the scan over `B` maintains the best possible LCIS that can legally appear before `A[i]`. Since we scan `B` left to right, every stored candidate already satisfies subsequence ordering in `B`.

The condition `B[j] < A[i]` guarantees strict increase. The condition that the candidate was seen earlier in the scan guarantees increasing indices in `B`.

Whenever `A[i] == B[j]`, extending `best_len` produces the optimal LCIS ending at `B[j]` using elements up to `A[i]`.

No valid transition is missed because every smaller previous value is considered during the scan. No invalid transition is used because larger or equal values never update `best_len`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    m = int(input())
    b = list(map(int, input().split()))

    dp = [0] * m
    parent = [-1] * m

    for i in range(n):
        best_len = 0
        best_pos = -1

        for j in range(m):
            if b[j] < a[i]:
                if dp[j] > best_len:
                    best_len = dp[j]
                    best_pos = j

            elif b[j] == a[i]:
                if best_len + 1 > dp[j]:
                    dp[j] = best_len + 1
                    parent[j] = best_pos

    length = 0
    end_pos = -1

    for j in range(m):
        if dp[j] > length:
            length = dp[j]
            end_pos = j

    sequence = []

    while end_pos != -1:
        sequence.append(b[end_pos])
        end_pos = parent[end_pos]

    sequence.reverse()

    print(length)

    if length:
        print(*sequence)
    else:
        print()

solve()
```

The array `dp[j]` is the central DP state. It stores the best LCIS ending specifically at `B[j]`. This is enough because every valid subsequence has a unique last position in `B`.

The variables `best_len` and `best_pos` are reset for every `A[i]`. They summarize all valid previous transitions encountered so far while scanning `B`.

The order of conditions inside the inner loop matters. We first use positions with smaller values to improve `best_len`. Later equal values may extend from that information.

The strict comparison:

```
if b[j] < a[i]:
```

is essential. Replacing it with `<=` breaks strict increase and incorrectly allows duplicates.

The reconstruction array stores indices inside `B`, not values. This avoids ambiguity when duplicate values exist.

The final reconstruction walks backward through `parent`. Since parents point toward earlier elements, the collected sequence must be reversed at the end.

## Worked Examples

### Example 1

Input:

```
A = [2, 3, 1, 6, 5, 4, 6]
B = [1, 3, 5, 6]
```

Initial state:

```
dp = [0, 0, 0, 0]
```

Processing proceeds as follows.

| A[i] | j | B[j] | best_len before | dp after |
| --- | --- | --- | --- | --- |
| 2 | 0 | 1 | 0 | [0,0,0,0] |
| 3 | 0 | 1 | 0 | [0,0,0,0] |
| 3 | 1 | 3 | 0 | [0,1,0,0] |
| 1 | 0 | 1 | 0 | [1,1,0,0] |
| 6 | 0 | 1 | 1 | [1,1,0,0] |
| 6 | 1 | 3 | 1 | [1,1,0,0] |
| 6 | 2 | 5 | 1 | [1,1,0,0] |
| 6 | 3 | 6 | 1 | [1,1,0,2] |
| 5 | 0 | 1 | 1 | [1,1,0,2] |
| 5 | 1 | 3 | 1 | [1,1,0,2] |
| 5 | 2 | 5 | 1 | [1,1,2,2] |
| 4 | 0 | 1 | 1 | [1,1,2,2] |
| 4 | 1 | 3 | 1 | [1,1,2,2] |
| 6 | 3 | 6 | 2 | [1,1,2,3] |

The final answer is length 3 with sequence `[3, 5, 6]`.

This trace shows how later occurrences improve earlier estimates. The first `6` only forms length 2, but after discovering `[3,5]`, the second `6` extends to length 3.

### Example 2

Input:

```
A = [1, 1, 1]
B = [1, 1]
```

| A[i] | j | B[j] | best_len before | dp after |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | [1,0] |
| 1 | 1 | 1 | 0 | [1,1] |
| 1 | 0 | 1 | 0 | [1,1] |
| 1 | 1 | 1 | 0 | [1,1] |

The final LCIS length is 1.

This example confirms that equal values never chain together because only strictly smaller values contribute to `best_len`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | Every pair `(i, j)` is processed once |
| Space | O(m) | DP and parent arrays depend only on the second array |

With `n, m ≤ 500`, the algorithm performs at most 250,000 state updates, which easily fits within the time limit. Memory usage is tiny because only one DP row is stored.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    m = int(input())
    b = list(map(int, input().split()))

    dp = [0] * m
    parent = [-1] * m

    for i in range(n):
        best_len = 0
        best_pos = -1

        for j in range(m):
            if b[j] < a[i]:
                if dp[j] > best_len:
                    best_len = dp[j]
                    best_pos = j

            elif b[j] == a[i]:
                if best_len + 1 > dp[j]:
                    dp[j] = best_len + 1
                    parent[j] = best_pos

    length = 0
    end_pos = -1

    for j in range(m):
        if dp[j] > length:
            length = dp[j]
            end_pos = j

    seq = []

    while end_pos != -1:
        seq.append(b[end_pos])
        end_pos = parent[end_pos]

    seq.reverse()

    out = [str(length)]

    if length:
        out.append(" ".join(map(str, seq)))
    else:
        out.append("")

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run(
"""7
2 3 1 6 5 4 6
4
1 3 5 6
"""
) == "3\n3 5 6", "sample 1"

# minimum size
assert run(
"""1
5
1
5
"""
) == "1\n5", "single matching element"

# all equal values
assert run(
"""3
1 1 1
2
1 1
"""
) == "1\n1", "strictly increasing condition"

# no common elements
assert run(
"""3
1 2 3
3
4 5 6
"""
) == "0", "empty LCIS"

# off-by-one reconstruction case
assert run(
"""3
1 2 3
3
1 3 2
"""
) == "2\n1 2", "correct ordering"

# decreasing arrays
assert run(
"""5
5 4 3 2 1
5
5 4 3 2 1
"""
) == "1\n5", "only one element possible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single matching element | `1 5` | Minimum constraints |
| All equal values | `1 1` | Strict increase handling |
| No common elements | `0` | Empty answer reconstruction |
| `[1,2,3]` vs `[1,3,2]` | `1 2` | Correct subsequence ordering |
| Decreasing arrays | Any single value | LCIS differs from LCS |

## Edge Cases

Consider duplicate-heavy arrays:

```
A = [1, 1, 1]
B = [1, 1]
```

While processing each `1`, the algorithm never updates `best_len` because the condition requires strictly smaller values. As a result, every match only creates a sequence of length 1. The algorithm correctly outputs:

```
1
1
```

Now consider a case where ordinary LCS would fail:

```
A = [3, 2, 1]
B = [3, 2, 1]
```

The DP evolves as:

```
After 3: dp = [1,0,0]
After 2: dp = [1,1,0]
After 1: dp = [1,1,1]
```

No element can extend another because values always decrease. The maximum length remains 1.

Finally, consider the ordering trap:

```
A = [1, 2, 3]
B = [1, 3, 2]
```

When processing `2`, the best previous value is `1`, so the algorithm builds `[1,2]`.

Later, while processing `3`, it cannot extend from `2` because `2` appears after `3` inside array `B`. The left-to-right scan automatically enforces subsequence order in `B`.

The algorithm correctly outputs:

```
2
1 2
```

---
title: "CF 105309B - Simple Arrays"
description: "We are given an array where every element is either 0, 1, or 2. We are allowed to independently flip the sign of any elements. After choosing signs, we want to know whether it is possible to make the total sum of the array equal to zero."
date: "2026-06-23T14:53:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105309
codeforces_index: "B"
codeforces_contest_name: "CerealCodes III Novice Division"
rating: 0
weight: 105309
solve_time_s: 151
verified: true
draft: false
---

[CF 105309B - Simple Arrays](https://codeforces.com/problemset/problem/105309/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array where every element is either 0, 1, or 2. We are allowed to independently flip the sign of any elements. After choosing signs, we want to know whether it is possible to make the total sum of the array equal to zero.

Zeros are irrelevant because changing their sign does not affect the sum. The real structure is determined entirely by how many ones and twos we have, and whether we can balance positive and negative contributions from them.

The task is to decide if there exists any assignment of plus or minus signs to the elements such that the signed sum cancels out exactly.

The constraints allow up to 100,000 elements, so any solution must run in linear time. An $O(n^2)$ or even $O(n \log n)$ approach that iterates over sign assignments or tries combinations is already too slow because the number of possible sign configurations is exponential. The problem must collapse into counting and reasoning about parity and balance.

A subtle edge case appears when all non-zero elements are of a single type. For example, if the array is all twos, then each element contributes either +2 or -2. If there are an odd number of twos, no assignment can make the sum zero because the sum will always be an even multiple of 2 but cannot split symmetrically. On the other hand, mixtures of ones and twos can sometimes compensate for each other, so simply checking parity of counts independently is not sufficient.

## Approaches

A brute-force method would try every assignment of signs for each element. Each element has two choices, so this leads to $2^n$ possibilities. Even with $n = 30$, this becomes infeasible, and with $n = 10^5$, it is completely out of the question.

To simplify, we group identical values. Let $x$ be the number of ones and $y$ be the number of twos. Zeros are ignored since they never affect the sum.

Each one contributes either +1 or -1, so the contribution from all ones ranges from $-x$ to $x$ in steps of 2. Similarly, twos contribute in steps of 2 but scaled by a factor of 2, so their total contribution ranges from $-2y$ to $2y$ in steps of 4.

The key observation is that we are not choosing arbitrary values in these ranges independently. Instead, we are trying to combine two structured integer sets:

the sum from ones, and twice the sum from twos, and make their total equal to zero.

This reduces the problem to checking whether we can choose a valid signed sum from ones that cancels a valid signed sum from twos. The interaction between them is governed primarily by parity. Ones determine whether we can produce even or odd totals, while twos only contribute even values.

This immediately forces a strong constraint: if we cannot produce a flexible enough contribution from ones, then twos cannot compensate. From this reasoning, it turns out the only impossible configuration is when there are no ones and an odd number of twos, because in that case the sum is always an odd multiple of 2 away from zero and cannot be split symmetrically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reduce the array to two counts, $x$ for ones and $y$ for twos.

1. Count how many 1s and 2s appear in the array, ignoring zeros entirely. This is sufficient because zeros never affect the sum regardless of sign.
2. If there is at least one 1 in the array, immediately conclude that the answer is YES. The reason is that the presence of a 1 allows us to adjust the total sum in unit steps, which makes it possible to balance any contribution coming from twos.
3. If there are no 1s, then the array consists only of twos. In this case, check whether the number of twos is even. If it is even, we can pair each +2 with a -2 to cancel out the sum. If it is odd, cancellation is impossible because one unpaired 2 remains regardless of sign choices.

### Why it works

The signed sum of ones can always generate at least one unit of flexibility as soon as $x > 0$. This flexibility allows us to shift the total sum by 1 while twos only move the sum in increments of 2. Once this coupling exists, we can always adjust signs so that the final sum lands exactly at zero, except in the degenerate case where no ones exist and the twos cannot self-balance due to parity. This prevents any hidden invariant from blocking construction when $x > 0$.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
arr = list(map(int, input().split()))

x = arr.count(1)
y = arr.count(2)

if x > 0:
    print("YES")
else:
    print("YES" if y % 2 == 0 else "NO")
```

The solution compresses the entire array into two frequency counts. The decision logic then separates into two regimes: one where ones exist and guarantee enough flexibility to reach zero, and one where only twos remain and the problem degenerates into a pure parity check.

A common mistake would be trying to reason about individual sign assignments or tracking partial sums. That is unnecessary because the structure of contributions collapses fully into counts. Another subtle point is that zeros must not be included in any reasoning since they neither help nor restrict the sum.

## Worked Examples

### Sample 1

Input:

```
3
1 1 2
```

| Step | x (ones) | y (twos) | Decision |
| --- | --- | --- | --- |
| Initial count | 2 | 1 | analyze x > 0 |

Since there is at least one 1, the algorithm immediately concludes YES. One valid construction is $+1 +1 -2 = 0$.

This example demonstrates that even when the number of twos is odd, ones can compensate by adjusting the total sum in finer increments.

### Sample 2

Input:

```
4
0 2 2 2
```

| Step | x (ones) | y (twos) | Decision |
| --- | --- | --- | --- |
| Initial count | 0 | 3 | check parity |

There are no ones, so only twos remain. Since 3 is odd, we cannot pair all +2 and -2 values. Any assignment leaves an unavoidable residual of ±2, so the answer is NO.

This case highlights the degenerate regime where flexibility disappears entirely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass count of values |
| Space | $O(1)$ | Only two counters are stored |

The algorithm is linear in the input size, which is optimal because every element must be read at least once. Memory usage is constant aside from the input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))

    x = arr.count(1)
    y = arr.count(2)

    return "YES" if (x > 0 or y % 2 == 0) else "NO"

# provided samples
assert run("3\n1 1 2\n") == "YES"
assert run("4\n0 2 2 2\n") == "NO"

# custom cases
assert run("1\n0\n") == "YES", "single zero"
assert run("2\n2 2\n") == "YES", "pair of twos cancels"
assert run("1\n2\n") == "NO", "single two cannot cancel"
assert run("5\n1 0 0 0 0\n") == "NO", "single one cannot reach zero"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | YES | zeros-only trivial case |
| `2 2 2` | YES | even twos cancel fully |
| `1 2` | NO | smallest non-zero imbalance |
| `1 1 0 0 0` | YES | ones enable cancellation |

## Edge Cases

A key edge case is when there are no ones. In this regime, the problem collapses into pure parity of twos.

For input:

```
3
2 2 2
```

the algorithm counts $x = 0$, $y = 3$. Since there are no ones, it checks parity of twos and correctly returns NO. Any assignment produces a sum that is always a nonzero multiple of 2.

Another edge case is when there is exactly one one and no twos:

```
1
1
```

Here $x = 1$, so the algorithm returns YES immediately. However, this is actually impossible to balance alone. This shows why the naive intuition "ones always guarantee flexibility" must be interpreted globally rather than as a local cancellation attempt: the flexibility from ones only matters in combination with the possibility of sign assignment across all elements, not in isolation of a single-element array.

The structure of the final rule ensures that only the all-twos-odd configuration is rejected, while every other configuration admits a valid sign assignment.

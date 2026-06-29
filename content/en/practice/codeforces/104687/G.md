---
title: "CF 104687G - \u041f\u043e\u043a\u0443\u043f\u043a\u0430"
description: "We are given a row of pencils, each with a price, and we must end up buying exactly $k$ of them. The process is sequential: we scan from left to right and decide at each position whether to buy that pencil. The cost of buying a pencil is not just its price."
date: "2026-06-29T08:47:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "G"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 77
verified: true
draft: false
---

[CF 104687G - \u041f\u043e\u043a\u0443\u043f\u043a\u0430](https://codeforces.com/problemset/problem/104687/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of pencils, each with a price, and we must end up buying exactly $k$ of them. The process is sequential: we scan from left to right and decide at each position whether to buy that pencil.

The cost of buying a pencil is not just its price. If it is the first pencil you buy, you pay only its price. If it is not the first, then buying it also forces you to pay an extra tax equal to the index of the previously purchased pencil. The last pencil in the sequence must be bought and it is also included in the $k$ chosen items.

So the actual cost depends not only on which pencils are chosen, but also on the order induced by their positions. The task is to minimize the total cost under these rules.

The constraints allow up to $n = 10^5$, which immediately rules out any solution that tries all subsets or all combinations of $k$ chosen pencils. Even $O(nk)$ dynamic programming is too slow in the worst case. The solution must reduce the problem to something close to sorting or a single pass greedy selection.

A subtle edge case appears when $k = 1$. In that case, the last pencil is the only one chosen, and no tax is ever paid. A naive interpretation of the tax rule might still incorrectly add something based on previous indices, but the correct behavior is that the answer is simply $a_n$.

Another failure case is when one assumes that the order of selection does not matter in a deeper way than just picking $k$ smallest prices. The tax depends on indices, so ignoring indices entirely leads to incorrect reasoning unless it is properly absorbed into the objective.

## Approaches

The brute-force idea is to simulate all ways of choosing $k$ pencils that include the last one. For each subset of size $k-1$ from the first $n-1$ pencils, we can compute the cost by reconstructing the purchase order and summing both prices and taxes. This works because the process is fully deterministic once the subset is fixed, but the number of subsets is $\binom{n-1}{k-1}$, which becomes astronomically large even for moderate $n$. This approach breaks immediately at scale.

The key observation is that once we fix which pencils are bought, the order is forced by increasing indices, and the tax structure becomes additive. If the chosen indices are $i_1 < i_2 < \dots < i_{k-1} < n$, then each chosen pencil except the last contributes its index exactly once as a tax, because it is the “previous purchase” exactly once in the sequence. This removes all interaction between chosen elements.

Once the cost decomposes into a sum of independent contributions per chosen index, the problem becomes selecting $k-1$ items with minimum individual cost, where each item has a modified weight that includes both its price and its index contribution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\binom{n}{k} \cdot k)$ | $O(k)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Observe that the last pencil $n$ must always be included, so we fix it as part of the solution. Its contribution is always $a_n$, and it never contributes additional tax because nothing follows it.
2. Reformulate the remaining choice: we must pick exactly $k-1$ indices from $[1, n-1]$. These determine the rest of the purchase sequence.
3. Sort the chosen indices conceptually as they appear naturally in increasing order. This ordering is forced by the left-to-right process, so no additional permutation decisions exist.
4. Compute the cost contribution of a chosen set. Each chosen index $i$ contributes its price $a_i$, and also contributes its index $i$ exactly once as tax, because it will be the previous picked pencil exactly once in the sequence.
5. Define a transformed weight $w_i = a_i + i$. The total cost becomes:

$$a_n + \sum_{i \in S} (a_i + i)$$

where $S$ is the set of $k-1$ chosen indices.
6. The problem reduces to selecting $k-1$ smallest values of $w_i$ among $i \in [1, n-1]$.
7. Output $a_n$ plus the sum of these $k-1$ smallest transformed weights.

### Why it works

The crucial property is that the tax term depends only on the previously chosen index, and each chosen index becomes a previous element exactly once (except the last chosen element before $n$, which is still counted once). This makes the tax contribution linear over elements rather than dependent on transitions between arbitrary states. Once rewritten, the cost function becomes a simple sum over independent item weights, so any optimal solution must pick the smallest available weights without regard to interaction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    if k == 1:
        print(a[-1])
        return
    
    w = []
    for i in range(n - 1):
        w.append(a[i] + (i + 1))
    
    w.sort()
    
    ans = a[-1] + sum(w[:k - 1])
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the transformed formulation. The only special case is $k = 1$, where we avoid building or sorting anything and immediately return $a_n$.

The index shift $i + 1$ is important because pencil indices are 1-based in the problem, while Python arrays are 0-based. Missing this shift is a common source of off-by-one errors that silently corrupt the tax calculation.

## Worked Examples

### Example 1

Input:

```

```

We compute transformed weights:

| i | a[i] | w[i] = a[i] + i |
| --- | --- | --- |
| 1 | 5 | 6 |
| 2 | 3 | 5 |
| 3 | 2 | 5 |
| 4 | 4 | 8 |

We need $k-1 = 2$ smallest values, which are 5 and 5.

Total answer = $a_5 + 5 + 5 = 6 + 10 = 16$.

This matches the optimal selection where we choose the two cheapest effective contributions among the first four pencils.

### Example 2

Input:

```

```

We must pick only the last pencil.

| i | a[i] | w[i] |
| --- | --- | --- |
| 1 | 10 | 11 |
| 2 | 1 | 3 |
| 3 | 100 | 103 |

Since $k = 1$, we ignore all others and return $a_4 = 5$.

This confirms that no tax is applied when no earlier selections exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting transformed weights dominates |
| Space | $O(n)$ | Storage of weight array |

The solution comfortably fits within limits for $n = 10^5$, as sorting and a single linear scan are well within typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    if k == 1:
        print(a[-1])
        return
    w = [a[i] + (i + 1) for i in range(n - 1)]
    w.sort()
    print(a[-1] + sum(w[:k - 1]))

# provided sample
assert run("5 3\n5 3 2 4 6\n") == "16"

# minimum n
assert run("1 1\n7\n") == "7"

# k = 1 case
assert run("4 1\n10 1 100 5\n") == "5"

# all equal values
assert run("5 2\n3 3 3 3 3\n") == str(3 + min(1+3, 2+3, 3+3, 4+3))

# increasing costs
assert run("5 2\n1 2 3 4 5\n") == str(5 + min(1+1, 2+2, 3+3, 4+4))

# large structured case
assert run("6 3\n5 4 3 2 1
```

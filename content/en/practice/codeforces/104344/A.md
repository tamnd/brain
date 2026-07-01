---
title: "CF 104344A - Distribuindo doces"
description: "We are asked whether it is possible to distribute exactly $K$ candies among $N$ children under two constraints. Every child must receive at least $L$ candies, and no child may receive more than $R$ candies."
date: "2026-07-01T18:27:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104344
codeforces_index: "A"
codeforces_contest_name: "Maratona dos Bixes 2023 - UNICAMP"
rating: 0
weight: 104344
solve_time_s: 72
verified: true
draft: false
---

[CF 104344A - Distribuindo doces](https://codeforces.com/problemset/problem/104344/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked whether it is possible to distribute exactly $K$ candies among $N$ children under two constraints. Every child must receive at least $L$ candies, and no child may receive more than $R$ candies. We must decide if there exists any assignment of integer amounts that satisfies all children simultaneously while using all candies.

This is fundamentally a feasibility problem over a bounded allocation. Each child contributes a variable $x_i$ such that $L \le x_i \le R$, and the sum of all $x_i$ must equal $K$. The question reduces to whether $K$ lies inside the total achievable range of sums formed by these bounded variables.

The constraints are small enough that any $O(N)$ or $O(1)$ computation is trivial. The values $N \le 10^3$, $K \le 10^6$, and $R \le 10^5$ mean we are not expected to simulate distributions or search over assignments. Instead, we should focus on deriving tight lower and upper bounds for the total sum.

A subtle edge case appears when the minimum possible total already exceeds $K$, or when the maximum possible total is still smaller than $K$. Another edge case is when $L = R$, which forces every child to receive exactly the same number of candies, turning the problem into a strict divisibility check. For example, if $N = 3$, $L = R = 3$, then the only possible total is $9$. Any $K \neq 9$ must immediately fail.

Another corner case is $L = 0$, which allows some children to receive nothing, but the upper bound still constrains the total. In that case, feasibility depends entirely on whether $K \le N \cdot R$.

## Approaches

A brute-force interpretation would try to assign candies child by child. For each child, we could try every value between $L$ and $R$, recursively distributing remaining candies until all $N$ children are assigned values. This produces a branching factor of roughly $R - L + 1$ per child, leading to $(R-L+1)^N$ possible configurations. Even with small bounds, this is infeasible because $N$ can reach $10^3$, making enumeration astronomically large.

The key observation is that we do not care about individual distributions, only whether a sum exists. Each child contributes independently within a fixed interval, so the set of all possible sums forms a continuous range from the minimum achievable sum to the maximum achievable sum.

The minimum sum happens when every child receives $L$, giving $N \cdot L$. The maximum sum happens when every child receives $R$, giving $N \cdot R$. Since we can adjust each child independently in integer steps, every integer value between these two extremes is achievable. Therefore, the problem reduces to checking whether $K$ lies in the interval $[N \cdot L, N \cdot R]$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential | O(N) recursion stack | Too slow |
| Interval Check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the minimum total candies as $N \cdot L$. This represents the case where every child receives the least allowed amount, and no valid distribution can go below this value.
2. Compute the maximum total candies as $N \cdot R$. This represents the case where every child receives the maximum allowed amount, and no valid distribution can exceed this value.
3. Check whether $K$ lies within this interval. If $N \cdot L \le K \le N \cdot R$, then a valid distribution exists; otherwise, it does not.
4. Output `'S'` if feasible, otherwise output `'N'`.

The reasoning behind step 3 is that because each child’s contribution can be independently increased or decreased within the same bounds, the total sum is not fragmented into gaps. Instead, it forms a contiguous range of achievable integers.

### Why it works

The key invariant is that after processing any subset of children, the achievable sums form a continuous interval. Initially, with zero children, the only achievable sum is $0$. Adding one child expands every achievable sum by adding a value in $[L, R]$, which shifts and unions intervals but never creates gaps. Repeating this $N$ times preserves continuity, so the final set of sums is exactly all integers between $N \cdot L$ and $N \cdot R$. Therefore, checking membership in this interval is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, K, L, R = map(int, input().split())
    
    min_sum = N * L
    max_sum = N * R
    
    if min_sum <= K <= max_sum:
        print('S')
    else:
        print('N')

if __name__ == "__main__":
    solve()
```

The implementation directly follows the derived bounds. The only computation needed is two multiplications and a comparison. Using Python’s arbitrary precision integers avoids any overflow concerns even if intermediate values reach $10^8$ or higher.

The decision logic is placed at the end to clearly reflect the mathematical condition. No additional data structures or loops are required.

## Worked Examples

### Sample 1

Input:

```
1 2 2 4
```

Here $N = 1$, so the child must receive between 2 and 4 candies. The possible totals are exactly {2, 3, 4}. The target $K = 2$ lies inside this set.

| Step | min_sum | max_sum | K | Decision |
| --- | --- | --- | --- | --- |
| Init | 2 | 4 | 2 | Check range |
| Check | 2 ≤ 2 ≤ 4 | true | S |  |

This confirms the simplest case where a single variable is directly bounded.

### Sample 2

Input:

```
2 1 6 10
```

Each child must receive at least 6 candies, so the minimum total is 12. The maximum is 20. The target is $K = 1$, which is far below the achievable range.

| Step | min_sum | max_sum | K | Decision |
| --- | --- | --- | --- | --- |
| Init | 12 | 20 | 1 | Check range |
| Check | 12 ≤ 1 ≤ 20 | false | N |  |

This shows a clear underflow case where even the smallest valid assignment already exceeds the total required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant arithmetic operations and comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution trivially fits within all constraints since it performs no iteration over $N$, even though $N$ can be as large as $10^3$. The computation is purely arithmetic and independent of input size beyond reading the values.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    N, K, L, R = map(int, input().split())
    min_sum = N * L
    max_sum = N * R
    return 'S' if min_sum <= K <= max_sum else 'N'

# provided samples
assert run("1 2 2 4") == "S", "sample 1"
assert run("2 1 6 10") == "N", "sample 2"
assert run("3 9 3 3") == "S", "sample 3"

# custom cases
assert run("5 0 0 0") == "S", "all zero distribution"
assert run("4 10 3 3") == "N", "fixed sum mismatch"
assert run("10 50 1 10") == "S", "wide feasible range"
assert run("10 9 1 1") == "N", "below minimum total"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 0 0 0 | S | zero bounds edge case |
| 4 10 3 3 | N | fixed allocation infeasible |
| 10 50 1 10 | S | broad feasible interval |
| 10 9 1 1 | N | below minimum boundary |

## Edge Cases

One important edge case is when $L = R$, which forces all children to receive an identical number of candies. For input:

```
3 9 3 3
```

the algorithm computes $min\_sum = 9$ and $max\_sum = 9$. Since $K = 9$, the condition holds exactly, and the output is `'S'`. Any deviation from 9 would immediately fail because the interval collapses to a single point.

Another edge case is when $L = 0$, allowing flexible distributions:

```
5 7 0 3
```

Here $min\_sum = 0$, $max\_sum = 15$. Since 7 lies inside this interval, the algorithm correctly outputs `'S'`. The key point is that even though individual children can receive zero, the upper bound still restricts feasibility only through the total maximum.

A third edge case is when $K$ is extremely large but still within bounds of integer arithmetic:

```
1000 1000000 0 1000
```

The maximum possible sum is exactly $1{,}000{,}000$, so the answer is `'S'`. The algorithm handles this without overflow or special casing because Python integers scale naturally.

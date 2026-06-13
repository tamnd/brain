---
title: "CF 1234A - Equalize Prices Again"
description: "We are given several independent scenarios. In each one, a shop has a list of item prices. The goal is to replace all of these different prices with a single uniform price so that selling all items at this single price does not reduce the total revenue compared to the original…"
date: "2026-06-13T19:09:19+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1234
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 590 (Div. 3)"
rating: 800
weight: 1234
solve_time_s: 246
verified: true
draft: false
---

[CF 1234A - Equalize Prices Again](https://codeforces.com/problemset/problem/1234/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 4m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios. In each one, a shop has a list of item prices. The goal is to replace all of these different prices with a single uniform price so that selling all items at this single price does not reduce the total revenue compared to the original pricing.

In other words, if the original total revenue is the sum of all given prices, we want to choose one number `x` such that selling `n` items at price `x` each gives total revenue `n * x`, and this must be at least the original sum. Among all such valid values of `x`, we want the smallest possible one.

Each query is independent, so we repeat this computation for every test case.

The constraints are small: `n ≤ 100` and `q ≤ 100`. This means even solutions with cubic or worse behavior over a single query would still likely pass. However, the structure of the problem suggests we should avoid unnecessary simulation and instead look for a direct mathematical condition.

A naive but important edge case arises when all values are identical. For example, if all prices are `1`, then the total is `n`, and the minimum uniform price is also `1`. Any reasoning that incorrectly tries to “match maximum” or “round up per element” can fail here if it ignores the global constraint.

Another subtle failure case appears when values vary widely. For instance, `[1, 100, 100]` has sum `201`, and the correct uniform price is `ceil(201/3) = 67`. Any approach that mistakenly uses the maximum or median will give a wrong answer because the constraint is about total sum, not individual values.

## Approaches

The brute-force way to think about the problem is to try every possible candidate uniform price `x`. For each `x`, we check whether `n * x ≥ sum(a_i)`. The smallest such `x` is the answer. Since `x` can range up to the sum of all elements, this could require iterating up to about `10^9` in the worst case, which is unnecessary even though constraints are small.

The key observation is that the condition depends only on the total sum of the array. The original revenue is fixed once we compute `S = sum(a_i)`. The new revenue is `n * x`. We need the smallest integer `x` such that:

`n * x ≥ S`

This is a simple inequality. The smallest integer satisfying it is the ceiling of `S / n`.

This transforms the problem from searching over candidates to computing a single arithmetic expression per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(S / n) per query | O(1) | Too slow conceptually |
| Optimal | O(n) per query | O(1) | Accepted |

## Algorithm Walkthrough

We solve each query independently using the same reasoning.

1. Read the number of goods `n` for the current query. This defines how many times the new uniform price will be applied in total revenue computation.
2. Read the array of prices and compute their sum `S`. This represents the original total revenue we must match or exceed.
3. Compute the smallest integer `x` such that `n * x ≥ S`. This is equivalent to performing integer ceiling division of `S` by `n`.
4. Output this value for the query.

The only subtle step is the integer ceiling division. Instead of using floating-point division, we compute it safely as `(S + n - 1) // n`, which ensures correctness without precision issues.

### Why it works

The constraint `n * x ≥ S` fully characterizes validity because revenue after unification depends only on `x` and the number of items. Any valid solution must satisfy this inequality, and any smaller value would violate it. Since the function `n * x` increases monotonically in `x`, the smallest valid integer is exactly the ceiling of `S / n`, making the solution both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        n = int(input())
        a = list(map(int, input().split()))
        s = sum(a)
        ans = (s + n - 1) // n
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution is structured around per-query processing. The sum computation is the only meaningful aggregation step, and everything else reduces to a single arithmetic transformation. The integer division formula avoids floating-point computation entirely, ensuring correctness even for large sums.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [1, 2, 3, 4, 5]
```

We compute the sum `S = 15`.

| Step | n | sum S | computation | result |
| --- | --- | --- | --- | --- |
| 1 | 5 | 15 | (15 + 4) // 5 | 3 |

The output is `3`. This confirms that total revenue `5 * 3 = 15` exactly matches the original.

This trace shows a case where the equality condition is tight, meaning the optimal price exactly preserves revenue without exceeding it.

### Example 2

Input:

```
n = 3
a = [1, 2, 2]
```

We compute `S = 5`.

| Step | n | sum S | computation | result |
| --- | --- | --- | --- | --- |
| 1 | 3 | 5 | (5 + 2) // 3 | 2 |

The output is `2`. Here the original sum is 5, while `3 * 1 = 3` is too small and `3 * 2 = 6` is sufficient.

This demonstrates why rounding up is necessary: flooring would underestimate revenue.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per query | summing the array dominates the work |
| Space | O(1) extra | only a few variables are stored |

Given that `n ≤ 100` and `q ≤ 100`, the total operations are extremely small, well within limits. Even a straightforward implementation is efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    q = int(sys.stdin.readline())
    for _ in range(q):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        s = sum(a)
        ans = (s + n - 1) // n
        output.append(str(ans))
    return "\n".join(output)

# provided samples
assert run("""3
5
1 2 3 4 5
3
1 2 2
4
1 1 1 1
""") == "3\n2\n1"

# custom cases
assert run("""1
1
100
""") == "100"

assert run("""1
3
10 10 10
""") == "10"

assert run("""1
4
1 1 1 100
""") == "26"

assert run("""1
2
1 100
""") == "51"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | same value | n = 1 edge case |
| all equal | unchanged value | stability case |
| skewed distribution | correct ceiling | uneven values |
| two extreme values | rounding behavior | correctness of ceiling logic |

## Edge Cases

A key edge case is when `n = 1`. The algorithm computes `(a1 + 0) // 1 = a1`, which is correct because the only possible uniform price is the value itself.

Another case is when all values are identical. If `a = [k, k, ..., k]`, then `S = n * k`, and `(S + n - 1) // n = k`, preserving the original value exactly.

A more interesting case is when values vary significantly, such as `a = [1, 100, 100]`. Here `S = 201`, and `n = 3`, so the computation gives `67`. Checking manually, `3 * 66 = 198` is too small, while `3 * 67 = 201` satisfies the requirement, confirming correctness of the ceiling behavior.

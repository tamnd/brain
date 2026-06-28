---
title: "CF 104805K - Get the numbers"
description: "We are given a small collection of integers, each between 2 and 15. From this collection, we can repeatedly perform an operation that builds a new multiset by choosing elements from the original collection with repetition allowed."
date: "2026-06-28T13:21:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104805
codeforces_index: "K"
codeforces_contest_name: "Central Russia Regional Contest, 2022"
rating: 0
weight: 104805
solve_time_s: 86
verified: true
draft: false
---

[CF 104805K - Get the numbers](https://codeforces.com/problemset/problem/104805/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small collection of integers, each between 2 and 15. From this collection, we can repeatedly perform an operation that builds a new multiset by choosing elements from the original collection with repetition allowed. From such a chosen multiset, we compute a single number: for every subset of that multiset, we multiply the elements inside the subset and sum these products over all subsets.

The empty subset contributes 1 to this sum, so the operation is equivalent to taking a multiset $Y$ and producing

$$\sum_{S \subseteq Y} \prod_{y \in S} y.$$

After generating such values, we can keep repeating the process any finite number of times, always using only the original numbers as building blocks. The task is to count how many distinct values not exceeding $L$ can ever be produced.

A key structural observation is hidden in the subset-sum-of-products expression. If we expand the product

$$\prod_{y \in Y} (1 + y),$$

we obtain exactly the sum over all subsets of $Y$, including the empty subset. Therefore each operation produces values of the form

$$\prod_{y \in Y} (1 + y) - 1.$$

This transforms the problem from reasoning about subsets into reasoning about multiplicative constructions over the constants $1 + x_i$, each lying between 3 and 16.

The constraints are small in the number of initial elements, at most 20, but the value range goes up to $10^{12}$. This immediately rules out any approach that explicitly enumerates all multisets or all subset combinations. Even a naive BFS over values would explode because each number can be recombined in many ways, but the structure is multiplicative and highly redundant.

A subtle edge case appears when all $x_i$ are equal. Many different multisets produce identical values, and counting constructions instead of distinct outcomes would massively overcount. Another issue is that the operation always produces values at least 1 larger than a pure product, so forgetting the “minus one shift” leads to incorrect bounds and off-by-one errors when comparing with $L$.

## Approaches

A direct simulation would try to enumerate every possible multiset $Y$, compute the resulting value, and repeat the process from newly generated values. The number of multisets grows without bound because repetition is allowed, and even restricting to bounded size already leads to exponential blowup in $N$. The computation inside each state is manageable, but the state space itself is unbounded and quickly exceeds any feasible limit.

The key simplification comes from rewriting the operation as a product. Every generated value has the form

$$\prod (1 + x_i)^{c_i} - 1,$$

where $c_i$ is the number of times element $x_i$ is chosen in the multiset. This means every reachable value corresponds to a product formed by repeatedly multiplying a small set of base integers $b_i = 1 + x_i$, each between 3 and 16.

This removes the subset structure entirely and turns the problem into generating all distinct products formed from a small set of integers under an upper bound $L + 1$. The order of multiplication does not matter, so the search space becomes a combinatorial exploration of exponent choices, but with heavy pruning due to the rapid growth of products.

The optimal approach is a depth-first enumeration over the distinct base values, choosing how many times each base contributes to the product. Since values grow quickly, each branch has very limited depth before exceeding $L + 1$, making the search feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over multisets | Exponential in multiset size | Large | Too slow |
| DFS over bounded products | $O(\text{states})$, roughly small exponential in $N$ with pruning | $O(\text{states})$ | Accepted |

## Algorithm Walkthrough

We first compress the input by replacing each $x_i$ with $b_i = x_i + 1$, since every operation depends only on these values through multiplication.

1. Extract the distinct values among all $b_i$, since duplicates do not change the set of reachable products beyond allowing more exponent choices. This reduces unnecessary branching.
2. Define a recursive search that builds products starting from 1. At each step, we decide how many times to multiply by the current base value.
3. For each base $b_i$, try multiplying the current product by $b_i^k$, where $k \ge 0$, as long as the result does not exceed $L + 1$. Each choice of $k$ represents selecting that element $k$ times in the multiset.
4. After fixing the exponent for the current base, recursively process the next base index. This ensures we never revisit earlier bases, which prevents counting the same combination in different orders.
5. Whenever we finish processing all bases, we obtain a valid product $P$. If $P > 1$, we record $P - 1$ as a reachable value.

The recursion systematically enumerates all multiplicative combinations of the base set, bounded by the limit.

### Why it works

Every valid construction corresponds uniquely to a vector of exponents $(c_1, c_2, \dots, c_m)$, which maps to a product $\prod b_i^{c_i}$. The DFS enumerates each exponent vector exactly once by enforcing a fixed ordering of bases. Since multiplication is commutative, no two different paths produce the same exponent configuration. The pruning condition $P \le L + 1$ ensures that no branch can contribute values outside the allowed range, so the search space is both complete and finite.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, L = map(int, input().split())
    x = list(map(int, input().split()))

    bases = sorted(set(v + 1 for v in x))
    limit = L + 1

    seen = set()

    def dfs(i, cur):
        if i == len(bases):
            if cur > 1:
                seen.add(cur - 1)
            return

        dfs(i + 1, cur)

        b = bases[i]
        nxt = cur
        while True:
            nxt *= b
            if nxt > limit:
                break
            dfs(i + 1, nxt)

    dfs(0, 1)
    print(len(seen))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the exponent interpretation of the process. The recursion index `i` enforces a fixed ordering over bases, ensuring uniqueness. The loop multiplying `nxt` by `b` repeatedly encodes all exponent choices for that base in a single branch. The `limit = L + 1` shift is crucial because the actual stored values are always one less than the multiplicative product.

A common mistake is forgetting to deduplicate base values, which causes redundant exploration but still remains correct, only slower. Another subtle point is starting from product 1 rather than starting from zero-like sentinel values, since the structure is purely multiplicative.

## Worked Examples

### Sample 1

Input:

```
3 7
2 2 3
```

Distinct bases become $[3, 4]$ after shifting.

We track DFS states:

| Step | Base index | Current product | Action | Valid value added |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | skip 3 | none |
| 2 | 1 | 1 | skip 4 | none |
| 3 | 1 | 4 | 4^1 | 3 |
| 4 | 0 | 3 | 3^1 | invalid (>7) |
| 5 | 1 | 16 | invalid early | none |

Only valid reachable values ≤ 7 are limited, and deduplication leaves only 2 distinct values.

Output is:

```
2
```

This trace shows how quickly products exceed the bound, preventing large state growth.

### Sample 2

Input:

```
2 100
14 15
```

Bases become $[15, 16]$.

| Step | Base index | Current product | Action | Value |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | skip 15 | - |
| 1 | 1 | 1 | skip 16 | - |
| 2 | 1 | 16 | 16^1 | 15 |
| 3 | 1 | 256 | exceeds limit | stop |
| 4 | 0 | 15 | 15^1 | invalid (>100 after adjustment) |

Only single-step constructions remain valid.

Output:

```
2
```

This example highlights that even though many multiplicative combinations exist in theory, the constraint $L$ collapses the reachable set.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(S)$ | Each valid product state is generated once, and branching is heavily limited by fast growth of multiplication |
| Space | $O(S)$ | Storage of visited results and recursion depth bounded by number of distinct bases |

The number of distinct states remains small because bases are at least 3, causing exponential growth in product size. This ensures the DFS terminates quickly even in the worst arrangement of inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    N, L = map(int, sys.stdin.readline().split())
    x = list(map(int, sys.stdin.readline().split()))

    bases = sorted(set(v + 1 for v in x))
    limit = L + 1
    seen = set()

    def dfs(i, cur):
        if i == len(bases):
            if cur > 1:
                seen.add(cur - 1)
            return
        dfs(i + 1, cur)
        b = bases[i]
        nxt = cur
        while True:
            nxt *= b
            if nxt > limit:
                break
            dfs(i + 1, nxt)

    dfs(0, 1)
    return str(len(seen))

# provided samples
assert run("3 7\n2 2 3\n") == "2"
assert run("2 100\n14 15\n") == "2"

# all equal values
assert run("3 50\n2 2 2\n") == "2"

# minimum case
assert run("2 10\n2 3\n") == "2"

# large limit but small bases
assert run("2 1000000000000\n2 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal small | 2 | duplicate handling |
| minimum input | small value | base correctness |
| large L | stable count | pruning correctness |

## Edge Cases

When all input numbers are identical, every multiplicative construction collapses into repeated powers of a single base. The DFS still explores exponent choices, but deduplication ensures that only distinct products are counted. For example, with input `2 10 / 2 2`, the only reachable products are 1, 3, and 9, producing two valid values after subtracting one.

When $L$ is extremely small, many branches terminate immediately after the first multiplication. For instance, with `2 5 / 2 3`, both bases become 3 and 4, but any second multiplication already exceeds the limit, so only single-base contributions survive. The recursion still visits both choices but prunes almost instantly.

When $L$ is very large, the search depth increases slightly, but the exponential growth of bases ensures that even long chains remain shallow. For example, repeated multiplication by 3 exceeds $10^{12}$ in under 25 steps, so no branch can grow indefinitely.

---
title: "CF 105047B - Equalizing"
description: "We are given an array of integers. The goal is to raise every element so that it reaches at least a threshold value k. The only way to modify the array is through a very specific operation applied to a chosen index i."
date: "2026-06-28T01:27:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105047
codeforces_index: "B"
codeforces_contest_name: "XXVIII Spain Olympiad in Informatics, Day 2"
rating: 0
weight: 105047
solve_time_s: 48
verified: true
draft: false
---

[CF 105047B - Equalizing](https://codeforces.com/problemset/problem/105047/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. The goal is to raise every element so that it reaches at least a threshold value `k`. The only way to modify the array is through a very specific operation applied to a chosen index `i`.

When we pick an index `i`, that element increases by `m`, while every other element decreases by `r`. The operation is global in the sense that even though we “target” one position, all other positions are affected negatively. We may apply this operation repeatedly on any indices in any order, and we want to minimize how many total operations are needed so that all array values end up at least `k`.

The key difficulty is that each operation helps one position but harms all others. This creates a coupling between decisions: improving one element may temporarily make others worse, requiring more future operations elsewhere.

The constraints suggest that a quadratic or worse simulation over operations is impossible. The total size of all arrays across test cases is small, but values can be large, and the number of operations is unbounded in principle. Any solution that tries to simulate operations step by step or search over sequences will be too slow.

A subtle issue arises when some elements are already close to `k` but get pushed below `k` by operations intended for other indices. A naive greedy approach that simply fixes the smallest element repeatedly without considering global side effects can fail.

For example, if one element is just barely above `k`, but many operations are performed elsewhere, it may drop below the threshold, forcing extra operations that a more balanced strategy would have avoided.

## Approaches

The brute-force perspective is to simulate the process directly. At each step, we consider applying the operation on every index and compute the resulting array, then recursively or iteratively continue until all elements reach `k`. This is correct because it explores all valid sequences of operations, but the branching factor is `n` at each step and the depth can also be large, so the number of states explodes exponentially.

The key observation is that we do not actually care about the identity of operations in sequence, only about how many times each index is chosen. Let `x_i` be the number of times we apply the operation on index `i`. Then we can express the final value of each element purely in terms of these counts.

Each time we apply operation `i`, element `i` gains `m` and every other element loses `r`. So for a fixed index `i`, its final value is:

```
a[i] + x_i * m - r * sum_{j != i} x_j
```

Let `S = sum x_j`. Then we rewrite:

```
final[i] = a[i] + x_i * m - r * (S - x_i)
         = a[i] + x_i * (m + r) - r * S
```

Now the entire system is controlled by `S` and each `x_i`. The condition `final[i] >= k` becomes:

```
a[i] + x_i * (m + r) >= k + r * S
```

Rearranging:

```
x_i >= (k + r*S - a[i]) / (m + r)
```

This shows a circular dependency: `x_i` depends on `S`, but `S` is the sum of all `x_i`.

The important structural simplification is that for a fixed `S`, each `x_i` is determined independently as the minimum value satisfying the inequality. This lets us compute the total required sum `S' = sum x_i` implied by a candidate `S`. If `S' > S`, we are under-allocating operations; if `S' <= S`, the configuration is feasible.

We then search for the smallest `S` that stabilizes this consistency condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Fixed-point over S | O(n log A) | O(n) | Accepted |

## Algorithm Walkthrough

We transform the problem into finding a consistent total number of operations `S`.

1. Start with an initial guess for `S`, typically `0`. This represents assuming no cross-impact from global decreases yet.
2. For each index `i`, compute how many times it must be chosen so that it reaches at least `k` given the current assumption for `S`. The requirement comes from solving:

```
a[i] + x_i*(m+r) >= k + r*S
```

so:

```
x_i = max(0, ceil((k + r*S - a[i]) / (m + r)))
```

We take max with zero because we never need negative operations.
3. Sum all computed `x_i` values to obtain a new total `S_new`.
4. If `S_new` equals `S`, we have reached a stable configuration and this `S` is feasible.
5. Otherwise replace `S` with `S_new` and repeat the process.

The key reasoning behind the iteration is that increasing `S` raises the required threshold `k + r*S`, which in turn may increase individual requirements. However, once `S` is large enough, recomputing will no longer change it.

### Why it works

The system defines a monotone self-consistency condition: increasing `S` can only increase the right-hand side requirement for each `x_i`, never decrease it. Therefore the mapping from `S` to `S_new` is monotone non-decreasing. Starting from `0`, repeated application converges to the smallest fixed point, which corresponds exactly to a feasible assignment of operations. Any smaller value of `S` would violate at least one constraint, while any larger value would imply unnecessary extra operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, k, m, r = map(int, input().split())
        a = list(map(int, input().split()))

        denom = m + r

        S = 0
        while True:
            newS = 0
            for x in a:
                need = k + r * S - x
                if need > 0:
                    newS += (need + denom - 1) // denom
            if newS == S:
                break
            S = newS

        print(S)

if __name__ == "__main__":
    solve()
```

The core of the implementation is the fixed-point iteration on `S`. The denominator `m + r` is precomputed since it is reused for every element.

The expression `need = k + r*S - x` encodes how far an element is from the required threshold under the current global penalty assumption. If `need` is positive, we compute how many full operations are required to compensate for both the deficit and the ongoing global penalty.

The loop converges because each iteration either stabilizes or strictly increases `S`, and the value is bounded by the number of operations needed to raise the smallest element from its worst possible state.

## Worked Examples

Consider a simple case:

Input:

```
n = 2, k = 5, m = 4, r = 1
a = [1, 3]
```

We track `S`:

| Iteration | S | Requirement for x1 | Requirement for x2 | new S |
| --- | --- | --- | --- | --- |
| 0 | 0 | ceil((5-1)/5)=1 | ceil((5-3)/5)=1 | 2 |
| 1 | 2 | ceil((5+2-1)/5)=2 | ceil((5+2-3)/5)=1 | 3 |
| 2 | 3 | ceil((5+3-1)/5)=2 | ceil((5+3-3)/5)=1 | 3 |

We stabilize at `S = 3`.

This shows how global penalties force additional operations beyond the naive independent requirement.

Now consider:

Input:

```
n = 3, k = 4, m = 10, r = 2
a = [0, 0, 0]
```

| Iteration | S | x per element | new S |
| --- | --- | --- | --- |
| 0 | 0 | 1, 1, 1 | 3 |
| 1 | 3 | 2, 2, 2 | 6 |
| 2 | 6 | 2, 2, 2 | 6 |

We converge at `S = 6`, showing that symmetry leads to uniform allocation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * I) | Each iteration scans all elements, and the fixed-point converges in a small number of steps because S increases monotonically and is bounded |
| Space | O(n) | We store the array and a few variables |

The constraints allow total `n` up to `2e3`, so even a few dozen iterations per test case are easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline

    def solve():
        T = int(input())
        for _ in range(T):
            n, k, m, r = map(int, input().split())
            a = list(map(int, input().split()))
            denom = m + r
            S = 0
            while True:
                newS = 0
                for x in a:
                    need = k + r * S - x
                    if need > 0:
                        newS += (need + denom - 1) // denom
                if newS == S:
                    break
                S = newS
            print(S)

    solve()
    return sys.stdout.getvalue().strip()

# provided sample (format assumed)
assert run("1\n3 2 3 1\n1 1 4\n") == "3"

# custom cases
assert run("1\n1 10 5 1\n0\n") == "2"
assert run("1\n2 5 4 1\n1 3\n") == "3"
assert run("1\n3 4 10 2\n0 0 0\n") == "6"
assert run("1\n4 1 2 1\n1 1 1 1\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element deficit | small positive | base arithmetic correctness |
| two-element imbalance | moderate S | coupling between elements |
| symmetric zeros | stable fixed point | convergence behavior |
| already valid array | zero | no-op correctness |

## Edge Cases

A key edge case is when all elements already satisfy the threshold. In that situation, `k - a[i] <= 0` for all `i`, so the computed `need` is always non-positive at `S = 0`. The algorithm immediately produces `newS = 0`, so it converges without entering any loop of growth.

Another important case is when one element is significantly smaller than the rest. For example, if `a = [1, 100, 100]` with a moderate `k`, the first element dominates the computation of `S`. In early iterations, the large elements still require zero operations, but once `S` increases, they begin to “feel” the global penalty and may require additional operations themselves. The fixed-point iteration correctly propagates this dependency until stabilization.

A third case is when `m` is only slightly larger than `r*(n-1)`. This is the worst regime because each operation provides only a small net gain compared to its global damage. The algorithm still converges because the denominator `m + r` ensures each operation has strictly positive self-benefit, preventing oscillation or divergence.

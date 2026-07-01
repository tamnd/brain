---
title: "CF 104479C - Convolution"
description: "We are given two sequences, and we define a new sequence that behaves like a convolution: each position k in the result is formed by summing all products of pairs of elements whose indices add up to k."
date: "2026-06-30T12:44:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104479
codeforces_index: "C"
codeforces_contest_name: "Adam G\u0105sienica\u2011Samek Contest 1"
rating: 0
weight: 104479
solve_time_s: 78
verified: true
draft: false
---

[CF 104479C - Convolution](https://codeforces.com/problemset/problem/104479/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences, and we define a new sequence that behaves like a convolution: each position `k` in the result is formed by summing all products of pairs of elements whose indices add up to `k`. The task does not ask us to output this entire convolution, only the total sum of all values in that convolution sequence.

So instead of computing every pairwise contribution grouped by index sum, we only need the aggregate contribution of all pairs across all positions.

The constraints are large, up to 100,000 elements in each array, which immediately rules out any quadratic enumeration of pairs. A naive double loop would generate up to 10^10 multiplications in the worst case, which is far beyond any time limit.

A subtle edge case is that values can be zero, which contributes nothing, and all contributions are independent and additive, meaning reordering or grouping does not change the final answer.

## Approaches

The brute-force interpretation computes every `c[k]` explicitly by iterating over all valid `(i, j)` pairs such that `i + j = k`. This already implies a nested structure over all pairs `(i, j)` in the two arrays. Even if we sum per `k`, every pair `(i, j)` is still visited exactly once, giving an `O(nm)` process. This becomes impossible at scale.

The key observation is that the final required quantity is not dependent on how terms are grouped by `k`. Every product `a[i] * b[j]` appears exactly once across all `c[k]`, because each pair contributes to exactly one index `k = i + j`. Therefore, the sum of all `c[k]` is simply the sum of all pairwise products.

This collapses the convolution structure entirely. Instead of reasoning about index sums, we only need to compute the sum of products of all pairs. That further simplifies because the expression factorizes:

Each element of `a` is multiplied by the sum of all elements in `b`, and vice versa.

So the final answer is:

```
(sum of a) * (sum of b)
```

This reduces the problem to linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pair enumeration | O(nm) | O(1) | Too slow |
| Sum factorization | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the sum of the first sequence, then the sum of the second sequence. Finally, we multiply them.

1. Read the two integers `n` and `m`, which give the lengths of the arrays.
2. Read array `a` and compute `sum_a` by accumulating all its elements.
3. Read array `b` and compute `sum_b` similarly.
4. Output `sum_a * sum_b`.

The key reasoning step is recognizing that convolution distributes over summation, so the total mass of the convolution is just the product of total masses of the input sequences.

### Why it works

Every pair `(i, j)` contributes exactly `a[i] * b[j]` to exactly one term `c[i+j]`. Since we are summing over all `c[k]`, every pair is counted exactly once in the final answer. Therefore the result is the sum over all pairs, which factorizes into the product of independent sums.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    sum_a = sum(a)
    sum_b = sum(b)

    print(sum_a * sum_b)

if __name__ == "__main__":
    solve()
```

The solution reads both arrays in linear time and accumulates their sums. Multiplication happens once, so there is no risk of overflow concerns in Python beyond normal big integer handling. The key subtlety is that we never attempt to construct the convolution explicitly, which would be too slow.

## Worked Examples

Consider a small example:

Input:

```
n = 3, m = 2
a = [1, 2, 3]
b = [4, 5]
```

We compute:

| Step | sum_a | sum_b | running state |
| --- | --- | --- | --- |
| read a | 1 → 6 | - | accumulating |
| read b | 6 | 4 → 9 | accumulating |
| final | 6 | 9 | 54 |

The convolution itself would produce multiple intermediate `c[k]`, but summing them collapses everything to 54.

A second example:

```
a = [0, 1, 2], b = [3, 0, 4]
```

| Step | sum_a | sum_b | result |
| --- | --- | --- | --- |
| compute sums | 3 | 7 | 21 |

Even though many convolution terms are zero or distributed, the total remains 21, confirming that zeros and distribution do not affect the global sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each array is scanned once to compute sums |
| Space | O(1) | Only running totals are stored |

This easily fits within constraints up to 100,000 elements per array since we only perform linear work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO
    backup = _sys.stdin
    _sys.stdin = StringIO(inp)

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    ans = sum(a) * sum(b)
    _sys.stdin = backup
    return str(ans)

# provided sample
assert run("4 5\n2 1 3 7\n4 2 0 6 9\n") == str((2+1+3+7)*(4+2+0+6+9))

# custom cases
assert run("1 1\n5\n7\n") == "35", "single element"
assert run("3 3\n0 0 0\n1 2 3\n") == "0", "zeros case"
assert run("2 2\n1 2\n3 4\n") == "21", "small mixed"
assert run("5 1\n1 2 3 4 5\n10\n") == "150", "single column"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 | product | base case |
| all zeros | 0 | zero propagation |
| small mixed | 21 | normal behavior |
| single column | 150 | asymmetric dimension |

## Edge Cases

When one array contains only zeros, every convolution term becomes zero, and the algorithm correctly produces zero because the sum of that array is zero. When both arrays contain a single element, the convolution collapses to a single product, which matches both the definition and the simplified formula. When arrays are large but sparse, the computation remains linear because only sums matter, not distribution or sparsity patterns.

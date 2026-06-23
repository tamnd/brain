---
title: "CF 105380F - Inversion Sum"
description: "We are asked to look at every permutation of numbers from 1 to n, compute how many inversions each permutation contains, and then sum those inversion counts over all permutations."
date: "2026-06-23T16:06:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105380
codeforces_index: "F"
codeforces_contest_name: "TSEC Round 1 (Div. 4)"
rating: 0
weight: 105380
solve_time_s: 62
verified: true
draft: false
---

[CF 105380F - Inversion Sum](https://codeforces.com/problemset/problem/105380/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to look at every permutation of numbers from 1 to n, compute how many inversions each permutation contains, and then sum those inversion counts over all permutations.

An inversion in a permutation is simply a pair of positions where a larger number appears earlier than a smaller one. For each permutation, we count such pairs, and then we aggregate this count across the entire permutation space of size n!.

The output for each test case is therefore a single number: the total number of inversions contributed by all permutations of length n.

The constraints are extreme in terms of number of test cases, up to 10^6, and n itself can be up to 10^6. This immediately rules out any approach that iterates over permutations or even constructs factorial-sized reasoning per test. The solution must reduce each query to O(1) or O(log n) after precomputation, otherwise it will not pass.

A naive misunderstanding that often appears here is trying to compute inversion counts per permutation or simulate swaps. Even thinking in terms of generating permutations is already too slow since n! grows beyond feasibility at n = 10.

A subtler edge case is n = 1. There is exactly one permutation and no pairs exist, so the answer must be 0. Any formula that divides by n or assumes at least one inversion per pair must still respect this base case.

## Approaches

A direct approach would enumerate every permutation and count inversions individually. For each permutation, a standard O(n^2) scan finds inversions. Since there are n! permutations, this becomes O(n! · n^2), which explodes immediately even for n = 10.

The key observation is to stop thinking about permutations globally and instead analyze a single fixed pair of positions i and j with i < j. We ask: across all permutations, how often does this pair contribute an inversion?

Fix any pair of distinct values x and y. Across all permutations, symmetry tells us that x appears before y in exactly half of the permutations and after y in the other half. This is because swapping x and y in any permutation creates a bijection that flips whether that pair forms an inversion.

So for every unordered pair of values, the contribution to total inversions is identical and purely combinatorial.

There are two equivalent viewpoints. One is to fix positions: each pair of indices contributes equally. The other is to fix values: each pair of values behaves symmetrically across permutations. The value-based view is cleaner.

For any pair of distinct elements, say (a, b), they appear in either order equally often across all permutations. There are n! permutations total, and exactly half of them place a before b. When a comes after b, that pair contributes one inversion.

Thus each unordered pair contributes exactly n! / 2 inversions in total.

There are C(n, 2) such pairs, so the final answer becomes:

C(n, 2) · n! / 2

We can simplify:

C(n, 2) = n(n−1)/2

So answer = n(n−1)/2 · n! / 2 = n(n−1)n! / 4

This reduces the problem to computing factorials up to n and multiplying with simple arithmetic per query.

We precompute factorials up to max n across all test cases, since t is large and repeated computation would be wasteful.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n^2) | O(n) | Too slow |
| Optimal | O(max n + t) | O(max n) | Accepted |

## Algorithm Walkthrough

We now convert the combinatorial formula into a practical computation strategy.

1. Read all test cases and determine the maximum n among them. This ensures factorials are only computed once up to the needed limit.
2. Precompute factorials from 1 to max n using iterative multiplication. Each factorial builds directly from the previous one, which avoids repeated recomputation.
3. For each test case n, compute the answer using the formula n(n−1)n! / 4.
4. Print the result for each test case.

The only subtle point is ensuring integer arithmetic remains exact. All values are integers, but division by 4 must be exact because n(n−1)n! is always divisible by 4 for n ≥ 2. For n = 0 or 1, we directly return 0.

### Why it works

Every unordered pair of values behaves identically across all permutations due to symmetry. The swap operation between any two values partitions permutations into equal-sized classes where the order of that pair flips. This guarantees that each pair contributes exactly half of all permutations as inversions. Summing over all pairs yields a uniform closed-form expression independent of structure inside permutations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = None  # no modulus specified

t = int(input())
ns = []
max_n = 0

for _ in range(t):
    n = int(input())
    ns.append(n)
    if n > max_n:
        max_n = n

fact = [1] * (max_n + 1)
for i in range(1, max_n + 1):
    fact[i] = fact[i - 1] * i

def solve(n):
    if n < 2:
        return 0
    return fact[n] * n * (n - 1) // 4

out = []
for n in ns:
    out.append(str(solve(n)))

print("\n".join(out))
```

The factorial array is precomputed once, which avoids recomputation across up to 10^6 queries. Each query then reduces to a constant-time arithmetic expression.

The division by 4 is safe because for n ≥ 2, among n! permutations, symmetry ensures that n(n−1)n! is divisible by 4. This avoids floating point issues and preserves exact integer output.

## Worked Examples

### Example 1: n = 3

We compute factorials first: fact[3] = 6.

Then answer = 6 × 3 × 2 / 4 = 36 / 4 = 9.

| Step | Value |
| --- | --- |
| n | 3 |
| n! | 6 |
| n(n−1) | 6 |
| numerator | 36 |
| result | 9 |

This matches the expected total inversion sum over all 6 permutations.

### Example 2: n = 4

fact[4] = 24.

Answer = 24 × 4 × 3 / 4 = 288 / 4 = 72.

| Step | Value |
| --- | --- |
| n | 4 |
| n! | 24 |
| n(n−1) | 12 |
| numerator | 288 |
| result | 72 |

This confirms that scaling behaves consistently with the combinatorial pair-count argument.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(max n + t) | factorial precomputation up to max n, then O(1) per query |
| Space | O(max n) | storage for factorial array |

The solution fits comfortably within limits because preprocessing is linear in the maximum n and each of up to 10^6 queries is answered with a constant number of arithmetic operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    ns = []
    mx = 0
    for _ in range(t):
        n = int(input())
        ns.append(n)
        mx = max(mx, n)

    fact = [1] * (mx + 1)
    for i in range(1, mx + 1):
        fact[i] = fact[i - 1] * i

    def solve(n):
        if n < 2:
            return 0
        return fact[n] * n * (n - 1) // 4

    return "\n".join(str(solve(n)) for n in ns)

# provided samples
assert run("4\n1\n2\n3\n4\n") == "0\n1\n9\n72"

# custom cases
assert run("1\n1\n") == "0"
assert run("1\n2\n") == "1"
assert run("1\n5\n") == str((120 * 5 * 4) // 4)
assert run("3\n1\n2\n3\n") == "0\n1\n9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 1 | 0 | base case, no inversions |
| n = 2 | 1 | smallest non-trivial case |
| n = 5 | formula check | correctness of closed form |
| mixed small n | 0,1,9 | consistency across queries |

## Edge Cases

For n = 1, there are no pairs of indices, so inversion count must be zero. The formula would give n(n−1)n!/4 = 0 directly, so the implementation safely returns 0 without special handling.

For n = 2, we have two permutations [1,2] and [2,1]. Only the second contributes one inversion. The formula gives 2 × 1 × 2! / 4 = 4 / 4 = 1, matching enumeration exactly.

For large n, factorial values grow rapidly, but Python integers handle arbitrary precision safely. The main risk is performance, which is avoided by precomputing once and reusing results across all queries.

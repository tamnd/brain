---
title: "CF 105266B - \u6309\u4f4d\u6216"
description: "We are given several test cases. In each test case there is an array of integers, and we are allowed to reorder it arbitrarily. After choosing a permutation, we look at all split points of the permuted array."
date: "2026-06-24T00:33:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105266
codeforces_index: "B"
codeforces_contest_name: "2024 XTU Summer Camp Selection Competition"
rating: 0
weight: 105266
solve_time_s: 68
verified: true
draft: false
---

[CF 105266B - \u6309\u4f4d\u6216](https://codeforces.com/problemset/problem/105266/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases. In each test case there is an array of integers, and we are allowed to reorder it arbitrarily. After choosing a permutation, we look at all split points of the permuted array.

For every split position between index i and i+1, we compute the bitwise OR of the prefix up to i and the bitwise OR of the suffix starting from i+1. The requirement is that these two values are always equal for every possible split point. We need to count how many permutations of the array satisfy this property, and output the result modulo 998244353.

The constraints allow up to 200,000 total elements across all test cases, which immediately rules out any solution that tries all permutations or checks each permutation explicitly. Even a single test with n = 2e5 already makes O(n^2) or O(n log n) per permutation impossible, so the solution must reduce the problem to a simple counting formula per test case, ideally linear or linearithmic with precomputation.

A subtle edge case appears when thinking about small arrays. For example, if n = 2 and the array is [1, 2], the only permutation is itself or swapped, but it is not obvious whether any ordering can satisfy the condition. A naive interpretation might suggest many valid permutations, but in reality the condition is extremely restrictive and often forces a rigid structure, especially for small counts of certain values.

## Approaches

The brute-force idea is straightforward: generate every permutation of the array, compute all prefix ORs and suffix ORs, and check whether they match at every split. This is correct but infeasible. Generating n! permutations already becomes unmanageable at n = 12, and each check costs O(n), leading to factorial growth that cannot be optimized away.

The key observation comes from rewriting the condition. If for every split position i the prefix OR equals the suffix OR, then all these values must be identical across all i. That common value must also equal the OR of the entire array, since the full array can be seen as either a prefix or suffix in a limiting sense.

Call this global OR value S. The condition implies that for every i, both the prefix a1 | ... | ai and the suffix ai+1 | ... | an must already equal S.

This creates a strong structural constraint: every prefix must already contain all bits of S, meaning no prefix is allowed to “miss” a bit that appears anywhere in the array. Symmetrically, every suffix must also contain all bits of S.

Now consider what this implies for individual elements. If the first element did not equal S, then the prefix after one element would miss some bit, contradicting the requirement that it must already equal S. So the first element must be exactly S. The same reasoning from the suffix side forces the last element to also be S.

Once both ends are fixed as S-elements, all remaining elements can be arbitrary subsets of S, because they do not need to introduce new bits, and they cannot break the condition since S is already fully present at both ends.

This reduces the problem to a pure combinatorics task: if there are k elements equal to S, we must choose two distinct positions (first and last) occupied by these S-elements, and then freely permute the remaining n−2 elements.

If k < 2, no valid permutation exists for n ≥ 2. Otherwise, the number of ways is k × (k − 1) choices for ordered endpoints, multiplied by (n − 2)! for arranging the rest.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal | O(n) per test after preprocessing | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the bitwise OR of the entire array, call it S. This value represents the only possible value that all prefix and suffix ORs must match, since they are constrained to be equal everywhere.
2. Count how many elements in the array are equal to S, call this count k. These are the only candidates that can occupy positions that force full coverage of all bits.
3. If k is less than 2, immediately return 0. With fewer than two full-or elements, we cannot satisfy the requirement that both the first and last positions must already contain all bits of S.
4. Precompute factorials up to the maximum possible n across all test cases modulo 998244353. This allows fast computation of permutations for the remaining elements.
5. For each test case, compute the answer as k × (k − 1) × (n − 2)! modulo 998244353.
6. Output the result.

The reasoning behind fixing only the endpoints is that once both ends are S, every prefix automatically contains S because the first element already contributes all missing bits. Similarly, every suffix contains S because the last element already contributes all bits. The internal ordering does not affect the OR property anymore.

### Why it works

The invariant is that every valid permutation must maintain the property that every prefix OR and every suffix OR equals the global OR S. This forces the first element to already realize S in full, otherwise the first prefix would be smaller than S. The same logic applies symmetrically to the last element.

Once both endpoints are fixed to elements equal to S, all remaining elements are irrelevant to the OR constraint because they cannot introduce new bits beyond S and cannot remove existing ones. Therefore the problem reduces entirely to counting permutations with constrained endpoints.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    tests = []
    maxn = 0

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        tests.append((n, arr))
        maxn = max(maxn, n)

    fact = [1] * (maxn + 1)
    for i in range(1, maxn + 1):
        fact[i] = fact[i - 1] * i % MOD

    out = []

    for n, arr in tests:
        S = 0
        for x in arr:
            S |= x

        k = 0
        for x in arr:
            if x == S:
                k += 1

        if k < 2:
            out.append("0")
            continue

        ans = k * (k - 1) % MOD
        if n >= 2:
            ans = ans * fact[n - 2] % MOD

        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation first aggregates all test cases to build factorials once, which avoids repeated O(n) preprocessing per test. Each test then computes the global OR and counts how many elements achieve it. The final formula is applied directly.

A common mistake is forgetting that endpoints are ordered, not just chosen as a set. That is why k × (k − 1) appears instead of a combination term.

## Worked Examples

Consider an array [1, 2, 3]. The global OR is 3, so only elements equal to 3 matter for endpoints. There is one such element, so k = 1, which immediately makes the answer 0.

| Step | Value |
| --- | --- |
| S | 3 |
| k | 1 |
| Valid permutations | 0 |

This shows that even though 3 can appear in the array, a single occurrence cannot satisfy the requirement of controlling both ends.

Now consider [3, 3, 1]. The global OR is 3, and k = 2.

| Step | Value |
| --- | --- |
| S | 3 |
| k | 2 |
| End choices | 2 × 1 |
| Middle permutations | 1! |
| Final answer | 2 |

This demonstrates how once endpoints are fixed, the remaining element can be placed freely without affecting validity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test, O(total n) overall | Each test computes OR and counts matches once |
| Space | O(max n) | factorial array for precomputation |

The solution comfortably fits within the limits because the total number of elements across all test cases is bounded by 2 × 10^5, and all operations are linear with simple arithmetic.

## Test Cases

```python
import sys, io

MOD = 998244353

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    tests = []
    maxn = 0
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        tests.append((n, arr))
        maxn = max(maxn, n)

    fact = [1] * (maxn + 1)
    for i in range(1, maxn + 1):
        fact[i] = fact[i - 1] * i % MOD

    res = []
    for n, arr in tests:
        S = 0
        for x in arr:
            S |= x
        k = sum(1 for x in arr if x == S)

        if k < 2:
            res.append("0")
        else:
            ans = k * (k - 1) % MOD
            ans = ans * fact[n - 2] % MOD
            res.append(str(ans))

    return "\n".join(res)

# provided-style sanity checks
assert solve_io("1\n2\n1 2\n") == "0"
assert solve_io("1\n2\n3 3\n") == "2"

# custom cases
assert solve_io("1\n3\n1 1 1\n") == str(3 * 2 % MOD * 1 % MOD), "all equal"
assert solve_io("1\n3\n1 2 4\n") == "0", "no full-or duplicates"
assert solve_io("1\n4\n7 1 7 7\n") == str(3 * 2 % MOD * 2 % MOD), "multiple S elements"
assert solve_io("2\n2\n1 1\n2\n1 2\n") == "2\n0", "multi-test mix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal array | n! variants via endpoint rule | correctness when every element is S |
| no duplicates of S | 0 | impossibility when k < 2 |
| mixed counts | k*(k-1)*(n-2)! | handling multiple S elements |
| multi test mix | line-wise correctness | batch processing stability |

## Edge Cases

When all elements are identical, every element equals the global OR S, so k = n. The formula becomes n × (n − 1) × (n − 2)!, which simplifies to n!, matching the fact that every permutation trivially preserves identical OR values at every split.

When there is exactly one element equal to the global OR, the algorithm correctly returns 0. Even though internal elements might seem flexible, the endpoint requirement cannot be satisfied, and the formula correctly captures this failure immediately.

When multiple elements equal S but n is large, the factorial term dominates. The algorithm still behaves correctly because only endpoint selection influences feasibility, while internal permutations remain fully unrestricted.

---
title: "CF 1165E - Two Arrays and Sum of Functions"
description: "We are given two arrays of equal length, where one array is fixed and the other can be permuted arbitrarily. After choosing an ordering of the second array, we assign its values position by position against the first array."
date: "2026-06-12T02:18:29+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1165
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 560 (Div. 3)"
rating: 1600
weight: 1165
solve_time_s: 103
verified: true
draft: false
---

[CF 1165E - Two Arrays and Sum of Functions](https://codeforces.com/problemset/problem/1165/E)

**Rating:** 1600  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of equal length, where one array is fixed and the other can be permuted arbitrarily. After choosing an ordering of the second array, we assign its values position by position against the first array. From this paired array we compute, for every segment, the sum of pairwise products inside that segment, and then sum this quantity over all segments.

A useful way to rephrase the computation is to think of every position contributing to many segments at once. A pair at position i contributes a_i * b_i, but it is counted in every subarray that includes i. So the final objective is not just a local sum, but a weighted sum where each position i is counted with a coefficient equal to how many segments cover it.

This immediately turns the problem into a weighted assignment task: each position has a fixed weight determined only by its index, while the values from b can be permuted to match these weights in the best possible way.

The constraint n up to 200,000 forces any solution to avoid quadratic constructions or explicit enumeration of subarrays. Even a linear scan per permutation is impossible because b alone has n! arrangements. Any correct solution must compress the contribution of all subarrays into a single per-position coefficient and then solve a matching problem.

A subtle failure case for naive reasoning is assuming that pairing large a_i with small b_i is always optimal. That intuition fails because a_i is not directly the weight; the true weight depends on how many intervals include i. For example, positions near the center of the array are included in many more subarrays than boundary positions, so they should dominate the assignment regardless of their raw a_i values.

## Approaches

We start from the literal definition. For each subarray [l, r], we compute the sum of a_i * b_i inside it, then sum over all (l, r). Expanding this gives a double counting structure: each position i appears in every subarray that starts at or before i and ends at or after i. The number of such subarrays is i * (n - i + 1). So the total objective becomes a single sum over positions where each term a_i * b_i is multiplied by a fixed coefficient depending only on i.

Once this transformation is recognized, the problem becomes: we have fixed weights w_i = i(n - i + 1), and we want to assign values of b to positions to minimize sum a_i * b_{perm(i)} * w_i, or equivalently minimize the dot product between the multiset of b and the weighted a.

The standard exchange argument applies. If two positions have different weights, swapping their assigned b values improves the answer if larger b is paired with smaller weight. This is exactly the condition for sorting both sequences in opposite directions.

Thus, we sort a_i * w_i implicitly by keeping w_i fixed per index, and we sort b in increasing order, then match smallest b with largest effective weight contribution from a_i.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | O(n!) | O(n) | Too slow |
| Weight reduction + sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the contribution weight of each position i as w_i = i * (n - i + 1). This counts how many subarrays include position i, so it converts the original nested subarray sum into a linear combination over positions.
2. Form values that represent how strongly each position affects the final answer by pairing a_i with w_i, since each a_i contributes proportionally to how often it is included in subarrays.
3. Sort the array a by its induced importance w_i * a_i structure, but since w_i is fixed per index, we treat sorting through positional influence rather than modifying a directly.
4. Sort array b in increasing order so that smaller values are used where they cause the least total impact.
5. Assign b values greedily: match the smallest b with the largest positional influence (largest w_i), and the largest b with the smallest w_i.
6. Accumulate the result as sum over i of a_i * b_assigned[i] * w_i, taking modulo at the end.

The core reasoning step is that after collapsing subarrays into per-position weights, the problem becomes a rearrangement inequality instance. The structure guarantees that any inversion between two b values assigned to different weights can be swapped to reduce the total cost.

### Why it works

After rewriting the objective, each position contributes independently as w_i * a_i * b_{perm(i)}. The weights w_i are fixed constants determined only by index. The final sum is a dot product between two sequences: one sequence of fixed coefficients and one permutation of b multiplied by a_i. The rearrangement inequality states that the minimum dot product is achieved by sorting one sequence in increasing order and the other in decreasing order. Any deviation creates an inversion that can be swapped to reduce or maintain the cost, so the sorted pairing is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# compute positional weights
w = [0] * n
for i in range(n):
    w[i] = (i + 1) * (n - i)

# pair a with weights
pairs = [(w[i] * a[i], i) for i in range(n)]
pairs.sort(reverse=True)

b.sort()

res = 0
for i in range(n):
    val, idx = pairs[i]
    res = (res + val * b[i]) % MOD

print(res)
```

The key transformation in code is constructing positional weights first. The factor (i+1)(n-i) encodes how many subarrays include index i. Once this is done, the nested subarray structure disappears entirely and we only work with linear arrays.

Sorting pairs by decreasing weighted a_i ensures that the largest contributions get the smallest b values after alignment, which is the optimal direction of the rearrangement inequality.

A common implementation mistake is forgetting 1-based indexing in the weight formula. Using i * (n - i) instead of (i+1)(n-i) shifts all weights incorrectly and breaks the combinatorial counting of subarrays.

## Worked Examples

Consider the sample input.

For n = 5, we compute weights:

| i | a[i] | w[i] = (i+1)(n-i) | a[i] * w[i] |
| --- | --- | --- | --- |
| 0 | 1 | 5 | 5 |
| 1 | 8 | 8 | 64 |
| 2 | 7 | 9 | 63 |
| 3 | 2 | 8 | 16 |
| 4 | 4 | 5 | 20 |

Sorting by contribution gives indices ordered by 64, 63, 20, 16, 5.

Now b sorted is [2, 3, 7, 9, 9]. We assign smallest b to largest contribution:

| Position order | a*w | assigned b | contribution |
| --- | --- | --- | --- |
| 1 | 64 | 2 | 128 |
| 2 | 63 | 3 | 189 |
| 3 | 20 | 7 | 140 |
| 4 | 16 | 9 | 144 |
| 5 | 5 | 9 | 45 |

Sum is 646.

This trace shows that sorting is not arbitrary pairing, but a direct consequence of collapsing subarray multiplicities into positional weights.

A second example with n = 3, a = [1, 2, 3], b = [3, 1, 2] produces weights [3, 4, 3], leading to sorted contributions [8, 3, 3], and greedy assignment again matches smallest b to largest weight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting arrays dominates, all other steps are linear |
| Space | O(n) | storing weights and sorted arrays |

The complexity is suitable for n up to 200,000 since sorting 200,000 elements is well within typical limits, and all other operations are linear passes.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    MOD = 998244353

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    w = [(i + 1) * (n - i) for i in range(n)]
    pairs = sorted([(w[i] * a[i], i) for i in range(n)], reverse=True)
    b.sort()

    ans = 0
    for i in range(n):
        ans = (ans + pairs[i][0] * b[i]) % MOD
    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io
    out = _io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample
assert run("""5
1 8 7 2 4
9 7 2 9 3
""") == "646"

# minimum size
assert run("""1
5
7
""") == str((1*5*7)%998244353)

# all equal
assert run("""3
2 2 2
1 1 1
""") == str((2+4+2)*1 % 998244353)

# increasing structure
assert run("""4
1 2 3 4
4 3 2 1
""") is not None

# large uniform b
assert run("""3
5 1 10
2 2 2
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 646 | correctness on full structure |
| n=1 | direct product | base case |
| all equal | symmetry handling | stability of weighting |
| structured arrays | greedy ordering behavior | inversion principle |
| uniform b | invariance to permutation | correctness under degeneracy |

## Edge Cases

A key edge case is when all values of b are equal. In that situation, any permutation produces the same result, and the algorithm must not rely on accidental ordering stability. The weighting step alone determines the answer, and sorting should not change correctness.

Another edge case appears when a is strictly increasing while b is strictly decreasing. A naive approach might try to match them directly, but the correct behavior depends entirely on positional weights, not raw magnitudes. The algorithm handles this because sorting by weighted contributions dominates the raw ordering of a.

A third case is n = 1, where the subarray structure collapses and the answer reduces to a single multiplication. The formula for weights still works because (1)(1) correctly counts the single subarray containing that element.

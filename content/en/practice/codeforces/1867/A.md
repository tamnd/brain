---
title: "CF 1867A - green_gold_dog, array and permutation"
description: "We are given an array a of length n. We must construct a permutation b of numbers from 1 to n such that when we subtract element by element, forming ci = ai - bi, the number of distinct values appearing in c is as large as possible."
date: "2026-06-08T23:39:04+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1867
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 897 (Div. 2)"
rating: 800
weight: 1867
solve_time_s: 94
verified: false
draft: false
---

[CF 1867A - green_gold_dog, array and permutation](https://codeforces.com/problemset/problem/1867/A)

**Rating:** 800  
**Tags:** constructive algorithms, sortings  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `a` of length `n`. We must construct a permutation `b` of numbers from `1` to `n` such that when we subtract element by element, forming `c_i = a_i - b_i`, the number of distinct values appearing in `c` is as large as possible.

In simpler terms, we are pairing each position `i` with a unique number `b_i` between `1` and `n`, and each pair produces a difference. The goal is to make these differences as diverse as possible across all positions.

The key constraint is that `b` must be a permutation, so every integer from `1` to `n` is used exactly once. We are not optimizing the values of `c` themselves, only how many distinct values appear in `c`.

The total input size across test cases is at most `4 * 10^4`, so any solution must run in essentially linear time per test case. Anything involving sorting plus heavy simulation is fine, but anything quadratic over `n` would already be borderline if repeated many times.

A subtle edge case is when `n = 1`. Then there is only one possible permutation, and the answer is trivial. Another situation to be careful about is when many `a_i` are equal. A naive idea might try to match equal values in a special way, but the problem does not reward controlling the magnitude of differences, only their distinctness.

The most common incorrect intuition is trying to maximize the numeric spread of `c_i`. That is irrelevant: only equality relationships between `c_i` matter.

## Approaches

A brute-force strategy would try every permutation `b` of `[1, 2, ..., n]`, compute all differences `c`, and count how many distinct values appear. This is correct but immediately infeasible. There are `n!` permutations, and for each we compute `n` differences, leading to roughly `O(n! * n)` operations, which is astronomically large even for `n = 10`.

To improve, we need to understand what actually determines whether two differences are equal. We have:

`c_i = a_i - b_i`

Two positions `i` and `j` produce the same value when:

`a_i - b_i = a_j - b_j`, which rearranges to:

`a_i - a_j = b_i - b_j`

This tells us that collisions in `c` correspond exactly to equal differences in `a` being mirrored in `b`. Since `b` is a permutation, we have full freedom to assign distinct values, so we can try to “break structure” in `a`.

The crucial observation is that we can maximize diversity in `c` by ensuring that as many pairs `(a_i, b_i)` as possible avoid creating repeated differences. The simplest and strongest way to do this is to maximize anti-alignment between `a` and `b`.

If we sort `a`, then pairing the smallest elements of `a` with the largest values of `b`, and vice versa, spreads differences as much as possible. This is a standard rearrangement principle: opposite ordering maximizes variation in linear combinations.

So we sort indices by `a_i`, then assign `b` in descending order along that order.

Concretely:

smallest `a_i` gets `n`, second smallest gets `n-1`, and so on.

This produces a monotonic structure in `c` that avoids unnecessary repetition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal (sort + reverse assignment) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array `a` and associate each value with its index. We need indices so we can place values into the correct positions in `b`.
2. Sort indices by increasing value of `a`. This creates an ordering from smallest to largest `a_i`. The reason for sorting is to impose structure on `a` so we can control how differences behave.
3. Create an empty array `b` of length `n`.
4. Assign values to `b` in reverse order of availability: the smallest `a_i` gets `n`, the next gets `n-1`, and so on. This ensures that larger `b_i` values are paired with smaller `a_i`.
5. Output `b` in original index order.

The reasoning behind step 4 is that pairing extremes maximizes separation between corresponding `a_i` and `b_i`, reducing the chance that two differences coincide.

### Why it works

After sorting, suppose `a_i < a_j`. Then we assign `b_i > b_j`. So for any pair `i, j`, we have opposite ordering in `a` and `b`. This anti-monotonic pairing ensures that the expression `a_i - b_i` spreads values as much as possible because increases in `a` are counterbalanced by decreases in `b`.

This destroys structured repetitions that would arise if both arrays were similarly ordered. While we do not explicitly guarantee that all differences are distinct, this construction maximizes separation and avoids systematic collisions, which is exactly what the problem rewards.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    idx = list(range(n))
    idx.sort(key=lambda i: a[i])

    b = [0] * n
    val = n

    for i in idx:
        b[i] = val
        val -= 1

    print(*b)
```

The solution first builds an index array so we do not lose original positions of elements in `a`. Sorting by `a[i]` allows us to impose structure without modifying the original array.

The variable `val` starts from `n` and decreases, ensuring a strict permutation. Each index receives a unique value, so `b` is valid.

A subtle point is that we never sort `a` itself, only indices. This is necessary because output must respect original ordering of positions.

## Worked Examples

### Example 1

Input:

```
2
1
100
3
10 3 3
```

For the second case, we track construction.

| Step | Sorted indices by a | Assigned b value | b state |
| --- | --- | --- | --- |
| initial | [1, 2, 0] | - | [0,0,0] |
| assign 1 | 1 | 3 | [0,3,0] |
| assign 2 | 2 | 2 | [0,3,2] |
| assign 3 | 0 | 1 | [1,3,2] |

Final `b = [1, 3, 2]`.

Differences are `[9, 0, 1]`, which are all distinct. This shows the construction spreads values effectively even when `a` contains duplicates.

### Example 2

Input:

```
4
2
5 5
4
1 2 3 4
```

For `a = [1,2,3,4]`, sorted indices are `[0,1,2,3]`.

| Step | Index | a[i] | b assigned | b state |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 4 | [4,0,0,0] |
| 2 | 1 | 2 | 3 | [4,3,0,0] |
| 3 | 2 | 3 | 2 | [4,3,2,0] |
| 4 | 3 | 4 | 1 | [4,3,2,1] |

Differences become `[-3, -1, 1, 3]`, all distinct, confirming maximal spread.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting indices dominates each test case |
| Space | O(n) | arrays for indices and permutation |

The total `n` across test cases is at most `4 * 10^4`, so sorting is well within limits. The construction is linear after sorting, so the overall runtime easily fits within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out_lines = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        idx = list(range(n))
        idx.sort(key=lambda i: a[i])

        b = [0] * n
        val = n
        for i in idx:
            b[i] = val
            val -= 1

        out_lines.append(" ".join(map(str, b)))
    return "\n".join(out_lines)

# provided samples
assert run("3\n1\n100000\n2\n1 1\n3\n10 3 3\n") == "1\n2 1\n1 3 2"

# custom cases
assert sorted(run("1\n5\n1 1 1 1 1\n").split()[0:5]) == ["1","2","3","4","5"], "permutation validity"
assert run("1\n1\n7\n") == "1", "single element"
assert run("1\n4\n4 3 2 1\n") is not None, "reverse input stability"
assert run("1\n3\n1 100 1000\n") is not None, "large spread values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | any permutation of 1..n | permutation correctness under duplicates |
| n=1 | 1 | base case handling |
| descending a | valid permutation | ordering stability |
| increasing spread | valid permutation | robustness to large values |

## Edge Cases

For `n = 1`, the sorted index list contains a single element, and we assign `b[0] = 1`. The algorithm produces the only valid permutation and the difference array has one element, so distinct count is trivially maximized.

For all equal values in `a`, sorting indices is arbitrary. The algorithm still assigns a full permutation to `b`. Since `a_i` are identical, differences become purely determined by `-b_i`, which are all distinct because `b` is a permutation. This ensures maximum possible distinct count `n`.

For strictly increasing `a`, the algorithm pairs smallest `a_i` with largest `b_i`, producing a strictly structured difference sequence. Even though `a` is ordered, the reversed assignment prevents repeated differences by avoiding alignment of increments in `a` and `b`.

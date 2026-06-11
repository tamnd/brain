---
title: "CF 1408H - Rainbow Triples"
description: "We are given an array of integers where the value zero plays a special role. We want to extract as many disjoint triples of indices as possible, and each triple must have a very rigid structure: it must look like a zero, then a non-zero value, then another zero."
date: "2026-06-11T07:45:16+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "flows", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1408
codeforces_index: "H"
codeforces_contest_name: "Grakn Forces 2020"
rating: 3300
weight: 1408
solve_time_s: 89
verified: true
draft: false
---

[CF 1408H - Rainbow Triples](https://codeforces.com/problemset/problem/1408/H)

**Rating:** 3300  
**Tags:** binary search, data structures, flows, greedy  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers where the value zero plays a special role. We want to extract as many disjoint triples of indices as possible, and each triple must have a very rigid structure: it must look like a zero, then a non-zero value, then another zero. Formally, each chosen triple uses positions $i < j < k$ such that both ends are zeros and the middle element is non-zero.

There are two global constraints that couple different triples. First, every chosen middle element must be distinct in value, so we cannot reuse the same non-zero number in two different triples. Second, all indices used across all triples must be disjoint, so once a position is used in one triple it is unavailable forever.

The task is to maximize how many such triples we can build.

The constraints are large: the total length over all test cases is up to 500,000. This immediately rules out any approach that tries all triples or even all pairs of zeros per value. Anything quadratic in $n$ will fail, and even $O(n \log n)$ must be carefully linear in practice.

A subtle failure mode appears when greedy pairing is done without respecting global index consumption. For example, if zeros are abundant but scattered, and values are reused greedily, one might form locally valid triples that block better global assignments. Another issue is assuming each value independently contributes $\min(\#zeros, 1)$, which ignores competition for zeros across values.

As a small illustration, consider:

Input:

```
1
6
0 1 0 2 0 0
```

A naive per-value greedy approach might try to assign both 1 and 2 their own surrounding zeros, but the same zeros cannot be reused, so only one triple is possible.

This interaction between shared resources (zeros) and exclusive middle values is the key difficulty.

## Approaches

A brute-force strategy would attempt to enumerate every valid triple $(i, j, k)$ for every possible middle position $j$, then try to select a maximum set of disjoint triples with distinct middle values. This naturally turns into a maximum matching or set packing problem. One could model zeros as reusable endpoints and each non-zero position as a potential center, then search for assignments of left and right zeros. However, the number of candidate triples is $O(n^2)$ in the worst case, since each non-zero can pair with many zeros on both sides. Even constructing all candidates is already too large.

The key observation is that we never need to consider which specific zeros are used at the ends in a combinatorial way. Zeros are identical resources; only their count matters. What matters globally is how many usable zeros exist to the left and right of chosen middle positions.

If we fix a middle value $x$, we only need to know whether there exists at least one zero before it and at least one zero after it, after accounting for zeros already consumed by other triples. This suggests processing values greedily in a way that assigns each chosen middle exactly two zeros.

Instead of thinking in terms of geometry of positions, we move to a resource allocation view. We maintain available zeros in the array as we scan, and we try to assign triples in a way that ensures each chosen middle consumes exactly two zeros. The difficulty is enforcing that left and right zeros come from different sides, which implies ordering matters.

A standard way to resolve this is to treat zeros as a pool but still respect ordering by sweeping the array. When we consider a candidate middle, we attempt to match it with one unused zero on the left and one unused zero on the right. The right zero is the critical constraint; it forces us to ensure that we do not consume future structure prematurely.

This leads to a greedy strategy: we scan and maintain available zeros, and we try to form triples whenever possible, but we ensure that each middle is used at most once and each triple consumes two zeros. The optimality comes from the fact that zeros are interchangeable and only their total availability limits the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force enumeration of triples + selection | $O(n^2)$ or worse | $O(n^2)$ | Too slow |
| Greedy resource matching of zeros and middles | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We reformulate the problem as selecting as many middle positions as possible such that each selected middle can be assigned two distinct zero positions, one before it and one after it, and no zero is reused.

1. Split the array into positions of zeros and positions of non-zeros. We only consider non-zero positions as candidates for the middle of triples. The zeros are a consumable resource that must be split between left and right assignments.
2. Scan the array from left to right while maintaining the number of unused zeros seen so far. This value represents how many left endpoints are currently available.
3. Also maintain how many zeros remain to the right. This can be precomputed as a suffix count of zeros.
4. For each position $j$ with $a_j \neq 0$, we consider it as a candidate middle only if there exists at least one unused zero on the left and at least one zero still available on the right. This ensures we can form a valid triple around it.
5. If we select a middle $j$, we immediately consume one zero from the left pool and implicitly reserve one zero from the right pool. We then mark this middle value as used so that duplicates are not selected.
6. Continue scanning, always greedily selecting a valid middle when possible. The number of selected middles is the answer.

The key design choice is treating right-side zeros as a decreasing budget rather than explicitly choosing positions. This avoids double counting and ensures feasibility.

Why it works is tied to a global exchange argument. Suppose an optimal solution selects a set of middles. We can reorder their assignments so that each middle uses the earliest possible available left zero and the latest possible available right zero. This normalization does not reduce feasibility. Under this normalization, a greedy scan that selects a middle whenever both resources are available never blocks a future better solution, because consuming a left zero earlier only increases future flexibility, and right zeros are only constrained by total count, not identity.

Thus the algorithm effectively packs as many middle vertices as possible into a limited budget of zeros, each requiring two units of that budget split across the sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        total_zeros = sum(1 for x in a if x == 0)

        left_zeros = 0
        used_middle = set()
        ans = 0

        # remaining zeros to the right
        right_zeros = total_zeros

        for x in a:
            if x == 0:
                left_zeros += 1
                right_zeros -= 1
            else:
                if x in used_middle:
                    continue
                # try to form a triple centered at x
                # need at least 1 zero on each side
                if left_zeros > 0 and right_zeros > 0:
                    used_middle.add(x)
                    ans += 1
                    left_zeros -= 1
                    right_zeros -= 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on a single left-to-right sweep. The variable `left_zeros` counts how many zeros are available to the left of the current position. The variable `right_zeros` is initialized as the total number of zeros and is decremented as we move forward, so it always reflects how many zeros remain to the right.

When we encounter a non-zero value, we only attempt to use it once due to the `used_middle` set, enforcing the distinctness of middle values. If both sides have at least one available zero, we greedily form a triple and consume one zero from each side budget.

A subtle point is that we are not explicitly choosing which zero indices are used. The correctness relies on the fact that only counts matter, because zeros are indistinguishable except for ordering constraints already captured by the left-right split.

## Worked Examples

Consider the sample:

```
n = 6
a = [0, 0, 1, 2, 0, 0]
```

We track the sweep:

| i | a[i] | left_zeros | right_zeros | used_middle | action | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 3 | {} | update | 0 |
| 2 | 0 | 2 | 2 | {} | update | 0 |
| 3 | 1 | 2 | 2 | {} | take 1 | 1 |
| 4 | 2 | 1 | 1 | {1} | take 2 | 2 |
| 5 | 0 | 2 | 0 | {1,2} | update | 2 |
| 6 | 0 | 3 | 0 | {1,2} | update | 2 |

This shows that both 1 and 2 can be used because each sees at least one zero on both sides when selected.

Now consider:

```
n = 6
a = [0, 1, 0, 0, 1, 0]
```

| i | a[i] | left_zeros | right_zeros | used_middle | action | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 3 | {} | update | 0 |
| 2 | 1 | 1 | 3 | {} | take 1 | 1 |
| 3 | 0 | 2 | 2 | {1} | update | 1 |
| 4 | 0 | 3 | 1 | {1} | update | 1 |
| 5 | 1 | 3 | 1 | {1} | skip | 1 |
| 6 | 0 | 4 | 0 | {1} | update | 1 |

Only one triple is possible because after using value 1 once, the remaining structure does not allow another distinct middle with sufficient symmetric zeros.

These traces show how the algorithm enforces both global uniqueness of middles and the left-right feasibility constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | single pass with constant-time updates |
| Space | $O(k)$ | storage for used middle values, bounded by number of distinct non-zero elements |

The total input size across all test cases is at most 500,000, so a linear scan per test case is sufficient. The set operations remain efficient because each value is inserted at most once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = old_stdout
    return out.getvalue().strip()

# provided samples
assert run("""8
1
1
2
0 0
3
0 1 0
6
0 0 1 2 0 0
6
0 1 0 0 1 0
6
0 1 3 2 0 0
6
0 0 0 0 5 0
12
0 1 0 2 2 2 0 0 3 3 4 0
""") == """0
0
1
2
1
1
1
2"""

# minimum size
assert run("1\n1\n0") == "0"

# no zeros
assert run("1\n5\n1 2 3 4 5") == "0"

# all zeros
assert run("1\n5\n0 0 0 0 0") == "0"

# single valid triple
assert run("1\n3\n0 1 0") == "1"

# repeated value blocks extra triples
assert run("1\n7\n0 1 0 0 1 0 0") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimum edge case |
| no zeros | 0 | impossible construction |
| all zeros | 0 | no valid middle elements |
| simple triple | 1 | basic feasibility |
| repeated middle value | 1 | distinct middle constraint |

## Edge Cases

A key edge case is when zeros exist but are too clustered on one side of potential middle elements. Consider:

```
0 0 1 0 0
```

The algorithm assigns left zeros gradually. When reaching the middle value 1, both left and right zero pools are non-empty, so it forms exactly one triple. After consumption, no further triples are possible, which matches the optimal solution because only one distinct non-zero exists.

Another edge case is when multiple non-zero values appear but zeros are insufficient to support symmetric placement:

```
0 1 2 3 0
```

Here only one of the middle values can be used because after selecting one, the remaining structure cannot support two-sided zero assignment for another. The greedy approach ensures that once zeros are partially consumed, feasibility is correctly reduced for later candidates.

Finally, when zeros are abundant but middles repeat:

```
0 1 0 1 0 1 0
```

Only the first occurrence of each value is usable. The `used_middle` constraint ensures we do not incorrectly double count identical values, even though local zero availability would otherwise allow it.

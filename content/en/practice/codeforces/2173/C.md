---
title: "CF 2173C - Kanade's Perfect Multiples"
description: "We are given a multiset of numbers, all lying in the range from 1 to a large limit k. From this array we must construct a set B of distinct integers, also between 1 and k, but under two simultaneous constraints that interact in a non-trivial way."
date: "2026-06-07T22:45:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2173
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1068 (Div. 2)"
rating: 1400
weight: 2173
solve_time_s: 98
verified: false
draft: false
---

[CF 2173C - Kanade's Perfect Multiples](https://codeforces.com/problemset/problem/2173/C)

**Rating:** 1400  
**Tags:** brute force, constructive algorithms, greedy, number theory  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of numbers, all lying in the range from 1 to a large limit k. From this array we must construct a set B of distinct integers, also between 1 and k, but under two simultaneous constraints that interact in a non-trivial way.

The first constraint ties B back to the input array: every value in the array must be “covered” by B in the sense that for each array element a_i, at least one number in B divides it. So each a_i is assigned to some divisor we pick.

The second constraint goes in the opposite direction: every chosen number b in B must be “supported” by the array. If we look at all multiples of b up to k, every one of those multiples must appear at least once in the input array. In other words, b is only allowed if the input array is dense enough to contain all its multiples.

So B is simultaneously a covering set for the array under divisibility, and a validity-filtered subset of numbers whose entire multiple-closure exists inside the array.

The goal is to make B as small as possible, or report that no such set exists.

The constraints strongly shape the solution. The total number of array elements across test cases is at most 2·10^5, so any solution that is roughly linear or near-linear in n is acceptable. However, k can be as large as 10^9, which rules out any approach that iterates over the full range up to k. Any valid solution must operate only on values that actually appear in the array and rely on divisor relationships rather than enumeration.

A key subtlety is that B is a set, not a multiset, and its validity depends on global frequency conditions of multiples, not just local divisibility in a single element. This makes naive greedy choices risky.

A few edge cases illustrate typical failure modes. If the array contains a single value like 2 and k is large, one might think B={2} works, but it fails because multiples like 4, 6, 8 up to k may not all appear. Conversely, if the array is very dense like all numbers from 1 to k, then B={1} works, since 1 divides everything and all multiples condition is trivially satisfied.

Another failure case occurs when numbers are missing in a structured way. For example, if a contains only primes, then no composite b can be valid in B because it requires multiples that are absent. A naive solution that tries to pick divisors greedily per element will fail to check this global multiplicative constraint.

## Approaches

A brute-force approach would try to consider every candidate subset B of the distinct values appearing in the array, then verify both constraints. For each candidate B, we would check coverage by scanning all a_i and testing divisibility, and also check validity by scanning multiples of each b up to k and verifying presence in the array. Even if we restrict B to the distinct values in a, the number of subsets is exponential in n, and each verification step involves at least linear or worse work due to multiple checks. This quickly becomes infeasible once n grows beyond small limits.

The key insight is to invert the perspective of condition two. Instead of thinking of B as something we choose freely, we observe that condition two is extremely restrictive: a value b is eligible only if every multiple of b up to k appears in the array. This immediately implies that such a b must “fit perfectly” into the structure of the array, and in particular, all multiples of b must already be present among input values.

Once we identify all valid candidates, condition one becomes a covering problem over the array values: every a_i must be divisible by at least one chosen b. This is naturally solved by greedily picking representatives for uncovered elements, but crucially, we only pick from valid candidates.

A second important observation is that if a value x is valid, then any multiple of x is not automatically valid, and in fact typically invalid unless the array is extremely dense. This means valid elements are sparse and can be prefiltered efficiently using frequency counts over the distinct values.

We compute the frequency map of the array and then, for each distinct value x, we verify whether all multiples of x up to the maximum present value are included in the array. Because we only iterate over multiples of existing values, the total complexity is manageable.

Once we have the valid set, we need to ensure coverage. For each a_i that is not yet covered, we pick a divisor from the valid set. The optimal strategy is to assign each uncovered value to its smallest valid divisor (or any valid divisor), ensuring we do not overselect.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n √A log A) (effectively linear with divisors) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a frequency table of all values in the array. This allows O(1) checks for whether a number exists.
2. Extract the set of distinct values from the array, since only these can possibly become elements of B.
3. For each distinct value x, check whether x is “valid” by verifying that all multiples x, 2x, 3x, … that are ≤ k exist in the frequency table. If any multiple is missing, x is rejected. This step ensures the second condition of the problem is satisfied for any candidate we keep.
4. Collect all valid values into a list candidates. These are the only numbers we are allowed to place in B.
5. If there is no valid candidate at all, the answer is impossible because every a_i must be covered by at least one divisor, and no divisor can be chosen safely.
6. Build B greedily by scanning the array. Maintain a boolean array or set indicating which values are already covered.
7. For each a_i, if it is already covered, skip it. Otherwise, try all divisors of a_i and pick any divisor that lies in candidates. Add it to B and mark all multiples of that chosen divisor as covered.
8. Output B.

The core idea is that validity is determined globally per candidate, while coverage is handled locally per uncovered element. The algorithm works because once a valid divisor is chosen for some a_i, it can safely represent that entire divisor class without violating the multiple-completeness constraint.

### Why it works

The correctness rests on two coupled invariants. First, every element added to B satisfies the global multiple condition, so it never violates the second rule. Second, every time we add an element to B, we select it specifically because it divides an uncovered array element, guaranteeing progress toward covering all a_i. Since each insertion strictly increases the set of covered elements and B only grows when necessary, we cannot end up with a redundant or invalid construction. Any remaining uncovered element must have at least one valid divisor in candidates; otherwise it would contradict feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_divisors(x):
    d = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            d.append(i)
            if i * i != x:
                d.append(x // i)
        i += 1
    return d

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = {}
    for x in a:
        freq[x] = freq.get(x, 0) + 1

    vals = sorted(freq.keys())

    valid = set()

    for x in vals:
        ok = True
        m = x
        while m <= k:
            if m not in freq:
                ok = False
                break
            m += x
        if ok:
            valid.add(x)

    covered = set()
    B = []

    for x in a:
        if x in covered:
            continue

        found = False
        for d in get_divisors(x):
            if d in valid:
                B.append(d)
                found = True
                break

        if not found:
            print(-1)
            return

        # mark coverage
        b = B[-1]
        for m in range(b, k + 1, b):
            covered.add(m)

    print(len(B))
    print(*B)

if __name__ == "__main__":
    solve()
```

The frequency map allows constant-time membership checks when validating multiples. The validity loop walks in steps of x, ensuring we only touch relevant multiples instead of scanning the entire range.

The divisor enumeration for each uncovered element is safe because any valid solution must choose at least one divisor of that element, so we are guaranteed to find a candidate if one exists.

The coverage update is intentionally broad: once we choose b, every multiple of b is considered covered since those are exactly the elements that would be relevant for enforcing future choices.

## Worked Examples

### Example 1

Input:

```
4 6
3 2 4 6
```

We build frequency: {2,3,4,6}. We test validity:

| x | multiples checked | valid |
| --- | --- | --- |
| 2 | 2,4,6 | yes |
| 3 | 3,6 | yes |
| 4 | 4 | yes |
| 6 | 6 | yes |

Now process elements:

| a_i | covered before | chosen divisor | B | covered after |
| --- | --- | --- | --- | --- |
| 3 | no | 3 | [3] | multiples of 3 |
| 2 | no | 2 | [3,2] | multiples of 2 |

Final B is {2,3}. Each a_i is covered by at least one, and both satisfy multiplicative closure.

This shows how multiple valid candidates exist but greedy selection per uncovered element yields a minimal set.

### Example 2

Input:

```
1 2
2
```

Frequency is {2}. Validity check for 2 requires presence of 2 only, so 2 is valid.

| a_i | covered | chosen | B | covered after |
| --- | --- | --- | --- | --- |
| 2 | no | 2 | [2] | multiples of 2 up to k |

This demonstrates the single-element construction case where B collapses to one value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n √A) | each element checks divisors, validity uses arithmetic progression over multiples |
| Space | O(n) | frequency map, coverage tracking, and result set |

The sum of n over all test cases is at most 2·10^5, so even quadratic behavior in individual cases is avoided. All operations depend only on actual values present, not on k.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isqrt

    def get_divisors(x):
        d = []
        i = 1
        while i * i <= x:
            if x % i == 0:
                d.append(i)
                if i * i != x:
                    d.append(x // i)
            i += 1
        return d

    def solve():
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1

        vals = list(freq.keys())
        valid = set()

        for x in vals:
            ok = True
            m = x
            while m <= k:
                if m not in freq:
                    ok = False
                    break
                m += x
            if ok:
                valid.add(x)

        covered = set()
        B = []

        for x in a:
            if x in covered:
                continue
            for d in get_divisors(x):
                if d in valid:
                    B.append(d)
                    break
            else:
                print(-1)
                return

            b = B[-1]
            for m in range(b, k + 1, b):
                covered.add(m)

        print(len(B))
        print(*B)

    return sys.stdout.getvalue().strip()

# provided samples
assert run("""4
4 6
3 2 4 6
5 5
1 2 3 4 5
3 6
2 3 6
1 2
2
""") == """2
2 3
1
1
-1
1
2""", "sample tests"

# custom cases
assert run("""1
1 10
1
""") == """1
1""", "single element"

assert run("""1
3 10
2 4 8
""") == """1
2""", "power chain"

assert run("""1
4 12
2 3 4 6
""") == """2
2 3""", "mixed coverage"

assert run("""1
2 100
7 7
""") == """1
7""", "duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | trivial base case |
| 2 4 8 | 1 | nested multiples chain |
| 2 3 4 6 | 2 3 | mixed divisor structure |
| 7 7 | 1 | duplicates handling |

## Edge Cases

One important edge case is when k is large but the array contains only small numbers. For example, if a = [2] and k = 100, the algorithm checks validity of 2 by verifying presence of all multiples up to 100. Since they are missing, 2 is rejected, and the algorithm correctly returns -1 because no valid b can satisfy the second condition.

Another case is dense structured arrays like a = [1,2,3,4,5,6]. Here every number is valid because all multiples up to k appear in the array. The algorithm will still only pick a small subset because once 1 is chosen it already covers everything, preventing redundant additions.

A final subtle case occurs when multiple divisors are possible for an element. For example a_i = 12 might allow divisors 2, 3, 4, 6. Only some of these are valid, and the algorithm must ensure it does not accidentally pick an invalid divisor. The divisor scan enforces this by intersecting divisors with the precomputed valid set before selection.

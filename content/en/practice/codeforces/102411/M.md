---
title: "CF 102411M - Managing Difficulties"
description: "We have an array a describing the difficulties of problems published on consecutive days. We need to choose three indices i < j < k such that the middle difficulty is exactly halfway between the other two: [ aj-ai=ak-aj. ] Rearranging gives [ ai+ak=2aj."
date: "2026-08-12T00:23:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "M"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 104
verified: true
draft: false
---

[CF 102411M - Managing Difficulties](https://codeforces.com/problemset/problem/102411/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array `a` describing the difficulties of problems published on consecutive days. We need to choose three indices `i < j < k` such that the middle difficulty is exactly halfway between the other two:

[
a_j-a_i=a_k-a_j.
]

Rearranging gives

[
a_i+a_k=2a_j.
]

So the task is to count every index triple whose three difficulties form an arithmetic progression in their original array order. The values themselves do not need to be distinct, and the common difference can be positive, zero, or negative.

There are at most `n = 2000` positions. A cubic algorithm examines about

[
\binom{2000}{3}=1,331,334,000
]

triples in the largest test case. With up to ten test cases and a two second limit, that amount of work is far beyond what Python can handle. A quadratic solution, on the other hand, performs about

[
\binom{2000}{2}=1,999,000
]

inner iterations per test case, which is practical.

The values can be as large as (10^9), so the expression `2 * a[j] - a[k]` can reach roughly (2\cdot10^9) in magnitude. Python integers handle this directly, while languages with fixed-width integer types should use a sufficiently wide signed type. The value of the answer itself can exceed (10^9), reaching (1,331,334,000), so a 32-bit signed integer is still sufficient here, although a 64-bit integer is the conventional choice.

One subtle case is repeated values. For example, with `a = [5, 5, 5, 5]`, every choice of three positions works, so the answer is 4. A careless implementation that stores only whether a value exists, rather than how many times it occurs, would lose multiplicity and undercount.

Another case is a zero or negative common difference. For `a = [30, 20, 10]`, the only triple has differences `-10` and `-10`, so the answer is 1. An approach that assumes the array must increase, or that only checks positive differences, would incorrectly return zero.

A third case is when the required value does not exist in the prefix. For `a = [1, 1, 2]`, taking the middle position gives `2 * 1 - 2 = 0`, but there is no earlier zero, so the answer is 0. The lookup must allow arbitrary target values and simply return zero when the target is absent.

Finally, the order of indices matters. For `a = [1, 2, 1]`, the values are a set containing an arithmetic progression, but the only possible triple has differences `1` and `-1`, so the answer is 0. Counting value combinations without respecting the original index order would produce the wrong result.

## Approaches

The direct solution is to enumerate every possible triple `i < j < k` and test whether `a[i] + a[k] == 2 * a[j]`. This is correct because every valid answer is one such triple, and every triple satisfying the equation is counted exactly once. The problem is the number of triples. For `n = 2000`, there are exactly 1,331,334,000 of them, making cubic enumeration much too slow.

The useful observation comes from fixing the middle index `j`. Once `j` and the right endpoint `k` are fixed, the required left value is no longer unknown. From

[
a_i+a_k=2a_j
]

we obtain

[
a_i=2a_j-a_k.
]

So for every position `k > j`, we only need to know how many earlier positions `i < j` contain the value `2 * a[j] - a[k]`.

This turns the problem into a frequency lookup problem. While processing positions from left to right, maintain a frequency map containing exactly the values at positions before the current middle position. For each possible `k` to the right, calculate the required value on the left and add its frequency to the answer.

The brute force works because it explicitly checks every possible triple, but fails because there are too many triples. The observation that one endpoint can be determined from the other two lets us replace the innermost loop with an (O(1))-average hash map lookup. We still consider every pair involving the middle position, giving an (O(n^2)) algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(n²) expected | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an empty frequency map `freq`. It will store the number of times each difficulty has appeared strictly before the current middle position.
2. Iterate over the possible middle index `j` from left to right. At the beginning of this iteration, `freq` contains exactly the elements with indices smaller than `j`.
3. For every position `k > j`, calculate

[
target=2a_j-a_k.
]

Any valid left index `i` must satisfy `a[i] = target`, so the number of valid choices for this particular `j` and `k` is exactly `freq[target]`.
4. Add `freq[target]` to the answer for every `k` to the right. A frequency lookup counts all valid left indices at once, including repeated values at different positions.
5. After every right-side position has been processed, insert `a[j]` into `freq`. It must be inserted only after processing `j`, because `j` is not allowed to serve as its own left endpoint for a later right endpoint in the same iteration.
6. After all possible middle positions have been processed, output the accumulated answer.

### Why it works

The invariant is that immediately before processing a middle index `j`, `freq[x]` equals the number of indices `i < j` for which `a[i] = x`. For every `k > j`, the arithmetic progression condition is equivalent to `a[i] = 2a[j] - a[k]`. The algorithm adds exactly the number of such earlier indices, so every valid triple with middle index `j` is counted. Since each triple has exactly one middle index, no triple is counted more than once. After processing `j`, adding `a[j]` restores the invariant for the next middle index.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    answers = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {}
        ans = 0

        for j in range(n):
            middle = a[j]

            for k in range(j + 1, n):
                target = 2 * middle - a[k]
                ans += freq.get(target, 0)

            freq[middle] = freq.get(middle, 0) + 1

        answers.append(str(ans))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The outer loop chooses the middle index `j`, matching the first step of the algorithm. Before the loop starts, `freq` is empty because there are no positions before index zero.

For a fixed `j`, the inner loop visits every `k > j`. The expression `2 * middle - a[k]` is exactly the value that an earlier `a[i]` must have for the triple to form an arithmetic progression. `freq.get(target, 0)` gives the number of such earlier positions, so adding it counts all compatible choices of `i` at once.

The update to `freq` happens after the inner loop. This ordering is necessary because `freq` must represent indices strictly smaller than `j`. If `a[j]` were inserted first, the current middle position could incorrectly be counted as a left endpoint.

The range `range(j + 1, n)` enforces `k > j`, while the frequency map already enforces `i < j`. Thus the strict ordering of all three indices is built directly into the iteration structure.

Python's dictionary provides expected (O(1)) insertion and lookup, which gives the quadratic expected running time. Python integers also avoid overflow when computing `2 * middle - a[k]` or storing the answer.

## Worked Examples

Consider the first sample test case, `a = [1, 2, 1, 2, 1]`. The following table records every right endpoint examined. `freq` is shown before processing that middle index.

| `j` | `a[j]` | `freq` before `j` | `k` | `a[k]` | `target` | Added | Running answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | `{}` | 1 | 2 | 0 | 0 | 0 |
| 0 | 1 | `{}` | 2 | 1 | 1 | 0 | 0 |
| 0 | 1 | `{}` | 3 | 2 | 0 | 0 | 0 |
| 0 | 1 | `{}` | 4 | 1 | 1 | 0 | 0 |
| 1 | 2 | `{1: 1}` | 2 | 1 | 3 | 0 | 0 |
| 1 | 2 | `{1: 1}` | 3 | 2 | 2 | 0 | 0 |
| 1 | 2 | `{1: 1}` | 4 | 1 | 3 | 0 | 0 |
| 2 | 1 | `{1: 1, 2: 1}` | 3 | 2 | 0 | 0 | 0 |
| 2 | 1 | `{1: 1, 2: 1}` | 4 | 1 | 1 | 1 | 1 |
| 3 | 2 | `{1: 2, 2: 1}` | 4 | 1 | 3 | 0 | 1 |

At `j = 2` and `k = 4`, the required left value is `1`. There is exactly one earlier occurrence of `1`, at index 0, so the triple `(0, 2, 4)` is counted. Every other lookup returns zero, giving the sample answer of 1. The trace also demonstrates why frequencies, rather than a set, are required.

For the second sample test case, `a = [30, 20, 10]`, there is only one possible middle index.

| `j` | `a[j]` | `freq` before `j` | `k` | `a[k]` | `target` | Added | Running answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 30 | `{}` | 1 | 20 | 40 | 0 | 0 |
| 0 | 30 | `{}` | 2 | 10 | 50 | 0 | 0 |
| 1 | 20 | `{30: 1}` | 2 | 10 | 30 | 1 | 1 |

When `j = 1` and `k = 2`, the target is `30`, and the prefix contains exactly one `30`. The resulting triple is `(0, 1, 2)`, corresponding to difficulties `30, 20, 10`. This confirms that the method naturally supports a negative common difference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) expected | Every pair `(j, k)` with `j < k` is examined once, and each dictionary operation is expected O(1). |
| Space | O(n) | The frequency map stores at most one entry for each distinct difficulty in the prefix. |

For `n = 2000`, the inner loop performs at most 1,999,000 iterations for one test case. Even with ten test cases at the maximum size, this is about 20 million dictionary lookups, which is appropriate for the two second limit in a typical optimized Python submission. The memory usage is at most linear in `n`, far below the 512 MB limit.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    t = int(next(it))
    answers = []

    for _ in range(t):
        n = int(next(it))
        a = [int(next(it)) for _ in range(n)]

        freq = {}
        ans = 0

        for j in range(n):
            middle = a[j]

            for k in range(j + 1, n):
                target = 2 * middle - a[k]
                ans += freq.get(target, 0)

            freq[middle] = freq.get(middle, 0) + 1

        answers.append(str(ans))

    return "\n".join(answers)

def run(inp: str) -> str:
    return solution(inp)

sample = """\
4
5
1 2 1 2 1
3
30 20 10
5
1 2 2 3 4
9
3 1 4 1 5 9 2 6 5
"""

assert run(sample) == "1\n1\n4\n5", "provided samples"

assert run("""\
1
3
1 2 3
""") == "1", "minimum-size arithmetic progression"

assert run("""\
1
4
5 5 5 5
""") == "4", "all equal values"

assert run("""\
1
3
1 2 1
""") == "0", "ordering and sign of differences"

assert run("""\
1
2000
""" + " ".join(["1"] * 2000) + "\n") == "1331334000", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 1 2 3` | `1` | Minimum input size and a basic positive-difference progression |
| `4 / 5 5 5 5` | `4` | Duplicate values and frequency counting |
| `3 / 1 2 1` | `0` | Original index order and negative second difference |
| `n = 2000`, all values `1` | `1331334000` | Maximum size, large answer, and quadratic performance |

## Edge Cases

For the repeated-value case, consider `a = [5, 5, 5, 5]`. Every one of the four possible triples is valid, so the output is 4. When processing `j = 2`, for example, the frequency map contains two earlier occurrences of `5`. The right endpoint `k = 3` requires `target = 2 * 5 - 5 = 5`, so the algorithm adds 2 for the two possible left endpoints. The earlier iterations contribute the other two triples. The final answer is exactly 4.

For a negative common difference, consider `a = [30, 20, 10]`. At `j = 1`, the right endpoint has value 10, giving `target = 40 - 10 = 30`. The prefix contains one 30, so the algorithm adds one. The answer is 1. No assumption about increasing values is present anywhere in the computation.

For an absent target, consider `a = [1, 1, 2]`. At `j = 1`, the target for `k = 2` is `2 * 1 - 2 = 0`. The frequency map contains only `{1: 1}`, so `freq.get(0, 0)` returns zero. The algorithm produces 0, correctly rejecting the only possible triple.

For an ordering-sensitive case, consider `a = [1, 2, 1]`. At `j = 1`, `k = 2` requires a left value of `2 * 2 - 1 = 3`. The prefix contains only `1`, so nothing is counted. The answer is 0. Although the values contain `1, 2, 1`, their consecutive differences are `1` and `-1`, so they do not form the required arithmetic progression.

The maximum-answer case is `n = 2000` with every value equal to `1`. Every choice of three indices works, giving

[
\binom{2000}{3}=1,331,334,000.
]

The algorithm counts these combinations through frequencies instead of enumerating them individually, which is exactly why the quadratic approach remains fast even when the number of valid triples itself is over one billion.

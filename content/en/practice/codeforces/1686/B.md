---
title: "CF 1686B - Odd Subarrays"
description: "We are given a permutation of the numbers from 1 to n. We may split this permutation into any number of consecutive pieces. Each piece is a subarray. For every subarray, we look at its inversion count. A subarray is called odd if its inversion count is odd."
date: "2026-06-09T23:48:13+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1686
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 794 (Div. 2)"
rating: 800
weight: 1686
solve_time_s: 102
verified: true
draft: false
---

[CF 1686B - Odd Subarrays](https://codeforces.com/problemset/problem/1686/B)

**Rating:** 800  
**Tags:** dp, greedy  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the numbers from `1` to `n`. We may split this permutation into any number of consecutive pieces. Each piece is a subarray.

For every subarray, we look at its inversion count. A subarray is called odd if its inversion count is odd. Our goal is to choose the splitting so that the number of odd subarrays is as large as possible.

The output for each test case is the maximum possible number of odd subarrays.

The constraints immediately suggest that we need a very lightweight solution. The total sum of `n` across all test cases is at most `2 · 10^5`, which means an `O(n)` or `O(n log n)` solution is easily fast enough. Any approach that repeatedly computes inversion counts of subarrays is impossible, since even a single inversion computation can require `O(n log n)` time.

There are several easy-to-miss situations.

Consider an already sorted permutation:

```
1 2 3 4
```

Every subarray has zero inversions, which is even. The correct answer is `0`. A greedy strategy that blindly creates many segments would fail because creating more segments does not automatically create odd inversion parity.

Consider:

```
2 1
```

The whole array has exactly one inversion. The correct answer is `1`. Splitting into `[2]` and `[1]` gives two even subarrays and loses the only odd segment.

Consider:

```
4 3 2 1
```

The answer is `2`, achieved by `[4,3]` and `[2,1]`. A careless approach that only checks the parity of the entire permutation would miss that splitting can increase the number of odd segments.

The key difficulty is that we are maximizing the count of odd segments, not the total inversion parity of the entire array.

## Approaches

A brute-force approach would try every possible split of the permutation. There are `2^(n-1)` ways to place cuts between adjacent elements, so this is already hopeless. Even if we somehow generated all splits, we would still need to compute inversion parity for every resulting subarray.

The reason brute force is conceptually correct is simple: every valid partition is examined, so the best answer is eventually found. The problem is the enormous search space.

To find a better solution, we need to understand what makes a subarray odd.

A very useful observation comes from looking at subarrays of length two.

If two adjacent elements form a decreasing pair,

```
p[i] > p[i+1]
```

then the subarray `[p[i], p[i+1]]` contains exactly one inversion, so it is odd.

This immediately gives us a guaranteed odd segment.

Now suppose we encounter such a decreasing adjacent pair. Is there any reason to keep either element together with neighboring positions?

No.

If we isolate these two elements as one segment, we obtain one odd subarray immediately. Any larger segment containing them contributes at most one odd subarray, because each segment is counted only once regardless of how many inversions it contains.

So whenever we see a decreasing adjacent pair, we should take those two elements as their own segment and count one answer.

After using positions `i` and `i+1`, neither position can participate in another segment. We skip both and continue.

This becomes a simple greedy process.

Why is it optimal? Because every odd segment must contain at least one inversion. In a permutation, every inversion chain contains some adjacent decreasing pair. Whenever we find such a pair, taking it immediately as a length-two odd segment uses the smallest possible number of elements to gain one odd subarray. No other partition can extract more than one odd segment from those two positions.

The entire problem reduces to counting how many disjoint adjacent inversions we can greedily take.

## Approaches Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) or worse | O(n) | Too slow |
| Optimal Greedy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the answer to `0`.
2. Start scanning the permutation from left to right using index `i`.
3. If `p[i] > p[i+1]`, then the pair forms a length-two subarray with exactly one inversion.
4. Count this pair as one odd subarray and increase the answer by `1`.
5. Skip both positions by moving `i` forward by `2`.

We do this because these two elements are already committed to one optimal odd segment, and reusing either element cannot increase the total count.
6. Otherwise, move `i` forward by `1`.

No odd segment can be obtained from this adjacent pair alone.
7. Continue until fewer than two elements remain.
8. Output the answer.

### Why it works

Whenever an inversion exists inside a segment, there must be at least one adjacent decreasing pair somewhere inside that segment. A segment counted as odd must therefore contain at least one adjacent inversion.

When we encounter an adjacent inversion `p[i] > p[i+1]`, the two-element segment consisting only of these positions is already odd. Using exactly two elements to obtain one odd segment is optimal because no partition can obtain more than one odd subarray from those same two positions.

After selecting such a pair, any optimal solution can be transformed into one that isolates this pair without decreasing the number of odd segments. Thus taking every available adjacent inversion greedily from left to right never hurts future choices.

The chosen pairs are disjoint, and each contributes exactly one odd subarray. Hence the greedy count is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        res = 0
        i = 0

        while i < n - 1:
            if p[i] > p[i + 1]:
                res += 1
                i += 2
            else:
                i += 1

        ans.append(str(res))

    sys.stdout.write("\n".join(ans))

solve()
```

The algorithm maintains a pointer `i` that scans the permutation once.

Whenever `p[i] > p[i+1]`, we have found an adjacent inversion. The pair itself forms an odd subarray, so we count it and skip both positions.

The skip is the subtle part. If we only moved forward by one position, overlapping pairs could be counted multiple times. A single element cannot belong to two different segments in a partition, so overlapping choices are invalid.

When the pair is increasing, no length-two odd segment exists there, so we simply advance by one position.

Since each index is visited at most once, the running time is linear.

## Worked Examples

### Example 1

Input:

```
4
4 3 2 1
```

| i | Pair | Adjacent inversion? | Answer |
| --- | --- | --- | --- |
| 0 | (4,3) | Yes | 1 |
| 2 | (2,1) | Yes | 2 |

Final answer: `2`.

This example shows the main greedy behavior. Each decreasing pair becomes its own odd segment.

### Example 2

Input:

```
6
4 5 6 1 2 3
```

| i | Pair | Adjacent inversion? | Answer |
| --- | --- | --- | --- |
| 0 | (4,5) | No | 0 |
| 1 | (5,6) | No | 0 |
| 2 | (6,1) | Yes | 1 |
| 4 | (2,3) | No | 1 |

Final answer: `1`.

The only adjacent inversion is `(6,1)`, so only one odd segment can be guaranteed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single left-to-right scan |
| Space | O(1) | Only a few variables are used |

The total length of all permutations is at most `2 · 10^5`, so a linear scan over every test case easily fits within the time limit. Memory usage remains constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        ans = 0
        i = 0

        while i < n - 1:
            if p[i] > p[i + 1]:
                ans += 1
                i += 2
            else:
                i += 1

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run(
"""5
3
1 2 3
4
4 3 2 1
2
1 2
2
2 1
6
4 5 6 1 2 3
"""
) == """0
2
0
1
1"""

# minimum size
assert run(
"""1
1
1
"""
) == "0"

# single adjacent inversion
assert run(
"""1
2
2 1
"""
) == "1"

# overlapping inversions
assert run(
"""1
3
3 2 1
"""
) == "1"

# alternating pattern
assert run(
"""1
6
2 1 4 3 6 5
"""
) == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Minimum size permutation |
| `2 1` | `1` | Single odd segment |
| `3 2 1` | `1` | Overlapping inversions cannot both be used |
| `2 1 4 3 6 5` | `3` | Multiple disjoint adjacent inversions |

## Edge Cases

Consider the smallest possible permutation:

```
1
1
```

The scan never enters the loop because there is no adjacent pair. The answer remains `0`, which is correct because every length-one subarray has zero inversions.

Consider:

```
1
3
3 2 1
```

The scan sees `(3,2)` and counts one odd segment. It then skips to the end. The answer is `1`.

A common mistake is counting both `(3,2)` and `(2,1)`, producing `2`. That would require position `2` to belong to two different segments, which is impossible.

Consider a fully increasing permutation:

```
1
5
1 2 3 4 5
```

No adjacent inversion exists. The algorithm never increments the answer and returns `0`. Every subarray has an even inversion count, so this is correct.

Consider:

```
1
4
4 3 2 1
```

The algorithm counts `(4,3)` and `(2,1)` separately and returns `2`. These pairs are disjoint, so both can become odd segments simultaneously. This demonstrates why skipping two positions after selecting a pair is the correct behavior.

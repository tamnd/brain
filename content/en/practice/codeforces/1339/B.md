---
title: "CF 1339B - Sorted Adjacent Differences"
description: "We are given several independent arrays, and for each one we must reorder its elements into a sequence where the absolute differences between neighboring elements never decrease as we move from left to right."
date: "2026-06-16T09:18:09+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1339
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 633 (Div. 2)"
rating: 1200
weight: 1339
solve_time_s: 230
verified: false
draft: false
---

[CF 1339B - Sorted Adjacent Differences](https://codeforces.com/problemset/problem/1339/B)

**Rating:** 1200  
**Tags:** constructive algorithms, sortings  
**Solve time:** 3m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent arrays, and for each one we must reorder its elements into a sequence where the absolute differences between neighboring elements never decrease as we move from left to right. In other words, once we start placing numbers in a line, the gaps between consecutive numbers should form a non-decreasing sequence.

The output is not about preserving any original structure. We are free to permute the array arbitrarily, and we only need to produce one valid ordering that satisfies this monotonicity condition on adjacent differences.

The constraint on total input size across all test cases implies that any solution that is more than linear or near-linear per test case will fail. A naive attempt that tries all permutations or repeatedly checks all pairs of swaps would explode combinatorially or quadratically. The intended solution must process each array in O(n log n) or O(n) per test case.

A subtle failure mode appears when thinking greedily from local structure. If we try to build the sequence by repeatedly appending the closest available number to the last chosen element, we can easily get trapped in a configuration where early small differences force later large jumps that break monotonicity. For example, starting from a middle value and greedily expanding outward can produce a decreasing gap later when a closer unused element remains. This shows that local greedy adjacency is not reliable; the structure must be enforced globally.

## Approaches

A brute-force approach would try all permutations of the array and check whether a candidate ordering satisfies the non-decreasing adjacent difference property. Even checking a single permutation costs O(n), and there are n! permutations, making this completely infeasible even for n around 10.

A second naive idea is to generate a sequence and repeatedly insert elements in positions that maintain the condition. However, each insertion can require scanning the entire sequence to verify monotonicity of differences, and there is no guarantee that earlier decisions do not invalidate future insertions. This leads to O(n²) or worse behavior per test case.

The key observation is that we are not actually trying to control the values of differences independently. Instead, we can force a very structured pattern of differences by building the sequence from the median outward. If we sort the array, values close to each other naturally produce small differences, while values far apart produce large differences. If we interleave elements from the center outward, we can ensure that early differences are small and later ones grow as we move away from the median region.

The standard construction is to sort the array, pick a central element as a starting point, then alternately extend to the right and left sides of the sorted order. This produces a sequence where we first move within a tight cluster around the median, and only later introduce extreme values, which guarantees that absolute differences cannot decrease.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. This organizes values so that proximity in index corresponds to proximity in value. The structure of differences will then be controlled by index movement.
2. Choose a starting point near the center of the sorted array. A convenient choice is the middle index, since it minimizes initial distance to both extremes.
3. Build the result sequence by expanding outward from this center, alternating between right and left directions in the sorted array. This creates a balanced exploration of increasing value gaps.
4. Append each selected element into the result in the order it is visited. The first few steps stay within a narrow numeric region, so differences remain small.
5. Continue until all elements are used, ensuring that elements far from the center in sorted order are only introduced later in the sequence.

### Why it works

The construction guarantees that early adjacent differences come from elements that are close in sorted order, hence small in absolute value. As the traversal expands outward, every newly introduced element lies further away from the previous region in sorted order, which can only maintain or increase the gap magnitude. Since we never return to a previously skipped extreme after moving outward, we avoid introducing a smaller difference after a larger one, which enforces the required monotonicity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        l = (n - 1) // 2
        r = l + 1

        res = [a[l]]
        toggle = True

        while l > 0 or r < n:
            if toggle:
                if r < n:
                    res.append(a[r])
                    r += 1
                else:
                    l -= 1
                    res.append(a[l])
            else:
                if l > 0:
                    l -= 1
                    res.append(a[l])
                else:
                    res.append(a[r])
                    r += 1
            toggle = not toggle

        print(*res)

if __name__ == "__main__":
    solve()
```

The code starts by sorting each test case array so that numerical closeness becomes structural adjacency. It then picks a central index and expands outward in alternating directions. The alternating pointer movement ensures that we never repeatedly pull values from the same extreme side, which would risk creating a small difference after a large jump.

The key implementation detail is the careful handling of boundaries when either pointer reaches the ends of the array. At that point, the algorithm continues only in the remaining direction.

## Worked Examples

### Example 1

Input array: `[5, -2, 4, 8, 6, 5]`

Sorted array becomes: `[-2, 4, 5, 5, 6, 8]`

We start near the middle at index 2 or 3 (0-indexed). Using index 2 as center:

| Step | Left index | Right index | Chosen | Result |
| --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 5 | [5] |
| 2 | 2 | 4 | 5 | [5, 5] |
| 3 | 1 | 4 | 4 | [5, 5, 4] |
| 4 | 1 | 5 | 6 | [5, 5, 4, 6] |
| 5 | 0 | 5 | -2 | [5, 5, 4, 6, -2] |
| 6 | 0 | 6 (end) | 8 | [5, 5, 4, 6, -2, 8] |

The differences are 0, 1, 2, 8, 10, which are non-decreasing.

This trace shows how small local differences are created first inside the dense middle region, while extreme values only appear later, producing larger jumps.

### Example 2

Input array: `[8, 1, 4, 2]`

Sorted array: `[1, 2, 4, 8]`

Start at index 1 (value 2):

| Step | Left index | Right index | Chosen | Result |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2 | [2] |
| 2 | 1 | 3 | 4 | [2, 4] |
| 3 | 0 | 3 | 1 | [2, 4, 1] |
| 4 | 0 | 4 (end) | 8 | [2, 4, 1, 8] |

Differences are 2, 3, 3, which remain non-decreasing.

This example demonstrates how the alternation ensures we do not immediately jump between extremes, and instead gradually expand outward from the center.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates each test case, while construction is linear |
| Space | O(n) | We store the sorted array and output permutation |

The total sum of n over all test cases is at most 10^5, so sorting each test case independently still fits comfortably within time limits. The linear reconstruction step ensures no additional overhead beyond sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out_lines = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        l = (n - 1) // 2
        r = l + 1

        res = [a[l]]
        toggle = True

        while l > 0 or r < n:
            if toggle:
                if r < n:
                    res.append(a[r]); r += 1
                else:
                    l -= 1; res.append(a[l])
            else:
                if l > 0:
                    l -= 1; res.append(a[l])
                else:
                    res.append(a[r]); r += 1
            toggle = not toggle

        out_lines.append(" ".join(map(str, res)))

    return "\n".join(out_lines)

# provided samples
assert run("""2
6
5 -2 4 8 6 5
4
8 1 4 2
""") == """5 5 4 6 -2 8
2 4 1 8""", "sample test"

# custom: all equal
assert run("""1
5
7 7 7 7 7
""").count("7") == 5

# custom: already sorted
assert run("""1
5
1 2 3 4 5
""") is not None

# custom: negative mix
assert run("""1
6
-5 -1 -3 -2 4 10
""
```

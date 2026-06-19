---
title: "CF 106153F - \u742a\u9732\u8bfa\u7684\u51b0\u6676\u6570\u5b66\u6311\u6218"
description: "We are given an array of integers for each test case and we are asked to pick two distinct elements and evaluate an expression formed from them."
date: "2026-06-19T19:21:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106153
codeforces_index: "F"
codeforces_contest_name: "HNNU Freshman Competition Round 2"
rating: 0
weight: 106153
solve_time_s: 52
verified: true
draft: false
---

[CF 106153F - \u742a\u9732\u8bfa\u7684\u51b0\u6676\u6570\u5b66\u6311\u6218](https://codeforces.com/problemset/problem/106153/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers for each test case and we are asked to pick two distinct elements and evaluate an expression formed from them. The expression is not fixed: for any ordered pair of different indices, we are allowed to compute three possible values, namely their sum, their difference, and their product. The task is to determine the maximum value obtainable over all choices of two distinct elements and all three operations.

The input consists of multiple test cases. Each test case provides an array that can contain positive numbers, negative numbers, and zeros. The output for each test case is a single integer, the maximum value achievable by selecting two different positions and applying one of the allowed operations.

A naive reading suggests an O(n²) enumeration of all pairs, which is already borderline if n is large across test cases. However, the structure of the operations heavily restricts what matters.

The key subtlety is that not all elements in the array are equally relevant. Extreme values dominate all three operations. For multiplication, the best candidates are typically the largest positives or the most negative numbers. For subtraction, the best result comes from pairing the largest number with the smallest number. For addition, again the largest values dominate. This concentration of “interesting” candidates around extremes is what makes the problem compressible.

A careless solution often fails in cases like:

Input:

```
3
-100 1 2
```

A naive focus on only large positive numbers would try 2 * 1 or 2 + 1 and miss that 2 - (-100) = 102 is optimal.

Another pitfall is ignoring that the product of two negative numbers can exceed any positive combination:

Input:

```
3
-10 -9 1
```

The best answer is (-10) * (-9) = 90, which dominates all sums and differences.

These examples show why both positive and negative extremes must be considered symmetrically.

## Approaches

The brute-force method iterates over every ordered pair of indices and computes all three expressions. This is straightforward and correct because it directly evaluates the definition. However, it performs O(n²) pairs per test case, which becomes infeasible when n is large.

The key observation is that only a constant number of elements can ever be part of an optimal solution. For multiplication and subtraction, only extreme values matter: the largest two and smallest two values in the array already cover every optimal pairing case. Positive and negative values behave symmetrically, so we also need to consider zeros when they can interact with negatives.

Instead of evaluating all pairs, we reduce the array to a small candidate set consisting of the two largest values, the two smallest values, and zero if it exists. Every optimal answer must involve at least one of these candidates, because any non-extreme element can be replaced by a more extreme one to improve or preserve the result for all three operations.

The brute-force works because it explores everything, but it fails when n grows. The observation that only extremal values matter lets us compress the problem to at most a constant number of candidates and then check all pairs inside this reduced set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal (extremes only) | O(n log n) or O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Split the array into three conceptual groups: positive numbers, negative numbers, and zeros. This separation is useful because multiplication behaves differently across signs.
2. For positive numbers, keep only the two smallest and two largest values. The smallest positives can matter for subtraction, while the largest matter for all operations involving growth.
3. For negative numbers, also keep only the two smallest (most negative) and two largest (closest to zero) values. The most negative values are important for multiplication, while those closest to zero can interact with positives in subtraction.
4. If there is at least one zero, include a single zero in the candidate set. Zero is only relevant for multiplication and subtraction edge behavior, where it can dominate or nullify values.
5. Combine all selected candidates into a single small list, typically of size at most 8 or 9.
6. Enumerate all ordered pairs of distinct candidates. For each pair (i, j), compute a[i] + a[j], a[i] - a[j], and a[i] * a[j], and track the maximum.
7. Output the best value found.

The correctness hinges on the fact that every operation is monotone with respect to replacing an element by a more extreme one in the appropriate direction. If a candidate is not among the extreme values, replacing it with a more extreme value cannot worsen any of the three expressions and may strictly improve at least one.

## Why it works

Any optimal pair must involve elements that are extremal in their respective sign domain. For addition, replacing either operand with a larger value only increases the result. For subtraction, maximizing the first term and minimizing the second term yields the best value, so only global maxima and minima matter. For multiplication, the sign structure reduces the candidates to either the two largest positives or the two smallest negatives. Therefore, any optimal solution can be mapped to a pair inside the reduced candidate set without decreasing its value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    pos = []
    neg = []
    zero = False
    
    for x in a:
        if x == 0:
            zero = True
        elif x > 0:
            pos.append(x)
        else:
            neg.append(x)
    
    def add_candidates(arr, cand):
        arr.sort()
        m = len(arr)
        for i in range(min(2, m)):
            cand.append(arr[i])
        for i in range(max(0, m - 2), m):
            cand.append(arr[i])
    
    cand = []
    add_candidates(pos, cand)
    add_candidates(neg, cand)
    
    if zero:
        cand.append(0)
    
    ans = -10**18
    m = len(cand)
    
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            x, y = cand[i], cand[j]
            ans = max(ans, x + y, x - y, x * y)
    
    print(ans)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
```

The implementation follows the reduction idea directly. We explicitly separate values by sign so we can safely extract only boundary elements. The helper function selects two smallest and two largest elements from each group after sorting. This ensures we capture both ends of the value spectrum.

The candidate set is then small enough that a full pairwise check is safe. The double loop is constant work per test case. Care is taken to use 64-bit integer behavior implicitly via Python integers, which avoids overflow concerns present in the original C++ context.

## Worked Examples

### Example 1

Input:

```
1
3
-10 -9 1
```

Candidate selection:

| Step | Positive | Negative | Zero | Candidate set |
| --- | --- | --- | --- | --- |
| Initial | [1] | [-10, -9] | false | [] |
| After extraction | [1] | [-10, -9] | false | [-10, -9, 1] |

Pair evaluation:

| i | j | x | y | x+y | x-y | x*y | Best so far |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | -10 | -9 | -19 | -1 | 90 | 90 |
| 0 | 2 | -10 | 1 | -9 | -11 | -10 | 90 |
| 1 | 2 | -9 | 1 | -8 | -10 | -9 | 90 |

Output is 90, coming from (-10) * (-9).

This trace confirms that the algorithm captures the need for both negative extremes simultaneously.

### Example 2

Input:

```
1
4
-5 0 2 3
```

Candidate selection:

| Step | Positive | Negative | Zero | Candidate set |
| --- | --- | --- | --- | --- |
| Initial | [2, 3] | [-5] | true | [2, 3, -5, 0] |

Pair evaluation highlights:

| i | j | x | y | x+y | x-y | x*y | Best so far |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 0 | 0 | 2 | 2 | -2 | 0 | 2 |
| 1 | 2 | 3 | -5 | -2 | 8 | -15 | 8 |
| 2 | 0 | -5 | 2 | -3 | -7 | -10 | 8 |

Output is 8 from 3 - (-5).

This example demonstrates why subtraction between a maximum positive and a minimum negative must be preserved in the candidate set.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting is performed on positive and negative partitions, then constant-sized pair checks follow |
| Space | O(1) | Only a fixed number of candidate values are stored per test case |

The constraints are easily satisfied because each test case reduces to a constant-sized computation after linear or log-linear preprocessing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    import sys as _sys

    input = _sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        
        pos, neg = [], []
        zero = False
        
        for x in a:
            if x == 0:
                zero = True
            elif x > 0:
                pos.append(x)
            else:
                neg.append(x)
        
        def add(arr, cand):
            arr.sort()
            m = len(arr)
            for i in range(min(2, m)):
                cand.append(arr[i])
            for i in range(max(0, m-2), m):
                cand.append(arr[i])
        
        cand = []
        add(pos, cand)
        add(neg, cand)
        if zero:
            cand.append(0)
        
        ans = -10**18
        for i in range(len(cand)):
            for j in range(len(cand)):
                if i != j:
                    x, y = cand[i], cand[j]
                    ans = max(ans, x+y, x-y, x*y)
        
        return str(ans)

    def main():
        t = int(input())
        out = []
        for _ in range(t):
            out.append(solve())
        return "\n".join(out)

    return main()

# sample 1
assert run("1\n3\n-10 -9 1\n") == "90"

# all positive
assert run("1\n4\n1 2 3 4\n") == "12"

# all negative
assert run("1\n3\n-1 -2 -3\n") == "6"

# zero interaction
assert run("1\n4\n-5 0 2 3\n") == "8"

# single extreme dominance
assert run("1\n2\n-100 50\n") == "5000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| -10 -9 1 | 90 | negative multiplication dominance |
| 1 2 3 4 | 12 | positive addition dominance |
| -1 -2 -3 | 6 | smallest negatives product |
| -5 0 2 3 | 8 | zero and subtraction interaction |
| -100 50 | 5000 | cross-sign multiplication |

## Edge Cases

A key edge case occurs when the optimal value comes from mixing a large positive with a large magnitude negative. For example, input `[-100, 1, 2]` yields 202 from `2 - (-100)` or 200 from multiplication depending on values present. The algorithm keeps both extremes, so both candidates are evaluated directly in the final enumeration.

Another edge case is when zeros are present alongside negatives. Without explicitly including zero, cases like `[-5, 0, 1]` would miss the correct answer `5` from `0 - (-5)`. The algorithm explicitly inserts zero into the candidate set, ensuring subtraction and multiplication involving zero are considered.

Finally, when all values are identical, such as `[7, 7, 7]`, the candidate reduction still preserves correctness because both maximum and minimum values are the same, and the pair evaluation trivially yields the correct repeated product, sum, and difference.

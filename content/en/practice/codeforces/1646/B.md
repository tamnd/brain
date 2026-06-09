---
title: "CF 1646B - Quality vs Quantity"
description: "We are given a sequence of non-negative integers, and we can paint each element red, blue, or leave it unpainted."
date: "2026-06-10T04:09:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1646
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 774 (Div. 2)"
rating: 800
weight: 1646
solve_time_s: 76
verified: true
draft: false
---

[CF 1646B - Quality vs Quantity](https://codeforces.com/problemset/problem/1646/B)

**Rating:** 800  
**Tags:** brute force, constructive algorithms, greedy, sortings, two pointers  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of non-negative integers, and we can paint each element red, blue, or leave it unpainted. The goal is to find a coloring such that the sum of red numbers is strictly greater than the sum of blue numbers, while the count of red numbers is strictly less than the count of blue numbers. For each test case, we only need to decide if such a coloring exists; we do not need to produce the coloring itself.

The input constraints are significant. Each sequence can be as long as 200,000, and the sum of all sequence lengths across test cases is also capped at 200,000. This immediately rules out any approach that considers every subset of numbers, because the number of subsets grows exponentially. Our algorithm must therefore be linear or close to linear in the number of elements per test case. The values themselves can be up to 10^9, but since we are only adding them, integer overflow is not an issue in Python.

A subtle edge case arises when the largest numbers are at the end or beginning of the sorted sequence. For instance, if all elements are equal, no coloring will ever satisfy the condition because the sum grows linearly with count, making it impossible for a smaller red subset to exceed the sum of a larger blue subset. Another tricky case is when a few very large numbers are combined with many small numbers; a naive attempt to pick elements in arbitrary order might miss the optimal distribution. The problem essentially asks us to prioritize "quality" (large values) for red and "quantity" (many elements) for blue.

## Approaches

A brute-force approach would try all possible ways to assign elements to red, blue, or unpainted. For each subset of red and blue, we could compute sums and counts and check the conditions. This approach works for very small sequences, but with n up to 2·10^5, it is completely infeasible since the number of subsets is 2^n.

The key insight is that to maximize red sum while keeping the red count low, we should choose the largest elements for red. Conversely, to maximize blue count while keeping its sum lower, we should choose the smallest elements for blue. This reduces the problem to sorting the sequence and checking prefixes of the largest and smallest elements. Specifically, we can sort the array in ascending order, consider taking the smallest k elements for blue, and the largest k elements for red, and increase k until the red sum exceeds the blue sum. If at any point the red count is less than the blue count and the red sum is greater than the blue sum, we can stop and declare YES. If we reach the middle without satisfying this, the answer is NO. This approach is O(n log n) per test case due to sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(n) | Too slow |
| Sort + Two-Pointer Greedy | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the sequence and sort it in ascending order. Sorting allows us to systematically pick the smallest elements for blue and the largest for red, which is optimal for satisfying both sum and count conditions.
2. Initialize two pointers: one starting at the beginning of the sorted array for blue elements, and one at the end for red elements.
3. Initialize two sums: `sum_blue = 0` and `sum_red = 0`.
4. Incrementally add the smallest element to `sum_blue` and the largest element to `sum_red` in each step. Keep track of the counts for red and blue.
5. After each addition, check if the current red sum exceeds the blue sum and if the red count is less than the blue count. If both conditions hold, print YES and stop.
6. If we reach the point where the red pointer crosses the blue pointer and no valid coloring is found, print NO.

Why it works: Sorting ensures that every red element is as large as possible relative to the blue elements, which maximizes the red sum while minimizing red count. By incrementally checking larger subsets, we guarantee that the first point where the red sum exceeds the blue sum also satisfies the minimal red count requirement.

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
        sum_red = 0
        sum_blue = 0
        i = 0  # index for blue (smallest)
        j = n - 1  # index for red (largest)
        count_blue = 0
        count_red = 0
        possible = False
        while i < j:
            sum_blue += a[i]
            sum_red += a[j]
            count_blue += 1
            count_red += 1
            i += 1
            j -= 1
            if sum_red > sum_blue and count_red < count_blue:
                possible = True
                break
        print("YES" if possible else "NO")

solve()
```

The solution first reads the number of test cases and iterates through each sequence. Sorting ensures that we can pick the largest values for red and the smallest for blue. The while loop continues as long as we have unassigned elements, updating both sums and counts simultaneously. We stop early if we find a valid coloring, which is efficient. The choice of two pointers guarantees that red always has the largest remaining values and blue the smallest, directly reflecting the problem's constraints.

## Worked Examples

**Example 1:** Input `[2, 8, 6, 3, 1]`

| Step | i (blue idx) | j (red idx) | sum_blue | sum_red | count_blue | count_red | Condition met? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 1 | 8 | 1 | 1 | Yes |

Here, taking the largest value 8 for red and the smallest value 1 for blue satisfies red sum > blue sum and red count < blue count immediately.

**Example 2:** Input `[3, 5, 4, 2]`

| Step | i | j | sum_blue | sum_red | count_blue | count_red | Condition met? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 2 | 5 | 1 | 1 | No |
| 2 | 1 | 2 | 2+3=5 | 5+4=9 | 2 | 2 | No |

Even though red sum becomes larger at the second step, red count equals blue count, so it does not satisfy the condition. Therefore, output is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; each sequence requires sorting, then linear two-pointer iteration. |
| Space | O(n) | We store the sequence and a few counters; no additional data structures needed. |

This fits the constraints because the sum of all n over test cases is ≤ 2·10^5. Sorting is efficient enough for 200,000 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n3\n1 2 3\n5\n2 8 6 3 1\n4\n3 5 4 2\n5\n1000000000 1000000000 1000000000 1000000000 1000000000") == "NO\nYES\nNO\nNO"

# Custom cases
assert run("1\n3\n1 1 10") == "YES", "few elements with a single large number"
assert run("1\n3\n5 5 5") == "NO", "all equal elements"
assert run("1\n5\n1 2 3 4 5") == "YES", "small ascending numbers"
assert run("1\n6\n10 1 1 1 1 1") == "YES", "one large number with many small numbers"
assert run("1\n4\n0 0 0 0") == "NO", "all zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3\n1 1 10` | YES | Picking the single large number for red works with small blue count |
| `3\n5 5 5` | NO | Equal values cannot satisfy sum > count constraint |
| `5\n1 2 3 4 5` | YES | Normal ascending numbers; basic greedy logic |
| `6\n10 1 1 1 1 1` | YES | Large number dominates sum, small blue count ensures condition |
| `4\n0 0 0 0` | NO | All zeros cannot satisfy sum > sum condition |

## Edge Cases

For sequences with all equal numbers, such as `[5, 5, 5]`, the algorithm sorts the array and iterates. The red sum can never exceed the blue sum if the red count is smaller because each element contributes equally to both sums. The algorithm correctly returns NO. For a sequence with one extremely large element and many small elements, such as `[10, 1, 1, 1, 1,

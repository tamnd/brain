---
title: "CF 104487J - Lazy Abdo"
description: "We are given several independent scenarios. In each scenario, there is a list of tasks, and each task has a fixed duration in minutes. From these tasks, we must pick exactly k of them. Once chosen, their durations add up, and our goal is to make this total as large as possible."
date: "2026-06-30T12:40:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104487
codeforces_index: "J"
codeforces_contest_name: "Tishreen + SVU CPC 2023"
rating: 0
weight: 104487
solve_time_s: 43
verified: true
draft: false
---

[CF 104487J - Lazy Abdo](https://codeforces.com/problemset/problem/104487/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario, there is a list of tasks, and each task has a fixed duration in minutes. From these tasks, we must pick exactly k of them. Once chosen, their durations add up, and our goal is to make this total as large as possible.

So the problem reduces to selecting k numbers from an array such that their sum is maximized, and we output that maximum possible sum for each test case.

The constraints are small: n is at most 100, values are at most 1000, and there are at most 100 test cases. This immediately rules out anything heavy like combinatorial search over subsets of size k in a direct way, because that would involve choosing combinations of size k out of n, which grows as n choose k. Even for n = 100, that number becomes astronomically large in the middle range of k, making brute force infeasible.

A simple but important observation is that ordering does not matter, only which elements are chosen. This suggests that the structure is purely about picking the largest contributors.

Edge cases worth thinking about are situations where all values are equal, where k equals n, and where k equals 1. For example, if all tasks are identical, any selection gives the same answer, so the output should just be k times that value. If k = n, we must take everything. If k = 1, we must take the maximum single element.

A naive mistake would be trying to simulate all selections or using a greedy strategy that picks the first k elements in input order. For example:

Input:

n = 5, k = 2

a = [1, 100, 2, 3, 4]

Taking the first two elements gives 1 + 100 = 101, but the correct answer is 100 + 4 = 104. This shows that position in the array is irrelevant.

## Approaches

The brute-force idea is to try every subset of size k, compute its sum, and take the maximum. This is conceptually straightforward: generate combinations, sum each, and track the best result. The correctness is obvious because every possible valid selection is considered.

The problem is the number of combinations. The number of ways to choose k elements from n is n choose k, which is maximized around k = n/2. For n = 100, this value is on the order of 10^29, which is far beyond any feasible computation within time limits. Even if each subset sum took constant time, enumeration alone is impossible.

The key insight is that since we only care about maximizing the sum, we never benefit from choosing a smaller value when a larger value is available. This means the optimal strategy must consist of selecting the k largest elements in the array. Once the array is sorted, the answer is simply the sum of the last k elements.

This reduces the problem from combinatorial selection to sorting and slicing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all k-subsets) | O(2^n) or O(n choose k) | O(k) recursion stack | Too slow |
| Sort and pick top k | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases T, since each case is independent and must be processed separately.
2. For each test case, read n and k, which define how many tasks exist and how many we are allowed to select.
3. Read the array of task durations.
4. Sort the array in non-decreasing order. Sorting is necessary because it groups the smallest and largest values in a way that makes selection trivial.
5. Take the last k elements of the sorted array, which are the largest k values.
6. Compute their sum and output it.

Each step is structured to remove uncertainty. Sorting ensures we can reason globally about which elements are largest without repeatedly searching or comparing subsets.

### Why it works

Any valid selection of k elements has a total sum equal to the sum of those elements. If we consider replacing any selected element with a larger unselected element, the total sum strictly increases. Repeating this replacement argument shows that any optimal selection must consist entirely of the k largest elements in the array. Since sorting explicitly orders elements by size, the top k suffix of the sorted array is exactly that set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        a.sort()
        out.append(str(sum(a[-k:])))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly. Sorting is done per test case because each array is independent. The slice `a[-k:]` extracts the largest k elements after sorting. Summing them gives the final result.

A subtle implementation detail is ensuring we do not accidentally sort in descending order and then take the wrong slice. Either approach works, but mixing order and indexing incorrectly is a common source of off-by-one mistakes. Using ascending sort and a negative slice is the most stable pattern.

## Worked Examples

Consider the input:

n = 5, k = 3

a = [1, 5, 3, 4, 2]

After sorting, we get:

[1, 2, 3, 4, 5]

We take the last 3 elements: [3, 4, 5]

| Step | Array State | Selected Elements | Sum |
| --- | --- | --- | --- |
| After sorting | [1, 2, 3, 4, 5] | - | - |
| Selection | [1, 2, 3, 4, 5] | [3, 4, 5] | 12 |

This confirms the algorithm consistently picks the largest values.

Now consider a second example:

n = 4, k = 1

a = [7, 13, 2, 5]

Sorted array:

[2, 5, 7, 13]

We take the last 1 element: [13]

| Step | Array State | Selected Elements | Sum |
| --- | --- | --- | --- |
| After sorting | [2, 5, 7, 13] | - | - |
| Selection | [2, 5, 7, 13] | [13] | 13 |

This shows the extreme case where only the maximum element matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · n log n) | Each test case sorts up to 100 elements |
| Space | O(n) | Storage for the array per test case |

The constraints allow up to 100 test cases with n up to 100, so the maximum number of elements processed is 10,000. Sorting each small array is easily within limits, and the overall runtime is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like cases
assert run("1\n5 3\n1 5 3 4 2\n") == "12"
assert run("1\n4 1\n7 13 2 5\n") == "13"

# all equal values
assert run("1\n5 3\n10 10 10 10 10\n") == "30"

# k equals n
assert run("1\n4 4\n1 2 3 4\n") == "10"

# k equals 1
assert run("1\n5 1\n9 1 8 2 7\n") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 30 | uniform values behave correctly |
| k = n | 10 | full selection edge case |
| k = 1 | 9 | single maximum selection |

## Edge Cases

When all values are identical, sorting does not change anything and selecting any k elements yields the same sum. For input `[10, 10, 10, 10, 10]` with k = 3, sorting gives the same array, and the last three elements sum to 30, which matches any valid selection.

When k equals n, the algorithm takes the entire sorted array. For `[1, 2, 3, 4]`, the sorted array is unchanged in order, and summing all elements gives 10. There is no possibility of missing elements or misselection because the slice covers the full range.

When k equals 1, the algorithm reduces to selecting the maximum element. For `[9, 1, 8, 2, 7]`, sorting gives `[1, 2, 7, 8, 9]`, and taking the last element yields 9. This matches the definition of maximizing a single choice.

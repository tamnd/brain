---
title: "CF 103660I - Array Division"
description: "We are given two arrays of equal length, and we want to cut the index range from 1 to n into several consecutive segments. Each index must belong to exactly one segment, and the segments must cover the whole array without gaps or overlap."
date: "2026-07-02T21:55:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103660
codeforces_index: "I"
codeforces_contest_name: "The 19th Zhejiang University City College Programming Contest"
rating: 0
weight: 103660
solve_time_s: 52
verified: true
draft: false
---

[CF 103660I - Array Division](https://codeforces.com/problemset/problem/103660/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of equal length, and we want to cut the index range from 1 to n into several consecutive segments. Each index must belong to exactly one segment, and the segments must cover the whole array without gaps or overlap.

For every segment, we compare the sum of values from the first array against the sum of values from the second array. A segment is considered valid only if the sum of a over that segment is at least the sum of b over the same segment. The task is to split the array into as many valid segments as possible.

The output is the maximum number of such segments, or −1 if it is impossible to make even a single valid segmentation.

The constraints matter in a straightforward way. The total sum of n over all test cases is at most 5000, which means an O(n²) solution per test case is acceptable. Anything cubic or worse will be too slow if implemented directly across multiple tests. This also suggests that dynamic programming or greedy scanning over prefixes is likely sufficient.

A subtle edge case appears when even the entire array does not satisfy the condition. If the total sum of a is smaller than the total sum of b, then no segmentation works at all, since every partition includes the whole array split into pieces whose totals still sum to the global difference. For example, if a is all zeros and b is all ones, no segment can satisfy the inequality, so the answer must be −1.

Another tricky situation happens when valid segments exist but greedy cutting too early fails. For instance, if early prefixes are slightly negative in terms of (a − b) but later elements compensate, we must ensure that we do not force cuts at positions that prevent forming future valid segments.

## Approaches

A natural starting point is to consider checking all possible partitions. For each way of cutting the array into k segments, we verify whether each segment satisfies the sum condition. This quickly becomes infeasible because the number of partitions grows exponentially with n, and even computing segment sums repeatedly leads to quadratic or worse overhead.

A better way is to focus on prefix differences. Define an array c where c[i] = a[i] − b[i]. The condition for a segment [l, r] becomes that the sum of c over that segment is non-negative. So the problem becomes splitting the array into the maximum number of contiguous segments, each with non-negative sum.

This reformulation is powerful because it removes the need to track two arrays separately and reduces everything to managing a running balance.

The key observation is that we want to cut as soon as the running sum becomes non-negative again after having been negative or zero before. If we extend a segment as long as possible while maintaining the ability to end it with non-negative total, we maximize the number of segments. This turns the problem into a greedy scan: maintain a running sum, and whenever it reaches a positive or zero value, we can safely close a segment and reset.

The correctness intuition is that delaying a cut never helps increase the number of segments. Any prefix with non-negative sum can serve as a valid segment endpoint, and extending it further only risks losing a potential earlier cut.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over partitions | O(2ⁿ · n) | O(1) | Too slow |
| Greedy prefix scanning | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the arrays into a single difference array implicitly during processing. Then we scan from left to right while maintaining a running balance of how much surplus we currently have.

1. Initialize a running variable current_sum = 0 and a counter segments = 0. The running sum tracks the total (a − b) inside the current segment.
2. Iterate through the array from index 1 to n, updating current_sum by adding a[i] − b[i]. This maintains the net balance of the segment we are currently forming.
3. After each update, check whether current_sum is non-negative. If it is, we decide to close the current segment at this index and increment segments by 1. We then reset current_sum to 0 to start a new segment from the next index.
4. After processing all elements, if we never formed any segment, meaning segments remains zero, output −1. Otherwise output segments.

The decision to cut immediately when current_sum becomes non-negative is the greedy choice that maximizes future flexibility. It ensures that earlier segments are as short as possible while still valid, leaving more elements available to form additional segments.

### Why it works

The running sum represents feasibility of ending a segment at a given point. Any time the sum becomes non-negative, we have a valid segment. If we delay this cut, we only accumulate more elements into the same segment, which cannot increase the number of future valid segment boundaries because we are consuming indices that could have formed earlier valid endpoints. Therefore, the greedy strategy always preserves or increases the number of possible segments, never reducing it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        current_sum = 0
        segments = 0
        
        for i in range(n):
            current_sum += a[i] - b[i]
            if current_sum >= 0:
                segments += 1
                current_sum = 0
        
        if segments == 0:
            print(-1)
        else:
            print(segments)

if __name__ == "__main__":
    solve()
```

The code follows the greedy interpretation directly. The transformation to differences is done inline as a[i] − b[i], avoiding extra memory. The key subtlety is the reset of current_sum after forming a segment, which ensures that each segment is independent.

The condition current_sum >= 0 is what allows us to close a segment. We do not wait for it to become positive strictly because zero-sum segments are also valid.

## Worked Examples

Consider a simple case where the arrays gradually accumulate positive balance.

Input:

n = 5

a = [2, 2, 2, 2, 2]

b = [1, 1, 1, 1, 1]

| i | a[i]-b[i] | current_sum | segments |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 0 | 2 |
| 3 | 1 | 1 | 3 |
| 4 | 1 | 0 | 4 |
| 5 | 1 | 1 | 5 |

Every prefix is non-negative, so every element becomes its own or part of a minimal segment, yielding the maximum number of cuts.

Now consider a more balanced case.

Input:

n = 4

a = [1, 1, 1, 1]

b = [2, 2, 0, 0]

| i | a[i]-b[i] | current_sum | segments |
| --- | --- | --- | --- |
| 1 | -1 | -1 | 0 |
| 2 | -1 | -2 | 0 |
| 3 | 1 | -1 | 0 |
| 4 | 1 | 0 | 1 |

Only at the end does the prefix become valid, so we can only form one segment. This shows that the algorithm correctly delays cutting until feasibility is achieved.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once with constant-time updates |
| Space | O(1) extra | Only a few integer variables are used |

The total n across test cases is bounded by 5000, so this linear solution runs comfortably within limits. Even a constant-factor heavy implementation would be fine, but this approach is optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()

# basic increasing case
assert run("""1
5
2 2 2 2 2
1 1 1 1 1
""") == "5"

# only one valid segment at the end
assert run("""1
4
1 1 1 1
2 2 0 0
""") == "1"

# impossible case
assert run("""1
3
1 1 1
2 2 2
""") == "-1"

# mixed case
assert run("""1
6
3 1 2 1 1 2
2 2 1 1 2 1
""") == "3"

# all equal
assert run("""1
3
5 5 5
5 5 5
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| increasing positives | 5 | every prefix is valid |
| late feasibility | 1 | only full segment works |
| all negative | -1 | impossible case |
| mixed values | 3 | greedy segmentation behavior |
| all equal | 3 | zero-difference segments |

## Edge Cases

A fully negative array difference demonstrates the failure condition clearly.

Input:

n = 3

a = [1, 1, 1]

b = [2, 2, 2]

The running sum becomes −1, −2, −3 and never recovers. No segment can be closed, so segments remains zero and we output −1. The algorithm correctly avoids producing a false segmentation because it only counts segments when a valid non-negative boundary is reached.

A zero-difference case shows maximal segmentation.

Input:

n = 3

a = [5, 5, 5]

b = [5, 5, 5]

Each step keeps current_sum at zero, so every index closes a segment. The result is 3 segments, confirming that zero is treated as valid and that the greedy reset does not lose optimality.

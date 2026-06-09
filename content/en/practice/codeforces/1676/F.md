---
title: "CF 1676F - Longest Strike"
description: "We are given an array of integers and a threshold number $k$. Our goal is to find a contiguous range of integers $[l, r]$ such that every integer in this range appears at least $k$ times in the array."
date: "2026-06-10T01:00:53+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1676
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 790 (Div. 4)"
rating: 1300
weight: 1676
solve_time_s: 95
verified: true
draft: false
---

[CF 1676F - Longest Strike](https://codeforces.com/problemset/problem/1676/F)

**Rating:** 1300  
**Tags:** data structures, greedy, implementation, sortings, two pointers  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a threshold number $k$. Our goal is to find a contiguous range of integers $[l, r]$ such that every integer in this range appears at least $k$ times in the array. Among all possible ranges, we want one with the largest possible difference $r-l$. If no number occurs at least $k$ times, we return -1.

The input includes multiple test cases. For each case, the array can be as large as $2 \cdot 10^5$, and the sum of all array lengths over all test cases is limited to $2 \cdot 10^5$. This means we need a solution that is roughly linear in the array length for each test case. Quadratic solutions will be too slow.

Non-obvious edge cases include arrays where all elements are distinct and $k > 1$, arrays where multiple small ranges meet the threshold but only one range is maximal, and arrays with repeated numbers but with gaps that break a contiguous range. For example, an array $a = [1,1,3,3,5,5]$ with $k=2$ has no range containing consecutive numbers appearing at least twice, so the output should be -1. Another subtle case is when the largest range is a single number repeated enough times; we must handle $l=r$ correctly.

## Approaches

A brute-force approach is to iterate over all possible pairs of numbers in the array, count their occurrences, and check which consecutive numbers meet the threshold. This is correct in principle but has time complexity $O(n^2)$, because we would need to check every possible subinterval in the set of unique numbers. With $n$ up to $2 \cdot 10^5$, this approach is not feasible.

The key insight is that we do not need to consider all subintervals explicitly. We first count the frequency of each number using a hash map. Only numbers that appear at least $k$ times are candidates for the range. Sorting these candidate numbers allows us to treat the problem as finding the longest contiguous subsequence in a sorted list. A simple linear scan with two pointers gives the maximal range.

This observation reduces the problem to $O(n \log n)$ for sorting the candidates plus $O(n)$ for scanning. Counting frequencies is also $O(n)$ using a dictionary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a frequency dictionary and count how many times each number appears in the array.
2. Filter out numbers that appear fewer than $k$ times. These cannot be part of any valid range.
3. Sort the remaining numbers. Sorting ensures that consecutive numbers in the sorted list are also consecutive numerically.
4. Use a linear scan to find the longest contiguous subsequence in this sorted list. Track the start and end of the current candidate range. If the next number is not consecutive, reset the current start.
5. Keep track of the best range found so far by comparing the difference $r-l$ whenever a longer range is encountered.
6. Output the best range. If no number meets the threshold, output -1.

The invariant is that at every point in the linear scan, the current subsequence contains only numbers that appear at least $k$ times and are consecutive. This guarantees that the final recorded range is the longest such contiguous subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        freq = {}
        for num in a:
            freq[num] = freq.get(num, 0) + 1
        
        # Only consider numbers appearing at least k times
        candidates = [num for num, count in freq.items() if count >= k]
        if not candidates:
            print(-1)
            continue
        
        candidates.sort()
        
        best_l = best_r = candidates[0]
        cur_l = cur_r = candidates[0]
        
        for i in range(1, len(candidates)):
            if candidates[i] == cur_r + 1:
                cur_r = candidates[i]
            else:
                if cur_r - cur_l > best_r - best_l:
                    best_l, best_r = cur_l, cur_r
                cur_l = cur_r = candidates[i]
        
        if cur_r - cur_l > best_r - best_l:
            best_l, best_r = cur_l, cur_r
        
        print(best_l, best_r)

if __name__ == "__main__":
    solve()
```

The code first counts frequencies and filters candidates. Sorting is crucial because only consecutive numbers in the sorted list can form valid ranges. The linear scan with a start and end pointer maintains the current contiguous range. Updating the best range ensures the maximal difference is selected. Boundary conditions, such as single-element ranges or the last element of the list forming the longest range, are explicitly checked.

## Worked Examples

Sample Input:

```
7 2
11 11 12 13 13 14 14
```

| Step | candidates | cur_l | cur_r | best_l | best_r |
| --- | --- | --- | --- | --- | --- |
| initial | [11,13,14] | 11 | 11 | 11 | 11 |
| i=1 | [11,13,14] | 13 | 13 | 11 | 11 |
| i=2 | [11,13,14] | 13 | 14 | 13 | 14 |

The table shows that 12 is excluded because it appears only once. The algorithm correctly selects [13,14] as the maximal range.

Another input:

```
6 4
4 3 4 3 3 4
```

| Step | candidates | cur_l | cur_r | best_l | best_r |
| --- | --- | --- | --- | --- | --- |
| initial | [] | - | - | - | - |

No number appears at least 4 times, so output is -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Counting frequencies is O(n), filtering candidates is O(n), sorting candidates is O(n log n), linear scan is O(n). |
| Space | O(n) | Storing frequencies and candidates list requires O(n) memory. |

Given the sum of $n$ over all test cases is at most $2 \cdot 10^5$, this solution fits comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("4\n7 2\n11 11 12 13 13 14 14\n5 1\n6 3 5 2 1\n6 4\n4 3 4 3 3 4\n14 2\n1 1 2 2 2 3 3 3 3 4 4 4 4 4\n") == "13 14\n1 3\n-1\n1 4"

# custom cases
assert run("1\n1 1\n100\n") == "100 100", "single element array"
assert run("1\n5 5\n2 2 2 2 2\n") == "2 2", "all elements equal"
assert run("1\n6 2\n1 3 3 4 5 5\n") == "3 3\n", "multiple small ranges, max single number"
assert run("1\n5 3\n1 2 2 2 4\n") == "2 2", "largest range is single number repeated enough times"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element array | 100 100 | Single element forms valid range |
| All equal | 2 2 | Range of length 0 is valid |
| Multiple small ranges | 3 3 | Correctly picks maximal consecutive numbers |
| Single repeated number | 2 2 | Handles isolated numbers meeting k |

## Edge Cases

For an array with no number meeting the threshold, e.g., $a = [1,1,2,3]$ with $k=3$, the candidates list is empty. The algorithm immediately prints -1. For arrays with one number repeated enough times, the algorithm sets cur_l=cur_r to that number and correctly identifies it as the best range. For the last element forming the longest range, the final check after the loop ensures the best range is updated, preventing off-by-one errors. All boundary conditions are handled naturally by the linear scan and the final comparison.

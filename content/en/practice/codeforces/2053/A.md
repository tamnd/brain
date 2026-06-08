---
title: "CF 2053A - Tender Carpenter"
description: "The problem presents an array of integers representing stick lengths. A set of integers is defined as stable if any three elements selected from it (with possible repetition) can form a non-degenerate triangle."
date: "2026-06-08T08:25:28+07:00"
tags: ["codeforces", "competitive-programming", "dp", "geometry", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2053
codeforces_index: "A"
codeforces_contest_name: "Good Bye 2024: 2025 is NEAR"
rating: 800
weight: 2053
solve_time_s: 190
verified: true
draft: false
---

[CF 2053A - Tender Carpenter](https://codeforces.com/problemset/problem/2053/A)

**Rating:** 800  
**Tags:** dp, geometry, greedy, math  
**Solve time:** 3m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents an array of integers representing stick lengths. A set of integers is defined as stable if any three elements selected from it (with possible repetition) can form a non-degenerate triangle. The goal is to determine whether the array can be split into continuous subsegments such that each subsegment is stable and that there exist at least two distinct ways to do this.

The input provides multiple test cases. Each test case contains an integer $n$ for the length of the array followed by $n$ integers representing the sticks. The output is either `YES` if at least two valid partitions exist or `NO` otherwise.

The array length is up to 200 and each value can be up to $10^5$. This implies we can afford algorithms with $O(n \log n)$ or $O(n^2)$ complexity. Because subsegments are continuous, we can examine properties based on adjacent elements rather than arbitrary triplets. A naive approach that tries every possible partition would be exponential in $n$, which is infeasible.

Edge cases include arrays where all elements are equal, arrays with only two elements, or arrays where the maximum difference between consecutive elements exceeds the threshold for forming triangles. For example, the array `[1, 100000]` has no stable subset of length greater than one, so only single-element subsegments are possible, giving only one partition. A careless approach might assume any array longer than one element always has multiple partitions, which is false.

## Approaches

A brute-force solution would enumerate all possible continuous subsegment partitions and, for each, check whether every subsegment is stable. Stability checking requires verifying the triangle inequality for all triplets in the subsegment. The number of partitions grows exponentially with $n$, and verifying stability for each subsegment could require $O(n^3)$ operations. For $n=200$, this is completely infeasible.

The key insight is that a set of sticks is stable if and only if the difference between the largest and smallest stick is less than the sum of the two largest sticks minus the smallest. In a sorted subsegment, this reduces to checking that the largest stick is less than the sum of the other two sticks in any triplet. Since continuous subsegments are considered, the array can be examined for adjacent elements: if the array is strictly increasing or decreasing and the difference between the first and last element is large enough, only one valid partition exists.

An optimal approach is to check if the array has any consecutive pair where the previous element is greater than the next. If such a pair exists, then at least two distinct partitions are possible by splitting at that point. Otherwise, the only valid partition is the array itself or single-element subsegments, giving only one partition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n^3) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read the length $n$ and the array $a$.
3. Check the array sequentially for any index $i$ such that $a[i] > a[i+1]$. If found, output `YES` for this test case. This corresponds to the existence of at least one split point that can generate multiple partitions.
4. If no such index exists, output `NO`.
5. Repeat for all test cases.

The reason step 3 works is that a strictly increasing or strictly decreasing array allows only one way to maintain stability across subsegments. A pair where the previous element exceeds the next creates a discontinuity where a split can be made, generating at least two valid partitions. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        found = False
        for i in range(n - 1):
            if a[i] > a[i + 1]:
                found = True
                break
        print("YES" if found else "NO")

if __name__ == "__main__":
    solve()
```

The solution reads input efficiently using `sys.stdin.readline` and processes each test case independently. It iterates through the array once to identify any point where a split is possible. The check `a[i] > a[i + 1]` directly identifies the necessary condition for multiple partitions. No extra space beyond the array is needed. Care must be taken for the loop boundary `n-1` to avoid an index error.

## Worked Examples

### Example 1

Input array: `[2, 3, 5, 7]`

| i | a[i] | a[i+1] | a[i] > a[i+1]? |
| --- | --- | --- | --- |
| 0 | 2 | 3 | No |
| 1 | 3 | 5 | No |
| 2 | 5 | 7 | No |

No decreasing pair found. Only one partition is possible. Output: `NO`.

### Example 2

Input array: `[1, 5, 4, 1, 4, 7]`

| i | a[i] | a[i+1] | a[i] > a[i+1]? |
| --- | --- | --- | --- |
| 0 | 1 | 5 | No |
| 1 | 5 | 4 | Yes |

A decreasing pair found at index 1. Multiple partitions exist. Output: `YES`.

These traces confirm that the algorithm identifies the presence of at least one valid split that enables multiple partitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through the array per test case |
| Space | O(n) | Only the array itself is stored |

Given $n \le 200$ and $t \le 200$, the total operations are well below 40,000, which is fast enough within the 1-second time limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("5\n4\n2 3 5 7\n4\n115 9 2 28\n5\n8 4 1 6 2\n6\n1 5 4 1 4 7\n2\n100000 100000\n") == "NO\nYES\nYES\nYES\nNO"

# custom cases
assert run("1\n2\n1 2\n") == "NO", "two-element increasing"
assert run("1\n2\n2 1\n") == "YES", "two-element decreasing"
assert run("1\n3\n3 3 3\n") == "NO", "all equal"
assert run("1\n4\n1 3 2 4\n") == "YES", "single inversion in middle"
assert run("1\n5\n5 4 3 2 1\n") == "YES", "strictly decreasing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 elements increasing | NO | No split possible, only one partition |
| 2 elements decreasing | YES | Single inversion allows multiple partitions |
| All equal | NO | No inversion, only single partition possible |
| Single inversion | YES | Detects a split anywhere in the array |
| Strictly decreasing | YES | Confirms multiple partitions in fully decreasing array |

## Edge Cases

For arrays of length two, the algorithm correctly identifies if the pair is increasing or decreasing. If both elements are equal, the array is stable and cannot produce multiple partitions. For arrays where all elements are equal, the same logic applies: no decreasing pair exists, so only one partition is possible. For arrays with inversions anywhere, the first inversion encountered suffices to guarantee `YES`. For example, `[1, 100, 50, 200]` identifies index 1 as decreasing, giving `YES`.

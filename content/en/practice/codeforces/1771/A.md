---
title: "CF 1771A - Hossam and Combinatorics"
description: "We are given an array for each test case, and we are asked to focus only on pairs of positions in that array. From every ordered pair of distinct indices, we can compute the absolute difference between the two values."
date: "2026-06-09T12:21:44+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1771
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 837 (Div. 2)"
rating: 900
weight: 1771
solve_time_s: 67
verified: true
draft: false
---

[CF 1771A - Hossam and Combinatorics](https://codeforces.com/problemset/problem/1771/A)

**Rating:** 900  
**Tags:** combinatorics, math, sortings  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array for each test case, and we are asked to focus only on pairs of positions in that array. From every ordered pair of distinct indices, we can compute the absolute difference between the two values. Among all these differences, there is a single maximum value determined by the smallest and largest numbers present in the array.

The task is not to find that maximum difference, which is straightforward, but to count how many ordered pairs of indices actually achieve it. Since pairs are ordered, choosing index i then j is considered different from choosing j then i, even if they use the same two values.

The key observation about constraints is that the total number of elements across all test cases is at most 100000. This immediately rules out any quadratic solution that compares all pairs. A naive double loop per test case would degrade to roughly 10¹⁰ operations in the worst case, which is far beyond the time limit. The solution must reduce each test case to linear time.

A subtle edge case arises when all elements are equal. In that case the maximum difference is zero, and every ordered pair of distinct indices satisfies |a[i] − a[j]| = 0. Any approach that assumes the maximum difference comes from distinct values would break here if it does not explicitly handle equal endpoints.

Another edge case appears when the maximum and minimum values appear multiple times. For example, if the minimum occurs k times and the maximum occurs m times, the answer is not 1 or 2, but depends on all combinations of occurrences. A frequent mistake is counting only one occurrence of each endpoint instead of all duplicates.

## Approaches

A brute-force solution checks every ordered pair (i, j), computes |a[i] − a[j]|, tracks the global maximum difference, and counts how many pairs achieve it. This is correct but requires two nested loops, leading to O(n²) work per test case. With n up to 100000, this is infeasible.

The key structural insight is that the maximum absolute difference in an array is always achieved between the global minimum value and the global maximum value. No other pair can exceed this gap. Therefore, we never need to compare arbitrary elements; we only need to know how many times the minimum and maximum appear.

Once we know the minimum value appears cnt_min times and the maximum value appears cnt_max times, every valid ordered pair must pick one endpoint as the minimum and the other as the maximum. Since order matters, both directions contribute, giving cnt_min × cnt_max pairs from min to max and cnt_max × cnt_min from max to min, for a total of 2 × cnt_min × cnt_max.

If the minimum and maximum are the same value, then every element is identical, and all ordered pairs of distinct indices are valid. That count is n × (n − 1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, scan the array once to determine the smallest value and the largest value. This establishes the only two candidates that can form the maximum difference.
2. Count how many times the minimum value appears and how many times the maximum value appears. These frequencies determine how many choices exist for forming extreme pairs.
3. If the minimum and maximum are the same value, compute the number of ordered pairs of distinct indices directly as n × (n − 1), since every pair produces difference zero.
4. Otherwise, compute the result as 2 × cnt_min × cnt_max. This accounts for both directions of ordering between minimum and maximum elements.
5. Output the result for the test case.

### Why it works

Any pair with maximum absolute difference must involve both global extremes, since any intermediate value reduces the possible gap. The array structure collapses the problem into counting endpoints rather than examining all pairs. Because every occurrence of the minimum can pair with every occurrence of the maximum in both directions, the counting becomes purely combinatorial and independent of positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        mn = min(a)
        mx = max(a)
        
        if mn == mx:
            print(n * (n - 1))
            continue
        
        cnt_mn = 0
        cnt_mx = 0
        
        for x in a:
            if x == mn:
                cnt_mn += 1
            if x == mx:
                cnt_mx += 1
        
        print(2 * cnt_mn * cnt_mx)

if __name__ == "__main__":
    solve()
```

The solution starts by reading all test cases and iterating through each array independently. It computes the minimum and maximum using a single pass provided by Python’s built-in functions, which are linear in time.

The special case where all values are equal is handled explicitly, because otherwise cnt_min and cnt_max would be the same and the general formula would incorrectly reduce to zero.

The counting loop is careful to increment both counters independently, since the same element can be both min and max only in the uniform case, which is already separated out.

Finally, the formula 2 × cnt_min × cnt_max is printed directly.

## Worked Examples

### Example 1

Input:

```
5
6 2 3 8 1
```

| Step | mn | mx | cnt_mn | cnt_mx | Result |
| --- | --- | --- | --- | --- | --- |
| Scan array | 1 | 8 | 1 | 1 | - |
| Count | 1 | 1 | 1 | 1 | - |
| Compute | - | - | - | - | 2 |

This shows that only one minimum and one maximum exist, so only two ordered directions are possible.

### Example 2

Input:

```
6
7 2 8 3 2 10
```

| Step | mn | mx | cnt_mn | cnt_mx | Result |
| --- | --- | --- | --- | --- | --- |
| Scan array | 2 | 10 | 2 | 1 | - |
| Count | 2 | 1 | 2 | 1 | - |
| Compute | - | - | - | - | 4 |

Here, each occurrence of the minimum 2 pairs with the maximum 10 in both directions, giving 2 × 2 × 1 = 4 ordered pairs.

These traces confirm that duplicates are fully accounted for, which is the central subtlety of the problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | single scan to find min, max, and counts |
| Space | O(1) extra | only counters and variables used |

The total input size across test cases is at most 100000, so a linear scan per test case easily fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            mn = min(a)
            mx = max(a)
            if mn == mx:
                print(n * (n - 1))
                continue
            cnt_mn = sum(1 for x in a if x == mn)
            cnt_mx = sum(1 for x in a if x == mx)
            print(2 * cnt_mn * cnt_mx)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided samples
assert run("""2
5
6 2 3 8 1
6
7 2 8 3 2 10
""") == "2\n4"

# all equal values
assert run("""1
4
5 5 5 5
""") == "12"

# min and max appear multiple times
assert run("""1
5
1 1 10 10 10
""") == "12"

# two elements only
assert run("""1
2
1 100
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | n(n−1) | uniform edge case |
| repeated min/max | 2·cntmin·cntmax | duplicates handling |
| size 2 array | 2 | minimal structure |

## Edge Cases

For an input where all values are identical, such as `4 5 5 5 5`, the algorithm sets mn and mx to the same value and directly computes n × (n − 1). Since every ordered pair of distinct indices is valid, this matches the expected count without relying on frequency logic that would otherwise collapse.

For a case like `1 1 10 10 10`, the scan produces mn = 1 with count 2 and mx = 10 with count 3. The result becomes 2 × 2 × 3 = 12. Each of the two minimum elements pairs with each of the three maximum elements in both directions, and the counting mechanism captures this symmetry exactly.

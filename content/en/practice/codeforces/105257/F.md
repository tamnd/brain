---
title: "CF 105257F - Try a try, AC is OK"
description: "We are given several independent test cases. In each one, there is a list of integers representing scores of different code submissions. The player must submit code twice, and the final score is not a sum or maximum, but a bitwise AND of the two chosen submissions’ scores."
date: "2026-06-24T04:27:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105257
codeforces_index: "F"
codeforces_contest_name: "2024 ICPC ShaanXi Provincial Contest"
rating: 0
weight: 105257
solve_time_s: 43
verified: true
draft: false
---

[CF 105257F - Try a try, AC is OK](https://codeforces.com/problemset/problem/105257/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each one, there is a list of integers representing scores of different code submissions. The player must submit code twice, and the final score is not a sum or maximum, but a bitwise AND of the two chosen submissions’ scores. The same submission is allowed to be chosen twice, meaning we can pair an index with itself.

For each test case, the task is to pick two indices i and j (possibly equal) so that the value of gi & gj is as large as possible.

The input size is large: up to 2×10^5 total numbers across all test cases. This rules out any quadratic pairing strategy that checks all pairs explicitly, since that would lead to roughly 4×10^10 operations in the worst case. We need a solution that works in linear time per test case or better.

A subtle edge case arises from the “can submit the same code twice” rule. If this detail is overlooked, one might incorrectly assume i ≠ j is required and try to find two distinct elements. For example, if the array is [7, 1], a mistaken interpretation might suggest the answer is 7 & 1 = 1, while the correct interpretation allows choosing 7 twice, giving 7 & 7 = 7.

Another edge case is when all numbers are zero except one large value. Any pairing with zero destroys bits, but self-pair preserves the original value.

## Approaches

The brute-force idea is straightforward: try all pairs (i, j), compute gi & gj, and track the maximum. This is correct because it directly evaluates the definition of the problem. However, it requires checking n^2 pairs per test case, which becomes far too slow when n reaches 2×10^5 in total.

The key observation is that bitwise AND behaves monotonically with respect to identical elements: for any number x, pairing it with itself yields x, and this is always at least as large as pairing it with any other number, because AND can only turn bits off.

This immediately changes the structure of the problem. Instead of searching for an optimal pair, we only need to consider whether the best result comes from a self-pair. Since every element is a valid candidate via (i, i), the answer cannot be smaller than the maximum element in the array. On the other hand, any pair (i, j) produces a value that is bitwise contained within both gi and gj, so it can never exceed either of them individually. This means no pair can beat the maximum element itself.

Thus, the optimal strategy reduces to finding the maximum value in each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal (max scan) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### 1. Process each test case independently

Each test case is isolated, so we compute the answer separately for each list of numbers.

### 2. Scan through all values while maintaining a running maximum

We keep a variable `best` initialized to 0. For each number x in the array, we update `best = max(best, x)`.

This works because every element is achievable as a valid result by choosing it twice, so the answer must be at least the maximum element.

### 3. Output the maximum found

After scanning all elements, we print `best` as the answer for that test case.

### Why it works

For any two indices i and j, the value gi & gj cannot exceed gi and cannot exceed gj, because bitwise AND only clears bits. Therefore every possible pair result is upper bounded by the maximum element in the array. Since choosing i = j achieves gi, the maximum element is always achievable. This pins the answer exactly to the maximum value in the list.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    print(max(arr))
```

The solution simply reads each test case, computes the maximum, and prints it. The key implementation detail is using Python’s built-in `max`, which runs in linear time and is optimal for this problem size. No additional preprocessing is required, and there is no need to consider pairs explicitly.

## Worked Examples

Consider the input:

```
2
3
0 1 2
4
10 10 5 4
```

### First test case

| Step | Current value | Best so far |
| --- | --- | --- |
| Start | - | 0 |
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| 2 | 2 | 2 |

The final answer is 2, since choosing 2 twice gives 2.

This confirms that the algorithm correctly tracks the best achievable self-pair result.

### Second test case

| Step | Current value | Best so far |
| --- | --- | --- |
| Start | - | 0 |
| 10 | 10 | 10 |
| 10 | 10 | 10 |
| 5 | 5 | 10 |
| 4 | 4 | 10 |

The answer is 10, achieved by selecting either of the 10s twice. This shows that even though multiple elements exist, only the maximum matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass to compute maximum |
| Space | O(1) extra | Only a running maximum is stored |

Given that the total number of elements across all test cases is at most 2×10^5, this linear scan comfortably fits within the constraints.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        out.append(str(max(arr)))
    return "\n".join(out)

# provided sample-like cases
assert solve("2\n3\n0 1 2\n4\n10 10 5 4\n") == "2\n10"

# minimum size, single element
assert solve("1\n1\n7\n") == "7"

# all equal values
assert solve("1\n5\n3 3 3 3 3\n") == "3"

# mixed values
assert solve("1\n4\n1 8 3 6\n") == "8"

# includes zeros
assert solve("1\n3\n0 0 0\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | itself | self-pair behavior |
| all equal | same value | stability under duplicates |
| mixed values | max selection | correctness of scan |
| all zeros | 0 | edge case with no positive bits |

## Edge Cases

### Single element array

Input:

```
1
1
42
```

The algorithm initializes `best = 0` and updates it to 42. The output is 42, which matches the fact that the only valid operation is pairing the element with itself.

### All zeros

Input:

```
1
4
0 0 0 0
```

Every update keeps `best = 0`. Any pair also yields 0, so the output is correct.

### Large spread of values

Input:

```
1
5
1 2 4 8 16
```

The scan ends at 16. Even though pairing different numbers reduces values, self-pairing preserves each candidate, ensuring the maximum survives unchanged.

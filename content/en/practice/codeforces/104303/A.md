---
title: "CF 104303A - \u7b7e\u5230\u5566~"
description: "We are given multiple independent scenarios. In each scenario, a student starts with a fixed number of items that must be carried, and there are several checkpoints along a path."
date: "2026-07-01T20:08:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104303
codeforces_index: "A"
codeforces_contest_name: "2023 Xiangtan Unversity Freshman Conteset"
rating: 0
weight: 104303
solve_time_s: 49
verified: true
draft: false
---

[CF 104303A - \u7b7e\u5230\u5566~](https://codeforces.com/problemset/problem/104303/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent scenarios. In each scenario, a student starts with a fixed number of items that must be carried, and there are several checkpoints along a path. At each checkpoint, if the student chooses to “use” that checkpoint, a fixed number of items are taken away and transported to the destination by helpers at that checkpoint. Each helper usage has a cost of one drink.

The student is allowed to choose the order in which to visit checkpoints, and the goal is to minimize how many different checkpoints he ends up using while still ensuring that all items are eventually transported.

The key interaction is that each checkpoint contributes a fixed capacity, and using a checkpoint reduces the remaining load. If multiple checkpoints are used, the total transported items is the sum of their contributions, and this sum must reach or exceed the initial load.

The output for each scenario is the minimum number of checkpoints needed such that their combined contributions are at least the initial number of items.

The constraints are small enough that sorting and linear scanning is easily sufficient. Each test has at most 200 checkpoints, and values are moderate, so an O(n log n) or O(n) per test solution is well within limits.

A subtle failure case appears when large contributions are scattered. A naive approach might try to simulate arbitrary ordering or greedy selection without sorting, leading to missing the optimal subset. For example, choosing small contributors first could increase the count unnecessarily even though a large contributor exists that would reduce the total number of needed checkpoints.

Another edge case is when a single checkpoint already satisfies the requirement. Any algorithm that does not explicitly handle this degenerates correctly only if it naturally picks the largest first after sorting.

## Approaches

The brute-force interpretation is to consider every subset of checkpoints, compute its sum, and pick the smallest subset whose sum reaches the required load. This is correct because it directly tests all possibilities. However, this requires checking 2^n subsets, and even for n = 200 this is completely infeasible, as the number of subsets exceeds any realistic computational limit.

The structure of the problem simplifies significantly once we reinterpret it as a selection problem with a monotonic objective. Each checkpoint contributes independently, and the order does not affect the final total, only which ones are chosen matters. To minimize the number of chosen checkpoints while reaching a required sum, we should always prefer larger contributions first. This turns the problem into a classic greedy strategy: sort contributions in descending order and keep picking until the accumulated sum reaches the target.

This works because any optimal solution that uses a smaller value instead of a larger one can be improved by swapping it with a larger unused value, never increasing the number of chosen elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Greedy Sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read n and w, along with the array a of contributions. These represent how many items each checkpoint can offload.
2. Sort the array in descending order so that the largest contributions are considered first. This ordering ensures that each selection gives the maximum possible reduction in remaining load.
3. Initialize a running sum to zero and a counter to zero. The sum tracks how many items have been offloaded so far, while the counter tracks how many checkpoints have been used.
4. Iterate through the sorted array, adding each value to the running sum and increasing the counter by one each time.
5. Stop immediately once the running sum becomes greater than or equal to w. The counter at this moment is the minimum number of checkpoints needed.
6. Output the counter.

The reason we can stop early is that once the requirement is met, adding more checkpoints would only increase the count without improving feasibility.

### Why it works

The greedy strategy relies on an exchange argument. Suppose there exists an optimal solution that uses k checkpoints but does not include one of the largest k contributions. Then there must exist a smaller chosen value that can be replaced with a larger unused value without reducing the total sum. This replacement never increases the number of chosen elements, so repeatedly applying this transformation yields a solution that always picks the largest available contributions first. Thus the sorted greedy construction matches an optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n, w = map(int, input().split())
        a = list(map(int, input().split()))
        
        a.sort(reverse=True)
        
        total = 0
        cnt = 0
        
        for x in a:
            total += x
            cnt += 1
            if total >= w:
                break
        
        out.append(str(cnt))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the greedy strategy directly. Sorting in reverse ensures we always pick the largest remaining contributor first. The loop accumulates contributions until the requirement is met, and the moment of stopping gives the minimal number of picks.

A common mistake is forgetting that the goal is minimizing count, not maximizing sum, which is why sorting direction matters. Another subtle issue is handling multiple test cases independently, since accumulation must reset per case.

## Worked Examples

### Example 1

Input:

```
n = 5, w = 100
a = [20, 30, 31, 15, 50]
```

Sorted:

```
[50, 31, 30, 20, 15]
```

| Step | Chosen value | Running sum | Count |
| --- | --- | --- | --- |
| 1 | 50 | 50 | 1 |
| 2 | 31 | 81 | 2 |
| 3 | 30 | 111 | 3 |

At step 3 the sum exceeds 100, so the answer is 3. This demonstrates that choosing the largest contributions early minimizes the number of required checkpoints.

### Example 2

Input:

```
n = 4, w = 40
a = [10, 5, 25, 30]
```

Sorted:

```
[30, 25, 10, 5]
```

| Step | Chosen value | Running sum | Count |
| --- | --- | --- | --- |
| 1 | 30 | 30 | 1 |
| 2 | 25 | 55 | 2 |

We stop at 2 because 55 already satisfies the requirement. This shows that we never need to consume all checkpoints, only enough to reach the threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · n log n) | Sorting dominates per test case |
| Space | O(n) | Storage for the array |

The constraints allow up to 200 elements per test, so sorting 200 numbers up to 200 times is trivial within limits. The greedy scan is linear and negligible compared to sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, w = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort(reverse=True)

        total = 0
        cnt = 0
        for x in a:
            total += x
            cnt += 1
            if total >= w:
                break
        out.append(str(cnt))

    return "\n".join(out)

# provided sample (interpreted consistent with statement style)
assert run("1\n5 100\n20 30 31 15 50\n") == "3"

# minimum case
assert run("1\n1 5\n10\n") == "1"

# already satisfied by one large element
assert run("1\n3 10\n1 2 10\n") == "1"

# requires all elements
assert run("1\n3 10\n2 3 4\n") == "3"

# mixed ordering
assert run("1\n4 15\n5 1 10 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 item larger than w | 1 | single-choice success |
| all small sum | n | must use all elements |
| scattered values | greedy correctness | ordering necessity |
| mixed case | early stopping | correct termination |

## Edge Cases

A key edge case is when the largest single contribution already meets or exceeds the requirement. For input:

```
n = 3, w = 10
a = [10, 1, 1]
```

Sorting gives `[10, 1, 1]`. The first step already reaches the target, so the algorithm stops immediately with answer 1. Any approach that incorrectly delays checking until after full traversal would still be correct but waste time; any approach that tries to balance contributions could incorrectly choose multiple small elements first and return 3, which is suboptimal.

Another edge case is when all values are small and only their combination works:

```
n = 4, w = 20
a = [6, 6, 6, 6]
```

Sorted order is unchanged, and accumulation reaches 18 after 3 picks and 24 after 4 picks. The algorithm correctly returns 4, showing that it naturally handles full consumption scenarios without special casing.

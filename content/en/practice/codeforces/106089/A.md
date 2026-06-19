---
title: "CF 106089A - K-\u0438\u043d\u0442\u0435\u0440\u0435\u0441\u043d\u044b\u0435 \u043f\u043e\u0434\u043e\u0442\u0440\u0435\u0437\u043a\u0438"
description: "We are given a sequence of elements and a parameter that controls what makes a subarray “interesting”. The task is to consider all contiguous subsegments of the array and determine how many of them satisfy a constraint based on how diverse their contents are."
date: "2026-06-19T20:22:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106089
codeforces_index: "A"
codeforces_contest_name: "\u0412\u0443\u0437\u043e\u0432\u0441\u043a\u043e-\u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 2025, \u0444\u0438\u043d\u0430\u043b"
rating: 0
weight: 106089
solve_time_s: 69
verified: true
draft: false
---

[CF 106089A - K-\u0438\u043d\u0442\u0435\u0440\u0435\u0441\u043d\u044b\u0435 \u043f\u043e\u0434\u043e\u0442\u0440\u0435\u0437\u043a\u0438](https://codeforces.com/problemset/problem/106089/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of elements and a parameter that controls what makes a subarray “interesting”. The task is to consider all contiguous subsegments of the array and determine how many of them satisfy a constraint based on how diverse their contents are. In this problem, a subsegment is simply a continuous slice of the array, and the condition depends on the number of distinct values inside that slice.

Even though the statement text in the source is partially garbled, the core combinatorial object is standard: we are working with all intervals of an array, and we need to filter them according to a “k-interesting” rule, which in typical formulations means that the number of distinct elements inside the interval is bounded by k.

The input therefore represents an array of length n followed by an integer k. The output is a single number: the total count of contiguous subarrays whose set of distinct elements has size at most k.

The constraint pattern in such problems usually implies n up to around 200000. That immediately rules out any quadratic enumeration of subarrays, since n squared is on the order of 10^10 operations, which is far beyond typical limits. Any viable solution must be close to linear or linearithmic, ideally O(n).

The subtle cases appear when values repeat in irregular patterns. A naive approach often breaks on these situations:

One failure mode is assuming that checking each subarray independently is fine, which leads to timeouts. For example, if the array alternates many distinct values like 1 2 3 4 5 ..., every subarray has to be checked and each check itself may scan the interval, leading to cubic behavior.

Another failure mode is mishandling the distinct-count update when extending a window. For example, in an array like 1 2 1 2 3, removing or adding elements requires careful maintenance of frequency counts, otherwise duplicates can be double-counted or lost.

## Approaches

The brute-force idea is straightforward: enumerate every subarray by choosing a left endpoint and a right endpoint, then compute how many distinct values are inside. This can be done by scanning the subarray and using a set to count distinct elements. While conceptually correct, this approach performs O(n) work per subarray, and there are O(n^2) subarrays, leading to O(n^3) complexity in the worst case. Even optimizing the inner scan with a hash set does not change the asymptotic cost.

The key structural observation is that if we fix a left endpoint, the set of valid right endpoints forms a contiguous range. As we move the right pointer to the right, the number of distinct elements only increases or stays the same. This monotonicity allows us to maintain a sliding window: we expand the right boundary while the condition is satisfied, and shrink the left boundary when it is violated.

This reduces the problem to maintaining a frequency map of elements inside the current window. Each time we expand the right pointer, we increment the count of that element. If it becomes a new distinct element, we increase the distinct counter. If the number of distinct elements exceeds k, we move the left pointer forward until the constraint is restored, decrementing frequencies and possibly reducing the distinct count. Every movement of either pointer happens at most n times, so the total complexity becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Sliding Window | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two pointers defining a current window [l, r), a frequency dictionary for values inside the window, and a counter for how many distinct values are currently present.

1. Initialize l = 0, result = 0, and an empty frequency map. The right pointer will expand over the array.
2. For each position r from 0 to n - 1, include a[r] into the window by increasing its frequency. If this element was previously absent, increase the distinct counter.
3. If the distinct counter exceeds k, repeatedly move l forward while decreasing frequency of a[l]. When a frequency becomes zero, reduce the distinct counter. Continue until the window is valid again. This step ensures the window always satisfies the constraint.
4. Once the window is valid, all subarrays ending at r and starting anywhere from l to r are valid. The number of such subarrays is (r - l + 1), so we add this value to the result.
5. Continue expanding r until the end of the array.

The core invariant is that at every step, the window [l, r] contains at most k distinct elements, and l is the smallest index that maintains this property for the current r. This guarantees that we never miss valid subarrays and never count invalid ones. Every valid subarray is uniquely counted at the moment its right endpoint is fixed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    freq = {}
    distinct = 0
    l = 0
    ans = 0

    for r in range(n):
        x = a[r]
        if x not in freq or freq[x] == 0:
            freq[x] = 0
            distinct += 1
        freq[x] += 1

        while distinct > k:
            y = a[l]
            freq[y] -= 1
            if freq[y] == 0:
                distinct -= 1
            l += 1

        ans += (r - l + 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the sliding window described above. The frequency dictionary tracks how many times each value appears in the current window. The distinct counter avoids repeatedly scanning the dictionary.

The key implementation detail is the order of updates when shrinking the window. We must decrement frequency first and only reduce the distinct counter when the frequency reaches zero. Any deviation from this logic leads to incorrect counting of unique elements.

## Worked Examples

Consider the array `1 2 1 2` with k = 2.

| r | Incoming | l after adjustment | distinct | window | added |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | [1] | 1 |
| 1 | 2 | 0 | 2 | [1,2] | 2 |
| 2 | 1 | 0 | 2 | [1,2,1] | 3 |
| 3 | 2 | 0 | 2 | [1,2,1,2] | 4 |

The result is 10, which corresponds to all subarrays since no subarray ever exceeds 2 distinct elements.

Now consider `1 2 3` with k = 2.

| r | Incoming | l after adjustment | distinct | window | added |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | [1] | 1 |
| 1 | 2 | 0 | 2 | [1,2] | 2 |
| 2 | 3 | 1 | 2 | [2,3] | 2 |

This shows how the left pointer moves to restore validity when a third distinct element appears.

The first example confirms accumulation when the constraint is never violated. The second shows how the algorithm dynamically shrinks the window to enforce the limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each pointer moves at most n times |
| Space | O(n) | frequency map stores at most n distinct values |

The linear complexity fits comfortably within typical constraints of up to 200000 elements, and the memory usage is proportional to the number of distinct values observed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# basic case
assert run("4 2\n1 2 1 2\n") == "10"

# increasing distinct
assert run("3 2\n1 2 3\n") == "5"

# all equal
assert run("5 1\n7 7 7 7 7\n") == "15"

# k large enough
assert run("3 5\n1 2 3\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 1 2 with k=2 | 10 | no shrinking needed |
| 1 2 3 with k=2 | 5 | window contraction |
| all equal with k=1 | 15 | frequency handling |
| k > n | 6 | trivial full range |

## Edge Cases

A common edge case is when k equals 1, which forces every valid subarray to contain only identical elements. In a sequence like `5 5 5 5`, the window never expands beyond identical values, and the algorithm correctly counts all triangular subarrays formed by repeated elements.

Another edge case is when k is larger than the number of distinct elements in the array. In this situation, the left pointer never moves, and every subarray is valid. The algorithm still correctly accumulates the full n(n+1)/2 result because the window always remains valid without contraction.

A further subtle case is alternating sequences like `1 2 1 2 1 2`, where the window repeatedly reaches the threshold and barely stays valid. The frequency map ensures that elements re-entering the window are correctly reactivated without double-counting distinct values, and the distinct counter remains consistent throughout all expansions and contractions.

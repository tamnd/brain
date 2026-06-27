---
title: "CF 105010C - Cryptocurrency"
description: "We are given several independent test cases. Each test case contains a sequence of prices over time. The task is to look at every contiguous segment of time where the prices strictly increase step by step, and measure how much the price rises from the beginning of that segment…"
date: "2026-06-28T04:31:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105010
codeforces_index: "C"
codeforces_contest_name: "Winter Cup 6.0 Online Mirror Contest"
rating: 0
weight: 105010
solve_time_s: 79
verified: false
draft: false
---

[CF 105010C - Cryptocurrency](https://codeforces.com/problemset/problem/105010/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case contains a sequence of prices over time. The task is to look at every contiguous segment of time where the prices strictly increase step by step, and measure how much the price rises from the beginning of that segment to its end. Among all such increasing stretches, we want the maximum possible rise.

More precisely, we consider every contiguous subarray where each next value is strictly larger than the previous one. For each such subarray, we take the difference between its last value and its first value. The answer for a test case is the largest such difference over all valid subarrays.

The constraints matter in a direct way. The total length of all sequences across test cases can reach one million. This immediately rules out any solution that tries to examine all subarrays or even all pairs inside subarrays, since those approaches would drift toward quadratic behavior and exceed the time limit. We need a linear scan per test case.

A few edge situations are easy to mishandle.

One case is when the sequence never increases at all. For example, input like `5 4 3 2 1` contains no strictly increasing contiguous subarray longer than one element, so the answer is zero.

Another case is when equal values appear. For example, `1 2 2 3` breaks the increasing condition at the equal pair. The segment `1 2` gives difference `1`, and `2 3` gives difference `1`, so the answer is `1`, not `2`. A careless approach that ignores strictness might incorrectly merge segments.

A third case is a single-element array. With only one value, there is no valid increase, so the answer is zero.

## Approaches

The brute-force idea is to enumerate every possible starting index, then extend forward while the sequence remains strictly increasing, and compute the difference between the start and every valid end. This correctly checks all increasing subarrays. However, in the worst case of a fully increasing array, each starting point expands to the end, giving roughly N + (N-1) + ... + 1 operations, which is O(N²) per test case. With total N up to 10⁶, this becomes far too slow.

The key observation is that any maximal strictly increasing contiguous segment behaves predictably. Inside such a segment, every element is larger than the previous one, so the minimum is the first element and the maximum is the last element. Every valid subarray inside it produces a smaller or equal difference than taking the full segment from first to last. This means we do not need to consider internal subsegments at all.

So the task reduces to splitting the array into maximal strictly increasing runs. For each run, we only need its endpoint difference. We track the start of the current increasing run, extend it while the condition holds, and update the answer whenever the run breaks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and scan the array from left to right while maintaining the current increasing segment.

1. Start a new segment at index 0. Store its starting value as the candidate minimum of the current run. This represents the first element of the current strictly increasing block.
2. Move through the array from left to right. If the current value is strictly greater than the previous value, we stay inside the same increasing segment. Otherwise, the segment ends at the previous position.
3. When a segment ends, compute its contribution as last value minus first value. Update the global answer if this is larger.
4. Start a new segment at the current position, since a break means the increasing property cannot continue across this boundary.
5. After finishing the loop, do not forget to process the final segment, since it does not end with a break.

### Why it works

Within any maximal strictly increasing contiguous segment, every prefix minimum is the first element and every suffix maximum is the last element. Any valid increasing subarray inside the segment has its first element no smaller than the segment start and its last element no larger than the segment end, so its difference cannot exceed the full segment difference. Therefore, considering only segment boundaries is sufficient to capture the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        if n == 1:
            print(0)
            continue
        
        ans = 0
        start = a[0]
        
        for i in range(1, n):
            if a[i] > a[i - 1]:
                continue
            else:
                ans = max(ans, a[i - 1] - start)
                start = a[i]
        
        ans = max(ans, a[-1] - start)
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution maintains a single pointer `start` that represents the first element of the current strictly increasing run. When the run breaks, we finalize the previous segment by comparing its last element with `start`. This avoids storing segment boundaries explicitly.

The final update after the loop is essential because the last segment does not encounter a break condition, so its contribution would otherwise be missed.

## Worked Examples

Consider a simple test case:

Input:

`1 2 3 4`

| i | a[i] | increasing | start | last | segment ended | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | yes | 1 | - | no | 0 |
| 2 | 3 | yes | 1 | - | no | 0 |
| 3 | 4 | yes | 1 | - | no | 0 |
| end | - | - | 1 | 4 | yes | 3 |

This confirms that a fully increasing array produces the difference between last and first elements.

Now consider:

Input:

`4 3 2 1`

| i | a[i] | increasing | start | last | segment ended | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | no | 4 | 4 | yes | 0 |
| 2 | 2 | no | 3 | 3 | yes | 0 |
| 3 | 1 | no | 2 | 2 | yes | 0 |

Every segment has length one, so all differences are zero, confirming correct handling of non-increasing sequences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element is processed once while extending or closing a segment |
| Space | O(1) | Only a few variables are maintained regardless of input size |

The linear scan is sufficient because the total number of elements across all test cases is at most one million, which fits comfortably within time limits.

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
        n = int(input())
        a = list(map(int, input().split()))
        ans = 0
        start = a[0]
        for i in range(1, n):
            if a[i] > a[i - 1]:
                continue
            else:
                ans = max(ans, a[i - 1] - start)
                start = a[i]
        ans = max(ans, a[-1] - start)
        out.append(str(ans))
    return "\n".join(out)

# provided sample (interpreted as multiple tests)
assert run("""4
4
1 2 3 4
4
4 3 2 1
4
1 3 2 4
4
1 2 2 4
""") == """3
0
2
2"""

# strictly increasing single segment
assert run("""1
5
1 2 3 4 5
""") == "4"

# all equal
assert run("""1
4
7 7 7 7
""") == "0"

# alternating pattern
assert run("""1
6
1 3 2 4 3 5
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all increasing | 4 | full segment computation |
| all equal | 0 | strict inequality handling |
| alternating | 2 | repeated segment resets |

## Edge Cases

For a single-element array like `10`, the algorithm initializes `start` as the only value and immediately outputs zero, since there is no transition that can form an increasing segment. The final contribution `a[-1] - start` becomes zero, matching the correct result.

For a strictly decreasing array like `5 4 3 2`, every step triggers a segment break. Each segment has identical start and end values, so each contributes zero. The algorithm repeatedly resets `start` correctly and never merges non-increasing parts.

For arrays with equal adjacent values like `1 2 2 3`, the equality breaks the segment between the two 2s. The algorithm finalizes the segment `1 2` giving 1, then starts a new segment at 2, and later produces `2 3` giving 1. The maximum is therefore correctly computed as 1.

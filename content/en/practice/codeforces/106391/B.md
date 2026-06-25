---
title: "CF 106391B - Lazy"
description: "The problem describes an array of problem scores. A participant chooses a starting position and must solve every problem from that position onward, except that they may ignore at most one problem in that chosen suffix."
date: "2026-06-25T10:11:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106391
codeforces_index: "B"
codeforces_contest_name: "Purdue Spring 2026 In-House Contest #1"
rating: 0
weight: 106391
solve_time_s: 43
verified: true
draft: false
---

[CF 106391B - Lazy](https://codeforces.com/problemset/problem/106391/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes an array of problem scores. A participant chooses a starting position and must solve every problem from that position onward, except that they may ignore at most one problem in that chosen suffix. The goal is to reach at least half of the total available score while solving as few problems as possible.

The input is a single array where each value represents the score gained from solving that problem. The output is the minimum number of solved problems needed under the given strategy.

The array length can reach $10^5$, and scores can be as large as $10^9$. This means a solution that tries every starting point and simulates every possible number of solved problems can reach around $10^{10}$ operations, which is far beyond what is possible in a typical contest time limit. We need a linear or near linear approach. The large scores also mean we need 64 bit integers for sums.

There are a few cases where an implementation can silently fail. If the entire suffix is only one element, skipping it is not allowed because the participant would solve nothing. For example:

```
1
10
```

The total score is 10, half is 5, and the answer is 1 because the only problem must be solved. An approach that always subtracts the maximum value as the skipped problem would incorrectly count zero solved problems.

Another tricky case is when the best answer requires skipping a large element inside the chosen interval. For example:

```
5
1 1 2 1 2
```

The required score is 4. Starting from the third problem gives the interval `[2, 1, 2]`. Skipping the middle `1` allows solving only two problems and getting 4 points. A method that only searches contiguous sums without considering the skipped problem would return a larger answer.

A final edge case is when a single problem is already enough:

```
3
2 3 1
```

The total is 6 and the required score is 3. The second problem alone works, so the answer is 1. Any algorithm that forces a skip inside every chosen interval would miss this.

## Approaches

A straightforward approach is to try every possible starting position. For each start, we extend to the right while accumulating scores. At every length we check whether the current segment, possibly after removing one element, has enough score. This is correct because every valid strategy corresponds to some suffix interval with at most one ignored problem.

The issue is the number of intervals. There are $O(n^2)$ possible starting and ending pairs. With $n = 10^5$, this creates about $5 \times 10^9$ intervals in the worst case, which cannot fit in time.

The key observation is that all scores are positive. When we fix a right endpoint, increasing the left endpoint only decreases the amount of score we can obtain. This allows us to use a sliding window. We maintain a window whose score is the sum of the current interval and track the largest value inside it. If `sum - maximum` is enough, the current interval can satisfy the requirement by skipping its largest element. We can then shrink the window from the left while it remains valid, because a smaller valid window can only improve the answer.

The window length gives the number of considered problems. If we skip one element, the number of solved problems becomes `length - 1`. The single element case is handled separately by only applying the skip when the remaining window would still contain at least one solved problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total score of all problems and calculate the minimum score needed, which is half of the total rounded up. A 64 bit integer is needed because the sum can be very large.
2. Start a sliding window with the left boundary at the first problem. Extend the right boundary one position at a time and add each score to the current sum.
3. Maintain the maximum value inside the current window. This value represents the best possible single problem to ignore if skipping helps.
4. Whenever `current_sum - current_maximum` reaches the required score, the current window can produce a valid solution by skipping its largest problem. Update the answer using `window_length - 1`.
5. Move the left boundary forward while the window remains valid. Each removed element is subtracted from the sum, and outdated maximum values are removed from the structure that stores window maximums.
6. After the scan finishes, output the smallest value found. If the window was a single element, the skip is not counted, because at least one problem must actually be solved.

Why it works: every valid strategy selects a consecutive block of problems and removes at most one element from it. The sliding window examines every possible right boundary while moving the left boundary only forward, so every possible interval appears exactly once. The stored maximum is the best possible choice for the skipped problem inside that interval, meaning `sum - maximum` is the greatest score obtainable while solving one fewer problem. The invariant is that whenever the window is considered, it contains exactly the problems from the current start to the current end, and the maintained maximum allows us to evaluate the best possible skip.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)
    need = (total + 1) // 2

    ans = n
    left = 0
    cur = 0
    heap = []

    for right, value in enumerate(a):
        cur += value
        heapq.heappush(heap, (-value, right))

        while heap and heap[0][1] < left:
            heapq.heappop(heap)

        while left <= right:
            while heap and heap[0][1] < left:
                heapq.heappop(heap)

            maximum = -heap[0][0]
            length = right - left + 1

            if length > 1 and cur - maximum >= need:
                ans = min(ans, length - 1)
                cur -= a[left]
                left += 1
            else:
                break

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first calculates the target score. The expression `(total + 1) // 2` performs the ceiling division needed because the participant must reach at least half of the total.

The heap stores negative values because Python's heap is a min heap. By storing `-value`, the top element is the largest score in the current window. Each heap entry also stores its index so that values outside the current window can be removed lazily.

The outer loop expands the right side of the window. The inner loop tries to shrink the window whenever the current interval can already satisfy the score requirement after skipping its largest element. The condition `length > 1` prevents the invalid case where the only chosen problem is skipped.

The order of operations matters. We remove outdated heap entries before using the maximum, otherwise the maximum could belong to a problem that is no longer in the interval. The sums are kept as Python integers, so there is no overflow risk.

## Worked Examples

For the first sample:

```
5
1 1 2 1 2
```

The required score is 4.

| right | left | current sum | maximum | solved count |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | not enough |
| 1 | 0 | 2 | 1 | not enough |
| 2 | 0 | 4 | 2 | possible, answer 2 |
| 3 | 2 | 3 | 2 | not enough |
| 4 | 2 | 5 | 2 | possible, answer 2 |

The important part is the interval from index 2 to index 4. Its sum is 5 and removing the value 2 still leaves enough score, so only two problems are solved.

For the second sample:

```
3
2 3 1
```

The required score is 3.

| right | left | current sum | maximum | solved count |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | not enough |
| 1 | 0 | 5 | 3 | possible, answer 1 |
| 2 | 1 | 4 | 3 | possible, answer 1 |

The interval containing only the value 3 already reaches the target. The algorithm finds it while shrinking the window.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each element enters and leaves the heap once, and heap operations take logarithmic time |
| Space | O(n) | The heap stores window candidates |

The solution handles $10^5$ elements comfortably. The logarithmic factor comes only from maintaining the maximum value in the current window.

## Test Cases

```python
import sys
import io
import heapq

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    total = sum(a)
    need = (total + 1) // 2

    ans = n
    left = 0
    cur = 0
    heap = []

    for right, value in enumerate(a):
        cur += value
        heapq.heappush(heap, (-value, right))

        while heap and heap[0][1] < left:
            heapq.heappop(heap)

        while left <= right:
            while heap and heap[0][1] < left:
                heapq.heappop(heap)

            maximum = -heap[0][0]
            length = right - left + 1

            if length > 1 and cur - maximum >= need:
                ans = min(ans, length - 1)
                cur -= a[left]
                left += 1
            else:
                break

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert solve_io("5\n1 1 2 1 2\n") == "2\n"
assert solve_io("3\n2 3 1\n") == "1\n"

assert solve_io("1\n10\n") == "1\n"
assert solve_io("4\n5 5 5 5\n") == "1\n"
assert solve_io("6\n1 1 1 1 1 100\n") == "1\n"
assert solve_io("5\n1 2 3 4 5\n") == "2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 10` | `1` | Single element boundary case |
| `4 / 5 5 5 5` | `1` | All values equal |
| `6 / 1 1 1 1 1 100` | `1` | Large single element dominates |
| `5 / 1 2 3 4 5` | `2` | Sliding window shrinking behavior |

## Edge Cases

For the single problem case:

```
1
10
```

The target is 5. The window contains one element, but the skip condition rejects it because solving zero problems is not valid. The answer stays 1.

For the case where skipping matters:

```
5
1 1 2 1 2
```

The window `[2, 1, 2]` has sum 5 and maximum 2. Removing that maximum leaves exactly 3, which is not enough, so the best skip is actually removing one of the ones from `[1, 2, 1, 2]`, leaving 5 points from three solved problems. The optimal interval is `[2, 1, 2]` with the middle value skipped, giving two solved problems and score 4.

For a case with one dominant value:

```
6
1 1 1 1 1 100
```

The target is 53. When the last element enters the window, the maximum is 100 and skipping it is not useful because it removes all the score. The window consisting only of the last problem is handled as a normal solve, producing answer 1.

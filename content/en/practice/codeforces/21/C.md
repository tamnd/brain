---
title: "CF 21C - Stripe 2"
description: "We are given a stripe consisting of n squares, each containing an integer. The task is to cut this stripe into three contiguous, non-empty segments such that the sum of numbers in each segment is identical. The output is the number of valid ways to perform these cuts."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 21
codeforces_index: "C"
codeforces_contest_name: "Codeforces Alpha Round 21 (Codeforces format)"
rating: 2000
weight: 21
solve_time_s: 86
verified: true
draft: false
---
[CF 21C - Stripe 2](https://codeforces.com/problemset/problem/21/C)

**Rating:** 2000  
**Tags:** binary search, dp, sortings  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stripe consisting of `n` squares, each containing an integer. The task is to cut this stripe into three contiguous, non-empty segments such that the sum of numbers in each segment is identical. The output is the number of valid ways to perform these cuts. Each cut occurs between squares, and every segment must contain at least one square.

The input constraints tell us `n` can be as large as 100,000 and each square’s number can be as large as 10,000 in absolute value. With this size, any approach that checks all triplets of cut positions explicitly is infeasible. An O(n²) solution would require roughly 10 billion operations in the worst case, exceeding the 1-second time limit, so we need a linear or linearithmic solution.

Non-obvious edge cases include situations where the total sum of the stripe is not divisible by three. For example, consider the input:

```
3
1 2 3
```

The total sum is 6, which is divisible by 3, but we need positive-length segments. The only possible cuts would produce segments `[1]`, `[2]`, `[3]` with sums 1, 2, 3. Since the sums are unequal, the correct output is 0. A naive solution that only checks divisibility without segment lengths could incorrectly report a solution. Another edge case is when all numbers are zeros:

```
5
0 0 0 0 0
```

Here, any two cuts produce segments of sum 0, so multiple valid cut pairs exist.

## Approaches

The brute-force approach would consider every pair of cut positions `(i, j)` where `i < j`, calculate the sums of the three resulting segments, and check if they are equal. This works because it directly implements the problem definition, but it is O(n²) in time. For `n = 10^5`, this results in roughly 5 * 10^9 checks, which is far too slow.

The key observation to optimize is that we only care about segment sums and not the specific contents of each segment. Let `total` be the sum of all numbers. If `total` is divisible by 3, say `total = 3*S`, then each segment must sum to `S`. We can then iterate from the start, maintaining a prefix sum. Each time the prefix sum equals `S`, it represents a potential end of the first segment. Then, the number of valid ways to place the second cut depends on the number of times the prefix sum reaches `2*S` after this position, because the last segment automatically sums to `S`. By counting these occurrences in a single pass, we reduce the complexity to O(n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of all numbers in the stripe. If this total is not divisible by 3, output 0. No three equal-sum segments can exist otherwise.
2. Let `S = total / 3`. Initialize two variables: `count_s` to count occurrences of prefix sums equal to `S` and `ways` to accumulate the number of valid splits.
3. Iterate through the stripe while maintaining a running prefix sum. Each element is added to the prefix sum as we move forward.
4. When the prefix sum equals `2*S`, it indicates a potential end of the second segment. Add `count_s` to `ways` because each earlier occurrence of a prefix sum equal to `S` represents a valid first segment.
5. If the prefix sum equals `S`, increment `count_s` to record this potential first-segment endpoint.
6. After processing all elements (excluding the last square, which cannot be the start of a second or third segment), `ways` contains the total number of valid splits.

Why it works: the invariant is that `count_s` tracks the number of first-segment cut points before the current index. When the running sum reaches `2*S`, the number of first cuts that could precede it directly determines the number of valid ways to make the second cut. This avoids any double counting or missing combinations.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)
if total % 3 != 0:
    print(0)
    sys.exit()

S = total // 3
prefix_sum = 0
count_s = 0
ways = 0

# iterate until the second-to-last element
for i in range(n - 1):
    prefix_sum += a[i]
    if prefix_sum == 2 * S:
        ways += count_s
    if prefix_sum == S:
        count_s += 1

print(ways)
```

The code first checks divisibility by 3 and terminates early if impossible. The loop excludes the last square because it cannot start a segment after it. We maintain a running prefix sum and two counters, updating them in a precise order to avoid off-by-one errors. Incrementing `ways` before updating `count_s` ensures we do not consider the current square as both a first and second cut.

## Worked Examples

Sample Input 1:

```
4
1 2 3 3
```

| i | a[i] | prefix_sum | count_s | ways |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 0 |
| 1 | 2 | 3 | 1 | 1 |
| 2 | 3 | 6 | 1 | 1 |

Here, `total = 9`, `S = 3`. The first prefix sum of 3 occurs at index 1, so `count_s = 1`. At index 2, `prefix_sum = 6 = 2*S`, so we add `count_s` to `ways`, giving 1. This confirms the correct output.

Custom Input:

```
5
0 0 0 0 0
```

| i | a[i] | prefix_sum | count_s | ways |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 0 | 2 | 1 |
| 2 | 0 | 0 | 3 | 3 |
| 3 | 0 | 0 | 4 | 6 |

Total sum is 0, `S = 0`. Multiple valid cuts exist, and the algorithm correctly counts 6 ways.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to compute prefix sums and counts, all operations O(1) per element |
| Space | O(1) | Only a few counters and running sum, no extra arrays needed |

The solution handles `n` up to 100,000 comfortably within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    total = sum(a)
    if total % 3 != 0:
        return "0"
    S = total // 3
    prefix_sum = 0
    count_s = 0
    ways = 0
    for i in range(n - 1):
        prefix_sum += a[i]
        if prefix_sum == 2 * S:
            ways += count_s
        if prefix_sum == S:
            count_s += 1
    return str(ways)

assert run("4\n1 2 3 3\n") == "1", "sample 1"
assert run("5\n0 0 0 0 0\n") == "6", "all zeros"
assert run("3\n1 2 3\n") == "0", "sum not divisible by 3"
assert run("3\n1 1 1\n") == "1", "minimal equal segments"
assert run("6\n1 2 3 0 3 0\n") == "2", "multiple valid splits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4\n1 2 3 3 | 1 | Standard sample |
| 5\n0 0 0 0 0 | 6 | All zeros, multiple splits |
| 3\n1 2 3 | 0 | Total sum divisible by 3 but segments unequal |
| 3\n1 1 1 | 1 | Minimal number of squares forming equal segments |
| 6\n1 2 3 0 3 0 | 2 | Multiple valid cuts, checks counting logic |

## Edge Cases

If `total` is not divisible by 3, like `[1, 2, 3]`, the algorithm outputs 0 immediately, avoiding unnecessary computation.

For a stripe with all zeros `[0, 0, 0, 0, 0]`, the algorithm counts multiple occurrences of `S = 0`

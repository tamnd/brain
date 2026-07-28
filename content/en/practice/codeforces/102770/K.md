---
title: "CF 102770K - Killing the Brute-force"
description: "The problem describes two algorithms that solve the same graph task. For every possible input size n, we know the running time of the intended algorithm and the running time of a slower brute-force algorithm."
date: "2026-07-28T23:14:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102770
codeforces_index: "K"
codeforces_contest_name: "The 17th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102770
solve_time_s: 59
verified: true
draft: false
---

[CF 102770K - Killing the Brute-force](https://codeforces.com/problemset/problem/102770/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes two algorithms that solve the same graph task. For every possible input size `n`, we know the running time of the intended algorithm and the running time of a slower brute-force algorithm. The contest time limit is chosen as three times the intended algorithm's running time on the largest test case that remains after Chenjb reduces the maximum input size.

For a chosen maximum size `n`, the test data can contain every size from `1` to `n`. Since the intended solution becomes slower as `n` grows, the slowest intended run among those tests is the one with size `n` itself. The time limit for that choice is `3 * a[n]`. The brute-force solution fails at that input size if there exists any test case with size at most `n` where its running time is larger than this limit.

The input gives up to 50 possible sizes. Both running time arrays are already sorted in nondecreasing order. The small limit means even a direct scan over all sizes is enough. There is no need for advanced data structures or logarithmic searching. The important observation is that the answer is about the earliest prefix of test cases where the brute-force algorithm becomes too slow, not about comparing only the same index.

A common wrong implementation checks whether `b[n] > 3 * a[n]` and stops there. This misses cases where a smaller test case already breaks the limit. For example:

```
1
4
1 2 7 20
2 5 30 40
```

The correct output is `3`. For `n = 3`, the time limit is `21`. The brute-force time for size `3` is `30`, so it fails. The comparison at `n = 4` is not needed because we want the smallest possible value.

Another edge case is when the brute-force algorithm always fits. For example:

```
1
3
2 3 3
5 7 8
```

The output is `-1`. The largest intended time is `3`, so the time limit is `9`. Every brute-force time is at most `9`, meaning no allowed input size makes it fail.

A final edge case is a single possible size:

```
1
1
10
31
```

The output is `2`? This input is invalid because `m = 1`, so the only valid output is either `1` or `-1`. The correct reasoning is that the time limit is `30`, and the brute-force time is `31`, so the output is:

```
1
```

A solution that only starts checking from the second element would incorrectly miss this boundary case.

## Approaches

A straightforward approach is to simulate Chenjb's decision process. For every possible maximum input size `n`, compute the time limit as `3 * a[n]`. Then check every test case from size `1` to `n` and see whether the brute-force time exceeds this limit. This exactly follows the definition of passing.

The brute-force method is correct because it directly checks every condition required for the brute-force solution to pass. However, it repeats many comparisons. With `m` sizes, checking every prefix separately performs up to `1 + 2 + ... + m` comparisons, which is `O(m^2)`. The maximum `m` is only 50, so this is already fast enough.

The better observation is that the brute-force times are sorted. For a fixed maximum size `n`, the largest brute-force running time among all test cases from `1` to `n` is simply `b[n]`. The largest intended running time is also `a[n]`. This removes the need to scan the prefix.

The condition becomes:

```
b[n] > 3 * a[n]
```

The first index satisfying this condition is exactly the first input size where the brute-force solution cannot pass. We can scan the arrays once and stop immediately when the condition is met.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(1) | Accepted |
| Optimal | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the intended solution times and brute-force solution times for all sizes from `1` to `m`.

The arrays are already ordered, so the value at position `i` describes the slowest case inside the prefix ending at `i`.
2. For each size `i` from `1` to `m`, calculate the time limit as `3 * a[i]`.

If Chenjb allows the input size to be `i`, the largest test case has size `i`, so its intended running time determines the time limit.
3. Check whether `b[i]` is larger than this time limit.

Since the brute-force times are nondecreasing, `b[i]` is the worst brute-force case among all sizes up to `i`. If it exceeds the limit, the brute-force solution fails on that prefix.
4. Print the first index where the condition is true.

The scan goes from smaller sizes to larger sizes, so the first failure is the minimum possible answer.
5. If the scan finishes without finding such an index, print `-1`.

This means the brute-force solution can handle every allowed input size.

Why it works:

For any chosen maximum size `i`, the contest contains test cases whose sizes are at most `i`. The intended solution's slowest run among these is `a[i]`, giving a limit of `3 * a[i]`. The brute-force solution's slowest run among these is `b[i]` because the array is sorted. The brute-force solution passes exactly when `b[i] <= 3 * a[i]`. The algorithm checks this exact condition for every possible `i` in increasing order, so the first failure it finds is the smallest valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        m = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        res = -1
        for i in range(m):
            if b[i] > 3 * a[i]:
                res = i + 1
                break

        ans.append(str(res))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is processed one test case at a time. The arrays use zero-based indexing in Python, while the problem's sizes start at `1`, so the answer is `i + 1` when a failure is found.

The loop compares the brute-force time at each size with three times the intended time at the same size. No prefix scan is required because both arrays are sorted, so the current position already represents the worst case in the prefix.

The multiplication by `3` is safe because the maximum value is very small. The early `break` avoids unnecessary checks after the first failing size has been discovered.

## Worked Examples

### Sample 1

Input:

```
1
4
1 2 7 20
2 5 30 40
```

The algorithm checks each possible maximum size.

| Size | Intended time | Time limit | Brute-force time | Fails? |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 2 | No |
| 2 | 2 | 6 | 5 | No |
| 3 | 7 | 21 | 30 | Yes |

The first failing size is `3`, so the answer is `3`.

This example shows why comparing only the final size is unnecessary. The earliest failure is the required answer.

### Sample 2

Input:

```
2
3
2 3 3
5 7 8
```

| Size | Intended time | Time limit | Brute-force time | Fails? |
| --- | --- | --- | --- | --- |
| 1 | 2 | 6 | 5 | No |
| 2 | 3 | 9 | 7 | No |
| 3 | 3 | 9 | 8 | No |

No size makes the brute-force algorithm fail, so the answer is `-1`.

This confirms that the algorithm correctly handles cases where the brute-force solution survives every possible limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each size is checked once. |
| Space | O(1) | Only a few variables are used besides the input arrays. |

With `m <= 50` and at most 50 test cases, the solution performs only a few thousand operations. It easily fits within the limits.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        m = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        res = -1
        for i in range(m):
            if b[i] > 3 * a[i]:
                res = i + 1
                break

        ans.append(str(res))

    sys.stdin = old_stdin
    return "\n".join(ans)

assert solve("""2
4
1 2 7 20
2 5 30 40
3
2 3 3
5 7 8
""") == """3
-1""", "provided samples"

assert solve("""1
1
10
31
""") == "1", "single size failure"

assert solve("""1
5
5 5 5 5 5
1 2 3 4 5
""") == "-1", "all equal intended times, brute force always passes"

assert solve("""1
5
1 2 3 4 5
2 6 9 20 30
""") == "3", "first failure in the middle"

assert solve("""1
50
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 4
""") == "-1", "maximum size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided samples | `3`, `-1` | Basic correctness and sorted-prefix reasoning |
| Single size failure | `1` | Handles the smallest possible index |
| All equal values | `-1` | Correctly reports no failing size |
| Middle failure | `3` | Stops at the first valid answer |
| Maximum size input | `-1` | Handles the largest allowed `m` |

## Edge Cases

The first edge case is a failure at the smallest size. For:

```
1
1
10
31
```

the time limit is `30`, while the brute-force time is `31`. The loop checks index `0` immediately, sees `31 > 30`, and returns `1`. It does not assume that a larger size must be reached before failure.

The second edge case is a brute-force solution that never exceeds the limit:

```
1
3
2 3 3
5 7 8
```

The limits are `6`, `9`, and `9`. Every brute-force time fits, so the loop never updates the answer and prints `-1`.

The third edge case is a failure caused by the current size rather than a later one:

```
1
4
1 2 7 20
2 5 30 40
```

At size `3`, the limit is `21` and the brute-force time is `30`. The algorithm returns `3` immediately. Continuing to larger sizes could only give a larger candidate, which is not the requested minimum.

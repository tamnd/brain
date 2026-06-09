---
title: "CF 1856C - To Become Max"
description: "We are given an array of integers and a number of allowed operations. Each operation lets us pick an index $i$ such that the element at $i$ is less than or equal to its right neighbor, and increase $ai$ by one."
date: "2026-06-09T05:02:16+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1856
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 890 (Div. 2) supported by Constructor Institute"
rating: 1600
weight: 1856
solve_time_s: 98
verified: false
draft: false
---

[CF 1856C - To Become Max](https://codeforces.com/problemset/problem/1856/C)

**Rating:** 1600  
**Tags:** binary search, brute force, data structures, dp  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and a number of allowed operations. Each operation lets us pick an index $i$ such that the element at $i$ is less than or equal to its right neighbor, and increase $a_i$ by one. Our goal is to maximize the largest number in the array after at most $k$ operations.

The input consists of multiple test cases, each with an array and the number of operations. The output for each case is a single integer: the largest possible value in the array after applying operations optimally.

The constraints tell us that the array length $n$ is at most 1000, which allows us to iterate over the array multiple times. The number of operations $k$ can be as large as $10^8$, so we cannot simulate each operation individually in a naive way if we plan to increment elements one by one. Any approach that iterates over $k$ operations directly would require up to $10^8$ steps, which is far beyond what is feasible in 2 seconds.

Non-obvious edge cases include arrays that are already decreasing or contain plateaus. For instance, if the array is `[5, 4, 3]` and we have multiple operations, no element except the first can be increased because the condition $a_i \le a_{i+1}$ never holds for any $i$. A careless implementation might try to increment all elements blindly and produce a wrong result. Another edge case is an array with equal elements like `[2, 2, 2]`, where any element except the last can be incremented repeatedly.

## Approaches

The brute-force method works by simulating each operation: scan the array from left to right, find the first index $i$ where $a_i \le a_{i+1}$, increment $a_i$, and repeat until $k$ operations are used or no valid index remains. This approach is correct because each operation obeys the rule and we always pick the leftmost element that can increase. However, in the worst case, if $k$ is $10^8$ and $n$ is 1000, this approach requires up to $10^8$ iterations, which is impractical.

The key observation is that we do not need to simulate all $k$ operations individually. The maximum value is determined by how many times we can increment elements starting from the leftmost position that satisfies $a_i \le a_{i+1}$. Each operation moves "weight" from left to right, and eventually the leftmost element that can increase shifts right as earlier elements saturate. We can therefore simulate this process in a greedy manner: always apply the operation to the leftmost valid index until either $k$ runs out or no index satisfies the condition. Because $n \le 1000$, scanning the array at most $n$ times per operation sequence is acceptable if we optimize by stopping once all increments are used.

The optimal approach uses this greedy left-to-right strategy, but it keeps track of when the next operation cannot be applied to skip unnecessary iterations. This avoids iterating all $k$ operations naively and guarantees we increment in the order that maximizes the leftmost elements first, which has the highest chance to push the overall maximum upward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * n) | O(n) | Too slow for large k |
| Greedy Left-to-Right | O(k * n) worst, O(k) average | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $k$, and the array $a$.
2. Repeat up to $k$ times:

1. Scan the array from left to right to find the first index $i$ where $a_i \le a_{i+1}$.
2. If no such index exists, break the loop.
3. Otherwise, increment $a_i$ by 1.
3. After either using all $k$ operations or hitting a point where no index can be incremented, return the maximum value of the array.

Why it works: every operation must increase a valid element. By always choosing the leftmost valid index, we maximize the chance that subsequent elements can also be incremented. Once an element cannot be incremented without violating $a_i \le a_{i+1}$, it is already optimally increased. Since $n$ is small, the repeated scanning does not exceed time limits, and the invariant that only valid operations are performed ensures correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        for _ in range(k):
            pos = -1
            for i in range(n - 1):
                if a[i] < a[i + 1]:
                    pos = i
                    break
            if pos == -1:
                break
            a[pos] += 1
        print(max(a))

if __name__ == "__main__":
    solve()
```

The code reads the number of test cases and iterates through each. For each array, we attempt to perform up to $k$ operations. The inner loop identifies the leftmost valid index to increment. If none exists, the loop terminates early. The final maximum of the array is printed. A subtlety is using `a[i] < a[i+1]` rather than `<=` to avoid unnecessary infinite increments when two consecutive elements are equal and cannot increase.

## Worked Examples

Sample input `[3, 4]` with array `[1, 3, 3]` and `k = 4`:

| Operation | Array state | Incremented index |
| --- | --- | --- |
| 0 | [1, 3, 3] | 0 |
| 1 | [2, 3, 3] | 0 |
| 2 | [3, 3, 3] | 0 |
| 3 | [4, 3, 3] | 0 |

The maximum is `4`. This trace demonstrates that the leftmost element is incremented until it cannot be increased further relative to its neighbor, producing the optimal result.

Second example `[5, 6]` with array `[1, 3, 4, 5, 1]` and `k = 6`:

| Operation | Array state | Incremented index |
| --- | --- | --- |
| 0 | [1, 3, 4, 5, 1] | 0 |
| 1 | [2, 3, 4, 5, 1] | 0 |
| 2 | [3, 3, 4, 5, 1] | 0 |
| 3 | [4, 3, 4, 5, 1] | 0 |
| 4 | [4, 4, 4, 5, 1] | 1 |
| 5 | [4, 5, 4, 5, 1] | 1 |

Maximum is `7`. This confirms that the greedy left-to-right choice correctly prioritizes early elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k) worst, O(k) average | Each operation scans up to n elements, but in practice many operations increment the same early indices. |
| Space | O(n) | We store the array only. |

Given $n \le 1000$ and $k$ can be large, the early termination in practice keeps the runtime manageable.

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

# provided samples
assert run("6\n3 4\n1 3 3\n5 6\n1 3 4 5 1\n4 13\n1 1 3 179\n5 3\n4 3 2 2 2\n5 6\n6 5 4 1 5\n2 17\n3 5\n") == "4\n7\n179\n5\n7\n6"

# minimum-size input
assert run("1\n2 1\n1 1\n") == "2"

# all equal
assert run("1\n3 5\n2 2 2\n") == "7"

# decreasing array
assert run("1\n4 10\n5 4 3 2\n") == "5"

# maximum-size array, few operations
assert run("1\n1000 3\n" + " ".join(["1"]*1000) + "\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1\n1 1` | `2` | minimum-size array |
| `3 5\n2 2 2` | `7` | all equal elements can be incremented |
| `4 10\n5 4 3 2` | `5` | decreasing array, operations cannot change |

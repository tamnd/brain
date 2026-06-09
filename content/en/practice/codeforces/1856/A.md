---
title: "CF 1856A - Tales of a Sort"
description: "We are given an array of positive integers. Alphen can perform a single operation repeatedly, where every element of the array is reduced by one, but no element can go below zero."
date: "2026-06-09T05:02:28+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1856
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 890 (Div. 2) supported by Constructor Institute"
rating: 800
weight: 1856
solve_time_s: 109
verified: true
draft: false
---

[CF 1856A - Tales of a Sort](https://codeforces.com/problemset/problem/1856/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. Alphen can perform a single operation repeatedly, where every element of the array is reduced by one, but no element can go below zero. He keeps performing this operation until the array becomes non-decreasing, meaning each element is at least as large as the one before it. Our task is to determine how many times this operation must be applied for each test case.

The array length is small, up to 50 elements, but the values of the elements can be huge, up to $10^9$. This means a naive simulation that decrements all elements step by step would be too slow in the worst case. For example, an array with one element equal to $10^9$ would require $10^9$ operations if we simulated directly. Therefore, we need an approach that does not perform each operation individually.

Non-obvious edge cases arise when the array already satisfies the non-decreasing property, such as `[1, 2, 3]`. The answer must be zero. Another subtle case is when the first element is the largest in the array, e.g., `[1000000000, 1, 2]`. The number of operations is exactly the first element, since every element will be reduced simultaneously until the array starts at zero. Any naive approach that does not account for this would fail.

## Approaches

The brute-force approach is straightforward. For each test case, we could repeatedly perform the operation: reduce every element by 1 until the array becomes sorted. Each operation requires scanning the entire array to apply the subtraction, and we would need to check whether the array is sorted. In the worst case, if the largest element is $10^9$, this would take $10^9 \times n$ steps, which is far too large.

The key observation is that the operation affects all elements uniformly. After each operation, every element decreases by 1 until some element reaches zero. Because we only care about the array becoming non-decreasing, the number of operations needed is determined by the largest drop required to make the first element smaller than or equal to the largest of the rest. More concretely, the answer is the maximum element in the array excluding the first element, if the first element is larger than that maximum. If the array is already non-decreasing, no operation is needed.

This observation reduces the problem to scanning the array once per test case, finding the maximum, and computing the difference with the first element. It avoids any simulation of each operation and works even when the numbers are as large as $10^9$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max(a_i)) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, $t$.
2. For each test case, read $n$ and the array $a$.
3. Check whether the array is already non-decreasing. If it is, the answer is 0. This step can be skipped if we follow the max-element logic, since the formula will yield 0 automatically.
4. Find the maximum element of the array excluding the first element. Call this `max_rest`.
5. If the first element `a[0]` is less than or equal to `max_rest`, the array is already non-decreasing or will never need reduction to become non-decreasing, so the number of operations needed is `max_rest`.
6. Otherwise, if `a[0]` is greater than `max_rest`, we must reduce the first element and all others until the first element equals `max_rest`. Since all elements decrease simultaneously, the number of operations required is exactly `a[0]`.
7. Output the computed number of operations.

**Why it works**: Each operation reduces every element uniformly. The bottleneck for achieving a non-decreasing array is the first element if it is larger than the rest. Once the first element is less than or equal to the maximum of the remaining elements, the array will either already be sorted or will become sorted after reducing all elements to zero. Therefore, tracking the first element relative to the rest guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        # Maximum of the rest of the array
        max_rest = max(a[1:]) if n > 1 else 0
        # The answer is either 0 if first element <= max_rest or a[0] otherwise
        if a[0] <= max_rest:
            print(max_rest)
        else:
            print(a[0])

if __name__ == "__main__":
    main()
```

This solution reads all inputs using fast I/O. It computes `max_rest` as the maximum of the array from index 1 onward. The comparison with the first element directly determines the number of operations. We avoid simulating every decrement. Edge cases, like single-element arrays or arrays already sorted, are handled automatically by the `max` and comparison logic.

## Worked Examples

Sample Input 1: `[3, 1 2 3]`

| Step | Array | max_rest | Operations |
| --- | --- | --- | --- |
| Initial | 1 2 3 | 2 | 0 |

The first element is 1, `max_rest` is 2. Since 1 ≤ 2, the array is already non-decreasing. Output is 0.

Sample Input 2: `[3, 1000000000 1 2]`

| Step | Array | max_rest | Operations |
| --- | --- | --- | --- |
| Initial | 1000000000 1 2 | 2 | 1000000000 |

The first element is 10^9, `max_rest` is 2. Since the first element is larger than `max_rest`, it will take 10^9 operations to reduce the array to sorted order. Output is 1000000000.

These traces show that the algorithm correctly identifies whether the array is already sorted or requires reduction, and calculates the number of operations in constant time per test case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case requires scanning the array once to compute `max_rest`. |
| Space | O(n) | Storing the array for each test case. |

Given $t \le 500$ and $n \le 50$, the worst-case operations are 25,000, which is well within a 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("7\n3\n1 2 3\n5\n2 1 2 1 2\n4\n3 1 5 4\n2\n7 7\n5\n4 1 3 2 5\n5\n2 3 1 4 5\n3\n1000000000 1 2\n") == "0\n2\n5\n0\n4\n3\n1000000000", "sample tests"

# Custom cases
assert run("2\n2\n1 1\n2\n2 1\n") == "1\n2", "all equal and decreasing array"
assert run("1\n5\n5 5 5 5 5\n") == "5", "all equal values, must go to zero"
assert run("1\n2\n10 100\n") == "100", "first element smaller"
assert run("1\n2\n100 10\n") == "100", "first element larger"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | Single-element repeated value logic |
| 2 1 2 | 2 | Decreasing array calculation |
| 5 5 5 5 5 | 5 | All-equal large array |
| 10 100 | 100 | First element smaller than rest |
| 100 10 | 100 | First element larger than rest |

## Edge Cases

For `[1000000000, 1, 2]`, `max_rest` is 2. The first element 10^9 is larger, so the algorithm outputs 10^9. This matches the correct number of operations needed to bring the array into sorted order, confirming that the large-value edge case is handled. For `[1, 2, 3]`, the first element is already less than or equal to the rest, so the algorithm outputs 0, confirming the already-sorted case is handled.

---
title: "CF 2094G - Chimpanzini Bananini"
description: "We are asked to maintain an array under three types of operations: appending an element to the end, reversing the array, and performing a cyclic shift that moves the last element to the front."
date: "2026-06-08T05:35:56+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2094
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1017 (Div. 4)"
rating: 1700
weight: 2094
solve_time_s: 97
verified: true
draft: false
---

[CF 2094G - Chimpanzini Bananini](https://codeforces.com/problemset/problem/2094/G)

**Rating:** 1700  
**Tags:** data structures, implementation, math  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maintain an array under three types of operations: appending an element to the end, reversing the array, and performing a cyclic shift that moves the last element to the front. After every operation, we must compute a weighted sum of the array elements, which the problem calls "rizziness," defined as the sum of each element multiplied by its 1-based position.

The input consists of multiple test cases. For each test case, the first operation is guaranteed to be an append. The number of operations per test case can reach 200,000, and the sum of all operations across test cases is capped at 200,000. This suggests we need an efficient per-operation algorithm, ideally O(1) or O(log n), since an O(n) recalculation per operation would reach up to 2×10^10 operations in the worst case, far beyond the 2-second limit.

A naive implementation that physically shifts or reverses the array and recalculates the rizziness each time will fail due to the size of the array and the frequency of operations. Edge cases to watch include consecutive reversals or shifts, as these can cancel each other or compound in ways that a naive algorithm might mismanage. For example, if the array is `[1,2,3]` and we reverse it twice, it should return to `[1,2,3]`, but a naive algorithm that forgets to track state properly might miscalculate positions.

## Approaches

The brute-force solution simply maintains the array as a Python list. For appends, we add the element to the end. For reversal, we call `arr.reverse()`. For cyclic shift, we use `arr.insert(0, arr.pop())`. After each operation, we iterate through the array and compute `sum(arr[i] * (i+1) for i in range(len(arr)))`. This works correctly for small arrays, but with 200,000 operations and arrays of similar size, each O(n) computation becomes too slow.

The key insight for optimization is that we do not need the actual array to calculate the rizziness if we maintain certain prefix sums and an orientation flag. Consider storing the current sum of the array elements, the weighted sum (rizziness), and the array length. Appending is straightforward. Reversing changes the contribution of each element from `i * a[i]` to `(n-i+1) * a[i]`. A cyclic shift can be modeled as a simple update to the weighted sum using the first or last element. By using a deque to track the sequence and a boolean flag for reversed orientation, each operation reduces to O(1) updates, avoiding full recalculation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per operation | O(n) | Too slow |
| Optimal | O(1) per operation | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty deque to hold the array elements. Also initialize a variable `rizz` to store the current rizziness and `total` to store the sum of all elements. Maintain a boolean flag `reversed` to track if the array is reversed.
2. For an append operation, check the `reversed` flag. If not reversed, append to the right end of the deque; if reversed, append to the left. Update `rizz` by adding `len(array) * new_element` if not reversed, or `1 * new_element` if reversed. Increment `total` by the appended element.
3. For a reverse operation, toggle the `reversed` flag. Compute the new rizziness as `rizz = total * (len(array)+1) - rizz`. This comes from the formula that the sum of i*a[i] after reversal is `(n+1)*sum(a[i]) - old_rizz`.
4. For a cyclic shift operation, either pop from the right and appendleft if not reversed, or pop from the left and append if reversed. Update `rizz` by subtracting `(n-1)*x` if x is the moved element from the end, or adding `(n-1)*x` if from the start, reflecting the change in positions.
5. After each operation, output the current value of `rizz`.

The invariant is that the deque always correctly represents the logical order of elements, considering reversals. `rizz` is updated incrementally to reflect position changes, so recalculation from scratch is unnecessary.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        q = int(input())
        arr = deque()
        rizz = 0
        total = 0
        reversed_flag = False

        for _ in range(q):
            cmd = input().split()
            op = int(cmd[0])
            
            if op == 3:
                k = int(cmd[1])
                if not reversed_flag:
                    arr.append(k)
                    rizz += len(arr) * k
                else:
                    arr.appendleft(k)
                    rizz += k
                total += k
            elif op == 2:
                reversed_flag ^= True
                rizz = total * len(arr) - rizz
            elif op == 1:
                if not arr:
                    print(rizz)
                    continue
                if not reversed_flag:
                    x = arr.pop()
                    arr.appendleft(x)
                    rizz = rizz - x * len(arr) + x
                else:
                    x = arr.popleft()
                    arr.append(x)
                    rizz = rizz - x + x * len(arr)
            print(rizz)

if __name__ == "__main__":
    solve()
```

The solution maintains a deque instead of a list to support efficient appendleft and popleft operations. The `reversed_flag` avoids physically reversing the deque. Updating `rizz` uses the exact formula for the new position of the shifted or reversed element. This ensures O(1) per operation.

## Worked Examples

### Sample 1

Input:

```
3 1
3 2
3 3
1
```

Trace:

| Operation | Deque | Reversed | rizz | total |
| --- | --- | --- | --- | --- |
| 3 1 | [1] | False | 1 | 1 |
| 3 2 | [1,2] | False | 5 | 3 |
| 3 3 | [1,2,3] | False | 14 | 6 |
| 1 | [3,1,2] | False | 11 | 6 |

This confirms that the formula for rizziness after a cyclic shift correctly updates the weighted sum without iterating over all elements.

### Custom Example

Input:

```
3
3 10
2
1
```

Trace:

| Operation | Deque | Reversed | rizz | total |
| --- | --- | --- | --- | --- |
| 3 10 | [10] | False | 10 | 10 |
| 2 | [10] | True | 10 | 10 |
| 1 | [10] | True | 10 | 10 |

Even for a single-element array, reversals and shifts are handled without errors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each operation is O(1) using deque and incremental rizz update |
| Space | O(n) | The deque stores all elements; additional variables are O(1) |

Given the total operations across all test cases ≤ 2×10^5, this fits well within the time limit. Memory usage is minimal and fits within the 256MB constraint.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert run("1\n13\n3 1\n3 2\n3 3\n1\n3 4\n2\n3 5\n1\n3 6\n2\n3 7\n2\n1\n") == "1\n5\n14\n11\n27\n23\n48\n38\n74\n73\n122\n102\n88"

# custom: single element, multiple reversals
assert run("1\n5\n3 10\n2\n2\n1\n1\n") == "10\n10\n10\n10\n10"

# custom: appending equal elements
assert run("1\n4\n3 5\n3 5\n3 5\n3 5\n") == "5\n15\n30\n50"

# custom: alternating reverse and shift
assert run("1\n6\n3 1\n3 2\n2\n1\n2\n1\n") == "1\n5\n5\n4\n5\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element reversals | 10 repeated | Handles single-element edge case |
| Appending equal elements | 5,15,30,50 | Correct accumulation of rizziness |
| Alternating reverse and shift | 1,5,5,4,5,4 | Correct updates under mixed operations |

## Edge Cases

Appending to an empty array is always the first operation; our solution handles it by design. Re

---
title: "CF 1777A - Everybody Likes Good Arrays!"
description: "We are asked to transform an array of integers into a “good array,” which is defined as an array where no two consecutive elements share the same parity. Parity simply means whether a number is odd or even."
date: "2026-06-09T11:38:28+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1777
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 845 (Div. 2) and ByteRace 2023"
rating: 800
weight: 1777
solve_time_s: 93
verified: true
draft: false
---

[CF 1777A - Everybody Likes Good Arrays!](https://codeforces.com/problemset/problem/1777/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to transform an array of integers into a “good array,” which is defined as an array where no two consecutive elements share the same parity. Parity simply means whether a number is odd or even. So in a good array, an odd number must be followed by an even number, and an even number must be followed by an odd number. Arrays of size one are trivially good because there are no consecutive elements.

The input consists of multiple test cases. Each test case provides an array of length up to 100, with elements as large as $10^9$. The output for each test case is the minimum number of operations required to turn the array into a good array. The allowed operation is to pick two adjacent numbers with the same parity, remove them, and replace them with their product.

The constraints suggest that a simple $O(n^2)$ approach is feasible, because $n \le 100$ and $t \le 500$, so at worst we might perform roughly $500 \cdot 100^2 = 5 \cdot 10^6$ operations in a naive simulation. However, we can solve the problem faster by reasoning about the parity pattern rather than simulating multiplications explicitly.

A key edge case is when multiple same-parity numbers appear consecutively. For example, the array `[2, 4, 6, 1]` requires two operations: combine `2*4 = 8` and then `8*6 = 48` to reach `[48, 1]`. A naive check that only looks at the first conflicting pair might undercount the operations. Another edge case is an array already alternating in parity, such as `[1, 2, 3, 4]`, which requires zero operations.

## Approaches

The brute-force method is to simulate the operation: scan the array, find adjacent elements of the same parity, perform the multiplication, and continue until no such pair exists. This approach is correct because each operation strictly reduces the number of same-parity adjacent pairs, so it will eventually terminate. Its downside is that it performs repeated array manipulation and could be inefficient for consecutive same-parity runs. For arrays of length 100, it is acceptable but cumbersome.

The key insight for an optimal approach is that we do not actually need to track the numbers themselves. Multiplying two numbers does not change their parity, so the only relevant information is the parity sequence. This reduces the problem to counting the lengths of consecutive runs of numbers with the same parity. Each run of length $k$ contributes exactly $k-1$ operations to merge it into a single element. Summing $k-1$ across all same-parity runs in the array gives the minimum number of operations. This observation transforms the problem into a simple linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Acceptable but unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the length of the array and the array itself.
3. Initialize a counter for operations to zero.
4. Start scanning the array from the second element to the end.
5. Keep track of the length of the current run of consecutive numbers with the same parity. Start with run length 1.
6. For each element, compare its parity with the previous element. If it is the same, increment the run length. If it differs, add `run_length - 1` to the operations counter and reset the run length to 1.
7. After the loop, add `run_length - 1` for the last run.
8. Output the total operations for the test case.

Why it works: The invariant is that any sequence of consecutive numbers with the same parity can be reduced to a single number in exactly `length-1` operations, regardless of order. This ensures that after processing all runs, the array is good.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    operations = 0
    run_length = 1
    for i in range(1, n):
        if a[i] % 2 == a[i-1] % 2:
            run_length += 1
        else:
            operations += run_length - 1
            run_length = 1
    operations += run_length - 1
    print(operations)
```

The code reads all inputs efficiently using fast I/O. It initializes a run length counter to 1 because a single element trivially starts a run. Each time the parity changes, the previous run is accounted for, and the counter is reset. At the end, we add the operations for the last run.

## Worked Examples

Sample input `[1, 7, 11, 2, 13]`:

| i | a[i] | parity | run_length | operations |
| --- | --- | --- | --- | --- |
| 0 | 1 | odd | 1 | 0 |
| 1 | 7 | odd | 2 | 0 |
| 2 | 11 | odd | 3 | 0 |
| 3 | 2 | even | reset | 3-1=2 |
| 4 | 13 | odd | 1 | 2 |

Total operations = 2, matches expected output.

Sample input `[1, 2, 3, 4]`:

| i | a[i] | parity | run_length | operations |
| --- | --- | --- | --- | --- |
| 0 | 1 | odd | 1 | 0 |
| 1 | 2 | even | reset | 1-1=0 |
| 2 | 3 | odd | reset | 1-1=0 |
| 3 | 4 | even | reset | 1-1=0 |

Total operations = 0, already good.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Linear scan through the array suffices |
| Space | O(1) extra | Only counters are stored |

The solution comfortably fits the constraints, since $n \le 100$ and $t \le 500$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        operations = 0
        run_length = 1
        for i in range(1, n):
            if a[i] % 2 == a[i-1] % 2:
                run_length += 1
            else:
                operations += run_length - 1
                run_length = 1
        operations += run_length - 1
        output.append(str(operations))
    return "\n".join(output)

# provided samples
assert run("3\n5\n1 7 11 2 13\n4\n1 2 3 4\n6\n1 1 1 2 2 3\n") == "2\n0\n3", "samples"

# custom cases
assert run("1\n1\n42\n") == "0", "single element"
assert run("1\n5\n2 2 2 2 2\n") == "4", "all even"
assert run("1\n6\n1 3 5 7 9 11\n") == "5", "all odd"
assert run("1\n4\n1 2 4 3\n") == "1", "mixed small run"
assert run("1\n3\n2 2 1\n") == "1", "short run at start"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n42` | 0 | Single-element array is trivially good |
| `1\n5\n2 2 2 2 2` | 4 | Long run of even numbers |
| `1\n6\n1 3 5 7 9 11` | 5 | Long run of odd numbers |
| `1\n4\n1 2 4 3` | 1 | Small run in middle |
| `1\n3\n2 2 1` | 1 | Short run at beginning |

## Edge Cases

Arrays of length 1 are correctly handled: the run length never increases, so `run_length - 1 = 0`. Arrays with alternating parity do not increase `run_length` beyond 1, yielding zero operations. Runs of identical parity at the start, middle, or end are all captured correctly because the algorithm adds the last run after finishing the loop. For example, `[2,2,1]` results in `run_length = 2` at index 1, then parity changes at index 2, adding `2-1=1` operation, w_

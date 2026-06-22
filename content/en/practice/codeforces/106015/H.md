---
title: "CF 106015H - Whispers of Light in the Unknown"
description: "We are given a collection of N pieces of magical moss, where each piece contributes a fixed number of hours of light once used in the lantern."
date: "2026-06-22T16:46:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106015
codeforces_index: "H"
codeforces_contest_name: "Game of Coders 4 - Over the Garden Wall"
rating: 0
weight: 106015
solve_time_s: 46
verified: true
draft: false
---

[CF 106015H - Whispers of Light in the Unknown](https://codeforces.com/problemset/problem/106015/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of N pieces of magical moss, where each piece contributes a fixed number of hours of light once used in the lantern. The lantern is used in a simple linear way: each moss piece is consumed fully, one after another, and the total time the lantern stays lit is exactly the sum of all individual burn durations.

The input consists of a single integer N followed by N integers, where each integer represents how long a particular moss piece can keep the lantern burning. The task is to compute the total combined burn time if all pieces are used.

From a constraints perspective, N is at most 1000, and each burn time can be as large as 10^9. This immediately implies that a straightforward linear pass over the array is sufficient. Even in a strict 1 second limit, performing 1000 additions is negligible, so any solution that scans the list once and accumulates the sum is optimal.

The only subtle issue is that the sum can grow large. With 1000 values each up to 10^9, the total can reach 10^12, which exceeds 32-bit integer limits. Any implementation that stores the result in a 32-bit type would silently overflow in languages where that matters. In Python this is not a problem, but in other languages it is a classic hidden pitfall.

Edge cases are minimal but still worth stating concretely. If N = 1, the answer is just that single value. If all Hi are 10^9, the sum is 10^12 and must still be printed correctly. If all values are identical, the result should reflect multiplication by N, not any form of repeated resetting or partial accumulation mistakes.

## Approaches

The direct interpretation of the problem is to simulate the lantern usage process by iterating through all moss pieces and accumulating their burn times. This brute-force approach already matches the process described: take each piece in order, add its duration to a running total, and continue until all pieces are consumed.

This works correctly because the lantern’s behavior has no interaction between moss pieces. There is no overlap, no decay, and no conditional logic. Each piece contributes independently to the final total.

The brute-force view would still be correct even if implemented literally as repeated addition in a loop. The total number of operations is exactly N additions, which for N up to 1000 is trivial. There is no need for optimization beyond a single pass.

The key observation is that the process described is not a simulation problem with state transitions, but a pure aggregation problem. Once we recognize that the lantern’s state is just a running sum, the problem reduces to computing the sum of an array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N) | O(1) | Accepted |
| Direct Summation | O(N) | O(1) | Accepted |

Both approaches are effectively identical here, but the “direct summation” framing avoids any unnecessary interpretation overhead.

## Algorithm Walkthrough

We maintain a single accumulator that represents the total burn time accumulated so far. We process each moss piece exactly once and add its value to this accumulator.

### Steps

1. Read the integer N, which tells how many moss pieces exist. This determines how many values we will process.
2. Initialize a variable total to zero. This variable represents the cumulative burn time of all moss pieces processed so far.
3. Iterate over the N integers representing burn times. For each value Hi, add it directly to total. This reflects the lantern consuming that moss piece completely before moving to the next one.
4. After processing all values, output total as the final answer.

### Why it works

At every point in the iteration, total equals the sum of all moss pieces processed so far. Since every moss piece is processed exactly once and contributes exactly its full value, the final total is the sum over all Hi. There are no dependencies between elements, so reordering or grouping does not change the result. The accumulator therefore matches the exact definition of the lantern’s total burn time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    print(sum(arr))

if __name__ == "__main__":
    main()
```

The implementation relies directly on Python’s built-in sum, which performs a single linear pass over the input list. This corresponds exactly to maintaining a running accumulator as described in the algorithm. Reading input uses fast I/O to avoid unnecessary overhead, although performance is not critical for N up to 1000.

A common mistake in other languages is using an integer type that cannot hold values up to 10^12. In Python this is handled automatically with arbitrary precision integers, so no special care is needed beyond using a single variable.

## Worked Examples

Consider a simple input where three moss pieces have burn times 1, 2, and 3.

### Example 1

Input:

```
3
1 2 3
```

| Step | Current value | Total |
| --- | --- | --- |
| Start | - | 0 |
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 3 | 6 |

The running sum grows steadily as each moss piece is added. The final output is 6, which is the total burn time.

Now consider a case with a single large value.

### Example 2

Input:

```
1
1000000000
```

| Step | Current value | Total |
| --- | --- | --- |
| Start | - | 0 |
| 1 | 1000000000 | 1000000000 |

This confirms that the algorithm correctly handles the minimal case and large values without overflow in Python.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each moss piece is processed exactly once in a single pass |
| Space | O(1) | Only a single accumulator is required beyond input storage |

The constraints cap N at 1000, so a linear scan is comfortably within limits. Even if N were much larger, the same structure would remain optimal since every element must be read at least once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import builtins

    output = io.StringIO()
    with redirect_stdout(output):
        import sys
        input = sys.stdin.readline

        n = int(sys.stdin.readline().strip())
        arr = list(map(int, sys.stdin.readline().split()))
        print(sum(arr))

    return output.getvalue().strip()

# provided sample
assert run("3\n1 2 3\n") == "6"

# single element
assert run("1\n5\n") == "5"

# all equal values
assert run("4\n2 2 2 2\n") == "8"

# large values
assert run("2\n1000000000 1000000000\n") == "2000000000"

# alternating values
assert run("5\n1 2 3 4 5\n") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 single value | 5 | Minimal input handling |
| 4 equal values | 8 | Repeated accumulation correctness |
| large pair | 2000000000 | Large integer correctness |
| 1..5 sequence | 15 | General summation behavior |

## Edge Cases

For N = 1, the algorithm reads a single value and immediately outputs it. For example, input `1 10` initializes total to 0, adds 10, and prints 10, matching the definition of the lantern burn time.

For maximum values like `1000` copies of `10^9`, the loop adds each value sequentially. The accumulator grows from 0 to 10^12 without any intermediate truncation in Python, producing the correct final result. In languages with fixed-width integers, this is where overflow would typically occur, but the logic itself remains correct.

If all values are identical, say `3 7 7 7`, the algorithm performs repeated addition of the same number. The structure of the loop does not assume uniqueness, so the final sum naturally becomes 21, matching the expected aggregate behavior.

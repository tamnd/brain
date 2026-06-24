---
title: "CF 105216F - Fair Prize"
description: "We are given a row of prize values, each prize having a positive integer value. John has a score limit $p$, and he is only allowed to pick prizes whose value does not exceed $p$. Among all valid prizes, he wants the one with the largest value."
date: "2026-06-24T17:05:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105216
codeforces_index: "F"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 105216
solve_time_s: 74
verified: false
draft: false
---

[CF 105216F - Fair Prize](https://codeforces.com/problemset/problem/105216/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of prize values, each prize having a positive integer value. John has a score limit $p$, and he is only allowed to pick prizes whose value does not exceed $p$. Among all valid prizes, he wants the one with the largest value.

In simpler terms, we scan through a list of integers and are only allowed to consider those that are at most a given threshold. The task is to find the maximum among those eligible integers.

The constraints are small: both the number of prizes $n$ and all values, including $p$, are at most 1000. This immediately tells us that even a straightforward linear scan over the array is more than fast enough. An $O(n)$ or even $O(n^2)$ approach would still run comfortably within limits, but anything beyond that is unnecessary complexity.

The structure of the input is also straightforward: one line gives the size and limit, and the second line gives the list of prize values.

A few edge cases matter even in such a simple problem. First, all values might be equal to $p$, meaning every item is valid and the answer is simply that value. Second, the maximum valid value might appear at the end of the list, so any early stopping strategy that assumes sorted order would fail if applied blindly. Third, values smaller than $p$ may appear everywhere, and we must ensure we do not accidentally pick the first valid element rather than the maximum valid one.

## Approaches

The brute-force idea is almost identical to the final solution. We scan through every prize and keep track of the best value we are allowed to take. For each element, if it is less than or equal to $p$, we compare it with our current best answer and update if it is larger.

This works because every valid candidate must be inspected at least once, and there is no ordering guarantee that lets us skip elements. The operation count is exactly $n$ comparisons against the threshold and up to $n$ updates of a maximum variable, so overall $O(n)$.

There is no meaningful optimization beyond this. Sorting would cost $O(n \log n)$ without improving the logic. Data structures like heaps or segment trees are unnecessary overhead for a single query over a static array. The key observation is that the problem is purely a constrained maximum over a static list.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | $O(n)$ | $O(1)$ | Accepted |
| Sorting then filtering | $O(n \log n)$ | $O(1)$ or $O(n)$ | Accepted but unnecessary |
| Optimal Scan | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process the array once while maintaining a single variable that stores the best valid prize seen so far.

1. Initialize a variable `best` with a value guaranteed to be smaller than any valid answer, such as 0. This works because all prize values are at least 1, so 0 cannot accidentally be the answer.
2. Iterate through each prize value $v_i$ in the array from left to right.
3. For each value, check whether it satisfies $v_i \le p$. This condition ensures we only consider prizes John is allowed to take.
4. If the value is valid, compare it with `best`. If $v_i > best$, update `best` to $v_i$. This step ensures we always retain the maximum valid value seen so far.
5. After processing all values, output `best` as the final answer.

The reason this procedure works is that every feasible candidate is examined exactly once, and the algorithm maintains the invariant that after processing the first $k$ elements, `best` stores the maximum value among all valid elements in that prefix. Since the final answer depends only on global maximum among valid values, extending this invariant to the full array guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, p = map(int, input().split())
    arr = list(map(int, input().split()))
    
    best = 0
    for v in arr:
        if v <= p and v > best:
            best = v
    
    print(best)

if __name__ == "__main__":
    solve()
```

The solution begins by reading the size of the list and the threshold. It then parses all prize values into an array.

The variable `best` is initialized to 0 because all values are positive, so this is a safe identity element for maximum tracking under the constraint $v_i \le p$.

The loop performs both checks in a single pass: first verifying feasibility with respect to $p$, then updating the maximum. This ordering prevents incorrect updates from invalid values.

Finally, the computed maximum is printed directly.

## Worked Examples

### Sample 1

Input:

```
5 10
4 2 4 3 9
```

We track `best`:

| Step | Value | Valid (≤ p) | best before | best after |
| --- | --- | --- | --- | --- |
| 1 | 4 | yes | 0 | 4 |
| 2 | 2 | yes | 4 | 4 |
| 3 | 4 | yes | 4 | 4 |
| 4 | 3 | yes | 4 | 4 |
| 5 | 9 | yes | 4 | 9 |

Final answer is 9.

This demonstrates that the algorithm does not stop early and correctly finds a later maximum.

### Sample 2

Input:

```
1 10
10
```

| Step | Value | Valid (≤ p) | best before | best after |
| --- | --- | --- | --- | --- |
| 1 | 10 | yes | 0 | 10 |

Final answer is 10.

This confirms correct handling of the minimal array size where only one candidate exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | each prize is processed exactly once |
| Space | $O(1)$ | only a single variable is used regardless of input size |

The input size is at most 1000 elements, so a linear scan is trivially within limits. Even with multiple test cases (which this problem does not include), the same linear strategy would remain efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue().strip() if False else None
```

Since we cannot rely on re-importing in this environment, below are conceptual assert-style tests consistent with the solution logic:

```python
import sys, io

def run_solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    def solve():
        n, p = map(int, input().split())
        arr = list(map(int, input().split()))
        best = 0
        for v in arr:
            if v <= p and v > best:
                best = v
        output.append(str(best))
    
    solve()
    return output[0]

# provided samples
assert run_solution("5 10\n4 2 4 3 9\n") == "9"
assert run_solution("1 10\n10\n") == "10"

# custom cases
assert run_solution("3 5\n1 2 3\n") == "3"
assert run_solution("4 2\n5 6 1 2\n") == "2"
assert run_solution("5 100\n10 20 30 40 50\n") == "50"
assert run_solution("6 3\n4 4 4 4 4 4\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed small values | max ≤ p | standard filtering |
| all invalid except one | correct selection | boundary filtering |
| all valid increasing | global max selection | correctness of max tracking |
| all invalid | 0 | handling no valid candidates |

## Edge Cases

One edge case is when all elements are greater than $p$. For example, if $p = 2$ and array is $[5, 6, 7]$, no value is eligible. The algorithm initializes `best` to 0 and never updates it, producing 0. Since the problem guarantees at least one valid selection exists, this case will not appear in official input, but the implementation still handles it safely.

Another edge case is when the maximum valid value appears at the first position. For input $p = 10$, array $[9, 1, 8]$, the algorithm correctly sets `best` to 9 immediately and does not get affected by later smaller values.

A final edge case is when the maximum valid value appears at the end. For input $p = 10$, array $[1, 2, 10]$, the algorithm updates progressively and correctly captures the last element as the best. This confirms that no ordering assumptions are required for correctness.

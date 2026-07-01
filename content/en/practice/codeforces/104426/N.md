---
title: "CF 104426N - Ichthyophobia"
description: "We are given a sequence of independent observations, each representing a lake and the number of fish in it. For every lake, we must decide whether Kaitokid can safely visit it. Safety is defined in a very strict way: a lake is acceptable only when it contains no fish at all."
date: "2026-06-30T19:09:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104426
codeforces_index: "N"
codeforces_contest_name: "Syrian Private Universities Collegiate Programming Contest 2023"
rating: 0
weight: 104426
solve_time_s: 89
verified: false
draft: false
---

[CF 104426N - Ichthyophobia](https://codeforces.com/problemset/problem/104426/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of independent observations, each representing a lake and the number of fish in it. For every lake, we must decide whether Kaitokid can safely visit it. Safety is defined in a very strict way: a lake is acceptable only when it contains no fish at all. Any positive number of fish makes the lake unsuitable.

The input consists of a single integer T describing how many lakes are reported. After that, we read T integers, each one bounded between 0 and 100 inclusive. For each of these values, we output a decision string indicating whether that specific lake is safe.

The constraints are small enough that the total amount of computation is negligible. Even at the maximum T of 10^4, we are only performing a constant-time check per lake. This means a direct linear scan is sufficient, and any solution with O(T) complexity will comfortably run within limits.

There are no hidden structural complications such as ordering dependencies or cross-lake interactions. Each lake can be processed independently, which is the key simplification.

The only edge case that matters is when the number of fish is exactly zero. A careless implementation might accidentally treat zero as falsy or skip it incorrectly depending on language constructs, but logically it is the only case that should produce a positive response.

## Approaches

A brute-force interpretation would still look at each lake one by one, check whether its fish count is zero, and print the result. There is no way to reduce the number of checks because every lake must be inspected at least once to produce its corresponding output. Even if we tried to store all values first and process them later, the total work remains proportional to T.

The only real "optimization" here is recognizing that no additional data structures or preprocessing are required. The decision rule is a single comparison per element: if x equals zero, print YES, otherwise print NO. The structure of the problem already matches the optimal evaluation pattern.

The brute-force view and the optimal view coincide, but the important realization is that no aggregation, sorting, or prefix computation changes anything. The computation is inherently O(T).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct per-lake check | O(T) | O(1) | Accepted |
| Any alternative transformation | O(T) | O(T) | Accepted but unnecessary |

## Algorithm Walkthrough

We process each lake independently in the order they are given.

1. Read the integer T, which tells us how many lakes we must evaluate. This defines the number of iterations we will perform.
2. For each of the next T integers, read the value x representing fish count in a single lake.
3. Check whether x is equal to zero. This is the defining condition of safety, since only empty lakes are acceptable.
4. If x equals zero, output YES immediately. Otherwise, output NO.
5. Repeat this process until all T lakes have been processed.

The reasoning behind each step is that no lake influences any other lake, so immediate evaluation is both safe and optimal.

### Why it works

The correctness relies on a direct equivalence between the problem definition and the condition x == 0. The algorithm evaluates this predicate exactly once per input value and produces the corresponding label. Since each decision is independent and fully determined by a single integer, there is no possibility of inconsistency or interaction effects across iterations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input().strip())
    for _ in range(t):
        x_line = input().strip()
        if not x_line:
            x_line = input().strip()
        x = int(x_line)
        if x == 0:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The implementation reads T first and then processes each lake in a loop. Each input line is parsed into an integer and checked against zero. The conditional is the core of the solution and directly mirrors the mathematical definition of a valid lake.

The only subtle implementation detail is ensuring that each input line is properly stripped before conversion, which avoids issues with trailing whitespace or empty reads in some environments. The output is printed immediately, which avoids storing results unnecessarily.

## Worked Examples

### Example 1

Input:

```
3
1
5
0
```

We track each lake sequentially.

| Step | x | Condition (x == 0) | Output |
| --- | --- | --- | --- |
| 1 | 1 | False | NO |
| 2 | 5 | False | NO |
| 3 | 0 | True | YES |

The trace shows that only the zero case triggers acceptance, while all positive values are rejected consistently.

### Example 2

Input:

```
4
0
0
2
1
```

| Step | x | Condition (x == 0) | Output |
| --- | --- | --- | --- |
| 1 | 0 | True | YES |
| 2 | 0 | True | YES |
| 3 | 2 | False | NO |
| 4 | 1 | False | NO |

This confirms that multiple valid lakes are handled independently without any state carryover.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each lake is checked exactly once with a constant-time comparison |
| Space | O(1) | No auxiliary storage is required beyond input parsing |

The runtime scales linearly with the number of lakes, which is optimal because every input value must be read at least once. The memory usage remains constant since we do not store the entire array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided sample
assert run("3\n1\n5\n0\n") == "NO\nNO\nYES"

# minimum case
assert run("1\n0\n") == "YES"

# all non-zero
assert run("3\n1\n2\n3\n") == "NO\nNO\nNO"

# alternating values
assert run("4\n0\n1\n0\n1\n") == "YES\nNO\nYES\nNO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 0 | YES | Minimum valid case |
| 1, 1 | NO | Minimum rejection case |
| 1 2 3 | NO NO NO | All non-zero handling |
| 0 1 0 1 | YES NO YES NO | Alternating correctness |

## Edge Cases

A key edge case is when the fish count is exactly zero. The algorithm treats this explicitly as the only accepting condition. For input `0`, the condition x == 0 evaluates to true and the output is YES, confirming correct handling of the boundary between acceptable and unacceptable lakes.

Another edge case is when all values are non-zero. For example, input `3 1 2 3` produces NO for every step because none of the values satisfy the acceptance condition. The algorithm does not rely on positivity or negativity, only exact equality, so there is no ambiguity.

Finally, the smallest possible input with T = 1 is handled correctly because the loop executes exactly once and produces a single decision without requiring any initialization or accumulation logic.

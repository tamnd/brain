---
title: "CF 130C - Decimal sum"
description: "We are given a sequence of integers and need to compute their total sum. The input starts with an integer n, which tells us how many numbers follow. Each of the next n lines contains one element of the array. The task is simply to add all of them together and print the result."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 130
codeforces_index: "C"
codeforces_contest_name: "Unknown Language Round 4"
rating: 1500
weight: 130
solve_time_s: 108
verified: true
draft: false
---

[CF 130C - Decimal sum](https://codeforces.com/problemset/problem/130/C)

**Rating:** 1500  
**Tags:** *special  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and need to compute their total sum. The input starts with an integer `n`, which tells us how many numbers follow. Each of the next `n` lines contains one element of the array. The task is simply to add all of them together and print the result.

The constraints are extremely small. The array contains at most 100 numbers, and every number is between 1 and 100. Even the simplest possible algorithm easily fits within the limits. A linear scan over the array performs only 100 additions in the worst case, which is effectively instantaneous.

Although the task is straightforward, there are still a few places where careless implementations can fail.

One common mistake is forgetting to convert input strings into integers before adding them. For example:

```
3
1
2
3
```

The correct output is:

```
6
```

If someone accidentally concatenates strings instead of summing integers, they could produce `"123"` instead.

Another mistake is reading only one line after `n` instead of reading all `n` elements. Consider:

```
5
1
2
3
4
5
```

The correct answer is:

```
15
```

A buggy implementation that reads only the first number would incorrectly output `1`.

There is also the minimum-size case:

```
1
42
```

The answer must still be computed correctly:

```
42
```

Algorithms that assume at least two elements may fail here.

## Approaches

The most direct solution is brute force: read every number one by one and keep a running total. After processing all `n` numbers, print the accumulated sum.

This works because the definition of the problem itself is additive. Every element contributes independently to the final result, so we never need to revisit earlier values or store complicated state. The algorithm performs exactly `n` additions. With `n ≤ 100`, the worst case is only 100 operations.

There is no need for a more sophisticated optimization. The brute-force approach is already optimal because every input number must be examined at least once. Any correct algorithm has a lower bound of `O(n)` time since skipping an element could miss part of the sum.

The key observation is that the problem has no hidden structure. There are no queries, updates, or ordering constraints. A single linear pass is both the simplest and the fastest possible solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, the number of elements in the array.
2. Initialize a variable `total = 0`. This variable stores the running sum of all numbers processed so far.
3. Repeat `n` times:

1. Read the next integer.
2. Add it to `total`.
4. After all numbers are processed, print `total`.

Why it works:

At every step, `total` equals the sum of all elements read so far. Initially, no elements have been processed, so the correct sum is `0`. Each iteration adds exactly one new array element to the running sum, preserving the invariant. After the final iteration, every array element has been included exactly once, so `total` equals the complete array sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

total = 0

for _ in range(n):
    total += int(input())

print(total)
```

The program starts by reading `n`, which determines how many integers follow. The variable `total` stores the cumulative sum.

The loop runs exactly `n` times. During each iteration, one integer is read and immediately added to `total`. Since the constraints are tiny, no special optimization is needed beyond standard fast input handling.

One subtle detail is converting the input to integers using `int(input())`. Input arrives as strings, and failing to convert would produce incorrect behavior.

The implementation also avoids storing the entire array. Since each value is used exactly once, processing numbers as they are read keeps the memory usage constant.

## Worked Examples

### Example 1

Input:

```
5
1
2
3
4
5
```

| Step | Current Number | total Before | total After |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 |
| 2 | 2 | 1 | 3 |
| 3 | 3 | 3 | 6 |
| 4 | 4 | 6 | 10 |
| 5 | 5 | 10 | 15 |

Final output:

```
15
```

This trace shows the invariant clearly. After every iteration, `total` matches the sum of all previously processed elements.

### Example 2

Input:

```
1
42
```

| Step | Current Number | total Before | total After |
| --- | --- | --- | --- |
| 1 | 42 | 0 | 42 |

Final output:

```
42
```

This example exercises the minimum-size boundary case. The algorithm still works because the loop naturally handles a single iteration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is read and added once |
| Space | O(1) | Only the running sum is stored |

With at most 100 numbers, the program performs at most 100 additions. Both the runtime and memory usage are far below the problem limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    total = 0

    for _ in range(n):
        total += int(input())

    print(total)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided samples
assert run("5\n1\n2\n3\n4\n5\n") == "15\n", "sample 1"

# minimum-size input
assert run("1\n42\n") == "42\n", "single element"

# all equal values
assert run("4\n7\n7\n7\n7\n") == "28\n", "all equal"

# boundary values
assert run("3\n100\n100\n100\n") == "300\n", "maximum element values"

# off-by-one style case
assert run("2\n1\n100\n") == "101\n", "reads exactly n elements"

# larger case
assert run("5\n10\n20\n30\n40\n50\n") == "150\n", "general accumulation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 42` | `42` | Minimum-size array |
| `4 7 7 7 7` | `28` | Repeated identical values |
| `3 100 100 100` | `300` | Maximum allowed element values |
| `2 1 100` | `101` | Correct handling of exactly `n` inputs |
| `5 10 20 30 40 50` | `150` | General accumulation logic |

## Edge Cases

Consider the smallest possible input:

```
1
42
```

The algorithm initializes `total = 0`, then processes exactly one number.

After reading `42`, the running sum becomes:

```
total = 0 + 42 = 42
```

The final printed answer is:

```
42
```

This confirms the loop handles a single iteration correctly.

Now consider repeated values:

```
4
7
7
7
7
```

The execution proceeds as follows:

```
0 -> 7 -> 14 -> 21 -> 28
```

Each occurrence is added independently, so duplicates cause no issues.

Finally, consider maximum element values:

```
3
100
100
100
```

The running sum evolves like this:

```
0 -> 100 -> 200 -> 300
```

Python integers easily handle these values, so there is no overflow risk. The algorithm correctly outputs:

```
300
```

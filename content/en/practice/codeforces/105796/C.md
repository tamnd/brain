---
title: "CF 105796C - Algoritmo de Euclides"
description: "The task is to count how many iterations are executed by a slow version of the Euclidean algorithm. The algorithm starts with two positive integers. While the two values are different, it repeatedly subtracts the smaller value from the larger value and increments a counter."
date: "2026-06-25T15:37:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105796
codeforces_index: "C"
codeforces_contest_name: "UNICAMP Selection Contest 2024"
rating: 0
weight: 105796
solve_time_s: 39
verified: true
draft: false
---

[CF 105796C - Algoritmo de Euclides](https://codeforces.com/problemset/problem/105796/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to count how many iterations are executed by a slow version of the Euclidean algorithm. The algorithm starts with two positive integers. While the two values are different, it repeatedly subtracts the smaller value from the larger value and increments a counter. The answer is the final value of this counter, not the greatest common divisor itself.

For example, starting with `15 10`, the process is `15 10 -> 5 10 -> 5 5`, so the answer is `2`. The challenge is that the input values can be extremely large, so simulating every subtraction is impossible.

The input contains up to 500 pairs of positive integers, and each integer can be as large as `10^18`. A direct simulation can require up to almost `10^18` operations. A pair such as `1 1000000000000000` would subtract `1` from the larger number nearly one quadrillion times, which cannot fit into any practical time limit. The solution must instead process whole groups of identical subtraction steps.

The tricky cases come from the exact stopping condition and from very large quotients. If both numbers are already equal, no subtraction happens.

```
Input
7 7
```

The correct output is:

```
0
```

A careless implementation that always performs at least one subtraction would produce an incorrect result.

Another edge case is when one number divides the other.

```
Input
1 1000000000000000
```

The correct output is:

```
999999999999999
```

The final subtraction is special because after repeatedly subtracting `1`, the numbers become equal. Counting `1000000000000000` subtractions would be one too many.

A third case is when the first division leaves a remainder.

```
Input
15 10
```

The correct output is:

```
2
```

The first subtraction changes the pair to `5 10`, and the second changes it to `5 5`. Treating the operation count as only the quotient `15 // 10` would miss the later Euclidean step.

## Approaches

The straightforward approach is to implement the given algorithm exactly. While the two numbers differ, subtract the smaller from the larger and increment the answer. This is correct because every loop iteration matches one subtraction in the original process.

The problem is the number of iterations. If the values are `1` and `10^18`, the loop performs `999999999999999` operations. Even a single such test case is too large, and there can be hundreds of test cases.

The key observation is that many consecutive loop iterations do the same thing. When the larger number is much bigger than the smaller one, the algorithm repeatedly subtracts the same value. Instead of performing these subtractions individually, we can count how many happen in one group.

Suppose the current values are `a > b`. Write:

```
a = q * b + r
```

If `r` is not zero, the slow algorithm subtracts `b` exactly `q` times before the larger value becomes `r`. The state changes from `(a, b)` to `(b, r)`.

If `r` is zero, after `q - 1` subtractions the values become equal. The `q`-th subtraction is not performed because the loop stops as soon as equality is reached. The state becomes `(b, b)` and contributes `q - 1` operations.

This is the same compression idea behind the Euclidean algorithm, but instead of only finding the gcd, we keep track of the number of subtraction steps that the slower version would have executed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow |
| Optimal | O(log(max(a, b))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read a pair of numbers and initialize the answer counter to zero.
2. If the two numbers are already equal, return zero because the original loop condition is false immediately.
3. While the numbers are different, make the larger number `a` and the smaller number `b`.
4. Compute `a // b` and `a % b`. The quotient tells how many times the slow algorithm would subtract `b` from `a` before the value drops below `b` or becomes equal.
5. Add `a // b` to the answer when there is a remainder. If there is no remainder, add one less than the quotient because the final subtraction would make the numbers equal and terminate the loop.
6. Replace the pair with the next Euclidean state `(b, a % b)` and continue until both values are equal.

The reason this works is that each compressed step represents a consecutive sequence of identical subtractions. The only adjustment needed is when the larger number is an exact multiple of the smaller one, because the original algorithm stops one subtraction earlier than a normal division process.

### Why it works

At every point, the slow algorithm only changes the larger number by subtracting the smaller one. Grouping those identical operations together does not change the intermediate value after the group finishes.

For `a > b`, the quotient `a // b` is exactly the maximum number of times `b` can be subtracted before the value is less than `b` or reaches zero. If there is a remainder, all those subtractions happen before the next pair `(b, remainder)` appears. If there is no remainder, the last subtraction would create equality, so it is excluded. Repeating this transformation follows the same states as the original algorithm, only skipping the individual operations inside each group.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_operations(a, b):
    ans = 0

    while a != b:
        if a < b:
            a, b = b, a

        q, r = divmod(a, b)

        if r == 0:
            ans += q - 1
            break
        else:
            ans += q
            a, b = b, r

    return ans

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        a, b = map(int, input().split())
        out.append(str(count_operations(a, b)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The function `count_operations` keeps the current pair of values and the number of compressed subtraction steps. The swap makes `a` the larger value before applying division, matching the condition in the original loop.

The `divmod` call computes both the quotient and remainder at once. This avoids manually calculating them and directly exposes the number of repeated subtractions.

The `r == 0` branch handles the boundary condition where the two numbers become equal. Adding `q` here would overcount by one because the original loop does not execute the subtraction that creates equality.

Python integers can store values larger than `10^18`, so there is no overflow risk. The loop only follows Euclidean reductions, so the number of iterations remains small.

## Worked Examples

### Example 1

Input:

```
15 10
```

| Step | a | b | Quotient | Remainder | Added operations | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Start | 15 | 10 | 1 | 5 | 1 | 1 |
| Continue | 10 | 5 | 2 | 0 | 1 | 2 |
| End | 5 | 5 | - | - | - | 2 |

The first compressed step represents the subtraction `15 - 10 = 5`. The second step has an exact division, so only one subtraction is counted because the next subtraction would make the numbers equal.

### Example 2

Input:

```
1 1000000000000000
```

| Step | a | b | Quotient | Remainder | Added operations | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Start | 1000000000000000 | 1 | 1000000000000000 | 0 | 999999999999999 | 999999999999999 |
| End | 1 | 1 | - | - | - | 999999999999999 |

This trace shows why simulating the process is impossible. The entire sequence of almost one quadrillion identical subtractions is represented by one division operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(max(a, b))) | Each iteration follows the same remainder reduction pattern as Euclid's algorithm. |
| Space | O(1) | Only a few integer variables are stored. |

The maximum value is `10^18`, so the number of Euclidean reductions is small. With at most 500 test cases, this easily fits within the limits.

## Test Cases

```python
import sys
import io

def count_operations(a, b):
    ans = 0
    while a != b:
        if a < b:
            a, b = b, a
        q, r = divmod(a, b)
        if r == 0:
            ans += q - 1
            break
        ans += q
        a, b = b, r
    return ans

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    t = int(sys.stdin.readline())
    ans = []
    for _ in range(t):
        a, b = map(int, sys.stdin.readline().split())
        ans.append(str(count_operations(a, b)))
    sys.stdin = old_stdin
    return "\n".join(ans)

assert run("""4
1 1
15 10
1 1000000000000000
1234500 54321001234500
""") == """0
2
999999999999999
44002456""", "provided samples"

assert run("""1
1 2
""") == "1", "minimum values"

assert run("""1
1000000000000000000 1
""") == "999999999999999999", "maximum quotient"

assert run("""1
42 42
""") == "0", "equal values"

assert run("""1
100 25
""") == "3", "exact division boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | The loop performs no operations when values start equal. |
| `1 2` | `1` | The smallest non-equal pair is handled correctly. |
| `1000000000000000000 1` | `999999999999999999` | Very large counts are compressed instead of simulated. |
| `42 42` | `0` | Equality termination condition. |
| `100 25` | `3` | Exact division requires subtracting one less than the quotient. |

## Edge Cases

For equal values, such as:

```
Input
7 7
```

the algorithm enters the loop condition check and immediately returns zero. No quotient is computed because no subtraction exists in the original process.

For a huge multiple, such as:

```
Input
1 1000000000000000
```

the algorithm swaps the values so the larger value is divided by `1`. The quotient is `1000000000000000` and the remainder is zero. It adds `999999999999999`, matching the number of times the subtraction loop runs before reaching `(1, 1)`.

For a pair with a remainder:

```
Input
15 10
```

the quotient is `1` and the remainder is `5`, so one operation is counted and the pair becomes `(10, 5)`. The next step detects exact division with quotient `2`, adds only `1`, and finishes at `(5, 5)`. The total is `2`, exactly matching the original subtraction process.

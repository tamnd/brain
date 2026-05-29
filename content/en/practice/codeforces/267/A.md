---
title: "CF 267A - Subtractions"
description: "We repeatedly apply the same operation to two positive integers. At every step, we subtract the smaller value from the larger one. The process stops as soon as one number becomes zero. The task is to count how many subtraction operations are performed for each pair."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 267
codeforces_index: "A"
codeforces_contest_name: "Codeforces Testing Round 5"
rating: 900
weight: 267
solve_time_s: 161
verified: true
draft: false
---

[CF 267A - Subtractions](https://codeforces.com/problemset/problem/267/A)

**Rating:** 900  
**Tags:** math, number theory  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We repeatedly apply the same operation to two positive integers. At every step, we subtract the smaller value from the larger one. The process stops as soon as one number becomes zero. The task is to count how many subtraction operations are performed for each pair.

For example, starting from `(4, 17)`:

`(4,17) → (4,13) → (4,9) → (4,5) → (4,1) → (3,1) → (2,1) → (1,1) → (0,1)`

This sequence contains `8` operations.

The input contains up to `1000` independent pairs, and each value can be as large as `10^9`. A direct simulation that performs one subtraction per operation can become extremely slow. Consider `(1, 10^9)`. The process performs almost one billion operations because the larger number decreases by only `1` each time. Any algorithm that literally simulates every subtraction will exceed the time limit.

The structure of the process strongly resembles the Euclidean algorithm for greatest common divisor. Instead of subtracting one time per iteration, we can count how many subtractions happen at once using integer division.

There are a few easy-to-miss corner cases.

When the numbers are equal, one operation immediately turns one value into zero. For example:

```
5 5
```

The answer is `1`, not `5`. A careless implementation that repeatedly subtracts until the larger becomes smaller could accidentally overcount.

Pairs where one number is much larger than the other are another trap. For example:

```
1 1000000000
```

The correct answer is `1000000000`. A naive loop would take one billion iterations.

Another subtle case appears when the larger number is an exact multiple of the smaller one:

```
3 12
```

The sequence is:

`(3,12) → (3,9) → (3,6) → (3,3) → (0,3)`

The answer is `4`. Using only the remainder operation without counting how many subtractions happened would lose information.

## Approaches

The most direct solution is to simulate the process exactly as described. At each step, compare the two numbers and subtract the smaller one from the larger one. Increment the answer after every subtraction.

This works because the rules are deterministic. Every operation reduces the sum of the two numbers, so the process eventually terminates.

The problem is performance. In the worst case, such as `(1, 10^9)`, the algorithm performs one billion iterations. That is far beyond what fits inside a one second time limit.

The key observation is that repeated subtraction is equivalent to division.

Suppose we have `(a, b)` with `a < b`. Repeatedly subtracting `a` from `b` continues until `b < a`. The number of performed subtractions is exactly `b // a`, and the remaining value becomes `b % a`.

For example:

`(4,17)`

Subtracting `4` repeatedly:

`17 → 13 → 9 → 5 → 1`

This took `17 // 4 = 4` operations, and the new value is `17 % 4 = 1`.

So instead of performing four separate operations, we can jump directly to the result in one step.

This transforms the process into the Euclidean algorithm. Each iteration reduces one number to a remainder, and the total number of subtractions accumulates through integer division.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow |
| Optimal | O(log(max(a,b))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each pair `(a, b)`, initialize `ans = 0`.
3. While both numbers are positive, do the following:

If `a < b`, then `b` can subtract `a` exactly `b // a` times before becoming smaller than `a`.

Add `b // a` to the answer and replace `b` with `b % a`.
4. Otherwise, if `a >= b`, then `a` can subtract `b` exactly `a // b` times before becoming smaller than `b`.

Add `a // b` to the answer and replace `a` with `a % b`.
5. Continue until one number becomes zero.
6. Print the accumulated answer.

### Why it works

At every stage, the process performs the maximum possible number of identical subtractions in one jump.

If `b > a`, repeatedly subtracting `a` from `b` is mathematically identical to:

```
b = b - a * (b // a)
```

The remaining value is exactly `b % a`, and the number of performed operations is `b // a`.

The algorithm preserves the exact sequence count while skipping unnecessary intermediate states. Since each iteration replaces one value with a strictly smaller remainder, the numbers decrease rapidly, exactly like the Euclidean algorithm.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    a, b = map(int, input().split())
    
    ans = 0
    
    while a > 0 and b > 0:
        if a < b:
            ans += b // a
            b %= a
        else:
            ans += a // b
            a %= b
    
    print(ans)
```

The solution follows the Euclidean algorithm structure closely.

The loop continues while both numbers remain positive. Once one value becomes zero, no further subtraction is possible, so the process ends naturally.

The most important detail is adding the quotient before taking the remainder. The quotient represents how many individual subtraction operations are skipped. Forgetting this step would compute only the final gcd process, not the total operation count.

Using modulo is safe because repeated subtraction and modulo produce the same remainder. The modulo version simply compresses many operations into one arithmetic step.

Python integers handle values up to `10^9` easily, so there are no overflow concerns.

## Worked Examples

### Example 1

Input:

```
4 17
```

| a | b | quotient added | total operations |
| --- | --- | --- | --- |
| 4 | 17 | 17 // 4 = 4 | 4 |
| 4 | 1 | 4 // 1 = 4 | 8 |
| 0 | 1 | stop | 8 |

The first iteration compresses four subtractions at once. The second iteration compresses the remaining four single-step reductions. The final answer matches the full manual simulation.

### Example 2

Input:

```
7 987654321
```

| a | b | quotient added | total operations |
| --- | --- | --- | --- |
| 7 | 987654321 | 141093474 | 141093474 |
| 7 | 3 | 2 | 141093476 |
| 1 | 3 | 3 | 141093479 |
| 1 | 0 | stop | 141093479 |

This example shows why the optimized method is necessary. The first iteration alone skips more than one hundred million individual subtractions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(max(a,b))) | Each iteration behaves like the Euclidean algorithm and rapidly reduces the numbers |
| Space | O(1) | Only a few integer variables are stored |

The constraints allow values up to `10^9`, but the Euclidean algorithm finishes in very few iterations, usually under a few dozen steps per test case. This easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    
    out = []
    
    for _ in range(t):
        a, b = map(int, input().split())
        
        ans = 0
        
        while a > 0 and b > 0:
            if a < b:
                ans += b // a
                b %= a
            else:
                ans += a // b
                a %= b
        
        out.append(str(ans))
    
    print("\n".join(out))

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
assert run("2\n4 17\n7 987654321\n") == "8\n141093479\n", "sample 1"

# minimum values
assert run("1\n1 1\n") == "1\n", "minimum case"

# exact multiple
assert run("1\n3 12\n") == "4\n", "exact multiple"

# consecutive numbers
assert run("1\n8 5\n") == "5\n", "fibonacci-like behavior"

# large imbalance
assert run("1\n1 1000000000\n") == "1000000000\n", "large quotient"

# equal large numbers
assert run("1\n1000000000 1000000000\n") == "1\n", "equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Immediate termination after one subtraction |
| `3 12` | `4` | Exact multiple handling |
| `8 5` | `5` | Multiple Euclidean reductions |
| `1 1000000000` | `1000000000` | Large quotient compression |
| `1000000000 1000000000` | `1` | Equal-value boundary case |

## Edge Cases

Consider equal numbers:

```
5 5
```

Execution trace:

| a | b | operations added | total |
| --- | --- | --- | --- |
| 5 | 5 | 1 | 1 |
| 0 | 5 | stop | 1 |

The algorithm correctly counts a single subtraction because `5 // 5 = 1`.

Now consider a huge imbalance:

```
1 1000000000
```

Execution trace:

| a | b | operations added | total |
| --- | --- | --- | --- |
| 1 | 1000000000 | 1000000000 | 1000000000 |
| 1 | 0 | stop | 1000000000 |

The optimized method finishes in one iteration instead of one billion iterations.

Finally, consider an exact multiple:

```
3 12
```

Execution trace:

| a | b | operations added | total |
| --- | --- | --- | --- |
| 3 | 12 | 4 | 4 |
| 3 | 0 | stop | 4 |

The quotient captures all repeated subtractions correctly. A careless implementation using only modulo without adding the quotient would incorrectly return zero operations here.

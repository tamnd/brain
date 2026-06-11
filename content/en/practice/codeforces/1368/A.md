---
title: "CF 1368A - C+="
description: "We start with two positive integers, a and b. In one operation we may add one variable into the other: a += b or b += a. Only one value changes per operation. Our goal is to make at least one of the two numbers become strictly larger than a given limit n."
date: "2026-06-11T11:45:09+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1368
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 8"
rating: 800
weight: 1368
solve_time_s: 110
verified: true
draft: false
---

[CF 1368A - C+=](https://codeforces.com/problemset/problem/1368/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation, math  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with two positive integers, `a` and `b`. In one operation we may add one variable into the other:

`a += b` or `b += a`.

Only one value changes per operation. Our goal is to make at least one of the two numbers become strictly larger than a given limit `n`. For each test case, we must find the minimum number of operations required.

The constraints are small in terms of test count, at most 100 cases, but the values themselves can be as large as `10^9`. That immediately suggests we should not simulate every possible sequence of choices with search or dynamic programming. Even a branching factor of two per move would explode. We need a direct strategy.

A useful observation is that the numbers grow very quickly. If we always add the larger value into the smaller one, the sequence behaves similarly to Fibonacci growth. Starting from values up to `10^9`, the number of operations needed before exceeding `n` is only a few dozen. This means a simple simulation is already fast enough if we always make the correct greedy choice.

There are a few edge cases worth checking carefully.

Suppose `a = 1`, `b = 1`, `n = 1`. The answer is `1`, not `0`, because the target is to become _strictly greater_ than `n`. Initially both values equal `n`, so one operation is still required.

Suppose `a = 1`, `b = 2`, `n = 3`. After one operation we can reach `(3,2)` or `(1,3)`, but neither value exceeds `3`. A second operation is necessary. The correct answer is `2`. A careless implementation that stops when a value becomes equal to `n` would produce the wrong result.

Suppose `a = 5`, `b = 4`, `n = 100`. Choosing updates poorly can increase the operation count. For example, repeatedly adding the smaller value into the larger one grows more slowly than the optimal strategy. The minimum answer requires making the largest possible increase every step.

## Approaches

A brute-force perspective is to think of every operation as a binary choice. From a state `(a, b)` we may move to `(a + b, b)` or `(a, a + b)`. Since we want the minimum number of operations, we could imagine a breadth-first search over all reachable states.

This approach is correct because BFS explores states in increasing operation count. The problem is the number of states. Even after a modest number of steps, the branching factor of two creates exponentially many possibilities. Such a search is completely impractical.

The key observation is that at any moment, if we want to exceed `n` as quickly as possible, we should always add the larger number into the smaller one.

Assume `a ≤ b`.

If we perform `a += b`, the new value becomes `a + b`.

If instead we perform `b += a`, the new value becomes `b + a`, but the smaller value stays unchanged.

The first choice transforms `(a, b)` into `(a + b, b)`, while the second transforms it into `(a, a + b)`.

The larger number after either operation is the same, namely `a + b`. The difference is that the first choice also increases the smaller value. A larger smaller-value can only help future operations, because every future addition uses both numbers. Keeping the smaller value as large as possible never hurts and often helps.

This leads to a simple greedy process:

Keep adding the larger number to the smaller number until one of them exceeds `n`.

Because the values grow like Fibonacci numbers, the number of iterations is tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy Simulation | O(k) | O(1) | Accepted |

Here `k` is the number of performed operations, which is at most around 50 for the given constraints.

## Algorithm Walkthrough

1. Initialize the operation counter to zero.
2. While both `a` and `b` are at most `n`, continue performing operations.
3. Compare the two values.
4. If `a < b`, perform `a += b`.
5. Otherwise perform `b += a`.

This always increases the smaller value, producing the largest possible pair for future growth.
6. Increment the operation counter.
7. When either value becomes greater than `n`, stop and output the counter.

### Why it works

At every step, let `x` be the smaller value and `y` be the larger value.

The two possible next states are `(x + y, y)` and `(x, x + y)`.

Both create the same new maximum value, `x + y`. The difference is the remaining value. Keeping it as `y` is always at least as good as keeping it as `x`, because `y ≥ x`.

So after one operation, updating the smaller value produces a state whose two numbers are both at least as large as the corresponding numbers in the alternative state. Since future operations only involve additions of these values, starting from a component-wise larger state cannot require more operations to exceed `n`.

Thus there always exists an optimal solution that updates the smaller value at every step, which is exactly what the algorithm does.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        a, b, n = map(int, input().split())
        
        ops = 0
        
        while max(a, b) <= n:
            if a < b:
                a += b
            else:
                b += a
            ops += 1
        
        print(ops)

solve()
```

The loop continues while both numbers are not yet large enough. Using `max(a, b) <= n` is equivalent to saying neither value exceeds `n`.

The greedy step always updates the smaller value. This is the central idea of the solution. After each update we increase the operation counter.

Python integers have arbitrary precision, so there is no overflow concern even though values can temporarily become larger than `10^9`.

A common mistake is stopping when a value becomes equal to `n`. The problem requires a value to be _strictly greater_ than `n`, so the condition must be `<= n` inside the loop.

## Worked Examples

### Example 1

Input:

```
a = 1, b = 2, n = 3
```

| Operation | a | b | Action |
| --- | --- | --- | --- |
| Start | 1 | 2 | Initial state |
| 1 | 3 | 2 | a += b |
| 2 | 3 | 5 | b += a |

After the second operation, `5 > 3`, so the answer is `2`.

This example shows why reaching exactly `n` is not enough. After the first move we have `a = 3`, but another operation is still required.

### Example 2

Input:

```
a = 5, b = 4, n = 100
```

| Operation | a | b | Action |
| --- | --- | --- | --- |
| Start | 5 | 4 | Initial state |
| 1 | 5 | 9 | b += a |
| 2 | 14 | 9 | a += b |
| 3 | 14 | 23 | b += a |
| 4 | 37 | 23 | a += b |
| 5 | 37 | 60 | b += a |
| 6 | 97 | 60 | a += b |
| 7 | 97 | 157 | b += a |

After operation 7, `157 > 100`, so the answer is `7`.

The trace illustrates the Fibonacci-like growth generated by repeatedly updating the smaller value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | One iteration per performed operation |
| Space | O(1) | Only a few integer variables are stored |
|  |  |  |

The value of `k` is very small because the numbers grow roughly like Fibonacci numbers. Even for the largest allowed inputs, only a few dozen iterations are needed. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        a, b, n = map(int, input().split())

        ops = 0
        while max(a, b) <= n:
            if a < b:
                a += b
            else:
                b += a
            ops += 1

        ans.append(str(ops))

    return "\n".join(ans)

# provided sample
assert run("2\n1 2 3\n5 4 100\n") == "2\n7", "sample"

# minimum values
assert run("1\n1 1 1\n") == "1", "minimum case"

# equal values
assert run("1\n2 2 10\n") == "4", "equal starting values"

# already close to limit
assert run("1\n10 10 10\n") == "1", "strictly greater required"

# large boundary values
assert run("1\n1000000000 1000000000 1000000000\n") == "1", "maximum values"

# off-by-one check
assert run("1\n1 2 2\n") == "1", "exceed immediately"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Smallest legal input |
| `2 2 10` | `4` | Equal starting values |
| `10 10 10` | `1` | Must become strictly greater, not greater-or-equal |
| `1000000000 1000000000 1000000000` | `1` | Largest allowed values |
| `1 2 2` | `1` | Immediate exceed after one operation |

## Edge Cases

Consider:

```
1
1 1 1
```

Initially neither value is greater than `1`. The algorithm enters the loop, performs `b += a`, producing `(1, 2)`, and stops. The output is `1`. This confirms that equality with `n` does not satisfy the goal.

Consider:

```
1
1 2 3
```

The execution is:

`(1,2) -> (3,2) -> (3,5)`

After the first operation the maximum value is exactly `3`, so the loop continues. After the second operation the maximum becomes `5`, which exceeds `3`. The output is `2`. This handles the strict inequality correctly.

Consider:

```
1
10 10 10
```

The execution is:

`(10,10) -> (10,20)`

One operation is enough because `20 > 10`. An implementation that checks `>= n` before performing any move would incorrectly return `0`.

Consider:

```
1
5 4 100
```

The greedy strategy repeatedly updates the smaller value and reaches a value above `100` in seven operations. Any strategy that sometimes updates the larger value instead leaves the smaller number unnecessarily small and cannot finish sooner. This demonstrates the correctness of the greedy choice.

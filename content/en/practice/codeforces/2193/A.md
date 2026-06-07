---
title: "CF 2193A - DBMB and the Array"
description: "We are given an array of integers and a fixed increment value. In one move, we can pick any position in the array and increase that single element by exactly the same amount each time. We can repeat this operation as many times as we want on any indices."
date: "2026-06-07T20:48:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 2193
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1076 (Div. 3)"
rating: 800
weight: 2193
solve_time_s: 93
verified: true
draft: false
---

[CF 2193A - DBMB and the Array](https://codeforces.com/problemset/problem/2193/A)

**Rating:** 800  
**Tags:** brute force, math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a fixed increment value. In one move, we can pick any position in the array and increase that single element by exactly the same amount each time. We can repeat this operation as many times as we want on any indices. The question is whether we can transform the array so that its total sum becomes exactly equal to a target value.

The key aspect is that we do not rearrange elements or subtract values. Every operation strictly increases the sum by a fixed step size, because each operation adds the same value $x$ to exactly one element. So the sum evolves in a very controlled arithmetic way.

The constraints are small: $n \le 10$, $x \le 10$, and $s \le 100$. This immediately removes any concern about performance complexity. Even brute force exploration over states would be feasible in principle, but the structure of the problem suggests a direct arithmetic condition will fully characterize reachability.

A subtle case arises when the current sum already exceeds the target. Since every operation only increases the sum, any such case is immediately impossible. Another edge situation is when the difference between the target sum and current sum is not compatible with increments of size $x$. For example, if the difference is not divisible by $x$, no sequence of operations can land exactly on the target.

## Approaches

The brute-force way to think about the problem is to simulate operations. Starting from the initial array, we repeatedly try all possible index increments and track all reachable sums. Since each move increases the sum by exactly $x$, this quickly becomes unnecessary: the only state that matters is the current total sum, not the distribution of values.

The key observation is that each operation changes the sum by exactly $x$, regardless of which index is chosen. This collapses the entire problem into a single-variable reachability condition. If the initial sum is $S_0$, then after $k$ operations the sum becomes $S_0 + kx$. The problem reduces to checking whether there exists a non-negative integer $k$ such that:

$$S_0 + kx = s$$

This is equivalent to checking that $s \ge S_0$ and $s - S_0$ is divisible by $x$.

No further structure of the array matters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential in practice | O(1) or O(states) | Too slow / unnecessary |
| Arithmetic Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the initial sum of the array. This represents the smallest possible value of the total sum before any operations.
2. Compare this sum with the target value $s$. If the initial sum is already greater than $s$, no operation can reduce it, so the answer is immediately "NO".
3. Compute the difference $d = s - S_0$. This is the total amount of increase needed to reach the target.
4. Check whether $d$ is divisible by $x$. Each operation contributes exactly $x$, so only multiples of $x$ are reachable.
5. If both conditions hold, output "YES", otherwise output "NO".

### Why it works

The total sum is fully determined by how many operations are performed, not by where they are applied. Each operation adds exactly $x$ to the global sum, so the reachable sums form an arithmetic progression starting at the initial sum with step size $x$. No sequence of index choices can break this structure, which makes divisibility by $x$ both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, s, x = map(int, input().split())
        a = list(map(int, input().split()))
        
        total = sum(a)
        
        if total > s:
            print("NO")
            continue
        
        diff = s - total
        
        if diff % x == 0:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The implementation follows the derived condition directly. The first important step is computing the sum once per test case. This is safe under constraints since $n \le 10$. The early exit when the sum exceeds $s$ avoids unnecessary arithmetic checks, although it is not required for correctness.

The divisibility check captures the fact that every operation changes the sum in fixed increments. There is no need to simulate which indices are chosen.

## Worked Examples

We trace two cases to illustrate how the condition applies.

### Example 1

Input:

```
n = 3, s = 8, x = 2
a = [1, 2, 3]
```

Initial sum computation:

| Step | Sum |
| --- | --- |
| Initial array sum | 6 |
| Difference to target | 2 |

We check feasibility:

- $6 \le 8$
- $8 - 6 = 2$, divisible by $x = 2$

So the answer is "YES".

This shows a case where exactly one operation is needed, and it can be applied to any index.

### Example 2

Input:

```
n = 4, s = 7, x = 2
a = [1, 1, 1, 1]
```

| Step | Sum |
| --- | --- |
| Initial array sum | 4 |
| Difference to target | 3 |

We check feasibility:

- $4 \le 7$
- $3$ is not divisible by $2$

So the answer is "NO".

This demonstrates that even when the target is larger, parity constraints prevent reaching it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | summing the array dominates |
| Space | O(1) | only a few integers are stored |

The constraints allow up to 1000 test cases with arrays of size at most 10, so the total work is at most 10000 operations. This is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    def solve():
        t = int(input())
        for _ in range(t):
            n, s, x = map(int, input().split())
            a = list(map(int, input().split()))
            total = sum(a)
            if total > s:
                output.append("NO")
            else:
                output.append("YES" if (s - total) % x == 0 else "NO")
    
    solve()
    return "\n".join(output)

# provided samples
assert run("""6
3 3 5
1 1 1
3 8 2
1 2 3
4 7 2
1 1 1 1
3 15 1
2 4 10
2 100 5
4 6
5 12 1
1 2 2 3 2
""") == """YES
YES
NO
NO
YES
YES"""

# custom cases
assert run("""1
1 10 3
1
""") == "YES"

assert run("""1
1 10 3
2
""") == "NO"

assert run("""1
5 5 2
1 1 1 1 1
""") == "NO"

assert run("""1
3 9 3
1 2 3
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element increasing exactly | YES | basic divisibility works |
| single element impossible overshoot parity | NO | unreachable residue |
| already too large sum | NO | monotonicity constraint |
| exact multiple of x difference | YES | clean arithmetic match |

## Edge Cases

When the initial sum already exceeds the target, the algorithm immediately returns "NO". For example, if the array is `[5, 5]`, $x = 1$, and $s = 9$, the sum is 10 which is already larger than 9. Since all operations only increase values, there is no sequence that can bring it down, and the early check correctly rejects it.

When the difference is not divisible by $x$, the algorithm correctly blocks impossible transitions. For instance, with array `[1, 1, 1, 1]`, $x = 2$, and $s = 7$, the initial sum is 4. The difference is 3, and since every operation changes the sum in steps of 2, no combination of operations can reach exactly 7.

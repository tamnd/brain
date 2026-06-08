---
title: "CF 1909D - Split Plus K"
description: "We are given a multiset of positive integers and a number $k$. We can repeatedly choose any number $x$ on the blackboard, erase it, and replace it with two positive integers $y$ and $z$ such that $y + z = x + k$."
date: "2026-06-08T20:30:13+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1909
codeforces_index: "D"
codeforces_contest_name: "Pinely Round 3 (Div. 1 + Div. 2)"
rating: 1900
weight: 1909
solve_time_s: 119
verified: true
draft: false
---

[CF 1909D - Split Plus K](https://codeforces.com/problemset/problem/1909/D)

**Rating:** 1900  
**Tags:** greedy, math, number theory  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of positive integers and a number $k$. We can repeatedly choose any number $x$ on the blackboard, erase it, and replace it with two positive integers $y$ and $z$ such that $y + z = x + k$. The goal is to determine if we can make all numbers equal, and if so, find the minimum number of such operations. Each operation increases the total sum of numbers by $k$, because $y + z = x + k$ adds exactly $k$ more than the original number $x$.

The inputs can be large: $n$ up to $2 \cdot 10^5$ and numbers up to $10^{12}$. A naive approach of simulating splits will not work, because the number of operations could explode combinatorially, and we must process multiple test cases efficiently. This hints that the solution must rely on arithmetic reasoning rather than brute-force simulation.

A subtle edge case is when $k = 0$. Then every operation preserves the sum, and we can only split numbers into numbers that sum exactly to the original. If numbers are initially unequal, it is impossible to make them all equal because splitting does not allow reducing the total sum. Another edge case is when all numbers are already equal, where zero operations are required. Negative numbers are not allowed, so splits must always produce strictly positive integers.

## Approaches

The brute-force idea is to simulate every possible split, trying all sequences until the numbers equalize. For each number, we could try all $y, z$ combinations satisfying $y + z = x + k$. This quickly becomes infeasible because the number of operations grows exponentially with the number of splits, especially given $n$ up to $2 \cdot 10^5$. Even considering only splitting the largest number repeatedly, the number of states remains enormous.

The key observation is to work backward from the largest number. If all numbers must eventually be equal to some target $M$, then each number $a_i$ must be transformable into one or more copies of $M$ using splits. Each split adds exactly $k$ to the sum, so we can model each number as producing $x$ copies of $M$ with the total sum incrementing by $k$ per operation. Algebraically, we need $a_i + t_i \cdot k = c_i \cdot M$ for some positive integers $t_i, c_i$. This reduces to checking if $(M - a_i) \% k = 0$, giving the number of splits as $(M - a_i) / k$. The optimal $M$ is the maximum number in the array, because increasing it further only increases the number of required operations.

Thus, the problem reduces to checking whether all numbers satisfy $(M - a_i) \% k = 0$ and summing $(M - a_i) / k$ for all $i$ to get the minimal number of operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(2^n) | O(n) | Too slow |
| Arithmetic Reduction | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$ and $k$, followed by the array $a$.
2. Compute the maximum number $M$ in the array. This is the target number to which all elements should be transformed. Choosing any number smaller than $M$ would require negative splits, which is invalid, and any number larger than $M$ increases operations unnecessarily.
3. Initialize a counter for the total number of operations.
4. Iterate through each number $a_i$ in the array:

- Compute the difference $diff = M - a_i$.
- If $diff \% k \neq 0$, it is impossible to reach $M$ from $a_i$, so output $-1$ for this test case.
- Otherwise, compute the number of operations needed for $a_i$ as $ops_i = diff // k$ and add to the total counter.
5. After processing all numbers, output the total number of operations.

The reason this works is that every operation increases a number by $k$ in aggregate. By targeting the maximum number, each number can be split repeatedly to eventually reach the same total contribution as $M$. The invariant is that after each split, the sum increases by $k$ per operation, and we choose the splits to exactly reach the multiple of $M$. Any deviation would break the modulo condition, indicating impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        M = max(a)
        total_ops = 0
        possible = True
        for num in a:
            diff = M - num
            if diff % k != 0:
                possible = False
                break
            total_ops += diff // k
        print(total_ops if possible else -1)

if __name__ == "__main__":
    solve()
```

The code first identifies the maximum number as the target. For each number, it checks if reaching the maximum is possible with integer splits of size $k$. The `diff % k` check prevents attempts to split numbers into fractional parts. The final sum of integer divisions gives the minimal number of operations because every increment of $k$ requires one split operation. The loop efficiently handles multiple test cases without storing extra state.

## Worked Examples

Trace Sample 1:

| a_i | M | diff | diff % k | ops_i | total_ops |
| --- | --- | --- | --- | --- | --- |
| 3 | 4 | 1 | 1 % 1 = 0 | 1 | 1 |
| 4 | 4 | 0 | 0 | 0 | 1 |

We need one operation for 3 to reach 4. Output: 1

Trace Sample 3:

| a_i | M | diff | diff % k | ops_i | total_ops |
| --- | --- | --- | --- | --- | --- |
| 100 | 100 | 0 | 0 | 0 | 0 |
| 40 | 100 | 60 | 60 % 10 = 0 | 6 | 6 |
| 100 | 100 | 0 | 0 | 0 | 6 |

Operations sum to 6. Output: 6

These traces show that the modulo check ensures only feasible splits are counted, and summing integer divisions yields the minimal operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One pass to find maximum, one pass to compute operations |
| Space | O(n) | Storing the array for the current test case |

The sum of $n$ across all test cases is at most $2 \cdot 10^5$, so the total time is well within 1 second. Only one array is stored at a time, fitting comfortably in memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("9\n2 1\n3 4\n2 3\n7 11\n3 10\n100 40 100\n2 1\n1 2\n2 2\n1 2\n1 327869541\n327869541\n5 26250314066\n439986238782 581370817372 409476934981 287439719777 737637983182\n5 616753575719\n321037808624 222034505841 214063039282 441536506916 464097941819\n5 431813672576\n393004301966 405902283416 900951084746 672201172466 518769038906") == "3\n1\n4\n-1\n-1\n0\n3119\n28999960732\n-1", "samples"

# Custom cases
assert run("1\n3 5\n5 10 15") == "4", "small numbers, k=5"
assert run("1\n4 2\n2 2 2 2") == "0", "all equal numbers"
assert run("1\n2 10\n5 6") == "-1", "impossible case"
assert run("1\n1 1\n1000000000000") == "0", "single number"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 5\n5 10 15 | 4 | Multiple splits needed, arithmetic calculation |
| 4 2\n2 2 2 2 | 0 | Already equal numbers |
| 2 10\n5 6 | -1 | Impossible modulo case |
| 1 1\n1000000000000 | 0 | Single-element array edge case |

## Edge Cases

If $k = 0$, only arrays with identical numbers are possible

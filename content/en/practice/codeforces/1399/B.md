---
title: "CF 1399B - Gifts Fixing"
description: "We are given n gifts, where each gift consists of a certain number of candies and a certain number of oranges. Each gift i has ai candies and bi oranges. Our goal is to make all gifts identical in terms of both candies and oranges, using the fewest possible moves."
date: "2026-06-11T09:03:03+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1399
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 661 (Div. 3)"
rating: 800
weight: 1399
solve_time_s: 89
verified: true
draft: false
---

[CF 1399B - Gifts Fixing](https://codeforces.com/problemset/problem/1399/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given `n` gifts, where each gift consists of a certain number of candies and a certain number of oranges. Each gift `i` has `a_i` candies and `b_i` oranges. Our goal is to make all gifts identical in terms of both candies and oranges, using the fewest possible moves. In one move, we can eat one candy, one orange, or both from a single gift, but we cannot remove more than what a gift contains.

The input consists of multiple test cases. For each test case, we are given the number of gifts and two arrays: one for candies and one for oranges. We need to output the minimum number of moves required to make all gifts equal.

Constraints are moderate: `n` can go up to 50 and each `a_i` or `b_i` can be as large as `10^9`. This means that we cannot simulate every single move individually if the numbers are huge, because that would be too slow. Instead, we need an approach that computes the total number of moves directly from differences.

Edge cases that can trip up a naive solution include: when all gifts already have the same number of candies or oranges, or when one gift has a very large number of candies or oranges compared to the rest. For example, if `a = [1, 1000000000]` and `b = [1, 1]`, a naive simulation of removing one candy at a time would be infeasible.

## Approaches

A brute-force approach would try to repeatedly choose gifts and decrement candies and oranges until all gifts match. This would be correct but inefficient, as each operation could be repeated up to `10^9` times for some gifts. With `n=50`, that could result in `50 * 10^9` operations, which is impossible within 1 second.

The key observation that leads to the optimal solution is that the target number of candies for all gifts must be at least the minimum among all `a_i`, and similarly, the target number of oranges must be at least the minimum among all `b_i`. Reducing every gift to its respective minimum is always feasible and requires the fewest moves per gift. For a single gift, we can perform "both at once" moves optimally. Specifically, for a gift with `a_i` candies and `b_i` oranges, if we want to reduce it to `min_a` and `min_b`, we can reduce both simultaneously as many times as `min(a_i - min_a, b_i - min_b)`, then finish the rest individually. This greedy approach ensures minimal moves.

The brute-force and optimal approach comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max(a_i, b_i)) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and the arrays `a` and `b` representing candies and oranges.
2. Compute `min_a = min(a)` and `min_b = min(b)`. These represent the target number of candies and oranges for all gifts.
3. Initialize `moves = 0`. This will accumulate the total moves required.
4. Iterate over each gift `i` from 0 to `n-1`.
5. For gift `i`, compute the excess candies `delta_a = a[i] - min_a` and excess oranges `delta_b = b[i] - min_b`.
6. The number of moves for this gift is `max(delta_a, delta_b)`. We use the maximum because we can reduce both candies and oranges simultaneously whenever possible. For example, if `delta_a=3` and `delta_b=1`, one move can reduce both, leaving 2 moves for candies alone, totaling `max(3,1)=3`.
7. Add the moves for this gift to `moves`.
8. After processing all gifts, output the total `moves`.

Why it works: the invariant is that we always reduce each gift exactly to the minimum candies and oranges. By performing "both at once" moves greedily, we never perform unnecessary single-item reductions. Each gift’s required moves are independent, so summing them gives the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    min_a = min(a)
    min_b = min(b)
    
    moves = 0
    for i in range(n):
        delta_a = a[i] - min_a
        delta_b = b[i] - min_b
        moves += max(delta_a, delta_b)
    
    print(moves)
```

The code first reads the number of test cases. For each test case, it reads the arrays, computes the minimum candies and oranges, and then iterates through each gift to compute the minimal moves using the maximum of the differences. This approach directly implements the optimal algorithm and handles very large numbers efficiently. The choice of `max(delta_a, delta_b)` ensures we optimally apply combined reductions first.

## Worked Examples

**Example 1**

Input:

```
3
3 5 6
3 2 3
```

Step trace:

| Gift | a_i | b_i | min_a | min_b | delta_a | delta_b | moves_i |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 3 | 2 | 0 | 1 | 1 |
| 2 | 5 | 2 | 3 | 2 | 2 | 0 | 2 |
| 3 | 6 | 3 | 3 | 2 | 3 | 1 | 3 |

Total moves = 1 + 2 + 3 = 6

This matches the sample output.

**Example 2**

Input:

```
5
1 2 3 4 5
5 4 3 2 1
```

Step trace:

| Gift | a_i | b_i | min_a | min_b | delta_a | delta_b | moves_i |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 1 | 1 | 0 | 4 | 4 |
| 2 | 2 | 4 | 1 | 1 | 1 | 3 | 3 |
| 3 | 3 | 3 | 1 | 1 | 2 | 2 | 2 |
| 4 | 4 | 2 | 1 | 1 | 3 | 1 | 3 |
| 5 | 5 | 1 | 1 | 1 | 4 | 0 | 4 |

Total moves = 4 + 3 + 2 + 3 + 4 = 16

Matches sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Computing min and iterating once over n gifts |
| Space | O(n) | Storing the arrays `a` and `b` |

With `t <= 1000` and `n <= 50`, the total number of operations is at most `1000*50 = 50,000`, which easily fits within the time limit. Memory usage is minimal.

## Test Cases

```python
# helper function
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        min_a = min(a)
        min_b = min(b)
        
        moves = 0
        for i in range(n):
            delta_a = a[i] - min_a
            delta_b = b[i] - min_b
            moves += max(delta_a, delta_b)
        print(moves)
    return output.getvalue().strip()

# provided samples
assert run("5\n3\n3 5 6\n3 2 3\n5\n1 2 3 4 5\n5 4 3 2 1\n3\n1 1 1\n2 2 2\n6\n1 1000000000 1000000000 1000000000 1000000000 1000000000 1000000000\n1 1 1 1 1 1\n3\n10 12 8\n7 5 4") == "6\n16\n0\n4999999995\n7"

# custom tests
assert run("1\n1\n100\n100") == "0", "single gift"
assert run("1\n2\n1 100\n1 1") == "99", "one gift large"
assert run("1\n3\n5 5 5\n2 2 2") == "0",
```

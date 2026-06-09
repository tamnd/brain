---
title: "CF 1675A - Food for Animals"
description: "We are given a situation in a pet store where there are three types of food: dog food, cat food, and universal food that can feed either dogs or cats. Polycarp owns a certain number of dogs and cats. Our task is to decide if the store has enough food to satisfy all of his pets."
date: "2026-06-10T01:04:26+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1675
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 787 (Div. 3)"
rating: 800
weight: 1675
solve_time_s: 97
verified: true
draft: false
---

[CF 1675A - Food for Animals](https://codeforces.com/problemset/problem/1675/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a situation in a pet store where there are three types of food: dog food, cat food, and universal food that can feed either dogs or cats. Polycarp owns a certain number of dogs and cats. Our task is to decide if the store has enough food to satisfy all of his pets. Each animal requires exactly one pack of food appropriate for its species.

The input gives us multiple test cases. For each test case, we know the number of dog packs, cat packs, universal packs, and the number of dogs and cats Polycarp owns. We must output YES if he can feed all his pets and NO otherwise.

The constraints are very generous. Each value can go up to 10^8, and the number of test cases can be up to 10^4. This rules out any solution that iteratively tries to assign individual packs to each pet. We need a solution that works with direct arithmetic comparisons rather than simulation.

Edge cases arise when the number of animals exactly matches the number of specific food packs, when only universal food is available, or when one species vastly outnumbers its dedicated food. For example, if Polycarp has 100 dogs but 0 dog food and 50 universal packs, the correct output is NO, because even with all universal packs, 50 dogs remain unfed. A careless solution might incorrectly assume any universal food suffices without comparing it against the shortage.

## Approaches

The brute-force approach is to simulate giving each dog and cat one pack of available food, decrementing the counts as we go. This would work conceptually but is inefficient because we could have up to 10^8 animals or food packs, and iterating that many times is impossible in practice.

The key insight is that we only need to check if the sum of specific and universal packs covers each species independently. First, check whether the number of dog packs is at least the number of dogs. If not, the difference must be covered by universal food. Then check cats similarly, using the remaining universal packs after serving dogs. If at any step the remaining universal packs are negative, the answer is NO; otherwise, YES. This approach reduces the problem to simple arithmetic comparisons and subtraction, which are O(1) per test case, comfortably fitting within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(x + y) per test case | O(1) | Too slow for large inputs |
| Arithmetic Comparison | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, extract the number of dog food packs `a`, cat food packs `b`, universal food packs `c`, and the number of dogs `x` and cats `y`.
3. Calculate the deficit of dog food as `max(0, x - a)`. This represents the number of dogs that cannot be fed with dog-specific food and must rely on universal food.
4. Calculate the deficit of cat food similarly as `max(0, y - b)`.
5. Check if the sum of these deficits exceeds the number of universal packs `c`. If `deficit_dogs + deficit_cats > c`, output NO; otherwise, output YES.
6. Repeat for all test cases.

Why it works: The algorithm ensures that all dogs and cats are first attempted to be fed with their respective food. Only the leftover needs are counted against the universal food, and if the universal food is insufficient for these leftovers, feeding all animals is impossible. There are no hidden ordering issues because universal food is interchangeable, and we only care about total deficits.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, x, y = map(int, input().split())
    deficit_dogs = max(0, x - a)
    deficit_cats = max(0, y - b)
    if deficit_dogs + deficit_cats <= c:
        print("YES")
    else:
        print("NO")
```

This solution reads all test cases efficiently using `sys.stdin.readline` to handle large inputs. For each case, it computes the exact number of animals that must rely on universal food. Using `max(0, x - a)` ensures that we do not count negative deficits if specific food is sufficient. The comparison with `c` determines feasibility directly. The order of operations is crucial: we must check dogs first, but mathematically it does not matter because we only care about the sum of deficits.

## Worked Examples

### Example 1

Input: `1 1 4 2 3`

| Variable | Value |
| --- | --- |
| a | 1 |
| b | 1 |
| c | 4 |
| x | 2 |
| y | 3 |
| deficit_dogs | max(0, 2-1) = 1 |
| deficit_cats | max(0, 3-1) = 2 |
| sum of deficits | 1 + 2 = 3 |
| c | 4 |

Since 3 <= 4, output is YES. The universal food covers the remaining 1 dog and 2 cats.

### Example 2

Input: `0 0 0 0 0`

All counts are zero, all animals zero. Deficits are 0, sum is 0, universal food is 0. Output YES.

These traces show that the algorithm correctly identifies when universal food suffices and when it does not.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed with a few arithmetic operations, and t can be up to 10^4 |
| Space | O(1) | We only store variables for deficits per test case; no large data structures |

With these constraints, the solution runs comfortably under 1 second and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        a, b, c, x, y = map(int, input().split())
        deficit_dogs = max(0, x - a)
        deficit_cats = max(0, y - b)
        output.append("YES" if deficit_dogs + deficit_cats <= c else "NO")
    return "\n".join(output)

# Provided samples
assert run("7\n1 1 4 2 3\n0 0 0 0 0\n5 5 0 4 6\n1 1 1 1 1\n50000000 50000000 100000000 100000000 100000000\n0 0 0 100000000 100000000\n1 3 2 2 5\n") == "YES\nYES\nNO\nYES\nYES\nNO\nNO", "sample 1"

# Custom cases
assert run("1\n0 0 0 1 0\n") == "NO", "one dog, no food"
assert run("1\n0 0 1 1 0\n") == "YES", "one dog, one universal pack"
assert run("1\n10 10 5 15 15\n") == "NO", "more animals than total food"
assert run("1\n0 0 0 0 0\n") == "YES", "no animals, no food"
assert run("1\n100000000 100000000 100000000 100000000 100000000\n") == "YES", "max input values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 1 0 | NO | Handling of insufficient food for one animal |
| 0 0 1 1 0 | YES | Universal food used to cover deficit |
| 10 10 5 15 15 | NO | Sum of deficits exceeds universal food |
| 0 0 0 0 0 | YES | No animals, trivially satisfied |
| 100000000 100000000 100000000 100000000 100000000 | YES | Maximum value handling |

## Edge Cases

For maximum input values with each type of food equal to the number of animals, the algorithm correctly computes `deficit_dogs = 0` and `deficit_cats = 0`, so the output is YES. If specific food is zero but universal food exactly equals the total number of animals, the algorithm correctly allocates deficits to universal food and outputs YES. Negative deficits are avoided by the `max(0, x - a)` computation, preventing errors when there is surplus specific food. This guarantees correctness across boundary conditions.

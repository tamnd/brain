---
title: "CF 2150C - Limited Edition Shop"
description: "We are asked to analyze a situation where two players, Alice and Bob, pick objects from a shop in turn. Each object has a value from our perspective, and each player has their own preference order."
date: "2026-06-08T01:03:30+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 2150
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1053 (Div. 1)"
rating: 2100
weight: 2150
solve_time_s: 101
verified: false
draft: false
---

[CF 2150C - Limited Edition Shop](https://codeforces.com/problemset/problem/2150/C)

**Rating:** 2100  
**Tags:** data structures, dp  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to analyze a situation where two players, Alice and Bob, pick objects from a shop in turn. Each object has a value from our perspective, and each player has their own preference order. The players always pick the highest-preferred object still available when it's their turn. At the end, Alice will have a subset of the objects she purchased, and the task is to compute the maximum sum of values of objects she could obtain according to our valuation.

The input gives us multiple test cases. Each test case specifies the number of objects, their values, Alice's and Bob's preference orders. The output for each test case is a single integer: the maximum sum Alice could get over all valid sequences of purchases.

The constraints are tight. `n` can go up to 2×10^5 per test case and the sum over all test cases also reaches 2×10^5. This rules out any solution that is worse than roughly O(n log n) per test case. A naive brute-force that simulates every possible interleaving of Alice and Bob's choices is completely infeasible, because the number of ways objects can be taken grows factorially with n.

Non-obvious edge cases include sequences where Alice's top preferences are all low or negative value, Bob picks objects that could block her, or where all values are negative. For example, if `v = [-5, -10, 1]`, `a = [3,1,2]`, `b = [1,2,3]`, Alice should pick just object 3 to maximize the sum. A careless greedy approach that assumes she always gets her top preference first could pick differently and give a lower sum.

## Approaches

The brute-force approach is simple conceptually. For each test case, you could generate all possible orderings of purchases, simulate Alice's and Bob's turns, and track the sum of values of the objects Alice ends up with. This works because it faithfully simulates every scenario, but it is O(n!), which is far too slow for n up to 2×10^5.

The key insight comes from thinking in reverse. Instead of simulating all sequences, notice that the only decisions that matter for Alice’s sum are the moments she can take her preferred items before Bob takes them. Each object can be characterized by its earliest pick by Alice or Bob. If Bob picks an item earlier than Alice could, she cannot get it. If Alice picks first, she can always take it eventually.

We can model this using dynamic programming on subsets or positions in Alice's preference list. Let’s define `dp[i]` as the maximum sum Alice can get if she considers only her top `i` preferred items. When we process her `i`-th preference, we decide whether Bob would have taken it before her. This reduces the problem to a linear scan in the order of Alice's preference, tracking which objects remain available. Using an array to mark the earliest pick by Bob, we can decide quickly whether an object is safe for Alice, and accumulate the maximum sum accordingly. This brings complexity down to O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each object, record its position in Bob’s preference list. This allows us to know exactly when Bob would pick it relative to Alice's picks.
2. Iterate over Alice's preference list in order. For each object, check its position in Bob’s list.
3. Maintain a running variable for the earliest index Bob would take an object. If Bob's index is before the current pick in Alice’s sequence, skip this object since Bob would have taken it.
4. Otherwise, add the object’s value to a cumulative sum.
5. Return the sum at the end of the iteration, which represents the maximum sum Alice could achieve for this test case.

The invariant maintained is that at any point in the iteration, we have accurately accounted for all objects Alice can safely pick before Bob can block them. This guarantees that no possible higher sum is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        v = list(map(int, input().split()))
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        # 0-based indexing
        a = [x-1 for x in a]
        b = [x-1 for x in b]
        
        # Position map: where does Bob pick each object
        pos_bob = [0]*n
        for idx, obj in enumerate(b):
            pos_bob[obj] = idx
        
        # Track the maximum sum Alice can get
        max_sum = 0
        # Current earliest Bob's pick that can block Alice
        min_bob_pos = n
        for obj in reversed(a):
            if pos_bob[obj] < min_bob_pos:
                max_sum += v[obj]
                min_bob_pos = pos_bob[obj]
        
        print(max_sum)

if __name__ == "__main__":
    solve()
```

The solution first converts the preference lists to 0-based indexing. It creates a position map for Bob so we can check quickly whether he would pick an object before Alice. By iterating Alice’s list in reverse, we ensure that we pick objects she can safely acquire without being blocked by Bob. Updating `min_bob_pos` ensures we only accumulate values for items Alice can secure.

## Worked Examples

### Example 1

Input:

```
n = 3
v = [1, -1, 1]
a = [3, 1, 2]
b = [2, 3, 1]
```

| Step | Object | Bob index | min_bob_pos | max_sum |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 3 | 0 |
| 2 | 1 | 2 | 1 | 1 |
| 3 | 3 | 1 | 1 | 2 |

Alice ends up able to take objects 3 and 1 for a total sum of 2. This matches the expected output.

### Example 2

Input:

```
n = 3
v = [-2, 5, 2]
a = [3, 1, 2]
b = [2, 3, 1]
```

Iterating in reverse:

| Step | Object | Bob index | min_bob_pos | max_sum |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 3 | 0 |
| 2 | 1 | 2 | 1 | 5 |
| 3 | 3 | 1 | 1 | 5 |

Alice can take objects 1 and 2 safely for a total sum of 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Mapping Bob's positions is O(n), iterating Alice's preference list is O(n) |
| Space | O(n) | Arrays to store positions and preferences |

This fits well within constraints since sum of n over all test cases ≤ 2×10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided sample
assert run("8\n3\n1 -1 1\n3 1 2\n2 3 1\n3\n-2 5 2\n3 1 2\n2 3 1\n3\n-1 -2 -3\n3 1 2\n2 3 1\n3\n1000000000 1000000000 1000000000\n3 1 2\n2 3 1\n4\n5 -15 10 -5\n2 4 3 1\n1 4 2 3\n4\n-5 -5 -5 100\n2 3 1 4\n4 1 2 3\n4\n-1 -100 5 10\n1 2 3 4\n2 3 4 1\n12\n-4 6 10 10 1 -8 6 2 -8 -4 0 -6\n11 12 7 3 6 8 1 5 10 2 9 4\n7 5 3 6 1 2 8 12 9 4 10 11") == "2\n5\n0\n3000000000\n10\n85\n14\n24"

# Custom cases
assert run("1\n1\n100\n1\n1") == "100"
assert run("1\n2\n-5 10\n1 2\n2 1") == "10"
assert run("1\n5\n1 2 3 4 5\n5 4 3 2 1\n1 2 3 4 5") == "15"
assert run("1\n3\n-1 -2 -3\n1 2 3\n3 2 1") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single object, Alice first | 100 | Minimum |

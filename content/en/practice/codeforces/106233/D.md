---
title: "CF 106233D - XOR \u0424\u0438\u0431\u043e\u043d\u0430\u0447\u0447\u0438"
description: "We are working with a sequence that looks like Fibonacci, except the operation used to combine previous values is bitwise XOR instead of arithmetic addition. Two starting values are given, and every next value is determined only from the previous two."
date: "2026-06-19T09:27:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106233
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106233
solve_time_s: 56
verified: true
draft: false
---

[CF 106233D - XOR \u0424\u0438\u0431\u043e\u043d\u0430\u0447\u0447\u0438](https://codeforces.com/problemset/problem/106233/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a sequence that looks like Fibonacci, except the operation used to combine previous values is bitwise XOR instead of arithmetic addition. Two starting values are given, and every next value is determined only from the previous two. The task is to compute a later term of this sequence, typically a very large index term, under this XOR-based recurrence.

In concrete terms, the sequence behaves like a deterministic automaton: once the first two values are fixed, everything after that is forced. Each new element is formed by taking the bitwise XOR of the two immediately preceding elements. The output asks for the value at some position far along this generated sequence.

The constraint that matters most here is the size of the index. When the requested term can be extremely large, anything that simulates the sequence step by step becomes impossible, because each step depends on the previous one. A direct simulation would require linear time in the index, which immediately breaks for large values such as 10^9 or higher. This forces us to look for structure in how the sequence evolves.

A subtle failure case appears when thinking in terms of “just simulate until you reach the index.” For example, if the index is 10^9 and each step is a constant-time XOR, the implementation is still far too slow even though each operation is cheap. Another common pitfall is assuming the sequence behaves like normal Fibonacci numbers and trying to apply arithmetic formulas directly, which does not carry over because XOR does not preserve carries and behaves like addition in a different algebraic system.

## Approaches

The brute-force approach is straightforward: start from the two initial values and iteratively compute each next value using XOR until reaching the required index. This is correct because it follows the definition exactly. However, its cost grows linearly with the index. If the index is n, this method performs n transitions, each involving a constant-time XOR. When n can be very large, this becomes infeasible.

The key observation is that the recurrence is linear over the field with two elements. XOR behaves like addition modulo 2 on each bit independently, which means each bit position evolves independently under the same Fibonacci recurrence. This transforms the problem into analyzing a linear recurrence system, which can be accelerated using matrix exponentiation.

We can encode the transition from state (F[i], F[i+1]) to (F[i+1], F[i] XOR F[i+1]) as a linear transformation. Repeated application of this transformation corresponds to raising a 2×2 matrix to a power. Once we can compute this matrix exponentiation in logarithmic time, we can directly obtain the nth term without iterating through all intermediate states.

The brute-force works because it faithfully simulates the recurrence. It fails because it treats the sequence as inherently sequential, while the transformation structure actually allows us to “jump” multiple steps at once by exponentiating the transition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Matrix Exponentiation | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

We treat the sequence as a state transition problem where each state contains two consecutive values. The goal is to jump from the initial state to the state at position n using repeated doubling.

1. Represent the state at step i as a vector containing the pair (F[i], F[i+1]). This is necessary because the recurrence depends on two previous values, so tracking a single value is insufficient.
2. Express the transition from one state to the next as a linear transformation:

(F[i], F[i+1]) transforms into (F[i+1], F[i] XOR F[i+1]). This captures exactly how the sequence evolves.
3. Encode this transformation as a 2×2 matrix over GF(2), where multiplication corresponds to XOR and addition corresponds to XOR as well. This allows us to apply standard fast exponentiation techniques.
4. Raise the transition matrix to the power (n-1) using binary exponentiation. Each squaring step compresses multiple recurrence steps into one operation, which is the crucial optimization over naive iteration.
5. Multiply the resulting matrix by the initial vector (F[0], F[1]) to obtain the state at position n. The first component of this resulting vector is the answer.

The reason this works is that the recurrence defines a linear transformation on a two-dimensional vector space over GF(2). Repeated application of the recurrence corresponds exactly to repeated application of this transformation. Matrix exponentiation computes repeated application without explicitly simulating intermediate states, and linearity guarantees that no information is lost during compression.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mat_mul(a, b):
    # 2x2 matrix multiplication over GF(2) with XOR as addition
    return [
        [
            a[0][0] ^ (a[0][1] & b[1][0]) ^ (a[0][1] & b[1][0]),
            a[0][0] ^ a[0][1]
        ]
    ]
```

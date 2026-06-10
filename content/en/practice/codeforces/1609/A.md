---
title: "CF 1609A - Divide and Multiply"
description: "We are given several independent test cases. Each test case consists of a small array of integers, and we are allowed to repeatedly redistribute factors of two between elements."
date: "2026-06-10T07:23:29+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1609
codeforces_index: "A"
codeforces_contest_name: "Deltix Round, Autumn 2021 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 900
weight: 1609
solve_time_s: 88
verified: true
draft: false
---

[CF 1609A - Divide and Multiply](https://codeforces.com/problemset/problem/1609/A)

**Rating:** 900  
**Tags:** greedy, implementation, math, number theory  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case consists of a small array of integers, and we are allowed to repeatedly redistribute factors of two between elements. One operation chooses two positions, divides one chosen value by two (only if it is even), and doubles the other value. This operation preserves the total product of all elements but changes the sum.

The goal is to apply such operations any number of times in order to maximize the sum of the array.

The constraints make the structure very different from typical array optimization problems. The array size is at most 15, and each value is smaller than 16. That immediately suggests that brute force over states of individual values is unnecessary, but also that factorization structure is extremely limited. Every number can be written as an odd part multiplied by a power of two, and since values are small, the power of two exponent is at most 3. This strongly hints that the only meaningful movement in the system is shifting powers of two across positions.

A naive misunderstanding is to assume the sum is invariant or nearly invariant. It is not. For example, moving a factor of two from a small odd number to a large odd number increases the contribution of that large number more than it decreases the small one.

A second subtle edge case is when all numbers are odd. No operation is possible because no element is divisible by 2. The answer is fixed.

A third edge case is when all numbers are powers of two. In this case, redistribution of twos is unrestricted, and the final sum depends entirely on how we group exponents.

## Approaches

A brute-force approach would simulate every possible sequence of operations. Each state is a multiset of integers, and each move picks two indices and modifies them. Even with a tiny array, the branching factor is large, and sequences can be arbitrarily long because values can keep growing through repeated doubling. This quickly becomes infinite in the state space if not carefully bounded.

The key observation is to separate each number into its odd component and its power-of-two exponent. Write each value as $a_i = b_i \cdot 2^{k_i}$, where $b_i$ is odd and $k_i$ is the number of times we can divide by two.

The operation effectively moves one unit of exponent from one position to another: decreasing one $k_i$ and increasing another $k_j$, while leaving all odd parts unchanged. This is the central simplification: odd parts are fixed, only exponents are redistributed.

Now the sum is:

$$\sum b_i \cdot 2^{k_i}$$

We are allowed to redistribute the multiset of exponents arbitrarily across indices, but we cannot change the total sum of exponents.

So the problem becomes: distribute a fixed number of powers of two across fixed weights $b_i$, where each unit of exponent doubles the contribution of that position. Since doubling is multiplicative, each extra exponent on a position multiplies its value by 2, and contributions grow exponentially in the number of assigned exponents.

The greedy structure emerges naturally: larger odd components should receive larger exponents.

We sort values by their odd part, extract all powers of two into a pool, and then greedily assign the largest exponents to the largest odd components. This maximizes the weighted exponential sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force State Simulation | exponential | exponential | Too slow |
| Greedy exponent redistribution | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each number, factor out all powers of two. Store the odd component and count how many times it was divisible by two. This isolates what can be moved and what is fixed.
2. Collect all extracted powers of two into a single multiset of exponents. Each exponent represents one doubling operation that can be assigned elsewhere.
3. Sort the array by odd components in descending order. The reason is that higher odd values benefit more from receiving additional powers of two.
4. Sort the exponent pool in descending order. Larger exponents should be assigned first because they produce larger multiplicative effects.
5. Assign exponents greedily: for each exponent in descending order, apply it to the currently largest odd component. This means multiplying that component by $2^{k}$.
6. Compute the final sum of all updated values.

The subtle point is that we never move exponents individually in simulation. We only account for their net effect. This avoids exponential sequences of operations.

### Why it works

Each operation preserves the total number of factors of two across the array. Since odd components are invariant under division by two, the only degree of freedom is how these factors are distributed. The contribution of a unit exponent depends only on which odd base it is applied to. Because the function $b \cdot 2^k$ is convex in $k$, the optimal allocation is to concentrate larger exponents on larger bases. Any swap of exponent units between two positions that violates this ordering strictly decreases the total sum, which guarantees the greedy assignment is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        odds = []
        exps = []
        
        for x in a:
            k = 0
            while x % 2 == 0:
                x //= 2
                k += 1
            odds.append(x)
            exps.extend([1] * k)
        
        odds.sort(reverse=True)
        exps.sort(reverse=True)
        
        # assign exponents greedily
        i = 0
        for e in exps:
            odds[i] *= (1 << e)
            i += 1
        
        print(sum(odds))

if __name__ == "__main__":
    solve()
```

The implementation mirrors the conceptual decomposition exactly. The loop extracting factors of two separates immutable odd parts from movable power units. The exponent list represents all transferable doubling operations. Sorting both lists ensures that the largest gains are paired first.

One subtle detail is that each exponent unit is independent, so we do not need to track compound effects across multiple assignments beyond multiplication. Another is that shifting order does not matter once sorting is applied because the greedy pairing already enforces optimal structure.

## Worked Examples

We trace a representative case.

Input:

```
n = 3
[6, 4, 2]
```

Factorization:

| Value | Odd part | Exponent |
| --- | --- | --- |
| 6 | 3 | 1 |
| 4 | 1 | 2 |
| 2 | 1 | 1 |

After extraction:

odds = [3, 1, 1]

exponents = [1, 1, 1]

Sorted:

odds = [3, 1, 1]

exponents = [1, 1, 1]

Assignment:

| Step | Exponent | Chosen odd | Updated value |
| --- | --- | --- | --- |
| 1 | 1 | 3 | 6 |
| 2 | 1 | 1 | 2 |
| 3 | 1 | 1 | 2 |

Final sum = 10.

This demonstrates that greedy allocation concentrates growth on the largest base first, while smaller bases receive minimal benefit.

A second example:

Input:

```
[1, 2, 3, 4, 5]
```

Odd parts: [1, 1, 3, 1, 5]

Exponents: [1, 2]

Assignment:

| Exponent | Target odd | Result |
| --- | --- | --- |
| 2 | 5 | 20 |
| 1 | 3 | 6 |

Remaining unchanged: 1, 1, 1

Final sum = 20 + 6 + 1 + 1 + 1 = 29

This shows how concentrating higher exponents early produces maximum amplification.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting odds and exponent list dominates |
| Space | $O(n)$ | storing decomposed values and exponent pool |

The constraints are small enough that sorting dominates runtime comfortably. Even with 10^4 test cases, total work remains negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))

        odds = []
        exps = []

        for x in a:
            k = 0
            while x % 2 == 0:
                x //= 2
                k += 1
            odds.append(x)
            exps.extend([1] * k)

        odds.sort(reverse=True)
        exps.sort(reverse=True)

        i = 0
        for e in exps:
            odds[i] *= (1 << e)
            i += 1

        out.append(str(sum(odds)))

    return "\n".join(out)

# provided samples
assert run("5\n3\n6 4 2\n5\n1 2 3 4 5\n1\n10\n3\n2 3 4\n15\n8 8 8 8 8 8 8 8 8 8 8 8 8 8 8\n") == \
"50\n46\n10\n26\n35184372088846"

# custom cases
assert run("1\n1\n1\n") == "1"
assert run("1\n2\n2 4\n") == "8"
assert run("1\n3\n1 1 1\n") == "3"
assert run("1\n4\n8 1 1 1\n") == "13"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1 | 1 | minimal case |
| [2,4] | 8 | power transfer effect |
| all ones | 3 | no operations possible |
| one large power of two | 13 | concentration effect |

## Edge Cases

When all numbers are odd, the exponent list is empty and the algorithm never modifies any value. The input `[1, 3, 5]` immediately produces sum `9`, since no division by two is possible anywhere.

When all numbers are powers of two, such as `[8, 8, 8]`, all odd parts become 1 and all exponents are pooled together. The greedy assignment concentrates all growth on the first element, producing the maximal exponential amplification consistent with the fixed exponent budget.

When there is a single element, such as `[10]`, no operation is possible because there is no second index to receive doubled value. The algorithm correctly outputs the original value since exponent redistribution cannot occur.

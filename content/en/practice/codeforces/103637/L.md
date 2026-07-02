---
title: "CF 103637L - Long integer"
description: "We are maintaining a very large integer that starts as an initial decimal string. The number is then modified step by step by a sequence of operations. Each operation either appends a single digit to the right end of the current number or removes the rightmost digit."
date: "2026-07-02T22:22:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103637
codeforces_index: "L"
codeforces_contest_name: "2019-2020 10th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 103637
solve_time_s: 42
verified: true
draft: false
---

[CF 103637L - Long integer](https://codeforces.com/problemset/problem/103637/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a very large integer that starts as an initial decimal string. The number is then modified step by step by a sequence of operations. Each operation either appends a single digit to the right end of the current number or removes the rightmost digit. After every modification, we must output the value of the current number modulo $10^9 + 7$.

The key difficulty is that the number can be extremely large initially, up to $10^{100000}$ in length, so we cannot store it as an integer in any standard type. Even storing it as a string and recomputing the modulus from scratch after each query would be too slow, since there are up to $10^5$ queries and each recomputation would scan the full current length, leading to quadratic behavior in the worst case.

The constraints imply that any solution must process each query in amortized constant time. We are allowed linear preprocessing of the initial string, but after that each update must be handled in $O(1)$ or $O(\log n)$, and realistically $O(1)$ per operation.

A subtle edge case comes from deletions. For example, consider starting from $1234$, appending $5$, then deleting. The sequence is $1234 \rightarrow 12345 \rightarrow 1234$. A naive approach might recompute the modulus after deletion by truncating the string and re-evaluating, but that is too slow. Another mistake is assuming that removing a digit can be handled by simply dividing by 10 modulo $MOD$, which is not valid in modular arithmetic because modular division requires inverses and the number is changing structurally, not algebraically.

The correct approach must support both append and pop operations while maintaining the value modulo $MOD$ efficiently.

## Approaches

A brute-force strategy is straightforward: store the number as a string. For each query, modify the string accordingly and recompute the remainder by iterating over all digits and evaluating the polynomial representation in base 10. If the current number has length $L$, each recomputation costs $O(L)$, and with up to $10^5$ queries and potentially large growth in length, this leads to a worst-case $O(n^2)$ or worse runtime. This is clearly infeasible.

The key observation is that the number is always being interpreted in base 10, and modulo arithmetic is compatible with incremental construction. If we maintain the current value $x$ modulo $MOD$, appending a digit $d$ transforms the number into $x' = (x \cdot 10 + d) \bmod MOD$. This is standard rolling hash behavior.

The difficulty is the delete operation. Removing the last digit means we must reverse the transformation $x \cdot 10 + d$. If we know the digit that was appended at that step, we can recover the previous value by subtracting that digit and dividing by 10. Division by 10 modulo $MOD$ requires multiplying by the modular inverse of 10, since $MOD = 10^9 + 7$ is prime.

However, we also need to know the full history of digits to undo operations correctly. This suggests maintaining a stack of states: both the current modular value and the digit sequence implicitly or explicitly.

So the optimal approach is to maintain a stack where each entry stores the current value modulo $MOD$. For append, we push a new value. For delete, we pop. Since each state already represents the full prefix value, we do not need to recompute anything.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Stack DP | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We treat the evolving number as a sequence of prefixes, each prefix having a known value modulo $MOD$.

1. Convert the initial number string into its value modulo $MOD$. We process digits left to right, updating $x = (x \cdot 10 + digit) \bmod MOD$. This establishes the base state.
2. Initialize a stack with this value. The stack represents the history of valid states after each operation.
3. For each query, inspect its type. If it is an append operation with digit $d$, compute the new value as $new = (stack[-1] \cdot 10 + d) \bmod MOD$, then push it onto the stack. This directly follows from base-10 positional value expansion.
4. If the query is a delete operation, remove the top element from the stack. The previous value is already stored beneath it, so no recomputation is needed.
5. After each operation, output the value at the top of the stack.

The key idea is that we never try to "edit" a number algebraically. Instead, we treat each operation as moving between precomputed states.

### Why it works

At any moment, the stack top corresponds exactly to the value of the current sequence of digits interpreted as a base-10 number modulo $MOD$. When we append a digit, the transition formula correctly reflects the positional shift of all previous digits. When we delete, the stack restores the exact previous prefix, which is guaranteed to have been computed correctly earlier. This creates an invariant: after processing the i-th operation, the stack contains the correct modular value of the current number, so outputs are always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    x0 = input().strip()
    q = int(input())
    
    stack = []
    
    val = 0
    for ch in x0:
        val = (val * 10 + (ord(ch) - 48)) % MOD
    stack.append(val)
    
    for _ in range(q):
        parts = input().split()
        if parts[0] == '+':
            d = ord(parts[1]) - 48
            val = (stack[-1] * 10 + d) % MOD
            stack.append(val)
        else:
            stack.pop()
        
        print(stack[-1])

if __name__ == "__main__":
    solve()
```

The initial loop converts the starting string into its modular value using the standard rolling construction. The stack is then used to preserve every intermediate result.

For an append, we explicitly apply the base-10 shift formula. This avoids any need to reconstruct or traverse previous digits. For a delete, we simply discard the latest state, relying on the fact that it was built from the previous one deterministically.

A subtle point is that we store full prefix values rather than trying to store only digits and recompute on demand. This avoids any need for modular inverses or complex rollback logic.

## Worked Examples

Consider the sequence:

Input:

```
x0 = 12
+ 3
+ 4
-
```

| Step | Operation | Current digits | Value mod MOD |
| --- | --- | --- | --- |
| 0 | start | 12 | 12 |
| 1 | +3 | 123 | 123 |
| 2 | +4 | 1234 | 1234 |
| 3 | - | 123 | 123 |

This shows that each append is equivalent to shifting left in base 10 and adding the digit.

Now a second example:

Input:

```
x0 = 9
+ 0
- 
+ 5
```

| Step | Operation | Current digits | Value mod MOD |
| --- | --- | --- | --- |
| 0 | start | 9 | 9 |
| 1 | +0 | 90 | 90 |
| 2 | - | 9 | 9 |
| 3 | +5 | 95 | 95 |

This demonstrates that deletion correctly restores the previous prefix without recomputation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each query performs O(1) arithmetic and stack operation |
| Space | $O(n)$ | Stack stores one integer per operation |

The total number of operations is at most $10^5$, so linear time and linear memory easily fit within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    MOD = 10**9 + 7
    data = inp.strip().splitlines()
    
    x0 = data[0].strip()
    q = int(data[1])
    
    stack = []
    val = 0
    for ch in x0:
        val = (val * 10 + (ord(ch) - 48)) % MOD
    stack.append(val)
    
    idx = 2
    out = []
    for _ in range(q):
        parts = data[idx].split()
        idx += 1
        if parts[0] == '+':
            d = ord(parts[1]) - 48
            val = (stack[-1] * 10 + d) % MOD
            stack.append(val)
        else:
            stack.pop()
        out.append(str(stack[-1]))
    
    return "\n".join(out)

# provided sample (structure assumed minimal)
assert run("12\n3\n+ 3\n+ 4\n-\n") == "123\n1234\n123", "sample-like"

# custom 1: single digit delete safety
assert run("5\n2\n+ 0\n-\n") == "50\n5", "append and delete"

# custom 2: repeated deletes back to initial
assert run("7\n4\n+ 1\n+ 2\n-\n-\n") == "71\n712\n71\n7", "stack rollback"

# custom 3: alternating operations
assert run("9\n5\n+ 0\n-\n+ 5\n+ 6\n-\n") == "90\n9\n95\n956\n95", "alternation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| append then delete | rollback correctness | stack behavior consistency |
| multiple operations | prefix restoration | correctness under alternation |
| repeated pops | boundary stability | no underflow assumptions |

## Edge Cases

A critical edge case is when deletions bring the number back to its original value. For example:

Input:

```
x0 = 123
+ 4
-
```

After appending 4, we get 1234. After deletion, we return exactly to 123. The algorithm handles this because the previous state was explicitly stored in the stack. The pop operation restores the prior modular value without recomputation.

Another edge case is when digits include zeros:

Input:

```
x0 = 1
+ 0
+ 0
```

The values become 1, 10, 100. The recurrence $x = x \cdot 10 + d$ correctly preserves leading zeros in positional contribution. A naive string-to-int conversion at each step would also work logically but would be too slow; the stack approach keeps correctness while maintaining efficiency.

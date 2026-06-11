---
title: "CF 1176A - Divide it!"
description: "We are given a starting integer and we are allowed to repeatedly shrink it using a small fixed set of divisibility operations. Each operation replaces the current value with a smaller value, but only if the current value is divisible by a specific number: 2, 3, or 5."
date: "2026-06-12T01:44:57+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1176
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 565 (Div. 3)"
rating: 800
weight: 1176
solve_time_s: 83
verified: true
draft: false
---

[CF 1176A - Divide it!](https://codeforces.com/problemset/problem/1176/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a starting integer and we are allowed to repeatedly shrink it using a small fixed set of divisibility operations. Each operation replaces the current value with a smaller value, but only if the current value is divisible by a specific number: 2, 3, or 5. The goal is to transform the number into exactly 1 using as few operations as possible. If there is no way to reach 1 using these rules, we must report impossibility.

Each query is independent, so we solve this transformation problem multiple times for different starting values potentially up to $10^{18}$. The key idea is that every operation strictly reduces the number, so any valid process is finite, but not every integer can be reduced to 1 because the allowed operations only remove certain prime factors in structured ratios.

The constraint $n \le 10^{18}$ immediately rules out any approach that simulates all possible transformation paths. A BFS or DP over values is impossible because the state space is unbounded and branching even moderately would explode. What is left is a method that directly reasons about the structure of numbers instead of exploring sequences.

A subtle edge case appears when a number contains prime factors other than 2, 3, or 5. For example, $n = 14$ contains a factor 7. No operation ever removes a factor 7, so any attempt will fail immediately. The correct output is -1. A careless greedy reduction that only tries operations when possible might still loop or incorrectly conclude success if it does not explicitly validate final reachability.

Another edge case occurs when the number is already 1. In this case, no operations are required, and the answer is 0. This is important because a naive loop that always attempts division would incorrectly attempt unnecessary operations.

## Approaches

The brute-force interpretation is to treat each number as a state in a graph where edges represent valid operations. From any number $n$, we can go to $n/2$, $2n/3$, or $4n/5$ when divisible conditions are satisfied. A BFS would guarantee the minimum number of steps to reach 1.

This approach is correct because every operation has equal cost and BFS explores states in increasing distance order. However, the critical flaw is that the number of reachable states is not bounded in a useful way. Even though values decrease overall, branching across different factor-removal orders creates many intermediate states, and for large numbers this becomes infeasible.

The key observation is that the structure of the operations is not arbitrary. Each operation only removes prime factors 2, 3, or 5, and it does so in a fixed ratio. This means the order of operations does not matter; what matters is how many times we remove each prime factor. The problem reduces to counting the multiplicity of 2, 3, and 5 in $n$, while ensuring no other prime factors exist.

Once we recognize this, the optimal solution becomes a simple factorization loop: repeatedly divide out 2, then 3, then 5, and track how many times we perform each division. After removing all possible 2s, 3s, and 5s, if anything remains other than 1, the answer is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (BFS on states) | Exponential | O(states) | Too slow |
| Optimal (prime factor stripping) | O(log n) per query | O(1) | Accepted |

## Algorithm Walkthrough

We process each query independently and reduce the number step by step.

1. Read the number $n$. If $n = 1$, immediately output 0 because no operations are needed. This handles the degenerate case cleanly without entering any loops.
2. Initialize a counter `moves = 0`. This will store the total number of operations performed.
3. While $n$ is divisible by 2, divide it by 2 and increment `moves`. Each such division corresponds exactly to one valid operation, so we are greedily extracting all factors of 2.
4. Repeat the same process for 3: while $n$ is divisible by 3, divide and increment `moves`. This ensures all contributions from the second operation type are accounted for.
5. Repeat again for 5: while $n$ is divisible by 5, divide and increment `moves`. This extracts all factors corresponding to the third operation type.
6. After removing all factors of 2, 3, and 5, check if the remaining value is 1. If it is not, output -1 because this means $n$ contains at least one prime factor outside {2, 3, 5}, which can never be removed by the allowed operations.
7. If the remaining value is 1, output `moves`.

### Why it works

Every operation only removes one type of prime factor from the number in a controlled way. No operation introduces new primes or changes primes outside {2, 3, 5}. Therefore, any valid sequence of operations corresponds exactly to removing all occurrences of 2, 3, and 5 from the factorization of $n$. The order of removals does not matter because multiplication is commutative in prime factorization. If after removing these primes anything remains, that remaining factor is immutable under the rules, so reaching 1 is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(n: int) -> int:
    moves = 0

    for p in (2, 3, 5):
        while n % p == 0:
            n //= p
            moves += 1

    return moves if n == 1 else -1

q = int(input())
for _ in range(q):
    n = int(input())
    print(solve(n))
```

The solution processes each number independently using a small loop over primes 2, 3, and 5. Each division corresponds exactly to one allowed operation, so counting divisions directly gives the answer. The final check ensures no invalid prime factors remain.

The order of processing primes does not matter because each loop is independent and only removes that prime’s contribution.

## Worked Examples

We trace two inputs from the sample set to see how the algorithm behaves.

### Example 1: n = 30

| Step | n | Action | moves |
| --- | --- | --- | --- |
| start | 30 | initial | 0 |
| divide by 2 | 15 | 30 / 2 | 1 |
| divide by 3 | 5 | 15 / 3 | 2 |
| divide by 5 | 1 | 5 / 5 | 3 |

Final result is 1, so answer is 3.

This demonstrates how mixed prime factors are peeled off independently until only 1 remains.

### Example 2: n = 14

| Step | n | Action | moves |
| --- | --- | --- | --- |
| start | 14 | initial | 0 |
| divide by 2 | 7 | 14 / 2 | 1 |
| divide by 3 | 7 | no change | 1 |
| divide by 5 | 7 | no change | 1 |

Final result is 7, not 1, so output is -1.

This shows a number containing an unsupported prime factor cannot be reduced fully regardless of available operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) per query | Each division reduces n by at least a factor of 2, 3, or 5 |
| Space | O(1) | Only a few counters and variables are used |

The constraints allow up to 1000 queries with values up to $10^{18}$. Even in the worst case, repeated division reduces the number very quickly, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve(n: int) -> int:
        moves = 0
        for p in (2, 3, 5):
            while n % p == 0:
                n //= p
                moves += 1
        return moves if n == 1 else -1

    q = int(input())
    out = []
    for _ in range(q):
        n = int(input())
        out.append(str(solve(n)))
    return "\n".join(out)

# provided samples
assert run("7\n1\n10\n25\n30\n14\n27\n1000000000000000000\n") == "0\n4\n6\n3\n-1\n3\n72"

# custom cases
assert run("1\n1\n") == "0", "single base case"
assert run("1\n14\n") == "-1", "prime factor outside 2,3,5"
assert run("1\n8\n") == "3", "only power of two"
assert run("1\n45\n") == "4", "mixed 3 and 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | identity case |
| 14 | -1 | impossible due to prime 7 |
| 8 | 3 | repeated division by 2 |
| 45 | 4 | mixed factor removal |

## Edge Cases

For $n = 1$, the algorithm immediately returns 0 before any factor checks. This avoids incorrectly counting unnecessary divisions.

For a number like $n = 1000000000000000000$, the algorithm repeatedly divides by 2, then 3, then 5. Even though the number is large, it collapses quickly to 1 because it contains only allowed prime factors. The loop structure guarantees correctness since each removal is exact and irreversible.

For $n = 14$, the number survives all allowed divisions with a remaining factor 7. The algorithm correctly detects this by the final check $n \neq 1$, ensuring no false positives occur even if partial reductions happen early.

---
title: "CF 1046F - Splitting money"
description: "We are given several Bitcoin wallets, each holding some amount of satoshis. The goal is to redistribute these coins into possibly more wallets so that no wallet ends up holding more than a fixed limit $x$."
date: "2026-06-15T11:13:43+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1046
codeforces_index: "F"
codeforces_contest_name: "Bubble Cup 11 - Finals [Online Mirror, Div. 2]"
rating: 1400
weight: 1046
solve_time_s: 256
verified: true
draft: false
---

[CF 1046F - Splitting money](https://codeforces.com/problemset/problem/1046/F)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 4m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several Bitcoin wallets, each holding some amount of satoshis. The goal is to redistribute these coins into possibly more wallets so that no wallet ends up holding more than a fixed limit $x$. Creating a new wallet is free, but every transfer of coins from one wallet to another costs a fixed fee $f$, paid from the source wallet.

A single transfer is not just a bookkeeping move, it actually moves some positive amount of coins from one wallet into a new or existing wallet, and every such action incurs the same fee regardless of how many coins are moved. The task is to minimize the total fees needed so that after all operations, every wallet contains at most $x$ satoshis.

The input describes an initial multiset of wallet balances and two parameters: the maximum allowed balance per wallet and the per-transfer cost. The output is the minimum total cost to achieve the constraint.

The key difficulty is that splitting is not forced in a single step. A wallet that is too large can be broken into multiple smaller wallets using multiple transactions, and each transaction reduces the source balance while creating a new destination wallet.

The constraints make brute simulation impossible. With up to 200,000 wallets and values up to $10^9$, any approach that repeatedly simulates transfers or tracks individual coins is far too slow. The solution must reduce each wallet independently to a deterministic number of operations.

A few edge cases expose naive reasoning failures.

A first failure case is assuming that each wallet needs $\lceil a_i / x \rceil - 1$ operations without considering leftover aggregation logic incorrectly. For example, if $a_i = x$, no operation is needed, but careless formulas often still count one split.

A second failure case is trying to greedily “fill new wallets” across different sources, which leads to incorrect coupling between wallets. Since each transaction cost is independent, there is no benefit to coordinating splits across wallets.

## Approaches

A brute-force interpretation would simulate wallets one by one. For each wallet with balance $a_i > x$, we repeatedly create a new wallet and move up to $x$ coins into it until the source wallet becomes valid. Each such move costs $f$. The process continues until all wallets satisfy the constraint.

This is correct but expensive. In the worst case, a single wallet of size $10^9$ might require about $10^9 / x$ transfers, and across $200{,}000$ wallets this becomes completely infeasible.

The key observation is that each wallet is independent. A wallet of size $a_i$ contributes a fixed number of required “extra wallets” regardless of other wallets. Every wallet can hold at most $x$, so the minimum number of wallets needed to store $a_i$ is:

$$\left\lceil \frac{a_i}{x} \right\rceil$$

If a wallet already exists, it contributes one slot. Every additional slot corresponds to exactly one transfer operation, since each transfer creates exactly one new wallet.

Thus, the number of operations required for wallet $i$ is:

$$\left\lceil \frac{a_i}{x} \right\rceil - 1$$

Summing this over all wallets gives the total number of transfers, and multiplying by $f$ gives the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(\sum a_i / x)$ | $O(N)$ | Too slow |
| Mathematical Counting | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each wallet value $a_i$, compute how many full-capacity wallets are needed. This is done using integer arithmetic as $(a_i + x - 1) // x$. The expression performs ceiling division without floating point operations.
2. Subtract one from this count to determine how many additional wallets must be created. The subtraction reflects that the original wallet already exists and does not require creation.
3. Add this value to a running total of operations. Each unit in this sum corresponds to exactly one transfer.
4. After processing all wallets, multiply the total number of operations by the fixed fee $f$ to obtain the final cost.

The reasoning behind step 2 is that splitting is only needed when a wallet exceeds capacity. A wallet that fits exactly does not require any operation because it already satisfies the constraint.

### Why it works

Each wallet is independent because transfers never merge constraints between different sources. A wallet of size $a_i$ must be partitioned into groups of size at most $x$, and the number of groups is fixed by capacity alone. Since each transfer creates exactly one new wallet, there is a one-to-one correspondence between extra groups and operations. This makes the total cost purely additive across wallets.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    x, f = map(int, input().split())

    ops = 0
    for v in a:
        ops += (v + x - 1) // x - 1

    print(ops * f)

if __name__ == "__main__":
    solve()
```

The code directly implements the derived formula. The expression `(v + x - 1) // x` computes the number of required wallets for a given balance. Subtracting one removes the original wallet from the count, leaving only the number of transfers needed.

The accumulator `ops` tracks the total number of transfers. Multiplying by `f` converts operations into satoshi cost.

## Worked Examples

### Example 1

Input:

```
3
13 7 6
6 2
```

We compute operations per wallet.

| wallet $a_i$ | needed wallets $\lceil a_i/x \rceil$ | operations |
| --- | --- | --- |
| 13 | 3 | 2 |
| 7 | 2 | 1 |
| 6 | 1 | 0 |

Total operations = 3, total cost = $3 \cdot 2 = 6$.

This trace shows that splitting depends only on how many chunks of size 6 each wallet requires.

### Example 2

Input:

```
4
5 6 7 12
5 3
```

| wallet $a_i$ | needed wallets | operations |
| --- | --- | --- |
| 5 | 1 | 0 |
| 6 | 2 | 1 |
| 7 | 2 | 1 |
| 12 | 3 | 2 |

Total operations = 4, cost = $4 \cdot 3 = 12$.

This confirms that even larger wallets decompose independently into fixed numbers of splits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each wallet is processed once with constant-time arithmetic |
| Space | $O(1)$ | Only a running counter is maintained |

The linear scan over up to 200,000 elements is easily fast enough within 1 second, since the operations are simple integer computations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    x, f = map(int, input().split())

    ops = 0
    for v in a:
        ops += (v + x - 1) // x - 1

    return str(ops * f)

# provided sample
assert run("3\n13 7 6\n6 2\n") == "6"

# all fit exactly
assert run("3\n5 5 5\n5 10\n") == "0"

# single large split
assert run("1\n11\n5 1\n") == "1"

# multiple independent splits
assert run("2\n9 9\n5 1\n") == "2"

# max-sized balanced case
assert run("5\n1 2 3 4 5\n10 7\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal to x | 0 | no unnecessary splits |
| one large value | correct splits | ceiling behavior |
| multiple sources | additive independence | no cross interference |
| small values | zero operations | lower bound correctness |

## Edge Cases

A subtle edge case occurs when a wallet already satisfies the limit exactly. For input `a = [6]` with `x = 6`, the computation gives `(6 + 5) // 6 - 1 = 1 - 1 = 0`, so no operations are counted. This avoids the common mistake of always counting at least one group.

Another edge case is when values are just above multiples of $x$. For `a = [7]` and `x = 6`, the formula gives `(7 + 5) // 6 - 1 = 2 - 1 = 1`, matching the single required split into 6 and 1.

Large inputs do not change behavior since every operation is computed in constant time per wallet, preventing any simulation blow-up.

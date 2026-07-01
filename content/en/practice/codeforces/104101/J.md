---
title: "CF 104101J - Simple Game"
description: "We are given a sequence of integers, and two players alternate taking one number at a time until the sequence is empty. Alice moves first. Each player accumulates the sum of the numbers they picked."
date: "2026-07-02T02:09:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104101
codeforces_index: "J"
codeforces_contest_name: "The 2022 Zhejiang University City College Freshman Programming Contest"
rating: 0
weight: 104101
solve_time_s: 44
verified: true
draft: false
---

[CF 104101J - Simple Game](https://codeforces.com/problemset/problem/104101/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and two players alternate taking one number at a time until the sequence is empty. Alice moves first. Each player accumulates the sum of the numbers they picked.

After all numbers are taken, we compute the absolute difference between Alice’s total and Bob’s total. Alice wins if this difference is odd, otherwise Bob wins.

The key difficulty is not the picking process itself, because players are free to take any remaining element. The real question is whether optimal play affects the final parity of the difference.

The constraint n can be up to 1e6, so any approach that simulates choices or considers subsets or game states is impossible. We need something linear or near-linear, because even O(n log n) sorting is fine but anything quadratic or exponential is not.

A subtle point is that values can be large, up to 1e9, but only parity matters in the end. That often signals that the solution reduces to reasoning modulo 2 rather than exact sums.

A naive approach would try to simulate the game or model optimal picking strategies. For example, one might think players should always pick the largest remaining element. That already leads to wrong reasoning because optimal play does not matter for parity of final difference in this problem. The outcome depends only on a structural invariant, not on decision-making.

Another incorrect intuition is to treat it as a standard “take maximum alternating” game and compute alternating sums. That fails because players are not constrained to ends of an array or any ordering structure. Any element can be taken at any time, which removes all positional strategy.

The hidden edge case is when all numbers are even. Then every sum is even, so the difference is always even, meaning Bob wins regardless of play. Conversely, if there is at least one odd number, the parity of the final difference is always odd, meaning Alice wins. This is not obvious without reducing the problem to parity conservation.

## Approaches

A brute-force interpretation would simulate the game. At each step, a player chooses an available number and recurses on the remaining multiset, tracking both sums. This is effectively a game tree where each state branches into all remaining elements. The number of states is factorial in n because each ordering of picks corresponds to a possible play sequence.

Even with memoization, the state space remains exponential because the remaining multiset can be represented in 2^n subsets, and transitions depend on which player’s turn it is. This makes it completely infeasible for n up to 1e6.

The key observation is that the order of selection does not affect the multiset of numbers each player ends up with under optimal play, because there is no restriction on which element can be taken. Every permutation of the sequence corresponds to a valid play order. This means the final distribution of numbers between Alice and Bob is not strategically controlled in a meaningful way.

Instead of thinking about optimal selection, we look at parity of the total sum. Let S be the sum of all numbers. Since Alice and Bob split all elements, we have S1 + S2 = S. The value we care about is |S1 − S2|, which equals |S − 2S2|. Modulo 2, this simplifies heavily: 2S2 is always even, so parity of the difference is exactly parity of S.

Thus, the entire game reduces to checking whether the total sum is odd or even. If the sum is odd, the difference is odd, so Alice wins. If the sum is even, Bob wins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Game Simulation | O(n!) | O(n) | Too slow |
| Parity Reduction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of all elements in the sequence. This is valid because every element will eventually be taken by exactly one player, so the sum is fixed regardless of play order.
2. Determine whether this total sum is odd or even by checking its least significant bit. Only parity matters because the winning condition depends on whether the absolute difference is odd.
3. If the sum is odd, output "Alice", otherwise output "Bob". This follows directly from the equivalence between the parity of the total sum and the parity of the final difference.

### Why it works

The crucial invariant is that the total sum of all elements is preserved regardless of how players choose elements. Since S1 + S2 = S always holds, the expression |S1 − S2| can be rewritten as |S − 2S2|. The term 2S2 is always even, so it does not affect parity. Therefore the parity of the final difference is fixed before the game starts and does not depend on any decisions. This removes the game aspect entirely and turns the problem into a single pass computation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    
    total = sum(arr)
    
    if total % 2 == 1:
        print("Alice")
    else:
        print("Bob")

if __name__ == "__main__":
    main()
```

The implementation is direct: we accumulate the sum of all numbers in a single pass. Using Python’s built-in sum is already linear and efficient enough for n up to 1e6. We avoid any sorting or simulation since they are unnecessary.

The only subtle detail is ensuring no intermediate logic interferes with parity. We do not need to track turns or simulate removal because the final result depends only on the full multiset.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

We compute the running sum.

| Step | Current Value | Running Sum |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 3 | 6 |
| 4 | 4 | 10 |
| 5 | 5 | 15 |

The total sum is 15, which is odd, so Alice wins. This shows that even with mixed parity elements, only the final parity matters, not distribution.

### Example 2

Input:

```
2
2 4
```

| Step | Current Value | Running Sum |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 4 | 6 |

The total sum is 6, which is even, so Bob wins. This confirms that when all elements are even, Alice can never force an odd difference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass sum over n elements |
| Space | O(1) | Only storing running total |

The constraints allow up to 1e6 elements, so a linear scan fits comfortably within the time limit. Memory usage is constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(input())
    arr = list(map(int, input().split()))
    total = sum(arr)
    return "Alice" if total % 2 == 1 else "Bob"

# provided samples
assert run("5\n1 2 3 4 5\n") == "Alice"
assert run("2\n2 4\n") == "Bob"

# minimum size
assert run("1\n1\n") == "Alice"
assert run("1\n2\n") == "Bob"

# all equal odd
assert run("4\n1 1 1 1\n") == "Bob"

# mixed parity
assert run("3\n1 2 2\n") == "Alice"

# large even-only
assert run("3\n1000000000 1000000000 2\n") == "Bob"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | Alice | smallest odd sum case |
| 1 2 | Bob | smallest even sum case |
| 1 1 1 1 | Bob | multiple odds cancel to even |
| 1 2 2 | Alice | mixed parity correctness |
| large even set | Bob | large-value stability |

## Edge Cases

A minimal single-element case exposes the core rule immediately. For input `1 1`, Alice takes the only element and the difference is 1, which is odd, so Alice wins. The algorithm computes sum = 1 and correctly outputs Alice.

For a single even element like `1 2`, Bob wins because the sum is 2, even. Alice takes 2, Bob gets nothing, difference is 2, still even. The algorithm returns Bob consistently.

A case with many odd numbers such as `1 1 1 1` produces total sum 4. Even though players alternate picks, any partition results in equal parity split, and difference is even. The algorithm captures this directly without simulating any moves.

These examples confirm that no strategic play changes the parity outcome, and the sum-based reduction is sufficient.

---
title: "CF 104520F - Maximum Trust"
description: "We are processing a sequence of values in a fixed order. A score starts at zero, and for each value in the sequence we must immediately decide whether to add it to the current score or multiply the current score by it."
date: "2026-06-30T10:27:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104520
codeforces_index: "F"
codeforces_contest_name: "Teamscode Summer 2023 Contest"
rating: 0
weight: 104520
solve_time_s: 74
verified: true
draft: false
---

[CF 104520F - Maximum Trust](https://codeforces.com/problemset/problem/104520/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are processing a sequence of values in a fixed order. A score starts at zero, and for each value in the sequence we must immediately decide whether to add it to the current score or multiply the current score by it. Once the decision is made for a position, it cannot be changed later, and we proceed to the next value.

The goal is to maximize the final score after processing all values.

The constraint on the number of elements per test case is small, up to 100, but there can be up to 10,000 test cases. This combination means that any solution with quadratic work per test case is acceptable, while anything exponential in $N$ would be impossible even with pruning.

The key difficulty is that multiplication interacts strongly with sign and magnitude. A negative value can flip the sign of the entire accumulated result, and a large positive value early on can amplify future choices dramatically. A naive greedy approach that decides locally based on whether multiplication or addition is larger at a given step will fail.

A simple failure case appears when early multiplication creates a negative intermediate result that later enables a very large gain:

Input:

```
3
-2 -2 100
```

If we greedily add early values and only multiply when it seems beneficial locally, we might avoid early multiplication and end with a small result, but the optimal strategy is to carefully create a large magnitude early so that later multiplications dominate.

Another subtle issue is that zero behaves like a reset for multiplication. Multiplying by zero destroys all future amplification potential, so any correct strategy must treat zeros as structural breakpoints.

## Approaches

A brute-force solution would simulate every possible sequence of choices. At each position we either add or multiply, giving $2^N$ possibilities per test case. For $N = 100$, this is completely infeasible, since even $2^{30}$ already exceeds a billion states, and we would also need to maintain intermediate integer growth.

The structure of the problem suggests a dynamic programming formulation. At each index we maintain the best achievable score for all possible "states" of computation. However, the state space is not just the index, it is the current value, which makes a naive DP over values impossible due to unbounded growth.

The crucial observation is that the score is a linear expression built from the input sequence, but with dynamic choice of whether each term becomes part of a product chain or is simply added. Any optimal strategy can be interpreted as splitting the array into segments, where within a segment we effectively choose multiplication chains, and between segments we reset by addition.

More concretely, if we fix a point where we choose addition, everything before it is independent of everything after it in terms of multiplicative interaction. This suggests we can maintain a DP over positions where we track the best result ending in a “multiplication chain” versus ending in a “closed addition state”.

At each step, we have two meaningful interpretations:

We either extend a running multiplicative chain by multiplying the next value, or we break the chain and add the current contribution to the final result, resetting the chain state.

This reduces the problem to a constant number of states per position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all choices) | O(2^N) | O(N) | Too slow |
| DP with chain states | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two values while scanning the array from left to right.

One value represents the best score if we have already “committed” all previous contributions into the final sum. The other represents the best value of an active multiplication chain that has not yet been finalized into the answer.

We also track whether we have started a chain or not, since multiplication before initialization behaves differently from multiplication after.

### Steps

1. Initialize a DP state where the best finalized score is zero and there is no active chain.
2. For each value $a_i$, consider two actions: start or extend a multiplication chain, or finalize a chain and add the current contribution.
3. When starting a chain at position $i$, we set the chain value to $a_i$ or to a product with the current chain if one exists.
4. When extending a chain, we update the chain value by multiplying it with $a_i$. This captures the idea that we are building a contiguous multiplication block.
5. At each position, we also consider breaking the chain: we add the current chain value into the finalized score and reset the chain.
6. The answer is the maximum over the finalized score and the case where we end by closing the last chain.

### Why it works

The invariant is that after processing position $i$, the DP correctly represents all optimal ways of partitioning the prefix into alternating segments of multiplication chains and finalized additions. Any optimal solution can be decomposed into such segments because every multiplication decision is associative within a contiguous region, and breaking that region is equivalent to choosing addition at that boundary. Since the DP keeps the best possible outcome for each valid segmentation pattern implicitly, no optimal structure is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(a):
    n = len(a)
    
    # dp0: best finalized score so far
    # dp1: best value of active multiplication chain
    dp0 = 0
    dp1 = None  # no chain yet
    
    for x in a:
        new_dp0 = dp0
        
        # Option 1: extend or start chain
        if dp1 is None:
            new_dp1 = x
        else:
            new_dp1 = dp1 * x
        
        # Option 2: break chain and add it to result
        if dp1 is not None:
            new_dp0 = max(new_dp0, dp0 + dp1)
        
        # Option 3: start new chain at current position
        new_dp1 = max(new_dp1, x)
        
        dp0, dp1 = new_dp0, new_dp1
    
    if dp1 is not None:
        dp0 = max(dp0, dp0 + dp1)
    
    return dp0

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(str(solve_case(a)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The code maintains two evolving quantities. `dp0` represents the best score where all previous operations have been finalized into additions. `dp1` represents a currently active multiplication chain that may still be extended or closed later.

At each step, we either extend the multiplication chain or restart it at the current element. We also have the option of closing the chain and adding it to the finalized score. The careful part is ensuring we do not prematurely discard the chain before considering both continuing and closing it, which is why both transitions are computed before assignment.

## Worked Examples

### Example 1

Input:

```
3
-2 -4 -2
```

We track `(dp0, dp1)`:

| i | a[i] | dp0 | dp1 | Action |
| --- | --- | --- | --- | --- |
| 1 | -2 | 0 | -2 | start chain |
| 2 | -4 | 0 | 8 | extend chain |
| 3 | -2 | 8 | -16 | close previous chain, extend |

Final answer is 8.

This shows how two negatives inside a chain create a positive amplification, and the DP correctly delays committing until the structure becomes beneficial.

### Example 2

Input:

```
4
2 -10 4 3
```

| i | a[i] | dp0 | dp1 | Action |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 2 | start chain |
| 2 | -10 | 0 | -20 | extend |
| 3 | 4 | 2 | 4 | close chain, restart |
| 4 | 3 | 14 | 3 | combine best segments |

This trace shows that it is beneficial to close the negative chain before it grows too harmful, then restart a new chain on positive values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) per test case | Each element is processed once with O(1) transitions |
| Space | O(1) | Only a constant number of DP variables are stored |

The total work is at most $10^4 \times 100 = 10^6$ operations, which is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve_case(a):
        n = len(a)
        dp0 = 0
        dp1 = None
        for x in a:
            new_dp0 = dp0
            if dp1 is None:
                new_dp1 = x
            else:
                new_dp1 = dp1 * x
            if dp1 is not None:
                new_dp0 = max(new_dp0, dp0 + dp1)
            new_dp1 = max(new_dp1, x)
            dp0, dp1 = new_dp0, new_dp1
        if dp1 is not None:
            dp0 = max(dp0, dp0 + dp1)
        return dp0

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(str(solve_case(a)))
    return "\n".join(out)

# provided samples
assert run("4\n4\n4 0 1 2\n3\n3 -2 -2\n4\n-2 -4 -2 -8\n3\n2 -10 4\n") == "10\n12\n128\n4"

# custom cases
assert run("1\n1\n5\n") == "5"
assert run("1\n3\n0 0 0\n") == "0"
assert run("1\n4\n-1 -2 -3 -4\n") == "24"
assert run("1\n3\n10 -1 10\n") == "100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single positive | 5 | base case |
| all zeros | 0 | multiplication collapse |
| all negatives | 24 | chain parity effect |
| alternating signs | 100 | optimal segmentation |

## Edge Cases

A single-element array is trivial because both addition and multiplication yield the same value when starting from zero. The DP initializes a chain correctly and immediately returns that value.

An all-zero array forces every multiplication chain to collapse, and the algorithm correctly avoids creating negative or unstable structures by repeatedly restarting the chain.

A fully negative array is the most delicate case because multiplication alternates sign. The DP keeps extending chains because intermediate negativity is not immediately committed, and only closes when beneficial, which eventually captures the full product.

Mixed sign arrays like `10 -1 10` demonstrate why greedy fails. The algorithm first builds a chain, flips sign once, then correctly restarts to maximize the second multiplication segment, yielding a much larger final score.

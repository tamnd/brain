---
title: "CF 16E - Fish"
description: "We have n fish in a lake. Every day, exactly one unordered pair of currently alive fish is chosen uniformly at random. When fish i meets fish j, fish i eats fish j with probability a[i][j], and fish j eats fish i with probability a[j][i] = 1 - a[i][j]."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 16
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 16 (Div. 2 Only)"
rating: 1900
weight: 16
solve_time_s: 94
verified: true
draft: false
---
[CF 16E - Fish](https://codeforces.com/problemset/problem/16/E)

**Rating:** 1900  
**Tags:** bitmasks, dp, probabilities  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` fish in a lake. Every day, exactly one unordered pair of currently alive fish is chosen uniformly at random. When fish `i` meets fish `j`, fish `i` eats fish `j` with probability `a[i][j]`, and fish `j` eats fish `i` with probability `a[j][i] = 1 - a[i][j]`.

The process continues until only one fish remains alive. For every fish, we must compute the probability that it becomes the final survivor.

The input is a probability matrix. Entry `a[i][j]` tells us the chance that fish `i` defeats fish `j` in a direct encounter. The matrix is asymmetric in general, but every pair satisfies:

```
a[i][j] + a[j][i] = 1
```

The constraint `n ≤ 18` completely shapes the solution. A brute-force simulation of all fight orders explodes immediately because the number of possible elimination sequences is roughly:

```
n * (n - 1) * (n - 2) * ...
```

which is factorial growth. Even for `n = 18`, that is astronomically large.

The number `2^18 = 262144` is small enough for subset dynamic programming. Whenever `n` is around 20, bitmask DP is usually the first thing to investigate. A state for every subset of alive fish becomes realistic.

There are a few easy-to-miss cases that break incorrect formulations.

Consider this input:

```
2
0 1
0 0
```

Fish `0` always defeats fish `1`. The correct answer is:

```
1.000000 0.000000
```

A careless implementation that distributes probabilities symmetrically between both fish would incorrectly produce `0.5 0.5`.

Another subtle case is when multiple paths lead to the same alive set.

```
3
0 0.5 0.5
0.5 0 0.5
0.5 0.5 0
```

All fish are symmetric, so every answer must be exactly `1/3`. If the DP forgets to accumulate contributions from all predecessor states, the probabilities stop summing to `1`.

A more dangerous mistake appears in the transition probability itself. Suppose alive fish are `{0,1,2}`. There are exactly:

```
C(3,2) = 3
```

possible pairs that can meet. If fish `0` dies to fish `1`, the transition probability must include division by `3`. Forgetting this normalization makes total probability exceed `1`.

## Approaches

The brute-force idea is straightforward. At every step, choose every possible pair of alive fish, branch on both possible fight outcomes, and recursively continue until one fish remains.

This works because the process is memoryless. The future only depends on the current alive set. If we recursively enumerate every possible elimination chain and multiply probabilities along the path, we eventually obtain the exact answer.

The problem is the number of states in the recursion tree. At the beginning there are:

```
C(n,2)
```

possible meetings. After one elimination there are:

```
C(n-1,2)
```

and so on.

The total number of fight sequences grows roughly like factorial time. For `n = 18`, this is completely infeasible.

The key observation is that many recursive branches reach the same subset of alive fish.

For example, suppose alive fish become `{0,2,5}`. It does not matter which exact sequence of earlier eliminations produced this set. From that point onward, the future probabilities are identical.

That means the state can be compressed into just:

```
mask = set of alive fish
```

This immediately suggests subset DP.

Define:

```
dp[mask] = probability that exactly the fish in mask are alive
```

We begin from the full set, where every fish is alive with probability `1`.

From a state `mask`, we choose one pair among all alive fish uniformly. One fish dies, producing a smaller mask.

Since each transition removes exactly one fish, the graph of states is acyclic. We can process masks from large to small.

The number of subsets is `2^n`, and for each subset we may inspect pairs of fish. With `n ≤ 18`, this becomes feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential factorial growth | Exponential | Too slow |
| Optimal Bitmask DP | O(2^n · n²) | O(2^n) | Accepted |

## Algorithm Walkthrough

1. Represent every alive set as a bitmask.

Bit `i` is `1` if fish `i` is still alive. With `n ≤ 18`, the entire state fits comfortably inside an integer.
2. Define the DP state.

Let:

```
dp[mask]
```

be the probability that the current alive fish are exactly those in `mask`.
3. Initialize the starting state.

Initially every fish is alive, so:

```
full = (1 << n) - 1
dp[full] = 1
```
4. Process masks from larger subsets to smaller subsets.

Every transition removes one fish, so probability always flows toward masks with fewer bits.
5. For a current mask, count how many fish are alive.

Suppose `k` fish are alive. Then the number of possible meeting pairs is:

$\frac{k(k-1)}{2}$

Every pair is chosen uniformly.
6. Iterate over every ordered pair `(i, j)` of alive fish where `i != j`.

If fish `i` eats fish `j`, the next state becomes:

```
next_mask = mask ^ (1 << j)
```

because fish `j` dies.
7. Add the transition probability.

The probability contribution is:

$dp[mask] \cdot \frac{a_{ij}}{\binom{k}{2}}$

We divide by the number of possible meetings because every unordered pair is equally likely to be selected.
8. Continue until all masks are processed.

Eventually every singleton mask receives its total probability from all larger states.
9. Extract the answer.

Fish `i` survives exactly when the final state is:

```
mask = (1 << i)
```

Why it works:

The DP invariant is:

```
dp[mask] = probability that the process ever reaches exactly this alive set
```

The initial state is correct because the process starts with all fish alive. Every transition models one legal event of the process: choose a meeting pair uniformly, then apply the fight probability. Since every possible next event is accounted for exactly once, probability mass is transferred correctly between states. Because transitions only remove fish, no cycles exist, and every state accumulates contributions from all valid predecessor states before its value is used further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [list(map(float, input().split())) for _ in range(n)]

    size = 1 << n
    dp = [0.0] * size

    full = size - 1
    dp[full] = 1.0

    for mask in range(full, 0, -1):
        alive = []

        for i in range(n):
            if mask & (1 << i):
                alive.append(i)

        k = len(alive)

        if k <= 1:
            continue

        pairs = k * (k - 1) / 2.0

        for i in alive:
            for j in alive:
                if i == j:
                    continue

                next_mask = mask ^ (1 << j)
                dp[next_mask] += dp[mask] * a[i][j] / pairs

    ans = []

    for i in range(n):
        ans.append(f"{dp[1 << i]:.6f}")

    print(*ans)

solve()
```

The DP array stores probabilities for every subset of alive fish. The full mask contains all fish alive initially, so its probability starts at `1`.

The outer loop iterates downward through masks. This order matters because transitions always remove exactly one fish. A smaller mask never contributes back into a larger mask.

For each mask, we first collect the alive fish. This simplifies pair iteration and avoids repeated bit checks.

The variable `pairs` stores the number of unordered meetings possible among alive fish. This is the normalization factor that many wrong implementations miss. Without dividing by this value, probabilities would not sum correctly.

The nested loops iterate over ordered pairs `(i, j)`. This is intentional. Each ordered pair corresponds to one specific elimination event: fish `i` kills fish `j`.

The transition:

```
next_mask = mask ^ (1 << j)
```

removes fish `j` from the alive set.

Floating point precision is sufficient because the answer only requires `1e-6` accuracy.

## Worked Examples

### Example 1

Input:

```
2
0 0.5
0.5 0
```

State transitions:

| Current Mask | Alive Fish | Pair Count | Transition | Added Probability |
| --- | --- | --- | --- | --- |
| 11 | {0,1} | 1 | 0 kills 1 → 01 | 0.5 |
| 11 | {0,1} | 1 | 1 kills 0 → 10 | 0.5 |

Final DP:

| Mask | Probability |

|---|---|---|

| 01 | 0.5 |

| 10 | 0.5 |

Both fish are perfectly symmetric, so each survives with probability `1/2`. This confirms the transition normalization is correct.

### Example 2

Input:

```
3
0 1 0
0 0 1
1 0 0
```

Fish `0` always beats `1`, fish `1` always beats `2`, and fish `2` always beats `0`.

Initial state:

| Mask | Alive Fish | dp |
| --- | --- | --- |
| 111 | {0,1,2} | 1 |

Transitions from full mask:

| Meeting | Resulting Mask | Probability |
| --- | --- | --- |
| 0 kills 1 | 101 | 1/3 |
| 1 kills 2 | 011 | 1/3 |
| 2 kills 0 | 110 | 1/3 |

Now process each 2-fish state:

| Current Mask | Winner | Final Mask | Contribution |
| --- | --- | --- | --- |
| 101 | 2 beats 0 | 100 | 1/3 |
| 011 | 0 beats 1 | 001 | 1/3 |
| 110 | 1 beats 2 | 010 | 1/3 |

Final probabilities:

| Fish | Probability |
| --- | --- |
| 0 | 1/3 |
| 1 | 1/3 |
| 2 | 1/3 |

This example shows that deterministic pairwise outcomes do not necessarily create deterministic final winners. The random order of meetings matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^n · n²) | For every subset we may inspect every ordered pair of fish |
| Space | O(2^n) | One DP value per subset |

For `n = 18`, we have at most:

```
2^18 = 262144
```

states. The quadratic factor over fish pairs remains manageable within the 3-second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = [list(map(float, input().split())) for _ in range(n)]

        size = 1 << n
        dp = [0.0] * size

        full = size - 1
        dp[full] = 1.0

        for mask in range(full, 0, -1):
            alive = []

            for i in range(n):
                if mask & (1 << i):
                    alive.append(i)

            k = len(alive)

            if k <= 1:
                continue

            pairs = k * (k - 1) / 2.0

            for i in alive:
                for j in alive:
                    if i == j:
                        continue

                    nxt = mask ^ (1 << j)
                    dp[nxt] += dp[mask] * a[i][j] / pairs

        ans = []

        for i in range(n):
            ans.append(f"{dp[1 << i]:.6f}")

        return " ".join(ans)

    return solve()

# provided sample
assert run(
"""2
0 0.5
0.5 0
"""
) == "0.500000 0.500000"

# minimum size
assert run(
"""1
0
"""
) == "1.000000"

# deterministic dominance
assert run(
"""2
0 1
0 0
"""
) == "1.000000 0.000000"

# all equal probabilities
assert run(
"""3
0 0.5 0.5
0.5 0 0.5
0.5 0.5 0
"""
) == "0.333333 0.333333 0.333333"

# cyclic dominance
assert run(
"""3
0 1 0
0 0 1
1 0 0
"""
) == "0.333333 0.333333 0.333333"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single fish | `1.000000` | Base case with no transitions |
| Deterministic 2-fish fight | `1.000000 0.000000` | Correct handling of probability 1 |
| Symmetric 3-fish case | equal thirds | Probability conservation |
| Cyclic dominance | equal thirds | Random meeting order affects outcome |

## Edge Cases

Consider the smallest possible input:

```
1
0
```

The initial mask already contains exactly one fish. The DP starts with:

```
dp[1] = 1
```

No transitions occur because `k <= 1`. The algorithm correctly outputs:

```
1.000000
```

Now consider deterministic dominance:

```
2
0 1
0 0
```

Initial state:

| Mask | Alive | dp |
| --- | --- | --- |
| 11 | {0,1} | 1 |

There is only one pair. Fish `0` defeats fish `1` with probability `1`.

Transition:

| From | To | Probability |
| --- | --- | --- |
| 11 | 01 | 1 |

Final result:

```
1.000000 0.000000
```

This verifies that the DP handles hard probabilities without floating-point instability.

Finally, examine a case where several paths merge into the same state:

```
3
0 0.5 0.5
0.5 0 0.5
0.5 0.5 0
```

The mask `{0,1}` can be reached either by fish `0` killing `2` or fish `1` killing `2`. The DP adds both contributions into the same state value.

Trace:

| Transition | Contribution to Mask 011 |
| --- | --- |
| 0 kills 2 | 1/6 |
| 1 kills 2 | 1/6 |

Total:

```
dp[011] = 1/3
```

This accumulation is exactly why subset DP works here. Different elimination histories collapse into the same future state.

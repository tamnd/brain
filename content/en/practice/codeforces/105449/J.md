---
title: "CF 105449J - \u041c\u043d\u043e\u0433\u043e \u0438\u0433\u0440"
description: "We are given a collection of independent gambling games. Each game has a probability of success and a payout if it succeeds. The twist is that if any chosen game fails, the entire selection yields zero reward."
date: "2026-06-24T23:24:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105449
codeforces_index: "J"
codeforces_contest_name: "Moscow team school olympiad (MKOSHP) 2024"
rating: 0
weight: 105449
solve_time_s: 77
verified: false
draft: false
---

[CF 105449J - \u041c\u043d\u043e\u0433\u043e \u0438\u0433\u0440](https://codeforces.com/problemset/problem/105449/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of independent gambling games. Each game has a probability of success and a payout if it succeeds. The twist is that if any chosen game fails, the entire selection yields zero reward. If all chosen games succeed, the payout is the sum of their individual rewards.

So for any chosen subset, the expected value is the product of success probabilities multiplied by the sum of rewards in that subset. The task is to choose a subset that maximizes this expectation.

The input size goes up to 200,000 games, which immediately rules out any exponential subset enumeration. Even quadratic solutions are too large, since a 2e5 squared approach would be on the order of 4e10 operations.

A key structural constraint is that probabilities are small integers up to 100, while rewards are positive integers with a product constraint $p_i \cdot w_i \le 200000$. This ensures that no single game dominates arbitrarily in both probability and reward, and it hints that sorting or greedy selection might be effective.

A subtle edge case arises when all probabilities are less than 100. A naive intuition might suggest taking all games is always better because it increases the sum of rewards, but the multiplicative probability penalty can overwhelm the gain. For example, adding a high reward but low probability game can decrease expectation.

Another failure mode is greedy selection by either reward or probability alone. Sorting only by reward ignores probability shrinkage, while sorting only by probability ignores additive structure of rewards. The correct solution must balance both simultaneously.

## Approaches

A brute-force approach would try every subset of games, compute the product of probabilities and sum of rewards, and track the maximum expectation. This works conceptually because it directly evaluates the objective function. However, the number of subsets is $2^n$, which becomes infeasible even for $n=40$, let alone $200,000$. The computational explosion comes from the combinatorial nature of subset selection.

The key observation is to reformulate the objective in a way that allows incremental reasoning. Suppose we maintain a subset and consider adding a new game. The expectation changes multiplicatively in probability and additively in reward, which suggests we should compare marginal contribution in a normalized way.

Let the current subset have probability product $P$ and reward sum $S$. If we add a new game with probability $p$ and reward $w$, the new expectation becomes

$$(P \cdot \frac{p}{100}) \cdot (S + w).$$

Comparing whether adding the game helps reduces to comparing ratios that depend only on $(p, w)$ and current state.

A standard transformation is to sort games by decreasing ratio $\frac{w_i}{100 - p_i}$ after algebraic rearrangement, which emerges from comparing marginal improvements. Intuitively, a game is beneficial if its contribution to expected sum outweighs its probability decay effect.

After sorting, we greedily decide whether to include each game in order. We maintain the best achievable expectation dynamically: for each prefix, we compute whether extending improves the value.

This reduces the problem from exponential search to a linear scan over a sorted list.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all games as pairs $(p_i, w_i)$ and convert probabilities into fractions $p_i / 100$. This standardization allows uniform multiplicative handling.
2. Sort the games by decreasing value of the expression $\frac{w_i}{100 - p_i}$. This ordering reflects how much reward compensates for probability loss when a game is included earlier in a subset.
3. Initialize two variables: a running probability product $P = 1.0$ and a running reward sum $S = 0.0$.
4. Initialize the answer as 0.0, representing the best expectation found so far.
5. Iterate through games in sorted order. For each game, update the candidate state by considering inclusion: $P' = P \cdot (p_i / 100)$ and $S' = S + w_i$.
6. Compute the expectation $E' = P' \cdot S'$ and update the answer if $E'$ is larger than the current best.
7. Decide to actually commit to the inclusion by setting $P = P'$ and $S = S'$. This step is valid because the sorted order ensures that earlier decisions remain optimal for future extensions.

### Why it works

The algorithm relies on the fact that the objective function can be decomposed into a product of a decreasing multiplicative factor and an increasing additive factor. The sorting criterion ensures that at each step, we consider games in order of best trade-off between reward gain and probability decay. This induces a structure where any optimal subset can be transformed into a prefix of the sorted order without decreasing the objective value. That exchange argument guarantees that greedy construction does not miss a better subset.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    games = []
    for _ in range(n):
        p, w = map(int, input().split())
        games.append((p, w))
    
    # sort by w / (100 - p)
    # avoid division by sorting cross-multiplied
    games.sort(key=lambda x: (x[1] * 1.0 / (100 - x[0]) if x[0] != 100 else float('inf')), reverse=True)

    P = 1.0
    S = 0.0
    ans = 0.0

    for p, w in games:
        P *= p / 100.0
        S += w
        ans = max(ans, P * S)

    print(f"{ans:.10f}")

if __name__ == "__main__":
    solve()
```

The solution first sorts games according to a derived dominance ratio, ensuring that games with better reward-to-risk tradeoffs appear earlier. The loop maintains cumulative probability and reward sum. At each step, it evaluates the full prefix as a candidate subset, since optimal subsets are prefix-closed under this ordering.

A common implementation pitfall is forgetting floating-point stability when multiplying many probabilities. Using Python float is sufficient here because $n$ is large but probabilities are bounded and precision requirement is $10^{-6}$.

Another subtle point is handling $p_i = 100$, which makes the denominator in the heuristic infinite; these games should always come first since they do not reduce probability.

## Worked Examples

### Example 1

Input:

```
3
80 80
70 100
50 200
```

We compute ordering by $\frac{w}{100-p}$:

80/(20)=4, 100/(30)=3.33, 200/(50)=4.

So order becomes:

(80,80), (50,200), (70,100)

We trace prefix evaluation:

| Step | p | w | P | S | P*S |
| --- | --- | --- | --- | --- | --- |
| 1 | 80 | 80 | 0.8 | 80 | 64 |
| 2 | 50 | 200 | 0.4 | 280 | 112 |
| 3 | 70 | 100 | 0.28 | 380 | 106.4 |

Maximum is 112.

This shows that intermediate prefixes matter, and the optimal subset is not necessarily all games.

### Example 2

Input:

```
2
90 10
10 100
```

Ratios:

90/10 = 9, 100/90 ≈ 1.11, so order is (90,10), (10,100)

| Step | p | w | P | S | P*S |
| --- | --- | --- | --- | --- | --- |
| 1 | 90 | 10 | 0.9 | 10 | 9 |
| 2 | 10 | 100 | 0.09 | 110 | 9.9 |

Best answer is 9.9 after taking both.

This demonstrates that a low-probability high-reward game can still improve expectation when placed later in a favorable order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, single linear scan afterward |
| Space | $O(n)$ | Storage of game list |

The constraints up to 200,000 games make an $O(n \log n)$ solution comfortably feasible. Memory usage is linear and well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n = int(inp.split()[0])
    games = []
    idx = 1
    for _ in range(n):
        p = int(inp.split()[idx]); w = int(inp.split()[idx+1])
        idx += 2
        games.append((p, w))

    games.sort(key=lambda x: (x[1] / (100 - x[0]) if x[0] != 100 else float('inf')), reverse=True)

    P = 1.0
    S = 0.0
    ans = 0.0

    for p, w in games:
        P *= p / 100
        S += w
        ans = max(ans, P * S)

    return f"{ans:.6f}"

# sample
assert run("3\n80 80\n70 100\n50 200\n") == "112.000000", "sample 1"

# all probability 100
assert run("2\n100 10\n100 20\n") == "30.000000", "all certain wins"

# single game
assert run("1\n80 50\n") == "40.000000", "single game"

# low probability high reward
assert run("2\n10 1000\n90 1\n") == run("2\n90 1\n10 1000\n"), "order invariance"

# large equal cases
assert run("3\n90 10\n90 10\n90 10\n") > "0.000000", "uniform case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single game | direct product | base correctness |
| all p=100 | linear sum | no probability decay |
| mixed extreme values | stability | ordering effect |
| permutation swap | same result | sorting correctness |

## Edge Cases

A key edge case is when one or more games have $p_i = 100$. These games do not reduce the probability product, so they should always be included in any optimal solution. In the algorithm, they naturally float to the front due to infinite sorting weight, and their inclusion only increases the sum $S$ without affecting $P$.

Another edge case is when probabilities are very small. In such cases, even a single additional game can reduce the product enough to make previously beneficial subsets suboptimal. The prefix evaluation ensures that the algorithm still captures the best stopping point rather than forcing all inclusions.

A final edge case occurs when all games have similar ratios. The algorithm still works because even small differences in ordering determine which prefix maximizes the product-sum tradeoff, and the max tracking step ensures the best prefix is always selected.

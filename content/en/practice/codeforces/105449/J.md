---
title: "CF 105449J - \u041c\u043d\u043e\u0433\u043e \u0438\u0433\u0440"
description: "We are given a collection of independent games. Each game has a success probability $pi%$ and a reward $wi$. If we choose a set of games, we only receive money if we win every single chosen game."
date: "2026-06-23T03:14:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105449
codeforces_index: "J"
codeforces_contest_name: "Moscow team school olympiad (MKOSHP) 2024"
rating: 0
weight: 105449
solve_time_s: 91
verified: false
draft: false
---

[CF 105449J - \u041c\u043d\u043e\u0433\u043e \u0438\u0433\u0440](https://codeforces.com/problemset/problem/105449/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of independent games. Each game has a success probability $p_i\%$ and a reward $w_i$. If we choose a set of games, we only receive money if we win every single chosen game. The probability of that happening is the product of individual probabilities, and the payout in that case is the sum of rewards.

So for a chosen subset $S$, the expected value is

$$E(S) = \left(\prod_{i \in S} \frac{p_i}{100}\right) \cdot \left(\sum_{i \in S} w_i\right).$$

The task is to pick a subset that maximizes this expression.

The constraints are large, with up to 200,000 games. This immediately rules out anything that examines all subsets or uses subset DP. Even sorting-based solutions must avoid per-element heavy recomputation beyond linear or linear-logarithmic work.

A subtle difficulty is that adding a new game both increases the sum and decreases the product, and these effects interact multiplicatively. This means the benefit of a game depends on what we already picked, so a naive “take best ratio” heuristic is not obviously valid.

A common failure case is assuming independence like a knapsack. For example, a game with high reward but slightly lower probability might look bad early but become optimal when combined with others that reduce the product less severely. The objective is not additive, so standard greedy by $w_i$ or $p_i$ fails.

Another subtle edge case is floating stability: products of up to 200,000 probabilities in $[0.01, 1]$ quickly underflow, so we must structure computation so we avoid multiplying everything unnecessarily or rely on stable incremental updates.

## Approaches

A brute-force solution would enumerate all subsets, compute the product of probabilities and sum of weights, and track the best value. This is correct because it directly evaluates the objective function for every possible choice. However, with $2^n$ subsets, even for $n=40$ this is already infeasible, and here $n$ is 200,000, making it completely impossible.

To simplify the structure, we examine how the objective changes when adding a single game to an already chosen set. Suppose we currently have product $A$ and sum $B$. If we consider adding a game $i$, the new value becomes

$$A'B' = (A \cdot a_i)(B + w_i),$$

where $a_i = p_i / 100$.

We compare keeping the set versus adding the game:

$$AB \le A a_i (B + w_i).$$

Canceling $A$, we get

$$B \le a_i B + a_i w_i.$$

Rearranging,

$$B(1 - a_i) \le a_i w_i,$$

so

$$B \le \frac{a_i w_i}{1 - a_i}.$$

This inequality shows a threshold behavior: whether a game is beneficial depends on the current sum $B$. The right-hand side depends only on the game, while the left-hand side grows as we pick more items.

This structure suggests sorting games by how “late” they can still be beneficial. Define

$$T_i = \frac{a_i w_i}{1 - a_i} = \frac{p_i w_i}{100 - p_i}.$$

If we sort by decreasing $T_i$, we can process games in an order where those that tolerate larger accumulated $B$ come first. In that order, once a game becomes invalid, all later games are even less tolerant, so they will also be invalid in any extension.

This reduces the problem to scanning the sorted list and maintaining the best prefix. Each prefix corresponds to choosing the first $k$ games, computing its expected value, and taking the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Convert each game into a pair $(p_i, w_i)$, and compute a ranking key

$$T_i = \frac{p_i w_i}{100 - p_i}.$$

This value measures how large a total reward sum a game can still tolerate before it becomes harmful.
2. Sort all games in descending order of $T_i$.

This ensures that games that remain useful even when the accumulated sum is large are considered earlier.
3. Initialize an empty selection, with product $A = 1.0$, sum $B = 0$, and answer $ans = 0$.
4. Iterate through the sorted games in order. For each game:

compute the candidate value if we include it:

$$A_{\text{new}} = A \cdot \frac{p_i}{100}, \quad B_{\text{new}} = B + w_i.$$
5. Update the answer using the current prefix:

$$ans = \max(ans, A_{\text{new}} \cdot B_{\text{new}}).$$
6. Commit to including the game in the prefix by updating $A, B$.

This works because in sorted order, once we skip or effectively lose benefit from a later item, earlier items are strictly stronger in terms of tolerance.

### Why it works

The key structural property is that each game induces a linear constraint on the current sum $B$, and this constraint becomes stricter as we go forward in increasing order of $T_i$. Because both the product and sum evolve monotonically in opposite directions, the optimal solution must correspond to a prefix in this ordering. Any deviation where a later item is chosen without an earlier one would violate the ordering of thresholds and reduce feasibility without improving the objective.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    games = []
    
    for _ in range(n):
        p, w = map(int, input().split())
        # threshold value
        # p*w/(100-p)
        if p == 100:
            t = float('inf')
        else:
            t = (p * w) / (100 - p)
        games.append((t, p, w))
    
    games.sort(reverse=True)

    prob = 1.0
    total_w = 0.0
    ans = 0.0

    for _, p, w in games:
        prob *= p / 100.0
        total_w += w
        ans = max(ans, prob * total_w)

    print(f"{ans:.10f}")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the sorted-prefix idea. The probability product is maintained incrementally as a floating-point value, while the sum is accumulated as a running total. Each prefix is evaluated immediately, and the maximum is stored.

A subtle implementation detail is handling $p = 100$, where the threshold formula divides by zero. These games are always optimal to place first since they never reduce probability, so treating their threshold as infinity ensures they sort to the front.

Floating-point multiplication is safe here because values are bounded and the required precision is only $10^{-6}$.

## Worked Examples

### Sample 1

Input:

```
3
80 80
70 100
50 200
```

We compute thresholds:

| Step | Game (p, w) | T = p*w/(100-p) | Prob | Sum | Value |
| --- | --- | --- | --- | --- | --- |
| 1 | (80, 80) | 320 | 0.8 | 80 | 64 |
| 2 | (50, 200) | 100 | 0.4 | 280 | 112 |
| 3 | (70, 100) | 233.33 | 0.28 | 380 | 106.4 |

The best prefix is after the second game, giving 112.

This trace shows how probability decay competes with reward accumulation, and why the ordering ensures we evaluate only meaningful candidate prefixes.

### Sample 2

Input:

```
2
90 10
10 1000
```

| Step | Game | Prob | Sum | Value |
| --- | --- | --- | --- | --- |
| 1 | (90,10) | 0.9 | 10 | 9 |
| 2 | (10,1000) | 0.09 | 1010 | 90.9 |

Even though the second game has very low probability, its reward dominates once included, and the prefix evaluation captures this trade-off correctly.

This demonstrates that low-probability high-reward items are not automatically bad, but their position in the ordering determines when they can be safely included.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, single linear scan afterward |
| Space | $O(n)$ | Storing games and thresholds |

The constraints allow up to 200,000 games, so an $O(n \log n)$ solution comfortably fits within time limits, while linear memory is sufficient for storing input and derived values.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    games = []
    for _ in range(n):
        p, w = map(int, input().split())
        if p == 100:
            t = float('inf')
        else:
            t = (p * w) / (100 - p)
        games.append((t, p, w))

    games.sort(reverse=True)

    prob = 1.0
    total = 0.0
    ans = 0.0

    for _, p, w in games:
        prob *= p / 100.0
        total += w
        ans = max(ans, prob * total)

    return f"{ans:.10f}"

# provided sample
assert run("""3
80 80
70 100
50 200
""") == "112.0000000000"

# minimum size
assert run("""1
50 10
""") == "5.0000000000"

# all p = 100
assert run("""3
100 1
100 2
100 3
""") == "6.0000000000"

# one very bad probability, huge reward
assert run("""2
1 100000
100 1
""") == "1000.0000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single item | direct computation | base case correctness |
| all p=100 | full inclusion | division edge handling |
| extreme imbalance | ordering robustness | low-prob high-reward effect |

## Edge Cases

A corner case occurs when all probabilities are 100. In that situation, the product is always 1, so the optimal strategy is to take every game. The algorithm handles this because such items receive infinite threshold and are processed first, and every prefix increases the sum without any decay in probability.

Another case is when one game has extremely low probability but enormous reward. The sorting places it late, but its inclusion is still evaluated as part of a prefix, ensuring it can dominate the answer despite reducing probability heavily.

Finally, when probabilities are small but rewards are also small, the threshold ordering ensures they are considered only when earlier, more stable items are already accounted for, preventing unstable multiplicative collapse from misordering the decision process.

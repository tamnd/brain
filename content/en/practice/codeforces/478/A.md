---
title: "CF 478A - Initial Bet"
description: "We are given the final state of a system with five participants who started a game under a very rigid rule: everyone begins with the same unknown positive number of coins, call it $b$. After this initialization, coins are only moved between players."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 478
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 273 (Div. 2)"
rating: 1100
weight: 478
solve_time_s: 59
verified: true
draft: false
---

[CF 478A - Initial Bet](https://codeforces.com/problemset/problem/478/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the final state of a system with five participants who started a game under a very rigid rule: everyone begins with the same unknown positive number of coins, call it $b$. After this initialization, coins are only moved between players. No coins are created or destroyed during the process; every operation simply transfers one coin from one person to another.

At the end, we observe how many coins each of the five players has. From this final distribution, we need to determine whether it is possible that all players originally had the same positive number of coins, and if so, recover that initial value $b$. If there is no way to explain the final state under those rules, we must report that it is impossible.

The key structural constraint is conservation of total coins. Since transfers do not change the total number of coins, the sum of final values must equal the sum of initial values, which is $5b$. This immediately implies that the total sum of the final array must be divisible by 5, and the quotient would be the candidate value of $b$.

The constraints are extremely small: each final count is at most 100 and there are only five values. This removes any need for sophisticated data structures or optimizations. A direct computation is sufficient.

The main subtlety lies in distinguishing valid redistribution from invalid ones. For example, a state like $1, 1, 1, 1, 1$ is valid with $b = 1$. A state like $2, 2, 2, 2, 2$ is valid with $b = 2$. But a state like $1, 1, 1, 1, 2$ has total sum 6, which is not divisible by 5, and therefore cannot come from equal starting values regardless of transfers.

A more misleading case is one where the sum is divisible by 5 but negative reasoning might suggest impossibility. For example, $0, 0, 0, 0, 5$ has sum 5, so $b = 1$. This is valid: one player can end up donating all coins. Any approach that tries to reason about individual feasibility without using total conservation risks overcomplicating what is fundamentally a single arithmetic condition.

## Approaches

A brute-force idea would be to try all possible initial values $b$ from 1 up to 100 and simulate whether we can redistribute coins from an initial state of five equal piles to reach the target configuration. While this is conceptually straightforward, it hides a difficult subproblem: determining reachability under arbitrary transfers. Since coins can be moved freely between any two players, the state space is large, but we are not constrained by graph structure or move limits. Simulation would therefore require reconstructing a sequence of transfers, which is unnecessary.

The key simplification is recognizing that transfers preserve total sum exactly. This collapses the problem from a dynamic reachability question into a static arithmetic condition. The final configuration is valid if and only if its total sum equals $5b$, where $b$ must be a positive integer.

Thus the entire problem reduces to computing the sum and checking divisibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(states or undefined) | O(1) | Overkill / unnecessary |
| Sum and Divisibility Check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the five integers representing final coin counts of each player.
2. Compute their total sum. This sum represents the total number of coins in the system, which never changes throughout the game.
3. Check whether the sum is divisible by 5. If it is not, no equal initial distribution is possible, because $5b$ must equal the total.
4. If divisible, compute $b = \frac{\text{sum}}{5}$.
5. Ensure $b > 0$. If the sum is zero, all players ended with zero coins, which contradicts the requirement that initial bets are strictly positive.
6. Output $b$ if valid, otherwise output -1.

### Why it works

The invariant is total coin conservation. Every operation in the game is a unit transfer between players, which preserves the sum of all coins. Therefore the final sum must equal the initial sum exactly. Since the initial configuration is five identical values $b$, the total must be $5b$. This uniquely determines $b$ whenever a solution exists, and any violation of divisibility or positivity rules immediately proves impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    c = list(map(int, input().split()))
    total = sum(c)

    if total % 5 != 0:
        print(-1)
        return

    b = total // 5

    if b <= 0:
        print(-1)
        return

    print(b)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the invariant-based reasoning. The only computation is the sum of the five values. The divisibility check ensures consistency with the model of equal initial distribution. The positivity check is necessary because the problem explicitly requires a positive initial bet, not zero.

A common mistake is to skip the positivity condition. Without it, an input like `0 0 0 0 0` would incorrectly yield $b = 0$, even though the rules forbid zero initial bets.

## Worked Examples

### Example 1

Input:

```
2 5 4 0 4
```

Total sum is 15, so candidate $b = 3$.

| Step | Sum | Divisible by 5 | b | Valid |
| --- | --- | --- | --- | --- |
| Initial | 15 | yes | 3 | yes |

Output is 3.

This confirms a consistent redistribution exists since total coins match 5 equal initial piles.

### Example 2

Input:

```
1 1 1 1 2
```

Total sum is 6, which is not divisible by 5.

| Step | Sum | Divisible by 5 | b | Valid |
| --- | --- | --- | --- | --- |
| Initial | 6 | no | - | no |

Output is -1.

This demonstrates that even though values look "close" to uniform, conservation of total mass immediately rules it out.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only five integers are processed once |
| Space | O(1) | No auxiliary data structures beyond a few variables |

The constraints are so small that even repeated evaluation would be trivial, but the constant-time solution directly matches the invariant structure of the problem.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided sample
assert run("2 5 4 0 4\n") == "3", "sample 1"

# all equal minimal valid
assert run("1 1 1 1 1\n") == "1", "all equal"

# impossible due to sum
assert run("1 1 1 1 2\n") == "-1", "sum not divisible"

# all zeros (invalid because b must be positive)
assert run("0 0 0 0 0\n") == "-1", "zero case"

# boundary-ish valid
assert run("0 0 0 0 5\n") == "1", "single pile concentration"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 5 4 0 4 | 3 | standard valid case |
| 1 1 1 1 2 | -1 | non-divisible sum |
| 0 0 0 0 0 | -1 | positivity constraint |
| 0 0 0 0 5 | 1 | extreme redistribution |

## Edge Cases

A subtle edge case is when all players end with zero coins. The sum is zero, which is divisible by 5, but it implies $b = 0$. Since the problem requires a strictly positive initial bet, this must be rejected. The algorithm handles this by explicitly checking $b > 0$, ensuring that zero does not pass through as a valid solution.

Another case is a highly skewed distribution like `0 0 0 0 5`. Here the sum is 5, giving $b = 1$. The invariant guarantees validity because the five initial coins can all be transferred to a single player over time, so the algorithm correctly accepts it.

Finally, any input where the sum is not divisible by 5 is rejected immediately, which covers a large fraction of invalid states without further reasoning.

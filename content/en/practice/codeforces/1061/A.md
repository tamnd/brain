---
title: "CF 1061A - Coins"
description: "We are given a collection of coin denominations that includes every integer value from 1 up to n, and we are allowed to use any number of coins of any of these values."
date: "2026-06-15T08:50:45+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1061
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 523 (Div. 2)"
rating: 800
weight: 1061
solve_time_s: 118
verified: true
draft: false
---

[CF 1061A - Coins](https://codeforces.com/problemset/problem/1061/A)

**Rating:** 800  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of coin denominations that includes every integer value from 1 up to n, and we are allowed to use any number of coins of any of these values. The task is to represent a target sum S using as few coins as possible, where repetition of the same coin value is allowed without restriction.

This is essentially a resource minimization problem: we want to decompose S into a multiset of integers in the range [1, n], minimizing the size of that multiset. Each coin contributes its value to the total, and we want to reach exactly S without exceeding it.

The constraints matter strongly here. The value of n can be as large as 100000, while S can be as large as 1e9. This immediately rules out any approach that attempts to simulate combinations or dynamic programming over S, since any state space depending on S would be far too large. Even O(S) solutions are impossible. We are forced into a solution that computes the answer in constant time or logarithmic time per test case, relying on structure rather than enumeration.

A naive but common mistake is to assume that using the largest coin greedily always works by repeatedly taking min(n, S) until S becomes zero. This fails in a subtle way when the remainder after taking large coins is small but cannot be efficiently expressed without increasing the total number of coins. Another incorrect intuition is to treat it as a knapsack problem and try to optimize composition directly; this also fails due to the scale of S.

## Approaches

The brute-force idea is straightforward: try every possible multiset of coins whose values are in [1, n] and whose sum is S, and compute the minimum cardinality. This is correct in principle because it explores all valid decompositions. However, the number of such multisets grows extremely quickly with S. Even restricting to bounded coin values, the number of partitions of an integer is exponential in the square root of S in general settings, making this approach infeasible long before reaching the given constraints.

The key observation is that the structure of the coin set makes the problem behave like a constrained version of integer partitioning where large values are always preferable. If we use k coins, the best possible sum we can achieve with k coins is obtained by taking k copies of n, giving k·n. This means any solution using k coins can only cover sums up to k·n. Conversely, if we want to reach S, we need at least enough coins so that their maximum achievable sum reaches S.

This immediately suggests a lower bound of ceil(S / n). The deeper question is whether this bound is always achievable. It turns out it is, because we can always express any remainder using smaller coin values: once we take as many n coins as possible, the leftover is strictly less than n, and that remainder can always be represented using a single coin (or at most one additional coin in combination adjustments, but the structure guarantees feasibility). This makes the lower bound tight.

So the optimal strategy reduces to a simple division argument: use as many n-valued coins as possible, and if there is a remainder, it can be covered with one additional coin.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

The solution relies on comparing the target sum S against the maximum contribution of coins of size n.

1. Compute how many full n-sized coins fit into S. This is S divided by n using integer division. This represents the maximum number of large coins we can use without exceeding S.
2. Compute the remainder after taking those n-sized coins. This is S modulo n. The remainder represents the leftover amount that cannot be covered by full n coins.
3. If the remainder is zero, the answer is exactly the number of full coins, since S is perfectly divisible by n.
4. If the remainder is non-zero, we need one additional coin to cover the leftover part. This is because any value from 1 to n is available, so any remainder strictly less than n can always be formed using one coin.

The reasoning hinges on the fact that coin value 1 always exists, so any leftover can always be represented without increasing complexity further.

### Why it works

The key invariant is that after taking floor(S / n) coins of value n, the remaining value is strictly less than n and therefore always representable using the available coin set. Since we always prefer larger coins to minimize count, any optimal solution must use as many n coins as possible; replacing an n coin with smaller coins never reduces the number of coins needed. This ensures that the greedy decomposition into n-sized chunks plus a remainder is optimal and cannot be improved.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, s = map(int, input().split())
    ans = s // n
    if s % n != 0:
        ans += 1
    print(ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the division-based reasoning. The integer division computes how many full n-coins fit into S. The conditional increment handles any leftover remainder that requires one additional coin.

A subtle point is that we do not need to construct the actual coin set. The problem only asks for the minimum number of coins, not the composition, so arithmetic suffices.

## Worked Examples

### Example 1

Input: n = 5, S = 11

| Step | Full coins (S//n) | Remainder (S%n) | Answer |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 3 |

We can take two coins of value 5, giving 10. The remaining 1 requires one more coin. This confirms that 3 coins are sufficient.

### Example 2

Input: n = 6, S = 16

| Step | Full coins (S//n) | Remainder (S%n) | Answer |
| --- | --- | --- | --- |
| 1 | 2 | 4 | 3 |

Two coins of value 6 give 12, leaving 4. One additional coin covers the remainder.

These traces show that the algorithm is effectively decomposing S into maximal chunks of size n and handling the leftover independently, confirming the correctness of the ceiling division behavior.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations are performed regardless of input size |
| Space | O(1) | No auxiliary data structures are used |

The solution easily satisfies the constraints since it performs a constant number of integer operations even when S is as large as 1e9.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, s = map(int, input().split())
    ans = s // n
    if s % n != 0:
        ans += 1
    return str(ans)

# provided samples
assert run("5 11\n") == "3", "sample 1"
assert run("6 16\n") == "3", "sample 2"

# custom cases
assert run("1 1000000000\n") == "1000000000", "only coin 1 available"
assert run("10 10\n") == "1", "exact division"
assert run("10 1\n") == "1", "small remainder"
assert run("7 49\n") == "7", "large exact multiple"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1000000000 | 1000000000 | extreme case where only unit coins matter |
| 10 10 | 1 | exact divisibility |
| 10 1 | 1 | smallest remainder case |
| 7 49 | 7 | larger exact multiple consistency |

## Edge Cases

One edge case is when S is smaller than n. In this situation, S // n becomes zero and S % n equals S. The algorithm correctly returns 1, since any value up to n can be represented by a single coin. For example, with n = 10 and S = 7, we take zero full coins and one coin of value 7.

Another edge case is when S is exactly divisible by n. For example, n = 4 and S = 12 gives S // n = 3 and remainder 0, so no extra coin is added. This reflects the optimal strategy of using only maximum-value coins.

A final edge case is when n = 1. Here every coin is 1, so the only way to form S is using S coins. The formula gives S // 1 = S and remainder 0, matching the correct answer exactly.

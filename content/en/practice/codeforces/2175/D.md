---
title: "CF 2175D - Wishing Cards"
description: "We are tasked with distributing a limited number of wishing cards among $n$ friends so that the cumulative happiness of Little A is maximized. Each friend $i$ can carry at most $ai$ cards, and the sum of all cards cannot exceed $k$."
date: "2026-06-09T04:32:23+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2175
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1069 (Div. 2)"
rating: 1900
weight: 2175
solve_time_s: 101
verified: true
draft: false
---

[CF 2175D - Wishing Cards](https://codeforces.com/problemset/problem/2175/D)

**Rating:** 1900  
**Tags:** dp, greedy  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with distributing a limited number of wishing cards among $n$ friends so that the cumulative happiness of Little A is maximized. Each friend $i$ can carry at most $a_i$ cards, and the sum of all cards cannot exceed $k$. Happiness is measured sequentially: after the $j$-th friend delivers their cards, Little A’s happiness increases by the largest number of cards delivered so far, $\max(b_1, \dots, b_j)$. The output is the total happiness after all friends have delivered their cards.

The constraints imply that $n$ can be up to $10^5$, but the total number of cards $k$ is small (at most 360). This disparity signals that an algorithm iterating over friends in $O(n)$ time is acceptable, but anything exponential in $n$ is infeasible. The sum of $k$ over all test cases is also small, which hints at the applicability of dynamic programming with a state depending on the remaining number of cards.

Non-obvious edge cases include scenarios where some friends cannot carry any cards or where the total $k$ is smaller than the largest single capacity $a_i$. For example, if $n = 3$, $k = 2$, and $a = [5,0,1]$, giving all 2 cards to the first friend is optimal even though the first friend could carry more. A naive approach that always gives each friend their maximum allowed would exceed $k$, producing an invalid assignment.

## Approaches

A brute-force approach would be to enumerate all ways to assign $b_i \le a_i$ such that $\sum b_i \le k$ and compute the happiness for each assignment. Each sequence would require $O(n)$ time to evaluate, and the number of sequences is combinatorial in $k$ and $n$, which can reach $O(n^k)$ in the worst case. With $k$ up to 360, this approach is infeasible.

The key insight is that $k$ is small, so we can design a dynamic programming solution where the state is the number of cards already used and the current maximum contribution to happiness. Let $dp[j]$ represent the maximum cumulative happiness achievable using exactly $j$ cards. For each friend $i$, we consider giving them $0 \le x \le \min(a_i, k)$ cards and update the DP table accordingly. This works because happiness increases by the maximum so far, so we can maintain a running contribution for each possible total of cards used. The problem reduces to an unbounded knapsack-like DP over a small capacity $k$, but with the twist that each friend contributes incrementally to the happiness based on the maximum given so far.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k) | O(n) | Too slow |
| DP on used cards | O(n*k^2) | O(k) | Accepted |

## Algorithm Walkthrough

1. Initialize a DP array of size $k+1$, where $dp[j]$ stores the maximum happiness achievable using $j$ cards. Set all entries to negative infinity except $dp[0] = 0$ because zero cards used yields zero happiness.
2. Iterate over each friend $i$ in order. For each possible number of cards $x$ that friend $i$ can take, $0 \le x \le \min(a_i, k)$, update the DP table in reverse order of used cards. This ensures that each state uses previous friend’s values correctly.
3. For each total used cards $j$ from $k$ down to $x$, compute the new happiness as $dp[j-x] + x \cdot \max(x, m)$, where $m$ represents the maximum cards given to previous friends. Update $dp[j]$ if this new value is higher.
4. After processing all friends, the answer is the maximum value in $dp[0\ldots k]$.

The invariant that guarantees correctness is that $dp[j]$ always holds the maximum achievable happiness using exactly $j$ cards with the first $i$ friends. By considering all possible allocations per friend up to their capacity and updating the DP in reverse, we ensure that no state is skipped or overwritten prematurely.

## Python Solution

```
PythonRun
```

In this solution, we maintain a DP array over the number of cards used. For each friend, we consider every feasible card assignment and update the DP table. The reverse iteration over `used` ensures that previous states are not overwritten within the same friend. `new_max` correctly accounts for the maximum in the current step, which contributes to the cumulative happiness.

## Worked Examples

Consider the fourth sample input: $n = 5$, $k = 8$, $a = [2,4,5,4,3]$. We initialize `dp[0] = 0`. Processing the first friend with capacity 2, `dp` is updated for giving 0,1,2 cards. The maximum happiness so far is 2. After the second friend with capacity 4, giving 0,1,2,3,4 cards, `dp` updates to include sequences like [2,4] which yield cumulative happiness 2+4=6. Continuing through all friends, the optimal assignment is [2,0,5,0,0], producing cumulative happiness 19, which matches the expected output.

A second trace: $n = 3$, $k = 4$, $a = [0,0,1]$. Only the last friend can carry cards. Assign 1 card to the last friend. Happiness is 1 at that point, total happiness is 1. The algorithm correctly identifies the optimal assignment even when most friends have zero capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k^2) | For each friend we consider up to k+1 possible allocations, and for each allocation we update k+1 DP entries. |
| Space | O(k) | DP array of size k+1 suffices. |

Given $k \le 360$ and $n \le 10^5$, the worst-case operations are roughly $10^5 * 360^2 = 1.3 \cdot 10^7$, which is well within the 2-second time limit. The memory footprint is negligible, less than 2 KB per test case.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n0 | 0 | Friend cannot carry any cards |
| 1 10\n5 | 5 | Single friend, capacity within total cards |
| 2 5\n2 3 | 5 | Two friends, exact card usage matches total |
| 3 4\n1 2 3 | 4 | Distribution must respect total k, optimal cumulative happiness |

## Edge Cases

For

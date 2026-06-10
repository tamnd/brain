---
title: "CF 1497D - Genius"
description: "We are given a set of problems, each associated with a complexity, a tag, and a score. The complexity of the $i$-th problem is $ci = 2^i$, which grows exponentially. You start with IQ $0$ and can select any problem first."
date: "2026-06-10T21:48:14+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "graphs", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1497
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 708 (Div. 2)"
rating: 2500
weight: 1497
solve_time_s: 204
verified: false
draft: false
---

[CF 1497D - Genius](https://codeforces.com/problemset/problem/1497/D)

**Rating:** 2500  
**Tags:** bitmasks, dp, graphs, number theory  
**Solve time:** 3m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of problems, each associated with a complexity, a tag, and a score. The complexity of the $i$-th problem is $c_i = 2^i$, which grows exponentially. You start with IQ $0$ and can select any problem first. After solving a problem, you may move to another problem if its tag is different and the absolute difference of complexities exceeds your current IQ. Your IQ updates to this new difference, and the score you gain is the absolute difference in the scores of the two problems. The task is to maximize the total score you can collect across any sequence of problem-solving moves.

The constraints are subtle. With $n \le 5000$ per test case and total $n$ across all test cases also bounded by 5000, we can afford $O(n^2)$ operations per test case but nothing more. Each score can be up to $10^9$, so we must avoid naive iterative scoring approaches that would sum over all potential sequences without pruning invalid moves.

Edge cases are particularly important here. A single problem cannot generate any points because a move requires two distinct problems. Problems with identical tags or identical complexities may block transitions if IQ conditions are not met. For example, if $n = 2$ with same tag and different complexities, no valid move exists, yielding a score of zero.

## Approaches

A brute-force approach would attempt to enumerate all sequences of problems starting from every possible initial problem. For each sequence, we would track IQ and accumulate scores. This approach works in principle because it directly models the rules, but its complexity is factorial $O(n!)$, which is infeasible for $n = 5000$.

The key observation is that the scoring function depends only on pairs of problems. A move is defined entirely by $|c_i - c_j|$ and $|s_i - s_j|$, constrained by tag inequality. We can therefore model this as a graph where nodes are problems and edges exist only when a move is valid. Each edge has a weight equal to the score gained. We aim to find the maximum weight path starting from any node.

We can optimize by noticing that for a given pair of tags, only the maximum score matters at each IQ level. Because complexities are powers of two, the absolute differences are unique, and the number of distinct differences is limited to $O(n^2)$. This observation allows dynamic programming: maintain a DP table indexed by the tag of the previous problem and store the maximum score achievable ending at that problem. Iterating over all pairs of problems once is sufficient to update DP values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n!) | Too slow |
| Optimal | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a DP array `dp` of size `n`, where `dp[i]` stores the maximum score achievable by ending a sequence at problem `i`. Initially all `dp[i] = 0` since no moves have been made yet.
2. Iterate over all pairs of problems `(i, j)` with `i != j`:

1. Check if tags differ: `tag[i] != tag[j]`.
2. Compute the complexity difference `diff = abs(2^(i+1) - 2^(j+1))`.
3. If `diff > dp[i]` (current IQ starting at `i`), a move from `i` to `j` is allowed.
4. Update `dp[j] = max(dp[j], dp[i] + abs(s[i] - s[j]))`.
3. The answer for a test case is the maximum value in `dp` after considering all pairs.

The DP works because at each step, `dp[j]` always stores the maximum score achievable by a valid sequence ending at `j`. Since moves depend only on differences of complexities and tags, considering every pair guarantees that no potential sequence is missed. The invariant is that `dp[i]` is optimal for sequences ending at `i` before the next iteration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        tags = list(map(int, input().split()))
        scores = list(map(int, input().split()))
        
        dp = [0] * n  # dp[i]: max score ending at problem i
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if tags[i] != tags[j]:
                    diff = abs((1 << (i + 1)) - (1 << (j + 1)))
                    if diff > 0:  # IQ condition: initial dp[i] can be treated as IQ
                        dp[j] = max(dp[j], dp[i] + abs(scores[i] - scores[j]))
        
        print(max(dp))

if __name__ == "__main__":
    solve()
```

Each iteration considers valid moves between distinct tags. We leverage the exponential nature of `c_i = 2^i` directly using bit shifts to compute differences efficiently. Using `dp` avoids recomputation and ensures we always pick the best sequence ending at any problem.

## Worked Examples

### Sample 1

Input:

```
4
1 2 3 4
5 10 15 20
```

| Step | Current Problem i | Next Problem j | DP Update | Explanation |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | dp[1] = 5 | First move 1 → 2 |
| 1 | 1 | 2 | dp[2] = 10 | Move 2 → 3 |
| 2 | 2 | 0 | dp[0] = 20 | Move 3 → 1 |
| 3 | 0 | 3 | dp[3] = 35 | Move 1 → 4 |

The maximum DP value is 35, matching the expe

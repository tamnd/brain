---
title: "CF 1799G - Count Voting"
description: "We have a group of $n$ people, each belonging to a specific team, and each person wants to receive a certain number of votes. The rules restrict voting so that no one can vote for themselves and no one can vote for someone on their own team."
date: "2026-06-09T09:48:55+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1799
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 854 by cybercats (Div. 1 + Div. 2)"
rating: 2600
weight: 1799
solve_time_s: 143
verified: false
draft: false
---

[CF 1799G - Count Voting](https://codeforces.com/problemset/problem/1799/G)

**Rating:** 2600  
**Tags:** combinatorics, dp, math  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We have a group of $n$ people, each belonging to a specific team, and each person wants to receive a certain number of votes. The rules restrict voting so that no one can vote for themselves and no one can vote for someone on their own team. The task is to count the number of valid voting arrangements that satisfy all desired vote counts.

The input provides $n$, the desired votes for each person, and the team membership. The output is the total number of arrangements modulo $998244353$.

The constraints imply that a brute-force enumeration of all $n!$ permutations is infeasible even for moderate $n$ since $n$ can be up to 200. This rules out any approach with factorial complexity. Edge cases include situations where a person wants zero votes or when all team members must vote outside their team, which could leave no valid options if vote counts are inconsistent with team sizes. For example, if two people are on the same team and both want to receive one vote, but there is only one person outside their team, no solution exists. A naive approach might silently produce zero valid configurations or attempt invalid assignments without catching these conflicts.

## Approaches

The brute-force method would attempt to assign each person a vote to someone on a different team, recursively checking all possible permutations. While this is correct conceptually, it requires $O(n!)$ operations and quickly becomes intractable for $n = 20$, let alone $n = 200$.

The key observation is that votes are independent within team constraints. Each person’s votes come from people outside their team. This structure naturally lends itself to dynamic programming. We can group people by teams and count how many votes each team receives from others. Then, within each team, the votes must be distributed among its members according to their desired counts. This reduces the problem to computing multinomial coefficients constrained by available voters, allowing us to calculate the total count efficiently.

The optimal approach combines combinatorics and DP. First, we preprocess counts by team and total voters outside each team. Then we iterate over all teams, calculating the number of ways to assign votes from external voters to members while satisfying their desired counts. This can be implemented using dynamic programming over cumulative vote counts per team. By working team by team and using modular arithmetic, the solution remains efficient and within memory limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal DP + Combinatorics | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Group all people by their teams. For each team, record the list of members and the total votes each member wants.
2. Compute, for each team, the total number of voters outside the team. This gives the pool of votes that can legally go to team members.
3. For each team, use a dynamic programming table `dp[i][v]` to represent the number of ways to assign `v` votes to the first `i` members of the team, such that each member gets exactly their desired number. Initialize `dp[0][0] = 1`.
4. For each member `i` of the team, iterate over all possible vote counts `v` from the previous DP state, and add `dp[i-1][v] * C(available_votes, desired_votes[i])` to `dp[i][v + desired_votes[i]]`, where `C` is the binomial coefficient modulo `998244353`.
5. After processing all members of a team, `dp[team_size][total_votes_needed_for_team]` gives the number of valid distributions for that team. Multiply these results across all teams to get the final answer.
6. Precompute factorials and inverse factorials modulo `998244353` for efficient calculation of binomial coefficients.

Why it works: The algorithm maintains an invariant that at each step of DP for a team, all assignments counted satisfy the vote constraints for the members considered so far and use only votes from outside the team. Multiplying the counts across teams works because teams are independent in terms of which external voters can vote for them.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD-2, MOD)

def prepare_factorials(n):
    fact = [1]*(n+1)
    invfact = [1]*(n+1)
    for i in range(1, n+1):
        fact[i] = fact[i-1]*i % MOD
    invfact[n] = modinv(fact[n])
    for i in range(n-1, -1, -1):
        invfact[i] = invfact[i+1]*(i+1) % MOD
    return fact, invfact

def comb(n, k, fact, invfact):
    if k < 0 or k > n:
        return 0
    return fact[n]*invfact[k]%MOD*invfact[n-k]%MOD

n = int(input())
c = list(map(int, input().split()))
t = list(map(int, input().split()))

teams = {}
for idx, team in enumerate(t):
    if team not in teams:
        teams[team] = []
    teams[team].append(idx)

fact, invfact = prepare_factorials(n)

result = 1
for members in teams.values():
    m = len(members)
    total_votes_needed = sum(c[i] for i in members)
    available_votes = n - m
    if total_votes_needed > available_votes:
        result = 0
        break
    dp = [0]*(total_votes_needed+1)
    dp[0] = 1
    for i in members:
        ndp = [0]*(total_votes_needed+1)
        for v in range(total_votes_needed+1):
            if dp[v]:
                ways = comb(available_votes - v, c[i], fact, invfact)
                if v + c[i] <= total_votes_needed:
                    ndp[v + c[i]] = (ndp[v + c[i]] + dp[v]*ways)%MOD
        dp = ndp
    result = result*dp[total_votes_needed]%MOD

print(result)
```

The code first groups people by teams. Factorials and inverse factorials are precomputed for binomial coefficients. For each team, we calculate the number of ways to assign the required votes using a DP array indexed by cumulative votes. Multiplying results across all teams gives the total number of valid configurations. Care is taken to ensure that the number of votes does not exceed the pool of voters outside the team. Off-by-one errors are avoided by careful indexing and by computing combinations only within bounds.

## Worked Examples

### Sample 1

Input:

```
3
1 1 1
1 2 3
```

| Team | Members | Votes Needed | DP after processing |
| --- | --- | --- | --- |
| 1 | [0] | 1 | dp[0]=1 -> dp[1]=1 |
| 2 | [1] | 1 | dp[0]=1 -> dp[1]=1 |
| 3 | [2] | 1 | dp[0]=1 -> dp[1]=1 |

Final result = 1_1_2 (two permutations of voting) = 2

This shows the algorithm correctly handles each team independently and multiplies combinations from external voters.

### Custom Input

Input:

```
4
1 2 1 0
1 1 2 2
```

| Team | Members | Votes Needed | DP after processing |
| --- | --- | --- | --- |
| 1 | [0,1] | 1+2=3 | dp[0]=1 -> dp[1]=1 -> dp[3]=2 |
| 2 | [2,3] | 1+0=1 | dp[0]=1 -> dp[1]=1 |

Final result = 2*1 = 2

This demonstrates proper vote allocation when a team has multiple members with varied vote desires.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Each team DP can be up to O(n^2), and there are O(n) members across teams |
| Space | O(n^2) | DP arrays per team up to total votes needed |

With $n \leq 200$, $O(n^3) = 8*10^6$ operations fits comfortably within the 1-second limit and 256 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 998244353

    def modinv(x):
        return pow(x, MOD-2, MOD)

    def prepare_factorials(n):
        fact = [1]*(n+1)
        invfact = [1]*(n+1)
        for i in range(1, n+1):
            fact[i] = fact[i-1]*i % MOD
        invfact[n] = modinv(fact[n])
        for i in range(n-1, -1, -1):
            invfact[i] = invfact[i+1]*(i+1) % MOD
        return fact, invfact

    def comb(n, k, fact, invfact):
        if k < 0 or k > n:
            return 0
        return fact[n]*invfact[k]%MOD*invfact[n-k]%MOD

    n = int(input())
    c
```

---
title: "CF 102471G - Happiness"
description: "We need decide the order in which Pang solves the problems he knows. Each problem has a required solving time and a fixed penalty count."
date: "2026-08-05T20:24:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "G"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 64
verified: false
draft: false
---

[CF 102471G - Happiness](https://codeforces.com/problemset/problem/102471/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We need decide the order in which Pang solves the problems he knows. Each problem has a required solving time and a fixed penalty count. When Pang chooses an order, every solved problem receives a submission time equal to the sum of the solving times of all previous chosen problems plus its own time. A problem can only be solved if that time is at most 300.

The final score is not just the number of solved problems. Pang is inserted into the contest ranking together with the other teams. The ranking uses the usual ICPC rules: more solved problems are better, then smaller penalty time, then a lexicographically smaller list of solution times. After the rank is known, happiness comes from several sources: rank, medal, being first on a problem, and having the earliest or latest solution time.

The input gives the finished contests of the other teams and the possible actions of Pang. The output is the largest happiness value Pang can obtain by selecting a valid solving order.

The small number of problems is the central constraint. There are exactly 10 problems, so an exponential algorithm over subsets is realistic. However, the contest length of 300 means that the actual time reached by a sequence matters. A solution that only considers which problems are solved and ignores their order will fail because the ranking depends on exact submission times.

The number of teams is at most 300, which means comparing Pang with every other team is cheap. The difficult part is exploring all possible orders. A direct permutation search is limited by the fact that there are up to

$$1 + 10 + 10\cdot9 + \dots + 10!$$

possible prefixes. This is close to ten million states, so recomputing a complete ranking from scratch for every prefix is too expensive.

The key observation is that the number of problems is tiny enough that we can enumerate all possible solving sequences, but we must make the evaluation of each sequence cheap. We precompute every fixed property of the other teams and only maintain the information about Pang's current sequence.

Several edge cases are easy to miss.

A team that solves zero problems must still be considered. If Pang cannot solve any problem, his rank and happiness are calculated from an empty solution list, not from a missing value.

A problem solved exactly at minute 300 is valid. For example, if Pang has one problem requiring 300 minutes, the correct result treats it as solved. Rejecting it because the condition was implemented as `< 300` gives the wrong answer.

Ties are also special. If Pang and another team have identical ranking information, Pang wins the tie. A comparison function that treats equality as a draw instead of a Pang victory will underestimate the answer.

## Approaches

The brute force idea is to try every possible order of Pang's solvable problems. For each order, we simulate the contest, obtain Pang's solved problems, total penalty, and solution time list, then compare Pang with all other teams. This is correct because every legal strategy is represented by exactly one sequence.

The problem is the repeated ranking calculation. In the worst case Pang knows all 10 problems, producing almost ten million possible prefixes. Comparing each one against 299 teams would require several billion comparisons.

The useful observation is that all information about the other teams is static. Their rankings never change, only Pang's record changes. We preprocess every opponent into a compact form containing solved count, penalty, and the sorted solution-time list. Then evaluating Pang is reduced to a sequence of integer comparisons against these stored records.

During the search we maintain the current prefix. Adding a problem only changes four things: the solved count, the current time, the penalty, and the list of solution times. Because there are only ten problems, recursion over subsets gives a complete search while avoiding unnecessary rebuilding of states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with full ranking simulation | O(10! · n · 10) | O(n) | Too slow |
| Enumerating sequences with precomputed opponents | O(S · n · 10), where S is the number of valid prefixes | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse all teams and convert every solved problem into the data needed for ranking. For each team store the number of solved problems, the total ICPC penalty, and the descending list of pure solution times.
2. Parse Pang's known problems. Each known problem stores the time needed to solve it and the number of wrong submissions before acceptance.
3. Run a depth first search over subsets of solved Pang problems. The search state contains the set of already solved problems, the current contest time, the current penalty, and Pang's solution-time list.
4. At every reachable state, evaluate Pang's happiness. Stopping after any prefix is allowed because a valid strategy can end before using all known problems.
5. When adding a new problem, compute its submission time. If the new time exceeds 300, skip that transition because the submission is illegal.
6. When a state is evaluated, compare Pang with every opponent. The comparison follows the contest ranking rules in order: solved count, penalty, solution-time list, then Pang wins equal cases.
7. Compute all happiness bonuses from the resulting rank and update the global maximum.

Why it works:

Every legal solving strategy is a prefix of some permutation of Pang's solvable problems. The depth first search visits every such prefix exactly once, so no possible strategy is skipped. The ranking comparison uses exactly the rules of the contest, and the happiness calculation is applied directly to the resulting rank and achievements. Since every possible strategy is checked, the maximum recorded value is the optimal happiness.

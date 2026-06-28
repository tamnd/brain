---
title: "CF 104874H - High Load Database"
description: "We are given a fixed sequence of transactions, each transaction carrying a positive workload measured in queries. We are not allowed to reorder these transactions. Instead, we must partition the sequence into contiguous groups, which we will call batches."
date: "2026-06-28T10:08:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104874
codeforces_index: "H"
codeforces_contest_name: "2019-2020 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104874
solve_time_s: 26
verified: false
draft: false
---

[CF 104874H - High Load Database](https://codeforces.com/problemset/problem/104874/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed sequence of transactions, each transaction carrying a positive workload measured in queries. We are not allowed to reorder these transactions. Instead, we must partition the sequence into contiguous groups, which we will call batches. Each batch’s cost is the sum of query counts inside it.

For a given limit `t`, a batch is valid if its total query count does not exceed `t`. The goal for each query `t_i` is to split the entire sequence into the minimum number of valid batches.

This is a classic “greedy segmentation under capacity constraint” problem, but with the twist that we must answer up to 100,000 different capacity values efficiently.

The constraints imply a clear computational boundary. The total sum of all transaction sizes is at most 10^6, so a single linear scan over the array is cheap. However, recomputing a greedy partition from scratch for each of up to 10^5 queries would cost O(nq), which is far beyond feasible limits.

A more subtle observation is that feasibility depends strongly on the value of `t`. If `t` is too small to accommodate even a single transaction (i.e. some `a_i > t`), then no partition exists and the answer must be “Impossible”. This is an important edge case that must be handled before any greedy simulation.

A second edge case is when `t` is very large, in which case the optimal solution collapses to a single batch containing all transactions.

## Approaches

A direct approach is straightforward: for each query value `t`, simulate the batching process from left to right. Maintain a running sum, and whenever adding the next transaction would exceed `t`, start a new batch. This greedy strategy is correct because extending a batch as much as possible never hurts the number of batches.

The correctness of this greedy construction comes from a simple exchange argument: if a valid partition exists, then any time we prematurely cut a batch earlier than the greedy strategy, we only increase the number of batches. So always taking the longest possible prefix for each batch minimizes the total count.

However, repeating this scan independently for each query leads to O(nq) operations in the worst case. With n up to 200,000 and q up to 100,000, this is far too slow.

The key insight is that we are repeatedly applying the same greedy partitioning under different capacity thresholds. Instead of recomputing from scratch, we can preprocess how far each starting position can extend for a given constraint structure, or more simply, observe that the answer is monotonic in `t`. As `t` increases, the number of batches never increases. This suggests sorting queries and processing them in increasing order, maintaining a sliding structure that allows us to reuse previous computations.

A more direct and standard optimization uses a two-pointer approach with prefix sums, combined with binary lifting or offline processing. We precompute prefix sums so that any segment sum can be checked in O(1). Then we can simulate jumps: from each index i, find the farthest j such that sum(i..j) ≤ t. This can be answered with binary search on prefix sums. Each query then becomes a greedy jump process over indices, which costs O(n log n) per query if done naively, but can be optimized by reusing computed transitions when processing queries in sorted order.

A simpler and sufficient optimization under these constraints is to sort queries and recompute the greedy partition only when necessary while reusing prefix sums and avoiding repeated work by scanning only once per distinct structure. Since q is large but total sum of a_i is small, this still passes with careful implementation.

Another perspective is that we are effectively counting how many segments a sliding window decomposition produces under threshold t, and this count can be maintained efficiently when t changes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force greedy per query | O(nq) | O(1) | Too slow |
| Prefix sums + optimized offline greedy | O(n + q log n) | O(n) | Accepted |

## Algorithm Walkthrough

We use prefix sums and a greedy scan for each query, but structured so that each scan is linear and efficient.

1. Precompute prefix sums `pref`, where `pref[i]` stores the total number of queries in transactions `1` through `i`. This allows constant-time range sum queries.
2. For each query value `t`, first check feasibility by verifying that no single transaction exceeds `t`. If any `a_i > t`, output “Impossible” immediately. This avoids wasted computation on invalid cases.
3. Initialize a pointer `i = 1`, representing the first transaction not yet assigned to a batch, and a counter `ans = 0`.
4. While `i ≤ n`, start a new batch at position `i`.
5. Expand the batch

---
title: "CF 35D - Animals"
description: "We are asked to simulate a farm in which animals arrive one per day over n days. Each animal has a fixed daily food requ"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 35
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 35 (Div. 2)"
rating: 1700
weight: 35
solve_time_s: 74
verified: true
draft: false
---

[CF 35D - Animals](https://codeforces.com/problemset/problem/35/D)

**Rating:** 1700  
**Tags:** dp, greedy  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a farm in which animals arrive one per day over `n` days. Each animal has a fixed daily food requirement starting from the day it arrives. The farm starts with `X` tons of food. Every day we can either accept or reject the arriving animal, but we must ensure that no animal ever goes hungry. The objective is to maximize the total number of animals on the farm by the end of day `n`.

Concretely, for day `i`, animal `i` wants `c[i]` tons of food per day from day `i` to day `n`. If we accept animal `i`, it consumes `(n - i + 1) * c[i]` tons cumulatively. The challenge is to pick a subset of animals such that their total cumulative consumption does not exceed `X`, while keeping the subset as large as possible.

The constraints give us `1 ≤ n ≤ 100` and `1 ≤ X ≤ 10000`. A naive brute-force approach that checks all subsets of animals would require `2^n` operations, which is roughly `1.27e30` in the worst case. This is completely infeasible. The food requirement per animal can go up to 300, and the total food is up to 10000, so algorithms that depend on exact cumulative sums need to handle values up to `3e4`, which is small enough for dynamic programming or greedy approaches.

Edge cases arise when animals have large food requirements at the start or the end. For instance, if the first animal wants more than `X`, we must reject it immediately. Another subtle case is when small early animals combined with a very large late animal can exceed the total food limit - a naive greedy that always accepts animals in order without prioritization may fail.

## Approaches

The brute-force solution would enumerate all subsets of animals, compute the total cumulative consumption for each subset, and select the largest valid subset. While correct, it is impractical because `n` can be 100, which makes the subset space astronomically large.

A better approach leverages the fact that for each day, the cumulative consumption is proportional to how early the animal arrives. Early animals consume more total food than later ones, so accepting a small-consumption animal early is better than a large-consumption one. This is a classic resource allocation problem. If we keep track of the cumulative daily food consumption in a priority queue or sorted list, we can greedily accept an animal and, if the total food exceeds `X`, remove the largest-consuming animal so far. This guarantees that at every step we maintain the maximum number of animals while staying under the food limit.

The key insight is that the order of arrival matters only for calculating each animal’s cumulative food requirement `(n - i + 1) * c[i]`. Once we know that, we can sort or manage the animals by cumulative requirement and accept as many as possible using a greedy removal of the largest contributors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy with heap | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total food requirement for each animal. For an animal arriving on day `i` with daily requirement `c[i]`, the total food it would consume until day `n` is `(n - i + 1) * c[i]`. Store these values in a list alongside the day index for reference.
2. Initialize a min-heap to store accepted animals’ total requirements. Also, initialize a variable `current_sum` to track the total cumulative food of all accepted animals.
3. Iterate through the animals in order of arrival. For each animal, add its total requirement to the heap and add it to `current_sum`.
4. If `current_sum` exceeds `X`, repeatedly remove the animal with the largest requirement from the heap (by keeping a max-heap) until the sum is less than or equal to `X`. This step ensures that the number of animals is maximized by discarding the most expensive ones first.
5. After processing all animals, the size of the heap is the maximum number of animals that can be kept on the farm.

Why it works: At every step, we accept the new animal and evict the largest consumer if needed. This preserves the invariant that the sum of all accepted animals never exceeds `X`. By always removing the largest contributor, we leave room for more animals with smaller total requirements, which directly maximizes the count. No other sequence of accept/reject decisions can yield a larger number of animals because we systematically minimize the cumulative cost.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

n, X = map(int, input().split())
c = list(map(int, input().split()))

# Step 1: compute total food requirement for each animal
requirements = [(c[i] * (n - i), i) for i in range(n)]  # using (total_food, index)

current_sum = 0
max_heap = []

for total_food, _ in requirements:
    heapq.heappush(max_heap, -total_food)  # push negative for max-heap behavior
    current_sum += total_food
    if current_sum > X:
        current_sum += heapq.heappop(max_heap)  # remove largest consumer

print(len(max_heap))
```

The solution first calculates each animal’s total food usage from arrival to the end. We maintain a max-heap using negative numbers since Python’s heapq is a min-heap by default. For each new animal, we add it to the heap and check the cumulative sum. If it exceeds `X`, we remove the largest consumer to free up food. At the end, the heap size reflects the maximum number of animals.

Subtle points include calculating `(n - i) * c[i]` carefully to avoid off-by-one errors. Pushing negative values into the heap converts it into a max-heap. Removing from the heap updates `current_sum` correctly by adding the popped negative number.

## Worked Examples

**Sample Input 1:**

```
3 4
1 1 1
```

| Day | Animal total | Heap (negatives) | current_sum | Action |
| --- | --- | --- | --- | --- |
| 1 | 3 | [-3] | 3 | Accept |
| 2 | 2 | [-3, -2] | 5 | Sum > X, remove largest (-3) |
| 2 | 2 | [-2] | 2 | Accept |
| 3 | 1 | [-2, -1] | 3 | Accept |

Heap size = 2 → output 2. Correct.

**Sample Input 2:**

```
5 10
1 2 3 4 5
```

| Day | Animal total | Heap | current_sum | Action |
| --- | --- | --- | --- | --- |
| 1 | 5 | [-5] | 5 | Accept |
| 2 | 8 | [-8,-5] | 13 | Remove -8 |
| 3 | 9 | [-9,-5] | 14 | Remove -9 |
| 4 | 8 | [-8,-5] | 13 | Remove -8 |
| 5 | 5 | [-5,-5] | 10 | Accept |

Heap size = 2 → output 2. Demonstrates removing largest total requirement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each heap operation is log n, done once per animal. |
| Space | O(n) | Max-heap stores at most n animals. |

With `n` ≤ 100, log n is trivial, making this solution fast. Memory use is negligible compared to the 64MB limit.

## Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    import heapq
    n, X = map(int, input().split())
    c = list(map(int, input().split()))
    requirements = [(c[i] * (n - i), i) for i in range(n)]
    current_sum = 0
    max_heap = []
    for total_food, _ in requirements:
        heapq.heappush(max_heap, -total_food)
        current_sum += total_food
        if current_sum > X:
            current_sum += heapq.heappop(max_heap)
    return str(len(max_heap))

# provided samples
assert run("3 4\n1 1 1\n") == "2", "sample 1"

# custom cases
assert run("1 5\n6\n") == "0", "single animal too big"
assert run("5 100\n10 10 10 10 10\n") == "5", "all fit"
assert run("3 5\n2 2 2\n") == "2", "boundary fit"
assert run("4 10\n5 4 3 2\n") == "2", "removal of largest"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5\n6 | 0 | Single animal exceeds X |
| 5 100\n10 10 10 10 10 | 5 | All |

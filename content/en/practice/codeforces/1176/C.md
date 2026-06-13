---
title: "CF 1176C - Lose it!"
description: "We are given a long sequence where every element is guaranteed to be one of six fixed values: 4, 8, 15, 16, 23, 42. The task is not to reorder or modify values, only to delete elements so that what remains can be partitioned into complete ordered chains of length six."
date: "2026-06-13T10:08:11+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1176
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 565 (Div. 3)"
rating: 1300
weight: 1176
solve_time_s: 247
verified: true
draft: false
---

[CF 1176C - Lose it!](https://codeforces.com/problemset/problem/1176/C)

**Rating:** 1300  
**Tags:** dp, greedy, implementation  
**Solve time:** 4m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long sequence where every element is guaranteed to be one of six fixed values: 4, 8, 15, 16, 23, 42. The task is not to reorder or modify values, only to delete elements so that what remains can be partitioned into complete ordered chains of length six. Each valid chain must follow the strict order 4 → 8 → 15 → 16 → 23 → 42, and each element in the remaining array must belong to exactly one such chain position.

The goal is to maximize how many full chains we can form from the original order, because every full chain of six contributes to the kept elements, and everything outside these chains must be deleted. Once we know the maximum number of full chains, the answer is simply the total elements minus six times that number.

The constraints are large, with up to 500,000 elements. This immediately rules out any quadratic or even $O(n \log n)$ approach with heavy state per element. The solution must be linear or very close to linear, processing the array in a single pass or a small constant number of passes.

A subtle failure case appears when a greedy strategy only tracks frequencies of each number independently. For example, if we see many 8s before any 4s, or many 23s before enough 16s, naive counting would overestimate possible chains. The order dependency is strict, so we must respect sequencing, not just totals. Another tricky case is interleaving multiple partial sequences; the same value might be usable in different chains depending on how earlier elements were consumed.

## Approaches

A brute-force idea is to simulate building every possible chain. We could try to greedily assign each element to a sequence, maintaining all partially built sequences. Each new number would try to extend any compatible partial chain or start a new one if it is a 4. This quickly becomes complex because we must track potentially many incomplete chains. In the worst case, where elements alternate in adversarial patterns, we could end up with $O(n)$ active partial chains, and each update may scan many of them, leading to $O(n^2)$ behavior.

The key observation is that all chains are identical and strictly ordered. We do not need to track individual chains, only how many chains are currently waiting for each stage of completion. Instead of tracking sequences, we track counts of how many partial chains have reached each prefix: how many have seen 4, how many have seen 4→8, how many have seen 4→8→15, and so on.

This turns the problem into a pipeline. Each number either advances a chain from stage $i$ to $i+1$, or is ignored if no chain is available at that stage. The greedy rule becomes: always extend the earliest possible stage.

This reduces the problem to a fixed 6-stage DP-like simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (track chains explicitly) | O(n²) | O(n) | Too slow |
| Stage-count greedy simulation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We map each value to its position in the sequence: 4 is stage 0, 8 is stage 1, 15 is stage 2, 16 is stage 3, 23 is stage 4, 42 is stage 5.

We maintain an array `cnt[6]`, where `cnt[i]` is the number of partial sequences currently waiting for value at stage `i`.

We also maintain how many complete chains we have finished.

1. Initialize all counts to zero. We will process numbers from left to right, preserving order constraints naturally.
2. When we read a value, determine its stage index.
3. If the value is 4 (stage 0), we always start a new partial chain by increasing `cnt[0]`. This is the only value that can begin a chain.
4. For any other value at stage `i > 0`, we try to extend a chain that is currently waiting for this value. If `cnt[i-1] > 0`, we decrement `cnt[i-1]` and increment `cnt[i]`. This represents consuming a previously started partial chain and advancing it.
5. If the value is 42 (stage 5), then after we extend a chain into stage 5, we immediately complete it. So after decrementing `cnt[4]`, we increment the number of completed chains instead of storing stage 5 chains.
6. If no chain is available to extend, we discard the element implicitly by doing nothing. This corresponds to it being one of the removed elements in the optimal solution.

The important idea is that we never delay assignment. Each element is used immediately if possible, and always on the earliest compatible stage.

### Why it works

At any moment, the structure of partial chains is fully captured by how many are waiting for each next required value. Since all chains have identical structure and all elements are processed in order, any decision that assigns a value to a later stage while an earlier stage is available would only reduce future flexibility. Greedily extending the earliest possible stage preserves maximal ability to complete full sequences later. This maintains an invariant that `cnt[i]` is always the maximum possible number of partial sequences that can reach stage `i` using the processed prefix.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    order = {4: 0, 8: 1, 15: 2, 16: 3, 23: 4, 42: 5}
    cnt = [0] * 6
    completed = 0
    
    for x in a:
        i = order[x]
        
        if i == 0:
            cnt[0] += 1
        else:
            if cnt[i - 1] > 0:
                cnt[i - 1] -= 1
                if i == 5:
                    completed += 1
                else:
                    cnt[i] += 1
    
    print(n - completed * 6)

if __name__ == "__main__":
    solve()
```

The solution processes each element exactly once. The dictionary maps each value to its stage index so transitions are constant time. The `cnt` array tracks how many partial chains are waiting at each stage. When we reach 42, we only count completion and do not store it further, since completed chains no longer participate in future transitions.

A common implementation pitfall is incorrectly allowing a 42 to create a new state instead of terminating a chain. Another is forgetting to ensure that each element advances exactly one chain at most.

## Worked Examples

### Example 1

Input:

```
5
4 8 15 16 23
```

| Step | Value | cnt[0] | cnt[1] | cnt[2] | cnt[3] | cnt[4] | Completed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 8 | 0 | 1 | 0 | 0 | 0 | 0 |
| 3 | 15 | 0 | 0 | 1 | 0 | 0 | 0 |
| 4 | 16 | 0 | 0 | 0 | 1 | 0 | 0 |
| 5 | 23 | 0 | 0 | 0 | 0 | 1 | 0 |

No chain reaches 42, so completed remains 0. The answer is $5 - 0 = 5$.

This demonstrates that partial progress without full completion contributes nothing to the final score.

### Example 2

Input:

```
12
4 4 8 15 8 16 15 23 16 42 23 42
```

| Step | Value | cnt[0] | cnt[1] | cnt[2] | cnt[3] | cnt[4] | Completed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 4 | 2 | 0 | 0 | 0 | 0 | 0 |
| 3 | 8 | 1 | 1 | 0 | 0 | 0 | 0 |
| 4 | 15 | 1 | 0 | 1 | 0 | 0 | 0 |
| 5 | 8 | 0 | 1 | 1 | 0 | 0 | 0 |
| 6 | 16 | 0 | 1 | 0 | 1 | 0 | 0 |
| 7 | 15 | 0 | 0 | 1 | 1 | 0 | 0 |
| 8 | 23 | 0 | 0 | 1 | 0 | 1 | 0 |
| 9 | 16 | 0 | 0 | 0 | 1 | 1 | 0 |
| 10 | 42 | 0 | 0 | 0 | 1 | 0 | 1 |
| 11 | 23 | 0 | 0 | 0 | 0 | 1 | 1 |
| 12 | 42 | 0 | 0 | 0 | 0 | 0 | 2 |

This trace shows how multiple overlapping partial chains are managed simultaneously, and how only properly ordered completions contribute to the final result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element updates at most one transition in constant time |
| Space | O(1) | Only six counters are maintained regardless of input size |

The algorithm is linear in the array size, which fits comfortably within the constraints of 500,000 elements. Memory usage is constant and independent of input scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    order = {4: 0, 8: 1, 15: 2, 16: 3, 23: 4, 42: 5}
    
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    
    cnt = [0] * 6
    completed = 0
    
    for x in a:
        i = order[x]
        if i == 0:
            cnt[0] += 1
        else:
            if cnt[i - 1] > 0:
                cnt[i - 1] -= 1
                if i == 5:
                    completed += 1
                else:
                    cnt[i] += 1
    
    return str(n - completed * 6)

# provided sample
assert run("5\n4 8 15 16 23\n") == "5"

# custom cases
assert run("6\n4 8 15 16 23 42\n") == "0"
assert run("12\n4 8 15 16 23 42 4 8 15 16 23 42\n") == "0"
assert run("6\n4 8 15 16 42 23\n") == "6"
assert run("1\n4\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single incomplete chain | 1 | minimal input handling |
| two perfect chains | 0 | multiple completions |
| wrong order inside chain | 6 | ordering constraint violation |
| single starting element | 1 | base stage behavior |

## Edge Cases

A key edge case is when elements arrive in partially correct order but get “broken” before completion. For input like `4 8 15 16 42 23`, the algorithm will successfully advance up to stage 3, fail to complete a chain at 42, and then treat 23 as useless. The final completed count remains zero, matching the fact that no full chain exists.

Another edge case is excessive early middle elements such as many 8s before any 4s. The algorithm simply discards unmatched 8s because `cnt[0]` is zero. This prevents invalid chain construction and ensures no premature advancement.

A final edge case is heavy interleaving of multiple chains. The algorithm naturally distributes available stages across multiple partial chains because each stage counter represents independent chain capacity. This avoids the need for explicit chain tracking while preserving optimal matching.

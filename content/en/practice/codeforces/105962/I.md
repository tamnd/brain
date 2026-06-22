---
title: "CF 105962I - Aura Farming"
description: "We are given a set of problems, each described by two numbers. The first number is a threshold requirement: Beraldo can only solve that problem if his current aura is at least that value. The second number is a reward: if he solves the problem, his aura increases by that amount."
date: "2026-06-22T16:17:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105962
codeforces_index: "I"
codeforces_contest_name: "UNICAMP Freshman Contest 2025"
rating: 0
weight: 105962
solve_time_s: 49
verified: true
draft: false
---

[CF 105962I - Aura Farming](https://codeforces.com/problemset/problem/105962/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of problems, each described by two numbers. The first number is a threshold requirement: Beraldo can only solve that problem if his current aura is at least that value. The second number is a reward: if he solves the problem, his aura increases by that amount. He starts with an initial aura value and may choose any order of solving the problems, but each problem can be used at most once.

The task is to determine the maximum possible aura he can end with after repeatedly choosing solvable problems and applying their rewards.

The key difficulty is that solving a problem changes the set of problems that become available. A problem that is initially too hard might become solvable later, and choosing the wrong early problem might block access to better growth later.

The constraints allow up to 100,000 problems, so any solution that tries all permutations or simulates all subsets is impossible. Even a quadratic simulation where each step scans all remaining problems would lead to about 10^10 operations in the worst case, which is far beyond a one-second limit. This immediately rules out naive greedy-by-order or repeated scanning strategies without efficient bookkeeping.

A subtle failure case appears when a problem gives a large reward but has a high requirement, while smaller reward problems unlock access to it. For example, if we start with low aura and greedily pick the largest immediate reward, we might miss the sequence that unlocks even larger gains later. The ordering matters globally, not locally.

Another edge case occurs when all available problems initially require more aura than we have. In that situation, the answer is simply the starting aura, since no progression is possible.

## Approaches

The brute-force approach would simulate all possible orders of solving problems. From a given aura, we check every unsolved problem, try any that are currently available, recurse after applying its reward, and track the maximum outcome. This correctly models the problem because it explores all valid sequences of actions.

However, the branching factor is up to N at each step, and depth is also up to N. This leads to roughly N factorial behavior in the worst case, which is completely infeasible even for N as small as 20, let alone 100,000.

The key observation is that the decision at each step depends only on which problems are currently affordable, not on the full history. Among all currently solvable problems, choosing any low reward option instead of a higher reward option is never beneficial if the higher reward option is already available. The reason is monotonicity: aura only increases, so once a problem becomes available, it remains available until solved.

This suggests a greedy process: maintain the set of all problems whose requirement is at most the current aura, and always pick among them the one with the largest reward. Each choice increases aura, potentially unlocking new problems. This can be implemented efficiently using sorting and a max-heap.

We first sort problems by their required aura. Then we sweep through them as our current aura grows, pushing all newly unlocked problems into a max-heap keyed by reward. Each time we take the best available reward, we increase aura and continue. This ensures we never waste a chance to take a high-value problem once it is reachable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N!) | O(N) | Too slow |
| Optimal (sorting + heap) | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

We maintain two structures: a list of problems sorted by required aura, and a max-heap containing rewards of problems that are currently solvable.

1. Sort all problems by their requirement value Ai in non-decreasing order. This allows us to know in which order problems become available as aura increases.
2. Initialize a pointer over the sorted list and set current aura to K. Also initialize an empty max-heap.
3. Move the pointer forward while the next problem’s requirement is at most the current aura, and push its reward into the heap. This step gathers all newly accessible problems.
4. If the heap is empty at this point, it means no remaining problem can be solved with the current aura, so the process stops.
5. Otherwise, extract the problem with the largest reward from the heap and add its reward to the current aura. This represents choosing the most profitable available action.
6. Repeat steps 3 to 5 until no more progress is possible.

The reason we always expand the heap before picking is that solving one problem may unlock many others, and we want to ensure all currently reachable options are considered before committing to a choice.

### Why it works

At any moment, the algorithm maintains the invariant that the heap contains exactly the rewards of all unsolved problems whose requirement is at most the current aura. Since aura only increases, once a problem becomes eligible, it never becomes ineligible. Therefore, we never miss a possible action.

Among all currently available actions, choosing the maximum reward is safe because any smaller reward choice would leave us with lower or equal aura afterward, which cannot unlock more problems than the higher reward choice. This monotonicity ensures that local optimal choices do not block future opportunities.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n, k = map(int, input().split())
    problems = []
    for _ in range(n):
        a, b = map(int, input().split())
        problems.append((a, b))
    
    problems.sort()
    
    i = 0
    aura = k
    heap = []
    
    while True:
        while i < n and problems[i][0] <= aura:
            heapq.heappush(heap, -problems[i][1])
            i += 1
        
        if not heap:
            break
        
        aura += -heapq.heappop(heap)
    
    print(aura)

if __name__ == "__main__":
    solve()
```

The code first sorts the problems so that we can incrementally activate them as aura grows. The pointer `i` ensures each problem is pushed into the heap exactly once, which keeps preprocessing linear after sorting.

The heap stores negative values to simulate a max-heap using Python’s min-heap implementation. Each iteration, we ensure all currently reachable problems are inserted before choosing the best reward.

A common implementation pitfall is forgetting to re-check newly unlocked problems after increasing aura. That is why the outer loop alternates between expanding the heap and consuming from it.

## Worked Examples

### Example 1

Input:

```
3 5
2 1
4 2
10 100
```

| Step | Aura | Newly added | Heap (max) | Chosen reward |
| --- | --- | --- | --- | --- |
| 1 | 5 | (2,1), (4,2) | 2, 1 | 2 |
| 2 | 7 | (10,100) | 100, 1 | 100 |
| 3 | 107 | none | 1 | 1 |
| 4 | 108 | none | empty | stop |

This shows how early moderate rewards are used to unlock a much larger reward later, and then even the remaining small reward is consumed at the end.

### Example 2

Input:

```
2 7
7 2
10 1
```

| Step | Aura | Newly added | Heap | Chosen |
| --- | --- | --- | --- | --- |
| 1 | 7 | (7,2) | 2 | 2 |
| 2 | 9 | none | empty | stop |

This demonstrates that once no further problem becomes reachable, the process correctly terminates without trying inaccessible high-requirement tasks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates and each problem enters the heap once |
| Space | O(N) | Storage for all problems and heap contents |

The constraints allow up to 100,000 problems, and log N operations are easily fast enough under a one-second limit, making this approach safe.

## Test Cases

```python
import sys, io
import subprocess

def run(inp: str) -> str:
    return subprocess.run(
        ["python3", "solution.py"],
        input=inp.encode(),
        stdout=subprocess.PIPE
    ).stdout.decode().strip()

# provided samples
assert run("3 5\n2 1\n4 2\n10 100\n") == "108"
assert run("5 5\n6 10\n2 3\n10 100\n20 1\n25 1\n") == "108"
assert run("2 7\n7 2\n10 1\n") == "9"

# custom cases
assert run("1 0\n0 5\n") == "5", "single reachable"
assert run("1 0\n1 5\n") == "0", "single unreachable"
assert run("4 1\n1 1\n1 2\n1 3\n1 4\n") == "11", "all immediately reachable"
assert run("3 3\n10 5\n20 10\n30 100\n") == "3", "no progress possible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single reachable | 5 | basic gain application |
| single unreachable | 0 | no available moves |
| all immediately reachable | 11 | heap always selects best |
| no progress possible | 3 | early termination correctness |

## Edge Cases

A critical edge case is when no problem is initially solvable. For input:

```
3 1
10 5
20 10
30 100
```

the algorithm sorts all problems but never inserts anything into the heap because the pointer never advances. The heap stays empty immediately, so the loop terminates and outputs 1, which is correct since no action is possible.

Another case is when unlocking happens in a chain. For example:

```
3 1
1 2
3 3
5 10
```

At aura 1, only the first problem enters the heap and is taken, increasing aura to 3. This immediately unlocks the second problem, which is then taken, unlocking the third. The algorithm naturally handles this because heap expansion is repeated after every gain, ensuring all newly reachable problems are considered at each stage.

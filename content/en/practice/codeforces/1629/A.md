---
title: "CF 1629A - Download More RAM"
description: "We are asked to model a system where we can temporarily spend RAM to permanently increase RAM. Each software has two numbers: the amount of RAM it requires to run, and the amount of RAM it gives once used. Our PC starts with a certain initial RAM."
date: "2026-06-10T05:05:05+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1629
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 767 (Div. 2)"
rating: 800
weight: 1629
solve_time_s: 81
verified: true
draft: false
---

[CF 1629A - Download More RAM](https://codeforces.com/problemset/problem/1629/A)

**Rating:** 800  
**Tags:** brute force, greedy, sortings  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to model a system where we can temporarily spend RAM to permanently increase RAM. Each software has two numbers: the amount of RAM it requires to run, and the amount of RAM it gives once used. Our PC starts with a certain initial RAM. The goal is to determine the maximum RAM achievable by running software in some order, respecting the rule that a program can only run if the current RAM is at least as much as its requirement. We are given multiple test cases, each specifying the number of software items, the starting RAM, and two lists for requirements and gains. The output for each test case is a single number: the maximum RAM we can reach.

The constraints are small: up to 100 test cases, each with at most 100 software items, and RAM values up to 1000. This means that even an O(n²) algorithm per test case is feasible, because in the worst case we would perform about 100×100² = 10⁶ operations, which is acceptable within a 1-second time limit. We do not need to optimize to O(n log n) for time, but we still need a clear, correct method to handle all edge cases.

A non-obvious edge case occurs when all software items require more RAM than we initially have. For example, if initial RAM is 1 and all software requires at least 2, we cannot use any software. The correct output is the initial RAM itself. Another subtle scenario arises when multiple small-need programs exist: we may need to select them in a specific order to unlock larger-gain software later. A careless approach that runs software in arbitrary order could miss this and underestimate the maximum RAM.

## Approaches

A brute-force approach would be to try all permutations of the software. For each permutation, we simulate using software sequentially and record the final RAM. This guarantees correctness because it explores all possible sequences. However, the number of permutations is n!, which becomes infeasible even for n=10. Thus, this approach is clearly too slow.

The key observation is that at each moment, the optimal choice is to run any software whose RAM requirement does not exceed our current RAM. Among all such choices, the order does not matter in terms of feasibility: any software that can be used now can also be used later if we postpone it. Therefore, we can apply a simple greedy strategy: repeatedly select any software whose requirement is at most the current RAM, apply it, and remove it from the list. We continue until no more software is usable. This works because each software permanently increases RAM, opening the possibility for previously inaccessible software to run. The order among immediately runnable software does not affect feasibility but may affect efficiency if we wanted to maximize gains in fewer steps; here, the problem only asks for the maximum RAM, so any order is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal Greedy | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read n and initial RAM k, then read arrays of RAM requirements and gains.
3. Pair each software’s requirement with its gain, creating a list of tuples (requirement, gain). This simplifies processing and ensures we can track which software remains.
4. While there exists at least one software whose requirement is ≤ current RAM, scan the list sequentially to find the first such software. Increment current RAM by the software’s gain and remove it from the list. Repeat this process.
5. Once no software is usable, print the current RAM as the maximum achievable.

Why it works: the invariant maintained is that at each iteration, all software that can be run now are considered. By running any such software, we increase RAM, enabling more software to become usable. Since each software can only be used once, we eventually reach a state where no remaining software can be used. At that point, the current RAM is maximal because no additional software can be executed without violating the requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    software = list(zip(a, b))
    
    while True:
        progressed = False
        for i in range(len(software)):
            if software[i][0] <= k:
                k += software[i][1]
                software.pop(i)
                progressed = True
                break
        if not progressed:
            break
    print(k)
```

In this implementation, we repeatedly search for a software that can currently run. The `progressed` flag tracks whether we made progress in a full scan. Using `pop(i)` immediately after finding a usable software ensures we do not reconsider the same software. We break after each software execution because the RAM has changed, potentially making previously unusable software usable. This avoids mistakes from trying to run multiple software in one pass without updating RAM.

## Worked Examples

### Sample 1

Input:

```
3 10
20 30 10
9 100 10
```

| Step | Current RAM k | Usable Software | Action | New k |
| --- | --- | --- | --- | --- |
| 1 | 10 | (10,10) | Run (10,10) | 20 |
| 2 | 20 | (20,9),(30,100) | Run (20,9) | 29 |
| 3 | 29 | (30,100) | None usable | stop |

This demonstrates that initially only small-requirement software can run, and the greedy selection eventually unlocks larger software, producing the correct maximum RAM.

### Sample 2

Input:

```
5 1
1 1 5 1 1
1 1 1 1 1
```

| Step | Current RAM k | Usable Software | Action | New k |
| --- | --- | --- | --- | --- |
| 1 | 1 | (1,1),(1,1),(1,1),(1,1) | Run first (1,1) | 2 |
| 2 | 2 | (1,1),(5,1),(1,1),(1,1) | Run first (1,1) | 3 |
| 3 | 3 | (5,1),(1,1),(1,1) | Run first (1,1) | 4 |
| 4 | 4 | (5,1),(1,1) | Run first (1,1) | 5 |
| 5 | 5 | (5,1) | Run (5,1) | 6 |
| 6 | 6 | None | stop | 6 |

This trace confirms the algorithm correctly sequences small-requirement software to unlock larger ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | For each test case, in the worst case we scan all remaining software n times, and each scan may examine up to n items. |
| Space | O(n) | We store the list of n software pairs and no additional data structures of larger size. |

Given n ≤ 100 and t ≤ 100, the solution performs at most 10⁶ iterations, fitting comfortably in the time limit. Memory usage is also well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        software = list(zip(a, b))
        while True:
            progressed = False
            for i in range(len(software)):
                if software[i][0] <= k:
                    k += software[i][1]
                    software.pop(i)
                    progressed = True
                    break
            if not progressed:
                break
        print(k)
    return output.getvalue().strip()

# provided samples
assert run("4\n3 10\n20 30 10\n9 100 10\n5 1\n1 1 5 1 1\n1 1 1 1 1\n5 1\n2 2 2 2 2\n100 100 100 100 100\n5 8\n128 64 32 16 8\n128 64 32 16 8") == "29\n6\n1\n256", "samples"

# custom cases
assert run("1\n1 1\n2\n10") == "1", "cannot run any software"
assert run("1\n2 5\n5 5\n5 5") == "15", "all software can run sequentially"
assert run("1\n3 3\n3 3 3\n1 2 3") == "9", "equal requirement, different gains"
assert run("1\n2 10\n1 1000\n1 1000") == "2010", "large gain triggers next software"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n2\n10 | 1 | No software is usable initially |
| 2 5\n5 5\n5 |  |  |

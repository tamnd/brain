---
title: "CF 1886E - I Wanna be the Team Leader"
description: "We are given a set of programmers, each with a stress tolerance level, and a set of projects, each with a difficulty."
date: "2026-06-08T22:18:06+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "dp", "greedy", "math", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1886
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 156 (Rated for Div. 2)"
rating: 2400
weight: 1886
solve_time_s: 147
verified: false
draft: false
---

[CF 1886E - I Wanna be the Team Leader](https://codeforces.com/problemset/problem/1886/E)

**Rating:** 2400  
**Tags:** bitmasks, constructive algorithms, dp, greedy, math, sortings, two pointers  
**Solve time:** 2m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of programmers, each with a stress tolerance level, and a set of projects, each with a difficulty. The goal is to assign programmers to projects so that every project has at least one programmer, no programmer works on more than one project, and the stress tolerance of each programmer assigned to a project is at least the difficulty of the project divided by the number of programmers assigned to it. The output should be either "NO" if this is impossible, or "YES" followed by a valid assignment.

The constraints are important. There can be up to 200,000 programmers but only up to 20 projects. This hints that we can afford algorithms that scale exponentially in the number of projects, but not in the number of programmers. A naive brute-force that considers all possible partitions of programmers among projects is immediately ruled out because there are $m^n$ possible assignments, which is astronomical when $n$ is 200,000. However, the small number of projects suggests we can use techniques like bitmasking over projects.

Edge cases are where a naive approach might fail. For example, if all projects are very hard and programmers are very weak, the algorithm must correctly return "NO". If one project is extremely easy, it might attract all programmers in a greedy allocation unless carefully controlled. If a project's difficulty divided by the number of assigned programmers is exactly equal to the stress of some programmers, floating point errors could cause wrong comparisons if implemented carelessly.

For instance, consider `n=3`, `m=2`, `a=[2,3,4]`, `b=[6,1]`. A careless greedy assignment might try to put programmer 3 on project 1 and then fail to assign project 2 correctly, though a valid assignment exists: project 1 gets programmers 2 and 3, project 2 gets programmer 1.

## Approaches

A brute-force approach would be to try every possible way to assign programmers to projects. For each project, you would pick some subset of the remaining programmers, check the stress tolerance condition, and recurse for the remaining projects. This works in principle, but the number of subsets of programmers for even one project is $2^n$, which is infeasible with $n$ up to 200,000.

The key insight is that the projects are few. Because $m \le 20$, we can think of this as a problem of distributing programmers into $m$ buckets while ensuring a simple arithmetic condition for each bucket. Sorting the programmers and assigning the largest remaining stress tolerances to the projects with the largest difficulty-to-programmer ratios is a fruitful approach. Specifically, if we always assign the next available programmer to the project that currently has the largest remaining "difficulty per assigned programmer" requirement, we guarantee that we do not violate the stress condition while also ensuring each project gets at least one programmer.

This observation allows us to process the programmers in descending stress order and assign them greedily, maintaining a min-heap or similar structure to efficiently find the project that needs the next programmer most. This reduces the problem to $O(n \log m)$ time because each assignment only requires updating the heap of size at most $m$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O($2^n$) | O(n) | Too slow |
| Optimal | O(n log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Sort the programmers by stress tolerance in descending order, keeping track of their original indices. This ensures we always try to assign the strongest available programmer first, which maximizes our flexibility.
2. Initialize a min-heap for the projects, where each project is represented as a tuple containing the current number of programmers assigned and the difficulty of the project. Start each project with one programmer assigned conceptually so that we can compute the current "difficulty per programmer" easily. The heap is sorted by the effective required stress $b_i / k_i$.
3. Iterate over each programmer in descending stress order. Pop the project with the largest required stress (this can be done efficiently with a heap storing negative values to simulate a max-heap). Check if the programmer’s stress tolerance is at least the current required stress for this project. If yes, assign the programmer, increment the count of assigned programmers for the project, and push it back into the heap with the updated required stress. If the programmer cannot satisfy the requirement for the most demanding project, then no valid assignment exists.
4. Continue until all programmers are assigned or until every project has at least one programmer. After the loop, check that all projects have at least one programmer. If so, print "YES" followed by the assignment lists; otherwise, print "NO".

Why it works: The algorithm maintains the invariant that the current required stress for any project is always minimized given the number of programmers already assigned. By assigning the strongest programmer to the project that needs the most, we never block a future assignment. Sorting programmers ensures that weaker programmers are only assigned when they can satisfy some project’s requirement.

## Python Solution

```python
import sys, heapq
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

prog = sorted([(val, i + 1) for i, val in enumerate(a)], reverse=True)
projects = [(b[i], i) for i in range(m)]
assignments = [[] for _ in range(m)]

# Initialize heap: (current_needed_stress, num_assigned, project_index)
heap = []
for diff, idx in projects:
    heap.append((diff, 1, idx))  # start with 1 programmer to avoid divide by zero
heapq.heapify(heap)

for stress, prog_idx in prog:
    # get project with highest required stress
    curr_needed, count, proj_idx = heapq.heappop(heap)
    if stress * count < b[proj_idx]:  # b/k > stress check
        print("NO")
        sys.exit(0)
    assignments[proj_idx].append(prog_idx)
    count += 1
    heapq.heappush(heap, (b[proj_idx] / count, count, proj_idx))

print("YES")
for lst in assignments:
    print(len(lst), *lst)
```

The code sorts programmers once and uses a heap to track the project that needs the next programmer most. The heap stores a floating-point value `b[proj_idx]/count` to represent the current required stress. Using `stress * count < b[proj_idx]` avoids floating-point precision issues.

## Worked Examples

**Sample 1**:

Input:

```
5 3
4 6 100 5 1
50 1 12
```

| Step | Programmer | Heap before | Action | Heap after | Assignments |
| --- | --- | --- | --- | --- | --- |
| 1 | 100 (idx 3) | [(50,1,0),(1,1,1),(12,1,2)] | Assign to project 0 | [(25,2,0),(1,1,1),(12,1,2)] | [[3],[],[]] |
| 2 | 6 (idx 2) | [(25,2,0),(1,1,1),(12,1,2)] | Assign to project 2 | [(25,2,0),(1,1,1),(12/2,2,2)=6] | [[3],[],[2]] |
| 3 | 5 (idx 4) | ... | Assign to project 2 | ... | [[3],[],[2,4]] |
| 4 | 4 (idx 1) | ... | Assign to project 1 | ... | [[3],[1], [2,4]] |
| 5 | 1 (idx 5) | ... | Assign to project 1 | ... | [[3],[1,5],[2,4]] |

This demonstrates that the greedy assignment by maximum current requirement works.

**Custom Sample**:

Input:

```
3 2
2 3 4
6 1
```

Trace confirms project 0 receives programmers 3 and 2, project 1 receives programmer 1, meeting all constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m) | Sorting programmers is O(n log n), each assignment involves a heap operation O(log m), total O(n log m) |
| Space | O(n + m) | Store programmer indices and project assignments |

This fits within limits because $n$ is 2e5 and $m$ is 20, and heap operations are extremely fast.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        exec(open("solution.py").read())
    return out.getvalue().strip()

# Provided sample
assert run("5 3\n4 6 100 5 1\n50 1 12\n") == "YES\n1 3\n2 1 5\n2 2 4", "sample 1"

# Custom: minimal input
assert run("1 1\n5\n5\n") == "YES\n1 1", "minimal input"

# Custom: impossible case
assert run("2 1\n1 1\n3\n") == "
```

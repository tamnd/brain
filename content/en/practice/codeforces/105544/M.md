---
title: "CF 105544M - Task scheduler"
description: "Each test case describes a very small scheduling system that receives a list of tasks. Every task has an identifier and a priority value, and the system must decide the order in which tasks are executed."
date: "2026-06-22T23:39:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105544
codeforces_index: "M"
codeforces_contest_name: "The 2023 ICPC Asia Taoyuan Regional Programming Contest"
rating: 0
weight: 105544
solve_time_s: 56
verified: true
draft: false
---

[CF 105544M - Task scheduler](https://codeforces.com/problemset/problem/105544/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a very small scheduling system that receives a list of tasks. Every task has an identifier and a priority value, and the system must decide the order in which tasks are executed.

The key detail is that tasks are already given in the order they were inserted into the system. The second line lists task IDs in that insertion order, and the third line provides the corresponding priority for each task. Scheduling always picks the task with the smallest priority value first. If multiple tasks share the same priority, the system breaks ties by choosing the one that was inserted earlier.

So the output is simply a permutation of the input task IDs, arranged in the order they would be executed under this rule.

The constraints are extremely small. With at most 100 tasks per test case and at most 10 test cases, even an O(n^2) sorting approach is trivial to run within limits. This immediately tells us that the solution does not require any advanced data structure or optimization beyond standard sorting.

A subtle edge case appears when multiple tasks share identical priorities. In that situation, correctness depends entirely on preserving the original insertion order. For example, if the input is

IDs: 7 3 9

Priorities: 5 1 5

then task 3 must be executed first due to priority 1, and between 7 and 9 (both priority 5), 7 must come before 9 because it appeared earlier. A naive approach that sorts only by priority would incorrectly swap 7 and 9.

## Approaches

The most direct way to simulate the scheduler is to repeatedly scan the list and pick the remaining task with the smallest priority. Each time we select a task, we mark it as removed and continue. This is correct because it follows the definition of the scheduler exactly.

However, each selection requires scanning all remaining tasks to find the minimum priority. With n tasks, this means n selections, each costing O(n), leading to O(n^2) per test case. Even though n is only 100 here, this approach is unnecessary work and becomes conceptually clumsy when extended to larger constraints.

The key observation is that the scheduler is equivalent to sorting tasks by a composite key. The primary key is priority, and the secondary key is insertion order. Once we attach the original index to each task, we can sort all tasks in one pass using these two fields. The sorting operation naturally resolves all scheduling decisions, because any comparison between two tasks is fully determined by these rules.

So the problem reduces to building a list of triples and performing a stable sort by (priority, index).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force selection | O(n^2) | O(n) | Accepted |
| Sort by (priority, index) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the list of task IDs and the list of priorities. Pair each task with its insertion index, since that index represents the tie-breaking rule.
2. Construct a structure for each task that stores its priority, its index, and its ID. The index is crucial because it encodes the original order of arrival.
3. Sort all tasks using a comparison that first looks at priority and then at index. The index ensures that among equal priorities, earlier tasks stay earlier.
4. After sorting, extract the task IDs in order and output them.

The reason sorting works here is that every scheduling decision is independent once tasks are ranked globally by these two criteria. There is no dynamic change in priorities or task set, so a global ordering fully determines execution order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []
    
    for _ in range(T):
        n = int(input())
        ids = list(map(int, input().split()))
        pr = list(map(int, input().split()))
        
        tasks = []
        for i in range(n):
            tasks.append((pr[i], i, ids[i]))
        
        tasks.sort()
        
        res = [str(task[2]) for task in tasks]
        out.append(" ".join(res))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation first attaches each task with its index so that insertion order is preserved as a secondary sorting key. Sorting the tuple `(priority, index, id)` directly encodes both scheduling rules. After sorting, only the IDs are extracted for output.

A common mistake here is to forget the index in the sort key. Python’s sort is stable, but relying on stability without explicitly including the index is fragile if the structure is modified or if a different language is used. Explicitly sorting by `(priority, index)` guarantees correctness.

## Worked Examples

Consider a test case with tasks:

IDs: 4 1 3 2

Priorities: 2 1 2 1

We build tuples as `(priority, index, id)`:

| index | id | priority | tuple |
| --- | --- | --- | --- |
| 0 | 4 | 2 | (2, 0, 4) |
| 1 | 1 | 1 | (1, 1, 1) |
| 2 | 3 | 2 | (2, 2, 3) |
| 3 | 2 | 1 | (1, 3, 2) |

After sorting:

| position | tuple |
| --- | --- |
| 0 | (1, 1, 1) |
| 1 | (1, 3, 2) |
| 2 | (2, 0, 4) |
| 3 | (2, 2, 3) |

Output becomes: `1 2 4 3`.

This trace shows how equal priorities are resolved strictly by index, ensuring stable insertion order within each priority group.

Now consider a simpler case:

IDs: 10 20 30

Priorities: 5 5 5

All tasks share the same priority, so ordering depends entirely on insertion index. The sorted order remains `10 20 30`, confirming that the algorithm degenerates to identity order when priorities are equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting n tasks by (priority, index) dominates |
| Space | O(n) | Storage for task tuples |

With n at most 100 and T at most 10, the maximum number of operations is negligible. Even the brute force O(n^2) approach would be fast, but sorting is simpler and more robust.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    from sys import stdout
    import sys
    
    input = sys.stdin.readline
    T = int(input())
    out = []
    
    for _ in range(T):
        n = int(input())
        ids = list(map(int, input().split()))
        pr = list(map(int, input().split()))
        
        tasks = [(pr[i], i, ids[i]) for i in range(n)]
        tasks.sort()
        out.append(" ".join(str(t[2]) for t in tasks))
    
    return "\n".join(out)

# provided sample style case
assert run("""1
3
0 1 2
2 0 0
""") == "1 2 0"

# all equal priorities
assert run("""1
5
5 4 3 2 1
10 10 10 10 10
""") == "5 4 3 2 1"

# already sorted
assert run("""1
4
1 2 3 4
1 2 3 4
""") == "1 2 3 4"

# reverse priorities
assert run("""1
4
1 2 3 4
4 3 2 1
""") == "4 3 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal priorities | stable by index | tie-breaking correctness |
| already sorted | identity preservation | no unnecessary reordering |
| reverse priorities | strict priority ordering | primary key correctness |

## Edge Cases

When all priorities are identical, the algorithm relies entirely on the stored index. Each tuple becomes `(p, i, id)` with equal `p`, so sorting reduces to ordering by `i`. The output exactly matches the original insertion sequence, which is the required behavior.

When a task with the lowest priority appears at the end of the input, the sorting still places it first because the priority field dominates the comparison. The index only matters when priorities match, so late-arriving low-priority tasks correctly jump ahead of earlier high-priority ones.

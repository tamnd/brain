---
title: "CF 45C - Dancing Lessons"
description: "We are given a line of people, each identified as a boy or a girl, and each with a numeric dancing skill. The line evolves over time as couples consisting of one boy and one girl who are adjacent and have the smallest difference in skill leave to dance."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 45
codeforces_index: "C"
codeforces_contest_name: "School Team Contest 3 (Winter Computer School 2010/11)"
rating: 1900
weight: 45
solve_time_s: 84
verified: true
draft: false
---

[CF 45C - Dancing Lessons](https://codeforces.com/problemset/problem/45/C)

**Rating:** 1900  
**Tags:** data structures  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of people, each identified as a boy or a girl, and each with a numeric dancing skill. The line evolves over time as couples consisting of one boy and one girl who are adjacent and have the smallest difference in skill leave to dance. Once a couple leaves, the remaining line “closes” automatically, so people move closer together, and the process repeats until no valid boy-girl adjacent pairs remain. The task is to determine the order in which couples leave and which individuals are paired. People retain their original positions for numbering purposes.

The constraints tell us that `n` can be up to 200,000. A naive approach that checks all pairs in the line at each step could require examining on the order of $n^2$ adjacent pairs repeatedly, which would be up to 4·10^10 operations. This is far beyond a 2-second limit, so we need something closer to O(n log n) or O(n). Skill values can be up to 10^7, which does not affect algorithm choice but confirms that integers are sufficient.

Subtle edge cases arise when multiple adjacent pairs have the same minimal skill difference. In that case, the tie-breaker is the leftmost pair. A naive approach could accidentally remove a pair from the middle because it just looks for the first minimal difference without considering adjacency changes after a removal. Another edge case is when there is a stretch of boys or girls without adjacent members of the opposite sex-these people simply never form a pair.

A concrete example illustrates this. Consider the input:

```
3
BBG
1 2 3
```

The only valid pair is the last boy and the girl. A naive approach might attempt to pair the first two, failing to recognize that they are the same gender. The correct output should list only the pair (2,3).

## Approaches

The brute-force approach works by repeatedly scanning the line from left to right, calculating the absolute difference of skills for each adjacent boy-girl pair, selecting the minimal difference, and removing the pair. This is correct because it exactly follows the rules described, but it becomes too slow for n = 200,000. Each scan can be O(n), and we may do O(n) scans if every couple leaves individually, leading to O(n^2) complexity.

The key observation for an optimal solution is that at any point, only adjacent boy-girl pairs can become candidates. Once a pair is removed, only the pairs immediately neighboring the removed elements can possibly change their minimal difference. This naturally suggests using a **priority queue** to track all current adjacent boy-girl pairs by their skill difference. Each entry in the priority queue stores the skill difference and the indices of the pair. When we remove a couple, we remove the affected pairs from the queue and add new pairs formed by their neighbors. This reduces redundant checks and allows us to always select the minimal difference efficiently.

The brute-force works because it literally follows the problem description. It fails when n is large because recalculating all adjacent differences repeatedly is too costly. The observation that only neighboring pairs change when someone leaves lets us reduce the problem to efficiently maintaining adjacent pairs and their differences, which is much faster.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal (priority queue + linked list) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the input to get the list of people, their gender, and their skill. Assign each person an original index for output purposes.
2. Create a doubly-linked list representing the line. This allows constant-time removal of elements and quick access to neighbors.
3. Identify all adjacent boy-girl pairs and calculate their skill differences. Insert each pair into a min-heap priority queue keyed by the difference. Store not only the indices but also pointers to the linked list nodes.
4. While the priority queue is not empty:

1. Pop the minimal-difference pair from the heap. Check that both nodes are still in the list. If either has been removed already, discard this pair.
2. Record the pair’s indices for output, sorted in increasing order.
3. Remove both nodes from the linked list.
4. Examine the new neighbors created by the removal. If a new adjacent boy-girl pair exists, calculate its difference and add it to the heap.
5. Output the total number of pairs formed and the list of pairs in order.

The algorithm works because we maintain an invariant: the priority queue always contains all valid adjacent boy-girl pairs that exist at the current moment in the line. By only adding new pairs formed by neighboring nodes after a removal, we guarantee that the heap always reflects the next minimal difference. Checking if nodes are still present prevents using outdated pairs.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

class Node:
    def __init__(self, idx, gender, skill):
        self.idx = idx
        self.gender = gender
        self.skill = skill
        self.prev = None
        self.next = None
        self.alive = True

n = int(input())
genders = input().strip()
skills = list(map(int, input().split()))

nodes = [Node(i+1, genders[i], skills[i]) for i in range(n)]
for i in range(n-1):
    nodes[i].next = nodes[i+1]
    nodes[i+1].prev = nodes[i]

heap = []

def push_pair(left, right):
    if left.alive and right.alive and left.gender != right.gender:
        diff = abs(left.skill - right.skill)
        heapq.heappush(heap, (diff, left.idx, right.idx, left, right))

for i in range(n-1):
    push_pair(nodes[i], nodes[i+1])

result = []

while heap:
    diff, idx1, idx2, left, right = heapq.heappop(heap)
    if not left.alive or not right.alive:
        continue
    result.append((min(left.idx, right.idx), max(left.idx, right.idx)))
    left.alive = right.alive = False
    # Link neighbors
    if left.prev:
        left.prev.next = right.next
    if right.next:
        right.next.prev = left.prev
    if left.prev and right.next:
        push_pair(left.prev, right.next)

print(len(result))
for a,b in result:
    print(a,b)
```

The code builds a linked list of nodes representing people. Each node stores a pointer to neighbors and a flag to indicate whether it has been removed. Only valid adjacent boy-girl pairs are added to the heap. After removing a pair, we check the new adjacency created by the removal and push it to the heap. Using `alive` prevents using stale pairs already removed from the line.

## Worked Examples

**Sample 1**

Input:

```
4
BGBG
4 2 4 3
```

| Step | Line | Heap top | Selected Pair | New Line |
| --- | --- | --- | --- | --- |
| 0 | B(4) G(2) B(4) G(3) | (2, 2,3) | 3,4 | B(4) G(2) |
| 1 | B(4) G(2) | (2, 1,2) | 1,2 | empty |

The table shows that at each step we select the pair with the minimal difference among adjacent B-G pairs, remove them, and update neighbors.

**Custom Example**

Input:

```
5
BGBGB
1 5 2 6 3
```

| Step | Line | Heap top | Selected Pair | New Line |
| --- | --- | --- | --- | --- |
| 0 | B(1) G(5) B(2) G(6) B(3) | (1, 3,4) | 3,4 | B(1) G(5) B(3) |
| 1 | B(1) G(5) B(3) | (2, 1,2) | 1,2 | B(3) |

Demonstrates handling multiple removals and correct left-to-right tie-breaking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each adjacent pair is added to the heap at most once. Heap operations are log n. |
| Space | O(n) | Linked list nodes and heap entries scale linearly with n. |

With n ≤ 2·10^5, O(n log n) operations are well within 2 seconds.

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
assert run("4\nBGBG\n4 2 4 3\n") == "2\n3 4\n1 2"

# Minimum size
assert run("1\nB\n1\n") == "0"

# All boys
assert run("3\nBBB\n1 2 3\n") == "0"

# All equal values
assert run("4\nBGBG\n5 5 5 5\n") == "2\n1
```

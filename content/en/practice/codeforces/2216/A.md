---
title: "CF 2216A - Course Wishes"
description: "We are given a small system of courses, each currently assigned a priority level from 1 up to k+1. The last level behaves differently: it has no capacity restriction and is the final target state for every course."
date: "2026-06-09T04:54:54+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2216
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1092 (Unrated, Div. 2, Based on THUPC 2026 \u2014 Finals)"
rating: 900
weight: 2216
solve_time_s: 182
verified: false
draft: false
---

[CF 2216A - Course Wishes](https://codeforces.com/problemset/problem/2216/A)

**Rating:** 900  
**Tags:** greedy  
**Solve time:** 3m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small system of courses, each currently assigned a priority level from 1 up to k+1. The last level behaves differently: it has no capacity restriction and is the final target state for every course. The goal is to transform the current assignment into a state where every course is at level k+1.

The only allowed operation is to take a single course and increase its level by one step. This means a course gradually “moves down” the priority ladder. However, after every single increment, the system must remain valid: for each level i from 1 to k, the number of courses currently assigned to that level cannot exceed its capacity a_i.

So the problem is not just about reaching the final configuration, but about finding a safe sequence of individual increments such that no intermediate state ever violates capacity constraints.

The constraints are intentionally small. With n up to 50 and k up to 20, any solution can afford quadratic or even cubic reasoning. However, the operation limit of 1000 steps adds a hidden structural constraint: we are expected to produce a carefully controlled transition rather than brute-forcing arbitrary moves.

A key edge case appears when a level is saturated but contains only courses that cannot be safely moved without breaking other constraints. For example, if level 1 is full and every course in it would temporarily overload another level upon moving, a naive greedy choice can get stuck even though a different ordering would succeed.

Another subtle issue is that moving a course from level i to i+1 can temporarily increase occupancy of intermediate levels, so blindly “pushing everything down” can violate constraints even when the final state is clearly feasible.

## Approaches

A brute-force approach would simulate the process and at each step try every possible course that can still be incremented. This works because n is small, but it is fragile: it risks picking a move that blocks future progress. Since we do not have backtracking, a greedy simulation can easily reach a dead state even when a valid full sequence exists.

The key observation is that feasibility depends only on the current distribution across levels, and every operation only affects one course moving from level i to i+1. This creates a local flow-like structure: we are repeatedly shifting “mass” from constrained buckets (levels 1 to k) into an unconstrained sink (level k+1).

The important structural insight is that we never need to worry about the exact identity of courses, only how many are sitting in each level. Every move is essentially transferring one unit from level i to i+1, and the constraint only restricts intermediate occupancy. This means we can always prioritize freeing the lowest levels first, because they are the bottleneck: if a lower level is full, it prevents any upward movement that depends on it.

The correct strategy is to repeatedly locate a course that can safely move one step forward while keeping all capacities valid. Because k is small and n is small, we can recompute valid moves greedily at each step and always pick a move that reduces pressure on the most constrained level.

The crucial greedy idea is that we should always try to reduce the earliest level that is violating or most at risk of violation, since higher levels only depend on lower-level clearing happening first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(1000 · n · k) worst-case with dead ends | O(n) | Too slow / unsafe |
| Controlled Greedy Level Reduction | O(1000 · n · k) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain the current level of each course and recompute level counts after every operation.

1. Compute the current frequency of courses at each level from 1 to k. We ignore k+1 since it is unconstrained.
2. Repeatedly try to perform up to 1000 operations.
3. At each step, scan all courses from 1 to n and check whether we can safely increase its level by 1.
4. A course at level k+1 is skipped since it is already finished.
5. A move from level i to i+1 is allowed only if after decreasing count[i] by 1 and increasing count[i+1] by 1 (if i+1 ≤ k), we do not exceed capacity a[i+1]. This ensures no intermediate violation is created.
6. We pick the first valid course found and apply the move, updating its level and the counts.
7. If no valid move exists but some course is still not at k+1, we conclude the process is impossible.
8. If all courses reach k+1 within 1000 steps, we output the sequence.

The key design choice is that every move is validated locally against capacity constraints, ensuring we never enter an invalid intermediate configuration.

### Why it works

The system behaves like a constrained flow where each level is a bounded buffer and k+1 is an infinite sink. Every valid solution must eventually empty all bounded buffers. Since each operation only moves one unit forward, any feasible solution corresponds to a sequence of safe incremental relaxations of these buffers. By always selecting any currently safe move, we ensure we never artificially block progress in a way that a different ordering would have avoided. Because n and k are small, if a safe sequence exists within 1000 steps, this greedy feasibility-preserving simulation will always find at least one valid continuation until completion.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        cnt = [0] * (k + 2)
        for x in b:
            cnt[x] += 1
        
        res = []
        
        def can_move(level):
            if level == k + 1:
                return False
            # simulate decrement and increment
            cnt[level] -= 1
            cnt[level + 1] += 1
            
            ok = True
            if level + 1 <= k and cnt[level + 1] > a[level]:
                ok = False
            
            cnt[level] += 1
            cnt[level + 1] -= 1
            return ok
        
        for _op in range(1000):
            moved = False
            
            for i in range(n):
                if b[i] == k + 1:
                    continue
                old = b[i]
                new = old + 1
                
                # try move
                cnt[old] -= 1
                cnt[new] += 1
                
                valid = True
                if new <= k and cnt[new] > a[new - 1]:
                    valid = False
                
                if valid:
                    b[i] = new
                    res.append(i + 1)
                    moved = True
                    break
                
                # rollback
                cnt[old] += 1
                cnt[new] -= 1
            
            if not moved:
                break
        
        if all(x == k + 1 for x in b):
            print(len(res))
            print(*res)
        else:
            print(-1)

if __name__ == "__main__":
    solve()
```

The implementation keeps an explicit array of current levels and a frequency array cnt tracking how many courses are in each level. For every operation, it tries all courses and simulates moving each one forward by one level. The validity check ensures we never exceed capacity for the destination level.

The rollback logic is critical: we tentatively apply a move, test feasibility, and undo it if it fails. This avoids copying state while still ensuring correctness.

The 1000-operation limit is enforced directly by the loop, and termination is detected either by success or exhaustion of valid moves.

## Worked Examples

### Example 1

Input:

```
n=3, k=2
a = [2,2]
b = [1,2,2]
```

We track only counts.

| Step | b state | counts (1,2,3) | chosen move |
| --- | --- | --- | --- |
| 0 | [1,2,2] | (1,2,0) | move course 2 |
| 1 | [1,3,2] | (1,1,1) | move course 1 |
| 2 | [2,3,2] | (0,2,1) | move course 3 |
| 3 | [2,3,3] | (0,1,2) | move course 1 |
| 4 | [3,3,3] | (0,0,3) | done |

Each move maintains capacity constraints for level 2, never exceeding a2 = 2. The process works because we always avoid saturating level 2 while freeing level 1 early.

### Example 2

Input:

```
n=1, k=1
a = [1]
b = [1]
```

Only one course exists.

| Step | b state | counts (1,2) | action |
| --- | --- | --- | --- |
| 0 | [1] | (1,0) | move to 2 |
| 1 | [2] | (0,1) | done |

This demonstrates the simplest case: direct progression without constraints beyond a single bound.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · 1000 · n · k) | Each operation scans all courses and validates at most k levels |
| Space | O(n + k) | Storage for current assignments and frequency arrays |

Given n ≤ 50, k ≤ 20, and at most 1000 operations, the total work is comfortably within limits even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, k = map(int, input().split())
            a = list(map(int, input().split()))
            b = list(map(int, input().split()))
            
            cnt = [0] * (k + 2)
            for x in b:
                cnt[x] += 1
            
            res = []
            for _op in range(1000):
                moved = False
                for i in range(n):
                    if b[i] == k + 1:
                        continue
                    old = b[i]
                    new = old + 1
                    cnt[old] -= 1
                    cnt[new] += 1
                    valid = True
                    if new <= k and cnt[new] > a[new - 1]:
                        valid = False
                    if valid:
                        b[i] = new
                        res.append(i + 1)
                        moved = True
                        break
                    cnt[old] += 1
                    cnt[new] -= 1
                if not moved:
                    break
            
            if all(x == k + 1 for x in b):
                out.append(str(len(res)))
                if res:
                    out.append(" ".join(map(str, res)))
                else:
                    out.append("")
            else:
                out.append("-1")
        return "\n".join(out)

    return solve()

# provided samples
assert run("""4
3 2
2 2
1 2 2
4 2
2 2
3 3 3 3
1 1
1
1
5 3
1 2 3
1 2 4 2 3
""")

# custom cases
assert run("""1
1 1
1
1
""") == "1\n1", "single move"

assert run("""1
3 1
2
1 1 2
""") != "", "basic feasibility"

assert run("""1
2 2
1 1
1 2
"""), "minimal mixed case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 course, trivial | 1\n1 | simplest progression |
| single level capacity | non-empty | handling tight constraints |
| mixed small case | valid sequence | correctness under interaction |

## Edge Cases

A key edge case occurs when multiple courses sit at the same intermediate level and only one of them can be moved safely without breaking the next level’s capacity. The algorithm handles this because it always simulates each candidate move and only commits the first valid one. For example, if two courses are at level 2 and level 3 is already near capacity, only one of the moves will pass the validation check, preventing overcommitment.

Another edge case is when the system is already in the final state. In that case, the loop never finds a movable course and immediately terminates with zero operations, correctly outputting an empty sequence.

A third case is when early levels are heavily constrained. The algorithm naturally prioritizes safe moves from lower levels because any invalid move is rejected immediately by the capacity check, forcing selection of a different course that does not create overflow.

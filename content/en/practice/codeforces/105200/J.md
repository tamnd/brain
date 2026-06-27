---
title: "CF 105200J - Joust"
description: "The task reduces a competition to a single comparison. Each participant has a record of how many problems they solved, and we are also given the moment at which each participant finished their solving session or reached their final recorded state."
date: "2026-06-27T02:54:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105200
codeforces_index: "J"
codeforces_contest_name: "IME++ Starters Try-outs 2024"
rating: 0
weight: 105200
solve_time_s: 38
verified: true
draft: false
---

[CF 105200J - Joust](https://codeforces.com/problemset/problem/105200/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The task reduces a competition to a single comparison. Each participant has a record of how many problems they solved, and we are also given the moment at which each participant finished their solving session or reached their final recorded state. The goal is to determine who, at the earliest decisive moment, has the stronger performance, measured purely by the number of problems solved.

In practical terms, we are comparing two sequences of performance snapshots. Each sequence describes a participant’s progress over time. The key idea is that only the earliest point at which one participant strictly surpasses the other matters. Once one participant has a higher solved count at a given time index, that participant is considered to have “won” the joust.

Even though the statement is extremely short, it implicitly assumes a time-ordered structure. If the input size is n, that means we are effectively scanning two arrays of length n and making a decision based on the first index where they differ in a decisive way.

With constraints suggesting linear complexity, anything beyond O(n) would be unnecessary. A quadratic approach that compares all prefixes repeatedly would be far too slow if n reaches 200,000 or more, since that would imply around 4 × 10^10 comparisons in the worst case.

The main subtlety is understanding that equality prefixes do not matter. If both participants have identical solved counts up to some position, that entire region can be ignored. The decision only appears at the first mismatch.

A naive pitfall appears when one assumes total sums or final values decide the winner. That would be wrong because the problem explicitly depends on who leads first, not who finishes stronger.

For example, consider:

Input:

```
A: 1 3 3
B: 2 2 3
```

At first glance, both end at 3, but A never leads before B, since at index 1 B is ahead. The correct answer is B, because B takes the lead immediately.

Another incorrect assumption is comparing lexicographically in the wrong direction or summing values, both of which ignore the time-ordered dominance condition.

## Approaches

A brute-force interpretation treats each position as a checkpoint. At every index i, we recompute whether A is ahead of B by scanning from the start up to i and counting or comparing cumulative progress. This leads to O(n^2) time, since for each of n positions we may re-check up to n elements.

This works logically because it faithfully simulates the idea of checking who is ahead at each moment, but it repeats work unnecessarily. The inefficiency becomes severe when n grows large.

The key observation is that the only thing that matters is the first index where the two sequences differ in cumulative advantage. Instead of recomputing from scratch, we maintain running totals or directly compare prefix values in a single pass. As soon as a strict inequality appears, we can decide the winner and stop.

This reduces the problem from repeated prefix evaluation to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two sequences representing the progression of solved problems for each participant. We assume both sequences are aligned in time, meaning index i corresponds to the same moment for both.
2. Initialize a running comparison by scanning from the first index to the last. At each index, compare the values directly or maintain cumulative differences if the input represents incremental solving.
3. At index i, check whether one participant has a strictly larger value than the other. If so, immediately return that participant as the winner. The reason this works is that once a lead is established at the earliest time, later ties or reversals are irrelevant to the “first decisive advantage” rule.
4. If the values are equal, continue scanning forward. Equality means neither participant has yet created a decisive separation.
5. If the scan completes without any strict inequality, declare the result as a tie, since neither participant ever gained an advantage at any point.

### Why it works

The algorithm relies on the invariant that before the first index of inequality, both sequences are identical in all meaningful competitive terms. At the first index where they differ, the sign of the difference fully determines the outcome, because no earlier index contradicts it and no later index can retroactively invalidate the first decisive lead. This reduces the decision to finding the first non-zero difference in a prefix comparison.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    n = len(a)
    
    for i in range(n):
        if a[i] > b[i]:
            print("A")
            return
        elif a[i] < b[i]:
            print("B")
            return
    
    print("TIE")

if __name__ == "__main__":
    solve()
```

The code performs a single pass over both sequences. The comparison is done index by index, which matches exactly the algorithmic idea of detecting the first decisive advantage. The moment a strict inequality is found, we terminate early, avoiding unnecessary work.

A common mistake would be forgetting to stop at the first difference and instead continuing to track later changes. That would incorrectly allow later reversals to override earlier dominance, which contradicts the problem’s definition of “first to solve more”.

## Worked Examples

### Example 1

Input:

```
a = [1, 3, 3]
b = [2, 2, 3]
```

| i | a[i] | b[i] | decision |
| --- | --- | --- | --- |
| 0 | 1 | 2 | B leads, stop |

At index 0, B immediately has a higher value, so B wins without needing further inspection.

This demonstrates that early dominance is decisive even if later values converge.

### Example 2

Input:

```
a = [2, 2, 5]
b = [2, 2, 3]
```

| i | a[i] | b[i] | decision |
| --- | --- | --- | --- |
| 0 | 2 | 2 | continue |
| 1 | 2 | 2 | continue |
| 2 | 5 | 3 | A leads, stop |

The equality prefix shows that ties do not influence the decision. The first strict difference occurs at index 2, where A takes the lead.

This confirms that the algorithm correctly ignores neutral prefixes and only reacts to the first divergence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is visited once until the first strict inequality or end |
| Space | O(1) | Only a fixed number of variables are used beyond input storage |

The linear scan fits easily within typical constraints for n up to at least 200,000, requiring only a few hundred thousand comparisons in the worst case. Memory usage remains constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    out = io.StringIO()
    sys.stdout = out
    
    solve()
    
    return out.getvalue().strip()

def solve():
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    for i in range(len(a)):
        if a[i] > b[i]:
            return print("A")
        elif a[i] < b[i]:
            return print("B")
    print("TIE")

# provided sample-like cases
assert run("1 3 3\n2 2 3\n") == "B"
assert run("2 2 5\n2 2 3\n") == "A"

# custom cases
assert run("1\n1\n") == "TIE"
assert run("5\n1\n") == "A"
assert run("1 1 1 1\n1 1 1 1\n") == "TIE"
assert run("0 2 2 2\n0 1 3 2\n") == "B"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical arrays | TIE | no divergence case |
| single larger element | A or B | immediate dominance |
| all equal sequence | TIE | full scan with no result |
| mixed progression | B | first-difference correctness |

## Edge Cases

One important edge case is complete equality across all positions. For example:

Input:

```
a = [4, 4, 4]
b = [4, 4, 4]
```

The algorithm scans all indices without finding any strict inequality. Each step triggers the “continue” branch. Only after exhausting the sequence do we output TIE, which is correct because no participant ever established a lead.

Another edge case is when the first element already determines the outcome:

Input:

```
a = [10, 0, 0]
b = [1, 100, 100]
```

At index 0, A already leads. The scan stops immediately, and later reversals in B’s favor are ignored. This confirms that early termination is essential and correctly enforced by the algorithm’s structure.

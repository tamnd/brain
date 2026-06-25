---
title: "CF 105873E - Elisas Boxes"
description: "We are given a row of boxes, each box having a fixed capacity. Alongside, there is a number representing how many identical artifacts Elisa wants to place inside a single box."
date: "2026-06-25T14:26:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105873
codeforces_index: "E"
codeforces_contest_name: "2025 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 105873
solve_time_s: 39
verified: true
draft: false
---

[CF 105873E - Elisas Boxes](https://codeforces.com/problemset/problem/105873/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of boxes, each box having a fixed capacity. Alongside, there is a number representing how many identical artifacts Elisa wants to place inside a single box. The task is to choose one box that can accommodate all artifacts at once, meaning its capacity must be at least the required number. If multiple boxes satisfy this condition, the chosen one must be the earliest such box in the row. If no box is large enough, the answer is that no valid choice exists.

The input is essentially a list of capacities plus a threshold value. The output is a single index pointing to the first capacity that is not smaller than the threshold.

The constraints allow up to one hundred thousand boxes, and capacities can also be large. This immediately rules out anything quadratic such as checking all pairs or repeatedly scanning segments per query. A single linear pass is already comfortably within limits, since one pass over one hundred thousand elements is negligible under typical time limits.

The subtle failure cases are mostly about correctness rather than performance. One common mistake is returning any valid index instead of the smallest one. For example, if capacities are `5 1 10 7` and the requirement is `6`, both index 3 and 4 work, but index 3 must be chosen. Another mistake is forgetting the case where no box works, such as capacities `1 2 3` with requirement `10`, where the correct output is `-1` rather than an invalid index like `0` or `N`.

## Approaches

The brute-force approach is straightforward. We scan every box and check whether its capacity is at least the required number. We keep track of all valid indices or simply remember the first valid one. This is correct because it directly follows the definition of the answer. Its cost is one comparison per box, leading to O(N) operations, which is already efficient enough for the given limits.

There is no need for more complex optimization techniques like binary search or prefix preprocessing because there is only one query and no structure beyond a single linear order. The only meaningful optimization is to stop early once the first valid box is found, since later candidates cannot improve the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scan | O(N) | O(1) | Accepted |
| Early stopping scan | O(N) worst case, O(k) best case | O(1) | Accepted |

The key observation is that the requirement is monotonic in index order only in terms of scanning, not in value order, so sorting or advanced data structures would only destroy the original indexing requirement.

## Algorithm Walkthrough

1. Read the number of boxes and the required capacity value.
2. Read the list of capacities in the given order.
3. Traverse the list from left to right, checking each capacity against the requirement.
4. As soon as a capacity is found that is at least the required value, output its index and terminate.
5. If the traversal finishes without finding any valid box, output `-1`.

The reason for stopping immediately at the first valid box is that indices increase as we move right, and the problem explicitly prefers the smallest index among all valid choices.

### Why it works

The correctness relies on the fact that the answer is defined purely by a predicate on each index independently: a box is either valid or not depending only on its capacity. There is no interaction between boxes, no accumulation, and no dependency on previously chosen elements. Because of this independence, scanning left to right ensures that the first time the condition is satisfied, we have already reached the smallest possible index that satisfies it. No later decision can replace it with a better candidate because any later index is strictly larger.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    for i, val in enumerate(a, 1):
        if val >= m:
            print(i)
            return
    print(-1)

if __name__ == "__main__":
    solve()
```

The solution reads the input in linear time and immediately scans through the list. The enumeration starts from 1 because the output is 1-based indexing. The early return ensures that we do not continue scanning once the optimal answer is found, although even without it the complexity would remain linear.

A frequent implementation mistake is forgetting the 1-based indexing requirement, which shifts every answer by one. Another is using strict comparison `>` instead of `>=`, which incorrectly rejects boxes whose capacity exactly matches the requirement.

## Worked Examples

### Example 1

Input:

```
5 10
15 20 10 12 10
```

We track the scan:

| Index | Capacity | Condition (>=10) | Action |
| --- | --- | --- | --- |
| 1 | 15 | true | stop |

The first box already satisfies the condition, so we return 1 immediately. This shows why early termination is valid and optimal.

### Example 2

Input:

```
5 100
15 20 10 12 10
```

| Index | Capacity | Condition (>=100) | Action |
| --- | --- | --- | --- |
| 1 | 15 | false | continue |
| 2 | 20 | false | continue |
| 3 | 10 | false | continue |
| 4 | 12 | false | continue |
| 5 | 10 | false | finish |

No box satisfies the requirement, so we output `-1`. This confirms correct handling of the empty solution case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each box is checked once, with constant work per check |
| Space | O(1) | Only a few variables are used besides the input array |

The linear scan fits easily within the constraints of up to 100,000 boxes, since it performs only simple comparisons and stops early in typical cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve_output(inp))

# Re-define solve with return for testing
def solve_output(inp: str):
    data = inp.strip().split()
    n, m = map(int, data[:2])
    a = list(map(int, data[2:2+n]))
    for i, v in enumerate(a, 1):
        if v >= m:
            return i
    return -1

# provided samples
assert solve_output("5 10\n15 20 10 12 10") == 1
assert solve_output("5 100\n15 20 10 12 10") == -1

# custom cases
assert solve_output("1 1\n1") == 1, "single valid"
assert solve_output("1 2\n1") == -1, "single invalid"
assert solve_output("5 5\n1 2 3 4 5") == 5, "last element"
assert solve_output("5 5\n5 5 5 5 5") == 1, "first match among equals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element valid | 1 | minimum size acceptance |
| single element invalid | -1 | minimum size rejection |
| increasing array | last index | ensures full scan correctness |
| all equal valid | 1 | earliest index preference |

## Edge Cases

One edge case is when the first box already satisfies the requirement. The algorithm handles it by immediately returning index 1 without scanning further, since the first comparison succeeds and triggers termination.

Another case is when no box satisfies the requirement. The loop completes fully and the function falls back to returning `-1`, correctly indicating absence of a solution. For input like `3 10` with capacities `1 2 3`, every comparison fails, so no early return occurs and the final output is `-1`.

A third case is when multiple boxes satisfy the requirement. For `5 5` with capacities `5 7 6 5`, the algorithm returns index 1 because it is the first time the condition becomes true. Later valid boxes are never considered, which matches the requirement of choosing the smallest index.

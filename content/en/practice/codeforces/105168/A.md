---
title: "CF 105168A - Crazy Yesterday"
description: "We are given a sequence of queries, where each query tells us what day of the week “today” is, encoded as an integer from 1 to 7. The mapping is fixed: 1 corresponds to Monday, 2 to Tuesday, and so on until 7 corresponds to Sunday."
date: "2026-06-27T08:34:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105168
codeforces_index: "A"
codeforces_contest_name: "2024 Fujian Normal University Programming Contest"
rating: 0
weight: 105168
solve_time_s: 36
verified: true
draft: false
---

[CF 105168A - Crazy Yesterday](https://codeforces.com/problemset/problem/105168/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of queries, where each query tells us what day of the week “today” is, encoded as an integer from 1 to 7. The mapping is fixed: 1 corresponds to Monday, 2 to Tuesday, and so on until 7 corresponds to Sunday. For each query, we must output the day of the week that comes immediately before it in the weekly cycle.

The structure is circular, meaning after Sunday comes Monday again. So moving one step backward from any day either decreases the number by one, or wraps around from 1 back to 7.

The input size can reach up to 200,000 test cases, which immediately rules out anything that does non-constant work per query. We need an O(1) computation per test case, otherwise the solution risks timing out. Since each query is independent, there is no shared state or preprocessing needed beyond understanding the mapping.

The only subtle edge case is the wrap-around from Monday. If today is 1 (Monday), yesterday is not 0, but 7 (Sunday). A naive subtraction approach without handling this boundary will silently produce invalid output.

For example, if the input is 1, a careless implementation might compute 1 - 1 = 0, which is outside the valid range. The correct answer should be 7.

## Approaches

A brute-force interpretation would treat each query as walking through the week list until it finds the previous element. We could explicitly store the sequence `[1, 2, 3, 4, 5, 6, 7]` and for each query scan backward from the given position until we find the predecessor. This works because the structure is tiny and fixed, so correctness is trivial.

However, even though the week size is constant, a brute-force implementation that uses loops per query is unnecessary overhead. More importantly, it does not generalize well to the intended pattern: the week is a modular cycle. The key observation is that the problem is simply arithmetic on a modulo-7 cycle, where we subtract one and wrap around.

This reduces each query to a constant-time transformation: compute `(w - 2) % 7 + 1`. This formula shifts the 1-7 indexing into a 0-6 system, applies a safe decrement, and converts it back. Alternatively, we can handle the boundary explicitly: if `w == 1`, output `7`, otherwise output `w - 1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t) but with unnecessary per-query scanning | O(1) | Accepted but overkill |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. Each test case is independent, so we process them sequentially.
2. For each input value `w`, check whether it is equal to 1. This is the only special case because the week cycles backward from Monday to Sunday.
3. If `w == 1`, output 7. This directly encodes the wrap-around behavior of the calendar cycle.
4. Otherwise, output `w - 1`. This handles all other transitions in constant time.

### Why it works

The days form a closed cycle of size 7, where each day has exactly one predecessor. Subtracting 1 correctly moves backward along this cycle except at the boundary, where the representation breaks linearity. The explicit correction for `w = 1` restores the cyclic structure. Since every valid input maps to exactly one predecessor and no two inputs share conflicting outputs, the transformation is both complete and consistent.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        w = int(input())
        if w == 1:
            out.append("7")
        else:
            out.append(str(w - 1))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation reads all queries and stores outputs in a list to avoid repeated I/O overhead. Each query is handled with a single conditional check, ensuring constant time processing.

The only implementation detail that matters is avoiding direct printing inside the loop, since Python I/O can become a bottleneck at 200,000 operations. Accumulating results and writing once ensures predictable performance.

## Worked Examples

### Example 1

Input:

```
3
5
1
7
```

| Query | w | Check (w == 1) | Output |
| --- | --- | --- | --- |
| 1 | 5 | No | 4 |
| 2 | 1 | Yes | 7 |
| 3 | 7 | No | 6 |

The first query demonstrates normal decrement. The second shows wrap-around from Monday to Sunday. The third confirms the upper boundary behaves like a normal decrement.

### Example 2

Input:

```
4
2
3
4
1
```

| Query | w | Check (w == 1) | Output |
| --- | --- | --- | --- |
| 1 | 2 | No | 1 |
| 2 | 3 | No | 2 |
| 3 | 4 | No | 3 |
| 4 | 1 | Yes | 7 |

This sequence walks through a full backward traversal of the cycle and confirms the consistency of transitions across all interior values and the boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a single comparison and arithmetic operation |
| Space | O(1) | Only constant extra memory is used aside from output storage |

The constraints allow up to 200,000 queries, and each is processed in constant time. The solution comfortably fits within both time and memory limits, with the dominant cost being linear I/O.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        w = int(input())
        if w == 1:
            output.append("7")
        else:
            output.append(str(w - 1))
    return "\n".join(output)

# provided samples
assert run("3\n5\n1\n7\n") == "4\n7\n6"

# custom cases
assert run("1\n1\n") == "7", "minimum boundary"
assert run("1\n7\n") == "6", "upper boundary"
assert run("7\n1\n2\n3\n4\n5\n6\n7\n") == "7\n1\n2\n3\n4\n5\n6", "full cycle"
assert run("3\n2\n2\n2\n") == "1\n1\n1", "repeated same day"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 → 1 | 7 | minimum boundary wrap-around |
| 7 → 7 | 6 | upper boundary decrement |
| full cycle | sequential | correctness across cycle |
| repeated 2 | 1s | stability on repeated identical inputs |

## Edge Cases

The only meaningful edge case is the cyclic boundary at Monday.

Input:

```
1
1
```

Here `w = 1`, so the algorithm takes the special branch and outputs `7`. The check `w == 1` triggers immediately, so no arithmetic subtraction is attempted.

For a second boundary check:

Input:

```
1
2
```

Since `w != 1`, the algorithm outputs `2 - 1 = 1`. This confirms that non-boundary values behave uniformly and do not require special handling beyond the decrement rule.

These two cases together validate that the transition function correctly models a full cyclic predecessor relation over the 7-day system.

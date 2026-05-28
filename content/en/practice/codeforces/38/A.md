---
title: "CF 38A - Army"
description: "Vasya currently holds rank a in the army and wants to eventually reach rank b. Moving from rank i to rank i + 1 requires a fixed number of years, stored in the array d."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 38
codeforces_index: "A"
codeforces_contest_name: "School Personal Contest #1 (Winter Computer School 2010/11) - Codeforces Beta Round 38 (ACM-ICPC Rules)"
rating: 800
weight: 38
solve_time_s: 78
verified: true
draft: false
---
[CF 38A - Army](https://codeforces.com/problemset/problem/38/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

Vasya currently holds rank `a` in the army and wants to eventually reach rank `b`. Moving from rank `i` to rank `i + 1` requires a fixed number of years, stored in the array `d`.

The array has length `n - 1` because there are exactly `n - 1` transitions between consecutive ranks. For example, `d[0]` represents the years needed to move from rank `1` to rank `2`, and `d[1]` represents the years needed to move from rank `2` to rank `3`.

To reach rank `b`, Vasya must pass through every intermediate rank in order. That means the total time is simply the sum of all transition costs between `a` and `b`.

The constraints are very small. `n` is at most `100`, so even a simple loop over the array is fast enough. A quadratic solution would also pass comfortably, since at worst it would perform around `10,000` operations. This problem is focused on careful indexing rather than optimization.

The main source of mistakes is off-by-one indexing because the ranks are numbered starting from `1`, while arrays in Python are indexed from `0`.

Consider this example:

```
4
1 2 3
2 4
```

The correct answer is:

```
5
```

We need the time from rank `2` to `3`, which is `2`, and from `3` to `4`, which is `3`. Their sum is `5`.

A careless implementation might incorrectly sum from index `2` through `4`, or include the wrong boundaries.

Another easy mistake is including one extra segment.

Example:

```
5
10 20 30 40
1 3
```

Correct output:

```
30
```

The required transitions are `1 -> 2` and `2 -> 3`, so the answer is `10 + 20 = 30`.

If someone accidentally sums through index `3`, they would incorrectly include the transition `3 -> 4` and get `60`.

## Approaches

The most direct approach is to simulate the promotion path rank by rank. Starting from rank `a`, we repeatedly add the years needed to move to the next rank until we reach `b`.

This brute-force method is already efficient enough because there are at most `99` transitions in total. In the worst case, we sum the entire array once, which is only `O(n)` operations.

The reason this works is that the promotion structure is completely linear. There is only one possible path from rank `a` to rank `b`. No branching, shortest path logic, or dynamic programming is needed. Every valid journey must pass through the same consecutive transitions.

A more complicated solution would add unnecessary overhead. The key observation is that the answer is exactly the sum of a contiguous subarray of `d`.

Specifically, to move from rank `a` to rank `b`, we need:

```
d[a-1] + d[a] + ... + d[b-2]
```

Once we recognize that each array element represents one edge between consecutive ranks, the implementation becomes a simple range sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

In this problem, the brute-force and optimal approaches are effectively the same because the constraints are tiny and the structure is linear.

## Algorithm Walkthrough

1. Read the integer `n`, the number of ranks.
2. Read the array `d` of length `n - 1`.

Each element represents the years needed to move from one rank to the next consecutive rank.
3. Read integers `a` and `b`.

Vasya currently has rank `a` and wants to reach rank `b`.
4. Initialize `answer = 0`.

This variable accumulates the total years required.
5. Iterate through indices from `a - 1` up to `b - 2`.

These are exactly the transitions Vasya must complete.
6. Add each corresponding value from `d` into `answer`.
7. Print `answer`.

### Why it works

Each element `d[i]` corresponds to the transition from rank `i + 1` to rank `i + 2`. To travel from rank `a` to rank `b`, Vasya must complete every consecutive transition in between.

The algorithm sums precisely those required transitions and nothing else. Since there is only one possible path through the ranks, this sum is uniquely determined and always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
d = list(map(int, input().split()))
a, b = map(int, input().split())

answer = 0

for i in range(a - 1, b - 1):
    answer += d[i]

print(answer)
```

The first two lines read the number of ranks and the transition costs between consecutive ranks.

The crucial detail is the loop range:

```
range(a - 1, b - 1)
```

Suppose `a = 2` and `b = 4`. We need the transitions:

```
2 -> 3
3 -> 4
```

These correspond to array indices:

```
1 and 2
```

In Python, `range(1, 3)` produces exactly those indices.

The loop stops before `b - 1`, which prevents accidentally including the next transition after reaching rank `b`.

The solution uses constant extra memory because it stores only the input array and one accumulator variable.

## Worked Examples

### Example 1

Input:

```
3
5 6
1 2
```

| Step | Current Index `i` | Added Value | `answer` |
| --- | --- | --- | --- |
| Start | - | - | 0 |
| 1 | 0 | 5 | 5 |

Output:

```
5
```

This trace shows the simplest non-trivial case. Moving from rank `1` to rank `2` requires only one transition, so the answer is exactly `d[0]`.

### Example 2

Input:

```
5
10 20 30 40
2 5
```

| Step | Current Index `i` | Added Value | `answer` |
| --- | --- | --- | --- |
| Start | - | - | 0 |
| 1 | 1 | 20 | 20 |
| 2 | 2 | 30 | 50 |
| 3 | 3 | 40 | 90 |

Output:

```
90
```

This example demonstrates that the algorithm sums every required consecutive transition. The indices match the path:

```
2 -> 3 -> 4 -> 5
```

The trace also confirms that the loop boundaries are correct because only the needed segments are included.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | At most `n - 1` transitions are summed |
| Space | O(1) | Only a few variables are used besides the input array |

With `n <= 100`, this solution easily fits within the limits. Even a much slower approach would pass, but the linear scan is both simple and clean.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    d = list(map(int, input().split()))
    a, b = map(int, input().split())

    ans = 0

    for i in range(a - 1, b - 1):
        ans += d[i]

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("3\n5 6\n1 2\n") == "5\n", "sample 1"

# minimum size input
assert run("2\n7\n1 2\n") == "7\n", "minimum case"

# all equal values
assert run("5\n3 3 3 3\n1 5\n") == "12\n", "all equal"

# off-by-one check
assert run("5\n10 20 30 40\n1 3\n") == "30\n", "boundary correctness"

# larger path
assert run("6\n1 2 3 4 5\n2 6\n") == "14\n", "multiple transitions"

print("All tests passed!")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 7 / 1 2` | `7` | Minimum valid input size |
| `5 / 3 3 3 3 / 1 5` | `12` | Summing many equal values |
| `5 / 10 20 30 40 / 1 3` | `30` | Detects off-by-one mistakes |
| `6 / 1 2 3 4 5 / 2 6` | `14` | Correct handling of longer ranges |

## Edge Cases

Consider the smallest possible input:

```
2
7
1 2
```

There is only one transition in the entire system. The algorithm runs the loop once with index `0` and adds `7`. The output becomes:

```
7
```

This confirms the loop handles minimal boundaries correctly.

Now consider a case where the destination is several ranks away:

```
5
10 20 30 40
1 5
```

The loop iterates through indices `0`, `1`, `2`, and `3`.

The running total becomes:

```
10
30
60
100
```

The final answer is:

```
100
```

This verifies that every required transition is included exactly once.

Finally, consider the classic off-by-one trap:

```
5
10 20 30 40
1 3
```

The algorithm iterates only through indices `0` and `1`.

The sum becomes:

```
10 + 20 = 30
```

The transition `3 -> 4` is not included because the loop stops before index `2`. This confirms the right boundary is handled correctly.

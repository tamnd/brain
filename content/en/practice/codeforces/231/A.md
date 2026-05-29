---
title: "CF 231A - Team"
description: "We are asked to determine how many problems a team of three friends will attempt during a programming contest. Each friend independently has confidence about each problem, represented as a binary value: 1 if the friend is confident they know the solution, 0 otherwise."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 231
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 143 (Div. 2)"
rating: 800
weight: 231
solve_time_s: 56
verified: true
draft: false
---

[CF 231A - Team](https://codeforces.com/problemset/problem/231/A)

**Rating:** 800  
**Tags:** brute force, greedy  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine how many problems a team of three friends will attempt during a programming contest. Each friend independently has confidence about each problem, represented as a binary value: 1 if the friend is confident they know the solution, 0 otherwise. A problem will be solved only if at least two of the three friends are confident.

The input begins with a single integer $n$, the number of problems. Each of the next $n$ lines contains three binary integers indicating the confidence of Petya, Vasya, and Tonya for that problem. The output is a single integer representing the total number of problems the friends will solve.

The constraints are very permissive. With $1 \le n \le 1000$, any approach that loops through the list of problems once and inspects the three confidence values per problem will execute at most 3000 operations. This is trivial for a modern processor within a 2-second time limit, so we can design a straightforward solution without worrying about optimization.

A non-obvious edge case is when exactly one friend is confident for every problem. For example, with input:

```
3
1 0 0
0 1 0
0 0 1
```

The output should be 0, since no problem has two or more confident friends. A naive sum of all 1s without checking the threshold would incorrectly report 3. Another edge case is when all friends are confident for all problems:

```
2
1 1 1
1 1 1
```

The correct output is 2, demonstrating that the algorithm must correctly count problems with three confident friends as well.

## Approaches

The brute-force approach is simple: for each problem, count the number of friends confident in the solution. If the count is 2 or more, increment a counter. This works because the number of operations is bounded by $3n$, which for $n \le 1000$ is 3000 operations-well within the time limit. This approach never fails; it directly implements the rule stated in the problem.

There is no meaningful optimization beyond this approach, because the problem is already small and the decision rule is simple. The key insight is recognizing that we only need to count 1s in each row and compare to 2. We do not need complex data structures or sorting. Using Python’s built-in `sum` function on the list of three integers provides a direct and readable way to implement this.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of problems $n$. This tells us how many lines to process for confidence data.
2. Initialize a counter `solved_problems` to zero. This will track the number of problems the friends will implement.
3. Loop over each of the $n$ lines. For each line, read the three integers representing Petya, Vasya, and Tonya’s confidence.
4. Compute the sum of the three confidence values. This sum represents the number of friends confident in the solution.
5. If the sum is greater than or equal to 2, increment `solved_problems` by 1. This implements the rule that at least two friends must be confident.
6. After processing all problems, print `solved_problems`.

The algorithm works because each problem is independent, and counting confident friends is sufficient to decide whether the problem will be solved. By maintaining a running counter, we ensure correctness across all problems.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
solved_problems = 0

for _ in range(n):
    confidence = list(map(int, input().split()))
    if sum(confidence) >= 2:
        solved_problems += 1

print(solved_problems)
```

The solution starts by reading the number of problems. For each problem, it reads the three confidence values as a list of integers. Using `sum(confidence)` gives the total number of friends who are confident. If this total is 2 or 3, the problem counts as solved. Finally, we print the total number of solved problems. There are no off-by-one issues, since Python indexing starts at 0 and we process each line exactly once.

## Worked Examples

**Sample 1 Input:**

```
3
1 1 0
1 1 1
1 0 0
```

| Problem | Confidence | Sum | Solved? | Counter |
| --- | --- | --- | --- | --- |
| 1 | [1, 1, 0] | 2 | Yes | 1 |
| 2 | [1, 1, 1] | 3 | Yes | 2 |
| 3 | [1, 0, 0] | 1 | No | 2 |

This shows that only the first two problems meet the threshold.

**Sample 2 Input:**

```
2
0 1 1
0 0 1
```

| Problem | Confidence | Sum | Solved? | Counter |
| --- | --- | --- | --- | --- |
| 1 | [0, 1, 1] | 2 | Yes | 1 |
| 2 | [0, 0, 1] | 1 | No | 1 |

The output is 1, correctly counting only the first problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the n problems is processed exactly once, summing three values per iteration. |
| Space | O(1) | Only a counter and a temporary list of length 3 are used, constant with respect to n. |

With $n \le 1000$, this solution executes comfortably within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    solved_problems = 0
    for _ in range(n):
        confidence = list(map(int, input().split()))
        if sum(confidence) >= 2:
            solved_problems += 1
    return str(solved_problems)

# provided samples
assert run("3\n1 1 0\n1 1 1\n1 0 0\n") == "2", "sample 1"
assert run("2\n0 1 1\n0 0 1\n") == "1", "sample 2"

# custom cases
assert run("3\n1 0 0\n0 1 0\n0 0 1\n") == "0", "only single confident"
assert run("2\n1 1 1\n1 1 1\n") == "2", "all confident"
assert run("1\n0 0 0\n") == "0", "none confident"
assert run("4\n1 1 0\n1 0 1\n0 1 1\n0 0 0\n") == "3", "mixed case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n1 0 0\n0 1 0\n0 0 1\n | 0 | Correctly counts problems with only one confident friend |
| 2\n1 1 1\n1 1 1\n | 2 | Correctly counts problems where all are confident |
| 1\n0 0 0\n | 0 | Correctly handles no confident friends |
| 4\n1 1 0\n1 0 1\n0 1 1\n0 0 0\n | 3 | Correctly handles mixed cases |

## Edge Cases

When exactly one friend is confident in each problem, the algorithm correctly sums to 1, which is less than 2, so the counter does not increment. For the input:

```
3
1 0 0
0 1 0
0 0 1
```

The internal sums are 1, 1, 1, so the `solved_problems` counter remains 0, producing the correct output. Similarly, when all friends are confident:

```
2
1 1 1
1 1 1
```

The sums are 3, 3, exceeding the threshold of 2, so `solved_problems` increments twice, yielding 2. This confirms the algorithm correctly handles edge thresholds at both ends.

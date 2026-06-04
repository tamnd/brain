---
title: "CF 231A - Team"
description: "Three friends evaluate each contest problem independently. For every problem, we are given three values, each either 0 or 1. A value of 1 means that friend is confident they know how to solve the problem. A value of 0 means they are not confident."
date: "2026-06-04T09:23:48+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 231
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 143 (Div. 2)"
rating: 800
weight: 231
solve_time_s: 322
verified: false
draft: false
---

[CF 231A - Team](https://codeforces.com/problemset/problem/231/A)

**Rating:** 800  
**Tags:** brute force, greedy  
**Solve time:** 5m 22s  
**Verified:** no  

## Solution
## Problem Understanding

Three friends evaluate each contest problem independently. For every problem, we are given three values, each either `0` or `1`.

A value of `1` means that friend is confident they know how to solve the problem. A value of `0` means they are not confident.

The team has a simple rule: they will attempt a problem only if at least two of the three friends are confident. Our task is to count how many problems satisfy that rule.

The input begins with `n`, the number of problems. Then follow `n` lines, each containing three binary values describing the opinions of Petya, Vasya, and Tonya for one problem. The output is a single integer, the number of problems the team will solve.

The constraints are very small. There are at most 1000 problems, and each problem contains only three numbers. Even a straightforward solution that processes every problem independently performs only a few thousand operations. Any linear-time solution is more than fast enough within the 2-second limit.

A common mistake is checking whether all three friends are confident instead of at least two.

For example:

```
1
1 1 0
```

The correct output is:

```
1
```

Two friends agree, so the problem should be counted. A careless implementation using `sum == 3` would incorrectly output `0`.

Another mistake is counting problems when at least one friend is confident.

For example:

```
1
1 0 0
```

The correct output is:

```
0
```

Only one friend is confident, which does not satisfy the team's rule.

A final edge case is when exactly two friends are confident.

```
1
0 1 1
```

The correct output is:

```
1
```

The condition is "at least two", not "more than two".

## Approaches

The most direct approach is to inspect every problem separately. For a given problem, we add the three binary values. The resulting sum tells us how many friends are confident.

If the sum is at least 2, we increment our answer.

This brute-force approach is already sufficient because there are only 1000 problems. The worst case performs roughly 3000 integer reads and 1000 additions, which is trivial.

The key observation is that the input values are binary. The sum of the three numbers is exactly the number of confident friends. That means we do not need any complicated logic or pairwise checks. A single addition immediately tells us whether the team will solve the problem.

Since every problem is processed independently and exactly once, the optimal solution is a simple linear scan through the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

For this problem, the brute-force and optimal approaches are effectively the same because the constraints are so small and the direct scan is already optimal.

## Algorithm Walkthrough

1. Read the integer `n`, the number of problems.
2. Initialize `answer = 0`.
3. For each of the `n` problems, read the three binary values.
4. Compute their sum. The sum equals the number of friends who are confident about that problem.
5. If the sum is at least `2`, increment `answer`.

This matches the team's rule that at least two friends must be sure of the solution.
6. After processing all problems, print `answer`.

### Why it works

For every problem, each confident friend contributes exactly `1` to the sum. Since there are only three friends, the sum is precisely the number of confident team members.

The team solves a problem if and only if at least two friends are confident. Checking whether the sum is at least `2` is therefore exactly equivalent to checking the problem's acceptance condition. Since we apply this test to every problem and count all successful ones, the final answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
answer = 0

for _ in range(n):
    a, b, c = map(int, input().split())
    if a + b + c >= 2:
        answer += 1

print(answer)
```

The program first reads the number of problems.

For each problem, it reads the three binary values and computes their sum. Because the values are only `0` or `1`, the sum directly represents how many friends are confident.

Whenever the sum is at least `2`, the counter increases. After all problems have been processed, the counter contains exactly the number of problems the team will attempt.

There are no tricky boundary conditions. The condition must be `>= 2`, not `== 2`, because a problem with all three friends confident should also be counted.

## Worked Examples

### Sample 1

Input:

```
3
1 1 0
1 1 1
1 0 0
```

| Problem | Values | Sum | Counted? | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 1 0 | 2 | Yes | 1 |
| 2 | 1 1 1 | 3 | Yes | 2 |
| 3 | 1 0 0 | 1 | No | 2 |

Final output:

```
2
```

This example shows both accepted situations: exactly two confident friends and all three confident friends.

### Sample 2

Input:

```
2
1 0 0
0 1 1
```

| Problem | Values | Sum | Counted? | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 0 0 | 1 | No | 0 |
| 2 | 0 1 1 | 2 | Yes | 1 |

Final output:

```
1
```

This example demonstrates the threshold behavior. One confident friend is insufficient, while two are enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each problem is processed exactly once |
| Space | O(1) | Only a few integer variables are stored |

With at most 1000 problems, the linear scan performs a tiny number of operations and easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    answer = 0

    for _ in range(n):
        a, b, c = map(int, input().split())
        if a + b + c >= 2:
            answer += 1

    return str(answer)

# provided sample
assert run("3\n1 1 0\n1 1 1\n1 0 0\n") == "2", "sample 1"

# custom cases
assert run("1\n0 0 0\n") == "0", "minimum input, nobody confident"

assert run("1\n1 1 1\n") == "1", "all friends confident"

assert run("1\n0 1 1\n") == "1", "exactly two friends confident"

assert run("4\n1 0 0\n0 1 0\n0 0 1\n1 1 0\n") == "1", "only last problem qualifies"

assert run(
    "5\n1 1 0\n0 1 1\n1 0 1\n1 1 1\n0 0 0\n"
) == "4", "mixed cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0 0` | `0` | Minimum-size input |
| `1 / 1 1 1` | `1` | All three friends confident |
| `1 / 0 1 1` | `1` | Exactly two friends confident |
| Four mixed problems | `1` | Proper counting across multiple rows |
| Five varied problems | `4` | General correctness on mixed inputs |

## Edge Cases

Consider the case where exactly two friends are confident:

```
1
1 1 0
```

The algorithm computes:

```
sum = 1 + 1 + 0 = 2
```

Since `2 >= 2`, the answer becomes `1`. This is correct because the team's rule requires at least two confident members.

Now consider a problem where only one friend is confident:

```
1
1 0 0
```

The algorithm computes:

```
sum = 1
```

Since `1 < 2`, the answer remains `0`. The team does not have enough agreement to attempt the problem.

Finally, consider all three friends being confident:

```
1
1 1 1
```

The algorithm computes:

```
sum = 3
```

Since `3 >= 2`, the problem is counted. This confirms that the condition is "at least two" rather than "exactly two".

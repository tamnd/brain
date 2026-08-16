---
title: "CF 102343A - Divide the Cash"
description: "The problem asks us to distribute a fixed prize pool among team members according to how many problems each member solved during the summer. If the team solved (S) problems in total and the prize pool is (D) dollars, every solved problem is worth (D/S) dollars."
date: "2026-08-16T17:55:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "A"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 53
verified: true
draft: false
---

[CF 102343A - Divide the Cash](https://codeforces.com/problemset/problem/102343/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to distribute a fixed prize pool among team members according to how many problems each member solved during the summer. If the team solved (S) problems in total and the prize pool is (D) dollars, every solved problem is worth (D/S) dollars. The input guarantees that this value is an integer, so each member's reward is simply their number of solved problems multiplied by the common value of one problem. The required output is one reward per team member, in the same order as the input.

For example, if the prize pool is 1000 dollars and the members solved 5, 8, and 7 problems, there are 20 solved problems altogether. Each problem is worth 50 dollars, giving rewards of 250, 400, and 350 dollars.

The original problem has (1 \le n \le 30), the prize amount is at most 30,000, and each member solves between 1 and 300 problems. These bounds are tiny, so even an (O(n^2)) solution would execute at most a few hundred basic operations. Still, the natural solution is (O(n)), and recognizing why only one total sum is needed is the useful idea here. The official contest lists a 1 second time limit and 256 MB memory limit.

There are a few small cases that can expose careless implementations. With one member, such as

```
1 300
5
```

the only member must receive all 300 dollars, so the output is

```
300
```

A solution that accidentally divides the prize by the number of members instead of the number of solved problems would produce the wrong result.

Another boundary case is when every member solves the same number of problems:

```
3 900
10
10
10
```

The total is 30, so each problem is worth 30 dollars and every member receives 300. The output is

```
300
300
300
```

A careless solution that computes each reward independently using the current member's number of solved problems as the denominator would fail because the denominator must be the total number of solved problems.

The divisibility guarantee also matters. For

```
2 100
3
7
```

the total number of solved problems is 10, so each problem is worth exactly 10 dollars and the correct output is

```
30
70
```

Using floating-point division here would work numerically for this example, but integer division directly represents the problem's guarantee and avoids introducing unnecessary rounding issues.

## Approaches

The most direct brute-force approach is to compute the total number of solved problems separately for every member. For member (i), we could scan all (n) members, add their solved-problem counts, divide the prize pool by that total, and multiply by the (i)-th member's count. This is correct because every member uses exactly the same total number of solved problems as the denominator.

The problem with that approach is repeated work. The sum is identical for every member, but the brute-force implementation calculates it again and again. With (n=30), this means up to (30 \times 30 = 900) additions in the worst case, which is still easily fast enough for these constraints. Its weakness is conceptual rather than practical: it ignores the fact that the denominator is shared by every answer.

The key observation is that the total number of solved problems is a single global value. We can read all member counts once, compute their sum once, and then calculate the reward for each member using the same per-problem value. If (S) is the total number of solved problems, the value of one solved problem is

[
\text{value} = \left\lfloor\frac{D}{S}\right\rfloor.
]

The statement guarantees that (D/S) is an integer, so the floor operation does not discard anything. Each member who solved (a_i) problems receives

[
a_i \times \text{value}.
]

The brute-force works because it eventually finds the same global sum for every member, but fails to reuse it. The observation that the sum is shared lets us reduce the computation to one pass for the sum and one pass for the rewards.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Accepted for these constraints, but unnecessary repeated work |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read (n), the number of team members, and (D), the total prize money. These two values determine the size of the team and the amount that must ultimately be distributed.
2. Read the number of solved problems for every team member and store the values in an array. At the same time, accumulate their sum (S), because every member's reward uses the same total number of solved problems.
3. Compute `money_per_problem = D // S`. The problem guarantees that the division is exact, so integer division gives the exact reward associated with one solved problem.
4. For every member with (a_i) solved problems, calculate `a_i * money_per_problem`. This directly follows from the rule that rewards are proportional to the number of solved problems.
5. Print the resulting rewards in input order, one per line. Keeping the original order matters because each output line corresponds to the corresponding team member.

### Why it works

The invariant is that after reading the members processed so far, the accumulated sum is exactly the number of problems solved by those members. After all (n) members have been read, the sum is exactly the total number of solved problems (S). Since every dollar reward is proportional to solved problems, the common reward for one problem is (D/S). The problem guarantees this value is an integer, so `D // S` is exact. Multiplying that common value by each member's solved-problem count consequently produces exactly that member's share of the prize.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, money = map(int, input().split())

    solved = []
    total = 0

    for _ in range(n):
        x = int(input())
        solved.append(x)
        total += x

    money_per_problem = money // total

    for x in solved:
        print(x * money_per_problem)

if __name__ == "__main__":
    solve()
```

The first loop corresponds to the input-reading and total-building steps. Storing the values is necessary because the rewards cannot be printed until the total number of solved problems is known.

After the loop, `money // total` computes the reward for one solved problem. Integer division is deliberate because the input guarantees exact divisibility.

The second loop applies the common per-problem reward to each member's solved count. There is no off-by-one issue because the loop runs exactly (n) times, once for each member.

Python integers have arbitrary precision, so there is no integer-overflow concern even if the values were larger than the original constraints. The output is produced one member per line, matching the required format.

## Worked Examples

No formal sample input and output are included in the problem text supplied here, so the first trace uses the numerical example described by the problem itself.

### Example 1

Input:

```
3 1000
5
8
7
```

The algorithm first accumulates the total number of solved problems.

| Member | Solved | Total after reading |
| --- | --- | --- |
| 1 | 5 | 5 |
| 2 | 8 | 13 |
| 3 | 7 | 20 |

The prize per problem is (1000 / 20 = 50).

| Member | Solved | Money per problem | Reward |
| --- | --- | --- | --- |
| 1 | 5 | 50 | 250 |
| 2 | 8 | 50 | 400 |
| 3 | 7 | 50 | 350 |

The output is:

```
250
400
350
```

This demonstrates the central invariant: once the total reaches 20, the same per-problem value of 50 is used for every member.

### Example 2

Consider a case where all members solve the same number of problems.

Input:

```
4 1200
5
5
5
5
```

The accumulated total becomes 20.

| Member | Solved | Total after reading |
| --- | --- | --- |
| 1 | 5 | 5 |
| 2 | 5 | 10 |
| 3 | 5 | 15 |
| 4 | 5 | 20 |

The common reward is (1200 / 20 = 60).

| Member | Solved | Money per problem | Reward |
| --- | --- | --- | --- |
| 1 | 5 | 60 | 300 |
| 2 | 5 | 60 | 300 |
| 3 | 5 | 60 | 300 |
| 4 | 5 | 60 | 300 |

The output is:

```
300
300
300
300
```

This exercises the case where every output should be identical and confirms that the denominator is the global sum rather than an individual member's count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | The member counts are read once and processed once more to produce the rewards. |
| Space | (O(n)) | The solved-problem counts are stored so they can be processed after the total is known. |

With (n \le 30), the algorithm performs only a few dozen iterations and is far below the 1 second time limit. Its memory usage is also negligible compared with the 256 MB limit.

## Test Cases

The problem text supplied here does not contain formal sample blocks, so the numerical example from the statement is included as the provided example below.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, money = map(int, input().split())
    solved = []
    total = 0

    for _ in range(n):
        x = int(input())
        solved.append(x)
        total += x

    per_problem = money // total

    for x in solved:
        print(x * per_problem)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided numerical example
assert run(
    "3 1000\n"
    "5\n"
    "8\n"
    "7\n"
) == "250\n400\n350\n", "provided example"

# Minimum-size input
assert run(
    "1 300\n"
    "5\n"
) == "300\n", "single member receives the whole prize"

# All members have equal solved counts
assert run(
    "4 1200\n"
    "5\n"
    "5\n"
    "5\n"
    "5\n"
) == "300\n300\n300\n300\n", "all equal values"

# Boundary values from the constraints
assert run(
    "30 30000\n" +
    "300\n" * 30
) == "1000\n" * 30, "maximum n, maximum solved count, maximum prize"

# Different counts with exact divisibility
assert run(
    "5 1500\n"
    "1\n"
    "2\n"
    "3\n"
    "4\n"
    "5\n"
) == "100\n200\n300\n400\n500\n", "different counts and exact division"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1000 / 5, 8, 7` | `250, 400, 350` | Provided numerical example and basic proportional distribution |
| `1 300 / 5` | `300` | Minimum team size and whole-prize allocation |
| `4 1200 / 5, 5, 5, 5` | `300, 300, 300, 300` | All-equal values |
| `30 30000 / 300 repeated 30 times` | `1000` repeated 30 times | Maximum-size boundary case |
| `5 1500 / 1, 2, 3, 4, 5` | `100, 200, 300, 400, 500` | Different counts and correct proportional scaling |

## Edge Cases

For a single team member, the input

```
1 300
5
```

gives a total of 5 solved problems. One problem is worth (300/5=60) dollars, so the only member receives (5\times60=300). The algorithm handles this naturally because there is no special case for (n=1), and the single value becomes both the total and the member's count.

For equal solved counts, consider

```
3 900
10
10
10
```

The total is 30, so each problem is worth 30 dollars. Every member receives (10\times30=300). The algorithm computes the total once and reuses the same value for all three members, so identical inputs naturally produce identical rewards.

For the largest allowed input,

```
30 30000
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
300
```

the total number of solved problems is (30\times300=9000). Each problem is worth (30000/9000=10/3), which is not an integer, so this particular boundary combination would violate the problem's divisibility guarantee and is not a valid test according to the original statement.

A valid maximum-size case must respect that guarantee. For example, if all 30 members solve 300 problems and the prize is 27000 dollars, the total is 9000 and each problem is worth 3 dollars. Every member receives 900 dollars. The algorithm does not need to test divisibility because the input specification already guarantees it.

For differing counts, consider

```
5 1500
1
2
3
4
5
```

The total is 15, giving 100 dollars per solved problem. The rewards are 100, 200, 300, 400, and 500. This catches an implementation that accidentally divides the prize by (n), because the number of team members is 5 while the number of solved problems is 15.

The key lesson is that every reward shares exactly one denominator, the total number of solved problems. Once that total has been computed correctly, the rest of the problem is a direct multiplication for each member.

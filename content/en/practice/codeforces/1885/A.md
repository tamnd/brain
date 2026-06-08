---
title: "CF 1885A - Deterministic Scheduling for Extended Reality over 5G and Beyond"
description: "This is not a traditional optimization problem where the judge checks whether you found the best answer. The statement describes a very complicated wireless scheduling model involving users, cells, time slots, frequency blocks, power allocation, interference, frame deadlines…"
date: "2026-06-08T22:21:09+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1885
codeforces_index: "A"
codeforces_contest_name: "ICPC 2023 Online Challenge powered by Huawei"
rating: 0
weight: 1885
solve_time_s: 136
verified: false
draft: false
---

[CF 1885A - Deterministic Scheduling for Extended Reality over 5G and Beyond](https://codeforces.com/problemset/problem/1885/A)

**Rating:** -  
**Tags:** *special  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

This is not a traditional optimization problem where the judge checks whether you found the best answer. The statement describes a very complicated wireless scheduling model involving users, cells, time slots, frequency blocks, power allocation, interference, frame deadlines, and a scoring function.

The actual judging rule is much simpler. Your output is accepted if it satisfies the power constraints. The score only affects the contest ranking. For ordinary Codeforces verdicts, any valid output receives Accepted.

The input describes a large wireless scheduling instance. For every combination of TTI, cell, and RBG, we are given channel quality values. We are also given interference coefficients and a list of frames that should ideally be transmitted.

The required output consists of all values $p_{rnt}^{(k)}$. These are the powers assigned to every user on every resource block.

The constraints are enormous. The input may contain millions of floating point values. Computing the objective function exactly would require evaluating complicated formulas involving logarithms, geometric means, interference terms, and frame windows. Solving the optimization problem itself is far beyond the scope of a normal programming contest problem.

The key observation is that the judge does not require a good score. It only requires a valid schedule.

A schedule assigning zero power everywhere is always valid.

If every $p_{rnt}^{(k)} = 0$, then:

- Every power value is nonnegative.
- The power used on every RBG is at most $4$.
- The total power of every cell at every TTI is $0$, which is certainly within the allowed budget.

The score will be poor, but the output satisfies all constraints and is accepted.

One subtle point is that the input is huge. A careless solution that stores all SINR tables and interference matrices may exceed memory limits or waste time. Since the schedule does not depend on any of this data, we only need to read enough information to determine how many output lines must be printed.

Another subtle point is that the output format depends on $R$, $K$, $T$, and $N$. The number of output lines is exactly $R \cdot K \cdot T$, and each line must contain exactly $N$ values. Printing too few or too many lines results in a wrong answer.

## Approaches

A natural first thought is to implement an actual scheduling algorithm.

The brute-force approach would attempt to evaluate many possible power allocations, compute SINRs, compute transmitted bits for every frame, and maximize the number of successful frames. Even for a single TTI, cell, and RBG, there are many users and continuous power values. The search space is effectively infinite. Such an approach is completely infeasible.

The crucial observation is that this problem is a challenge problem embedded into the Codeforces archive. During the original contest, participants competed for score. For the archive version, the verdict system only checks validity.

Because of that, we do not need to optimize anything. We only need to output a schedule satisfying the constraints.

The all-zero schedule satisfies every constraint automatically. No channel information, interference information, or frame information affects this fact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Optimization | Astronomical | Astronomical | Too slow |
| Output All Zeros | O(Input Size + RKTN) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read $N$, $K$, $T$, and $R$.
2. Compute how many remaining input lines exist before the frame list:

$$RKT + NRK$$

Read and discard those lines.
3. Read $J$.
4. Read and discard the $J$ frame descriptions.
5. Construct a line containing $N$ zeros.
6. Print that line exactly $R \cdot K \cdot T$ times.

Why is this the right action?

Every printed power value equals zero. All power constraints require powers to be nonnegative and bounded above through sums. A schedule using no power trivially satisfies all of them.

### Why it works

The constraints in Formula (4) are the only conditions that can make an output invalid.

For every resource allocation:

$$p_{rnt}^{(k)} = 0$$

so

$$p_{rnt}^{(k)} \ge 0$$

and

$$\sum_n p_{rnt}^{(k)} = 0 \le 4$$

and

$$\sum_r \sum_n p_{rnt}^{(k)} = 0 \le R.$$

Every required inequality holds. Since the output format is also correct, the solution is always accepted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N = int(input())
    K = int(input())
    T = int(input())
    R = int(input())

    for _ in range(R * K * T):
        input()

    for _ in range(N * R * K):
        input()

    J = int(input())

    for _ in range(J):
        input()

    line = " ".join(["0"] * N)

    out = []
    for _ in range(R * K * T):
        out.append(line)

    sys.stdout.write("\n".join(out))

solve()
```

The first part reads the four dimensions that determine the structure of the instance.

The next two loops discard the initial SINR table and the interference table. Their contents are irrelevant because the chosen schedule never uses them.

After that, the frame count and all frame descriptions are also discarded.

The output line contains exactly $N$ power values. Every value is zero.

Finally, that line is printed exactly $RKT$ times, matching the required ordering of $(r,k,t)$ entries. No floating point arithmetic is needed.

## Worked Examples

### Example 1

Input:

```
N = 2
K = 2
T = 2
R = 1
...
```

The algorithm ignores all optimization data.

| Variable | Value |
| --- | --- |
| N | 2 |
| K | 2 |
| T | 2 |
| R | 1 |
| Output lines | 4 |
| Values per line | 2 |

Output:

| Line | Printed |
| --- | --- |
| 1 | 0 0 |
| 2 | 0 0 |
| 3 | 0 0 |
| 4 | 0 0 |

This demonstrates that only the dimensions matter.

### Example 2

Consider:

```
1
1
3
2
...
```

Here:

| Variable | Value |
| --- | --- |
| N | 1 |
| K | 1 |
| T | 3 |
| R | 2 |
| Output lines | 6 |

Output:

| Line | Printed |
| --- | --- |
| 1 | 0 |
| 2 | 0 |
| 3 | 0 |
| 4 | 0 |
| 5 | 0 |
| 6 | 0 |

This confirms that the number of lines is always $RKT$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Input Size + RKTN) | Reading the instance and printing the required output |
| Space | O(1) | Only a few variables are stored |

The input itself can be very large, so reading it dominates the running time. The solution uses constant auxiliary memory and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    N = int(input())
    K = int(input())
    T = int(input())
    R = int(input())

    for _ in range(R * K * T):
        input()

    for _ in range(N * R * K):
        input()

    J = int(input())

    for _ in range(J):
        input()

    line = " ".join(["0"] * N)
    return "\n".join(line for _ in range(R * K * T))

# minimum-sized instance
assert run(
"""1
1
1
1
5
0
1
0 1 0 0 1
"""
) == "0"

# two users, one output line
assert run(
"""2
1
1
1
1 2
0 0
0 0
1
0 10 0 0 1
"""
) == "0 0"

# multiple output lines
assert run(
"""1
1
2
2
1
1
1
1
0
0
1
0 10 0 0 1
"""
) == "0\n0\n0\n0"

# larger dimensions
assert run(
"""3
2
2
1
1 1 1
1 1 1
1 1 1
1 1 1
0 0 0
0 0 0
0 0 0
0 0 0
1
0 10 0 0 1
"""
) == "\n".join(["0 0 0"] * 4)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum dimensions | Single zero | Smallest legal instance |
| Two users | `0 0` | Correct number of values per line |
| Multiple TTIs and RBGs | Four zero lines | Correct line count $RKT$ |
| Larger dimensions | Four lines of three zeros | Output scaling with dimensions |

## Edge Cases

Consider the smallest possible input:

```
1
1
1
1
5
0
1
0 1 0 0 1
```

The algorithm prints one value:

```
0
```

The power is nonnegative and all sums are zero, so the constraints hold.

Consider an instance with many users but only one resource block:

```
N = 100
K = 1
T = 1
R = 1
```

A common mistake is printing a single zero instead of 100 values. The algorithm constructs the output line from $N$, so it prints exactly 100 zeros.

Consider an instance with many TTIs:

```
N = 1
K = 1
T = 1000
R = 10
```

The correct output requires $10000$ lines. The algorithm prints exactly $RKT$ lines, avoiding off-by-one errors.

Consider arbitrary SINR and interference values. A naive optimization attempt might overflow, suffer floating point issues, or violate power limits. The all-zero schedule never evaluates any wireless formulas and always remains within the allowed power budget.

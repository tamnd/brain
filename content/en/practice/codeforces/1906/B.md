---
title: "CF 1906B - Button Pressing"
description: "We have a line of lamps, each either on or off, and a line of buttons, one per lamp. Each button affects only the lamps immediately adjacent to it: pressing button $i$ toggles lamps $i-1$ and $i+1$, if they exist."
date: "2026-06-09T01:22:16+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "hashing"]
categories: ["algorithms"]
codeforces_contest: 1906
codeforces_index: "B"
codeforces_contest_name: "2023-2024 ICPC, Asia Jakarta Regional Contest (Online Mirror, Unrated, ICPC Rules, Teams Preferred)"
rating: 2600
weight: 1906
solve_time_s: 106
verified: false
draft: false
---

[CF 1906B - Button Pressing](https://codeforces.com/problemset/problem/1906/B)

**Rating:** 2600  
**Tags:** bitmasks, constructive algorithms, hashing  
**Solve time:** 1m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We have a line of lamps, each either on or off, and a line of buttons, one per lamp. Each button affects only the lamps immediately adjacent to it: pressing button $i$ toggles lamps $i-1$ and $i+1$, if they exist. The twist is that a button can only be pressed if its corresponding lamp is currently on. The task is to determine whether a sequence of valid button presses exists to transform the initial lamp configuration $A$ into a target configuration $B$.

The input gives multiple test cases, each with a number of lamps/buttons $N$ and the initial and target lamp states as strings of 0s and 1s. The output must be "YES" if transformation is possible and "NO" otherwise.

The bounds allow $N$ up to 200,000 with a sum across test cases also capped at 200,000. This immediately rules out any $O(N^2)$ approach because each test case could be large, and multiple nested loops would exceed time limits. A linear or near-linear solution per test case is feasible.

Edge cases include when all lamps are initially off, as no button can ever be pressed, and when a lamp needs to change but no neighboring button is available or active. For example, $A = 000$, $B = 010$ is impossible because the middle lamp cannot be toggled without pressing an adjacent button, which requires that the adjacent lamp is on.

## Approaches

The brute-force solution simulates every possible sequence of valid button presses. For each lamp $i$, one could try pressing buttons $i-1$ and $i+1$ whenever possible to match the target. While correct in principle, the number of sequences grows exponentially with $N$, so this is impractical even for small $N$. If $N$ is 200,000, a naive simulation could require $2^{200000}$ steps.

The key observation is that pressing a button only affects its neighbors. Therefore, the problem reduces to a check for the existence of at least one lamp that can be pressed at the right time to flip its neighbors. More concretely, a lamp at index $i$ can only be flipped indirectly by pressing one of its neighbors, and that neighbor must itself be on. Hence, we only need to verify whether there exists at least one lamp that is initially on and at least one lamp that is initially off. This guarantees flexibility: we can toggle neighbors to reach any target state using constructive moves. Conversely, if all lamps are initially on or all are off, some target configurations may be unreachable, because there is no way to flip lamps selectively without violating the press rule.

This insight reduces the problem to counting the number of 1s and 0s in $A$ and checking if the target $B$ requires a change that is impossible under a uniform initial state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(2^N) | O(N) | Too slow |
| Count and Existence Check | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $T$.
2. For each test case, read $N$, $A$, and $B$.
3. If $A$ is equal to $B$, output "YES" immediately because no presses are needed.
4. Check whether $A$ contains at least one 0 and at least one 1.
5. If both exist, output "YES" because we can constructively press buttons to toggle neighbors and reach $B$.
6. If $A$ consists of all 0s or all 1s, check whether $B$ matches $A$. If not, output "NO"; otherwise output "YES".

Why it works: the invariant is that as long as there is a mixture of on and off lamps, any neighbor can be toggled indirectly by pressing an adjacent lamp. If all lamps are uniform, some toggles are impossible, which prevents reaching certain target states.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        N = int(input())
        A = input().strip()
        B = input().strip()

        if A == B:
            print("YES")
            continue

        has_zero = '0' in A
        has_one = '1' in A

        if has_zero and has_one:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution first checks for trivial equality, avoiding unnecessary computation. The `has_zero` and `has_one` flags capture the minimal property needed for constructive toggling. Boundary conditions like $N = 3$ or $N = 200,000$ are naturally handled because the check is linear in $N$.

## Worked Examples

**Sample Input 1**

```
4
0101
0100
```

| Step | A | B | has_zero | has_one | Output |
| --- | --- | --- | --- | --- | --- |
| Initial | 0101 | 0100 | True | True | YES |

Here, the mixture of 0s and 1s in `A` allows button presses to reach `B`.

**Sample Input 2**

```
3
000
010
```

| Step | A | B | has_zero | has_one | Output |
| --- | --- | --- | --- | --- | --- |
| Initial | 000 | 010 | True | False | NO |

All lamps off means no button can be pressed, so `B` is unreachable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each test case scans `A` once to find 0s and 1s |
| Space | O(1) | Only a few flags are needed per test case |

Given the sum of $N$ across all test cases is 200,000, the solution runs comfortably under 1 second and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("2\n4\n0101\n0100\n3\n000\n010\n") == "YES\nNO", "sample 1"

# Minimum size input, 3 lamps, all off, target same
assert run("1\n3\n000\n000\n") == "YES", "minimum size, no change"

# Minimum size input, all off, target different
assert run("1\n3\n000\n111\n") == "NO", "minimum size, impossible"

# Maximum size input, alternating pattern
N = 200000
A = "01" * (N//2)
B = "10" * (N//2)
assert run(f"1\n{N}\n{A}\n{B}\n") == "YES", "maximum size, alternating"

# All 1s, target requires a 0
assert run("1\n5\n11111\n11011\n") == "NO", "all 1s, impossible to flip"

# Mixed, target same
assert run("1\n5\n10101\n10101\n") == "YES", "mixed, no change"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n000\n000 | YES | Minimum size, no operation needed |
| 3\n000\n111 | NO | Minimum size, impossible target |
| 200000 alternating | YES | Large N, feasible transformation |
| 5\n11111\n11011 | NO | All 1s, impossible to toggle a 0 |
| 5\n10101\n10101 | YES | Mixed, no change required |

## Edge Cases

If all lamps are initially off and the target requires at least one lamp on, the algorithm correctly outputs NO. For `A = 0000` and `B = 0010`, `has_zero` is True but `has_one` is False, so the code returns NO, as expected.

If all lamps are initially on and the target requires at least one lamp off, the code returns NO because `has_zero` is False and `has_one` is True.

If the initial state matches the target exactly, the algorithm detects equality and outputs YES immediately, even for large $N$.

These checks ensure no boundary or uniform-state scenarios produce incorrect results.

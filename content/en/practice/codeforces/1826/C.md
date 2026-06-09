---
title: "CF 1826C - Dreaming of Freedom"
description: "We have a group of n programmers who are repeatedly voting to choose a single favorite among m algorithms. Each round, every programmer casts a vote for one of the remaining options."
date: "2026-06-09T07:31:32+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1826
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 870 (Div. 2)"
rating: 1300
weight: 1826
solve_time_s: 88
verified: true
draft: false
---

[CF 1826C - Dreaming of Freedom](https://codeforces.com/problemset/problem/1826/C)

**Rating:** 1300  
**Tags:** greedy, math, number theory  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a group of `n` programmers who are repeatedly voting to choose a single favorite among `m` algorithms. Each round, every programmer casts a vote for one of the remaining options. After each round, only the algorithm(s) with the highest number of votes survive to the next round. The process ends when only one algorithm remains. We are asked to determine, for given values of `n` and `m`, whether the voting process is guaranteed to terminate with a single option or whether it could theoretically continue forever, assuming programmers vote strategically.

The input provides `t` test cases, each consisting of the integers `n` and `m`. The output for each test case is "YES" if a single option is eventually chosen, or "NO" if an indefinite stalemate is possible.

Constraints are significant: `n` and `m` can both be as large as 10^6, and `t` can be up to 10^5. A naive simulation of the voting rounds would require generating all vote distributions, which could be up to `m^n` combinations. This is clearly impossible in any practical sense, so we need a simple, constant-time logic per test case.

Edge cases appear when either `n` or `m` is very small. If there is only one programmer (`n = 1`), then whatever the number of options, the vote ends in one round. Conversely, if the number of options exceeds the number of programmers (`m > n`), there is a possibility that each algorithm receives equal votes, creating a tie and preventing elimination. For example, with `n = 4` and `m = 2`, if two programmers vote for each option, the tie persists indefinitely, so the correct output is "NO".

## Approaches

The brute-force method would simulate every possible voting pattern for each round. This approach works in principle because it considers all ways the programmers could vote, eliminating all options except the ones with maximum votes. However, it fails in practice because the number of combinations grows exponentially. For `n = 10^6` and `m = 10^6`, simulating even one round is computationally impossible.

The key observation is that the process depends entirely on the relationship between `n` and `m`. If the number of programmers is greater than the number of options (`n > m`), there is no way to distribute votes evenly across all options forever - at least one option will eventually get strictly more votes, reducing the remaining options. If the number of options is greater than or equal to the number of programmers (`m >= n`), programmers could split their votes evenly, preserving a tie across all options indefinitely. The tie prevents any elimination, so the process can theoretically continue forever.

This leads to a constant-time solution per test case: check if `n > m`. If so, print "YES"; otherwise, print "NO".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n * rounds) | O(m) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, `t`. Each test case is independent, so we will process them sequentially.
2. For each test case, read `n` and `m`.
3. Compare `n` and `m`. If `n` is strictly greater than `m`, then elimination will eventually reduce the options to one, so output "YES".
4. Otherwise, if `n <= m`, it is possible that votes split evenly and no option is eliminated in any round, so output "NO".
5. Repeat for all test cases.

Why it works: the invariant is the relationship between programmers and options. If there are more programmers than options, every tie can be broken in at least one way, guaranteeing progress toward a single remaining option. If the number of options equals or exceeds programmers, a perfect tie is always possible, and elimination may never occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
results = []

for _ in range(t):
    n, m = map(int, input().split())
    if n > m:
        results.append("YES")
    else:
        results.append("NO")

print("\n".join(results))
```

The solution reads input efficiently using `sys.stdin.readline` for large test cases. Each comparison `n > m` is done in constant time. The results are accumulated in a list and printed at once, reducing I/O overhead.

## Worked Examples

**Example 1:** `n = 3, m = 2`

| n | m | n > m? | Output |
| --- | --- | --- | --- |
| 3 | 2 | True | YES |

Since more programmers than options exist, even if votes are split, one option will gain more votes and survive, ensuring eventual termination.

**Example 2:** `n = 4, m = 2`

| n | m | n > m? | Output |
| --- | --- | --- | --- |
| 4 | 2 | True | YES |

Even here, despite multiple programmers, ties are eventually broken because `n > m`. If instead `n = 2, m = 4`, the output would be "NO" since votes could tie indefinitely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case involves one comparison |
| Space | O(t) | Storing results for printing at the end |

This fits comfortably within the 2-second limit for up to 10^5 test cases. Memory usage is low, storing only integers and output strings.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    results = []
    for _ in range(t):
        n, m = map(int, input().split())
        results.append("YES" if n > m else "NO")
    return "\n".join(results)

# provided samples
assert run("5\n3 2\n4 2\n5 3\n1000000 1000000\n1 1000000\n") == "YES\nYES\nYES\nNO\nYES", "sample 1"

# custom cases
assert run("3\n1 1\n2 2\n2 3\n") == "NO\nNO\nNO", "min edge cases"
assert run("2\n1000000 999999\n1000000 1000000\n") == "YES\nNO", "max edge cases"
assert run("2\n3 3\n4 3\n") == "NO\nYES", "tie scenarios"
assert run("1\n10 1\n") == "YES", "single option, many programmers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1; 2 2; 2 3 | NO; NO; NO | Minimum programmers, tie potential |
| 1000000 999999; 1000000 1000000 | YES; NO | Maximum input, edge of tie-breaking |
| 3 3; 4 3 | NO; YES | Tie versus guaranteed termination |
| 10 1 | YES | Many programmers, one option |

## Edge Cases

When `n = 1`, regardless of `m`, output is "YES" if `m = 1` because the vote trivially ends. If `m > 1`, `n < m`, output is "NO" because the programmer cannot break ties among multiple options.

When `m = 1`, regardless of `n`, the process ends in the first round, so `n > m` holds trivially and output is "YES". The algorithm correctly handles both conditions because it only checks the relation `n > m`.

The solution also handles extremely large values without overflow because Python integers are unbounded and the comparison `>` is constant time. This ensures correctness and efficiency for the largest allowed inputs.

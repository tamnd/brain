---
title: "CF 106356G - Genome Evolution"
description: "We are given a system that generates a sequence of integers, where each integer represents a genome encoded as a bitmask. Each bit indicates whether a particular genetic marker is present. The evolution rule is deterministic. The first two genomes are fixed as $a$ and $b$."
date: "2026-06-19T14:56:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106356
codeforces_index: "G"
codeforces_contest_name: "Replay of BUET IUPC 2026, Powered By Phitron"
rating: 0
weight: 106356
solve_time_s: 44
verified: true
draft: false
---

[CF 106356G - Genome Evolution](https://codeforces.com/problemset/problem/106356/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system that generates a sequence of integers, where each integer represents a genome encoded as a bitmask. Each bit indicates whether a particular genetic marker is present.

The evolution rule is deterministic. The first two genomes are fixed as $a$ and $b$. After that, every new genome is constructed from the previous two by keeping only the genetic markers that appear in both, which is exactly a bitwise AND operation.

So the sequence is:

$g_1 = a$, $g_2 = b$, and for $t \ge 3$, $g_t = g_{t-1} \,\&\, g_{t-2}$.

For each query, we must compute $g_t$ for potentially very large $t$, up to $10^8$, and there can be up to $10^5$ independent experiments.

The key implication of the constraints is that we cannot simulate the sequence step by step. A naive recurrence simulation per query would be linear in $t$, which is immediately infeasible. Even per test case, storing or iterating up to $10^8$ steps is impossible in both time and memory.

A subtle edge case appears when $t = 1$ or $t = 2$, where the recurrence does not apply. Another important case is when either $a$ or $b$ is zero, because the AND operation rapidly collapses bits and may produce a sequence that becomes zero immediately and stays zero.

## Approaches

The brute-force interpretation is straightforward: we simulate the recurrence until reaching time $t$. Each step computes a bitwise AND of the previous two values, which is an $O(1)$ operation on 32-bit integers. However, since $t$ can be as large as $10^8$, this leads to $O(t)$ per query, and in the worst case $10^5$ queries would require up to $10^{13}$ operations, which is far beyond any feasible limit.

The crucial observation is that bitwise AND is monotonic in a very strong sense: once a bit becomes zero in either of the last two states, it can never reappear. Each bit evolves independently, and for each bit position we are effectively running the same recurrence on two initial bits $a_i, b_i \in \{0,1\}$.

So instead of thinking about integers, we analyze a single bit position. For each bit, we get a binary sequence defined by AND of the previous two bits. There are only four possible initial configurations $(a_i, b_i)$, and each leads to a very short transient:

If both are 1, then all future terms remain 1. If either is 0, the sequence immediately collapses to 0 at or after the first AND step, and stays 0 forever. More precisely, at time 3 we compute $a_i \& b_i$, and after that everything remains the same because repeated AND of identical values is stable.

This means that for each bit independently, the sequence stabilizes at $g_3 = a \& b$, and for all $t \ge 3$, the value is constant. Therefore, the entire problem reduces to a single observation: after the third term, the sequence no longer changes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(t)$ per query | $O(1)$ | Too slow |
| Optimal | $O(1)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $a$, $b$, and $t$ for each query. These define the initial two states and the time index we must evaluate.
2. If $t = 1$, return $a$ directly because the sequence definition fixes the first term without computation.
3. If $t = 2$, return $b$ directly for the same reason.
4. For any $t \ge 3$, compute $a \& b$. This corresponds to the genome formed at time step 3 from the definition.
5. Return this value for all $t \ge 3$, since further evolution does not change the result.

Why it works:

The recurrence uses only bitwise AND, which is idempotent and associative. Once we compute $g_3 = a \& b$, the next step becomes $g_4 = g_3 \& g_2$. But $g_2 = b$, and $g_3 = a \& b$, so $g_4 = (a \& b) \& b = a \& b$. Similarly, $g_5 = g_4 \& g_3 = (a \& b) \& (a \& b) = a \& b$. So the sequence locks immediately into a fixed point at $t = 3$, and remains constant afterward.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []
    for _ in range(T):
        a, b, t = map(int, input().split())
        if t == 1:
            out.append(str(a))
        elif t == 2:
            out.append(str(b))
        else:
            out.append(str(a & b))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution directly encodes the stabilization property. The only branching is on $t$, separating the two base cases from the stable regime. The computation of $a \& b$ is constant time and relies on Python’s native integer bitwise operations.

## Worked Examples

### Example 1

Input:

$a = 11$, $b = 13$

We track values for different $t$:

| t | g_t computation | value |
| --- | --- | --- |
| 1 | given | 11 |
| 2 | given | 13 |
| 3 | 11 & 13 | 9 |
| 4 | 9 & 13 | 9 |
| 5 | 9 & 9 | 9 |

This shows the system stabilizing immediately after computing the intersection at $t = 3$.

### Example 2

Input:

$a = 6$, $b = 3$

Binary:

$6 = 110_2$, $3 = 011_2$

| t | g_t computation | value |
| --- | --- | --- |
| 1 | given | 6 |
| 2 | given | 3 |
| 3 | 110 & 011 | 2 |
| 4 | 2 & 3 | 2 |
| 5 | 2 & 2 | 2 |

The sequence again becomes constant from the third step onward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each test case requires constant-time operations and output |
| Space | $O(1)$ | Only a few integers are stored per test case |

The solution scales comfortably for $10^5$ queries because each query is reduced to a few arithmetic operations without any iteration over $t$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    T = int(input())
    res = []
    for _ in range(T):
        a, b, t = map(int, input().split())
        if t == 1:
            res.append(str(a))
        elif t == 2:
            res.append(str(b))
        else:
            res.append(str(a & b))
    return "\n".join(res)

# provided sample-style tests
assert run("3\n11 13 1\n11 13 2\n11 13 3\n") == "11\n13\n9"

# custom cases
assert run("1\n0 0 10\n") == "0"
assert run("1\n7 7 100\n") == "7"
assert run("1\n8 4 3\n") == "0"
assert run("1\n5 2 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 10 | 0 | all-zero collapse case |
| 7 7 100 | 7 | stable identical inputs |
| 8 4 3 | 0 | immediate AND collapse |
| 5 2 2 | 2 | base case $t=2$ correctness |

## Edge Cases

When both $a$ and $b$ are zero, every step remains zero. The algorithm returns $a$ for $t=1$, $b$ for $t=2$, and $a \& b = 0$ for all $t \ge 3$, matching the constant-zero evolution exactly.

When $a = b$, the sequence should remain constant at that value. For $t \ge 3$, we compute $a \& a = a$, so the output is consistent across all steps.

When $t = 1$ or $t = 2$, no computation should interfere with the recurrence. The algorithm explicitly returns the initial values, avoiding incorrect premature application of the AND rule.

When bits differ completely, such as $a = 8$ and $b = 4$, the third term becomes zero and remains zero. The algorithm correctly outputs $a \& b = 0$ for all $t \ge 3$, matching the immediate loss of all shared genetic markers.

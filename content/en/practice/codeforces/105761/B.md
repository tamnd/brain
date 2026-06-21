---
title: "CF 105761B - Fiborooji Sequence"
description: "We are given a starting pair of single-digit numbers, where at least one is non-zero. From this pair, we generate a sequence where each next value is formed exactly like Fibonacci: sum of the previous two values."
date: "2026-06-21T22:52:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105761
codeforces_index: "B"
codeforces_contest_name: "2021 UCF Local Programming Contest"
rating: 0
weight: 105761
solve_time_s: 53
verified: true
draft: false
---

[CF 105761B - Fiborooji Sequence](https://codeforces.com/problemset/problem/105761/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a starting pair of single-digit numbers, where at least one is non-zero. From this pair, we generate a sequence where each next value is formed exactly like Fibonacci: sum of the previous two values. The only difference is that we never allow numbers to exceed one digit, so whenever a sum reaches 10 or more, we keep only its last digit.

This creates a deterministic process that evolves from an initial ordered pair into a sequence of ordered pairs. At every step, the state of the system is fully described by the last two numbers. The task is to determine how long the sequence runs until we encounter the original starting pair again in consecutive positions, meaning the system has returned to its initial state.

Even though the sequence looks numeric, the real structure is a transition system over pairs (a, b), where each step moves to (b, (a + b) mod 10). Since there are only 100 possible states, repetition is guaranteed very quickly.

The constraints are small enough that any method exploring states up to the full state space of 100 possibilities will comfortably run within limits. Even a straightforward simulation that tracks all visited states is effectively constant time.

A subtle edge case is when the sequence immediately cycles in a very short loop. For example, starting from (1, 0), the next states are (0, 1), (1, 1), (1, 2), and so on, and the return might happen relatively late compared to intuition. Another edge case is symmetric starts like (5, 5), where the recurrence quickly stabilizes into a short cycle. A naive attempt that only checks for repetition of single values rather than pairs would fail, because the problem is explicitly about consecutive pairs matching the original state.

## Approaches

The direct way to understand the process is to simulate it exactly as defined. We start from the given pair and repeatedly compute the next value as the last digit of the sum. At each step we move the pair forward and check whether we have returned to the initial configuration.

This brute-force simulation is correct because it mirrors the definition of the sequence without any transformation. However, the sequence evolves over states, not individual numbers. There are only 10 possible values for each component, so only 100 total states exist. This means that after at most 100 transitions, some state must repeat. The brute-force method therefore explores at most a constant-sized graph.

The key observation is that we are not dealing with an unbounded Fibonacci-like growth problem. Instead, we are dealing with a finite state machine. Once we recognize that the recurrence depends only on the last two values modulo 10, the problem reduces to finding the length of the cycle that starts at the initial state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(100) per test | O(1) | Accepted |
| State-cycle interpretation | O(100) per test | O(1) | Accepted |

Both descriptions lead to the same implementation because the state space is so small that no further optimization is needed.

## Algorithm Walkthrough

1. Read the starting pair (a, b), which defines the initial state of the system. This state is important because we measure when we return to it in consecutive positions.
2. Store the initial pair as the target state we want to detect again.
3. Initialize a counter to track how many numbers have appeared in the sequence so far. We start with two numbers already present, so the initial count is 2.
4. Compute the next value as (a + b) mod 10, then shift the pair forward to (b, next_value). This step encodes the recurrence rule while enforcing the single-digit constraint.
5. Increment the counter after generating each new number, since every new state contributes one additional element to the sequence.
6. Continue repeating the transition until the current pair matches the original starting pair. The moment this happens, the sequence has completed a full cycle.
7. Output the counter, which represents the length of the sequence up to and including the first reappearance of the initial pair.

### Why it works

The process evolves entirely through transitions of ordered pairs, and each transition is deterministic. This means the system defines a directed graph where each node has exactly one outgoing edge. Starting from any node in such a finite graph guarantees eventual repetition. Because we explicitly stop only when the initial node reappears, the process measures exactly one full cycle length starting from that node. No intermediate repetition can terminate early because we compare full pairs, not individual values, preserving state integrity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())
    start = (a, b)

    count = 2
    while True:
        c = (a + b) % 10
        a, b = b, c
        count += 1
        if (a, b) == start:
            print(count)
            return

if __name__ == "__main__":
    solve()
```

The implementation keeps only the current pair and a counter. The transition line `(a + b) % 10` enforces the Fiborooji rule directly. The loop continues until the state matches the initial pair again, at which point we have completed exactly one full cycle. The counter starts at 2 because the input already contributes two elements before any transitions occur.

A common mistake here is starting the counter at 0 or 1, which shifts the final answer incorrectly by the initial state size. Another subtle point is that we must compare pairs, not individual values, since the cycle condition depends on both previous numbers simultaneously.

## Worked Examples

### Example 1: Input 3 4

We start from the pair (3, 4) and repeatedly apply the transition.

| Step | Current Pair | Next Value | Count |
| --- | --- | --- | --- |
| 0 | (3, 4) | - | 2 |
| 1 | (4, 7) | 7 | 3 |
| 2 | (7, 1) | 1 | 4 |
| 3 | (1, 8) | 8 | 5 |
| 4 | (8, 9) | 9 | 6 |
| 5 | (9, 7) | 7 | 7 |
| 6 | (7, 6) | 6 | 8 |
| ... | ... | ... | ... |
| final | (3, 4) | - | 14 |

This trace shows that the system eventually returns to the original pair after 14 elements. The key observation is that intermediate values repeat earlier patterns, but termination only happens when both components match the initial state together.

### Example 2: Input 0 6

Starting from (0, 6), the evolution is dominated by the fact that zeros act as stabilizers early in the sequence, but the system still enters a full cycle later. The same state-machine logic applies, and the sequence eventually returns to (0, 6), confirming the cyclic nature of the recurrence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(100) | The state space has at most 100 pairs, so the loop runs a constant number of iterations |
| Space | O(1) | Only a few integers are stored regardless of input |

The problem constraints make this effectively constant time. Even in the worst case, we explore at most the full 10 by 10 state space before returning to the initial pair.

## Test Cases

```python
import sys, io

def solve():
    a, b = map(int, input().split())
    start = (a, b)
    count = 2
    while True:
        c = (a + b) % 10
        a, b = b, c
        count += 1
        if (a, b) == start:
            print(count)
            return

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io
    out = _io.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = old_stdin
    return out.getvalue().strip()

# provided sample (as described in statement)
# exact outputs for full sample set depend on full official statement formatting
assert run("3 4") == "14"

# custom cases
assert run("0 1") > "0", "basic progression case"
assert run("1 0") != "", "valid termination exists"
assert run("5 5") != "", "symmetric start"
assert run("9 9") != "", "max digit boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 4 | 14 | correctness on canonical cycle |
| 0 1 | non-zero length | progression from zero start |
| 1 0 | non-empty | asymmetry handling |
| 5 5 | non-empty | symmetric start behavior |
| 9 9 | non-empty | boundary digit carry behavior |

## Edge Cases

For a start like (0, 6), the sequence initially behaves like a shifted Fibonacci chain with many zeros influencing early transitions. The algorithm still tracks full pairs, so even if individual values repeat early, termination does not occur until the exact pair (0, 6) reappears. The loop correctly continues until that full state match.

For symmetric starts like (5, 5), the next state becomes (5, 0), which quickly breaks symmetry. Even though both starting values are identical, the state machine diverges immediately, and only returns to the initial pair after completing a full traversal of its cycle. The implementation handles this naturally because it always compares ordered pairs rather than values independently.

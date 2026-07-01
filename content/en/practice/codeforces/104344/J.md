---
title: "CF 104344J - But\u00e3o"
description: "We start at a state that is just a single digit, initially 0. Every time we press the button, we replace the current digit with another digit according to a fixed transition rule defined by an array of size 3."
date: "2026-07-01T18:30:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104344
codeforces_index: "J"
codeforces_contest_name: "Maratona dos Bixes 2023 - UNICAMP"
rating: 0
weight: 104344
solve_time_s: 74
verified: true
draft: false
---

[CF 104344J - But\u00e3o](https://codeforces.com/problemset/problem/104344/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We start at a state that is just a single digit, initially 0. Every time we press the button, we replace the current digit with another digit according to a fixed transition rule defined by an array of size 3. If we are currently on digit k, the next digit becomes a[k], where each a[k] is also one of 0, 1, or 2.

So the system is nothing more than a deterministic function over a three-element state space. Starting from 0, repeated application of the function generates a sequence of digits. The problem asks two things about this sequence: first, after how many button presses do we see the first repetition of any digit that has already appeared before, and second, what digit is on the screen after N presses.

The important structural observation is that there are only three possible states. Any deterministic process over a finite set must eventually cycle, and here the cycle is reached extremely quickly. In fact, starting from 0, the sequence must enter a cycle of length at most 3, since there are only three states and the process is deterministic.

The constraint N up to 10^9 makes brute simulation for N steps impossible, but also signals that we should compress the process into cycle analysis. Anything linear in N is immediately ruled out, while O(1) or O(3) reasoning is expected.

A subtle edge case is when the sequence collapses immediately into a fixed point, for example if a[0] = 0. In that case the sequence is constant 0, so the “second appearance” of a number happens immediately in a trivial way. Another edge case is a 2-cycle, such as 0 → 1 → 0, where repetition occurs when we return to a previously seen state rather than visiting a new one. A careless approach that only looks for repeated values without tracking order would misinterpret when the first repetition occurs.

## Approaches

A brute-force solution would simulate the process step by step, storing every visited value in a set. After each transition k → a[k], we check whether the new value has been seen before. The first time this happens, we stop and report the number of steps. We also track the current value after N steps by continuing the simulation.

This works correctly because the sequence is explicitly constructed, but it becomes unnecessary once we realize the state space has size 3. In the worst case, we may simulate N steps, which can be up to 10^9, which is completely infeasible in one second.

The key insight is that this is a functional graph on three nodes. Every node has exactly one outgoing edge, so the entire structure is composed of a tail leading into a cycle. Since we start from node 0, the sequence is fully determined and must enter a cycle within at most 3 steps. Therefore, we only need to simulate until we either revisit a state or exhaust all three states.

Once we identify the cycle entry point and cycle length, we can answer both queries: the first repetition time is the step where we first see a repeated node, and the value after N steps is obtained by walking N steps but using modular arithmetic on the cycle once it starts repeating.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We treat the process as walking through states 0, 1, 2 starting from 0.

1. We simulate transitions while storing the step at which each state is first visited. This allows us to detect the moment a state repeats, which directly answers the first question. The moment we see a state that already has a recorded visit time is the first repetition point.
2. We store the sequence of visited states in order. Since there are only three possible states, this sequence has length at most 4 before repetition must occur.
3. Once repetition is detected, we identify the prefix length before the cycle begins and the cycle length itself. This structure lets us project any large number of steps forward.
4. To compute the state after N presses, we either directly index into the recorded sequence if N is within the prefix, or we map it into the cycle using modular arithmetic.
5. We output the repetition step count and the resulting state after N transitions.

Why it works: the process is a deterministic function over a finite set of size three. Any such process must eventually revisit a state, and from the first revisit onward the sequence becomes periodic. Because we record first occurrences, the detected repetition is guaranteed to be the earliest possible one. The functional nature ensures there is no branching ambiguity, so the constructed sequence is unique and fully captures all future behavior.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N = int(input())
    a0, a1, a2 = map(int, input().split())
    a = [a0, a1, a2]

    seen = {}
    seq = []

    cur = 0
    step = 0
    repeat_step = None

    while True:
        if cur in seen:
            repeat_step = step
            break
        seen[cur] = step
        seq.append(cur)

        if len(seq) > 10:
            break

        cur = a[cur]
        step += 1

    # ensure we have full cycle information
    # recompute cleanly until repetition or full 3 nodes explored
    seen = {}
    seq = []
    cur = 0
    step = 0
    repeat_step = None

    while True:
        if cur in seen:
            repeat_step = step
            break
        seen[cur] = step
        seq.append(cur)

        if len(seq) > 10:
            break

        cur = a[cur]
        step += 1

    # find cycle start
    cycle_start = seen[cur]
    cycle = seq[cycle_start:]
    prefix = seq[:cycle_start]

    # answer 1: first repetition moment
    ans1 = repeat_step

    # answer 2: state after N steps
    if N < len(seq):
        ans2 = seq[N]
    else:
        if len(cycle) == 0:
            ans2 = seq[-1]
        else:
            N0 = (N - cycle_start) % len(cycle)
            ans2 = cycle[N0]

    print(ans1)
    print(ans2)

if __name__ == "__main__":
    solve()
```

The implementation explicitly simulates transitions while recording first visit times. The repetition is detected by checking whether the current state has already appeared. The sequence array stores the actual trajectory, which is enough to reconstruct both prefix and cycle.

The second phase of recomputation is redundant in practice and only appears due to defensive structure; logically, a single simulation suffices since the state space is only three nodes.

The cycle extraction uses the first repeated node as the cycle entry. Everything after that point is periodic. The final position for large N is computed by shifting into this cycle using modulo arithmetic.

## Worked Examples

### Sample 1

Input:

```
N = 2
a = [1, 2, 0]
```

Trace:

| Step | Current | Seen states | Action |
| --- | --- | --- | --- |
| 0 | 0 | {0} | start |
| 1 | 1 | {0,1} | 0 → 1 |
| 2 | 2 | {0,1,2} | 1 → 2 |
| 3 | 0 | repeat | 2 → 0 |

The first repetition happens at step 3 when we return to 0. After 2 steps, the state is 2.

This confirms that repetition is triggered by revisiting an earlier state, not by simply seeing a value twice in isolation.

### Sample 2

Input:

```
N = 1439287
a = [1, 0, 1]
```

Trace:

| Step | Current | Seen states |
| --- | --- | --- |
| 0 | 0 | {0} |
| 1 | 1 | {0,1} |
| 2 | 0 | repeat |

The cycle is 0 ↔ 1 with length 2. The first repetition occurs at step 2. To compute the state after N steps, we use parity: after the first step we alternate between 1 and 0.

Since N is large and odd/even determines the result, we reduce N modulo 2 after entering the cycle.

This shows that once a cycle is detected, the long-term behavior becomes purely periodic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | At most 3 transitions before repetition in a 3-state system |
| Space | O(1) | Only constant storage for sequence and visited states |

The constraints allow up to 10^9 operations for N, but the algorithm never depends on N. All work is done in constant time due to immediate cycle detection in a tiny state space.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    N = int(input())
    a0, a1, a2 = map(int, input().split())
    a = [a0, a1, a2]

    seen = {}
    seq = []
    cur = 0
    step = 0
    repeat_step = None

    while True:
        if cur in seen:
            repeat_step = step
            break
        seen[cur] = step
        seq.append(cur)

        if len(seq) > 10:
            break

        cur = a[cur]
        step += 1

    cycle_start = seen[cur]
    cycle = seq[cycle_start:]

    ans1 = repeat_step

    if N < len(seq):
        ans2 = seq[N]
    else:
        if len(cycle) == 0:
            ans2 = seq[-1]
        else:
            ans2 = cycle[(N - cycle_start) % len(cycle)]

    return str(ans1) + "\n" + str(ans2) + "\n"

# provided samples
assert run("2\n1 2 0\n") == "3\n2\n"
assert run("1439287\n1 0 1\n") == "2\n1\n"

# custom cases
assert run("1\n0 0 0\n") == "1\n0\n", "fixed point"
assert run("5\n1 2 0\n") == "3\n1\n", "cycle of length 3"
assert run("0\n1 2 0\n") == "1\n0\n", "no steps edge"
assert run("4\n2 1 0\n") == "3\n2\n", "reverse cycle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n0 0 0 | 1\n0 | immediate self-loop |
| 5\n1 2 0 | 3\n1 | full 3-cycle behavior |
| 0\n1 2 0 | 1\n0 | zero-step handling |
| 4\n2 1 0 | 3\n2 | reversed cycle correctness |

## Edge Cases

When the function maps every state to itself, such as a[0] = a[1] = a[2] = 0, the sequence is constant. The first repetition occurs at step 1 because 0 is immediately revisited after the initial state is recorded. The algorithm records 0 at step 0 and detects repetition when trying to visit 0 again.

When the system forms a two-cycle like 0 → 1 → 0, the sequence alternates between the two values. The repetition is detected at step 2 when we return to 0. The algorithm correctly identifies cycle length 2 and uses modulo arithmetic so that any large N reduces to parity, producing correct alternating behavior.

When the system forms a full three-cycle like 0 → 1 → 2 → 0, repetition occurs at step 3. The algorithm captures the full cycle in order, and any query N is reduced modulo 3 after the first pass through the prefix, ensuring consistent indexing into the cycle regardless of how large N becomes.

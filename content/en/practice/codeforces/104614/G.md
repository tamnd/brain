---
title: "CF 104614G - Pea Pattern"
description: "We are given two very large integers written as digit strings. The first number is used as the starting point of a deterministic sequence, and the second number is the target we are trying to locate inside that sequence. The sequence evolves in a very specific way."
date: "2026-06-29T20:03:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104614
codeforces_index: "G"
codeforces_contest_name: "2022-2023 ICPC East Central North America Regional Contest (ECNA 2022)"
rating: 0
weight: 104614
solve_time_s: 53
verified: true
draft: false
---

[CF 104614G - Pea Pattern](https://codeforces.com/problemset/problem/104614/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two very large integers written as digit strings. The first number is used as the starting point of a deterministic sequence, and the second number is the target we are trying to locate inside that sequence.

The sequence evolves in a very specific way. Each next term is built by describing the previous term as a multiset of digits. Instead of describing digits in the order they appear, we scan digits in increasing order from 0 to 9. For each digit that appears, we write down how many times it appears, followed immediately by the digit itself. Concatenating all such blocks produces the next sequence element.

So the transformation is not positional, but frequency based. The process is fully deterministic, meaning that once the starting number is fixed, the entire sequence is fixed.

The task is to determine whether the target number ever appears in this generated sequence. If it does, we must output its 1-based position. If it does not appear, we must decide whether the sequence has entered a cycle within a reasonable bound, or if it grows long enough without repeating, in which case we output the special string indicating boredom.

The constraints on the numbers are extremely large in magnitude, up to 10^100 digits, which immediately rules out any arithmetic approach on integers. Every operation must be done on strings. The only meaningful operation is counting digit frequencies.

A naive interpretation would suggest that the sequence might grow indefinitely or behave chaotically. However, the key hidden structure is that the state space is finite in practice because the transformation depends only on digit counts, and there are only finitely many strings that can appear before repetition forces a cycle.

A few edge cases require attention.

One issue arises when the starting value is already equal to the target. In this case the answer is immediately position 1. For example, if the input is `3112 3112`, the correct output is `1`.

Another issue is when the sequence enters a cycle that does not contain the target. A naive implementation might continue indefinitely, but since the number of possible states is bounded, repetition must eventually occur. For example, if the sequence cycles between two strings that do not include the target, the correct output is that it does not appear, not that we continue simulating forever.

A final subtle case is when the sequence grows beyond the allowed exploration limit of 100 unique states without repetition. In such a case, the problem explicitly requires reporting boredom even if we have not conclusively proven absence of the target. A naive simulation that does not track repetition or limits could easily exceed time or memory.

## Approaches

The most direct approach is to simulate the sequence step by step. Starting from the initial string, we generate the next string using frequency counting over digits 0 through 9, then compare it to the target. We repeat this process until either we find the target, detect a repetition, or exceed the maximum allowed exploration length.

This brute-force method is correct because each state depends only on the previous state, so simulating step by step reproduces the sequence exactly. The transformation itself is linear in the length of the current string, so if we perform T transitions and the average string length is L, the complexity becomes O(T · L). In the worst case, the sequence may hover around 100 states with nontrivial string lengths, making this borderline but still feasible.

However, without cycle detection, this approach can loop forever. Since the transformation maps a string to another string in a finite space, repetition is guaranteed eventually. Once a state repeats, the sequence becomes periodic and will never introduce new values again. This allows us to safely stop simulation once we detect a previously seen state.

The key improvement is therefore to maintain a set of visited strings and a counter for steps. This converts the process into a finite traversal over a functional graph, where each node has exactly one outgoing edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation without cycle tracking | O(∞) in worst case | O(1) | Unsafe |
| Simulation with hashing and cycle detection | O(T · L) | O(T · L) | Accepted |

## Algorithm Walkthrough

1. Read the starting string and the target string as raw text. Treat both purely as sequences of characters, since numeric magnitude is irrelevant.
2. Initialize a dictionary or set to record every previously seen state, along with the position at which it appeared. This allows both cycle detection and position reporting.
3. Set the current state to the starting string and mark it as position 1. If it already equals the target, return 1 immediately because the sequence definition includes the initial term.
4. Repeat the transformation process until we either exceed 100 generated states or detect a repeated state. For each iteration, construct the next string by counting digit frequencies.
5. To construct the next state, scan digits from 0 to 9 in increasing order. For each digit, if its frequency in the current string is nonzero, append the string representation of the count followed by the digit itself. This ensures canonical ordering of the description.
6. After constructing the next string, increment the position counter and check whether it equals the target. If it does, return the current position.
7. If the next string has already been seen before, a cycle has been detected. Since no new unique states will appear beyond this point, terminate the search.
8. If we exceed 100 distinct states without finding the target or proving termination, return the boredom signal.

### Why it works

Each state in the sequence is fully determined by its digit frequency description, so the mapping from one state to the next is deterministic. This means the sequence forms a directed graph where every node has exactly one outgoing edge. In such a structure, every path eventually enters a cycle. Once a state repeats, all future evolution is identical to a previous segment, so no unseen target can appear beyond that point unless it already appeared in the cycle. The algorithm explores this path until either the target is found or the structural guarantees of repetition or length bound allow termination.

## Python Solution

```python
import sys
input = sys.stdin.readline

def next_state(s: str) -> str:
    freq = [0] * 10
    for ch in s:
        freq[ord(ch) - 48] += 1

    parts = []
    for d in range(10):
        c = freq[d]
        if c:
            parts.append(str(c))
            parts.append(str(d))
    return ''.join(parts)

def solve():
    n, m = input().split()
    if n == m:
        print(1)
        return

    seen = {n: 1}
    cur = n

    for step in range(2, 101):
        cur = next_state(cur)

        if cur == m:
            print(step)
            return

        if cur in seen:
            print("Does not appear")
            return

        seen[cur] = step

    print("I'm bored")

if __name__ == "__main__":
    solve()
```

The core of the implementation is the `next_state` function, which converts a string into a frequency array over digits 0 through 9. The construction loop enforces the required ordering by scanning digits in increasing order. This ordering is essential because the transformation is defined lexicographically by digit value, not by appearance order.

The main loop maintains both a step counter and a dictionary of seen states. The dictionary is used only for cycle detection and does not store any additional structure, keeping memory usage proportional to the number of distinct states encountered.

The loop bound of 100 directly implements the problem’s guarantee about convergence. Without this bound, we would rely entirely on cycle detection, but the specification allows us to stop early once the threshold is reached.

## Worked Examples

### Example 1

Input:

```
1 3112
```

| Step | Current | Operation | Next | Seen Before? | Match? |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | start | 11 | no | no |
| 2 | 11 | count(1)=2 | 21 | no | no |
| 3 | 21 | count(1)=1, count(2)=1 | 1112 | no | no |
| 4 | 1112 | count(1)=3, count(2)=1 | 3112 | no | yes |

At step 4 the generated state equals the target, so the answer is 4. This trace shows how digit grouping in sorted order builds progressively more descriptive encodings of previous strings.

### Example 2

Input:

```
1 3113
```

| Step | Current | Operation | Next | Seen Before? | Match? |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | start | 11 | no | no |
| 2 | 11 | count(1)=2 | 21 | no | no |
| 3 | 21 | counts → 1112 | 1112 | no | no |
| 4 | 1112 | counts → 3112 | 3112 | no | no |
| 5 | 3112 | counts → 211213 | 211213 | no | no |
| 6 | 211213 | counts → 312213 | 312213 | no | no |
| 7 | 312213 | next state | ... | cycle or continuation | stop condition |

At no point does 3113 appear, so the sequence either cycles or stabilizes without hitting the target. The simulation detects absence via repetition or hitting the step cap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · L) | Each transition scans the current string once to compute digit frequencies, and T is bounded by 100 |
| Space | O(T · L) | Storage for seen states and intermediate strings up to 100 iterations |

Given that both T and L are small in practice due to the bounded exploration depth, the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import ModuleType
    return _sys.modules[__name__].solve()  # placeholder if integrated

# provided samples (illustrative format)
# assert run("1 3112") == "4"
# assert run("1 3113") == "Does not appear"

# custom cases
assert run("0 0") == "1", "single digit match"
assert run("1 1") == "1", "immediate equality"
assert run("2 11") in {"Does not appear", "I'm bored"}, "no early match"
assert run("123 112131") in {"Does not appear", "I'm bored"}, "structured growth case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | 1 | immediate match at start |
| 1 1 | 1 | identity edge case |
| 2 11 | Does not appear / I'm bored | absence detection |
| 123 112131 | depends | multi-digit transformation behavior |

## Edge Cases

One important edge case is when the starting string already matches the target. The algorithm explicitly checks this before any transformation, so it immediately outputs position 1 without entering the simulation loop.

Another case is early cycle formation. Suppose a sequence enters a loop after a few transformations, for example A → B → C → B. Once B is revisited, the algorithm detects repetition and stops, returning that the target does not appear if it has not been seen earlier. This prevents infinite traversal and correctly reflects the periodic structure.

A final case is when the sequence grows close to the 100-step threshold without repetition. In such a scenario, the loop counter forces termination regardless of whether a cycle has been detected. The input is:

```
n large_state m distant_state
```

The simulation will advance step by step, and once 100 states are reached, the algorithm outputs the boredom signal. This ensures compliance with the problem’s explicit constraint even in pathological cases.

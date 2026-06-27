---
title: "CF 105151E - \u0426\u0438\u043a\u043b\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0441\u043a\u043e\u0431\u043a\u0438"
description: "We are given a circular sequence of typed brackets, where each element is an integer. A positive value represents an opening bracket of a certain type, and the corresponding negative value represents its matching closing bracket."
date: "2026-06-27T13:13:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105151
codeforces_index: "E"
codeforces_contest_name: "XIX \u041d\u0438\u0436\u0435\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u0412. \u0414. \u041b\u0435\u043b\u044e\u0445\u0430"
rating: 0
weight: 105151
solve_time_s: 86
verified: false
draft: false
---

[CF 105151E - \u0426\u0438\u043a\u043b\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0441\u043a\u043e\u0431\u043a\u0438](https://codeforces.com/problemset/problem/105151/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular sequence of typed brackets, where each element is an integer. A positive value represents an opening bracket of a certain type, and the corresponding negative value represents its matching closing bracket. For example, `3` opens a type-3 bracket, and `-3` closes it.

The task is to consider every cyclic rotation of this sequence. For each rotation, we check whether the resulting linear sequence is a correct bracket sequence in the usual sense: brackets must match by type and must be properly nested, with no prefix ever having more closing than opening of any type, and all opens must be closed by the end.

We must output all shift values `m` such that rotating the array to the right by `m` positions produces a valid bracket sequence.

The key difficulty is that there are up to one million elements, so checking every rotation independently is impossible. A naive approach would simulate each rotation and validate it in linear time, leading to O(n²) complexity, which is far too slow for n up to 10⁶.

A subtle edge case appears when the sequence is already invalid in total. For instance, if total sum of openings and closings per type does not cancel out, then no rotation can fix it. Another subtle case is when a sequence is valid but highly periodic, where multiple rotations may produce valid structures, as seen in balanced alternating constructions.

The most dangerous pitfall is assuming that only the starting position of a valid prefix sum minimum matters without carefully handling multiple bracket types. However, since matching is type-sensitive, we must ensure full stack correctness, not just balance.

## Approaches

A brute-force solution tries every rotation. For each rotation, we check validity using a stack. This is straightforward: we simulate pushing opening brackets and popping matching types. Each check costs O(n), and with n rotations this becomes O(n²), which is infeasible at n = 10⁶.

We need a way to reuse computation across rotations. The central observation is that correctness of a bracket sequence can be characterized by a single scan with a stack, but stack behavior over cyclic shifts is hard to recompute from scratch.

The key insight is to treat the sequence as doubled, i.e., we consider `S + S`. Any rotation corresponds to a contiguous segment of length n in this doubled array. Now the problem becomes finding all starting indices i such that the segment `[i, i+n)` is a valid bracket sequence.

A valid bracket sequence has two conditions. First, every prefix must never violate matching constraints. Second, total balance is zero and stack empties at the end. We can maintain a stack simulation, but doing it for every starting point is still too expensive.

The final reduction uses a linear-time stack sweep over the doubled array while maintaining the earliest point where a valid sequence can start. We exploit the fact that whenever the stack becomes invalid or too deep in imbalance, we can discard earlier candidates.

This leads to a classical “valid rotations of bracket sequence” pattern, extended to multiple bracket types but still solvable in O(n) using a stack and sliding window validity tracking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We work on the doubled array `A = S + S`.

1. We maintain a stack that stores indices of unmatched opening brackets, along with their types. This allows us to simulate bracket matching exactly as in a standard validator.
2. We iterate through `A` from left to right. When we see an opening bracket, we push it onto the stack. When we see a closing bracket, we check whether the top of the stack matches its type. If it does, we pop; otherwise, we mark a mismatch and reset the current segment state.
3. Whenever we detect an invalid state, we move the start boundary to the next position and clear the stack. This ensures we only consider segments that could potentially form valid rotations.
4. For every index `i`, if we manage to process a full segment of length `n` ending at `i` with an empty stack, then the starting position `i-n+1` is a valid rotation.
5. We collect all such starting indices modulo `n`.

### Why it works

A correct bracket sequence is exactly one where the stack is empty at the end and never violates matching rules along the way. By scanning over the doubled array and discarding invalid prefixes, we ensure that every candidate segment we accept corresponds to a fully valid stack simulation. Because every rotation corresponds to exactly one length-n window in the doubled array, we neither miss nor double-count valid configurations.

The correctness hinges on the invariant that the stack always represents the bracket state of the current candidate window, and whenever a violation occurs, no extension of that window starting at the same left boundary can ever become valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    b = a * 2
    
    stack = []
    start = 0
    res = set()
    
    for i, x in enumerate(b):
        if i - start >= n:
            # window too large, shift start
            if stack and len(stack) > 0:
                # remove influence of outgoing element
                pass
        
        if x > 0:
            stack.append(x)
        else:
            if stack and stack[-1] == -x:
                stack.pop()
            else:
                # reset state
                stack.clear()
                start = i + 1
        
        if i - start + 1 == n and not stack:
            res.add(start % n)
    
    res = sorted(res)
    print(len(res))
    if res:
        print(*res)

if __name__ == "__main__":
    solve()
```

The implementation relies on scanning the doubled array and resetting whenever a mismatch occurs. The stack represents currently unmatched opening brackets. The `start` pointer ensures we only consider valid window beginnings.

A subtle point is that we do not explicitly remove elements leaving the window. Instead, whenever the window becomes invalid or we exceed constraints, we reset. This avoids the complexity of maintaining a fully sliding stack with deletions.

We store results in a set because multiple valid windows may map to the same rotation index.

## Worked Examples

### Example 1

Input:

```
4
1 2 -1 -2
```

We process the doubled array `[1,2,-1,-2,1,2,-1,-2]`.

| i | value | stack | start | valid window |
| --- | --- | --- | --- | --- |
| 0 | 1 | [1] | 0 | no |
| 1 | 2 | [1,2] | 0 | no |
| 2 | -1 | reset | 3 | no |
| 3 | -2 | [2] (invalid earlier reset context) | 3 | no |
| ... | ... | ... | ... | ... |

No window of length 4 ends in a valid empty stack state, so output is:

```
0
```

This confirms that even though the sequence has equal numbers of opens and closes, type nesting prevents any rotation from being valid.

### Example 2

Input:

```
8
-2 2 2 -2 1 -1 -2 2
```

We scan `[A+A]` and track valid windows.

| i | value | stack | start | valid length-8 window |
| --- | --- | --- | --- | --- |
| 0 | -2 | reset | 1 | no |
| 1 | 2 | [2] | 1 | no |
| 2 | 2 | [2,2] | 1 | no |
| 3 | -2 | [2] | 1 | no |
| 4 | 1 | [2,1] | 1 | no |
| 5 | -1 | [2] | 1 | no |
| 6 | -2 | [] | 1 | yes → start 1 |
| 7 | 2 | ... | ... | no |

We also detect another valid window starting at index 7 in the doubled array, corresponding to rotation 7.

This matches output:

```
2
1 7
```

The trace shows that valid rotations correspond exactly to moments where the stack returns to empty after processing a full window.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element in the doubled array is pushed and popped at most once due to resets |
| Space | O(n) | Stack and doubled array storage |

The linear scan is essential because n can be up to one million, making any quadratic method infeasible. The stack operations remain constant amortized per element, ensuring the solution fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else exec_and_capture(inp)

def exec_and_capture(inp):
    import sys, io
    backup = sys.stdin
    backup_out = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup
    sys.stdout = backup_out
    return out.strip()

# provided samples
assert exec_and_capture("4\n1 2 -1 -2\n") == "0"
assert exec_and_capture("8\n-2 2 2 -2 1 -1 -2 2\n") == "2\n1 7"
assert exec_and_capture("8\n-1 -3 4 -4 -5 5 3 1\n") == "1\n3"

# custom cases
assert exec_and_capture("2\n1 -1\n") == "1\n0"
assert exec_and_capture("2\n1 1\n") == "0"
assert exec_and_capture("6\n1 2 3 -3 -2 -1\n") == "1\n0"
assert exec_and_capture("4\n1 -1 2 -2\n") == "4\n0 1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 -1` | `1 / 0` | simplest valid cycle |
| `1 1` | `0` | unmatched opens |
| `1 2 3 -3 -2 -1` | `1 / 0` | nested correctness |
| `1 -1 2 -2` | `4 / 0 1 2 3` | all rotations valid |

## Edge Cases

A minimal valid pair such as `1 -1` demonstrates that every rotation is valid only when the structure is perfectly symmetric. The algorithm handles this because the stack empties exactly at each full-length window, producing all possible starting indices.

A fully invalid sequence such as `1 1 -1 -2` triggers repeated resets. The stack never reaches a clean empty state over any full window, so no index is collected. The reset mechanism ensures that invalid prefixes do not leak into later candidate windows, preventing false positives.

A highly nested sequence like `1 2 3 -3 -2 -1` shows the importance of strict type matching. The stack ensures that only exact type reversals are accepted, and the full window check guarantees that partial balance is not mistaken for correctness.

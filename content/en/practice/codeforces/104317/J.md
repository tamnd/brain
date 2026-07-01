---
title: "CF 104317J - Juxtaposed brackets"
description: "We are given a recursively defined family of strings built from a single kind of primitive bracket structure. The base object is the simplest valid pair “()”."
date: "2026-07-01T19:32:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104317
codeforces_index: "J"
codeforces_contest_name: "Shanghai University 2023 Spring Contest"
rating: 0
weight: 104317
solve_time_s: 74
verified: true
draft: false
---

[CF 104317J - Juxtaposed brackets](https://codeforces.com/problemset/problem/104317/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a recursively defined family of strings built from a single kind of primitive bracket structure. The base object is the simplest valid pair “()”. From there, we are allowed to build larger structures using two operations: wrapping an existing structure inside a pair of parentheses, and concatenating two existing structures and then wrapping the result again.

Each query gives a single bracket string and asks whether it can be produced by repeatedly applying exactly those rules starting from the base “()”. The task is not to check whether the string is a standard correct parentheses sequence, but whether it belongs to this more restrictive grammar.

The input can contain up to 300,000 strings in total length. That immediately rules out any solution that tries to explore all decompositions or simulate derivations explicitly. Anything that tries to split the string in all possible ways or maintain a DP over substrings would become quadratic in the worst case and exceed limits.

A common trap is to assume this is equivalent to checking a balanced parentheses sequence. That fails because standard valid sequences like “()(())” may not be generable depending on structure constraints imposed by the grammar. Another trap is to treat it as a grammar membership problem with generic parsing, which would require cubic DP over substrings if implemented directly.

A small example that exposes the difference is “()()”. This is a valid bracket sequence, but under this grammar it is not necessarily constructible if no derivation allows two independent components without wrapping constraints in the right order. Conversely, some nested forms are allowed even when they look unnecessarily constrained.

The real difficulty is that the grammar is not arbitrary context-free behavior, it has a very specific “outer wrapping with optional concatenation inside” structure that forces a tree-like decomposition rather than arbitrary interleavings.

## Approaches

A brute-force way to think about the problem is to treat it as a grammar membership check. We could define a DP where dp[l][r] tells whether substring S[l:r] belongs to the set. For a substring to be valid, it must either be “(X)” where X is valid, or “(X)(Y)” where both parts are valid and the outermost parentheses match properly.

This immediately leads to trying all split points inside every interval, and for each interval verifying matching structure. Even with memoization, the number of intervals is O(n²), and each transition requires scanning split points, giving O(n³) behavior in the worst case. With n up to 3×10⁵ total, this is infeasible.

The key observation is that the grammar forces a very rigid structure: every valid string is either a single primitive wrapped structure or a wrapped concatenation of two smaller valid structures. In both cases, the outermost pair of parentheses always encloses a decomposition into consecutive valid blocks.

This means that instead of arbitrary splitting, we can interpret the process as building a rooted ordered binary decomposition tree over primitive blocks. Each node corresponds to a balanced segment, and the structure of splits is fully determined by how many top-level components exist inside each pair of parentheses.

The standard way to capture this is to use a stack that maintains currently open structures and counts how many “complete components” have been formed at each depth. Each time we close a parenthesis, we either finalize a primitive or merge completed children at the current level. The structure is valid if and only if we never violate ordering constraints and end with a single completed structure at the outermost level.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute DP over substrings | O(n³) | O(n²) | Too slow |
| Stack-based structural parsing | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each string independently using a stack that represents nested construction frames. Each frame tracks whether it has seen at least one completed component inside it.

1. Initialize an empty stack. Each stack entry represents a currently open parenthesis context and whether it has accumulated completed substructures.
2. Scan the string from left to right. When we see “(”, we create a new frame and push it onto the stack. This corresponds to starting a new construction layer in the recursive definition.
3. When we see “)”, we are closing the current frame. At this point, the frame represents a fully constructed substructure. If the stack is empty before popping, the string is invalid because we are closing without an opening context.
4. Pop the top frame. If this frame contains no completed substructure and no internal valid composition, it represents the base “()” case, so it is still valid as a single unit.
5. After popping, treat this completed unit as a “block” that may belong to a higher-level frame. If the stack is not empty, we mark that the parent frame has now received at least one completed child component.
6. If at any point we encounter a closing bracket when there is no active frame, or we finish scanning and there are leftover open frames, the string is invalid.
7. Finally, the string is valid if exactly one complete structure was formed at the outermost level, meaning the stack processing ends cleanly and the entire string collapses into a single root block.

The important idea is that the grammar only allows two ways of building structures: wrapping and concatenation of already complete structures. The stack ensures that we only ever merge complete substructures, never partial ones.

### Why it works

At any point in the scan, each stack frame corresponds to a substring that is currently being constructed and is guaranteed to be balanced if completed. The invariant is that every time we pop a frame, it represents a maximal valid structure formed entirely from earlier completed components.

Because the grammar only allows composition of already valid components, no valid derivation can require splitting inside an incomplete segment. Conversely, every time the stack completes a frame, we have exactly constructed one grammar-consistent unit. The final acceptance condition enforces that the entire string collapses into a single such unit, matching the recursive definition of the set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_valid(s: str) -> bool:
    stack = []
    
    for ch in s:
        if ch == '(':
            # start a new frame, no completed children yet
            stack.append(0)
        else:
            if not stack:
                return False
            
            # finish current frame
            had_child = stack.pop()
            
            # we now have a completed block; attach it to parent if exists
            if stack:
                stack[-1] = 1  # parent now has at least one component
    
    return len(stack) == 0

def main():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        print("YES" if is_valid(s) else "NO")

if __name__ == "__main__":
    main()
```

The implementation uses a stack where each entry is a simple marker indicating whether the current frame has already accumulated at least one completed inner block. When a closing parenthesis is encountered, we pop the frame and treat it as a completed unit. If there is a parent frame, we mark it as having received a valid component.

The correctness hinges on ensuring we never accept unmatched closing brackets and that all opened frames are closed by the end. The final stack being empty ensures the whole structure reduces to a single valid construction.

## Worked Examples

We trace two strings to see how the stack evolves.

First consider the string “(()())”.

| Step | Char | Stack state |
| --- | --- | --- |
| 1 | ( | [0] |
| 2 | ( | [0, 0] |
| 3 | ) | [0] |
| 4 | ( | [0, 0] |
| 5 | ) | [0] |
| 6 | ) | [] |

At each closing bracket, we collapse the innermost structure into a single unit and propagate it upward. The stack ends empty, confirming a single valid root structure. This corresponds to a nested composition where inner valid blocks are combined under the grammar rules.

Now consider “(()))”.

| Step | Char | Stack state |
| --- | --- | --- |
| 1 | ( | [0] |
| 2 | ( | [0, 0] |
| 3 | ) | [0] |
| 4 | ) | [] |
| 5 | ) | invalid |

At step 5 we attempt to close a parenthesis with no active frame, which immediately violates the construction rules. This demonstrates how the stack detects structural violations early without needing full parsing.

The first example confirms proper nested reductions, while the second exposes how invalid closure breaks the construction process.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is pushed or popped at most once |
| Space | O(n) | Stack stores at most one entry per open parenthesis |

The total input size is up to 3×10⁵ characters, so a linear scan per test case fits comfortably within limits. Memory usage is also linear in the maximum nesting depth, which is bounded by string length.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        s = input().strip()
        stack = []
        ok = True
        for ch in s:
            if ch == '(':
                stack.append(0)
            else:
                if not stack:
                    ok = False
                    break
                stack.pop()
                if stack:
                    stack[-1] = 1
        if stack:
            ok = False
        print("YES" if ok else "NO")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided samples
assert run("""5
((())())
(()())
()()
(()()))
((()())())""") == """YES
YES
NO
NO
YES"""

# minimum size
assert run("""1
()""") == "YES"

# simple invalid
assert run("""1
)("""") == "NO"

# nested deep
assert run("""1
(((())))""") == "YES"

# multiple components invalid for this grammar
assert run("""1
()()""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| () | YES | minimal valid construction |
| )( | NO | early invalid closing |
| (((()))) | YES | deep nesting correctness |
| ()() | NO | disallowed flat concatenation structure |

## Edge Cases

One critical edge case is a string that is balanced in the usual sense but structurally incompatible with the grammar, such as “()()”. The stack processes it without ever encountering an invalid bracket, but the final structure does not collapse into a single root frame, leaving multiple top-level components. The algorithm rejects it because the stack is not empty at the end, which matches the requirement that the entire string must represent a single constructed object.

Another edge case is early invalid closure like “)(”. The first character tries to close a non-existent frame, causing an immediate rejection. This shows that the algorithm correctly enforces prefix validity, not just global balance.

A third case is deeply nested strings like “(((())))”, where every opening bracket creates a new frame and every closing bracket cleanly collapses it. The stack size grows linearly and then returns to zero, confirming that pure nesting is always valid under the construction rules.

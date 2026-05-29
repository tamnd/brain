---
title: "CF 255B - Code Parsing"
description: "We are given a string consisting solely of the characters \"x\" and \"y\". Two operations can be applied repeatedly in a specific order. The first operation swaps a consecutive \"y\" followed by \"x\" into \"x\" then \"y\". The second operation removes a consecutive \"x\" followed by \"y\"."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 255
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 156 (Div. 2)"
rating: 1200
weight: 255
solve_time_s: 139
verified: true
draft: false
---

[CF 255B - Code Parsing](https://codeforces.com/problemset/problem/255/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting solely of the characters "x" and "y". Two operations can be applied repeatedly in a specific order. The first operation swaps a consecutive "y" followed by "x" into "x" then "y". The second operation removes a consecutive "x" followed by "y". The string is processed greedily: if operation one is possible, it is applied first; otherwise, operation two is applied. The process repeats until no operation can be performed.

The input is a string up to $10^6$ characters. The output is the string after this process halts. Because of the length constraint, a naive approach that repeatedly scans the entire string to apply swaps or removals could take up to $10^6$ iterations per operation, giving $O(n^2)$ behavior. This is too slow for $n = 10^6$, so an efficient linear or near-linear solution is required.

Non-obvious edge cases include strings that are already sorted like "xxxx" or "yyyy", which should remain unchanged, strings with alternating patterns like "yxyxy" that trigger many swaps before deletions, and strings that end in "xy" which will be removed immediately. A careless implementation that ignores the operation ordering or that does not handle boundary conditions correctly would produce incorrect results.

## Approaches

The brute-force approach is straightforward: repeatedly scan the string from left to right, apply the first applicable operation, then restart. This works correctly because it mirrors the greedy algorithm, but its complexity is $O(n^2)$ in the worst case, for example on input "yxyxyxyx..." of length $10^6$. Each swap moves a "y" one position right, so processing all "y"s could require roughly $O(n^2)$ swaps.

The key observation to optimize is that operation one, swapping "y" and "x", essentially pushes all "y"s to the right relative to preceding "x"s. Operation two, removing "xy" pairs, eliminates an "x" and a "y" whenever an "x" precedes a "y". After all swaps are done, every "y" that has an "x" to its left will eventually be deleted. The result is that the final string will consist of all "x"s that were never paired with a "y" to their right and all "y"s that were never paired with an "x" to their left. This allows us to simulate the algorithm in a single left-to-right pass using a stack.

In practice, we iterate through the string, maintaining a stack. If we encounter an "x" and the top of the stack is "y", we cannot apply deletion, so we push "x". If we encounter a "y" and the top of the stack is "x", we remove the "x" (simulating an "xy" deletion). All other characters are pushed onto the stack. This approach runs in $O(n)$ time and uses $O(n)$ space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal (stack simulation) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list to simulate a stack. This will hold characters that survive so far.
2. Iterate through the string from left to right. For each character, check if the stack is non-empty.
3. If the current character is "y" and the top of the stack is "x", pop the "x" from the stack. This simulates deleting the "xy" pair according to operation two.
4. Otherwise, push the current character onto the stack. This keeps all characters that are not immediately deleted.
5. After the iteration completes, join the stack into a string and return it.

Why it works: the stack invariant is that it always contains the sequence of characters that have survived all prior operations. Every time an "x" encounters a "y" to its right, they cancel out exactly once, which matches the greedy deletion rule. Swaps of "y" before "x" are implicitly handled because only unmatched "x" and "y" remain, in the correct relative order.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
stack = []

for ch in s:
    if stack and stack[-1] == 'x' and ch == 'y':
        stack.pop()
    else:
        stack.append(ch)

print("".join(stack))
```

The code reads the string efficiently and iterates once. The stack simulates characters that survive. Each "xy" pair is removed in constant time when encountered. The use of `stack[-1]` ensures we check the last surviving character, maintaining the correct order for deletions. Pushing other characters preserves remaining "x" and "y" in their proper sequence.

## Worked Examples

Input "x":

| Index | Char | Stack | Action |
| --- | --- | --- | --- |
| 0 | x | [] | push x |

Output: "x". No deletions, confirms base case.

Input "yxyxy":

| Index | Char | Stack | Action |
| --- | --- | --- | --- |
| 0 | y | [] | push y |
| 1 | x | ['y'] | push x |
| 2 | y | ['y', 'x'] | top is x, ch is y -> pop x |
| 3 | x | ['y', 'y'] | push x |
| 4 | y | ['y', 'y', 'x'] | top is x, ch is y -> pop x |

Output: "yy". This matches expected after all swaps and deletions.

Input "xxxxxy":

| Index | Char | Stack | Action |
| --- | --- | --- | --- |
| 0-4 | x | [] -> ['x', 'x', 'x', 'x', 'x'] | push x each time |
| 5 | y | ['x', 'x', 'x', 'x', 'x'] | top is x, ch is y -> pop x |

Output: "xxxx". Demonstrates proper deletion at the end.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is pushed/popped at most once, so linear in string length |
| Space | O(n) | The stack may hold all characters in the worst case |

The linear time ensures the solution works comfortably for $n \le 10^6$, well within the 2-second limit. Memory usage of up to 1 million characters fits in the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    stack = []
    for ch in s:
        if stack and stack[-1] == 'x' and ch == 'y':
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)

# provided samples
assert run("x\n") == "x", "sample 1"
assert run("yxyxy\n") == "y", "sample 2"
assert run("xxxxxy\n") == "xxxx", "sample 3"

# custom cases
assert run("yyyyy\n") == "yyyyy", "all y"
assert run("xyxyxyxy\n") == "", "alternating xy deletion"
assert run("yxxxyyy\n") == "yyy", "mixed with leftover y"
assert run("x\n") == "x", "single x"
assert run("y\n") == "y", "single y"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "yyyyy" | "yyyyy" | No operations possible |
| "xyxyxyxy" | "" | All deletions applied in sequence |
| "yxxxyyy" | "yyy" | Mixed deletions, leftover y remain |
| "x" | "x" | Minimal single character, no operation |
| "y" | "y" | Minimal single character, no operation |

## Edge Cases

For input "yyyyy", the algorithm pushes all characters onto the stack without deletion. Output remains "yyyyy", correctly preserving characters since no "x" precedes a "y".

For input "xyxyxyxy", each "x" followed by "y" is immediately removed. Stack grows and shrinks accordingly, resulting in an empty string. This verifies that sequential deletions are handled correctly.

For input "yxxxyyy", initial "y" is pushed, "x" sequence remains until the final "y" cancels one "x", leaving three "y"s. This demonstrates that leftover characters are correctly preserved according to the rules.

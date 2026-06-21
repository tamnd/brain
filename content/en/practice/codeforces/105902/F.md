---
title: "CF 105902F - Imbalanced Bracket"
description: "We are given a string made of opening and closing brackets. We are allowed to change characters one by one, each change turning a bracket into the opposite type. After performing some number of such changes, we look at every possible non-empty subsequence of the resulting string."
date: "2026-06-21T12:16:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105902
codeforces_index: "F"
codeforces_contest_name: "2025 Fujian Normal University Programming Contest"
rating: 0
weight: 105902
solve_time_s: 49
verified: true
draft: false
---

[CF 105902F - Imbalanced Bracket](https://codeforces.com/problemset/problem/105902/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made of opening and closing brackets. We are allowed to change characters one by one, each change turning a bracket into the opposite type. After performing some number of such changes, we look at every possible non-empty subsequence of the resulting string. The requirement is that none of these subsequences should be “balanced”, where balanced means it can be interpreted as a valid parenthesis expression after inserting `+` and `1` appropriately, which is equivalent to the usual notion of a correct bracket sequence.

The task is to compute the minimum number of single-position changes needed so that every non-empty subsequence becomes invalid as a balanced bracket sequence.

The input size goes up to two hundred thousand characters in total across test cases, so any solution must run in linear time per test case. Anything quadratic, such as checking all subsequences or simulating transformations per subset, is immediately infeasible because the number of subsequences grows exponentially.

A subtle point is what it means for a subsequence to be balanced. The smallest balanced subsequence is `"()"`, and it only requires one `'('` and one `')'` with the `'('` appearing before the `')'` in the original string. This creates an important structural constraint: if both types of brackets exist in the final string, then a valid subsequence of length two is always possible.

Edge cases that often confuse naive reasoning come from this observation:

If the string is `"()"`, then it already contains a balanced subsequence, so zero operations is not acceptable since the full set of subsequences includes a valid one. The correct answer would require modifying at least one character.

If the string is `"((("`, there is no way to form a balanced subsequence at all, because there is no closing bracket. In this case, all subsequences are automatically imbalanced.

If the string is `")))"`, the same reasoning applies symmetrically.

These examples suggest that the only dangerous situation is when both types of brackets are present.

## Approaches

A brute-force strategy would try every possible way to modify the string, and for each candidate string, enumerate all subsequences and check whether any of them is balanced. Checking a single string already involves an exponential number of subsequences, and the number of possible modified strings is also exponential in the number of positions changed. Even with pruning, this approach collapses under the input limits.

The key simplification comes from recognizing that the existence of any `'('` and any `')'` immediately guarantees a valid subsequence `"()"`. This means the entire property “all non-empty subsequences are imbalanced” is equivalent to the much simpler condition that the final string must not contain both types of brackets simultaneously.

So the target configuration is extremely restricted: the final string must be either all `'('` or all `')'`. Any mixture automatically fails.

Once this is understood, the problem reduces to choosing which uniform string we want and counting how many positions must be flipped to achieve it. We try both possibilities and take the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsequences | O(2^n · n) | O(n) | Too slow |
| Make string uniform | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Count how many `'('` and `')'` appear in the string. This gives the full description of how far the string is from being uniform.
2. Compute the cost of converting the entire string into all `'('`. This cost is exactly the number of `')'` characters, since each must be flipped.
3. Compute the cost of converting the entire string into all `')'`. This cost is exactly the number of `'('` characters.
4. Return the minimum of these two values, since either target configuration guarantees that no subsequence can contain both types of brackets.

The reasoning behind choosing only uniform strings is that any mixed configuration inevitably contains at least one `"()"` subsequence, because any occurrence of `'('` to the left of a `')'` already forms a valid balanced subsequence.

### Why it works

A string fails the requirement as soon as it contains both bracket types, because the subsequence consisting of one `'('` and one later `')'` is already balanced. Therefore, eliminating all such subsequences is equivalent to ensuring that one of the bracket types is completely absent. Any uniform string satisfies this condition, and any non-uniform string violates it.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input().strip())
    s = input().strip()

    open_cnt = s.count('(')
    close_cnt = n - open_cnt

    # make all '(' or all ')'
    print(min(open_cnt, close_cnt))
```

The solution relies only on counting character frequencies. The key implementation detail is avoiding any attempt to simulate subsequences or transformations. The answer is fully determined by global counts, so a single linear scan (or even Python’s built-in `count`) is sufficient.

The only subtlety is ensuring that both conversion directions are considered. Choosing only one direction can be wrong in cases where the majority character differs.

## Worked Examples

### Example 1: `()))`

We compute counts first.

| Step | '(' count | ')' count | Action |
| --- | --- | --- | --- |
| Initial | 1 | 3 | Evaluate both conversion targets |
| To all '(' | 1 | 3 | Cost = 3 |
| To all ')' | 1 | 3 | Cost = 1 |
| Result | - | - | 1 |

This shows that flipping the single `'('` is optimal, producing a uniform string of `')'`.

### Example 2: `)()()((`

| Step | '(' count | ')' count | Action |
| --- | --- | --- | --- |
| Initial | 4 | 3 | Evaluate both targets |
| To all '(' | 4 | 3 | Cost = 3 |
| To all ')' | 4 | 3 | Cost = 4 |
| Result | - | - | 3 |

The optimal strategy is to convert all `')'` into `'('`, resulting in a fully uniform string.

These traces confirm that only global frequency matters, not structure or ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each string is scanned once to count brackets |
| Space | O(1) | Only two counters are used |

The total input size across all test cases is bounded by 2 × 10^5, so a linear solution comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()
        open_cnt = s.count('(')
        close_cnt = n - open_cnt
        out.append(str(min(open_cnt, close_cnt)))
    return "\n".join(out)

# provided samples
assert run("2\n3\n())\n7\n)()()((\n") == "1\n3"

# all same characters
assert run("2\n3\n(((\n3\n)))\n") == "0\n0"

# single imbalance mix
assert run("1\n2\n()\n") == "1"

# already uniform
assert run("1\n5\n(((((\n") == "0"

# alternating structure
assert run("1\n6\n()()()\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `(((` | 0 | already safe uniform case |
| `)))` | 0 | symmetric case |
| `()` | 1 | minimal mixed case |
| `()()()` | 3 | alternating worst-case flips |

## Edge Cases

A critical edge case is when the string alternates between brackets, such as `"()()()"`. Although it might look structurally complex, it still contains both `'('` and `')'`, so a subsequence `"()"` always exists. The algorithm counts both types and correctly returns the number of flips needed to eliminate one type entirely.

Another edge case is when the string is already uniform, for example `"(((("`. Here, the counts show zero closing brackets, so the answer is zero. The algorithm naturally handles this without special branching.

Finally, the smallest non-trivial input `"()"` highlights why structure does not matter: even though it is a valid full sequence, it is immediately disqualified because it contains a balanced subsequence of length two. The computation still reduces to one flip, matching the uniformization logic.

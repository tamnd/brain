---
title: "CF 190C - STL"
description: "We are given a sequence of words that originally described a type in a fictional language. The language has only two valid constructions. The simplest type is int. The second type is pair<type,type, where each side is itself another valid type."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar"]
categories: ["algorithms"]
codeforces_contest: 190
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 120 (Div. 2)"
rating: 1500
weight: 190
solve_time_s: 109
verified: true
draft: false
---

[CF 190C - STL](https://codeforces.com/problemset/problem/190/C)

**Rating:** 1500  
**Tags:** dfs and similar  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of words that originally described a type in a fictional language. The language has only two valid constructions.

The simplest type is `int`.

The second type is `pair<type,type>`, where each side is itself another valid type.

The punctuation was removed before the words were written down, so the input only contains tokens `"pair"` and `"int"`. Our task is to reconstruct the unique valid type expression, or determine that no valid reconstruction exists.

For example, the sequence:

```
pair pair int int int
```

can become:

```
pair<pair<int,int>,int>
```

because the outer `pair` needs two types. Its first child is another `pair<int,int>`, and its second child is `int`.

The important structural observation is that every `"pair"` token creates a node that requires exactly two child types, while every `"int"` token immediately completes one type. This turns the problem into parsing a recursive grammar.

The constraints are large enough that the solution must run in linear time. The total number of tokens is at most `10^5`, so anything quadratic is unsafe. Recursive backtracking over all possible parenthesizations would explode combinatorially. Even repeatedly concatenating long Python strings carelessly can become too slow. A proper parser that processes each token once is required.

Several edge cases are easy to mishandle.

One dangerous case is when the expression ends before all required types are filled.

Input:

```
2
pair int
```

The token `pair` requires two child types, but only one `int` exists. The correct output is:

```
Error occurred
```

A careless parser might stop after building the first child and incorrectly accept the result.

Another subtle case is when extra tokens remain after a valid type has already been completed.

Input:

```
1
int int
```

The first `int` already forms a complete type. The second token cannot belong anywhere, so the answer is invalid. The correct output is:

```
Error occurred
```

A parser that only checks whether some valid prefix exists would incorrectly accept this.

Deep nesting is another implementation hazard.

Input:

```
4
pair pair pair int int int int
```

produces:

```
pair<pair<pair<int,int>,int>,int>
```

The nesting depth can reach `10^5`, so recursive DFS in Python risks hitting recursion limits. An iterative approach is safer unless recursion depth is explicitly increased.

## Approaches

The brute-force idea is to try every possible way to insert angle brackets and commas, then test whether the resulting expression matches the grammar.

This works conceptually because the grammar is unambiguous. If a valid reconstruction exists, exactly one parse tree exists. The problem is that the number of possible binary tree structures grows exponentially. Even for a moderate number of `pair` tokens, the search space becomes enormous. With up to `10^5` tokens, exhaustive generation is completely impossible.

A more disciplined recursive parser improves the situation. Since the grammar is:

```
type := int | pair<type,type>
```

we can process tokens from left to right.

If the current token is `int`, we immediately return `"int"`.

If the token is `pair`, we recursively parse the left child, then the right child, and finally wrap them as:

```
pair<left,right>
```

This already reduces the complexity to linear time because every token is consumed once.

The key observation is that the token stream itself already uniquely determines the parse order. A `"pair"` always consumes exactly two complete types after it. There is no ambiguity, so we never need backtracking.

The remaining issue is implementation safety. A deeply nested structure may create recursion depth near `10^5`, which exceeds Python's default recursion limit. We can either increase the recursion limit or write the parser iteratively. Competitive programming solutions for this problem usually keep the recursive structure and raise the recursion limit because the parsing logic maps naturally onto the grammar.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Recursive Parsing | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all tokens into an array.
2. Maintain a pointer `idx` representing the next unread token.
3. Define a recursive function `parse()` that tries to build one complete type starting from `tokens[idx]`.
4. If `idx` already reached the end of the array, parsing failed because some parent type expected more children.
5. If the current token is `"int"`, increment `idx` and return the string `"int"`.
6. If the current token is `"pair"`, increment `idx` and recursively parse two child types.

The grammar requires exactly two children, so we must successfully construct both.
7. If either recursive call fails, propagate failure upward.
8. Otherwise, combine the two child strings as:

```
pair<left,right>
```
9. After building the root type, verify that every token was consumed.

If unread tokens remain, the expression is invalid because extra words exist outside the parsed type.
10. If parsing failed at any point or unused tokens remain, print:

```
Error occurred
```

Otherwise print the constructed type.

### Why it works

The grammar is deterministic. Every `"int"` corresponds to one complete leaf type, and every `"pair"` corresponds to an internal node with exactly two children.

The parser always consumes tokens in preorder traversal order. When it encounters `"pair"`, the next tokens must form the left subtree followed immediately by the right subtree. Since the grammar has no ambiguity, there is exactly one possible parse tree.

The algorithm succeeds exactly when the token sequence forms a complete valid tree and no extra tokens remain. If some subtree cannot be completed, recursion reaches the end of the token list and fails. If additional tokens remain afterward, the input contains multiple disconnected types instead of one valid type expression.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

n = int(input())
tokens = input().split()

idx = 0

def parse():
    global idx

    if idx >= len(tokens):
        return None

    token = tokens[idx]
    idx += 1

    if token == "int":
        return "int"

    left = parse()
    if left is None:
        return None

    right = parse()
    if right is None:
        return None

    return f"pair<{left},{right}>"

result = parse()

if result is None or idx != len(tokens):
    print("Error occurred")
else:
    print(result)
```

The parser directly mirrors the grammar definition.

The global pointer `idx` tracks how many tokens have already been consumed. Every successful parse advances this pointer exactly over the tokens belonging to that subtree.

The base case handles `"int"`. Since `int` is already a complete type, the function simply returns the string `"int"`.

The `"pair"` case is more interesting. After consuming the `"pair"` token itself, the parser must recursively build two complete child types. If either child cannot be constructed, the whole parse fails immediately.

The final validation step is critical. Even if a valid type was built, extra tokens invalidate the input. This catches cases like:

```
int int
```

where the first token alone forms a valid type but additional unused tokens remain.

The recursion limit is increased because the nesting depth may reach `10^5`. Without this adjustment, Python would raise a recursion error on deeply nested valid inputs.

## Worked Examples

### Example 1

Input:

```
3
pair pair int int int
```

| Step | idx | Current Token | Action | Partial Result |
| --- | --- | --- | --- | --- |
| 1 | 0 | pair | Parse left child | pending |
| 2 | 1 | pair | Parse left child | pending |
| 3 | 2 | int | Return int | int |
| 4 | 3 | int | Return int | int |
| 5 | 4 | combine | Build pair<int,int> | pair<int,int> |
| 6 | 4 | int | Return int | int |
| 7 | 5 | combine | Build outer pair | pair<pair<int,int>,int> |

The inner `pair` consumes two `int` tokens and becomes a complete subtree. The outer `pair` then uses that subtree as its left child and the final `int` as its right child.

### Example 2

Input:

```
2
pair int
```

| Step | idx | Current Token | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | 0 | pair | Parse left child | pending |
| 2 | 1 | int | Return int | int |
| 3 | 2 | end | Missing right child | failure |

The parser successfully builds the left child of the `pair`, but no tokens remain for the required right child. The parse fails correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each token is processed exactly once |
| Space | O(n) | Recursive call stack and output string storage |

The solution comfortably fits the constraints. Processing `10^5` tokens linearly is fast enough for a 2-second limit, and the memory usage remains proportional to the input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    sys.setrecursionlimit(1 << 25)

    n = int(input())
    tokens = input().split()

    idx = 0

    def parse():
        nonlocal idx

        if idx >= len(tokens):
            return None

        token = tokens[idx]
        idx += 1

        if token == "int":
            return "int"

        left = parse()
        if left is None:
            return None

        right = parse()
        if right is None:
            return None

        return f"pair<{left},{right}>"

    result = parse()

    if result is None or idx != len(tokens):
        print("Error occurred")
    else:
        print(result)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
"""3
pair pair int int int
"""
) == "pair<pair<int,int>,int>", "sample 1"

# minimum valid input
assert run(
"""1
int
"""
) == "int", "single int"

# missing child
assert run(
"""2
pair int
"""
) == "Error occurred", "incomplete pair"

# extra unused token
assert run(
"""1
int int
"""
) == "Error occurred", "unused token"

# deep left nesting
assert run(
"""4
pair pair pair int int int int
"""
) == "pair<pair<pair<int,int>,int>,int>", "nested pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / int` | `int` | Smallest valid expression |
| `2 / pair int` | `Error occurred` | Missing subtree detection |
| `1 / int int` | `Error occurred` | Extra token validation |
| Nested pairs input | Nested pair output | Correct recursive structure |

## Edge Cases

A common failure case is incomplete construction.

Input:

```
2
pair int
```

The parser reads `pair` and knows two child types are required. It successfully parses the first `int`, but then reaches the end of the token array while searching for the second child. The recursive call returns failure, which propagates upward, producing:

```
Error occurred
```

Another subtle case is leftover tokens.

Input:

```
1
int int
```

The parser constructs a complete type immediately from the first token. After parsing finishes, `idx` equals `1` while the token array length is `2`. Since unused tokens remain, the algorithm rejects the input.

Deep nesting also matters.

Input:

```
4
pair pair pair int int int int
```

The parser repeatedly descends into the left child until reaching the first `int`. It then unwinds layer by layer, constructing:

```
pair<int,int>
pair<pair<int,int>,int>
pair<pair<pair<int,int>,int>,int>
```

The increased recursion limit prevents stack overflow on large nested inputs.

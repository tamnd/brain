---
title: "CF 223A - Bracket Sequence"
description: "We are given a string consisting only of four bracket characters: (, ), [ and ]. The string itself is not guaranteed to be balanced. Our task is to find a contiguous substring that forms a valid bracket sequence."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "expression-parsing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 223
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 138 (Div. 1)"
rating: 1700
weight: 223
solve_time_s: 101
verified: true
draft: false
---

[CF 223A - Bracket Sequence](https://codeforces.com/problemset/problem/223/A)

**Rating:** 1700  
**Tags:** data structures, expression parsing, implementation  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting only of four bracket characters: `(`, `)`, `[` and `]`. The string itself is not guaranteed to be balanced.

Our task is to find a contiguous substring that forms a valid bracket sequence. Among all valid substrings, we want the one containing the largest number of opening square brackets `'['`. After finding such a substring, we print the number of `'['` characters inside it and the substring itself.

A valid bracket sequence follows the usual stack rules. Every opening bracket must be closed later by the matching type, and nesting order must remain correct. For example, `([])` is valid, but `([)]` is not because the closing order breaks nesting.

The length of the string can reach `10^5`, which immediately rules out anything quadratic or cubic. Checking every substring would require about `n^2` candidates, and validating each candidate with a stack would add another factor of `n`, producing `O(n^3)` time in the worst case. Even with optimizations, `O(n^2)` is still too large for `10^5`. We need something close to linear time.

Several edge cases are easy to mishandle.

Consider the input:

```
([)]
```

The whole string is not valid, even though the total number of opening and closing brackets matches. A careless implementation that only counts bracket frequencies would incorrectly accept it.

The correct answer is:

```
1
[]
```

Another tricky case is:

```
]]]][[[[
```

There is no valid non-empty substring at all. The correct output is:

```
0
```

The second line is empty. Some implementations accidentally print garbage values or crash because they assume at least one valid segment exists.

Nested structures also matter. For example:

```
([][])
```

The entire string is valid and contains two `'['` characters. A greedy approach that only tracks locally matched pairs could incorrectly return just `[]`.

Finally, mismatched closing brackets must fully invalidate the current nesting chain. In:

```
([)]
```

when we encounter `)`, it does not match `[`. Every currently open bracket before that point becomes unusable for substrings crossing this position.

## Approaches

The brute-force idea is straightforward. Enumerate every substring `s[l...r]`, check whether it is a correct bracket sequence using a stack, and count how many `'['` characters it contains. If the substring is valid and improves the answer, store it.

The validity check itself takes linear time in the substring length. Since there are `O(n^2)` substrings, the total complexity becomes `O(n^3)`. Even if we precompute prefix sums for square bracket counts, validation still dominates with `O(n^3)` time. For `n = 10^5`, this is completely infeasible.

The key observation is that we do not actually need to validate every substring independently. While scanning the string once, we can determine which brackets successfully match using a stack, exactly like the classic longest valid parentheses problem.

Suppose position `i` contains a closing bracket. If the top of the stack contains the corresponding opening bracket type, then these two positions form a matched pair. Otherwise, the nesting breaks.

Once all matched pairs are known, another important property appears. Any maximal continuous region where every bracket belongs to some correct matching behaves like a valid bracket structure. This lets us identify valid substrings in linear time.

We still need to maximize the number of `'['` characters. Prefix sums solve that part efficiently. If `pref[i]` stores how many `'['` characters appear in the prefix ending before index `i`, then the number inside substring `[l, r]` is:

$$pref[r+1] - pref[l]$$

So the problem reduces to:

1. Find all matched bracket positions with a stack.
2. Identify continuous valid regions.
3. Use prefix sums to count square brackets inside each region.
4. Keep the best one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a stack that stores indices of opening brackets.

We need indices instead of characters because later we must mark exact positions as matched.
2. Scan the string from left to right.

If the current character is `(` or `[`, push its index onto the stack.
3. When encountering a closing bracket, check the stack top.

If the stack is empty, this closing bracket cannot match anything.

Otherwise, compare the bracket types:

`(` matches `)`

`[` matches `]`
4. If the top opening bracket matches the current closing bracket, mark both positions as valid.

We maintain a boolean array `good[]` where `good[i] = True` means character `i` belongs to some matched pair.

Then pop the opening bracket index from the stack.
5. If the types do not match, clear the stack.

This step is crucial. A mismatch destroys every unfinished structure before it. Any substring crossing this mismatch cannot be valid.
6. Build a prefix sum array counting occurrences of `'['`.

`pref[i+1] = pref[i] + (s[i] == '[')`
7. Scan the `good[]` array to find maximal continuous valid segments.

Whenever we see consecutive `True` values from `l` to `r`, the substring `s[l:r+1]` is a valid bracket sequence.
8. Compute how many `'['` characters this segment contains using prefix sums.

If this count exceeds the current best, store the segment boundaries.
9. Print the maximum count and the corresponding substring.

### Why it works

The stack guarantees that we only match brackets respecting proper nesting order. Whenever a mismatch occurs, no valid substring can pass through that position while preserving earlier unmatched openings, so clearing the stack is correct.

Every position marked `good = True` belongs to some correctly matched pair. Continuous runs of such positions correspond exactly to valid bracket substrings because nesting consistency was enforced during matching.

The prefix sums correctly count square brackets inside any chosen segment in constant time, so selecting the segment with the maximum number of `'['` characters is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    good = [False] * n
    stack = []

    match = {
        ')': '(',
        ']': '['
    }

    for i, ch in enumerate(s):
        if ch in '([':
            stack.append(i)
        else:
            if stack and s[stack[-1]] == match[ch]:
                j = stack.pop()
                good[i] = True
                good[j] = True
            else:
                stack.clear()

    pref = [0] * (n + 1)

    for i in range(n):
        pref[i + 1] = pref[i] + (1 if s[i] == '[' else 0)

    best_count = 0
    best_l = 0
    best_r = -1

    i = 0

    while i < n:
        if not good[i]:
            i += 1
            continue

        j = i

        while j < n and good[j]:
            j += 1

        cnt = pref[j] - pref[i]

        if cnt > best_count:
            best_count = cnt
            best_l = i
            best_r = j - 1

        i = j

    print(best_count)

    if best_r >= best_l:
        print(s[best_l:best_r + 1])
    else:
        print()

if __name__ == "__main__":
    solve()
```

The first part of the solution performs bracket matching with a stack. Each opening bracket index is pushed. When a closing bracket appears, we verify whether it matches the most recent unmatched opening bracket. If yes, both positions become part of a valid structure.

The `good[]` array is the core representation. Instead of explicitly building valid substrings during matching, we simply remember which positions participate in valid pairs. This keeps the implementation simple and linear.

The stack reset after a mismatch is subtle but necessary. Suppose we process:

```
([)]
```

After reading `(` and `[`, the stack contains both indices. Encountering `)` does not match `[`. Any valid substring crossing this point is impossible, so the earlier `(` cannot remain usable. Clearing the stack enforces this.

The prefix sum array lets us count square brackets in constant time for every candidate segment. Without it, counting would require rescanning substrings and increase complexity.

The final scan groups consecutive `good` positions into maximal valid regions. Since every position in such a region belongs to properly nested matched pairs, the whole segment forms a correct bracket sequence.

The boundary handling deserves attention. If no valid substring exists, `best_r` stays `-1`, and we print an empty second line.

## Worked Examples

### Example 1

Input:

```
([])
```

### Matching phase

| Index | Character | Stack After Step | good[] Updated |
| --- | --- | --- | --- |
| 0 | ( | [0] | No |
| 1 | [ | [0,1] | No |
| 2 | ] | [0] | good[1], good[2] |
| 3 | ) | [] | good[0], good[3] |

Final `good[]`:

```
[T, T, T, T]
```

### Segment scan

| Segment | Substring | Number of `[` |
| --- | --- | --- |
| [0,3] | ([]) | 1 |

Best answer:

```
1
([])
```

This trace shows that nested matching works naturally. The inner `[]` pair closes first, then the outer `()` pair.

### Example 2

Input:

```
([)]
```

### Matching phase

| Index | Character | Stack After Step | Action |
| --- | --- | --- | --- |
| 0 | ( | [0] | Push |
| 1 | [ | [0,1] | Push |
| 2 | ) | [] | Mismatch, clear stack |
| 3 | ] | [] | No match |

Final `good[]`:

```
[F, F, F, F]
```

### Segment scan

No valid segment exists.

Output:

```
0
```

This example demonstrates why type checking matters. Even though counts balance globally, the nesting order is invalid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is pushed and popped from the stack at most once |
| Space | O(n) | Stack, prefix sums, and validity array all use linear memory |

With `n ≤ 10^5`, linear complexity easily fits within the limits. The algorithm performs only a few passes over the string and uses simple array operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    s = input().strip()
    n = len(s)

    good = [False] * n
    stack = []

    match = {
        ')': '(',
        ']': '['
    }

    for i, ch in enumerate(s):
        if ch in '([':
            stack.append(i)
        else:
            if stack and s[stack[-1]] == match[ch]:
                j = stack.pop()
                good[i] = True
                good[j] = True
            else:
                stack.clear()

    pref = [0] * (n + 1)

    for i in range(n):
        pref[i + 1] = pref[i] + (1 if s[i] == '[' else 0)

    best_count = 0
    best_l = 0
    best_r = -1

    i = 0

    while i < n:
        if not good[i]:
            i += 1
            continue

        j = i

        while j < n and good[j]:
            j += 1

        cnt = pref[j] - pref[i]

        if cnt > best_count:
            best_count = cnt
            best_l = i
            best_r = j - 1

        i = j

    out = [str(best_count)]

    if best_r >= best_l:
        out.append(s[best_l:best_r + 1])
    else:
        out.append("")

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run("([])\n") == "1\n([])\n", "sample 1"

# no valid substring
assert run("]]]][[[[\n") == "0\n\n", "no valid substring"

# mismatched nesting
assert run("([)]\n") == "0\n\n", "crossed brackets"

# multiple valid regions
assert run("[](()[])[]\n") == "3\n[](()[])[]\n", "whole string valid"

# minimum size
assert run("[\n") == "0\n\n", "single bracket"

# nested valid structure
assert run("(([[[]]]))\n") == "3\n(([[[]]]))\n", "deep nesting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `]]]][[[[` | `0` and empty line | No valid substring exists |
| `([)]` | `0` and empty line | Incorrect nesting must fail |
| `[](()[])[]` | Whole string returned | Multiple nested structures |
| `[` | `0` and empty line | Minimum-size edge case |
| `(([[[]]]))` | Entire string with count 3 | Deep nested matching |

## Edge Cases

Consider the input:

```
([)]
```

The algorithm pushes `(` and `[` onto the stack. When `)` appears, the top of the stack is `[`, which does not match. The stack is cleared immediately.

That prevents the earlier `(` from incorrectly matching future brackets across the mismatch. The final `good[]` array contains no valid positions, so the algorithm outputs:

```
0
```

Now consider:

```
]]]][[[[
```

Every character is either an unmatched closing bracket or an opening bracket that never closes. No positions become marked as valid.

During the final scan, no valid segment exists, so the stored answer remains empty. The output becomes:

```
0
```

Finally, examine:

```
([][])
```

The stack operations correctly preserve nesting:

1. `(` pushed
2. `[` pushed
3. `]` matches `[`
4. `[` pushed
5. `]` matches `[`
6. `)` matches `(`

All positions become marked valid. Since the entire string forms one continuous valid region, the algorithm counts two `'['` characters and returns the whole substring.

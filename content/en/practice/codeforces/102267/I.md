---
title: "CF 102267I - Ultimate Army"
description: "The input describes a rooted tree of soldiers, encoded without explicit edges. Every soldier appears as an integer ID, and immediately after that ID comes zero or more parenthesized descriptions of its direct subordinates."
date: "2026-08-17T19:27:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102267
codeforces_index: "I"
codeforces_contest_name: "The 2019 University of Jordan Collegiate Programming Contest"
rating: 0
weight: 102267
solve_time_s: 206
verified: false
draft: false
---

[CF 102267I - Ultimate Army](https://codeforces.com/problemset/problem/102267/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 26s  
**Verified:** no  

## Solution
## Problem Understanding

The input describes a rooted tree of soldiers, encoded without explicit edges. Every soldier appears as an integer ID, and immediately after that ID comes zero or more parenthesized descriptions of its direct subordinates. A pair of parentheses contains exactly one complete subtree. For example, `2(3(4))(1)` describes a tree whose root is soldier 2, with children 3 and 1, while 3 has child 4.

The task is to recover the parent of every soldier. For each ID from 1 through `n`, we output the ID of its direct supervisor. The unique soldier at the root has parent 0.

The first constraint gives at most 140,000 soldiers, while the encoded string can contain up to one million characters. This means an algorithm proportional to the number of soldiers or characters is easily suitable, but repeatedly scanning a large part of the string for every soldier is too expensive. With a one second time limit, we should aim for linear time, or at worst something close to it. A quadratic algorithm over a million-character string could require around `10^12` character operations, which is far beyond the limit.

The first edge case is a single soldier. The input

```
1
1
```

has no parentheses at all, and the correct output is

```
0
```

A parser that assumes every soldier has at least one child would fail here.

Another edge case is a chain, where every soldier has exactly one child:

```
4
1(2(3(4)))
```

The correct output is

```
0 1 2 3
```

A careless implementation that treats the most recently parsed soldier as a sibling after encountering `)` can lose the ancestor relationship. After soldier 4 finishes, the parser must return to soldier 3, then to soldier 2, then to soldier 1.

A third case is several siblings:

```
4
1(2)(3)(4)
```

The answer is

```
0 1 1 1
```

The closing parenthesis of soldier 2 must restore soldier 1 as the current supervisor before soldier 3 is parsed. An implementation that forgets to remove a finished soldier from its active path could incorrectly make 2 the parent of 3.

Finally, IDs may have multiple digits, so parsing one character at a time as a separate ID is incorrect. For example,

```
3
10(2)(30)
```

would describe IDs 10, 2, and 30 if such IDs were allowed by the chosen `n`; the parser must consume the complete sequence of digits before processing the soldier. Under the actual constraint that IDs are exactly 1 through `n`, the same issue appears whenever `n >= 10`.

## Approaches

A straightforward approach is to process each soldier independently. After finding the position where an ID occurs, we could scan backward through the string and determine which soldier's parentheses contain that position. Parentheses give enough information to recover the enclosing subtree, so this approach is correct.

The problem is that the same characters are scanned over and over. Consider a deeply nested tree such as `1(2(3(4(...)))`. For a soldier near the bottom, a backward search can traverse almost the entire prefix of the string. If there are `n` soldiers and the string has length `L`, the worst-case work is `O(nL)`. With `n = 140000` and `L` close to `10^6`, this can reach roughly `1.4 × 10^11` character inspections. Even though the exact maximum of both quantities cannot occur independently in every shape, this bound is already far too large.

The structure of the encoding gives us a much better observation. At any point while reading the string from left to right, there is a unique path from the root to the soldier currently being described. That path consists exactly of the soldiers whose opening `(` has been encountered but whose corresponding `)` has not yet been encountered.

This active path can be maintained with a stack. When a new soldier ID is read, the top of the stack is its supervisor. We then push the new soldier because all of its children, if any, belong below it. When `)` is encountered, the current soldier's entire description has ended, so we pop it. Every character is processed once, and every soldier is pushed and popped once.

The brute-force method works because parentheses implicitly tell us which soldier contains another soldier, but it repeatedly reconstructs that relationship from scratch. The observation that the active ancestors are exactly a stack reduces the problem to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nL)` in the worst case | `O(n)` | Too slow |
| Stack Parsing | `O(L)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read `n` and the encoded string. Allocate an answer array of length `n + 1`, where `parent[x]` will eventually contain the supervisor of soldier `x`.
2. Initialize an empty stack. The stack represents the current path from the root to the soldier whose description is being processed. Its top is always the currently active soldier.
3. Scan the string from left to right. When a digit is found, continue consuming digits until the complete integer ID has been read. This is necessary because an ID such as `123` is one soldier, not three separate soldiers.
4. Once the complete ID `x` has been parsed, inspect the stack. If it is nonempty, its top is the direct supervisor of `x`, so set `parent[x]` to that value. If the stack is empty, `x` is the root and its parent remains 0.
5. Push `x` onto the stack. From this point until the corresponding closing parenthesis, `x` is the active supervisor for every direct child encountered inside its subtree.
6. When the scan encounters `(`, simply advance past it. The opening parenthesis does not introduce a new soldier, so there is no stack operation to perform.
7. When the scan encounters `)`, pop the top soldier. Its complete subtree has just ended, so it can no longer be the active supervisor. The new stack top is its parent.
8. After the complete string has been scanned, output `parent[1]` through `parent[n]`. Every soldier has been encountered exactly once, so every parent relationship has already been determined.

### Why it works

The key invariant is that immediately before reading a soldier ID, the stack contains exactly the ancestors of that soldier, in root-to-parent order. The opening of a soldier's description causes that soldier to be pushed, so its children see it at the top of the stack. When its closing parenthesis is reached, its whole subtree is finished and popping it restores its own parent as the top element. Thus, whenever an ID is parsed, the stack top is exactly its direct supervisor. The root is the only ID parsed with an empty stack, so it correctly receives parent 0.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data):
    lines = data.splitlines()
    n = int(lines[0])
    s = lines[1].strip()

    parent = [0] * (n + 1)
    stack = []

    i = 0
    length = len(s)

    while i < length:
        c = s[i]

        if '0' <= c <= '9':
            x = 0

            while i < length:
                c = s[i]
                if c < '0' or c > '9':
                    break
                x = x * 10 + (ord(c) - 48)
                i += 1

            if stack:
                parent[x] = stack[-1]

            stack.append(x)
        elif c == ')':
            stack.pop()
            i += 1
        else:
            # '('
            i += 1

    return ' '.join(map(str, parent[1:]))

def main():
    data = sys.stdin.read()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The parser uses an index `i` instead of splitting the string. This avoids creating a large collection of temporary substrings and lets us process the input directly.

When `s[i]` is a digit, the inner loop builds the complete ID numerically. After it finishes, `i` already points at the first non-digit character, so there is no extra increment at the end of the digit branch. This detail prevents skipping a following parenthesis.

The stack stores integer IDs rather than string positions. This makes the parent lookup immediate, because `stack[-1]` is exactly the supervisor we need.

For an ID read when the stack is empty, no assignment is necessary because the answer array was initialized with zeros. There is exactly one such soldier because the input represents one rooted tree.

When `)` is processed, the stack cannot be empty for a valid input. The pop operation removes the soldier whose description has just ended. An opening `(` needs no stack operation because the soldier being opened is pushed when its ID is read.

Python integers do not have an overflow issue here. The largest ID is only 140,000, and the string itself contains at most one million characters.

The implementation uses `sys.stdin.read()` inside `solve` rather than repeatedly calling `input()`. This is convenient for the million-character input and also makes the solver easy to test. The required `input = sys.stdin.readline` is defined as standard competitive-programming fast I/O, although the main solver reads the entire input at once.

## Worked Examples

For Sample 1, the encoded tree is `2(3(4))(1)`. The following trace records the meaningful parser actions. Parentheses are shown explicitly because they are responsible for stack changes.

| Position / token | Action | Stack after action | Parent assignment |
| --- | --- | --- | --- |
| `2` | Read soldier 2, no active parent | `[2]` | `parent[2] = 0` |
| `(` | Enter child description | `[2]` | unchanged |
| `3` | Read soldier 3 | `[2, 3]` | `parent[3] = 2` |
| `(` | Enter child description | `[2, 3]` | unchanged |
| `4` | Read soldier 4 | `[2, 3, 4]` | `parent[4] = 3` |
| `)` | Finish soldier 4 | `[2, 3]` | unchanged |
| `)` | Finish soldier 3 | `[2]` | unchanged |
| `(` | Enter next child | `[2]` | unchanged |
| `1` | Read soldier 1 | `[2, 1]` | `parent[1] = 2` |
| `)` | Finish soldier 1 | `[2]` | unchanged |

The final parent array is `2 0 2 3`. The trace shows why siblings work correctly: after soldier 3's closing parenthesis, soldier 2 becomes active again before soldier 1 is parsed.

For Sample 2, the string is `4(2)(5(3(6)(1))(7))`.

| Token | Action | Stack after action | Parent assignment |
| --- | --- | --- | --- |
| `4` | Read soldier 4 | `[4]` | `parent[4] = 0` |
| `(` | Enter child description | `[4]` | unchanged |
| `2` | Read soldier 2 | `[4, 2]` | `parent[2] = 4` |
| `)` | Finish soldier 2 | `[4]` | unchanged |
| `(` | Enter next child | `[4]` | unchanged |
| `5` | Read soldier 5 | `[4, 5]` | `parent[5] = 4` |
| `(` | Enter child description | `[4, 5]` | unchanged |
| `3` | Read soldier 3 | `[4, 5, 3]` | `parent[3] = 5` |
| `(` | Enter child description | `[4, 5, 3]` | unchanged |
| `6` | Read soldier 6 | `[4, 5, 3, 6]` | `parent[6] = 3` |
| `)` | Finish soldier 6 | `[4, 5, 3]` | unchanged |
| `(` | Enter next child | `[4, 5, 3]` | unchanged |
| `1` | Read soldier 1 | `[4, 5, 3, 1]` | `parent[1] = 3` |
| `)` | Finish soldier 1 | `[4, 5, 3]` | unchanged |
| `)` | Finish soldier 3 | `[4, 5]` | unchanged |
| `(` | Enter next child | `[4, 5]` | unchanged |
| `7` | Read soldier 7 | `[4, 5, 7]` | `parent[7] = 5` |
| `)` | Finish soldier 7 | `[4, 5]` | unchanged |
| `)` | Finish soldier 5 | `[4]` | unchanged |
| `)` | Finish soldier 4 | `[]` | unchanged |

The resulting output is `3 4 5 0 4 3 5`. This example exercises both nesting and multiple siblings. In particular, soldier 7 becomes a child of 5 rather than 3 because the closing parenthesis after soldier 3 removes 3 from the active path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(L)` | Every character is inspected once, and every ID is pushed exactly once. |
| Space | `O(n)` | The answer array and the stack each contain at most `n` integers. |

Here `L` is the length of the encoded string, with `L <= 10^6`, and `n <= 1.4 × 10^5`. A million-character linear scan is appropriate for the one second limit, while the stack can contain at most all soldiers in a single chain, which is well within the 256 MB memory limit.

## Test Cases

```python
import sys
import io

def solve(data):
    lines = data.splitlines()
    n = int(lines[0])
    s = lines[1].strip()

    parent = [0] * (n + 1)
    stack = []

    i = 0
    length = len(s)

    while i < length:
        c = s[i]

        if '0' <= c <= '9':
            x = 0

            while i < length:
                c = s[i]
                if c < '0' or c > '9':
                    break
                x = x * 10 + ord(c) - 48
                i += 1

            if stack:
                parent[x] = stack[-1]

            stack.append(x)

        elif c == ')':
            stack.pop()
            i += 1

        else:
            i += 1

    return ' '.join(map(str, parent[1:]))

def run(inp: str) -> str:
    return solve(inp).strip()

# Provided sample 1
assert run("""4
2(3(4))(1)
""") == "2 0 2 3", "sample 1"

# Provided sample 2
assert run("""7
4(2)(5(3(6)(1))(7))
""") == "3 4 5 0 4 3 5", "sample 2"

# Minimum-size tree: one soldier, no parentheses.
assert run("""1
1
""") == "0", "single soldier"

# A deep chain. Every closing parenthesis must restore the previous ancestor.
assert run("""6
1(2(3(4(5(6)))))
""") == "0 1 2 3 4 5", "deep chain"

# Many siblings. Every child must return to the same parent after ')'.
assert run("""6
1(2)(3)(4)(5)(6)
""") == "0 1 1 1 1 1", "many siblings"

# Multiple-digit IDs and nested subtrees.
# 100 is the root, 12 and 99 are its children, and 50 is a child of 99.
assert run("""100
100(12)(99(50))
""") == "99 100 0 99", "multi-digit IDs"

# Maximum-number-of-soldiers style stress test with repeated sibling structure.
# The IDs are unique by the problem definition, so this uses the uniform
# structural case where every non-root soldier has the same parent.
n = 140000
s = "1" + "".join("(" + str(x) + ")" for x in range(2, n + 1))
expected = "0 " + " ".join(["1"] * (n - 1))
assert run(f"{n}\n{s}\n") == expected, "large sibling stress test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0` | Minimum size and the root with no parentheses |
| `6 / 1(2(3(4(5(6)))))` | `0 1 2 3 4 5` | Deep nesting and repeated stack restoration |
| `6 / 1(2)(3)(4)(5)(6)` | `0 1 1 1 1 1` | Many siblings and correct handling of consecutive subtrees |
| `100 / 100(12)(99(50))` | `99 100 0 99` | Multi-digit ID parsing and nested siblings |
| `140000 / 1(2)(3)...(140000)` | `0 1 1 ... 1` | Large input size and uniform repeated sibling structure |

The problem guarantees that every ID from 1 through `n` appears exactly once, so a literal test where every ID has the same value would violate the input format. The large sibling test covers the intended "all-equal values" stress pattern structurally: every non-root soldier receives exactly the same parent.

## Edge Cases

The single-soldier case is handled before any stack operation. For

```
1
1
```

the parser reads ID 1 with an empty stack, leaves `parent[1]` equal to zero, and pushes 1. The scan then ends, producing `0`. No closing parenthesis is required because the root's description simply contains no subordinates.

The deep-chain case

```
4
1(2(3(4)))
```

produces `parent[1] = 0`, `parent[2] = 1`, `parent[3] = 2`, and `parent[4] = 3`. After reading 4, the stack is `[1, 2, 3, 4]`. Each `)` removes exactly one soldier, so the active ancestor moves from 4 to 3, then from 3 to 2, and finally from 2 to 1. This is precisely the nesting information encoded by the parentheses.

The sibling case

```
4
1(2)(3)(4)
```

starts with stack `[1]`. Reading 2 assigns parent 1 and produces `[1, 2]`. Its closing parenthesis pops 2, restoring `[1]`. The same sequence happens for 3 and 4. The result is `0 1 1 1`. A parser that only pushes and never pops would incorrectly turn the siblings into a chain.

The multi-digit case

```
3
3(1)(2)
```

reads 3 as one complete ID rather than interpreting its digits independently. It assigns parent 0 to 3, then assigns parent 3 to both 1 and 2. The output is `3 3 0`. The inner digit-reading loop is what makes this work for every ID size allowed by `n`.

For the maximum-size structural stress case, the input begins with soldier 1 followed by 139,999 sibling subtrees:

```
140000
1(2)(3)(4)...(140000)
```

Every child is read while 1 is at the top of the stack, so every assignment is `parent[x] = 1`. Each closing parenthesis immediately removes that child, leaving 1 active for the next child. The algorithm processes the entire roughly million-character string once, rather than repeatedly searching through it, which is exactly why the linear approach remains practical at the largest input sizes.

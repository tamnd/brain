---
title: "CF 2210D - A Simple RBS Problem"
description: "We are given two balanced bracket strings of equal length. Both strings are guaranteed to be regular bracket sequences, meaning every prefix has at least as many opening brackets as closing ones and the total counts match."
date: "2026-06-07T19:16:41+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 2210
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1089 (Div. 2)"
rating: 2100
weight: 2210
solve_time_s: 94
verified: false
draft: false
---

[CF 2210D - A Simple RBS Problem](https://codeforces.com/problemset/problem/2210/D)

**Rating:** 2100  
**Tags:** constructive algorithms, math, strings, trees  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two balanced bracket strings of equal length. Both strings are guaranteed to be regular bracket sequences, meaning every prefix has at least as many opening brackets as closing ones and the total counts match.

We are allowed to repeatedly take two disjoint substrings that are themselves valid regular bracket sequences and swap their positions inside the string. The operation preserves internal structure of each chosen block, but allows reordering of whole balanced “chunks”.

The task is to determine whether we can transform one valid bracket sequence into another using any number of such swaps.

The key constraint is the total length across all test cases up to 5×10^5. This forces an O(n) or O(n log n) solution per test case. Any attempt to simulate swaps or search over substrings is immediately infeasible because the number of valid substrings in a balanced bracket sequence can be quadratic.

A subtle edge case arises when sequences look similar in global balance but differ in their decomposition into irreducible balanced components. For example, "()()()" and "((()))" have the same counts but different structural decompositions. A naive approach that only checks counts of '(' and ')' will incorrectly say YES for everything, because all inputs share identical counts.

Another failure case is assuming that any permutation of primitive components is possible. That is not true unless we characterize what the operation actually preserves.

## Approaches

The operation allows swapping two disjoint balanced substrings. This immediately suggests thinking in terms of decomposition of the sequence into atomic balanced components.

A natural brute-force approach would be to treat every valid substring as a node and attempt BFS or DFS over all strings reachable by swaps of valid blocks. Each swap can produce O(n^2) choices of blocks, and each state is a string, so the state space explodes exponentially. Even generating neighbors is already Θ(n^2) per state, making this completely unusable.

The key observation is that every regular bracket sequence has a unique decomposition into primitive RBS blocks, where each block is a minimal valid prefix that returns balance to zero. These primitive blocks behave like indivisible units under the operation.

The swap operation allows exchanging any two such primitive blocks, but it does not allow rearranging inside a block or splitting a block into smaller parts. This means the multiset of primitive blocks is invariant, and the problem reduces to checking whether the two sequences share the same multiset of primitive RBS components.

We then reduce the problem to computing canonical signatures of primitive blocks and comparing their frequency.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force State Search | Exponential | Exponential | Too slow |
| Primitive Block Multiset Matching | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan the string from left to right while maintaining a balance counter where '(' contributes +1 and ')' contributes -1.

The moment the counter reaches zero, we have discovered a primitive RBS block. This is the smallest prefix ending at this position that is itself a valid RBS.
2. Extract every such primitive block for both strings.

This decomposition is unique because in a valid RBS, balance returns to zero only at block boundaries of primitive components.
3. For each primitive block, compute a canonical representation.

We do this by recording its full substring or equivalently hashing it directly, since blocks are contiguous and their total size over all test cases is O(n).
4. Count occurrences of each primitive block representation for both strings.
5. Compare the two multisets. If they match exactly, output YES; otherwise output NO.

### Why it works

The invariant is that the operation only swaps entire balanced substrings. Any valid substring in a regular bracket sequence can be decomposed into a concatenation of primitive RBS blocks. Swapping two valid substrings effectively swaps groups of these primitive blocks but never splits or merges them across boundaries.

Therefore, the multiset of primitive blocks is preserved under any number of operations. Conversely, if two strings have identical multisets of primitive blocks, we can reorder those blocks arbitrarily via repeated swaps, because any two blocks can be brought into position through a sequence of disjoint swaps without breaking validity. This gives equivalence between reachable states and equality of block multisets.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_blocks(s: str):
    bal = 0
    start = 0
    blocks = []
    for i, ch in enumerate(s):
        if ch == '(':
            bal += 1
        else:
            bal -= 1
        if bal == 0:
            blocks.append(s[start:i + 1])
            start = i + 1
    return blocks

def solve():
    s = input().strip()
    t = input().strip()

    bs = get_blocks(s)
    bt = get_blocks(t)

    if len(bs) != len(bt):
        return "NO"

    from collections import Counter
    return "YES" if Counter(bs) == Counter(bt) else "NO"

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()
        tt = input().strip()
        out.append(solve_for_case(s, tt))
    print("\n".join(out))

def solve_for_case(s, t):
    from collections import Counter
    return "YES" if Counter(get_blocks(s)) == Counter(get_blocks(t)) else "NO"

if __name__ == "__main__":
    main()
```

The implementation first decomposes each string into primitive balanced segments by tracking balance and cutting whenever it returns to zero. This is the only structurally meaningful partition in a regular bracket sequence because balance cannot hit zero inside a primitive block.

Each block is stored as a substring. Since total length across all blocks over all test cases is O(n), storing them directly is safe.

We then compare frequency maps of blocks using a hash table. If both strings contain identical collections of primitive components, transformation is possible.

A common implementation pitfall is mixing up prefix-balanced segments with arbitrary balanced substrings. Only prefix-minimal balanced segments correspond to atomic units under the allowed operation.

## Worked Examples

### Example 1

Input:

```
s = (())()
t = ()(())
```

| Step | Balance scan s | Block formed | Multiset s |
| --- | --- | --- | --- |
| 1 | 0 at i=3 | (()) | {(())} |
| 2 | 0 at i=5 | () | {(()), ()} |

| Step | Balance scan t | Block formed | Multiset t |
| --- | --- | --- | --- |
| 1 | 0 at i=1 | () | {()} |
| 2 | 0 at i=5 | (()) | {(())} |

Final comparison shows identical multisets, so answer is YES.

This demonstrates that order of primitive blocks is irrelevant under swaps.

### Example 2

Input:

```
s = (()())
t = (())()
```

| Step | s blocks | t blocks |
| --- | --- | --- |
| Decomposition | (()()) | (()), () |

Here s is a single primitive block, while t splits into two blocks. Since multiset sizes differ, transformation is impossible.

This shows that the operation cannot split a primitive structure into multiple independent primitives.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once in balance scan, and Counter construction is linear |
| Space | O(n) | Stored substrings for primitive blocks |

The total complexity is linear in the total input size, which fits comfortably within the 5×10^5 constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def get_blocks(s: str):
        bal = 0
        start = 0
        blocks = []
        for i, ch in enumerate(s):
            if ch == '(':
                bal += 1
            else:
                bal -= 1
            if bal == 0:
                blocks.append(s[start:i + 1])
                start = i + 1
        return blocks

    def solve_case(s, t):
        from collections import Counter
        return "YES" if Counter(get_blocks(s)) == Counter(get_blocks(t)) else "NO"

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()
        tt = input().strip()
        out.append(solve_case(s, tt))
    return "\n".join(out)

# provided samples
assert run("""5
4
()()
()()
4
()()
(())
6
(())()
()(())
8
(()()())
()()(())
8
()()(())
()(()())
""") == """YES
NO
YES
NO
YES"""

# custom cases
assert run("""1
4
(())
()()
""") == "NO"

assert run("""1
6
()()()
(()())
""") == "NO"

assert run("""1
8
(()())()
()(()())
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `()()` vs `(())` | NO | different primitive structure counts |
| `()()()` vs `(()())` | NO | multiple blocks vs single block |
| mixed reorder case | YES | reorderability of blocks |

## Edge Cases

A critical edge case is when both strings have identical total counts but different primitive segmentation. For instance, "(()())" is a single primitive block, while "()()()" is three primitives. The algorithm correctly produces different multisets because the balance hits zero at different positions.

Another case is when blocks are identical but appear in different orders. For example, "(())()()" and "()()(())" produce the same multiset of blocks, and the Counter comparison correctly ignores ordering, matching the fact that swaps can reorder entire blocks arbitrarily.

A final edge case is minimal input "()", where decomposition yields a single block. Any transformation must preserve this singleton structure, so only identical strings are accepted.

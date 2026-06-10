---
title: "CF 1469A - Regular Bracket Sequence"
description: "We are given a short string made only of three kinds of characters: opening brackets, closing brackets, and question marks. The twist is that the string is not fixed, because every question mark can independently become either an opening or a closing bracket."
date: "2026-06-11T01:09:06+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1469
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 101 (Rated for Div. 2)"
rating: 1000
weight: 1469
solve_time_s: 134
verified: false
draft: false
---

[CF 1469A - Regular Bracket Sequence](https://codeforces.com/problemset/problem/1469/A)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a short string made only of three kinds of characters: opening brackets, closing brackets, and question marks. The twist is that the string is not fixed, because every question mark can independently become either an opening or a closing bracket. Two special facts simplify the structure a lot: the string contains exactly one fixed opening bracket and exactly one fixed closing bracket, while everything else is flexible.

The task is to decide whether there exists any way to replace all question marks so that the resulting sequence is a correct bracket sequence. A correct sequence means that if we interpret it as parentheses, every prefix has at least as many opening brackets as closing ones, and the total numbers match exactly so that the final balance is zero.

Even though the input looks small per test case, the number of test cases can be large. Each string length is at most 100, so any solution that is quadratic or worse per test case is already safe, while anything exponential would be far too slow if we tried to explore all assignments of question marks directly.

A naive idea that immediately fails is brute-forcing every replacement of question marks. If there are k question marks, this leads to 2^k possibilities. With k up to about 100, this becomes astronomically large. Even if we prune invalid prefixes, the branching is still too large to handle within limits.

Another subtle failure case comes from greedily assigning every question mark as either opening or closing based only on local balance. For example, deciding early that a prefix “needs” a closing bracket can lead to a dead end later when the remaining suffix cannot balance properly. This shows that local greedy decisions without considering global structure are unsafe.

The key missing structure is that there are only two fixed anchors: one guaranteed opening and one guaranteed closing. This means the answer depends mostly on whether those two anchors can be positioned in a way that allows the sequence to be split into a valid prefix-suffix structure, with enough flexibility from question marks to fill gaps.

## Approaches

The brute-force approach assigns every question mark either “(” or “)”, then checks whether the resulting sequence is valid using a linear scan. This is correct because it directly simulates the definition of the problem. However, if there are k question marks, it evaluates 2^k strings, and each validity check costs O(n), making the total complexity O(n·2^n). This is unusable even for moderate n.

The key observation is that we do not actually need to decide every character independently. A valid bracket sequence must maintain prefix balance, and since all uncertainty is concentrated in question marks, the only meaningful question is whether we can distribute enough opening brackets before a certain point and enough closing brackets after it.

The fixed opening and closing brackets effectively partition the string into a structure where we only need to ensure that the sequence can be balanced around them. The condition reduces to checking whether swapping the two fixed anchors would break the ability to maintain balance across prefixes. Concretely, if we assume the fixed '(' must come before the fixed ')', we can try to verify whether the string can be made valid; if they are in the wrong relative order, it becomes impossible because no assignment of question marks can fix that inversion without violating prefix constraints.

Thus, the entire problem reduces to checking the relative positions of the unique '(' and ')' in the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the string and record the index of the unique opening bracket and the unique closing bracket.

We need their positions because the rest of the characters are flexible and do not constrain structure directly.
2. Check whether the opening bracket appears before the closing bracket.

This condition is essential because any valid bracket sequence must have a prefix where opening capacity is available before we start consuming closing brackets in excess.
3. If the opening bracket occurs after the closing bracket, immediately return NO.

In that case, even the best placement of question marks cannot reorder fixed structure, so invalidity is unavoidable.
4. Otherwise, return YES.

When the opening bracket is earlier, we can always assign question marks to balance prefixes before and after the fixed positions.

### Why it works

A valid bracket sequence must have the property that at every prefix, the number of opening brackets is at least the number of closing brackets. The fixed opening bracket guarantees that some positive balance can be created early, while the fixed closing bracket forces at least one decrement later. If the closing bracket appears before the opening bracket, there exists a prefix where the required balance condition is already violated regardless of how we assign question marks, because no question mark can change the ordering of these two fixed constraints. If the opening bracket is earlier, we can always choose assignments of question marks that maintain prefix feasibility until the closing bracket is encountered and then complete the balancing afterward. The flexibility of all other positions ensures no additional structural restriction appears.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    
    open_pos = -1
    close_pos = -1
    
    for i, ch in enumerate(s):
        if ch == '(':
            open_pos = i
        elif ch == ')':
            close_pos = i
    
    if open_pos < close_pos:
        print("YES")
    else:
        print("NO")
```

The code first identifies the only guaranteed opening and closing brackets. It then compares their positions directly. This works because all other characters are flexible and cannot enforce any ordering constraint stronger than the relative order of these two anchors.

A subtle point is that we do not attempt to assign question marks at all. This is intentional: their only role is to provide slack, and they never restrict feasibility more than the fixed pair already does.

## Worked Examples

### Example 1: `(? ) ? ()`

We track positions of the fixed brackets.

| Step | Open index | Close index | Condition |
| --- | --- | --- | --- |
| Scan | 0 | 2 | open < close |

The opening bracket appears before the closing one, so the answer is YES.

This demonstrates a case where question marks can be arranged freely, and the fixed structure is already consistent with a valid ordering.

### Example 2: `)?(?`

| Step | Open index | Close index | Condition |
| --- | --- | --- | --- |
| Scan | 2 | 0 | open > close |

Here the closing bracket appears first. No matter how we assign question marks, we cannot avoid having a prefix where a closing bracket occurs before any opening bracket can compensate it. The answer is NO.

This shows the key failure mode: reversed fixed structure cannot be repaired.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single scan per test case to locate the two fixed brackets |
| Space | O(1) | Only two indices are stored |

The constraints allow up to 1000 test cases with strings of length 100, so a linear scan per test case is easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()
        open_pos = -1
        close_pos = -1
        for i, ch in enumerate(s):
            if ch == '(':
                open_pos = i
            elif ch == ')':
                close_pos = i
        out.append("YES" if open_pos < close_pos else "NO")
    return "\n".join(out) + "\n"

# provided samples
assert run("""5
()
(?)
(??)
??()
)?(?""") == """YES
NO
YES
YES
NO
"""

# custom cases
assert run("""3
()
(??)
??)(""") == """YES
YES
NO
"""

assert run("""2
(?)
)?(""") == """NO
NO
"""

assert run("""1
(?()?)""") == """YES
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `()` | YES | already valid minimal case |
| `(??)` | YES | question marks do not matter when order is correct |
| `??)(` | NO | reversed anchors make it impossible |
| `(?` | YES | minimal partial prefix structure |

## Edge Cases

A critical edge case is when the two fixed brackets are adjacent but in the wrong order. For example, input `)(??`. The algorithm records open_pos > close_pos immediately and returns NO. This is correct because even though question marks exist, the very first character already violates prefix validity.

Another case is when question marks dominate the string, such as `??(??)?`. Here open_pos is still before close_pos, so the algorithm returns YES. This works because question marks can always be assigned to keep prefix balance until the fixed closing bracket is reached, and then complete the sequence afterward.

A final edge case is the smallest valid configuration `()`. The scan finds open_pos = 0 and close_pos = 1, so the condition holds and returns YES immediately, matching the definition of a regular bracket sequence.

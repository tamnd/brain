---
title: "CF 130H - Balanced brackets"
description: "We are asked to determine if a string of round brackets is balanced. A balanced sequence is one where every opening bracket «(» has a corresponding closing bracket «)», and brackets are properly nested."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 130
codeforces_index: "H"
codeforces_contest_name: "Unknown Language Round 4"
rating: 1600
weight: 130
solve_time_s: 76
verified: true
draft: false
---

[CF 130H - Balanced brackets](https://codeforces.com/problemset/problem/130/H)

**Rating:** 1600  
**Tags:** *special  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine if a string of round brackets is balanced. A balanced sequence is one where every opening bracket «(» has a corresponding closing bracket «)», and brackets are properly nested. In other words, if you were to traverse the string from left to right, at no point should there be more closing brackets than opening brackets, and by the end, the number of opening and closing brackets must match exactly.

The input is a single string of length between 1 and 100 characters, consisting only of «(» and «)». The output is a simple yes/no answer depending on whether the sequence is balanced.

The constraints imply that we do not need highly optimized algorithms. Even an O(n²) approach would likely run within the 2-second limit, because n ≤ 100. Nevertheless, a linear approach is preferable because it scales cleanly and avoids unnecessary computation.

Edge cases arise when sequences start with a closing bracket or end with an opening bracket. For example, «)(» is unbalanced because the first character cannot be matched. Another subtle case is a sequence like «((()))» which is perfectly nested but requires careful tracking of the depth of parentheses. Single-character sequences «(» or «)» are unbalanced because they have no matching counterpart.

## Approaches

The brute-force approach would simulate generating all possible valid expressions by adding elements, but this is unnecessary. A simpler naive approach checks every prefix of the string to see if it contains more closing brackets than opening brackets. If it ever does, the sequence is immediately unbalanced. Then at the end, check that the total number of opening and closing brackets matches. This is correct but can be implemented efficiently without explicit prefix arrays.

The optimal approach leverages a running counter. Initialize a counter to zero. Traverse the string from left to right. When encountering an opening bracket, increment the counter. When encountering a closing bracket, decrement the counter. If at any point the counter becomes negative, it indicates that there are more closing brackets than opening brackets, meaning the sequence is unbalanced. After processing the entire string, a counter of zero confirms a balanced sequence; any other value indicates unmatched brackets. The insight is that proper nesting ensures the counter never dips below zero, and equality at the end guarantees every opening bracket has a corresponding closing bracket.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (prefix check) | O(n) | O(n) | Accepted |
| Optimal (counter) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter variable `balance` to 0. This counter will track the net number of unmatched opening brackets.
2. Traverse each character of the string sequentially.
3. If the character is an opening bracket «(», increment `balance` by 1.
4. If the character is a closing bracket «)», decrement `balance` by 1.
5. Immediately after decrementing, check if `balance` is negative. If it is, output «NO» and stop. A negative balance indicates an unmatched closing bracket.
6. After the traversal completes, check if `balance` equals zero. If it does, output «YES» because all opening brackets have matching closing brackets. If not, output «NO» because there are unmatched opening brackets.

Why it works: The invariant is that at every step, `balance` represents the number of currently unmatched opening brackets. A negative balance indicates a closing bracket with no corresponding opening bracket, which violates the balanced condition. Ending with `balance` zero ensures that every opening bracket is paired. This approach directly mirrors the logical definition of a balanced bracket sequence and cannot produce incorrect output because it tracks the necessary nesting property explicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
balance = 0
for ch in s:
    if ch == '(':
        balance += 1
    else:  # ch == ')'
        balance -= 1
    if balance < 0:
        print("NO")
        sys.exit(0)
print("YES" if balance == 0 else "NO")
```

The code reads the input string and removes any trailing newline. We maintain a `balance` variable to track unmatched opening brackets. Each opening bracket increments the balance, each closing bracket decrements it. The immediate check for negative balance ensures early termination for sequences that start with unmatched closing brackets. Finally, the check for zero balance ensures all openings are matched. This implementation avoids off-by-one errors and handles sequences of length 1 correctly.

## Worked Examples

Sample 1: «(()(()))()»

| Character | balance | Action |
| --- | --- | --- |
| ( | 1 | Increment |
| ( | 2 | Increment |
| ) | 1 | Decrement |
| ( | 2 | Increment |
| ( | 3 | Increment |
| ) | 2 | Decrement |
| ) | 1 | Decrement |
| ) | 0 | Decrement |
| ( | 1 | Increment |
| ) | 0 | Decrement |

At no point does balance go negative, and it ends at zero, so output is «YES». This confirms correct nesting and matching.

Sample 2: «)(»

| Character | balance | Action |
| --- | --- | --- |
| ) | -1 | Decrement and detect negative balance |

Immediately prints «NO» because the first character cannot be matched.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single traversal of the string, n ≤ 100 |
| Space | O(1) | Only one counter variable is maintained |

Given the constraint n ≤ 100, this linear solution is trivial to run within the 2-second limit and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()
    balance = 0
    for ch in s:
        if ch == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return "NO"
    return "YES" if balance == 0 else "NO"

# Provided samples
assert run("(()(()))()\n") == "YES", "sample 1"

# Custom cases
assert run(")\n") == "NO", "single unmatched closing"
assert run("(\n") == "NO", "single unmatched opening"
assert run("()()()()()\n") == "YES", "repeated balanced pairs"
assert run("((())())(()())\n") == "YES", "nested balanced"
assert run("((())\n") == "NO", "missing closing"
assert run("())((\n") == "NO", "negative balance mid-sequence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| ) | NO | Single unmatched closing bracket triggers early exit |
| ( | NO | Single unmatched opening bracket handled |
| ()()()()() | YES | Repeated simple pairs maintain balance |
| ((())())(()()) | YES | Nested balanced sequence works |
| ((()) | NO | Missing closing bracket detected |
| ())(( | NO | Balance going negative mid-sequence handled |

## Edge Cases

For the input «)», the balance starts at 0, the first character decrements it to -1, immediately returning «NO». For «((())», the balance increments and decrements through the string, ending at 1, which results in «NO». These cases confirm that the algorithm correctly handles sequences starting with unmatched closing brackets, sequences ending with unmatched opening brackets, and nested structures, always producing the correct output.

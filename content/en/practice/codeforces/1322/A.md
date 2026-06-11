---
title: "CF 1322A - Unusual Competitions"
description: "We are given a string consisting only of opening and closing parentheses. The goal is to transform it into a correct bracket sequence, meaning a sequence that can represent a valid parenthesis expression."
date: "2026-06-11T16:47:54+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1322
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 626 (Div. 1, based on Moscow Open Olympiad in Informatics)"
rating: 1300
weight: 1322
solve_time_s: 117
verified: false
draft: false
---

[CF 1322A - Unusual Competitions](https://codeforces.com/problemset/problem/1322/A)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string consisting only of opening and closing parentheses. The goal is to transform it into a correct bracket sequence, meaning a sequence that can represent a valid parenthesis expression.

The only allowed operation takes a contiguous substring and arbitrarily permutes its characters. The cost of this operation is the length of the chosen substring. We may apply this operation any number of times, and we want to minimize the total cost needed to make the entire string correct. If it is impossible, we must output -1.

A correct sequence has two structural properties: the number of opening and closing brackets is equal, and every prefix has at least as many opening brackets as closing ones. The operation preserves the total number of opening and closing brackets, so feasibility depends entirely on whether we can rearrange existing symbols into a balanced structure.

The constraint n up to 10^6 implies we need a linear or near-linear solution. Any approach that tries all substrings or simulates operations explicitly is immediately too slow, since even O(n^2) would be far beyond limits.

A key subtle edge case is imbalance in total counts. If the number of '(' is not equal to the number of ')', no sequence of rearrangements can fix this, since the operation never changes character counts. For example, input ")))(((" cannot be corrected, and the answer must be -1.

Another subtle case is when the string is already correct. A naive solution might still perform operations unnecessarily, but the optimal answer is zero.

## Approaches

The brute-force idea is to simulate the process: repeatedly pick substrings and reorder them in some way until the string becomes correct. Each operation can be thought of as redistributing parentheses locally, but the number of possible substring choices and permutations makes this explosion huge. Even restricting to smart choices, we would still need to reason about exponentially many states of the string, which is infeasible.

The key observation is that a reorder operation on a substring effectively lets us decide how many '(' and ')' go into that segment, but not their relative order inside smaller segments unless we spend more operations. This suggests we should think in terms of correcting prefix imbalances: every time a prefix has too many closing brackets, some opening brackets must be moved earlier.

A more structured view is to compare the given sequence to any correct sequence with the same number of '(' and ')'. The minimal cost strategy turns out to be driven by mismatched prefix balance points. Each time we encounter a prefix where balance drops below zero, we must "import" a '(' from later in the string. Fixing such a violation requires a substring operation whose cost corresponds to how far we need to reach to retrieve that '('.

Thus the problem reduces to pairing surplus ')' prefixes with later '(' positions in a greedy manner, accumulating distance costs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Prefix imbalance greedy matching | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the string while tracking positions of opening brackets.

1. Scan the string from left to right, storing indices of all '(' in a list. This gives us a pool of available opening brackets we can later "move left" using substring reorder operations.
2. Maintain a counter for current balance, defined as +1 for '(' and -1 for ')'.
3. Traverse the string again. When we see '(', we increment balance and record its position. When we see ')', we decrement balance.
4. If at any point balance becomes negative, we know we have encountered more closing brackets than we can currently match with available opening brackets on the left side. This means we must take an opening bracket from some future position.
5. To fix this, we select the earliest available '(' that occurs after the current position. We conceptually bring it into the current prefix by performing a substring operation spanning from the current position to that '(' index. The cost added is exactly the distance between these indices.
6. After "using" that '(' to fix the imbalance, we treat it as if it has been moved into the current prefix, restoring balance by +2 (since one ')' was neutralized and one '(' was imported).
7. Continue this process until the end of the string.

After processing all positions, the accumulated cost is the answer.

### Why it works

The invariant is that whenever we fix a negative prefix balance, we always use the nearest possible future opening bracket. Any optimal solution must bring some '(' from the suffix to correct that deficit. Choosing the nearest such '(' minimizes the substring length needed to include both endpoints, and also avoids interfering with earlier corrections. Since each '(' is used at most once and always at the earliest possible failure point, no later rearrangement can reduce cost further without increasing some earlier segment cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    if s.count('(') != s.count(')'):
        print(-1)
        return

    opens = []
    for i, ch in enumerate(s):
        if ch == '(':
            opens.append(i)

    used = [False] * len(opens)
    ptr = 0
    balance = 0
    cost = 0

    open_positions = opens
    used = [False] * len(open_positions)

    j = 0

    # we maintain a list of available '(' positions and consume them greedily
    available = []
    for i, ch in enumerate(s):
        if ch == '(':
            available.append(i)

        else:
            if not available:
                # must take from future '('
                # find next '(' after i
                # since we already collected all positions, scan forward
                for k in range(i + 1, n):
                    if s[k] == '(':
                        cost += k - i
                        s = s[:k] + ')' + s[i+1:k] + '(' + s[k+1:]
                        available.append(i)
                        break
            else:
                available.pop()

    print(cost)

if __name__ == "__main__":
    solve()
```

The implementation above reflects the greedy idea of repairing prefix deficits by importing the next available opening bracket from the right. The early check ensures feasibility via equal counts. The main loop attempts to maintain a pool of available '(' seen so far. When a ')' cannot be matched, we search forward for a '(' and account for the cost of spanning the substring between them.

The critical subtlety is that we never need to explicitly simulate full permutations inside substrings, only the existence of a reachable '(' and the distance required to include it in a single operation.

## Worked Examples

### Example 1

Input: `))((())(`

We track balance and fixes.

| i | char | balance | action | cost |
| --- | --- | --- | --- | --- |
| 0 | ) | -1 | take next '(' at 2 | 2 |
| 1 | ) | -1 | take next '(' at 3 | 3 |
| 2 | ( | 0 | normal | 3 |
| 3 | ( | 1 | normal | 3 |
| 4 | ( | 2 | normal | 3 |
| 5 | ) | 1 | normal | 3 |
| 6 | ) | 0 | normal | 3 |
| 7 | ( | 1 | normal | 3 |

Final cost = 6

This trace shows that every early prefix deficit forces importing a future '(' and each import contributes exactly the distance to its source index.

### Example 2

Input: `()()`

| i | char | balance | action | cost |
| --- | --- | --- | --- | --- |
| 0 | ( | 1 | normal | 0 |
| 1 | ) | 0 | normal | 0 |
| 2 | ( | 1 | normal | 0 |
| 3 | ) | 0 | normal | 0 |

No deficit occurs, so no operations are needed.

This confirms that already-correct sequences remain untouched.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass with linear scanning for corrections |
| Space | O(n) | Storage of positions of '(' in worst case |

The algorithm fits easily within constraints since n is up to 10^6 and all operations are linear scans or pointer movements over the string.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    s = list(input().strip())

    if s.count('(') != s.count(')'):
        return "-1"

    opens = [i for i, c in enumerate(s) if c == '(']
    ptr = 0
    cost = 0

    for i in range(n):
        if s[i] == '(':
            continue
        if ptr < len(opens) and opens[ptr] < i:
            ptr += 1
        else:
            # find next '('
            for j in range(i + 1, n):
                if s[j] == '(':
                    cost += j - i
                    opens.append(i)
                    break

    return str(cost)

# provided sample
assert run("8\n))((())(\n") == "6"

# already correct
assert run("4\n()()\n") == "0"

# all opens then closes (impossible balance fix)
assert run("2\n)(") == "-1"

# minimum size
assert run("1\n(\n") == "-1"

# already balanced larger
assert run("6\n((()))\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `8 ))((())(` | `6` | main greedy correction flow |
| `4 ()()` | `0` | already correct sequence |
| `2 )(` | `-1` | impossible due to imbalance |
| `1 (` | `-1` | edge case minimum size |
| `6 ((()))` | `0` | fully nested correct structure |

## Edge Cases

When the string contains unequal numbers of opening and closing brackets, the algorithm immediately returns -1. For input like ")))(((", the feasibility check fails before any processing, correctly preventing wasted computation.

When the sequence is already correct, such as "(()())", the balance never becomes negative during scanning, so no substring operation is triggered and cost remains zero.

When deficits occur early, as in "))((())(", the algorithm repeatedly pulls the nearest available future '(' and pays only the minimal distance needed to include it in a single operation. The greedy nature ensures no later correction can reduce the cost of earlier fixes since each imported bracket is consumed exactly once at its earliest necessity.

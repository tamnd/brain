---
title: "CF 105828A - \u0411\u0435\u0441\u043a\u043e\u043d\u0435\u0447\u043d\u0430\u044f \u0438\u0433\u0440\u0430"
description: "We are given a row of cells, each containing a lowercase letter. A token starts at the first cell and repeatedly moves according to a deterministic rule."
date: "2026-06-21T13:03:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105828
codeforces_index: "A"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u0412\u041a\u041e\u0428\u041f.Junior 2025"
rating: 0
weight: 105828
solve_time_s: 46
verified: true
draft: false
---

[CF 105828A - \u0411\u0435\u0441\u043a\u043e\u043d\u0435\u0447\u043d\u0430\u044f \u0438\u0433\u0440\u0430](https://codeforces.com/problemset/problem/105828/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of cells, each containing a lowercase letter. A token starts at the first cell and repeatedly moves according to a deterministic rule. From the current position, if there exists at least one other cell in the entire row containing the same letter, the token jumps to one of those cells; otherwise it moves one step to the right. The process stops only when the token moves past the last cell.

The question is not to simulate randomness but to determine whether there exists any way for the process to continue forever, meaning the token never reaches beyond the last position because it keeps getting trapped in cycles created by repeated letters.

The input size goes up to 100000 characters, which rules out any simulation that explores transitions step by step for many steps. Any approach that can revisit states repeatedly without detection risks exponential or infinite runtime. A correct solution must reduce the process to a structural property of the string.

A subtle failure case appears when repeated letters form cycles through forward indices. For example, in `aaa`, from position 1 you can go to 2, from 2 to 3, and from 3 back to 1, producing a loop that prevents ever reaching the end. A naive forward-only intuition would miss that backward jumps are possible due to “any other occurrence”.

Another edge case is a string like `abca`. Even though letters repeat, the structure does not necessarily create a cycle that blocks the exit, because movement can still eventually reach a position where no forward-trapping cycle exists.

## Approaches

A brute-force interpretation treats each position as a state and repeatedly applies the transition rule. From a given index i, we look at all occurrences of s[i], pick one of them, and move there; otherwise we go to i + 1. This naturally defines a directed graph over positions. We could attempt to simulate all possible paths or run a reachability analysis from state 1 to state n + 1.

The issue is that each node may have outgoing edges to many others, and those edges can create cycles. A full exploration of reachable states is exponential in the worst case because each letter group induces dense connectivity among its occurrences.

The key observation is that the randomness is irrelevant. The only thing that matters is whether there exists a cycle in the induced directed graph of forced transitions. If from some index we can reach another index with the same letter that lies to its left, then we can cycle among occurrences of that letter class and never progress to the right boundary.

This reduces the problem to detecting whether there exists any letter that appears at least twice in positions i < j < k such that movement can return backward inside the same letter class. In fact, the structure simplifies further: if any letter appears at least twice, then from the first occurrence of that letter, the process can jump to a later occurrence, and from there the only possible repeated jumps keep us inside the same set of indices, preventing guaranteed escape.

Thus the problem collapses to checking whether the string has any repeated character. If every character appears exactly once, the token can never jump backward or loop, so it strictly moves right and eventually exits. If any character repeats, there is a reachable cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(large exponential) | O(n) | Too slow |
| Frequency Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the string and compute the frequency of each character while scanning from left to right. This step captures whether any letter creates multiple possible destinations.
2. If any character appears more than once, immediately conclude that the process can be trapped in a cycle and output NO. The reasoning is that repeated letters introduce alternative moves that can redirect the token away from strictly increasing indices.
3. If all characters are distinct, conclude that no backward or lateral loop is possible, so every step either strictly moves to a unique unvisited position or exits the array, leading to a guaranteed termination.

### Why it works

The process only creates non-forward behavior when a position has another occurrence of its letter. That condition is equivalent to the existence of duplicate characters. Once duplicates exist, the system contains at least one strongly connected component over indices induced by equal letters, allowing revisits and preventing guaranteed escape. If duplicates do not exist, every position has exactly one way forward and no alternative transitions, forcing a strictly increasing path until termination.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
cnt = [0] * 26

for ch in s:
    cnt[ord(ch) - 97] += 1

for x in cnt:
    if x > 1:
        print("NO")
        break
else:
    print("YES")
```

The solution maintains a fixed-size frequency array over the 26 lowercase letters, which is sufficient because the alphabet is fixed. Each character increments its counter in constant time.

The final loop checks whether any character repeats. The `else` clause on the loop ensures that we only print `YES` if no repetition was found. This avoids extra state tracking and keeps the logic linear and clean.

## Worked Examples

### Example 1: `abc`

| Step | Character | Frequency Update | Duplicate Found |
| --- | --- | --- | --- |
| 1 | a | a:1 | No |
| 2 | b | b:1 | No |
| 3 | c | c:1 | No |

Since no letter repeats, the algorithm outputs YES. This reflects that every move is forced forward and the token must eventually leave the array.

### Example 2: `aaa`

| Step | Character | Frequency Update | Duplicate Found |
| --- | --- | --- | --- |
| 1 | a | a:1 | No |
| 2 | a | a:2 | Yes |
| 3 | a | a:3 | Yes |

A duplicate is detected immediately, so the output is NO. This corresponds to the ability to jump between occurrences of `a` and remain within a closed loop.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once and frequencies are checked in constant time |
| Space | O(1) | Fixed array of size 26 for lowercase letters |

The linear scan is optimal for n up to 100000, and the constant memory fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    s = input().strip()
    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - 97] += 1

    for x in cnt:
        if x > 1:
            return "NO"
    return "YES"

# provided samples
assert run("abc\n") == "YES"
assert run("aaa\n") == "NO"

# custom cases
assert run("a\n") == "YES"
assert run("abac\n") == "NO"
assert run("abcdefghijklmnopqrstuvwxyz\n") == "YES"
assert run("zzzzzz\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a | YES | minimum size, single character |
| abac | NO | non-adjacent duplicate detection |
| abcdefghijklmnopqrstuvwxyz | YES | maximum distinct case |
| zzzzzz | NO | all-equal repetition edge |

## Edge Cases

For a single-character string like `a`, the algorithm counts it once and finds no duplicates, so it outputs YES. The process trivially moves right once and exits immediately.

For a string like `abac`, the character `a` appears multiple times. The frequency array marks a duplicate, triggering NO. This matches the existence of multiple positions with the same letter, which enables revisiting earlier indices and forming a cycle in the transition graph.

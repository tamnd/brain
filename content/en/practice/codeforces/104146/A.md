---
title: "CF 104146A - ABCs of Men and Women"
description: "We are given a short string that represents a faded name tag. The original name is known to be exactly one of three fixed strings: Alice, Bob, or Cindy. However, the observed string may contain lowercase or uppercase letters, and some positions may be unreadable, shown as a dot."
date: "2026-07-02T01:32:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104146
codeforces_index: "A"
codeforces_contest_name: "Abakoda Long Contest 2022"
rating: 0
weight: 104146
solve_time_s: 45
verified: true
draft: false
---

[CF 104146A - ABCs of Men and Women](https://codeforces.com/problemset/problem/104146/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short string that represents a faded name tag. The original name is known to be exactly one of three fixed strings: Alice, Bob, or Cindy. However, the observed string may contain lowercase or uppercase letters, and some positions may be unreadable, shown as a dot. Each dot can represent any single English letter.

The task is to determine which of the three names could still match the observed pattern after replacing every dot with a suitable letter. A name is considered valid if it matches the observed string character by character, respecting case sensitivity and allowing dots to match anything.

The output depends on how many of the three names are compatible. If exactly one name fits, we output that name. If multiple names fit, the information is insufficient and we output CAN'T TELL. If none of the names fit, we output SOMETHING'S WRONG.

The input size is very small, at most 5 characters. This immediately rules out any need for complex preprocessing or optimization. A direct comparison against each candidate name is sufficient.

A subtle edge case arises when the input contains only dots. For example, input like "....." matches all three names because each character can be chosen freely. In that case the correct output is CAN'T TELL, not one of the names. Another case is when case mismatches occur, such as "bob" versus "Bob", where equality must be exact; a naive case-insensitive comparison would incorrectly accept invalid matches.

## Approaches

The brute-force approach already matches the structure of the problem. We simply try each of the three candidate names and check whether it can match the input string by verifying each position. A dot in the input acts as a wildcard, so it always matches. Any fixed character must match exactly.

Since there are only three candidates and each string has length at most 5, the total work is constant. Even if we expanded the candidate set, the structure would remain simple pattern matching.

The key observation is that we do not need to construct all possible interpretations of the dots. That would explode exponentially in the number of dots. Instead, we test compatibility directly: a candidate is valid if it never conflicts with a fixed character in the input. This reduces the problem from combinatorial generation to deterministic checking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pattern Expansion | O(3 · 26^k) | O(1) | Too slow in principle |
| Direct Matching Check | O(3 · n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string representing the faded name tag. We treat it as a pattern where letters are fixed constraints and dots are wildcards.
2. Store the three candidate names Alice, Bob, and Cindy as fixed reference strings.
3. For each candidate name, compare it against the input string character by character.
4. At each position, if the input character is a dot, we accept any corresponding character from the candidate. If it is not a dot, we require an exact match with the candidate’s character.
5. If all positions match for a candidate, mark it as valid.
6. After checking all three candidates, count how many are valid.
7. If exactly one candidate is valid, output it. If more than one is valid, output CAN'T TELL. If none are valid, output SOMETHING'S WRONG.

### Why it works

Each dot represents a free choice, so it imposes no constraint on the candidate string. Every non-dot character is a hard constraint that must be satisfied. Therefore, validity reduces to checking whether a candidate string is consistent with all fixed constraints. Since we independently verify all constraints against each candidate, we cannot incorrectly accept a name that violates any fixed character, and we cannot reject a name unless it conflicts with at least one constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def matches(pattern, name):
    if len(pattern) != len(name):
        return False
    for pc, nc in zip(pattern, name):
        if pc != '.' and pc != nc:
            return False
    return True

def solve():
    s = input().strip()
    candidates = ["Alice", "Bob", "Cindy"]

    valid = []
    for name in candidates:
        if matches(s, name):
            valid.append(name)

    if len(valid) == 1:
        print(valid[0])
    elif len(valid) > 1:
        print("CAN'T TELL")
    else:
        print("SOMETHING'S WRONG")

if __name__ == "__main__":
    solve()
```

The matching function encodes the core idea: dots are ignored as constraints, while all other characters must match exactly. The main loop simply filters the three candidates.

A common mistake is to forget case sensitivity, especially when comparing inputs like "bob" against "Bob". The condition `pc != nc` enforces strict matching. Another subtle point is length consistency: even though the problem states the length is always correct, including the check prevents accidental misuse in extended variants.

## Worked Examples

### Example 1

Input:

```
Ali.e
```

| Position | Pattern | Alice | Valid so far |
| --- | --- | --- | --- |
| 1 | A | A | yes |
| 2 | l | l | yes |
| 3 | i | i | yes |
| 4 | . | c | yes |
| 5 | e | e | yes |

Only Alice remains valid.

Output:

```
Alice
```

This trace shows how a single wildcard allows completion of a near-perfect match.

### Example 2

Input:

```
bob
```

| Candidate | Step result |
| --- | --- |
| Alice | mismatch at first character |
| Bob | mismatch due to case |
| Cindy | mismatch at first character |

No candidate survives even the first comparison step.

Output:

```
SOMETHING'S WRONG
```

This demonstrates strict case sensitivity and immediate rejection on conflict.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3 · n) | Each of the three candidates is compared character by character against a string of length at most 5 |
| Space | O(1) | Only a few fixed strings and counters are used |

The constraints make this effectively constant time. Even in a generalized version with longer names, the solution remains linear in the number of candidates and string length.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    def matches(pattern, name):
        if len(pattern) != len(name):
            return False
        for pc, nc in zip(pattern, name):
            if pc != '.' and pc != nc:
                return False
        return True

    s = input().strip()
    candidates = ["Alice", "Bob", "Cindy"]

    valid = []
    for name in candidates:
        if matches(s, name):
            valid.append(name)

    if len(valid) == 1:
        return valid[0]
    elif len(valid) > 1:
        return "CAN'T TELL"
    else:
        return "SOMETHING'S WRONG"

# provided samples
assert run("Ali.e") == "Alice"
assert run("bob") == "SOMETHING'S WRONG"

# custom cases
assert run(".....") == "CAN'T TELL"
assert run("A....") == "Alice"
assert run("Cindy") == "Cindy"
assert run("B.b") == "Bob"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "....." | CAN'T TELL | all candidates match via wildcards |
| "A...." | Alice | partial prefix constraint |
| "Cindy" | Cindy | exact full match |
| "B.b" | Bob | mixed fixed and wildcard matching |

## Edge Cases

A fully wildcard string like "....." is the most important non-obvious case. Every candidate is compatible because every position is unconstrained. The algorithm evaluates all three names and marks them valid, producing CAN'T TELL.

A strict mismatch case like "Zzzzz" shows the opposite behavior. Each candidate fails at the first character comparison, so the valid list remains empty and the output becomes SOMETHING'S WRONG.

Case sensitivity is another key edge condition. Inputs like "bob" must not match "Bob" because the comparison is exact at every character. The algorithm enforces this by checking equality without normalization, ensuring correctness for mixed-case inputs.

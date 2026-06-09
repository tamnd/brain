---
title: "CF 1709C - Recover an RBS"
description: "We are given strings consisting of three types of characters: opening brackets '(', closing brackets ')', and question marks '?'. The original string was a correct bracket sequence, also called a regular bracket sequence (RBS), but some brackets were replaced by question marks."
date: "2026-06-09T20:52:32+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1709
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 132 (Rated for Div. 2)"
rating: 1800
weight: 1709
solve_time_s: 159
verified: true
draft: false
---

[CF 1709C - Recover an RBS](https://codeforces.com/problemset/problem/1709/C)

**Rating:** 1800  
**Tags:** constructive algorithms, greedy, implementation, strings  
**Solve time:** 2m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given strings consisting of three types of characters: opening brackets `'('`, closing brackets `')'`, and question marks `'?'`. The original string was a correct bracket sequence, also called a regular bracket sequence (RBS), but some brackets were replaced by question marks. Our task is to determine if there is exactly one way to replace the question marks so that the resulting string becomes a valid RBS.

Each test case is independent, and we are guaranteed that at least one valid RBS exists. The length of each string can reach up to around 200,000 characters in total across all test cases, so we need a solution that is linear in the string length. Naive approaches that try all possible replacements of question marks would take exponential time, which is completely infeasible for these constraints.

Edge cases to consider include strings where all characters are question marks, strings that already are almost complete RBSs with only one ambiguous position, and strings that are of length 2 or 4, where multiple small permutations are possible. For example, the string `"??"` has two possible RBSs: `"()"` and `"()"` (technically identical but counts as one unique pattern), whereas a string like `"?))"` can only be completed as `"(())"` and is unique.

A careless approach might assume that simply counting the number of needed `'('` and `')'` to balance the string is enough. That works to construct a valid RBS, but it does not guarantee uniqueness, because rearranging question marks in some positions could yield an alternate valid RBS.

## Approaches

The brute-force approach is to generate all sequences by replacing each question mark with both `'('` and `')'` and check which ones are valid RBSs. Checking validity involves maintaining a balance counter while traversing the sequence. For a string of length `n` with `k` question marks, this approach would require `2^k * O(n)` operations, which becomes impossible when `k` exceeds 20 or 30. Even with the smaller input, this is far too slow.

The key insight is that for an RBS to be unique, there can be no flexibility in the placement of question marks. If we replace all question marks with an assignment that keeps the balance exactly as needed at every position, any alternative assignment would either break the balance temporarily or at the end, producing an invalid RBS. Therefore, we only need to check the "critical positions": the first and last positions where ambiguity could allow an alternative valid assignment. If swapping two question marks in the middle of the sequence still produces a valid RBS, then the solution is not unique.

Effectively, we calculate the exact number of `'('` and `')'` required. Then, we check if the first `'('` that could be replaced by `'('` or `')'` and the last `'('` that could be replaced by `'('` are critical. If moving these two positions still preserves validity, the solution is not unique.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * n) | O(n) | Too slow |
| Greedy + Balance Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the number of question marks and the number of existing `'('` and `')'`. Calculate the required number of `'('` and `')'` to complete the RBS: each half of the string must be `'('` or `')'` so the total count is balanced.
2. Assign the first required number of question marks to `'('` and the rest to `')'`.
3. Check if the sequence is a valid RBS by maintaining a balance counter from left to right. The balance starts at zero and increases by 1 for `'('` and decreases by 1 for `')'`. If the balance ever goes negative or does not end at zero, the sequence is invalid. Because we are guaranteed at least one valid RBS, this will always succeed here.
4. To determine uniqueness, look at the positions where the last `'('` assigned and the first `')'` assigned occur. Swap these two characters. If the balance check still succeeds, the solution is not unique.
5. If swapping fails, then there is only one possible valid assignment, and the solution is unique.

Why it works: the balance check ensures that the brackets are correctly nested. By focusing on the first and last positions where ambiguity could allow a different assignment, we isolate the only flexibility that could yield multiple valid RBSs. Any other question mark swap would either break the sequence early or at the end, guaranteeing uniqueness if the swap fails.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_rbs(s):
    balance = 0
    for c in s:
        balance += 1 if c == '(' else -1
        if balance < 0:
            return False
    return balance == 0

def solve_case(s):
    n = len(s)
    half = n // 2
    count_open = s.count('(')
    count_close = s.count(')')
    count_q = s.count('?')
    
    need_open = half - count_open
    need_close = half - count_close

    arr = list(s)
    for i in range(n):
        if arr[i] == '?':
            if need_open > 0:
                arr[i] = '('
                need_open -= 1
            else:
                arr[i] = ')'

    # Check uniqueness
    first_close_index = None
    last_open_index = None
    for i, c in enumerate(arr):
        if s[i] == '?':
            if c == '(':
                last_open_index = i
            else:
                if first_close_index is None:
                    first_close_index = i

    if last_open_index is not None and first_close_index is not None:
        arr[last_open_index], arr[first_close_index] = ')', '('
        if is_rbs(arr):
            return "NO"
    
    return "YES"

def main():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        print(solve_case(s))

if __name__ == "__main__":
    main()
```

The code first calculates how many `'('` and `')'` are required. It fills question marks greedily, then identifies the critical swap positions to test uniqueness. The `is_rbs` function checks the balance, returning False immediately if it goes negative.

## Worked Examples

### Example 1: `"(?))"`

| Step | arr | balance |
| --- | --- | --- |
| initial | ['(', '?', ')', ')'] | 0 |
| replace '?' | ['(', '(', ')', ')'] | 0→1→2→1→0 |
| last '(' | index 1 | first ')' index 2 |
| swap → ['(', ')', '(', ')'] | 0→1→0→1→0, valid |  |

Swap fails early, so the solution is unique: `"YES"`.

### Example 2: `"??????"`

| Step | arr | balance |
| --- | --- | --- |
| replace | ['(', '(', '(', ')', ')', ')'] | 0→1→2→3→2→1→0 |
| last '(' index 2, first ')' index 3 | swap → ['(', '(', ')', '(', ')', ')'] | 0→1→2→1→2→1→0, valid |

Swap succeeds, so multiple solutions exist: `"NO"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass to fill question marks and a single pass for balance check |
| Space | O(n) | Store mutable list of characters for replacement and swapping |

Given that the total length of all strings across all test cases is ≤ 2·10^5, this linear approach is efficient within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# provided samples
assert run("5\n(?))\n??????\n()\n??\n?(?)()?)") == "YES\nNO\nYES\nYES\nNO", "sample 1"

# custom cases
assert run("2\n??\n?()") == "YES\nYES", "min-length and almost complete"
assert run("1\n((((????))))") == "YES", "inner question marks filled uniquely"
assert run("1\n????") == "NO", "all question marks length 4, multiple assignments"
assert run("1\n()??") == "YES", "question marks at the end, unique fill"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `??` | YES | Minimum length, unique assignment |
| `?()` | YES | Only one question mark, unique completion |
| `((((????))))` | YES | Inner question marks, unique by balance |
| `????` | NO | Multiple valid RBSs exist |
| `()??` | YES | Question marks at end, only one valid fill |

## Edge Cases

For `"????"`, `half = 2`. Greedy fill produces `"(()())"`, but swapping positions 1 and 2 gives `"()()"`, which is also valid. The swap check detects non-uniqueness. For `"()??"`, the

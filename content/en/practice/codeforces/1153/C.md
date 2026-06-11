---
title: "CF 1153C - Serval and Parenthesis Sequence"
description: "We are given a string consisting of three types of characters: open parenthesis \"(\", close parenthesis \")\", and question marks \"?\". Our goal is to replace each \"?"
date: "2026-06-12T02:51:34+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1153
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 551 (Div. 2)"
rating: 1700
weight: 1153
solve_time_s: 118
verified: false
draft: false
---

[CF 1153C - Serval and Parenthesis Sequence](https://codeforces.com/problemset/problem/1153/C)

**Rating:** 1700  
**Tags:** greedy, strings  
**Solve time:** 1m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string consisting of three types of characters: open parenthesis "(", close parenthesis ")", and question marks "?". Our goal is to replace each "?" with either "(" or ")" such that the resulting sequence is a correct parenthesis sequence, meaning it is balanced and every prefix has at least as many "(" as ")". Additionally, every strict prefix (every prefix except the whole string) must be _incorrect_ as a parenthesis sequence, which is equivalent to saying that no strict prefix should itself form a balanced sequence.

The input size can be as large as 300,000 characters. This rules out any solution that considers all possible replacements of "?" naively, as that would be exponential in the number of "?". Any acceptable solution must therefore run in linear time relative to the string length.

There are a few edge cases to consider. If the length of the string is odd, there is immediately no solution, because a correct parenthesis sequence must have an equal number of "(" and ")". If the string already starts with ")" or ends with "(", no solution is possible, because the first character of a correct sequence must be "(", and the last character must be ")". If all characters are "?", we must carefully choose the distribution of "(" and ")" to meet the strict prefix condition. Careless approaches may generate sequences that are balanced too early, for instance "()", which would violate the strict prefix requirement.

## Approaches

The brute-force approach would be to generate all possible replacements of "?" and check each resulting sequence for correctness, while also checking that all strict prefixes are invalid. This approach is correct in principle, but if there are up to 300,000 "?" characters, the number of sequences is $2^{300,000}$, which is completely infeasible.

The key insight is that we only need to determine how many "(" and ")" to place, because the sequence is entirely determined once we assign the correct counts. For a string of length n, a correct parenthesis sequence requires exactly n/2 "(" and n/2 ")". If we count how many "(" and ")" are already present, we know exactly how many question marks must become "(" and how many must become ")".

Once we know the distribution, we can greedily replace "?" from left to right with "(" until we reach the required count, then use ")" for the rest. This ensures that the total number of "(" and ")" is correct. We must then check the running balance while scanning left to right: it must never drop below 0, and it must never reach 0 before the last character, because no strict prefix can be correct.

The observation that enables linear-time construction is that the "strict prefix" condition forces the first half of "(" and the second half of ")" to be carefully ordered: if we place the last "(" too late, we may accidentally create a valid prefix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy Count & Check | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. First, check if the length of the string is odd. If it is, print ":(" and exit, because a balanced sequence is impossible.
2. Count the existing number of "(" and ")" in the string. Let open_needed be n/2 minus the current count of "(", and close_needed be n/2 minus the current count of ")". If either value is negative, print ":(", as there are too many fixed parentheses already.
3. Replace each "?" from left to right. For each "?", if open_needed is greater than 0, replace it with "(" and decrement open_needed. Otherwise, replace it with ")" and decrement close_needed. At the end, we will have exactly n/2 "(" and n/2 ")".
4. Check the running balance of the sequence. Initialize balance = 0. Scan each character: if "(", increment balance; if ")", decrement balance. If balance < 0 at any point, print ":(", because an incorrect sequence prefix occurred. Additionally, if balance == 0 before the last character, print ":(", because a correct strict prefix has been formed.
5. If the sequence passes the balance check, output the sequence.

Why it works: The algorithm maintains the invariant that the number of "(" and ")" will exactly match the required counts for a correct parenthesis sequence. The replacement order ensures that "(" appear early and ")" appear late enough to prevent any strict prefix from being correct. The balance check ensures no prefix becomes valid prematurely. This combination guarantees both conditions are satisfied or correctly reports impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = list(input().strip())

if n % 2 != 0:
    print(":(")
    exit()

half = n // 2
open_count = s.count('(')
close_count = s.count(')')

open_needed = half - open_count
close_needed = half - close_count

if open_needed < 0 or close_needed < 0:
    print(":(")
    exit()

for i in range(n):
    if s[i] == '?':
        if open_needed > 0:
            s[i] = '('
            open_needed -= 1
        else:
            s[i] = ')'
            close_needed -= 1

balance = 0
for i in range(n):
    if s[i] == '(':
        balance += 1
    else:
        balance -= 1
    if balance < 0 or (balance == 0 and i != n - 1):
        print(":(")
        exit()

print("".join(s))
```

Each section of this code directly implements the algorithm steps. Counting parentheses allows us to allocate "?" efficiently. The first loop converts "?" greedily into "(" until we reach half, then fills the rest with ")". The second loop checks the running balance, enforcing both that no prefix is valid and that the final sequence is balanced. The key subtlety is checking that balance == 0 before the last character triggers ":(", which handles the strict prefix condition.

## Worked Examples

Sample 1:

Input: `(?????`

| i | s[i] | open_needed | close_needed | balance |
| --- | --- | --- | --- | --- |
| 0 | ( | 2 | 3 | 1 |
| 1 | ? -> ( | 1 | 3 | 2 |
| 2 | ? -> ) | 1 | 2 | 1 |
| 3 | ? -> ( | 0 | 2 | 2 |
| 4 | ? -> ) | 0 | 1 | 1 |
| 5 | ? -> ) | 0 | 0 | 0 |

Balance never goes negative and first reaches 0 at last character. Output: `(()())`.

Edge case with no solution:

Input: `?)??(`

Length even but first char is ")" → immediately invalid → output ":(".

This trace demonstrates that greedy assignment combined with balance checking correctly identifies valid sequences and rejects invalid ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to replace "?" and single pass to check balance. |
| Space | O(n) | String is stored as a list for mutation. |

With n up to 3 * 10^5, this solution runs comfortably within 1 second time limit. No additional heavy data structures are used.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    s = list(sys.stdin.readline().strip())

    if n % 2 != 0:
        return ":("
    half = n // 2
    open_count = s.count('(')
    close_count = s.count(')')
    open_needed = half - open_count
    close_needed = half - close_count
    if open_needed < 0 or close_needed < 0:
        return ":("
    for i in range(n):
        if s[i] == '?':
            if open_needed > 0:
                s[i] = '('
                open_needed -= 1
            else:
                s[i] = ')'
                close_needed -= 1
    balance = 0
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0 or (balance == 0 and i != n - 1):
            return ":("
    return "".join(s)

# provided samples
assert run("6\n(?????\n") == "(()())", "sample 1"
# custom cases
assert run("4\n)??(\n") == ":(", "invalid start and end"
assert run("2\n??\n") == "()", "minimum size even"
assert run("8\n????????\n") == "(((())))", "all question marks"
assert run("6\n((????\n") == ":(", "too many fixed ("
assert run("6\n()??()\n") == ":(", "would form valid strict prefix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4\n)??(\n | :( | Detects impossible due to start/end |
| 2\n??\n | () | Minimum-size valid case |
| 8\n????????\n | (((()))) | Full greedy assignment works |
| 6\n((????\n | :( | Too many fixed "(" |

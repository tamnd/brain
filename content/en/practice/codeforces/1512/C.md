---
title: "CF 1512C - A-B Palindrome"
description: "We are given a string composed of characters '0', '1', and '?', along with two integers a and b representing the total number of '0's and '1's that the final string must contain. The task is to replace every '?"
date: "2026-06-10T18:51:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1512
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 713 (Div. 3)"
rating: 1200
weight: 1512
solve_time_s: 116
verified: true
draft: false
---

[CF 1512C - A-B Palindrome](https://codeforces.com/problemset/problem/1512/C)

**Rating:** 1200  
**Tags:** constructive algorithms, implementation, strings  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string composed of characters '0', '1', and '?', along with two integers `a` and `b` representing the total number of '0's and '1's that the final string must contain. The task is to replace every '?' with either '0' or '1' such that the string becomes a palindrome while exactly matching the counts `a` and `b`. A palindrome requires that the string reads the same forwards and backwards, so every character at position `i` must match the character at position `n-i-1`.

The problem combines two constraints simultaneously: maintaining the palindrome property and matching the exact counts of '0's and '1's. The string length can reach up to 200,000 over all test cases, and the number of test cases can be 10,000. This means our solution must run in linear time per string, since quadratic or brute-force approaches would involve too many operations.

Subtle edge cases exist when there are conflicting fixed characters (e.g., a '0' at index `i` and a '1' at index `n-i-1`) or when the remaining count of '0's or '1's cannot satisfy the '?' replacements. Another tricky case is a string of odd length with the middle character being '?'; the algorithm must ensure that the middle character can be assigned consistently with the remaining counts.

## Approaches

The brute-force approach would enumerate all possible replacements of '?' with '0' or '1', then check each candidate for the palindrome property and count correctness. This approach is correct in principle but becomes infeasible because each '?' doubles the number of possibilities, leading to exponential complexity in the number of '?'. For strings of length up to 2*10^5, this is impossible.

The key insight is that we do not need to try all combinations. The palindrome constraint lets us propagate known values across their mirrored positions, reducing the number of '?' to fill. Specifically, if `s[i]` is '?' but `s[n-i-1]` is '0', then we must replace `s[i]` with '0'. After this propagation, we can check if the counts `a` and `b` are still achievable. Then, for remaining pairs of '?', we can greedily assign either '0' or '1' in mirrored positions, using up the remaining counts. The middle character, if the string has odd length, can be assigned independently if it is '?', provided we still have the count available.

This approach is linear because each position is visited at most twice: once for propagation and once for filling remaining '?'. Conflicts and count insufficiencies are checked in constant time per pair.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the string to a list of characters for mutable operations. Initialize counters for remaining '0's and '1's using `a` and `b`, subtracting the counts of existing '0's and '1's in the string.
2. Propagate known characters to their mirrored positions. For each index `i` in the first half of the string, if `s[i]` is '?' and `s[n-i-1]` is not, replace `s[i]` with `s[n-i-1]` and decrement the appropriate counter. If both positions are fixed and unequal, output `-1` as a solution is impossible.
3. After propagation, check if any counter has gone negative. If so, output `-1` because we cannot satisfy the required counts.
4. Fill remaining pairs of '?' in the first half of the string. For each pair `(i, n-i-1)` that are both '?', assign '0' if at least 2 zeros remain, otherwise assign '1' if at least 2 ones remain. Update counters accordingly. If neither is possible, output `-1`.
5. If the string length is odd, handle the middle character separately. If it is '?', assign '0' if one zero remains, else '1' if one one remains. If no count is available, output `-1`.
6. After filling all positions, the counters for zeros and ones should be exactly zero. If not, output `-1`. Otherwise, join the list back into a string and output it.

Why it works: The algorithm maintains the invariant that after each propagation and filling step, the current partial string can still be completed into a palindrome satisfying the counts. Conflicts are detected immediately, preventing invalid solutions. Greedy assignment for remaining '?' works because any pair can be assigned independently once conflicts are resolved, and the total counts are tracked.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        s = list(input().strip())
        n = len(s)
        possible = True

        # Step 1: initial count deduction
        a -= s.count('0')
        b -= s.count('1')

        # Step 2: propagate known characters
        for i in range(n // 2):
            j = n - i - 1
            if s[i] == '?' and s[j] != '?':
                s[i] = s[j]
                if s[i] == '0': a -= 1
                else: b -= 1
            elif s[i] != '?' and s[j] == '?':
                s[j] = s[i]
                if s[j] == '0': a -= 1
                else: b -= 1
            elif s[i] != '?' and s[j] != '?' and s[i] != s[j]:
                possible = False
                break

        if a < 0 or b < 0:
            possible = False

        # Step 3: fill remaining '?'
        for i in range(n // 2):
            j = n - i - 1
            if s[i] == '?' and s[j] == '?':
                if a >= 2:
                    s[i] = s[j] = '0'
                    a -= 2
                elif b >= 2:
                    s[i] = s[j] = '1'
                    b -= 2
                else:
                    possible = False
                    break

        # Step 4: handle middle character if odd length
        if n % 2 == 1 and s[n // 2] == '?':
            if a > 0:
                s[n // 2] = '0'
                a -= 1
            elif b > 0:
                s[n // 2] = '1'
                b -= 1
            else:
                possible = False

        if possible and a == 0 and b == 0:
            print("".join(s))
        else:
            print(-1)

if __name__ == "__main__":
    solve()
```

The solution first accounts for the fixed characters to reduce the number of remaining zeros and ones. Then it propagates mirrored values to resolve '?' deterministically. Remaining pairs of '?' are filled greedily, which works because the palindrome symmetry allows us to assign both positions simultaneously. Finally, the middle character is treated separately if needed. Any conflict or count violation immediately results in `-1`.

## Worked Examples

**Sample Input 1:**

`4 4 01?????0`

| i | j | s before | Action | s after | a | b |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 7 | 0 & 0 | match | 0 & 0 | 3 | 4 |
| 1 | 6 | 1 & ? | propagate 1 | 1 & 1 | 3 | 3 |
| 2 | 5 | ? & ? | assign 0 | 0 & 0 | 1 | 3 |
| 3 | 4 | ? & ? | assign 1 | 1 & 1 | 1 | 1 |

Final string: `01011010`, counts match exactly.

**Sample Input 2:**

`2 2 01?0`

Propagating mirrored characters gives a conflict at positions 1 and 2 (1 vs '?'), but '?' is assigned to 1, giving `0110`, counts match. Works.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited at most twice: propagation and filling |
| Space | O(n) | String is converted to a list for mutable operations |

Given the sum of lengths over all test cases is 2*10^5, the solution fits well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("9\n4 4\n01?????0\n3 3\n??????\n1 0\n?\n2 2\n0101\n2 2\n01?0\n0 1\n0\n0 3\n1?1\n2 2\n?00?\n4 3\n??010?0\n") == "01011010\n-1\n0\n-1\n0110\n-1\n
```

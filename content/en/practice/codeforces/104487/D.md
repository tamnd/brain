---
title: "CF 104487D - Similarity"
description: "We are given several strings, all having the same fixed length. We are allowed to construct one new string of that same length. The goal is to choose this constructed string so that it matches the given strings as much as possible in total."
date: "2026-06-30T12:38:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104487
codeforces_index: "D"
codeforces_contest_name: "Tishreen + SVU CPC 2023"
rating: 0
weight: 104487
solve_time_s: 41
verified: true
draft: false
---

[CF 104487D - Similarity](https://codeforces.com/problemset/problem/104487/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several strings, all having the same fixed length. We are allowed to construct one new string of that same length. The goal is to choose this constructed string so that it matches the given strings as much as possible in total.

A match is counted position by position. For a fixed position, if our constructed string has the same character as a given string at that position, we gain one unit of similarity for that string. The final score is the sum of these matches over all strings and all positions.

Reframing this in a more structural way, each position in the final string contributes independently to the total score. At position i, we choose a single character, and that choice simultaneously affects how many of the n strings match at that position.

The constraints are small, with both the number of strings and their lengths bounded by 50. This immediately implies that even a cubic or quadratic per test case solution is easily fast enough. A full scan over all characters in all positions is at most 2500 cells per test case, and even with T up to 50, the total work is negligible.

There are no tricky edge cases involving ordering or dependencies between positions, since each position contributes independently. The only subtle issue that could trip a naive approach is trying to build the string greedily without realizing that each position is solved independently and optimally by local frequency maximization.

For example, if at a position we choose a character that appears 2 times instead of one that appears 3 times, that decision cannot be compensated elsewhere, because contributions do not transfer across positions. Another pitfall is attempting to construct the actual string unnecessarily when only the score is required, which can lead to avoidable complexity or errors.

## Approaches

A brute-force idea is to try every possible string of length m over the alphabet implied by the input. For each candidate string, compute its similarity against all n given strings by comparing all m positions. The cost of evaluating one candidate is O(nm), and the number of candidates is exponential in m. Even restricting to characters appearing in the input, the branching factor is still large, making this approach infeasible beyond tiny m.

The key observation is that there is no interaction between positions. The contribution of position i depends only on which character we choose at position i, and is independent of all other positions. This decouples the problem into m separate subproblems, one per column.

For a fixed position i, we only need to know how many strings contain each character at that position. If a character c appears freq[c] times among the n strings at position i, then choosing c gives exactly freq[c] contribution from that position. The optimal choice is therefore simply the most frequent character in that column.

So instead of searching over full strings, we compute frequencies per column and sum the maximum frequency.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | Σ | ^m · n m) |
| Optimal | O(n m) | O( | Σ |

## Algorithm Walkthrough

We process each test case independently.

1. Read n and m, then read all strings.
2. For each position i from 0 to m−1, compute a frequency map of characters appearing in that column across all n strings.
3. For each column, find the maximum frequency among all characters appearing there.
4. Add this maximum to the answer.
5. Output the accumulated sum for the test case.

The key design choice is treating each column independently. This is valid because selecting a character at position i affects only matches at position i and does not influence any other position.

### Why it works

The total score can be written as a sum over positions, where each term depends only on the chosen character at that position. Since there is no coupling between positions, optimizing each term independently yields a globally optimal solution. For each column, any deviation from the most frequent character strictly decreases the contribution of that column without improving any other column, so no tradeoff exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        arr = [input().strip() for _ in range(n)]
        
        ans = 0
        
        for j in range(m):
            freq = {}
            for i in range(n):
                c = arr[i][j]
                freq[c] = freq.get(c, 0) + 1
            ans += max(freq.values())
        
        out.append(str(ans))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution iterates column by column, building a frequency dictionary for each column. The inner loop over n strings is unavoidable since we must inspect each character at least once. The dictionary is reset per column, ensuring no cross-column contamination.

A common mistake is trying to maintain a global frequency across the entire matrix, which would mix unrelated positions and destroy correctness. Another subtle issue is forgetting to reset the frequency map per column, which would incorrectly accumulate counts across columns.

## Worked Examples

### Example 1

Input:

```
3 3
abc
ebd
fbd
```

We compute column-wise frequencies.

| Column | Frequencies | Max char | Contribution |
| --- | --- | --- | --- |
| 0 | a:1, e:1, f:1 | any (1) | 1 |
| 1 | b:3 | b | 3 |
| 2 | c:1, d:2 | d | 2 |

Total = 1 + 3 + 2 = 6.

This shows that even though the optimal constructed string is "ebd", we never need to explicitly construct it; only column counts matter.

### Example 2

Input:

```
2 3
abc
aff
```

| Column | Frequencies | Max char | Contribution |
| --- | --- | --- | --- |
| 0 | a:2 | a | 2 |
| 1 | b:1, f:1 | b or f | 1 |
| 2 | c:1, f:1 | c or f | 1 |

Total = 2 + 1 + 1 = 4.

This example demonstrates that ties in frequency do not affect the answer, since only the count matters, not which character is chosen among maxima.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nmT) | Each test case scans all n strings over m columns |
| Space | O(1) per column | Only a small frequency map is stored at a time |

With n, m ≤ 50 and T ≤ 50, the total operations are at most 125000 character inspections, which is trivially within limits for 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return "\n".join(solve() or [])

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        arr = [input().strip() for _ in range(n)]
        ans = 0
        for j in range(m):
            freq = {}
            for i in range(n):
                c = arr[i][j]
                freq[c] = freq.get(c, 0) + 1
            ans += max(freq.values())
        out.append(str(ans))
    return out

# provided sample
assert run("""1
3 3
abc
ebd
fbd
""") == "6"

# all equal strings
assert run("""1
3 3
aaa
aaa
aaa
""") == "9"

# binary tie case
assert run("""1
2 4
abab
baba
""") == "4"

# single string
assert run("""1
1 5
abcde
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal strings | 9 | full overlap maximum |
| alternating binary | 4 | tie handling per column |
| single string | 5 | base case correctness |

## Edge Cases

A minimal case with one string shows that every column contributes exactly 1, since that string defines the only possible match. The algorithm handles this because each column frequency map has a single entry equal to n = 1, so the maximum is always 1.

A tie-heavy column, such as two strings with different characters, still produces a correct result because max frequency remains 1. The algorithm does not depend on which character is chosen, only on how many times it appears.

A fully uniform matrix produces maximum score n × m. The frequency map per column always has a single dominant character with count n, so summing across columns yields the expected maximum without special casing.

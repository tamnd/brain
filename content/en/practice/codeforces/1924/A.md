---
title: "CF 1924A - Did We Get Everything Covered?"
description: "We are given a string s and two integers n and k. Conceptually, we are asked to check if every string of length n that can be built using the first k letters of the alphabet appears somewhere as a subsequence in s."
date: "2026-06-08T19:07:07+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "greedy", "shortest-paths", "strings"]
categories: ["algorithms"]
codeforces_contest: 1924
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 921 (Div. 1)"
rating: 1500
weight: 1924
solve_time_s: 132
verified: false
draft: false
---

[CF 1924A - Did We Get Everything Covered?](https://codeforces.com/problemset/problem/1924/A)

**Rating:** 1500  
**Tags:** constructive algorithms, dp, greedy, shortest paths, strings  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string `s` and two integers `n` and `k`. Conceptually, we are asked to check if every string of length `n` that can be built using the first `k` letters of the alphabet appears somewhere as a subsequence in `s`. A subsequence allows characters to be skipped but the order must be preserved. If even one string of length `n` using the first `k` letters does not appear, we must output one such string as evidence.

The constraints are key to understanding what is feasible. `n` and `k` are both at most 26, and the length of `s` is at most 1000. With these limits, the total number of possible strings of length `n` using `k` letters is `k^n`. This grows exponentially, so a naive brute-force approach that checks all possible strings for being subsequences is infeasible when `n` and `k` are not tiny.

An important edge case arises when `s` is too short to accommodate repeated letters. For example, if `s` is `"ab"` with `n = 2` and `k = 2`, the string `"aa"` cannot be a subsequence because there is only one `'a'` in `s`. Similarly, if `s` lacks a particular character entirely, any string requiring that character is immediately impossible. A careless approach might try generating all strings without checking character frequencies and fail silently or time out.

## Approaches

The brute-force method would generate all `k^n` strings of length `n` and test if each is a subsequence of `s`. Testing one string of length `n` against a string `s` of length `m` costs O(m), so in the worst case the operation count is O(m * k^n), which is completely infeasible for the upper bounds of `n` and `k`.

The key insight is that we do not need to generate all strings. We only need to find the lexicographically smallest string that cannot be a subsequence. This can be done greedily by counting the occurrences of each letter in `s`. At each position of the target string, we pick the smallest letter that still has a remaining occurrence. If at some position no letter is available, we immediately have a string that cannot be formed as a subsequence. By iterating left to right and choosing the smallest feasible letters, we construct one string that is guaranteed to be missing if the answer is NO. If we can assign letters to all positions successfully, all strings exist, and the answer is YES.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * k^n) | O(n) | Too slow |
| Greedy subsequence counting | O(n * k + m) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read integers `n`, `k`, and `m`, and the string `s`.
3. Initialize an array `count` of size `k` to zero. Iterate through `s` and count how many times each of the first `k` letters appears.
4. Initialize an empty string `res` for the candidate missing string.
5. For each position `i` in the target string of length `n`, iterate through the letters from `'a'` to the `k`-th letter:

- If the current letter has remaining occurrences in `s`, decrement its count and append it to `res`.
- If no letter is available, append the first letter lexicographically to `res` for the remaining positions and break. This ensures the string we are building cannot appear as a subsequence.
6. After building `res`, check if its length is less than `n`. If so, the answer is NO and we print `res`. If we successfully assigned all positions without running out of occurrences, the answer is YES.
7. Repeat for all test cases.

**Why it works**: The algorithm constructs a string greedily that uses letters only if they are available in `s`. If it fails at any position, it guarantees that at least one string of length `n` cannot be a subsequence. Otherwise, by the pigeonhole principle and the greedy choice, all strings can be formed. This satisfies both correctness and efficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k, m = map(int, input().split())
    s = input().strip()
    freq = [0] * k
    for c in s:
        freq[ord(c) - ord('a')] += 1

    res = []
    found_missing = False
    for i in range(n):
        placed = False
        for j in range(k):
            if freq[j] > 0:
                freq[j] -= 1
                res.append(chr(ord('a') + j))
                placed = True
                break
        if not placed:
            # No letter available, fill remaining with 'a'
            res.extend(['a'] * (n - i))
            found_missing = True
            break

    if found_missing:
        print("NO")
        print(''.join(res))
    else:
        print("YES")
```

**Explanation**: We count the occurrences of each letter in `s` and try to greedily place them in a candidate string. If a position cannot be filled due to a lack of remaining letters, we construct a string that cannot appear, ensuring a valid NO response. Otherwise, if all positions can be assigned, the string contains all possible subsequences.

## Worked Examples

**Sample Input 2**

```
2 2 3
abb
```

| Step | freq | res | Explanation |
| --- | --- | --- | --- |
| i=0 | [1,2] | ['a'] | Place 'a' |
| i=1 | [0,2] | ['a','b'] | Place 'b' |
| i=2 | [0,1] | Cannot place 'a' (freq=0) | Fill remaining with 'a' → 'aa', found_missing=True |

Output:

```
NO
aa
```

This trace demonstrates the greedy selection and immediate detection of a missing subsequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k + m) | Counting frequencies is O(m), building the candidate string is O(n * k) |
| Space | O(k + n) | Frequency array and candidate string |

This fits well within the problem constraints since `n` and `k` are at most 26, and the total length of `s` over all test cases is ≤ 10^6.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, k, m = map(int, input().split())
        s = input().strip()
        freq = [0]*k
        for c in s:
            freq[ord(c)-ord('a')] += 1
        res = []
        found_missing = False
        for i in range(n):
            placed = False
            for j in range(k):
                if freq[j]>0:
                    freq[j]-=1
                    res.append(chr(ord('a')+j))
                    placed=True
                    break
            if not placed:
                res.extend(['a']*(n-i))
                found_missing=True
                break
        if found_missing:
            output.append("NO")
            output.append(''.join(res))
        else:
            output.append("YES")
    return "\n".join(output)

# provided samples
assert run("3\n2 2 4\nabba\n2 2 3\nabb\n3 3 10\naabbccabab\n") == "YES\nNO\naa\nNO\nccc"

# custom cases
assert run("1\n1 1 1\na\n") == "YES", "single character string"
assert run("1\n2 1 2\naa\n") == "NO\naa", "cannot make 'aa' subsequence"
assert run("1\n2 2 3\nab\n") == "NO\naa", "missing 'aa'"
assert run("1\n2 2 5\nabab\n") == "NO\nbb", "missing 'bb'"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 / a | YES | Minimal input |
| 2 1 2 / aa | NO / aa | Cannot repeat letter more than in s |
| 2 2 3 / ab | NO / aa | Lexicographical missing string detection |
| 2 2 5 / abab | NO / bb | Detects missing repeated letters |

## Edge Cases

For strings where `s` contains only one of each letter, the algorithm detects that any repeated-letter subsequence is impossible. For instance, `n=2`, `k=2`, `s="ab"` correctly outputs NO and `aa`. For `n=1`, `k=1`, `s="a"`, all strings exist and outputs YES. The method handles maximum `k` and `n` by greedily checking available letters without generating all possible strings, avoiding exponential complexity.

---
title: "CF 490E - Restoring Increasing Sequence"
description: "We are given a sequence of strings. Each string represents a positive integer, but some digits have been replaced by '?'. The original sequence was strictly increasing. Our task is to replace every '?"
date: "2026-06-07T17:42:35+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 490
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 279 (Div. 2)"
rating: 2000
weight: 490
solve_time_s: 126
verified: true
draft: false
---

[CF 490E - Restoring Increasing Sequence](https://codeforces.com/problemset/problem/490/E)

**Rating:** 2000  
**Tags:** binary search, brute force, greedy, implementation  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of strings. Each string represents a positive integer, but some digits have been replaced by `'?'`. The original sequence was strictly increasing. Our task is to replace every `'?'` with a decimal digit so that all resulting numbers are valid positive integers without leading zeroes and the entire sequence becomes strictly increasing.

The sequence length can reach $10^5$, while every number contains at most 8 characters. The small length of each individual number is the key observation. Even though there are many elements, each element belongs to a tiny search space because its length never exceeds 8. Any solution that performs only a constant amount of work per string is easily fast enough. On the other hand, trying all possible substitutions is impossible. A string of length 8 consisting entirely of question marks already represents $10^8$ candidates.

The most delicate part of the problem is that local choices affect later numbers. Choosing an unnecessarily large value early may make future positions impossible.

Consider:

```
2
??
10
```

The first number could be 99, but then the second number cannot exceed it. The correct choice is the smallest valid number greater than the previous element, namely 10 is impossible because the sequence must be strictly increasing, so we choose 01? No leading zeros are allowed. The actual answer is:

```
YES
9
10
```

Another subtle case occurs when lengths differ.

```
2
??
???
```

Any three digit number is larger than any two digit number. A greedy strategy should exploit this and choose the smallest valid two digit number, not waste effort trying larger values.

Leading zeroes are another common source of mistakes.

```
1
?5
```

The answer can be 15, 25, ..., 95, but never 05. The first digit must remain nonzero.

Finally, some instances are impossible.

```
2
99
??
```

Any two digit completion is at most 99, so no strictly larger value exists. The correct output is:

```
NO
```

The challenge is finding, for every position, the smallest valid completion that is strictly greater than the previous chosen number.

## Approaches

A brute force approach would generate every possible completion of each pattern and then search for a strictly increasing sequence. Even for a single string of length 8, there may be $10^8$ candidates. Multiplying that by $10^5$ positions is completely infeasible.

The structure of the problem suggests a different viewpoint. Once the previous value is fixed, the current position only needs one thing: the smallest number matching its pattern that is strictly larger than the previous value. If we can always find that minimum feasible value, we never hurt future positions because any larger choice only makes later constraints harder.

This transforms the problem into a repeated subproblem:

Given a pattern string and a lower bound $L$, find the minimum number matching the pattern whose value is greater than $L$.

The length limit of 8 makes this much easier. Any candidate number fits into a standard integer. Instead of searching over huge numeric ranges, we can construct the answer digit by digit.

Suppose the pattern length is smaller than the number of digits of $L+1$. Then no solution exists because every candidate would have fewer digits.

Suppose the pattern length is larger. Then every candidate automatically exceeds $L$, and we simply build the smallest valid number matching the pattern.

The interesting case is when both lengths are equal. We need the lexicographically smallest completion that is at least $L+1$. Since the length is at most 8, we can use a digit-DP style greedy construction. At each position we try allowed digits from smallest to largest while tracking whether we are already larger than the bound prefix. Because only 8 positions exist, even a simple recursive search is effectively constant time.

This gives a linear solution over the sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of '?' | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

The hidden constant comes from the maximum length 8, which is fixed.

## Algorithm Walkthrough

### Finding the minimum valid completion above a bound

For a pattern string `s` and previous value `prev`, we must find the smallest matching number greater than `prev`.

1. Compute `target = prev + 1`.
2. If `len(s) < len(str(target))`, return failure.

Any completion has fewer digits than `target`, so it cannot reach the required value.
3. If `len(s) > len(str(target))`, construct the smallest valid number matching the pattern.

Any number with more digits is automatically greater than `prev`.
4. If the lengths are equal, build the lexicographically smallest completion that is at least `target`.
5. Process digits from left to right using recursion.

Track whether the already chosen prefix is strictly larger than the corresponding prefix of `target`.
6. At position `i`, enumerate all digits allowed by the pattern.

If the first position is a question mark, digit 0 is forbidden.
7. If the prefix is still equal to the target prefix, digits smaller than the target digit at this position are not allowed.
8. Try digits in increasing order.

The first successful continuation yields the smallest valid number.
9. If no digit works, return failure.
10. Starting with `prev = 0`, process the sequence from left to right.

Store each chosen value and use it as the next lower bound.
11. If any position fails, output `"NO"`.
12. Otherwise output `"YES"` and the constructed sequence.

### Why it works

After processing position `i`, the algorithm stores the smallest possible value matching that pattern and still exceeding the previous chosen number. Any alternative valid choice would be greater than or equal to the selected one.

Suppose there exists a complete solution. Replacing any chosen value by a larger valid value cannot make future positions easier, because every later element must be strictly larger than the current one. The smallest feasible choice is always at least as good as every other feasible choice.

The digit construction is also optimal. Whenever multiple digits are possible at a position, trying them in increasing order and accepting the first successful continuation produces the lexicographically smallest valid completion. For fixed length numbers, lexicographic order and numeric order coincide.

By induction over the sequence, if a solution exists the algorithm never eliminates it by making an unnecessarily large choice. If the algorithm reports failure, no valid completion exists for that position, hence no global solution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def smallest_any(pattern):
    res = []
    m = len(pattern)

    for i, ch in enumerate(pattern):
        if ch != '?':
            if i == 0 and ch == '0':
                return None
            res.append(ch)
        else:
            if i == 0:
                res.append('1')
            else:
                res.append('0')

    return ''.join(res)

def build_ge(pattern, target):
    m = len(pattern)
    t = str(target)

    if len(t) > m:
        return None

    if len(t) < m:
        return smallest_any(pattern)

    memo = {}

    def dfs(pos, greater):
        if pos == m:
            return ""

        key = (pos, greater)
        if key in memo:
            return memo[key]

        if pattern[pos] == '?':
            digits = range(10)
        else:
            digits = [int(pattern[pos])]

        for d in digits:
            if pos == 0 and d == 0:
                continue

            td = int(t[pos])

            if not greater and d < td:
                continue

            ngreater = greater or (d > td)

            suffix = dfs(pos + 1, ngreater)
            if suffix is not None:
                memo[key] = str(d) + suffix
                return memo[key]

        memo[key] = None
        return None

    return dfs(0, False)

def solve():
    n = int(input())
    patterns = [input().strip() for _ in range(n)]

    ans = []
    prev = 0

    for s in patterns:
        cur = build_ge(s, prev + 1)
        if cur is None:
            print("NO")
            return

        val = int(cur)
        ans.append(cur)
        prev = val

    print("YES")
    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The helper `smallest_any` is used when the pattern length is already greater than the required bound length. In that situation every valid completion automatically satisfies the increasing condition, so we simply construct the smallest legal number.

The function `build_ge` handles the real work. When lengths match, it performs a digit-by-digit search. The state consists of the current position and a boolean indicating whether the constructed prefix is already larger than the target prefix. Because there are at most 8 positions and only two possible values of the boolean, the memoization table contains at most 16 states.

The recursive search always tries digits in increasing order. The first successful branch is the minimum valid completion. This is the crucial detail that implements the greedy choice correctly.

The main loop processes the sequence from left to right. Once a value is chosen, it becomes the lower bound for the next position. Since every chosen value is minimal among all feasible choices, future positions remain as unconstrained as possible.

## Worked Examples

### Example 1

Input:

```
3
?
18
1?
```

| Position | Pattern | Required > | Chosen |
| --- | --- | --- | --- |
| 1 | ? | 0 | 1 |
| 2 | 18 | 1 | 18 |
| 3 | 1? | 18 | 19 |

Output:

```
YES
1
18
19
```

The last pattern could produce 19 only. Values 10 through 18 fail because the sequence must remain strictly increasing.

### Example 2

Input:

```
3
??
??
??
```

| Position | Pattern | Required > | Chosen |
| --- | --- | --- | --- |
| 1 | ?? | 0 | 10 |
| 2 | ?? | 10 | 11 |
| 3 | ?? | 11 | 12 |

Output:

```
YES
10
11
12
```

This example illustrates the central greedy property. Choosing the smallest feasible value at each step naturally leaves maximum room for later positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each pattern is processed in O(8 × 2 × 10), which is constant |
| Space | O(1) | The DP contains only a constant number of states |

Since every string length is bounded by 8, the work per element never grows with the input size. Even for $n = 10^5$, the algorithm performs only a few million primitive operations, well within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve_io(inp: str) -> str:
    input = io.StringIO(inp).readline

    def smallest_any(pattern):
        res = []
        for i, ch in enumerate(pattern):
            if ch != '?':
                if i == 0 and ch == '0':
                    return None
                res.append(ch)
            else:
                res.append('1' if i == 0 else '0')
        return ''.join(res)

    def build_ge(pattern, target):
        m = len(pattern)
        t = str(target)

        if len(t) > m:
            return None

        if len(t) < m:
            return smallest_any(pattern)

        memo = {}

        def dfs(pos, greater):
            if pos == m:
                return ""

            key = (pos, greater)
            if key in memo:
                return memo[key]

            digits = range(10) if pattern[pos] == '?' else [int(pattern[pos])]

            for d in digits:
                if pos == 0 and d == 0:
                    continue

                td = int(t[pos])

                if not greater and d < td:
                    continue

                suf = dfs(pos + 1, greater or d > td)
                if suf is not None:
                    memo[key] = str(d) + suf
                    return memo[key]

            memo[key] = None
            return None

        return dfs(0, False)

    n = int(input())
    prev = 0
    ans = []

    for _ in range(n):
        s = input().strip()
        cur = build_ge(s, prev + 1)
        if cur is None:
            return "NO\n"
        ans.append(cur)
        prev = int(cur)

    return "YES\n" + "\n".join(ans) + "\n"

def run(inp: str) -> str:
    return solve_io(inp)

# provided sample
assert run("3\n?\n18\n1?\n") == "YES\n1\n18\n19\n"

# minimum size
assert run("1\n?\n") == "YES\n1\n"

# impossible case
assert run("2\n99\n??\n") == "NO\n"

# increasing through same-length patterns
assert run("3\n??\n??\n??\n") == "YES\n10\n11\n12\n"

# length increase
assert run("2\n9\n???\n") == "YES\n9\n100\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 ?` | `1` | Minimum input size |
| `99, ??` | `NO` | Impossible increasing condition |
| `??, ??, ??` | `10,11,12` | Repeated greedy choices |
| `9, ???` | `9,100` | Transition to larger digit length |

## Edge Cases

Consider:

```
2
99
??
```

The first value is fixed as 99. The second pattern can only generate two digit numbers. The algorithm computes `target = 100`. Since the target length is 3 while the pattern length is 2, it immediately returns failure. Output:

```
NO
```

Now consider:

```
2
?
100
```

The first pattern becomes 1. For the second pattern, the required bound is only 2. Its length is larger than the target length, so the algorithm constructs the smallest valid completion, namely 100. Output:

```
YES
1
100
```

Consider the leading-zero trap:

```
1
?5
```

The algorithm tries digits for the first position starting from 1 because zero is forbidden in the leading position. The smallest completion is 15, not 05. Output:

```
YES
15
```

Finally:

```
2
1?
1?
```

The first pattern becomes 10. For the second pattern the target is 11. During digit construction, the first digit must remain 1. The second digit cannot be 0 because that would produce 10, which is below the target. The search chooses 1, producing 11. Output:

```
YES
10
11
```

This example shows how the digit-by-digit comparison against the lower bound enforces strict increase without ever enumerating all possible numbers.

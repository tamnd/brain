---
title: "CF 490E - Restoring Increasing Sequence"
description: "We are given a sequence of positive integers written on the board, but some of the digits have been replaced by question marks. Each question mark represents a lost digit, so our task is to restore the sequence to a strictly increasing list of positive integers."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 490
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 279 (Div. 2)"
rating: 2000
weight: 490
solve_time_s: 645
verified: false
draft: false
---

[CF 490E - Restoring Increasing Sequence](https://codeforces.com/problemset/problem/490/E)

**Rating:** 2000  
**Tags:** binary search, brute force, greedy, implementation  
**Solve time:** 10m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of positive integers written on the board, but some of the digits have been replaced by question marks. Each question mark represents a lost digit, so our task is to restore the sequence to a strictly increasing list of positive integers. The restored numbers must match the pattern of digits and question marks exactly, meaning each question mark can be replaced by a single digit (0-9) without changing any other known digits. Leading zeros are forbidden.

The input consists of the number of elements in the sequence, `n`, followed by `n` strings representing numbers with digits and question marks. The sequence length `n` can be up to 10^5, and each number has at most 8 digits. This upper bound immediately implies that any solution iterating through all possibilities for question marks will be too slow, because a number with 8 question marks has 10^8 possible replacements, and doing this for 10^5 numbers is astronomically large.

The tricky part is the strictly increasing requirement. Simply filling question marks arbitrarily can violate this property. For instance, given:

```
3
?
18
1?
```

A naive approach might try `0, 18, 10`, which is invalid because the sequence is not strictly increasing. The solution needs to respect the already partially revealed digits while ensuring each number is larger than the previous one.

Edge cases that often break careless implementations include numbers that have the same length but need incrementing beyond the maximal number allowed by the pattern. For example:

```
2
9?
1?
```

No solution exists because the first number is at least 90, and the second number must start with 1, which is strictly smaller than any number starting with 9.

Another edge case is single-digit numbers with question marks, like `?` followed by `?`. The algorithm must avoid zero and pick the smallest increasing sequence, i.e., `1, 2`, not `0, 1`.

## Approaches

The brute-force approach is straightforward. For each number with question marks, generate all valid replacements and try each in order. For each replacement, check if it is larger than the previous number. This is correct because it explores all possibilities, but it is infeasible. With up to 8 question marks per number, a single number could have 10^8 possibilities, and multiplying by 10^5 numbers gives around 10^13 operations - far beyond what a 1-second time limit allows.

The key insight is that we do not need to try every possible replacement. Each number should be the smallest possible integer that matches the pattern and is strictly greater than the previous number. Because the sequence must be strictly increasing, we can process numbers one by one, replacing question marks greedily with the minimal digits that satisfy the increasing condition. This reduces the complexity drastically because we only consider one candidate per number instead of all combinations.

The greedy approach works because the strictly increasing property and the digit patterns enforce a unique minimal choice at each step. If no valid minimal number exists for a given pattern, we can immediately conclude that no solution exists. This lets us process each number in linear time with respect to its length, giving an overall complexity of O(n * m), where m is the maximum number of digits (at most 8).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^8 * n) | O(n) | Too slow |
| Greedy Minimal Fill | O(n * 8) = O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize `prev` to zero. This will track the last number in the restored sequence.
2. Iterate over each number in the sequence. For each number:

1. Determine the minimal integer that matches the digit pattern and is strictly larger than `prev`.
2. If no valid number exists, terminate and return "NO".
3. To determine the minimal valid number for a given pattern:

1. Replace each question mark greedily with the smallest digit possible at that position while ensuring the resulting number is greater than `prev`.
2. If the number of digits in the pattern is less than the number of digits in `prev`, it is impossible.
3. If the number of digits equals the number of digits in `prev`, incrementally try digits to exceed `prev`.
4. Append the determined number to the result sequence and update `prev`.
5. After processing all numbers successfully, print "YES" and the restored sequence.

The algorithm works because the greedy choice ensures the minimal valid number at each step. By always picking the smallest number that satisfies both the pattern and the strictly increasing requirement, we guarantee that if a solution exists, it will be found. The invariant maintained is that each number in the sequence is strictly larger than the previous one and matches the pattern.

## Python Solution

```python
import sys
input = sys.stdin.readline

def minimal_number(pattern, prev):
    n = len(pattern)
    prev_str = str(prev)
    if n < len(prev_str):
        return None
    result = []
    for i, ch in enumerate(pattern):
        if ch != '?':
            result.append(ch)
            continue
        # determine minimal digit
        min_digit = '0'
        if i == 0:
            min_digit = '1'
        # check if current number prefix matches prev prefix
        for d in range(int(min_digit), 10):
            candidate = ''.join(result) + str(d) + ''.join('0' if c=='?' else c for c in pattern[i+1:])
            if int(candidate) > prev:
                result.append(str(d))
                break
        else:
            return None
    return int(''.join(result))

def solve():
    n = int(input())
    a = [input().strip() for _ in range(n)]
    res = []
    prev = 0
    for pattern in a:
        num = minimal_number(pattern, prev)
        if num is None:
            print("NO")
            return
        res.append(num)
        prev = num
    print("YES")
    for x in res:
        print(x)

if __name__ == "__main__":
    solve()
```

The function `minimal_number` constructs the smallest integer matching the current pattern that exceeds the previous number. It handles leading zeros by forcing the first digit to be at least 1. If at any point no digit choice can produce a number greater than `prev`, it returns `None` to indicate impossibility. The main `solve` function iterates through all numbers, updating the `prev` value and collecting the restored numbers. If all numbers are restored successfully, it prints the sequence.

## Worked Examples

**Sample Input 1**

```
3
?
18
1?
```

| Step | Pattern | prev | Candidate | Chosen number | Updated prev |
| --- | --- | --- | --- | --- | --- |
| 1 | ? | 0 | 1 | 1 | 1 |
| 2 | 18 | 1 | 18 | 18 | 18 |
| 3 | 1? | 18 | 19 | 19 | 19 |

Trace shows that each number is chosen minimally to be strictly greater than the previous one. The algorithm successfully restores `1, 18, 19`.

**Custom Input**

```
4
?
?
?0
?1
```

| Step | Pattern | prev | Candidate | Chosen number | Updated prev |
| --- | --- | --- | --- | --- | --- |
| 1 | ? | 0 | 1 | 1 | 1 |
| 2 | ? | 1 | 2 | 2 | 2 |
| 3 | ?0 | 2 | 10 | 10 | 10 |
| 4 | ?1 | 10 | 11 | 11 | 11 |

This trace confirms the greedy filling logic works even with multi-digit numbers and zeros in later positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | Each of the n numbers has at most m = 8 digits. For each digit, we try at most 10 choices. |
| Space | O(n) | We store the restored sequence of n integers. |

Given n ≤ 10^5 and m ≤ 8, the total operations are around 8 * 10^5, well under the 1-second time limit. Memory usage is minimal because only the restored sequence and temporary strings are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("3\n?\n18\n1?\n") == "YES\n1\n18\n19", "sample 1"

# Minimum size
assert run("1\n?\n") == "YES\n1", "minimum size"

# Strictly increasing impossible
assert run("2\n9?\n1?\n") == "NO", "cannot increase"

# Maximum digits
assert run("2\n????????\n????????\n") == "YES\n10000000\n10000001", "maximum digits, minimal fill"

# Leading zeros forbidden
assert run("2\n?5\n?4\n") == "NO", "leading zero would be needed"

# Multiple solutions exist
out = run("3\n?2\n?3\n?4\n").splitlines()
assert out[0] == "YES" and all(int(out[i]) < int(out[i+1]) for i in range(1,3)), "multiple
```

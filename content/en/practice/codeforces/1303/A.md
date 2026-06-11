---
title: "CF 1303A - Erasing Zeroes"
description: "We are given a binary string, a sequence of 0's and 1's, and the goal is to manipulate it so that all the 1's appear in one contiguous block. The only allowed operation is to remove some 0's."
date: "2026-06-11T18:06:01+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1303
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 82 (Rated for Div. 2)"
rating: 800
weight: 1303
solve_time_s: 109
verified: true
draft: false
---

[CF 1303A - Erasing Zeroes](https://codeforces.com/problemset/problem/1303/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string, a sequence of 0's and 1's, and the goal is to manipulate it so that all the 1's appear in one contiguous block. The only allowed operation is to remove some 0's. We need to compute the minimum number of 0's that must be removed for this condition to hold.

The input consists of multiple test cases, each with a string of length at most 100. This means we can afford algorithms that are quadratic in the string length if necessary, but linear-time solutions are obviously cleaner and simpler. Because strings can contain only 0's and 1's, we do not have to handle any other characters.

A non-obvious edge case arises when there are no 1's in the string, such as "0" or "0000". In these cases, there are no gaps between 1's to eliminate, so the answer is 0. Similarly, if all characters are 1, no removals are necessary. Another subtle case occurs when there are leading or trailing 0's, like "0011100", where removing the middle 0's is required, but leading and trailing 0's do not matter. A naive solution might incorrectly count all 0's or fail to correctly identify the subsegment of 1's.

## Approaches

The brute-force approach would iterate over every possible contiguous segment of the string and count how many 0's are inside that segment. For each segment that starts and ends with 1, we would compute the number of 0's between these 1's, and then take the minimum over all segments. This approach works because it explicitly simulates removing 0's to make 1's contiguous, but it requires checking O(n^2) segments, and for the maximum string length of 100, this is around 10,000 operations per test case. It is feasible but unnecessarily complex.

The key observation that leads to an optimal solution is that the only 0's that matter are those strictly between the first and last occurrence of 1. Any 0 before the first 1 or after the last 1 cannot disrupt the contiguous block of 1's and therefore do not need removal. Once we know the positions of the first and last 1, we can iterate over that substring and count the 0's. That count is exactly the minimum number of 0's to erase. This observation reduces the problem to a single linear scan per test case, which is simpler and fast enough given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Accepted but unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the binary string.
2. Find the index of the first occurrence of '1'. If there is no '1', immediately return 0 because no removals are needed.
3. Find the index of the last occurrence of '1'.
4. Iterate over the substring from the first '1' to the last '1'. Count the number of '0's in this range.
5. Output this count. This represents the minimum number of 0's to erase to make all 1's contiguous.

Why it works: The invariant is that any 0 outside the first-to-last-1 range is irrelevant. Counting only the 0's within this range ensures that after removing them, the 1's form a single uninterrupted segment. No other configuration can yield fewer removals because any 0 inside the range must be removed to merge separated 1's.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    if '1' not in s:
        print(0)
        continue
    first = s.index('1')
    last = s.rindex('1')
    count = s[first:last+1].count('0')
    print(count)
```

The solution first handles the trivial case where there are no 1's. It then identifies the substring that contains all the 1's and counts the internal 0's. Using `index` and `rindex` ensures the bounds are correctly identified, and slicing the string from first to last guarantees only the relevant portion is scanned. Off-by-one errors are avoided by including `last+1` in the slice, which is the standard Python convention for inclusive end in ranges.

## Worked Examples

### Sample Input 1

```
010011
```

| Variable | Value |
| --- | --- |
| first | 1 |
| last | 5 |
| s[first:last+1] | "10011" |
| count of '0' | 2 |

The algorithm identifies that 0's at positions 2 and 3 must be removed. The output is 2, which matches the expected result.

### Sample Input 2

```
0
```

| Variable | Value |
| --- | --- |
| first | not found |
| last | not found |
| output | 0 |

No 1's exist, so no removals are necessary. The algorithm correctly returns 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Finding first and last 1, slicing, and counting zeros are all linear in string length |
| Space | O(1) extra | Only indices and a counter are stored; slicing produces a temporary substring but does not scale with input size significantly |

Given maximum `t = 100` and maximum string length 100, this algorithm executes roughly 10,000 operations, well within 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    res = []
    for _ in range(t):
        s = input().strip()
        if '1' not in s:
            res.append('0')
            continue
        first = s.index('1')
        last = s.rindex('1')
        count = s[first:last+1].count('0')
        res.append(str(count))
    return '\n'.join(res)

# Provided samples
assert run("3\n010011\n0\n1111000\n") == "2\n0\n0", "sample 1"

# Custom test cases
assert run("1\n0000\n") == "0", "all zeros"
assert run("1\n1111\n") == "0", "all ones"
assert run("1\n1010101\n") == "3", "alternating ones and zeros"
assert run("1\n10001\n") == "3", "zeros between first and last ones"
assert run("1\n011110\n") == "0", "zeros outside first and last ones"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0000 | 0 | all zeros, no 1's to make contiguous |
| 1111 | 0 | all ones, no zeros to remove |
| 1010101 | 3 | alternating pattern, internal zeros must be removed |
| 10001 | 3 | zeros strictly between first and last 1 |
| 011110 | 0 | leading/trailing zeros ignored |

## Edge Cases

For the input "0000", the algorithm finds no '1', returns 0 immediately. For "1111", the first and last 1 are at indices 0 and 3, the substring is the full string, and there are no 0's, returning 0. For "10001", the first and last 1 are at indices 0 and 4, the substring is "10001", internal zeros counted as 3, which matches intuition. All edge cases involving strings without 1's, strings with only 1's, and strings with zeros outside the block of 1's are correctly handled.

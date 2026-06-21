---
title: "CF 106057G - MeX is not Max"
description: "We are given one or more sequences of non-negative integers. For each sequence, we want to find the smallest non-negative integer that does not appear anywhere in that sequence. This value is called the MEX, short for “minimum excluded value”."
date: "2026-06-21T08:42:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106057
codeforces_index: "G"
codeforces_contest_name: "CoU CSE Fest 2025 - Inter University Programming Contest (Divisional)"
rating: 0
weight: 106057
solve_time_s: 36
verified: true
draft: false
---

[CF 106057G - MeX is not Max](https://codeforces.com/problemset/problem/106057/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one or more sequences of non-negative integers. For each sequence, we want to find the smallest non-negative integer that does not appear anywhere in that sequence. This value is called the MEX, short for “minimum excluded value”.

Think of the array as a collection of marked integers on the number line starting from zero. Some numbers are present, some are missing. The task is to identify the first gap when scanning from 0 upward.

The input format typically provides a number of test cases, and for each test case a sequence length followed by the sequence itself. The output is a single integer per test case, representing the MEX.

The constraints are not explicitly stated here, but the intended solution runs in linear time per test case. That strongly suggests that the sum of all array sizes across test cases is at most around 2 × 10^5 or 10^6. Any solution that repeatedly scans or sorts the array per test case would become too slow if the total size is large.

A subtle edge case appears when all numbers from 0 to N−1 are present. For example, if the array is `[0, 1, 2, 3]`, then the answer is `4`, because that is the first missing non-negative integer. A naive approach that only checks values up to `max(array)` would fail here if it does not consider the possibility that the MEX is exactly `N`.

Another edge case occurs when the array contains only large values, for example `[10, 11, 12]`. The correct answer is `0`, since zero is missing immediately. A mistaken implementation that starts scanning from the minimum element instead of zero would miss this.

Finally, duplicates do not affect correctness but can mislead inefficient solutions that try to remove or sort elements repeatedly.

## Approaches

A brute-force way to compute the MEX is to repeatedly check whether each integer starting from 0 appears in the array. For each candidate value x, we scan the entire array and check if x exists. If it does not, we return x immediately.

This approach is correct because it directly follows the definition of MEX. The problem is its cost. In the worst case, we may check all values from 0 up to N, and for each one scan N elements. That leads to O(N^2) operations per test case, which becomes too slow when N is large.

The key observation is that we do not need repeated full scans. We only care about whether each number in the range [0, N] appears at least once. Any number greater than N cannot affect the answer, because the MEX of an array of size N is always at most N. This bounds the search space.

We can therefore mark which values in [0, N] exist using a boolean array or hash set in a single pass over the input. After marking, we scan from 0 upward and return the first unmarked index. This reduces the problem to two linear passes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(1) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the array size N and the array values. We will only track values in the range [0, N], since anything larger cannot be the answer.
2. Create a boolean array `present` of size N+1 initialized to False. Each index i in this array represents whether value i exists in the input.
3. Iterate through each element x in the input array. If 0 ≤ x ≤ N, mark `present[x] = True`. This step compresses all relevant information about the array into a compact existence table.
4. Scan from i = 0 to N inclusive. The first index i such that `present[i]` is False is the MEX, so we return it immediately.
5. If all values from 0 to N are present, return N. This covers the case where the array contains a full prefix of integers.

### Why it works

The correctness comes from the fact that the MEX is defined as the smallest non-negative integer absent from the array. The boolean array exactly represents membership for all candidates that could possibly be the answer. Since any MEX of an array of size N cannot exceed N, restricting attention to [0, N] does not lose information. The final scan checks candidates in increasing order, so the first missing index must be the true minimum excluded value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        present = [False] * (n + 1)

        for x in arr:
            if 0 <= x <= n:
                present[x] = True

        ans = n
        for i in range(n + 1):
            if not present[i]:
                ans = i
                break

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by reading the number of test cases and iterating over them. For each case, it builds a presence array sized `n+1` to cover all potentially relevant values. The conditional check inside the loop ensures we ignore values outside the meaningful range, which avoids unnecessary writes and keeps the logic tight.

The final loop is structured to stop immediately upon finding the first missing number. This early exit is important because it preserves linear behavior in practice and matches the definition of MEX directly.

## Worked Examples

### Example 1

Input:

```
1
5
0 1 2 4 4
```

We track presence for indices 0 through 5.

| i | present[i] after processing |
| --- | --- |
| 0 | True |
| 1 | True |
| 2 | True |
| 3 | False |
| 4 | True |
| 5 | False |

Scanning upward, the first False is at i = 3.

Output:

```
3
```

This shows that missing numbers inside the range matter more than duplicates or larger values.

### Example 2

Input:

```
1
4
10 11 12 13
```

Only values outside [0, 4] exist, so nothing is marked.

| i | present[i] |
| --- | --- |
| 0 | False |
| 1 | False |
| 2 | False |
| 3 | False |
| 4 | False |

The first index that is False is 0, so the MEX is 0.

Output:

```
0
```

This demonstrates why we must always consider 0 even if the array contains large numbers only.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) per test case | One pass to mark presence and one scan to find MEX |
| Space | O(N) | Boolean array of size N+1 |

The total work scales linearly with the input size, which fits comfortably within typical constraints for problems of this type, even when multiple test cases are present.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        present = [False] * (n + 1)

        for x in arr:
            if 0 <= x <= n:
                present[x] = True

        ans = n
        for i in range(n + 1):
            if not present[i]:
                ans = i
                break

        output.append(str(ans))

    return "\n".join(output)

# sample-style cases
assert run("1\n5\n0 1 2 4 4\n") == "3"
assert run("1\n4\n10 11 12 13\n") == "0"

# custom cases
assert run("1\n1\n0\n") == "1", "missing 1"
assert run("1\n3\n1 2 3\n") == "0", "missing zero"
assert run("1\n3\n0 1 2\n") == "3", "full prefix"
assert run("1\n6\n2 2 2 2 2 2\n") == "0", "duplicates only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element present | 1 | smallest missing at upper boundary |
| 1 2 3 | 0 | missing zero handling |
| 0 1 2 | 3 | full prefix case |
| all duplicates | 0 | ignores repetition correctly |

## Edge Cases

One important edge case is when the array contains all integers from 0 to N−1. For example:

Input:

```
1
4
0 1 2 3
```

The algorithm marks all positions from 0 to 4 as present except 4, which is never inserted. The scan finds that `present[4]` is False, so it returns 4. This matches the correct MEX because the array fully covers the prefix.

Another edge case is when all elements are outside the valid range:

Input:

```
1
5
100 200 300 400 500
```

During marking, every value is ignored since none lie in [0, 5]. The boolean array remains all False. The scan immediately returns 0, which is correct because zero is the smallest missing integer.

A third case involves duplicates:

Input:

```
1
5
0 0 0 1 1
```

Only 0 and 1 are marked. The scan finds 2 as the first unmarked index. Duplicates do not change the state of the presence array, so correctness is preserved.

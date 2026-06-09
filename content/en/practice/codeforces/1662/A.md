---
title: "CF 1662A - Organizing SWERC"
description: "Gianni needs to assemble a problem set for SWERC from a pool of problems submitted by judges. Each problem has a beauty score and a difficulty rating from 1 to 10."
date: "2026-06-10T02:39:06+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1662
codeforces_index: "A"
codeforces_contest_name: "SWERC 2021-2022 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 0
weight: 1662
solve_time_s: 88
verified: true
draft: false
---

[CF 1662A - Organizing SWERC](https://codeforces.com/problemset/problem/1662/A)

**Rating:** -  
**Tags:** brute force, implementation  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

Gianni needs to assemble a problem set for SWERC from a pool of problems submitted by judges. Each problem has a beauty score and a difficulty rating from 1 to 10. Gianni wants the final problem set to have exactly one problem of each difficulty from 1 to 10, and for each difficulty he will select the problem with the highest beauty. If any difficulty is missing in the pool, Gianni cannot form a full set.

The input provides multiple test cases. Each test case specifies the number of problems and then lists the beauty and difficulty of each problem. The output must either be the total beauty of the selected problem set or the string `MOREPROBLEMS` if a full set cannot be made.

Constraints are small: each test case has at most 100 problems and there are at most 100 test cases. Since there are only 10 difficulties, a solution that processes each difficulty individually is feasible. The input size is small enough that nested loops over the 10 difficulties and the problems are acceptable.

Edge cases include when a difficulty is completely missing, or when multiple problems share the same difficulty but have different beauty scores. For instance, if the input is:

```
1
3
5 1
4 1
7 2
```

The expected output is `MOREPROBLEMS` because difficulties 3 through 10 are missing, even though we have multiple problems for difficulties 1 and 2. A careless solution might sum all beauties without checking for missing difficulties, producing an incorrect total of 16 instead of reporting the impossibility.

## Approaches

The naive approach is to iterate over all 10 difficulties for each test case, and for each difficulty, scan the entire list of problems to find the maximum beauty for that difficulty. If a difficulty is missing, we return `MOREPROBLEMS`. This works because both the number of difficulties and problems are small. The worst-case operation count is `t * 10 * n` where `t` is the number of test cases and `n` the number of problems. With `t ≤ 100` and `n ≤ 100`, this gives at most 100,000 operations, which is acceptable for a 2-second time limit.

The optimal approach leverages a small fixed range of difficulties. We can use an array of size 11 (index 1 to 10) to track the maximum beauty for each difficulty. We iterate through the list of problems once, updating the maximum beauty for the problem's difficulty. After processing all problems, we check if any difficulty has no problem (beauty remains at initial value). If so, output `MOREPROBLEMS`. Otherwise, sum the stored maximum beauties. This approach reduces repeated scanning and is clean and direct.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t * n * 10) | O(1) | Accepted |
| Optimal | O(t * n) | O(10) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. For each test case:
2. Read the number of problems `n`.
3. Initialize an array `max_beauty` of size 11 with all entries set to -1. Index `i` will store the maximum beauty of problems with difficulty `i`.
4. For each problem, read its beauty `b` and difficulty `d`. Update `max_beauty[d]` to be the maximum of its current value and `b`. This ensures that after reading all problems, `max_beauty[d]` stores the most beautiful problem of difficulty `d`.
5. Check all difficulties from 1 to 10. If any `max_beauty[d]` is still -1, print `MOREPROBLEMS` for this test case.
6. Otherwise, sum the values in `max_beauty[1..10]` and print the result.

Why it works: The invariant is that after processing all problems, `max_beauty[d]` contains the maximum beauty of any problem with difficulty `d`, or -1 if no such problem exists. Checking for -1 ensures we do not miss any difficulty. Summing these maximums produces the total beauty of the problem set because Gianni always chooses the most beautiful problem per difficulty.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    max_beauty = [-1] * 11  # indices 1..10
    for _ in range(n):
        b, d = map(int, input().split())
        if b > max_beauty[d]:
            max_beauty[d] = b
    if -1 in max_beauty[1:]:
        print("MOREPROBLEMS")
    else:
        print(sum(max_beauty[1:]))
```

The code initializes `max_beauty` with -1 to clearly detect missing difficulties. Each problem updates the maximum beauty for its difficulty. The check for `-1` ensures that we only compute a sum if all difficulties are covered. Using indices 1 to 10 matches the problem's difficulty numbering and avoids off-by-one errors. Fast input via `sys.stdin.readline` is used to handle multiple test cases efficiently.

## Worked Examples

### Sample 1

Input:

```
3
8 4
9 3
6 7
```

| Step | Problem | max_beauty[1..10] after update |
| --- | --- | --- |
| 1 | 8 4 | [-1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1] |
| 2 | 9 3 | [-1, -1, 9, 8, -1, -1, -1, -1, -1, -1, -1] |
| 3 | 6 7 | [-1, -1, 9, 8, -1, -1, 6, -1, -1, -1, -1] |

Check `max_beauty[1..10]`: missing entries at indices 1,2,5,6,8,9,10 → output `MOREPROBLEMS`.

### Sample 2

Input:

```
12
3 10
10 1
10 2
10 3
10 4
3 10
10 5
10 6
10 7
10 8
10 9
1 10
```

| Step | Problem | max_beauty[1..10] after update |
| --- | --- | --- |
| 1 | 3 10 | [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3] |
| 2 | 10 1 | [-1, 10, -1, -1, -1, -1, -1, -1, -1, -1, 3] |
| ... | ... | ... |
| 12 | 1 10 | last problem has beauty 1 → max_beauty[10] remains 3 |

Sum `max_beauty[1..10] = 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 3 = 93`.

This trace confirms the algorithm correctly updates the maximum beauty per difficulty and computes the total beauty while handling multiple problems per difficulty.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each problem is processed once, updating an array of size 10. Checking for missing difficulties takes O(10) per test case. |
| Space | O(10) | `max_beauty` array stores 10 values per test case. |

With t ≤ 100 and n ≤ 100, the solution performs at most 10,000 operations, well within the 2-second limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        t = int(input())
        for _ in range(t):
            n = int(input())
            max_beauty = [-1] * 11
            for _ in range(n):
                b, d = map(int, input().split())
                max_beauty[d] = max(max_beauty[d], b)
            if -1 in max_beauty[1:]:
                print("MOREPROBLEMS")
            else:
                print(sum(max_beauty[1:]))
    return out.getvalue().strip()

# Provided samples
assert run("2\n3\n8 4\n9 3\n6 7\n12\n3 10\n10 1\n10 2\n10 3\n10 4\n3 10\n10 5\n10 6\n10 7\n10 8\n10 9\n1 10") == "MOREPROBLEMS\n93"

# Minimum-size input
assert run("1\n1\n1 1") == "MOREPROBLEMS", "only one problem, missing difficulties 2..10"

# Maximum-size input with all difficulties
input_data = "1\n100\n" + "\n".join(f"{i%10+1} {i%10+1}" for i in range(100))
expected_sum =
```

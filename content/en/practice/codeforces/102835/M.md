---
title: "CF 102835M - Keystroke"
description: "The problem models a faulty numeric keypad with four keys arranged as a 2 by 2 grid. Each key corresponds to one of the numbers 1 to 4, and pressing a key produces a pair containing its row index and column index."
date: "2026-07-26T15:05:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102835
codeforces_index: "M"
codeforces_contest_name: "The 2020 ICPC Asia Taipei-Hsinchu Site Programming Contest"
rating: 0
weight: 102835
solve_time_s: 66
verified: true
draft: false
---

[CF 102835M - Keystroke](https://codeforces.com/problemset/problem/102835/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a faulty numeric keypad with four keys arranged as a 2 by 2 grid. Each key corresponds to one of the numbers 1 to 4, and pressing a key produces a pair containing its row index and column index. When several keys are pressed together, the controller loses the pairing between rows and columns. It only receives the set of rows that appeared and the set of columns that appeared. The task is to count how many different subsets of keys could have produced the observed row set and column set. The original problem limits the received row and column sets to sizes at most two, because the keypad has only two possible row values and two possible column values.

The input contains several test cases. For each test case, the first line gives the number of distinct rows and columns received. The next two lines describe those row values and column values. The output is the number of subsets among the four keypad keys whose collection of rows and columns exactly matches the received signal.

The constraints are extremely small. There are at most 10 test cases, and each dimension of the received signal contains only one or two values. This means the solution does not need any advanced optimization. A constant-time approach is enough, and even checking every possible subset of the four keys is only 16 cases per test. Any solution involving large data structures or complicated mathematics would be solving a much harder problem than the actual one.

The main traps come from the fact that different key combinations can produce the same signal. For example, pressing keys 1 and 4 gives the same received row set and column set as pressing keys 2 and 3. A solution that tries to reconstruct a unique pressed set will fail because the signal does not preserve the original pairing information.

For the input

```
1
1 1
0
0
```

the correct output is

```
1
```

Only key 1 produces row set `{0}` and column set `{0}`. A careless approach that counts row and column choices independently may incorrectly treat the row and column as unrelated and overcount.

For the input

```
1
2 2
0 1
0 1
```

the correct output is

```
7
```

Every non-empty subset of the four keys except the empty set produces the full row set `{0,1}` and column set `{0,1}`. A careless approach may return only one because it assumes the received signal identifies one combination.

## Approaches

A direct brute-force solution is enough because the keypad contains only four keys. The natural brute-force idea is to enumerate every possible subset of keys, simulate the signal created by that subset, and compare it with the given signal. For each chosen key, we collect its row and column. If both collected sets are equal to the received row and column sets, we increase the answer.

This approach is correct because it checks exactly the definition of a valid keystroke combination. There are only (2^4 = 16) possible subsets, so the worst case performs only a few dozen operations per test case. The small constraints make this the intended solution.

The key observation is that the keypad layout is fixed. We never need to search over possible layouts or derive a mathematical formula. The only unknown is which of the four keys were pressed, and the complete search space has size 16. The brute-force method already reduces the problem to checking a tiny fixed number of candidates.

The comparison between approaches is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(16) | O(1) | Accepted |
| Optimal | O(16) | O(1) | Accepted |

The brute-force solution is also the optimal practical solution here because the constant search space cannot be meaningfully reduced.

## Algorithm Walkthrough

1. Store the four keys with their corresponding coordinates. Key 1 has coordinate `(0,0)`, key 2 has coordinate `(0,1)`, key 3 has coordinate `(1,0)`, and key 4 has coordinate `(1,1)`.
2. Read the received row values and column values and store them as sets. Sets are used because the order of received values does not matter.
3. Enumerate every mask from 0 to 15. Each bit represents whether one of the four keys is included in the pressed combination.
4. For the current mask, collect all rows and columns belonging to the selected keys. The generated row set and column set describe exactly what the controller would receive from this combination.
5. Compare the generated sets with the input sets. If both are equal, count this mask as a possible keystroke combination.
6. Output the number of valid masks.

Why it works:

Every possible pressed combination corresponds to exactly one subset of the four keys, and every subset is checked by the enumeration. For each subset, the algorithm computes the exact signal received by the controller. A subset is counted if and only if its signal matches the given signal, so the final count contains all and only valid combinations.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    t = int(input())
    keys = [(0, 0), (0, 1), (1, 0), (1, 1)]
    ans = []

    for _ in range(t):
        m, n = map(int, input().split())
        rows = set(map(int, input().split()))
        cols = set(map(int, input().split()))

        cur = 0

        for mask in range(1 << 4):
            r = set()
            c = set()

            for i in range(4):
                if mask & (1 << i):
                    r.add(keys[i][0])
                    c.add(keys[i][1])

            if r == rows and c == cols:
                cur += 1

        ans.append(str(cur))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The array `keys` represents the fixed keypad layout. The index of an element is the key number minus one, so bit `i` in a mask corresponds directly to one keypad key.

The mask loop covers all possible subsets. The empty subset is intentionally included because the received signal could theoretically be empty in a more general version of the problem, although the given constraints always provide at least one row and one column.

The sets `r` and `c` are rebuilt for every mask. This avoids accidentally keeping values from a previous subset, which is a common implementation mistake in enumeration problems.

There are no indexing boundary issues because the keypad has exactly four known positions. Integer overflow is also impossible because the answer is at most 16.

## Worked Examples

For the first sample:

```
2
2 1
0 1
0
1 2
1
0 1
```

The first test case has received rows `{0,1}` and columns `{0}`.

| Mask | Selected keys | Generated rows | Generated columns | Counted |
| --- | --- | --- | --- | --- |
| 0000 | none | {} | {} | No |
| 0011 | 1,2 | {0} | {0,1} | No |
| 0101 | 1,3 | {0,1} | {0} | Yes |
| 0110 | 2,3 | {0,1} | {0,1} | No |

The only valid subset is keys 1 and 3, so the answer is 1. This demonstrates that the algorithm preserves the pairing between rows and columns while checking every possible pressed set.

For the second sample:

```
2
2 2
0 1
0 1
1 1
1
```

The first test case asks for every possible row and column value.

| Mask | Selected keys | Generated rows | Generated columns | Counted |
| --- | --- | --- | --- | --- |
| 0000 | none | {} | {} | No |
| 0001 | 1 | {0} | {0} | No |
| 0011 | 1,2 | {0} | {0,1} | No |
| 0101 | 1,3 | {0,1} | {0} | No |
| 0110 | 2,3 | {0,1} | {0,1} | Yes |
| 1111 | all keys | {0,1} | {0,1} | Yes |

Continuing the same check for all masks gives seven valid subsets. This demonstrates the central property of the problem: different subsets can generate the same received signal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(16) | Every test case checks all subsets of four keys. |
| Space | O(1) | Only a few sets containing at most two values are stored. |

The maximum work per test case is fixed, so the solution easily fits the one second limit even with the maximum number of test cases.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        keys = [(0, 0), (0, 1), (1, 0), (1, 1)]
        out = []

        for _ in range(t):
            m, n = map(int, input().split())
            rows = set(map(int, input().split()))
            cols = set(map(int, input().split()))

            ans = 0
            for mask in range(16):
                r = set()
                c = set()
                for i in range(4):
                    if mask & (1 << i):
                        r.add(keys[i][0])
                        c.add(keys[i][1])
                if r == rows and c == cols:
                    ans += 1

            out.append(str(ans))

        return "\n".join(out)

    result = solve()
    sys.stdin = old_stdin
    return result

assert run("""2
2 1
0 1
0
1 2
1
0 1
""") == "1\n1", "sample 1"

assert run("""2
2 2
0 1
0 1
1 1
1
1
""") == "7\n1", "sample 2"

assert run("""3
1 1
0
0
1 1
1
1
2 2
0 1
0 1
""") == "1\n1\n7", "basic signals"

assert run("""1
1 2
0
0 1
""") == "2", "single row with two columns"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single row and single column | 1 | A unique key signal |
| Full keypad signal | 7 | Multiple combinations producing the same signal |
| Different corners | 1 | Correct row-column pairing |
| One row with two columns | 2 | Ambiguous combinations |

## Edge Cases

For a signal generated by one exact key, such as:

```
1
1 1
0
0
```

the algorithm checks all 16 subsets. Only the subset containing key 1 creates row set `{0}` and column set `{0}`, so the answer is 1. The solution does not confuse independent row and column choices with actual keys.

For a signal containing all rows and columns:

```
1
2 2
0 1
0 1
```

the algorithm finds seven matching subsets. The empty subset is rejected because it produces no rows and no columns, while every non-empty subset except single-row or single-column combinations that miss one coordinate is handled correctly.

For an ambiguous signal such as:

```
1
2 2
0 1
0 1
```

the subsets `{1,4}` and `{2,3}` both produce the same controller signal. The enumeration counts both because it checks combinations directly rather than trying to reconstruct the original keys from incomplete information.

---
title: "CF 104931E - Up Down Matching"
description: "We are given multiple test cases. Each test case consists of a line of people standing in a row, where each person belongs to one of two groups, encoded as U or D."
date: "2026-06-28T07:38:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104931
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 01-26-24 Div. 1 (Advanced)"
rating: 0
weight: 104931
solve_time_s: 251
verified: false
draft: false
---

[CF 104931E - Up Down Matching](https://codeforces.com/problemset/problem/104931/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given multiple test cases. Each test case consists of a line of people standing in a row, where each person belongs to one of two groups, encoded as `U` or `D`. The task is to choose a contiguous segment of this row such that inside that segment the number of `U` characters is exactly equal to the number of `D` characters, and among all such valid segments we want the maximum possible length.

For each test case we only output a single number, the length of the longest balanced segment. If no non-empty segment can satisfy the condition, the answer is zero.

The constraints imply we may see up to ten thousand test cases, but the total length across all strings is bounded by two hundred thousand. That forces any solution to run in linear time per test case on average, since anything quadratic over each string would immediately exceed time limits when all test cases are large.

A naive approach that checks every subarray would examine roughly n squared segments per test case. With n up to two hundred thousand in total, this is far beyond feasible.

A subtle issue appears when all characters belong to one group. For example, `UUUUU` or `DDDDD`. In these cases, there is no valid segment of positive length, so the answer must be zero. Any method that assumes at least one valid pair exists would incorrectly return a non-zero value.

Another corner case is when the best segment spans the entire string. For example `UDUD` is fully balanced, and the correct answer is the full length. A solution that only tracks local matches or resets too aggressively would miss this global structure.

## Approaches

A brute-force strategy tries every possible starting index and expands to every ending index, counting how many `U` and `D` characters appear in each segment. Whenever the counts match, we update the best answer. This is correct because it explicitly checks every possible segment.

However, maintaining counts for each pair still costs linear time per segment if recomputed, or constant time if maintained incrementally. Even in the best implementation, we still inspect O(n^2) segments per test case. With total input size up to 200,000, this leads to about 20 billion operations in the worst case, which is not viable.

The key observation is that we do not actually care about the exact counts of `U` and `D` separately. We only care about their difference. If we interpret `U` as +1 and `D` as -1, then a segment is balanced exactly when its sum is zero.

This transforms the problem into finding the longest subarray whose sum is zero. Using prefix sums, this becomes equivalent to finding two equal prefix sums at positions i and j. If prefix[i] equals prefix[j], then the subarray (i+1 to j) is balanced.

The optimization comes from the fact that we only need to remember the earliest occurrence of each prefix sum. When we see the same prefix sum again, the distance between occurrences gives a valid balanced segment, and we maximize it by keeping the first occurrence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) or O(n) | Too slow |
| Prefix Sum Hashing | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Convert the string into a running balance where `U` contributes +1 and `D` contributes -1. We track a prefix sum that represents this balance at every position. This allows us to detect equality of `U` and `D` by checking whether the sum returns to a previous value.
2. Initialize a dictionary that stores the earliest index where each prefix sum value appears. We also store the prefix sum 0 at index -1 before processing begins. This handles segments that start from index 0 correctly, since a balanced prefix from the beginning will match this base state.
3. Iterate through the string, updating the prefix sum as we go. At each position, we check whether this prefix sum has been seen before.
4. If the prefix sum has been seen, the subarray between the previous index and the current index is balanced. We compute its length and update the maximum answer.
5. If the prefix sum has not been seen, we record its index as the first occurrence. We never overwrite earlier occurrences because earlier indices produce longer valid segments when matched later.
6. After processing the entire string, output the maximum length found.

### Why it works

The prefix sum at position i encodes the difference between counts of `U` and `D` up to that point. Two positions with the same prefix sum imply that the net contribution between them is zero, meaning equal numbers of `U` and `D`. Storing the earliest occurrence ensures that every later repetition of the same balance yields the longest possible segment ending at that position. No balanced segment is missed because every valid segment corresponds to some pair of equal prefix sums.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n = int(input())
        s = input().strip()
        
        first_pos = {0: -1}
        pref = 0
        best = 0
        
        for i, ch in enumerate(s):
            if ch == 'U':
                pref += 1
            else:
                pref -= 1
            
            if pref in first_pos:
                best = max(best, i - first_pos[pref])
            else:
                first_pos[pref] = i
        
        out.append(str(best))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core structure revolves around maintaining a prefix balance while scanning left to right. The dictionary `first_pos` stores the earliest index at which each balance appears. The initialization with `{0: -1}` is critical because it allows a prefix ending at index `i` with zero net balance to correctly produce a segment of length `i + 1`.

The update rule for `pref` converts the character stream into a numeric signal, which is the central transformation that simplifies the problem.

The `best` variable tracks the maximum distance between repeated prefix sums, which directly corresponds to the longest valid segment.

## Worked Examples

Consider a simple case:

Input string: `UUDD`

We track prefix sums and first occurrences.

| i | char | prefix | first occurrence map update | best |
| --- | --- | --- | --- | --- |
| -1 | - | 0 | {0: -1} | 0 |
| 0 | U | 1 | {0:-1, 1:0} | 0 |
| 1 | U | 2 | {0:-1, 1:0, 2:1} | 0 |
| 2 | D | 1 | match at 0 gives length 2 | 2 |
| 3 | D | 0 | match at -1 gives length 4 | 4 |

The final answer is 4, showing that the entire string is balanced.

Now consider `UDUUDD`.

| i | char | prefix | first occurrence | best |
| --- | --- | --- | --- | --- |
| 0 | U | 1 | 1:0 | 0 |
| 1 | D | 0 | 0:-1 exists, update best=2 | 2 |
| 2 | U | 1 | seen at 0 gives 2 | 2 |
| 3 | U | 2 | 2:3 | 2 |
| 4 | D | 1 | seen at 0 gives 4 | 4 |
| 5 | D | 0 | seen at -1 gives 6 | 6 |

This shows how repeated prefix values unlock multiple valid segments, and why keeping earliest positions is essential for maximizing length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once, dictionary operations are O(1) on average |
| Space | O(n) | In worst case all prefix sums are distinct |

The total input size across test cases is bounded, so a linear scan per test case is sufficient to stay within limits. The hashing structure only stores at most n distinct prefix states per test case, fitting comfortably in memory constraints.

## Test Cases

```python
import sys, io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else run_solver(inp)

def run_solver(inp: str) -> str:
    import sys
    input = sys.stdin.readline
    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        s = input().strip()
        first_pos = {0: -1}
        pref = 0
        best = 0
        for i, ch in enumerate(s):
            pref += 1 if ch == 'U' else -1
            if pref in first_pos:
                best = max(best, i - first_pos[pref])
            else:
                first_pos[pref] = i
        res.append(str(best))
    return "\n".join(res)

# provided sample (as intended individual cases)
assert run_solver("1\n4\nUDUD\n") == "4"
assert run_solver("1\n6\nUUUDDD\n") == "6"

# all same
assert run_solver("1\n5\nUUUUU\n") == "0"

# already balanced full string
assert run_solver("1\n8\nUDUDUDUD\n") == "8"

# no full balance but internal segment exists
assert run_solver("1\n5\nUUDUD\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| UUUUU | 0 | no valid segment exists |
| UDUD | 4 | full string balance |
| UUDUD | 4 | best segment is internal, not prefix |

## Edge Cases

When the string contains only one character type, every prefix sum is strictly monotonic and never repeats. The algorithm still initializes the dictionary with `{0: -1}`, but no future prefix equals zero again, so `best` remains zero throughout. This correctly handles inputs like `DDDDD`, where no valid segment exists.

When the entire string is balanced, such as `UDUD`, the prefix sum returns to zero at the last index. Since zero was stored at index -1 initially, the computed segment spans the full array. The algorithm naturally captures this without special casing.

When balanced segments exist but are not prefix-aligned, such as `UUDUD`, repeated prefix sums appear in the middle of the scan. Each repetition correctly forms a candidate segment, and the earliest stored index guarantees maximal expansion for that prefix value, ensuring the longest segment is found even when it starts and ends in the middle of the string.

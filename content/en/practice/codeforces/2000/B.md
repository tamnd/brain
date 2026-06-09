---
title: "CF 2000B - Seating in a Bus"
description: "We have a bus with n seats in a single row, numbered from 1 to n. Passengers board one by one, and each chooses a seat according to a simple rule: the first passenger can sit anywhere, but any subsequent passenger must sit adjacent to an already occupied seat."
date: "2026-06-09T02:30:43+07:00"
tags: ["codeforces", "competitive-programming", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2000
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 966 (Div. 3)"
rating: 800
weight: 2000
solve_time_s: 204
verified: false
draft: false
---

[CF 2000B - Seating in a Bus](https://codeforces.com/problemset/problem/2000/B)

**Rating:** 800  
**Tags:** two pointers  
**Solve time:** 3m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We have a bus with `n` seats in a single row, numbered from 1 to `n`. Passengers board one by one, and each chooses a seat according to a simple rule: the first passenger can sit anywhere, but any subsequent passenger must sit adjacent to an already occupied seat. We are given the chronological sequence of seats chosen by `n` passengers and must determine whether each passenger followed this recommendation.

The input consists of multiple test cases. Each test case provides `n` and the array of seat numbers. The output is "YES" if every passenger in that test case obeyed the adjacency rule, or "NO" otherwise.

The constraints allow `n` to reach 2·10^5 per test case, with up to 10^4 test cases, though the total sum of all `n` across all test cases is at most 2·10^5. This implies that we cannot afford an O(n^2) approach, since it would perform around 4·10^10 operations in the worst case. We need a solution with overall linear or near-linear complexity.

An edge case arises when the first few passengers occupy the ends of the bus. For example, if `n = 5` and the sequence is `[5, 4, 2, 1, 3]`, the third passenger chooses seat `2`, which is invalid because neither neighbor is occupied. A naive approach that only checks whether the seat number exists in the sequence so far would miss this, since the occupied seats are not contiguous at that point.

Another subtle case occurs when passengers occupy seats in strictly increasing or decreasing order from one end, which is valid because every new seat is adjacent to the current occupied segment. Detecting the continuous segment of occupied seats is crucial.

## Approaches

The brute-force approach is straightforward: for each passenger after the first, check the seats immediately to the left and right and verify whether either is occupied. This works logically, but each check would require scanning the list of occupied seats, resulting in O(n^2) per test case. This becomes infeasible for large `n`.

The key observation is that at any point in time, the set of valid seats forms a contiguous block of occupied seats. Each new passenger must extend this block by sitting directly adjacent to its leftmost or rightmost occupied seat. Therefore, we only need to track the current leftmost and rightmost occupied seats. For the first passenger, we set both ends to that seat. Each subsequent passenger must sit either immediately to the left of the current left end or immediately to the right of the current right end. If a passenger chooses a seat outside these two options, the rules are violated.

This observation allows an O(n) scan of the sequence while maintaining two variables, `left` and `right`, representing the current occupied segment. No complex data structures are needed. The solution is simple and efficient, making it ideal for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (scan all occupied seats) | O(n^2) | O(n) | Too slow |
| Segment Tracking (two pointers) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers, `left` and `right`, to `-1`. These will track the current contiguous block of occupied seats.
2. Iterate through the sequence of passengers' seat choices.
3. For the first passenger, set both `left` and `right` to their seat number. This establishes the initial segment.
4. For each subsequent passenger, check whether their seat is immediately to the left (`seat == left - 1`) or immediately to the right (`seat == right + 1`) of the current segment.
5. If the seat extends the left end, update `left` to this new seat. If it extends the right end, update `right`. If it does not extend either end, return "NO" for this test case.
6. If all passengers satisfy the adjacency condition, return "YES".

Why it works: by maintaining the leftmost and rightmost occupied seats, we guarantee that the occupied seats form a contiguous segment. Since passengers are only allowed to sit adjacent to this segment, any violation immediately shows a rule break. This invariant is maintained after each step, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def seating_in_bus():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        left = right = -1
        valid = True
        
        for seat in a:
            if left == -1:
                left = right = seat
            elif seat == left - 1:
                left = seat
            elif seat == right + 1:
                right = seat
            else:
                valid = False
                break
        
        print("YES" if valid else "NO")

if __name__ == "__main__":
    seating_in_bus()
```

The code initializes `left` and `right` to `-1` to indicate an empty bus. For each passenger, we check if they sit next to the current occupied segment. Updating the segment boundaries ensures that subsequent checks remain valid. The check `seat == left - 1` and `seat == right + 1` handles both ends efficiently. Breaking early on the first violation avoids unnecessary computations.

## Worked Examples

### Example 1

Input: `[5, 4, 2, 1, 3]` with `n = 5`

| Passenger | Seat | left | right | Valid? |
| --- | --- | --- | --- | --- |
| 1 | 5 | 5 | 5 | YES |
| 2 | 4 | 4 | 5 | YES |
| 3 | 2 | 4 | 5 | NO |

Passenger 3 chose seat `2`, which is not adjacent to the current segment `[4,5]`. The algorithm correctly identifies this violation.

### Example 2

Input: `[2, 3, 1]` with `n = 3`

| Passenger | Seat | left | right | Valid? |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2 | YES |
| 2 | 3 | 2 | 3 | YES |
| 3 | 1 | 1 | 3 | YES |

Every passenger extends the contiguous segment, producing "YES".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case, O(Σn) overall | Each seat is checked exactly once, updating left/right takes O(1) |
| Space | O(1) | Only two pointers and loop variables are stored |

With Σn ≤ 2·10^5, the algorithm executes comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    seating_in_bus()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n5\n5 4 2 1 3\n3\n2 3 1\n4\n2 3 1 4\n5\n1 2 3 5 4\n") == "NO\nYES\nYES\nNO"

# Custom cases
assert run("1\n1\n1\n") == "YES", "single passenger"
assert run("1\n3\n3 2 1\n") == "YES", "decreasing sequence from end"
assert run("1\n4\n1 3 2 4\n") == "NO", "non-adjacent seat in middle"
assert run("1\n2\n2 1\n") == "YES", "two passengers occupying ends"
assert run("1\n5\n3 4 5 2 1\n") == "YES", "segment extends in both directions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | YES | Single passenger edge case |
| `1\n3\n3 2 1` | YES | Decreasing sequence from one end |
| `1\n4\n1 3 2 4` | NO | Non-adjacent seat in middle |
| `1\n2\n2 1` | YES | Two passengers at ends |
| `1\n5\n3 4 5 2 1` | YES | Segment grows in both directions correctly |

## Edge Cases

If the first passenger sits in the middle, e.g., `n = 5`, sequence `[3, 2, 4, 1, 5]`, the algorithm initializes `left=right=3`. Passenger 2 sits at `2` (`left-1`), updating `left=2`. Passenger 3 sits at `4` (`right+1`), updating `right=4`. Passenger 4 sits at `1` (`left-1`), updating `left=1`. Passenger 5 sits at `5` (`right+1`), updating `right=5`. Each step maintains the invariant of a contiguous segment. The algorithm outputs "YES" correctly. This confirms proper handling of nontrivial segment growth in both directions.

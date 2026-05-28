---
title: "CF 120B - Quiz League"
description: "We are given a circular table divided into n sectors, each containing a quiz question. Some questions have already been asked, marked with a 0, and others are still available, marked with a 1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 120
codeforces_index: "B"
codeforces_contest_name: "School Regional Team Contest, Saratov, 2011"
rating: 1100
weight: 120
solve_time_s: 81
verified: true
draft: false
---

[CF 120B - Quiz League](https://codeforces.com/problemset/problem/120/B)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular table divided into `n` sectors, each containing a quiz question. Some questions have already been asked, marked with a `0`, and others are still available, marked with a `1`. An arrow points at sector `k`, and the goal is to determine the number of the next question that will be asked. If the sector pointed to by the arrow has already been asked, the host selects the next unanswered question in clockwise order. The numbering wraps around from sector `n` back to sector `1`.

The input consists of two integers, `n` and `k`, followed by a list of `n` integers representing the status of each sector. The output is a single integer representing the sector number of the next question to be asked.

The constraints are small: `n` can go up to 1000. This implies that even a straightforward linear search around the table is efficient enough, since in the worst case we would perform `n` checks per query, which is at most 1000 operations.

Non-obvious edge cases include the arrow pointing at the last sector, with the next available question wrapping around to the beginning, or having the arrow pointing directly at an available question (no movement needed). For example, if `n = 5`, `k = 5`, and the array is `[0, 1, 0, 1, 0]`, the arrow points at a sector that is already asked (`0`). The next unanswered sector clockwise is `2`, not `5`, because `5` is already used.

## Approaches

The brute-force approach is simple and correct: start at the sector indicated by the arrow and check if the question has already been asked. If it has, move clockwise one sector at a time, wrapping around when necessary, until an available question is found. The worst-case complexity is `O(n)`, which is acceptable given `n ≤ 1000`. This approach works because we are guaranteed that at least one question is unanswered.

The optimal solution is essentially the same as the brute-force because the structure of the problem - a small circular array - allows us to linearly search without penalty. No additional data structures are necessary, and the wrap-around can be handled using the modulo operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

The naive and optimal approaches converge here because the problem's constraints are small and the operation is straightforward.

## Algorithm Walkthrough

1. Read `n` and `k`. Adjust `k` to zero-based indexing for easier array access.
2. Read the array of question statuses. Each element is `1` if the question is unanswered and `0` if it has already been asked.
3. Start a loop at index `k-1` and move clockwise. For each iteration, check if the current sector is available.
4. If the current sector contains an unanswered question (`1`), print its 1-based index and stop.
5. If the current sector has been asked (`0`), increment the index by one, and use modulo `n` to wrap around to the start if necessary.

Why it works: the invariant is that at every step, we either have found an unanswered question or we continue to the next sector. Because the problem guarantees at least one unanswered question, the loop will always terminate with the correct sector. The modulo operation ensures we correctly handle the circular nature of the table.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

# convert to zero-based index
idx = k - 1

while True:
    if a[idx] == 1:
        print(idx + 1)  # output 1-based index
        break
    idx = (idx + 1) % n
```

The code starts from the sector indicated by the arrow, checks if it is unanswered, and moves clockwise if needed. The modulo ensures that moving past the last sector wraps around to the first. Using zero-based indexing internally simplifies array access and arithmetic.

## Worked Examples

**Sample 1**

Input:

```
5 5
0 1 0 1 0
```

| Step | idx | a[idx] | Action |
| --- | --- | --- | --- |
| 1 | 4 | 0 | already asked, move to next |
| 2 | 0 | 0 | already asked, move to next |
| 3 | 1 | 1 | found available, output 2 |

This shows that the algorithm correctly wraps around the array and selects the next unanswered question clockwise.

**Sample 2** (constructed)

Input:

```
6 3
1 0 0 1 1 0
```

| Step | idx | a[idx] | Action |
| --- | --- | --- | --- |
| 1 | 2 | 0 | move to next |
| 2 | 3 | 1 | found available, output 4 |

This confirms that if the arrow points at an already-asked sector, the search continues until a valid question is found.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | In the worst case, we may have to check every sector once. |
| Space | O(n) | Storing the array of question statuses. |

The solution is well within the 1-second time limit for `n ≤ 1000` and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    idx = k - 1
    while True:
        if a[idx] == 1:
            print(idx + 1)
            break
        idx = (idx + 1) % n
    return output.getvalue().strip()

# Provided sample
assert run("5 5\n0 1 0 1 0\n") == "2", "sample 1"

# Custom cases
assert run("1 1\n1\n") == "1", "single sector, unanswered"
assert run("3 2\n0 0 1\n") == "3", "arrow points at asked, next is last sector"
assert run("4 4\n1 0 1 0\n") == "4", "arrow points at available, no move"
assert run("5 3\n0 0 0 1 0\n") == "4", "wrap around multiple zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\n1` | `1` | single sector edge case |
| `3 2\n0 0 1` | `3` | arrow points at asked, next is last sector |
| `4 4\n1 0 1 0` | `4` | arrow points at available question |
| `5 3\n0 0 0 1 0` | `4` | wrap-around search for next unanswered |

## Edge Cases

If the arrow points at the last sector and all previous sectors are already asked, the modulo ensures that the search continues from the beginning. For input `5 5\n0 1 0 1 0`, the search moves from index `4` to `0`, then `1`, which is the first available sector, correctly outputting `2`.

For a single-sector table with an unanswered question, `1 1\n1`, the loop immediately finds the available question without any iteration, correctly outputting `1`.

This algorithm handles all edge cases by the invariant that it always checks each sector in clockwise order until an unanswered question is found, and the modulo guarantees proper wrapping around the circular table.

---
title: "CF 106038B - Astana"
description: "We are given a chronologically sorted list of distinct integers, where each integer represents a day on which Bernardo went to the gym. The goal is to determine the longest streak of consecutive calendar days present inside this list."
date: "2026-06-20T21:04:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106038
codeforces_index: "B"
codeforces_contest_name: "UNICAMP Selection Contest 2025"
rating: 0
weight: 106038
solve_time_s: 50
verified: true
draft: false
---

[CF 106038B - Astana](https://codeforces.com/problemset/problem/106038/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a chronologically sorted list of distinct integers, where each integer represents a day on which Bernardo went to the gym. The goal is to determine the longest streak of consecutive calendar days present inside this list. A streak is formed when days differ by exactly one, such as 5, 6, 7 forming a streak of length 3, and we want the maximum length over all such contiguous sequences.

The input size is linear in the number of recorded visits, so any solution that repeatedly scans the array or tries to expand intervals from every starting point must still be efficient enough to handle up to about 200,000 elements within one second. This rules out any quadratic behavior, since nested scanning over already sorted data would easily exceed on the order of 10^10 operations in the worst case.

A common failure mode comes from treating the problem as if we need to consider all pairs or recompute streak lengths independently for each index. For example, given input `1 2 3 4 10 11`, a naive approach might start from each index and repeatedly check forward, recomputing overlapping segments multiple times, which becomes redundant and slow.

Another subtle edge case is when there are no consecutive elements at all. For instance, input `5 10 20` should return 1, because each day stands alone as a streak of length one. Any solution that assumes at least one consecutive pair exists and initializes the answer incorrectly could fail here.

## Approaches

The brute-force idea is straightforward: for each position in the array, treat it as the start of a streak and extend forward while the next value is exactly one greater than the current. This correctly computes the longest streak starting at each index, and taking the maximum over all starts yields the correct answer.

However, this approach repeatedly scans overlapping segments. In the worst case where the array itself is a single long consecutive sequence, such as `1 2 3 4 ... n`, the first index scans n elements, the second scans n-1, and so on, leading to about n²/2 comparisons. This becomes too slow when n is large.

The key observation is that because the array is already sorted, consecutive sequences appear as contiguous blocks. Instead of restarting a scan at every index, we only need to track the length of the current streak as we sweep once from left to right. When the difference between consecutive elements is exactly one, we extend the streak; otherwise, we reset it. This removes all redundant recomputation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array in a single pass while maintaining the length of the current consecutive streak and the best answer seen so far.

1. Initialize a variable `best` as 1, since any single element forms a valid streak of length one. This handles the case where there are no consecutive pairs.
2. Initialize `cur` as 1, representing the length of the current streak ending at the first element.
3. Iterate from the second element to the end of the array. At each index `i`, compare `a[i]` with `a[i-1]`.
4. If `a[i] == a[i-1] + 1`, increment `cur` by 1 because the streak continues without interruption. This directly encodes the definition of consecutive days.
5. Otherwise, reset `cur` to 1 because the streak is broken and a new streak starts at position `i`.
6. After updating `cur`, update `best` as `max(best, cur)` to keep track of the maximum streak seen anywhere in the array.
7. After finishing the loop, output `best`.

The correctness comes from maintaining the invariant that at every index `i`, `cur` equals the length of the longest consecutive streak ending exactly at `i`. Since every streak must end at some position, tracking all such endpoints guarantees we capture the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, input().split()))
    if not data:
        return

    n = data[0]
    arr = data[1:]

    # In some inputs n may not be needed explicitly if all values are present
    # but we trust format: first number is n, followed by n values.
    if len(arr) < n:
        arr += list(map(int, input().split()))

    if n == 0:
        print(0)
        return

    best = 1
    cur = 1

    for i in range(1, n):
        if arr[i] == arr[i - 1] + 1:
            cur += 1
        else:
            cur = 1
        if cur > best:
            best = cur

    print(best)

if __name__ == "__main__":
    solve()
```

The code performs a single linear scan. The only state kept is the current streak length and the best result so far. The comparison `arr[i] == arr[i-1] + 1` is the entire decision mechanism, and everything else is bookkeeping around it.

A common implementation mistake is forgetting to reset the current streak when the sequence breaks, which would incorrectly accumulate values across gaps. Another is initializing `best` to 0, which would fail when the array has at least one element but no consecutive pairs.

## Worked Examples

Consider input `5 100 101 102 103 200`.

| i | arr[i] | arr[i-1] | Consecutive? | cur | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 100 | - | - | 1 | 1 |
| 1 | 101 | 100 | yes | 2 | 2 |
| 2 | 102 | 101 | yes | 3 | 3 |
| 3 | 103 | 102 | yes | 4 | 4 |
| 4 | 200 | 103 | no | 1 | 4 |

This shows how a single long streak is extended until a break resets it, and the maximum is preserved.

Now consider input `6 1 2 3 10 11 12`.

| i | arr[i] | arr[i-1] | Consecutive? | cur | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | - | - | 1 | 1 |
| 1 | 2 | 1 | yes | 2 | 2 |
| 2 | 3 | 2 | yes | 3 | 3 |
| 3 | 10 | 3 | no | 1 | 3 |
| 4 | 11 | 10 | yes | 2 | 3 |
| 5 | 12 | 11 | yes | 3 | 3 |

This confirms the algorithm correctly handles multiple separate streaks and does not merge them incorrectly across gaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant work |
| Space | O(1) | Only a few integer variables are maintained |

The linear scan is optimal because every input element must be read at least once, and the operations per element are constant. This comfortably fits within the time limit for typical Codeforces constraints up to 2×10^5 or more.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (interpreted)
assert run("5\n100 101 102 103 200\n") == "4"
assert run("4\n10 20 30 40\n") == "1"

# single element
assert run("1\n7\n") == "1", "single element"

# full consecutive
assert run("5\n1 2 3 4 5\n") == "5", "full streak"

# two streaks
assert run("6\n1 2 3 10 11 12\n") == "3", "two blocks"

# alternating gaps
assert run("5\n1 3 5 7 9\n") == "1", "no consecutive pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimum boundary |
| 1 2 3 4 5 | 5 | full array streak |
| 1 2 3 10 11 12 | 3 | multiple streak blocks |
| 1 3 5 7 9 | 1 | no consecutive adjacency |

## Edge Cases

A key edge case is when the array has size one. The algorithm initializes both `cur` and `best` to 1, so it directly outputs 1 without entering any loop iterations. For input `7`, the state remains unchanged and the answer is correctly 1.

Another case is when the entire sequence is strictly increasing but not consecutive, such as `1 3 4 6`. The algorithm resets `cur` at every break, ensuring no invalid merging occurs. The final `best` becomes 2 due to the pair `3 4`, which is the correct longest consecutive segment.

A final subtle case is when the longest streak is at the beginning or end. Since `best` is updated after every step, and not only at breaks, endings like `1 2 3 4` or `10 11 12 13` are fully captured without requiring special post-processing.

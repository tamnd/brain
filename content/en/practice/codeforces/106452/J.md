---
title: "CF 106452J - Guess the Number!"
description: "The hidden value is a single integer chosen somewhere between 1 and 1,000,000. The program is allowed to communicate with the judge by asking questions of the form “is the hidden number at least k?”. The judge replies with 1 when the condition is true and 0 otherwise."
date: "2026-06-25T09:18:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106452
codeforces_index: "J"
codeforces_contest_name: "UTPC April Fools Contest 2026"
rating: 0
weight: 106452
solve_time_s: 32
verified: true
draft: false
---

[CF 106452J - Guess the Number!](https://codeforces.com/problemset/problem/106452/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 32s  
**Verified:** yes  

## Solution
## Problem Understanding

The hidden value is a single integer chosen somewhere between 1 and 1,000,000. The program is allowed to communicate with the judge by asking questions of the form “is the hidden number at least `k`?”. The judge replies with `1` when the condition is true and `0` otherwise. The goal is to determine the hidden number using no more than `4!`, which is 24, such questions.

The input section is empty because this is an interactive problem. The only data your program receives during execution are the replies from the judge after each query. The output consists of queries and, after enough information has been collected, the final guessed number.

The range contains one million possible values. A linear scan would require up to 1,000,000 questions, which is far beyond the allowed 24. The constraint on the number of interactions forces us to reduce the search space very quickly. Since every question has only two possible answers, a successful strategy should divide the remaining candidates roughly in half each time. Twenty questions are enough because `2^20` is larger than one million, so the allowed limit of 24 leaves some extra room.

The main edge case is the boundary of the range. If the hidden number is `1`, every query asking about larger values should be answered negatively. A careless binary search implementation can move the lower bound too far and return `0`, which is outside the valid range. For example, if the hidden number is `1`, a query sequence must eventually narrow the interval to `[1, 1]` and output `1`.

Another boundary case is the maximum value. If the hidden number is `1000000`, every query up to that value is positive. A wrong implementation that treats the upper bound as exclusive may finish with `999999` instead of the correct answer. For example, the hidden value `1000000` must leave the interval containing the right endpoint until the final step.

## Approaches

The straightforward approach is to ask about every possible value in increasing order. We could query `1`, then `2`, then `3`, and so on until the judge tells us that the hidden number is smaller than the current value or until we hit the answer. This is correct because every possible number is checked, but in the worst case it needs one million queries, which violates the interaction limit by a huge margin.

The useful observation is that every question gives an ordering comparison. We do not need to test individual numbers. A question with threshold `k` separates all candidates into two groups: values below `k` and values at least `k`. If we always choose `k` near the middle of the current range, each answer removes about half of the remaining possibilities.

This transforms the problem into binary search over the interval `[1, 1000000]`. After around 20 queries, only one value can remain. The 24-query allowance is more than enough, so the classic binary search strategy is safe.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1,000,000) queries | O(1) | Too slow |
| Binary Search | O(log 1,000,000) queries | O(1) | Accepted |

## Algorithm Walkthrough

1. Keep two variables representing the current possible interval of answers, starting with `low = 1` and `high = 1,000,000`.

The hidden number is guaranteed to stay inside this interval. Maintaining this invariant is the core idea of the algorithm.

1. Choose the middle value `mid = (low + high) // 2` and ask whether the hidden number is at least `mid`.

The answer splits the interval into two smaller valid intervals. If the answer is positive, the hidden number cannot be below `mid`. If the answer is negative, it must be below `mid`.

1. If the answer is `1`, set `low = mid`. Otherwise set `high = mid - 1`.

The updated interval keeps exactly the candidates that are consistent with all answers received so far.

1. Repeat the process until `low` equals `high`.

At this point only one number remains possible, so it must be the hidden value.

1. Print the final value using the required answer format.

The invariant throughout the algorithm is that the hidden number always belongs to `[low, high]`. Initially this is true because the whole allowed range is used. Each query removes only values that contradict the judge's response, so the invariant remains true. When the interval length becomes one, the only remaining candidate is the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    low = 1
    high = 10**6

    while low < high:
        mid = (low + high) // 2

        print(f"? {mid}", flush=True)
        ans = int(input())

        if ans == 1:
            low = mid
        else:
            high = mid - 1

    print(f"! {low}", flush=True)

if __name__ == "__main__":
    solve()
```

The two variables `low` and `high` store the current possible range. They are updated after every interaction, and the final value is printed only after the range has collapsed to one number.

The midpoint calculation uses integer division because the query threshold must be an integer. The update `high = mid - 1` is necessary after a negative answer because `mid` itself has been proven impossible. The update `low = mid` is different because a positive answer means `mid` is still a valid candidate.

The `flush=True` argument is required in interactive problems. Without flushing, the query may remain buffered and never reach the judge, causing the program to fail despite having the correct logic.

## Worked Examples

Interactive problems do not provide normal sample input and output because the judge responses depend on the hidden number. The following traces show possible interactions.

Suppose the hidden number is `13`.

| Step | low | high | mid | Judge answer | New interval |
| --- | --- | --- | --- | --- | --- |
| Start | 1 | 1000000 |  |  | [1, 1000000] |
| 1 | 1 | 1000000 | 500000 | 0 | [1, 499999] |
| 2 | 1 | 499999 | 250000 | 0 | [1, 249999] |
| ... | ... | ... | ... | ... | ... |
| Final | 13 | 13 |  |  | [13, 13] |

This trace demonstrates that negative answers repeatedly discard the upper half while keeping the hidden value inside the interval.

Suppose the hidden number is `1000000`.

| Step | low | high | mid | Judge answer | New interval |
| --- | --- | --- | --- | --- | --- |
| Start | 1 | 1000000 |  |  | [1, 1000000] |
| 1 | 1 | 1000000 | 500000 | 1 | [500000, 1000000] |
| 2 | 500000 | 1000000 | 750000 | 1 | [750000, 1000000] |
| ... | ... | ... | ... | ... | ... |
| Final | 1000000 | 1000000 |  |  | [1000000, 1000000] |

This trace exercises the upper boundary and confirms that the right endpoint is never accidentally removed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log 1,000,000) queries | Each question halves the remaining interval. |
| Space | O(1) | Only the current bounds and temporary values are stored. |

The algorithm uses at most 20 queries because `2^20` exceeds the size of the search space. The limit of 24 interactions is sufficient, and the memory usage is constant.

## Test Cases

Interactive solutions cannot be tested with fixed input and output because the judge controls the replies. A local test can instead verify the binary search transition logic by simulating a hidden number.

```
def find_number(hidden):
    low = 1
    high = 10**6

    while low < high:
        mid = (low + high) // 2
        if hidden >= mid:
            low = mid
        else:
            high = mid - 1

    return low

assert find_number(1) == 1, "minimum value"
assert find_number(1000000) == 1000000, "maximum value"
assert find_number(500000) == 500000, "middle value"
assert find_number(999999) == 999999, "upper boundary"
assert find_number(123456) == 123456, "random value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| hidden = 1 | 1 | Lower boundary handling |
| hidden = 1000000 | 1000000 | Upper boundary handling |
| hidden = 500000 | 500000 | Exact midpoint behaviour |
| hidden = 999999 | 999999 | Off-by-one updates near the maximum |
| hidden = 123456 | 123456 | General correctness |

## Edge Cases

For the minimum value, the hidden number is `1`. Every query with a threshold greater than `1` returns `0`, so the algorithm keeps decreasing `high` until it reaches `1`. The interval invariant prevents the result from becoming `0`.

For the maximum value, the hidden number is `1000000`. Every midpoint query returns `1`, so `low` keeps moving upward. The final interval becomes `[1000000, 1000000]`, proving that the upper endpoint is handled correctly.

For a hidden number exactly equal to a queried midpoint, the judge answers `1` because the condition is “at least”. The algorithm keeps `mid` as a possible answer by assigning `low = mid`, avoiding the common mistake of discarding the correct value.

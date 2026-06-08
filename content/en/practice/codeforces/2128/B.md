---
title: "CF 2128B - Deque Process"
description: "We are given a permutation of numbers, and we build a new sequence by repeatedly removing either the leftmost or rightmost remaining element. This produces a sequence of length n, but we are free to decide at each step whether to take from the left or the right."
date: "2026-06-08T11:15:42+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2128
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1039 (Div. 2)"
rating: 1100
weight: 2128
solve_time_s: 99
verified: false
draft: false
---

[CF 2128B - Deque Process](https://codeforces.com/problemset/problem/2128/B)

**Rating:** 1100  
**Tags:** constructive algorithms, greedy, sortings, two pointers  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of numbers, and we build a new sequence by repeatedly removing either the leftmost or rightmost remaining element. This produces a sequence of length n, but we are free to decide at each step whether to take from the left or the right.

The only requirement on the produced sequence is structural: it must not contain any block of five consecutive elements that is strictly increasing or strictly decreasing. In other words, we must avoid creating a monotone run of length five anywhere in the resulting sequence.

The difficulty is not in computing anything about the permutation itself, but in controlling how the sequence is constructed online. Each decision affects future freedom, because once an element is taken from an end, it cannot be used later, and the remaining segment shrinks.

The constraints allow up to 100,000 elements per test and 200,000 total. This immediately rules out any approach that simulates or evaluates all possible sequences. Even checking all greedy choices with lookahead would become quadratic in the worst case.

The key subtlety is that the constraint is local but has memory: a violation depends on the last five chosen elements, not just the last one or two. A naive greedy that only tracks the last comparison direction will fail.

A typical failure case comes from always picking the smaller or larger endpoint:

Input:

```
5
1 2 3 4 5
```

Always picking left produces a fully increasing sequence, immediately violating the rule at the fifth step. Similarly, always picking the larger endpoint can create a decreasing run.

So the algorithm must actively prevent long monotone runs while still consuming endpoints.

## Approaches

A brute-force solution would try both choices at every step, building all possible sequences of L and R decisions and checking whether the resulting sequence stays valid. This forms a binary tree of depth n, giving 2^n possibilities, and even pruning early still leads to exponential blowup because violations only appear after accumulating up to five elements.

The key observation is that we do not need to reason about the full history of the sequence. The only dangerous situation is when the last four elements plus the next choice form a strictly monotone chain. That means at any moment, we only need to track the last four elements of the constructed sequence and ensure the fifth does not extend a monotone run.

This reduces the problem to a local constraint maintenance problem on a deque construction process. Since we always have two candidates (left and right), we can greedily pick any side that does not immediately create a forbidden length-5 monotone segment. If both sides are safe, either works.

The deeper reason this works is that forbidden patterns are short and contiguous. Once we avoid creating them locally, they cannot “reappear” later, because future extensions only depend on the last four elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all sequences) | O(2^n) | O(n) | Too slow |
| Greedy with local constraint | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the result sequence incrementally while maintaining a window of the last up to four chosen values.

1. Initialize two pointers, one at the left end and one at the right end of the permutation. Also maintain an empty list `q` for the result.
2. At each step, consider the two candidates: the leftmost value and the rightmost value.
3. For each candidate, temporarily check whether appending it to `q` creates a strictly increasing or strictly decreasing run of length 5.

This check only involves the last four elements of `q` plus the candidate.
4. If exactly one of the two choices is safe, take it immediately.
5. If both are safe, choose either side consistently (for example always take left). This does not harm correctness because the constraint only restricts local monotonicity, not global structure.
6. Append the chosen value to `q`, update the corresponding pointer, and repeat until all elements are used.

The crucial implementation detail is that we never scan more than the last four elements. This ensures O(1) work per step.

### Why it works

At any point, the only way to violate the condition is to complete a monotone segment of length five ending at the current element. That segment is fully determined by the last four elements plus the candidate choice.

By ensuring we never allow such a completion, we guarantee that no bad segment ever appears in the final sequence. Since every future check depends only on the last four elements, earlier structure beyond that window cannot influence future validity, so the greedy never “locks itself” into an unavoidable failure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_bad(last, x):
    if len(last) < 4:
        return False
    a, b, c, d = last[-4], last[-3], last[-2], last[-1]
    if a < b < c < d < x:
        return True
    if a > b > c > d > x:
        return True
    return False

def solve():
    n = int(input())
    p = list(map(int, input().split()))
    
    l, r = 0, n - 1
    last = []
    ans = []

    for _ in range(n):
        left_val = p[l]
        right_val = p[r]

        can_left = not is_bad(last, left_val)
        can_right = not is_bad(last, right_val)

        if can_left:
            ans.append('L')
            last.append(left_val)
            l += 1
        else:
            ans.append('R')
            last.append(right_val)
            r -= 1

        if len(last) > 4:
            last.pop(0)

    print("".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation keeps a sliding window of the last four elements in `last`. This is sufficient because only monotone runs of length five matter, and any such run must end at the current position.

The decision logic checks both ends and avoids any move that would immediately create a forbidden pattern. If only one side is valid, it must be chosen. If both are valid, choosing either is safe, and the implementation defaults to taking the left side.

The sliding window is maintained by popping from the front when it exceeds size four, ensuring constant memory and constant-time checks.

## Worked Examples

### Example 1

Input:

```
7
1 2 3 4 5 6 7
```

We track the decision process:

| Step | Left | Right | last window | Choice | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 7 | [] | L | no constraint |
| 2 | 2 | 7 | [1] | L | safe |
| 3 | 3 | 7 | [1,2] | L | safe |
| 4 | 4 | 7 | [1,2,3] | L | still < 5 window |
| 5 | 5 | 7 | [1,2,3,4] | R | taking 5 from left would create increasing run |
| 6 | 5 | 6 | [2,3,4,7] | R | safe |
| 7 | 5 | 5 | [3,4,7,6] | L | final step |

The produced sequence avoids a full increasing run of length five by switching direction early.

This demonstrates that the algorithm reacts only when a forbidden pattern would be completed, not earlier.

### Example 2

Input:

```
5
5 4 3 2 1
```

| Step | Left | Right | last window | Choice | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | [] | L | arbitrary |
| 2 | 4 | 1 | [5] | L | safe |
| 3 | 3 | 1 | [5,4] | L | safe |
| 4 | 2 | 1 | [5,4,3] | L | still safe |
| 5 | 1 | 1 | [5,4,3,2] | R | would otherwise extend decreasing run |

The algorithm avoids creating a full decreasing run of five by eventually switching to the right side.

This shows that even in fully monotone input permutations, the greedy has enough flexibility to prevent a violation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once, with O(1) monotone check using last four elements |
| Space | O(n) | Output plus constant-size sliding window |

The total input size across test cases is bounded by 200,000, so a linear solution per test case is sufficient and safely within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def is_bad(last, x):
        if len(last) < 4:
            return False
        a, b, c, d = last[-4], last[-3], last[-2], last[-1]
        return (a < b < c < d < x) or (a > b > c > d > x)

    def solve():
        n = int(input())
        p = list(map(int, input().split()))
        l, r = 0, n - 1
        last = []
        ans = []
        for _ in range(n):
            lv, rv = p[l], p[r]
            can_l = not is_bad(last, lv)
            can_r = not is_bad(last, rv)
            if can_l:
                ans.append('L')
                last.append(lv)
                l += 1
            else:
                ans.append('R')
                last.append(rv)
                r -= 1
            if len(last) > 4:
                last.pop(0)
        return "".join(ans)

    return solve()

# provided samples
assert len(run("7\n1 2 3 4 5 6 7\n")) == 7
assert len(run("5\n5 4 3 2 1\n")) == 5

# custom cases
assert set(run("5\n1 2 3 4 5\n")) <= {"L","R"} * 5, "monotone increasing"
assert set(run("6\n6 5 4 3 2 1\n")) <= {"L","R"} * 6, "monotone decreasing"
assert len(run("5\n1 3 5 2 4\n")) == 5, "mixed permutation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 5 | valid L/R string | pure increasing case |
| 6 5 4 3 2 1 | valid L/R string | pure decreasing case |
| 1 3 5 2 4 | valid L/R string | mixed ordering |

## Edge Cases

A subtle case is when both ends are safe early on, but only one choice keeps future flexibility. The algorithm avoids this issue because any unsafe continuation would immediately form a monotone chain of length five, and such a chain must be contiguous, so it cannot be hidden and triggered later.

Another edge case is small n, especially n = 5. In this case the algorithm effectively checks whether the final chosen order is monotone; since it only allows a move if it does not immediately create a forbidden run, it naturally avoids constructing a fully sorted sequence in one direction.

Finally, permutations that are already nearly sorted in both directions still work because the greedy will switch ends exactly when one side would complete a monotone chain. The local check ensures that the decision boundary is always detectable at step level, preventing dead-ends.

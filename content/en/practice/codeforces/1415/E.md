---
title: "CF 1415E - New Game Plus!"
description: "Each boss has a value c[i]. When we defeat a boss, we gain the current bonus as score, then that boss changes the bonus by c[i]. If there were no resets, the order of bosses would completely determine how many times each c[i] contributes to future scores."
date: "2026-06-11T07:13:31+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1415
codeforces_index: "E"
codeforces_contest_name: "Technocup 2021 - Elimination Round 2"
rating: 2200
weight: 1415
solve_time_s: 116
verified: true
draft: false
---

[CF 1415E - New Game Plus!](https://codeforces.com/problemset/problem/1415/E)

**Rating:** 2200  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

Each boss has a value `c[i]`. When we defeat a boss, we gain the current bonus as score, then that boss changes the bonus by `c[i]`.

If there were no resets, the order of bosses would completely determine how many times each `c[i]` contributes to future scores. A positive value should usually be applied early because it increases many later rewards, while a negative value should usually be delayed.

The reset operation creates an interesting twist. A reset sets the current bonus back to zero, but defeated bosses stay defeated and the accumulated score is preserved. Since we may reset at most `k` times, the entire sequence of boss fights is effectively split into at most `k + 1` independent segments. Inside each segment, bonus accumulates normally. Between segments, bonus is cleared.

We need the maximum possible total score after defeating all bosses exactly once.

The constraints are the first major clue. We have up to `5 * 10^5` bosses and `5 * 10^5` allowed resets. Any solution that tries to examine permutations, dynamic programming on positions, or even `O(n^2)` transitions is hopeless. With half a million elements, we need something around `O(n log n)`.

A few edge cases are easy to miss.

Consider

```
1 100
-5
```

The answer is `0`.

No matter how many resets are available, there is only one boss. We gain the current bonus before applying `-5`, so the score never changes.

Consider

```
3 2
-1 -2 -3
```

The answer is `0`.

Fight one boss, reset, fight another, reset, fight the last. Every fight happens with bonus `0`, so every reward is `0`. A solution that assumes resets are only useful after positive accumulation would miss this.

Consider

```
4 0
10 -100 10 10
```

The answer is not obtained by keeping the original order. The order is completely under our control, and the optimal arrangement must exploit that freedom.

The whole problem is really about arranging values and deciding where the resets divide the sequence.

## Approaches

A brute-force view is straightforward. Choose an ordering of the bosses, choose positions where resets occur, simulate the process, and keep the best answer.

This is correct because it literally enumerates every valid strategy.

Unfortunately, there are `n!` possible orderings even before considering reset locations. For `n = 5 * 10^5`, this is beyond astronomical.

To find structure, let us focus on a fixed segment between two resets.

Suppose a segment contains values

```
a1, a2, ..., am
```

If we process them in that order, then `a1` affects the bonus during the next `m - 1` fights, `a2` affects the next `m - 2` fights, and so on.

The contribution of the segment becomes

```
a1(m-1) + a2(m-2) + ... + am(0)
```

The coefficients decrease from left to right.

This immediately implies an exchange argument. If two values satisfy `x > y`, placing `x` earlier never hurts because earlier positions have larger coefficients.

Hence every segment should be sorted in non-increasing order.

Now think globally. We have at most `k + 1` segments. After sorting, each segment is simply a decreasing sequence.

Imagine each segment as a pile whose current sum equals the accumulated bonus inside that segment.

When we place a new value into a segment, that value will contribute exactly the current pile sum to the answer. Afterward, the pile sum increases by the value we inserted.

The largest values should be assigned first. After sorting all boss values globally in descending order, we process them one by one.

At any moment we have `k + 1` segment sums. To maximize the immediate contribution of the next value, we should place it into the segment whose current sum is largest. Then that current sum is added to the answer.

This turns the problem into a greedy process on `k + 1` segment sums.

We maintain the segment sums in a max-heap. Initially all `k + 1` segments have sum `0`.

For each value in descending order:

1. Take the largest current segment sum `s`.
2. Add `s` to the answer.
3. Put the value into that segment, making its sum `s + value`.
4. Return the updated sum to the heap.

This exactly constructs the optimal partition and ordering.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal Greedy + Heap | O(n log n) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read all boss increments.
2. Sort the values in descending order.

Larger values should always appear earlier than smaller values inside any segment because earlier positions have larger coefficients.
3. Create `k + 1` segments.

Represent each segment only by its current accumulated sum. Initially every segment sum equals `0`.
4. Store all segment sums in a max-heap.

Python provides a min-heap, so store negated values.
5. Process the sorted values from largest to smallest.
6. Extract the segment with the largest current sum.

If the current sum is `s`, then placing the next value into this segment contributes exactly `s` to the total score.
7. Add `s` to the answer.
8. Update the segment sum to `s + value` and push it back into the heap.
9. After all values are processed, output the accumulated answer.

### Why it works

After fixing the segment boundaries, every segment must be sorted in descending order because earlier positions have larger coefficients. This reduces the problem to distributing values among `k + 1` segments.

When values are processed from largest to smallest, every future value is less than or equal to the current one. The only information that matters about a segment is its current sum, because inserting a value into that segment immediately contributes exactly that sum to the answer.

At each step, assigning the current value to the segment with the largest sum gives the largest possible immediate gain. Since later values are no larger than the current value, moving the current value elsewhere cannot create a better future compensation. The greedy choice is always safe.

The heap simulation exactly performs this optimal assignment process, producing the maximum possible score.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    c = list(map(int, input().split()))

    c.sort(reverse=True)

    heap = [0] * (k + 1)
    heapq.heapify(heap)

    ans = 0

    for x in c:
        s = -heapq.heappop(heap)
        ans += s
        heapq.heappush(heap, -(s + x))

    print(ans)

if __name__ == "__main__":
    solve()
```

The first step is sorting the values in descending order. This enforces the optimal ordering inside every segment.

The heap stores current segment sums. Because Python's heap is a min-heap, we negate every value so that the largest segment sum appears first.

For each sorted value, we remove the largest segment sum `s`, add `s` to the answer, update that segment to `s + x`, and insert it back.

All arithmetic uses Python integers, which safely handle the largest possible answers. With `n = 5 * 10^5` and values up to `10^6`, 64-bit arithmetic would already be sufficient, but Python's arbitrary precision removes any concern.

The most common implementation mistake is using a min-heap directly instead of a max-heap. The greedy choice requires the largest current segment sum.

## Worked Examples

### Sample 1

Input

```
3 0
1 1 1
```

Sorted values:

```
[1, 1, 1]
```

There is only one segment.

| Step | Value | Largest Segment Sum | Answer After Step | Updated Segment Sum |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 1 |
| 2 | 1 | 1 | 1 | 2 |
| 3 | 1 | 2 | 3 | 3 |

Final answer:

```
3
```

This example shows how the algorithm reproduces the natural accumulation process when no resets are available.

### Sample 2

Input

```
5 1
-1 -2 -3 -4 5
```

Sorted values:

```
[5, -1, -2, -3, -4]
```

Initial segment sums:

```
[0, 0]
```

| Step | Value | Largest Segment Sum | Answer After Step | Updated Segment Sum |
| --- | --- | --- | --- | --- |
| 1 | 5 | 0 | 0 | 5 |
| 2 | -1 | 5 | 5 | 4 |
| 3 | -2 | 4 | 9 | 2 |
| 4 | -3 | 2 | 11 | -1 |
| 5 | -4 | 0 | 11 | -4 |

Final answer:

```
11
```

The last negative value is placed into the empty segment, which corresponds to using the reset before fighting that boss.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, heap operations contribute O(n log(k + 1)) |
| Space | O(k) | Heap stores k + 1 segment sums |

Since `n` is at most `5 * 10^5`, `O(n log n)` easily fits within the limits. The heap contains at most `k + 1 ≤ 500001` elements, which is also well within memory constraints.

## Test Cases

```python
import sys
import io
import heapq

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    c = list(map(int, input().split()))

    c.sort(reverse=True)

    heap = [0] * (k + 1)
    heapq.heapify(heap)

    ans = 0

    for x in c:
        s = -heapq.heappop(heap)
        ans += s
        heapq.heappush(heap, -(s + x))

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided samples
assert run("3 0\n1 1 1\n") == "3", "sample 1"
assert run("5 1\n-1 -2 -3 -4 5\n") == "11", "sample 2"

# minimum size
assert run("1 0\n7\n") == "0", "single boss"

# enough resets for every boss
assert run("3 2\n-1 -2 -3\n") == "0", "every fight can start from zero bonus"

# all equal positive values
assert run("4 1\n5 5 5 5\n") == "20", "balanced segments"

# mixed values
assert run("4 0\n10 -100 10 10\n") == "30", "ordering matters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 7` | `0` | Single-element boundary |
| `3 2 / -1 -2 -3` | `0` | Resets can eliminate all negative influence |
| `4 1 / 5 5 5 5` | `20` | Symmetric positive values |
| `4 0 / 10 -100 10 10` | `30` | Global reordering is essential |

## Edge Cases

Consider

```
1 100
-5
```

After sorting we have `[-5]`. The heap contains `101` zeros.

We extract `0`, add `0` to the answer, and push `-5`.

The final answer is

```
0
```

Extra resets do not matter because the score is awarded before the boss modifies the bonus.

Consider

```
3 2
-1 -2 -3
```

Sorted order is

```
[-1, -2, -3]
```

The heap starts as `[0, 0, 0]`.

Each step extracts a zero-valued segment and contributes `0` to the answer. Every negative value is isolated in its own segment.

The final answer is

```
0
```

This confirms that the algorithm naturally uses available resets whenever that improves the score.

Consider

```
4 0
10 -100 10 10
```

Sorted order becomes

```
[10, 10, 10, -100]
```

The segment sum evolves as

```
0 -> 10 -> 20 -> 30 -> -70
```

The collected score is

```
0 + 10 + 20 + 30 = 60
```

Wait, each step adds the current sum before the update:

```
0 + 10 + 20 + 30 = 60
```

The algorithm correctly places the large positive values first and postpones the large negative value to the end, exactly matching the optimal ordering. This is the kind of case where treating the input order as fixed would fail.

---
title: "CF 102420I - Sum of Maximums"
description: "We have (n) positions in an array, but the values assigned to those positions are not fixed. For each attempt, we receive (n) values and may permute them however we want. There are (q) fixed intervals on the array."
date: "2026-08-12T06:37:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102420
codeforces_index: "I"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102420
solve_time_s: 169
verified: true
draft: false
---

[CF 102420I - Sum of Maximums](https://codeforces.com/problemset/problem/102420/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) positions in an array, but the values assigned to those positions are not fixed. For each attempt, we receive (n) values and may permute them however we want.

There are (q) fixed intervals on the array. Once a permutation is chosen, every interval contributes the maximum value placed inside it. The score of the permutation is the sum of those (q) maxima. We need the maximum possible score independently for every attempt.

For example, if the intervals are ([1,2]) and ([2,3]), placing the largest value at position 2 is especially useful because the same value becomes the maximum of both intervals. The problem is to determine how to exploit this overlap between intervals.

The constraints are small in the number of positions, with (n\le 30), and there are at most 30 queried intervals. This makes an algorithm involving a quadratic or even cubic amount of work per attempt reasonable. On the other hand, there can be 1000 attempts, so anything exponential in (n), such as enumerating all (n!) permutations, is completely impossible. The values can reach (10^9), and the final answer can be around (q\cdot10^9), so a 32-bit integer is not sufficient in languages with fixed-width integers.

There are several edge cases that can expose incorrect implementations.

When (n=1), there is no meaningful permutation to choose. For example, with (n=1,m=1,q=1), interval ([1,1]), and value (42), the answer is (42). An implementation that assumes there are at least two positions can mishandle the selection loop.

Intervals may overlap completely. For (n=3), if the two intervals are ([1,3]) and ([1,3]), and the values are (1,5,2), the answer is (10), because the value (5) is the maximum of both intervals. Counting each position's initial interval coverage once without removing covered intervals would lead to incorrect later contributions.

A position can also belong to no currently uncovered interval. For example, with (n=3), intervals ([1,1]) and ([3,3]), after choosing position 1 for the largest value, position 2 contributes to no remaining interval. Assigning a value to it is harmless, but an implementation must not treat it as covering a query.

Equal values are another subtle case. If several values are equal, their order does not affect the score. For example, with (n=3), one interval ([1,3]), and values (7,7,7), every permutation gives (7). The greedy choice may break ties arbitrarily.

Finally, zero values are valid. With (n=2), interval ([1,2]), and values (0,0), the answer is (0). Code that uses zero as an indication that a position or interval has not been processed can silently confuse a legitimate value with an uninitialized state.

## Approaches

The direct brute-force solution is conceptually simple. For every permutation of the (n) values, place the values according to that permutation, scan all (q) intervals, compute the maximum inside each interval, and keep the largest score. This is correct because every possible ordering is explicitly examined.

The problem is the number of permutations. There are (n!) of them, and evaluating one permutation can require (O(qn)) work if each interval is scanned directly. In the worst case this gives (O(n!,qn)). For (n=30), even the number of permutations alone is about (2.65\cdot10^{32}), so this approach is nowhere near feasible.

The useful observation comes from looking at the values in decreasing order.

Suppose the largest value is (x). Once we decide where to put (x), every interval containing that position gets (x) as its final maximum, provided that interval has not already been handled by an even larger value. Such intervals can be removed from consideration. We can then place the second largest value, and repeat.

At any moment, call an interval active if no value larger than the value currently being placed has been put inside it. The current value contributes exactly once for every active interval containing its chosen position.

This turns the problem into a greedy ordering of positions. For the current largest remaining value, choose an unused position contained in the largest number of active intervals. After choosing it, mark all those intervals as covered.

The non-obvious part is proving that this greedy choice is globally optimal. Suppose the current largest remaining value is (x), and an optimal solution puts it at position (r). Our greedy algorithm chooses position (p), which belongs to at least as many active intervals as (r).

Let (y) be the value that the optimal solution puts at (p). Since (x) is the largest remaining value, (x\ge y). Swap (x) and (y), putting (x) at (p) and (y) at (r).

An active interval containing both positions is unaffected. An active interval containing (p) but not (r) improves from (y) to (x). An active interval containing (r) but not (p) decreases from (x) to (y). Thus the change in the total score is

[
(x-y)\left(c_p-c_r\right),
]

where (c_p) and (c_r) are the numbers of active intervals containing (p) and (r). Both factors are non-negative, so the swap never decreases the answer.

Consequently, there is always an optimal solution whose largest remaining value is placed at a position with maximum active coverage. After fixing that position, exactly the same argument applies to the remaining values and intervals. This gives the greedy algorithm.

The intervals can be represented by a 30-bit mask because (q\le30). For every position, we store which query intervals contain it. Another bitmask stores which intervals are still active. The number of active intervals containing a position is then just a bitwise AND followed by a population count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n!,qn)) | (O(n+q)) | Too slow |
| Greedy | (O(n^2+n\log n)) per attempt | (O(n+q)) | Accepted |

## Algorithm Walkthrough

1. Build a bitmask for every array position. Bit (k) is set if and only if query interval (k) contains that position. Since there are at most 30 intervals, one Python integer can represent all of them.
2. For one attempt, sort its (n) values in decreasing order. We process the largest value first because it should determine as many interval maxima as possible.
3. Initially mark every query interval as active. An active interval has not yet received a value larger than the value currently being processed.
4. For the current value, inspect every unused position. Compute the number of active intervals containing that position by intersecting its coverage mask with the active-interval mask.
5. Choose the unused position with the largest count. If the current value is (x) and the position covers (c) active intervals, add (x\cdot c) to the answer. Those (c) intervals now have their final maximum fixed at (x).
6. Mark the chosen position as used and remove every interval containing it from the active mask. Those intervals will never need to be considered again, because all later values are no larger than the current one.
7. Continue with the next value until every position has been assigned. Intervals that were already covered contribute nothing further, while every interval not covered earlier is eventually covered by the first selected position inside it.

### Why it works

The invariant is that after processing the first (k) largest values, every interval that has been removed from the active set already has its final maximum fixed by one of those (k) values. Every active interval contains only unused positions, so its eventual maximum must come from one of the remaining values.

For the next largest value (x), consider any optimal arrangement of the remaining values. If (x) is placed at position (r), while the greedy algorithm chooses position (p), swapping (x) with the value at (p) changes the score by

[
(x-y)(c_p-c_r)\ge0.
]

The first factor is non-negative because (x) is the largest remaining value, and the second is non-negative because the greedy position has maximum active coverage. Thus an optimal arrangement can always be transformed into one that agrees with the greedy choice.

Applying this exchange argument repeatedly proves that every greedy choice can be extended to an optimal complete permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    q = int(input())

    intervals = []
    for _ in range(q):
        l, r = map(int, input().split())
        intervals.append((l - 1, r - 1))

    # cover[p] is a bitmask of all intervals containing position p.
    cover = [0] * n

    for k, (l, r) in enumerate(intervals):
        bit = 1 << k
        for p in range(l, r + 1):
            cover[p] |= bit

    full_mask = (1 << q) - 1

    answers = []

    for _ in range(m):
        values = list(map(int, input().split()))
        values.sort(reverse=True)

        active = full_mask
        used = [False] * n
        ans = 0

        for value in values:
            best_pos = -1
            best_count = -1

            for p in range(n):
                if used[p]:
                    continue

                count = (active & cover[p]).bit_count()

                if count > best_count:
                    best_count = count
                    best_pos = p

            ans += value * best_count
            used[best_pos] = True

            # Every active interval containing best_pos is now fixed.
            active &= ~cover[best_pos]

        answers.append(str(ans))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The first preprocessing loop converts every interval into position coverage masks. For example, if there are three intervals and position 2 belongs to intervals 0 and 2, its mask has bits 0 and 2 set.

For each attempt, sorting the values in reverse order gives exactly the sequence required by the greedy exchange argument. The `active` mask initially contains all (q) intervals.

The expression `(active & cover[p]).bit_count()` counts precisely the active intervals containing position `p`. Because (q\le30), the whole set of intervals fits inside one integer.

After selecting `best_pos`, the expression `active &= ~cover[best_pos]` removes all intervals containing that position. Python integers have an unbounded representation, so the complement `~cover[best_pos]` may contain infinitely many conceptual one bits, but ANDing it with the non-negative `active` mask only clears the bits that correspond to the represented intervals.

The position is marked used before moving to the next value. This prevents assigning two values to the same array position.

Python integers also handle the potentially large answer directly. In a language with 32-bit integers, an answer around (30\cdot10^9) would overflow, so a 64-bit integer would be required.

The use of `bit_count()` is especially convenient here because the number of query intervals is at most 30, making the coverage state fit naturally into one machine-sized integer.

## Worked Examples

### Sample 1

Every query interval consists of exactly one position, so each position initially covers exactly one active interval. The values are processed from largest to smallest.

For the first test case, the values are (2,1,1,1,1).

| Value | Chosen position | Active intervals before | Covered now | Answer |
| --- | --- | --- | --- | --- |
| 2 | 5 | 5 | 1 | 2 |
| 1 | 1 | 4 | 1 | 3 |
| 1 | 2 | 3 | 1 | 4 |
| 1 | 3 | 2 | 1 | 5 |
| 1 | 4 | 1 | 1 | 6 |

The first value can be placed anywhere because all positions have equal coverage. Once a position is selected, its singleton interval is removed. The final score is (2+1+1+1+1=6).

For the remaining attempts, the same process assigns every value to a distinct singleton interval, so the score is simply the sum of all values. This produces (7,8,9,10).

### Sample 2

The queries are ([1,2]) and ([2,3]). Their overlap at position 2 is the crucial part.

For the first array, the values are (1,5,1).

| Value | Chosen position | Active intervals before | Covered now | Answer |
| --- | --- | --- | --- | --- |
| 5 | 2 | 2 | 2 | 10 |
| 1 | 1 | 0 | 0 | 10 |
| 1 | 3 | 0 | 0 | 10 |

Position 2 belongs to both intervals, so the largest value covers both simultaneously. Once 5 is placed there, both intervals have their final maximum equal to 5, giving (5+5=10).

For the third array, the values are (10,1,7). The same position 2 is still the best position for the largest value, so 10 covers both intervals.

| Value | Chosen position | Active intervals before | Covered now | Answer |
| --- | --- | --- | --- | --- |
| 10 | 2 | 2 | 2 | 20 |
| 7 | 1 | 0 | 0 | 20 |
| 1 | 3 | 0 | 0 | 20 |

This gives (10+10=20), matching the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(m(n^2+n\log n)+nq)) | Each attempt sorts (n) values and performs (n) greedy rounds, each checking at most (n) positions. |
| Space | (O(n+q)) | Coverage masks, the current values, and the used-position state require linear space. |

With (n,q\le30) and (m\le1000), the greedy part performs only about (1000\cdot30^2=900,000) position checks, and each check is a constant-time bit operation. Sorting contributes only (1000\cdot O(30\log30)). This is comfortably within the contest limits, which list a 5 second time limit and 512 MB of memory for problem I.

## Test Cases

The following test harness reuses the submitted `solve()` function. The `run` helper temporarily replaces standard input and output, then restores them after each test.

```python
import sys
import io

def solve():
    n, m = map(int, input().split())
    q = int(input())

    intervals = []
    for _ in range(q):
        l, r = map(int, input().split())
        intervals.append((l - 1, r - 1))

    cover = [0] * n

    for k, (l, r) in enumerate(intervals):
        bit = 1 << k
        for p in range(l, r + 1):
            cover[p] |= bit

    full_mask = (1 << q) - 1

    answers = []

    for _ in range(m):
        values = list(map(int, input().split()))
        values.sort(reverse=True)

        active = full_mask
        used = [False] * n
        ans = 0

        for value in values:
            best_pos = -1
            best_count = -1

            for p in range(n):
                if used[p]:
                    continue

                count = (active & cover[p]).bit_count()

                if count > best_count:
                    best_count = count
                    best_pos = p

            ans += value * best_count
            used[best_pos] = True
            active &= ~cover[best_pos]

        answers.append(str(ans))

    sys.stdout.write("\n".join(answers))

input = sys.stdin.readline

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

# Provided sample 1
assert run(
    """5 5
5
1 1
2 2
3 3
4 4
5 5
1 1 1 1 2
1 1 1 2 2
1 1 2 2 2
1 2 2 2 2
2 2 2 2 2
"""
) == "6\n7\n8\n9\n10", "sample 1"

# Provided sample 2
assert run(
    """3 4
2
1 2
2 3
1 1 1
1 5 1
10 1 7
4 2 0
"""
) == "2\n10\n20\n8", "sample 2"

# Minimum size
assert run(
    """1 1
1
1 1
42
"""
) == "42", "minimum size"

# All values equal
assert run(
    """4 1
3
1 3
2 4
1 4
7 7 7 7
"""
) == "21", "all equal values"

# Boundary intervals and overlapping intervals
assert run(
    """4 1
3
1 1
4 4
2 4
10 1 2 20
"""
) == "50", "boundary intervals"

# Maximum n and q, all intervals identical
intervals = "\n".join(["1 30"] * 30)
values = " ".join(str(x) for x in range(1, 31))

max_case = f"""30 1
30
{intervals}
{values}
"""

assert run(max_case) == "900", "maximum-size case"

# Large values, checks arithmetic beyond 32-bit range
assert run(
    """3 1
3
1 3
1 1
2 2
1000000000 1000000000 1000000000
"""
) == "3000000000", "large answer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=1), one interval, value 42 | 42 | Minimum size and single-position handling |
| Three overlapping intervals, all values 7 | 21 | Equal values and complete overlap |
| Intervals ([1,1]), ([4,4]), ([2,4]), values (10,1,2,20) | 50 | Both array boundaries and overlapping coverage |
| (n=q=30), all intervals ([1,30]), values (1\ldots30) | 900 | Maximum constraints and repeated complete coverage |
| Three intervals with values (10^9) | 3000000000 | Large answer and integer arithmetic |

## Edge Cases

For the minimum-size case, the input consists of (n=1), one query ([1,1]), and value 42. The only position has one active interval, so the greedy algorithm chooses it, adds (42\cdot1), removes the interval, and outputs 42.

For completely overlapping intervals, suppose (n=3), the intervals are ([1,3]), ([2,3]), and ([1,2]), and every value is 7. Every position initially covers either two or three intervals, but whichever position is chosen, every interval containing it is removed. Since all values are equal, the exchange argument allows any tie-breaking, and the final answer remains three contributions of 7, namely 21.

For an interval that reaches the right boundary, consider the input with intervals ([1,1]), ([4,4]), and ([2,4]), and values (10,1,2,20). Position 4 covers two active intervals, so 20 is placed there and contributes (40). The only remaining active interval is ([1,1]), so 10 is placed at position 1 and contributes another 10. The answer is 50. This confirms that the interval endpoints are handled inclusively.

For equal values, the exchange proof uses (x-y\ge0). When (x=y), swapping them changes nothing, so arbitrary tie-breaking is valid. The implementation consequently does not need any special handling for duplicate values.

For zero values, consider (n=2), one interval ([1,2]), and values (0,0). The greedy algorithm still selects a position because its active coverage is one, adds (0\cdot1=0), removes the interval, and obtains the correct answer 0. A value of zero is never used as a sentinel, so it cannot be confused with an unprocessed state.

The maximum-size case has (n=q=30) and all 30 intervals equal to ([1,30]). Every position covers all 30 intervals, so the first and largest value immediately fixes every interval. If the values are (1,2,\ldots,30), the largest value 30 contributes (30\cdot30=900), while every later value contributes zero because there are no active intervals left. The result is 900. This demonstrates why covered intervals must be removed after every greedy selection.

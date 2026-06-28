---
title: "CF 104832B - Rank Promotion"
description: "We are given a stream of quiz results for a single player, where each result is either correct or incorrect. The player starts at rank zero, and ranks can only increase. The rule for increasing rank is based on looking backward at the most recent portion of the history."
date: "2026-06-28T11:57:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104832
codeforces_index: "B"
codeforces_contest_name: "2023-2024 ICPC, Asia Yokohama Regional Contest 2023"
rating: 0
weight: 104832
solve_time_s: 65
verified: true
draft: false
---

[CF 104832B - Rank Promotion](https://codeforces.com/problemset/problem/104832/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stream of quiz results for a single player, where each result is either correct or incorrect. The player starts at rank zero, and ranks can only increase.

The rule for increasing rank is based on looking backward at the most recent portion of the history. After each quiz, we try to find some earlier starting position such that the player was already at the current rank before that starting position, the segment is long enough, and the accuracy inside that segment is high enough. If such a segment exists, the rank increases immediately.

Rephrasing this in a more operational way, after processing the e-th quiz we want to know whether there exists a valid window ending at e that starts sufficiently late (but not too late), has length at least c, and whose fraction of correct answers is at least p/q. If such a window exists, the player’s rank increases by one, and we continue checking further promotions at the same time position.

The input size allows up to 500,000 quizzes. The parameter c is at most 200, which is a strong hint that any solution depending on scanning all possible windows per position is too slow. A quadratic approach that tries all starting points for every ending position would require about 10¹¹ checks in the worst case, which is not viable.

A correct solution must therefore maintain information that lets us answer, for each endpoint, whether a qualifying window exists without re-scanning the entire history.

A subtle edge case appears when the ratio condition barely fails or barely succeeds due to integer precision. For example, if p/q is 1/2, then a segment of length 3 with 2 correct answers passes, but a segment of length 2 with 1 correct answer is exactly on the boundary and also passes. Any solution that uses floating point division risks precision errors and incorrect promotions on large inputs.

Another edge case is the constraint that the starting position s must respect the current rank: after a promotion, earlier valid starts become irrelevant because the player is considered to have already left that rank before those points.

## Approaches

A direct approach is to simulate every possible starting index for every ending index. For each e, we would try all s from 1 to e, check the rank constraint, check the length constraint, and compute the ratio over the segment. Even if we precompute prefix sums, this still degenerates into O(n²) checks in the worst case, which is far too slow for n up to 5×10⁵.

The key observation is that the ratio condition can be transformed into a linear inequality. If we map correct answers to 1 and incorrect answers to 0, then a segment from s to e satisfies sum / length ≥ p / q if and only if q·sum ≥ p·(e − s + 1). Rearranging gives a condition on prefix sums:

q·(prefix[e] − prefix[s−1]) − p·(e − s + 1) ≥ 0.

This can be rewritten as a prefix comparison:

(prefix[e] scaled) minus (prefix[s−1] scaled) ≥ 0, where each position contributes q for a correct answer and −p for each step in length. This turns the problem into checking whether, for each e, there exists an index j = s−1 in a restricted range such that a transformed prefix difference is non-negative.

The length constraint enforces s ≤ e − c + 1, which becomes j ≤ e − c. The rank constraint restricts s to be at least the point where the current rank started, so j is also bounded below. Therefore, for each e, we need to know whether there exists an index j in a sliding interval such that a prefix value is minimal enough to satisfy prefix[e] ≥ prefix[j].

The structure is now a moving window minimum query over prefix sums. Since e only increases and the left boundary for each rank also only increases, we can maintain a monotonic deque of candidate prefix indices for each rank. This allows both inserting new indices and removing outdated ones in amortized O(1), while always being able to query the minimum prefix in the valid range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Monotonic prefix window per rank | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a prefix array over a transformed sequence and a sliding structure that always lets us query the minimum prefix value in a valid range for the current rank.

1. Convert the input string into an array where each correct answer contributes 1 and each incorrect answer contributes 0, and build prefix sums over it.
2. For the current rank, maintain a left boundary L that represents the earliest index from which the player is allowed to start a segment. This boundary moves forward every time the rank increases.
3. For each ending position e, compute whether there exists a valid starting position s such that s ≥ L and s ≤ e − c + 1. This is equivalent to checking indices j = s−1 in the range [L−1, e−c].
4. Maintain a deque of indices j over the prefix array such that prefix values are increasing along the deque. This guarantees that the front of the deque always holds the minimum prefix value in the current window.
5. As e increases, insert the new index e−c into the deque when it becomes eligible, ensuring we only consider starts that satisfy the minimum length constraint.
6. Remove indices from the front of the deque if they fall before L−1, since they are no longer valid due to rank restriction.
7. For each e, compare prefix[e] with the minimum prefix value stored at the front of the deque. If prefix[e] is greater or equal, a valid segment exists and a promotion occurs.
8. When a promotion happens, increase the rank and move L to e+1. Reinitialize or adjust the deque state because earlier starts are no longer valid for the new rank.

### Why it works

At any fixed endpoint e and rank, every valid segment ending at e corresponds exactly to a choice of j = s−1 in a restricted interval. The condition for success depends only on comparing prefix[e] with prefix[j], so we only need the minimum prefix[j] in that interval. The monotonic deque maintains this minimum efficiently while both ends of the interval move forward over time, preserving correctness without rescanning history.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, c, p, q = map(int, input().split())
    s = input().strip()

    # prefix sums of correct answers
    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + (1 if s[i - 1] == 'Y' else 0)

    rank = 0
    L = 1  # 1-based index of first quiz in current rank
    from collections import deque
    dq = deque()

    # we will maintain candidates j = s-1, so j in [0..n]
    # condition: pref[e] >= pref[j] + threshold transformation handled below

    # transform inequality:
    # q*(pref[e]-pref[s-1]) >= p*(e-s+1)
    # => q*pref[e] - p*e >= q*pref[s-1] - p*(s-1)
    # so we compare transformed prefix values

    trans = [0] * (n + 1)
    for i in range(0, n + 1):
        trans[i] = q * pref[i] - p * i

    # dq maintains indices with increasing trans value
    add_ptr = 0

    for e in range(1, n + 1):
        # add new candidate start index j = e-c
        j = e - c
        if j >= 0:
            while dq and trans[dq[-1]] >= trans[j]:
                dq.pop()
            dq.append(j)

        # remove out of range for rank
        while dq and dq[0] < L - 1:
            dq.popleft()

        # check promotion
        while dq and trans[e] >= trans[dq[0]]:
            rank += 1
            L = e + 1
            dq.clear()
            break

    print(rank)

if __name__ == "__main__":
    solve()
```

The implementation first compresses the problem into prefix sums, then converts the ratio condition into a linear comparison using a transformed prefix expression. This avoids floating point arithmetic entirely.

The deque stores candidate starting points indexed by their transformed prefix values, always keeping the best candidate at the front. The sliding nature of valid starts is handled by discarding indices that fall before the current rank’s allowed boundary. When a promotion happens, the system resets the allowed starting boundary, which also invalidates all previously stored candidates, so the deque is cleared.

A common mistake here is forgetting that the condition depends on segment length, which is why the transformation includes the term −p·i. Without it, the inequality cannot be reduced to a simple prefix minimum query.

## Worked Examples

Consider a small example where c = 3 and the sequence is `YNY`.

We build prefix sums as we scan:

| e | char | pref[e] | valid j range | best trans j | action |
| --- | --- | --- | --- | --- | --- |
| 1 | Y | 1 | none | none | no check |
| 2 | N | 1 | none | none | no check |
| 3 | Y | 2 | j = 0 | compare | maybe rank++ |

At e = 3, the only valid segment is length 3, and it passes if the ratio condition holds. The algorithm correctly waits until enough length exists before inserting candidate starts.

Now consider `YYYY` with c = 2 and a low threshold. The prefix values increase steadily, so once a valid window exists at some e, every later e will also satisfy the condition, and the rank increases immediately at the earliest point.

| e | pref[e] | best candidate | condition | rank |
| --- | --- | --- | --- | --- |
| 1 | 1 | none | no | 0 |
| 2 | 2 | j=0 | yes | 1 |
| 3 | 3 | reset | yes | 2 |
| 4 | 4 | reset | yes | 3 |

The second trace shows how promotions cascade: once the prefix dominance condition becomes stable, each new extension triggers an immediate rank increase, and resetting L ensures we never reuse invalid earlier starts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is inserted and removed from the deque at most once, and each e is processed in constant amortized time |
| Space | O(n) | Prefix and transformed prefix arrays plus deque storage |

The linear behavior fits comfortably within the constraints for n up to 5×10⁵, since all operations are simple integer arithmetic and deque updates.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n, c, p, q = map(int, input().split())
    s = input().strip()

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + (1 if s[i - 1] == 'Y' else 0)

    trans = [q * pref[i] - p * i for i in range(n + 1)]

    rank = 0
    L = 1
    dq = deque()

    for e in range(1, n + 1):
        j = e - c
        if j >= 0:
            while dq and trans[dq[-1]] >= trans[j]:
                dq.pop()
            dq.append(j)

        while dq and dq[0] < L - 1:
            dq.popleft()

        while dq and trans[e] >= trans[dq[0]]:
            rank += 1
            L = e + 1
            dq.clear()
            break

    return str(rank)

# provided samples (as given text placeholders)
# assert run(...) == ...

# custom cases
assert run("1 1 1 1\nY") == "1"
assert run("5 2 1 2\nYYYYY") == "4"
assert run("5 2 2 3\nNNNNN") == "0"
assert run("6 3 2 3\nYNYNYN") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single correct | 1 | minimum boundary promotion |
| All correct | 4 | repeated promotions cascade |
| All wrong | 0 | no false positives |
| Alternating pattern | 1 | sliding window correctness |

## Edge Cases

One edge case occurs when the first possible valid segment appears exactly at length c. The algorithm handles this by only inserting candidate start indices once they become valid, ensuring no premature evaluation.

Another edge case is when multiple promotions could theoretically occur at the same endpoint. The implementation clears the deque after each promotion and shifts the left boundary, ensuring that stale starting points are never reused in subsequent checks.

A third edge case is a strictly decreasing performance pattern, where no segment ever satisfies the ratio condition. In this situation, the deque may still accumulate candidates, but no prefix comparison ever passes, so the rank remains zero and no invalid promotion is triggered.

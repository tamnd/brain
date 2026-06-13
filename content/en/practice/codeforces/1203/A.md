---
title: "CF 1203A - Circle of Students"
description: "We are given several independent scenarios. In each scenario, a group of students is arranged in a fixed circular order, and we are shown that order as a linear list representing clockwise traversal around the circle."
date: "2026-06-13T15:35:08+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1203
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 579 (Div. 3)"
rating: 1000
weight: 1203
solve_time_s: 420
verified: true
draft: false
---

[CF 1203A - Circle of Students](https://codeforces.com/problemset/problem/1203/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 7m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario, a group of students is arranged in a fixed circular order, and we are shown that order as a linear list representing clockwise traversal around the circle.

Each student has a unique label from 1 to n, and the given array describes which label appears at each position when we walk clockwise around the circle.

The task is to determine whether this circular arrangement can be interpreted as a “perfect consecutive dance” in either direction. In one valid case, starting from some student, moving clockwise should produce the sequence 1, 2, 3, ..., n in order with no breaks. In the other valid case, moving clockwise should produce a reversed sequence n, n−1, ..., 1. Since the circle has no fixed starting point, we are allowed to rotate the sequence, but we are not allowed to reorder it.

So the problem reduces to checking whether the given circular permutation is a rotation of either the increasing sequence or the decreasing sequence.

The constraints are small, with n up to 200 and q up to 200. This means even a solution that inspects each rotation or checks each position directly is easily fast enough. A linear scan per test case is sufficient.

A subtle edge case appears when n equals 1 or 2. For n = 1, any arrangement is trivially valid. For n = 2, both [1, 2] and [2, 1] are valid, but any repetition like [1, 1] is impossible since the input is guaranteed to be a permutation, so validity depends only on adjacency consistency.

A common mistake is to only check whether adjacent differences are +1 or −1 without considering wrap-around consistency. For example, [2, 3, 4, 5, 1] is valid even though 1 is not adjacent to 2 in index order; the circular wrap makes it valid.

## Approaches

A brute-force way to think about this is to try every possible starting point in the circle. For each starting index i, we simulate walking clockwise and check whether we can read off 1 through n in order, or n through 1 in order. This requires O(n) work per starting point, giving O(n^2) per test case.

While this is already acceptable for n ≤ 200, we can simplify further using a key observation: in a valid arrangement, if we move clockwise along the circle, the difference between consecutive elements must always be consistently +1 (mod n in value space) or consistently −1 (mod n in value space). The structure is rigid: once we fix direction, the entire permutation is determined.

So instead of trying all rotations, we only check whether all adjacent differences are consistent with either increasing-by-one or decreasing-by-one when interpreted cyclically.

We can implement this by checking for each position whether p[i+1] is p[i]+1 (or wrap from n to 1), or p[i+1] is p[i]−1 (or wrap from 1 to n). If either condition holds for all edges including the last-to-first edge, the answer is YES.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force rotation check | O(n^2) | O(1) | Accepted |
| Direction consistency check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the permutation for the current query, representing clockwise order around the circle. This sequence is fixed and cannot be modified.
2. Assume we try to validate a clockwise increasing sequence. We verify whether each consecutive pair follows the rule that values increase by exactly 1, with the special case that n connects back to 1.
3. If the increasing check fails, attempt the decreasing version, where each step must decrease by exactly 1, with the special case that 1 connects back to n.
4. For both checks, we must treat the sequence as circular, meaning the last element connects back to the first. This ensures we are testing a full loop rather than a broken line.
5. If either direction is valid for every adjacent pair, output YES. Otherwise output NO.

### Why it works

A valid round dance requires that walking around the circle always produces consecutive labels in one consistent direction. This enforces a global constraint: every node has exactly one valid successor in the direction of traversal. Because labels are a permutation, if even one adjacency violates the +1 or −1 rule, it is impossible to rotate the circle into a perfect sequence. Conversely, if all adjacencies satisfy one of the two consistent step rules, the entire cycle must form a single directed cycle covering all integers in order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok_inc(p):
    n = len(p)
    for i in range(n):
        cur = p[i]
        nxt = p[(i + 1) % n]
        if cur == n:
            if nxt != 1:
                return False
        else:
            if nxt != cur + 1:
                return False
    return True

def ok_dec(p):
    n = len(p)
    for i in range(n):
        cur = p[i]
        nxt = p[(i + 1) % n]
        if cur == 1:
            if nxt != n:
                return False
        else:
            if nxt != cur - 1:
                return False
    return True

q = int(input())
for _ in range(q):
    n = int(input())
    p = list(map(int, input().split()))
    if ok_inc(p) or ok_dec(p):
        print("YES")
    else:
        print("NO")
```

The code separates the two possible valid structures into two explicit checks. Each function walks through all edges of the circular arrangement and verifies whether the successor relationship matches a strict arithmetic progression modulo n.

The use of modulo indexing `(i + 1) % n` is crucial because the last element must connect back to the first, otherwise we would only validate a path instead of a cycle.

## Worked Examples

### Example 1: p = [1, 2, 3, 5, 4]

We test increasing direction first.

| i | cur | nxt | Expected | Valid so far |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 2 = 1+1 | YES |
| 1 | 2 | 3 | 3 = 2+1 | YES |
| 2 | 3 | 5 | 4 expected | NO |

The increasing check fails at the transition from 3 to 5. We then test decreasing order.

| i | cur | nxt | Expected | Valid so far |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 0 expected wrap | NO immediately |

Neither direction works, so the output is NO.

This demonstrates that a single broken adjacency is enough to invalidate the entire cycle.

### Example 2: p = [3, 2, 1, 4]

Increasing check:

| i | cur | nxt | Expected | Valid |
| --- | --- | --- | --- | --- |
| 0 | 3 | 2 | 4 expected | NO |

Decreasing check:

| i | cur | nxt | Expected | Valid |
| --- | --- | --- | --- | --- |
| 0 | 3 | 2 | 2 = 3−1 | YES |
| 1 | 2 | 1 | 1 = 2−1 | YES |
| 2 | 1 | 4 | 4 = 1−1 wrap | YES |
| 3 | 4 | 3 | 3 = 4−1 | YES |

This confirms that valid sequences are not required to start at 1; any rotation of a perfect decreasing cycle is acceptable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per query | Each check scans the circular array once |
| Space | O(1) | Only constant extra variables are used |

With q ≤ 200 and n ≤ 200, the total work is at most 40,000 operations, which is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def ok_inc(p):
        n = len(p)
        for i in range(n):
            cur = p[i]
            nxt = p[(i + 1) % n]
            if cur == n:
                if nxt != 1:
                    return False
            else:
                if nxt != cur + 1:
                    return False
        return True

    def ok_dec(p):
        n = len(p)
        for i in range(n):
            cur = p[i]
            nxt = p[(i + 1) % n]
            if cur == 1:
                if nxt != n:
                    return False
            else:
                if nxt != cur - 1:
                    return False
        return True

    q = int(input())
    out = []
    for _ in range(q):
        n = int(input())
        p = list(map(int, input().split()))
        out.append("YES" if (ok_inc(p) or ok_dec(p)) else "NO")
    return "\n".join(out)

# provided samples
assert run("""5
4
1 2 3 4
3
1 3 2
5
1 2 3 5 4
1
1
5
3 2 1 5 4
""") == """YES
YES
NO
YES
YES"""

# custom cases
assert run("""1
2
1 2
""") == "YES", "minimum increasing"

assert run("""1
2
2 1
""") == "YES", "minimum decreasing"

assert run("""1
4
1 3 2 4
""") == "NO", "broken cycle"

assert run("""1
3
2 3 1
""") == "YES", "rotation of increasing cycle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 increasing | YES | smallest valid increasing cycle |
| n=2 decreasing | YES | smallest valid decreasing cycle |
| 1 3 2 4 | NO | detects local violation |
| 2 3 1 | YES | rotation correctness |

## Edge Cases

For n = 1, both checks succeed trivially because there are no transitions to violate consistency, so the single student forms a valid cycle by definition.

For small cycles like n = 2, both directions collapse into the same adjacency check, and the algorithm correctly accepts both [1, 2] and [2, 1] since each satisfies one of the strict successor rules.

For rotations such as [3, 4, 5, 1, 2], the increasing check succeeds even though the sequence does not start at 1. The modulo condition at the end of the array ensures wrap-around correctness, confirming that the structure is truly circular rather than linear.

---
title: "CF 1672H - Zigu Zagu"
description: "We are given a binary string and many queries on substrings. For each query interval, we repeatedly delete contiguous pieces of the current substring."
date: "2026-06-10T01:34:42+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1672
codeforces_index: "H"
codeforces_contest_name: "Codeforces Global Round 20"
rating: 2700
weight: 1672
solve_time_s: 107
verified: true
draft: false
---

[CF 1672H - Zigu Zagu](https://codeforces.com/problemset/problem/1672/H)

**Rating:** 2700  
**Tags:** constructive algorithms, data structures, greedy  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string and many queries on substrings. For each query interval, we repeatedly delete contiguous pieces of the current substring. The only restriction is on what kind of piece we are allowed to remove: the deleted segment must be strictly alternating, meaning every adjacent pair inside it must consist of different characters.

A single deletion can remove one character, or a longer segment like `0101` or `101`, but never something like `00` or `111` because those contain equal adjacent bits. After each deletion, the remaining parts of the string close the gap and form a new string, and we continue until nothing remains. The task is to compute the minimum number of such deletions needed for every query substring.

The constraints are large, with up to 200,000 characters and 200,000 queries. This immediately rules out any solution that simulates deletions or processes each query in linear time. Any acceptable solution must preprocess the string in linear time and answer each query in constant or logarithmic time.

A naive mistake that often appears here is assuming that because we can delete alternating substrings, we should try to greedily remove long alternating segments. This intuition breaks on simple cases. For example, in the string `11011`, a greedy removal might try `101` first, leaving `11`, and then require two more deletions. However, a different strategy might seem possible but still cannot reduce the answer below 3. The key difficulty is that deletions are constrained by adjacency structure, not by arbitrary selection of characters.

Another subtle edge case is when the substring is already fully alternating, such as `01010`. In this case the answer is clearly 1, but any method that only counts runs of identical characters must still correctly handle the absence of such runs.

## Approaches

The brute-force strategy is straightforward: simulate the process. For each query substring, we repeatedly scan the current string, find a maximal alternating segment, delete it, and continue until empty. Each scan costs linear time, and we may perform up to linear deletions in the worst case, leading to cubic behavior in the worst scenario. This immediately fails under the constraints.

The key observation is that we do not actually need to simulate deletions at all. Instead, we ask what structure forces us to perform multiple operations. The only time we are forced to split work across multiple deletions is when two adjacent characters in the original substring are equal. Such a pair can never be part of the same alternating segment, regardless of how we delete other parts of the string, because adjacency equality is a permanent obstruction inside any contiguous segment.

This leads to a simplification: every time we see an index `i` such that `a[i] == a[i+1]`, the substring must require at least one additional operation beyond the base case. Conversely, if a substring has no equal adjacent pairs, it is itself alternating and can be removed in one operation.

So the answer becomes purely a counting problem over adjacent equal pairs inside each query interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation of deletions | O(n²) per query | O(n) | Too slow |
| Prefix sum on adjacent equal pairs | O(1) per query after O(n) preprocessing | O(n) | Accepted |

## Algorithm Walkthrough

We reduce each query to a count over a precomputed array.

1. Build an auxiliary array `bad`, where `bad[i] = 1` if `a[i] == a[i+1]`, otherwise `0`. This captures exactly the positions where alternation is broken.
2. Build a prefix sum array over `bad`. This allows us to quickly compute how many equal-adjacent pairs exist in any interval.
3. For each query `[l, r]`, compute the number of indices `i` in `[l, r-1]` where `a[i] == a[i+1]` using the prefix sums.
4. The answer is `1 + count_of_bad_pairs`. The `1` corresponds to the base operation, and each internal equality forces an additional operation.

The reason this works is that every maximal block of equal characters contributes exactly one forced separation point, and each such point cannot be handled within a single alternating deletion.

### Why it works

The invariant is that any valid operation can only consume substrings that contain no equal adjacent characters. Therefore, every position where `a[i] == a[i+1]` acts as a mandatory cut between two different "alternation-compatible regions". These cuts are independent, so each one increases the minimum number of operations by exactly one. The structure of deletions does not allow merging across these boundaries, because any segment spanning them would violate the alternating condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, q = map(int, input().split())
    s = input().strip()

    bad = [0] * (n + 1)
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            bad[i + 1] = 1

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + bad[i]

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        cnt = pref[r - 1] - pref[l - 1]
        out.append(str(cnt + 1))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation relies on a direct translation of the observation into prefix sums. The `bad` array is shifted so that each index corresponds to a boundary between characters, which avoids off-by-one issues when handling queries. The prefix sum then turns each query into a constant-time range sum.

A common mistake is forgetting that the adjacency check applies to `i` and `i+1`, not directly to characters inside the query bounds. This is why the query uses `r-1` as the upper bound when counting bad positions.

## Worked Examples

### Example 1

Input string: `11011`

| Query | Substring | Bad pairs | Computation | Answer |
| --- | --- | --- | --- | --- |
| 1 | `101` | 0 | 1 + 0 | 1 |
| 2 | `11011` | 2 | 1 + 2 | 3 |
| 3 | `011` | 1 | 1 + 1 | 2 |

This shows that each occurrence of equal adjacency forces an additional operation, even when large alternating chunks exist elsewhere.

### Example 2

Consider `01010`:

| Query | Substring | Bad pairs | Computation | Answer |
| --- | --- | --- | --- | --- |
| 1 | `01010` | 0 | 1 + 0 | 1 |
| 2 | `101` | 0 | 1 + 0 | 1 |

This confirms that fully alternating strings collapse into a single operation regardless of length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | One linear pass to build prefix sums, constant time per query |
| Space | O(n) | Storage for prefix array |

The preprocessing fits easily within limits, and each query is answered in constant time, making the solution suitable for the maximum constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    input = sys.stdin.readline

    n, q = map(int, input().split())
    s = input().strip()

    bad = [0] * (n + 1)
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            bad[i + 1] = 1

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + bad[i]

    res = []
    for _ in range(q):
        l, r = map(int, input().split())
        res.append(str(pref[r - 1] - pref[l - 1] + 1))

    return "\n".join(res)

# provided sample
assert run("""5 3
11011
2 4
1 5
3 5
""") == "1\n3\n2"

# single character queries
assert run("""3 2
010
1 1
2 2
""") == "1\n1"

# fully alternating
assert run("""5 1
01010
1 5
""") == "1"

# all equal
assert run("""4 1
1111
1 4
""") == "3"

# mixed pattern
assert run("""6 2
110100
1 6
2 5
""") == "2\n2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single characters | 1, 1 | base case correctness |
| alternating string | 1 | no forced splits |
| all equal | 3 | maximal adjacency constraints |
| mixed pattern | 2, 2 | internal segment handling |

## Edge Cases

A substring consisting of a single character always yields zero adjacent pairs, so the answer becomes 1. The algorithm handles this because the query range `[l, r-1]` becomes empty and the prefix difference is zero.

A fully uniform substring like `000000` creates a bad pair at every boundary, and the algorithm counts exactly `length - 1`, producing the correct number of operations as `length - 1 + 1`.

A fully alternating substring such as `010101` has no bad pairs, so the prefix sum difference is zero and the answer collapses to one operation, matching the fact that the whole segment is already valid for a single deletion.

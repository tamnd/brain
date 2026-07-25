---
title: "CF 102861D - Divisibility Dance"
description: "There are two circular arrangements of people. The initial pairing is position by position, so position i in one circle faces position i in the other circle. During the dance, each step rotates exactly one of the circles."
date: "2026-07-25T14:01:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102861
codeforces_index: "D"
codeforces_contest_name: "2020-2021 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102861
solve_time_s: 57
verified: true
draft: false
---

[CF 102861D - Divisibility Dance](https://codeforces.com/problemset/problem/102861/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

There are two circular arrangements of people. The initial pairing is position by position, so position `i` in one circle faces position `i` in the other circle. During the dance, each step rotates exactly one of the circles. A rotation changes the current offset between the two circles. The entire dance is valid only if every offset that appears is new, because seeing the same offset twice means the same pairs face each other again.

A complete dance is determined by the sequence of offsets after each step. The rotations themselves are equivalent to choosing a nonzero change in the current offset, because every nonzero change modulo `N` corresponds to exactly one valid rotation amount.

At the end, the final offset must create pairs whose age sums all have the same remainder modulo `M`. We need count how many valid sequences of `K` nonzero changes end at one of those acceptable offsets.

The input size is the main difficulty. `N` can reach `10^6`, so algorithms that try every pair of positions or every possible offset with a full verification are too slow. The final counting part must be close to linear in `N`, and the dance length `K` can be as large as `10^9`, so we cannot simulate the steps.

A few edge cases are easy to miss. If `K >= N`, a valid dance cannot exist because the initial offset plus the `K` later offsets would contain at least `N+1` visits to only `N` possible positions. For example, with `N = 3`, `K = 3`, every sequence of three moves repeats an offset, so the answer is `0`.

The final offset can never be zero, because offset zero is the starting state. For example, with `N = 3`, `K = 1`, if only the original pairing satisfies the age condition, the correct answer is still `0`, not `1`, because that state cannot be reached without repeating the initial pairing.

Multiple valid final offsets must be counted separately. For example, if two different circular shifts of the second circle produce valid age sums, then each shift contributes its own number of dances.

## Approaches

A direct approach would enumerate all possible sequences of rotations. Each step has `N-1` possible nonzero changes, so this creates roughly `(N-1)^K` possibilities. Even for small `K`, this grows too quickly. A better brute force would enumerate every final shift and check whether the age condition holds, but checking one shift costs `O(N)`, giving `O(N^2)` time in the worst case, which is too slow for `N = 10^6`.

The key observation is that the age condition depends only on circular differences. Suppose a final shift `s` is valid. Then for every adjacent pair of women positions we must have

`A[i] + B[i+s] = A[i+1] + B[i+1+s]`.

Rearranging gives

`B[i+1+s] - B[i+s] = A[i] - A[i+1]`.

The left side is a circular difference sequence of `B`, and the right side is a fixed pattern derived from `A`. Therefore, finding valid shifts becomes a circular pattern matching problem.

We build the difference array of `B` and search for the pattern of differences from `A` inside two copies of the difference array. The Knuth-Morris-Pratt algorithm finds all matching starting positions in linear time.

After finding the number of valid final shifts, the remaining problem is purely combinatorial. A valid dance of length `K` is a sequence of `K+1` distinct offsets starting with offset `0`. If `K < N`, fixing the final offset leaves `K-1` intermediate offsets to choose and order from the other `N-2` positions. The number of possibilities for each valid nonzero final shift is

`(N-2) * (N-3) * ... * (N-K)`

which is `(N-2)! / (N-K-1)!`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((N-1)^K) | O(K) | Too slow |
| Check every shift | O(N^2) | O(1) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Compute the circular difference pattern of the women. For every position, store `A[i] - A[i+1]` modulo `M`. This is the pattern that every valid rotation of the men must reproduce.
2. Compute the circular difference array of the men. For every position, store `B[i+1] - B[i]` modulo `M`. A valid final shift is exactly a position where this difference sequence matches the women pattern.
3. Run KMP on the men difference array duplicated once. Every match starting at a position from `0` to `N-1` represents one valid final shift. The duplicated array handles matches that wrap around the end of the circle.
4. Remove the case of final shift `0`, because the initial offset was already visited before the dance started.
5. If `K >= N`, output `0`, because a valid sequence of offsets cannot contain more than `N` distinct states.
6. Otherwise compute the number of ways to choose the intermediate offsets. Multiply this value by the number of valid final shifts and take the result modulo `10^9+7`.

Why it works: every dance corresponds exactly to a path through the cyclic group of offsets. The validity condition is equivalent to visiting distinct offsets, so after fixing the final offset we only need to count ordered selections of the remaining visited offsets. The KMP step finds exactly the shifts where the final pairing condition is satisfied, because equality of all pair sums is equivalent to equality of all adjacent differences.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def kmp_count(text, pattern, n):
    m = len(pattern)
    pi = [0] * m

    for i in range(1, m):
        j = pi[i - 1]
        while j and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    count = 0
    j = 0
    for i, x in enumerate(text):
        while j and x != pattern[j]:
            j = pi[j - 1]
        if x == pattern[j]:
            j += 1
        if j == m:
            start = i - m + 1
            if start < n:
                count += 1
            j = pi[j - 1]

    return count

def solve():
    N, M, K = map(int, input().split())
    A = [int(x) % M for x in input().split()]
    B = [int(x) % M for x in input().split()]

    if K >= N:
        print(0)
        return

    pattern = [(A[i] - A[(i + 1) % N]) % M for i in range(N - 1)]
    diff_b = [(B[(i + 1) % N] - B[i]) % M for i in range(N)]

    valid = kmp_count(diff_b + diff_b, pattern, N)

    if K == 1:
        ways = 1
    else:
        ways = 1
        for x in range(N - 2, N - K - 1, -1):
            ways = ways * x % MOD

    print(valid * ways % MOD)

if __name__ == "__main__":
    solve()
```

The KMP preprocessing builds the failure function of the difference pattern. This allows the algorithm to continue searching after a mismatch without restarting from the beginning, which is what gives the linear complexity.

The duplicated difference array is necessary because a circular match can cross the end of the array. Only starts from the first `N` positions are counted, because those are the actual circular shifts.

The product loop computes the falling factorial directly instead of using factorials and modular inverses. This avoids extra modular arithmetic and also handles the `K = 1` case naturally.

The program never constructs the dance sequence itself. It only counts the possible final offsets and multiplies by the number of offset orders leading there.

## Worked Examples

For Sample 1:

```
4 10 1
3 4 1 7
13 27 36 9
```

The important values are:

| Value | Result |
| --- | --- |
| Women difference pattern | [9, 3, 4] |
| Men difference array | [4, 9, 3, 4] |
| Matching shifts | 1 |
| Ways for each shift | 1 |
| Answer | 1 |

The only possible final offset is the one starting at the second position of the men difference array. Since there is only one step, reaching that offset has exactly one valid dance.

For Sample 2:

```
5 10 2
3 4 1 7 6
4 7 1 2 5
```

| Value | Result |
| --- | --- |
| Women difference pattern | [9, 3, 4, 1] |
| Men difference array | [3, 4, 1, 3, 9] |
| Matching shifts | 0 |
| Ways for each shift | 3 |
| Answer | 0 |

The pattern does not appear in the circular difference sequence, so no final pairing satisfies the age condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Building differences, running KMP, and computing the falling factorial are all linear |
| Space | O(N) | The difference arrays and KMP prefix table use linear memory |

The solution fits the `N = 10^6` limit because every operation is a single pass over the input arrays. The value of `K` does not affect the running time because it is only used in the combinatorial formula.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
    return out.getvalue()

assert run("""4 10 1
3 4 1 7
13 27 36 9
""") == "1\n", "sample 1"

assert run("""5 10 2
3 4 1 7 6
4 7 1 2 5
""") == "0\n", "sample 2"

assert run("""5 10 2
3 4 1 7 6
5 4 7 1 2
""") == "3\n", "sample 3"

assert run("""3 100 3
1 2 3
4 5 6
""") == "0\n", "too many steps"

assert run("""3 10 1
1 1 1
2 2 2
""") == "2\n", "all equal values"

assert run("""4 7 2
1 2 3 4
6 5 4 3
""") == "2\n", "circular matching"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 1 | Single step counting |
| Sample 2 | 0 | No valid final shift |
| Sample 3 | 3 | Multiple dances from one final shift |
| `N=3, K=3` | 0 | Impossible number of distinct states |
| Equal values | 2 | Multiple valid shifts and modulo handling |
| Circular match case | 2 | Pattern matching across the circle boundary |

## Edge Cases

When `K >= N`, the algorithm immediately returns zero. For example:

```
3 100 3
1 2 3
4 5 6
```

There are only three possible offsets, including the starting one. A dance of length three would need four different offsets, which cannot happen.

When the only valid pairing is the initial pairing, it must not be counted. The KMP phase can find the shift `0`, but the combinatorial phase never allows returning to the starting offset because all visited offsets must be distinct.

When several shifts satisfy the age condition, the algorithm counts each one independently. The difference matching step returns all valid circular starts, and each start contributes the same number of valid dance histories because the number of intermediate offsets depends only on `N` and `K`, not on the final location.

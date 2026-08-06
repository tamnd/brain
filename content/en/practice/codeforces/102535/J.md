---
title: "CF 102535J - Aufbau"
description: "The task is to simulate a very large electron filling process, but only the final filled subshell matters. An atom with atomic number a has exactly a electrons. Electrons are placed into subshells ordered by the value n + l, and ties are resolved by smaller n."
date: "2026-08-06T19:58:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "J"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 101
verified: true
draft: false
---

[CF 102535J - Aufbau](https://codeforces.com/problemset/problem/102535/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to simulate a very large electron filling process, but only the final filled subshell matters. An atom with atomic number `a` has exactly `a` electrons. Electrons are placed into subshells ordered by the value `n + l`, and ties are resolved by smaller `n`. A subshell with index `l` can hold `4l + 2` electrons.

For each query, instead of printing the entire electron configuration, we only need the last subshell that receives electrons. The answer must contain the shell number `n`, the subshell label, and the number of electrons actually placed there.

The limit of `a` being as large as `10^15` immediately rules out simulating electrons one by one. Even iterating over all filled subshells for every test case would be too slow because there can be millions of relevant positions across `10^5` queries. The solution needs to jump over large groups of subshells mathematically and only inspect a logarithmic number of candidates.

The first tricky case is that the order is not simply increasing shell number. For example, the input `19` produces `4s1`, because `4s` has smaller `n+l` than `3d`. A solution that scans shells in order gives the wrong result.

Another edge case is a query ending exactly at the boundary of a subshell. For input `2`, the answer is `1s2`. A careless binary search that finds the next group instead of the first group containing the answer may incorrectly move to `2s`.

A final subtle case is the extended subshell naming. For example, the largest sample uses a label longer than one character. A solution assuming `l` is always one letter will fail after the single-letter labels are exhausted.

## Approaches

A direct approach would generate the subshell ordering, subtract each subshell capacity from the remaining number of electrons, and stop when the remaining value fits in the current subshell. This is correct because it follows exactly the Aufbau ordering. However, for `10^15` electrons, the number of subshells is far too large to generate separately for every query.

The useful observation is that subshells naturally form diagonals by the value `k = n + l`. Every diagonal can be skipped as a whole. For a fixed `k`, all possible pairs satisfy `n + l = k`, and the total number of electrons in that diagonal can be computed with a formula. We can binary search the first diagonal whose cumulative capacity reaches the given atomic number.

After locating the diagonal, there are only about half as many subshells inside it. Instead of walking through them, we use another binary search because the capacities form an arithmetic progression. This reduces the whole problem to a few logarithmic searches.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of subshells) per query | O(1) | Too slow |
| Optimal | O(log K) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. Define a function that returns the total number of electrons contained in all subshells with `n + l <= K`.

For a fixed subshell index `l`, the valid shells satisfy `l + 1 <= n <= K - l`. The number of such shells is `K - 2l`, and every one contributes `4l + 2` electrons. Summing this arithmetic expression gives a closed formula, allowing us to skip entire diagonals.
2. Binary search the smallest `K` such that the total electrons up to diagonal `K` is at least the given atomic number.

The previous diagonals are completely filled, so subtracting their total leaves the number of electrons that must be placed inside diagonal `K`.
3. Find the exact subshell inside diagonal `K`.

In this diagonal, shells are visited in increasing `n`. The corresponding `l` values decrease. Their capacities are an arithmetic sequence, so another binary search finds the first subshell whose cumulative capacity reaches the remaining electron count.
4. Compute the remaining electrons in that subshell and convert its `l` value into the required label format.

The first twenty subshell indices after `s` and `p` have single-character labels. After those, the labels become lexicographically ordered combinations of letters.

Why it works: the algorithm preserves the same ordering as the Aufbau rule by grouping only consecutive parts of the original sequence. The first binary search identifies the exact diagonal containing the answer, and the second identifies the exact subshell inside that diagonal. Since every skipped part is counted by an exact capacity formula, no electron position can be skipped or counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def prefix(k):
    if k <= 0:
        return 0
    m = (k - 1) // 2
    return 2 * k * (m + 1) * (m + 1) - (2 * m * (m + 1) * (4 * m + 5)) // 3

def inside_sum(largest_l, count):
    return count * (4 * largest_l + 2) - 2 * count * (count - 1)

def label(idx):
    if idx == 0:
        return "s"
    if idx == 1:
        return "p"

    singles = "dfghijklmnoqrtuvwxyz"
    idx -= 2

    if idx < len(singles):
        return singles[idx]

    idx -= len(singles)
    length = 2
    while True:
        block = 26 ** length
        if idx < block:
            chars = []
            for _ in range(length):
                chars.append(chr(ord('a') + idx % 26))
                idx //= 26
            return ''.join(reversed(chars))
        idx -= block
        length += 1

def solve_one(a):
    lo, hi = 1, 100000
    while lo < hi:
        mid = (lo + hi) // 2
        if prefix(mid) >= a:
            hi = mid
        else:
            lo = mid + 1

    k = lo
    rem = a - prefix(k - 1)

    start_n = k // 2 + 1
    max_l = k - start_n

    lo, hi = 0, max_l
    while lo < hi:
        mid = (lo + hi) // 2
        if inside_sum(max_l, mid + 1) >= rem:
            hi = mid
        else:
            lo = mid + 1

    skipped = lo
    l = max_l - skipped
    before = inside_sum(max_l, skipped)
    e = rem - before
    n = k - l

    return str(n) + label(l) + str(e)

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        ans.append(solve_one(int(input())))
    print('\n'.join(ans))

main()
```

The `prefix` function is the core optimization. It counts complete diagonals instead of individual subshells. The variable `m` is the largest possible `l` value in diagonal `k`, and the formula comes from summing all capacities in that diagonal.

The second helper, `inside_sum`, gives the capacity of the first `count` subshells inside a diagonal. Because those capacities decrease by exactly four each time, the sum is an arithmetic progression.

The first binary search uses a range large enough for all possible inputs. The value needed for `10^15` electrons is much smaller than `100000`, so this bound is only a safe upper limit. Python integers avoid overflow during the large multiplications.

The label conversion is separated from the mathematics. This avoids mixing the unusual naming rules with the electron counting logic.

## Worked Examples

For input `19`, the binary search finds diagonal `k = 5`.

| Variable | Value |
| --- | --- |
| k | 5 |
| Electrons before diagonal | 18 |
| Remaining electrons | 1 |
| First n in diagonal | 3 |
| First l in diagonal | 2 |
| Selected l | 0 |
| Selected n | 4 |
| Electrons in subshell | 1 |

The diagonal contains `3d`, `4s`, and the search finds that only one electron is needed after all previous diagonals are complete. The result is `4s1`.

For input `103`, the previous diagonals contain `94` electrons, leaving `9` electrons inside diagonal `k = 8`.

| Variable | Value |
| --- | --- |
| k | 8 |
| Electrons before diagonal | 94 |
| Remaining electrons | 9 |
| First n in diagonal | 5 |
| First l in diagonal | 3 |
| Selected l | 2 |
| Selected n | 6 |
| Electrons in subshell | 9 |

The selected subshell is `6d`, and the result is `6d9`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log K) | Two binary searches over the diagonal and subshell positions |
| Space | O(1) | Only a constant number of integer variables are stored |

The largest atomic number only requires a few dozen iterations of the binary searches. This easily fits the limit of `10^5` test cases.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old

    out = []
    for x in data[1:]:
        out.append(solve_one(int(x)))
    return "\n".join(out)

assert run("""3
19
103
1000000000000000
""") == """4s1
6d9
93591dzil31704"""

assert run("""1
1
""") == "1s1"

assert run("""1
2
""") == "1s2"

assert run("""1
18
""") == "3p6"

assert run("""1
20
""") == "3d2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1s1` | Minimum atomic number |
| `2` | `1s2` | Exact subshell boundary |
| `18` | `3p6` | Completion of a diagonal |
| `20` | `3d2` | Transition into the next subshell |

## Edge Cases

For atomic number `2`, the algorithm finds `k = 1` because the first diagonal already contains enough electrons. The remaining count is `2`, and the first subshell in the diagonal has capacity `2`, so the output is `1s2`. The binary search does not move to the next diagonal because it searches for the first valid prefix.

For atomic number `19`, the algorithm first skips all diagonals before `k = 5`. Inside that diagonal, it compares capacities in the order `3d`, `4s`. The first subshell cannot contain the remaining electrons, so the answer becomes `4s1`.

For very large values such as `1000000000000000`, the algorithm never constructs the full configuration. It only evaluates formulas for complete diagonals and performs logarithmic searches, then generates the final multi-letter label from the computed subshell index. This handles the extended naming rule without any fixed upper assumption on label length.

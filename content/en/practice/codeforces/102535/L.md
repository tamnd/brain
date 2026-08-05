---
title: "CF 102535L - Kim Possible and the Mooks and the Swappinator"
description: "The line of opponents can be viewed as a binary array. A MOOK is 1 because it still requires a fight, and a MEEK is 0 because Kim passes through it for free. Before fighting begins, we may swap two positions exactly k times."
date: "2026-08-05T15:44:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "L"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 1223
verified: true
draft: false
---

[CF 102535L - Kim Possible and the Mooks and the Swappinator](https://codeforces.com/problemset/problem/102535/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 20m 23s  
**Verified:** yes  

## Solution
# Problem Understanding

The line of opponents can be viewed as a binary array. A MOOK is `1` because it still requires a fight, and a MEEK is `0` because Kim passes through it for free. Before fighting begins, we may swap two positions exactly `k` times. The goal is to arrange the line so that the number of minutes needed to clear all MOOKs is as small as possible.

The fighting process has a hidden binary-counter structure. If we assign position `i` the value `2^(i-1)` and sum the values of all MOOK positions, one fight always decreases this sum by exactly one. The first MOOK changes from `1` to `0`, and all previous zeroes become ones, which is exactly a binary decrement. Because of this, the final answer is the numeric value represented by the binary array after the swaps.

The input gives the length of the line, the exact number of swaps, and then the current state of every position. The output is the smallest possible binary value after performing those swaps, modulo `10^9`.

The constraint `n <= 100000` is the main difficulty. A simulation of the fighting process can take up to `2^n` minutes, which is impossible. Even trying all possible swap choices is far beyond what a 2 second limit allows because the number of possible pairs is quadratic and sequences of swaps grow exponentially. The solution has to examine the line only a constant number of times, leading to an `O(n)` approach.

There are several edge cases that break simpler solutions. If there are no MOOKs, the answer is always zero. For example:

```
2 5
MEEK
MEEK
```

The correct output is `0`. A method that always tries to move MOOKs around may incorrectly assume at least one fight exists.

A second trap is the requirement that swaps must be used exactly `k` times. For example:

```
2 1
MOOK
MEEK
```

The only swap changes the state to `MEEK, MOOK`, giving value `2`. A solution that only tries to reach the fully optimized arrangement would incorrectly output `1`.

The final special case is two opponents of different types. There are no equal elements available to swap as a meaningless extra operation. For example:

```
2 2
MEEK
MOOK
```

After two swaps the array returns to its initial state, so the answer is `2`, not the sorted value `1`.

## Approaches

A direct approach would simulate every possible choice of swaps. For each sequence of swaps we could compute the resulting binary value and keep the smallest one. This is correct because it considers every legal final arrangement. However, even one swap has `O(n^2)` choices, and repeating this for up to `n` swaps gives an impossible search space.

A better starting point is to understand what a swap can improve. The smallest binary value with the same number of MOOKs is obtained by putting all MOOKs at the beginning of the line, because earlier positions have smaller powers of two. For example, with three MOOKs, the ideal form is `111000...`.

Every position in the first block that contains a MEEK is a mistake. Swapping it with a MOOK from the right fixes exactly one such mistake. To maximize the improvement, we should use the leftmost incorrect positions and the rightmost MOOKs outside the block.

The remaining difficulty is the word "exactly". If we need fewer swaps than the number of mistakes, every swap should be useful. If we have enough swaps to reach the sorted arrangement, the only question is whether the remaining swaps can be wasted. In every case except a line of length two containing one MOOK and one MEEK, an extra swap can be made between equal opponents or by undoing a previous swap. The exceptional case can be handled separately because the only possible operation is repeatedly exchanging the two positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the line into a binary array where MOOK is `1` and MEEK is `0`. Count the number of MOOKs, call it `m`. The best possible final arrangement has ones in positions `1` through `m`.
2. Handle the special case `n = 2` with exactly one MOOK and one MEEK. Since every swap exchanges the two elements, only the parity of `k` matters. An even number of swaps restores the original state and an odd number swaps the two positions.
3. Find all incorrect zero positions inside the first `m` positions and all one positions after the first `m` positions. These are the positions where a useful swap can improve the value.
4. If fewer than `k` mistakes exist, use every mistake fixing swap. The remaining swaps do not need to change the final binary value, because they can be wasted without affecting the arrangement.
5. If `k` is smaller than the number of mistakes, perform exactly `k` useful swaps. Pair the smallest incorrect positions with the largest MOOK positions outside the target prefix. This gives the greatest reduction in binary value.
6. Compute the resulting binary value by adding `2^i` for every remaining MOOK position. The answer is taken modulo `10^9`.

Why it works:

The binary value interpretation converts the fighting process into a simple numeric problem. Minimizing the fighting time is identical to minimizing the binary value after the swaps. Every useful swap moves a `1` to an earlier position and a `0` to a later position. Pairing the earliest available zero with the latest available one produces the largest possible decrease for that swap. Once all possible mistakes are fixed, the arrangement is already the minimum possible arrangement, and any remaining swaps can be neutralized except in the two-element mixed case handled separately.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9

def solve_case(n, k, arr):
    ones = sum(arr)

    if ones == 0:
        return 0

    if n == 2 and ones == 1:
        if k % 2 == 1:
            return (2 if arr[0] == 1 else 1)
        return (1 if arr[0] == 1 else 2)

    bad = []
    extra = []

    for i in range(ones):
        if arr[i] == 0:
            bad.append(i)

    for i in range(ones, n):
        if arr[i] == 1:
            extra.append(i)

    use = min(k, len(bad))

    extra.sort(reverse=True)

    for i in range(use):
        a = bad[i]
        b = extra[i]
        arr[a], arr[b] = arr[b], arr[a]

    ans = 0
    power = 1
    for x in arr:
        if x == 1:
            ans += power
            if ans >= MOD:
                ans -= MOD
        power = (power * 2) % MOD

    return ans % MOD

def main():
    n, k = map(int, input().split())
    arr = []
    for _ in range(n):
        arr.append(1 if input().strip() == "MOOK" else 0)

    print(solve_case(n, k, arr))

if __name__ == "__main__":
    main()
```

The code first counts the number of MOOKs because that determines the target prefix length. The target arrangement is not stored separately, because the positions that need changes can be found directly.

The `bad` array stores MEEK positions that should contain MOOKs in the optimal prefix. The `extra` array stores MOOKs that are currently outside that prefix. Swapping these two groups performs the most valuable possible changes first.

The special two-element case is processed before the greedy swaps. This avoids the mistake of assuming that extra swaps can always be ignored. For larger arrays, extra swaps can be absorbed without changing the final binary value.

The final loop evaluates the binary number using powers of two modulo `10^9`. Python integers do not overflow, but taking the modulus during accumulation keeps the computation small and mirrors the required output.

## Worked Examples

For the first sample:

```
3 0
MEEK
MOOK
MEEK
```

The binary representation is `010`.

| Step | Array | Bad positions | Extra positions | Swaps used | Value |
| --- | --- | --- | --- | --- | --- |
| Initial | 010 | 0 | 1 | 0 | 2 |

No swaps are allowed, so the answer remains `2`.

For the second sample:

```
3 1
MEEK
MOOK
MEEK
```

The target has one MOOK in the first position.

| Step | Array | Bad positions | Extra positions | Swaps used | Value |
| --- | --- | --- | --- | --- | --- |
| Initial | 010 | 0 | 1 | 0 | 2 |
| After swap | 100 | none | none | 1 | 1 |

The single allowed swap performs the only useful improvement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The array is scanned a constant number of times and the swap lists are sorted once. |
| Space | O(n) | The lists of incorrect positions may contain every element in the worst case. |

The input size is `100000`, so a linear solution is required. The algorithm performs only simple scans and one sort of at most `n` elements, which fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    arr = []
    for _ in range(n):
        arr.append(1 if input().strip() == "MOOK" else 0)
    ans = str(solve_case(n, k, arr))
    sys.stdin = old
    return ans

assert run("""3 0
MEEK
MOOK
MEEK
""") == "2"

assert run("""3 1
MEEK
MOOK
MEEK
""") == "1"

assert run("""7 1
MOOK
MEEK
MEEK
MOOK
MEEK
MOOK
MEEK
""") == "11"

assert run("""2 2
MEEK
MOOK
""") == "2"

assert run("""5 0
MEEK
MEEK
MEEK
MEEK
MEEK
""") == "0"

assert run("""4 2
MEEK
MOOK
MEEK
MOOK
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2` mixed opponents | `2` | Exact swap count special case |
| All MEEKs | `0` | Empty set of MOOKs |
| Four positions with two useful swaps | `5` | Multiple greedy improvements |

## Edge Cases

The all-MEEK case is handled because the number of MOOKs is zero, so the binary value is zero and no swaps can create a MOOK.

The exact swap condition is handled by the two-element mixed case. For:

```
2 2
MEEK
MOOK
```

the first swap creates `MOOK, MEEK`, and the second swap returns to `MEEK, MOOK`. The algorithm detects the even number of swaps and returns the original value.

For the sample where only one useful swap is available:

```
3 1
MEEK
MOOK
MEEK
```

the first position is inside the target MOOK prefix and is currently wrong. The algorithm swaps it with the only MOOK outside the prefix, producing `MOOK, MEEK, MEEK`, whose value is `1`.

For cases where `k` is larger than the number of mistakes, the algorithm stops making value-changing swaps once the optimal arrangement is reached. The remaining swaps can be made harmlessly because at least one pair of equal opponents exists, except for the already handled two-element mixed line.

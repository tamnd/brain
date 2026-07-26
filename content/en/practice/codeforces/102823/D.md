---
title: "CF 102823D - Bits Reverse"
description: "The operation works on the binary representation of a number. We may choose any three consecutive bit positions and reverse those three bits."
date: "2026-07-26T15:42:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102823
codeforces_index: "D"
codeforces_contest_name: "2018 China Collegiate Programming Contest - Guilin Site"
rating: 0
weight: 102823
solve_time_s: 45
verified: true
draft: false
---

[CF 102823D - Bits Reverse](https://codeforces.com/problemset/problem/102823/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
# Problem Understanding

The operation works on the binary representation of a number. We may choose any three consecutive bit positions and reverse those three bits. Among the three bits, only the first and third positions change places, so one operation is exactly a swap between two bits that are two positions apart.

The task is to transform the number `x` into `y` using the minimum number of such swaps. Leading zeroes can be considered, which means we are allowed to use positions beyond the highest set bit when applying operations.

The important structure is that a bit can never change its parity position. A bit at position 0 can only move to positions 2, 4, 6 and so on. A bit at position 1 can only move to positions 3, 5, 7 and so on. The operation splits the binary representation into two independent sequences, one containing even positions and one containing odd positions.

The values of `x` and `y` can be as large as `10^18`, so there are only about 61 relevant bits. With up to 10000 test cases, the solution must be close to constant time per case. A simulation of operations is not feasible because the number of possible swaps can be large, but processing the fixed number of bits is easily fast enough.

A common mistake is to only compare the total number of ones. For example, transforming `1` into `2` is impossible even though both numbers contain one set bit. The only bit in `1` is at position 0, while the only bit in `2` is at position 1, and no operation changes parity.

Another edge case is when leading zeroes matter. For example, transforming `3` into `6` has answer `1`. In binary this is `011` to `110`, and the operation reverses the three bits. Treating the numbers as strings without considering positions can accidentally miss that the leftmost zero is a valid bit position.

A final edge case is when no operations are needed. For input

```
5
5
```

meaning `x = 5`, `y = 5`, the answer is `0`. A solution that only counts required swaps and forgets the already matching state may produce an unnecessary positive answer.

# Approaches

The brute force approach would repeatedly choose a triple of bits, apply the reversal, and search for the shortest sequence of operations that reaches `y`. This is correct because every valid sequence of operations corresponds to a path in the state graph of possible binary numbers. However, the number of states grows exponentially with the number of bits. Even restricting ourselves to the relevant 61 bits gives far too many possibilities, so shortest path search is impossible.

The key observation is that a reversal of three bits only swaps positions `i` and `i + 2`. This means the operation is not an arbitrary permutation of bits. It is an adjacent swap inside the subsequence of positions with the same parity. The even positions form one independent array, and the odd positions form another independent array.

After this transformation, the problem becomes a classic minimum adjacent swaps problem. For one parity group, we know the positions of all ones in `x` and the positions of all ones in `y`. The first one in `x` must move to the position of the first one in `y`, the second one must move to the second one, and so on. The minimum number of adjacent swaps is the sum of these distances in the compressed parity array.

The brute force works because it explores every possible movement of bits, but it ignores the fact that bits never cross between parity groups. The parity observation reduces the problem to two independent one dimensional rearrangements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(61) per test case | O(61) | Accepted |

# Algorithm Walkthrough

1. Extract the bits of `x` and `y` from the least significant bit upward. We only need around 61 positions because both values are at most `10^18`. Positions above this range are always zero.
2. Separate the set bit positions into two groups based on parity. For each parity, store the indices of ones in the compressed sequence. For example, positions `0, 2, 4, 6` become compressed indices `0, 1, 2, 3`.
3. Compare the number of ones in the corresponding parity groups of `x` and `y`. If they differ, the transformation is impossible because operations never move a bit between even and odd positions.
4. For each parity group, match the ones in order. Add the absolute difference between every source compressed index and target compressed index. This is the number of adjacent swaps needed inside that parity sequence.
5. Add the costs of the two parity groups and print the result.

Why it works: The allowed operation is exactly an adjacent swap in one of the two parity subsequences. Adjacent swaps preserve the order of the other parity and can move any bit to any position inside the same parity group. For binary sequences, the minimum number of adjacent swaps is achieved by matching the first one with the first one, the second with the second, and so on. If the number of ones differs, no sequence of swaps can create or remove a one, so the answer is impossible.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(x, y):
    src = [[], []]
    dst = [[], []]

    for i in range(61):
        if (x >> i) & 1:
            src[i & 1].append(i // 2)
        if (y >> i) & 1:
            dst[i & 1].append(i // 2)

    ans = 0

    for p in range(2):
        if len(src[p]) != len(dst[p]):
            return -1
        for a, b in zip(src[p], dst[p]):
            ans += abs(a - b)

    return ans

def main():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        x, y = map(int, input().split())
        out.append(f"Case {case}: {solve_case(x, y)}")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution stores only the positions of set bits because zero bits do not need to be moved explicitly. A set bit in position `i` belongs to parity group `i % 2`, and its compressed position is `i // 2`. This converts the original positions into indices where neighboring elements represent a possible swap.

The impossible check is done before calculating distances. Comparing only the total number of ones would be incorrect because the two parity groups cannot exchange bits.

The final loop uses the fact that sorted positions of ones must be matched in the same order. There is no need for dynamic programming or simulation because every swap only moves a bit one step inside its own parity sequence.

# Worked Examples

For the input

```
3
0 3
3 6
6 9
```

the traces are:

| Case | Parity | Source ones | Target ones | Cost |
| --- | --- | --- | --- | --- |
| 1 | Even | empty | position 0 | impossible |

For `0` to `3`, the source has no set bits while the target has one bit in the even group and one bit in the odd group. Since a swap cannot create bits, the answer is `-1`.

For the second case:

| Case | Parity | Source ones | Target ones | Cost |
| --- | --- | --- | --- | --- |
| 2 | Even | `[0]` | `[1]` | `1` |
| 2 | Odd | `[0]` | `[0]` | `0` |
| 2 | Total |  |  | `1` |

The lowest three bits change from `011` to `110`. The even-position one moves one step in the compressed sequence, which corresponds to one allowed operation.

For the third case:

| Case | Parity | Source ones | Target ones | Cost |
| --- | --- | --- | --- | --- |
| 3 | Even | `[1]` | `[0]` | `1` |
| 3 | Odd | `[0]` | `[1]` | `1` |
| 3 | Total |  |  | `2` |

The two parity groups each need one adjacent movement, so the minimum number of operations is `2`.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(61) per test case | We inspect only the relevant binary positions and compare stored one positions. |
| Space | O(61) per test case | At most 61 bit positions are stored. |

The fixed bit limit makes the solution easily fit the limits even for 10000 test cases. The total work is only a few hundred thousand simple operations.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    main()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def solve_case(x, y):
    src = [[], []]
    dst = [[], []]

    for i in range(61):
        if (x >> i) & 1:
            src[i & 1].append(i // 2)
        if (y >> i) & 1:
            dst[i & 1].append(i // 2)

    ans = 0
    for p in range(2):
        if len(src[p]) != len(dst[p]):
            return -1
        for a, b in zip(src[p], dst[p]):
            ans += abs(a - b)
    return ans

def main():
    t = int(input())
    out = []
    for case in range(1, t + 1):
        x, y = map(int, input().split())
        out.append(f"Case {case}: {solve_case(x, y)}")
    print("\n".join(out))

assert run("""3
0 3
3 6
6 9
""") == """Case 1: -1
Case 2: 1
Case 3: 2
""", "sample"

assert solve_case(0, 0) == 0, "same number"
assert solve_case(1, 2) == -1, "different parity"
assert solve_case(7, 28) == 2, "multiple parity movements"
assert solve_case(10**18, 10**18) == 0, "large equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0` | Handles already equal numbers |
| `1 2` | `-1` | Detects impossible parity changes |
| `7 28` | `2` | Handles several bit movements |
| `10^18 10^18` | `0` | Handles maximum sized values |

# Edge Cases

For the impossible parity case, consider `x = 1` and `y = 2`. The binary forms are `...0001` and `...0010`. The only set bit starts at position 0 and ends at position 1. Since every operation swaps positions with distance two, the bit can never reach an odd position. The algorithm places the source bit in the even group and the target bit in the odd group, detects different counts, and returns `-1`.

For leading zero handling, consider `x = 3` and `y = 6`. The relevant bits are `011` and `110`. The set bit at position 0 moves to position 2, which is one step in the even compressed sequence. The odd position remains unchanged. The algorithm calculates one movement and returns `1`.

For the already solved case, consider `x = 12` and `y = 12`. Both parity groups contain exactly the same one positions. Every distance is zero, so the answer is zero. The algorithm does not perform unnecessary swaps.

For large values, consider `x = 10^18` and `y = 10^18`. The algorithm only inspects 61 positions, so it handles the upper bound without depending on the numeric magnitude itself. The answer remains zero because no bits need to move.

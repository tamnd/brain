---
title: "CF 105940K - The Cage in ASZoo"
description: "The cage can hold exactly k animals. There are n animal families, and a family can contribute any nonnegative number of animals because every family has infinitely many members. Family i contributes animals of weight a[i]."
date: "2026-06-25T13:56:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105940
codeforces_index: "K"
codeforces_contest_name: "ASU Coding Cup 10"
rating: 0
weight: 105940
solve_time_s: 37
verified: true
draft: false
---

[CF 105940K - The Cage in ASZoo](https://codeforces.com/problemset/problem/105940/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The cage can hold exactly `k` animals. There are `n` animal families, and a family can contribute any nonnegative number of animals because every family has infinitely many members. Family `i` contributes animals of weight `a[i]`. The task is to find every total weight that can be formed by choosing exactly `k` animals, allowing repeated use of the same family. The output is the list of all reachable sums in increasing order.

The limits are small for the number of families and the number of animals, but the possible answer range is the important part. Since `k` and every weight are at most `1000`, the largest possible sum is at most `1,000,000`. This means a solution depending on the maximum weight range is realistic. On the other hand, a direct dynamic programming approach over every family, every animal count, and every sum would take around `1000 * 1000 * 1,000,000` operations, which is far beyond what we can afford.

The tricky cases come from the fact that families can be reused. A solution that treats each family as usable only once would fail. For example:

```
Input
1 3
5

Output
15
```

The only possible choice is taking the same family three times. A subset style DP would incorrectly say that only weight `5` is possible.

Another common mistake is forgetting that exactly `k` animals are required. For example:

```
Input
2 2
1 100

Output
2 101 200
```

The sum `1` is not valid even though a single animal of weight `1` exists. We must track the number of selected animals, not only reachable sums.

A final edge case appears when all families have the same weight:

```
Input
5 5
7 7 7 7 7

Output
35
```

Many different choices exist, but they all produce the same sum. The answer must contain only unique weights.

## Approaches

The straightforward idea is to build a dynamic programming table where `dp[c][s]` tells us whether we can choose exactly `c` animals with total weight `s`. For every reachable state we try every family as the next animal. This is correct because every valid selection can be described by repeatedly adding one animal.

The problem is the transition count. There are up to `k` possible animal counts, up to `k * max(a[i])` possible sums, and up to `n` choices for the next animal. In the worst case this is around `1000 * 1,000,000 * 1000`, which is roughly one quadrillion operations.

The key observation is that the transition is the same for every reachable sum. We only need to shift all currently reachable sums by each family weight. Bitsets are designed exactly for this. A bit at position `x` means that sum `x` is reachable. Shifting the bitset left by `a[i]` marks all sums that can be created by adding one animal from family `i`.

Instead of storing all sums in a large table, we keep one bitset for every possible number of animals. When we process a new animal count, we update the next layer using bit shifts. Python integers already behave like arbitrary length bitsets, so a single shift and OR operation updates thousands of states at once.

The brute force works because it explores every possible final choice. The faster method keeps the same state definition but replaces millions of individual transitions with machine-level bit operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * k * max(a) * n) | O(k * k * max(a)) | Too slow |
| Optimal | O(k * n * (k * max(a)) / word_size) | O(k * k * max(a) / word_size) | Accepted |

## Algorithm Walkthrough

1. Create `k + 1` bitsets. The `i`-th bitset represents all weights achievable using exactly `i` animals. Initially only zero animals with weight zero is possible, so the first bitset contains only bit `0`.
2. For every possible number of already chosen animals from `0` to `k - 1`, try adding one more animal. For each family weight `w`, shift the current bitset left by `w` and merge it into the next layer. The shift represents adding one animal of that family.
3. After building all layers, inspect the bitset for exactly `k` animals. Every set bit corresponds to one achievable total weight, so collect those positions in increasing order.

The update order matters. We only move from fewer animals to more animals, so a sum created at level `c + 1` is never reused during the same level and accidentally counted as using extra animals.

Why it works: the invariant is that after finishing layer `c`, every set bit in that layer represents exactly the weights obtainable with `c` animals, and no invalid weight is stored. Adding one more animal from any family is equivalent to shifting the whole set of reachable weights by that family weight. Taking the union of all such shifts produces exactly the valid states for `c + 1` animals. By induction, the final layer contains precisely all possible cage weights.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:2 + n]

    dp = [0] * (k + 1)
    dp[0] = 1

    for cnt in range(k):
        cur = dp[cnt]
        if cur == 0:
            continue
        nxt = 0
        for w in a:
            nxt |= cur << w
        dp[cnt + 1] = nxt

    ans = []
    bits = dp[k]
    pos = 0
    while bits:
        low = bits & -bits
        pos = low.bit_length() - 1
        ans.append(str(pos))
        bits ^= low

    print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The array `dp` stores the bitset state for each exact animal count. The initialization `dp[0] = 1` means only sum zero is reachable before choosing any animals.

For every layer, the variable `cur` contains all currently reachable sums. Each `cur << w` adds one animal of weight `w` to every previous possibility. The OR operation combines all possible families.

The extraction loop repeatedly finds the lowest set bit. Because integer bits are ordered from low to high, this naturally produces answers in ascending order. Removing the lowest bit avoids scanning through every possible weight value.

The implementation does not need special handling for integer overflow because Python integers grow automatically. The main boundary detail is iterating only until `k - 1`, because the last transition creates the state for exactly `k` animals.

## Worked Examples

### Sample 1

Input:

```
3 2
1 2 3
```

The trace is:

| Animals chosen | Current reachable sums | Action |
| --- | --- | --- |
| 0 | {0} | Add weights 1, 2, 3 |
| 1 | {1, 2, 3} | Add weights 1, 2, 3 |
| 2 | {2, 3, 4, 5, 6} | Output |

The first transition creates every single-animal weight. The second transition adds another animal and creates all valid pairs.

### Sample 2

Input:

```
5 5
1 1 1 1 1
```

| Animals chosen | Current reachable sums | Action |
| --- | --- | --- |
| 0 | {0} | Add weight 1 |
| 1 | {1} | Add weight 1 |
| 2 | {2} | Add weight 1 |
| 3 | {3} | Add weight 1 |
| 4 | {4} | Add weight 1 |
| 5 | {5} | Output |

Even though there are many ways to pick five animals, the reachable set contains only one value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k * n * S / word_size) | Each layer shifts a bitset of maximum size `S`, where `S` is the maximum possible sum. |
| Space | O(k * S / word_size) | We store one bitset for each possible animal count. |

Here `S` is at most `1,000,000`. The bitset representation compresses many boolean states into each machine integer, making the approach fit comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return ""
    n, k = data[0], data[1]
    a = data[2:2+n]

    dp = [0] * (k + 1)
    dp[0] = 1
    for c in range(k):
        for w in a:
            dp[c + 1] |= dp[c] << w

    ans = []
    x = dp[k]
    while x:
        b = x & -x
        ans.append(str(b.bit_length() - 1))
        x -= b

    sys.stdin = old
    return " ".join(ans)

assert run("""3 2
1 2 3
""") == "2 3 4 5 6", "sample 1"

assert run("""5 5
1 1 1 1 1
""") == "5", "sample 2"

assert run("""3 3
3 5 11
""") == "9 11 13 15 17 19 21 25 27 33", "sample 3"

assert run("""1 3
5
""") == "15", "repeated family"

assert run("""2 2
1 100
""") == "2 101 200", "exact count"

assert run("""4 1
7 7 7 7
""") == "7", "duplicate weights"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / 5` | `15` | A family can be chosen multiple times. |
| `2 2 / 1 100` | `2 101 200` | Exactly `k` animals must be selected. |
| `4 1 / 7 7 7 7` | `7` | Duplicate family weights produce unique sums. |
| `5 5 / 1 1 1 1 1` | `5` | Many choices can collapse into one answer. |

## Edge Cases

For the repeated-family case:

```
Input
1 3
5
```

The algorithm starts with reachable sums `{0}`. After one transition it has `{5}`, after two it has `{10}`, and after three it has `{15}`. The final layer contains only `15`, correctly allowing unlimited use of one family.

For the exact-count case:

```
Input
2 2
1 100
```

After one animal the reachable weights are `{1, 100}`. The second transition combines these states again and creates `{2, 101, 200}`. The value `1` never appears in the final layer because it uses only one animal.

For the duplicate-weight case:

```
Input
5 5
7 7 7 7 7
```

Every transition shifts by the same amount. The reachable set grows as `{0}`, `{7}`, `{14}`, `{21}`, `{28}`, `{35}`. The bitset automatically removes duplicate possibilities because a bit can only be set once.

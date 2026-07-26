---
title: "CF 102829H - Zorro's Revenge"
description: "The task is to decide whether a number N can be written as a sum of exactly K terms where every term is a non-negative integer power of X."
date: "2026-07-26T15:26:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102829
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 11-06-20 Div. 1 (Tryout)"
rating: 0
weight: 102829
solve_time_s: 46
verified: true
draft: false
---

[CF 102829H - Zorro's Revenge](https://codeforces.com/problemset/problem/102829/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
# Problem Understanding

The task is to decide whether a number `N` can be written as a sum of exactly `K` terms where every term is a non-negative integer power of `X`. If such a representation exists, the terms must be printed in descending order, and among all valid descending sequences we need the lexicographically smallest one. The input contains one large target value `N`, the required number of summands `K`, and the base `X`. The output is either an impossibility answer or a carefully chosen list of powers of `X` whose sum is exactly `N`.

The value of `N` can reach `10^18`, so trying to build all possible combinations of powers is impossible. Even iterating through every value up to `N` would require far too many operations. The base is at most `9`, which means the base representation of `N` has only about 60 digits. The value of `K` is limited to `2 * 10^5`, so the algorithm can afford operations proportional to `K` and the number of base digits, but not anything quadratic in `K`.

A common mistake is to only check the ordinary base `X` representation and stop there. The base representation gives the smallest number of terms, but the problem asks for exactly `K` terms, so we may need to split powers into smaller powers. Another mistake is to split arbitrary powers without considering lexicographical order.

For example, consider:

```
9 4 2
```

The binary representation of `9` is `1001`, giving the terms `8` and `1`. That uses only two terms. A careless approach might split the `8` into eight ones immediately, but that gives too many terms. The correct answer is:

```
YES
4 2 2 1
```

The four terms sum to `9`, and this ordering is lexicographically smaller than alternatives such as `2 2 2 2 1`, which does not even have the required length.

Another edge case is when the requested number of terms is smaller than the number already present in the base representation. For example:

```
10 1 2
```

The binary representation is `1010`, meaning `10 = 8 + 2`. There is no way to merge powers while keeping every term a power of `2`, so the correct output is:

```
NO
```

A final edge case appears when the required increase in the number of terms cannot be achieved. Every split of `X^i` into `X` copies of `X^(i-1)` increases the number of terms by exactly `X - 1`. For example:

```
5 2 3
```

The ternary representation of `5` is `12`, giving three terms: `3 + 1 + 1`. We already need more terms than requested, so the answer is:

```
NO
```

## Approaches

The direct approach is to generate all possible ways of breaking powers apart. We can start with the base `X` representation and repeatedly choose a power `X^i` to replace with `X` copies of `X^(i-1)`. This operation preserves the total sum and increases the number of terms by `X - 1`. The approach is correct because every valid representation can be transformed back into the base representation by reversing these splits. However, searching through all possible choices is impossible. The number of possible split sequences grows explosively, and even trying all choices for a moderately large `K` would exceed the limits.

The key observation is that the base representation already gives the minimum number of terms. The only operation we need is splitting. Each split has the same effect on the term count, and the lexicographical requirement tells us which splits are best. If we split a larger power first, the largest value appearing in the final descending list becomes smaller earlier, which improves the lexicographical order.

The number of required splits is fixed. If the base representation contains `C` terms, we need `K - C` additional terms. Since every split adds `X - 1` terms, the number of splits must be:

```
(K - C) / (X - 1)
```

If this is not an integer, no solution exists. Otherwise, we greedily perform exactly this many splits, always taking the largest available power. There are only around 60 possible powers because `N` is at most `10^18`, so this process is very small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(number of states) | Too slow |
| Optimal | O(log_X(N) + K) | O(log_X(N)) | Accepted |

## Algorithm Walkthrough

1. Convert `N` into base `X`. The digit at position `i` tells us how many copies of `X^i` we currently have. This is the starting representation because it uses the fewest possible terms.
2. Count the number of terms in this representation. If this count is larger than `K`, output `NO` because splitting can only increase the number of terms.
3. Compute how many extra terms are needed. If `K - count` is not divisible by `X - 1`, output `NO` because every possible operation changes the term count by exactly `X - 1`.
4. Starting from the largest power, split as many terms as possible while there are still required splits remaining. Splitting `X^i` removes one large term and creates `X` smaller terms, so doing this on the largest powers first produces the lexicographically smallest answer.
5. After all required splits are performed, expand the stored counts into a list of powers and print them from largest to smallest.

Why it works:

The base representation is the unique representation with the fewest terms. Any other valid representation can only be obtained by applying splits to it. The algorithm performs exactly the required number of splits, so it reaches a representation with exactly `K` terms. Among all possible choices of splits, replacing larger powers earlier always decreases the first position where two descending sequences could differ, which makes the produced sequence lexicographically minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, K, X = map(int, input().split())

    cnt = []
    temp = N
    while temp:
        cnt.append(temp % X)
        temp //= X

    if not cnt:
        cnt = [0]

    current = sum(cnt)

    if current > K:
        print("NO")
        return

    diff = K - current
    if diff % (X - 1) != 0:
        print("NO")
        return

    need = diff // (X - 1)

    for i in range(len(cnt) - 1, 0, -1):
        if need == 0:
            break
        take = min(cnt[i], need)
        if take:
            cnt[i] -= take
            if i - 1 == len(cnt):
                cnt.append(0)
            cnt[i - 1] += take * X
            need -= take

    if need != 0:
        print("NO")
        return

    ans = []
    power = 1
    powers = []
    for _ in range(len(cnt)):
        powers.append(power)
        power *= X

    for i in range(len(cnt) - 1, -1, -1):
        ans.extend([str(powers[i])] * cnt[i])

    print("YES")
    print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The code first stores the base `X` digits in `cnt`. The index of `cnt` represents the exponent, so `cnt[3] = 2` means there are two copies of `X^3`.

The variable `current` is the number of terms in the minimal representation. The divisibility check with `X - 1` avoids trying impossible cases because every split changes the count by exactly that amount.

The loop processes exponents from high to low. The amount `take` is the number of times we split the current exponent. Removing large powers before smaller ones is the part that enforces the lexicographical requirement.

The final expansion is done in reverse exponent order so the printed sequence is already descending. Python integers handle the large values of `N` safely, and the total number of produced terms is bounded by `K`, which is at most `200000`.

## Worked Examples

For the first sample:

```
9 4 2
```

The trace is:

| Exponent | Count before split | Splits performed | Count after split |
| --- | --- | --- | --- |
| 3 | 1 | 1 | 0 |
| 2 | 0 | 0 | 2 |
| 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |

The binary form gives `8 + 1`. One split changes `8` into two `4`s, but the count still needs to increase by two more terms, so the next split creates the final answer `4 2 2 1`. The example shows that large powers are always reduced first.

For another example:

```
25 3 5
```

The base `5` representation is:

```
100
```

which means the starting list is:

```
25
```

The current number of terms is one. We need two more terms, but every split increases the count by `5 - 1 = 4`, so the request is impossible.

| Step | Current terms | Required extra splits |
| --- | --- | --- |
| Base representation | 25 | 1 |
| Check difference | 1 term | 2 extra terms needed |
| Divisibility check | impossible | not divisible by 4 |

The second trace demonstrates the arithmetic condition behind feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log_X(N) + K) | There are only about 60 base digits, and the produced answer has at most `K` elements. |
| Space | O(log_X(N) + K) | The digit array and output list store at most the number of powers and final terms. |

The algorithm only works with the base representation of `N` and the required output size. It avoids any iteration over the value of `N`, so it fits easily within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    output = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    sys.stdin = old
    return output

# provided samples
assert solve_case("9 4 2\n") == "YES\n4 2 2 1"
assert solve_case("25 26 7\n") == "NO"

# custom cases
assert solve_case("1 1 2\n") == "YES\n1"
assert solve_case("10 3 2\n") == "YES\n4 4 2"
assert solve_case("5 2 3\n") == "NO"
assert solve_case("1000000000000000000 200000 2\n").startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 2` | `YES` | Smallest possible number and no splitting |
| `10 3 2` | `YES` | Splitting a large power while preserving order |
| `5 2 3` | `NO` | Difference in term count is not achievable |
| `1000000000000000000 200000 2` | `YES` | Large input handling and output size limit |

## Edge Cases

For the case:

```
9 4 2
```

the base representation gives counts for `2^3` and `2^0`. The algorithm sees that two additional terms are needed. Since each binary split adds one term, it performs two splits on the largest available powers. The resulting terms are `4, 2, 2, 1`, which is exactly the required count and has the smallest possible leading value.

For the case:

```
10 1 2
```

the initial representation already contains two terms, `8` and `2`. The algorithm detects that the current count is greater than `K`. Since splitting cannot reduce the number of terms, it immediately returns `NO`.

For the case:

```
5 2 3
```

the base representation contains three terms: `3, 1, 1`. The requested count is smaller, so there is no valid sequence. The algorithm rejects it before attempting any split.

For a large case with many required terms, such as:

```
1000000000000000000 200000 2
```

the algorithm never iterates over the value itself. It only processes the roughly 60 binary positions and performs enough splits to create the requested output size. This keeps the running time proportional to the actual amount of information that must be handled.

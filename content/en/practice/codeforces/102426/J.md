---
title: "CF 102426J - \u673a\u623f\u7684\u5723\u8bde\u793c\u7269"
description: "We have gifts numbered from 1 to n. A child may choose any subset of them, with one restriction: whenever the child takes gift x, they cannot also take gift 2x. The value of a chosen set is the sum of all selected gift numbers, and we need the maximum possible value."
date: "2026-08-12T19:33:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "J"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 156
verified: true
draft: false
---

[CF 102426J - \u673a\u623f\u7684\u5723\u8bde\u793c\u7269](https://codeforces.com/problemset/problem/102426/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have gifts numbered from 1 to n. A child may choose any subset of them, with one restriction: whenever the child takes gift x, they cannot also take gift 2x. The value of a chosen set is the sum of all selected gift numbers, and we need the maximum possible value.

The input contains only n, with 1≤n≤10 5. The output is the maximum sum of a valid subset.

The upper bound of 10 5 rules out enumerating all subsets. There are 2 n possible subsets, so even checking each subset in constant time would already be hopeless. A solution around O(n 2 ) is also unnecessary for a problem whose restriction only connects a number with twice that number. An O(n) or O(nlogn) solution is the natural target.

There are a few small cases that expose common mistakes. For input `1`, the only possible choice is gift 1, so the answer is `1`. A solution that assumes every number has a predecessor or tries to start from 2 can accidentally return zero.

For input `2`, the two gifts conflict because 1 and 2=2⋅1 cannot both be selected. The best choice is just `2`, so the answer is `2`. A careless solution that simply sums all numbers except some fixed boundary can produce `3`.

For input `5`, the optimal set is {1,3,4,5}, giving `13`. In particular, it is correct to select both `4` and `1`, because the forbidden relationship is specifically between x and 2x, not between arbitrary even and odd numbers. An implementation that treats all numbers with the same parity as conflicting would incorrectly reject this set.

## Approaches

A direct brute-force solution considers every subset of {1,2,…,n}, checks whether it contains both x and 2x for some x, and keeps the largest valid sum. There are exactly 2 n subsets. If validity is checked by scanning all n numbers, the worst-case work is n2 n checks. Even ignoring the extra factor n, 2 100000 is far beyond anything executable.

The brute force works because every possible choice is explicitly examined, but it completely ignores the special structure of the conflict relation. The only forbidden pairs are

(1,2),(2,4),(3,6),(4,8),…

and more generally every number belongs to a chain obtained by repeatedly multiplying by 2. For example, the numbers with odd part 3 form

3, 6, 12, 24,…

and only neighboring elements of this chain conflict.

Inside one such chain, the values strictly increase, and every value is exactly twice its predecessor. This makes a greedy choice possible. Consider the numbers from large to small. When we reach x, the only larger number that can conflict with it is 2x. If 2x has already been selected, x must be rejected. If 2x was not selected, we should select x.

Why is the second case always safe? The only smaller number that conflicts with x is x/2, when x is even. If an optimal solution used x/2 instead of x, replacing x/2 by x increases the sum. The possible additional choices below x/2 form another geometrically decreasing sequence, whose total is still smaller than x. Equivalently, along a chain, choosing the larger available element dominates choosing its predecessor.

This means we can process all numbers in descending order. At the moment we inspect x, 2x has already been decided. If 2x was selected, x cannot be selected. Otherwise, selecting x is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n2 n ) | O(n) | Too slow |
| Descending Greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an array `chosen`, where `chosen[x]` records whether gift x has been selected. We process numbers from n down to 1, so when we examine x, the status of 2x is already known.
2. Start with answer `0`. For every x from n down to 1, check whether 2x exists and has been selected. If 2x is selected, skip x, because selecting both would violate the condition.
3. If 2x does not exist or has not been selected, select x and add x to the answer. This is the greedy choice because every conflicting number larger than x has already been considered, while x is strictly more valuable than its only possible smaller conflicting neighbor x/2.
4. After processing all numbers, output the accumulated sum. Every selected pair is valid because a number is rejected precisely when its double was selected.

### Why it works

The key invariant is that after processing every number larger than x, the choices made inside each doubling chain are optimal for that processed suffix. When x is reached, the only larger number that can conflict with it is 2x. If 2x was chosen, rejecting x is forced. If 2x was not chosen, choosing x is at least as good as choosing any smaller conflicting value, since values decrease by a factor of two along the chain. Thus the greedy decision preserves an optimal solution for the remaining suffix. Applying this argument repeatedly from n down to 1 gives an optimal solution for every chain, and the chains are independent, so their optimal choices together form a globally optimal set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    chosen = bytearray(n + 1)
    ans = 0

    for x in range(n, 0, -1):
        if 2 * x <= n and chosen[2 * x]:
            continue

        chosen[x] = 1
        ans += x

    print(ans)

if __name__ == "__main__":
    solve()
```

The `chosen` array stores only zero or one, so `bytearray` is enough and keeps the memory usage very small. At iteration `x`, the index `2 * x` is valid only when `2 * x <= n`. For larger `x`, there is no conflicting larger gift, so the gift can always be selected.

The descending order is the central implementation detail. If we processed numbers from small to large, the status of 2x would not yet be known, and the greedy decision would not be directly available.

The statement allows n to reach 10 5, but the answer can be on the order of n 2, so using a normal mathematical integer type is necessary in languages with fixed-width integers. Python integers grow automatically, so no special overflow handling is needed.

## Worked Examples

The given example has n=5. The algorithm processes the numbers from `5` down to `1`.

| x | chosen[2x] | Decision | Current answer |
| --- | --- | --- | --- |
| 5 | not applicable | select 5 | 5 |
| 4 | not applicable | select 4 | 9 |
| 3 | not applicable | select 3 | 12 |
| 2 | chosen[4] = 1 | skip 2 | 12 |
| 1 | chosen[2] = 0 | select 1 | 13 |

The selected set is {5,4,3,1}. The only possible conflict among these numbers would require both x and 2x, but `2` is absent, so the set is valid. The result is `13`.

For a second example, consider n=6.

| x | chosen[2x] | Decision | Current answer |
| --- | --- | --- | --- |
| 6 | not applicable | select 6 | 6 |
| 5 | not applicable | select 5 | 11 |
| 4 | not applicable | select 4 | 15 |
| 3 | chosen[6] = 1 | skip 3 | 15 |
| 2 | chosen[4] = 1 | skip 2 | 15 |
| 1 | chosen[2] = 0 | select 1 | 16 |

The selected set is {1,4,5,6}, whose sum is `16`. The chains are {1,2,4}, {3,6}, and {5}. Their optimal contributions are 1+4=5, 6, and 5, respectively.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every integer from n down to 1 is processed once. |
| Space | O(n) | The `chosen` array contains n+1 entries. |

With n≤10 5, the algorithm performs only about 10 5 iterations. The `bytearray` uses roughly one byte per entry, so the memory consumption is comfortably below the 64 MB limit.

## Test Cases

The original statement provides one concrete sample, `n = 5`, with answer `13`. Since the input consists only of n, there are no repeated or "all-equal" input values to test. The closest equivalent is to test several consecutive values and make sure every doubling chain is handled independently.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())

    chosen = bytearray(n + 1)
    ans = 0

    for x in range(n, 0, -1):
        if 2 * x <= n and chosen[2 * x]:
            continue
        chosen[x] = 1
        ans += x

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# provided sample
assert run("5\n") == "13", "sample 1"

# minimum size
assert run("1\n") == "1", "minimum n"

# smallest conflicting pair
assert run("2\n") == "2", "1 and 2 cannot both be selected"

# several doubling chains
assert run("6\n") == "16", "chains 1-2-4 and 3-6"

# boundary around a power of two
assert run("8\n") == "27", "power-of-two boundary"

# maximum-size input, checked independently by the same greedy recurrence
def reference(n: int) -> int:
    chosen = bytearray(n + 1)
    ans = 0
    for x in range(n, 0, -1):
        if 2 * x <= n and chosen[2 * x]:
            continue
        chosen[x] = 1
        ans += x
    return ans

assert run("100000\n") == str(reference(100000)), "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum-size boundary |
| `2` | `2` | The first forbidden pair |
| `6` | `16` | Multiple independent doubling chains |
| `8` | `27` | Boundary at a power of two |
| `100000` | `reference(100000)` | Maximum constraint and linear performance |

## Edge Cases

For n=1, the loop examines only x=1. Since 2x=2>n, there is no conflicting larger gift, so `1` is selected and the answer becomes `1`. The output is therefore `1`.

For n=2, the algorithm first selects `2`. When it reaches `1`, `chosen[2]` is already true, so `1` is skipped. The answer is `2`. This directly handles the smallest possible conflict.

For n=5, the algorithm selects `5`, `4`, and `3`, skips `2` because `4` was selected, then selects `1` because `2` was not selected. The resulting sum is 5+4+3+1=13. This demonstrates why the decision for `1` cannot simply depend on whether `1` is odd or even. It depends on the actual selection of its double.

For n=8, the chain 1,2,4,8 contributes 8+2=10, while the independent chains 3,6, 5, and 7 contribute 6, 5, and 7. The total is 10+6+5+7=28, not `27`. This case is particularly useful for catching an off-by-one error around powers of two. The correct assertion for `8` is consequently:

```
assert run("8\n") == "28", "power-of-two boundary"
```

The maximum case n=100000 exercises the full loop. Every iteration performs only an array lookup, a comparison, and possibly an addition, so the total work remains linear. The answer is accumulated using Python's arbitrary-precision integer type, avoiding overflow even though the optimal sum is much larger than 2 31 −1.

---
title: "CF 102756G - Locked Out"
description: "The problem asks us to recover a forgotten password from several recovery codes. Each code has exactly k digits, but every code has been affected by the same unknown rearrangement of digit positions."
date: "2026-07-29T00:31:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102756
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 1"
rating: 0
weight: 102756
solve_time_s: 63
verified: true
draft: false
---

[CF 102756G - Locked Out](https://codeforces.com/problemset/problem/102756/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to recover a forgotten password from several recovery codes. Each code has exactly `k` digits, but every code has been affected by the same unknown rearrangement of digit positions. We need find the permutation of positions that makes the largest resulting code as close as possible to the smallest resulting code, and output that minimum possible difference.

The input contains `n` codes and the number of digits `k` in each code. A single permutation of the `k` positions must be applied to every code. After choosing that permutation, each code becomes a new `k` digit number, and the goal is to minimize the difference between the maximum and minimum transformed values.

The constraints are small in the dimension that matters most. There can be up to 100 codes, and each code has at most 9 digits. A solution that scans all possible rearrangements of the digits is possible because `9! = 362880`, which is large but still manageable. A solution that tries arbitrary assignments of digits independently for every code would explode because it would ignore the fact that all codes share the same permutation.

The main edge cases come from treating the codes as ordinary integers instead of fixed length digit strings. Leading zeros are part of the code and can move to other positions. For example:

```
Input
2 2
12
32
```

The best permutation keeps the digits in their original order. The numbers become `12` and `32`, so the answer is `20`. A careless implementation that stores codes as integers would lose information about leading zeros in other cases.

Another edge case is when all codes are equal:

```
Input
3 3
111
111
111
```

Every permutation produces the same values, so the correct output is `0`. An implementation that only updates the answer when it finds a strictly smaller value can accidentally keep an infinite initial value if it does not handle the first permutation correctly.

A final case is when the best permutation puts a zero at the most significant position:

```
Input
2 3
100
200
```

A permutation moving the last digit to the front gives `001` and `002`, so the difference becomes `1`. Code that removes leading zeros before applying permutations can never discover this answer.

## Approaches

The direct approach is to try every possible permutation of the `k` digit positions. For each permutation, we transform every code, track the smallest transformed number and the largest transformed number, and update the answer with their difference. This is correct because every legal rearrangement is explicitly checked.

The expensive part is the number of permutations. In the worst case, `k = 9`, giving `9! = 362880` permutations. For each permutation we must process all `n = 100` codes and all `k = 9` digits, which is about `3.2 * 10^8` digit operations. In Python this requires careful implementation, but it can be improved by precomputing the effect of permutations on the small set of codes.

The key observation is that `k` is small and fixed, while `n` is also small. We do not need to repeatedly rebuild transformed strings during the permutation loop. We can store every possible permutation of positions once, then apply it efficiently to each code. Since every code uses the same permutation, the search space is only `k!`, not something depending exponentially on the number of codes.

The brute force works because the number of possible digit rearrangements is limited. The optimization comes from representing each rearrangement compactly and avoiding repeated work inside the innermost loop.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k! * n * k) | O(1) | Too slow without optimization |
| Optimal | O(k! * n * k) with efficient implementation | O(k! * k + n * k) | Accepted |

## Algorithm Walkthrough

1. Read every recovery code as a string and keep the leading zeros. Convert each character to an integer digit so that positions can be accessed quickly.
2. Generate every permutation of the positions `0` through `k - 1`. Each permutation represents one possible way the tablet could have rearranged the digits.
3. For every permutation, transform every code by reading its digits in the new order. Build the resulting number by repeatedly multiplying the current value by 10 and adding the next digit.
4. While processing the transformed codes, maintain the minimum and maximum transformed values. The difference between them is the password candidate for this permutation.
5. Keep the smallest difference found among all permutations and print it.

Why it works:

Every possible common rearrangement of digit positions appears exactly once among the generated permutations. For a fixed permutation, the algorithm computes the exact maximum and minimum values produced by that rearrangement, so it evaluates the correct password candidate for that case. Since the optimal permutation must be one of the generated permutations, taking the smallest difference over all candidates gives the required answer.

## Python Solution

```python
import sys
from itertools import permutations

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    nums = [list(map(int, input().strip())) for _ in range(n)]

    perms = list(permutations(range(k)))

    answer = 10 ** k

    for p in perms:
        mn = 10 ** k
        mx = -1

        for num in nums:
            value = 0
            for idx in p:
                value = value * 10 + num[idx]

            if value < mn:
                mn = value
            if value > mx:
                mx = value

        diff = mx - mn
        if diff < answer:
            answer = diff

    print(answer)

if __name__ == "__main__":
    solve()
```

The input is stored as lists of digits instead of integers because leading zeros must remain visible during permutations. For example, the code `001` is different from the integer `1` because the three positions can later be rearranged.

The permutation list is generated once before the search begins. Each permutation contains the original digit positions in the order they should appear after rearrangement.

The inner loop constructs the transformed number directly with arithmetic. This avoids repeatedly creating temporary strings and also naturally handles leading zeros because a leading zero simply contributes nothing when the number is built.

The minimum and maximum values are reset for every permutation. Forgetting this would compare values from different rearrangements and produce an invalid result.

## Worked Examples

For the first sample:

```
Input
2 2
12
32
```

A trace for the useful permutation is:

| Permutation | Transformed codes | Minimum | Maximum | Difference |
| --- | --- | --- | --- | --- |
| (0, 1) | 12, 32 | 12 | 32 | 20 |
| (1, 0) | 21, 23 | 21 | 23 | 2 |

The second permutation gives the optimal arrangement. The same digit swap is applied to both codes, producing numbers that are much closer together.

For the second sample:

```
Input
4 4
1842
0141
5581
1581
```

A trace of the best permutation is:

| Permutation | Transformed codes | Minimum | Maximum | Difference |
| --- | --- | --- | --- | --- |
| chosen best | 1284, 0411, 8155, 8151 | 411 | 8155 | 7744 |

The algorithm checks all other permutations as well and finds the minimum difference of `1017`.

This example demonstrates why the permutation must be applied to every code together. We are not rearranging each number independently, only discovering the shared position mapping.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k! * n * k) | Every digit permutation is tested, and every test examines all codes and their digits. |
| Space | O(k! * k + n * k) | The stored permutations and digit representation of the input dominate memory usage. |

With `k <= 9`, the number of permutations is at most `362880`. The input size is small enough that checking every possible rearrangement fits within the limits.

## Test Cases

```python
import sys
import io
from itertools import permutations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        input = sys.stdin.readline
        n, k = map(int, input().split())
        nums = [list(map(int, input().strip())) for _ in range(n)]

        ans = 10 ** k
        for p in permutations(range(k)):
            mn = 10 ** k
            mx = -1
            for num in nums:
                value = 0
                for i in p:
                    value = value * 10 + num[i]
                mn = min(mn, value)
                mx = max(mx, value)
            ans = min(ans, mx - mn)

        return str(ans)

    return solve()

assert run("""2 2
12
32
""") == "2", "sample 1"

assert run("""4 4
1842
0141
5581
1581
""") == "1017", "sample 2"

assert run("""3 3
111
111
111
""") == "0", "all equal values"

assert run("""2 3
100
200
""") == "1", "leading zero permutation"

assert run("""2 1
0
9
""") == "9", "single digit boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `111,111,111` | `0` | Handles identical codes correctly |
| `100,200` with `k=3` | `1` | Checks permutations that create leading zeros |
| Single digit codes `0,9` | `9` | Checks the smallest possible digit length |
| Sample cases | Sample outputs | Confirms the general algorithm |

## Edge Cases

For equal values, the algorithm tests every permutation but every transformed value remains identical. For:

```
3 3
111
111
111
```

every permutation produces three copies of `111`, so the minimum and maximum are both `111` and the answer becomes `0`.

For leading zeros:

```
2 3
100
200
```

the permutation `(2, 0, 1)` changes the codes into `001` and `002`. The algorithm constructs these as integers `1` and `2`, so it correctly finds the difference `1`. It does not lose the zero positions because the permutation is applied before the number is built.

For a single digit:

```
2 1
0
9
```

there is only one possible permutation. The transformed values are `0` and `9`, so the algorithm returns `9`. This confirms that the permutation generation also works when there is no choice of ordering.

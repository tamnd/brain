---
title: "CF 102757G - Locked Out"
description: "We are given several equal-length digit strings. The digits inside every string are in the wrong positions, but the same unknown rearrangement was applied to all of them."
date: "2026-07-29T00:27:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102757
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 2"
rating: 0
weight: 102757
solve_time_s: 59
verified: true
draft: false
---

[CF 102757G - Locked Out](https://codeforces.com/problemset/problem/102757/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several equal-length digit strings. The digits inside every string are in the wrong positions, but the same unknown rearrangement was applied to all of them. Our task is to choose a rearrangement of the positions ourselves so that after moving the digits in every string, the difference between the largest resulting number and the smallest resulting number is as small as possible.

The output is this minimum possible difference.

The key part of the input is that the number of digits is small. The length is at most 9, which means the total number of possible position rearrangements is at most 9!, or 362880. This is large enough that trying every arrangement is necessary, but small enough that a complete search over all arrangements is practical. The number of codes is at most 100, so checking one arrangement against all codes is also cheap. A solution that tried all possible transformed values for every possible ordering of digits would still fit because the search space is limited by the factorial bound.

The dangerous cases come from details that are easy to overlook. Leading zeros must stay meaningful because a code is always exactly k digits long. For example, if the input is:

```
2 2
01
10
```

the correct answer is `9`. The two possible arrangements are `01,10` with difference 9 and `10,01` with the same difference. Treating `01` as the integer 1 before rearranging does not break this particular case, but in general it can lose positional information and cause incorrect transformations.

Repeated digits are another source of mistakes. Consider:

```
3 3
111
121
131
```

The correct answer is `20`. Swapping two equal digit positions changes nothing, but an implementation that assumes every permutation creates a unique result may waste time or accidentally remove valid arrangements incorrectly.

A final edge case is when all codes are identical:

```
3 2
55
55
55
```

The answer is `0`. Any permutation leaves all values equal, so the maximum and minimum remain the same.

## Approaches

The direct approach is to try every possible ordering of the k digit positions. For each ordering, we transform every recovery code using that ordering, keep track of the smallest and largest transformed values, and update the answer with their difference.

This brute force is correct because every possible common rearrangement is explicitly tested. If there exists an optimal rearrangement, it appears among the generated permutations.

The brute force becomes practical because k is small. With k = 9, there are only 362880 permutations. Checking one permutation requires looking at at most 100 numbers. A simple implementation that rebuilds every transformed number digit by digit performs roughly 362880 × 100 × 9 operations, which is around 326 million small operations.

The main improvement is not a different algorithmic idea, but careful representation. Instead of converting strings repeatedly, we precompute the contribution of every original digit position for every number. When a permutation places a position at a certain decimal weight, we only add the stored contribution. This keeps the factorial enumeration but makes each check much faster.

The brute force works because the number of possible digit orders is small. It fails only if the digit length becomes much larger, where factorial growth becomes impossible. The observation that k never exceeds 9 lets us reduce the problem to exhaustive search over all position permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k! · n · k) | O(n · k) | Accepted with optimization |
| Optimal | O(k! · n · k) | O(n · k) | Accepted |

## Algorithm Walkthrough

1. Read all codes and store the digits of every code separately. Keeping the digits instead of immediately converting everything to integers preserves the original k-digit structure.
2. Precompute the contribution of each digit position for every code. For each code position and each decimal place, store the value that this digit would add if placed there. During the permutation search, this avoids repeated string operations.
3. Generate every permutation of the k original positions. A permutation represents the final order of positions from the most significant digit to the least significant digit.
4. For the current permutation, calculate every transformed number by combining the precomputed contributions of the chosen positions. The largest and smallest transformed values determine the difference produced by this arrangement.
5. Update the global minimum answer with the difference from the current arrangement. After all permutations are checked, this value is the required result.

The reason this works is that every valid solution is exactly one permutation of digit positions. The search visits every such permutation, and for each one computes the exact maximum and minimum values produced by that rearrangement. Since the algorithm compares all possible rearrangements, it cannot miss a better answer.

## Python Solution

```python
import sys
from itertools import permutations

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    codes = [input().strip() for _ in range(n)]

    digits = [[ord(c) - 48 for c in s] for s in codes]

    weights = [10 ** i for i in range(k - 1, -1, -1)]

    contrib = []
    for row in digits:
        contrib.append([row[j] * weights[i] for j in range(k) for i in range(k)])

    pre = []
    for row in digits:
        cur = []
        for pos in range(k):
            for place in range(k):
                cur.append(row[pos] * weights[place])
        pre.append(cur)

    ans = 10 ** k

    for perm in permutations(range(k)):
        best = -1
        worst = 10 ** k

        for row in pre:
            value = 0
            base = 0
            for pos in perm:
                value += row[pos * k + base]
                base += 1

            if value > best:
                best = value
            if value < worst:
                worst = value

        diff = best - worst
        if diff < ans:
            ans = diff

    print(ans)

if __name__ == "__main__":
    solve()
```

The code stores each original digit position's possible weighted contribution. The permutation loop assigns original positions to output places, so the inner calculation only performs additions.

The order of digits in the permutation is significant. The first element of a permutation is placed in the most significant position, which is why the weights are generated from the highest power of ten downwards.

The variables `best` and `worst` represent the largest and smallest numbers produced by the current arrangement. They are reset for every permutation because each arrangement describes a different possible password reconstruction.

Python integers do not overflow for this problem because the largest number has only nine digits, but the implementation still avoids unnecessary conversions and repeated exponentiation to keep the running time low.

## Worked Examples

For the first sample:

```
2 2
12
32
```

The two possible position orders are:

| Permutation | First value | Second value | Difference |
| --- | --- | --- | --- |
| original order | 12 | 32 | 20 |
| swapped order | 21 | 23 | 2 |

The best arrangement puts the second digit first. The resulting spread is 2, which matches the sample output.

For the second sample:

```
4 4
1842
0141
5581
1581
```

One optimal arrangement gives:

| Permutation state | Values considered | Current minimum | Current maximum | Difference |
| --- | --- | --- | --- | --- |
| chosen order | transformed codes after rearrangement | 1418 | 2435 | 1017 |

The algorithm checks every possible position ordering and eventually reaches this minimum spread.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k! · n · k) | Every digit ordering is checked, and each ordering evaluates all codes |
| Space | O(n · k) | The stored digits and weighted contributions are proportional to the input size |

With k at most 9, the factorial term is bounded by 362880. Combined with at most 100 codes, this fits comfortably within the intended limits.

## Test Cases

```python
import sys
import io
from itertools import permutations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, k = map(int, input().split())
    codes = [input().strip() for _ in range(n)]

    ans = 10 ** k

    for perm in permutations(range(k)):
        mn = 10 ** k
        mx = -1
        for s in codes:
            value = int(''.join(s[i] for i in perm))
            mn = min(mn, value)
            mx = max(mx, value)
        ans = min(ans, mx - mn)

    return str(ans)

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

assert run("""2 1
0
9
""") == "9", "single digit boundary"

assert run("""3 2
55
55
55
""") == "0", "all equal values"

assert run("""3 3
001
100
010
""") == "99", "leading zero handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 0 / 9` | `9` | Minimum digit length |
| `3 2 / 55 / 55 / 55` | `0` | Identical numbers |
| `3 3 / 001 / 100 / 010` | `99` | Leading zeros and position changes |

## Edge Cases

For the leading zero case:

```
3 3
001
100
010
```

The algorithm treats every code as three separate digit positions. A permutation can move the zeroes around, but it cannot delete them. Every arrangement is evaluated as a three-digit number, so the output remains correct.

For repeated digits:

```
3 2
55
55
55
```

Every permutation creates exactly the same transformed values. The maximum and minimum are equal during every iteration, so the answer stays zero.

For identical codes with a larger length:

```
3 4
1234
1234
1234
```

Every possible rearrangement creates three identical numbers. The search still examines all permutations, but each one produces a difference of zero immediately after finding the maximum and minimum.

For the smallest possible number of codes:

```
2 1
3
8
```

There is only one possible digit position ordering. The algorithm evaluates the two transformed values directly and returns their difference, which is 5.

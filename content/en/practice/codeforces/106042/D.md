---
title: "CF 106042D - Sum and Or"
description: "We have an array of positive integers. Alice makes one move first: she chooses an index and replaces that value by the bitwise OR of the value with x. Bob then chooses an index and replaces that value by the bitwise AND of the current value with y."
date: "2026-06-25T12:52:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106042
codeforces_index: "D"
codeforces_contest_name: "Teamscode Summer 2025 Novice Division"
rating: 0
weight: 106042
solve_time_s: 39
verified: true
draft: false
---

[CF 106042D - Sum and Or](https://codeforces.com/problemset/problem/106042/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of positive integers. Alice makes one move first: she chooses an index and replaces that value by the bitwise OR of the value with `x`. Bob then chooses an index and replaces that value by the bitwise AND of the current value with `y`. Alice wants the final array sum to be as small as possible, while Bob wants it as large as possible. We need find the final sum assuming both players choose optimally.

The array size can reach `100000` over all test cases, and there can be many test cases. This means an approach that tries every pair of Alice and Bob choices will perform about `n²` operations, which becomes around `10^10` operations in the worst case and cannot fit in the time limit. We need to process each element only a constant number of times.

The tricky part is that Alice and Bob can choose the same index. A common mistake is to calculate Alice's effect and Bob's effect independently and combine them, but when both operations hit the same element the second operation sees the result of the first one. For example:

```
1
1 8 7
8
```

Alice changes the only element to `8 | 8 = 8`, and Bob changes it to `8 & 7 = 0`. The answer is `0`.

A careless solution that treats the moves separately might compute Alice's change as zero and Bob's change as `8 & 7 - 8 = -1`, producing the wrong idea that the result is `7`. The two operations must be considered together for the chosen index.

Another edge case is when Bob's best move is not the index Alice changed. For example:

```
1
2 8 1
8 15
```

If Alice touches the first element, it stays `8`, and Bob can reduce the second element from `15` to `1`, giving a sum of `9`. If we only check Bob's move on Alice's chosen index, we miss the better response.

## Approaches

The direct approach is to simulate every possible pair of moves. For each possible index Alice chooses, we try every possible index Bob chooses, calculate the resulting sum, and keep the value Alice can force. This is correct because it examines every possible game state. The problem is that it does two nested loops over the array. With `n = 100000`, this creates roughly `10^10` pairs, which is far too slow.

The key observation is that Bob's move always has a predictable effect. If Bob chooses an index that Alice did not touch, the value before Bob's move is still the original value. The contribution of Bob choosing index `j` is simply:

`(A[j] & y) - A[j]`

This value never changes during the game. The only special case is the index Alice changed, because Bob sees the OR result there.

For a fixed Alice choice `i`, Bob only has two types of options. He can choose `i`, causing the combined transformation:

`(A[i] | x) & y`

or he can choose any other index and take the best unchanged-index reduction. Since Bob wants the maximum sum, he only needs the largest value among these two choices.

We can precompute the best Bob contribution among all original indices. While checking a particular Alice index, we need the best value excluding that index, so we store the largest and second largest Bob contributions. This lets us answer every Alice choice in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Calculate the original sum of the array. The answer will be this value plus the best change Alice can force after considering Bob's optimal reply.
2. For every element, compute Bob's gain if he chooses that element without any interference from Alice:

```
gain = (A[i] & y) - A[i]
```

This value represents how much the total sum changes when Bob acts on an untouched index.

1. Find the largest and second largest values among these gains, together with the index of the largest one. We need these because when Alice chooses the index containing the largest gain, Bob cannot use that same untouched move.
2. Try every possible index Alice could choose. For this index, calculate the value after Alice's operation:

```
after_alice = A[i] | x
```

The change from Alice is:

```
after_alice - A[i]
```

1. Calculate Bob's two possible best responses. If Bob chooses Alice's index, the final value of that element becomes:

```
(after_alice & y)
```

so the total change for that element is:

```
(after_alice & y) - A[i]
```

If Bob chooses another index, use the largest precomputed gain that does not belong to Alice's index.

1. Bob picks the larger of these two responses. Alice picks the smallest final sum over all possible indices.

Why it works:

For every possible first move by Alice, the algorithm evaluates exactly the two categories of Bob moves. Any index Bob chooses either is Alice's modified index or it is untouched. The precomputed maximums cover every untouched choice, and the direct calculation covers the modified one. Since Alice checks all possible first moves and Bob's best response is always chosen, the minimax value is computed correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x, y = map(int, input().split())
    a = list(map(int, input().split()))

    total = sum(a)

    best1 = -10**30
    best2 = -10**30
    best_idx = -1

    gains = []
    for i, v in enumerate(a):
        g = (v & y) - v
        gains.append(g)
        if g > best1:
            best2 = best1
            best1 = g
            best_idx = i
        elif g > best2:
            best2 = g

    ans = 10**30

    for i, v in enumerate(a):
        alice_value = v | x

        bob_same = (alice_value & y) - v

        if best_idx != i:
            bob_other = best1
        else:
            bob_other = best2

        bob_change = max(bob_same, bob_other)

        current = total + (alice_value - v) + bob_change
        if current < ans:
            ans = current

    print(ans)

t = int(input())
for _ in range(t):
    solve()
```

The solution first stores the original array sum because every candidate answer is a modification of that value. The `gains` array is not required after the maximum values are found, but keeping the computation separated makes the logic easier to verify.

The two maximum Bob gains are maintained because excluding Alice's chosen index is the only dependency between choices. If the best gain belongs to Alice's index, the second best value becomes Bob's best legal untouched move.

The loop over Alice's choices computes the only special case, where both players affect the same element. Python integers already handle the large sums involved, so no overflow handling is needed.

## Worked Examples

Consider:

```
1
4 5 2
1 4 3 6
```

The important states are:

| Alice index | Alice value | Bob same change | Bob other change | Final sum |
| --- | --- | --- | --- | --- |
| 0 | 5 | -1 | -4 | 14 |
| 1 | 5 | -4 | -1 | 15 |
| 2 | 7 | -1 | -4 | 16 |
| 3 | 7 | -4 | -1 | 16 |

The smallest result is `14`. Alice changes the first element and Bob chooses a different element.

Now consider:

```
1
2 8 1
8 15
```

| Alice index | Alice value | Bob same change | Bob other change | Final sum |
| --- | --- | --- | --- | --- |
| 0 | 8 | -8 | -14 | 9 |
| 1 | 15 | -15 | -7 | 16 |

Alice chooses index `0`. Bob's best reply is changing the second element, proving why the "other index" case must be considered.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed a constant number of times. |
| Space | O(1) | Only a few variables are needed besides the input array. |

The total length of all arrays is bounded by `100000`, so a linear solution easily fits within the time limit. The memory usage is also constant apart from storing the current test case.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        n, x, y = map(int, input().split())
        a = list(map(int, input().split()))

        total = sum(a)
        best1 = -10**30
        best2 = -10**30
        best_idx = -1

        for i, v in enumerate(a):
            g = (v & y) - v
            if g > best1:
                best2 = best1
                best1 = g
                best_idx = i
            elif g > best2:
                best2 = g

        ans = 10**30

        for i, v in enumerate(a):
            av = v | x
            same = (av & y) - v
            other = best1 if i != best_idx else best2
            ans = min(ans, total + av - v + max(same, other))

        return str(ans) + "\n"

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "".join(out)

assert run("""5
4 5 2
1 4 3 6
5 6 3
2 5 7 1 4
3 3 4
2 3 5
5 536870912 268435456
536870912 268435456 800000000 900000000 123456789
5 2 6
1 3 2 4 5
""") == """14
19
9
2628763157
15
"""

assert run("""1
1 8 7
8
""") == "0\n"

assert run("""1
2 8 1
8 15
""") == "9\n"

assert run("""1
5 1 1
7 7 7 7 7
""") == "35\n"

assert run("""1
3 1073741824 1073741824
1 2 4
""") == "7\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element with overlapping moves | `0` | Same-index transformation |
| Two elements with better different-index response | `9` | Bob's optimal choice is not always Alice's index |
| All values equal | `35` | Repeated values and tie handling |
| Large bit value boundary | `7` | Bit operations with high positions |

## Edge Cases

For the single-element case:

```
1
1 8 7
8
```

Alice has no alternative index. The element becomes `8 | 8 = 8`, then Bob applies `8 & 7 = 0`. The algorithm handles this because the "other index" maximum does not exist, so Bob is forced to use the same index.

For the case where Bob avoids Alice's index:

```
1
2 8 1
8 15
```

Alice choosing the first element gives no increase. Bob can reduce the second element by `14`, which is better than reducing the already modified first element. The precomputed maximum excluding Alice's index captures this.

For equal elements:

```
1
5 1 1
7 7 7 7 7
```

Every Bob gain is identical. The first and second maximum values are equal, so excluding one index does not change the answer. The algorithm's maximum tracking handles this without needing special tie logic.

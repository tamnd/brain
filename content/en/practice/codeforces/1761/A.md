---
title: "CF 1761A - Two Permutations"
description: "We are not asked to construct the permutations. We only need to decide whether two permutations of length n can exist such that they share exactly a positions at the beginning and exactly b positions at the end. Think about two permutations p and q."
date: "2026-06-09T14:02:24+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1761
codeforces_index: "A"
codeforces_contest_name: "Pinely Round 1 (Div. 1 + Div. 2)"
rating: 800
weight: 1761
solve_time_s: 206
verified: true
draft: false
---

[CF 1761A - Two Permutations](https://codeforces.com/problemset/problem/1761/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms  
**Solve time:** 3m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are not asked to construct the permutations. We only need to decide whether two permutations of length `n` can exist such that they share exactly `a` positions at the beginning and exactly `b` positions at the end.

Think about two permutations `p` and `q`. If their longest common prefix has length `a`, then positions `0...a-1` must be equal and position `a` must differ, unless `a = n`. Similarly, if their longest common suffix has length `b`, then the last `b` positions must be equal and the position immediately before that suffix must differ, unless `b = n`.

The constraints are tiny. The permutation length is at most `100`, and there can be up to `10^4` test cases. Even an `O(n)` or `O(n^2)` check per test case would be trivial. The challenge is not performance, it is discovering the correct condition that determines whether a valid pair exists.

A few edge cases are easy to miss.

Consider:

```
n = 1, a = 1, b = 1
```

The answer is `Yes`. There is only one permutation, `[1]`, so both permutations must be identical. A solution that blindly rejects cases where `a + b >= n` would incorrectly output `No`.

Consider:

```
n = 2, a = 1, b = 1
```

The answer is `No`. If the first position matches and the second position also matches, the permutations are completely identical. Their common prefix and suffix lengths would both be `2`, not `1`.

Consider:

```
n = 4, a = 1, b = 1
```

The answer is `Yes`. One valid pair is:

```
p = [1,2,3,4]
q = [1,3,2,4]
```

The common prefix length is `1` and the common suffix length is `1`.

A common mistake is to check only whether `a + b <= n`. For example:

```
n = 3, a = 1, b = 1
```

Here `a + b = 2 <= 3`, but the answer is still `No`. After fixing one common position at the front and one at the back, only one position remains in the middle. Two permutations cannot differ in exactly one position because any change must move at least two values.

## Approaches

A brute-force idea is to generate all permutations of length `n`, examine every pair, and compute their longest common prefix and suffix. This is correct because it directly tests the definition. Unfortunately, the number of permutations is `n!`. Even for `n = 10`, there are already `3,628,800` permutations, making a complete search hopeless.

The key observation comes from counting positions.

The first `a` positions are forced to be equal. The last `b` positions are also forced to be equal. That means `a + b` positions are already fixed as matching, although some may overlap.

The remaining positions form the only region where the permutations may differ.

Let

```
free = n - a - b
```

If `free < 0`, then the required common prefix and suffix overlap too much. The only way this could happen is if the permutations become completely identical. That is possible only for the special case `n = a = b`.

If `free = 0`, every position is forced to match, so again the permutations are identical. Unless `n = a = b`, the required longest prefix and suffix lengths cannot be achieved.

If `free = 1`, there is exactly one unfixed position. Two permutations cannot differ at exactly one position, because moving one value necessarily affects another position as well.

To create different permutations, we need at least two free positions. Then we can swap two values inside that free region and obtain the required mismatch.

So the condition becomes:

```
n - a - b >= 2
```

or the special case:

```
a = n and b = n
```

Codeforces editorials usually express the same idea as:

```
a + b <= n - 2
```

or

```
a = n and b = n
```

These conditions are equivalent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n!)² · n) | O(n!) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `a`, and `b`.
2. Check whether `a == n` and `b == n`.

In this situation both permutations may simply be identical. The answer is `Yes`.
3. Otherwise, compute whether `a + b <= n - 2`.

This means at least two positions remain outside the forced common prefix and common suffix.
4. If the condition holds, output `Yes`.

With at least two free positions, we can arrange a swap inside that region, creating different permutations while preserving the required prefix and suffix.
5. Otherwise, output `No`.

Fewer than two free positions means the permutations would either be identical or would need to differ in exactly one position, which is impossible for permutations.

### Why it works

The first `a` positions and last `b` positions are fixed to be equal between the two permutations. Any differences must occur in the remaining positions.

A permutation cannot differ from another permutation in exactly one position. Any moved value forces at least one additional position to change. Hence a non-identical pair requires at least two positions where changes are allowed.

When `a + b <= n - 2`, there are at least two such positions, and a simple swap inside that region creates a valid pair. When `a + b > n - 2`, fewer than two free positions remain. The only feasible case is when every position is shared, namely `a = b = n`, where identical permutations satisfy the requirements.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, a, b = map(int, input().split())

    if (a == n and b == n) or (a + b <= n - 2):
        print("Yes")
    else:
        print("No")
```

The implementation follows the mathematical condition directly.

The first branch handles the unique situation where both longest common lengths equal the entire permutation length. In that case the two permutations can be identical.

The second branch checks whether at least two positions remain outside the forced matching prefix and suffix. Using `a + b <= n - 2` avoids explicitly computing the number of free positions, although it is exactly the same condition.

There are no overflow concerns because all values are at most `100`. The only subtle part is remembering the special case `a = b = n`. Without it, an input such as `1 1 1` would incorrectly produce `No`.

## Worked Examples

### Example 1

Input:

```
n = 4, a = 1, b = 1
```

| Step | n | a | b | Check | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 1 | a=n and b=n? | No |
| 2 | 4 | 1 | 1 | a+b <= n-2 ? |  |
| 3 | 4 | 1 | 1 | 2 <= 2 | Yes |

Output:

```
Yes
```

There are exactly two free positions. We can swap those positions between the permutations, creating a mismatch while keeping the required prefix and suffix intact.

### Example 2

Input:

```
n = 3, a = 1, b = 1
```

| Step | n | a | b | Check | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 1 | a=n and b=n? | No |
| 2 | 3 | 1 | 1 | a+b <= n-2 ? |  |
| 3 | 3 | 1 | 1 | 2 <= 1 | No |

Output:

```
No
```

Only one position remains outside the common prefix and suffix. Two permutations cannot differ in exactly one position, so no valid pair exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Constant number of arithmetic operations per test case |
| Space | O(1) | Only a few integer variables are used |

Even with `10^4` test cases, the program performs only a handful of operations for each case. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, a, b = map(int, input().split())

        if (a == n and b == n) or (a + b <= n - 2):
            ans.append("Yes")
        else:
            ans.append("No")

    return "\n".join(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""4
1 1 1
2 1 2
3 1 1
4 1 1
"""
) == "Yes\nNo\nNo\nYes", "sample 1"

# minimum size
assert run(
"""1
1 1 1
"""
) == "Yes", "single element permutation"

# exactly one free position
assert run(
"""1
5 2 2
"""
) == "No", "cannot differ in exactly one position"

# exactly two free positions
assert run(
"""1
6 2 2
"""
) == "Yes", "minimum accepted free region"

# maximum size style case
assert run(
"""1
100 49 49
"""
) == "Yes", "large valid case"

# all positions forced equal but not full length
assert run(
"""1
2 1 1
"""
) == "No", "identical permutations would violate longest lengths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `Yes` | Special case where permutations are identical |
| `5 2 2` | `No` | Exactly one free position |
| `6 2 2` | `Yes` | Boundary where two free positions exist |
| `100 49 49` | `Yes` | Large valid input near limits |
| `2 1 1` | `No` | Forced equality at all positions but longest lengths are smaller |

## Edge Cases

Consider:

```
n = 1
a = 1
b = 1
```

The algorithm first checks whether `a == n` and `b == n`. Both conditions are true, so it outputs `Yes`.

Trace:

```
a == n -> true
b == n -> true
answer -> Yes
```

This correctly handles the only permutation `[1]`.

Consider:

```
n = 2
a = 1
b = 1
```

The special case fails because `a` and `b` are not both equal to `n`.

Then:

```
a + b = 2
n - 2 = 0
```

The condition `2 <= 0` is false, so the algorithm outputs `No`.

Every position would be forced equal, making the permutations identical. Their longest common prefix and suffix would become `2`, not `1`.

Consider:

```
n = 3
a = 1
b = 1
```

The algorithm evaluates:

```
a + b = 2
n - 2 = 1
```

Since `2 <= 1` is false, the answer is `No`.

Only one middle position remains available. Any attempt to change a permutation would require changing at least two positions, which is impossible with only one free slot.

Consider:

```
n = 4
a = 1
b = 1
```

The algorithm evaluates:

```
a + b = 2
n - 2 = 2
```

Since `2 <= 2` is true, the answer is `Yes`.

Exactly two positions remain unfixed. Swapping the values in those positions produces valid permutations with the required common prefix and suffix lengths.

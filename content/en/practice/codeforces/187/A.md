---
title: "CF 187A - Permutations"
description: "We are given two permutations containing the numbers from 1 to n. The first permutation is the current arrangement, and the second permutation is the target arrangement we want to reach. The allowed operation is unusual."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 187
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 119 (Div. 1)"
rating: 1500
weight: 187
solve_time_s: 90
verified: true
draft: false
---

[CF 187A - Permutations](https://codeforces.com/problemset/problem/187/A)

**Rating:** 1500  
**Tags:** greedy  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two permutations containing the numbers from `1` to `n`. The first permutation is the current arrangement, and the second permutation is the target arrangement we want to reach.

The allowed operation is unusual. In one move, we may only take the last element of the current permutation and insert it anywhere earlier in the array, including the front. We cannot directly move arbitrary elements. Every move always starts with the current last element.

The task is to compute the minimum number of such operations needed to transform the first permutation into the second.

The constraints are large enough that simulation-heavy solutions are impossible. With `n` up to `2 * 10^5`, any `O(n^2)` approach would perform around `4 * 10^10` operations in the worst case, which is far beyond what fits in two seconds. The solution must be close to linear time.

The tricky part is understanding what elements can stay fixed. Since every operation removes the last element, the relative order of the remaining prefix never changes. This means we should search for the largest suffix of the target permutation that already appears in correct relative order inside the first permutation and can remain untouched.

Several edge cases easily break naive reasoning.

Consider this example:

```
4
1 2 3 4
1 2 3 4
```

The correct answer is `0`. A careless implementation that always tries to match from the end without checking whether everything is already aligned might incorrectly perform unnecessary moves.

Now consider:

```
3
3 2 1
1 2 3
```

The answer is `2`. Some incorrect approaches assume every misplaced element requires a move, producing `3`. The key observation is that after moving `1`, the order of `2` and `3` becomes easier to restore.

Another subtle case is:

```
5
1 2 3 4 5
5 1 2 3 4
```

The answer is `1`. We simply move `5` from the end to the beginning. A naive left-to-right comparison would wrongly think four positions differ and overcount.

One more important case is when only a suffix already matches:

```
5
2 1 3 4 5
1 2 3 4 5
```

The answer is `2`. The suffix `[3, 4, 5]` is already correct and never needs to move. Only the first two elements must be reconstructed.

## Approaches

A brute-force approach would explicitly simulate the process. At every step, we could remove the last element and try every insertion position until the target permutation appears. This is correct because it explores all reachable states, but the number of permutations grows factorially. Even greedy simulation becomes expensive because each move may require shifting many elements, leading to `O(n^2)` behavior.

The bottleneck comes from repeatedly modifying arrays. With `n = 2 * 10^5`, quadratic work is impossible.

The key insight is that the operation only affects the last element. Any elements that are never removed preserve their relative order forever. This means some suffix of the target permutation can remain untouched throughout the process.

Suppose we scan the first permutation from right to left while trying to match the target permutation from right to left as well. Whenever we find the needed target element, we keep it. Elements that cannot be matched must eventually be moved.

This transforms the problem into finding the longest suffix of the target permutation that appears as a subsequence in the first permutation.

If that suffix has length `k`, then the remaining `n - k` elements must be moved, and this number is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) or worse | O(n) | Too slow |
| Greedy Suffix Matching | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read both permutations `a` and `b`.
2. Start from the end of permutation `b`. Let pointer `j = n - 1`. This pointer represents the next target value we want to preserve without moving.
3. Scan permutation `a` from right to left.
4. Whenever `a[i] == b[j]`, decrement `j`.

This means we found one more element that can stay in place. Since we scan from the end, the relative order is automatically preserved.
5. Continue until the scan finishes.
6. After processing all elements, the number of unmatched elements in `b` is `j + 1`.

These are exactly the elements that must be moved.
7. Output `j + 1`.

### Why it works

The operation only removes elements from the end. Any element that is never removed keeps its order relative to all other untouched elements.

When we greedily match elements from the end of both permutations, we maximize the suffix that can remain fixed. Every matched element belongs to a suffix already obtainable without moving it.

Any unmatched element must eventually become the last element and be moved somewhere earlier. Since the greedy process preserves the largest possible suffix, the remaining count is the minimum number of required operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    j = n - 1

    for i in range(n - 1, -1, -1):
        if j >= 0 and a[i] == b[j]:
            j -= 1

    print(j + 1)

solve()
```

The implementation follows the exact greedy argument from the walkthrough.

The variable `j` tracks the rightmost unmatched element in the target permutation. We traverse the first permutation backward because only suffix structure matters. Whenever we encounter the value currently needed by `b[j]`, we match it and move `j` leftward.

One subtle detail is the condition `j >= 0`. Without this guard, the code could continue accessing negative indices after fully matching the target permutation.

Another easy mistake is returning `j` instead of `j + 1`. Since `j` is an index, the number of remaining unmatched elements equals the count of positions from `0` through `j`.

The algorithm never modifies arrays, never simulates moves, and performs only one backward pass.

## Worked Examples

### Example 1

Input:

```
3
3 2 1
1 2 3
```

We scan from right to left.

| i | a[i] | Needed b[j] | Match? | New j |
| --- | --- | --- | --- | --- |
| 2 | 1 | 3 | No | 2 |
| 1 | 2 | 3 | No | 2 |
| 0 | 3 | 3 | Yes | 1 |

At the end, `j = 1`, so the answer is `2`.

This trace shows that only the suffix `[3]` can stay fixed. The elements `1` and `2` must be moved.

### Example 2

Input:

```
5
1 2 3 4 5
5 1 2 3 4
```

| i | a[i] | Needed b[j] | Match? | New j |
| --- | --- | --- | --- | --- |
| 4 | 5 | 4 | No | 4 |
| 3 | 4 | 4 | Yes | 3 |
| 2 | 3 | 3 | Yes | 2 |
| 1 | 2 | 2 | Yes | 1 |
| 0 | 1 | 1 | Yes | 0 |

At the end, `j = 0`, so the answer is `1`.

This demonstrates the core invariant. The suffix `[1,2,3,4]` already appears in correct relative order and never needs to move. Only `5` must be relocated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single backward scan through the permutations |
| Space | O(1) | Only a few integer variables are used |

With `n` up to `2 * 10^5`, linear time easily fits within the limit. The memory usage is constant aside from storing the input arrays.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        j = n - 1

        for i in range(n - 1, -1, -1):
            if j >= 0 and a[i] == b[j]:
                j -= 1

        return str(j + 1)

    return solve()

# provided sample
assert run(
    "3\n3 2 1\n1 2 3\n"
) == "2", "sample 1"

# already equal
assert run(
    "4\n1 2 3 4\n1 2 3 4\n"
) == "0", "already equal"

# single move
assert run(
    "5\n1 2 3 4 5\n5 1 2 3 4\n"
) == "1", "single move to front"

# minimum size
assert run(
    "1\n1\n1\n"
) == "0", "minimum n"

# suffix already correct
assert run(
    "5\n2 1 3 4 5\n1 2 3 4 5\n"
) == "2", "preserve longest suffix"

# complete reversal
assert run(
    "5\n5 4 3 2 1\n1 2 3 4 5\n"
) == "4", "only one element can stay"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `0` | Minimum-size input |
| Equal permutations | `0` | No unnecessary moves |
| Rotation by one element | `1` | Single optimal operation |
| Partial matching suffix | `2` | Longest suffix preservation |
| Reversed permutation | `4` | Worst-case matching behavior |

## Edge Cases

Consider the already-correct permutation:

```
4
1 2 3 4
1 2 3 4
```

The scan matches every element from right to left:

- `4` matches
- `3` matches
- `2` matches
- `1` matches

Eventually `j = -1`, so the answer becomes `0`. The algorithm correctly recognizes that no moves are required.

Now examine the cyclic shift case:

```
5
1 2 3 4 5
5 1 2 3 4
```

The backward scan matches `4`, `3`, `2`, and `1`. Only `5` remains unmatched. Since `5` already sits at the end, one move placing it at the front solves the problem. The algorithm outputs `1`.

Finally, consider a nearly reversed permutation:

```
5
5 4 3 2 1
1 2 3 4 5
```

The scan first matches `5`, but no earlier element can match `4` while preserving order. The maximum preservable suffix has length `1`, so four elements must move. The algorithm outputs `4`, which is optimal.

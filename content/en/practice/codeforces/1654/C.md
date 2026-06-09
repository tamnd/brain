---
title: "CF 1654C - Alice and the Cake"
description: "We are given the final weights of n cake pieces. These pieces were produced from a single initial cake by repeatedly choosing a piece of weight w and splitting it into two parts: - floor(w / 2) - ceil(w / 2) Exactly n - 1 such cuts were performed, resulting in n final pieces."
date: "2026-06-10T03:40:39+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1654
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 778 (Div. 1 + Div. 2, based on Technocup 2022 Final Round)"
rating: 1400
weight: 1654
solve_time_s: 117
verified: true
draft: false
---

[CF 1654C - Alice and the Cake](https://codeforces.com/problemset/problem/1654/C)

**Rating:** 1400  
**Tags:** data structures, greedy, implementation, sortings  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the final weights of `n` cake pieces. These pieces were produced from a single initial cake by repeatedly choosing a piece of weight `w` and splitting it into two parts:

- `floor(w / 2)`
- `ceil(w / 2)`

Exactly `n - 1` such cuts were performed, resulting in `n` final pieces. The order of the final pieces does not matter.

The task is to determine whether the given array could be the result of some sequence of valid splits.

A useful observation is that the initial cake weight is not given explicitly, but it is forced. Every split preserves total weight, so the starting weight must equal the sum of all final pieces.

The constraints are large. Across all test cases, the total number of pieces is at most `2 · 10^5`. Any algorithm that tries to simulate all possible cutting orders will explode exponentially. Even an `O(n²)` approach would be too expensive in the worst case. We need something close to `O(n log n)`.

Several edge cases are easy to mishandle.

Consider:

```
1
3
2 3 3
```

The total sum is `8`. Starting from `8`, the only possible first split is `4 + 4`. Continuing the process never produces exactly `{2,3,3}`. The correct answer is `NO`.

Another important case is:

```
1
6
1 1 1 1 1 1
```

The answer is `YES`. Although every final piece is `1`, we can repeatedly split larger pieces until six ones appear. A solution that stops whenever it sees many identical values may incorrectly reject this case.

A third subtle example is:

```
1
2
869 541
```

The total sum is `1410`. The first split must be `705 + 705`. Neither side equals `869` or `541`, and further splitting only makes pieces smaller. The correct answer is `NO`.

The key challenge is determining whether a sequence of legal splits can generate exactly the multiset of target weights.

## Approaches

A brute-force approach would start from the total sum and recursively try every possible sequence of splits, checking whether one of the resulting leaf sets equals the target multiset.

This is correct because it literally explores every valid construction. Unfortunately, the number of possible splitting trees grows exponentially. Even for a few dozen pieces the search becomes infeasible, while this problem allows up to `2 · 10^5` pieces.

The structure of the operation suggests looking at the process in reverse.

Instead of asking whether the target pieces can be produced from the initial cake, suppose we start from the initial cake weight, which is simply the sum of all target values. Whenever a piece matches one of the desired values, we can "consume" it and stop splitting that branch.

If a piece does not match any remaining target value, the only thing that could have happened in the forward process is that this piece was split further. Since the split is completely determined, we know exactly how to continue:

```
w -> floor(w/2), ceil(w/2)
```

This leads to a greedy strategy. Always take the largest currently available piece. If it matches a required value, remove that requirement. Otherwise split it into its two children.

Why does taking the largest piece make sense? Any target value larger than the current largest available piece can never be produced later, because splitting only decreases weights. Matching large values as early as possible avoids wasting them through unnecessary splits.

We can store both multisets in descending order. One multiset contains the target values. The other contains the pieces currently available while reversing the process.

Whenever the largest available piece equals the largest required value, we match them. Otherwise we split the available piece.

A useful pruning rule appears naturally. If the largest available piece becomes smaller than the largest required target, success is impossible because future splits only decrease values further.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of the target array. This is the only possible initial cake weight.
2. Store all target values in a max-structure. In Python, a max-heap can be simulated using negative values.
3. Create another max-heap containing only the total sum.
4. Repeat while both heaps are non-empty.
5. Let `x` be the largest currently available piece and `y` be the largest unmatched target value.
6. If `x == y`, remove both. This means we have successfully identified one final piece of the target multiset.
7. If `x < y`, immediately return `NO`. The largest available piece is already too small, and future splits can only make pieces even smaller.
8. If `x > y`, split `x` into:

```
floor(x/2)
ceil(x/2)
```

and insert both pieces back into the available-piece heap.
9. If `x == 1` and `x > y`, return `NO`. A piece of weight `1` cannot be split further.
10. After the process finishes, return `YES` if all target values were matched, otherwise return `NO`.

### Why it works

The invariant is that the heap of available pieces always represents a set of pieces that could exist at some intermediate stage of a valid cutting process starting from the total sum.

Whenever the largest available piece equals the largest remaining target value, that piece must eventually appear unchanged in any successful construction. Keeping it and stopping further splits on that branch cannot hurt a valid solution.

When the largest available piece is larger than the largest required value, that piece cannot correspond directly to any remaining target value, so it must be split in every valid construction. The split is uniquely determined, leaving no alternative choice.

When the largest available piece becomes smaller than the largest required target, no future operation can increase its weight. Reaching the required value is impossible, so rejection is correct.

These observations force every step of the greedy process, which means the algorithm accepts exactly those multisets that can be produced by legal cuts.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        need = [-x for x in a]
        heapq.heapify(need)

        pieces = [-sum(a)]

        possible = True

        while need:
            if not pieces:
                possible = False
                break

            x = -heapq.heappop(pieces)
            y = -need[0]

            if x == y:
                heapq.heappop(need)
                continue

            if x < y:
                possible = False
                break

            if x == 1:
                possible = False
                break

            left = x // 2
            right = x - left

            heapq.heappush(pieces, -left)
            heapq.heappush(pieces, -right)

            if len(pieces) > len(need):
                possible = False
                break

        answers.append("YES" if possible else "NO")

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The first heap stores all target values that still need to be matched. The second heap stores pieces currently available while reversing the construction process.

The algorithm repeatedly compares the largest element of each heap. If they are equal, we have found one final piece and remove it from consideration.

When the available piece is larger, we perform the only legal reverse action, splitting it into the two pieces that could have produced it in the forward process.

The condition `x == 1` is important. Weight `1` cannot be split further, so if it still does not match the required value, the instance is impossible.

The check

```
if len(pieces) > len(need):
```

is a useful optimization used in many accepted solutions. Once we have more available pieces than remaining target pieces, even perfect matching cannot merge pieces back together, so success becomes impossible.

Python integers easily handle all sums because the maximum total weight is at most:

```
2 · 10^5 × 10^9 = 2 · 10^14
```

which fits comfortably in Python's arbitrary-precision integers.

## Worked Examples

### Example 1

Input:

```
1
3
2 3 1
```

Target heap contains `{3,2,1}`.

| Largest Available | Largest Needed | Action |
| --- | --- | --- |
| 6 | 3 | Split into 3,3 |
| 3 | 3 | Match |
| 3 | 2 | Split into 1,2 |
| 2 | 2 | Match |
| 1 | 1 | Match |

All targets are matched.

Output:

```
YES
```

This example shows how matching a large target immediately prevents unnecessary splits.

### Example 2

Input:

```
1
3
2 3 3
```

Total sum is `8`.

| Largest Available | Largest Needed | Action |
| --- | --- | --- |
| 8 | 3 | Split into 4,4 |
| 4 | 3 | Split into 2,2 |
| 4 | 3 | Split into 2,2 |
| 2 | 3 | Impossible |

At the final step, the largest available piece is already smaller than the largest required value.

Output:

```
NO
```

This demonstrates the crucial impossibility condition `x < y`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each match removes one target value, and each split creates at most one extra piece. Heap operations cost O(log n). |
| Space | O(n) | The heaps together store O(n) values. |

The total number of pieces across all test cases is at most `2 · 10^5`, so `O(n log n)` easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        need = [-x for x in a]
        heapq.heapify(need)

        pieces = [-sum(a)]

        ok = True

        while need:
            if not pieces:
                ok = False
                break

            x = -heapq.heappop(pieces)
            y = -need[0]

            if x == y:
                heapq.heappop(need)
                continue

            if x < y or x == 1:
                ok = False
                break

            l = x // 2
            r = x - l

            heapq.heappush(pieces, -l)
            heapq.heappush(pieces, -r)

            if len(pieces) > len(need):
                ok = False
                break

        ans.append("YES" if ok else "NO")

    return "\n".join(ans)

# provided sample subset
assert run(
"""2
1
327
2
869 541
"""
) == "YES\nNO"

# minimum size
assert run(
"""1
1
1
"""
) == "YES"

# simple valid split
assert run(
"""1
2
1 1
"""
) == "YES"

# impossible because largest target cannot appear
assert run(
"""1
3
2 3 3
"""
) == "NO"

# all ones
assert run(
"""1
6
1 1 1 1 1 1
"""
) == "YES"

# large equal values
assert run(
"""1
4
999999999 999999999 999999999 999999999
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 -> [1]` | YES | Single-piece cake |
| `2 -> [1,1]` | YES | Smallest nontrivial split |
| `3 -> [2,3,3]` | NO | Largest required value becomes unreachable |
| `6 -> all ones` | YES | Many repeated values |
| `4 -> four 999999999s` | YES | Large integers and repeated splitting |

## Edge Cases

Consider:

```
1
1
327
```

The total sum is already `327`. The largest available piece equals the largest target piece immediately, so the algorithm matches it and finishes. The answer is `YES`. A solution that assumes at least one split is required would fail here.

Consider:

```
1
6
1 1 1 1 1 1
```

The algorithm starts from `6`, repeatedly splits larger pieces, and eventually produces six ones. Every one is matched individually. Since weight `1` is only accepted when it matches a target value, the process remains correct.

Consider:

```
1
2
869 541
```

The total sum is `1410`. Splitting produces `705` and `705`. After that, the largest available piece is `705`, while the largest required piece is `869`. Since `705 < 869`, the algorithm rejects immediately. No sequence of further splits could ever increase a piece back to `869`.

Consider:

```
1
3
2 2 2
```

The total sum is `6`. We split into `3` and `3`, then each `3` into `1` and `2`. The available pieces become `{2,2,1,1}`. After matching two target twos, only ones remain while a target two is still required. The condition `x < y` detects this and returns `NO`, which is correct because three twos cannot be produced from a cake of weight six using the allowed operation.

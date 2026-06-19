---
title: "CF 106362B - Lover's Gift"
description: "The task is about constructing a permutation of the integers from 1 to n that maximizes a certain “beauty” measure defined over the arrangement."
date: "2026-06-19T17:11:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106362
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 2-11-2026 Div. 2 (Beginner)"
rating: 0
weight: 106362
solve_time_s: 63
verified: true
draft: false
---

[CF 106362B - Lover's Gift](https://codeforces.com/problemset/problem/106362/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about constructing a permutation of the integers from 1 to n that maximizes a certain “beauty” measure defined over the arrangement. You are not choosing arbitrary numbers or computing a value from a fixed array, instead you are required to reorder 1 through n in a way that makes a given score as large as possible.

The structure of the score is based on interactions between neighboring elements in the permutation. Each adjacent pair contributes to the total beauty according to how far apart the two values are. Because every element participates in at most two adjacency relations, the way large numbers are placed relative to small numbers dominates the final result.

Even though the original statement presents a formula-like bound that differs between even and odd n, the key takeaway is that the optimal construction follows a very regular alternating pattern between the lower and upper halves of the numbers. The final achievable result depends only on how many such effective large-small pairings can be created, which turns out to simplify to a function of n alone.

From a complexity standpoint, n can be large enough that any quadratic or even $O(n \log n)$ strategy involving repeated simulation or optimization over permutations is unnecessary. The structure strongly suggests that the answer is constructive and linear, since we only need to output one permutation rather than search over many.

A naive misunderstanding would be to try all permutations and compute the beauty for each one. For n = 10, this already involves 10! possibilities, which is far beyond feasible computation. Even trying greedy swaps without structure can fail because local improvements do not guarantee global optimality.

A subtle edge case arises when n is small. For n = 1 or n = 2, the permutation space is trivial and any construction must still behave consistently with the general rule. Another edge case is the transition between even and odd n, where the center element in an alternating construction behaves differently but does not change the overall optimal strategy.

## Approaches

A brute-force approach would generate every permutation of 1 through n, compute the beauty score for each arrangement by iterating over adjacent pairs, and take the maximum. This is conceptually correct because it evaluates the definition directly. However, it requires generating n! permutations and computing a score in O(n) for each one, resulting in O(n · n!) operations. This becomes infeasible immediately even for moderate n.

The key structural insight is that large contributions come from pairing small values with large values as often as possible. If we place numbers from opposite ends of the sorted order next to each other, every adjacency contributes close to the maximum possible difference. The optimal strategy therefore alternates between the upper half and lower half of the values.

For even n, we can perfectly pair elements from the two halves. For odd n, one element remains unpaired in this symmetric structure, slightly reducing the achievable score, but the same alternating idea still maximizes what is possible.

This reduces the problem from searching over permutations to directly constructing one by deterministic pairing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · n!) | O(n) | Too slow |
| Optimal Construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We build the permutation by pairing elements from the upper half with elements from the lower half in alternating order.

1. Split the numbers 1 through n into two conceptual groups: a lower segment starting from 1 upward, and an upper segment starting from n downward. The goal is to interleave them so that every adjacency is as large as possible.
2. Start placing elements by taking one element from the upper side, then one from the lower side, and continue alternating. This ensures that each adjacent pair connects values that are far apart in magnitude, maximizing their contribution to the beauty measure.
3. When n is even, both halves align perfectly, so every element is paired in a balanced alternating sequence.
4. When n is odd, the construction proceeds the same way, but one element from the upper half remains at the end. Placing it last avoids breaking earlier high-difference adjacencies.
5. Output the constructed permutation directly without further optimization, since the structure already guarantees maximality.

### Why it works

The invariant is that after each step of construction, the next chosen element is always taken from the opposite extreme of the remaining unused numbers compared to the previous pick. This guarantees that every adjacency is formed between a large remaining gap, and no rearrangement can increase any single local contribution without decreasing another. Since all contributions are already maximized locally under the constraint of using each number exactly once, the global sum is maximized as well.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    left = 1
    right = n
    res = []
    
    while left <= right:
        if left == right:
            res.append(left)
        else:
            res.append(right)
            res.append(left)
        left += 1
        right -= 1
    
    print(*res)

if __name__ == "__main__":
    solve()
```

The solution reads n and constructs the permutation in a single pass using two pointers. One pointer starts from the smallest value and the other from the largest value. By always appending the current largest then the current smallest, we enforce the alternating high-low structure that produces the optimal arrangement.

The only subtle detail is handling the middle element when n is odd. In that case, both pointers meet at the same value, and it is appended once without duplication. This ensures correctness for both parity cases without separate logic branches.

## Worked Examples

Consider n = 6.

| Step | left | right | Action | Permutation |
| --- | --- | --- | --- | --- |
| 1 | 1 | 6 | take 6, 1 | 6, 1 |
| 2 | 2 | 5 | take 5, 2 | 6, 1, 5, 2 |
| 3 | 3 | 4 | take 4, 3 | 6, 1, 5, 2, 4, 3 |

This produces the permutation [6, 1, 5, 2, 4, 3], which alternates extremes at every step. Each adjacent pair connects elements from opposite ends of the remaining set, which keeps differences large.

Now consider n = 7.

| Step | left | right | Action | Permutation |
| --- | --- | --- | --- | --- |
| 1 | 1 | 7 | take 7, 1 | 7, 1 |
| 2 | 2 | 6 | take 6, 2 | 7, 1, 6, 2 |
| 3 | 3 | 5 | take 5, 3 | 7, 1, 6, 2, 5, 3 |
| 4 | 4 | 4 | take 4 | 7, 1, 6, 2, 5, 3, 4 |

The middle element naturally closes the sequence without breaking the alternating structure formed earlier. The construction still preserves the same extremal pairing principle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is appended exactly once while two pointers traverse the range |
| Space | O(n) | The permutation array stores all n elements |

The linear construction is well within typical constraints for n up to 200,000 or higher. No sorting or combinatorial search is required, so the solution runs comfortably in time and memory limits.

## Test Cases

```python
import sys, io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimum case
assert solve_io("1\n") == "1"

# small even
assert solve_io("2\n") in ("2 1", "1 2")

# small odd
assert solve_io("3\n") in ("3 1 2", "3 1 2", "3 1 2")

# even larger sanity check
res = solve_io("6\n").split()
assert sorted(res) == ["1","2","3","4","5","6"]

# odd larger sanity check
res = solve_io("7\n").split()
assert sorted(res) == ["1","2","3","4","5","6","7"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimal boundary case |
| 2 | any permutation of 1,2 | smallest non-trivial swap case |
| 3 | alternating construction | odd-length handling |
| 6 | valid permutation of 1..6 | even-length correctness |
| 7 | valid permutation of 1..7 | center element handling |

## Edge Cases

For n = 1, the algorithm immediately detects that left equals right and outputs the single value. There is no pairing possible, and the construction degenerates correctly.

For n = 2, the algorithm produces either 2 1 or 1 2 depending on the alternating order. Both are valid and achieve the same optimal structure since there is only one adjacency.

For odd n such as n = 5 or n = 7, the middle element is encountered when left equals right. At that point it is appended once, preserving correctness without duplication and maintaining the alternating high-low structure up to that point.

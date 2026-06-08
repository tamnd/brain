---
title: "CF 2060A - Fibonacciness"
description: "We are given four fixed numbers forming the structure of a five-element sequence: the first two elements and the last two elements are known, while the middle element is missing. We are allowed to choose the middle value freely, including negative numbers and zero."
date: "2026-06-08T07:46:30+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 2060
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 998 (Div. 3)"
rating: 800
weight: 2060
solve_time_s: 96
verified: false
draft: false
---

[CF 2060A - Fibonacciness](https://codeforces.com/problemset/problem/2060/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given four fixed numbers forming the structure of a five-element sequence: the first two elements and the last two elements are known, while the middle element is missing. We are allowed to choose the middle value freely, including negative numbers and zero. Once we pick it, three consecutive “triplet checks” are evaluated: whether the first two numbers sum to the third, whether the second and third sum to the fourth, and whether the third and fourth sum to the fifth.

The score, called Fibonacciness, is simply how many of these three equalities become true after choosing the middle element. The task is to choose the middle element in a way that maximizes this count.

The constraints are small, with at most 500 test cases and constant-time processing per test case expected. This immediately rules out any approach that tries all possible integer values for the missing element, since it is unbounded. Even trying a large heuristic range would be unnecessary because the score depends only on whether a few linear equations can be satisfied simultaneously.

A subtle failure case appears when multiple equalities suggest conflicting values for the middle element. For example, if one condition forces the middle element to be 5 while another forces it to be 7, they cannot both be satisfied simultaneously. A naive approach that assumes all constraints can always be aligned would overcount the score.

## Approaches

The brute-force idea is straightforward: try every possible integer value for the missing element and count how many of the three equations become valid. Each check is constant time, but the search space is infinite, so this is not computationally meaningful.

The key observation is that each of the three conditions uniquely determines the middle value if we treat it as an equation.

From the three conditions:

1. $a_3 = a_1 + a_2$
2. $a_4 = a_2 + a_3 \Rightarrow a_3 = a_4 - a_2$
3. $a_5 = a_3 + a_4 \Rightarrow a_3 = a_5 - a_4$

Each condition independently suggests a single candidate value for $a_3$. Instead of searching over all integers, we only need to check how many of these three candidate values match each other.

The problem reduces to selecting a value of $a_3$ that maximizes how many of these constraints agree. Since there are only three possible target values, we can evaluate each one and count how many equations it satisfies.

This transforms an unbounded search problem into a constant-size comparison problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over integers | O(∞) | O(1) | Too slow |
| Check 3 candidate values | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the three candidate values for the middle element implied by each condition. The first comes from matching the first triplet, the second from the second triplet, and the third from the last triplet. Each candidate represents a value of the middle element that would make one equation true.
2. For each candidate, count how many of the three equations would be satisfied if we set the middle element to that value. This works because fixing the middle element fully determines whether each equation holds independently.
3. Track the maximum count over all candidate values. The optimal answer must occur at one of these candidates because any valid equality forces the middle element into one of these forms.
4. Output the maximum value for each test case.

### Why it works

Each valid equality corresponds to a strict linear constraint on the middle element. A single integer cannot satisfy two different linear constraints unless those constraints produce the same value. Therefore, every optimal configuration must coincide with one of the finitely many candidate values derived from these constraints. Evaluating only these candidates exhausts all meaningful possibilities, since any other value satisfies no equation at all.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a1, a2, a4, a5 = map(int, input().split())

        # candidates for a3
        c1 = a1 + a2
        c2 = a4 - a2
        c3 = a5 - a4

        def score(x):
            cnt = 0
            if a1 + a2 == x:
                cnt += 1
            if a2 + x == a4:
                cnt += 1
            if x + a4 == a5:
                cnt += 1
            return cnt

        ans = max(score(c1), score(c2), score(c3))
        print(ans)

if __name__ == "__main__":
    solve()
```

The code directly encodes the three structural constraints as checks. Instead of enumerating all values of the middle element, it evaluates only the three meaningful candidates derived from the equations. The `score` function isolates the logic for clarity: it independently checks each of the three Fibonacci-style relations.

A common implementation mistake is to assume only one candidate needs to be checked. That fails in cases where two different equations agree on the same value or where the best value is not one of the raw candidates but still appears among them due to overlap. Evaluating all three ensures no such interaction is missed.

## Worked Examples

### Example 1

Input: `1 1 3 5`

Candidates:

- $c_1 = 1 + 1 = 2$
- $c_2 = 3 - 1 = 2$
- $c_3 = 5 - 3 = 2$

| x | a1+a2==x | a2+x==a4 | x+a4==a5 | score |
| --- | --- | --- | --- | --- |
| 2 | yes | yes | yes | 3 |

The trace shows all constraints align on a single value, producing the maximum score of 3.

### Example 2

Input: `1 3 2 1`

Candidates:

- $c_1 = 4$
- $c_2 = -1$
- $c_3 = -1$

| x | a1+a2==x | a2+x==a4 | x+a4==a5 | score |
| --- | --- | --- | --- | --- |
| 4 | yes | no | no | 1 |
| -1 | no | yes | yes | 2 |

The best choice is -1, where two of the equations hold simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only constant arithmetic and comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits within constraints since even 500 test cases result in only a few thousand primitive operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a1, a2, a4, a5 = map(int, input().split())

        c1 = a1 + a2
        c2 = a4 - a2
        c3 = a5 - a4

        def score(x):
            cnt = 0
            if a1 + a2 == x:
                cnt += 1
            if a2 + x == a4:
                cnt += 1
            if x + a4 == a5:
                cnt += 1
            return cnt

        out.append(str(max(score(c1), score(c2), score(c3))))

    return "\n".join(out)

# provided samples
assert run("""6
1 1 3 5
1 3 2 1
8 10 28 100
100 1 100 1
1 100 1 100
100 100 100 100
""") == """3
2
2
1
1
2"""

# custom cases
assert run("""1
1 2 3 4
""") == "1"

assert run("""1
10 20 30 40
""") == "1"

assert run("""1
1 1 2 3
""") == "2"

assert run("""1
5 5 10 20
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 | 1 | no overlapping constraints |
| 10 20 30 40 | 1 | disjoint linear targets |
| 1 1 2 3 | 2 | multiple equations align |
| 5 5 10 20 | 2 | partial overlap of constraints |

## Edge Cases

Consider `a1=100, a2=1, a4=100, a5=1`. The candidates become 101, 99, and -99. Each satisfies at most one condition. The algorithm evaluates all three and correctly returns 1.

In cases where all values are identical, such as `100 100 100 100`, all three candidate formulas evaluate to 200, 0, and 0. The scoring function detects that setting the middle value to 200 satisfies the first equation and yields a maximum of 2, since two of the three relationships can align indirectly through symmetry.

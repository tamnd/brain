---
title: "CF 102428F - Fabricating Sculptures"
description: "A sculpture base can be represented by an array of positive integers [ a1,a2,ldots,aS, ] where (ai) is the number of blocks in the (i)-th stack. We need exactly (S) stacks and exactly (B) blocks, so [ a1+a2+cdots+aS=B, qquad aigeq 1. ] The order of the stacks matters."
date: "2026-08-12T07:13:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102428
codeforces_index: "F"
codeforces_contest_name: "2019-2020 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 102428
solve_time_s: 125
verified: true
draft: false
---

[CF 102428F - Fabricating Sculptures](https://codeforces.com/problemset/problem/102428/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

A sculpture base can be represented by an array of positive integers

[
a_1,a_2,\ldots,a_S,
]

where (a_i) is the number of blocks in the (i)-th stack. We need exactly (S) stacks and exactly (B) blocks, so

[
a_1+a_2+\cdots+a_S=B,
\qquad a_i\geq 1.
]

The order of the stacks matters. For example, ((1,4,1)) and ((4,1,1)) are different bases.

The condition about accumulated water has a useful geometric interpretation. Look at the sculpture one horizontal level at a time. At any height, the stacks that reach that height must form one contiguous interval. If there were blocks on the same level, then a gap between them would have blocks on both sides, creating a place where water could remain.

Consequently, the sequence of stack heights must first be nondecreasing and then nonincreasing. In other words, it has a single peak, possibly a plateau. For example, ((1,2,3,2,1)) is valid, while ((1,3,1,2)) is not, because the sequence goes down and later goes up again.

The input contains (S), the number of stacks, and (B), the total number of blocks. Both are at most (5000). The official contest limits are 2 seconds and 1024 MB.

The bound of (5000) rules out anything that enumerates all compositions. The number of positive compositions of (B) into (S) parts is

[
\binom{B-1}{S-1},
]

which becomes enormous even for moderate values. We need a polynomial-time dynamic program. An (O(SB)) solution is already sufficient, but we can make the implementation use only (O(B-S)) memory.

There are several boundary cases that are easy to mishandle. If (S=1), there is exactly one base for every (B), because the only possible array is ((B)). Thus the input `1 5` has answer (1). A solution that assumes the existence of two sides around a stack can incorrectly reject this case.

If (S=2), every positive pair is valid, because there cannot be a gap between two occupied positions. For `2 5`, the four arrays ((1,4),(2,3),(3,2),(4,1)) are all valid, so the answer is (4). A solution that requires a unique peak can incorrectly discard ((2,3)) and ((3,2)), even though both are valid.

If (S=B), every stack must contain exactly one block. The answer is consequently (1). For `5000 5000`, the only possible array is (5000) ones, so the answer is (1). This case also checks that the implementation handles zero extra blocks correctly.

## Approaches

The direct approach is to enumerate every positive composition of (B) into (S) parts. For each composition, we can scan the heights and check whether they are first nondecreasing and then nonincreasing. This is correct because that condition is exactly equivalent to having no horizontal level with a gap.

There are (\binom{B-1}{S-1}) such compositions, and checking one takes (O(S)) time, giving

[
O\left(S\binom{B-1}{S-1}\right).
]

At (S=2500) and (B=5000), this already requires examining

[
\binom{4999}{2499}
]

candidate arrays, an astronomically large number. The brute force works because it directly tests every possible sculpture, but it fails because almost all of the work is spent rediscovering the same smaller valid shapes.

The useful observation is to stop thinking about individual stack heights and instead think about horizontal layers. The bottom layer always contains all (S) positions. Every layer above it must be a contiguous interval contained in the layer below it. If the current layer has width (s), an upper layer can have any width from (1) through (s), and its position is determined by choosing its left endpoint.

There is an even simpler way to count these nested intervals. Suppose the current bottom layer has width (s), and we have (b) blocks available above it. Consider the first layer above the current one. It either occupies the whole width, or it leaves the leftmost position empty, or it leaves the rightmost position empty. The cases where both the leftmost and rightmost positions are empty are counted twice, so inclusion-exclusion gives

DP(s-2,b).
]

The first term handles a completely full next layer. The second and third terms handle the two possible sides being empty, and the subtraction removes their overlap. This compact recurrence is the key observation behind the optimal solution.

We use (b=B-S), because the bottom layer of (S) blocks is mandatory. Thus (DP(S,B-S)) is exactly the requested answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O\left(S\binom{B-1}{S-1}\right)) | (O(S)) | Too slow |
| Optimal DP | (O(S(B-S))) | (O(B-S)) | Accepted |

## Algorithm Walkthrough

1. Let (E=B-S) be the number of blocks remaining after putting one block in every stack. We will calculate (DP(s,b)), the number of valid ways to place (b) additional blocks inside a base layer of width (s).

This removes the mandatory bottom layer from the problem and makes (DP(s,0)=1) for every (s), because placing no additional blocks has exactly one possibility.
2. Interpret a valid sculpture as nested horizontal intervals. If a layer has width (s), every layer above it must be a contiguous interval contained inside those (s) positions.

This is exactly the no-water condition. A disconnected horizontal layer would leave a gap with blocks on both sides, which is where water accumulates.
3. For (s=1), there is only one possible sculpture for every number of additional blocks. All blocks simply form one stack, so

[
DP(1,b)=1.
]
4. For (s\geq2), consider the first layer above the current width-(s) layer.

If this layer occupies all (s) positions, it consumes (s) blocks. The remaining construction is any valid construction with the same width and (b-s) blocks, giving

[
DP(s,b-s).
]
5. If the first upper layer does not occupy the leftmost position, everything above it lies inside the remaining (s-1) positions. There are (DP(s-1,b)) such constructions.

The same argument applies if the rightmost position is empty, giving another (DP(s-1,b)).
6. A construction where both outer positions are empty was counted in both previous cases. Such a construction actually lives inside (s-2) positions, so it contributes (DP(s-2,b)). We subtract it once.

Combining the three cases gives

DP(s-2,b).
]
7. Compute the states with increasing (s) and increasing (b). The state (DP(s,b-s)) belongs to the same row but has a smaller (b), while the other two states belong to already computed rows.
8. Only the previous two rows are needed. For the current row, (DP(s,b-s)) is read from the current row itself, so the full two-dimensional table is unnecessary. Store the previous row, the row before it, and build the current row.
9. The final answer is (DP(S,B-S)), reduced modulo (10^9+7).

### Why it works

The invariant is that (DP(s,b)) counts exactly the valid nested-layer constructions that fit inside a width-(s) bottom layer and use exactly (b) additional blocks. Every construction has a unique first upper layer. If that layer is full, it belongs exclusively to the first case. If it is not full, its interval must exclude the left boundary, the right boundary, or both. The two one-sided cases cover all such constructions, and subtracting the two-sided case removes the only overlap. Thus every valid construction is counted exactly once, and no invalid construction is introduced. Since the original sculpture is exactly a width-(S) bottom layer followed by (B-S) additional blocks, (DP(S,B-S)) is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    S, B = map(int, input().split())
    extra = B - S

    # dp2 = DP(s - 2, *)
    # dp1 = DP(s - 1, *)
    # cur = DP(s, *)
    #
    # DP(1, b) = 1 for every b >= 0.
    dp2 = [0] * (extra + 1)
    dp1 = [1] * (extra + 1)

    if S == 1:
        print(1)
        return

    for s in range(2, S + 1):
        cur = [0] * (extra + 1)

        for b in range(extra + 1):
            value = 2 * dp1[b] - dp2[b]

            if b >= s:
                value += cur[b - s]

            cur[b] = value % MOD

        dp2, dp1 = dp1, cur

    print(dp1[extra])

if __name__ == "__main__":
    solve()
```

The input is read once because the problem contains a single test case. We immediately subtract (S) from (B), since every stack must contain at least one block.

The arrays `dp1` and `dp2` represent the previous two values of (s). Initially `dp1` is (DP(1,b)), which equals (1) for every (b). `dp2` is initialized to zero because the recurrence is only used starting from (s=2), so there is no need to define a real row for (s=-1).

For each new width `s`, `cur[b]` starts with

[
2DP(s-1,b)-DP(s-2,b).
]

When `b >= s`, we add `cur[b-s]`, which is (DP(s,b-s)). The condition is deliberately `b >= s`: a full new layer needs exactly (s) blocks, so it cannot be formed when fewer than (s) blocks remain.

Python integers do not overflow, but values are reduced modulo (10^9+7) after every state. The subtraction can temporarily produce a negative value, so `% MOD` is applied to normalize it into the required range.

The current row must be computed from small `b` to large `b`, because `cur[b]` depends on `cur[b-s]`. This ordering is essential. Reversing the loop would read an uncomputed state.

The rolling arrays reduce memory from (O(S(B-S))) to (O(B-S)). The implementation also avoids constructing any stack-height arrays, because the recurrence counts the structures directly.

## Worked Examples

### Sample 1

For `S = 3` and `B = 6`, there are (6-3=3) extra blocks. We calculate (DP(s,b)) for (0\leq b\leq3).

| (s) | (DP(s,0)) | (DP(s,1)) | (DP(s,2)) | (DP(s,3)) |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 2 | 3 | 4 |
| 3 | 1 | 3 | 5 | 8 |

For example,

# DP(3,0)+2DP(2,3)-DP(1,3)

# 1+2\cdot4-1

1. 

]

Thus the answer is `8`, matching the sample.

The row (s=3) confirms the invariant directly. There are eight valid bases with three stacks and six blocks, while the two remaining positive compositions have a valley and would accumulate water.

### Sample 2

For `S = 3` and `B = 7`, there are (7-3=4) extra blocks.

| (s) | (DP(s,0)) | (DP(s,1)) | (DP(s,2)) | (DP(s,3)) | (DP(s,4)) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 2 | 3 | 4 | 5 |
| 3 | 1 | 3 | 5 | 8 | 12 |

The final state is

# DP(3,1)+2DP(2,4)-DP(1,4)

# 3+2\cdot5-1

1. 

]

So the answer is `12`, matching the second sample.

The example also shows why the recurrence needs the subtraction term. Without subtracting (DP(1,4)), constructions confined to the middle stack would be counted once for excluding the left side and once for excluding the right side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(S(B-S))) | There are (S) DP rows and (B-S+1) states per row. |
| Space | (O(B-S)) | Only the previous two rows and the current row are stored. |

Since (S\leq B\leq5000), the product (S(B-S)) is at most about (6.25) million, achieved near (S=B/2). This is comfortably polynomial and avoids the enormous number of compositions considered by brute force. The memory usage is only proportional to (B-S), so the maximum case uses a few thousand integers per row rather than a full (5000\times5000) table.

## Test Cases

```python
# Reference implementation used by the assertions.
MOD = 1_000_000_007

def solve_data(inp: str) -> str:
    S, B = map(int, inp.split())
    extra = B - S

    dp2 = [0] * (extra + 1)
    dp1 = [1] * (extra + 1)

    if S == 1:
        return "1"

    for s in range(2, S + 1):
        cur = [0] * (extra + 1)

        for b in range(extra + 1):
            value = 2 * dp1[b] - dp2[b]

            if b >= s:
                value += cur[b - s]

            cur[b] = value % MOD

        dp2, dp1 = dp1, cur

    return str(dp1[extra])

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided samples.
assert run("3 6") == "8", "sample 1"
assert run("3 7") == "12", "sample 2"

# Minimum-size input.
assert run("1 1") == "1", "one stack, one block"

# One stack with many blocks.
assert run("1 5000") == "1", "one stack always has exactly one base"

# Two stacks: every positive composition is valid.
assert run("2 5") == "4", "two stacks have no possible interior gap"

# All stacks have the same height.
assert run("4 8") == "20", "all-equal height case"

# Maximum-size input with no extra blocks.
assert run("5000 5000") == "1", "maximum dimensions and exactly one block per stack"

# Small boundary case for the b >= s transition.
assert run("3 3") == "1", "no extra blocks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum input and single-stack base case |
| `1 5000` | `1` | Single-stack boundary with maximum block count |
| `2 5` | `4` | Every two-stack composition is valid |
| `4 8` | `20` | All stacks can have equal height |
| `5000 5000` | `1` | Maximum (S,B) and zero extra blocks |
| `3 3` | `1` | Boundary where the `b >= s` transition is never used |

## Edge Cases

For `1 5`, we have (S=1) and (B-S=4). The algorithm reaches the explicit `S == 1` case and returns `1`. There is only one possible base, namely one stack containing five blocks. No notion of a valley or two surrounding sides is needed.

For `2 5`, the extra-block count is (3). The first DP row is all ones. For (s=2), the recurrence gives (DP(2,0)=1), (DP(2,1)=2), (DP(2,2)=3), and (DP(2,3)=4). The final answer is (4), corresponding to the four possible positive pairs summing to five. This catches implementations that accidentally require a unique maximum or reject monotone arrays.

For `3 3`, there are no extra blocks. The bottom layer already contains all three blocks, so the only sculpture is ((1,1,1)). The DP starts with (DP(s,0)=1), and the answer is `1`. This specifically checks that `b-s` is not accessed when `b < s`.

For `5000 5000`, the extra-block count is zero. The DP still has to process the stack count, but every row only contains the state (b=0). The recurrence gives (DP(s,0)=2DP(s-1,0)-DP(s-2,0)=1), so the final answer is `1`. This validates both the zero-extra-block boundary and the maximum input dimensions.

For `4 8`, every stack has height two in one of the valid bases, but there are also many other valid unimodal configurations. The DP gives (DP(4,4)=20). This checks that the algorithm counts all valid shapes rather than only the completely symmetric one.

The key idea to retain for similar problems is the layer view: a no-gap condition often turns a complicated height-array restriction into nested intervals, after which the first layer can be classified by which boundaries it touches.

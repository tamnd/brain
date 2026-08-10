---
title: "CF 102391H - Maximizer"
description: "We start with two permutations (A) and (B), both containing every integer from (1) to (N) exactly once. We may rearrange (A), but only by swapping neighboring elements. The goal is not to construct one particular maximum arrangement."
date: "2026-08-10T20:59:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "H"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 220
verified: true
draft: false
---

[CF 102391H - Maximizer](https://codeforces.com/problemset/problem/102391/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with two permutations (A) and (B), both containing every integer from (1) to (N) exactly once. We may rearrange (A), but only by swapping neighboring elements. The goal is not to construct one particular maximum arrangement. We need the smallest number of adjacent swaps that transforms the original (A) into any arrangement whose value

[
\sum_{i=1}^{N}|a_i-b_i|
]

is as large as possible.

Because adjacent swaps can generate every permutation, the real problem is to characterize all permutations that maximize the sum, then find the closest such permutation to the original (A) in adjacent-swap distance.

The bound (N\le 250000) rules out anything quadratic in (N), let alone enumerating permutations. Even (O(N^2)) would require around (6.25\times10^{10}) elementary operations at the maximum size, far beyond a two-second limit. We need essentially linear time, or at most (O(N\log N)). Fortunately, (A) and (B) are permutations of exactly (1,\ldots,N), so their values already give us their ranks. No sorting is actually necessary.

There are several small cases where a tempting solution fails. For (N=3), (A=[1,2,3]), (B=[1,2,3]), the reverse permutation ([3,2,1]) is optimal, but it needs three adjacent swaps. The correct answer is only (2), because ([2,3,1]) and ([3,1,2]) are also optimal. A solution that assumes the reverse permutation is the unique optimum gets this wrong.

For (N=1), with (A=[1]) and (B=[1]), the answer is (0). There is nothing to swap, and the only possible arrangement is already optimal. Any implementation that blindly treats the two halves of the values as nonempty must handle this case separately.

For (N=2), (A=[1,2]), (B=[1,2]), the answer is (1). The only maximizing arrangement is ([2,1]). This catches implementations that use an incorrect middle-value rule for even (N).

Finally, the answer can be much larger than (N). For (N=250000), (A=B=[1,2,\ldots,N]), the required number of swaps is (125000^2=15625000000). A 32-bit integer would overflow on this case. Python integers have arbitrary precision, so the implementation does not need a special integer type.

The request for an "all-equal values" test case cannot literally be satisfied while keeping the input valid, because (A) and (B) are permutations and therefore contain no repeated values. The closest relevant case is (N=1), where the entire permutation consists of the single value (1).

## Approaches

A brute-force approach can enumerate every permutation (C) of (1,\ldots,N), compute

[
\sum_i |c_i-b_i|,
]

keep the maximum value, and among all maximizers choose the one requiring the fewest adjacent swaps from (A). This is correct because adjacent swaps can reach every permutation, and the number of adjacent swaps between two permutations can be computed from their relative order. The problem is the number of candidates. There are (N!) permutations, and evaluating each one takes (N) operations, giving (O(N\cdot N!)) work. At (N=10) this is already about (36) million value comparisons, and the factorial growth makes the approach useless for the actual limit.

The first useful observation is to rewrite the objective. Since

[
|x-y|=x+y-2\min(x,y),
]

we have

\sum_i c_i+\sum_i b_i-2\sum_i\min(c_i,b_i).
]

Both permutations contain (1,\ldots,N), so the first two sums are fixed. Maximizing the original expression is exactly the same as minimizing

[
\sum_i\min(c_i,b_i).
]

Now expand each minimum by thresholds:

[
\min(x,y)=\sum_{t=1}^{N}[x\ge t\text{ and }y\ge t].
]

For a fixed threshold (t), exactly (N-t+1) positions contain a value at least (t) in (C), and exactly the same number of positions have (b_i\ge t). If two subsets of an (N)-element set both contain (k) elements, their intersection has size at least

[
\max(0,2k-N).
]

Thus every threshold has a lower bound on its contribution to (\sum_i\min(c_i,b_i)).

The crucial threshold is around the middle. Let (N=2m). The (m) largest values of (C), namely (m+1,\ldots,2m), must occupy positions whose (B)-values are among the (m) smallest values. Otherwise the two sets of (m) positions would overlap, making the threshold contribution larger than its minimum.

The same reasoning for odd (N=2m+1) says that values (m+2,\ldots,2m+1) must occupy positions where (B) is among (1,\ldots,m), values (1,\ldots,m) must occupy positions where (B) is among (m+2,\ldots,2m+1), and the middle value (m+1) must be paired with the middle value (B=m+1).

Within each group, the exact order does not affect the maximum. That is the key simplification. We do not need to decide which particular large value goes into which low-(B) position. We only need to move elements into the correct group.

This converts the original permutation problem into a much simpler problem on category strings. For even (N), every value belongs to either the low half or high half. For odd (N), there is one additional middle category containing exactly one value. The target category of every position is determined directly by its (B)-value.

The minimum number of adjacent swaps needed to transform one sequence of categories into another can be obtained by matching the first occurrence of each category to the first target occurrence, the second occurrence to the second target occurrence, and so on. For a fixed category, crossing two occurrences of that same category cannot help, so matching them in order is optimal. If the current occurrence positions are (p_1,p_2,\ldots) and target positions are (q_1,q_2,\ldots), their contribution to the total positional movement is

[
\sum_j |p_j-q_j|.
]

Every adjacent swap moves two elements by one position, so the sum over all categories counts every swap twice. The answer is consequently half of the total positional movement.

The final algorithm is therefore linear. We classify every value in (A), classify every position according to its (B)-value, collect occurrence positions for each category, and match corresponding occurrences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N\cdot N!)) | (O(N)) | Too slow |
| Optimal | (O(N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Let (m=\lfloor N/2\rfloor). Define categories for values of (A). Values (1,\ldots,m) belong to the low category, values (m+2,\ldots,N) belong to the high category, and when (N) is odd, value (m+1) is the middle category.

This classification captures exactly the three groups that can appear in an optimal permutation.
2. Classify each position according to its value in (B). If (B_i\le m), an optimal arrangement must put a high (A)-value there. If (B_i>m+1), it must put a low (A)-value there. For odd (N), the unique position with (B_i=m+1) must receive the middle value.

For even (N), there is no middle category, so the condition simply swaps the low and high halves.
3. Scan (A) and record the positions at which each category currently occurs. Also scan the target categories induced by (B) and record the positions where each category must occur.

The exact values inside one category do not matter. This is why recording only categories is sufficient.
4. For every category, pair its current occurrences and target occurrences in their left-to-right order. Add the absolute difference between every paired position.

Matching occurrences in another order would force two equal-category elements to cross. Since they are interchangeable with respect to the objective, such a crossing can only add swaps and cannot improve the result.
5. Divide the total positional movement by two and print it.

Each adjacent swap moves one element one position to the left and another one position to the right. Thus it contributes exactly (2) to the total sum of absolute position changes.

### Why it works

The threshold argument proves that every maximizing permutation has exactly the required category at every position. Conversely, any permutation satisfying those category requirements reaches all threshold lower bounds simultaneously, so it is maximizing. Once the categories are fixed, values belonging to the same category are interchangeable for the objective. The minimum adjacent-swap transformation between two category sequences is obtained by matching equal-category occurrences in order. Hence the computed positional movement is exactly twice the minimum number of swaps, and the algorithm returns the required minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    m = n // 2

    # Categories:
    # 0 = low values
    # 1 = middle value, only for odd n
    # 2 = high values
    #
    # Store positions of each category in the current A
    # and in the required target category sequence.
    cur = [[], [], []]
    target = [[], [], []]

    for i, x in enumerate(a):
        if x <= m:
            cur[0].append(i)
        elif n % 2 == 1 and x == m + 1:
            cur[1].append(i)
        else:
            cur[2].append(i)

    for i, x in enumerate(b):
        if x <= m:
            # Small B values need large A values.
            target[2].append(i)
        elif n % 2 == 1 and x == m + 1:
            # The middle value must meet the middle value.
            target[1].append(i)
        else:
            # Large B values need small A values.
            target[0].append(i)

    movement = 0

    for c in range(3):
        for p, q in zip(cur[c], target[c]):
            movement += abs(p - q)

    print(movement // 2)

if __name__ == "__main__":
    solve()
```

The first loop classifies the elements of (A) by their numerical value. For even (N), the low half is (1,\ldots,N/2), while every larger value belongs to the high half. For odd (N), the single value ((N+1)/2) receives its own category.

The second loop performs the same classification from the other direction. A small (B_i) requires a large (A)-value in an optimal arrangement, while a large (B_i) requires a small (A)-value. For odd (N), the middle position must receive the middle value.

The positions are stored as zero-based indices. This is convenient because the distance between two positions is still exactly the number of adjacent swaps needed to move an element between them. There is no boundary adjustment required.

The `zip` operation pairs occurrences in their natural left-to-right order. Both lists contain the same number of occurrences because both (A) and (B) are permutations. The total movement is accumulated over all categories and divided by two because each adjacent swap changes the positions of exactly two elements.

The answer can exceed (2^{31}-1), but Python integers automatically expand as necessary. The largest possible answer is on the order of (N^2), which is easily handled by Python's integer arithmetic.

## Worked Examples

### Sample 1

The input is

```
3
1 2 3
1 2 3
```

Here (N=3) and (m=1). The value (1) is low, (2) is middle, and (3) is high.

| Position | A value | Current category | B value | Target category |
| --- | --- | --- | --- | --- |
| 0 | 1 | Low | 1 | High |
| 1 | 2 | Middle | 2 | Middle |
| 2 | 3 | High | 3 | Low |

The low category is currently at position (0) but must be at position (2), contributing (2). The high category moves from position (2) to position (0), contributing another (2). The middle category does not move.

| Category | Current positions | Target positions | Movement |
| --- | --- | --- | --- |
| Low | [0] | [2] | 2 |
| Middle | [1] | [1] | 0 |
| High | [2] | [0] | 2 |

The total movement is (4), so the answer is (4/2=2).

This demonstrates why reversing (A) is not necessary. The target could be ([2,3,1]), which has the same maximum objective and requires only two swaps.

### Sample 2

The input is

```
4
3 4 1 2
3 2 4 1
```

Now (N=4) and (m=2). Values (1,2) are low, while (3,4) are high.

| Position | A value | Current category | B value | Target category |
| --- | --- | --- | --- | --- |
| 0 | 3 | High | 3 | Low |
| 1 | 4 | High | 2 | High |
| 2 | 1 | Low | 4 | Low |
| 3 | 2 | Low | 1 | High |

The high values currently occupy positions (0,1), but they need positions (1,3). Their movement is

[
|0-1|+|1-3|=3.
]

The low values move from positions (2,3) to positions (0,2), also contributing (3).

| Category | Current positions | Target positions | Movement |
| --- | --- | --- | --- |
| Low | [2, 3] | [0, 2] | 3 |
| High | [0, 1] | [1, 3] | 3 |

The total movement is (6), so the minimum number of swaps is (6/2=3).

This also shows why we do not need to decide whether the final high values should be (3,4) or (4,3) in their target positions. Both choices are equally good, and occurrence matching automatically chooses the cheaper ordering relative to the original (A).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | Each element of (A) and (B) is classified once, and every stored position is processed once. |
| Space | (O(N)) | The current and target occurrence positions together contain (O(N)) positions. |

The linear complexity is comfortably within the (N\le250000) limit. The algorithm performs only a few passes over the input and does not sort or use a Fenwick tree, segment tree, or graph structure. The memory consumption is also linear and well below the 1024 MB limit.

## Test Cases

```python
import sys
import io

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    m = n // 2

    cur = [[], [], []]
    target = [[], [], []]

    for i, x in enumerate(a):
        if x <= m:
            cur[0].append(i)
        elif n % 2 == 1 and x == m + 1:
            cur[1].append(i)
        else:
            cur[2].append(i)

    for i, x in enumerate(b):
        if x <= m:
            target[2].append(i)
        elif n % 2 == 1 and x == m + 1:
            target[1].append(i)
        else:
            target[0].append(i)

    movement = 0
    for c in range(3):
        for p, q in zip(cur[c], target[c]):
            movement += abs(p - q)

    print(movement // 2)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        input = sys.stdin.readline

        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

# Provided samples
assert run("""3
1 2 3
1 2 3
""") == "2", "sample 1"

assert run("""4
3 4 1 2
3 2 4 1
""") == "3", "sample 2"

# Minimum size
assert run("""1
1
1
""") == "0", "single element"

# Even N, exactly one required swap
assert run("""2
1 2
1 2
""") == "1", "even boundary"

# Odd N, middle value must stay with the middle B-value
assert run("""5
1 2 3 4 5
1 2 3 4 5
""") == "6", "odd middle case"

# Already has an optimal category arrangement
assert run("""4
3 4 1 2
1 2 3 4
""") == "0", "already optimal"

# Maximum-size case and a large answer.
# For A=B=1..N with N=250000, the first half must cross
# with the second half, requiring (N/2)^2 swaps.
n = 250000
a = " ".join(map(str, range(1, n + 1)))
large_input = f"{n}\n{a}\n{a}\n"
assert run(large_input) == "15625000000", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (N=1,\ A=[1],\ B=[1]) | 0 | Minimum size and the single-value case |
| (N=2,\ A=[1,2],\ B=[1,2]) | 1 | Even-size boundary and complete half swap |
| (N=5,\ A=[1,2,3,4,5],\ B=[1,2,3,4,5]) | 6 | Odd size and the fixed middle value |
| (N=4,\ A=[3,4,1,2],\ B=[1,2,3,4]) | 0 | An arrangement that is already optimal |
| (N=250000,\ A=B=[1,\ldots,N]) | 15625000000 | Maximum input size and large integer answer |

The requested all-equal-value scenario is deliberately absent from the executable tests because it violates the permutation condition. A valid permutation cannot contain equal values. The (N=1) test covers the smallest possible instance instead.

## Edge Cases

For (N=1), the input

```
1
1
1
```

has only one possible arrangement. The middle category contains the single value, its current position and target position are both zero, and the movement is zero. The algorithm prints (0).

For the even boundary (N=2),

```
2
1 2
1 2
```

the first (B)-position has a low value and therefore requires the high value (2). The second position requires the low value (1). The current category sequence is Low, High, while the target is High, Low. The two category occurrences move by one position each, giving total movement (2) and answer (1).

For the odd case (N=3),

```
3
1 2 3
1 2 3
```

the middle value (2) must remain at the middle position, while (1) and (3) exchange categories. The low and high occurrences each move two positions, giving total movement (4) and answer (2). This is exactly the case where blindly choosing the complete reverse permutation would overestimate the required number of swaps.

For a configuration that is already optimal,

```
4
3 4 1 2
1 2 3 4
```

the first two positions have small (B)-values and already contain the high (A)-values (3,4). The last two positions have large (B)-values and already contain the low values (1,2). Every current category position matches its target position, so the movement is zero and no swap is needed.

For the maximum-size case, take (N=250000) with (A=B=[1,2,\ldots,N]). The first (125000) positions currently contain low values but must contain high values, while the last (125000) positions contain high values but must contain low values. Every low occurrence must cross every high occurrence, producing

[
125000\cdot125000=15625000000
]

adjacent swaps. The algorithm obtains exactly this value without ever constructing the final permutation.

---
title: "CF 102299I - Sobytiynyy Proyekt Casino"
description: "We have (N) pairs ((pi,fi)). When a pair is reached, the player receives (pi) rubles and can stop immediately, paying (fi) rubles. If (fi) is negative, paying it means receiving additional money. If the player reaches the final pair, stopping is mandatory there."
date: "2026-08-13T08:19:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102299
codeforces_index: "I"
codeforces_contest_name: "2019 USP Try-outs"
rating: 0
weight: 102299
solve_time_s: 109
verified: true
draft: false
---

[CF 102299I - Sobytiynyy Proyekt Casino](https://codeforces.com/problemset/problem/102299/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (N) pairs ((p_i,f_i)). When a pair is reached, the player receives (p_i) rubles and can stop immediately, paying (f_i) rubles. If (f_i) is negative, paying it means receiving additional money. If the player reaches the final pair, stopping is mandatory there.

The casino chooses the order of all pairs before the game starts. The player then chooses the best possible stopping point. Our task is to choose the ordering that makes the player's optimal final gain as small as possible, and output that minimum possible gain.

For a fixed ordering, suppose the first (i) pairs have been played. If the player stops exactly there, her gain is

[
p_1+p_2+\cdots+p_i-f_i.
]

The player can choose any stopping position, including the last one. Consequently, for a fixed permutation the player's optimal gain is

[
\max_{1\le i\le N}\left(\sum_{j=1}^{i}p_j-f_i\right).
]

So the problem becomes a pure ordering problem: arrange the pairs so that the maximum of these prefix expressions is minimized.

With (N) up to (10^5), enumerating permutations is impossible. Even a quadratic algorithm would already perform around (10^{10}) operations in the largest case, far beyond the available time. We need a sorting-based solution, which gives (O(N\log N)).

There are several edge cases that easily cause incorrect solutions. A negative (f_i) must be handled literally. For example,

```
1
1 -2
```

The player receives (1) and then receives another (2), so the answer is (3), not (1) or (-1). A solution that assumes the fee is always nonnegative gets this wrong.

The final pair is also special in the game description, but it does not need separate treatment in the formula. For example,

```
1
0 1
```

forces the player to pay (1), so the answer is (-1). The expression (0-1=-1) already captures this. Treating the final pair as if the player could simply ignore its fee would produce the wrong answer.

Zero values of (p_i) are allowed. For

```
2
0 1
3 4
```

the ordering shown gives prefix values (-1) and (-1), so the answer is (-1). A proof or implementation that relies on every round strictly increasing the accumulated amount would be invalid.

Finally, equal (f_i) values do not require a special tie-breaking rule. Any order among equal (f_i) values is optimal. For example,

```
3
2 5
1 5
3 5
```

has prefix values (-3,-2,1) in any order, so the answer is (1).

## Approaches

The direct approach is to try every permutation of the (N) pairs. For each permutation, scan from left to right, maintain the accumulated (p), and compute the largest value of (prefix-f_i). This is correct because it evaluates exactly the gain available to the optimal player for every possible stopping position, then takes the best one. However, there are (N!) permutations and each one takes (O(N)) time to evaluate, giving (O(N\cdot N!)) operations. Even at (N=10), this is already about (36) million basic positions to inspect, and (N=11) raises that to roughly (440) million. At (N=10^5), this approach is not remotely feasible.

The useful observation is that the player's gain has exactly the form of a scheduling objective. Think of (p_i) as the processing time of job (i), and (f_i) as its due date. After processing the first (i) jobs, its completion time is the prefix sum of the (p)'s, and its lateness is

[
C_i-f_i.
]

We need to minimize the maximum lateness. The classical exchange argument says that jobs should be processed in nondecreasing order of their due dates, which here means sorting the pairs by increasing (f_i).

The reason can be derived directly without relying on the scheduling terminology. Suppose two adjacent pairs (a) and (b) are currently ordered incorrectly, so (f_a>f_b). Let (S) be the accumulated (p) before these two pairs. In the order (a,b), the two relevant values are

[
S+p_a-f_a
]

and

[
S+p_a+p_b-f_b.
]

Because (f_a>f_b) and (p_b\ge0), the second value is always at least the first. Thus this pair contributes

[
S+p_a+p_b-f_b
]

to the maximum.

Now swap them into the order (b,a). The two values become

[
S+p_b-f_b
]

and

[
S+p_b+p_a-f_a.
]

The first is no larger than the old maximum because (p_a\ge0). The second is no larger because (f_a>f_b), so subtracting (f_a) can only make it smaller than subtracting (f_b). Thus swapping an inversion cannot increase the player's optimal gain.

Repeatedly removing every inversion leaves the pairs sorted by increasing (f_i), and never makes the answer worse. Hence this sorted order is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N\cdot N!)) | (O(N)) | Too slow |
| Optimal | (O(N\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Read all pairs ((p_i,f_i)). The only property that determines their relative order is (f_i), so we can keep each pair intact and sort by its second component.
2. Sort the pairs by increasing (f_i). The exchange argument shows that whenever a larger (f) appears before a smaller (f), swapping those two pairs cannot increase the maximum gain available to the player. Repeating this process gives exactly the sorted order.
3. Scan the sorted pairs from left to right and maintain `prefix`, the total amount of money received so far. After adding a pair ((p,f)), the player could stop at this pair and obtain `prefix - f`.
4. Maintain the maximum of all values `prefix - f`. This maximum is the player's optimal gain for the chosen ordering because every possible stopping position has been considered.
5. Print the maximum. Since the ordering was chosen optimally, this is the smallest gain that any ordering can allow an optimal player to obtain.

### Why it works

For any fixed ordering, the player can stop at exactly one position, and stopping at position (i) gives the value (prefix_i-f_i). Thus the player's optimal gain is exactly the maximum of these values.

Consider any adjacent inversion where (f_a>f_b). With the two pairs ordered as (a,b), the larger of their two affected stopping values is (S+p_a+p_b-f_b). After swapping them, the two affected values are (S+p_b-f_b) and (S+p_a+p_b-f_a). Both are at most the old maximum because (p_a\ge0) and (f_a>f_b). All other stopping positions have exactly the same prefix sum and are unchanged. Hence removing an inversion never increases the objective.

Every permutation can be transformed into nondecreasing (f) order by repeatedly removing inversions. Since none of those swaps increases the objective, the sorted order has an objective value no larger than any other ordering. It is consequently optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pairs = [tuple(map(int, input().split())) for _ in range(n)]

    pairs.sort(key=lambda x: x[1])

    prefix = 0
    answer = None

    for p, f in pairs:
        prefix += p
        value = prefix - f
        if answer is None or value > answer:
            answer = value

    print(answer)

if __name__ == "__main__":
    solve()
```

The input is stored as pairs so that sorting never separates a (p_i) from its corresponding (f_i). The sort key is the second component, giving increasing (f_i).

`prefix` is updated before calculating `value`. This corresponds to the player receiving (p_i) before deciding whether to leave at that round. Calculating `prefix - f` before adding (p_i) would represent a different game and creates an off-by-one error.

`answer` starts as `None` instead of a large hard-coded number. This is especially convenient because the correct answer can be negative, as in Sample 3. Python integers also handle the largest possible prefix automatically. The total of all (p_i) can reach (10^{14}), which would overflow a 32-bit integer in languages such as C++, although Python has arbitrary-precision integers.

There is no separate branch for the final pair. Its value is included when the scan reaches it, and because the player must stop there, the expression `prefix - f` is exactly the required final payoff.

## Worked Examples

For Sample 1, the input pairs are ((1,2)), ((3,3)), and ((2,1)). Sorting by (f) gives ((2,1)), ((1,2)), ((3,3)).

| Pair | Prefix | Prefix - f | Current answer |
| --- | --- | --- | --- |
| ((2,1)) | 2 | 1 | 1 |
| ((1,2)) | 3 | 1 | 1 |
| ((3,3)) | 6 | 3 | 3 |

The player's three possible stopping gains are (1), (1), and (3). She chooses the largest one, namely (3). Since increasing (f) order is optimal, no other permutation can force a smaller optimal gain.

For Sample 2, there is only one pair, ((1,-2)).

| Pair | Prefix | Prefix - f | Current answer |
| --- | --- | --- | --- |
| ((1,-2)) | 1 | 3 | 3 |

The negative fee increases the player's gain, giving (1-(-2)=3). The forced final payment is handled naturally by the same expression.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) | Sorting dominates the linear scan |
| Space | (O(N)) | The (N) pairs are stored for sorting |

With (N=10^5), sorting requires roughly (N\log N) comparisons, which is practical. The scan afterward is linear, and the memory usage is proportional to the number of input pairs. The accumulated sum can reach (10^{14}), and Python integers safely represent it.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    pairs = [tuple(map(int, input().split())) for _ in range(n)]

    pairs.sort(key=lambda x: x[1])

    prefix = 0
    answer = None

    for p, f in pairs:
        prefix += p
        value = prefix - f
        if answer is None or value > answer:
            answer = value

    return str(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("""3
1 2
3 3
2 1
""") == "3", "sample 1"

assert run("""1
1 -2
""") == "3", "sample 2"

assert run("""2
0 1
3 4
""") == "-1", "sample 3"

# Minimum-size input
assert run("""1
0 0
""") == "0", "single zero pair"

# Equal f values, any internal order is optimal
assert run("""4
2 5
2 5
2 5
2 5
""") == "3", "equal f values"

# Negative f and ordering direction
assert run("""2
1 -1
1 1
""") == "2", "negative f and increasing f order"

# Maximum-size input, also checks large prefix sums
max_case = "100000\n" + "1 0\n" * 100000
assert run(max_case) == "100000", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0` | `0` | Minimum size and zero values |
| `4 / 2 5` repeated | `3` | Equal (f_i) values and arbitrary tie order |
| `2 / 1 -1 / 1 1` | `2` | Negative fee and correct ascending sort direction |
| (100000) copies of `1 0` | `100000` | Maximum (N), large prefix sum, and linear scan |

## Edge Cases

The single negative-fee pair

```
1
1 -2
```

is handled by sorting the one-element array and computing `prefix = 1`, followed by `prefix - f = 1 - (-2) = 3`. The algorithm does not assume that stopping costs money. A negative (f) is simply a bonus when the player leaves.

The forced final pair does not require a special case. For

```
1
0 1
```

the scan obtains `prefix = 0` and computes `0 - 1 = -1`. Because this is the only possible stopping position, the answer is exactly (-1). More generally, the final position is included among the same stopping expressions as every earlier position.

Zero (p_i) values are also handled directly. In

```
2
0 1
3 4
```

the pairs are already sorted by (f). The first prefix is (0), giving (-1), and the second prefix is (3), giving (3-4=-1). The maximum is (-1). The exchange proof uses (p_i\ge0), so zero processing times are fully valid.

Equal (f_i) values do not affect the greedy argument. For

```
4
2 5
2 5
2 5
2 5
```

every possible ordering is equivalent because all fees are identical. The prefix values are (2,4,6,8), so the stopping gains are (-3,-1,1,3), and the answer is (3). Sorting is stable or unstable here without affecting the result.

Negative answers are valid and must not be confused with an absence of profit. Sample 3 produces (-1), because every available stopping position loses one ruble. Initializing the answer to zero would incorrectly turn this into (0), which is why the implementation initializes it from the first computed value.

The largest accumulated amount can be (10^5\cdot10^9=10^{14}). Python's integer representation handles this exactly, while a 32-bit implementation would overflow. The algorithm never performs arithmetic on values larger than this scale, so there is no numerical issue in Python.

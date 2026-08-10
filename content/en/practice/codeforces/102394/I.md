---
title: "CF 102394I - Interesting Permutation"
description: "We have a permutation (a) containing every integer from (1) to (n) exactly once. For every prefix (a1,ldots,ai), consider its largest and smallest values. Their difference is (hi)."
date: "2026-08-10T21:24:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "I"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 97
verified: true
draft: false
---

[CF 102394I - Interesting Permutation](https://codeforces.com/problemset/problem/102394/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a permutation (a) containing every integer from (1) to (n) exactly once. For every prefix (a_1,\ldots,a_i), consider its largest and smallest values. Their difference is (h_i). The task is to determine how many different permutations produce exactly the given sequence (h), with the answer taken modulo (10^9+7).

The crucial fact is that (h_i) describes only the width of the interval between the current minimum and maximum. It does not tell us which endpoint is the minimum or maximum, nor where the values strictly between those endpoints appeared. The counting problem is thus about how many ways we can grow this interval while placing each permutation element exactly once.

The official archive gives a 1 second time limit and 512 MB memory limit. The value of (n) can reach (10^5), and the total (n) over all test cases can reach (2\cdot10^6). A solution that is quadratic in (n) would already perform around (10^{10}) operations in the largest aggregate input, which is far beyond the intended limit. Even (O(n\log n)) is unnecessary here because the information needed at position (i) depends only on the previous width and the number of currently unused interior values. The target is a linear scan.

There are several invalid sequences that a careless implementation can mishandle. First, (h_1) must be zero because the first prefix contains only one value, so its maximum and minimum are equal. For example, with (n=2) and (h=[1,1]), the correct answer is (0). An implementation that starts processing only from (i=2) without checking (h_1) could incorrectly accept it.

Second, the width can never decrease. Once a value has been seen, the prefix minimum can only stay the same or decrease, while the prefix maximum can only stay the same or increase. Thus (h_i\ge h_{i-1}). For example, (n=3) and (h=[0,2,1]) has answer (0). A careless recurrence that treats every non-equal transition as an expansion would count this impossible decrease as another valid expansion.

Third, the width cannot exceed (n-1), because all permutation values lie in the interval ([1,n]). For example, (n=3) and (h=[0,3,3]) has answer (0). The largest possible difference is (3-1=2).

Finally, a plateau can be impossible even though the sequence is nondecreasing. Consider (n=3) and (h=[0,1,1]). After the first expansion, the prefix must contain the two endpoints of an interval of width (1), such as (1,2) or (2,3). There is no unused value strictly between those endpoints, so the third position has no legal choice. The correct answer is (0). A naive solution that multiplies by some fixed number for every equal transition can miss this lack of available interior values.

At the other extreme, (n=1) with (h=[0]) is valid and has exactly one permutation, namely ([1]). This case is useful because there are no transitions to process, so the initial answer must already be (1).

## Approaches

The direct approach is to enumerate every permutation of (1,\ldots,n). For each permutation, scan it from left to right, maintaining its prefix maximum and minimum, and compare the resulting differences with the given (h). This is correct because every possible permutation is checked exactly once.

The problem is the number of permutations. There are (n!) of them, and checking one permutation takes (\Theta(n)) time. The total complexity is therefore (\Theta(n\cdot n!)). Even at (n=10), this already means roughly (3.6\times10^7) prefix operations, while (n) is allowed to be (10^5). The brute-force method is not merely slightly too slow, it is unusable.

The useful observation is that we never need to know the exact minimum and maximum values. We only need to know how their distance changes.

Suppose the current prefix has width (h_{i-1}). Since the prefix interval cannot shrink, (h_i<h_{i-1}) is immediately impossible.

If (h_i>h_{i-1}), the new value (a_i) must become either the new maximum or the new minimum. Those are the only two possibilities, so this transition contributes a factor of (2). If the width grows by (d=h_i-h_{i-1}), the new endpoint leaves exactly (d-1) previously unseen values strictly inside the new interval. These values become future choices for positions where the width stays unchanged.

If (h_i=h_{i-1}), the new value cannot be a new maximum or minimum. It must be an unused value strictly between the current endpoints. Thus the number of choices is exactly the number of unused interior values.

This gives a very small state. Let `slots` be the number of unused values currently lying strictly between the prefix minimum and maximum. When the interval expands by (d), we add (d-1) new interior values. When the interval stays unchanged, we choose one of the `slots` values and remove it, so the answer is multiplied by `slots` and then `slots` decreases by one.

The brute-force works because every permutation determines a unique sequence of endpoint expansions and interior placements. It fails because it explores all permutations independently. The observation that the only relevant information is the current width and the number of unused interior values lets us count all permutations sharing the same history simultaneously.

The resulting approaches are:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n\cdot n!)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) for the input array, (O(1)) extra | Accepted |

## Algorithm Walkthrough

1. Read (n) and the sequence (h). A valid sequence must start with (h_1=0), because the first prefix contains only one value. Also, every (h_i) must be at most (n-1), and the final value must be (n-1), because after all (n) values have been inserted, the prefix contains both (1) and (n). If any of these conditions fails, the answer is zero.
2. Scan the sequence from (i=2) to (n), keeping `ans`, the number of partial permutations represented by the current state, and `slots`, the number of unused values strictly between the current minimum and maximum.
3. If (h_i<h_{i-1}), return zero. A prefix interval can only stay the same or expand, never contract.
4. If (h_i>h_{i-1}), the new element must extend one of the two endpoints. It can become the new maximum or the new minimum, giving exactly two choices, so multiply `ans` by (2).
5. Let (d=h_i-h_{i-1}). The newly extended side has (d) positions of width added, but the endpoint itself is occupied immediately by (a_i). The remaining (d-1) values are strictly inside the new interval and have not appeared earlier, so increase `slots` by (d-1).
6. If (h_i=h_{i-1}), the new element must be strictly inside the current interval. There are exactly `slots` unused values available, so multiply `ans` by `slots` and decrease `slots` by one. If `slots` is zero, no permutation can realize this transition, and the answer becomes zero.
7. Perform every multiplication modulo (10^9+7), then print the final answer.

### Why it works

The invariant is that after processing position (i), `slots` is exactly the number of values that have not yet appeared in the permutation and are strictly between the current prefix minimum and maximum. When the width grows, the new endpoint is forced to be either the minimum or maximum, giving two choices, and every newly created interior integer is unused because all earlier values were inside the old interval. There are exactly (h_i-h_{i-1}-1) such values. When the width stays unchanged, the next value must be one of these unused interior values, and every such choice preserves both the current interval and all previous (h)-values. Thus every valid permutation is counted exactly once, while every counted transition corresponds to a valid placement.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))

        if h[0] != 0 or h[-1] != n - 1:
            out.append("0")
            continue

        valid = True
        for i in range(1, n):
            if h[i] < h[i - 1] or h[i] > n - 1:
                valid = False
                break

        if not valid:
            out.append("0")
            continue

        ans = 1
        slots = 0

        for i in range(1, n):
            if h[i] == h[i - 1]:
                if slots == 0:
                    ans = 0
                    break

                ans = ans * slots % MOD
                slots -= 1
            else:
                diff = h[i] - h[i - 1]

                ans = ans * 2 % MOD
                slots += diff - 1

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first validation checks (h_1=0) and (h_n=n-1). The first condition describes the one-element prefix, while the second follows from the fact that the complete permutation contains both (1) and (n).

The monotonicity check rejects a decreasing width immediately. The upper-bound check is technically implied by (h_n=n-1) together with monotonicity, but keeping it explicit makes the validity conditions clear and protects the transition logic from impossible input values.

`slots` starts at zero. At the beginning there is only one permutation element, so there cannot yet be an unused value strictly between the minimum and maximum.

For an expanding transition, `diff` is positive. Multiplying by two accounts for choosing whether the new element becomes the minimum or the maximum. The expression `diff - 1` counts the new interior values. When `diff` is one, no interior value is created, which is why this update can correctly add zero.

For an equal transition, `slots` is the exact number of legal choices. Checking `slots == 0` before multiplication avoids ever making the state negative. A negative slot count would have no combinatorial meaning and could cause an incorrect modular answer.

Python integers do not overflow, but the modulo operation is still required because the answer grows exponentially. The total input size is at most (2\cdot10^6), so storing one (h)-array per test case and processing it once is easily manageable.

## Worked Examples

### Sample 1

The first sample case is (n=3) with (h=[0,2,2]).

| Position | (h_i) | Previous (h) | Transition | `ans` | `slots` |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | Initial state | 1 | 0 |
| 2 | 2 | 0 | Expand by 2 | 2 | 1 |
| 3 | 2 | 2 | Use an interior value | 2 | 0 |

At position 2, the width jumps from zero to two. The new value can be the new minimum or the new maximum, giving two possibilities. The width increase is two, so exactly one new value lies strictly between the endpoints. At position 3 that value is forced. The two resulting permutations are ([1,3,2]) and ([3,1,2]), giving answer (2).

### Sample 2

The second sample case is (n=3) with (h=[0,1,2]).

| Position | (h_i) | Previous (h) | Transition | `ans` | `slots` |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | Initial state | 1 | 0 |
| 2 | 1 | 0 | Expand by 1 | 2 | 0 |
| 3 | 2 | 1 | Expand by 1 | 4 | 0 |

Every transition expands the interval by exactly one. Each expansion has two choices, but creates no unused interior value because `diff - 1` is zero. Hence the answer is (2\cdot2=4). The four permutations are ([1,2,3]), ([2,1,3]), ([2,3,1]), and ([3,2,1]).

These two examples show the two fundamental transition types. The first creates an interior slot and later consumes it, while the second only expands the endpoints and never needs an interior placement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) per test case, (O(\sum n)) overall | The sequence is scanned a constant number of times. |
| Space | (O(n)) | The input sequence is stored; the counting state uses (O(1)) extra space. |

Since the sum of all (n) is at most (2\cdot10^6), the total number of loop iterations is linear in the complete input size. This fits the intended constraints, while quadratic or factorial approaches do not. The official problem limits are 1 second and 512 MB.

## Test Cases

```python
import io
import sys

MOD = 10**9 + 7

def solve_data(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))

        if h[0] != 0 or h[-1] != n - 1:
            out.append("0")
            continue

        valid = True
        for i in range(1, n):
            if h[i] < h[i - 1] or h[i] > n - 1:
                valid = False
                break

        if not valid:
            out.append("0")
            continue

        ans = 1
        slots = 0

        for i in range(1, n):
            if h[i] == h[i - 1]:
                if slots == 0:
                    ans = 0
                    break
                ans = ans * slots % MOD
                slots -= 1
            else:
                diff = h[i] - h[i - 1]
                ans = ans * 2 % MOD
                slots += diff - 1

        out.append(str(ans))

    return "\n".join(out)

# Provided samples
sample = """\
3
3
0 2 2
3
0 1 2
3
0 2 3
"""
assert solve_data(sample) == "2\n4\n0", "provided samples"

# Minimum-size input
assert solve_data("""\
1
1
0
""") == "1", "n=1 has exactly one permutation"

# All equal values, impossible for n > 1
assert solve_data("""\
1
4
0 0 0 0
""") == "0", "no distinct permutation can keep width zero"

# Boundary case with exactly one interior slot
assert solve_data("""\
1
3
0 2 2
""") == "2", "one forced interior placement"

# Decreasing width
assert solve_data("""\
1
3
0 2 1
""") == "0", "prefix width cannot decrease"

# Width larger than n - 1
assert solve_data("""\
1
3
0 3 3
""") == "0", "maximum possible width is n-1"

# Equal transition with no available interior slot
assert solve_data("""\
1
3
0 1 1
""") == "0", "plateau cannot be filled"

# Maximum-size input.
# h = [0, 1, 2, ..., n-1], so every transition has two choices.
n = 100000
h = list(range(n))
inp = "1\n{}\n{}\n".format(n, " ".join(map(str, h)))
expected = str(pow(2, n - 1, MOD))
assert solve_data(inp) == expected, "maximum-size linear scan"
```

The custom cases validate the smallest possible permutation, the impossibility of keeping the width zero after the first element, the creation and consumption of an interior slot, decreasing widths, widths outside the range allowed by the permutation, an off-by-one plateau with zero available slots, and the maximum allowed input size.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 0` | `1` | Minimum size and empty transition loop |
| `1 / 4 / 0 0 0 0` | `0` | All-equal widths for (n>1) |
| `1 / 3 / 0 2 2` | `2` | Interior-slot counting |
| `1 / 3 / 0 2 1` | `0` | Decreasing width |
| `1 / 3 / 0 3 3` | `0` | Width greater than (n-1) |
| `1 / 3 / 0 1 1` | `0` | Equal transition with zero slots |
| `1 / 100000 / 0 1 \ldots 99999` | (2^{99999}\bmod(10^9+7)) | Maximum-size linear processing |

## Edge Cases

For (n=1), the only possible permutation is ([1]), so the generated sequence is ([0]). The algorithm accepts (h_1=0), confirms (h_n=n-1=0), performs no transition, and returns the initial answer (1).

For an invalid first value, consider (n=2) and (h=[1,1]). A one-element prefix always has maximum equal to minimum, so its width must be zero. The initial validation rejects the sequence before the transition scan, giving (0).

For a decreasing sequence, consider (n=3) and (h=[0,2,1]). After the first two elements produce width (2), adding another element cannot make the prefix range narrower. The scan detects (1<2) and returns (0).

For an excessively large width, consider (n=3) and (h=[0,3,3]). The only values available are (1,2,3), so the largest possible difference is (2). Since (h_2=3>n-1), the sequence is rejected and the answer is (0).

For a plateau without an available interior value, consider (n=3) and (h=[0,1,1]). The first expansion has `diff=1`, so it creates `diff-1=0` interior slots. At the next position the width stays equal, but `slots` is zero, so there is no legal value to place and the answer becomes (0).

For a plateau with an available interior value, consider (n=3) and (h=[0,2,2]). The expansion has `diff=2`, creating one interior slot. The equal transition multiplies the answer by one and consumes that slot. The two endpoint orientations remain distinct, giving answer (2).

For the largest possible width, consider (h=[0,1,2,\ldots,n-1]). Every transition expands the interval by one, so there are always exactly two choices and no interior slots are created. The result is (2^{n-1}\bmod(10^9+7)), which also provides a useful maximum-size performance test.

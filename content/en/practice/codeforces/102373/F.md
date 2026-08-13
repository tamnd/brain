---
title: "CF 102373F - \u041e\u043d\u0438"
description: "We have a line of (n) positions. Position (i) contains (ai) children. The old Pennywise takes a prefix of the array, positions (1) through (l), while the modern Pennywise takes a suffix, positions (r) through (n). The two parts must not overlap, so (l<r)."
date: "2026-08-14T03:12:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102373
codeforces_index: "F"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434 \u0434\u043b\u044f \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102373
solve_time_s: 188
verified: false
draft: false
---

[CF 102373F - \u041e\u043d\u0438](https://codeforces.com/problemset/problem/102373/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We have a line of (n) positions. Position (i) contains (a_i) children. The old Pennywise takes a prefix of the array, positions (1) through (l), while the modern Pennywise takes a suffix, positions (r) through (n). The two parts must not overlap, so (l<r).

If (P_k=a_1+a_2+\dots+a_k) is a prefix sum and (T=P_n) is the total number of children, then the two frightened counts are

[
S_1=P_l,
\qquad
S_2=T-P_{r-1}.
]

The goal is to choose valid (l,r) so that (|S_1-S_2|) is as small as possible, and output that minimum together with any pair achieving it.

The array can contain up to (10^6) elements, and each element can be as large as (10^9). The official statement gives a 2 second time limit and 512 MB memory limit. An (O(n^2)) algorithm would examine roughly (5\cdot10^{11}) pairs at the maximum size, so it is far beyond what the time limit allows. We need a linear or near-linear solution. The sums can reach (10^{15}), so a fixed-width implementation needs 64-bit integers. Python integers already handle this range safely.

There are several boundary cases that can make an otherwise reasonable implementation fail. With (n=2) and input `7 7`, the only valid choice is (l=1,r=2), giving output `0 1 2`. Code that requires two different prefix-sum indices would incorrectly reject this case, because the transformation below permits the same prefix sum to be used twice.

An initially perfect answer must also be checked before moving either pointer. For `4` and `5 1 1 5`, choosing (l=1,r=4) gives (S_1=S_2=5), so the correct output can be `0 1 4`. If an implementation moves a pointer before recording the current pair, it can silently lose the optimum.

The best pair can also be adjacent. For `3` and `1 2 3`, choosing (l=2,r=3) gives (3) children to each Pennywise, so the answer is `0 2 3`. Any loop that stops while (l+1=r) without evaluating that state misses a valid solution.

Finally, the sums can be very large. With (n=2) and `1000000000 1000000000`, the total is (2\cdot10^9), and for (n=10^6) it can reach (10^{15}). Using 32-bit arithmetic would overflow in languages with fixed-width integers.

## Approaches

The direct approach is to try every valid pair ((l,r)). There are

[
(n-1)+(n-2)+\dots+1=\frac{n(n-1)}2
]

such pairs. With prefix sums, each pair can be evaluated in (O(1)), so this gives (O(n^2)) time. It is correct because every possible choice is explicitly examined, but for (n=10^6) it means exactly (499{,}999{,}500{,}000) candidate pairs, which is much too slow.

The useful observation comes from rewriting the difference. Since

[
S_1=P_l
]

and

[
S_2=T-P_{r-1},
]

we have

# |P_l-(T-P_{r-1})|

|P_l+P_{r-1}-T|.
]

Now introduce

[
i=l,\qquad j=r-1.
]

The condition (l<r) becomes simply (i\le j). Thus the original problem is equivalent to choosing two prefix sums (P_i) and (P_j), with (1\le i\le j\le n-1), whose sum is as close as possible to (T).

This is exactly a closest two-sum problem on a sorted array. Because every (a_i) is positive, prefix sums are strictly increasing. We can put one pointer at the smallest usable prefix sum, (P_1), and another at the largest usable prefix sum, (P_{n-1}).

If their sum is smaller than (T), the only way to get closer to (T) is to increase the smaller pointer. If their sum is larger than (T), the only way to get closer is to decrease the larger pointer. Each pointer moves only in one direction, so the complete search takes (O(n)).

The connection with the brute-force solution is now clear. Brute force considers every pair of prefix sums, while the monotonicity of the prefix sums lets us discard an entire row or column of impossible-to-improve pairs after each comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the array and convert it into prefix sums in place. After this transformation, `a[k]` represents (P_{k+1}), the sum of the first (k+1) original elements. The final prefix sum is the total (T).
2. Set the left pointer `i = 0`. This represents (P_1), so it corresponds to (l=1). Set the right pointer `j = n-2`. This represents (P_{n-1}), so it corresponds to (r=n). These are exactly the smallest and largest prefix sums that can participate in a valid pair.
3. Compute `a[i] + a[j]` and compare it with the total (T). Record the absolute difference if it improves the best answer found so far. The current pair must be checked before changing either pointer because it can already be optimal.
4. If `a[i] + a[j] < T`, increment `i`. Increasing a prefix sum is the only pointer movement that can make the current sum larger. Decreasing `j` would make the sum even smaller, so it cannot improve the current candidate.
5. If `a[i] + a[j] >= T`, decrement `j`. When the sum is too large, decreasing the right prefix sum is the only movement that can bring the pair toward the target. If the sum is exactly (T), the difference is zero and the optimum has already been found, although the loop may safely continue.
6. Stop when `i > j`. Every valid pair has (i\le j), so no unexamined valid pair remains.
7. Convert the prefix-sum indices back to the required positions. Since zero-based `i` represents (P_{i+1}), we have (l=i+1). Since zero-based `j` represents (P_{j+1}=P_{r-1}), we have (r=j+2).

### Why it works

The invariant is that every pair discarded by moving a pointer cannot contain a better answer than the candidates still represented by the two pointers. Suppose (P_i+P_j<T). For this fixed (j), every prefix sum (P_k) with (k<i) is even smaller, so (P_k+P_j) is farther below (T). Such values can never produce a better pair, so increasing (i) safely discards them. The case (P_i+P_j>T) is symmetric: for this fixed (i), every (P_k) with (k>j) produces an even larger sum and is farther above (T). Since all prefix sums are strictly increasing, these discarded regions can never contain a better solution. Each pointer moves monotonically, so when the pointers cross, every relevant pair has either been evaluated or safely discarded.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # Turn the array into prefix sums in place.
    total = 0
    for i in range(n):
        total += a[i]
        a[i] = total

    # a[i] represents P_{i+1}.
    # We need P_l and P_{r-1}, with l < r,
    # so their zero-based indices satisfy i <= j.
    i = 0
    j = n - 2

    best = 10**30
    best_i = i
    best_j = j

    while i <= j:
        current = a[i] + a[j]
        diff = abs(current - total)

        if diff < best:
            best = diff
            best_i = i
            best_j = j

        if current < total:
            i += 1
        else:
            j -= 1

    l = best_i + 1
    r = best_j + 2

    print(best, l, r)

if __name__ == "__main__":
    solve()
```

The first loop converts the original array into prefix sums without allocating a second (O(n)) array. After processing position `i`, `a[i]` is the sum of the original elements from position (1) through (i+1). The final value stored in `a[-1]` is the total number of children.

The two pointers operate on `a[0]` through `a[n-2]`. The last prefix sum cannot be used because (P_n) would correspond to (r-1=n), or (r=n+1), which is outside the array. The zero-based mapping is easy to get wrong: `i` becomes (l=i+1), while `j` becomes (r=j+2).

The comparison uses `current < total` rather than `current <= total`. An exact equality is already the best possible difference, but either pointer movement after recording it is harmless. Keeping equality in the `else` branch gives a simple loop that always makes progress.

The best candidate is updated before moving a pointer. This handles cases where the initial pair is already optimal, including an exact zero difference. Python integers need no special overflow handling, even though the total can reach (10^{15}).

## Worked Examples

### Sample 1

The input is

```
5
5 1 1 1 1
```

The prefix sums are (5,6,7,8,9), and the total is (9).

| i | j | (P_{i+1}) | (P_{j+1}) | Pair sum | Difference | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 | 5 | 8 | 13 | 4 | decrease `j` |
| 0 | 2 | 5 | 7 | 12 | 3 | decrease `j` |
| 0 | 1 | 5 | 6 | 11 | 2 | decrease `j` |
| 0 | 0 | 5 | 5 | 10 | 1 | decrease `j` |

The best pair is `P_1=5` and `P_1=5`, giving (l=1) and (r=2). The corresponding suffix is the second position through the fifth, whose sum is (4), so the difference is (1). The trace also demonstrates why (i=j) is valid.

### Sample 2

The input is

```
4
1 2 3 4
```

The prefix sums are (1,3,6,10), and the total is (10).

| i | j | (P_{i+1}) | (P_{j+1}) | Pair sum | Difference | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 6 | 7 | 3 | increase `i` |
| 1 | 2 | 3 | 6 | 9 | 1 | increase `i` |
| 2 | 2 | 6 | 6 | 12 | 2 | decrease `j` |

The best state is `i=1`, `j=2`. It represents (P_2=3) and (P_3=6), so (l=2) and (r=4). The modern Pennywise gets (10-P_3=4), producing the required difference of (1).

The trace demonstrates the central two-pointer rule. While the current sum is below the target, only the left prefix sum should increase. Once the sum passes the target, the right prefix sum decreases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Building prefix sums takes (O(n)), and each pointer moves at most (n) times. |
| Space | (O(n)) | The input array is reused to store prefix sums. |

With (n\le10^6), a linear scan is appropriate for the 2 second limit, while the quadratic brute-force approach would require about (5\cdot10^{11}) candidate pairs in the largest case. The in-place prefix-sum construction also keeps memory comfortably below the 512 MB limit.

## Test Cases

```python
# Complete assert-based tests for the solution above.
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    total = 0
    for i in range(n):
        total += a[i]
        a[i] = total

    i = 0
    j = n - 2

    best = 10**30
    best_i = i
    best_j = j

    while i <= j:
        current = a[i] + a[j]
        diff = abs(current - total)

        if diff < best:
            best = diff
            best_i = i
            best_j = j

        if current < total:
            i += 1
        else:
            j -= 1

    print(best, best_i + 1, best_j + 2)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("5\n5 1 1 1 1\n") == "1 1 2", "sample 1"
assert run("4\n1 2 3 4\n") == "1 2 4", "sample 2"

# Minimum-size input
assert run("2\n7 7\n") == "0 1 2", "minimum size"

# All values equal, with several optimal pairs
assert run("5\n4 4 4 4 4\n") == "0 1 5", "all equal"

# Optimum occurs at the adjacent boundary l + 1 = r
assert run("3\n1 2 3\n") == "0 2 3", "adjacent optimum"

# Maximum-size input, also testing a large number of iterations
max_n = 10**6
max_input = str(max_n) + "\n" + ("1 " * (max_n - 1)) + "1\n"
assert run(max_input) == "0 1 1000000", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 7 7` | `0 1 2` | Minimum size and the valid case (i=j) |
| `5 / 4 4 4 4 4` | `0 1 5` | All equal values and an initially exact match |
| `3 / 1 2 3` | `0 2 3` | Adjacent boundaries and correct index conversion |
| `1000000 / 1 1 ... 1` | `0 1 1000000` | Maximum (n), linear runtime, and large input handling |

## Edge Cases

For the minimum-size case

```
2
7 7
```

the prefix array is `[7, 14]`, with total (14). The usable prefix-sum range contains only (P_1=7), so the pointers start at `i=0,j=0`. Their sum is (14), giving difference (0). The conversion produces (l=1) and (r=2). This confirms that (i=j) must be allowed.

For an initially exact match,

```
4
5 1 1 5
```

the prefix sums are `[5, 6, 7, 12]`, with total (12). The initial pointer state uses (5+7=12), so the algorithm immediately records difference (0), corresponding to (l=1,r=4). It does not matter that the loop later moves a pointer, because the best answer has already been stored. This is why updating the answer before pointer movement is necessary.

For an optimum at adjacent positions,

```
3
1 2 3
```

the prefix sums are `[1, 3, 6]` and the total is (6). The initial pair gives (1+3=4), which is below the target, so `i` increases. The next pair is (3+3=6), giving difference (0). The two prefix indices are equal, which maps to (l=2,r=3). The two Pennywises therefore occupy positions `1..2` and `3..3`, exactly the required adjacent split.

For the large-value case,

```
2
1000000000 1000000000
```

the prefix sums are `[1000000000, 2000000000]`, and the total is (2000000000). The only usable prefix sum is (10^9), and using it twice gives exactly the total. The answer is `0 1 2`. At the maximum input size, the total can instead reach (10^{15}), which is still safely represented by Python's integer type and requires a 64-bit integer in languages with fixed-width arithmetic.

---
title: "CF 125D - Two progressions"
description: "We are given a sequence of distinct integers in a fixed order. Every element must be assigned to exactly one of two subsequences. Inside each subsequence, the original order must be preserved. The goal is to make both subsequences arithmetic progressions."
date: "2026-06-02T16:23:26+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 125
codeforces_index: "D"
codeforces_contest_name: "Codeforces Testing Round 2"
rating: 2200
weight: 125
solve_time_s: 144
verified: false
draft: false
---

[CF 125D - Two progressions](https://codeforces.com/problemset/problem/125/D)

**Rating:** 2200  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of distinct integers in a fixed order. Every element must be assigned to exactly one of two subsequences. Inside each subsequence, the original order must be preserved.

The goal is to make both subsequences arithmetic progressions. A progression of length 1 or 2 is always valid. A progression of length 0 is not allowed, so both resulting subsequences must contain at least one element.

The sequence length is up to 30000. Any approach that tries many different assignments of elements immediately becomes impossible. Even checking all $2^n$ partitions is absurdly large. The solution has to exploit strong structural properties of arithmetic progressions and run in roughly linear time.

The most subtle part of the problem is that arithmetic progressions are defined by order, not by sorting. For example:

```
1 5 3
```

The subsequence `1 3` is arithmetic, but `1 5 3` is not. Any solution that sorts the array first solves a different problem.

Another easy mistake is assuming that once we guess one progression, every matching value must belong to it. Consider:

```
1 2 3 -2 -7
```

Both of the following are valid:

```
1 2 3
-2 -7
```

and

```
1 2
3 -2 -7
```

The algorithm must allow for this ambiguity.

A third pitfall appears when one progression is almost correct and only its last chosen element is misplaced. For example:

```
4 1 2 7 3 10
```

If we build the progression `1 2 3`, everything works. For other guesses, the remaining elements may fail to be arithmetic until we move the last selected element from one progression to the other.

## Approaches

A brute-force idea is to try every partition of the sequence into two subsequences and check whether both are arithmetic. This is correct because it directly tests every possible answer. Unfortunately there are $2^n$ partitions. Even for $n=50$ this is already hopeless, and here $n$ reaches 30000.

The key observation comes from the first three elements.

When three elements are distributed into two subsequences, by the pigeonhole principle at least two of them belong to the same progression. Those two elements determine the common difference of that progression.

Among the first three positions there are only three possible pairs:

```
(1,2), (1,3), (2,3)
```

So there are only three candidate differences worth considering.

Suppose we choose one of these pairs and assume it belongs to progression A. Its difference is fixed. Once the difference is fixed, the entire progression A is determined: starting from its first chosen value, the next value must be exactly `start + d`, then `start + 2d`, and so on.

We scan the sequence from left to right. Whenever we encounter the next expected value of A, we put it into A. Everything else is temporarily placed into B.

After this construction, either B is already an arithmetic progression, or it is not.

The remaining trick is the only non-obvious part. If B is not arithmetic, we try moving the last element chosen for A into B and check again. If that still fails, then this candidate difference cannot produce a valid answer.

Why is moving only the last element enough? Suppose some solution exists for this candidate difference. The greedy construction always takes every available expected value of A. The only value that can be safely "given back" to B is the last one taken. If moving that last element does not repair B, then moving even more elements cannot help. The original Codeforces solution relies on this property and checks only these two configurations.

Since there are only three candidate differences and each check is linear, the whole algorithm is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. If `n = 2`, output the two elements as two single-element progressions.
2. Consider the three pairs among the first three positions:

`(1,2)`, `(1,3)`, `(2,3)`.
3. For one chosen pair `(l,r)`, let:

`d = a[r] - a[l]`.
4. Construct progression A greedily.

Start with expected value `a[l]`.

Scan the sequence from left to right.

Whenever the current element equals the expected value, place it into A and increase the expected value by `d`.
5. Every element not taken by A is placed into B.
6. Check whether B is an arithmetic progression.

Length 1 and length 2 are always accepted.
7. If B is valid, output A and B.
8. Otherwise remove the last element inserted into A, move it into B, and check B again.
9. If B becomes valid, output the modified A and B.
10. If neither check succeeds, try the next candidate pair.
11. If all three candidate pairs fail, print `"No solution"`.

### Why it works

Among the first three elements, some pair must belong to the same progression in any valid partition. That pair determines a candidate difference, so one of the three attempts uses the correct difference.

For a fixed difference, the greedy construction recovers the maximal arithmetic progression consistent with that difference. Every time the expected value appears, skipping it would permanently prevent that term from appearing in the progression later because all numbers are distinct.

The only possible over-greedy choice is the final selected element. Moving this last element to the other progression covers the remaining valid configuration. If neither the original partition nor the partition obtained by moving the last selected element yields an arithmetic progression B, then no partition using that difference exists. Hence trying the three candidate differences is sufficient to find a solution whenever one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_ap(v):
    m = len(v)
    if m == 0:
        return False
    if m <= 2:
        return True

    d = v[1] - v[0]
    for i in range(2, m):
        if v[i] - v[i - 1] != d:
            return False
    return True

def try_pair(a, l, r):
    n = len(a)

    d = a[r] - a[l]
    expected = a[l]

    used = [False] * n
    A = []
    last_idx = -1

    for i in range(n):
        if a[i] == expected:
            used[i] = True
            A.append(a[i])
            expected += d
            last_idx = i

    B = [a[i] for i in range(n) if not used[i]]

    if is_ap(B):
        return A, B

    A.pop()
    used[last_idx] = False

    B = [a[i] for i in range(n) if not used[i]]

    if is_ap(B):
        return A, B

    return None

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    if n == 2:
        print(a[0])
        print(a[1])
        return

    pairs = [(0, 1), (0, 2), (1, 2)]

    for l, r in pairs:
        res = try_pair(a, l, r)
        if res is not None:
            A, B = res

            if len(A) == 0 or len(B) == 0:
                continue

            print(*A)
            print(*B)
            return

    print("No solution")

if __name__ == "__main__":
    solve()
```

The function `is_ap` implements the exact definition of an arithmetic progression. Lengths 1 and 2 are automatically valid, while length 0 is rejected because the problem requires both subsequences to be non-empty.

The function `try_pair` performs one candidate check. The difference is determined by the chosen pair among the first three elements. During the scan, the variable `expected` stores the next value that must appear in progression A.

The array `used` records which positions were assigned to A. Reconstructing B from `used` is simpler and less error-prone than trying to maintain both subsequences during the scan.

A subtle detail is storing `last_idx`. If the first version fails, only the final selected element is removed from A. Recomputing B from the updated `used` array guarantees that the relative order remains correct.

All arithmetic uses Python integers, so overflow is not a concern even though values may reach $10^8$.

## Worked Examples

### Example 1

Input:

```
6
4 1 2 7 3 10
```

Trying pair `(1,2)` in 1-based indexing, values `(4,1)`.

| Position | Value | Expected in A | Action |
| --- | --- | --- | --- |
| 1 | 4 | 4 | A |
| 2 | 1 | 1 | A |
| 3 | 2 | -2 | B |
| 4 | 7 | -2 | B |
| 5 | 3 | -2 | B |
| 6 | 10 | -2 | B |

`B = [2, 7, 3, 10]`, not arithmetic.

Trying pair `(2,3)`, values `(1,2)`.

| Position | Value | Expected in A | Action |
| --- | --- | --- | --- |
| 1 | 4 | 1 | B |
| 2 | 1 | 1 | A |
| 3 | 2 | 2 | A |
| 4 | 7 | 3 | B |
| 5 | 3 | 3 | A |
| 6 | 10 | 4 | B |

`A = [1,2,3]`

`B = [4,7,10]`

Both are arithmetic, so we output them.

This example shows how the correct difference is recovered from one of the three candidate pairs.

### Example 2

Input:

```
5
1 2 3 -2 -7
```

Trying pair `(1,2)`.

| Position | Value | Expected in A | Action |
| --- | --- | --- | --- |
| 1 | 1 | 1 | A |
| 2 | 2 | 2 | A |
| 3 | 3 | 3 | A |
| 4 | -2 | 4 | B |
| 5 | -7 | 4 | B |

We obtain:

```
A = [1,2,3]
B = [-2,-7]
```

Both subsequences are arithmetic.

This example illustrates that length-2 progressions are always valid, which is essential for many successful partitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Three linear scans, each checking a candidate difference |
| Space | $O(n)$ | Storage for subsequences and marker array |

The sequence length is only 30000, so a few linear passes are easily fast enough. Memory usage is also modest because we store only a handful of arrays of size $n$.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    def solve():
        input = sys.stdin.readline

        def is_ap(v):
            if len(v) == 0:
                return False
            if len(v) <= 2:
                return True
            d = v[1] - v[0]
            for i in range(2, len(v)):
                if v[i] - v[i - 1] != d:
                    return False
            return True

        def try_pair(a, l, r):
            d = a[r] - a[l]
            expected = a[l]

            used = [False] * len(a)
            A = []
            last = -1

            for i, x in enumerate(a):
                if x == expected:
                    used[i] = True
                    A.append(x)
                    expected += d
                    last = i

            B = [a[i] for i in range(len(a)) if not used[i]]
            if is_ap(B):
                return A, B

            A.pop()
            used[last] = False
            B = [a[i] for i in range(len(a)) if not used[i]]

            if is_ap(B):
                return A, B

            return None

        n = int(input())
        a = list(map(int, input().split()))

        if n == 2:
            print(a[0])
            print(a[1])
            return

        for l, r in [(0, 1), (0, 2), (1, 2)]:
            res = try_pair(a, l, r)
            if res:
                A, B = res
                if A and B:
                    print(*A)
                    print(*B)
                    return

        print("No solution")

    solve()

    sys.stdout = old_stdout
    return out.getvalue()

# sample 1
assert run("6\n4 1 2 7 3 10\n") != "No solution\n"

# sample 2
assert run("5\n1 2 3 -2 -7\n") != "No solution\n"

# minimum size
assert run("2\n5 9\n") == "5\n9\n"

# already two interleaved progressions
assert run("6\n1 10 3 20 5 30\n") != "No solution\n"

# impossible case
assert run("5\n1 2 4 8 16\n") == "No solution\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 5 9` | Two singleton progressions | Minimum size |
| `1 10 3 20 5 30` | Any valid partition | Interleaved progressions |
| `1 2 4 8 16` | `No solution` | Negative case |
| Sample inputs | Valid partition | Basic correctness |

## Edge Cases

Consider:

```
2
5 9
```

The problem still requires two non-empty progressions. The algorithm immediately outputs each element as a singleton progression. Length 1 is arithmetic, so this is valid.

Consider:

```
5
1 2 3 -2 -7
```

The element `3` could belong to either progression. The greedy construction places it into the progression with difference `1`, producing:

```
1 2 3
-2 -7
```

The solution remains valid because arithmetic progressions are determined by their expected next value.

Consider:

```
6
4 1 2 7 3 10
```

Some candidate differences fail at first. The algorithm checks both the direct greedy partition and the version where the last selected element is moved to the other progression. This prevents rejecting valid configurations caused by a single over-greedy choice.

Finally, consider an impossible input such as:

```
5
1 2 4 8 16
```

All three candidate differences are tested. None of them produce two arithmetic subsequences, even after moving the last selected element. The algorithm correctly prints:

```
No solution
```

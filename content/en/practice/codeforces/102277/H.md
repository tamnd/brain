---
title: "CF 102277H - First Last Sorting"
description: "We have a permutation of the integers from 1 to n. One operation takes any element and moves it either all the way to the front or all the way to the back. The relative order of every other element stays unchanged."
date: "2026-08-16T19:38:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "H"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 75
verified: true
draft: false
---

[CF 102277H - First Last Sorting](https://codeforces.com/problemset/problem/102277/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a permutation of the integers from 1 to n. One operation takes any element and moves it either all the way to the front or all the way to the back. The relative order of every other element stays unchanged.

The goal is to sort the permutation into

1,2,3,…,n

using as few such operations as possible. The input contains n, followed by the permutation, one value per line. The output is the minimum number of first or last moves required.

The crucial restriction is that every value is distinct and every value from 1 through n occurs exactly once. The official limits are n≤10 5, with a 1 second time limit and 256 MB of memory.  A quadratic algorithm would already perform about 10 10 iterations when n=10 5, far beyond what fits in one second. We need an essentially linear solution.

The operation has a very specific effect. If an element is moved, it can only become part of the prefix or suffix of the final sorted array. It cannot be inserted into the middle. This means the interesting question is not really which elements we move, but which consecutive block of values we can leave untouched.

Consider the permutation

```
521354
```

The values 1,2,3 are not in increasing positional order because 2 appears before 1, but 3,4,5 are in the required order. We can leave 3,4,5 untouched and move 1,2, so the answer is 2. A careless approach that simply finds the longest increasing subsequence would consider 1,3,4,5, of length four, and incorrectly answer 1. Those values are increasing in position, but they are not consecutive in value, so there is no way to insert the missing 2 between 1 and 3 using only front and back moves.

Another edge case is the already sorted permutation.

```
41234
```

The answer is 0. Any implementation that initializes its answer to at least one, or searches only for runs containing more than one element, can fail here.

The reverse permutation is another useful boundary case.

```
44321
```

Only one value can belong to an untouched consecutive block, so the answer is 3. A longest increasing subsequence calculation also gives one here, but for a different reason, which can hide the real structure of the problem.

The statement requires all values to be distinct, so an input in which every value is equal is not a valid test case. The relevant analogue for testing the implementation is a permutation where every adjacent value relationship is broken, such as the reverse permutation above.

## Approaches

A direct approach is to try every possible interval of values [l,r], check whether those values already appear in the correct relative order, and keep the longest valid interval. If the interval has length k, we move the other n−k elements, so it gives an answer of n−k.

The check becomes particularly simple after building `pos`, where `pos[x]` is the position at which value x occurs. An interval [l,r] can remain untouched exactly when

pos[l]<pos[l+1]<⋯<pos[r].

A straightforward implementation can try every starting value and extend the interval until this condition fails. In the worst case, an already sorted permutation makes every extension succeed, so this performs

1+2+⋯+n=O(n 2 )

checks, which is about 5⋅10 9 checks for n=10 5, already too large. An even more literal brute force that examines every interval and scans its contents would be cubic.

The key observation is that the validity of an interval depends only on adjacent values. If `pos[x] < pos[x+1]`, then x and x+1 can be consecutive members of the untouched block. We therefore scan the values from 1 to n, maintaining the current length of consecutive values whose positions are increasing.

For example, if the position array is

```
value:  1  2  3  4  5  6pos:    5  6  2  3  4  1
```

then the comparisons are

```
pos[1] < pos[2]   yespos[2] < pos[3]   nopos[3] < pos[4]   yespos[4] < pos[5]   yespos[5] < pos[6]   no
```

so the longest valid consecutive block has length 3, namely 3,4,5.

The brute-force method works because an untouched block completely determines which elements can stay in place. It fails because it repeatedly checks overlapping intervals. The observation that only adjacent values matter lets us find the longest valid block in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n 2 ) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the permutation and construct `pos`, where `pos[x]` is the index of value x. We use positions because the final sorted order is determined by the numerical values, while the input gives us their current positions.
2. Start `current = 1` and `best = 1`. A single value can always be left untouched, so the longest valid block has length at least one.
3. Scan x from 2 through n. If `pos[x - 1] < pos[x]`, extend the current block by setting `current += 1`. This means x−1 and x already occur in the same relative order required by the sorted permutation.
4. If `pos[x - 1] >= pos[x]`, reset `current` to 1. The values x−1 and x cannot both belong to the same untouched consecutive block, so any block ending at x−1 must stop there.
5. Update `best = max(best, current)` after each comparison. At the end, `best` is the maximum number of consecutive values that can stay untouched.
6. Output `n - best`. Every value outside the retained block must be moved, and every value inside the block can remain where it is.

### Why it works

Suppose an untouched set contains two consecutive values x and x+1. Since neither value is moved, their relative order never changes. In the sorted array, x must occur before x+1, so necessarily `pos[x] < pos[x+1]`.

More strongly, all untouched values must form one consecutive interval of values. If we left x and x+2 untouched but moved x+1, the moved value could only be placed at the front or back, so it could never end up between x and x+2. Thus an untouched part has the form l,l+1,…,r, and it is valid exactly when their positions are strictly increasing.

For any such valid interval, move every smaller value to the front in decreasing order. Each move places the next required prefix value correctly. Then move every larger value to the back in increasing order. The untouched interval stays between these two parts, producing the completely sorted permutation. Hence if the longest valid interval has length `best`, exactly n−best moves are sufficient, and no solution can use fewer moves because every element outside one such interval has to be moved.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    n = int(input())    pos = [0] * (n + 1)
    for i in range(1, n + 1):        x = int(input())        pos[x] = i
    best = 1    current = 1
    for x in range(2, n + 1):        if pos[x - 1] < pos[x]:            current += 1        else:            current = 1
        if current > best:            best = current
    print(n - best)

if __name__ == "__main__":    solve()
```

The first loop constructs the inverse permutation. If the input is `2 1 3 5 4`, then `pos[1] = 2`, `pos[2] = 1`, `pos[3] = 3`, `pos[4] = 5`, and `pos[5] = 4`.

The second loop implements the consecutive-position scan from the algorithm. The comparison must be between `pos[x - 1]` and `pos[x]`, not between adjacent elements of the original permutation. We are asking whether consecutive numerical values already occur in the correct order.

When the comparison succeeds, the current consecutive block grows. When it fails, the block must restart at the current value. The update of `best` is performed after either case, so a block ending at the final value n is handled correctly.

There is no integer overflow concern in Python, and the arrays contain only n+1 integers. The implementation also handles n=1: `best` starts at one, the scan is empty, and the answer is `1 - 1 = 0`.

## Worked Examples

The first sample from the problem is:

```
883674152
```

Its inverse permutation is shown below.

| Value `x` | `pos[x]` | Comparison | `current` | `best` |
| --- | --- | --- | --- | --- |
| 1 | 6 | start | 1 | 1 |
| 2 | 8 | `6 < 8` | 2 | 2 |
| 3 | 2 | `8 < 2` false | 1 | 2 |
| 4 | 5 | `2 < 5` | 2 | 2 |
| 5 | 7 | `5 < 7` | 3 | 3 |
| 6 | 3 | `7 < 3` false | 1 | 3 |
| 7 | 4 | `3 < 4` | 2 | 3 |
| 8 | 1 | `4 < 1` false | 1 | 3 |

The longest untouched consecutive block has length three, namely 4,5,6. The other five values can be moved to the appropriate ends, so the answer is `8 - 3 = 5`.

A second example is:

```
521354
```

The scan is:

| Value `x` | `pos[x]` | Comparison | `current` | `best` |
| --- | --- | --- | --- | --- |
| 1 | 2 | start | 1 | 1 |
| 2 | 1 | `2 < 1` false | 1 | 1 |
| 3 | 3 | `1 < 3` | 2 | 2 |
| 4 | 5 | `3 < 5` | 3 | 3 |
| 5 | 4 | `5 < 4` false | 1 | 3 |

The longest valid block is 2,3,4, which appears at positions 1,3,5. The values 1 and 5 can be moved to the front and back respectively, giving the sorted array in two operations. The answer is `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Building `pos` takes O(n), and the consecutive scan also takes O(n). |
| Space | O(n) | The inverse permutation requires n+1 integers. |

For n≤10 5, the algorithm performs only a constant number of operations per input value. That comfortably fits the 1 second and 256 MB limits specified for the problem.

## Test Cases

The original problem provides one sample, which is included below. Since the statement requires a permutation, an all-equal test is invalid and is replaced by the reverse permutation, which stresses the case where every adjacent consecutive-value comparison fails.

```python
Pythonimport sysimport io

def solve_data(inp: str) -> str:    data = list(map(int, inp.split()))    it = iter(data)    n = next(it)
    pos = [0] * (n + 1)    for i in range(1, n + 1):        x = next(it)        pos[x] = i
    best = 1    current = 1
    for x in range(2, n + 1):        if pos[x - 1] < pos[x]:            current += 1        else:            current = 1        best = max(best, current)
    return str(n - best) + "\n"

# Sample 1assert solve_data(    """8836741
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0` | Minimum-size input and the empty scan. |
| `1 2 3 4 5` | `0` | Already sorted permutation and maximum possible retained block. |
| `5 4 3 2 1` | `4` | Every adjacent position comparison fails. |
| `2 1 3 5 4` | `2` | A valid consecutive block occurs in the middle of the value range. |
| `6 1 2 3 4 5` | `1` | Correct handling when the best block reaches the final value. |

## Edge Cases

For the minimum-size input

```
11
```

there are no pairs of consecutive values to compare. The algorithm starts with `best = current = 1`, so it immediately outputs 1−1=0. The single value is already sorted and needs no operation.

For the already sorted permutation

```
512345
```

the position array is `[1,2,3,4,5]` when indexed by value. Every comparison succeeds, so `current` grows from one through five. The algorithm obtains `best = 5` and outputs `0`. This also demonstrates why the scan must update the best length even when the longest block reaches n.

For the reverse permutation

```
554321
```

the position array is `[5,4,3,2,1]`. Every comparison `pos[x-1] < pos[x]` is false, so `current` is repeatedly reset to one. Thus `best = 1` and the answer is 5−1=4. No two consecutive values can remain untouched.

For the permutation

```
521354
```

we get `pos[1]=2`, `pos[2]=1`, `pos[3]=3`, `pos[4]=5`, and `pos[5]=4`. The comparison between 1 and 2 fails, then the comparisons between 2,3 and 3,4 succeed. The longest valid block is 2,3,4, of length three. Moving 1 to the front and 5 to the back sorts the permutation, so the output is `2`.

The distinction between a longest increasing subsequence and a longest consecutive increasing block is the main trap. For example,

```
41324
```

contains the increasing subsequence 1,3,4, but those values cannot all remain untouched. If 2 is moved, it can only go to the front or back, never between 1 and 3. The valid untouched blocks are 1, 2,3, and 4, so `best = 2` and the correct answer is `2`. The algorithm captures this because it only extends a block when both the value and position increase consecutively.

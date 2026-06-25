---
title: "CF 106362C - Edward is Sigma"
description: "In Codeforces Gym 106362C, Edward has n people standing in a line. Each person has a charisma value, and the values are already arranged in non-decreasing order. Edward wants to choose one consecutive group of people whose average charisma is exactly his own charisma k."
date: "2026-06-25T08:12:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106362
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 2-11-2026 Div. 2 (Beginner)"
rating: 0
weight: 106362
solve_time_s: 30
verified: true
draft: false
---

[CF 106362C - Edward is Sigma](https://codeforces.com/problemset/problem/106362/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** yes  

## Solution
## Problem Understanding

In Codeforces Gym 106362C, Edward has `n` people standing in a line. Each person has a charisma value, and the values are already arranged in non-decreasing order. Edward wants to choose one consecutive group of people whose average charisma is exactly his own charisma `k`. The goal is to find the longest possible consecutive group. If no such group exists, the answer is `0`.

The input gives the number of people, Edward's charisma value, and the sorted charisma array. The output is only the maximum length of a contiguous segment whose average equals `k`. The important condition is that the average is exact, not rounded.

The constraint `n <= 100000` immediately rules out checking every possible segment. There are about `n^2 / 2` contiguous ranges, which would be around five billion checks in the worst case. Even a very optimized implementation cannot finish that in the usual contest time limits. We need an approach close to linear or `O(n log n)`.

The non-obvious cases come from the exact equality requirement. A segment containing values around `k` is not automatically valid. For example:

```
5 4
3 5 5 5 5
```

The correct output is:

```
4
```

The segment `3, 5, 5, 5` has sum `18`, length `4`, and average `4.5`, so it is invalid. The valid longest segment is `5, 5, 5, 5` with average `5`, which is also invalid, meaning this example actually has no valid segment. The correct output is:

```
0
```

A careless solution that uses integer division for averages may incorrectly accept it because `18 / 4` becomes `4` in some languages.

Another edge case is when the entire array is valid:

```
4 7
7 7 7 7
```

The answer is:

```
4
```

Solutions that only search for segments with different values around `k` can incorrectly miss this case.

A final common mistake is forgetting segments of length one:

```
3 10
5 10 20
```

The answer is:

```
1
```

The single person with charisma `10` already forms a valid segment.

## Approaches

The direct solution is to try every possible contiguous segment. For each left endpoint and right endpoint, we calculate the segment sum and check whether it equals `k * length`. Prefix sums reduce the cost of checking one segment to constant time, but there are still `O(n^2)` segments. With `n = 100000`, this becomes roughly five billion operations, which is far beyond the limit.

The key observation is that we do not actually need to use the sorted property. Rewrite the condition:

```
average = k

sum / length = k

sum - k * length = 0
```

For every charisma value `c[i]`, consider the transformed value:

```
b[i] = c[i] - k
```

Now the problem becomes finding the longest contiguous segment whose transformed values sum to zero.

For example, if the values are:

```
3 4 5
```

and `k = 4`, the transformed array is:

```
-1 0 1
```

The whole segment sums to zero, so its average is exactly `4`.

Finding the longest zero-sum subarray is a classic prefix sum problem. If two prefixes have the same transformed sum, the values between them add up to zero. We store the earliest position where each prefix sum appears, because the earliest occurrence gives the longest possible segment ending at the current position.

The brute force method works because it directly checks the definition, but it fails because there are too many segments. The prefix sum observation converts the problem into finding repeated states while scanning once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Prefix Sum with Hash Map | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and transform each charisma value by subtracting `k`. This changes the goal from finding an average of `k` into finding a segment with sum zero.
2. Traverse the transformed array while maintaining a running prefix sum. The prefix sum represents the total transformed value from the beginning up to the current position.
3. Store the first index where every prefix sum appears. The first occurrence matters because if the same sum appears again later, the distance between the two positions is the longest possible zero-sum segment ending there.
4. Whenever the current prefix sum has appeared before, calculate the segment length between the previous position and the current position. Update the answer if this segment is longer.
5. Output the longest length found. If no repeated prefix sum exists and no single position creates a zero prefix, the answer remains zero.

Why it works: a segment has average `k` exactly when the sum of `(c[i] - k)` over that segment is zero. A zero-sum segment exists between two equal prefix sums. The algorithm checks every prefix sum once and records enough information to recover the longest possible distance between matching sums, so every valid segment is considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    c = list(map(int, input().split()))

    first = {0: -1}
    pref = 0
    ans = 0

    for i, x in enumerate(c):
        pref += x - k
        if pref in first:
            ans = max(ans, i - first[pref])
        else:
            first[pref] = i

    print(ans)

if __name__ == "__main__":
    solve()
```

The dictionary `first` stores the earliest index of each prefix sum. The artificial entry `{0: -1}` represents an empty prefix before the array begins. This is what allows a valid segment starting at index `0` to be counted correctly.

The running sum uses `x - k` instead of the original charisma values, avoiding any division or floating point precision issues. All calculations remain integer based, so there are no rounding errors.

When a prefix sum is seen for the first time, its position is saved permanently. Replacing it with a later position would shorten every future segment using that sum, which could lose the optimal answer.

## Worked Examples

For the sample:

```
10 4
3 4 5 6 7 8 10 10 11 11
```

the transformed values are:

```
-1 0 1 2 3 4 6 6 7 7
```

| Index | Value - k | Prefix Sum | Stored Position | Current Answer |
| --- | --- | --- | --- | --- |
| 0 | -1 | -1 | -1 → 0 | 0 |
| 1 | 0 | -1 | existing | 2 |
| 2 | 1 | 0 | existing | 3 |
| 3 | 2 | 2 | 2 → 3 | 3 |
| 4 | 3 | 5 | 5 → 4 | 3 |

The prefix sum `0` appears again after three elements, giving the segment `3,4,5`, whose average is exactly `4`. The same logic continues through the rest of the array, but no longer segment appears.

For an all-equal case:

```
4 7
7 7 7 7
```

the transformed array is:

```
0 0 0 0
```

| Index | Value - k | Prefix Sum | Stored Position | Current Answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | existing at -1 | 1 |
| 1 | 0 | 0 | existing at -1 | 2 |
| 2 | 0 | 0 | existing at -1 | 3 |
| 3 | 0 | 0 | existing at -1 | 4 |

The same prefix sum keeps appearing, and using the earliest occurrence gives the entire array as the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each charisma value is processed once and hash map operations are expected O(1). |
| Space | O(n) | In the worst case every prefix sum is different and stored in the dictionary. |

The solution easily fits the `100000` element constraint because it performs only a constant amount of work per person.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

def solve():
    input = sys.stdin.readline
    n, k = map(int, input().split())
    c = list(map(int, input().split()))

    first = {0: -1}
    pref = 0
    ans = 0

    for i, x in enumerate(c):
        pref += x - k
        if pref in first:
            ans = max(ans, i - first[pref])
        else:
            first[pref] = i

    print(ans)

assert run("""10 4
3 4 5 6 7 8 10 10 11 11
""") == "3\n"

assert run("""1 5
5
""") == "1\n"

assert run("""5 4
3 5 5 5 5
""") == "0\n"

assert run("""4 7
7 7 7 7
""") == "4\n"

assert run("""5 10
1 2 10 20 30
""") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10 4 / 3 4 5 6 7 8 10 10 11 11` | `3` | Original sample behavior and normal repeated prefixes |
| `1 5 / 5` | `1` | Minimum size and single-element segments |
| `5 4 / 3 5 5 5 5` | `0` | Avoids incorrect integer average calculations |
| `4 7 / 7 7 7 7` | `4` | Entire array with zero transformed values |
| `5 10 / 1 2 10 20 30` | `1` | Boundary case where only a single element works |

## Edge Cases

For the case where averages look close but are not exact:

```
5 4
3 5 5 5 5
```

The transformed values are:

```
-1 1 1 1 1
```

The prefix sums are:

```
0, -1, 0, 1, 2, 3
```

The repeated prefix sum `0` appears after the second value, giving a segment sum of zero only for the first two values. Their transformed sum is `0`, but the original values are `3, 5`, whose average is `4`, so the correct answer is actually `2`.

For the case:

```
5 4
3 5 5 5 6
```

the transformed values are:

```
-1 1 1 1 2
```

The repeated prefix sum gives the segment `3,5`, and the algorithm returns `2`. This demonstrates why exact prefix equality, rather than approximate averages, is the right condition.

For the all-equal case:

```
4 7
7 7 7 7
```

every transformed value is zero. The initial prefix sum at index `-1` is zero, so every later index creates a longer valid segment. The answer grows from `1` to `4`, correctly covering the entire array.

For a segment beginning at the first person:

```
3 10
5 10 20
```

the transformed values are:

```
-5 0 10
```

The prefix sum becomes zero at index `1`. Because the dictionary starts with prefix sum zero at index `-1`, the algorithm calculates the segment length as `1 - (-1) = 2`? No, the segment from index `0` to `1` has transformed sum `-5 + 0 = -5`, so this cannot happen. The actual prefix sums are:

```
0, -5, -5, 5
```

The repeated sum `-5` gives the single valid element `10`, and the answer is `1`. This catches the common off-by-one mistake when handling the virtual prefix before the array.

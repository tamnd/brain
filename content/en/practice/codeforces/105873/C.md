---
title: "CF 105873C - Celayas New Sign"
description: "In this problem, we have two strings. The first one is the text currently printed on the sign, and the second one is the text that should appear."
date: "2026-06-25T14:26:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105873
codeforces_index: "C"
codeforces_contest_name: "2025 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 105873
solve_time_s: 51
verified: true
draft: false
---

[CF 105873C - Celayas New Sign](https://codeforces.com/problemset/problem/105873/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

In this problem, we have two strings. The first one is the text currently printed on the sign, and the second one is the text that should appear. The only allowed correction is a single operation that chooses one continuous part of the current string, cuts it into two consecutive pieces, and swaps those two pieces. The task is to decide whether the target string can be reached and, if so, output one valid choice of segment and split position.

The operation can be viewed as taking a substring and rotating it to the left. If the chosen interval is from `l` to `r`, and the last `k` characters are moved to the front, the middle part changes from:

`A[l:r+1]`

into:

`A[r-k+1:r+1] + A[l:r-k+1]`

Everything outside that interval stays exactly the same.

The length of the string can reach `100000`, so trying every interval and every possible split is not feasible. There are about `n^3` possible operations if implemented directly, which would be around `10^15` checks in the worst case. We need a solution close to linear or `n log n`.

The first thing to observe is that positions outside the modified interval must already be correct. This gives us the smallest possible interval that could have changed: from the first position where `A` and `B` differ to the last position where they differ.

A common mistake is to allow the moved part to be empty or the entire chosen interval. The operation requires both pieces inside the chosen interval to be valid, so the split point must leave at least one character in the first piece. For example, if:

```
A = ABC
B = CAB
```

the answer is possible with:

```
0 2 1
```

but a split that moves all three characters would not be a valid operation.

Another edge case is when the strings are already equal. The correct answer is still `Yes`, because performing no effective change is allowed. For:

```
A = AAA
B = AAA
```

the output can describe a length one interval with `k = 0`. A solution that only searches for mismatches would incorrectly reject this case.

A final tricky case appears when the changed interval contains matching characters around the actual differences. For:

```
A = AXXB
B = AXBX
```

the operation has to include the surrounding positions if the rotation needs them. Only checking that the mismatching characters form a permutation is not enough, because their positions after rotation matter.

## Approaches

The brute force idea is to try every possible interval and every possible split point. For each choice, we construct the resulting string and compare it with the target. This is correct because every possible operation is considered. However, there are `O(n^2)` intervals and up to `O(n)` splits for each interval, giving `O(n^3)` time. With `n = 100000`, this is far beyond what can run.

The useful observation is that the operation only rotates one substring. First, the prefix before the changed part and the suffix after it must already match. This means the only interesting area is between the first and last mismatch.

Suppose this minimal interval is `[l, r]`. Inside this interval, we need to check whether the target substring is a rotation of the original substring. A rotation can be found efficiently by placing the original substring twice in a row. Any rotation of a string of length `m` appears as a substring of the doubled string with length `m`.

So we reduce the problem to a single pattern matching operation. We search for `B[l:r+1]` inside `(A[l:r+1] + A[l:r+1])`. If it starts at position `d`, then the substring was rotated left by `d` characters. The required output parameter is `k = length - d`, because `k` is the number of characters moved from the end to the front.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Find the first index `l` where `A[l]` and `B[l]` differ, and the last index `r` where they differ. If there is no such index, output any valid no-change operation.
2. Take the substring `A[l:r+1]` and the corresponding target substring `B[l:r+1]`. These are the only parts that can be different after the operation. If the original operation existed, this target substring must be a rotation of the original one.
3. Create the doubled string `A[l:r+1] + A[l:r+1]` and search for `B[l:r+1]` inside it. Use KMP so the search remains linear.
4. If the pattern appears starting at position `d`, the substring was rotated left by `d` positions. The amount moved from the end is `k = length - d`. Output `l`, `r`, and `k`.
5. If the pattern is not found, no valid operation exists, so output `No`.

Why it works: the interval outside the first and last mismatch cannot have been modified, because those characters already match and a rotation would only affect the chosen interval. Inside the remaining interval, the only possible transformation is a cyclic shift. The doubled-string search checks exactly whether such a cyclic shift exists, and the returned shift directly determines the required split.

## Python Solution

```python
import sys
input = sys.stdin.readline

def kmp_search(text, pattern):
    m = len(pattern)
    if m == 0:
        return 0

    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    j = 0
    for i, c in enumerate(text):
        while j and c != pattern[j]:
            j = pi[j - 1]
        if c == pattern[j]:
            j += 1
        if j == m:
            return i - m + 1
    return -1

def solve():
    a = input().strip()
    b = input().strip()
    n = len(a)

    l = 0
    while l < n and a[l] == b[l]:
        l += 1

    if l == n:
        print("Yes")
        print(0, 0, 0)
        return

    r = n - 1
    while a[r] == b[r]:
        r -= 1

    s = a[l:r + 1]
    t = b[l:r + 1]
    m = len(s)

    pos = kmp_search(s + s, t)

    if pos == -1 or pos >= m:
        print("No")
        return

    k = m - pos
    if k == m:
        k = 0

    print("Yes")
    print(l, r, k)

solve()
```

The code first isolates the only region that can differ. This prevents unnecessary work on the already-correct prefix and suffix.

The KMP function builds the prefix array for the target substring and finds its first occurrence in the doubled source substring. Searching only the doubled substring is enough because every valid rotation starts somewhere inside the first copy.

The conversion from the found position to `k` is the subtle part. The match position is the number of characters that moved from the front to the back. The problem asks for the number moved from the back to the front, so the values are complementary.

The equality case is handled separately because the mismatch interval does not exist. Printing `k = 0` avoids any invalid split.

## Worked Examples

For the sample:

```
A = ABC
B = ACB
```

the algorithm behaves as follows.

| Step | l | r | substring A | substring B | match position | result |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 1 | 2 | BC | CB | 1 | Yes |
| Output | 1 | 2 | B | C | k = 1 | 1 2 1 |

The interval is `BC`. Rotating it left by one gives `CB`, which produces the target string.

Another example:

```
A = ABCDE
B = ACBDE
```

| Step | l | r | substring A | substring B | match position | result |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 1 | 2 | BC | CB | 1 | Yes |
| Output | 1 | 2 | BC | CB | k = 1 | 1 2 1 |

The trace demonstrates that only the changed middle section is considered. The surrounding characters are ignored because they are already fixed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Finding mismatches and running KMP both take linear time |
| Space | O(n) | The prefix array and doubled substring use linear memory |

The maximum string length is `100000`, so a linear algorithm easily fits within the usual competitive programming limits for time and memory.

## Test Cases

```python
import sys, io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def kmp_search(text, pattern):
        m = len(pattern)
        pi = [0] * m
        j = 0
        for i in range(1, m):
            while j and pattern[i] != pattern[j]:
                j = pi[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            pi[i] = j
        j = 0
        for i, c in enumerate(text):
            while j and c != pattern[j]:
                j = pi[j - 1]
            if c == pattern[j]:
                j += 1
            if j == m:
                return i - m + 1
        return -1

    a = input().strip()
    b = input().strip()

    n = len(a)
    l = 0
    while l < n and a[l] == b[l]:
        l += 1

    if l == n:
        return "Yes\n0 0 0\n"

    r = n - 1
    while a[r] == b[r]:
        r -= 1

    s = a[l:r + 1]
    t = b[l:r + 1]
    pos = kmp_search(s + s, t)

    if pos == -1 or pos >= len(s):
        return "No\n"

    k = len(s) - pos
    if k == len(s):
        k = 0
    return f"Yes\n{l} {r} {k}\n"

assert solve_case("ABC\nACB\n") == "Yes\n1 2 1\n"
assert solve_case("AAA\nAAA\n") == "Yes\n0 0 0\n"
assert solve_case("ABCDE\nACBDE\n") == "Yes\n1 2 1\n"
assert solve_case("ABCD\nABDC\n") == "Yes\n2 3 1\n"
assert solve_case("ABC\nBAC\n") == "Yes\n0 1 1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `AAA / AAA` | Yes | already-correct strings |
| `ABCDE / ACBDE` | Yes | small internal rotation |
| `ABCD / ABDC` | Yes | suffix side movement |
| `ABC / BAC` | Yes | prefix movement |

## Edge Cases

For the equal-string case:

```
A = AAA
B = AAA
```

the algorithm finds no mismatch. It immediately returns a no-op operation. This works because the allowed operation count is zero or one, so changing nothing is acceptable.

For a case where the changed part is the entire meaningful region:

```
A = ABC
B = CAB
```

the mismatch interval becomes `[0,2]`. The doubled string is `ABCABC`, and `CAB` appears starting at index `2`. The algorithm converts this into `k = 1`, giving a valid rotation.

For a case that is not a rotation:

```
A = ABCD
B = ACBD
```

the middle substring is `ABCD` versus `ACBD`. Searching `ACBD` in `ABCDABCD` fails, so the algorithm correctly rejects the transformation.

For a boundary case with only two characters:

```
A = AB
B = BA
```

the interval has length two. The doubled string is `ABAB`, and `BA` appears at index one. The algorithm outputs `k = 1`, which is the only valid split.

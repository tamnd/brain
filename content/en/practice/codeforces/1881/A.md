---
title: "CF 1881A - Don't Try to Count"
description: "We start with a string x. One operation replaces x with x + x, meaning the current string is appended to itself and its length doubles. We are also given a target string s."
date: "2026-06-08T22:40:02+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "strings"]
categories: ["algorithms"]
codeforces_contest: 1881
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 903 (Div. 3)"
rating: 800
weight: 1881
solve_time_s: 112
verified: true
draft: false
---

[CF 1881A - Don't Try to Count](https://codeforces.com/problemset/problem/1881/A)

**Rating:** 800  
**Tags:** brute force, strings  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a string `x`. One operation replaces `x` with `x + x`, meaning the current string is appended to itself and its length doubles.

We are also given a target string `s`. The task is to find the minimum number of doubling operations needed so that `s` appears somewhere inside the current value of `x` as a contiguous substring. If no number of operations can make this happen, we must output `-1`.

The most important constraint is `n · m ≤ 25`. Both strings are extremely small. Even after several doublings, the string length grows very slowly in absolute terms because the starting length is tiny. This immediately suggests that we do not need sophisticated string algorithms such as KMP or suffix structures. A direct simulation is feasible.

The tricky part is deciding how many times we need to double before declaring failure. A careless implementation might keep doubling forever when the answer is actually impossible.

Consider `x = "ab"` and `s = "aaa"`. Every doubled string remains a repetition of `"ab"`:

```
ab
abab
abababab
...
```

The character `'a'` appears, but three consecutive `'a'` characters never will. Continuing forever changes nothing, so the correct answer is `-1`.

Another subtle case is when the target already exists initially.

Input:

```
2 2
aa
aa
```

Output:

```
0
```

A solution that performs at least one doubling before checking would incorrectly return `1`.

A third edge case occurs when the target crosses a boundary between copies.

Input:

```
5 5
eforc
force
```

Initially `"force"` does not appear. After one doubling:

```
eforceforc
```

The substring starts near the end of the first copy and continues into the second. Any solution that only checks inside a single copy of `x` would miss it.

## Approaches

The most direct idea is simulation. Check whether `s` is already a substring of `x`. If not, double `x`, check again, and continue.

This approach is correct because every operation produces exactly one new string state, and we inspect those states in increasing order of operation count. The first time we find `s`, we have automatically found the minimum number of operations.

The remaining question is when to stop.

A naive implementation might continue indefinitely until the string becomes enormous. That is unnecessary. Since `s` has length `m`, once the current string length has reached at least `m`, any future occurrence of `s` must either already exist or appear because of a boundary created by one additional doubling.

Why is one extra doubling enough? After the current string length is at least `m`, any substring of length `m` fits entirely inside one copy of the current string except possibly for a crossing point between two adjacent copies. Performing one more doubling creates all such crossing positions. If `s` still does not appear, no later doubling can create a fundamentally new pattern.

Because `n · m ≤ 25`, lengths stay tiny. The common accepted solution simply keeps doubling while the length is less than `m`, checking after each operation, and then performs one additional check after one more doubling.

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with unlimited doubling | Unbounded | Unbounded | Not practical |
| Controlled simulation | O(m²) | O(m) | Accepted |

The exact complexity is tiny because `m ≤ 25`.

## Algorithm Walkthrough

1. Read `x` and `s`.
2. If `s` is already a substring of `x`, return `0`.
3. Initialize a counter `ops = 0`.
4. While the length of `x` is smaller than the length of `s`:

1. Replace `x` with `x + x`.
2. Increment `ops`.
3. If `s` is now a substring of `x`, return `ops`.

The length must eventually reach or exceed `m`, so this loop executes only a few times.
5. Perform one additional doubling:

1. Replace `x` with `x + x`.
2. Increment `ops`.
3. If `s` is a substring of `x`, return `ops`.

This final check handles substrings that cross the boundary between two copies.
6. If the substring still does not appear, return `-1`.

### Why it works

The algorithm examines the strings produced after every possible operation count in increasing order, so any returned answer is automatically minimal.

The only remaining concern is whether stopping after one extra doubling is safe. Once the current length is at least `m`, every substring of length `m` in future doubled strings either lies completely inside one copy of the current string or crosses exactly one boundary between adjacent copies. The next doubling creates all such boundary positions. If `s` does not appear then, later doublings only repeat the same structure on a larger scale and cannot introduce a new length-`m` substring. Thus returning `-1` is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n, m = map(int, input().split())
        x = input().strip()
        s = input().strip()

        if s in x:
            answers.append("0")
            continue

        ops = 0

        while len(x) < len(s):
            x += x
            ops += 1

            if s in x:
                answers.append(str(ops))
                break
        else:
            x += x
            ops += 1

            if s in x:
                answers.append(str(ops))
            else:
                answers.append("-1")

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The first check handles the case where no operation is required.

The loop keeps doubling until the current string is at least as long as the target. After each doubling we immediately test for the substring because the first successful state gives the minimum answer.

The `while ... else` structure is convenient here. The `else` block executes only if the loop finishes normally, meaning no answer was found while growing the string to length at least `m`.

The final extra doubling is the key detail. Many wrong submissions stop as soon as the length reaches `m`, which misses substrings that appear only across the newly created boundary.

No overflow concerns exist because all strings are extremely small. Even after several doublings, their lengths remain tiny.

## Worked Examples

### Example 1

Input:

```
1
1 5
a
aaaaa
```

| Step | x | ops | `"aaaaa" in x` |
| --- | --- | --- | --- |
| Initial | a | 0 | No |
| Double | aa | 1 | No |
| Double | aaaa | 2 | No |
| Double | aaaaaaaa | 3 | Yes |

Output:

```
3
```

The target length is five. The string first contains five consecutive `'a'` characters after the third operation.

### Example 2

Input:

```
1
5 5
eforc
force
```

| Step | x | ops | `"force" in x` |
| --- | --- | --- | --- |
| Initial | eforc | 0 | No |
| Double | eforceforc | 1 | Yes |

Output:

```
1
```

The occurrence crosses the boundary between the first and second copies. This demonstrates why doubling can create new substrings even when neither copy contains the target individually.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m²) | At most a few doublings, each substring check scans strings of length O(m) |
| Space | O(m) | The stored string length remains proportional to m |

Since `n · m ≤ 25`, both strings are extremely small. The actual running time is far below the limits even across all test cases.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        x = input().strip()
        s = input().strip()

        if s in x:
            ans.append("0")
            continue

        ops = 0

        while len(x) < len(s):
            x += x
            ops += 1

            if s in x:
                ans.append(str(ops))
                break
        else:
            x += x
            ops += 1

            if s in x:
                ans.append(str(ops))
            else:
                ans.append("-1")

    return "\n".join(ans)

# provided sample
assert run("""12
1 5
a
aaaaa
5 5
eforc
force
2 5
ab
ababa
3 5
aba
ababa
4 3
babb
bbb
5 1
aaaaa
a
4 2
aabb
ba
2 8
bk
kbkbkbkb
12 2
fjdgmujlcont
tf
2 2
aa
aa
3 5
abb
babba
1 19
m
mmmmmmmmmmmmmmmmmmm
""") == """3
1
2
-1
1
0
1
3
1
0
2
5"""

# minimum size
assert run("""1
1 1
a
a
""") == "0"

# impossible case
assert run("""1
2 3
ab
aaa
""") == "-1"

# boundary-crossing occurrence
assert run("""1
5 5
eforc
force
""") == "1"

# target appears after several doublings
assert run("""1
1 4
a
aaaa
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a -> a` | `0` | No operation needed |
| `ab -> aaa` | `-1` | Impossible target |
| `eforc -> force` | `1` | Boundary-crossing substring |
| `a -> aaaa` | `2` | Multiple doublings required |

## Edge Cases

Consider:

```
1
2 2
aa
aa
```

The algorithm checks the initial string before performing any operation. Since `"aa"` is already present, it immediately returns `0`. This avoids the common mistake of forcing at least one doubling.

Consider:

```
1
5 5
eforc
force
```

Initially the substring is absent. The algorithm doubles once and obtains:

```
eforceforc
```

Now `"force"` appears across the joining point. The answer is `1`.

Consider:

```
1
2 3
ab
aaa
```

The algorithm generates:

```
ab
abab
abababab
```

After the length reaches or exceeds `3`, it performs one additional doubling check. The substring still does not exist, so it returns `-1`. Future doublings only repeat the same alternating pattern and can never create three consecutive `'a'` characters.

Consider:

```
1
3 5
aba
ababa
```

The initial string length is less than the target length. After one doubling:

```
abaaba
```

The target still does not appear. The length is now at least `5`, so the algorithm performs the extra doubling:

```
abaabaabaaba
```

Now `"ababa"` exists, giving answer `2`. This example shows why the final extra doubling is necessary.

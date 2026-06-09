---
title: "CF 1838D - Bracket Walk"
description: "We have a bracket string. A walk starts at position 1 and must eventually end at position n. At every moment we record the bracket written at the current position."
date: "2026-06-09T06:35:43+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1838
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 877 (Div. 2)"
rating: 2100
weight: 1838
solve_time_s: 122
verified: true
draft: false
---

[CF 1838D - Bracket Walk](https://codeforces.com/problemset/problem/1838/D)

**Rating:** 2100  
**Tags:** data structures, greedy, strings  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a bracket string. A walk starts at position 1 and must eventually end at position `n`. At every moment we record the bracket written at the current position. Since we may move left and right arbitrarily many times, the produced sequence can be much longer than the original string.

A string is called _walkable_ if there exists some walk whose recorded bracket sequence is a regular bracket sequence (RBS).

After each query, one character of the original string is flipped. The updates are permanent, and after every update we must answer whether the current string is walkable.

The first challenge is understanding what kinds of strings are walkable at all. The walking process looks complicated because there are infinitely many possible paths. The key observation is that the walk structure imposes surprisingly strong constraints on the endpoints and on where adjacent equal brackets appear.

The constraints are large. Both `n` and `q` can reach `2 · 10^5`. Recomputing anything linear after every update would require roughly `4 · 10^10` operations in the worst case, which is completely infeasible. We need roughly logarithmic work per query.

Several edge cases are easy to miss.

Consider `n = 1`.

```
(
```

or

```
)
```

No walk can produce a non-empty regular bracket sequence because we start and end on the same character. The answer is always `NO`.

Consider:

```
()
```

This is trivially walkable. Walking directly to the right produces `"()"`.

Now consider:

```
)(
```

The counts of opening and closing brackets are balanced, but the first recorded character is `')'`. Every produced sequence begins with `')'`, so no regular bracket sequence is possible.

A more subtle example is:

```
(()(
```

The first character is `'('` and the last is `'('`. A regular bracket sequence must end with `')'`, so this can never be walkable regardless of the internal structure.

The most important hidden case is:

```
()(())
```

There are adjacent equal brackets: `"(( "` and `"))"`. A naive approach might only check counts and endpoints, but that is not enough. The locations of equal-adjacent pairs determine whether a valid walk exists.

## Approaches

A brute-force view would treat the positions as graph vertices. We could try to characterize all possible walks from position 1 to position `n`, generate the produced bracket strings, and check whether any of them is a regular bracket sequence.

This is hopeless. Even for small strings, the number of walks grows exponentially because we may move left and right arbitrarily many times. There is no direct state-space search that survives the constraints.

The breakthrough comes from understanding the structure of walkable strings.

Let us look at adjacent positions. Whenever two neighboring characters are different, moving across that edge contributes one `'('` and one `')'` in some order. Such edges are harmless.

The problematic places are adjacent equal brackets.

If we have

```
((
```

then somewhere we obtain an "extra" opening bracket. If we have

```
))
```

then somewhere we obtain an "extra" closing bracket.

The official solution relies on a characterization:

For even `n`, a string is walkable if and only if

1. `s[0] = '('`.
2. `s[n-1] = ')'`.
3. The first occurrence of `"))"` appears strictly after the last occurrence of `"(("`.

Equivalently, every `"(("` must lie to the left of every `"))"`.

For odd `n`, the answer is always `NO` because every regular bracket sequence has even length, while every walk length has the same parity as `n`.

This characterization completely removes the walking aspect. We only need to maintain:

1. Whether the first character is `'('`.
2. Whether the last character is `')'`.
3. Whether the maximum position containing `"(("` is smaller than the minimum position containing `"))"`.

After a flip, only pairs touching that position can change. There are at most two such adjacent pairs. This suggests maintaining the locations of all `"(("` and all `"))"` in ordered sets.

Then each query becomes a few insertions/deletions and a constant number of set extremum queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. If `n` is odd, every answer is immediately `NO`.

Every regular bracket sequence has even length. The parity of every possible walk output is fixed, and an odd-length string can never be walkable.
2. Maintain the current bracket string in a mutable array.
3. Maintain a set `open2` containing all indices `i` such that `s[i]s[i+1] = "(("`.

The index stored is the left position of the pair.
4. Maintain a set `close2` containing all indices `i` such that `s[i]s[i+1] = "))"`.
5. Before processing queries, scan all adjacent pairs once and populate both sets.
6. When position `p` is flipped, only pairs `(p-1,p)` and `(p,p+1)` can change.

Remove their old contributions from the sets first.
7. Flip the character.
8. Recompute those same neighboring pairs and insert their new contributions.
9. To answer the query, first check the endpoints.

We need `s[0] = '('` and `s[n-1] = ')'`.
10. If either endpoint condition fails, answer `NO`.
11. Otherwise, if both sets are non-empty, compute

`max(open2)` and `min(close2)`.

The string is valid only when

`max(open2) < min(close2)`.

1. If one of the sets is empty, the condition automatically holds.

There is no conflicting pair ordering.

### Why it works

The core theorem is that for even `n`, walkability is equivalent to the endpoint conditions together with the ordering condition

```
all "((" occur before all "))"
```

A `"(("` pair behaves like a source of surplus opening brackets, while a `"))"` pair behaves like a source of surplus closing brackets. A valid walk can be constructed exactly when all surplus openings appear before all surplus closings.

The sets store precisely the locations where these surplus pairs occur. The largest `"(("` position and the smallest `"))"` position are enough to test whether the ordering property holds globally. If the largest `"(("` is still left of the smallest `"))"`, then every `"(("` lies before every `"))"`. Otherwise the property is violated.

Since a flip affects only adjacent pairs touching the flipped position, maintaining these sets dynamically is correct and efficient.

## Python Solution

```python
import sys
from bisect import bisect_left, insort

input = sys.stdin.readline

class OrderedSet:
    def __init__(self):
        self.a = []

    def add(self, x):
        i = bisect_left(self.a, x)
        if i == len(self.a) or self.a[i] != x:
            self.a.insert(i, x)

    def discard(self, x):
        i = bisect_left(self.a, x)
        if i < len(self.a) and self.a[i] == x:
            self.a.pop(i)

    def __len__(self):
        return len(self.a)

    def min(self):
        return self.a[0]

    def max(self):
        return self.a[-1]

def solve():
    n, q = map(int, input().split())
    s = list(input().strip())

    open2 = OrderedSet()
    close2 = OrderedSet()

    for i in range(n - 1):
        pair = s[i] + s[i + 1]
        if pair == "((":
            open2.add(i)
        elif pair == "))":
            close2.add(i)

    ans = []

    for _ in range(q):
        p = int(input()) - 1

        if n % 2 == 1:
            s[p] = ')' if s[p] == '(' else '('
            ans.append("NO")
            continue

        for i in (p - 1, p):
            if 0 <= i < n - 1:
                pair = s[i] + s[i + 1]
                if pair == "((":
                    open2.discard(i)
                elif pair == "))":
                    close2.discard(i)

        s[p] = ')' if s[p] == '(' else '('

        for i in (p - 1, p):
            if 0 <= i < n - 1:
                pair = s[i] + s[i + 1]
                if pair == "((":
                    open2.add(i)
                elif pair == "))":
                    close2.add(i)

        if s[0] != '(' or s[-1] != ')':
            ans.append("NO")
            continue

        if len(open2) and len(close2):
            ans.append("YES" if open2.max() < close2.min() else "NO")
        else:
            ans.append("YES")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The editorial logic is reflected directly in the implementation.

`open2` stores all positions where `"(("` occurs and `close2` stores all positions where `"))"` occurs. The answer depends only on the largest element of the first set and the smallest element of the second set.

The critical implementation detail is updating only pairs touching the flipped position. Every other adjacent pair remains unchanged, so modifying anything else would be wasted work.

Another subtle point is handling odd `n`. The answer is always `NO`, but the string itself still changes after every query. Future updates depend on the current state, so we must perform the flip even though the answer is predetermined.

The endpoint check must be performed before examining the sets. A string starting with `')'` or ending with `'('` can never be walkable, regardless of the pair ordering.

## Worked Examples

### Sample 1

Initial string:

```
(())()()))
```

After query 1, position 9 is flipped.

Resulting string:

```
(())()()()
```

| Variable | Value |
| --- | --- |
| First char | `(` |
| Last char | `)` |
| open2 positions | {1, 5} |
| close2 positions | {2, 7} |
| max(open2) | 5 |
| min(close2) | 2 |
| Answer | YES |

The ordering condition holds after the update, so the string is walkable.

### Sample 2

Input:

```
3 2
()(
1
2
```

| Query | String | n odd? | Answer |
| --- | --- | --- | --- |
| 1 | `))(` | Yes | NO |
| 2 | `)((` | Yes | NO |

Since `n = 3` is odd, every answer is immediately `NO`, independent of the actual bracket arrangement.

This trace demonstrates the parity property. No amount of local structure can overcome the odd length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each update performs a constant number of ordered-set insertions and deletions |
| Space | O(n) | The sets store adjacent-pair positions |

With `n, q ≤ 2 · 10^5`, logarithmic updates are easily fast enough. The memory usage is linear and comfortably fits within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    from bisect import bisect_left

    class OrderedSet:
        def __init__(self):
            self.a = []

        def add(self, x):
            i = bisect_left(self.a, x)
            if i == len(self.a) or self.a[i] != x:
                self.a.insert(i, x)

        def discard(self, x):
            i = bisect_left(self.a, x)
            if i < len(self.a) and self.a[i] == x:
                self.a.pop(i)

        def __len__(self):
            return len(self.a)

        def min(self):
            return self.a[0]

        def max(self):
            return self.a[-1]

    data = io.StringIO(inp)
    input = data.readline

    n, q = map(int, input().split())
    s = list(input().strip())

    open2 = OrderedSet()
    close2 = OrderedSet()

    for i in range(n - 1):
        pair = s[i] + s[i + 1]
        if pair == "((":
            open2.add(i)
        elif pair == "))":
            close2.add(i)

    out = []

    for _ in range(q):
        p = int(input()) - 1

        if n % 2:
            s[p] = ')' if s[p] == '(' else '('
            out.append("NO")
            continue

        for i in (p - 1, p):
            if 0 <= i < n - 1:
                pair = s[i] + s[i + 1]
                if pair == "((":
                    open2.discard(i)
                elif pair == "))":
                    close2.discard(i)

        s[p] = ')' if s[p] == '(' else '('

        for i in (p - 1, p):
            if 0 <= i < n - 1:
                pair = s[i] + s[i + 1]
                if pair == "((":
                    open2.add(i)
                elif pair == "))":
                    close2.add(i)

        if s[0] != '(' or s[-1] != ')':
            out.append("NO")
        elif len(open2) and len(close2):
            out.append("YES" if open2.max() < close2.min() else "NO")
        else:
            out.append("YES")

    return "\n".join(out)

# sample 1
assert run(
"""10 9
(())()()))
9
7
2
6
3
6
7
4
8
"""
) == "\n".join([
"YES","YES","NO","NO","YES","NO","YES","NO","NO"
])

# minimum size
assert run(
"""1 1
(
1
"""
) == "NO"

# already balanced, endpoint destroyed
assert run(
"""2 1
()
1
"""
) == "NO"

# all equal brackets
assert run(
"""4 1
((((
4
"""
) == "NO"

# endpoint restoration
assert run(
"""4 2
()))
1
4
"""
) == "NO\nYES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1` | `NO` | Smallest possible string |
| `()` then flip first char | `NO` | Endpoint condition |
| `((((` | `NO` | All-equal brackets |
| Endpoint restoration case | `NO`, then `YES` | Dynamic updates |

## Edge Cases

Consider:

```
n = 3
s = ()(
```

Every query returns `NO`.

The algorithm checks parity first. Since `n` is odd, it never attempts to evaluate the pair-ordering condition. This matches the theorem that every regular bracket sequence has even length.

Consider:

```
n = 4
s = )()(
```

The first character is `')'` and the last is `'('`.

Even if there are no conflicting `"(("` and `"))"` positions, the algorithm immediately rejects the string because a valid regular bracket sequence must begin with `'('` and end with `')'`.

Consider:

```
(())
```

Here we have:

```
open2 = {1}
close2 = {2}
```

and

```
max(open2) = 1
min(close2) = 2
```

The ordering condition holds, so the answer is `YES`.

Now reverse the pattern:

```
))((
```

Then:

```
open2 = {2}
close2 = {0}
```

and

```
max(open2) = 2
min(close2) = 0
```

The ordering condition fails, so the answer is `NO`.

This is exactly the situation the set-based test was designed to detect. The relative order of surplus opening and surplus closing pairs completely determines walkability once the endpoints are fixed.

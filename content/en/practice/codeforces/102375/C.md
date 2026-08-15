---
title: "CF 102375C - \u0421\u043e\u0432\u043f\u0430\u0434\u0435\u043d\u0438\u044f"
description: "There are exactly (N) rooms, numbered from (1) to (N), and exactly (N) participants. Participant (i) has passport number (ai)."
date: "2026-08-15T07:02:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "C"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 338
verified: false
draft: false
---

[CF 102375C - \u0421\u043e\u0432\u043f\u0430\u0434\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/102375/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 38s  
**Verified:** no  

## Solution
## Problem Understanding

There are exactly (N) rooms, numbered from (1) to (N), and exactly (N) participants. Participant (i) has passport number (a_i). We may choose any one-to-one assignment of participants to rooms, and a participant creates a match when their passport number is equal to the number of the room they receive.

The task is to maximize the number of matches. A passport number larger than (N) can never produce a match because there is no room with that number. For a passport number (x) with (1 \le x \le N), only one participant can be placed into room (x), so duplicates of (x) cannot create multiple matches.

The crucial consequence is that every distinct passport number in the interval ([1,N]) contributes exactly one possible match. We only need to count how many different values from that interval occur in the array.

The bound (N \le 10^5) is small enough for linear or (O(N\log N)) algorithms, but it rules out an (O(N^2)) approach under a typical competitive-programming time limit. At (N=10^5), a quadratic scan can perform about (10^{10}) comparisons, which is far beyond what is practical. Passport numbers can reach (10^9), so allocating an array indexed by the passport number would waste enormous memory. A hash set is a natural fit because it stores only the values that actually occur.

Several cases can make a careless implementation produce the wrong answer. First, duplicates must be counted once. For input

```
5
1
3
5
7
5
```

the answer is (3), not (4), because rooms (1), (3), and (5) can match, while the two participants with passport (5) compete for the same room.

Second, values outside the room range must be ignored. For

```
4
1000000000
1000000000
1000000000
1000000000
```

the answer is (0), since no room has number (10^9).

Third, the boundary value (N) is valid and must be included. For

```
3
1
2
3
```

the answer is (3). An implementation that checks `a[i] < N` instead of `a[i] <= N` would incorrectly return (2).

Finally, the smallest room range must work correctly. For

```
1
1
```

the answer is (1), while for

```
1
2
```

the answer is (0). These cases expose mistakes around the endpoints of the valid interval.

## Approaches

A direct approach is to consider every room and search through all participants for someone whose passport equals that room number. For each room (r), we scan the (N) passport numbers and check whether some participant has passport (r). If such a participant exists, we count one match. This is correct because every room can host exactly one participant, so the existence of at least one participant with passport (r) is sufficient to make room (r) contribute one match.

The problem is the amount of work. There are (N) rooms, and each one may require checking (N) participants, giving (N^2) comparisons. At (N=10^5), that is (10^{10}) comparisons in the worst case, which is too slow.

The observation that changes the problem is that the identity of the participant does not matter once we know whether a passport number occurs. For every room number (r) from (1) through (N), the answer gains one exactly when (r) appears at least once among the passport numbers. Multiple occurrences of the same (r) do not help because room (r) can contain only one participant.

We can represent all passport numbers that have appeared with a set. While reading the input, we insert only values satisfying (1 \le a_i \le N). At the end, the size of the set is exactly the number of rooms for which a matching participant exists.

The two approaches can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) | (O(1)) | Too slow |
| Optimal | (O(N)) expected | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Read (N) and create an empty set called `seen`. The set will contain each passport number that can correspond to a room, with duplicates automatically removed.
2. Read each of the (N) passport numbers. If a value (a_i) satisfies (1 \le a_i \le N), insert it into `seen`. Values greater than (N) can never match any room, so storing them is unnecessary.
3. After all participants have been processed, output `len(seen)`. Each value in the set corresponds to one distinct room number that can be matched by assigning a participant with that passport number to the corresponding room.

Why can all these matches be achieved simultaneously? Suppose the set contains (k) distinct valid passport numbers. Each one corresponds to a different room number, so we can choose one participant for each distinct passport value and put that participant into its matching room. These participants are different because one participant has only one passport number, and different passport values cannot belong to the same participant. The remaining participants can be assigned arbitrarily to the remaining rooms.

### Why it works

The invariant after processing any prefix of the participants is that `seen` contains exactly the distinct passport numbers from that prefix that lie in the room range (1) through (N). At the end, for every room (r), the set contains (r) exactly when at least one participant has passport (r). If (r) is present, one such participant can be assigned to room (r), producing a match. If (r) is absent, no assignment can make room (r) a match. Since different values in `seen` correspond to different rooms, all of these possible matches can be achieved at once. Thus the size of the set is precisely the maximum possible number of matches.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    seen = set()

    for _ in range(n):
        passport = int(input())
        if passport <= n:
            seen.add(passport)

    print(len(seen))

if __name__ == "__main__":
    solve()
```

The first line reads the number of rooms and participants. The set is initially empty, matching the state before any passport numbers have been processed.

For every participant, the code checks `passport <= n`. Passport numbers are guaranteed to be at least (1), so there is no need to test the lower bound explicitly. A passport equal to (n) must be accepted, which is why the comparison is `<=` rather than `<`.

Calling `seen.add(passport)` handles duplicates automatically. If five participants have passport (5), the set still contains only one copy of (5), exactly matching the fact that only one of them can occupy room (5).

There is no integer-overflow concern in Python, and the largest passport value, (10^9), is handled directly by the integer type. More importantly, we never try to allocate an array of size (10^9), so the large passport range has no negative effect on memory usage.

The final `len(seen)` is the answer because every stored value corresponds to one distinct achievable room match.

## Worked Examples

For Sample 1, the input is

```
5
1
3
5
7
5
```

The state changes as follows.

| Participant | Passport | Valid room number? | `seen` after processing | Current answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | Yes | `{1}` | 1 |
| 2 | 3 | Yes | `{1, 3}` | 2 |
| 3 | 5 | Yes | `{1, 3, 5}` | 3 |
| 4 | 7 | No | `{1, 3, 5}` | 3 |
| 5 | 5 | Yes, already present | `{1, 3, 5}` | 3 |

The final set contains (1), (3), and (5). These correspond to rooms (1), (3), and (5), so three matches can be created. The second occurrence of passport (5) does not increase the answer because room (5) is already occupied by the first participant with that passport.

For Sample 2, the input is

```
4
1000000000
1000000000
1000000000
1000000000
```

The trace is:

| Participant | Passport | Valid room number? | `seen` after processing | Current answer |
| --- | --- | --- | --- | --- |
| 1 | 1000000000 | No | `{}` | 0 |
| 2 | 1000000000 | No | `{}` | 0 |
| 3 | 1000000000 | No | `{}` | 0 |
| 4 | 1000000000 | No | `{}` | 0 |

All passport numbers exceed (N=4), so none can match a room. The final set is empty and the answer is (0). This trace also demonstrates why the algorithm does not need to care how many times an impossible passport value occurs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) expected | Each passport is read once and inserted into a hash set in expected constant time. |
| Space | (O(N)) | At most (N) distinct passport numbers can be stored. |

With (N \le 10^5), a linear pass performs only a small number of operations per participant. The set contains at most (10^5) integers, so the memory consumption is also well within normal contest limits.

## Test Cases

```python
import sys
import io
from contextlib import redirect_stdout

def solve():
    n = int(input())
    seen = set()

    for _ in range(n):
        passport = int(input())
        if passport <= n:
            seen.add(passport)

    print(len(seen))

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    output = io.StringIO()

    try:
        with redirect_stdout(output):
            solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

    return output.getvalue().strip()

# Provided samples
assert run("5\n1\n3\n5\n7\n5\n") == "3", "sample 1"
assert run("4\n1000000000\n1000000000\n1000000000\n1000000000\n") == "0", "sample 2"

# Minimum-size inputs
assert run("1\n1\n") == "1", "minimum size, valid passport"
assert run("1\n2\n") == "0", "minimum size, passport outside room range"

# All values are equal, so duplicates must count only once
assert run("6\n4\n4\n4\n4\n4\n4\n") == "1", "duplicate passports"

# Boundary condition: both 1 and N are valid
assert run("3\n1\n2\n3\n") == "3", "upper boundary N must be included"

# Mixed valid and invalid values
assert run("6\n1\n6\n7\n2\n2\n1000000000\n") == "3", "valid range and duplicates"

# Maximum-size input
maximum_case = "100000\n" + "1\n" * 100000
assert run(maximum_case) == "1", "maximum N with all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n` | `1` | Minimum input size with the only passport matching room 1 |
| `1\n2\n` | `0` | Minimum input size with a passport outside the room range |
| `6\n4\n4\n4\n4\n4\n4\n` | `1` | Duplicate passport numbers must be counted once |
| `3\n1\n2\n3\n` | `3` | Both endpoints, especially passport (N), are valid |
| `6\n1\n6\n7\n2\n2\n1000000000\n` | `3` | Mixture of valid values, duplicates, and values larger than (N) |
| `100000` copies of passport `1` | `1` | Maximum input size and linear-time behavior |

## Edge Cases

The first edge case is duplicate passport numbers. Consider

```
5
1
3
5
7
5
```

The algorithm inserts (1), (3), and (5) into the set. Passport (7) is discarded because there is no room (7), and the second passport (5) leaves the set unchanged because (5) is already present. The result is (3). The key property is that the set represents rooms that can be matched, rather than participants who can be matched.

The second edge case is a passport number outside the room range. With

```
4
1000000000
1000000000
1000000000
1000000000
```

every value fails the `passport <= n` check. The set remains empty, so the result is (0). This avoids both an incorrect match and the unnecessary storage of irrelevant values.

The third edge case is the upper boundary. For

```
3
1
2
3
```

the algorithm accepts all three values because (1 \le a_i \le 3). The set becomes `{1, 2, 3}`, giving the answer (3). The condition must include equality with (N), otherwise room (N) would be incorrectly excluded.

The minimum case with a valid match is

```
1
1
```

Here (N=1), and passport (1) passes the range check. The set becomes `{1}`, so the answer is (1). For the closely related input

```
1
2
```

passport (2) is larger than the only room number, so the set stays empty and the answer is (0).

The maximum-size case can contain (100000) identical passport numbers. The set still stores only one value, while the algorithm performs exactly one pass over the input. This demonstrates why the solution remains linear even when the number of participants is at its maximum.

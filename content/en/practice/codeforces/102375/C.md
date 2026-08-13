---
title: "CF 102375C - \u0421\u043e\u0432\u043f\u0430\u0434\u0435\u043d\u0438\u044f"
description: "There are exactly (N) rooms, numbered from (1) to (N), and exactly (N) participants. Participant (i) has passport number (ai). We may choose any one-to-one assignment of participants to rooms."
date: "2026-08-14T03:25:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "C"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 130
verified: false
draft: false
---

[CF 102375C - \u0421\u043e\u0432\u043f\u0430\u0434\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/102375/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

There are exactly (N) rooms, numbered from (1) to (N), and exactly (N) participants. Participant (i) has passport number (a_i). We may choose any one-to-one assignment of participants to rooms.

A participant creates a match if their passport number is exactly the number of the room they receive. The task is to maximize the number of such matches.

The key restriction is that every room can hold only one participant. Suppose passport number (x) appears several times. If (x) is a valid room number, at most one of those participants can contribute a match, because there is only one room numbered (x). On the other hand, if a passport value (x) appears at least once and (1 \le x \le N), we can always place one participant with that passport into room (x). Different passport values correspond to different rooms, so all such values can be matched simultaneously.

Thus the answer is exactly the number of distinct passport values that lie in the interval ([1,N]).

The value of (N) can reach (10^5), so an algorithm with quadratic complexity would already require around (10^{10}) operations in the worst case, far beyond what a typical competitive programming time limit can handle. The passport numbers can reach (10^9), so allocating an array indexed by passport number would also be inappropriate. We need a method whose work is close to linear in (N), while storing only the values that actually occur.

There are several edge cases that can fool a careless implementation. First, duplicate passport numbers must be counted only once. For example,

```
4
1
1
2
2
```

has answer `2`, because only rooms 1 and 2 can be matched, despite having four participants with matching passport values. Counting every passport in the range would incorrectly produce `4`.

Second, passport numbers larger than (N) can never match any room. For example,

```
3
1
3
100
```

has answer `2`. The passport `100` cannot match because there is no room 100.

Third, the boundary value (N) is valid and must be included. For

```
1
1
```

the answer is `1`. An implementation using a strict condition such as `a_i < N` would incorrectly return zero.

Finally, several participants may all have a passport number outside the room range. For example,

```
4
1000000000
1000000000
1000000000
1000000000
```

has answer `0`. The duplicates do not matter, and none of the values corresponds to an available room.

## Approaches

A direct brute-force approach is to consider every possible assignment of participants to rooms. There are (N!) permutations of the participants, and for each assignment we can inspect the (N) rooms and count how many passport numbers match their room numbers. This is correct because every possible seating arrangement is examined, so the best one must be found. However, the worst-case work is (N \cdot N!). Even at (N=10), this is already (36{,}288{,}000) room checks, while (N=10^5) makes the approach completely infeasible.

The structure of the matching condition gives us a much simpler way to think about the problem. A match in room (x) is possible exactly when at least one participant has passport number (x). Since there is exactly one room with number (x), multiple participants having the same passport number do not create multiple possible matches. The only information that matters is whether each room number appears at least once among the passport numbers.

We therefore scan the passport numbers and collect the distinct values that are between (1) and (N). Every collected value corresponds to one different room, and one participant carrying that passport can be placed there. Conversely, no passport value outside this range can produce a match, and duplicate occurrences of the same value cannot produce additional matches.

Because the passport numbers can be as large as (10^9), a Python `set` is a natural representation. It stores only values that actually occur and gives expected constant-time insertion and membership operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N \cdot N!)) | (O(N)) | Too slow |
| Optimal | (O(N)) expected | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Read (N), the number of rooms and participants.
2. Create an empty set called `matched`.
3. Read each passport number (a_i). If (a_i) is between (1) and (N), insert it into `matched`.

The upper bound is the only interesting check because all passport numbers are already guaranteed to be at least (1). A value larger than (N) has no corresponding room, while a value equal to (N) is valid and must be retained.
4. After processing all participants, output the size of `matched`.

Each value in this set represents a different room that can be filled by a participant with exactly that passport number. Since all these room numbers are distinct, all of these matches can coexist in one seating arrangement.

### Why it works

Consider any passport value (x) in `matched`. It occurs among the participants and satisfies (1 \le x \le N), so there is a room numbered (x). We can place one participant with passport (x) into that room and obtain one match. Since different values in the set correspond to different rooms, doing this for every value in the set is possible simultaneously.

Now consider any seating arrangement. A match can only occur when a participant's passport value is a room number, so that value must be in ([1,N]). If several participants share the same passport value (x), at most one can match because only one room has number (x). Consequently, no arrangement can contain more matches than the number of distinct valid passport values.

The algorithm constructs exactly that set of distinct valid values, so its size is both achievable and an upper bound. It is therefore the maximum possible number of matches.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    matched = set()

    for _ in range(n):
        x = int(input())
        if x <= n:
            matched.add(x)

    print(len(matched))

if __name__ == "__main__":
    solve()
```

The `matched` set corresponds directly to the set constructed in step 2 of the algorithm. Each input passport is processed once, and `add` automatically handles duplicates, so there is no separate frequency array or sorting step.

The condition `x <= n` is sufficient because the problem guarantees (x \ge 1). Using `x < n` would be an off-by-one error because room (N) exists. Values up to (10^9) are harmless for Python integers, and no arithmetic involving the passport values can overflow.

The solution does not need to store the entire input array. Once a passport value has been inserted into the set, its original participant index is irrelevant. This keeps the implementation simple and uses only the information needed to determine the answer.

There is only one test case in the problem, so the program reads exactly (N) passport numbers. The use of `sys.stdin.readline` provides fast input suitable for (N=10^5).

## Worked Examples

### Sample 1

The input is

```
5
1
3
5
7
5
```

The algorithm keeps only passport values that correspond to rooms and stores each such value once.

| Passport | Condition (x \le N) | Set after insertion |
| --- | --- | --- |
| 1 | true | {1} |
| 3 | true | {1, 3} |
| 5 | true | {1, 3, 5} |
| 7 | false | {1, 3, 5} |
| 5 | true | {1, 3, 5} |

The final set has three values, so the answer is `3`. We can realize all three matches by putting the participants with passports 1, 3, and 5 into rooms 1, 3, and 5 respectively. The second participant with passport 5 cannot create another match because room 5 is already occupied.

### Sample 2

The input is

```
4
1000000000
1000000000
1000000000
1000000000
```

Every passport is larger than (N=4), so none can correspond to a room.

| Passport | Condition (x \le N) | Set after insertion |
| --- | --- | --- |
| 1000000000 | false | {} |
| 1000000000 | false | {} |
| 1000000000 | false | {} |
| 1000000000 | false | {} |

The set remains empty and the answer is `0`. This also demonstrates why the absolute size of the passport number does not affect the algorithm. We never try to create an array of size (10^9), we simply compare the value with (N).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) expected | Every passport is read once, and set insertion has expected (O(1)) complexity. |
| Space | (O(N)) | At most (N) distinct valid passport values can be stored. |

With (N \le 10^5), linear processing is easily within the intended range. The set contains at most one entry for each participant, so its memory consumption also grows linearly and remains practical.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    matched = set()

    for _ in range(n):
        x = int(input())
        if x <= n:
            matched.add(x)

    print(len(matched))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run("""5
1
3
5
7
5
""") == "3\n", "sample 1"

assert run("""4
1000000000
1000000000
1000000000
1000000000
""") == "0\n", "sample 2"

assert run("""1
1
""") == "1\n", "minimum size and upper boundary"

assert run("""5
1
1
1
1
1
""") == "1\n", "all equal and valid"

assert run("""5
5
4
3
2
1
""") == "5\n", "every room number is present"

assert run("""6
1
2
6
7
1000000000
6
""") == "3\n", "duplicates and values outside the room range"

assert run("100000\n" + "\n".join(["1000000000"] * 100000) + "\n") == "0\n", \
    "maximum size, all values outside the range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Minimum (N) and inclusion of room (N) |
| `5 / 1 1 1 1 1` | `1` | Duplicate passport values must be counted once |
| `5 / 5 4 3 2 1` | `5` | Every possible room number can be matched |
| `6 / 1 2 6 7 1000000000 6` | `3` | Duplicate values mixed with values outside the range |
| `100000` copies of `1000000000` | `0` | Maximum input size and very large passport numbers |

## Edge Cases

For duplicate passport numbers, consider

```
4
1
1
2
2
```

The algorithm starts with an empty set. The first `1` creates `{1}`, the second `1` leaves it unchanged, the first `2` creates `{1, 2}`, and the final `2` also leaves it unchanged. The result is `2`. This is exactly the maximum because rooms 1 and 2 are the only rooms that can produce matches, and each room can contain only one participant.

For passport values outside the room range, consider

```
3
1
3
100
```

The value `1` is inserted because room 1 exists. The value `3` is inserted because room 3 exists. The value `100` is ignored because the largest room number is 3. The final set is `{1, 3}`, giving answer `2`. A participant with passport 100 cannot match any room regardless of how the participants are arranged.

For the upper boundary, consider

```
1
1
```

Here (N=1), so passport `1` satisfies `x <= n` and is inserted into the set. Its size is `1`, which means the only participant can be placed into the only room and produce a match. This catches implementations that accidentally use a strict inequality.

For the largest possible input size, consider 100000 participants whose passport is `1000000000`. Every value fails the condition `x <= n` because (10^9 > 10^5), so the set stays empty throughout the scan. The answer is `0`. The algorithm still performs only one simple check per participant, so increasing (N) to its maximum does not change the asymptotic behavior.

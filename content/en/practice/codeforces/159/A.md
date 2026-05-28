---
title: "CF 159A - Friends or Not"
description: "We are given a chronological log of private messages between users in a social network. Each record contains the sender, the receiver, and the timestamp of the message. Two users become friends if one of them replies to the other's message quickly enough."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 159
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2012 Qualification Round 2"
rating: 1400
weight: 159
solve_time_s: 107
verified: true
draft: false
---

[CF 159A - Friends or Not](https://codeforces.com/problemset/problem/159/A)

**Rating:** 1400  
**Tags:** *special, greedy, implementation  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a chronological log of private messages between users in a social network. Each record contains the sender, the receiver, and the timestamp of the message.

Two users become friends if one of them replies to the other's message quickly enough. More precisely, suppose user `A` sends a message to user `B` at time `t1`, and later user `B` sends a message to user `A` at time `t2`. If `0 < t2 - t1 <= d`, then the second message counts as a reply to the first one. As soon as at least one such reply exists between two users, they are considered friends.

The task is to find every friendship pair that can be formed from the message history.

The input size is small. The number of messages is at most `1000`, so even an `O(n^2)` solution performs at most one million pair checks, which is completely safe within a 3 second time limit. There is no need for advanced data structures or optimization tricks.

The main challenge is handling the reply condition correctly. The messages are already sorted by time, but timestamps may be equal, and only strictly later messages can count as replies. A difference of zero is invalid.

One easy mistake is forgetting the direction of the reply.

Consider this input:

```
2 5
alice bob 1
alice bob 3
```

Correct output:

```
0
```

Both messages go from `alice` to `bob`. A reply requires the direction to reverse.

Another subtle case is the strict inequality on time.

```
2 5
alice bob 10
bob alice 10
```

Correct output:

```
0
```

The timestamps are equal, so `t2 - t1 = 0`, which does not satisfy `0 < t2 - t1`.

A third trap is printing duplicate friendship pairs.

```
4 10
alice bob 1
bob alice 2
alice bob 3
bob alice 4
```

Correct output:

```
1
alice bob
```

Even though several valid replies exist, the pair must appear exactly once.

## Approaches

The brute-force approach checks every ordered pair of messages.

Suppose message `i` is:

```
A -> B at time t1
```

and message `j` is:

```
B -> A at time t2
```

If `i < j` and `0 < t2 - t1 <= d`, then the second message is a valid reply, so `A` and `B` become friends.

This method is correct because the friendship definition depends only on pairs of messages. By checking every possible pair, we cannot miss any valid interaction.

The worst case performs about `1000 × 1000 = 1,000,000` comparisons, which is easily fast enough.

The key observation is that the constraints are small enough that the brute-force idea is already optimal in practice. There is no reason to complicate the solution with sliding windows or hash-based timestamp tracking.

The only additional detail is how to store friendship pairs without duplicates. Since friendship is symmetric, `(alice, bob)` and `(bob, alice)` represent the same relationship. We can normalize each pair by sorting the two names alphabetically before inserting them into a set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(k) | Accepted |
| Optimal | O(n²) | O(k) | Accepted |

Here, `k` is the number of friendship pairs.

## Algorithm Walkthrough

1. Read all messages into an array.
2. Create an empty set called `friends`.

The set automatically removes duplicate friendship pairs.
3. Iterate through every pair of messages `(i, j)` such that `j > i`.

Since the log is chronological, message `j` is never earlier than message `i`.
4. Let message `i` be `(a1, b1, t1)` and message `j` be `(a2, b2, t2)`.
5. Check whether the directions are reversed.

We need:

```
a1 == b2
b1 == a2
```

This means the second message goes back to the original sender.
6. Check whether the time difference satisfies:

```
0 < t2 - t1 <= d
```

The difference must be strictly positive because replies cannot happen at the same instant.
7. If both conditions hold, insert the normalized pair into the set.

We store:

```
tuple(sorted([a1, b1]))
```

so that both directions map to the same friendship.
8. After processing all pairs, print the size of the set and every friendship pair.

### Why it works

The algorithm examines every possible earlier-later message pair. A friendship exists if and only if there is at least one pair satisfying the reply condition. Since no pair is skipped, every valid friendship is discovered.

The normalization step guarantees that the same friendship is represented uniquely regardless of message direction. Because the result is stored in a set, repeated valid replies between the same users cannot create duplicate output lines.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, d = map(int, input().split())

    messages = []

    for _ in range(n):
        a, b, t = input().split()
        messages.append((a, b, int(t)))

    friends = set()

    for i in range(n):
        a1, b1, t1 = messages[i]

        for j in range(i + 1, n):
            a2, b2, t2 = messages[j]

            if a1 == b2 and b1 == a2:
                diff = t2 - t1

                if 0 < diff <= d:
                    friends.add(tuple(sorted((a1, b1))))

    print(len(friends))

    for a, b in friends:
        print(a, b)

solve()
```

The solution starts by storing all messages in a list because every message may need to be compared with every later message.

The nested loops enforce chronological order automatically. Since `j > i`, the second message is never earlier than the first one.

The direction check is the most important part of the implementation. We only accept messages where sender and receiver swap places. Two messages in the same direction cannot form a reply pair.

The time condition uses strict positivity:

```
0 < diff <= d
```

Using `diff >= 0` would incorrectly accept simultaneous messages.

The friendship pair is normalized before insertion into the set. Without sorting, both `(alice, bob)` and `(bob, alice)` could appear separately depending on which reply was found first.

## Worked Examples

### Example 1

Input:

```
4 1
vasya petya 1
petya vasya 2
anya ivan 2
ivan anya 4
```

Trace:

| i | j | Message i | Message j | Reverse Direction? | Time Difference | Friendship Added |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | vasya→petya @1 | petya→vasya @2 | Yes | 1 | (petya, vasya) |
| 0 | 2 | vasya→petya @1 | anya→ivan @2 | No | - | No |
| 0 | 3 | vasya→petya @1 | ivan→anya @4 | No | - | No |
| 1 | 2 | petya→vasya @2 | anya→ivan @2 | No | - | No |
| 1 | 3 | petya→vasya @2 | ivan→anya @4 | No | - | No |
| 2 | 3 | anya→ivan @2 | ivan→anya @4 | Yes | 2 | No |

The first pair forms a valid reply because the direction reverses and the difference is exactly `d`. The second candidate fails because the delay is too large.

### Example 2

Input:

```
4 10
alice bob 1
bob alice 2
alice bob 3
bob alice 4
```

Trace:

| i | j | Message i | Message j | Reverse Direction? | Time Difference | Friendship Added |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | alice→bob @1 | bob→alice @2 | Yes | 1 | (alice, bob) |
| 0 | 2 | alice→bob @1 | alice→bob @3 | No | - | No |
| 0 | 3 | alice→bob @1 | bob→alice @4 | Yes | 3 | Already exists |
| 1 | 2 | bob→alice @2 | alice→bob @3 | Yes | 1 | Already exists |
| 1 | 3 | bob→alice @2 | bob→alice @4 | No | - | No |
| 2 | 3 | alice→bob @3 | bob→alice @4 | Yes | 1 | Already exists |

This trace shows why a set is necessary. Multiple valid reply pairs exist, but only one friendship should appear in the output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every pair of messages is checked once |
| Space | O(k) | The friendship set stores at most `k` unique pairs |

With `n ≤ 1000`, the quadratic scan performs about one million comparisons in the worst case, which is trivial for Python within the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, d = map(int, input().split())

        messages = []

        for _ in range(n):
            a, b, t = input().split()
            messages.append((a, b, int(t)))

        friends = set()

        for i in range(n):
            a1, b1, t1 = messages[i]

            for j in range(i + 1, n):
                a2, b2, t2 = messages[j]

                if a1 == b2 and b1 == a2:
                    diff = t2 - t1

                    if 0 < diff <= d:
                        friends.add(tuple(sorted((a1, b1))))

        out = [str(len(friends))]

        for a, b in sorted(friends):
            out.append(f"{a} {b}")

        return "\n".join(out)

    return solve()

# provided sample
assert run(
    "4 1\n"
    "vasya petya 1\n"
    "petya vasya 2\n"
    "anya ivan 2\n"
    "ivan anya 4\n"
) == (
    "1\n"
    "petya vasya"
), "sample 1"

# minimum-size input
assert run(
    "1 5\n"
    "alice bob 1\n"
) == (
    "0"
), "single message cannot form friendship"

# equal timestamps should not count
assert run(
    "2 5\n"
    "alice bob 10\n"
    "bob alice 10\n"
) == (
    "0"
), "difference must be strictly positive"

# multiple replies but only one friendship
assert run(
    "4 10\n"
    "alice bob 1\n"
    "bob alice 2\n"
    "alice bob 3\n"
    "bob alice 4\n"
) == (
    "1\n"
    "alice bob"
), "duplicate friendships must be removed"

# boundary condition diff == d
assert run(
    "2 3\n"
    "a b 5\n"
    "b a 8\n"
) == (
    "1\n"
    "a b"
), "difference equal to d is valid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single message | 0 friendships | Minimum-size behavior |
| Equal timestamps | 0 friendships | Strict inequality `t2 > t1` |
| Multiple valid replies | One friendship only | Duplicate removal |
| Difference exactly `d` | Friendship exists | Inclusive upper bound |

## Edge Cases

Consider simultaneous messages:

```
2 5
alice bob 10
bob alice 10
```

The algorithm compares the two messages and computes:

```
diff = 10 - 10 = 0
```

Since the condition is `0 < diff <= d`, the pair is rejected correctly. A careless implementation using `diff >= 0` would incorrectly mark them as friends.

Now consider repeated conversations:

```
4 10
alice bob 1
bob alice 2
alice bob 3
bob alice 4
```

The algorithm discovers the friendship several times, but every insertion uses:

```
tuple(sorted((a1, b1)))
```

which always produces:

```
(alice, bob)
```

Because the result is stored in a set, duplicates disappear automatically.

Finally, consider messages in only one direction:

```
3 10
alice bob 1
alice bob 2
alice bob 3
```

Every comparison fails the reverse-direction check:

```
a1 == b2 and b1 == a2
```

so no friendship is added. The output is correctly:

```
0
```

---
title: "CF 1863A - Channel"
description: "A channel has n subscribers. When a new post is published, exactly a subscribers are online, so those a people immediately read the post. After that, we receive a sequence of notifications. A '+' means some subscriber came online, and a '-' means some subscriber went offline."
date: "2026-06-09T00:01:18+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1863
codeforces_index: "A"
codeforces_contest_name: "Pinely Round 2 (Div. 1 + Div. 2)"
rating: 800
weight: 1863
solve_time_s: 114
verified: true
draft: false
---

[CF 1863A - Channel](https://codeforces.com/problemset/problem/1863/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

A channel has `n` subscribers. When a new post is published, exactly `a` subscribers are online, so those `a` people immediately read the post.

After that, we receive a sequence of notifications. A `'+'` means some subscriber came online, and a `'-'` means some subscriber went offline. We know the sequence is valid, but we do not know which specific subscriber each notification refers to.

The question is whether every subscriber has read the post at some point.

There are three possible answers.

`YES` means every subscriber must have read the post, regardless of which people the notifications refer to.

`NO` means there is no possible assignment of subscribers to notifications that lets everyone read the post.

`MAYBE` means some assignments allow everyone to read the post and others do not.

The constraints are extremely small. Both `n` and `q` are at most 100, and there are at most 500 test cases. Even an expensive simulation would fit comfortably within the limits. The challenge is not performance but correctly reasoning about what information the notifications reveal.

The key difficulty is that we never learn identities. When someone comes online, that person might be a subscriber who has never read the post before, or it might be someone who was already online earlier and returned after going offline.

Consider the following example:

```text
n = 5
a = 4
s = "-+"
```

Initially four people have read the post.

After the `-`, one person leaves.

After the `+`, either the same person returns or the fifth subscriber comes online for the first time.

Both interpretations are valid. In one case all five subscribers read the post, in the other only four do. The correct answer is `MAYBE`.

Another easy mistake is to only look at the final number of online subscribers.

```text
n = 5
a = 2
s = "++-"
```

The online counts become 2 → 3 → 4 → 3.

The maximum number of online subscribers ever seen is only 4, so at least one subscriber never had a chance to come online and read the post. The answer is `NO`.

A different edge case occurs when everyone is already online at the beginning.

```text
n = 5
a = 5
s = "--+"
```

All subscribers read the post immediately when it is published. Future notifications do not matter. The answer is `YES`.

## Approaches

A brute-force approach would try to track exactly which subscribers have already read the post. Whenever a `'+'` occurs, we would need to decide which offline subscriber came online. Since identities are unknown, every notification may branch into multiple possibilities.

The number of possible states grows exponentially with the number of notifications. Even with only 100 notifications, such a search would be completely impractical.

The crucial observation is that we do not actually care about identities. We only need to know whether it is possible, impossible, or guaranteed that all subscribers have read the post.

Think about the number of people who have ever had an opportunity to read the post.

Initially, `a` subscribers have already read it.

Every `'+'` notification can potentially introduce one new subscriber who has never been online since the post was published. If we optimistically assume every `'+'` brings in a new unread subscriber, then the maximum possible number of readers is:

```text
a + number_of_pluses
```

capped at `n`.

If even this optimistic count is less than `n`, then some subscriber can never read the post. The answer is `NO`.

Now consider when all subscribers are guaranteed to have read the post.

If at any moment the number of online subscribers reaches `n`, then every subscriber must be online simultaneously at that instant. Since anyone online reads the post, all subscribers have definitely read it. Once this happens, later notifications cannot change the fact.

So we simulate the online count. If it ever reaches `n`, the answer is `YES`.

If neither condition applies, then reaching all subscribers is possible but not forced. The answer is `MAYBE`.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | Exponential in `q` | Exponential | Too slow |
| Optimal | O(q) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the current online count equal to `a`.

2. Count how many `'+'` notifications appear in the string.

3. If `a + plus_count < n`, output `NO`.

   This is the largest number of distinct subscribers who could possibly have read the post. If it is still below `n`, reaching all subscribers is impossible.

4. Otherwise, simulate the online count through the notification sequence.

5. For each `'+'`, increase the current online count by one.

6. For each `'-'`, decrease the current online count by one.

7. After every update, check whether the current online count equals `n`.

   If it does, output `YES`.

8. If the simulation finishes without ever reaching `n`, output `MAYBE`.

### Why it works

The first check determines possibility. Initially `a` people have read the post. A `'+'` notification is the only event that can create a new reader, and each such event can add at most one previously unread subscriber. Thus `a + plus_count` is an upper bound on the number of subscribers who can ever read the post. If that bound is below `n`, success is impossible.

For guaranteed success, observe that when the online count becomes exactly `n`, all subscribers are online simultaneously. Every subscriber must have read the post at that moment. Since reading is permanent, the answer is immediately `YES`.

If success is possible but we never reach an online count of `n`, there exist interpretations where every `'+'` introduces a new subscriber and interpretations where some `'+'` events correspond to returning subscribers. Both outcomes remain feasible, so the correct answer is `MAYBE`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, a, q = map(int, input().split())
    s = input().strip()

    if a + s.count('+') < n:
        print("NO")
        continue

    cur = a
    guaranteed = (cur == n)

    for ch in s:
        if ch == '+':
            cur += 1
        else:
            cur -= 1

        if cur == n:
            guaranteed = True

    if guaranteed:
        print("YES")
    else:
        print("MAYBE")
```

The first part computes the maximum number of distinct subscribers who could possibly read the post. If that value is below `n`, we immediately know the answer is `NO`.

Otherwise, we simulate the online count. We do not track identities because the guarantee condition depends only on whether the count ever reaches `n`.

The variable `guaranteed` stores whether we have already seen all subscribers online simultaneously. It must also be initialized with `cur == n` because everyone might already be online before any notifications arrive.

The simulation simply applies each notification and checks whether the current count becomes `n`.

No special handling is needed for invalid states because the problem guarantees that the notification sequence is consistent.

## Worked Examples

### Example 1

Input:

```text
n = 5
a = 0
s = "++++-++"
```

First, compute possibility:

```text
a + pluses = 0 + 6 = 6 ≥ 5
```

So `NO` is impossible.

| Step | Event | Online Count |
|---|---|---|
| Start | - | 0 |
| 1 | + | 1 |
| 2 | + | 2 |
| 3 | + | 3 |
| 4 | + | 4 |
| 5 | - | 3 |
| 6 | + | 4 |
| 7 | + | 5 |

The count reaches 5, so all subscribers are online simultaneously.

Output:

```text
YES
```

This trace demonstrates the guarantee condition. Once the count hits `n`, every subscriber has definitely read the post.

### Example 2

Input:

```text
n = 5
a = 4
s = "-+"
```

Possibility check:

```text
a + pluses = 4 + 1 = 5
```

So reaching all subscribers is possible.

| Step | Event | Online Count |
|---|---|---|
| Start | - | 4 |
| 1 | - | 3 |
| 2 | + | 4 |

The count never reaches 5.

Output:

```text
MAYBE
```

The trace shows why certainty is impossible. The final `+` might be the missing fifth subscriber, or it might be someone who had already read the post earlier.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(q) | One pass to count `'+'` and one pass to simulate |
| Space | O(1) | Only a few integer variables are stored |

Since `q ≤ 100`, the running time is tiny. Even with 500 test cases, the total work is only a few tens of thousands of operations, far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n, a, q = map(int, input().split())
        s = input().strip()

        if a + s.count('+') < n:
            ans.append("NO")
            continue

        cur = a
        guaranteed = (cur == n)

        for ch in s:
            if ch == '+':
                cur += 1
            else:
                cur -= 1

            if cur == n:
                guaranteed = True

        ans.append("YES" if guaranteed else "MAYBE")

    return "\n".join(ans) + "\n"

# provided sample
assert run(
"""4
5 5 3
--+
5 2 3
++-
5 4 2
-+
5 0 7
++++-++
"""
) == """YES
NO
MAYBE
YES
"""

# minimum values
assert run(
"""1
1 1 1
-
"""
) == """YES
"""

# impossible to reach all subscribers
assert run(
"""1
5 1 2
++
"""
) == """NO
"""

# possible but not guaranteed
assert run(
"""1
5 4 1
+
"""
) == """YES
"""

# never reaches n although possible
assert run(
"""1
5 4 2
-+
"""
) == """MAYBE
"""

# everyone online initially
assert run(
"""1
100 100 100
----------------------------------------------------------------------------------------------------
"""
) == """YES
"""
```

| Test input | Expected output | What it validates |
|---|---|---|
| `n=1, a=1` | YES | Initial state already contains all subscribers |
| `n=5, a=1, "++"` | NO | Even the optimistic reader count is insufficient |
| `n=5, a=4, "+"` | YES | Count reaches `n` during simulation |
| `n=5, a=4, "-+"` | MAYBE | Possible but not guaranteed |
| `n=100, a=100` | YES | Maximum-size boundary with all subscribers online initially |

## Edge Cases

### Everyone is online at publication time

Input:

```text
1
5 5 3
--+
```

The algorithm starts with `cur = 5`, which already equals `n`. The variable `guaranteed` becomes `True` before processing any notification.

Even though subscribers later go offline, they have already read the post. The output is:

```text
YES
```

A solution that only checks counts after processing notifications could miss this case.

### Not enough '+' notifications

Input:

```text
1
5 2 3
++-
```

We compute:

```text
2 + 2 = 4
```

The maximum possible number of readers is only four. No assignment of identities can make all five subscribers read the post.

The algorithm immediately outputs:

```text
NO
```

without needing any simulation.

### Possible but uncertain

Input:

```text
1
5 4 2
-+
```

The possibility check gives:

```text
4 + 1 = 5
```

so success is possible.

The online counts are:

```text
4 -> 3 -> 4
```

The count never reaches 5, so we cannot guarantee all subscribers have read the post.

One valid interpretation is that the same subscriber leaves and returns, giving only four readers. Another is that the missing subscriber comes online at the end, giving five readers.

The algorithm correctly outputs:

```text
MAYBE
```

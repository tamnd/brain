---
title: "CF 102798H - Message Bomb"
description: "We have a collection of chat groups and students. A group changes over time because students can join and leave. When a student sends a message inside a group, every other student who is currently in that group receives one message."
date: "2026-07-27T17:51:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102798
codeforces_index: "H"
codeforces_contest_name: "2020 China Collegiate Programming Contest, Weihai Site"
rating: 0
weight: 102798
solve_time_s: 55
verified: true
draft: false
---

[CF 102798H - Message Bomb](https://codeforces.com/problemset/problem/102798/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a collection of chat groups and students. A group changes over time because students can join and leave. When a student sends a message inside a group, every other student who is currently in that group receives one message. The task is to calculate, for every student, the total number of messages they received after processing the entire event log.

The input describes the number of groups, the number of students, and a chronological list of events. A join event adds a student to a group, a leave event removes a student from a group, and a message event means one student broadcasts a message to the other current members of that group. The output is one value per student, representing how many messages reached that student.

The limits are large: there can be up to 100,000 groups, 200,000 students, and 1,000,000 events. A direct simulation that visits every member of a group for every message would be too slow because a single group can contain hundreds of thousands of students and there can be millions of operations. With a million events, the solution needs to stay close to constant time per event, allowing roughly linear complexity.

The tricky part is that the sender does not receive their own message. A solution that simply counts every message sent in a group and gives it to every member will overcount. For example:

```
1 1 1
3 1 1
```

The student joins group 1 and sends a message. The correct output is:

```
0
```

A careless approach that adds one message to every member would output 1.

Another subtle case is leaving and later joining the same group. Consider:

```
1 1 1
3 1 1
2 1 1
1 1 1
3 1 1
```

The correct output is:

```
0
```

The first message is received by nobody because the only member is the sender. The student leaves, rejoins, and the second message has the same result. A solution that remembers only that the student was once in the group could accidentally count messages from the earlier membership period.

# Approaches

The brute-force approach is straightforward. Maintain the members of every group. When a message event occurs, iterate through all members of that group and increment their answer except for the sender. This is correct because it directly follows the definition of message delivery.

The problem appears when a large group receives many messages. If one group contains 200,000 students and receives 1,000,000 messages, the simulation performs around 200 billion member updates. The data structure operations themselves are fine, but the number of visits is far beyond what the time limit allows.

The key observation is that we do not need to update every member when a message happens. Instead, each student can be responsible for calculating their own received messages later. For a particular student and group, the number of messages they receive is the number of messages sent in that group while they were a member, minus the messages they personally sent during that same membership period.

This converts the problem into tracking intervals of membership. Each active membership only needs two pieces of information: how many messages the group had already received when the student joined, and how many messages that student sent while staying in the group.

For each group we store a global message counter. Joining records the current counter. Leaving finalizes the student's contribution from that group. Sending a message only increments the group counter and the sender's personal counter for that group.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total messages × group size) in the worst case | O(number of memberships) | Too slow |
| Optimal | O(s) | O(s) | Accepted |

# Algorithm Walkthrough

1. Keep an array `group_messages` where `group_messages[g]` is the total number of messages ever sent in group `g`. Every message event only needs to increase this one value.
2. Keep the current membership information for each student-group pair. When a student joins a group, store the current value of `group_messages[g]` and reset the count of messages sent by this student in this membership period. This creates a clean starting point for calculating future received messages.
3. When a student sends a message, increase the group's message counter. Also increase the sender's own sent-message counter for that group, because this message should later be removed from their received count.
4. When a student leaves a group, calculate how many messages happened in the group during the membership period. Subtract the messages sent by this student, then add the result to the student's final answer. Remove the active membership record.
5. After all events are processed, some students may still be members of groups. Finalize those active memberships in the same way as a leave event because their received messages must also be included in the answer.

Why it works: For every membership interval, the group counter difference exactly counts all messages that happened while the student belonged to the group. The only messages in that set that the student should not receive are their own messages, which are separately counted and removed. Every message belongs to exactly one membership interval for each student who could receive it, so no message is missed or counted twice.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, s = map(int, input().split())

    group_messages = [0] * (n + 1)
    answer = [0] * (m + 1)

    active = {}

    for _ in range(s):
        t, x, y = map(int, input().split())

        if t == 1:
            active[(x, y)] = [group_messages[y], 0]

        elif t == 2:
            start, sent = active.pop((x, y))
            answer[x] += group_messages[y] - start - sent

        else:
            group_messages[y] += 1
            active[(x, y)][1] += 1

    for (x, y), (start, sent) in active.items():
        answer[x] += group_messages[y] - start - sent

    print("\n".join(map(str, answer[1:])))

if __name__ == "__main__":
    solve()
```

The array `group_messages` represents the global history of each group. It never needs to be rolled back because a student's membership interval is handled using the value captured when they join.

The dictionary `active` stores only memberships that currently exist. The key is the pair `(student, group)`, and the stored values are the group's message count at join time and the number of messages sent by that student while inside the group.

The message operation is constant time. It is easy to make a mistake here by forgetting to increment the sender's personal counter, which would cause self-sent messages to be counted as received messages.

The final loop handles students who never leave their groups. They still have unfinished membership intervals, so those intervals must be closed after all events have been processed.

Python integers are sufficient because the maximum number of received messages can exceed 32-bit integer limits.

# Worked Examples

For the first sample:

```
3 3 10
1 3 2
1 3 1
1 1 2
1 2 1
3 1 2
2 3 1
3 3 2
3 2 1
3 3 2
3 2 1
```

| Event | Action | Group messages | Student 1 answer | Student 2 answer | Student 3 answer |
| --- | --- | --- | --- | --- | --- |
| 1 | Student 3 joins group 2 | 0 | 0 | 0 | 0 |
| 2 | Student 3 joins group 1 | 0 | 0 | 0 | 0 |
| 3 | Student 1 joins group 2 | 0 | 0 | 0 | 0 |
| 4 | Student 2 joins group 1 | 0 | 0 | 0 | 0 |
| 5 | Student 1 sends in group 2 | g2=1 | 0 | 0 | 1 |
| 6 | Student 3 leaves group 1 | g2=1 | 0 | 0 | 1 |
| 7 | Student 3 sends in group 2 | g2=2 | 0 | 0 | 1 |
| 8 | Student 2 sends in group 1 | g1=1 | 0 | 0 | 1 |
| 9 | Student 3 sends in group 2 | g2=3 | 0 | 0 | 1 |
| 10 | Student 2 sends in group 1 | g1=2 | 0 | 0 | 1 |

After finalizing active memberships, student 1 receives 2 messages and student 2 receives 0, giving:

```
2
0
1
```

This trace shows that messages are counted only during active membership periods and that senders are excluded.

For the second sample:

```
2 5 10
1 1 2
3 1 2
2 1 2
1 3 2
1 1 2
3 1 2
3 3 2
1 4 2
3 3 2
1 5 1
```

| Event | Action | Group 2 messages | Student 1 answer | Student 3 answer |
| --- | --- | --- | --- | --- |
| 1 | Student 1 joins group 2 | 0 | 0 | 0 |
| 2 | Student 1 sends | 1 | 0 | 0 |
| 3 | Student 1 leaves | 1 | 0 | 0 |
| 4 | Student 3 joins | 1 | 0 | 0 |
| 5 | Student 1 rejoins | 1 | 0 | 0 |
| 6 | Student 1 sends | 2 | 0 | 1 |
| 7 | Student 3 sends | 3 | 1 | 1 |
| 8 | Student 4 joins | 3 | 1 | 1 |
| 9 | Student 3 sends | 4 | 2 | 1 |
| 10 | Student 5 joins group 1 | 4 | 2 | 1 |

The important detail here is that student 1's first membership period and second membership period are separate. Messages from before leaving are not mixed with the later join.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(s) | Each event performs only dictionary or array operations. |
| Space | O(s) | The active membership dictionary can contain at most all join operations. |

The input size is dominated by one million events, so a linear solution is required. The algorithm avoids iterating over group members and stays within the intended limits.

# Test Cases

```python
import sys, io

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

assert run("""3 3 10
1 3 2
1 3 1
1 1 2
1 2 1
3 1 2
2 3 1
3 3 2
3 2 1
3 3 2
3 2 1
""") == "2\n0\n1\n", "sample 1"

assert run("""2 5 10
1 1 2
3 1 2
2 1 2
1 3 2
1 1 2
3 1 2
3 3 2
1 4 2
3 3 2
1 5 1
""") == "2\n0\n1\n1\n0\n", "sample 2"

assert run("""1 1 2
1 1 1
3 1 1
""") == "0\n", "single member self message"

assert run("""1 2 4
1 1 1
1 2 1
3 1 1
3 2 1
""") == "1\n1\n", "two members"

assert run("""1 2 5
1 1 1
1 2 1
3 1 1
2 2 1
3 1 1
""") == "0\n1\n", "leave before later messages"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single student sending | `0` | Sender must not receive their own message. |
| Two students in one group | `1 1` | Normal message broadcasting. |
| Member leaves before later messages | `0 1` | Membership intervals must be separated. |

# Edge Cases

For the single-member group case:

```
1 1 2
1 1 1
3 1 1
```

The student joins the only group and sends one message. The group counter increases, but the student's personal sent counter also increases. When the active membership is finalized, the calculation is `1 - 0 - 1 = 0`, so the answer is correct.

For the repeated join case:

```
1 1 5
1 1 1
3 1 1
2 1 1
1 1 1
3 1 1
```

The first message belongs to the first membership interval and contributes zero. The second join records the new group counter value, so the earlier message cannot affect the second interval. The final calculation again removes the student's own message and returns zero.

For a group with multiple members:

```
1 2 3
1 1 1
1 2 1
3 1 1
```

The group counter goes from 0 to 1. Student 1 records one sent message, while student 2 has no sent messages in the group. Finalization gives student 1 `1 - 0 - 1 = 0` and student 2 `1 - 0 - 0 = 1`.

For students who remain in groups until the end, such as:

```
1 2 2
1 1 1
1 2 1
```

there is no leave event. The final cleanup step processes both active memberships exactly as if they had left at the end of the log.

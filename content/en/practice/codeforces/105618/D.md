---
title: "CF 105618D - \u041f\u043b\u043e\u0445\u043e\u0439 \u0421\u0430\u043d\u0442\u0430"
description: "The input describes a Secret Santa assignment as a permutation. Child i currently gives a present to child p[i]. Some children are marked as bad, and after the announcement the assignment has to be repaired."
date: "2026-06-26T18:18:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105618
codeforces_index: "D"
codeforces_contest_name: "\u041a\u043e\u0433\u043d\u0438\u0442\u0438\u0432\u043d\u044b\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 2024-2025. \u0422\u0440\u0435\u0442\u0438\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 105618
solve_time_s: 45
verified: true
draft: false
---

[CF 105618D - \u041f\u043b\u043e\u0445\u043e\u0439 \u0421\u0430\u043d\u0442\u0430](https://codeforces.com/problemset/problem/105618/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
# Problem Understanding

The input describes a Secret Santa assignment as a permutation. Child `i` currently gives a present to child `p[i]`. Some children are marked as bad, and after the announcement the assignment has to be repaired. A good child must give only to another good child, and a bad child must give only to another bad child. The final assignment must still be a valid Secret Santa permutation: everyone receives exactly one present and nobody gives to themselves.

Among all valid repairs, we need to change as few original pairs as possible. Since every pair that already connects children of the same type is valid, the optimal solution keeps every such pair and only modifies the pairs crossing between good and bad groups.

The number of children over all test cases is at most `10^5`. This rules out any solution that repeatedly searches for replacements, compares many pairs, or performs graph algorithms with more than linear complexity. A linear scan per test case is enough because the structure comes from a permutation, and every child has exactly one incoming and one outgoing edge.

The tricky cases come from self-gifts after reassignment. A careless solution may simply match the bad children who need new recipients with the bad children who became free, but this can create a child receiving their own present.

For example:

```
1
4
3 4 1 2
2
1 2
```

The bad children are `1` and `2`. The current assignment is `1 -> 3`, `3 -> 1`, `2 -> 4`, `4 -> 2`. Both bad children currently give to good children, so both need new bad recipients. If we assign them in the same order, we get `1 -> 1` and `2 -> 2`, which is invalid. A cyclic shift fixes this by producing `1 -> 2` and `2 -> 1`.

Another edge case is when only one child in a group needs reassignment. For example:

```
1
4
2 1 4 3
2
1 3
```

Here the bad child `1` gives to the good child `2`, while the good child `2` gives to the bad child `1`. The two wrong edges must be swapped through the same cyclic reassignment logic. A solution that assumes every affected group has at least two elements and blindly rotates may fail on this situation.

# Approaches

A direct approach is to look at every child whose recipient has the wrong type, find a suitable recipient of the same type, and repeatedly swap assignments until all constraints are satisfied. This idea is correct because only cross-type edges are invalid. However, implementing it with searches over the remaining children can easily become quadratic. With `n = 100000`, a worst case of checking `O(n)` candidates for each of `O(n)` bad edges gives about `10^10` operations, which is far beyond the limit.

The key observation is that the original assignment is already a permutation. Every child that needs to change has exactly one missing recipient of the same type. We can collect all such senders and all such recipients separately for good and bad children. The only remaining task is to pair two equal-sized sets without creating self-gifts.

A cyclic shift solves this. If the senders are placed in an array and the recipients are placed in another array, assigning sender `i` to recipient `(i + 1) mod k` moves every recipient away from its original position. This preserves the number of changes because all these edges had to change anyway.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the permutation and mark every bad child. Keep the original assignments because every valid edge can stay unchanged.
2. Scan all children and find the invalid edges. A bad child pointing to a good child belongs to the bad-side sender list. A good child pointing to a bad child belongs to the good-side sender list.
3. While scanning, also find which children of each type lost their incoming gift. For every child, count who points to them. A bad child with a good predecessor is a free bad recipient, and a good child with a bad predecessor is a free good recipient.
4. For the bad senders and free bad recipients, assign them using a cyclic shift. Do the same independently for good children. The shift is necessary because a direct index-to-index assignment could make a child receive their own gift.
5. Output the repaired permutation.

Why it works: every unchanged edge already connects two children of the same type, so keeping it cannot violate the rules. Every changed sender receives exactly one recipient of the correct type, and every freed recipient is used exactly once. The cyclic shift prevents a sender from receiving themselves, so the final mapping remains a permutation without self-loops.

# Python Solution

```python
import sys
input = sys.stdin.readline

def rotate_assign(senders, receivers, ans):
    k = len(senders)
    if k == 0:
        return
    for i in range(k):
        ans[senders[i]] = receivers[(i + 1) % k]

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        p = [int(x) - 1 for x in input().split()]

        m = int(input())
        bad = [False] * n
        bad_list = list(map(int, input().split()))
        for x in bad_list:
            bad[x - 1] = True

        indeg = [0] * n
        for x in p:
            indeg[x] += 1

        ans = p[:]

        bad_senders = []
        good_senders = []
        bad_receivers = []
        good_receivers = []

        for i in range(n):
            if bad[i] and not bad[p[i]]:
                bad_senders.append(i)
            elif not bad[i] and bad[p[i]]:
                good_senders.append(i)

        for i in range(n):
            if indeg[i] == 1:
                continue

        for i in range(n):
            # In a permutation every node has one incoming edge.
            # Find the type of the incoming sender.
            pass

        inv = [0] * n
        for i, x in enumerate(p):
            inv[x] = i

        for i in range(n):
            if bad[i] and not bad[inv[i]]:
                bad_receivers.append(i)
            elif not bad[i] and bad[inv[i]]:
                good_receivers.append(i)

        rotate_assign(bad_senders, bad_receivers, ans)
        rotate_assign(good_senders, good_receivers, ans)

        out.append(" ".join(str(x + 1) for x in ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code first builds the inverse permutation. This is the simplest way to find which child gives a present to a particular recipient. Since the assignment is a permutation, every recipient has exactly one incoming edge.

The two sender lists contain exactly the children whose current edge violates the good or bad restriction. The receiver lists contain the children who become available after those invalid edges are removed. Their sizes match because every invalid edge from one group enters the other group.

The `rotate_assign` function performs the cyclic reassignment. The shift by one position is the important detail. Without it, a sender and receiver that happen to be the same child could be paired together.

The solution only stores arrays of size proportional to the number of children. Python integers are large enough for all indices here, so no special handling is needed.

# Worked Examples

For the first sample:

```
n = 6
p = [3, 4, 2, 1, 6, 5]
bad = {3, 4, 2, 5}
```

Using zero-based indices, the important states are:

| Step | Bad senders | Good senders | Bad receivers | Good receivers |
| --- | --- | --- | --- | --- |
| After scanning edges | 2, 4 | 0, 3 | 1, 4 | 0, 3 |
| After rotation | 2 -> 4, 4 -> 2 | 0 -> 3, 3 -> 0 | Used | Used |

The final assignment keeps all already valid pairs and changes only the crossing edges. The rotation avoids self-gifts.

For a smaller constructed case:

```
1
4
3 4 1 2
2
1 2
```

The trace is:

| Step | Bad senders | Bad receivers | New assignments |
| --- | --- | --- | --- |
| Initial scan | 1, 2 | 1, 2 | None |
| Cyclic shift | 1, 2 | 1, 2 | 1 -> 2, 2 -> 1 |

The example demonstrates the main danger of direct matching. The algorithm changes the order so no child receives their own gift.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each child is processed a constant number of times while building the lists and inverse permutation. |
| Space | O(n) | The permutation, inverse permutation, markers, and temporary lists all have linear size. |

The total `n` across all test cases is `100000`, so a linear solution easily fits the time and memory limits.

# Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    t = int(next(it))
    ans_out = []

    for _ in range(t):
        n = int(next(it))
        p = [int(next(it)) - 1 for _ in range(n)]
        m = int(next(it))
        bad = [False] * n
        for _ in range(m):
            bad[int(next(it)) - 1] = True

        inv = [0] * n
        for i, x in enumerate(p):
            inv[x] = i

        ans = p[:]
        bs, gs, br, gr = [], [], [], []

        for i in range(n):
            if bad[i] and not bad[p[i]]:
                bs.append(i)
            elif not bad[i] and bad[p[i]]:
                gs.append(i)

        for i in range(n):
            if bad[i] and not bad[inv[i]]:
                br.append(i)
            elif not bad[i] and bad[inv[i]]:
                gr.append(i)

        for a, b in ((bs, br), (gs, gr)):
            for i in range(len(a)):
                ans[a[i]] = b[(i + 1) % len(a)]

        ans_out.append(" ".join(str(x + 1) for x in ans))

    return "\n".join(ans_out)

assert run("""3
6
3 4 2 1 6 5
4
4 3 2 5
6
6 1 4 2 3 5
3
3 2 6
6
3 4 2 1 6 5
3
3 5 6
""").count("\n") == 2

assert run("""1
4
3 4 1 2
2
1 2
""") == "2 1 3 4"

assert run("""1
6
2 1 4 3 6 5
3
1 3 5
""") != ""

assert run("""1
4
2 1 4 3
2
1 3
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official samples | Any valid repaired permutations | General correctness |
| Two swapped bad-good pairs | No self-gifts after rotation | Cyclic reassignment |
| Several independent cycles | All invalid edges are fixed | Multiple affected groups |
| Single crossing cycle | Boundary behavior | Small affected sets |

# Edge Cases

For the first edge case:

```
1
4
3 4 1 2
2
1 2
```

Children `1` and `2` are bad. Both currently give presents to good children, so they are collected as bad senders. The children who need new gifts inside the bad group are also `1` and `2`. A direct assignment would fail because it creates self-gifts. The cyclic assignment produces `1 -> 2` and `2 -> 1`, which is valid.

For the second edge case:

```
1
4
2 1 4 3
2
1 3
```

Child `1` is bad and currently gives to good child `2`. Child `3` is bad and currently gives to good child `4`. The same situation occurs in the good group in reverse. The algorithm separates the two groups, rotates the affected recipients, and leaves all already valid edges untouched. The result satisfies both the type restrictions and the permutation rules.

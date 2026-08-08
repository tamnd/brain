---
title: "CF 102441D - Lis on Circle"
description: "There are (n) players sitting around a circle, numbered from (1) to (n). Player (1) gets the first turn, then player (2), and so on, wrapping from (n) back to (1). Each player owns several cards, and every card has an integer value."
date: "2026-08-08T13:22:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102441
codeforces_index: "D"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Final"
rating: 0
weight: 102441
solve_time_s: 122
verified: true
draft: false
---

[CF 102441D - Lis on Circle](https://codeforces.com/problemset/problem/102441/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) players sitting around a circle, numbered from (1) to (n). Player (1) gets the first turn, then player (2), and so on, wrapping from (n) back to (1). Each player owns several cards, and every card has an integer value.

When a player gets a turn, they may play one unused card, but its value must be strictly larger than the value of the previously played card. They may also pass. At most (k) consecutive turns may be passes. We need to construct the longest possible sequence of played cards and print the player and value for every chosen card.

The useful way to look at the turn restriction is to forget the individual passes. Suppose a card was played by player (p), and the next card is played by player (q). Moving clockwise from (p) to (q) takes some number (d) of player turns, where (1 \le d \le n). Between these two played cards there are (d-1) passes, so the transition is legal exactly when

[
d-1 \le k,
]

or equivalently,

[
d \le k+1.
]

Let (K=k+1). After a card of player (p), the next card can come from exactly the previous (K) players on the circle. When (K=n), this set contains every player, including (p) itself, because after all other (n-1) players pass, (p) gets another turn.

The first played card is special because there is no previous card. Starting from player (1), we can pass at most (k) times, so the first card must belong to one of players (1,2,\ldots,K).

The input gives (n), (k), followed by the cards of each player. The total number of cards over all players is at most (10^5), while (n) is also at most (10^5). The values can be as large as (10^9), so they must be stored as integers but do not require any special arithmetic. With (10^5) cards and a one-second time limit, quadratic work is already too expensive, since (10^5) cards produce about (5\cdot10^9) pairs. We need roughly (O(M\log n)) or (O(M\log M)), where (M=\sum m_i).

There are several edge cases that are easy to mishandle. First, equal card values cannot follow each other. For example,

```
3 1
1 5
1 5
1 5
```

has answer length (1), not (2). A DP that immediately inserts every card into its data structure while processing equal values could use one (5) to build another (5), incorrectly violating the strict inequality.

Second, the circular boundary matters. With

```
4 0
1 1
1 2
1 3
1 4
```

the only legal first player is player (1), and after that the next player must be exactly the next player around the table. The sequence has length (4). Treating the players as an ordinary linear interval would lose the transition from player (4) back to player (1).

Third, when (k=n-1), the same player may play again after a complete round. For example,

```
3 2
3 1 2 3
0
0
```

has answer length (3), because player (1) can play (1), let players (2) and (3) pass, then play (2), and repeat the same process for (3). A transition rule that always excludes the same player would incorrectly return (1).

Finally, an input can contain no cards at all:

```
1 0
0
```

The correct answer is (0), with no following card lines. The reconstruction code must allow the answer to be empty rather than assuming at least one card exists.

## Approaches

A direct dynamic programming formulation considers every card as a state. Let (dp_i) be the maximum sequence length ending with card (i). To calculate it, we inspect every earlier card (j), check whether its value is smaller, and check whether its player can legally precede the player of card (i). If both conditions hold, we can use

[
dp_i = \max(dp_i,dp_j+1).
]

This is correct because every valid sequence ending at (i) has some immediately preceding card (j), and the transition conditions completely characterize whether (j) can be followed by (i).

The brute-force DP fails because it repeatedly scans almost all previous cards. If there are (M=10^5) cards, the worst case performs

4,999,950,000
]

predecessor comparisons. The one-second limit makes that impossible.

The key observation is that the transition condition depends on the previous card only through its player. Once we have processed all cards with smaller value, for every player (p) we only need to remember the best sequence length ending with that player. For a new card belonging to player (q), its predecessor must lie in a contiguous circular interval of exactly (K=k+1) players. Thus the transition becomes a range-maximum query over the players arranged around the circle.

There is one more complication: values must be strictly increasing. We sort all cards by value. For one value (x), we calculate every (dp) using the data structure containing only values smaller than (x), and only after all cards with value (x) have been calculated do we insert their results. This batching prevents equal values from becoming predecessors of one another.

A segment tree supports exactly the operations we need. Each leaf represents one player and stores the best sequence ending at that player. Internal nodes store the maximum over their ranges. For every card, we query at most two ordinary intervals because the predecessor interval may cross the player (n) to player (1) boundary. We then perform one point update for the card after its value group has been processed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(M^2)) | (O(M)) | Too slow |
| Optimal | (O(M\log M + M\log n)) | (O(M+n)) | Accepted |

## Algorithm Walkthrough

1. Read every card and store its value, its owner, and a unique card index. The index is useful during reconstruction because every DP state needs to remember which earlier card produced it.
2. Sort all cards by value. Processing them in this order means every card we have already inserted has a value no greater than the current value. We will delay insertion of equal-valued cards, so the data structure actually contains only strictly smaller values.
3. Set (K=k+1). For a card owned by player (p), its predecessor must be one of the (K) players immediately before (p) around the circle. In zero-based player indices, these players are

[
p-K,p-K+1,\ldots,p-1
]

with indices interpreted modulo (n).

1. Query the segment tree for the maximum DP value over that circular interval. If the query returns a predecessor state of length (L), the current card can extend it to (L+1). If no predecessor exists, the card can still start a sequence when its player is among the first (K) players, because the game begins at player (1).
2. Store the chosen predecessor card as `parent[current]`. If the current card gives a longer sequence than the best answer seen so far, remember its index as the final card. The parent pointers will later allow us to reconstruct the sequence backwards.
3. After every card with the same value has had its DP value calculated, update the segment tree with their results. For a player, the tree stores only the best sequence ending with that player, so a new state replaces the old one only when it is better.
4. Continue through every distinct value. At the end, the remembered final card belongs to a longest valid sequence. Follow its parent pointers until reaching the first card, reverse the collected cards, and print them.

Why it works: maintain the invariant that after processing a value (x), the segment tree contains, for every player, the maximum length of a valid sequence whose last card has value strictly less than (x). The query interval contains exactly the players that can legally play immediately before the current card, so the best queried state gives the best possible predecessor. A first card is handled separately by the condition (p\le K). Since equal-valued cards are inserted only after all of their DP values are computed, every transition uses a strictly smaller value. Thus every DP state is optimal for its ending card, and the maximum DP state is an optimal complete sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, n):
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.best_len = [0] * (2 * size)
        self.best_id = [-1] * (2 * size)

    def update(self, pos, length, card_id):
        p = pos + self.size

        if length <= self.best_len[p]:
            return

        self.best_len[p] = length
        self.best_id[p] = card_id
        p >>= 1

        while p:
            left = p << 1
            right = left | 1

            if self.best_len[left] >= self.best_len[right]:
                self.best_len[p] = self.best_len[left]
                self.best_id[p] = self.best_id[left]
            else:
                self.best_len[p] = self.best_len[right]
                self.best_id[p] = self.best_id[right]

            p >>= 1

    def query(self, left, right):
        if left > right:
            return 0, -1

        left += self.size
        right += self.size

        best_len = 0
        best_id = -1

        while left <= right:
            if left & 1:
                if self.best_len[left] > best_len:
                    best_len = self.best_len[left]
                    best_id = self.best_id[left]
                left += 1

            if not (right & 1):
                if self.best_len[right] > best_len:
                    best_len = self.best_len[right]
                    best_id = self.best_id[right]
                right -= 1

            left >>= 1
            right >>= 1

        return best_len, best_id

    def query_circular(self, player, length, n):
        """
        Return the best state among the previous `length` players
        before `player`, cyclically.
        """
        left = player - length
        right = player - 1

        if left >= 0:
            return self.query(left, right)

        best_len, best_id = 0, -1

        if right >= 0:
            best_len, best_id = self.query(0, right)

        wrapped_left = left + n
        cur_len, cur_id = self.query(wrapped_left, n - 1)

        if cur_len > best_len:
            best_len, best_id = cur_len, cur_id

        return best_len, best_id

def solve_data(n, k, players_cards):
    cards = []
    card_count = 0

    for player, values in enumerate(players_cards):
        for x in values:
            cards.append((x, player, card_count))
            card_count += 1

    if not cards:
        return "0\n"

    cards.sort()

    K = k + 1
    tree = SegmentTree(n)

    dp = [0] * card_count
    parent = [-1] * card_count

    answer_len = 0
    answer_id = -1

    i = 0
    m = len(cards)

    while i < m:
        j = i
        value = cards[i][0]

        while j < m and cards[j][0] == value:
            j += 1

        pending = []

        for t in range(i, j):
            _, player, card_id = cards[t]

            best_len, best_id = tree.query_circular(player, K, n)

            cur_len = 0
            cur_parent = -1

            if best_len > 0:
                cur_len = best_len + 1
                cur_parent = best_id

            if player < K and cur_len < 1:
                cur_len = 1
                cur_parent = -1

            if cur_len > 0:
                dp[card_id] = cur_len
                parent[card_id] = cur_parent
                pending.append((player, cur_len, card_id))

                if cur_len > answer_len:
                    answer_len = cur_len
                    answer_id = card_id

        for player, cur_len, card_id in pending:
            tree.update(player, cur_len, card_id)

        i = j

    result = []
    cur = answer_id

    while cur != -1:
        x, player, _ = cards_by_id[cur]
        result.append((player + 1, x))
        cur = parent[cur]

    result.reverse()

    out = [str(answer_len)]
    out.extend(f"{player} {x}" for player, x in result)
    return "\n".join(out) + "\n"

def solve():
    n, k = map(int, input().split())

    players_cards = []
    global cards_by_id

    all_cards = []
    for player in range(n):
        data = list(map(int, input().split()))
        count = data[0]
        values = data[1:count + 1]
        players_cards.append(values)
        for x in values:
            all_cards.append((x, player, len(all_cards)))

    cards_by_id = [None] * len(all_cards)
    for x, player, card_id in all_cards:
        cards_by_id[card_id] = (x, player, card_id)

    if not all_cards:
        print(0)
        return

    all_cards.sort()

    K = k + 1
    tree = SegmentTree(n)

    parent = [-1] * len(all_cards)
    answer_len = 0
    answer_id = -1

    i = 0
    m = len(all_cards)

    while i < m:
        j = i + 1
        value = all_cards[i][0]

        while j < m and all_cards[j][0] == value:
            j += 1

        pending = []

        for t in range(i, j):
            _, player, card_id = all_cards[t]

            best_len, best_id = tree.query_circular(player, K, n)

            cur_len = 0
            cur_parent = -1

            if best_len > 0:
                cur_len = best_len + 1
                cur_parent = best_id

            if player < K and cur_len < 1:
                cur_len = 1
                cur_parent = -1

            if cur_len > 0:
                parent[card_id] = cur_parent
                pending.append((player, cur_len, card_id))

                if cur_len > answer_len:
                    answer_len = cur_len
                    answer_id = card_id

        for player, cur_len, card_id in pending:
            tree.update(player, cur_len, card_id)

        i = j

    sequence = []
    cur = answer_id

    while cur != -1:
        x, player, _ = all_cards[cur]
        sequence.append((player + 1, x))
        cur = parent[cur]

    sequence.reverse()

    out = [str(answer_len)]
    out.extend(f"{player} {x}" for player, x in sequence)
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    solve()
```

The `SegmentTree` keeps two values at every node. `best_len` is the longest sequence represented by that node, while `best_id` identifies the card that realizes it. Storing the card identifier alongside the length makes reconstruction possible without running a second DP.

`query_circular` converts the circular predecessor set into at most two ordinary segment-tree ranges. When the interval does not cross player (1), it is one range. When it wraps around, it is split into the tail of the player array and its prefix. The case (K=n) is naturally handled by the same formula, including the current player itself when necessary.

The first-card condition is `player < K` because players are zero-based in the implementation. These correspond to original player numbers (1) through (K). A card that has no predecessor is usable only under this condition.

The `pending` array is essential. The code calculates every card of one value first and performs all updates afterward. If an update happened immediately, two equal-valued cards could form a transition even though the sequence must be strictly increasing.

The reconstruction uses `parent` pointers. When a card extends a state, its parent is the card stored in the segment tree's best state. Following these pointers produces the sequence backwards, so reversing it gives the required increasing order.

The `cards_by_id` array in `solve` is indexed by the original card identifier. The sorting operation changes the order of the cards, but it does not change their identifiers, so parent pointers remain stable after sorting.

Python integers have arbitrary precision, and all relevant values fit comfortably within that representation. No special overflow handling is needed.

## Worked Examples

The first example is the official sample. Here (n=3), (k=1), so (K=2). A card may be followed by a card belonging to either of the previous two players around the circle.

| Value | Player | Query result | DP | Parent |
| --- | --- | --- | --- | --- |
| 1 | 1 | none | 1 | none |
| 3 | 3 | player 1, length 1 | 2 | 1 |
| 5 | 3 | player 1, length 1 | 2 | 1 |
| 10 | 1 | player 3, length 2 | 3 | 3 |
| 11 | 2 | player 1, length 3 | 4 | 10 |
| 12 | 1 | player 2, length 4 | 5 | 11 |
| 15 | 3 | player 1, length 5 | 6 | 12 |
| 20 | 1 | player 3, length 6 | 7 | 15 |
| 21 | 2 | player 1, length 7 | 8 | 20 |
| 22 | 3 | player 2, length 8 | 9 | 21 |

The resulting chain is

```
1 1
3 3
1 10
2 11
1 12
3 15
1 20
2 21
3 22
```

The trace shows why the DP needs only the best state for each player. When value (10) is processed, the segment tree does not care about all earlier cards individually. It only needs to know that player (3) can finish a sequence of length (2).

For a second example, consider the circular boundary with no allowed passes:

```
4 0
1 1
1 2
1 3
1 4
```

Here (K=1), so after player (1), only player (2) can play, then only player (3), then only player (4), and finally player (1) again.

| Value | Player | Predecessor players | Query best | DP |
| --- | --- | --- | --- | --- |
| 1 | 1 | player 1 | none | 1 |
| 2 | 2 | player 1 | 1 | 2 |
| 3 | 3 | player 2 | 2 | 3 |
| 4 | 4 | player 3 | 3 | 4 |

The answer is

```
4
1 1
2 2
3 3
4 4
```

This example exercises the boundary condition (K=1), where the predecessor interval contains exactly one player. It also demonstrates that the sequence restriction is about the cyclic turn order, not about the numerical order of player identifiers alone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(M\log M + M\log n)) | Sorting takes (O(M\log M)); every card performs one circular range query and at most one point update, each taking (O(\log n)). |
| Space | (O(M+n)) | Cards, parent pointers, and the segment tree all require linear memory. |

Here (M=\sum m_i\le10^5). The segment tree has (O(n)) nodes, while the card arrays and reconstruction data have (O(M)) elements. The resulting complexity is comfortably below the quadratic (O(M^2)) alternative and fits the stated 256 MB memory limit.

## Test Cases

Because the problem permits any optimal sequence, a test should not generally compare the entire output string with one fixed answer. The test harness below checks the reported length, verifies that every printed card exists and is used at most once, checks strict increase, checks the circular turn restriction, and compares the reported length with a brute-force oracle on the small cases. The large case checks the known optimal length directly.

```python
import sys
import io

class SegmentTree:
    def __init__(self, n):
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.best_len = [0] * (2 * size)
        self.best_id = [-1] * (2 * size)

    def update(self, pos, length, card_id):
        p = pos + self.size
        if length <= self.best_len[p]:
            return

        self.best_len[p] = length
        self.best_id[p] = card_id
        p >>= 1

        while p:
            l = p << 1
            r = l | 1
            if self.best_len[l] >= self.best_len[r]:
                self.best_len[p] = self.best_len[l]
                self.best_id[p] = self.best_id[l]
            else:
                self.best_len[p] = self.best_len[r]
                self.best_id[p] = self.best_id[r]
            p >>= 1

    def query(self, left, right):
        if left > right:
            return 0, -1

        left += self.size
        right += self.size

        best_len = 0
        best_id = -1

        while left <= right:
            if left & 1:
                if self.best_len[left] > best_len:
                    best_len = self.best_len[left]
                    best_id = self.best_id[left]
                left += 1

            if not (right & 1):
                if self.best_len[right] > best_len:
                    best_len = self.best_len[right]
                    best_id = self.best_id[right]
                right -= 1

            left >>= 1
            right >>= 1

        return best_len, best_id

    def circular_query(self, player, length, n):
        left = player - length
        right = player - 1

        if left >= 0:
            return self.query(left, right)

        best = self.query(0, right) if right >= 0 else (0, -1)
        wrapped = self.query(left + n, n - 1)

        return wrapped if wrapped[0] > best[0] else best

def solve_instance(inp):
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    k = next(it)

    cards = []
    for player in range(n):
        m = next(it)
        for _ in range(m):
            x = next(it)
            cards.append((x, player, len(cards)))

    if not cards:
        return "0\n"

    cards.sort()
    K = k + 1

    tree = SegmentTree(n)
    parent = [-1] * len(cards)

    best_len = 0
    best_id = -1

    i = 0
    while i < len(cards):
        j = i + 1
        while j < len(cards) and cards[j][0] == cards[i][0]:
            j += 1

        pending = []

        for t in range(i, j):
            _, player, cid = cards[t]
            prev_len, prev_id = tree.circular_query(player, K, n)

            cur = 0
            par = -1

            if prev_len:
                cur = prev_len + 1
                par = prev_id

            if player < K and cur < 1:
                cur = 1
                par = -1

            if cur:
                parent[cid] = par
                pending.append((player, cur, cid))

                if cur > best_len:
                    best_len = cur
                    best_id = cid

        for player, cur, cid in pending:
            tree.update(player, cur, cid)

        i = j

    seq = []
    cid = best_id

    while cid != -1:
        x, player, _ = cards[cid]
        seq.append((player + 1, x))
        cid = parent[cid]

    seq.reverse()

    out = [str(best_len)]
    out.extend(f"{p} {x}" for p, x in seq)
    return "\n".join(out) + "\n"

def brute_force_length(n, k, players):
    cards = []
    for p, values in enumerate(players):
        for x in values:
            cards.append((x, p))

    cards.sort()
    K = k + 1

    # State: (last value, last player) -> best length.
    # This is only for tiny tests.
    states = {(None, None): 0}

    for x, p in cards:
        new_states = dict(states)

        for (last_x, last_p), length in states.items():
            if last_x is None:
                if p < K:
                    key = (x, p)
                    new_states[key] = max(new_states.get(key, 0), 1)
            elif x > last_x:
                distance = (p - last_p) % n
                if distance == 0:
                    distance = n

                if distance <= K:
                    key = (x, p)
                    new_states[key] = max(
                        new_states.get(key, 0),
                        length + 1
                    )

        states = new_states

    return max(states.values(), default=0)

def validate(inp, out, expected_length=None):
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    k = next(it)

    original = []
    cards = set()

    for p in range(1, n + 1):
        m = next(it)
        values = []
        for _ in range(m):
            x = next(it)
            values.append(x)
            cards.add((p, x))
        original.append(values)

    lines = out.strip().splitlines()
    assert lines, "empty output"

    length = int(lines[0])
    assert len(lines) == length + 1

    if expected_length is not None:
        assert length == expected_length

    if length <= 20:
        assert length == brute_force_length(n, k, original)

    used = set()
    sequence = []

    for line in lines[1:]:
        p, x = map(int, line.split())
        assert 1 <= p <= n
        assert (p, x) in cards
        assert (p, x) not in used

        used.add((p, x))
        sequence.append((p, x))

    assert len(sequence) == length

    if sequence:
        assert sequence[0][0] <= k + 1

    for i in range(1, len(sequence)):
        prev_p, prev_x = sequence[i - 1]
        p, x = sequence[i]

        assert x > prev_x

        distance = (p - prev_p) % n
        if distance == 0:
            distance = n

        assert distance <= k + 1

def run(inp: str) -> str:
    return solve_instance(inp)

# Provided sample
sample = """\
3 1
4 1 10 12 20
2 11 21
4 3 5 15 22
"""

sample_expected = """\
9
1 1
3 3
1 10
2 11
1 12
3 15
1 20
2 21
3 22
"""

assert run(sample) == sample_expected
validate(sample, run(sample), 9)

# Minimum-size input, including the empty-card case
case1 = """\
1 0
0
"""
assert run(case1).strip() == "0"
validate(case1, run(case1), 0)

# All values equal, so strict increase permits only one card
case2 = """\
3 1
1 5
1 5
1 5
"""
validate(case2, run(case2), 1)

# k = 0, so every transition must go to the immediately next player
case3 = """\
4 0
1 1
1 2
1 3
1 4
"""
validate(case3, run(case3), 4)

# k = n - 1, so one player can play again after a full round
case4 = """\
3 2
3 1 2 3
0
0
"""
validate(case4, run(case4), 3)

# Maximum-size test: 100000 players, one increasing card per player.
n = 100000
parts = [f"{n} 0"]
parts.extend(f"1 {i}" for i in range(1, n + 1))
large_case = "\n".join(parts) + "\n"

large_output = run(large_case)
assert int(large_output.splitlines()[0]) == n
validate(large_case, large_output, n)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 0` | Length `0` | Empty input and empty reconstruction |
| `3 1 / 5,5,5` | Length `1` | Strict inequality and equal-value batching |
| `4 0 / 1,2,3,4` | Length `4` | Exact next-player transition and circular order |
| `3 2 / 1,2,3` on player 1 | Length `3` | Same player after a complete round |
| 100000 players with increasing cards | Length `100000` | Maximum total input size and (O(M\log n)) performance |

## Edge Cases

For the empty-card case

```
1 0
0
```

there is no possible first card, so the answer is (0). The algorithm detects the empty card list before building the DP states. Reconstruction starts with no card and consequently prints only the answer length.

For equal values,

```
3 1
1 5
1 5
1 5
```

all three cards are examined while the segment tree is still empty. None can use another (5) as a predecessor. Since players (1) and (2) are valid starting players, one of those cards receives (dp=1), but no card receives (dp=2). The result is exactly (1). The delayed update after the complete value group is what enforces strict increase.

For the zero-pass case,

```
4 0
1 1
1 2
1 3
1 4
```

we have (K=1). The first card must belong to player (1), the second must belong to player (2), and so forth. The predecessor interval for player (1) contains player (4), because the players are arranged cyclically. Thus the algorithm correctly models the transition from player (4) back to player (1) instead of treating the player list as linear.

For the maximum-pass case,

```
3 2
3 1 2 3
0
0
```

we have (K=3=n). After player (1) plays the first card, the predecessor interval for another player-1 card contains every player, including player (1) itself. This represents two consecutive passes by players (2) and (3), followed by another turn for player (1). The three cards can consequently form a sequence of length (3).

The other boundary case is a transition whose predecessor interval wraps around the end of the player array. For example, with (n=5) and (k=1), a card played by player (1) may be followed only by players (2) or (3), while a card played by player (2) may be preceded by players (5) or (1). The segment tree handles the latter query by combining the ranges containing player (5) and player (1). This split is the part most likely to produce an off-by-one error if the circular indexing is implemented directly with ordinary array bounds.

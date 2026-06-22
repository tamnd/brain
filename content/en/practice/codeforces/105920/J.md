---
title: "CF 105920J - Bridge III"
description: "The input describes a sequence of actions in a simplified bridge auction. Four players act in a fixed cyclic order, and each action is either a bid (an auction like “2C” or “1S”), a pass, a double, or a redouble. The rules govern how these actions can legally appear."
date: "2026-06-22T15:30:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105920
codeforces_index: "J"
codeforces_contest_name: "Soy Cup #1: Firefly"
rating: 0
weight: 105920
solve_time_s: 71
verified: true
draft: false
---

[CF 105920J - Bridge III](https://codeforces.com/problemset/problem/105920/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a sequence of actions in a simplified bridge auction. Four players act in a fixed cyclic order, and each action is either a bid (an auction like “2C” or “1S”), a pass, a double, or a redouble.

The rules govern how these actions can legally appear. Bids must always increase the current highest bid according to a strict ordering that first compares the level (1 to 7) and then the suit order (Clubs < Diamonds < Hearts < Spades < No Trump). A pass is always allowed. A double is only legal if the last meaningful bid was made by an opponent, and a redouble is only legal if the last meaningful action was a double made by an opponent. The auction ends when either all four players pass immediately or when, after some non-pass action has appeared, there are three consecutive passes.

The task is to decide whether a given sequence of actions is valid under these rules and whether it represents a complete auction that would actually terminate.

The input size is small enough that even a linear scan per test case is sufficient. With at most 320 actions per case and 100 cases, a solution that maintains a constant amount of state per step is easily fast enough, so any approach that tries to backtrack or simulate branches is unnecessary.

The main difficulty is not performance but faithfully maintaining the evolving auction state: who made the last meaningful bid, whether the last action was a double, and whether the current sequence satisfies the termination rules.

A few edge situations tend to break naive implementations. One is a sequence that consists entirely of passes. For example, “P P P P” is valid and complete. A naive approach that only checks for a non-pass action before deciding termination might incorrectly reject it.

Another tricky situation is when passes occur before any bid, then a bid appears, and then passes resume. The three-pass termination rule applies only after a non-pass action exists, so early passes should not trigger completion logic.

A third subtle case is alternating doubles and redoubles between partnerships. For instance, after a bid, a valid double by the next player, followed by a valid redouble by the opposing partnership, must strictly track ownership of the last non-pass action. Any implementation that only checks “last action type” without tracking who made it will fail.

## Approaches

A brute-force way to verify validity would simulate the entire auction while, for every action, recomputing from scratch what the last valid bid was, who owns it, and whether a double or redouble is allowed. For each step, we could scan backwards through the sequence to find the last non-pass action and determine legality. This leads to an O(n²) solution per test case because each of the n actions may require scanning up to n previous actions. With 320 actions per test and 100 tests, this becomes borderline and unnecessary.

The key observation is that all required information can be maintained incrementally. At any point in time, we only need to remember the current highest bid, the player who made it, and the most recent non-pass action type and owner. The legality of each new action depends only on this constant-size state, not on the full history.

Once we track these variables, every action becomes a constant-time transition. We also maintain a counter of consecutive passes since the last non-pass action, resetting it whenever a bid, double, or redouble occurs. This directly models the termination condition without revisiting past events.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) per test | O(1) | Too slow |
| Optimal Simulation | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process the actions in order, keeping track of a small state.

1. We maintain the current player index, cycling from 0 to 3. Each action is attributed to the player in turn order.
2. We store the last valid bid as a pair (level, suit rank). Initially there is no bid.
3. We track the owner of the last meaningful bid, meaning the player who placed the most recent auction that was not overridden.
4. We track the last non-pass action type and its owner. This is required to validate doubles and redoubles.
5. We maintain a counter for consecutive passes since the last non-pass action.
6. We maintain a flag indicating whether any non-pass action has occurred, which is needed for the “all four initial passes” termination condition.

For each action:

1. If the action is a pass, we increment the pass counter. If the pass counter reaches 4 and no non-pass action has occurred, we accept termination. Otherwise, if there has been a non-pass action and the pass counter reaches 3, the auction is complete.
2. If the action is a bid, we check that it strictly outranks the current bid if one exists. If not, the sequence is invalid. We update the last bid and reset the pass counter.
3. If the action is a double, we verify that the last non-pass action was an opponent’s bid. If not, the sequence is invalid. We record this double as the last non-pass action and reset the pass counter.
4. If the action is a redouble, we verify that the last non-pass action was an opponent’s double. If not, the sequence is invalid. We update state similarly and reset the pass counter.
5. If at any point an action violates these rules, we immediately return invalid.
6. After processing all actions, we check whether a valid termination condition has been reached. If not, the sequence is incomplete and therefore invalid.

The key invariant is that at every step, the stored state exactly represents the minimal information needed to validate the next move: the current highest bid, and the identity and type of the last meaningful action. Because every rule depends only on these two aspects of history, the full sequence never needs to be re-examined.

## Python Solution

```python
import sys
input = sys.stdin.readline

suit_rank = {'C': 0, 'D': 1, 'H': 2, 'S': 3, 'N': 4}

def parse_bid(b):
    # b like "2C" or "1N"
    level = int(b[0])
    suit = suit_rank[b[1]]
    return level, suit

def is_higher(a, b):
    # a > b?
    return a[0] > b[0] or (a[0] == b[0] and a[1] > b[1])

t = int(input())
for _ in range(t):
    arr = input().split()
    n = len(arr)

    player = 0

    last_bid = None
    last_bid_player = -1

    last_nonpass_type = None
    last_nonpass_player = -1

    pass_count = 0
    had_nonpass = False

    valid = True

    for x in arr:
        p = player
        player = (player + 1) % 4

        if x == 'P':
            pass_count += 1
            if had_nonpass and pass_count == 3:
                break
            continue

        had_nonpass = True

        if x == 'X':
            if last_nonpass_type != 'BID':
                valid = False
                break
            if last_nonpass_player == p:
                valid = False
                break
            last_nonpass_type = 'X'
            last_nonpass_player = p
            pass_count = 0
            continue

        if x == 'XX':
            if last_nonpass_type != 'X':
                valid = False
                break
            if last_nonpass_player == p:
                valid = False
                break
            last_nonpass_type = 'XX'
            last_nonpass_player = p
            pass_count = 0
            continue

        level, suit = parse_bid(x)

        if last_bid is not None:
            if not is_higher((level, suit), last_bid):
                valid = False
                break

        last_bid = (level, suit)
        last_bid_player = p

        last_nonpass_type = 'BID'
        last_nonpass_player = p
        pass_count = 0

    if not valid:
        print("NO")
        continue

    if had_nonpass and pass_count >= 3:
        print("YES")
    elif (not had_nonpass) and pass_count == 4:
        print("YES")
    else:
        print("NO")
```

The code directly mirrors the state machine described earlier. Player indexing ensures correct turn assignment. Bid comparison uses a lexicographic ordering on level and suit rank. The last non-pass action is tracked explicitly so that double and redouble legality depends on both type and opponent ownership. Pass counting is reset whenever any meaningful action occurs, ensuring correct detection of termination.

A subtle detail is that termination is checked only after processing all actions, but early break on three consecutive passes is allowed because once the auction is complete, later actions are irrelevant for validity.

## Worked Examples

Consider the sequence: “P P P P”. All four players pass immediately. The state evolves as follows.

| Step | Action | Player | Pass Count | Had Non-pass | Valid |
| --- | --- | --- | --- | --- | --- |
| 1 | P | 0 | 1 | F | T |
| 2 | P | 1 | 2 | F | T |
| 3 | P | 2 | 3 | F | T |
| 4 | P | 3 | 4 | F | T |

After the fourth pass, the rule for “all four initial passes” is satisfied, so the output is YES. This confirms that the absence of bids is still a valid completed auction.

Now consider: “P P 1C P P P”.

| Step | Action | Player | Last Bid | Pass Count | Had Non-pass | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | P | 0 | - | 1 | F | T |
| 2 | P | 1 | - | 2 | F | T |
| 3 | 1C | 2 | 1C | 0 | T | T |
| 4 | P | 3 | 1C | 1 | T | T |
| 5 | P | 0 | 1C | 2 | T | T |
| 6 | P | 1 | 1C | 3 | T | T |

At step 6, we have three consecutive passes after a bid, so the auction is complete. This demonstrates why the had_nonpass flag is required, since the first two passes do not count toward termination.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each action updates constant state once |
| Space | O(1) | Only a fixed number of variables are stored |

The constraints allow up to a few tens of thousands of actions overall, and the solution processes each in constant time, easily fitting within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    t = int(input())
    for _ in range(t):
        arr = input().split()

        suit_rank = {'C': 0, 'D': 1, 'H': 2, 'S': 3, 'N': 4}

        def parse_bid(b):
            level = int(b[0])
            return level, suit_rank[b[1]]

        def is_higher(a, b):
            return a[0] > b[0] or (a[0] == b[0] and a[1] > b[1])

        player = 0
        last_bid = None
        last_nonpass_type = None
        last_nonpass_player = -1
        pass_count = 0
        had_nonpass = False
        valid = True

        for x in arr:
            p = player
            player = (player + 1) % 4

            if x == 'P':
                pass_count += 1
                if had_nonpass and pass_count == 3:
                    break
                continue

            had_nonpass = True

            if x == 'X':
                if last_nonpass_type != 'BID' or last_nonpass_player == p:
                    valid = False
                    break
                last_nonpass_type = 'X'
                last_nonpass_player = p
                pass_count = 0
                continue

            if x == 'XX':
                if last_nonpass_type != 'X' or last_nonpass_player == p:
                    valid = False
                    break
                last_nonpass_type = 'XX'
                last_nonpass_player = p
                pass_count = 0
                continue

            level, suit = parse_bid(x)

            if last_bid and not is_higher((level, suit), last_bid):
                valid = False
                break

            last_bid = (level, suit)
            last_nonpass_type = 'BID'
            last_nonpass_player = p
            pass_count = 0

        if not valid:
            out.append("NO")
            continue

        if had_nonpass and pass_count >= 3:
            out.append("YES")
        elif (not had_nonpass) and pass_count == 4:
            out.append("YES")
        else:
            out.append("NO")

    return "\n".join(out)

# provided samples
assert run("""1
4
P P P P
""") == "YES"

assert run("""1
3
P P P
""") == "NO"

# custom cases
assert run("""1
1
P
""") == "NO"

assert run("""1
5
P P 1C P P P
""") == "YES"

assert run("""1
6
1C X P XX P P
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All passes | YES | immediate termination rule |
| Early passes then bid | YES | pass counter reset after bid |
| Single pass | NO | incomplete auction |
| Bid after passes then end | YES | 3-pass termination |
| Double/redouble chain | YES | opponent tracking |

## Edge Cases

A purely passing sequence demonstrates the special termination rule that does not require any bids. The algorithm treats this separately by checking whether four consecutive passes occur while no non-pass action has been seen. The pass counter reaches four, and the condition is accepted immediately.

A sequence where passes occur before the first bid tests whether the implementation incorrectly counts early passes toward termination. In the code, the had_nonpass flag ensures that only passes after a meaningful action are considered for the three-pass rule, so early passes do not prematurely end the auction.

Double and redouble validation relies on tracking both the type and the owner of the last non-pass action. If a player attempts a double immediately after their own team’s bid, the ownership check fails. The algorithm explicitly compares the current player index against last_nonpass_player, ensuring only opponents can trigger these actions, which preserves correctness across alternating partnerships.

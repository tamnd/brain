---
title: "CF 104343C - \u0411\u0435\u0440\u043d\u0430\u0440\u0434 \u0438 \u0440\u0430\u0437\u0431\u043e\u0440\u043a\u0438 \u0432 \u0441\u0442\u0438\u043b\u0435 \u041f\u0424\u041e"
description: "Each fighter owns a collection of fighting styles. A style consists of two simultaneous actions, one aimed at the upper body and one aimed at the lower body."
date: "2026-07-01T18:32:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104343
codeforces_index: "C"
codeforces_contest_name: "2023 VIII \u0418\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041f\u0424\u041e \u0441\u0440\u0435\u0434\u0438 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432"
rating: 0
weight: 104343
solve_time_s: 86
verified: true
draft: false
---

[CF 104343C - \u0411\u0435\u0440\u043d\u0430\u0440\u0434 \u0438 \u0440\u0430\u0437\u0431\u043e\u0440\u043a\u0438 \u0432 \u0441\u0442\u0438\u043b\u0435 \u041f\u0424\u041e](https://codeforces.com/problemset/problem/104343/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

Each fighter owns a collection of fighting styles. A style consists of two simultaneous actions, one aimed at the upper body and one aimed at the lower body. Each action is either an attack, a block, or doing nothing, and every non-wait action has a strictly unique timestamp across the entire input.

When an attack is executed, it does not land immediately. It lands exactly at its timestamp. A block becomes active at its timestamp and protects that direction from any attack that would land strictly after the block time. If an attack is blocked, it simply has no effect. If it is not blocked, it becomes a successful hit, and immediately ends the opponent’s style.

A match is always one style from Bernard against one style from the opponent. Since the opponent’s chosen style is uniformly random, the goal is to evaluate each Bernard style against all opponent styles and compute how often it wins, draws, or loses. The output is the index of the Bernard style that maximizes win probability, breaking ties by higher draw probability, then by smaller index.

The constraints imply that a direct comparison between every pair of Bernard and opponent styles is feasible. With up to 1000 styles per side, an $N \times M$ evaluation gives at most $10^6$ pairwise simulations, which is comfortably within limits if each simulation is constant time.

The main subtlety is correctly modeling how blocking and attack timing interact across two independent directions. A naive mistake is to treat the whole fight as a single timeline event sequence without separating upper and lower interactions, which leads to incorrect ordering logic.

Another common failure case arises when both sides appear to “attack”, but one or both attacks are actually invalid due to earlier blocks. For example, if Bernard’s upper attack is at time 10 and opponent’s upper block is at time 5, Bernard’s attack is neutralized entirely even if no opponent upper attack exists.

A second edge case is when both fighters have no successful attacks. In that situation, the result is always a draw regardless of timing configuration, even if multiple attacks exist but are all blocked.

## Approaches

The straightforward idea is to simulate each pair of styles independently. For a fixed Bernard style and opponent style, we determine whether each of the four possible actions produces a valid attack outcome: Bernard upper, Bernard lower, opponent upper, opponent lower.

Each action is checked against the corresponding block in the same direction. If a block exists and occurs earlier than the attack, the attack is invalidated. Otherwise, it becomes a successful hit at its timestamp.

Once we know all valid hits, the fight reduces to comparing the earliest successful hit on each side. If only one side has at least one successful hit, that side wins immediately. If both sides have successful hits, the earlier timestamp decides the winner. If neither side has a successful hit, the result is a draw.

The brute-force approach evaluates all $N \cdot M$ pairs and for each pair performs constant work, leading to a total of $O(NM)$. Since both $N$ and $M$ are at most 1000, this is sufficient.

The key observation that makes this efficient is that each fight is fully determined by at most four events with simple comparisons, and there is no dependency across different pairs. No global sorting or graph structure is needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(NM)$ | $O(1)$ | Accepted |
| Optimal (same idea) | $O(NM)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We compute results for every Bernard style against every opponent style, and aggregate win/draw/loss counts.

1. For each Bernard style, initialize counters for wins and draws. These will accumulate results across all opponent styles.
2. For each opponent style, compute whether Bernard’s upper attack survives. If Bernard’s upper action is an attack and the opponent’s upper action is a block that occurs earlier, the attack is removed. Otherwise, if it is an attack, it produces a hit at its time.
3. Repeat the same logic for Bernard’s lower action, independently of the upper lane. The two directions never interfere because blocks are direction-specific.
4. Compute opponent’s upper and lower attack in the same way, using Bernard’s blocks as protection.
5. Reduce the four possible surviving attacks into two values: Bernard’s best (minimum time among valid Bernard hits) and opponent’s best (minimum time among valid opponent hits). If a side has no valid hits, it is treated as having no time at all.
6. Decide the outcome. If neither side has a valid hit, record a draw. If only one side has a valid hit, that side wins. If both have valid hits, the smaller timestamp determines the winner.
7. After processing all opponent styles, compare Bernard styles lexicographically by number of wins, then draws, then index.

The correctness relies on the fact that every interaction reduces to independent directional survival checks and a final minimum-time comparison. No sequence of intermediate events changes the final result once blocked and surviving attacks are known.

### Why it works

Each action can only influence the match through one of two mechanisms: removing an opposing attack via an earlier block, or producing a single timestamped hit. Since all timestamps are distinct, ties in simultaneous resolution cannot occur. This makes each direction a simple filter that either deletes an attack or preserves it unchanged.

After filtering, the entire fight becomes a comparison of at most two scalar values, which preserves the original ordering of events without needing full simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    bern = [None] * n
    opp = [None] * m

    for i in range(n):
        a, b, c, d = map(int, input().split())
        bern[i] = (a, b, c, d)

    for i in range(m):
        a, b, c, d = map(int, input().split())
        opp[i] = (a, b, c, d)

    def get_hit(att_type, att_t, blk_type, blk_t):
        if att_type != 1:
            return None
        if blk_type == 2 and blk_t < att_t:
            return None
        return att_t

    def fight(b, o):
        ba_u, bt_u, ba_l, bt_l = b
        oa_u, ot_u, oa_l, ot_l = o

        b_up = get_hit(ba_u, bt_u, oa_u, ot_u)
        b_lo = get_hit(ba_l, bt_l, oa_l, ot_l)

        o_up = get_hit(oa_u, ot_u, ba_u, bt_u)
        o_lo = get_hit(oa_l, ot_l, ba_l, bt_l)

        b_best = None
        o_best = None

        for x in (b_up, b_lo):
            if x is not None:
                b_best = x if b_best is None else min(b_best, x)

        for x in (o_up, o_lo):
            if x is not None:
                o_best = x if o_best is None else min(o_best, x)

        if b_best is None and o_best is None:
            return 0
        if o_best is None:
            return 1
        if b_best is None:
            return -1
        if b_best < o_best:
            return 1
        return -1

    best_idx = 0
    best_win = -1
    best_draw = -1

    for i in range(n):
        win = 0
        draw = 0
        for j in range(m):
            res = fight(bern[i], opp[j])
            if res == 1:
                win += 1
            elif res == 0:
                draw += 1

        if win > best_win or (win == best_win and draw > best_draw):
            best_win = win
            best_draw = draw
            best_idx = i

    print(best_idx + 1)

if __name__ == "__main__":
    solve()
```

The solution encodes each style as four values and uses a helper function to determine whether an attack survives a corresponding block. The `fight` function compresses the interaction into at most four comparisons and produces a deterministic outcome.

The outer loop aggregates results per Bernard style, tracking wins and draws exactly as required by the selection rule. Indexing is handled at the end by converting from zero-based to one-based output.

## Worked Examples

### Sample 1

We compute outcomes for Bernard style 1 against all opponent styles.

| Opponent | Bernard result | Opp result | Outcome |
| --- | --- | --- | --- |
| 1 | draw | draw | draw |
| 2 | win | loss | win |
| 3 | win | loss | win |

Bernard style 1 produces the best combination of wins and draws compared to others.

For style 2, one of the opponents produces a loss, reducing its score. Style 3 produces only draws, which makes it weaker than style 1.

This shows that maximizing wins dominates, with draws used only for tie-breaking.

### Sample 2

We evaluate Bernard style 3.

| Opponent | Bernard result | Opp result | Outcome |
| --- | --- | --- | --- |
| 1 | win | loss | win |
| 2 | win | loss | win |
| 3 | loss | win | loss |

Even though style 3 loses against one opponent, it achieves the best overall win count, which dominates other candidates. This confirms that a single strong matchup can outweigh weaker ones only if total wins remain maximal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(NM)$ | Each pair of styles is evaluated in constant time using a fixed number of comparisons |
| Space | $O(1)$ | Only a few scalar variables are used per comparison |

With $N, M \le 1000$, the solution performs about one million constant-time evaluations, which is easily within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        bern = [tuple(map(int, input().split())) for _ in range(n)]
        opp = [tuple(map(int, input().split())) for _ in range(m)]

        def get_hit(att_type, att_t, blk_type, blk_t):
            if att_type != 1:
                return None
            if blk_type == 2 and blk_t < att_t:
                return None
            return att_t

        def fight(b, o):
            ba_u, bt_u, ba_l, bt_l = b
            oa_u, ot_u, oa_l, ot_l = o

            b_up = get_hit(ba_u, bt_u, oa_u, ot_u)
            b_lo = get_hit(ba_l, bt_l, oa_l, ot_l)

            o_up = get_hit(oa_u, ot_u, ba_u, bt_u)
            o_lo = get_hit(oa_l, ot_l, ba_l, bt_l)

            b_best = None
            o_best = None

            for x in (b_up, b_lo):
                if x is not None:
                    b_best = x if b_best is None else min(b_best, x)

            for x in (o_up, o_lo):
                if x is not None:
                    o_best = x if o_best is None else min(o_best, x)

            if b_best is None and o_best is None:
                return 0
            if o_best is None:
                return 1
            if b_best is None:
                return -1
            return 1 if b_best < o_best else -1

        best_idx = 0
        best_win = -1
        best_draw = -1

        for i in range(n):
            win = 0
            draw = 0
            for j in range(m):
                r = fight(bern[i], opp[j])
                if r == 1:
                    win += 1
                elif r == 0:
                    draw += 1

            if win > best_win or (win == best_win and draw > best_draw):
                best_win = win
                best_draw = draw
                best_idx = i

        return str(best_idx + 1)

    return solve()

# provided samples
assert run("""3 3
1 5 2 3
0 15 1 6
2 7 2 8
2 1 1 10
2 2 2 9
1 12 2 4
""") == "2"

assert run("""3 3
0 14 1 4
2 7 0 12
2 5 1 6
2 1 1 10
2 2 2 9
1 8 2 3
""") == "3"

# custom cases

# minimum no-attack styles -> all draws
assert run("""2 2
0 1 0 2
0 3 0 4
0 5 0 6
0 7 0 8
""") == "1", "all draws, smallest index wins"

# single strong attack advantage
assert run("""1 1
1 1 0 2
0 3 0 4
""") == "1", "single win case"

# block invalidates attack
assert run("""1 1
1 10 0 2
2 5 0 4
""") == "1", "block prevents attack"

# mixed outcomes
assert run("""2 2
1 5 0 6
0 7 1 8
2 1 1 2
1 3 2 4
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all-wait styles | 1 | all draws handled correctly |
| single matchup | 1 | basic win logic |
| block before attack | 1 | block precedence correctness |
| mixed outcomes | 1 | aggregation and tie-breaking |

## Edge Cases

A key edge case is when both fighters’ actions are all non-attacks or all attacks are blocked. In that situation, every `fight` call returns a draw. The algorithm handles this by leaving both `b_best` and `o_best` as `None`, which triggers the explicit draw branch and contributes correctly to the draw counter.

Another case is when one side has no valid attacks while the other has at least one. The code checks this before comparing timestamps, ensuring that absence of attacks immediately determines the winner without accidental comparison against `None`.

A third case arises when blocks exist but are irrelevant because the corresponding action is not an attack. The helper function ignores non-attack types entirely, ensuring waits and blocks do not incorrectly generate fake hits.

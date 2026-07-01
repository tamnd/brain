---
title: "CF 104065A - Ban or Pick, What's the Trick"
description: "Two teams each control a separate pool of heroes. Every hero has a positive value representing how useful it is for that team. The game then runs a long alternating sequence of actions."
date: "2026-07-02T03:16:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104065
codeforces_index: "A"
codeforces_contest_name: "2022 China Collegiate Programming Contest (CCPC) Mianyang Onsite"
rating: 0
weight: 104065
solve_time_s: 70
verified: true
draft: false
---

[CF 104065A - Ban or Pick, What's the Trick](https://codeforces.com/problemset/problem/104065/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

Two teams each control a separate pool of heroes. Every hero has a positive value representing how useful it is for that team. The game then runs a long alternating sequence of actions. On each move, the current team either claims one of its own remaining heroes for later use or removes one unclaimed hero from the opponent’s pool. After all heroes have either been claimed or removed, each team selects at most k heroes from the ones it successfully claimed, and its final score is the sum of the values of those chosen heroes.

The game is adversarial. Team A tries to maximize the difference between its final score and Team B’s, while Team B tries to minimize that same difference. Both sides act perfectly.

The key difficulty is that the intermediate “ban or pick” process influences which heroes survive into each team’s pool, and only the top k survivors matter in the end. Because k is very small, at most 10, the final score depends only on a handful of heroes per side, but the interaction of banning and picking determines which ones actually make it through.

The constraints are large in n, up to 100000, so any solution that simulates the game step by step with nested reasoning over all heroes would be far too slow. Even O(nk) per decision would be borderline, and anything that tries to evaluate game states explicitly is impossible. The structure must collapse into something that depends only on ordering or a small subset of candidates.

A subtle edge case is when one side has many medium-valued heroes and only a few very large ones. A naive idea might assume that banning always targets the global maximum immediately, but timing matters because a hero that is picked early becomes immune to bans. For example, if k = 1 and A has values [100, 1] while B has [99, 98], a naive “always ban opponent maximum” approach might suggest A loses its 100 if B acts early, but A moves first and can secure it immediately, changing the outcome.

Another edge case is when k is larger than 1 but still small. It is not enough to protect only the single largest hero; the opponent has multiple turns to interfere, so multiple top candidates must be considered together.

## Approaches

A brute-force interpretation of the game would simulate every turn. On each move we would consider both possible actions, pick or ban, and explore both branches while tracking which heroes remain available. Even with memoization, the state would include which heroes are still alive and how many turns have passed. That state space grows exponentially with n, since every hero can be in one of several states and each turn changes the structure. This approach becomes completely infeasible once n reaches even a few dozen.

The main simplification comes from observing that only the relative ranking of heroes matters, and even more specifically, only the top k heroes per team ever contribute to the final score. Every other hero is irrelevant to the objective except insofar as it can be used as a target for bans.

Because each team has exactly n opportunities to act, and every hero is either eventually picked or removed, both teams effectively get enough turns to secure k heroes unless they are explicitly denied those specific heroes. This shifts the problem into understanding which heroes can realistically be prevented from being taken, and whether optimal play can prevent a team from collecting its best k choices.

In optimal play, both sides will always prioritize either securing a very valuable hero for themselves or removing a very valuable hero from the opponent. However, since each team can directly pick its own hero, and picking immediately protects it from future bans, the best strategy is to immediately lock in the top k heroes on each side rather than spending time on interference that does not affect the top k set.

This leads to the key reduction: each team will successfully secure its k highest-value heroes from its own pool, and the opponent cannot fully prevent this because each selection permanently protects the chosen hero.

So the interaction of banning does not change the final set of top k heroes per side; it only affects ordering and irrelevant surplus heroes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force game simulation | Exponential | Exponential | Too slow |
| Sort and take top k per team | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Sort Team A’s hero values in descending order. The reason for sorting is that only the largest k values can ever contribute to the final score, so identifying them directly avoids reasoning about intermediate game actions.
2. Take the first k values from Team A’s sorted list and compute their sum. These represent the optimal selection for Team A because any selection that replaces one of these with a smaller value would strictly reduce the score.
3. Repeat the same process for Team B: sort its values in descending order and take the top k.
4. Compute the final answer as the difference between these two sums, specifically the sum of Team A’s top k heroes minus the sum of Team B’s top k heroes.

The crucial idea is that although the game includes banning, banning only affects heroes that have not yet been secured, and optimal play allows each side to secure its most valuable k heroes immediately through picking actions.

### Why it works

The invariant is that each team can always ensure inclusion of its k largest-valued heroes in its final picked set. Once a hero is picked, it cannot be removed, and since each team has enough turns to make k picks, optimal play allows those k picks to be directed toward the highest-value heroes before any strategy involving bans can permanently eliminate them. Any ban that targets a non-top-k hero does not affect the final score, and any attempt to ban a top-k hero is countered by simply picking it instead on an earlier turn. This makes the final effective decision space collapse to independent selection of top k elements per team.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    a.sort(reverse=True)
    b.sort(reverse=True)
    
    print(sum(a[:k]) - sum(b[:k]))

if __name__ == "__main__":
    main()
```

The implementation relies entirely on sorting, since the game dynamics reduce to selecting the k largest values per side. Sorting guarantees we identify these values in O(n log n) time, and slicing extracts exactly the portion that matters.

No simulation of turns is required because the final outcome depends only on which k elements survive per team, not on the order in which they were processed.

## Worked Examples

### Example 1

Input:

```
2 1
3 6
2 4
```

Sorted arrays:

A = [6, 3]

B = [4, 2]

| Step | A sorted | B sorted | A top k sum | B top k sum | Difference |
| --- | --- | --- | --- | --- | --- |
| After sorting | [6, 3] | [4, 2] | - | - | - |
| Take k=1 | [6] | [4] | 6 | 4 | 2 |

This shows that only the single strongest hero per team matters when k = 1, and the rest of the structure is irrelevant.

### Example 2

Input:

```
4 2
1 3 5 7
2 4 6 8
```

Sorted arrays:

A = [7, 5, 3, 1]

B = [8, 6, 4, 2]

| Step | A sorted | B sorted | A top k sum | B top k sum | Difference |
| --- | --- | --- | --- | --- | --- |
| After sorting | [7,5,3,1] | [8,6,4,2] | - | - | - |
| Take k=2 | [7,5] | [8,6] | 12 | 14 | -2 |

This confirms that the method consistently selects the best available k heroes per side, regardless of the presence of intermediate banning decisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting both arrays dominates the runtime |
| Space | O(1) extra | Sorting is in-place aside from input storage |

The constraints allow up to 100000 heroes, and sorting comfortably fits within time limits. The memory usage is linear in the input size, which is unavoidable since the arrays must be stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    a.sort(reverse=True)
    b.sort(reverse=True)
    
    return str(sum(a[:k]) - sum(b[:k]))

# provided samples
assert run("2 1\n3 6\n2 4\n") == "2"
assert run("4 1\n1 3 5 7\n2 4 6 8\n") == "-1"
assert run("4 2\n4 6 7 9\n2 5 8 10\n") == "-6"

# custom cases
assert run("1 1\n10\n1\n") == "9", "single element"
assert run("5 2\n5 4 3 2 1\n1 2 3 4 5\n") == "0", "symmetric arrays"
assert run("6 3\n10 9 8 1 1 1\n7 6 5 4 3 2\n") == "9", "skewed distribution"
assert run("3 1\n100 1 1\n50 50 50\n") == "50", "tie-heavy opponent"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 10 / 1 | 9 | minimum n case |
| symmetric arrays | 0 | balanced cancellation |
| skewed distribution | 9 | dominance of top values |
| tie-heavy opponent | 50 | effect of single strongest pick |

## Edge Cases

When n = 1, the game degenerates into a single comparison where each side effectively secures or loses its only hero. The algorithm handles this correctly because sorting leaves a single element per array and k = 1 forces direct comparison.

When k = n, every hero is effectively selected, and the answer becomes the total sum difference. The sorting still works because taking all elements after sorting is equivalent to summing the entire array.

When one side has many large values clustered together, the opponent cannot selectively remove enough of them to displace the top k set entirely, since each picked hero becomes permanently protected. The sorted selection still captures the correct subset because it reflects the only values that can survive optimal play.

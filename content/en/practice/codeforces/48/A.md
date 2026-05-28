---
title: "CF 48A - Rock-paper-scissors"
description: "Three players simultaneously choose one of the classic rock-paper-scissors gestures: \"rock\", \"paper\", or \"scissors\". A player wins only if their gesture defeats the gestures shown by both other players."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "schedules"]
categories: ["algorithms"]
codeforces_contest: 48
codeforces_index: "A"
codeforces_contest_name: "School Personal Contest #3 (Winter Computer School 2010/11) - Codeforces Beta Round 45 (ACM-ICPC Rules)"
rating: 900
weight: 48
solve_time_s: 91
verified: true
draft: false
---

[CF 48A - Rock-paper-scissors](https://codeforces.com/problemset/problem/48/A)

**Rating:** 900  
**Tags:** implementation, schedules  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

Three players simultaneously choose one of the classic rock-paper-scissors gestures: `"rock"`, `"paper"`, or `"scissors"`. A player wins only if their gesture defeats the gestures shown by both other players.

That means there is a winner only in these situations:

- One player shows rock while the other two show scissors.
- One player shows scissors while the other two show paper.
- One player shows paper while the other two show rock.

Every other configuration produces no winner.

The input consists of exactly three strings. The first belongs to Uncle Fyodor, the second to Matroskin, and the third to Sharic. The output is a single character representing the winner: `"F"`, `"M"`, `"S"`, or `"?"` if nobody uniquely wins.

The constraints are tiny because there are always exactly three players and only three possible gestures. Any solution runs instantly. Even checking every possible interaction manually would take constant time. The real challenge is implementing the game logic correctly without missing edge cases.

The tricky part is that many states do not have a winner. A careless implementation often assumes there must always be one.

Consider this input:

```
rock
paper
scissors
```

Every gesture both wins and loses against another gesture. Nobody defeats both opponents, so the correct answer is:

```
?
```

A naive implementation that simply checks pairwise victories might incorrectly declare a winner here.

Another easy mistake appears when two players tie with the same gesture:

```
paper
rock
rock
```

The correct output is:

```
F
```

Paper beats rock, and since both opponents showed rock, Uncle Fyodor defeats both simultaneously.

The opposite situation must also be handled correctly:

```
rock
paper
paper
```

Now the correct answer is:

```
M
```

Even though two players showed the winning gesture, there is still no unique winner according to the rules. The first paper player wins because the game identifies players individually, not gestures collectively. Since Matroskin is the only player whose move defeats both opponents, he is the winner.

Finally, when everyone chooses the same gesture:

```
scissors
scissors
scissors
```

nobody wins, so the output is:

```
?
```

## Approaches

The most direct approach is to simulate the game exactly as described. For each player, check whether their gesture defeats the gestures of both other players. If it does, that player wins.

Since there are only three players, this brute-force approach already works perfectly. We can define a helper rule such as:

- rock beats scissors
- scissors beats paper
- paper beats rock

Then for every player, compare their gesture against the other two.

The total work is constant because we perform only a few comparisons. Even the most naive implementation easily fits inside the limits.

The key observation is that the structure of rock-paper-scissors makes the winning condition extremely small. A player wins only if the other two gestures are identical and specifically vulnerable to the winner’s gesture.

For example:

- rock wins only against two scissors
- scissors wins only against two papers
- paper wins only against two rocks

This lets us simplify the implementation even further. Instead of simulating every duel, we can directly check the three possible winning patterns.

That gives a short and clean constant-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three gestures into variables representing Fyodor, Matroskin, and Sharic.
2. Create a mapping describing which gesture defeats which:

- `"rock"` defeats `"scissors"`
- `"scissors"` defeats `"paper"`
- `"paper"` defeats `"rock"`
3. Check whether Fyodor defeats both other players.

This is true when Fyodor’s gesture defeats Matroskin’s gesture and also defeats Sharic’s gesture.
4. If Fyodor wins, print `"F"` and stop.
5. Repeat the same check for Matroskin.

If his gesture defeats both opponents, print `"M"`.
6. Repeat the same check for Sharic.

If his gesture defeats both opponents, print `"S"`.
7. If none of the three conditions succeeded, print `"?"`.

This covers cycles like rock-paper-scissors and cases where all gestures are equal.

### Why it works

The rules define a winner as someone whose gesture defeats both other gestures simultaneously. The algorithm checks that exact condition independently for each player.

Rock-paper-scissors has deterministic outcomes. A gesture either defeats another or it does not. Since every possible winner must satisfy the condition checked by the algorithm, and every checked condition exactly matches the game rules, the algorithm cannot miss a valid winner or invent an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution

f = input().strip()
m = input().strip()
s = input().strip()

beats = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock"
}

if beats[f] == m and beats[f] == s:
    print("F")
elif beats[m] == f and beats[m] == s:
    print("M")
elif beats[s] == f and beats[s] == m:
    print("S")
else:
    print("?")
```

The program starts by reading the three gestures in the fixed order required by the statement. Using `.strip()` is necessary because input lines contain newline characters.

The `beats` dictionary encodes the game rules directly. For example:

```
beats["rock"] == "scissors"
```

means rock defeats scissors.

Each conditional checks whether one player defeats both opponents. For example:

```
beats[f] == m and beats[f] == s
```

asks whether Fyodor’s gesture defeats Matroskin’s gesture and Sharic’s gesture simultaneously.

The order of checks does not matter because at most one player can satisfy the winning condition. If none of the conditions match, the game has no unique winner, so the program prints `"?"`.

A subtle point is that ties are handled naturally. Suppose the input is:

```
paper
rock
rock
```

Then:

```
beats["paper"] == "rock"
```

is true for both opponents, so Fyodor wins correctly.

## Worked Examples

### Example 1

Input:

```
rock
rock
rock
```

| Variable | Value |
| --- | --- |
| f | rock |
| m | rock |
| s | rock |

| Check | Result |
| --- | --- |
| rock beats rock | False |
| No player defeats both opponents | True |

Output:

```
?
```

This example shows the all-equal case. No gesture defeats itself, so nobody can beat both opponents.

### Example 2

Input:

```
paper
rock
rock
```

| Variable | Value |
| --- | --- |
| f | paper |
| m | rock |
| s | rock |

| Check | Result |
| --- | --- |
| paper beats rock | True |
| paper beats rock again | True |
| Fyodor wins | True |

Output:

```
F
```

This trace demonstrates the key winning pattern: one player shows the gesture that defeats the identical gestures of both opponents.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of comparisons are performed |
| Space | O(1) | The program stores only three strings and one small dictionary |

The input size never grows, so the runtime and memory usage remain constant. The solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    f = input().strip()
    m = input().strip()
    s = input().strip()

    beats = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    if beats[f] == m and beats[f] == s:
        print("F")
    elif beats[m] == f and beats[m] == s:
        print("M")
    elif beats[s] == f and beats[s] == m:
        print("S")
    else:
        print("?")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue()

# provided sample
assert run("rock\nrock\nrock\n") == "?\n", "sample 1"

# custom cases
assert run("paper\nrock\nrock\n") == "F\n", "Fyodor wins"
assert run("rock\npaper\nrock\n") == "M\n", "Matroskin wins"
assert run("rock\nrock\npaper\n") == "S\n", "Sharic wins"
assert run("rock\npaper\nscissors\n") == "?\n", "cyclic case"
assert run("scissors\nscissors\nscissors\n") == "?\n", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `paper rock rock` | `F` | First player defeating two equal opponents |
| `rock paper rock` | `M` | Second player winning |
| `rock rock paper` | `S` | Third player winning |
| `rock paper scissors` | `?` | Cyclic no-winner configuration |
| `scissors scissors scissors` | `?` | All-equal configuration |

## Edge Cases

Consider the cyclic configuration:

```
rock
paper
scissors
```

The algorithm checks each player separately.

Fyodor uses rock, which defeats scissors but loses to paper, so he cannot win.

Matroskin uses paper, which defeats rock but loses to scissors.

Sharic uses scissors, which defeats paper but loses to rock.

Since nobody defeats both opponents, the algorithm reaches the final branch and prints:

```
?
```

Now consider a duplicated losing gesture:

```
paper
rock
rock
```

The algorithm first checks Fyodor:

```
beats["paper"] == "rock"
```

This is true for both opponents, so the answer becomes:

```
F
```

The remaining checks are skipped because a valid winner has already been found.

Finally, consider all gestures equal:

```
rock
rock
rock
```

Every comparison fails because rock does not defeat rock. None of the three winner conditions becomes true, so the algorithm correctly outputs:

```
?
```

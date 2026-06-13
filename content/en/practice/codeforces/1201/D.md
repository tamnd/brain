---
title: "CF 1201D - Treasure Hunting"
description: "We are given a grid with rows increasing upward and columns increasing left to right. We start at the bottom-left cell and want to collect all treasures placed on various cells."
date: "2026-06-13T15:07:14+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1201
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 577 (Div. 2)"
rating: 2100
weight: 1201
solve_time_s: 102
verified: false
draft: false
---

[CF 1201D - Treasure Hunting](https://codeforces.com/problemset/problem/1201/D)

**Rating:** 2100  
**Tags:** binary search, dp, greedy, implementation  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid with rows increasing upward and columns increasing left to right. We start at the bottom-left cell and want to collect all treasures placed on various cells. Movement is restricted: we can move left or right freely, but moving up is only allowed in special “safe” columns. Once we are in a safe column, we can climb upward any number of times, but we can never move down.

The objective is to visit all treasure cells in any order and minimize the total number of moves, where each step is a move in one of the allowed directions. Collecting a treasure costs nothing beyond standing on its cell.

The core difficulty is that horizontal movement is unrestricted but vertical movement is heavily constrained. This creates a structure where each time we decide to climb, we are effectively committing to a column and a row range.

The constraints push us away from any state-based shortest path on the grid. With up to 200,000 treasures and safe columns, any per-cell or per-state dynamic programming over the grid is impossible. Even an O(k²) approach over treasures would be far too slow, since k can reach 200,000.

A naive but instructive idea is to simulate collecting treasures in some order and compute shortest paths between them while respecting the “must be in safe column to go up” rule. This fails because shortest path computation itself is expensive and the number of orderings is factorial.

A second naive idea is to treat each row independently, but that ignores the fact that we must physically travel upward through safe columns and horizontal travel accumulates across rows.

A subtle edge case appears when all treasures are in a single column that is not safe. You might think the answer depends only on horizontal movement, but in fact you are forced to first move to a safe column before any vertical progress, which can dominate the cost.

## Approaches

The key structural observation is that vertical movement is the bottleneck, not horizontal movement. We can only increase our row when standing in a safe column, so every time we transition from a lower row to a higher one, we must pass through some safe column. That means the optimal path naturally decomposes into “horizontal sweeps” within a row, and “vertical jumps” between rows done at safe columns.

If we fix a row, visiting all treasures in that row is equivalent to covering the interval between the leftmost and rightmost treasure in that row. Once we enter that interval, we pay the cost of walking from one side to the other. The question is where we enter and exit, because we want to minimize horizontal travel while still ensuring we can continue upward at a safe column.

The critical insight is to process rows from bottom to top and maintain, for each row, the leftmost and rightmost treasure. Between consecutive rows that contain treasures, we decide how we transition: we end the previous row at some safe column, then move vertically, and then enter the next row from either its left or right boundary, whichever is cheaper.

The remaining difficulty is choosing the best safe column to “anchor” vertical movement. Since safe columns are fixed, we can pre-sort them and, for any position, quickly find the closest safe column to minimize horizontal cost when transitioning upward or downward.

This reduces the problem to maintaining intervals per row and computing minimal transitions between consecutive rows using nearest safe column queries, which can be handled with binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over paths | exponential | O(k) | Too slow |
| Row interval + greedy transitions | O(k log q + k log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Group all treasures by row and, for each row, compute the minimum and maximum column containing a treasure. This compresses each row into

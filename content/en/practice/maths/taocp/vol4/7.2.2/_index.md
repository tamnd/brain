---
title: "TAOCP 7.2.2: Backtracking"
description: "Section 7.2.2 exercises: 39/79 solved."
tags: ["taocp", "mathematics", "algorithms"]
categories: ["mathematics"]
section: "7.2.2"
section_title: "Backtracking"
chapter: 7
chapter_title: "Combinatorial Searching"
volume: 4
weight: 7020200
draft: false
---

# Section 7.2.2. Backtracking

Exercises from [TAOCP Volume 4](../) Section 7.2.2: 39/79 solved.

| # | Rating | Category | Status | Time |
|---|--------|----------|--------|------|
| [1](01.md) | &#9654; [**] |  | verified | 4m39s |
| [2](02.md) |  [**] |  | verified | 7m08s |
| [3](03.md) |  [**] |  | verified | 2m59s |
| [4](04.md) |  [**] |  | verified | 3m11s |
| [5](05.md) |  [**] |  | verified | 2m27s |
| [6](06.md) |  [**] |  | verified | 2m24s |
| [7](07.md) |  [**] |  | solved | 8m55s |
| [8](08.md) |  [**] |  | solved | 2m37s |
| [9](09.md) |  [**] |  | verified | 6m25s |
| [10](10.md) | &#9654; [**] |  | verified | 1m35s |
| [11](11.md) |  [**] |  | solved | 8m01s |
| [12](12.md) |  [**] |  | solved | 10m12s |
| [13](13.md) |  [**] |  | verified | 5m30s |
| [14](14.md) |  [**] |  | verified | 4m09s |
| [15](15.md) |  [**] |  | solved | 8m06s |
| 16 |  [**] |  | - | - |
| [17](17.md) |  [**] |  | verified | 2m11s |
| [18](18.md) |  [**] |  | solved | 7m44s |
| [19](19.md) |  [**] |  | verified | 1m50s |
| [20](20.md) | &#9654; [**] |  | verified | 2m21s |
| 21 | &#9654; [*M25*] | math-medium | - | - |
| 22 |  [*M26*] | math-hard | - | - |
| [23](23.md) |  [*17*] | medium | verified | 3m43s |
| [24](24.md) |  [*20*] | medium | solved | 7m34s |
| 25 | &#9654; [*25*] | medium | - | - |
| [26](26.md) |  [*21*] | medium | solved | 9m19s |
| [27](27.md) |  [*22*] | medium | verified | 4m39s |
| [28](28.md) | &#9654; [*23*] | medium | verified | 4m26s |
| [29](29.md) |  [*20*] | medium | verified | 3m15s |
| [30](30.md) |  [*22*] | medium | solved | 5m20s |
| [31](31.md) |  [*39*] | project | solved | 6m57s |
| 32 |  [*22*] | medium | - | - |
| [33](33.md) |  [*21*] | medium | solved | 3m14s |
| [34](34.md) |  [*15*] | simple | verified | 2m55s |
| [35](35.md) | &#9654; [*22*] | medium | verified | 7m41s |
| [36](36.md) |  [**] |  | verified | 3m23s |
| [37](37.md) | &#9654; [**] |  | solved | 7m03s |
| 38 |  [*HM28*] | hm-hard | - | - |
| [39](39.md) |  [*18*] | medium | solved | 7m52s |
| [40](40.md) | &#9654; [*15*] | simple | verified | 1m53s |
| [41](41.md) |  [*17*] | medium | solved | 4m08s |
| [42](42.md) |  [*18*] | medium | solved | 5m08s |
| [43](43.md) |  [*20*] | medium | verified | 1m17s |
| [44](44.md) | &#9654; [*25*] | medium | verified | 3m15s |
| 45 | &#9654; [*28*] | hard | - | - |
| [46](46.md) |  [*M35*] | math-hard | verified | 2m44s |
| 47 |  [*HM29*] | hm-hard | - | - |
| 48 |  [*M42*] | math-project | - | - |
| 49 |  [*20*] | medium | - | - |
| 50 |  [*M15*] | math-simple | - | - |
| 51 |  [*M22*] | math-medium | - | - |
| 52 | &#9654; [*HM25*] | hm-medium | - | - |
| 53 | &#9654; [*M30*] | math-hard | - | - |
| 54 |  [*M21*] | math-medium | - | - |
| 55 |  [*M30*] | math-hard | - | - |
| 56 | &#9654; [*M25*] | math-medium | - | - |
| 57 |  [*HM21*] | hm-medium | - | - |
| 58 |  [*27*] | hard | - | - |
| 59 |  [*26*] | hard | - | - |
| 60 | &#9654; [*20*] | medium | - | - |
| 61 |  [*HM26*] | hm-hard | - | - |
| 62 | &#9654; [*22*] | medium | - | - |
| 63 |  [*10*] | simple | - | - |
| 64 |  [**] |  | - | - |
| 65 |  [*25*] | medium | - | - |
| 66 | &#9654; [*23*] | medium | - | - |
| 67 | &#9654; [*26*] | hard | - | - |
| 68 | &#9654; [*28*] | hard | - | - |
| 69 |  [*41*] | project | - | - |
| 70 |  [*HM40*] | hm-project | - | - |
| 71 | &#9654; [*M29*] | math-hard | - | - |
| 72 |  [*HM28*] | hm-hard | - | - |
| 73 | &#9654; [*30*] | hard | - | - |
| 74 |  [*21*] | medium | - | - |
| 75 | &#9654; [*30*] | hard | - | - |
| 76 |  [*23*] | medium | - | - |
| 77 |  [*M22*] | math-medium | - | - |
| 78 |  [*22*] | medium | - | - |
| 79 | &#9654; [*M30*] | math-hard | - | - |

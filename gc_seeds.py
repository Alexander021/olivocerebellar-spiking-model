"""Generate a new granule-cell activation schedule (elig_list)."""

import pprint
import numpy as np

seed = 1  # Change this value to generate another schedule.
rng = np.random.default_rng(seed)
keys = list(range(100))
max_attempts = 100000

for attempt in range(max_attempts):
    prev = {}
    count = dict.fromkeys(keys, 2)
    elig_list = {k: [] for k in keys}
    failed = False

    for time in range(1, 5001, 25):
        candidates = [
            k for k in keys
            if count[k] >= 1 and (k not in prev or prev[k] + 350 <= time)
        ]
        if not candidates:
            failed = True
            break
        num = int(rng.choice(candidates))
        count[num] -= 1
        prev[num] = time
        elig_list[num].append(time)

    valid = (
        not failed
        and all(count[k] == 0 for k in keys)
        and all(len(elig_list[k]) == 2 for k in keys)
        and all(elig_list[k][1] - elig_list[k][0] >= 350 for k in keys)
    )
    if valid:
        break
else:
    raise RuntimeError("A valid elig_list was not generated within max_attempts.")

print("Seed:", seed)
print("Total activation onsets:", sum(len(v) for v in elig_list.values()))
print("All cells have two onsets:", all(len(v) == 2 for v in elig_list.values()))
print("Minimum within-cell separation is at least 35 ms:",
      all(elig_list[k][1] - elig_list[k][0] >= 350 for k in keys))
print()
print("Copy the following block into model.py:")
print()
print("elig_list = " + pprint.pformat(elig_list, width=118, sort_dicts=True))

"""
Standalone 1500-s simulation of the olivo-cerebellar spiking model.

NEST Simulator 3.8.0
Neuron model: glif_cond, GLIF Model 1
"""

import nest
import numpy as np


resolution = 0.1
sim_time = 10000
update_interval = 1

window_size = 60
T_e = 6
I = 1
eps = 0.01
initial_weight = 4.01


nest.ResetKernel()
nest.set_verbosity("M_WARNING")

nest.SetKernelStatus({
    "local_num_threads": 1,
    "resolution": resolution,
    "rng_seed": 1,
})


common_glif_params = {
    "g_m": 9.43,
    "tau_syn": (0.2, 2.0),
    "E_rev": (0.0, -85.0),
    "spike_dependent_threshold": False,
    "after_spike_currents": False,
    "adapting_threshold": False,
}


climb_fiber = nest.Create("glif_cond", 1, params={
    **common_glif_params,
    "C_m": 150.0,
    "E_L": -70.0,
    "V_m": -70.0,
    "V_reset": -70.0,
    "V_th": -60.0,
    "t_ref": 15.0,
})

purk = nest.Create("glif_cond", 1, params={
    **common_glif_params,
    "C_m": 200.0,
    "E_L": -70.0,
    "V_m": -70.0,
    "V_reset": -70.0,
    "V_th": -55.0,
    "t_ref": 2.0,
})

gran_cell = nest.Create("glif_cond", 100, params={
    **common_glif_params,
    "C_m": 10.0,
    "E_L": -70.0,
    "V_m": -70.0,
    "V_reset": -70.0,
    "V_th": -60.0,
    "t_ref": 1.0,
})

nuc = nest.Create("glif_cond", 1, params={
    **common_glif_params,
    "C_m": 150.0,
    "E_L": -70.0,
    "V_m": -60.0,
    "V_reset": -70.0,
    "V_th": -55.0,
    "t_ref": 3.0,
})

external_input = nest.Create("glif_cond", 1, params={
    **common_glif_params,
    "C_m": 200.0,
    "E_L": -70.0,
    "V_m": -70.0,
    "V_reset": -70.0,
    "V_th": -55.0,
    "t_ref": 2.0,
})


dc_ex = nest.Create("dc_generator", 1, params={
    "amplitude": 0,
    "start": 0.0,
    "stop": 10000000.0,
})

dc_nuc_1 = nest.Create("dc_generator", 1, params={
    "amplitude": 200.0,
    "start": 0.0,
    "stop": 10000000.0,
})


sr_purk = nest.Create("spike_recorder", 1)
sr_gran = nest.Create("spike_recorder", 1)
sr_climb = nest.Create("spike_recorder", 1)
sr_ex = nest.Create("spike_recorder", 1)
sr_nuc = nest.Create("spike_recorder", 1)


nest.Connect(
    dc_nuc_1,
    nuc,
    syn_spec={"delay": resolution, "receptor_type": 0},
)

nest.Connect(
    nuc,
    climb_fiber,
    syn_spec={
        "weight": -18.0,
        "delay": resolution,
        "receptor_type": 1,
    },
)

nest.Connect(
    purk,
    nuc,
    syn_spec={
        "weight": -25.0,
        "delay": resolution,
        "receptor_type": 1,
    },
    conn_spec={"rule": "all_to_all"},
)

nest.Connect(
    external_input,
    climb_fiber,
    syn_spec={
        "weight": 19.4,
        "receptor_type": 1,
    },
)

nest.Connect(
    gran_cell,
    purk,
    syn_spec={
        "weight": initial_weight,
        "delay": resolution,
        "receptor_type": 1,
    },
)

nest.Connect(
    dc_ex,
    external_input,
    syn_spec={"weight": 10.0},
)

nest.Connect(climb_fiber, sr_climb)
nest.Connect(purk, sr_purk)
nest.Connect(gran_cell, sr_gran)
nest.Connect(external_input, sr_ex)
nest.Connect(nuc, sr_nuc)


# GC activation schedule used in the original simulation file.
# Replace elig_list with another generated list if a different GC schedule is required.
elig_list = {
    0: [2151, 4826], 1: [1176, 1526], 2: [151, 1051], 3: [1901, 4426],
    4: [1351, 3826], 5: [1, 3276], 6: [501, 2026], 7: [3651, 4301],
    8: [2901, 4101], 9: [2951, 3701], 10: [1476, 3576], 11: [3426, 4376],
    12: [3801, 4401], 13: [176, 1151], 14: [101, 751], 15: [126, 601],
    16: [476, 2126], 17: [2101, 3051], 18: [3326, 3901], 19: [576, 3601],
    20: [4326, 4776], 21: [2551, 3401], 22: [451, 976], 23: [701, 1776],
    24: [26, 4251], 25: [351, 2076], 26: [2176, 4501], 27: [1201, 2851],
    28: [4726], 29: [301, 2476], 30: [901, 4026], 31: [4051, 4451],
    32: [3001, 3351], 33: [2301, 3526], 34: [3026, 3751], 35: [1851, 2276],
    36: [2051, 4276], 37: [826, 1976], 38: [1576, 2601], 39: [676, 4651],
    40: [3851, 4801], 41: [1951, 2351], 42: [76, 651], 43: [951, 3126],
    44: [1751, 3176], 45: [2926, 3951], 46: [3626, 4176], 47: [526, 3476],
    48: [551, 2826], 49: [3301, 4001], 50: [876, 1426], 51: [2376, 4126],
    52: [2251, 3151], 53: [4351, 4876], 54: [1376, 2501], 55: [2401, 3376],
    56: [1101, 2801], 57: [4076, 4901], 58: [51, 2626], 59: [1701, 4151],
    60: [4526, 4926], 61: [4476, 4851], 62: [1801, 3676], 63: [1826, 2426],
    64: [2326, 2701], 65: [426, 2876], 66: [1626, 2726], 67: [276, 3201],
    68: [1026, 1551], 69: [326, 3251], 70: [2676, 3976], 71: [776, 3551],
    72: [926, 4751], 73: [626, 1726], 74: [1451, 2576], 75: [201, 1676],
    76: [1401, 4201], 77: [251, 1501], 78: [801, 1926], 79: [1001, 4676],
    80: [3101, 3776], 81: [2651, 3926], 82: [3226, 4226], 83: [1126, 1876],
    84: [401, 851], 85: [1301, 3726], 86: [4701], 87: [726, 2751],
    88: [1326, 2226], 89: [2526, 2976], 90: [1601, 4551], 91: [1076, 3076],
    92: [1276, 2451], 93: [2001, 3876], 94: [226, 2201], 95: [2776, 3451],
    96: [1226, 4576], 97: [1251, 1651], 98: [3501, 4601], 99: [376, 4626]
}


spikes = []

for num in range(100):
    a = len(elig_list[num])

    for time in range(a):
        for j in range(5):
            spikes.append(
                elig_list[num][time] / 10 + 2 * j
            )

        for i in range(1, 3000):
            for j in range(5):
                spikes.append(
                    elig_list[num][time] / 10
                    + 500 * i
                    + 2 * j
                )

        sg = nest.Create(
            "spike_generator",
            params={"spike_times": spikes},
        )

        nest.Connect(
            sg,
            gran_cell[num],
            syn_spec={
                "weight": 40.0,
                "receptor_type": 1,
            },
        )

        spikes = []


def chi(time, climb_spike):
    if climb_spike.size > 0 and (time - climb_spike[-1]) < window_size:
        return -50
    else:
        return 1


def eligibility(num, elig_list, climb_spike, time, e_list):
    diff = 500 * (time // 500)

    if (
        1.1 > time - (elig_list[num][-1] / 10 + diff + 5) > -1.1
        or 1.1 > time - (elig_list[num][0] / 10 + diff + 5) > -1.1
    ):
        e_list[num].append(1)

    else:
        if time - (elig_list[num][-1] / 10 + diff + 5) > 0:
            e_list[num].append(
                I * np.exp(
                    -(time - (elig_list[num][-1] / 10 + diff + 5)) / T_e
                )
            )

        elif time - (elig_list[num][0] / 10 + diff + 5) > 0:
            e_list[num].append(
                I * np.exp(
                    -(time - (elig_list[num][0] / 10 + diff + 5)) / T_e
                )
            )

        else:
            e_list[num].append(
                I * np.exp(
                    -(time - (elig_list[num][-1] / 10 + diff + 5 - 500)) / T_e
                )
            )

    return e_list[num][-1]


def change_weight(num, previous_weight, elig_list, climb_spike, time, e_list):
    e = eligibility(
        num,
        elig_list,
        climb_spike,
        time,
        e_list,
    )

    chi_func = chi(
        time,
        climb_spike,
    )

    if previous_weight + eps * e * chi_func > 0:
        new_weight = previous_weight + eps * e * chi_func
    else:
        new_weight = 0

    return new_weight


weight_values = []
e_list = []

for i in range(100):
    weight_values.append([initial_weight])
    e_list.append([0])


for step in range(0, sim_time + 1, int(update_interval)):
    nest.Simulate(update_interval)

    current_time = step

    events = nest.GetStatus(
        sr_climb,
        "events",
    )[0]

    spike_times = np.array(
        events["times"]
    )


    if current_time < 500000:
        nest.SetStatus(
            dc_ex,
            {"amplitude": 57.9},
        )

    elif current_time < 1000000:
        nest.SetStatus(
            dc_ex,
            {"amplitude": 56.7},
        )

    else:
        nest.SetStatus(
            dc_ex,
            {"amplitude": 59.1},
        )


    climb_spike = spike_times[
        spike_times > (current_time - 1000)
    ]


    for i in range(100):
        conn = nest.GetConnections(
            source=gran_cell[i],
            target=purk,
        )

        previous_weight = weight_values[i][-1]

        new_weight = change_weight(
            i,
            previous_weight,
            elig_list,
            climb_spike,
            current_time,
            e_list,
        )

        weight_values[i].append(
            new_weight
        )

        nest.SetStatus(
            conn,
            {"weight": new_weight},
        )


events = sr_climb.get("events")
save_climb_spikes = events["times"]

events = sr_nuc.get("events")
save_nuc_spikes = events["times"]

events = sr_purk.get("events")
save_purk_spikes = events["times"]


end_weights = []

for i in range(len(weight_values)):
    end_weights.append(
        [weight_values[i][-1]]
    )


weight_save = []

for syn in weight_values:
    syn_list = []

    for i in range(len(syn)):
        if i % 100 == 0:
            syn_list.append(
                syn[i]
            )

    weight_save.append(
        syn_list
    )


with open(
    "simulation_results.txt",
    "w",
    encoding="utf-8",
) as f:

    f.write(
        f"end_weights = {repr(end_weights)}\n\n"
    )

    f.write(
        f"elig_list = {repr(elig_list)}\n\n"
    )

    f.write(
        "save_climb_spikes = ["
    )

    for item in save_climb_spikes:
        f.write(
            f"{item}, "
        )

    f.write(
        "]\n\n"
    )


    f.write(
        "save_purk_spikes = ["
    )

    for item in save_purk_spikes:
        f.write(
            f"{item}, "
        )

    f.write(
        "]\n\n"
    )


    f.write(
        "save_nuc_spikes = ["
    )

    for item in save_nuc_spikes:
        f.write(
            f"{item}, "
        )

    f.write(
        "]\n\n"
    )


    f.write(
        f"weight_values = {repr(weight_save)}\n"
    )


print(
    "Simulation completed."
)

print(
    "Results saved to simulation_results.txt"
)

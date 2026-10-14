# Olivo-cerebellar spiking model

This repository contains a standalone NEST implementation of the closed-loop olivo-cerebellar spiking model used in the manuscript **“Adaptive spiking dynamics in a cerebellar model with synaptic plasticity and feedback.”**

`model.py` contains all model parameters and the GC activation schedule directly in the source file. No JSON or external configuration file is required.

## Files

- `model.py` — complete network, plasticity rule, simulation, and raw-data export.
- `gc_seeds.py` — generates a new `elig_list` that can be copied directly into `model.py`.
- `requirements.txt` — Python dependency list. NEST Simulator 3.8.0 must be installed separately.

## Software and GLIF variant

- NEST Simulator: **3.8.0**
- NEST neuron model: **`glif_cond`**
- GLIF level: **GLIF Model 1 (traditional LIF)**
- Simulation resolution: **0.1 ms**
- NEST kernel RNG seed: **1**
- Local NEST threads: **1**

The GLIF level is fixed explicitly in the source:

| Mechanism | Value |
|---|---:|
| `spike_dependent_threshold` | `False` |
| `after_spike_currents` | `False` |
| `adapting_threshold` | `False` |

Thus, spike-dependent threshold/reset adaptation, after-spike currents, and voltage-dependent threshold adaptation are disabled. Parameters associated exclusively with GLIF2–GLIF5 do not contribute to the dynamics.

## Effective neuron parameters

All neuron populations use `g_m = 9.43 nS`, `tau_syn = (0.2, 2.0) ms`, and `E_rev = (0.0, -85.0) mV`.

| Population | C_m (pF) | g_m (nS) | E_L (mV) | Initial V_m (mV) | V_reset (mV) | V_th (mV) | t_ref (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|
| CFC | 150 | 9.43 | -70 | -70 | -70 | -60 | 15 |
| PC | 200 | 9.43 | -70 | -70 | -70 | -55 | 2 |
| GC | 10 | 9.43 | -70 | -70 | -70 | -60 | 1 |
| SNC | 150 | 9.43 | -70 | -60 | -70 | -55 | 3 |
| External-input neuron | 200 | 9.43 | -70 | -70 | -70 | -55 | 2 |

NEST uses mV for membrane/reversal potentials, pF for membrane capacitance, nS for conductances, and ms for time parameters in `glif_cond`.

## Synapses and inputs

For `glif_cond`, a spike-event weight of 1.0 produces a peak conductance change of 1 nS. Therefore spike-synapse weights are reported in nS.

| Connection | Weight | Delay | Receptor type |
|---|---:|---:|---:|
| Spike generator → GC | 40 nS | 1.0 ms | 1 |
| GC → PC | initial 4 nS, plastic | 0.1 ms | 1 |
| PC → SNC | -25 nS | 0.1 ms | 1 |
| SNC → CFC | -18 nS | 0.1 ms | 1 |
| External-input neuron → CFC | 19.4 nS | 1.0 ms | 1 |

The negative PC→SNC and SNC→CFC weights and their receptor assignments are retained exactly from the original implementation.

### DC input

The SNC background `dc_generator` amplitude is **200 pA**. Its connection uses `static_synapse` weight 1.0, delay 0.1 ms, and receptor type 0.

The external-input neuron is driven by a `dc_generator`; the connection uses `static_synapse` weight **10.0**, delay 1.0 ms, and receptor type 0. The generator amplitudes used in the three-level experiment are:

| Interval | DC amplitude |
|---|---:|
| 0–500 s | 57.9 pA |
| 500–1000 s | 56.7 pA |
| 1000–1500 s | 59.1 pA |

NEST defines `dc_generator.amplitude` in pA.

## GC activation schedule

`model.py` contains the hard-coded `elig_list` present in the original simulation notebook. It is fixed for a run and is not redrawn during simulation. Values are divided by 10 when converted to model time, so a separation of 350 schedule units corresponds to **35 ms**.

The embedded source-notebook schedule contains **98 cells with two onset positions and two cells (28 and 86) with one onset position**. This has been preserved rather than silently corrected. If a strict two-onset schedule for all 100 cells is required, generate a new schedule with `gc_seeds.py` and copy its printed dictionary into `model.py`.

Each onset generates a burst of 5 spikes at 500 Hz. The fixed schedule is repeated every 500 ms for the entire simulation duration.

## GC–PC plasticity

GC–PC weights start at **4 nS** and are updated every **1 ms**:

`new_weight = max(0, previous_weight + eps * e * chi)`

| Parameter | Value |
|---|---:|
| `eps` | 0.01 |
| LTD window (`window_size`) | 60 ms |
| `chi` inside LTD window | -50 |
| `chi` outside LTD window | +1 |
| `T_e` | 6 ms |
| Eligibility scaling `I` | 1 |
| GC-to-eligibility-peak delay | 5 ms |
| Lower weight bound | 0 nS |
| Upper weight bound | none |

## Running the model

For a 150-s constant-input run, keep:

```python
protocol = "constant"
plasticity_enabled = True
constant_external_amplitude = 57.9
```

For the 1500-s three-level input protocol, use:

```python
protocol = "adaptation"
```

For fixed-weight controls, set:

```python
plasticity_enabled = False
```

The model writes `simulation_results.npz` with raw spike times, CFC membrane potential, sampled GC–PC weights, final weights, the protocol name, and the embedded GC schedule.

## Generating another GC schedule

Run:

```bash
python gc_seeds.py
```

Change `seed` at the top of `gc_seeds.py` to generate another schedule. The script prints a complete `elig_list = {...}` block that can be copied into `model.py`; no JSON file is needed.

## Reproducibility checklist

The repository explicitly specifies the exact GLIF variant, effective neuron parameters, reversal potentials and synaptic time constants, DC amplitudes, synaptic weights and delays, initial GC–PC weight, NEST RNG seed, GC schedule behavior, and plasticity parameters. The GC schedule is generated once and remains fixed during a run.

## NEST documentation

- https://nest-simulator.readthedocs.io/en/stable/models/glif_cond.html
- https://nest-simulator.readthedocs.io/en/v3.8/models/dc_generator.html

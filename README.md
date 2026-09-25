# HYACDCSIM

HYACDCSIM is a research software tool developed and owned by Universidad Pontificia Comillas.

![alt text](HYACDCSIM.jpg)

The principal author is Javier Renedo. The main contributors are Carlos Prieto, Saeed Rezaeian-Marjani, and Lukas Sigrist.

HYACDCSIM (Hybrid AC/DC system simulator) extends PSS/E with steady-state and dynamic models of multi-terminal DC (MTDC) systems, so that hybrid AC/DC power flows and electromechanical simulations can be run on existing AC cases. HYACDCSIM enables cascading simulations of hybrid AC/DC power systems. A detailed description is given in the [user manual](Usermanual/HY_ACDC_SIM_usermanual.pdf).

## Features

**Hybrid AC/DC power flow**

- Sequential AC/DC power flow: PSS/E solves the AC power flow, while the DC power flow (Newton-Raphson) and the AC/DC coupling are solved in Python. The call can substitute the standard PSS/E power-flow solution API.
- VSC stations modelled on the AC side by a transformer, an LC filter and a phase reactor, and on the DC side by a current source; converter losses follow the quadratic law `ploss = a + b·ic + c·ic²`, with separate quadratic terms for rectifier and inverter operation.
- Converter control modes: active power or DC voltage (DC slack) on the active-power axis, and reactive power or AC voltage magnitude on the reactive-power axis. VSCs appear as PV or PQ buses to the AC power flow.
- Multiple, electrically independent MTDC grids are supported and their DC power flows are solved simultaneously.
- Results summary covering DC bus quantities, DC branch quantities, AC/DC coupling losses (transformer, reactor, converter) and converter internal quantities, with convergence reported.

**Dynamic modelling**

- Automatic generation of the data needed for dynamic simulation: the DC-grid `.txt` data files (buses, lines, incidence matrix `Ac`, admittance matrix `Ydc`) and an updated `.dyr` file containing the converter, supplementary-control and DC-grid models.
- User-written PSS/E models (FORTRAN) in [_ForUserModels/](_ForUserModels/):
  - `VSCGFL` — grid-following VSC (generator-type, coordinated-call current-injecting model), vector control with a first-order inner current loop and PI outer loops, with P/Q limits, current limit (d-axis, q-axis or equal priority) and modulation-index limit.
  - `VSCDRO` — grid-forming VSC with angle/frequency and voltage droop (similar in structure to `REGFM_A1`).
  - `DDCGRD` — dynamic DC-grid model (governor-type): DC bus voltages and DC line currents as states, π-equivalent lines, `nb + nL` state variables.
  - `SDCGRD` — static DC-grid model: the DC network is solved algebraically, without DC-grid state variables.
  - `SPWDRD` — active-power-related supplementary control (exciter-type): distributed DC-voltage droop, frequency droop, time-optimal/Lyapunov control and synthetic inertia.
  - `SQWDRD` — reactive-power-related supplementary control (stabilizer-type): AC-voltage control and frequency-based power-oscillation damper.
  - `WDELAY` — communication delays between VSC stations for wide-area controls, constant or randomly varying according to a triangular density function (second-order Padé approximation).

## Running the tool

The tool is run in two stages.

**1. AC/DC power flow and generation of the dynamic data** — run [main_hyacdcsim.py](main_hyacdcsim.py). Before executing it, adapt the user-defined input block at the top of the file:

- `str_lffile`, `str_dyrfile` — the initial AC power flow (`.sav`) and dynamic (`.dyr`) files of the case under study.
- `str_MTDCdatafile` — the Excel file defining the MTDC systems (`define_grids_mtdc.xls`).
- `str_pathlffile`, `str_path4dynamics` — the input and simulation folders of the case.
- `issetdynamicfiles`, `issavedclfresults`, `isprogress` — whether the dynamic files are built, whether the AC/DC power-flow results are saved, and where progress information is reported.
- `lftol`, `lfmaxiter` — power-flow tolerance and maximum number of iterations.

The MTDC systems themselves are defined in the Excel file, in which each DC network is identified by a unique ID. It contains four sheets:

| Sheet | Content |
| --- | --- |
| `baseMVA` | Power rating of the MTDC system |
| `converter` | One row per converter: DC and AC bus numbers, transformer (`rt`, `xt`), filter (`bf`) and reactor (`rc`, `xc`) data, loss coefficients (`a`, `b`, `crect`, `cinv`), P/Q limits and ratings (per-unit values on the converter rating `rateA`) |
| `dcbus` | One row per DC bus: P and Q control modes, initial AC-side voltage and power, DC voltage set point, `Pdc`, `idc`, bus conductance `gdc` and capacitance `Cdc` (per-unit on `baseMVA`) |
| `dcbranch` | One row per DC branch: from/to DC bus, `rdc`, `Ldc`, `Ccc` and ratings (per-unit on `baseMVA`) |

Note that `Cdc` aggregates the converter capacitance and half of the capacitances of the branches connected to the VSC.

**2. Dynamic simulation** — the generated `.txt` files and the updated `.dyr` file are placed in the simulation folder of the case, together with the compiled DLL of the user-written models. The `.dyr` file must then be adapted to set appropriate parameter values for the user-written models; the parameter lists (CON, ICON, STATE) and the `.dyr` record format of each model are documented in the user manual. [Simulation/main_runsimulation.py](Simulation/main_runsimulation.py) shows how the simulation is set up and run from Python.

The repository is organised around the folders expected by the tool, with `main_hyacdcsim.py` at the same level:

- [_ForUserModels/](_ForUserModels/) — source of the user-written dynamic models.
- [_PyModules/](_PyModules/) — `module_acdc.py` (set-up and solution of the sequential AC/DC power flow, results display, generation of the dynamic data files) and `module_dclf.py` (DC power flow and DC-slack iteration).
- [Input/](Input/) — one subfolder per case, with the initial `.sav` and `.dyr` files and the MTDC definition file.
- [Simulation/](Simulation/) — one subfolder per case, with the compiled DLL of the user-written models and the automatically generated `data_Buses_base.txt`, `data_Lines_base.txt`, `data_acdcbus.txt`, `data_Ac.txt` and `data_Ydc.txt`. The DLL and the `.txt` files must be located in the same folder.

## Requirements

- PSS/E version 34, which runs on Python 2.7 (32 bit).
- A NumPy package compatible with that Python distribution, installed from `\Python27\Scripts` with `pip install <package name>`.
- An Intel Visual Fortran compiler compatible with PSS/E 34, needed to compile the user-written models in [_ForUserModels/](_ForUserModels/) into the DLL used by the dynamic simulations.

## Citation

If you use HYACDCSIM in research, teaching, a publication, report, thesis, or other scholarly work, please cite the software and the following publications:

1. S. Rezaeian-Marjani, L. Sigrist, and A. García-Cerrada, “Dynamic Cascading Simulations of Hybrid AC/DC Power Systems in PSS/E,” *Energies*, vol. 19, no. 7, article 1611, 2026. [https://doi.org/10.3390/en19071611](https://doi.org/10.3390/en19071611)

2. J. Renedo, A. García-Cerrada, L. Rouco, L. Sigrist, I. Egido, and S. Sanz Verdugo, “Development of a PSS/E tool for power-flow calculation and dynamic simulation of VSC-HVDC multi-terminal systems,” in *13th IET International Conference on AC and DC Power Transmission (ACDC 2017)*, pp. 1–6, 2017. [https://doi.org/10.1049/cp.2017.0060](https://doi.org/10.1049/cp.2017.0060)

Machine-readable citation metadata are provided in [`CITATION.cff`](CITATION.cff). GitHub displays these metadata through **Cite this repository**.

## Contributing

Contributions are welcome through GitHub issues and pull requests.

Unless explicitly agreed otherwise in writing, contributions submitted for inclusion in HYACDCSIM are provided under the GNU General Public License version 3 only (`GPL-3.0-only`). Contributors retain copyright in their original contributions unless copyright has been assigned under a separate written agreement.

By submitting a contribution, you confirm that you have the right to provide it under `GPL-3.0-only` and that it does not contain confidential, proprietary, personal, or otherwise restricted material.

## Copyright and licence

Copyright (C) Universidad Pontificia Comillas.

HYACDCSIM is licensed under the GNU General Public License version 3 only (`GPL-3.0-only`). See [`LICENSE`](LICENSE) for the complete licence text.

You may use, study, modify, and distribute the software, including for commercial purposes, subject to the terms of `GPL-3.0-only`. Covered modified versions that are distributed must comply with the GPL source-code, notice, and same-licence requirements.

This summary is provided for convenience only. The `LICENSE` file contains the binding licence terms.

## Disclaimer

The software is provided without warranty, as stated in the licence. Users are responsible for validating the software and its results for their intended application.

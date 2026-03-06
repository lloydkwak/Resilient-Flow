# DIRCA-S: Dynamical Intermediate Representation Control Architecture with Safe-Stop

This repository implements **DIRCA-S**, a novel decoupled hierarchical framework designed for **Fault-Tolerant Physical AI**. By drawing inspiration from the LLVM compiler paradigm, the system completely decouples task-space kinematic intent from joint-space physical execution. This ensures robust sensorimotor control, hardware agnosticism, and graceful degradation even under severe morphological failures (e.g., locked joints, actuator loss).

## 1. Overview

Traditional Vision-Language-Action (VLA) models attempt to map visual inputs directly to joint-space actions, leading to catastrophic out-of-distribution (OOD) failures when the robot's physical constraints change. **DIRCA-S** solves this by establishing an abstraction layer:

* **Front-End (Flow Matching Planner):** Generates morphology-agnostic, task-space $SE(3)$ vector fields (the "Intermediate Representation" or IR) based on visual observations. It is completely blind to the robot's hardware state.
* **Back-End (Whole-Body Compiler):** A classical Operational Space Controller (OSC) that runs at 1kHz. It receives the task-space IR and compiles it into optimal joint torques ($\tau$) by exploiting the robot's kinematic redundancy via Jacobian null-space projection.
* **Safety Layer (Passive Dissipator):** A mathematically grounded Safe-Stop mechanism that monitors the manipulability ellipsoid ($\det(JJ^T)$). If an unreachable singularity is detected due to severe fault, it safely dissipates the system's kinetic energy using a Control Lyapunov Function (CLF), preventing physical blow-ups.

## 2. Architecture and Data Flow

The architecture operates asynchronously to ensure both cognitive flexibility and physical stability:

1. **Global Planning (20Hz):** The Flow Matching policy constructs an optimal transport spatial flow ($\dot{x}_{IR}$) based on visual context, without concerning itself with the robot's physical health.
2. **Fault Monitoring (1kHz):** A momentum-based observer continuously monitors sensor residuals to dynamically update the fault mask ($m_{fault}$).
3. **Local Execution & Safe Abort (1kHz):** - **Nominal/Recoverable:** The controller actively projects the task into the null-space of the broken joints, calculating torques using only the surviving actuators.
   - **Infeasible/Singularity:** If the target flow is unreachable, the system triggers the **Safe-Stop** protocol, transitioning to a highly damped state ($\tau = -B\dot{q}$) to absorb external impacts.

## 3. Key Features

* **Morphology Agnosticism:** The Front-End generates pure $SE(3)$ task flows, enabling zero-shot cross-embodiment transfer.
* **Extreme Resilience:** Decoupled Back-End ensures 1ms response to joint failures without waiting for the heavy vision model to replan.
* **Provable Safety:** Lyapunov-based energy dissipation guarantees the system will not diverge or oscillate when confronted with kinematically impossible commands.

---

## 4. Installation

Ensure you have a CUDA-capable GPU, Python 3.10+, and Docker installed (recommended).

```bash
git clone [https://github.com/your_username/Resilient-Flow.git](https://github.com/your_username/Resilient-Flow.git)
cd Resilient-Flow
pip install -r requirements.txt
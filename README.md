# Resilient-Flow: Fault-Tolerant Robotic Control via Flow Matching and CfC

This repository implements **Resilient-Flow**, a novel hierarchical framework designed for **Fault-Tolerant Physical AI**. By combining the deterministic trajectory generation of Flow Matching (FM) with the ultra-fast, continuous-time dynamic adaptation of Closed-form Continuous-time Neural Networks (CfC), the system achieves robust sensorimotor control even under severe hardware failures and unexpected external perturbations.

## 1. Overview

Traditional Vision-Language-Action (VLA) models assume perfect hardware conditions, often leading to catastrophic failure when physical constraints change (e.g., joint locked, external impact). **Resilient-Flow** shifts the paradigm from "optimization for success" to "graceful degradation and survival" through a biologically inspired dual-loop architecture:

* **High-Level Brain (Flow Matching Policy):** Generates 16-step optimal kinematic trajectories based on visual observations and current physical health conditions.
* **Low-Level Nerve (CfC Controller):** Translates kinematic intents into continuous torque commands, instantly adapting to dynamic changes and identifying structural faults in real-time.

## 2. Architecture and Data Flow

The architecture operates asynchronously to ensure both cognitive flexibility and physical stability:

1. **Strategic Planning:** The Flow Matching policy solves the Probability Flow ODE to construct a 16-step spatial trajectory $x_{16}$ that routes around identified physical limitations.
2. **Visuomotor Execution:** The CfC neural muscle smoothly interpolates and executes this trajectory by outputting high-frequency torque signals ($\tau$) that account for the robot's real-time mass, friction, and inertia.
3. **Resilience Feedback Loop:** If the CfC detects an anomaly (via residual errors between predicted latent states and actual proprioception), it constructs a `Fault_Context` tensor. This tensor is asynchronously fed back to the FM, triggering immediate replanning or a "Safe Abort".

## 3. Key Features

* **OT-Flow for Trajectory Generation:** Fast, deterministic 16-step spatial path generation using Optimal Transport Flow Matching.
* **Liquid Neural Muscle:** 1ms control loop via CfC (Liquid AI) for dynamic compliance and external force rejection.
* **Self-Healing Replanning:** Real-time bottom-up feedback that explicitly conditions the high-level planner with localized fault diagnostics.
* **Safe Abort Protocol:** Automatically evaluates the reachability of the workspace and transitions to an energy-minimizing neutral pose when the goal is physically impossible.

---

## 4. Installation

Ensure you have a CUDA-capable GPU and Python 3.8+.

```bash
git clone https://github.com/your_username/Resilient-Flow.git
cd Resilient-Flow
pip install -r requirements.txt

```

**Key Dependencies:** `torch`, `torchcfm`, `ncps` (Neural Circuit Policies), `mujoco`, `robosuite`.

---

## 5. Pipeline Execution

### A. Data Engine (Fault-Injection Simulation)

Generate baseline trajectories and Oracle-guided fault recovery data using MPC:

```bash
python3 scripts/generate_fault_dataset.py --env mujoco_panda --fault_type joint_lock

```

### B. High-Level Brain Training (Flow Matching)

Train the conditional vector field generator to plan routes based on visual and fault contexts:

```bash
python3 scripts/train_fm_planner.py --config config/fm_planner.yaml

```

### C. Low-Level Nerve Training (CfC)

Train the continuous-time torque controller via imitation learning:

```bash
python3 scripts/train_cfc_muscle.py --config config/cfc_torque.yaml

```

---

## 6. Evaluation

### Nominal Evaluation

Test the baseline performance without any hardware faults:

```bash
python3 eval_nominal.py

```

### Fault-Tolerant Evaluation (Closed-Loop)

Inject real-time faults and evaluate the system's replanning and safe abort capabilities:

```bash
python3 scripts/eval_resilience.py --inject_fault true --fault_timestep 50

```

---

## Citation

If you use this framework in your research, please cite:

```bibtex
@article{yourname2026resilientflow,
  title={Resilient-Flow: Fault-Tolerant Robotic Control via Flow Matching and Continuous-time Neural Adaptation},
  author={Your Name},
  journal={In Preparation},
  year={2026}
}

```

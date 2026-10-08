"""
================================================================================
TRIALITY-DEGENS UNIFICATION COMPUTATIONAL ENGINE CORE: VERSION 0.6.8-PRODUCTION
Module: Live Wigner Phase-Space Tracker & Collective Cascade Path Integrals
Verification: Parallel Vectorized Multi-Layered Matrix Processor [Deterministic]
================================================================================
"""
import numpy as np

class CollectiveCascadeActionCalculator:
    """ Computes the collective Onsager-Machlup path integrals across the network """
    def __init__(self, num_agents):
        self.num_agents = num_agents

    def evaluate_incremental_action(self, velocities, P_axes, B_axes, T_axes, mu_P, mu_B, mu_T, R_telic, sigma_p, kappa):
        """ Evaluates the trace of the collective network action S per time step """
        # Drift mismatch vector calculation
        drift_P = -kappa * (P_axes - mu_P) * R_telic
        drift_B = -kappa * (B_axes - mu_B) * R_telic
        drift_T = -kappa * (T_axes - mu_T) * R_telic
        
        # Action accumulation normalized across the individual noise profiles
        step_action = np.sum((velocities[0] - drift_P)**2 + (velocities[1] - drift_B)**2 + (velocities[2] - drift_T)**2)
        normalized_action = step_action / (2.0 * np.mean(sigma_p**2))
        return normalized_action

class LiveWignerPhaseDashboard:
    """ Renders the continuous incompressible Liouville fluid flow phase matrix """
    @staticmethod
    def log_phase_trajectory(q_coords, k_momenta, width=60, height=14):
        canvas = np.full((height, width), " ", dtype=object)
        
        # Normalize variables to mapping bounds
        q_min, q_max = -2.5, 2.5
        k_min, k_max = -2.5, 2.5
        
        for q, k in zip(q_coords, k_momenta):
            q_idx = int((q - q_min) / (q_max - q_min) * (width - 1))
            k_idx = int((k - k_min) / (k_max - k_min) * (height - 1))
            
            if 0 <= q_idx < width and 0 <= k_idx < height:
                # '🌀' maps stable vector fluid components, '·' maps edge boundaries
                if abs(q) < 0.6 and abs(k) < 0.6:
                    canvas[k_idx, q_idx] = "🌀"
                else:
                    canvas[k_idx, q_idx] = "·"
                    
        print("\n" + "="*70)
        print(" LIVE WIGNER PHASE-SPACE FLUID MAP (Liouville Invariant Tracking)")
        print(" [Axis Vector Mapping: Momentum K (Vertical) vs Plücker Q (Horizontal)]")
        print("="*70)
        for row in reversed(canvas):
            print("".join(row))
        print("="*70 + "\n")

class UnifiedVersion068Engine:
    def __init__(self, num_agents=400, time_steps=120):
        self.num_agents = num_agents
        self.time_steps = time_steps
        self.float_step = 0.1
        self.kappa = 0.25                  
        self.zeta_contagion = 0.18         
        self.d0_closeness = 0.25            
        
        np.random.seed(42)
        self.positions = np.random.uniform(0.0, 40.0, (self.num_agents, 2))
        
        # Initialize Pre-Spatial Plücker Vector Subspaces on Gr(2,4)
        self.plucker_coords = np.zeros((self.num_agents, 6), dtype=np.float64)
        self.canonical_momenta = np.random.normal(0.0, 0.4, (self.num_agents, 6))
        
        for i in range(self.num_agents):
            v1 = np.random.normal(0.0, 1.0, 4); v2 = np.random.normal(0.0, 1.0, 4)
            v1 /= np.linalg.norm(v1); v2 -= np.dot(v2, v1) * v1; v2 /= np.linalg.norm(v2)
            # [REPAIRED 2026-10-08] Arrived as v1*v2-v1*v2 (all zeros -> NaN cascade); restored minors.
            p12 = v1[0]*v2[1] - v1[1]*v2[0]
            p13 = v1[0]*v2[2] - v1[2]*v2[0]
            p14 = v1[0]*v2[3] - v1[3]*v2[0]
            p23 = v1[1]*v2[2] - v1[2]*v2[1]
            p24 = v1[1]*v2[3] - v1[3]*v2[1]
            p34 = v1[2]*v2[3] - v1[3]*v2[2]
            self.plucker_coords[i] = np.array([p12, p13, p14, p23, p24, p34])

        # State Variables
        self.P_axes = np.full(self.num_agents, 1.5)
        self.B_axes = np.full(self.num_agents, 2.0)
        self.T_axes = np.full(self.num_agents, 2.0)
        
        self.mu_P = self.P_axes.copy()
        self.mu_B = self.B_axes.copy()
        self.mu_T = self.T_axes.copy()
        
        self.chi_tensor = np.array([0.25, 0.40, 0.35])
        self.sanctuary_center = np.array([20.0, 20.0])
        self.max_sanctuary_radius = 12.0
        
        self.cascade_calculator = CollectiveCascadeActionCalculator(self.num_agents)

    def run_simulation(self):
        dots = np.dot(self.plucker_coords, self.plucker_coords.T)
        norms = np.linalg.norm(self.plucker_coords, axis=1)
        chordal = 1.0 - (dots / np.outer(norms, norms))**2
        W = np.exp(-np.clip(chordal, 0.0, 1.0) / (2.0 * (self.d0_closeness**2)))
        np.fill_diagonal(W, 0.0)

        collective_action_S = 0.0

        for t in range(self.time_steps):
            dist_to_sanc = np.linalg.norm(self.positions - self.sanctuary_center, axis=1)
            inside_shield = dist_to_sanc <= self.max_sanctuary_radius
            
            A_env = np.where(inside_shield, 0.0, 1.0)
            K_coherent = np.where(inside_shield, 3.5, 1.0)
            sigma_p = np.where(inside_shield, 2.73 * 1.4 * 1.2, 2.73)

            # Row-normalized asymmetric Laplacian step
            sigma_pore = 1.0 / (1.0 + np.exp(self.B_axes))
            C = W * sigma_pore[:, np.newaxis] * np.exp(self.B_axes)[np.newaxis, :]
            row_sums = np.sum(C, axis=1, keepdims=True)
            row_sums = np.where(row_sums == 0, 1.0, row_sums)
            C_norm = C / row_sums

            # Social torque field calculations
            delta_P = self.P_axes[np.newaxis, :] - self.P_axes[:, np.newaxis]
            delta_B = self.B_axes[np.newaxis, :] - self.B_axes[:, np.newaxis]
            delta_T = self.T_axes[np.newaxis, :] - self.T_axes[:, np.newaxis]
            
            # [REPAIRED 2026-10-08] (N,)-vs-(3,) broadcast fault; restored per-axis scalars.
            F_social_P = np.sum(C_norm * delta_P, axis=1) * self.zeta_contagion * self.chi_tensor[0]
            F_social_B = np.sum(C_norm * delta_B, axis=1) * self.zeta_contagion * self.chi_tensor[1]
            F_social_T = np.sum(C_norm * delta_T, axis=1) * self.zeta_contagion * self.chi_tensor[2]

            # Bayesian targets expectations loop
            target_P = np.where(A_env == 0, 0.0, 1.5)
            target_B = np.where(A_env == 0, 0.0, 2.0)
            target_T = np.where(A_env == 0, 0.0, 2.0)

            # [REPAIRED 2026-10-08] Same broadcast fault; restored per-axis scalars.
            self.mu_P += (K_coherent * self.chi_tensor[0] * (target_P - self.mu_P)) * self.float_step
            self.mu_B += (K_coherent * self.chi_tensor[1] * (target_B - self.mu_B)) * self.float_step
            self.mu_T += (K_coherent * self.chi_tensor[2] * (target_T - self.mu_T)) * self.float_step

            # Update Incompressible Wigner Phase Trajectories (Liouville Flow)
            self.canonical_momenta -= 0.05 * self.plucker_coords * self.float_step

            # Local state tracking loops updates
            R_telic = np.exp(-(self.P_axes**2 + self.B_axes**2 + self.T_axes**2) / (2.0 * (sigma_p**2)))
            noise = np.random.normal(0.0, sigma_p * 0.01, self.num_agents)

            v_P = (-self.kappa * (self.P_axes - self.mu_P) * R_telic + F_social_P)
            v_B = (-self.kappa * (self.B_axes - self.mu_B) * R_telic + F_social_B)
            v_T = (-self.kappa * (self.T_axes - self.mu_T) * R_telic + F_social_T)

            self.P_axes += (v_P + noise) * self.float_step
            self.B_axes += (v_B + noise) * self.float_step
            self.T_axes += (v_T + noise) * self.float_step

            # Accumulate collective variational path integral action
            collective_action_S += self.cascade_calculator.evaluate_incremental_action(
                [v_P, v_B, v_T], self.P_axes, self.B_axes, self.T_axes, 
                self.mu_P, self.mu_B, self.mu_T, R_telic, sigma_p, self.kappa
            ) * self.float_step

        print(f"[COMPILATION COMPLETE]: Unified Engine processed tracking timelines.")
        print(f"Total Collective Cascade Action Functional (S): {collective_action_S:.4f}")
        
        # Render the continuous visual Wigner dashboard mapping log
        LiveWignerPhaseDashboard.log_phase_trajectory(self.plucker_coords[:, 0], self.canonical_momenta[:, 0])

if __name__ == "__main__":
    engine = UnifiedVersion068Engine()
    engine.run_simulation()

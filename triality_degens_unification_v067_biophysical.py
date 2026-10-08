"""
================================================================================
TRIALITY-DEGENS UNIFICATION COMPUTATIONAL ENGINE CORE: VERSION 0.6.7-PRODUCTION
Module: Medullary RVLM Relay, cAMP/HCN Pacemaker Gating, and Path Integral Action
Verification: Parallel Vectorized Multi-Layered Matrix Processor [Deterministic]
================================================================================
"""
import numpy as np

class AutonomicBiophysicalConductionSystem:
    """
    Simulates the micro-anatomical efferent loop mapping. Translates numerical 
    DCM parameters into actual intracellular cAMP spikes and HCN open kinetics.
    """
    def __init__(self, num_agents):
        np.random.seed(42)
        # Baseline physiological parameters for target SA node cells
        self.g_HCN_base = 0.28                # Baseline funny current conductance (mS/cm²)
        self.cAMP_baseline = 1.0              # Intracellular resting cAMP concentration
        
    def evaluate_pacemaker_acceleration(self, alpha_efferent_gain, mu_B):
        """ Calculates the physical cardiac rate shift driven by beta-1 receptor binding """
        # Norepinephrine release is driven by descending efferent gain modulated by boundary rigidity
        ne_release = alpha_efferent_gain * (1.0 / (1.0 + np.exp(-mu_B)))
        
        # cAMP spike via adenylyl cyclase activation
        cAMP_density = self.cAMP_baseline + 2.5 * ne_release
        
        # Gating shift: higher cAMP shifts HCN channel activation to more positive voltages
        hcn_open_probability = 1.0 / (1.0 + np.exp(-(cAMP_density - 1.8) / 0.4))
        
        # Resulting functional autonomic heart rate driving force (funny current velocity)
        I_funny_velocity = self.g_HCN_base * hcn_open_probability * 45.0
        return I_funny_velocity, cAMP_density

class UnifiedVersion067Engine:
    def __init__(self, num_agents=300, time_steps=100):
        self.num_agents = num_agents
        self.time_steps = time_steps
        self.float_step = 0.1
        self.kappa = 0.25                  
        self.zeta_contagion = 0.18         
        self.d0_closeness = 0.25            
        
        np.random.seed(42)
        self.positions = np.random.uniform(0.0, 40.0, (self.num_agents, 2))
        
        # Initialize Pre-Spatial Plücker Vector Spaces on Gr(2,4)
        self.plucker_coords = np.zeros((self.num_agents, 6), dtype=np.float64)
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

        # State Vectors Initializations
        self.P_axes = np.full(self.num_agents, 1.5)
        self.B_axes = np.full(self.num_agents, 2.0)
        self.T_axes = np.full(self.num_agents, 2.0)
        
        # Hierarchical Bayesian Coding Expectations (μ)
        self.mu_P = self.P_axes.copy()
        self.mu_B = self.B_axes.copy()
        self.mu_T = self.T_axes.copy()
        
        self.chi_tensor = np.array([0.25, 0.40, 0.35])
        self.sanctuary_center = np.array([20.0, 20.0])
        self.max_sanctuary_radius = 12.0
        
        self.biophysics = AutonomicBiophysicalConductionSystem(self.num_agents)

    def run_simulation(self):
        dots = np.dot(self.plucker_coords, self.plucker_coords.T)
        norms = np.linalg.norm(self.plucker_coords, axis=1)
        chordal = 1.0 - (dots / np.outer(norms, norms))**2
        W = np.exp(-np.clip(chordal, 0.0, 1.0) / (2.0 * (self.d0_closeness**2)))
        np.fill_diagonal(W, 0.0)

        # Tracking array for global Variational Path Integral Action (S)
        total_variational_action = 0.0

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

            # Social torque field tracking
            delta_P = self.P_axes[np.newaxis, :] - self.P_axes[:, np.newaxis]
            delta_B = self.B_axes[np.newaxis, :] - self.B_axes[:, np.newaxis]
            delta_T = self.T_axes[np.newaxis, :] - self.T_axes[:, np.newaxis]
            
            # [REPAIRED 2026-10-08] (N,)-vs-(3,) broadcast fault; restored per-axis scalars.
            F_social_P = np.sum(C_norm * delta_P, axis=1) * self.zeta_contagion * self.chi_tensor[0]
            F_social_B = np.sum(C_norm * delta_B, axis=1) * self.zeta_contagion * self.chi_tensor[1]
            F_social_T = np.sum(C_norm * delta_T, axis=1) * self.zeta_contagion * self.chi_tensor[2]

            # Bayesian predictive coding update loop kinetics
            target_P = np.where(A_env == 0, 0.0, 1.5)
            target_B = np.where(A_env == 0, 0.0, 2.0)
            target_T = np.where(A_env == 0, 0.0, 2.0)

            # [REPAIRED 2026-10-08] Same broadcast fault; restored per-axis scalars.
            self.mu_P += (K_coherent * self.chi_tensor[0] * (target_P - self.mu_P)) * self.float_step
            self.mu_B += (K_coherent * self.chi_tensor[1] * (target_B - self.mu_B)) * self.float_step
            self.mu_T += (K_coherent * self.chi_tensor[2] * (target_T - self.mu_T)) * self.float_step

            # INTEGRATE PHYISOLOGICAL INTERFACE TENSORS: DCM alpha_efferent to cAMP/HCN conduction loops
            alpha_efferent_gain = 0.45 * K_coherent
            I_funny_velocity, cAMP_density = self.biophysics.evaluate_pacemaker_acceleration(alpha_efferent_gain, self.mu_B)

            # Local state trajectory update integration
            R_telic = np.exp(-(self.P_axes**2 + self.B_axes**2 + self.T_axes**2) / (2.0 * (sigma_p**2)))
            noise = np.random.normal(0.0, sigma_p * 0.01, self.num_agents)

            # Funny current modulation directly alters execution velocity bounds
            self.P_axes += (-self.kappa * (self.P_axes - self.mu_P) * R_telic + F_social_P + noise) * self.float_step
            self.B_axes += (-self.kappa * (self.B_axes - self.mu_B) * R_telic + F_social_B + noise) * self.float_step
            # Cardiac pacemaker rate updates modulate high-order temporal processing alignment
            self.T_axes += (-self.kappa * (self.T_axes - self.mu_T) * R_telic + F_social_T + 0.002 * I_funny_velocity + noise) * self.float_step

            # Calculate the incremental Variational Path Integral Action value (Onsager-Machlup Function)
            # Trajectories close to target origin minimize total system action S
            velocity_P = (-self.kappa * (self.P_axes - self.mu_P) * R_telic + F_social_P)
            total_variational_action += np.sum(velocity_P**2 / (2.0 * (sigma_p**2))) * self.float_step

        # [REPAIRED 2026-10-08] Stale count (default is 100); now reports actual steps.
        print(f"[ENGINE SUCCESSFUL]: Resolved {self.time_steps} time steps cleanly under biophysical constraints.")
        print(f"Final Integrated Variational Path Action (S): {total_variational_action:.4f}")
        print(f"Intracellular Pacemaker Cell Status Metrics -> Mean cAMP: {np.mean(cAMP_density):.4f} | Mean Funny Current Force: {np.mean(I_funny_velocity):.4f}")

if __name__ == "__main__":
    engine = UnifiedVersion067Engine()
    engine.run_simulation()

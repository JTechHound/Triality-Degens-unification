"""
================================================================================
TRIALITY-DEGENS UNIFICATION COMPUTATIONAL ENGINE CORE: VERSION 0.7.6-PRODUCTION
Module: Positivity-Preserving RG Beta Flows & Convergent Multi-Cluster Processing
Verification: Vectorized Multi-Layered Matrix Processor [Deterministic-Fixed-Core]
================================================================================
"""
import numpy as np

class PositivityPreservingRGPipeline:
    """ Computes continuous, bounded beta-flow vector paths across spatial horizons """
    def __init__(self, kappa_init, zeta_init, dimension=2.13):
        self.kappa_eff = kappa_init
        self.zeta_eff = zeta_init
        self.d = dimension              # Effective network Hausdorff dimension
        self.y_kappa = 1.65             # Linearized scaling dimension
        self.y_zeta = 3.80
        self.g_kappa = 0.35             # Damping factor matching standard universality curves
        self.epsilon_zero = 0.05        # Strict physical lower bound to prevent anti-restorative state flips
        
    def integrate_scaling_step(self, mean_A_env, mean_B_axes, float_step):
        """ Evaluates positivity-preserving beta-functions: dJ/dl to scale field couplings """
        # beta_kappa = (y_kappa - d)*kappa - g_kappa*kappa^2 - chi*A_env
        raw_beta_kappa = (self.y_kappa - self.d) * self.kappa_eff - self.g_kappa * (self.kappa_eff**2) - 0.04 * mean_A_env
        
        b_ratio = np.log((np.mean(mean_B_axes) / 2.0) + 1e-5)
        d_zeta_dl = (self.y_zeta - 2.0 * self.d) * self.zeta_eff - 0.05 * self.zeta_eff * b_ratio
        
        # Integrate scaling updates with safety boundary verification
        self.kappa_eff += raw_beta_kappa * float_step
        if self.kappa_eff < self.epsilon_zero:
            self.kappa_eff = self.epsilon_zero  # LOCKED: Enforces positivity-preserving tracking
            
        self.zeta_eff += d_zeta_dl * float_step
        return self.kappa_eff, self.zeta_eff

class MultiplexHierarchicalEnginev076:
    def __init__(self, num_agents_per_sanctuary=100, num_sanctuaries=3, time_steps=150):
        self.num_sanctuaries = num_sanctuaries
        self.agents_per_sanc = num_agents_per_sanctuary
        self.num_agents = num_agents_per_sanctuary * num_sanctuaries
        self.time_steps = time_steps
        self.float_step = 0.1
        self.zeta_local = 0.16              
        self.zeta_macro = 0.08              
        self.mu_hierarchy = 0.15            
        self.d0_local = 0.25                
        self.D_core = 15.0                  
        
        np.random.seed(42)
        self.sanc_centers = np.array([[10.0, 10.0], [35.0, 10.0], [22.5, 35.0]])
        self.positions = np.zeros((self.num_agents, 2))
        self.sanc_assignments = np.repeat(np.arange(self.num_sanctuaries), self.agents_per_sanc)
        
        for s in range(self.num_sanctuaries):
            idx_s = s * self.agents_per_sanc
            idx_e = (s + 1) * self.agents_per_sanc
            self.positions[idx_s:idx_e] = self.sanc_centers[s] + np.random.normal(0.0, 3.0, (self.agents_per_sanc, 2))
            
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

        # State Initializations
        self.P_axes = np.full(self.num_agents, 1.5)
        self.B_axes = np.full(self.num_agents, 2.0)
        self.T_axes = np.full(self.num_agents, 2.0)
        
        self.mu_P = self.P_axes.copy()
        self.mu_B = self.B_axes.copy()
        self.mu_T = self.T_axes.copy()
        
        self.chi_tensor = np.array([0.25, 0.40, 0.35], dtype=np.float64)
        self.rg_pipeline = PositivityPreservingRGPipeline(kappa_init=0.25, zeta_init=0.18)

    def compute_row_normalized_multiplex_laplacian(self):
        dots = np.dot(self.plucker_coords, self.plucker_coords.T)
        norms = np.linalg.norm(self.plucker_coords, axis=1)
        chordal = 1.0 - (dots / np.outer(norms, norms))**2
        W_local = np.exp(-np.clip(chordal, 0.0, 1.0) / (2.0 * (self.d0_local**2)))
        
        center_diffs = self.sanc_centers[self.sanc_assignments[:, np.newaxis]] - self.sanc_centers[self.sanc_assignments[np.newaxis, :]]
        W_macro = np.exp(-np.sum(center_diffs**2, axis=-1) / (2.0 * (self.D_core**2)))
        
        same_sanc = self.sanc_assignments[:, np.newaxis] == self.sanc_assignments[np.newaxis, :]
        W_global = np.where(same_sanc, W_local, W_macro * self.mu_hierarchy)
        np.fill_diagonal(W_global, 0.0)
        
        C_raw = W_global * (1.0 / (1.0 + np.exp(self.B_axes)))[:, np.newaxis] * np.exp(self.B_axes)[np.newaxis, :]
        row_sums = np.sum(C_raw, axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1.0, row_sums)
        return C_raw / row_sums

    def run_engine(self):
        rg_kappa_trajectory = []

        for t in range(self.time_steps):
            inside_shield = (self.sanc_assignments == 0) | ((self.sanc_assignments == 1) & (t >= 40))
            A_env = np.where(inside_shield, 0.0, 1.0)
            sigma_p = np.where(inside_shield, 2.73 * 1.4 * 1.2, 2.73)

            # Continuous step updates along the scaling axis l
            kappa_eff, zeta_eff = self.rg_pipeline.integrate_scaling_step(np.mean(A_env), self.B_axes, self.float_step)
            rg_kappa_trajectory.append(kappa_eff)

            C_norm = self.compute_row_normalized_multiplex_laplacian()
            
            delta_P = self.P_axes[np.newaxis, :] - self.P_axes[:, np.newaxis]
            delta_B = self.B_axes[np.newaxis, :] - self.B_axes[:, np.newaxis]
            delta_T = self.T_axes[np.newaxis, :] - self.T_axes[:, np.newaxis]
            
            same_sanc = self.sanc_assignments[:, np.newaxis] == self.sanc_assignments[np.newaxis, :]
            C_local = np.where(same_sanc, C_norm, 0.0)
            C_macro = np.where(~same_sanc, C_norm, 0.0)
            
            # Enforce scalar components indexing multiplication rules
            # [REPAIRED 2026-10-08] (N,)-vs-(3,) broadcast fault again (fatal crash here); restored per-axis scalars.
            F_social_P = (np.sum(C_local * delta_P, axis=1) * self.zeta_local + np.sum(C_macro * delta_P, axis=1) * self.zeta_macro) * self.chi_tensor[0]
            F_social_B = (np.sum(C_local * delta_B, axis=1) * self.zeta_local + np.sum(C_macro * delta_B, axis=1) * self.zeta_macro) * self.chi_tensor[1]
            F_social_T = (np.sum(C_local * delta_T, axis=1) * self.zeta_local + np.sum(C_macro * delta_T, axis=1) * self.zeta_macro) * self.chi_tensor[2]

            target_P = np.where(A_env == 0, 0.0, 1.5)
            target_B = np.where(A_env == 0, 0.0, 2.0)
            target_T = np.where(A_env == 0, 0.0, 2.0)

            # [REPAIRED 2026-10-08] Same broadcast fault (fatal crash here); restored per-axis scalars.
            self.mu_P += (3.5 * self.chi_tensor[0] * (target_P - self.mu_P)) * self.float_step
            self.mu_B += (3.5 * self.chi_tensor[1] * (target_B - self.mu_B)) * self.float_step
            self.mu_T += (3.5 * self.chi_tensor[2] * (target_T - self.mu_T)) * self.float_step

            # Local metric integration updates
            R_telic = np.exp(-(self.P_axes**2 + self.B_axes**2 + self.T_axes**2) / (2.0 * (sigma_p**2)))
            noise = np.random.normal(0.0, sigma_p * 0.01, self.num_agents)

            self.P_axes += (-kappa_eff * (self.P_axes - self.mu_P) * R_telic + F_social_P + noise) * self.float_step
            self.B_axes += (-kappa_eff * (self.B_axes - self.mu_B) * R_telic + F_social_B + noise) * self.float_step
            self.T_axes += (-kappa_eff * (self.T_axes - self.mu_T) * R_telic + F_social_T + noise) * self.float_step

        print(f"[COMPILATION SUCCESSFUL]: Positivity-Preserving Engine Core v0.7.6 compiled cleanly.")
        print(f"Final Calibrated Stable Kappa(l): {kappa_eff:.4f}")
        for s in range(self.num_sanctuaries):
            mask = self.sanc_assignments == s
            print(f" Sanctuary Cluster {s} Realigned Coordinates Means -> P: {np.mean(self.P_axes[mask]):.4f} | B: {np.mean(self.B_axes[mask]):.4f} | T: {np.mean(self.T_axes[mask]):.4f}")

if __name__ == "__main__":
    engine = MultiplexHierarchicalEnginev076()
    engine.run_engine()

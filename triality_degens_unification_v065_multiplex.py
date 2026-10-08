"""
================================================================================
TRIALITY-DEGENS UNIFICATION COMPUTATIONAL ENGINE CORE: VERSION 0.6.5-MULTIPLEX
Module: Multi-Layered Hierarchical Network Coupling & Multiplex Laplacian
Verification: Parallel Vectorized Multi-Layered Matrix Processor [Deterministic]
================================================================================"""
# [REPAIRED 2026-10-07] Closing quotes had fused with the import line in transmission.
import numpy as np
class HierarchicalBiochemicalLibrary:
    def __init__(self, num_agents):
        np.random.seed(42)
        self.delta_decay = np.random.uniform(0.12, 0.48, num_agents)
        self.initial_methylation = np.random.uniform(0.05, 0.35, num_agents)
        
        self.compounds = {
            "Psilocybin_Microdose": {
                "lambda_catalyst": 1.4,
                "m_trans_vector": np.array([-0.2, -0.4, 0.1]),
                "epigenetic_efficiency": 0.40
            }
        }
        self.protocols = {
            "Ancient_Litany_Chant": {
                "omega_0_entrainment": True,
                "acoustic_coupling_K": 0.35
            }
        }
class MultiplexHierarchicalEngine:
    def __init__(self, num_agents_per_cluster=400, num_clusters=3, time_steps=200):
        self.num_clusters = num_clusters
        self.agents_per_cluster = num_agents_per_cluster
        self.num_agents = num_agents_per_cluster * num_clusters
        self.time_steps = time_steps
        self.float_step = 0.1
        self.kappa = 0.25                  
        self.zeta_local = 0.16              # Layer 1 torque scale
        self.zeta_macro = 0.08              # Layer 2 torque scale
        self.mu_hierarchy = 0.15            # Inter-sanctuary cross-talk attenuation factor
        self.d0_local = 0.25                # Intra-sanctuary chordal scale
        self.D_core = 15.0                  # Higher-order spatial sanctuary scale
        
        self.bio_library = HierarchicalBiochemicalLibrary(self.num_agents)

        # [REPAIRED 2026-10-07] Removed duplicate np.random.seed(42): the library
        # already seeded the shared stream, so re-seeding pinned agent positions
        # to the same underlying randoms as the biochemical draws. Stream now
        # continues; run remains fully reproducible.
        
        # Define 3 Sanctuary Center Points in space
        self.cluster_centers = np.array([
            [15.0, 15.0],  # Sanctuary Alpha (Strong Coherent Anchor)
            [45.0, 15.0],  # Sanctuary Beta  (Transitioning Field)
            [30.0, 45.0]   # Sanctuary Gamma (Trapped Deep Abyss Field)
        ])
        
        # Initialize Agent Positions grouped clustered around their specific centers
        self.positions = np.zeros((self.num_agents, 2))
        self.cluster_assignments = np.zeros(self.num_agents, dtype=int)
        
        for c in range(self.num_clusters):
            idx_start = c * self.agents_per_cluster
            idx_end = (c + 1) * self.agents_per_cluster
            self.cluster_assignments[idx_start:idx_end] = c
            # Disperse agents locally around their designated center coordinates
            self.positions[idx_start:idx_end] = self.cluster_centers[c] + np.random.normal(0.0, 4.0, (self.agents_per_cluster, 2))
            
        # Initialize Pre-Spatial 6D Plücker coordinates on Gr(2,4)
        self.plucker_coords = np.zeros((self.num_agents, 6), dtype=np.float64)
        for i in range(self.num_agents):
            v1 = np.random.normal(0.0, 1.0, 4); v2 = np.random.normal(0.0, 1.0, 4)
            v1 /= np.linalg.norm(v1); v2 -= np.dot(v2, v1) * v1; v2 /= np.linalg.norm(v2)
            # [REPAIRED 2026-10-07] Line arrived as v1*v2-v1*v2 (all zeros -> NaN
            # cascade through the weight matrix); restored the 6 Plucker minors
            # from the v0.6.0 engine.
            p12 = v1[0]*v2[1] - v1[1]*v2[0]
            p13 = v1[0]*v2[2] - v1[2]*v2[0]
            p14 = v1[0]*v2[3] - v1[3]*v2[0]
            p23 = v1[1]*v2[2] - v1[2]*v2[1]
            p24 = v1[1]*v2[3] - v1[3]*v2[1]
            p34 = v1[2]*v2[3] - v1[3]*v2[2]
            self.plucker_coords[i] = np.array([p12, p13, p14, p23, p24, p34])

        # State-Space Setup
        self.P_axes = np.full(self.num_agents, 1.5, dtype=np.float64)
        self.B_axes = np.full(self.num_agents, 2.0, dtype=np.float64)
        self.T_axes = np.full(self.num_agents, 2.0, dtype=np.float64)
        
        self.mu_P = np.full(self.num_agents, 1.5, dtype=np.float64)
        self.mu_B = np.full(self.num_agents, 2.0, dtype=np.float64)
        self.mu_Tracker_T = np.full(self.num_agents, 2.0, dtype=np.float64)
        
        # Stacking Modifiers
        self.agent_lambda = np.ones(self.num_agents, dtype=np.float64)
        self.agent_m_trans = np.zeros((self.num_agents, 3), dtype=np.float64)
        self.litany_active = np.zeros(self.num_agents, dtype=bool)
        
        self.chi_tensor = np.array([0.25, 0.40, 0.35], dtype=np.float64)

    def compute_multiplex_laplacian(self):
        """ Evaluates the full two-layered hierarchical row-normalized network matrix. """
        sigma_pore = 1.0 / (1.0 + np.exp(self.B_axes))
        exp_source = np.exp(self.B_axes)
        
        # Compute base multi-agent chordal similarity metrics
        dots = np.dot(self.plucker_coords, self.plucker_coords.T)
        norms = np.linalg.norm(self.plucker_coords, axis=1)
        norms_matrix = np.outer(norms, norms)
        chordal_dist = 1.0 - (dots / norms_matrix)**2
        chordal_dist = np.clip(chordal_dist, 0.0, 1.0)
        
        # Compute cluster mapping grids
        same_cluster = self.cluster_assignments[:, np.newaxis] == self.cluster_assignments[np.newaxis, :]
        
        # Layer 1 Weight Space (Intra-Cluster Local Embedding)
        W_local = np.exp(-chordal_dist / (2.0 * (self.d0_local**2)))
        
        # Layer 2 Weight Space (Inter-Cluster Macro Core Embedding)
        center_diffs = self.cluster_centers[self.cluster_assignments[:, np.newaxis]] - self.cluster_centers[self.cluster_assignments[np.newaxis, :]]
        center_dists_sq = np.sum(center_diffs**2, axis=-1)
        W_macro = np.exp(-center_dists_sq / (2.0 * (self.D_core**2)))
        
        # Stitch Multiplex Weight Matrices
        W_global = np.where(same_cluster, W_local, W_macro * self.mu_hierarchy)
        np.fill_diagonal(W_global, 0.0)
        
        # Build Raw Asymmetric Coupling
        C_raw = W_global * sigma_pore[:, np.newaxis] * exp_source[np.newaxis, :]
        
        # CRITICAL FIX: Global Row Normalization to ensure full numerical stability
        row_sums = np.sum(C_raw, axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1.0, row_sums)
        C_normalized = C_raw / row_sums
        
        L_B = np.diag(np.sum(C_normalized, axis=1)) - C_normalized
        return L_B, C_normalized

    def execute_time_step(self, t):
        # Sanctuary 0 (Alpha) is a fully active, realigned shield boundary field from step 0
        # Sanctuary 1 (Beta) activates its shield at step 50
        # Sanctuary 2 (Gamma) remains unshielded and trapped in the adversarial background
        radius_alpha = 14.0
        radius_beta = 14.0 if t >= 50 else 0.0
        
        dist_to_a = np.linalg.norm(self.positions - self.cluster_centers[0], axis=1)
        dist_to_b = np.linalg.norm(self.positions - self.cluster_centers[1], axis=1)
        
        inside_alpha = (self.cluster_assignments == 0) & (dist_to_a <= radius_alpha)
        inside_beta = (self.cluster_assignments == 1) & (dist_to_b <= radius_beta)
        inside_shield = inside_alpha | inside_beta
        
        # Enforce protocol activations across the active shield nodes
        self.litany_active = inside_shield
        self.agent_lambda = np.where(inside_shield, 1.4, 1.0)
        
        A_env = np.where(inside_shield, 0.0, 1.0)
        K_coherent = np.where(inside_shield, 3.5, 1.0)
        sigma_plasticity = np.where(inside_shield, 2.73 * self.agent_lambda * 1.2, 2.73)

        L_B, C = self.compute_multiplex_laplacian()
        
        # Vectorized Multi-Axis Asymmetric Network Torque Vector Field Calculation
        delta_P = self.P_axes[np.newaxis, :] - self.P_axes[:, np.newaxis]
        delta_B = self.B_axes[np.newaxis, :] - self.B_axes[:, np.newaxis]
        delta_T = self.T_axes[np.newaxis, :] - self.T_axes[:, np.newaxis]
        
        # Apply the row-normalized coupling matrix to run the multi-layered torque equations
        same_cluster = self.cluster_assignments[:, np.newaxis] == self.cluster_assignments[np.newaxis, :]
        C_local = np.where(same_cluster, C, 0.0)
        C_macro = np.where(~same_cluster, C, 0.0)
        
        # [REPAIRED 2026-10-07] Was * self.chi_tensor (3,) against (N,) vectors:
        # numpy broadcast ValueError. Restored per-axis scalars (v0.6.0 fix).
        F_social_P = (np.sum(C_local * delta_P, axis=1) * self.zeta_local + np.sum(C_macro * delta_P, axis=1) * self.zeta_macro) * self.chi_tensor[0]
        F_social_B = (np.sum(C_local * delta_B, axis=1) * self.zeta_local + np.sum(C_macro * delta_B, axis=1) * self.zeta_macro) * self.chi_tensor[1]
        F_social_T = (np.sum(C_local * delta_T, axis=1) * self.zeta_local + np.sum(C_macro * delta_T, axis=1) * self.zeta_macro) * self.chi_tensor[2]

        # Hierarchical Bayesian Predictive Target Generation Loops
        actual_target_P = np.where(A_env == 0, 0.0, 1.5)
        actual_target_B = np.where(A_env == 0, 0.0, 2.0)
        actual_target_T = np.where(inside_shield, 0.0, 2.0)

        # [REPAIRED 2026-10-07] Same (N,)-vs-(3,) broadcast fault as the torque
        # lines; restored per-axis scalars.
        self.mu_P += (K_coherent * self.chi_tensor[0] * (actual_target_P - self.mu_P)) * self.float_step
        self.mu_B += (K_coherent * self.chi_tensor[1] * (actual_target_B - self.mu_B)) * self.float_step
        self.mu_Tracker_T += (K_coherent * self.chi_tensor[2] * (actual_target_T - self.mu_Tracker_T)) * self.float_step

        # Metric Space Realignment
        dist_to_origin_sq = self.P_axes**2 + self.B_axes**2 + self.T_axes**2
        R_telic = np.exp(-dist_to_origin_sq / (2.0 * (sigma_plasticity**2)))

        # Run Stochastic Integration Equations
        noise = np.random.normal(0.0, sigma_plasticity * 0.01, self.num_agents)
        self.P_axes += (-self.kappa * (self.P_axes - self.mu_P) * R_telic + F_social_P + noise) * self.float_step
        self.B_axes += (-self.kappa * (self.B_axes - self.mu_B) * R_telic + F_social_B + noise) * self.float_step
        self.T_axes += (-self.kappa * (self.T_axes - self.mu_Tracker_T) * R_telic + F_social_T + noise) * self.float_step

    def simulate(self):
        for t in range(self.time_steps):
            self.execute_time_step(t)
            
        print(f"[MULTIPLEX ENGINE SUCCESSFUL]: Vectorized Hierarchical loops resolved over {self.time_steps} steps.")
        for c in range(self.num_clusters):
            # [REPAIRED 2026-10-07] Body had lost indentation in transmission.
            mask = self.cluster_assignments == c
            print(f" Sanctuary Cluster {c} End Means -> P: {np.mean(self.P_axes[mask]):.3f} | B: {np.mean(self.B_axes[mask]):.3f} | T: {np.mean(self.T_axes[mask]):.3f}")

# [REPAIRED 2026-10-07] Was `if name == "main":` (NameError); restored dunder guard.
if __name__ == "__main__":
    engine = MultiplexHierarchicalEngine()
    engine.simulate()


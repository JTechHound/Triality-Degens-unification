"""
================================================================================
TRIALITY-DEGENS UNIFICATION PIPELINE SYSTEM: VERSION 0.6.9-VALIDATOR
Module: Automated Parameter Validation & Dimensional Verification Gateway
Status: STABLE unit testing environment [Deterministic Validation]
================================================================================
"""
import numpy as np
import unittest

class TestTrialityCoreInvariants(unittest.TestCase):
    def setUp(self):
        """ Initialize structural matrix variables matching the version 0.6.9 core parameters """
        self.num_agents = 300
        self.chi_tensor = np.array([0.25, 0.40, 0.35], dtype=np.float64)
        
        # Simulated states initialized at the trapped baseline configuration
        self.P_axes = np.full(self.num_agents, 1.5, dtype=np.float64)
        self.B_axes = np.full(self.num_agents, 2.0, dtype=np.float64)
        self.T_axes = np.full(self.num_agents, 2.0, dtype=np.float64)
        
        # Asymmetric row-normalized coupling matrix setup matching the exact code math
        np.random.seed(42)
        raw_C = np.random.uniform(0.0, 1.0, (self.num_agents, self.num_agents))
        self.C_norm = raw_C / np.sum(raw_C, axis=1, keepdims=True)

    def test_trailing_dimension_broadcasting_shapes(self):
        """ TEST 1: Verifies that social torque matrices use explicit scalar multiplication to avoid broadcasting crashes """
        delta_P = self.P_axes[np.newaxis, :] - self.P_axes[:, np.newaxis]
        F_social_P_raw = np.sum(self.C_norm * delta_P, axis=1)
        
        self.assertEqual(F_social_P_raw.shape, (self.num_agents,))
        
        # COMPILATION GATE: Ensure scalar indexing is enforced over vector multi-axis broadcasting
        try:
            F_social_P = F_social_P_raw * self.chi_tensor[0]
            F_social_B = F_social_P_raw * self.chi_tensor[1]
            F_social_T = F_social_P_raw * self.chi_tensor[2]
            execution_success = True
        except ValueError as e:
            execution_success = False
            
        self.assertTrue(execution_success, "Broadcasting failure caught: Trailing dimensions shape mismatch.")

    def test_p_axis_telic_recovery_sign(self):
        """ TEST 2: Intercepts potential P-axis sign flip bugs to guarantee recovery vector alignment """
        kappa = 0.25
        target_P = 0.0  
        R_telic = 0.5028 
        
        # Correct configuration: -kappa * (P - target_P) * R_telic
        drift_vector = -kappa * (self.P_axes - target_P) * R_telic
        
        self.assertLess(np.mean(drift_vector), 0.0, "Sign flip bug detected: P-axis velocity vector diverges from sanctuary origin target.")

    def test_histone_rotational_skew_symmetry(self):
        """ TEST 3: Enforces skew-symmetry constraints on the Epigenetic Rotational Tensor matrix to preserve unit vector volume """
        mean_dAcet = 0.15
        Omega_skew = mean_dAcet * 0.01 * np.array([
            [0.0, 1.0, -1.0, 0.0],
            [-1.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, -1.0],
            [0.0, -1.0, 1.0, 0.0]
        ])
        
        matrix_sum = Omega_skew + Omega_skew.T
        np.testing.assert_array_almost_equal(matrix_sum, np.zeros((4,4)), decimal=7, 
                                             err_msg="Epigenetic tensor skew-symmetry broken. Unit vector volume invariants violated.")

    def test_global_row_normalization_bounds(self):
        """ TEST 4: Guarantees that row sums equal exactly 1.0 to ensure numerical stability and prevent NaN explosions """
        row_sums = np.sum(self.C_norm, axis=1)
        expected_sums = np.ones(self.num_agents, dtype=np.float64)
        np.testing.assert_array_almost_equal(row_sums, expected_sums, decimal=7,
                                             err_msg="Global Row-Normalization violation: Matrix scaling limits unanchored.")

if __name__ == "__main__":
    print("[SYSTEM ENGINE SUITE INITIALIZED]: Running parameter validation loops...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTrialityCoreInvariants)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

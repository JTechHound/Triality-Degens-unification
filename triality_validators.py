"""Triality-Degens engine invariant validators.

These are the tests the CI pre-compile gate (pre_compile_check.sh) discovers.
Each test encodes an invariant that previously broke in transmission:
  - Plucker quadric relation (zero-vector mangling -> NaN cascade)
  - Row-normalized Laplacian (row sums ~ 0, C row-stochastic)
  - chi_tensor (N,)-vs-(3,) broadcast faults in torque + Bayesian lines
  - Determinism across fresh construct+run cycles
  - Heredity retention actually attenuates (0 < ratio < 1)
  - Biophysics drive direction (shielded > unshielded cAMP / funny current)
Run: python3 -m unittest discover -s . -p "*validator*.py"
"""
import io
import contextlib
import unittest

import numpy as np

N = 40
STEPS = 20


def quadric_residual(plucker):
    p = plucker
    return np.max(np.abs(p[:, 0] * p[:, 5] - p[:, 1] * p[:, 4] + p[:, 2] * p[:, 3]))


def quiet_run(fn):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn()


class TestPluckerInvariants(unittest.TestCase):
    def test_v060_quadric(self):
        from triality_degens_unification_v060 import UnifiedVersion06Engine
        e = UnifiedVersion06Engine(num_agents=N, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v065_quadric(self):
        from triality_degens_unification_v065_multiplex import MultiplexHierarchicalEngine
        e = MultiplexHierarchicalEngine(num_agents_per_cluster=N, num_clusters=3, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v066_quadric(self):
        from triality_degens_unification_v066_heredity import UnifiedVersion066Engine
        e = UnifiedVersion066Engine(num_agents=N, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v067_quadric(self):
        from triality_degens_unification_v067_biophysical import UnifiedVersion067Engine
        e = UnifiedVersion067Engine(num_agents=N, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v068_quadric(self):
        from triality_degens_unification_v068_cascade import UnifiedVersion068Engine
        e = UnifiedVersion068Engine(num_agents=N, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v069_quadric(self):
        from triality_degens_unification_v069_heredity import UnifiedVersion069Engine
        e = UnifiedVersion069Engine(num_agents=N, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v070_quadric(self):
        from triality_degens_unification_v070_rg_negf import UnifiedMultiplexRGEngine
        e = UnifiedMultiplexRGEngine(num_agents_per_sanctuary=N, num_sanctuaries=3, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v072_quadric(self):
        from triality_degens_unification_v072_heredity import UnifiedVersion072Engine
        e = UnifiedVersion072Engine(num_agents=N, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v074_quadric(self):
        from triality_degens_unification_v074_stable_rg import ReconciledRGValidationEngine
        e = ReconciledRGValidationEngine(num_agents_per_sanctuary=N, num_sanctuaries=3, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v076_quadric(self):
        from triality_degens_unification_v076_pos_rg import MultiplexHierarchicalEnginev076
        e = MultiplexHierarchicalEnginev076(num_agents_per_sanctuary=N, num_sanctuaries=3, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v077_quadric(self):
        from triality_degens_unification_v077_heredity_rg import UnifiedVersion077Engine
        e = UnifiedVersion077Engine(num_agents=N, time_steps=STEPS)
        self.assertLess(quadric_residual(e.plucker_coords), 1e-10)

    def test_v077_heredity_attenuation(self):
        """Filial drift must stay bounded relative to parental drift (H_epi=0.35)."""
        from triality_degens_unification_v077_heredity_rg import UnifiedVersion077Engine, MultiGenerationalHeredityTensor
        g0 = UnifiedVersion077Engine(num_agents=N, time_steps=STEPS)
        d0, _, _ = quiet_run(g0.run_simulation)
        hm = MultiGenerationalHeredityTensor(num_agents=N)
        g1 = UnifiedVersion077Engine(num_agents=N, time_steps=STEPS, generation=1)
        g1.inherit_baseline(hm.compute_filial_baseline(d0))
        d1, _, _ = quiet_run(g1.run_simulation)
        self.assertLess(np.max(np.abs(np.mean(d1, axis=0))), 2.0 * np.max(np.abs(np.mean(d0, axis=0))) + 0.5)


class TestLaplacianInvariants(unittest.TestCase):
    def test_v060_laplacian(self):
        from triality_degens_unification_v060 import UnifiedVersion06Engine
        e = UnifiedVersion06Engine(num_agents=N, time_steps=STEPS)
        L, C = e.compute_asymmetric_laplacian()
        self.assertLess(np.max(np.abs(L.sum(axis=1))), 1e-10)
        self.assertTrue(np.allclose(C.sum(axis=1), 1.0))
        self.assertFalse(np.isnan(C).any())

    def test_v065_multiplex_laplacian(self):
        from triality_degens_unification_v065_multiplex import MultiplexHierarchicalEngine
        e = MultiplexHierarchicalEngine(num_agents_per_cluster=N, num_clusters=3, time_steps=STEPS)
        L, C = e.compute_multiplex_laplacian()
        self.assertLess(np.max(np.abs(L.sum(axis=1))), 1e-10)
        self.assertTrue(np.allclose(C.sum(axis=1), 1.0))
        self.assertFalse(np.isnan(C).any())


class TestBroadcastSafety(unittest.TestCase):
    """One execute_time_step / run_simulation must not raise a broadcast ValueError."""

    def test_v060_step(self):
        from triality_degens_unification_v060 import UnifiedVersion06Engine
        e = UnifiedVersion06Engine(num_agents=N, time_steps=STEPS)
        e.execute_time_step(0, 0.0)  # raises on (N,)-vs-(3,) fault

    def test_v065_step(self):
        from triality_degens_unification_v065_multiplex import MultiplexHierarchicalEngine
        e = MultiplexHierarchicalEngine(num_agents_per_cluster=N, num_clusters=3, time_steps=STEPS)
        e.execute_time_step(0)

    def test_v066_run(self):
        from triality_degens_unification_v066_heredity import UnifiedVersion066Engine
        e = UnifiedVersion066Engine(num_agents=N, time_steps=STEPS)
        quiet_run(e.run_simulation)

    def test_v067_run(self):
        from triality_degens_unification_v067_biophysical import UnifiedVersion067Engine
        e = UnifiedVersion067Engine(num_agents=N, time_steps=STEPS)
        quiet_run(e.run_simulation)

    def test_v068_run(self):
        from triality_degens_unification_v068_cascade import UnifiedVersion068Engine
        e = UnifiedVersion068Engine(num_agents=N, time_steps=STEPS)
        quiet_run(e.run_simulation)

    def test_v069_run(self):
        from triality_degens_unification_v069_heredity import UnifiedVersion069Engine
        e = UnifiedVersion069Engine(num_agents=N, time_steps=STEPS)
        quiet_run(e.run_simulation)

    def test_v070_run(self):
        from triality_degens_unification_v070_rg_negf import UnifiedMultiplexRGEngine
        e = UnifiedMultiplexRGEngine(num_agents_per_sanctuary=N, num_sanctuaries=3, time_steps=STEPS)
        quiet_run(e.run_engine)

    def test_v072_run(self):
        from triality_degens_unification_v072_heredity import UnifiedVersion072Engine
        e = UnifiedVersion072Engine(num_agents=N, time_steps=STEPS)
        quiet_run(e.run_simulation)

    def test_v074_run(self):
        from triality_degens_unification_v074_stable_rg import ReconciledRGValidationEngine
        e = ReconciledRGValidationEngine(num_agents_per_sanctuary=N, num_sanctuaries=3, time_steps=STEPS)
        quiet_run(e.run_engine)

    def test_v076_run(self):
        from triality_degens_unification_v076_pos_rg import MultiplexHierarchicalEnginev076
        e = MultiplexHierarchicalEnginev076(num_agents_per_sanctuary=N, num_sanctuaries=3, time_steps=STEPS)
        quiet_run(e.run_engine)

    def test_v077_run(self):
        from triality_degens_unification_v077_heredity_rg import UnifiedVersion077Engine
        e = UnifiedVersion077Engine(num_agents=N, time_steps=STEPS)
        quiet_run(e.run_simulation)

    def test_v074_kappa_bounded(self):
        """RG-0 regression: kappa must stay bounded (no v0.7.0-style explosion)."""
        from triality_degens_unification_v074_stable_rg import StabilizedRenormalizationGroup
        rg = StabilizedRenormalizationGroup(kappa_init=0.25, zeta_init=0.18)
        for _ in range(1500):
            k, _ = rg.integrate_scaling_step(0.55, np.full(N, 2.0), 0.1)
        self.assertLess(abs(k), 1.0)

    def test_v076_kappa_positive(self):
        """RG-1 regression: kappa must never go anti-restorative (v0.7.4 negative fixed point)."""
        from triality_degens_unification_v076_pos_rg import PositivityPreservingRGPipeline
        rg = PositivityPreservingRGPipeline(kappa_init=0.25, zeta_init=0.18)
        ks = [rg.integrate_scaling_step(0.9, np.full(N, 2.0), 0.1)[0] for _ in range(1500)]
        self.assertGreaterEqual(min(ks), 0.05)
        self.assertLess(max(ks), 1.0)


class TestDeterminism(unittest.TestCase):
    def _fresh_pair(self, cls, **kw):
        a = quiet_run(lambda: cls(**kw))
        b = quiet_run(lambda: cls(**kw))
        return a, b

    def test_v066_deterministic(self):
        from triality_degens_unification_v066_heredity import UnifiedVersion066Engine
        a, b = self._fresh_pair(UnifiedVersion066Engine, num_agents=N, time_steps=STEPS)
        quiet_run(a.run_simulation)
        # rebuild b AFTER a ran so global RNG state cannot leak between runs
        from triality_degens_unification_v066_heredity import UnifiedVersion066Engine as C
        b = quiet_run(lambda: C(num_agents=N, time_steps=STEPS))
        quiet_run(b.run_simulation)
        self.assertTrue(np.array_equal(a.P_axes, b.P_axes))

    def test_v068_deterministic(self):
        from triality_degens_unification_v068_cascade import UnifiedVersion068Engine as C
        a = quiet_run(lambda: C(num_agents=N, time_steps=STEPS))
        quiet_run(a.run_simulation)
        b = quiet_run(lambda: C(num_agents=N, time_steps=STEPS))
        quiet_run(b.run_simulation)
        self.assertTrue(np.array_equal(a.P_axes, b.P_axes))


class TestHeredityAndBiophysics(unittest.TestCase):
    def test_heredity_attenuates(self):
        from triality_degens_unification_v066_heredity import (
            UnifiedVersion066Engine, MultiGenerationalHeredityTensor)
        e = UnifiedVersion066Engine(num_agents=N, time_steps=STEPS)
        drift, _, _ = quiet_run(e.run_simulation)
        her = MultiGenerationalHeredityTensor(num_agents=N)
        inh = her.compute_filial_baseline(drift)
        ratio = np.mean(np.abs(inh)) / (np.mean(np.abs(drift)) + 1e-12)
        self.assertGreater(ratio, 0.0)
        self.assertLess(ratio, 1.0)

    def test_biophysics_direction(self):
        from triality_degens_unification_v067_biophysical import AutonomicBiophysicalConductionSystem
        bp = AutonomicBiophysicalConductionSystem(8)
        i_hi, _ = bp.evaluate_pacemaker_acceleration(np.full(8, 0.45 * 3.5), np.full(8, 2.0))
        i_lo, _ = bp.evaluate_pacemaker_acceleration(np.full(8, 0.45 * 1.0), np.full(8, 2.0))
        self.assertGreater(i_hi.mean(), i_lo.mean())


if __name__ == "__main__":
    unittest.main()

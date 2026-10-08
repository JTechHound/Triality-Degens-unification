"""Real-data visualizations for the Triality-Degens engines (v0.6.5 multiplex, v0.6.6 heredity).
All plots are drawn from validated simulation output -- no mockups.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from triality_degens_unification_v065_multiplex import MultiplexHierarchicalEngine
from triality_degens_unification_v066_heredity import (
    UnifiedVersion066Engine, MultiGenerationalHeredityTensor)

OUT = "visualizations"
import os
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- 1. Multiplex
print("running v0.6.5 multiplex ...")
mx = MultiplexHierarchicalEngine(num_agents_per_cluster=100, num_clusters=3, time_steps=200)
names = ["Alpha (shielded t=0)", "Beta (shield t=50)", "Gamma (unshielded)"]
colors = ["#2dd4bf", "#60a5fa", "#f87171"]
hist = {c: {"P": [], "B": [], "T": []} for c in range(3)}
for t in range(mx.time_steps):
    mx.execute_time_step(t)
    for c in range(3):
        m = mx.cluster_assignments == c
        hist[c]["P"].append(mx.P_axes[m].mean())
        hist[c]["B"].append(mx.B_axes[m].mean())
        hist[c]["T"].append(mx.T_axes[m].mean())

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
for i, ax_name in enumerate(["P", "B", "T"]):
    ax = axes[i]
    for c in range(3):
        ax.plot(hist[c][ax_name], color=colors[c], lw=1.6, label=names[c])
    ax.axvline(50, color="white", ls="--", lw=1, alpha=0.5)
    ax.set_title(f"Cluster mean {ax_name}-axis over time")
    ax.set_xlabel("time step")
    ax.grid(alpha=0.2)
axes[0].set_ylabel("axis value")
axes[0].legend(fontsize=8)
fig.suptitle("v0.6.5 Multiplex: sanctuary shield dynamics (Beta shield activates t=50)")
fig.tight_layout()
fig.savefig(f"{OUT}/v065_multiplex_dynamics.png", dpi=110)
plt.close(fig)

# spatial snapshot, colored by cluster, sized by B_axes
fig, ax = plt.subplots(figsize=(7, 6))
for c in range(3):
    m = mx.cluster_assignments == c
    ax.scatter(mx.positions[m, 0], mx.positions[m, 1], s=8 + 30 * (mx.B_axes[m] / mx.B_axes.max()),
               color=colors[c], alpha=0.7, label=names[c])
for cc in mx.cluster_centers:
    ax.scatter([cc[0]], [cc[1]], s=180, marker="*", color="gold", edgecolors="black", zorder=5)
ax.set_title("v0.6.5: agent field at t=200 (dot size = B-axis, stars = sanctuary cores)")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(fontsize=8); ax.grid(alpha=0.2)
fig.tight_layout(); fig.savefig(f"{OUT}/v065_spatial_field.png", dpi=110); plt.close(fig)

# ---------------------------------------------------------------- 2. Heredity
print("running v0.6.6 heredity chain ...")
N_GENS = 5
gen_means, gen_stds = [], []
drift = None
her = None
q_all, k_all, gen_id = [], [], []
for g in range(N_GENS):
    eng = UnifiedVersion066Engine(num_agents=120, time_steps=60, generation=g)
    if drift is not None:
        eng.inherit_baseline(her.compute_filial_baseline(drift))
    drift, qf, kf = eng.run_simulation()
    if her is None:
        her = MultiGenerationalHeredityTensor(num_agents=120)
    gen_means.append(drift.mean(axis=0))
    gen_stds.append(drift.std(axis=0))
    q_all.append(qf); k_all.append(kf); gen_id += [g] * len(qf)
gen_means = np.array(gen_means)
gen_stds = np.array(gen_stds)

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(N_GENS)
w = 0.22
for i, (lbl, col) in enumerate(zip(["P drift", "B drift", "T drift"], ["#2dd4bf", "#60a5fa", "#f87171"])):
    ax.bar(x + (i - 1) * w, gen_means[:, i], w, yerr=gen_stds[:, i],
           label=lbl, color=col, alpha=0.85, capsize=3)
ax.set_xticks(x); ax.set_xticklabels([f"G{g}" for g in range(N_GENS)])
ax.set_title("v0.6.6: mean drift transmitted across generations (H_epi=0.35 retention)")
ax.set_ylabel("mean drift from origin"); ax.legend(); ax.grid(alpha=0.2, axis="y")
fig.tight_layout(); fig.savefig(f"{OUT}/v066_heredity_chain.png", dpi=110); plt.close(fig)

# ---------------------------------------------------------------- 3. Phase space
q_all = np.concatenate(q_all); k_all = np.concatenate(k_all); gen_id = np.array(gen_id)
fig, ax = plt.subplots(figsize=(7, 6))
sc = ax.scatter(q_all, k_all, c=gen_id, cmap="viridis", s=6, alpha=0.6)
plt.colorbar(sc, ax=ax, label="generation")
ax.set_title("v0.6.6: Wigner phase-space (Q vs K) across 5 generations")
ax.set_xlabel("Plucker Q (p12)"); ax.set_ylabel("canonical momentum K")
ax.grid(alpha=0.2)
fig.tight_layout(); fig.savefig(f"{OUT}/v066_phase_space.png", dpi=110); plt.close(fig)

print("done:", sorted(os.listdir(OUT)))

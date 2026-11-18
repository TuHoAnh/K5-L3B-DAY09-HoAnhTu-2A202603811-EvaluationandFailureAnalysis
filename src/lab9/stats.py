"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

import inspect
from collections.abc import Sequence

import numpy as np
from scipy.stats import bootstrap

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    if len(human) != len(judge):
        raise ValueError("human and judge labels must have equal lengths")
    pairs = [(str(h).strip().upper(), str(j).strip().upper()) for h, j in zip(human, judge)]
    tp = sum(h == POS and j == POS for h, j in pairs)
    fp = sum(h != POS and j == POS for h, j in pairs)
    fn = sum(h == POS and j != POS for h, j in pairs)
    tn = sum(h != POS and j != POS for h, j in pairs)
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    cm = confusion(human, judge)
    precision = cm["tp"] / (cm["tp"] + cm["fp"]) if cm["tp"] + cm["fp"] else 0.0
    recall = cm["tp"] / (cm["tp"] + cm["fn"]) if cm["tp"] + cm["fn"] else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    n = len(human)
    if n == 0:
        raise ValueError("cohen_kappa requires at least one label")
    cm = confusion(human, judge)
    p_o = (cm["tp"] + cm["tn"]) / n
    p_e = ((cm["tp"] + cm["fp"]) * (cm["tp"] + cm["fn"])
           + (cm["fn"] + cm["tn"]) * (cm["fp"] + cm["tn"])) / (n * n)
    if abs(1.0 - p_e) < 1e-12:
        raise ValueError("cohen_kappa is undefined when p_e == 1")
    return (p_o - p_e) / (1.0 - p_e)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    denom = sensitivity + specificity - 1.0
    if denom <= 1e-12:
        return min(1.0, max(0.0, float(observed_rate)))
    corrected = (observed_rate + specificity - 1.0) / denom
    return min(1.0, max(0.0, float(corrected)))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    if len(a) != len(b) or len(a) == 0:
        raise ValueError("paired samples must have equal, non-zero lengths")
    a_arr = np.asarray(a, dtype=float)
    b_arr = np.asarray(b, dtype=float)
    if np.array_equal(a_arr, b_arr):
        return (0.0, 0.0, 0.0)
    delta = float(np.mean(a_arr) - np.mean(b_arr))
    statistic = lambda x, y, axis=-1: np.mean(x, axis=axis) - np.mean(y, axis=axis)
    rng_arg = {"rng": np.random.default_rng(rng)} if "rng" in inspect.signature(bootstrap).parameters else {
        "random_state": np.random.default_rng(rng)
    }
    res = bootstrap((a_arr, b_arr), statistic, paired=True, n_resamples=n_resamples,
                    method="percentile", confidence_level=confidence, **rng_arg)
    return (delta, float(res.confidence_interval.low), float(res.confidence_interval.high))


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError

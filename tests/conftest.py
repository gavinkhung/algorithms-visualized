"""Shared test setup: draw off-screen, so the suite runs headless."""

import matplotlib

matplotlib.use("Agg")

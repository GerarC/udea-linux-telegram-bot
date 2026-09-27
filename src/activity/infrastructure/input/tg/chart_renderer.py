import io

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from activity.domain.model.monthly_activity import MonthlyActivity
from activity.domain.utils.constants import MONTH_ABBREVIATIONS

# NOTE: single sequential hue (magnitude, one series - no legend needed) and muted
# chart chrome, matching this project's dataviz palette (see dataviz skill).
_BAR_COLOR = "#2a78d6"
_SURFACE_COLOR = "#fcfcfb"
_PRIMARY_INK = "#0b0b0b"
_SECONDARY_INK = "#52514e"
_MUTED_INK = "#898781"
_GRIDLINE_COLOR = "#e1e0d9"
_BASELINE_COLOR = "#c3c2b7"


def _month_label(entry: MonthlyActivity) -> str:
    return f"{MONTH_ABBREVIATIONS[entry.period_month.month - 1]} {entry.period_month.year % 100:02d}"


def render_monthly_activity_chart(history: list[MonthlyActivity]) -> bytes:
    labels = [_month_label(entry) for entry in history]
    values = [entry.message_count for entry in history]

    fig, ax = plt.subplots(figsize=(7, 4), dpi=160)
    fig.patch.set_facecolor(_SURFACE_COLOR)
    ax.set_facecolor(_SURFACE_COLOR)

    # NOTE: width < 1 leaves air around each bar instead of filling the slot.
    bars = ax.bar(labels, values, width=0.5, color=_BAR_COLOR, zorder=3)

    max_value = max(values, default=0)
    headroom = max(max_value * 0.15, 1)
    ax.set_ylim(0, max_value + headroom)

    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + headroom * 0.1,
            f"{value:,}",
            ha="center",
            va="bottom",
            color=_SECONDARY_INK,
            fontsize=10,
        )

    ax.set_title("Actividad del grupo — últimos 6 meses", color=_PRIMARY_INK, fontsize=13, pad=16, loc="left")

    ax.tick_params(axis="x", colors=_MUTED_INK, labelsize=10, length=0)
    ax.tick_params(axis="y", colors=_MUTED_INK, labelsize=9, length=0)
    ax.yaxis.set_visible(max_value > 0)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(_BASELINE_COLOR)

    ax.yaxis.grid(True, color=_GRIDLINE_COLOR, linewidth=1, zorder=0)
    ax.set_axisbelow(True)

    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    return buffer.getvalue()

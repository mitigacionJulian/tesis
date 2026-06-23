"""Genera figuras PNG del marco conceptual — ViaData Medellín."""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import numpy as np

OUT = Path(__file__).parent
DPI = 200
FONT = "DejaVu Sans"


def save(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.35,
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"OK {path.name}")


def fig_arquitectura_mtv():
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Cliente
    ax.add_patch(FancyBboxPatch((3.2, 8.2), 3.6, 1.0, boxstyle="round,pad=0.05",
                                facecolor="#E8F4FC", edgecolor="#1565C0", linewidth=1.5))
    ax.text(5, 8.85, "Cliente (SPA)", ha="center", va="center", fontsize=11, fontweight="bold", fontfamily=FONT)
    ax.text(5, 8.45, "React · Vite · Leaflet", ha="center", va="center", fontsize=9, fontfamily=FONT)

    # Servidor capas
    layers = [
        ("API REST (Django REST Framework)", "#FFF3E0"),
        ("Lógica de negocio / predicciones", "#FFE0B2"),
        ("Acceso a datos (ORM / SQL)", "#FFCC80"),
        ("GeoDjango + PostGIS", "#FFB74D"),
    ]
    y0, h, w = 3.2, 0.85, 5.0
    x0 = 2.5
    for i, (label, color) in enumerate(layers):
        y = y0 + i * h
        ax.add_patch(FancyBboxPatch((x0, y), w, h - 0.08, boxstyle="square,pad=0.02",
                                    facecolor=color, edgecolor="#E65100", linewidth=1.2))
        ax.text(x0 + w / 2, y + (h - 0.08) / 2, label, ha="center", va="center", fontsize=9, fontfamily=FONT)
    ax.text(5, 7.5, "Servidor Django (monolito)", ha="center", fontsize=11, fontweight="bold", fontfamily=FONT)

    # BD
    ax.add_patch(FancyBboxPatch((2.8, 0.5), 4.4, 1.3, boxstyle="round,pad=0.05",
                                facecolor="#E3F2FD", edgecolor="#1565C0", linewidth=1.5))
    ax.text(5, 1.35, "PostgreSQL + PostGIS", ha="center", fontsize=10, fontweight="bold", fontfamily=FONT)
    ax.text(5, 0.85, "Incidentes · víctimas · catálogos · geometrías", ha="center", fontsize=8, fontfamily=FONT)

    # Flechas
    ax.annotate("", xy=(7.8, 7.8), xytext=(7.8, 6.8),
                arrowprops=dict(arrowstyle="-|>", color="#C62828", lw=1.8))
    ax.text(8.15, 7.3, "HTTP\n(JSON)", fontsize=8, color="#C62828", fontfamily=FONT)

    ax.annotate("", xy=(2.2, 6.8), xytext=(2.2, 7.8),
                arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.8))
    ax.text(1.0, 7.15, "Respuesta\nJSON/HTML", fontsize=8, color="#2E7D32", fontfamily=FONT, ha="center")

    ax.annotate("", xy=(5, 3.0), xytext=(5, 1.9),
                arrowprops=dict(arrowstyle="<->", color="#37474F", lw=1.8))
    ax.text(5.55, 2.45, "SQL / PostGIS", fontsize=8, fontfamily=FONT)

    save(fig, "fig_arquitectura_mtv.png")


def fig_flujo_datos():
    steps = [
        ("Mede\n(Excel)", "#E8F5E9", "#2E7D32"),
        ("Limpieza ETL\nmede_limpieza.py", "#FFF8E1", "#F9A825"),
        ("PostgreSQL\n+ PostGIS", "#E3F2FD", "#1565C0"),
        ("Consultas\nespaciales", "#E8EAF6", "#3949AB"),
        ("Tablero y mapa\ninteractivo", "#FCE4EC", "#C2185B"),
    ]
    bw = 1.72
    gap = 0.42
    margin_x = 0.75
    margin_right = 0.85
    bh = 1.45
    y_box = 0.85
    total_w = margin_x + margin_right + len(steps) * bw + (len(steps) - 1) * gap
    fig_h = 3.0

    fig, ax = plt.subplots(figsize=(12.5, fig_h))
    ax.set_xlim(0, total_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")
    ax.margins(x=0.02)

    x = margin_x
    cy = y_box + bh / 2
    for i, (label, fill, edge) in enumerate(steps):
        ax.add_patch(FancyBboxPatch(
            (x, y_box), bw, bh, boxstyle="round,pad=0.06",
            facecolor=fill, edgecolor=edge, linewidth=1.5, zorder=2,
        ))
        ax.text(x + bw / 2, cy, label, ha="center", va="center",
                fontsize=8.5, fontweight="bold", fontfamily=FONT, zorder=3)
        if i < len(steps) - 1:
            ax.annotate(
                "", xy=(x + bw + gap - 0.08, cy), xytext=(x + bw + 0.08, cy),
                arrowprops=dict(arrowstyle="-|>", color="#546E7A", lw=2),
                zorder=1,
            )
        x += bw + gap

    save(fig, "fig_flujo_datos_geoespacial.png")


def fig_taxonomia():
    fig, ax = plt.subplots(figsize=(7.5, 5.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.5)
    ax.axis("off")

    layers = [
        ("Descriptiva", 2.15, "#A5D6A7", "KPIs, series, mapa"),
        ("Diagnóstica", 1.85, "#FFF59D", "Índices, rankings P05"),
        ("Predictiva", 1.65, "#FFCC80", "Módulo /predicciones"),
        ("Prescriptiva", 1.55, "#FFAB91", "Asistente IA orientado"),
    ]
    cx = 4.2
    y = 0.8
    widths = [7.0, 5.4, 4.0, 2.6]
    for i, (name, h, color, note) in enumerate(layers):
        w = widths[i]
        w_top = widths[i + 1] if i + 1 < len(widths) else w * 0.42
        if i < len(layers) - 1:
            coords = [
                (cx - w / 2, y), (cx + w / 2, y),
                (cx + w_top / 2, y + h), (cx - w_top / 2, y + h),
            ]
            ax.add_patch(Polygon(coords, closed=True, facecolor=color,
                               edgecolor="#37474F", linewidth=1.2, zorder=2))
        else:
            ax.add_patch(Polygon(
                [(cx - w / 2, y), (cx + w / 2, y), (cx, y + h)],
                closed=True, facecolor=color, edgecolor="#37474F", linewidth=1.2, zorder=2,
            ))
        mid_y = y + h / 2
        ax.text(cx, mid_y + 0.12, name, ha="center", va="center",
                fontsize=10, fontweight="bold", fontfamily=FONT, zorder=3)
        ax.text(cx, mid_y - 0.28, note, ha="center", va="center",
                fontsize=7.5, fontfamily=FONT, color="#37474F", zorder=3)
        y += h

    save(fig, "fig_taxonomia_analitica.png")


def fig_modelo_estrella():
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    positions = {
        "center": (5.0, 5.0, 2.5, 1.15, "#FFE082", "Incidentes\n(hechos)"),
        "top": (5.0, 8.0, 2.1, 0.88, "#FFF9C4", "Tiempo"),
        "bottom": (5.0, 2.0, 2.1, 0.88, "#FFF9C4", "Víctima"),
        "left": (1.9, 5.0, 2.2, 0.95, "#FFF9C4", "Tipo de\nincidente"),
        "right": (8.1, 5.0, 2.1, 0.88, "#FFF9C4", "Ubicación"),
    }

    def draw_box(key):
        cx, cy, w, h, fc, text = positions[key]
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.04",
            facecolor=fc, edgecolor="#F57F17", linewidth=1.3, zorder=3,
        ))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=10,
                fontweight="bold", fontfamily=FONT, zorder=4)
        return cx, cy, w, h

    def connect(key_from, key_to):
        cx1, cy1, w1, h1 = positions[key_from][:4]
        cx2, cy2, w2, h2 = positions[key_to][:4]
        dx, dy = cx2 - cx1, cy2 - cy1
        norm = (dx ** 2 + dy ** 2) ** 0.5
        ux, uy = dx / norm, dy / norm
        x1 = cx1 + ux * (w1 / 2 + 0.05)
        y1 = cy1 + uy * (h1 / 2 + 0.05)
        x2 = cx2 - ux * (w2 / 2 + 0.05)
        y2 = cy2 - uy * (h2 / 2 + 0.05)
        ax.plot([x1, x2], [y1, y2], color="#78909C", lw=1.4, zorder=1)

    for k in ("top", "bottom", "left", "right"):
        connect("center", k)
    draw_box("center")
    for k in ("top", "bottom", "left", "right"):
        draw_box(k)

    save(fig, "fig_modelo_estrella.png")


def fig_holdout_validacion():
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    def panel_box(x, y, w, h, text, fc):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.05",
            facecolor=fc, edgecolor="#455A64", linewidth=1.2, zorder=2,
        ))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=8.5, fontfamily=FONT, zorder=3)

    # Panel in-sample
    ix, iw, ih, igap = 0.6, 3.5, 0.95, 0.35
    y1, y2 = 3.55, 2.25
    panel_box(ix, y1, iw, ih, "Modelo ajustado\ncon todos los meses", "#ECEFF1")
    panel_box(ix, y2, iw, ih, r"$R^2$ y MAPE in-sample", "#ECEFF1")
    ax.annotate("", xy=(ix + iw / 2, y2 + ih), xytext=(ix + iw / 2, y1),
                arrowprops=dict(arrowstyle="-|>", color="#455A64", lw=1.5), zorder=1)
    ax.add_patch(FancyBboxPatch(
        (ix - 0.2, y2 - 0.25), iw + 0.4, y1 + ih - y2 + 0.5,
        boxstyle="square,pad=0.02", fill=False, edgecolor="#90A4AE",
        linewidth=1.0, linestyle="--", zorder=0,
    ))
    ax.text(ix + iw / 2, y1 + ih + 0.45, "In-sample", ha="center",
            fontsize=10, fontweight="bold", fontfamily=FONT)

    # Panel hold-out
    hx = 4.6
    steps = [
        "Reservar últimos\n$N$ meses",
        "Entrenar sin\nesos meses",
        "Predecir meses\nreservados",
        r"MAPE hold-out" + "\n(métrica clave)",
    ]
    ys = [3.55, 2.65, 1.75, 0.85]
    for i, (text, y) in enumerate(zip(steps, ys)):
        panel_box(hx, y, iw, ih, text, "#E3F2FD")
        if i < len(steps) - 1:
            ax.annotate("", xy=(hx + iw / 2, ys[i + 1] + ih), xytext=(hx + iw / 2, y),
                        arrowprops=dict(arrowstyle="-|>", color="#1565C0", lw=1.5), zorder=1)
    ax.add_patch(FancyBboxPatch(
        (hx - 0.2, ys[-1] - 0.25), iw + 0.4, ys[0] + ih - ys[-1] + 0.5,
        boxstyle="square,pad=0.02", fill=False, edgecolor="#64B5F6",
        linewidth=1.0, linestyle="--", zorder=0,
    ))
    ax.text(hx + iw / 2, ys[0] + ih + 0.45, "Hold-out", ha="center",
            fontsize=10, fontweight="bold", fontfamily=FONT)

    # Decisión
    dx, dy, dw, dh = 8.5, 1.55, 2.0, 1.0
    ax.add_patch(FancyBboxPatch(
        (dx, dy), dw, dh, boxstyle="round,pad=0.06",
        facecolor="#FFCCBC", edgecolor="#E64A19", linewidth=1.3, zorder=2,
    ))
    ax.text(dx + dw / 2, dy + dh / 2, "Decisión\nde modelo", ha="center", va="center",
            fontsize=9, fontweight="bold", fontfamily=FONT, zorder=3)

    # Flechas hacia decisión (sin solapamiento)
    ax.annotate("", xy=(dx, dy + dh / 2), xytext=(ix + iw, y2 + ih / 2),
                arrowprops=dict(arrowstyle="-|>", color="#78909C", lw=1.3,
                                connectionstyle="arc3,rad=0.08"), zorder=1)
    ax.annotate("", xy=(dx, dy + dh / 2), xytext=(hx + iw, ys[-1] + ih / 2),
                arrowprops=dict(arrowstyle="-|>", color="#1565C0", lw=2.0,
                                connectionstyle="arc3,rad=-0.12"), zorder=1)
    ax.text(7.55, 1.15, "prioridad", ha="center", fontsize=8,
            fontstyle="italic", color="#1565C0", fontfamily=FONT)

    save(fig, "fig_holdout_validacion.png")


def fig_modelo_copo():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis("off")

    def box(cx, cy, text, w=1.85, h=0.72, fc="#BBDEFB", fs=9, bold=False):
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.04",
            facecolor=fc, edgecolor="#1565C0", linewidth=1.2, zorder=3,
        ))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, fontfamily=FONT,
                fontweight="bold" if bold else "normal", zorder=4)

    def link(x1, y1, x2, y2, dashed=False):
        ax.plot([x1, x2], [y1, y2], color="#78909C", lw=1.1,
                linestyle="--" if dashed else "-", zorder=1)

    cx, cy = 6.5, 4.6
    box(cx, cy, "Incidentes", w=2.1, h=0.85, fc="#90CAF9", fs=10, bold=True)

    dims = [
        (2.5, 7.2, "Víctima"),
        (10.5, 7.2, "Tipo\nincidente"),
        (2.5, 2.0, "Tiempo"),
        (10.5, 2.0, "Ubicación"),
    ]
    for dx, dy, label in dims:
        box(dx, dy, label, fc="#BBDEFB", bold=True)
        link(cx, cy, dx, dy)

    tiempo_children = [(1.2, 0.55, "Año"), (2.5, 0.55, "Mes"), (3.8, 0.55, "Día")]
    for tx, ty, label in tiempo_children:
        box(tx, ty, label, w=1.35, h=0.58, fc="#E3F2FD", fs=8)
        link(2.5, 2.0 - 0.36, tx, ty + 0.29, dashed=True)

    ubic_children = [(9.2, 0.55, "Comuna"), (10.5, 0.55, "Ciudad"), (11.8, 0.55, "Barrio")]
    for ux, uy, label in ubic_children:
        box(ux, uy, label, w=1.35, h=0.58, fc="#E3F2FD", fs=8)
        link(10.5, 2.0 - 0.36, ux, uy + 0.29, dashed=True)

    save(fig, "fig_modelo_copo_nieve.png")


def fig_metodologia():
    """Flujo metodológico de la investigación ViaData — Medellín."""
    phases = [
        ("1. Fuente Mede\n(datos abiertos)", "#E8F5E9", "#2E7D32"),
        ("2. ETL reproducible\nmede_limpieza.py", "#FFF8E1", "#F9A825"),
        ("3. Modelo de datos\nPostgreSQL + PostGIS", "#E3F2FD", "#1565C0"),
        ("4. Desarrollo del sistema\nDjango · React · API REST", "#F3E5F5", "#6A1B9A"),
        ("5. Análisis y predicciones\nTablero · mapa · hold-out", "#FFE0B2", "#E65100"),
        ("6. Validación\ntécnica y de modelos", "#ECEFF1", "#37474F"),
    ]
    bw, bh = 4.2, 0.95
    gap = 0.38
    fig_h = len(phases) * (bh + gap) + 1.2
    fig, ax = plt.subplots(figsize=(6.5, fig_h))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    cx = 5.0
    y = fig_h - 1.0
    for i, (label, fc, ec) in enumerate(phases):
        ax.add_patch(FancyBboxPatch(
            (cx - bw / 2, y - bh), bw, bh, boxstyle="round,pad=0.05",
            facecolor=fc, edgecolor=ec, linewidth=1.4,
        ))
        ax.text(cx, y - bh / 2, label, ha="center", va="center",
                fontsize=9.5, fontfamily=FONT, fontweight="bold")
        if i < len(phases) - 1:
            ax.annotate(
                "", xy=(cx, y - bh - gap + 0.05), xytext=(cx, y - bh - 0.02),
                arrowprops=dict(arrowstyle="-|>", color="#546E7A", lw=1.6),
            )
        y -= bh + gap

    save(fig, "fig_metodologia.png")


if __name__ == "__main__":
    fig_arquitectura_mtv()
    fig_flujo_datos()
    fig_taxonomia()
    fig_holdout_validacion()
    fig_modelo_estrella()
    fig_modelo_copo()
    fig_metodologia()

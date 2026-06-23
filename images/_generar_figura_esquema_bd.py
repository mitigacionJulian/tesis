"""Diagrama entidad-relación simplificado — esquema ViaData Medellín."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).parent
DPI = 220
FONT = "DejaVu Sans"

# Colores
C_HECHO = ("#FFE0B2", "#E65100")
C_CAT = ("#E8F5E9", "#2E7D32")
C_TERR = ("#F3E5F5", "#6A1B9A")
C_AUTH = ("#ECEFF1", "#37474F")
C_ARROW = "#607D8B"


def entity(ax, cx, cy, w, h, title, fields, fc, ec, dashed=False, zorder=3):
    """Caja centrada en (cx, cy)."""
    x, y = cx - w / 2, cy - h / 2
    ls = "--" if dashed else "-"
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.04",
        facecolor=fc, edgecolor=ec, linewidth=1.4, linestyle=ls, zorder=zorder,
    ))
    ax.text(cx, cy + h / 2 - 0.18, title, ha="center", va="top",
            fontsize=9.5, fontweight="bold", fontfamily=FONT, zorder=zorder + 1)
    if fields:
        ax.text(cx - w / 2 + 0.12, cy + h / 2 - 0.42, "\n".join(fields),
                ha="left", va="top", fontsize=7, fontfamily=FONT,
                linespacing=1.3, zorder=zorder + 1)


def link(ax, x1, y1, x2, y2, dashed=False, rad=0.0, zorder=1):
    style = f"arc3,rad={rad}" if rad else "arc3"
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=11, linewidth=1.05,
        color=C_ARROW, linestyle="--" if dashed else "-",
        connectionstyle=style, shrinkA=4, shrinkB=4, zorder=zorder,
    ))


def main():
    fig, ax = plt.subplots(figsize=(14, 10.8))
    ax.set_xlim(0, 14)
    ax.set_ylim(-0.75, 10.2)
    ax.axis("off")

    ax.text(7, 9.55, "Modelo relacional — ViaData Medellín (núcleo de dominio)",
            ha="center", fontsize=13, fontweight="bold", fontfamily=FONT)

    # --- Zona central: hechos ---
    entity(ax, 7.0, 6.35, 3.4, 1.45, "incidente", [
        "PK  id  ·  radicado (UK)",
        "fecha_hora_incidente",
        "latitud  ·  longitud",
        "FK  clase_incidente_id",
        "FK  comuna_id  ·  barrio_id",
        "FK  via_id  ·  punto_critico_id (opc.)",
    ], *C_HECHO)

    entity(ax, 7.0, 4.15, 3.0, 1.25, "victima", [
        "PK  id",
        "FK  incidente_id  (ON DELETE CASCADE)",
        "FK  sexo_id  ·  grupo_edad_id",
        "FK  condicion_id  ·  gravedad_victima_id",
    ], *C_HECHO)

    link(ax, 7.0, 5.62, 7.0, 4.78)  # incidente → victima (1:N)

    # --- Catálogo incidente ---
    entity(ax, 7.0, 8.05, 2.6, 0.75, "clase_incidente", [
        "PK  id  ·  codigo/nombre",
    ], *C_CAT)
    link(ax, 7.0, 7.67, 7.0, 7.08)

    # --- Catálogos víctima (columna izquierda) ---
    cats = [
        (2.1, 5.50, "sexo", ["PK  id  ·  codigo"]),
        (2.1, 4.55, "grupo_edad", ["PK  id  ·  rango edad"]),
        (2.1, 3.60, "condicion", ["PK  id  ·  codigo"]),
        (2.1, 2.65, "gravedad_victima", ["PK  id  ·  FATAL / GRAVE…"]),
    ]
    bus_x = 4.45
    victima_left = 5.5
    # Puntos de llegada distribuidos en el borde izquierdo de victima
    victima_targets = [4.62, 4.28, 3.95, 3.62]
    rads = [0.22, 0.10, -0.10, -0.22]

    bus_y_min = min(c[1] for c in cats) - 0.05
    bus_y_max = max(c[1] for c in cats) + 0.05
    ax.plot([bus_x, bus_x], [bus_y_min, bus_y_max], color=C_ARROW,
            linewidth=1.1, zorder=1, solid_capstyle="round")

    for (cx, cy, name, fld), ty, rad in zip(cats, victima_targets, rads):
        entity(ax, cx, cy, 2.35, 0.72, name, fld, *C_CAT)
        # Catálogo → bus (horizontal)
        link(ax, cx + 1.18, cy, bus_x, cy, rad=0.0)
        # Bus → victima (curvas separadas)
        link(ax, bus_x, cy, victima_left, ty, rad=rad)

    ax.text(2.1, 6.18, "Catálogos víctima", ha="center", fontsize=8,
            fontweight="bold", color="#2E7D32", fontfamily=FONT)

    # --- Territorio (columna derecha) ---
    entity(ax, 11.5, 7.55, 2.45, 0.72, "comuna", ["PK  id  ·  nombre"], *C_TERR)
    entity(ax, 11.5, 6.45, 2.45, 0.72, "barrio", ["PK  id  ·  FK comuna_id"], *C_TERR)
    entity(ax, 11.5, 5.15, 2.45, 0.72, "via", ["PK  id  ·  FK comuna_id"], *C_TERR, dashed=True)
    entity(ax, 11.5, 3.75, 2.45, 0.88, "punto_critico", [
        "PK  id  ·  lat/lon",
        "FK  via_id  ·  comuna_id  ·  barrio_id",
    ], *C_TERR, dashed=True)

    # Jerarquía territorial (flechas verticales internas)
    link(ax, 11.5, 6.09, 11.5, 6.91)   # barrio → comuna
    link(ax, 11.5, 5.51, 11.5, 6.09, dashed=True)  # via → comuna
    link(ax, 11.5, 4.19, 11.5, 4.79, dashed=True)  # punto_critico → via

    # Territorio → incidente
    link(ax, 10.28, 7.55, 8.7, 6.55, rad=-0.12)
    link(ax, 10.28, 6.45, 8.7, 6.35, rad=-0.05)
    link(ax, 10.28, 5.15, 8.7, 6.15, dashed=True, rad=0.05)
    link(ax, 10.28, 3.75, 8.7, 6.05, dashed=True, rad=0.12)

    ax.text(11.5, 8.25, "Territorio", ha="center", fontsize=8,
            fontweight="bold", color="#6A1B9A", fontfamily=FONT)
    ax.text(11.5, 2.95, "via y punto_critico:\nvacíos en carga Mede",
            ha="center", fontsize=7, color="#6A1B9A", fontstyle="italic",
            fontfamily=FONT, linespacing=1.2)

    # --- Autenticación (franja inferior, separada) ---
    ax.plot([0.5, 13.5], [1.85, 1.85], color="#CFD8DC", linewidth=0.8, zorder=0)
    ax.text(7, 2.02, "Autenticación Django (app accounts)", ha="center",
            fontsize=8, fontweight="bold", color="#37474F", fontfamily=FONT)

    entity(ax, 4.8, 1.05, 2.2, 0.78, "auth_user", ["PK  id  ·  username"], *C_AUTH)
    entity(ax, 7.5, 1.05, 2.5, 0.78, "perfil_usuario", [
        "PK  id  ·  FK user_id (1:1)",
        "FK  rol_id",
    ], *C_AUTH)
    entity(ax, 10.2, 1.05, 2.1, 0.78, "rol", [
        "ciudadano · analista",
        "administrador · autoridad",
    ], *C_AUTH)

    link(ax, 5.9, 1.05, 6.25, 1.05)
    link(ax, 8.75, 1.05, 9.15, 1.05)

    # --- Leyenda (banda inferior separada) ---
    ax.plot([0.4, 13.6], [-0.18, -0.18], color="#ECEFF1", linewidth=1.0, zorder=0)

    leg_items = [
        (0.55, "Hechos", *C_HECHO, False),
        (2.05, "Catálogos", *C_CAT, False),
        (3.55, "Territorio", *C_TERR, False),
        (5.15, "Opcional / vacío", *C_TERR, True),
        (6.75, "Auth", *C_AUTH, False),
        (7.95, "FK  →  tabla referenciada", None, C_ARROW, False),
    ]
    ly = -0.52
    for item in leg_items:
        if item[1] == "FK  →  tabla referenciada":
            lx, label, _, ec, dash = item
            link(ax, lx + 0.55, ly + 0.1, lx + 1.15, ly + 0.1)
            ax.text(lx + 1.28, ly + 0.1, label, fontsize=7, va="center", fontfamily=FONT)
            continue
        lx, label, fc, ec, dash = item
        ls = "--" if dash else "-"
        ax.add_patch(FancyBboxPatch(
            (lx, ly), 0.38, 0.2, boxstyle="square,pad=0",
            facecolor=fc, edgecolor=ec, linewidth=1.1, linestyle=ls,
        ))
        ax.text(lx + 0.48, ly + 0.1, label, fontsize=7.5, va="center", fontfamily=FONT)

    path = OUT / "fig_esquema_bd.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.5,
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"OK {path.name}")


if __name__ == "__main__":
    main()

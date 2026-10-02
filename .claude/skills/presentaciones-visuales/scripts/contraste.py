"""Calcula el contraste WCAG 2.x entre pares de colores (texto, fondo).

Uso:
    python contraste.py "#texto" "#fondo" ["#texto2" "#fondo2" ...]

Imprime el ratio de cada par y si pasa 4.5:1 (texto normal) y 3:1 (texto
grande: 24px o más, o 18.66px en negrita). Sale con código 1 si algún par
no llega a 4.5:1, para poder usarlo en una verificación automática.
"""
import sys


def luminancia(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"color no válido: {hex_color!r} (se espera #rgb o #rrggbb)")
    canales = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        canales.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = canales
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(texto: str, fondo: str) -> float:
    a, b = sorted((luminancia(texto), luminancia(fondo)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def main(args: list[str]) -> int:
    if not args or len(args) % 2:
        print(__doc__)
        return 2
    falla = False
    for texto, fondo in zip(args[::2], args[1::2]):
        r = ratio(texto, fondo)
        normal = r >= 4.5
        grande = r >= 3
        falla |= not normal
        print(f"{texto} sobre {fondo}: {r:.2f}:1  "
              f"normal {'OK' if normal else 'FALLA'}  grande {'OK' if grande else 'FALLA'}")
    return 1 if falla else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

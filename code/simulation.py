"""Pendule simple non linéaire : intégration par Runge-Kutta d'ordre 4.

Équation sans dimension (tau = omega_0 * t) :  theta'' = -sin(theta).
Le script écrit dans data/ les fichiers CSV lus par le compte rendu LaTeX :
    periode.csv, tableau_periode.csv, convergence.csv, resume.csv

Usage :  python code/simulation.py        (bibliothèque standard uniquement)
"""
import csv
import math
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent.parent / "data"
T0 = 2.0 * math.pi            # période des petites oscillations (omega_0 = 1)


def accel(theta):
    """Accélération angulaire : theta'' = -sin(theta)."""
    return -math.sin(theta)


def rk4(theta, omega, h):
    """Un pas de Runge-Kutta d'ordre 4 pour (theta, omega)."""
    k1t, k1w = omega, accel(theta)
    k2t, k2w = omega + 0.5 * h * k1w, accel(theta + 0.5 * h * k1t)
    k3t, k3w = omega + 0.5 * h * k2w, accel(theta + 0.5 * h * k2t)
    k4t, k4w = omega + h * k3w, accel(theta + h * k3t)
    return (theta + h / 6 * (k1t + 2 * k2t + 2 * k3t + k4t),
            omega + h / 6 * (k1w + 2 * k2w + 2 * k3w + k4w))


def periode(theta0, h):
    """Période = 4 fois la durée du premier passage par theta = 0 (lâché sans vitesse)."""
    t, theta, omega = 0.0, theta0, 0.0
    while True:
        suivant = rk4(theta, omega, h)
        if suivant[0] <= 0.0:                    # zéro dans [t, t + h]
            bas, haut = 0.0, h                   # bissection sur le pas partiel
            for _ in range(60):
                milieu = 0.5 * (bas + haut)
                if rk4(theta, omega, milieu)[0] > 0.0:
                    bas = milieu
                else:
                    haut = milieu
            return 4.0 * (t + 0.5 * (bas + haut))
        t, (theta, omega) = t + h, suivant


def periode_exacte(theta0):
    """T exacte = T0 / AGM(1, cos(theta0 / 2)) (moyenne arithmético-géométrique)."""
    a, b = 1.0, math.cos(theta0 / 2)
    while abs(a - b) > 1e-15:
        a, b = 0.5 * (a + b), math.sqrt(a * b)
    return T0 / a


def periode_serie(theta0):
    """Développement en série : T / T0 = 1 + theta0^2 / 16 + 11 theta0^4 / 3072."""
    return T0 * (1 + theta0**2 / 16 + 11 * theta0**4 / 3072)


def ecrire(nom, entetes, lignes):
    with open(DOSSIER / nom, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(entetes)
        w.writerows(lignes)


def main():
    DOSSIER.mkdir(exist_ok=True)
    h = 0.01

    # 1) Période en fonction de l'amplitude (5° à 170°)
    lignes = []
    for deg in range(5, 175, 5):
        th = math.radians(deg)
        t_num, t_ex, t_se = periode(th, h), periode_exacte(th), periode_serie(th)
        lignes.append([deg, t_num / T0, t_ex / T0, t_se / T0, abs(t_num - t_ex) / t_ex])
    entetes = ["theta0", "T_rk4", "T_exacte", "T_serie", "erreur_rel"]
    ecrire("periode.csv", entetes, lignes)
    ecrire("tableau_periode.csv", entetes, [l for l in lignes if l[0] in (10, 30, 60, 90, 120, 150, 170)])

    # 2) Convergence en h pour theta0 = 60°
    th, hs, erreurs = math.radians(60), [0.4, 0.2, 0.1, 0.05, 0.025, 0.0125], []
    for pas in hs:
        erreurs.append(abs(periode(th, pas) - periode_exacte(th)) / periode_exacte(th))
    ecrire("convergence.csv", ["h", "erreur_rel"], list(zip(hs, erreurs)))

    # 3) Ordre observé : pente de log(erreur) en fonction de log(h) (moindres carrés)
    x = [math.log(v) for v in hs]
    y = [math.log(e) for e in erreurs]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    ordre = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    ecrire("resume.csv", ["ordre_observe", "erreur_min", "erreur_max_pas_001"],
           [[round(ordre, 2), erreurs[-1], max(l[4] for l in lignes)]])
    print(f"Ordre observé de la méthode : {ordre:.2f}")


if __name__ == "__main__":
    main()

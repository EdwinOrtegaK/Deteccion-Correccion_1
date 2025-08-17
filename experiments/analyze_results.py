import pandas as pd
import glob
import matplotlib.pyplot as plt
import os

files = glob.glob("results/*.csv")
if not files:
    print("No se encontraron archivos en results/")
    raise SystemExit(0)

summary = []

for f in files:
    df = pd.read_csv(f)

    total = len(df)
    ok = (df["status"] == "OK").sum()
    corr = (df["status"] == "CORRECTED").sum()
    disc = (df["status"] == "DISCARD").sum()

    # Sacamos parámetros desde el propio CSV
    alg = df["alg"].iloc[0] if "alg" in df.columns else "?"
    p = df["p"].iloc[0] if "p" in df.columns else None
    L = df["msg_bytes"].iloc[0] if "msg_bytes" in df.columns else None

    summary.append({
        "alg": alg,
        "p": p,
        "len": L,
        "N": total,
        "OK": ok,
        "CORR": corr,
        "DISC": disc,
        "EntregaCorrecta(%)": 100*(ok+corr)/total,
        "Descartes(%)": 100*disc/total,
        "archivo": os.path.basename(f)
    })

df_sum = pd.DataFrame(summary)
df_sum.to_csv("results_summary.csv", index=False)
print(df_sum)

# Graficar: EntregaCorrecta vs p para cada algoritmo y longitud
for L in sorted(df_sum["len"].dropna().unique()):
    subset = df_sum[df_sum["len"]==L]
    plt.figure()
    for alg in subset["alg"].unique():
        ss = subset[subset["alg"]==alg]
        plt.plot(ss["p"], ss["EntregaCorrecta(%)"], marker="o", label=alg)
    plt.title(f"Tasa de entrega correcta vs p (len={L} bytes)")
    plt.xlabel("Probabilidad de error p")
    plt.ylabel("Entrega correcta (%)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"results/plot_entrega_len{L}.png", bbox_inches="tight")
    plt.close()

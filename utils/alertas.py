from datetime import datetime

def exibir_alerta(nivel, chuva, risco, probabilidades=None, tendencia=None):
    cores = {
        "baixo": "\033[92m🟩 BAIXO\033[0m",
        "medio": "\033[93m🟨 MÉDIO\033[0m",
        "alto": "\033[91m🟥 ALTO\033[0m"
    }

    # Cabeçalho do alerta
    if risco == "baixo":
        print("\nℹ️ Monitoramento Ativo")
    elif risco == "medio":
        print("\n⚠️ Atenção – Condições Elevadas")
    elif risco == "alto":
        print("\n" + "🚨" * 2 + " ALERTA DE ENCHENTE " + "🚨" * 2)
    else:
        print("\n🔔 Alerta de Monitoramento")

    # Dados atuais
    print(f"🌊 Nível da água: {nivel:.1f} cm")
    print(f"🌧️ Precipitação: {chuva:.1f} mm")
    print(f"⚠️ Nível de Risco: {cores.get(risco, risco.upper())}")

    # Informações preditivas
    if probabilidades:
        print("\n📊 Probabilidades de Risco:")
        print(f"  • Baixo: {probabilidades['baixo']*100:.1f}%")
        print(f"  • Médio: {probabilidades['medio']*100:.1f}%")
        print(f"  • Alto:  {probabilidades['alto']*100:.1f}%")

    if tendencia is not None:
        print("\n📈 Tendência:")
        if tendencia > 0.5:
            print("  ⚠️ Subida rápida do nível da água!")
        elif tendencia > 0:
            print("  ⚠️ Nível da água subindo")
        elif tendencia < -0.5:
            print("  ✅ Nível da água baixando rapidamente")
        elif tendencia < 0:
            print("  ✅ Nível da água baixando")
        else:
            print("  ↔️ Nível da água estável")

    print("-" * 50)

    registrar_log(nivel, chuva, risco, probabilidades, tendencia)

def registrar_log(nivel, chuva, risco, probabilidades=None, tendencia=None):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs.txt", "a") as arquivo:
        log = f"[{agora}] Nível: {nivel} cm | Chuva: {chuva} mm | Risco: {risco}"
        if probabilidades:
            log += f" | Prob: B={probabilidades['baixo']*100:.1f}% M={probabilidades['medio']*100:.1f}% A={probabilidades['alto']*100:.1f}%"
        if tendencia is not None:
            log += f" | Tendência: {tendencia:.2f}"
        arquivo.write(log + "\n")

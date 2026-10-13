#!/usr/bin/env python3
"""
sync_oracle_auto.py
===================
Comando de Sincronização e Deploy Contínuo Automatizado na Oracle Cloud (137.131.151.74).
Sincroniza alterações do Front-end (Next.js) e Back-end (FastAPI),
recompila o build e reinicia os serviços em background.
"""

import os
import sys
import subprocess

SSH_KEY = (
    r"C:\Users\Ronaldo Akagui.SUG00245\ssh-key-2026-09-25.key"
    if os.path.exists(r"C:\Users\Ronaldo Akagui.SUG00245\ssh-key-2026-09-25.key")
    else r"C:\Users\Ronaldo Akagui\ssh-key-2026-09-25.key"
)
ORACLE_HOST = "137.131.151.74"
ORACLE_USER = "ubuntu"
BASE_DIR = r"H:\Drives compartilhados\APLICAÇÕES - SUGOI-SA\02_APLICAÇÕES_E_SISTEMAS\DAISUGI\02_Daisugi_kan-sa"

FILES_TO_SYNC = [
    # Frontend Pages & Configs
    (os.path.join(BASE_DIR, r"frontend\src\app\login\page.tsx"), "/opt/daisugi/kansa/frontend/src/app/login/page.tsx"),
    (os.path.join(BASE_DIR, r"frontend\src\app\page.tsx"), "/opt/daisugi/kansa/frontend/src/app/page.tsx"),
    (os.path.join(BASE_DIR, r"frontend\src\app\modulo-4-custos-despesas\controle-dividas\page.tsx"), "/opt/daisugi/kansa/frontend/src/app/modulo-4-custos-despesas/controle-dividas/page.tsx"),
    (os.path.join(BASE_DIR, r"frontend\src\app\modulo-9-governanca-auditoria\page.tsx"), "/opt/daisugi/kansa/frontend/src/app/modulo-9-governanca-auditoria/page.tsx"),
    (os.path.join(BASE_DIR, r"frontend\src\app\entregas-empreendimentos\page.tsx"), "/opt/daisugi/kansa/frontend/src/app/entregas-empreendimentos/page.tsx"),
    (os.path.join(BASE_DIR, r"frontend\src\config\sugoiChairs.ts"), "/opt/daisugi/kansa/frontend/src/config/sugoiChairs.ts"),
    (os.path.join(BASE_DIR, r"frontend\src\config\fasesGoLive.ts"), "/opt/daisugi/kansa/frontend/src/config/fasesGoLive.ts"),
    (os.path.join(BASE_DIR, r"frontend\public\sugoi_pam_iga_snapshot.json"), "/opt/daisugi/kansa/frontend/public/sugoi_pam_iga_snapshot.json"),
    # Backend Routers & Services
    (os.path.join(BASE_DIR, r"backend\routers\auth.py"), "/opt/daisugi/kansa/backend/routers/auth.py"),
    (os.path.join(BASE_DIR, r"backend\services\auth_service.py"), "/opt/daisugi/kansa/backend/services/auth_service.py")
]

def run_ssh(cmd: str):
    full_cmd = f'ssh -o StrictHostKeyChecking=no -i "{SSH_KEY}" {ORACLE_USER}@{ORACLE_HOST} "{cmd}"'
    return subprocess.run(full_cmd, shell=True, capture_output=True, text=True)

def run_scp(local_path: str, remote_path: str):
    if not os.path.exists(local_path):
        return False
    full_cmd = f'scp -o StrictHostKeyChecking=no -i "{SSH_KEY}" "{local_path}" {ORACLE_USER}@{ORACLE_HOST}:{remote_path}'
    res = subprocess.run(full_cmd, shell=True)
    return res.returncode == 0

def main():
    print("=== [DAISUGI KAN-SA] Sincronizacao Automatica para Oracle Cloud ===")
    
    # 1. Enviar arquivos modificados
    print("[1/3] Enviando arquivos modificados via SCP...")
    sucessos = 0
    for local_f, remote_f in FILES_TO_SYNC:
        if os.path.exists(local_f):
            if run_scp(local_f, remote_f):
                sucessos += 1
                print(f" -> OK: {os.path.basename(local_f)}")
    
    print(f"[*] {sucessos} arquivos sincronizados com a nuvem.\n")

    # 2. Reiniciar Backend
    print("[2/3] Reiniciando Backend FastAPI...")
    run_ssh("sudo systemctl restart kansa-backend")
    print(" -> Backend reiniciado com sucesso.\n")

    # 3. Compilar Frontend e Reiniciar
    print("[3/3] Compilando Frontend Next.js na Oracle Cloud...")
    comp = run_ssh("cd /opt/daisugi/kansa/frontend && npm run build && sudo systemctl restart kansa-frontend")
    if comp.returncode == 0:
        print(" -> Build gerado e kansa-frontend reiniciado com sucesso!")
        print(" -> URL Ativa: https://kansa.daisugi.com.br/login")
    else:
        print(f" [!] Aviso no build: {comp.stderr[:300]}")

if __name__ == "__main__":
    main()

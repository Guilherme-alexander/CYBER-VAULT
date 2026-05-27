<div align="center">

```
####################################################+ #++- -#############################################
##########################################.#### .-. .####++++.  #########################################
########################################   ##..##########++++++- ########################################
#######################################--##-+##+-####   .++++++++  ######################################
#######################################++##### +#+. -+#+  ++++-.++- +####################################
#######################################. ###  ############+-+##+ .++ -###################################
####################################### #. #.+######### -#######  ++   ##################################
#####################################     ##############+.####. ++++. +  .###############################
##################################   +## ###+#################.- .++  ####.  -###########################
###############################-  -####-+##  ####+###.   #####-- - + .#######   #########################
#############--+#############-  +###### ###+###--#######+#####++  .  ##########.  #######################
##########+.###+ ##########+  +#######+ ###### .##############++--  +############.  #####################
##########.####. #########  -#########- ######- ###############+#. -###############  +###################
##########-#### #########  ###########- ##.##########. -##########- +###############. .##################
##########.#### #######+ .############+ +  +-.    .+##. -#########  #################+  #################
##########-####- #####- -##############. #.+  +###-  +#.######.  .+####################  ################
#######      .###- +#- .################  ###################  +########################  ###############
##### ########+ .##    ##################  ################- -##########################+ .##############
#####.########## -##    .+################.  ############.  -##   +######################+ +#############
#####-        ++ ###.  ----.         ..----- . .########## -###- .   .####################  #############
##### #########. ### + --------------------  ##-     ++-  ####+ ......  -#################+ +############
##### +###++####+ #. # .-------------------- #####.   .######.  ........   ################  ############
######-.-###-.   ##-.# ....-----------------. +############   .............  ##############. ############
######.######### +# #. ..........---- ------- +######+.    .................  .############- +###########
#######.        +- #  .............   ------- +###### ........................  -##########+ -###########
#########+-      #  ........    .-### ------. ######- ..........................  #########+ -###########
##################  ################# ------ .######  ...........................  +#######- -###########
##################  ################# ------ #######  .........    ...............  .######. ############
##################. ################# ------ #######  .........         ..........   .#####  ############
################### .################ ------ ######+ .........       ###+  ......    ######  ############
###################  +############### ------ ######+ .........      +### ......     -#####  #############
###################+ .############### .----- ######+ ........       ###  ....      .######  #############
####################. -##############. ----- ######+ ........       #+  ...        ######  ##############
#####################  ##############+  .--- ######+ .......       -# ...         ######. +##############
######################  ############## ##.   ######+ .......       +             ######. +###############
#######################  +############ #############          -++# +            ######. -################
########################  +###########-###########################  +-        .######. +#################
#########################. .##########- ########################## .###+-    +######  ###################
###########################  +########+   #######################. .#####+ #. ####. -####################
############################-  #######+ .---    .++###++-.          ##### -++ -#-  ######################
##############################.  +##### .---...............          #######  .  ########################
```

# CYBER VAULT

**Cofre criptografado local para Windows 10/11**  
Construído com Python + PyQt5 · AES-256-GCM · PBKDF2-HMAC-SHA256

---

![Python](https://img.shields.io/badge/Python-3.10%2B-39ff14?style=flat-square&logo=python&logoColor=39ff14&labelColor=000000)
![PyQt5](https://img.shields.io/badge/PyQt5-UI-39ff14?style=flat-square&logo=qt&logoColor=39ff14&labelColor=000000)
![Crypto](https://img.shields.io/badge/AES--256--GCM-Criptografia-39ff14?style=flat-square&logo=gnuprivacyguard&logoColor=39ff14&labelColor=000000)
![SQLite](https://img.shields.io/badge/SQLite-Armazenamento-39ff14?style=flat-square&logo=sqlite&logoColor=39ff14&labelColor=000000)
![Windows](https://img.shields.io/badge/Windows-10%2F11-39ff14?style=flat-square&logo=windows&logoColor=39ff14&labelColor=000000)
![License](https://img.shields.io/badge/License-MIT-39ff14?style=flat-square&labelColor=000000)

</div>

---

## O que é

Cyber Vault é um cofre de arquivos criptografado que roda localmente no Windows. Nenhum dado sai da sua máquina — sem nuvem, sem servidor, sem telemetria.

Quando **bloqueado**, a pasta protegida não existe em texto plano em lugar nenhum. O conteúdo é comprimido, cifrado com AES-256-GCM e armazenado como blob binário dentro de um banco SQLite. A chave de decriptação deriva da sua senha via PBKDF2 com 300.000 iterações — sem senha, os dados são irrecuperáveis.

Quando **desbloqueado**, a pasta aparece no sistema de arquivos normalmente. Um clique em **LOCK NOW** recomprime, recifra, apaga com wipe seguro e volta ao estado bloqueado.

---

## Tela

<div align="center">

```
┌─────────────────────────────────────────────────────┐
│  ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL        █   │
├─────────────────────────────────────────────────────┤
│                                                     │
│              C Y B E R   V A U L T                  │
│        >> ENCRYPTED SECURE WORKSPACE <<             │
│  ─────────────────────────────────────────────────  │
│  > USERNAME:                                        │
│  ┌─────────────────────────────────────────────┐    │
│  │ ENTER USERNAME_                             │    │
│  └─────────────────────────────────────────────┘    │
│  > PASSWORD:                                        │
│  ┌─────────────────────────────────────────────┐    │
│  │ ••••••••_                                   │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │          > UNLOCK VAULT <                   │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  STATE: LOCKED  │  AES-256-GCM  │  PBKDF2 x300000   │
└─────────────────────────────────────────────────────┘
```

*Tema terminal Fallout — fonte pixelada, fósforo verde, fundo preto*

</div>

---

## Modelo de segurança

### Derivação de chave

```
username
password          PBKDF2-HMAC-SHA256
salt (32 bytes)   300.000 iterações
       │
       ▼
  AES-256 key  ──►  decripta vault
```

Nenhuma chave AES é armazenada. A chave deriva da senha em tempo de execução e existe apenas na RAM enquanto o vault está aberto. Ao bloquear, a chave é descartada.

### Ciclo de lock/unlock

```
UNLOCK                              LOCK
──────                              ────
Lê blob SQLite                      Lê arquivos da pasta
Deriva chave (PBKDF2)               Comprime em ZIP (deflate)
Decripta AES-GCM                    Cifra AES-GCM (nonce aleatório)
Valida tag GCM ──► erro = senha     Salva blob no SQLite
Extrai ZIP na pasta                 Wipe seguro (zeros + fsync)
Abre Windows Explorer               Remove arquivos plaintext
STATE = OPEN                        STATE = CLOSE
```

### O que fica em disco quando bloqueado

```
Vault/
├── vault.exe          ← executável (opcional)
├── vault.lock.db      ← blob criptografado (oculto)
├── .config            ← metadados (oculto)
└── secret/            ← pasta vazia (oculta)
```

Nenhum arquivo plaintext. O blob SQLite contém apenas `nonce (12 bytes) + ciphertext + tag GCM`.

### Proteções implementadas

| Ameaça | Mitigação |
|---|---|
| Acesso físico ao disco | AES-256-GCM — força bruta inviável |
| Senha fraca | PBKDF2 × 300.000 iters — custo alto por tentativa |
| Roubo do banco SQLite | Sem chave embutida — depende inteiramente da senha |
| Crash com vault aberto | Auto-lock no próximo boot (STATE=OPEN detectado) |
| Recuperação de arquivos deletados | Wipe com zeros + fsync antes de unlink |
| Adulteração do executável | Hash SHA-256 verificado no boot (opcional) |

---

## Requisitos

- Windows 10 ou 11
- Python 3.10+
- Dependências:

```bash
pip install pyqt5 cryptography
```

---

## Instalação

```bash
git clone https://github.com/Guilherme-alexander/CYBER-VAULT.git
cd CYBER-VAULT
pip install pyqt5 cryptography
```

### Criar um vault novo

```bash
python build.py
```

O wizard interativo vai pedir localização, nome da pasta, usuário e senha. Ao final, o vault estará criado, criptografado e oculto.

```
=== CYBER VAULT BUILD ===

  PASSO 1 / 4  —  LOCALIZAÇÃO
  ────────────────────────────────────────────────────────
  [1]  C:\Users\...\OneDrive\Área de Trabalho\Vault
  [2]  C:\Users\...\Desktop\Vault
  [3]  Local personalizado
  [4]  Sair

  Escolha > 1
  [OK]   Destino selecionado

  PASSO 2 / 4  —  CONFIGURAÇÃO
  Nome da pasta secreta > arquivos

  PASSO 3 / 4  —  CREDENCIAIS
  Usuário > casap
  Senha   > ••••••••

  PASSO 4 / 4  —  CONSTRUINDO VAULT
  |   Criando estrutura de pastas...
  /   Inicializando banco de dados...
  --  Gerando salt criptográfico...
  \   Registrando usuário  (PBKDF2 x300000)...
  |   Criptografando vault  (AES-256-GCM)...
  [OK]  VAULT CRIADO COM SUCESSO
```

### Abrir o vault

```bash
python main.py
```

Ou execute `vault.exe` se tiver compilado com PyInstaller.

---

## Compilar o executável

Instale o PyInstaller:

```bash
pip install pyinstaller
```

Compile:

```bash
pyinstaller --onefile --windowed main.py -n vault
```

Copie o executável gerado para dentro da pasta `Vault/`:

```
Vault/
└── vault.exe   ← copie aqui
```

Atualize o hash de integridade no `.config` (opcional):

```bash
python -c "from config import file_sha256; print(file_sha256('Vault/vault.exe'))"
```

Cole o resultado em `.config`:

```ini
VAULT_HASH=<hash_aqui>
```

---

## Estrutura do projeto

```
CYBER-VAULT/
│
├── main.py        ← controller principal + lógica de login/lock/unlock
├── window.py      ← UI PyQt5 (tema terminal Fallout)
├── encrypt.py     ← motor criptográfico (PBKDF2, AES-GCM, zip, wipe)
├── config.py      ← leitura/escrita de .config (resolve PermissionError em hidden files)
├── build.py       ← wizard de criação do vault (CLI com animações)
└── README.md
```

### Responsabilidades por arquivo

**`encrypt.py`** — tudo que envolve criptografia:
- `derive_key()` — PBKDF2-HMAC-SHA256, 300.000 iterações
- `encrypt_blob()` / `decrypt_blob()` — AES-256-GCM com nonce aleatório de 12 bytes
- `lock_folder()` / `unlock_folder()` — fluxo completo de lock/unlock
- `wipe_file()` — sobrescreve com zeros + fsync antes de deletar

**`config.py`** — gerencia o arquivo `.config` oculto:
- Resolve automaticamente o `PermissionError` do Windows ao escrever em arquivos com atributo `HIDDEN` (remove o atributo, escreve, re-aplica)
- Armazena estado, hash do usuário, path do vault e versão

**`main.py`** — controller da aplicação:
- Detecta o vault em múltiplos locais (pasta atual, Desktop, OneDrive PT-BR e EN-US)
- Verifica integridade do executável
- Auto-lock no boot se detectar vault aberto (crash recovery)
- Orquestra login → unlock → painel → lock

**`window.py`** — interface gráfica:
- Tema terminal Fallout: fundo preto, verde fósforo `#39ff14`, fonte pixelada
- Cursor `█` piscando via QTimer
- Barra de status com state e algoritmo
- Suporte a `Enter` para submeter login

**`build.py`** — wizard de criação:
- Banner ASCII art com colorização por caractere
- Efeito de digitação caractere a caractere
- Spinner animado `| / -- \` em thread separada
- Cores ANSI completas (funciona em cmd.exe, PowerShell, Windows Terminal)

---

## Banco de dados

O arquivo `vault.lock.db` (SQLite) contém duas tabelas:

```sql
CREATE TABLE users (
    id            INTEGER PRIMARY KEY,
    username_hash TEXT,    -- SHA-256 do username
    salt          BLOB,    -- 32 bytes aleatórios
    password_hash TEXT,    -- SHA-256(PBKDF2(password, salt))
    iterations    INTEGER  -- 300000
);

CREATE TABLE vault (
    id         INTEGER PRIMARY KEY,
    nonce      BLOB,    -- 12 bytes (AES-GCM nonce)
    ciphertext BLOB,    -- ZIP criptografado + tag GCM
    updated_at TEXT     -- datetime('now')
);
```

A senha não é armazenada em nenhuma forma reversível. O `password_hash` serve apenas para validação rápida antes de tentar a decriptação completa.

---

## Detecção automática do vault

O `main.py` procura o vault na seguinte ordem de prioridade:

```
1. Pasta do próprio executável (vault.exe ao lado do .config)
2. Desktop\Vault               (C:\Users\<user>\Desktop\Vault)
3. OneDrive\Área de Trabalho\Vault   (PT-BR)
4. OneDrive\Desktop\Vault           (EN-US)
```

Dentro do `.config`, o campo `ROOT_PATH` armazena o caminho absoluto para garantir que o vault seja encontrado mesmo se movido entre pastas padrão.

---

## Crash recovery

Se o Windows travar com o vault aberto:

```
próximo boot
     │
     ▼
main.py lê .config
     │
     ├── STATE=OPEN ?  ──►  set_close()  ──►  pede login
     │
     └── pasta tem arquivos ?  ──►  set_close()  ──►  pede login
```

O usuário precisa fazer login novamente. Os arquivos plaintext que porventura existam na pasta são ignorados — o vault só é considerado acessível após autenticação bem-sucedida.

---

## Limitações conhecidas

- Wipe seguro depende do filesystem. SSDs com wear leveling e sistemas com journaling podem manter cópias em setores inacessíveis ao SO.
- Blobs grandes (GBs) podem deixar o SQLite pesado. Para arquivos muito grandes considere armazenamento externo cifrado.
- Sem suporte a múltiplos usuários na UI atual (banco suporta, interface não).
- Sem sincronização em nuvem — o `.db` pode ser copiado manualmente, mas não há merge automático.

---

## Roadmap

- [ ] Ícone na bandeja do sistema (tray icon)
- [ ] Auto-lock por timeout de inatividade
- [ ] Drag & drop de arquivos
- [ ] Troca de senha sem recriar o vault
- [ ] Backup exportável do blob criptografado
- [ ] Wipe multi-passagem (DoD 5220.22-M)
- [ ] Log de auditoria (data/hora de unlock/lock)
- [ ] Suporte a múltiplos usuários na UI

---

## Regras para contribuição

Ao modificar o código, **não quebre compatibilidade** com vaults existentes:

- Não altere o tamanho do salt (32 bytes)
- Não altere o tamanho do nonce AES-GCM (12 bytes)
- Não renomeie colunas do banco sem migração
- Não renomeie `vault.lock.db`, `.config` ou a pasta `Vault`
- Mantenha o número de iterações PBKDF2 constante ou adicione campo de migração

---

## Licença

MIT — use, modifique e distribua livremente.  
Sem garantia de qualquer tipo. Use por sua conta e risco.

---

<div align="center">

```
STATE: ACTIVE DEVELOPMENT  │  AES-256-GCM  │  PBKDF2 x300000  │  Python 3
```

*Feito para quem leva privacidade a sério.*

</div>

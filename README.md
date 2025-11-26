# Pose (PoSE-PQC)

Módulo de **Proof of Semantic Existence** pensado para pipelines do
MatVerse com sensibilidade a coerência (Ψ) e integração omega. O foco
é manter o núcleo livre de dependências externas enquanto expõe ganchos
claros para um backend pós-quântico real (ex.: Dilithium) quando
necessário.

## Componentes

- `pose_pqc.PoSEPQC`: gera evidences com HMAC-SHA-512, mantendo API
  compatível com backends PQC futuros.
- `omega_integration.OmegaIntegration`: ponte simples para engines de
  coerência que precisem receber evidences validadas.
- `tests/`: suíte pytest cobrindo geração unitária, lote e integração.

## Uso rápido

```python
from pose.pose_pqc import PoSEPQC

pose = PoSEPQC()
claim = "O MatVerse mantém Ψ >= 0.85 para persistência."  # mensagem a provar
psi = 0.93  # coerência calculada pelo pipeline
iti = "ITI-GENESIS-001"  # identificador imutável do agente

note = pose.generate_evidence(claim, psi, iti)
print(note.to_dict())
```

Para gerar lotes alinhados com requisitos de alto volume:

```python
batch = pose.generate_batch(
    count=1000,
    claim=claim,
    base_psi=0.9,
    iti_seed="MV-epoch-1",
    psi_jitter=0.0005,
)
```

## Requisitos

- Python 3.10+
- Nenhuma dependência obrigatória além da biblioteca padrão.

Pytest está configurado no `pyproject.toml` e pode ser executado com:

```bash
pip install -e .[dev]
pytest
```

## Caminho para um backend PQC

A assinatura padrão usa HMAC-SHA-512 para manter o repositório
executável em ambientes restritos. Quando um backend Dilithium estiver
disponível, basta adicionar o signer desejado nos métodos de assinatura
mantendo a interface estável da classe `PoSEPQC`.

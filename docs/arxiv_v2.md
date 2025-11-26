# PoSE-PQC Paper (arXiv v2) – Release v1.0.0 Hook

Esta atualização vincula o paper ao artefato público gerado pela tag `v1.0.0`.

- **Release alvo:** GitHub release `v1.0.0` (gerado automaticamente ao criar a tag correspondente).
- **Hash imutável do commit:** resolvido em tempo de ação via `git rev-parse HEAD` e exposto nas notas de release.
- **Batch PoSE-PQC 100k:** arquivo `pose_pqc_batch_100k.json` anexado ao release com todas as evidences assinadas.

Quando publicar o preprint no arXiv, inclua no texto:

> "Implementação PoSE-PQC v1.0.0 (hash ${HASH_COMMIT}) disponível em https://github.com/<org>/Pose/releases/tag/v1.0.0 com lote de 100k evidences." 

Substitua `${HASH_COMMIT}` pelo valor exibido nas release notes geradas pela action.

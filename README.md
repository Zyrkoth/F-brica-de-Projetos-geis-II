# F-brica-de-Projetos-geis-II
# Aegis Traffic DSIN — Auditoria Inteligente de Infrações e Prioridade Viária

Sistema de visão computacional desenvolvido no âmbito da **Fábrica de Projetos Ágeis II** em parceria com a **DSIN**, projetado para auditar registos de radares de velocidade e automatizar a triagem de isenções legais para veículos de emergência (Art. 29 do Código de Trânsito Brasileiro).

---

## Objetivo e Funcionamento

O sistema opera como um **árbitro automatizado de exceções** sobre vídeos de infrações pré-capturados por radares (onde o excesso de velocidade já foi constatado pelo equipamento físico):

1. **Deteção de Veículos (YOLOv8):** Identifica e delimita automóveis, motociclos, autocarros e camiões quadro a quadro no fluxo de vídeo.
2. **Análise Espectral de Giroflex (OpenCV / HSV):** Isola o terço superior da caixa delimitadora (*bounding box*) de cada veículo e monitoriza emissões luminosas de alta saturação nas faixas características de sinalizadores de emergência (vermelho e azul).
3. **Consistência Temporal e Veredito:** Calcula a taxa de persistência do sinalizador ao longo do trajeto para evitar falsos positivos (como reflexos de semáforos ou faróis de travagem) e emite o parecer técnico:
   - **Sirene / Giroflex Ativo:** `MULTA ANULADA (Veículo em Emergência — Art. 29 CTB)`
   - **Sem Evidência de Emergência:** `MULTA VALIDADA (Infração Comum)`

---

# 🌱 EcoDetector v2.0 — Classificação Inteligente de Resíduos



![tela inicial](tela_inicial.png)

## 📌 Sobre o Projeto

O **EcoDetector v2.0** é um sistema inteligente desenvolvido com foco em **classificação de resíduos recicláveis** usando **Visão Computacional** e **Inteligência Artificial**. O objetivo é auxiliar no descarte correto de materiais, promovendo a educação ambiental por meio de uma interface gamificada e acessível ao público geral.

---

## 🧰 Tecnologias Utilizadas

| Camada           | Ferramentas & Tecnologias                            |
|------------------|-----------------------------------------------------|
| **IA / Backend** | PyTorch, TorchVision, Scikit-learn, LightGBM        |
| **Frontend**     | Streamlit, Plotly, PyDeck, PIL                      |
| **Estilo Visual**| CSS customizado (glassmorphism, animações)          |
| **Visualização** | Gráficos interativos, mapa com pontos de coleta     |
| **Gamificação**  | Sistema de medalhas, EcoMoedas, níveis, conquistas  |

---

## 🧠 Funcionalidades Principais

- Upload e análise de imagens com IA
- Classificação em 6 categorias: `paper`, `plastic`, `metal`, `glass`, `cardboard`, `trash`
- Sistema de confiança e detecção de outliers
- EcoMoedas como recompensa
- Ranking, medalhas e progresso
- Mapa com pontos reais de coleta (RS)
- Dashboard com impacto ambiental do usuário

---

## 💡 Evolução do Código: De Protótipo a Sistema Modular

### Comparativo Técnico

| Aspecto               | Versão Inicial | Versão Final (v2.0) | Ganho       |
|-----------------------|----------------|---------------------|-------------|
| Linhas de Código      | ~45            | 200+                | +340%       |
| Arquitetura           | Monolítica     | Modular (7 funções) | ✅          |
| Métricas Avaliadas    | Apenas Loss    | Accuracy, F1, por classe | ✅     |
| Visualização          | Nenhuma        | Gráficos, Matriz, Curvas | ✅     |
| Interface             | Inexistente    | Responsiva e interativa  | ✅     |

---
### 📊 Matriz de Confusão

A matriz de confusão abaixo permite visualizar o desempenho do modelo em relação à classificação correta dos resíduos.

- **Linhas** representam as **classes reais**
- **Colunas** representam as **classes preditas pelo modelo**
- A diagonal principal indica as classificações corretas
- Valores fora da diagonal indicam erros de classificação

Isso permite identificar se o modelo está confundindo tipos de resíduos, como plástico com papel, por exemplo.


![Matriz de Confusão](confusion_matrix.png)
## 🔬 Resultados e Análise

### 📈 Desempenho do Modelo

- **Acurácia inicial**: 79.45%
- **F1-Score inicial**: 0.79
- **Acurácia após fine-tuning**: 88.54%
- **F1-Score final**: 0.88

![Curva de Treinamento](training_curve.png)

> Após o fine-tuning, houve um ganho de **+9% em acurácia** e melhora significativa nas classes de `plastic` e `trash`.

---

## 🎨 Interface Gamificada

Embora o foco principal seja IA, a interface recebeu atenção especial:

- Design com CSS moderno e responsivo
- Navegação lateral por páginas (Detector, Dashboard, Mapa, Ranking)
- Feedback visual com emojis, efeitos e animações
- Upload de imagem com drag-and-drop
- Recomendações de descarte + curiosidades por material
- Indicadores de impacto ambiental individual

---

## 📦 Organização do Código

- `completo.py`: Código completo da aplicação Streamlit
- `modelo_oikos.pt`: Arquivo com pesos do modelo treinado
- `assets/`: Imagens e ícones para visualização
- `prompt_inicial.txt`: Log real do processo de treinamento
- `analise_predicoes_final.png`, `feature_importance.png`: Resultados visuais

---

## 🧭 Próximos Passos

- [ ] Inserção de novos materiais (baterias, eletrônicos)
- [ ] Expansão para reconhecimento via vídeo
- [ ] Deploy em nuvem com cache de usuários
- [ ] Coleta de dados anonimizados para pesquisa ambiental

---

## 🏁 Conclusão

O EcoDetector mostra como é possível **aliar IA com impacto social**, promovendo **consciência ecológica** e facilitando decisões sustentáveis. A aplicação combina:

- 🔍 **Classificação automática com IA**
- 🎮 **Gamificação para engajar usuários**
- 🌍 **Visualização do impacto gerado**

---

**🛠️ Desenvolvido em 2025 com foco em tecnologia + meio ambiente.**
tabela_bibliotecas_md = """
### 📚 Bibliotecas Utilizadas

| Biblioteca    | Função Principal |
|---------------|------------------|
| PyTorch       | Criação, treino e ajuste da rede neural (EfficientNetB0) |
| TorchVision   | Pré-processamento de imagens e carregamento de datasets |
| Scikit-learn  | Avaliação do modelo: métricas como accuracy, F1 e matriz de confusão |
| Matplotlib    | Geração de gráficos como curva de treinamento e distribuição |
| Seaborn       | Visualização da matriz de confusão com estilo estatístico |
| Pandas        | Manipulação de dados tabulares durante análises |
| NumPy         | Operações matemáticas com arrays para pós-processamento |
| Streamlit     | Criação da interface web interativa para o usuário final |
"""


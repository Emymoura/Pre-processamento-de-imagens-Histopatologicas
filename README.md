# Pré-processamento de imagens Histopatológicas
Este repositório contém o código utilizado para o pré-processamento de imagens histopatológicas de câncer de mama em formato Whole-Slide Image (WSI/SVS), com foco na preparação dos dados para futuras tarefas de classificação computacional.
## Bibliotecas e Dependecias
O projeto utiliza as seguintes bibliotecas:

```bash
pip install openslide-python
pip install numpy
pip install opencv-python
pip install matplotlib
pip install scikit-image
pip install pillow
```
## Estrutura do Repositório
📦 Pre-processamento-de-imagens-Histopatologicas

  📂 NotebooksCode 
  
  ┗ 📄 Preprocessamento.ipynb
 
  📂 PythonCode
 
  ┗ 📄 PreProcessamento.py
 
  📂 imagens
 
  ┗ 🖼️ Exemplo_segmentacao_extracao.png
 
  ┗ 🖼️ Fluxograma.png
 
  📄 README.md
## Fluxo Metodológico
```bash
TCGA Whole-Slide Images
        ↓
Leitura em baixa resolução
        ↓
Conversão para escala de cinza
        ↓
Segmentação utilizando Otsu
        ↓
Extração de patches representativos (256×256)
        ↓
Filtragem HSV
        ↓
Dataset comprimido em JPG
```
## Resultados
O pipeline reduz a complexidade das imagens histopatológicas por meio da geração de patches representativos de tecido em formato JPG, preservando estruturas morfológicas relevantes e reduzindo redundância e custo computacional.
## Autores
Emily Vitorya de Moura

### Contato
[![Gmail](https://skillicons.dev/icons?i=gmail)](emailto:emilymoura@alunos.utfpr.edu.br;)

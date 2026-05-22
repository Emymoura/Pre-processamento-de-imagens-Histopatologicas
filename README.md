<p align="center">
  <img 
    src="https://capsule-render.vercel.app/api?type=waving&height=150&width=1000&color=4B0082&reversal=false&fontAlignY=20&text=Pré-processamento%20de%20Imagens%20Histopatológicas&fontSize=30&fontColor=F5F5DC&animation=fadeIn"
    width="100%"
  />
</p>

> [!IMPORTANT]
> Este repositório contém o código utilizado para o pré-processamento de imagens histopatológicas de câncer de mama em formato Whole-Slide Image (WSI/SVS), com foco na preparação dos dados para futuras tarefas de classificação computacional.
## Bibliotecas e Dependecias
> [!NOTE]
> O projeto foi desenvolvido utilizando a linguagem Python 3.11 com as seguintes bibliotecas:
```bash
pip install openslide-python
pip install numpy
pip install opencv-python
pip install matplotlib
pip install scikit-image
pip install pillow
```
## Estrutura do Repositório
📦 [Pre-processamento-de-imagens-Histopatologicas](./)

  📂 [NotebooksCode](./NotebooksCode/)
  
  ┗ 📄  [Preprocessamento.ipynb](./NotebooksCode/Preprocessamento.ipynb) 
 
  📂 [PythonCode](./PythonCode/) 
 
  ┗ 📄 [PreProcessamento.py](./PythonCode/PreProcessamento.py)
 
  📂  [imagens](./imagens/)  
 
  ┗  🖼️ [Exemplo_segmentacao_extracao.png](./imagens/Exemplo_segmentacao_extracao.png) 
 
  ┗ 🖼️ [Fluxograma.png](./imagens/Fluxograma.png)  
 
  📄 [README.md](./README.md)

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
[![Gmail](https://skillicons.dev/icons?i=gmail)](mailto:emilymoura@alunos.utfpr.edu.br)
[![GitHub](https://skillicons.dev/icons?i=github)](https://github.com/Emymoura)
[![LinkedIn](https://skillicons.dev/icons?i=linkedin)](https://www.linkedin.com/in/emily-vitorya-de-moura-ab799b273)

<p align="center">
  <img 
    src="https://capsule-render.vercel.app/api?type=waving&height=150&color=4B0082&section=footer"
    width="100%"
  />
</p>

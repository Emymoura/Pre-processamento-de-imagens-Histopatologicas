#Pre-processamento Imagens Histopatologicas
#Codigo em python 

#1- IMPORTAÇÕES:

# Biblioteca usada para abrir imagens histopatológicas no formato SVS
import openslide
# Biblioteca usada para trabalhar com matrizes e arrays numéricos
import numpy as np
# Biblioteca usada para processamento de imagens
import cv2
# Biblioteca usada para exibir imagens e gráficos
import matplotlib.pyplot as plt
# Função que aplica o método de Otsu para encontrar automaticamente um limiar
from skimage.filters import threshold_otsu
# Biblioteca usada para manipular caminhos e criar pastas
import os

#2- CARREGAR IMAGEM SVS

# Caminho da imagem SVS no computador
slide_path = (r"CaminhoImagem.svs")

# Abre a imagem histopatológica usando OpenSlide
slide = openslide.OpenSlide(slide_path)

# Mostra quantos níveis de resolução a imagem possui
print("Quantidade de níveis:", slide.level_count)

# Mostra as dimensões de cada nível da imagem
print("Dimensões dos níveis:", slide.level_dimensions)

# 3. Criar uma thumbnail

# Define o tamanho máximo da thumbnail
thumbnail_size = (1024, 1024)

# Cria uma versão menor da imagem original
thumbnail = slide.get_thumbnail(thumbnail_size)

# Converte a thumbnail para array NumPy
thumbnail = np.array(thumbnail)


# 4- LE IMAGEM EM BAIXA RESOLUÇÃO:

# Seleciona o menor nível de resolução
# Isso reduz o custo computacional
level_mask = slide.level_count - 1

# Lê a imagem inteira nesse nível
img = slide.read_region(
    (0, 0),
    level_mask,
    slide.level_dimensions[level_mask]
).convert("RGB")

# Converte para NumPy
img = np.array(img)


#5- CONVERSÃO PARA GREYSCALE:
# O método de Otsu funciona em escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


#6- APLICAR O MÉTODO OTSU:
# Calcula automaticamente o melhor threshold
thresh = threshold_otsu(gray)

# Cria máscara binária
# Pixels escuros → tecido
# Pixels claros → fundo
tissue_mask = gray < thresh

# Exibe valor do threshold
print("Threshold calculado:", thresh)


#7- CRIAR PASTA:
# Obtém nome do arquivo SVS
slide_name = os.path.splitext(
    os.path.basename(slide_path))[0]

# Nome da pasta
output_dir = f"patches_{slide_name}"

# Cria pasta
os.makedirs(output_dir, exist_ok=True)

print("Pasta criada:", output_dir)

#8- CRIAR PASTA DE SALVAMENTO:
# Pega apenas o nome do arquivo SVS, sem o caminho e sem a extensão
slide_name = os.path.splitext(os.path.basename(slide_path))[0]

# Define o nome da pasta de saída
output_dir = f"patches_{slide_name}"

# Cria a pasta, caso ela ainda não exista
os.makedirs(output_dir, exist_ok=True)

# Mostra onde os patches serão salvos
print("Pasta de saída:", output_dir)

#9- DEFINIR PARÂMETROS:
# Tamanho dos patches
PATCH_SIZE = 256

# Nível de resolução da WSI
LEVEL = 1

# Passo usado na máscara
# Quanto maior:
# - menos patches
# - menos redundância
STEP_MASK = 128

# Quantidade mínima de tecido
MIN_TISSUE_RATIO = 0.85

# Saturação mínima
# Remove patches muito brancos
MIN_SATURATION = 25

# Qualidade melhor que 80, sem pesar tanto
JPEG_QUALITY = 90

#10- CALCULAR ESCALA ENTRA MASCARA E IMG ORIGINAL:
# Dimensões da imagem original
wsi_w, wsi_h = slide.level_dimensions[0]

# Dimensões da máscara
mask_h, mask_w = tissue_mask.shape[:2]

# Conversão máscara → WSI
scale_x = wsi_w / mask_w
scale_y = wsi_h / mask_h

print("Dimensão WSI:", wsi_w, wsi_h)

print("Dimensão máscara:", mask_w, mask_h)

print("Escala X:", scale_x)

print("Escala Y:", scale_y)

#11- EXTRAIR E SALVAR PATCHES:
# Contadores
patch_count = 0
discarded_by_tissue = 0
discarded_by_saturation = 0

# Guarda um patch exemplo
example_patch = None


# Calcula tamanho equivalente do patch na máscara
mask_patch_w = max(1, int(PATCH_SIZE / scale_x))
mask_patch_h = max(1, int(PATCH_SIZE / scale_y))


# Percorre máscara usando STEP_MASK
for y in range(0, mask_h - mask_patch_h, STEP_MASK):

    for x in range(0, mask_w - mask_patch_w, STEP_MASK):

        # ANALISA ÁREA INTEIRA DA MÁSCARA
        # Recorta janela correspondente ao patch
        mask_window = tissue_mask[
            y:y + mask_patch_h,
            x:x + mask_patch_w
        ]


        # Calcula porcentagem de tecido
        tissue_ratio = np.sum(mask_window) / mask_window.size


        # Descarta regiões com pouco tecido
        if tissue_ratio < MIN_TISSUE_RATIO:

            discarded_by_tissue += 1

            continue

        # CONVERTE COORDENADAS PARA WSI

        wsi_x = int(x * scale_x)
        wsi_y = int(y * scale_y)


        # Evita sair da imagem
        if (
            wsi_x + PATCH_SIZE > wsi_w
            or
            wsi_y + PATCH_SIZE > wsi_h
        ):
            
            continue
        # EXTRAI PATCH
        patch = slide.read_region(
        (wsi_x, wsi_y),
        LEVEL,
        (PATCH_SIZE, PATCH_SIZE)
    ).convert("RGB")


        patch = np.array(patch)

        # FILTRO HSV
        hsv = cv2.cvtColor(
            patch,
            cv2.COLOR_RGB2HSV
        )

        mean_saturation = hsv[:, :, 1].mean()


        # Remove patches muito brancos
        if mean_saturation < MIN_SATURATION:

            discarded_by_saturation += 1

            continue


        # Guarda patch exemplo
        if example_patch is None:

            example_patch = patch.copy()

        # SALVA PATCH
        patch_name = f"patch_{patch_count:06d}.jpg"

        patch_path = os.path.join(
            output_dir,
            patch_name
        )

        cv2.imwrite(
            patch_path,
            cv2.cvtColor(
                patch,
                cv2.COLOR_RGB2BGR
            ),
            [cv2.IMWRITE_JPEG_QUALITY, 80]
        )

        patch_count += 1

#12- MOSTRAR ESTATISTICAS:
# Mostra quantos patches foram salvos
print("Total de patches salvos:", patch_count)

# Mostra quantos patches foram descartados por pouca área de tecido
print("Patches descartados por baixa área de tecido:", discarded_by_tissue)

# Mostra quantos patches foram descartados por baixa saturação
print("Patches descartados por baixa saturação:", discarded_by_saturation)

#13- EXEMPLO DE PATCH E FECHAR IMAGEM SVS:
# Se pelo menos um patch foi salvo, mostra um exemplo
if example_patch is not None:
    plt.figure(figsize=(5, 5))
    plt.imshow(example_patch)
    plt.title("Exemplo de patch extraído")
    plt.axis("off")
    plt.show()

# Caso nenhum patch tenha sido salvo, mostra aviso
else:
    print("Nenhum patch foi salvo. Tente reduzir MIN_TISSUE_RATIO ou MIN_SATURATION.")

#Fecha a imagem SVS
slide.close()
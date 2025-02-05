import csv
import os
import comfy.sd
import comfy.utils
from server import PromptServer  # type: ignore
from aiohttp import web

# Caminho para a pasta CSV
csv_path = os.path.abspath(os.path.join(__file__, "../CSV"))


class ReadCSVRowNode:
    @classmethod
    def INPUT_TYPES(cls):
        # Lista todos os arquivos CSV na pasta CSV
        try:
            csv_files = []
            for root, dirs, files in os.walk(csv_path):
                for file in files:
                    if file.endswith(".csv"):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, csv_path)
                        rel_path = rel_path.replace("\\", "⧵")  # Substitui barras invertidas
                        csv_files.append(rel_path)
        except Exception:
            csv_files = []

        return {
            "required": {
                "csv_file": (csv_files,),  # Lista de arquivos CSV
                "row_index": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),  # Índice da linha
            },
        }

    RETURN_TYPES = ("STRING",)  # Retorna apenas o prompt
    RETURN_NAMES = ("prompt",)  # Nome da saída
    FUNCTION = "read_csv"  # Função principal
    CATEGORY = "custom"  # Categoria do nó

    def read_csv(self, csv_file, row_index):
        # Substitui "⧵" por "/" no caminho do arquivo
        csv_file = csv_file.replace("⧵", "/")
        csv_file_path = os.path.join(csv_path, csv_file)

        # Verifica se o arquivo existe
        if not os.path.exists(csv_file_path):
            print(f"Erro: Arquivo CSV não encontrado em {csv_file_path}")
            return ("Erro: Arquivo CSV não encontrado",)

        try:
            # Abre o arquivo CSV e lê todas as linhas
            with open(csv_file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                rows = list(reader)  # Lê todas as linhas

                # Verifica se o índice da linha está dentro do intervalo
                if row_index >= len(rows):
                    print(f"Erro: Índice de linha {row_index} fora do intervalo. O arquivo tem {len(rows)} linhas.")
                    return ("Erro: Índice de linha inválido",)

                # Retorna o prompt da linha selecionada
                prompt = rows[row_index][0].strip()  # Assume que cada linha tem apenas uma coluna (o prompt)
                return (prompt,)
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV: {e}")
            return ("Erro ao ler o CSV",)

# Registrando o nó no ComfyUI
NODE_CLASS_MAPPINGS = {
    "ReadCSVRowNode": ReadCSVRowNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ReadCSVRowNode": "Read CSV Row Node"
}
import os
import sys
from grpc_tools import protoc

# --- НАСТРОЙКИ ---
# Получаем абсолютный путь к папке проекта (где лежит этот скрипт)
project_root = os.path.abspath(os.path.dirname(__file__))

# Папка, где лежат .proto файлы и куда будем класть .py файлы
# Путь: compare_performance/grpc_app/protos
proto_dir = os.path.join(project_root, "grpc_app", "protos")

# Имя файла
proto_file = "dictionary.proto"

def generate():
    print(f"--- Начало генерации gRPC кода ---")
    print(f"Рабочая папка: {proto_dir}")
    
    # Полный путь к proto файлу
    full_proto_path = os.path.join(proto_dir, proto_file)
    
    if not os.path.exists(full_proto_path):
        print(f"ОШИБКА: Файл не найден: {full_proto_path}")
        return

    # 1. Запуск protoc
    # Обратите внимание: мы используем -I=. (текущая директория поиска внутри proto_dir)
    command = [
        "grpc_tools.protoc",
        f"-I{proto_dir}",               # Где искать импорты
        f"--python_out={proto_dir}",    # Куда класть py файлы
        f"--grpc_python_out={proto_dir}",# Куда класть grpc файлы
        f"--pyi_out={proto_dir}",        # Подсказки типов
        full_proto_path,
    ]
    
    print("Запускаем protoc...")
    exit_code = protoc.main(command)
    
    if exit_code != 0:
        print("Ошибка при генерации protobuf файлов. Проверьте синтаксис .proto")
        sys.exit(exit_code)

    # 2. FIX ИМПОРТОВ
    grpc_file_path = os.path.join(proto_dir, "dictionary_pb2_grpc.py")
    print(f"Исправляем импорты в файле: {grpc_file_path}")
    
    if os.path.exists(grpc_file_path):
        with open(grpc_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем абсолютный импорт на относительный
        # Ищем: import dictionary_pb2 as
        # Меняем на: from . import dictionary_pb2 as
        if "from . import dictionary_pb2" not in content:
            new_content = content.replace(
                "import dictionary_pb2 as dictionary__pb2", 
                "from . import dictionary_pb2 as dictionary__pb2"
            )
            
            with open(grpc_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("УСПЕШНО: Импорт исправлен на относительный (from . import).")
        else:
            print("ИНФО: Импорт уже был исправлен ранее.")
    else:
        print("ОШИБКА: Сгенерированный файл не найден!")

if __name__ == "__main__":
    generate()
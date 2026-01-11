import uuid
import sys
from pathlib import Path
import time
import sys
import os
import random
import grpc
from locust import User, HttpUser, task, between, events

# --- НАСТРОЙКА ПУТЕЙ ---
# Добавляем корневую папку в sys.path, чтобы видеть модули grpc_app
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Импорт сгенерированных gRPC файлов (убедись, что пути совпадают)
# ПРАВИЛЬНО (файлы лежат в protos)
from grpc_app.protos import dictionary_pb2
from grpc_app.protos import dictionary_pb2_grpc


# --- 1. КЛАСС ДЛЯ gRPC КЛИЕНТА (ОБЕРТКА) ---
class GrpcClient:
    def __init__(self, host):
        self.channel = grpc.insecure_channel(host)
        self.stub = dictionary_pb2_grpc.DictionaryStub(self.channel)

    def close(self):
        self.channel.close()

    def request(self, name, func, **kwargs):
        """
        Обертка, которая выполняет gRPC запрос, замеряет время
        и отправляет статистику в Locust.
        """
        start_time = time.time()
        result = None
        try:
            result = func(**kwargs)
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=total_time,
                response_length=0, # В gRPC сложно точно измерить байты без перехватчиков
                exception=None,
            )
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=total_time,
                response_length=0,
                exception=e,
            )
        return result

# --- 2. ПОЛЬЗОВАТЕЛЬ REST (FASTAPI) ---
class RestUser(HttpUser):
    wait_time = between(1, 3) # Пауза между действиями 1-3 сек
    host = "http://127.0.0.1:8000" # Адрес REST сервиса

    @task(3) # Вес 3: выполняется чаще
    def get_terms(self):
        self.client.get("/terms", name="/terms (ALL)")

    @task(1) # Вес 1: создание термина
    def create_term(self):
        # term_id = f"Term_{random.randint(1, 100000)}"
        # self.client.post(
        #     "/terms", 
        #     json={"term": term_id, "definition": "Test definition"},
        #     name="/terms (POST)"
        # )

        term_id = f"Term_{uuid.uuid4()}" 
        
        self.client.post(
            "/terms", 
            json={"term": term_id, "definition": "Test definition"},
            name="/terms (POST)"
        )

# --- 3. ПОЛЬЗОВАТЕЛЬ gRPC ---
class GrpcUser(User):
    wait_time = between(1, 3)
    # Адрес gRPC сервиса (без http://)
    host = "localhost:50051" 
    
    def on_start(self):
        """Инициализация клиента при запуске виртуального пользователя"""
        self.grpc_client = GrpcClient(self.host)

    def on_stop(self):
        """Закрытие соединения при остановке"""
        self.grpc_client.close()

    @task(3)
    def get_all_terms(self):
        self.grpc_client.request(
            "GetAllTerms",
            self.grpc_client.stub.GetAllTerms,
            request=dictionary_pb2.GetAllTermsRequest()
        )

    @task(1)
    def add_term(self):
        # term_id = f"Term_{random.randint(1, 100000)}"
        term_id = f"Term_{uuid.uuid4()}"
        term_obj = dictionary_pb2.Term(term=term_id, definition="Test definition")
        req = dictionary_pb2.AddTermRequest(term_to_add=term_obj)
        
        self.grpc_client.request(
            "AddTerm",
            self.grpc_client.stub.AddTerm,
            request=req
        )
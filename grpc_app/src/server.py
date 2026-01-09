import grpc
from concurrent import futures
import time
import os

# Импортируем сгенерированные классы
from grpc_app.protos import dictionary_pb2
from grpc_app.protos import dictionary_pb2_grpc


# Словарь для хранения терминов в памяти
in_memory_dictionary = {}

# Класс-сервисер, реализующий логику API
class DictionaryServicer(dictionary_pb2_grpc.DictionaryServicer):
    """
    Реализация сервиса Dictionary с полным набором CRUD-операций.
    """
    def AddTerm(self, request, context):
        term_to_add = request.term_to_add
        term = term_to_add.term
        definition = term_to_add.definition
        print(f"Получен запрос AddTerm: '{term}'")
        if term in in_memory_dictionary:
            msg = f"Термин '{term}' уже существует."
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(msg)
            return dictionary_pb2.AddTermResponse(success=False, message=msg)
        
        in_memory_dictionary[term] = definition
        print(f"Термин '{term}' успешно добавлен.")
        return dictionary_pb2.AddTermResponse(
            success=True, message=f"Термин '{term}' успешно добавлен."
        )

    def GetTerm(self, request, context):
        term = request.term
        print(f"Получен запрос GetTerm: '{term}'")
        if term in in_memory_dictionary:
            return dictionary_pb2.Term(
                term=term, definition=in_memory_dictionary[term]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Термин '{term}' не найден.")
            return dictionary_pb2.Term()

    def GetAllTerms(self, request, context):
        print("Получен запрос GetAllTerms")
        # ИСПРАВЛЕНИЕ: завершаем создание списка терминов
        term_list = [
            dictionary_pb2.Term(term=term, definition=definition)
            for term, definition in in_memory_dictionary.items()
        ]
        return dictionary_pb2.GetAllTermsResponse(terms=term_list)

    def UpdateTerm(self, request, context):
        original_term = request.original_term
        new_data = request.new_term_data
        print(f"Получен запрос UpdateTerm для '{original_term}'")
        if original_term not in in_memory_dictionary:
            msg = f"Термин '{original_term}' для обновления не найден."
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(msg)
            return dictionary_pb2.UpdateTermResponse(success=False, message=msg)

        # Удаляем старый термин и добавляем новый (позволяет менять ключ)
        del in_memory_dictionary[original_term]
        in_memory_dictionary[new_data.term] = new_data.definition
        print(f"Термин '{original_term}' успешно обновлен на '{new_data.term}'.")
        return dictionary_pb2.UpdateTermResponse(
            success=True, message=f"Термин '{original_term}' успешно обновлен."
        )

    def DeleteTerm(self, request, context):
        term = request.term
        print(f"Получен запрос DeleteTerm: '{term}'")
        if term in in_memory_dictionary:
            del in_memory_dictionary[term]
            print(f"Термин '{term}' успешно удален.")
            return dictionary_pb2.DeleteTermResponse(
                success=True, message=f"Термин '{term}' успешно удален."
            )
        else:
            msg = f"Термин '{term}' для удаления не найден."
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(msg)
            return dictionary_pb2.DeleteTermResponse(success=False, message=msg)

def serve():
    """
    Функция для запуска gRPC сервера.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dictionary_pb2_grpc.add_DictionaryServicer_to_server(
        DictionaryServicer(), server
    )
    port = os.environ.get('PORT', '50051')
    server.add_insecure_port(f'[::]:{port}')
    print(f"Сервер запущен и слушает порт {port}...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        print("Сервер остановлен.")

if __name__ == '__main__':
    serve()
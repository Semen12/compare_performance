from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Term(_message.Message):
    __slots__ = ("term", "definition")
    TERM_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    term: str
    definition: str
    def __init__(self, term: _Optional[str] = ..., definition: _Optional[str] = ...) -> None: ...

class AddTermRequest(_message.Message):
    __slots__ = ("term_to_add",)
    TERM_TO_ADD_FIELD_NUMBER: _ClassVar[int]
    term_to_add: Term
    def __init__(self, term_to_add: _Optional[_Union[Term, _Mapping]] = ...) -> None: ...

class AddTermResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class GetTermRequest(_message.Message):
    __slots__ = ("term",)
    TERM_FIELD_NUMBER: _ClassVar[int]
    term: str
    def __init__(self, term: _Optional[str] = ...) -> None: ...

class GetAllTermsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllTermsResponse(_message.Message):
    __slots__ = ("terms",)
    TERMS_FIELD_NUMBER: _ClassVar[int]
    terms: _containers.RepeatedCompositeFieldContainer[Term]
    def __init__(self, terms: _Optional[_Iterable[_Union[Term, _Mapping]]] = ...) -> None: ...

class UpdateTermRequest(_message.Message):
    __slots__ = ("original_term", "new_term_data")
    ORIGINAL_TERM_FIELD_NUMBER: _ClassVar[int]
    NEW_TERM_DATA_FIELD_NUMBER: _ClassVar[int]
    original_term: str
    new_term_data: Term
    def __init__(self, original_term: _Optional[str] = ..., new_term_data: _Optional[_Union[Term, _Mapping]] = ...) -> None: ...

class UpdateTermResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class DeleteTermRequest(_message.Message):
    __slots__ = ("term",)
    TERM_FIELD_NUMBER: _ClassVar[int]
    term: str
    def __init__(self, term: _Optional[str] = ...) -> None: ...

class DeleteTermResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

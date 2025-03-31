from fastapi.middleware.cors import CORSMiddleware

def add_cors(app):
    origins = [
        "http://localhost:5173",  # адрес твоего фронтенда на Vite
        "http://127.0.0.1:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # разрешенные источники
        allow_credentials=True,
        allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
        allow_headers=["*"],  # Разрешаем все заголовки
    )
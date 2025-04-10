from fastapi.middleware.cors import CORSMiddleware


def add_cors(app):
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

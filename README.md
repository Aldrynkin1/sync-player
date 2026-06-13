# Sync Player

Sync Player — веб-приложение для синхронного просмотра видео в комнатах.  
Проект состоит из backend на FastAPI и frontend на React. Основная идея — позволить нескольким пользователям находиться в одной комнате и синхронно управлять воспроизведением видео.

## Статус проекта

Проект заброшен и больше не развивается.  
Репозиторий сохранён как пример реализации и для демонстрации основной логики приложения.

## Возможности

- Создание и удаление пользователей.
- Создание и удаление комнат.
- Добавление участников в комнату.
- Получение списка пользователей и комнат.
- Получение комнаты по id или названию.
- Синхронизация состояния видео через WebSocket.
- Поддержка действий `PLAY`, `PAUSE`, `SEEK`, `CHANGE_VIDEO`.
- Проверка прав доступа: управлять комнатой может только владелец.

## Стек технологий

### Backend
- Python
- FastAPI
- SQLAlchemy
- WebSocket
- CORS middleware

### Frontend
- React
- JavaScript
- CSS Modules

## Структура проекта

```text
backend/
  app/
    core/
    models/
    repositories/
    routes/
    schemas/
    services/
  main.py

frontend/
  src/
    api/
    components/
    pages/
    styles/
```

## Архитектура

Backend построен по слоистой архитектуре:

- `routes` — обработка HTTP и WebSocket-запросов.
- `services` — бизнес-логика.
- `repositories` — работа с базой данных.
- `models` — ORM-модели.
- `schemas` — Pydantic-схемы.

## Основные роуты

### Пользователи

- `GET /users/` — получить всех пользователей.
- `GET /users/{user_id}` — получить пользователя по id.
- `POST /users/create` — создать пользователя.
- `POST /users/join/{user_id}` — присоединить пользователя к комнате.
- `DELETE /users/delete/{user_id}` — удалить пользователя.

### Комнаты

- `GET /room/` — получить все комнаты.
- `GET /room/{room_name}` — получить комнату по названию.
- `POST /room/create` — создать комнату.
- `GET /room/{room_id}` — получить комнату по id.
- `POST /room/members/add/{user_id}/to/{room_id}` — добавить пользователя в комнату.
- `DELETE /room/delete/{room_id}` — удалить комнату.

### WebSocket

- `WS /room/ws/message/{room_id}` — канал синхронизации состояния комнаты.

## WebSocket-логика

При подключении клиент получает начальное состояние комнаты:

```json
{
  "type": "INITIAL_STATE",
  "video_url": "...",
  "current_time": 0.0,
  "is_playing": false,
  "owner_id": 1
}
```

Доступные действия:

### PLAY / PAUSE
```json
{
  "type": "PLAY",
  "time": 10.5,
  "user_id": 1
}
```

### SEEK
```json
{
  "type": "SEEK",
  "time": 42.0,
  "user_id": 1
}
```

### CHANGE_VIDEO
```json
{
  "type": "CHANGE_VIDEO",
  "video_url": "https://example.com/video.mp4",
  "user_id": 1
}
```

Только владелец комнаты может управлять воспроизведением и изменять видео.

## Запуск backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Запуск frontend

```bash
cd frontend
npm install
npm run dev
```

## Пример сценария

1. Пользователь создаёт комнату.
2. Владелец подключает видео.
3. Участники присоединяются к комнате.
4. Владелец нажимает play, pause или перематывает видео.
5. У всех подключённых пользователей состояние обновляется одновременно.

## Примечание

Frontend проекта не был доведён до финальной рабочей версии из-за проблем с запуском React-плеера на используемом ноутбуке.  
Backend-часть и основная серверная логика сохранены в репозитории.

## Лицензия

Проект размещён в репозитории в учебных и демонстрационных целях.

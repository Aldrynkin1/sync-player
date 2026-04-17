from fastapi import APIRouter, status, Depends, WebSocket, WebSocketDisconnect  
from app.models.room import Room
from app.schemas.room import RoomResponse, RoomCreate
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.room_service import RoomService
from fastapi import HTTPException
from app.models.video_manager import manager
from fastapi.concurrency import run_in_threadpool
from app.core.auth import get_current_user


rout = APIRouter(
    prefix='/room',
    tags=['rooms']
)

@rout.get('/',  status_code=status.HTTP_200_OK)
def get_all_rooms(db: Session = Depends(get_db)):
    
    serv = RoomService(db)
    rooms = serv.get_all_rooms()    
    return rooms

@rout.get('/{room_name}', status_code=status.HTTP_200_OK)
def get_room_by_name(room_name: str,db: Session = Depends(get_db)) -> Room:
    serv = RoomService(db)
    room = serv.get_room_by_name(room_name)
    return room
    

@rout.post('/create', status_code=status.HTTP_200_OK)
def create_room(
    room_data: RoomCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    serv = RoomService(db)
    return serv.create_room(room_data, current_user.id)

@rout.get('/{room_id}')
def get_room_by_id(room_id: int, db: Session = Depends(get_db)):
    serv = RoomService(db)

    return serv.get_room_by_id(room_id)

@rout.post('/members/add/{user_id}/to/{room_id}', response_model=RoomResponse)
def add_user_to_room(user_id: int, room_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    serv = RoomService(db)
    room = serv.repo.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Room not found')
    
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail='Only owner can add members')

    return serv.add_user_to_room(room_id, user_id)

@rout.delete('/delete/{room_id}')
def delete_room(room_id: int, user_id: int, db: Session = Depends(get_db)):
    serv = RoomService(db)
    
    if not serv.delete_room(room_id, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Room not found')
    
    

    return {'status': 'success', 'message': 'Room deleted'}

@rout.websocket("/ws/message/{room_id}")
async def websocket_message(websocket: WebSocket, room_id: int, user_id: int):
    await manager.connect(room_id, websocket)

    db = next(get_db())
    serv = RoomService(db)

    try:
        room = await run_in_threadpool(serv.repo.get_room_by_id, room_id)

        if not room:
            await websocket.send_json({"type": "ERROR", "detail": "Room not found"})
            await websocket.close(code=1008)
            return

        #состояние при подключении
        await websocket.send_json({
            "type": "INITIAL_STATE",
            "video_url": room.video_url,
            "current_time": room.current_time,
            "is_playing": room.is_playing,
            "owner_id": room.owner_id
        })

        while True:
            data = await websocket.receive_json()

            action_type = data.get("type")
            current_time = data.get("time", 0.0)
            sender_id = data.get("user_id")

            if sender_id is None:
                await websocket.send_json({"type": "ERROR", "detail": "user_id required"})
                continue

            if sender_id != room.owner_id:
                await websocket.send_json({"type": "ERROR", "detail": "Only owner can control room"})
                await websocket.close(code=1008)
                return

            if action_type in ["PLAY", "PAUSE"]:
                is_playing = (action_type == "PLAY")

                await run_in_threadpool(serv.update_room_state, room_id, current_time, is_playing)

                await manager.broadcast(room_id, {
                    "type": action_type,
                    "time": current_time
                })

            elif action_type == "SEEK":
                await run_in_threadpool(serv.update_room_state, room_id, current_time, True)

                await manager.broadcast(room_id, {
                    "type": "SEEK",
                    "time": current_time
                })

            elif action_type == "CHANGE_VIDEO":
                new_video_url = data.get("video_url")

                if not new_video_url:
                    await websocket.send_json({"type": "ERROR", "detail": "video_url required"})
                    continue

                await run_in_threadpool(serv.new_video, room_id, new_video_url, sender_id)

                await manager.broadcast(room_id, {
                    "type": "CHANGE_VIDEO",
                    "video_url": new_video_url
                })

            else:
                await websocket.send_json({"type": "ERROR", "detail": "Unknown action type"})

    except WebSocketDisconnect:
        await manager.disconnect(room_id, websocket)

    except Exception as e:
        await manager.disconnect(room_id, websocket)
        print("WebSocket error:", e)

    finally:
        db.close()
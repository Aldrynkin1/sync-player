import { useState } from "react";
import { CreateRoom } from "../api/room_api";
import { useNavigate } from "react-router-dom";

export default function CreateRoomPage() {
  const [roomName, setRoomName] = useState("");
  const [createdRoom, setCreatedRoom] = useState(null);
  const navigate = useNavigate();

  const handleCreate = async () => {
    try {
      const data = await CreateRoom({ name: roomName });
      setCreatedRoom(data);
      navigate('/create')
    } catch (err) {
      console.error("Ошибка создания комнаты", err);
    }
  };
  return (
    <div>
      <h1>Создать новую комнату</h1>
      <input
        type="text"
        value={roomName}
        onChange={(e) => setRoomName(e.target.value)}
        placeholder="Название комнаты"
      />
      <button onClick={handleCreate}>Создать</button>

      {createdRoom && (
        <div>
          <p>Комната {createdRoom.name} успешно создана</p>
          <small>Room ID: {createdRoom.name}</small>
        </div>
      )}
    </div>
  );
}

import { useState, useEffect } from "react";
import { GetRooms } from "../api/room_api";
import { useNavigate } from "react-router-dom";

import cl from "../styles/for_app.module.css";

export default function GetAllRooms() {
  const [rooms, setRooms] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    GetRooms()
      .then(setRooms)
      .catch((err) => console.error(err));
  }, []);
  navigate('/')

  return (
    <div className={cl.all_rooms_cont}>
      <h1>Rooms</h1>
      {rooms.map((room) => (
        <div key={room.id} className={cl.room_cont}>
          {room.name} | {room.video_url}
        </div>
      ))}
    </div>
  );
}

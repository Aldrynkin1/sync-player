const API_URL = "http://127.0.0.1:8000";

export async function GetRooms() {
  const res = await fetch(`${API_URL}/room/`);
  if (!res.ok) throw new Error("Ошибка загрузки комнат");
  return res.json();
}

export async function CreateRoom(roomData) {
  const res = await fetch(
    `${API_URL}/room/create?owner_id=${roomData.owner_id}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(roomData),
    },
  );

  if (!res.ok) throw new Error("Ошибка создания комнаты");
  return res.json();
}

export async function GetRoomById(id) {
  const res = await fetch(`${API_URL}/room/${id}`);
  if (!res.ok) throw new Error("Ошибка нахождения комнаты по id");
  return res.json();
}

export async function DeleteRoom(roomId) {
  const res = await fetch(`${API_URL}/room/delete/${roomId}`);
  if (!res.ok) throw new Error("Ошибка удаления комнаты");
  return res.json();
}

export async function AddUserToRoom(id, userId) {
  const res = await fetch(`${API_URL}/room/members/add/${userId}/to/${id}`)
  if (!res.ok) throw new Error('Ошибка добавления пользователя в комнату')
  return res.json()
}
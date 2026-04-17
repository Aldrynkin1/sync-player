const API_URL = "http://127.0.0.1:8000";

export async function getUsers() {
  const res = await fetch(`${API_URL}/users/`);
  if (!res.ok) throw new Error("Ошибка загрузки пользователей");
  return res.json();
}

export async function createUser(userData) {
  const res = await fetch(`${API_URL}/users/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  });
  if (!res.ok) throw new Error("Не удалось создать пользователя");
  return res.json;
}
export async function getUserById(id) {
  const res = await fetch(`${API_URL}/users/${id}`);
  if (!res.ok) throw new Error("Не удалось найти пользователя");
  return res.json();
}

export async function deleteUser(id) {
  const res = await fetch(`${API_URL}/users/delete/${id}`);
  if (!res.ok) throw new Error("Ошибка удаления юзера");
  return res.json();
}

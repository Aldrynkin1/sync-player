import GetAllRooms from "./components/RoomsList";
import CreateRoomPage from "./pages/CreateRoomPage";
import VideoRoom from "./pages/RoomPage";
import cl from "./styles/app.module.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

function App() {
  const roomId = 1;
  const userId = 1;
  return (
    <div>
      <BrowserRouter>
      <nav>
        <Link to={"/"}>Список комнат</Link>
        <Link to={'create'}>Создать комнату</Link>
        <Link to={'/video/room/:roomId/:userId'}>Просмотр видео</Link>
      </nav>

      <Routes>
        <Route path="/" element={<GetAllRooms/>}/>
        <Route path="/create" element={<CreateRoomPage/>}/>
        <Route path="/video/room/:roomId/:userId" element={<VideoRoom roomId={roomId} userId={userId} />} />
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

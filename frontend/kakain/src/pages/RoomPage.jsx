import { useState, useEffect, useRef } from "react";
import ReactPlayer from "react-player";
import cl from "../styles/VideoRoom.module.css";

export default function VideoRoom({ roomId, userId }) {
  const playerRef = useRef(null);
  const [isReady, setIsReady] = useState(false);
  const socket = useRef(null);
  const [videoUrl, setVideoUrl] = useState(
    "https://www.youtube.com/watch?v=uZOxM7YB3AU",
  );
  const [state, setState] = useState({
    url: "",
    playing: false,
    isReady: false,
  });

  // отправка сообщений заблокирована, чтобы не было беск цикла
  const isInternalUpdate = useRef(false);

  useEffect(() => {
    socket.current = new WebSocket(
      `ws://127.0.0.1:8000/room/ws/message/${roomId}?user_id=${userId}`,
    );

    socket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case "INITIAL_STATE":
          setState((s) => ({
            ...s,
            url: data.video_url,
            playing: data.is_playing,
          }));
          setTimeout(() => {
            if (isReady) {
              playerRef.current?.seekTo(data.current_time, "seconds");
            }
          }, 1000);
          break;

        case "PLAY":
          setState((s) => ({ ...s, playing: true }));
          break;

        case "PAUSE":
          setState((s) => ({ ...s, playing: false }));
          break;

        case "SEEK":
          isInternalUpdate.current = true; // паеремотка сокетом
          playerRef.current?.seekTo(data.time, "seconds");
          break;

        case "CHANGE_VIDEO":
          setState((s) => ({ ...s, url: data.video_url }));
          break;
      }
    };

    return () => socket.current.close();
  }, [roomId, userId, isReady]);

  // функции овнера
  const handlePlay = () => {
    if (!isInternalUpdate.current) {
      socket.current.send(
        JSON.stringify({
          type: "PLAY",
          time: playerRef.current.getCurrentTime(),
          user_id: userId,
        }),
      );
    }
    isInternalUpdate.current = false;
  };

  const handlerSubmit = (e) => {
    e.preventDefault();
    if (videoUrl.trim()) {
      socket.current.send(
        JSON.stringify({
          type: "CHANGE_VIDEO",
          videoUrl: videoUrl,
          user_id: userId,
        }),
      );
      setVideoUrl("");
    }
  };

  const handlePause = () => {
    if (!isInternalUpdate.current) {
      socket.current.send(
        JSON.stringify({
          type: "PAUSE",
          time: playerRef.current.getCurrentTime(),
          user_id: userId,
        }),
      );
    }
    isInternalUpdate.current = false;
  };

  const handleSeek = (seconds) => {
    if (!isInternalUpdate.current) {
      socket.current.send(
        JSON.stringify({
          type: "SEEK",
          time: seconds,
          user_id: userId,
        }),
      );
    }
    isInternalUpdate.current = false;
  };

  return (
    <div>
      <ReactPlayer
        style={{
          marginTop: 30,
          display: "flex",
          justifyContent: "center",
          marginLeft: 350,
        }}
        ref={playerRef}
        url={state.url}
        playing={state.playing}
        onReady={() => setIsReady(true)}
        onPlay={handlePlay}
        onPause={handlePause}
        onSeek={handleSeek}
        controls={true}
        width="700px"
        height="400px"
      />
      <form onSubmit={handlerSubmit}>
        <input
          type="text"
          placeholder="Ссылка на youtube"
          value={videoUrl}
          onChange={(e) => setVideoUrl(e.target.value)}
        />
        <button type="submit">Сменить видео</button>
      </form>
    </div>
  );
}

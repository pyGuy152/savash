
import { useEffect } from "react";
import "./App.css";
import HomeNav from "./components/HomeNav";
import { apiUrl, getToken, LOGOUT } from "./types";
import { useNavigate } from "react-router-dom";


function App() {

  const navigate = useNavigate();

  useEffect(() => {
          
          if (getToken(document.cookie)) {
            fetch(apiUrl + "/users/", {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + getToken(document.cookie),
              },
            })
              .then((res) => res.json())
              .then((user) => {
                localStorage.setItem("role", user.role);
                localStorage.setItem("username", user.username);
                if (user.role === "teacher") {
                  navigate("/classes");
                } else {
                  navigate("/dashboard");
                }
              })
              .catch(() => {
                LOGOUT();
              });
          }
      }, []);

  return (
    <>
      <HomeNav />
      <h1 className="welcome">Welcome to Savash</h1>
      <h2 className="welcome">The note taking and assignment submission app</h2>
      {Array.from({ length: 200 }).map((_, i) => (<br key={i} />))}
      <button>Secret</button>
    </>
  );
}

export default App;

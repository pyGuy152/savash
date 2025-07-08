
import { useEffect } from "react";
import "./App.css";
import HomeNav from "./components/HomeNav";
import { apiUrl, getToken } from "./types";
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
              .catch(() => {})}});
  return (
    <>
      <HomeNav />

      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-start",
          background:
            "linear-gradient(135deg, var(--backgroundColor) 20%, var(--tint) 100%)",
          padding: "0",
          width: "100%",
        }}
      >
        <h1 className="welcome">
          Welcome to{" "}
          <span
            style={{
              textDecoration: "underline overline",
              textShadow: "5px 5px 10px #3333",
              color: "var(--warningColor)",
            }}
          >
            Savash
          </span>
        </h1>
        <h2 className="welcome subtitle">
          Your all-in-one classroom management and learning platform
        </h2>
        <div className="cta-btns">
          <button className="cta-btn" onClick={() => navigate("/login")}>
            Login
          </button>
          <button
            className="cta-btn register"
            onClick={() => navigate("/register")}
          >
            Register
          </button>
        </div>
        <br />
        <br />
        <br />
        <div className="desc-section">
          <p>
            <b>Savash</b> is a modern classroom management tool designed to
            simplify teaching and learning. Organize assignments, manage
            classes, and foster collaboration—all in one place.
          </p>
        </div>
        <div className="desc-section">
          <ul className="features-list">
            <li>
              <b>Secure:</b> Your data is safe (we hash your
              passwords)
            </li>
            <li>
              <b>Resources:</b> Access class materials anytime.
            </li>
            <li>
              <b>Personalized:</b> See your assignments,
              class posts and classmates in your dashboard.
            </li>
            <li>
              <b>Fun:</b> Have fun participating in the Savash
              game!
            </li>
            <li>
              <b>Easy:</b> Create, submit, and track
              assignments with just a few clicks.
            </li>
          </ul>
        </div>
      </div>
    </>
  );
}

export default App;

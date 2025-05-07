
import { useEffect } from "react";
import HomeNav from "./components/HomeNav";
import "./Register.css";
import { useNavigate } from "react-router-dom";

const apiUrl = "https://api.codewasabi.xyz";

import { LOGOUT, getToken } from "./types.ts";

function Login() {
    const navigate = useNavigate();

    useEffect(() => {
        
        if (getToken(document.cookie)) {
          fetch(apiUrl + "/users", {
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

    function fetchUserData(token: string) {
        console.log(token);
        fetch(apiUrl + "/users", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "bearer " + token,
          },
        })
          .then((res) => res.json())
          .then((user) => {
            localStorage.setItem("role", user.role);
            localStorage.setItem("username", user.username);
            localStorage.setItem("email", user.email);
            if (user.role === "teacher") {
              navigate("/classes");
            } else {
              navigate("/dashboard");
            }
          })
          .catch((err) => {
            console.log(err);
            alert("Invalid email or password.");
          });
    };

    function submitForm(event: React.FormEvent<HTMLFormElement>) {
      event.preventDefault();
      const emailElem = document.getElementById("email") as HTMLInputElement;
      const passwordElem = document.getElementById(
        "password"
      ) as HTMLInputElement;
      let email = emailElem.value;
      let password = passwordElem.value;
      if (email === "" || password === "") {
        alert("Please fill in all fields.");
        return;
      }
      if (password.length < 8) {
        alert("Password must be at least 8 characters long.");
        return;
      }
      if (emailElem.checkValidity() === false) {
        alert("Please enter a valid email address.");
        return;
      }
      const data = { email, password };
      console.log(apiUrl);
      fetch(apiUrl + "/login", {
        body: JSON.stringify(data),
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      }).then((res) => res.json()).then((token) => {
        token = token.access_token;
        let today = new Date();
        let expire = new Date(today.getTime() + 60 * 60 * 1000); // 1 hour
        document.cookie = `token=${token}; expires=${expire.toUTCString()}; path=/`;
        fetchUserData(token);
    })
    
    }

    return (
      <>
        <HomeNav />
        <div>
          <form className="Register" onSubmit={submitForm}>
            <h2>Login</h2>
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              pattern="[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
              required
            />
            <label htmlFor="password">Password:</label>
            <input type="password" id="password" name="password" required />
            <button type="submit" className="submit">
              Login
            </button>
          </form>
        </div>
      </>
    );
}

export default Login;
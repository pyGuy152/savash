import HomeNav from "./components/HomeNav";

import './Register.css';

const apiUrl = "https://api.codewasabi.xyz";

import { useNavigate } from "react-router-dom";

function Register() {
    const navigate = useNavigate();
    
    function submitForm(event : React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        const emailElem = document.getElementById(
          "email"
        ) as HTMLInputElement;
        const passwordElem = document.getElementById("password") as HTMLInputElement;
        const nameElem = document.getElementById("name") as HTMLInputElement;
        const usernameElem = document.getElementById("username") as HTMLInputElement;
        const roleElem = document.getElementById("role") as HTMLInputElement;
        let email = emailElem.value;
        let password = passwordElem.value;
        let name = nameElem.value;
        let username = usernameElem.value;
        let role = roleElem.checked ? "teacher" : "student";
        if (email === "" || password === "") {
          alert("Please fill in all fields.");
          return;
        }
        if (password.length < 8) {
          alert("Password must be at least 8 characters long.");
          return;
        }
        if (name.length < 3) {
          alert("Name must be at least 3 characters long.");
            return;
        }
        if (username.length < 3) {
          alert("Username must be at least 3 characters long.");
          return;
        }
        if (emailElem.checkValidity() === false) {
          alert("Please enter a valid email address.");
          return;
        }
        const data = { email, password, name, username, role };
        console.log(apiUrl);
        fetch(apiUrl + "/users", {
            body: JSON.stringify(data),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            }
        }).then(() => {
            navigate("/login");
        })
        .catch((err) => {
          if(err){
            alert(err);
          }
          navigate
        });
    }

    return (
      <div>
        <HomeNav />
        <form className="Register" onSubmit={submitForm}>
          <h2>Create Account</h2>
          <label htmlFor="name">Name:</label>
          <input type="text" name="name" id="name" required />
          <label htmlFor="username">Username:</label>
          <input type="text" name="username" id="username" required />
          <label htmlFor="email">Email:</label>
          <input
            type="text"
            name="email"
            id="email"
            required
            pattern="[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
          />
          <label htmlFor="password">Password:</label>
          <input type="password" name="password" id="password" required />
          <br />
          <label htmlFor="role">
            I am a teacher:
            <input type="checkbox" name="role" id="role" className="isTeacher" />
          </label>
          <button type="submit" className="submit">
            Register
          </button>
        </form>
      </div>
    );
}

export default Register;
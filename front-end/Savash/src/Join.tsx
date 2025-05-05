import StudentNav from "./components/StudentNav";
import "./Join.css";

import { useNavigate } from "react-router-dom";
import { getToken } from "./types";

const apiUrl = "https://api.codewasabi.xyz";

function Join() {
  const navigate = useNavigate();

  function submitForm(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const codeElem = document.getElementById("code") as HTMLInputElement;
    let code = codeElem.value;
    if (code.length < 3) {
      alert("Name must be at least 3 characters long.");
      return;
    }

    const data = { code };
    console.log(apiUrl);
    fetch(apiUrl + "/classes/join", {
      body: JSON.stringify(data),
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "bearer " + getToken(document.cookie)
      },
    }).then(() => {
      navigate("/dashboard");
    });
  }

  return (
    <div>
      <StudentNav />
      <form className="Register" onSubmit={submitForm}>
        <h2>Join Class</h2>
        <label htmlFor="code">Code:</label>
        <input type="number" name="code" id="code" required />
        <button type="submit" className="submit">
          Join
        </button>
      </form>
    </div>
  );
}

export default Join;

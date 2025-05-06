
import TeacherNav from "./components/TeacherNav";
import "./CreateClass.css";

import { useNavigate } from "react-router-dom";

const apiUrl = "https://api.codewasabi.xyz"

import { getToken } from "./types.ts"

function CreateClass() {
    const navigate = useNavigate();

    function submitForm(event: React.FormEvent<HTMLFormElement>) {
      event.preventDefault();
      const nameElem = document.getElementById("name") as HTMLInputElement;
      let name = nameElem.value;
      if (name.length < 3) {
        alert("Name must be at least 3 characters long.");
        return;
      }
      
      const data = { name };
      console.log(apiUrl);
      fetch(apiUrl + "/classes", {
        body: JSON.stringify(data),
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "bearer " + getToken(document.cookie)
        },
      }).then(() => {
        navigate("/classes");
      });
    }

    return (
      <div>
        <TeacherNav />
        <form className="Register" onSubmit={submitForm}>
          <h2>Create Class</h2>
          <label htmlFor="name">Name:</label>
          <input type="text" name="name" id="name" required />
          <button type="submit" className="submit">
            Create
          </button>
        </form>
      </div>
    );
}

export default CreateClass;
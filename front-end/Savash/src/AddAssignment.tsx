import { useParams, Link, useNavigate } from "react-router-dom";
import TeacherNav from "./components/TeacherNav";
import { getToken } from "./types.ts";
import Slider from "./components/Slider.tsx";
import { useState } from "react";

const apiUrl = "https://api.codewasabi.xyz"

function AddAssignment() {
    let code = Number(useParams().id);

    const [selectedType, setSelectedType] = useState(0);

    if (!code || code < 0) {
      return (
        <>
          <h1>Cannot find class with id</h1>
          <Link to="/">Home</Link>
        </>
      );
    }

    const navigate = useNavigate();

    function submitForm(event: React.FormEvent<HTMLFormElement>) {
      event.preventDefault();
      const nameElem = document.getElementById("name") as HTMLInputElement;
      const dueElem = document.getElementById("due") as HTMLInputElement;
      const descElem = document.getElementById("desc") as HTMLInputElement;

      let name = nameElem.value;
      let due_date = new Date(dueElem.value);
      let description = descElem.value;

      let today = new Date();
      if (name.length < 3) {
        alert("Name must be at least 3 characters long.");
        return;
      }

      if (!due_date || due_date.getTime() < today.getTime()) {
        alert("Due date is invalid");
        return;
      }

      if(!description){
        description = "There is no information about this assignment.";
      }
      
      const data = { title: name, due_date, description };
      console.log(data);
      fetch(apiUrl + "/classes/" + code + "/assignments/", {
        body: JSON.stringify(data),
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "bearer " + getToken(document.cookie)
        },
      }).then(() => {
        navigate("/class/"+code);
      });
    }

    const sliderOptions = ["Written", "MCQ", "FRQ", "TFQ"]

    return (
      <div>
        <TeacherNav />
        <form className="Register" onSubmit={submitForm}>
          <h2>Create Assignment</h2>
          <label htmlFor="name">Name:</label>
          <input type="text" name="name" id="name" required />
          <label htmlFor="desc">Description:</label>
          <input type="text" name="desc" id="desc" />
          <label htmlFor="due"></label>
          <input type="date" id="due" required />
          <Slider options={sliderOptions} setSelectedType={setSelectedType} />
          <button type="submit" className="submit">
            Register
          </button>
        </form>
      </div>
    );
}

export default AddAssignment;
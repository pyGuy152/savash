import { useParams, Link, useNavigate } from "react-router-dom";
import TeacherNav from "./components/TeacherNav";
import { Assignment, getToken } from "./types.ts";
import Slider from "./components/Slider.tsx";
import {  useState } from "react";
import ConstructWritten from "./components/AssignmentContructing/ConstructWritten.tsx";

import "./AddAssignment.css"
import ConstructMCQ from "./components/AssignmentContructing/ConstructMCQ.tsx";
import ConstructFRQ from "./components/AssignmentContructing/ConstructFRQ.tsx";
import ConstructTFQ from "./components/AssignmentContructing/ConstructTFQ.tsx";

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

    const [assignmentData, setAssignmentData] = useState<Assignment>({
      points: 0,
      questions: [],
      choices: []
      });


    function submitForm() {
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
      
      let data : Assignment = { title: name, due_date, description, points: 0, created_at: new Date()};
      let type = "";

      switch(selectedType){
        case 0:
          data.points = assignmentData.points;
          type = "written";
          break;
        case 1:
          data.points = assignmentData.points;
          data.choices = assignmentData.choices;
          data.questions = assignmentData.questions;
          data.correct_answer = assignmentData.correct_answer;
          type = "mcq";
          break;
        case 2:
          data.points = assignmentData.points;
          data.questions = assignmentData.questions;
          type = "frq";
          break;
        case 3:
          data.points = assignmentData.points;
          data.questions = assignmentData.questions;
          data.correct_answer = assignmentData.correct_answer;
          type = "tfq";
          break;
      }
      
      console.log(data);
      fetch(apiUrl + "/classes/" + code + "/assignments/" + type + "/", {
        body: JSON.stringify(data),
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "bearer " + getToken(document.cookie)
        },
      }).catch((err) => {
        alert(err);
      }).then(() => {
        navigate("/class/"+code);
      });
    }

    
    const sliderOptions = ["Written", "MCQ", "FRQ", "TFQ"];
    const sliderElems = [
      <ConstructWritten
        setAssignmentData={setAssignmentData}
        assignmentData={assignmentData}
      />,
      <ConstructMCQ
        setAssignmentData={setAssignmentData}
        assignmentData={assignmentData}
      />,
      <ConstructFRQ
        setAssignmentData={setAssignmentData}
        assignmentData={assignmentData}
      />,
      <ConstructTFQ
        setAssignmentData={setAssignmentData}
        assignmentData={assignmentData}
      />,
    ];

    return (
      <div>
        <TeacherNav />
        <form className="Register" onSubmit={(e) => e.preventDefault()}>
          <h2>Create Assignment</h2>
          <label htmlFor="name">Name:</label>
          <input type="text" name="name" id="name" required />
          <label htmlFor="desc">Description:</label>
          <input type="text" name="desc" id="desc" />
          <label htmlFor="due"></label>
          <input type="datetime-local" id="due" required />
          <hr />
          <Slider options={sliderOptions} setSelectedType={setSelectedType} />
          {sliderElems[selectedType]}
          <button onClick={submitForm} type="submit" className="submit">
            Publish
          </button>
        </form>
      </div>
    );
}

export default AddAssignment; 
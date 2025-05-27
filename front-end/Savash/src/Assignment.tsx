
import { useRef, useState } from "react";
import { Assignment } from "./types.ts"

import "./Assignment.css"
import "./components/HomeNav.css"
import { Link, useParams } from "react-router-dom";

function AssignmentPage() {

    let [assignmentData] = useState<Assignment>({
      title: "Hello",
      points: 10,
      description: 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Blanditiis, numquam ad. Id et magnam molestias. Necessitatibus cum neque sequi dolorem dolores pariatur officiis consectetur! Eius quo quos facilis minima veritatis.',
        created_at: new Date(10000),
        due_date: new Date()

    });

    let classID = useParams().classid
    //let assignmentID = useParams().assignmentid;

    let modal = useRef<HTMLDialogElement>(null);

    function openModal(){
        modal.current!.showModal();
    }

    function closeModal(){
        modal.current!.close();
    }


    if(localStorage.getItem("role") === "teacher"){
        return (
          <>
            <dialog ref={modal} className="deleteModal">
              <h2>Are you sure you want to delete this assignment?</h2>
              <h3>This is permanent!</h3>
              <div className="row">
                <button onClick={closeModal}>Cancel</button>
                <button className="deleteButton">Delete</button>
              </div>
            </dialog>
            <nav className="HomeNav">
              <ul className="left">
                <li>
                  <Link to={`/class/${classID}/`}>
                    <img
                      src="/icons/chevron.png"
                      alt="Back"
                      className="rotate-90deg"
                    />{" "}
                    Back
                  </Link>
                </li>
              </ul>
              <ul className="center">
                <li>
                  <p className="class-title">{assignmentData.title}</p>
                </li>
              </ul>
              <ul className="right">
                <button onClick={openModal} className="deleteAssignment">
                  Delete
                </button>
              </ul>
            </nav>

            <div className="assignmentOverview">
              <div className="header">
                <div className="row">
                  <h1>{assignmentData.title}</h1>
                  <p>{assignmentData.points.toString()}/100 points</p>
                </div>
                <div className="row">
                  <p>Created: {assignmentData.created_at!.toLocaleDateString()}</p>
                  <p>Due By: {assignmentData.due_date!.toLocaleDateString()}</p>
                </div>
                <hr></hr>
              </div>
              <div className="content">
                <p>{assignmentData.description}</p>
              </div>
            </div>
          </>
        );
    }
    else{
    }
}

export default AssignmentPage;

import { useNavigate, useParams } from "react-router-dom";

import ClassNav from "./components/ClassNav";

const apiUrl = "https://api.codewasabi.xyz";

import { Assignment, Class, getToken, LOGOUT, Tab } from "./types.ts"
import { useEffect, useRef, useState } from "react";

import "./Register.css";
import InviteModal from "./components/InviteModal.tsx";

import "./Class.css"

import AssignmentList from "./components/AssignmentList.tsx"
import Tabs from "./components/Tabs.tsx";

function ClassComponent(){
    const navigate = useNavigate();
    const invite = useRef<HTMLDialogElement | null>(null);

    const [assignments, setAssignments] = useState<Assignment[]>([]);

    const classID = Number(useParams().id);
    const [classData, setClassData] = useState<Class>({
        name: "Loading",
        code: 0,
        created_at: new Date(),
      });

    function fetchClasses() {
        if(!classID || classID < 0){
            alert("classID not valid: " + classID);
        }
        fetch(apiUrl + "/classes", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "bearer " + getToken(document.cookie),
          },
        })
          .then((res) => res.json())
          .then((data) => {
            if (!data || data.length == 0) {
              alert("You aren't in any classes");
              if(localStorage.getItem("role") === "teacher"){
                navigate("/classes");
              }
              else{
                navigate("/dashboard")
              }
              return;
            }
            console.log(data);
            let dateParsed = data.find((classItem: Class) => classItem.code === classID);
            if(!dateParsed){
                alert("You are not in this class");
                navigate("/");
                return;
            }
            setClassData(dateParsed);
          })
          .catch((err) => {
            alert(err);
            LOGOUT();
            navigate("/");
            console.error(err);
          });
      }

      function fetchAssignments() {
        fetch(apiUrl + "/classes/assignments", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "bearer " + getToken(document.cookie),
          },
          body: JSON.stringify({
            code: classID
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (!data || !Array.isArray(data)) {
              return;
            }
            console.log(data);
            setAssignments(data);
          })
          .catch((err) => {
            alert(err);
            LOGOUT();
            navigate("/");
            console.error(err);
          });
      }

    useEffect(fetchClasses, []);
    useEffect(fetchAssignments, []);

    function inviteModalToggle() {
        if(invite){
            invite.current?.showModal();
        }
    }

    function closeInviteModal() {
        if(invite){
            invite.current?.close();
        }
    }

    const tabList : Tab[] = [{
      title: "Assignments",
      element: <AssignmentList list={assignments} />
    },
    {
      title: "People",
      element: <h1>Many people</h1>
    }
    ];

    return (
      <>
        <dialog className="inviteDialog" ref={invite}>
          <InviteModal code={classData.code} closeModal={closeInviteModal} />
        </dialog>
        <ClassNav
          classSelected={classData}
          inviteModalToggle={inviteModalToggle}
        />
        <main>
          <Tabs options={tabList}/>
        </main>
      </>
    );
}

export default ClassComponent;
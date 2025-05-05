
import "./Classes.css";

import { useEffect, useState } from "react";

const apiUrl = "https://api.codewasabi.xyz";

import { Class, LOGOUT, getToken } from "./types.ts";

import ClassList from "./ClassList.tsx"
import { useNavigate } from "react-router-dom";
import TeacherNav from "./components/TeacherNav.tsx";

function Classes() {
    let [classes, setClasses] = useState<Class[]>([]);
    const navigate = useNavigate();

    function fetchClasses() {
        fetch(apiUrl + "/classes", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "bearer " + getToken(document.cookie),
            }
        }).then((res) => res.json())
        .then((data) => {
            if(data == null){
                return;
            }
            console.log(data)
            let dateParsed = data.map((classItem : Class) => {
              return {
                ...classItem,
                created_at: new Date(classItem.created_at),
              };
            });
            setClasses(dateParsed);
        }).catch((err) => {
             alert(err);
            LOGOUT();
            navigate("/");
            console.error(err);
        });
    }

    useEffect(fetchClasses, []);

    return (
      <>
      <TeacherNav />
        <div className="classes">
          <h1>Classes</h1>
          <ClassList classes={classes} />
        </div>
      </>
    );
}

export default Classes;

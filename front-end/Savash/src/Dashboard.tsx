
import ClassList from "./ClassList";
import StudentNav from "./components/StudentNav"

import { Class, getToken, LOGOUT } from "./types.ts"
import { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom"

const apiUrl = "https://api.codewasabi.xyz";

import "./Dashboard.css"

function Dashboard() {

    let [classes, setClasses] = useState<Class[]>([]);
    const navigate = useNavigate();

    function fetchClasses() {
      fetch(apiUrl + "/classes", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "bearer " + getToken(document.cookie),
        },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data == null || !data.name) {
            return;
          }
          console.log(data);
          let dateParsed = data.map((classItem: Class) => {
            return {
              ...classItem,
              created_at: new Date(classItem.created_at),
            };
          });
          setClasses(dateParsed);
        })
        .catch((err) => {
          alert(err);
          LOGOUT();
          navigate("/");
          console.error(err);
        });
    }

    useEffect(fetchClasses, []);

    return (
        <>
        <StudentNav />
        <h1>Dashboard</h1>
        <ClassList classes={classes}/>
        </>
    )
}

export default Dashboard;

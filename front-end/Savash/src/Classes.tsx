import "./Classes.css";

import { useEffect, useState } from "react";

const apiUrl = "https://api.codewasabi.xyz";

import { Class, LOGOUT, getAllClasses, getToken } from "./types.ts";

import ClassList from "./components/ClassList.tsx";
//import { useNavigate } from "react-router-dom";
import TeacherNav from "./components/TeacherNav.tsx";

function Classes() {
  let [classes, setClasses] = useState<Class[]>([{
    name: "Loading",
    code: 0,
    created_at: new Date()
  }]);
  //const navigate = useNavigate();

  async function fetchClasses() {
    setClasses(await getAllClasses());
  }

  useEffect(() => {
    fetchClasses();
  }, []);

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

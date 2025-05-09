import ClassList from "./components/ClassList.tsx";
import StudentNav from "./components/StudentNav";

import { Class } from "./types.ts";
import { useState, useEffect } from "react";
//import { useNavigate } from "react-router-dom";

import { getAllClasses } from "./types.ts";

import "./Dashboard.css";

function Dashboard() {
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
      <StudentNav />
      <h1>Dashboard</h1>
      <ClassList classes={classes} />
    </>
  );
}

export default Dashboard;

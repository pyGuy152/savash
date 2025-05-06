import { Link } from "react-router-dom";
import { Class } from "../types.ts";

interface ClassListProps {
  classes: Class[];
}

function ClassList({ classes }: ClassListProps) {
  if(classes.length != 0 && classes[0].code == 0){
    return (
      <ul className="class-container">
        {Array.from({ length: 8 }).map((_, i) => (
          <li className="class loading" key={i} style={{width: Math.floor(Math.random() * 10 + 10) + "rem", animation: "load 1s infinite " + -i/5 + "s"}}>
            <div className="header">
              <h2></h2>
              <p></p>
            </div>
            <h2 className="code"></h2>
          </li>
        ))}
      </ul>
    );
  }
  return (
    <ul className="class-container">
      {classes.map((classItem) => (
        <Link to={"/class/" + classItem.code} key={classItem.code}>
          <li className="class">
            <div className="header">
              <h2>{classItem.name}</h2>
              <hr></hr>
              <p>{classItem.created_at.toLocaleDateString()}</p>
            </div>
            <h2 className="code">{classItem.code}</h2>
          </li>
        </Link>
      ))}
    </ul>
  );
}

export default ClassList;

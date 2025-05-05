 
import { Link } from "react-router-dom";
import { Class } from "./types.ts"

interface ClassListProps {
    classes : Class[]
}

function ClassList({classes} : ClassListProps) {
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
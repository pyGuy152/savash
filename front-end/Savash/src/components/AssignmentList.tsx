
import "./AssignmentList.css"

import { Assignment } from "../types.ts"

interface AssignmentListProps {
    list : Assignment[]
}


function AssignmentList({ list }:AssignmentListProps) {
    if(list.length == 0){
        return <h2 className="noAssignments">No assignments yet.</h2>;
    }
    return (
      <ul className="assignment-list">
        {list.map((row, i) => (
          <li key={i} className="row">
            <div className="left">
              <img src="/icons/paperclip.png"></img>
              <p>{row.title}</p>
            </div>
            <p>{row.due_date.toLocaleDateString()}</p>
          </li>
        ))}
      </ul>
    );
}

export default AssignmentList;
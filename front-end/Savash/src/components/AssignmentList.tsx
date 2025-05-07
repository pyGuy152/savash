
import "./AssignmentList.css"

import { Assignment } from "../types"

interface AssignmentListProps {
    list : Assignment[]
}


function AssignmentList({ list }:AssignmentListProps) {
    if(list.length == 0){
        return <h2 className="noAssignments">No assignments yet.</h2>;
    }
    return (
        <ul className="assignment-list">
            {
                list.map(row => (
                    <li className="row">
                        <img src="/icons/paperclip.png"></img>
                        <p>{row.title}</p>
                        <p>{row.due_date.toLocaleDateString()}</p>
                    </li>
                ))
            }
        </ul>
    )
}

export default AssignmentList;
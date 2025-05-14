import { Assignment } from "../../types";

interface ConstructMCQProps {
    setAssignmentData : Function;
    assignmentData : Assignment | undefined;
}

function ConstructMCQ({setAssignmentData, assignmentData} : ConstructMCQProps) {
    return (
      <div className="assignment-specific">
        <div className="questions">
            <div className="row">
                <h2>Questions</h2>
                <button className="add">Add</button>
            </div>
        </div>
        <label htmlFor="points">Assignment Weight:</label>
        <input type="number" />
      </div>
    );
}

export default ConstructMCQ;
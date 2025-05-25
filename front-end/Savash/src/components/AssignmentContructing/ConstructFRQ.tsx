import { Assignment } from "../../types.ts"

interface ConstructFRQProps {
    setAssignmentData: Function;
    assignmentData: Assignment | undefined;
}

function ConstructFRQ({
    setAssignmentData,
    assignmentData,
}: ConstructFRQProps){
    function pointsHandler(e: { target: { value: any } }) {
      setAssignmentData({ ...assignmentData, points: e.target.value });
    }
    return (
      <div className="assignment-specific">
        <label htmlFor="points">Assignment Weight (%):</label>
        <input onChange={pointsHandler} type="number" id="points" />
      </div>
    );
}

export default ConstructFRQ;
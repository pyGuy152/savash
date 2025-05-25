import { Assignment } from "../../types.ts";

interface ConstructWrittenProps {
  setAssignmentData: Function;
  assignmentData: Assignment | undefined;
}

function ConstructWritten({
  setAssignmentData,
  assignmentData,
}: ConstructWrittenProps) {
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

export default ConstructWritten;

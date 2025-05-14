import { Assignment } from "../../types";

interface ConstructWrittenProps {
  setAssignmentData: Function;
  assignmentData: Assignment | undefined;
}

function ConstructWritten({
  setAssignmentData,
  assignmentData,
}: ConstructWrittenProps) {
  return (
    <div className="assignment-specific">
      <label htmlFor="points">Assignment Weight:</label>
      <input
        onChange={(n) => setAssignmentData({...assignmentData, points:n})}
        type="number"
        id="points"
      />
    </div>
  );
}

export default ConstructWritten;

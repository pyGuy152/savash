import { Assignment } from "../../types";

interface ConstructMCQProps {
    setAssignmentData : Function;
    assignmentData : Assignment;
}

function ConstructMCQ({setAssignmentData, assignmentData} : ConstructMCQProps) {
  
  function pointsHandler(e: { target: { value: any } }){
    setAssignmentData({ ...assignmentData, points: e.target.value });
  }

  function addQuestion(){
    let ques = assignmentData.questions
    ques?.push("")
    setAssignmentData({
      ...assignmentData,
      questions: ques
    })
  }
  
  return (
    <div className="assignment-specific">
      <div className="questions">
        <div className="row">
          <h2>Questions</h2>
          <button onClick={addQuestion} className="add">
            Add
          </button>
        </div>
        {assignmentData.questions && assignmentData.questions.map((e, i) => (
          <div className="mcq">
            <h2 className="question">{e}</h2>
            <ol className="choices">
              {assignmentData.choices &&
                assignmentData.choices[i].map((a) => (
                  <li className="choice">{a}</li>
                ))}
            </ol>
          </div>
        ))}
      </div>
      <label htmlFor="points">Assignment Weight:</label>
      <input type="number" onChange={pointsHandler} />
    </div>
  );
}


export default ConstructMCQ;
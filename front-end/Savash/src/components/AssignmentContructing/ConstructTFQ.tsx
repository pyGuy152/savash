import { MouseEvent } from "react";
import { Assignment } from "../../types";

interface ConstructTFQProps {
  setAssignmentData: Function;
  assignmentData: Assignment;
}

function ConstructTFQ({
  setAssignmentData,
  assignmentData,
}: ConstructTFQProps) {
  function pointsHandler(e: { target: { value: any } }) {
    setAssignmentData({ ...assignmentData, points: e.target.value });
  }

  function makeCopy() {
    const choices: string[][] = assignmentData.choices
      ? assignmentData.choices.map((row) => [...row])
      : [];
    return choices;
  }

  function removeQuestion(e: MouseEvent<HTMLButtonElement>, i: number) {
    e.preventDefault();
    let questions = assignmentData.questions
      ? [...assignmentData.questions]
      : [];
    let choices = makeCopy();

    questions.splice(i, 1);
    choices.splice(i, 1);

    setAssignmentData({
      ...assignmentData,
      questions,
      choices,
    });
  }

  function addQuestion() {
    const questions = assignmentData.questions
      ? [...assignmentData.questions]
      : [];
    const choices = makeCopy();
    const copy = assignmentData.correct_answer
      ? [...assignmentData.correct_answer]
      : [];
    questions.push("");
    choices.push(["True", "False"]);
    copy.push("True");
    setAssignmentData({
      ...assignmentData,
      questions,
      choices,
      correct_answer: copy
    });
  }

  function makeRight(i: number, j: number){
    const copy = assignmentData.correct_answer ? [...assignmentData.correct_answer] : [];
    copy[i] = assignmentData.choices ? assignmentData.choices[i][j] : "Error";
    console.log(copy);
    setAssignmentData({
      ...assignmentData,
      correct_answer: copy
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
        {assignmentData.questions!.map((_, i) => (
          <div className="mcq" key={i}>
            <div className="question-header">
              <h2>{i + 1 + "."}</h2>
              <input
                type="text"
                placeholder="Question"
                value={
                  assignmentData.questions ? assignmentData.questions[i] : ""
                }
                onChange={(e) => {
                  const questions = assignmentData.questions
                    ? [...assignmentData.questions]
                    : [];
                  questions[i] = e.target.value;
                  setAssignmentData({
                    ...assignmentData,
                    questions,
                  });
                }}
              />
              <button
                type="button"
                className="delete"
                onClick={(e) => removeQuestion(e, i)}
              >
                X
              </button>
            </div>
            <ol className="choices">
              {assignmentData.choices &&
                assignmentData.choices[i].map((a, j) => (
                  <li className="choice" key={i + "-" + j}>
                    <p>{a}</p>
                    <input
                      onChange={() => makeRight(i, j)}
                      checked={
                        assignmentData.correct_answer && assignmentData.choices
                          ? assignmentData.correct_answer[i] ===
                            assignmentData.choices[i][j]
                          : false
                      }
                      type="checkbox"
                    ></input>
                  </li>
                ))}
            </ol>
          </div>
        ))}
      </div>
      <label htmlFor="points">Assignment Weight (%):</label>
      <input id="points" type="number" onChange={pointsHandler} />
    </div>
  );
}

export default ConstructTFQ;

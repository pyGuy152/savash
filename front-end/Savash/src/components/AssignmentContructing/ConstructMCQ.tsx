import { MouseEvent, ReactEventHandler } from "react";
import { Assignment } from "../../types";

interface ConstructMCQProps {
  setAssignmentData: Function;
  assignmentData: Assignment;
}

function ConstructMCQ({
  setAssignmentData,
  assignmentData,
}: ConstructMCQProps) {
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

  function changeChoice(
    e: React.ChangeEvent<HTMLInputElement>,
    i: number,
    j: number
  ) {
    let choices = makeCopy();
    choices[i][j] = e.target.value;

    setAssignmentData({
      ...assignmentData,
      choices,
    });
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
                    <input
                      type="text"
                      value={a}
                      onChange={(e) => changeChoice(e, i, j)}
                      placeholder={"choice " + (j + 1)}
                    />
                    <input type="checkbox"></input>
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

export default ConstructMCQ;


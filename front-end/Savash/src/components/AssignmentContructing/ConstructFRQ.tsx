

import { MouseEvent } from "react";
import { Assignment } from "../../types";

interface ConstructFRQProps {
  setAssignmentData: Function;
  assignmentData: Assignment;
}

function ConstructFRQ({ setAssignmentData, assignmentData }: ConstructFRQProps) {
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
    let questions = assignmentData ? [...assignmentData.questions!] : [];
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
    questions.push("");
    choices.push(["", "", "", ""]);
    setAssignmentData({
      ...assignmentData,
      questions,
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
          </div>
        ))}
        <label htmlFor="points">Assignment Weight (%):</label>
        <input onChange={pointsHandler} type="number" id="points" />
      </div>
    </div>
  );
}

export default ConstructFRQ;

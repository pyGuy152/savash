import { useState, useEffect, useRef } from "react";
import { apiUrl, getPeopleFromClass, getToken, Person } from "../types.ts";

interface PeopleListProp {
    classID : number;
}

function PeopleList({classID}: PeopleListProp) {

    const [people, setPeople] = useState<Person[]>([]);

    const [victim, setVictim] = useState<string>("rohanjain0725@gmail.com");

    const confirmDialog = useRef<HTMLDialogElement>(null);

    async function updatePeople(){
        let data = await getPeopleFromClass(classID);
        if(data){ 
            setPeople(data);
        }
        console.log(data);
    }

    useEffect(() => {
        updatePeople();
    }, [])

    function openDialog(email: string){
      confirmDialog.current!.show();
      setVictim(email);
    }

    function closeDialog(){
      confirmDialog.current!.close();
    }

    async function kickPerson(){
      fetch(apiUrl + "/classes/" + classID + "/remove/", {
        method: "POST",
        body: JSON.stringify({
          email: victim,
        }),
        headers: {
          Authorization: "bearer " + getToken(document.cookie)
        }
      });
    }

    if(people.length === 0 || !Array.isArray(people)){
        return <h1>Empty class?</h1>;
    }
    else{
        return (
          <>
            <dialog ref={confirmDialog} className="kick">
              <h1>Are you sure you wanna kick <span className="victim">{victim}</span>?</h1>
              <div className="row">
                <button onClick={closeDialog} className="no">No</button>
                <button onClick={kickPerson} className="yes">Yes</button>
              </div>
            </dialog>
            <ul className="people-list">
              {people.map((e, i) => (
                <li key={i} className="person-row">
                  <p className="left">
                    {e.name}
                    <span className="username">({e.username})</span>
                  </p>
                  <div className="middle">
                    <p>{e.email}</p>
                    <button onClick={() => openDialog(e.email)} className="kick">Kick</button>
                  </div>
                </li>
              ))}
            </ul>
          </>
        );
    }
}
export default PeopleList;

